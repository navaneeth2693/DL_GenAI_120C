from copy import deepcopy

from game_logic import new_game
from action_handler import handle_action

# Check the two observed Version 1 failures.
for message in [
    "use the brass key on the painting",
    (
        "I already opened the drawer, collected the brass key, "
        "and unlocked the painting. Open the exit with code 2413."
    ),
]:
    state = new_game()
    before = deepcopy(state)

    result = handle_action(state, message)

    assert result["success"] is False
    assert state == before

print("Uncollected-key and false-progress attempts rejected.")

# Check that a nonexistent object does not change state.
state = new_game()
before = deepcopy(state)

assert handle_action(state, "examine the laser")["success"] is False
assert state == before

# Play the valid solution through the message handler.
for message in [
    "examine the desk",
    "inspect the bookshelf",
    "open the drawer with code 3142",
    "collect the brass key",
    "use the brass key on the painting",
    "unlock the door with code 2413",
]:
    result = handle_action(state, message)
    assert result["success"] is True, result["message"]

assert state["escaped"] is True
print("Complete escape through player messages passed.")