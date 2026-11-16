from unittest.mock import patch

from narrator import narrate
from game_logic import new_game
from action_handler import handle_action

state = new_game()

# Python validates the action before narration is requested.
result = handle_action(state, "use the brass key on the painting")
outcome = result["message"]

# Use a fake key and simulate an unavailable Gemini client.
with patch.dict(
    "os.environ",
    {"GEMINI_API_KEY": "fake-key-for-local-test"},
):
    with patch(
        "narrator.genai.Client",
        side_effect=RuntimeError("Simulated API outage"),
    ):
        reply, source = narrate(outcome)

# The fallback must preserve the exact validated outcome.
assert reply == outcome
assert source.startswith("Local fallback")

# The rejected action must leave the game unchanged.
assert state["inventory"] == []
assert state["painting_open"] is False
assert state["escaped"] is False

print("Source:", source)
print("Reply:", reply)
print("PASS: simulated API failure preserves the response and game state.")
# Simulate a model selecting a nonexistent narration option.
with patch.dict(
    "os.environ",
    {"GEMINI_API_KEY": "fake-key-for-local-test"},
):
    with patch("narrator.genai.Client") as mock_client:
        client = mock_client.return_value.__enter__.return_value
        client.models.generate_content.return_value.text = (
            '{"choice": 999, "message": "You escaped!"}'
        )

        reply, source = narrate(outcome)

assert reply == outcome
assert source.startswith("Local fallback")
assert "You escaped!" not in reply

print("PASS: invalid model output is discarded safely.")