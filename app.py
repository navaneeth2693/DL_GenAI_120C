import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Read the API key without putting it in the source code.
load_dotenv(Path(__file__).with_name(".env"))
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="AI Escape Room", page_icon="🔑")
st.title("AI Escape Room — Version 1")
st.caption("The Locked Library")

if not api_key:
    st.error("Add GEMINI_API_KEY to your .env file.")
    st.stop()

# In Version 1, Gemini is responsible for enforcing these rules.
SYSTEM_PROMPT = """
You are the Game Master of a locked-library escape room.
Use the conversation history to remember the player's progress.
Give short, atmospheric responses and allow natural-language actions.

The room contains exactly five main interactive objects:
a desk, a bookshelf, a locked drawer, a painting, and an exit door.

Puzzle design:
1. Examining the desk reveals a note:
   "The shelf keeps time: dawn, noon, dusk, night."
2. Examining the bookshelf reveals four numbered books:
   Dawn = 3, Noon = 1, Dusk = 4, Night = 2.
   The drawer combination is 3142.
3. Entering 3142 opens the drawer and reveals a brass key.
   The player must explicitly collect the key before using it.
4. The painting's frame has a keyhole.
   Using the collected brass key unlocks the painting and reveals:
   "Night, dusk, noon, dawn."
5. This reversed book order gives the exit code 2413.
   The door opens only after the drawer has been opened,
   the key collected, the painting unlocked, and 2413 entered.

Rules:
- Start with no collected items and all locks closed.
- Reveal each clue only when the relevant object is investigated.
- Never invent extra objects or alternate escape routes.
- Incorrect combinations must not open locks.
- If the player requests a hint, guide them without revealing answers.
- Remember collected items and completed puzzles.
- Set escaped to true only when the exit is legitimately unlocked.
- Otherwise, escaped must be false.

Return JSON containing:
message: your response to the player
escaped: a boolean
"""

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "message": {"type": "STRING"},
        "escaped": {"type": "BOOLEAN"},
    },
    "required": ["message", "escaped"],
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "escaped" not in st.session_state:
    st.session_state.escaped = False

if st.button("Restart game"):
    st.session_state.messages = []
    st.session_state.escaped = False
    st.rerun()

st.info(
    "You wake inside a locked library. You see a desk, a bookshelf, "
    "a locked drawer, a painting, and an exit door. "
    "Find clues and solve the puzzles to escape."
)

st.write(
    "Try: 'examine the desk', 'inspect the bookshelf', "
    "'check my inventory', or 'give me a hint'."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.escaped:
    st.success("You escaped the library!")

player_action = st.chat_input(
    "What would you like to do?",
    disabled=st.session_state.escaped,
    max_chars=600,
)

if player_action:
    # Send previous messages so Gemini can remember the game.
    conversation = st.session_state.messages + [
        {"role": "user", "content": player_action}
    ]

    contents = [
        types.Content(
            role="model" if item["role"] == "assistant" else "user",
            parts=[types.Part(text=item["content"])],
        )
        for item in conversation
    ]

    try:
        with st.spinner("The Game Master is thinking..."):
            with genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(
                    timeout=120_000,
                    retry_options=types.HttpRetryOptions(attempts=1),
                ),
            ) as client:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=contents,
                                        config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=RESPONSE_SCHEMA,
                        thinking_config=types.ThinkingConfig(
                            thinking_level="LOW",
                        ),
                    ),
                )

            result = json.loads(response.text or "{}")

            if not isinstance(result, dict):
                raise ValueError("Invalid response format")

            if not isinstance(result.get("message"), str):
                raise ValueError("Missing game message")

            if type(result.get("escaped")) is not bool:
                raise ValueError("Missing completion status")

        # Save the turn only after a valid response arrives.
        st.session_state.messages = conversation + [
            {"role": "assistant", "content": result["message"]}
        ]
        st.session_state.escaped = result["escaped"]
        st.rerun()

    except Exception as error:
        st.error("Could not complete this turn. Please try again.")
        st.caption(
            f"Error: {type(error).__name__} | "
            f"Code: {getattr(error, 'code', 'Not available')}"
        )