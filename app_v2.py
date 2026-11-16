import streamlit as st

from game_logic import new_game
from action_handler import handle_action
from narrator import narrate

st.set_page_config(
    page_title="AI Escape Room — Version 2",
    page_icon="🔑",
)

st.title("AI Escape Room — Version 2")
st.caption("Python-controlled game state and action validation")
st.caption("Python validates actions; Gemini selects approved narration.")

# Keep game state separate from the displayed conversation.
if "v2_state" not in st.session_state:
    st.session_state.v2_state = new_game()

if "v2_messages" not in st.session_state:
    st.session_state.v2_messages = []

if st.button("Restart game"):
    st.session_state.v2_state = new_game()
    st.session_state.v2_messages = []
    st.session_state.pop("v2_narration_source", None)
    st.rerun()

state = st.session_state.v2_state

st.info(
    "You wake inside a locked library. You see a desk, "
    "a bookshelf, a locked drawer, a painting, and an exit door. "
    "Investigate objects and solve the puzzles to escape."
)

with st.sidebar:
    st.header("Game progress")

    st.subheader("Inventory")
    if state["inventory"]:
        for item in state["inventory"]:
            st.write(f"- {item}")
    else:
        st.write("Empty")

    st.write("Drawer:", "Open" if state["drawer_open"] else "Locked")
    st.write(
        "Painting:",
        "Unlocked" if state["painting_open"] else "Locked",
    )
    st.write("Exit:", "Open" if state["escaped"] else "Locked")

with st.expander("How to play"):
    st.write("Enter one action at a time. Examples:")
    st.code(
        "examine the desk\n"
        "inspect the bookshelf\n"
        "open the drawer with code 1234\n"
        "collect the brass key\n"
        "use the brass key on the painting\n"
        "unlock the door with code 1234\n"
        "check my inventory"
    )
    st.write("1234 is only an example. Discover the real codes.")

for message in st.session_state.v2_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if state["escaped"]:
    st.success("You escaped the library!")

player_action = st.chat_input(
    "What would you like to do?",
    disabled=state["escaped"],
    max_chars=600,
)

if player_action:
    # Python determines the outcome and updates state.
    result = handle_action(state, player_action)

    # Gemini can select narration, but cannot change the outcome.
    with st.spinner("Preparing the Game Master's response..."):
        reply, source = narrate(result["message"])

    st.session_state.v2_messages.extend(
        [
            {"role": "user", "content": player_action},
            {"role": "assistant", "content": reply},
        ]
    )

    st.session_state.v2_narration_source = source
    st.rerun()

if "v2_narration_source" in st.session_state:
    st.caption(st.session_state.v2_narration_source)
with st.expander("Inspect Python game state"):
    st.json(state)