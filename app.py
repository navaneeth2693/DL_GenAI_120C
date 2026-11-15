import streamlit as st

st.set_page_config(
    page_title="AI Escape Room",
    page_icon="🔑"
)

st.title("AI Escape Room")
st.write("Welcome to the Locked Library!")

st.info(
    "You wake up inside a locked library. "
    "You see a desk, a bookshelf, a painting, "
    "a locked drawer, and an exit door."
)

st.write("Explore the room, find clues, and solve puzzles to escape.")

# Keep messages when Streamlit reruns the page.
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Restart game"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept a new player action.
player_action = st.chat_input("What would you like to do?")

if player_action:
    st.session_state.messages.append(
        {"role": "user", "content": player_action}
    )

    # Temporary response; Gemini will replace this later.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                f"You tried: {player_action}\n\n"
                "The AI Game Master is not connected yet."
            ),
        }
    )

    st.rerun()