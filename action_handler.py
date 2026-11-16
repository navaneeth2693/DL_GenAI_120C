import re

from game_logic import (
    open_drawer,
    collect_key,
    use_key_on_painting,
    unlock_exit,
)


def examine_object(state, target):
    """Reveal only the information currently available."""
    if target not in state["available_objects"]:
        return {
            "success": False,
            "message": "That object is not in this room.",
        }

    if target not in state["examined_objects"]:
        state["examined_objects"].append(target)

    descriptions = {
        "desk": (
            "A note reads: "
            "'The shelf keeps time: dawn, noon, dusk, night.'"
        ),
        "bookshelf": (
            "Four books have numbered spines: "
            "Dawn = 3, Noon = 1, Dusk = 4, Night = 2."
        ),
        "door": "The exit door has a four-digit keypad.",
    }

    if target == "drawer":
        if not state["drawer_open"]:
            message = "The drawer is locked with a four-digit code."
        elif "brass key" in state["inventory"]:
            message = "The drawer is open and empty."
        else:
            message = "The open drawer contains a brass key."

    elif target == "painting":
        if state["painting_open"]:
            message = (
                "Behind the painting, a message reads: "
                "Night, dusk, noon, dawn."
            )
        else:
            message = "The painting's frame has a brass keyhole."

    else:
        message = descriptions[target]

    return {"success": True, "message": message}


def handle_action(state, player_text):
    """Recognize one complete action without trusting player claims."""
    text = player_text.strip().lower()

    if not text or len(text) > 600:
        return {
            "success": False,
            "message": "Enter an action between 1 and 600 characters.",
        }

    text = text.rstrip(".!?")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(
        r"^(?:please |i want to |i would like to )",
        "",
        text,
    )

    if state["escaped"]:
        return {
            "success": False,
            "message": "You already escaped. Restart to play again.",
        }

    if text in ("inventory", "check my inventory", "show inventory"):
        items = ", ".join(state["inventory"]) or "empty"
        return {"success": True, "message": f"Inventory: {items}."}

    match = re.fullmatch(
        r"(?:examine|inspect|look at|investigate) (?:the )?(.+)",
        text,
    )
    if match:
        return examine_object(state, match.group(1))

    match = re.fullmatch(
        r"(?:open|unlock) (?:the )?drawer "
        r"(?:with|using) (?:code )?([0-9]{4})",
        text,
    )
    if match:
        return open_drawer(state, match.group(1))

    if re.fullmatch(
        r"(?:collect|take|pick up) (?:the )?(?:brass )?key",
        text,
    ):
        return collect_key(state)

    if re.fullmatch(
        r"use (?:the )?(?:brass )?key on (?:the )?painting",
        text,
    ):
        return use_key_on_painting(state)

    match = re.fullmatch(
        r"(?:open|unlock) (?:the )?(?:door|exit) "
        r"(?:with|using) (?:code )?([0-9]{4})",
        text,
    )
    if match:
        return unlock_exit(state, match.group(1))

    return {
        "success": False,
        "message": (
            "That action is not supported. Try one action at a time: "
            "'examine the desk', 'collect the brass key', "
            "or 'open the drawer with code 1234'. "
            "Use the actual code you discover."
        ),
    }