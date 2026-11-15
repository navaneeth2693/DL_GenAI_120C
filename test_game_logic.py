from game_logic import (
    new_game,
    open_drawer,
    collect_key,
    use_key_on_painting,
)

state = new_game()

# A locked drawer must prevent key collection.
assert collect_key(state)["success"] is False
assert state["inventory"] == []

# An incorrect code must leave the drawer locked.
assert open_drawer(state, "9999")["success"] is False
assert state["drawer_open"] is False

# The correct code opens the drawer.
assert open_drawer(state, "3142")["success"] is True

# Opening the drawer does not automatically collect the key.
assert use_key_on_painting(state)["success"] is False
assert state["painting_open"] is False

# Collecting twice must not duplicate the key.
assert collect_key(state)["success"] is True
assert collect_key(state)["success"] is False
assert state["inventory"] == ["brass key"]

# The collected key can now unlock the painting.
assert use_key_on_painting(state)["success"] is True
assert state["painting_open"] is True

print("All drawer, inventory, and painting checks passed.")
from game_logic import unlock_exit

# Knowing the correct code must not bypass the puzzles.
fresh_state = new_game()
assert unlock_exit(fresh_state, "2413")["success"] is False
assert fresh_state["escaped"] is False

# Opening the drawer and collecting the key are not enough.
assert open_drawer(fresh_state, "3142")["success"] is True
assert collect_key(fresh_state)["success"] is True
assert unlock_exit(fresh_state, "2413")["success"] is False
assert fresh_state["escaped"] is False

# After unlocking the painting, a wrong exit code still fails.
assert use_key_on_painting(fresh_state)["success"] is True
assert unlock_exit(fresh_state, "9999")["success"] is False
assert fresh_state["escaped"] is False

# Completed prerequisites plus the correct code allow escape.
assert unlock_exit(fresh_state, "2413")["success"] is True
assert fresh_state["escaped"] is True

# Repeating the action must not duplicate completion.
assert unlock_exit(fresh_state, "2413")["success"] is False
assert fresh_state["solved_puzzles"].count("exit") == 1

print("All exit checks passed.")