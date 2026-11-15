def new_game():
    """Return a fresh, independent game state."""
    return {
        "available_objects": [
            "desk",
            "bookshelf",
            "drawer",
            "painting",
            "door",
        ],
        "inventory": [],
        "examined_objects": [],
        "solved_puzzles": [],
        "drawer_open": False,
        "painting_open": False,
        "escaped": False,
    }


def use_key_on_painting(state):
    """Python checks possession before allowing the action."""
    if "brass key" not in state["inventory"]:
        return {
            "success": False,
            "message": (
                "You do not have the brass key. "
                "Find and collect it before using it."
            ),
        }

    if state["painting_open"]:
        return {
            "success": False,
            "message": "The painting is already unlocked.",
        }

    state["painting_open"] = True
    state["solved_puzzles"].append("painting")

    return {
        "success": True,
        "message": (
            "The painting opens. Behind it, a message reads: "
            "Night, dusk, noon, dawn."
        ),
    }
DRAWER_CODE = "3142"


def open_drawer(state, code):
    if state["drawer_open"]:
        return {
            "success": False,
            "message": "The drawer is already open.",
        }

    if code != DRAWER_CODE:
        return {
            "success": False,
            "message": "Incorrect code. The drawer remains locked.",
        }

    state["drawer_open"] = True
    state["solved_puzzles"].append("drawer")

    return {
        "success": True,
        "message": (
            "The drawer opens, revealing a brass key. "
            "You must collect it before using it."
        ),
    }


def collect_key(state):
    if not state["drawer_open"]:
        return {
            "success": False,
            "message": "The drawer is locked. No key is available.",
        }

    if "brass key" in state["inventory"]:
        return {
            "success": False,
            "message": "You already have the brass key.",
        }

    state["inventory"].append("brass key")

    return {
        "success": True,
        "message": "You collect the brass key.",
    }
EXIT_CODE = "2413"


def unlock_exit(state, code):
    if state["escaped"]:
        return {
            "success": False,
            "message": "You have already escaped.",
        }

    prerequisites_complete = (
        state["drawer_open"]
        and "brass key" in state["inventory"]
        and state["painting_open"]
    )

    if not prerequisites_complete:
        return {
            "success": False,
            "message": (
                "The exit remains locked. You must open the drawer, "
                "collect the key, and unlock the painting first."
            ),
        }

    if code != EXIT_CODE:
        return {
            "success": False,
            "message": "Incorrect exit code. The door remains locked.",
        }

    state["escaped"] = True
    state["solved_puzzles"].append("exit")

    return {
        "success": True,
        "message": "The door opens. You escaped the library!",
    }