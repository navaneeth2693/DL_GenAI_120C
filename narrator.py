import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).with_name(".env"))


def narrate(outcome):
    """Return a safe description and its source."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return outcome, "Local fallback: API key missing"

    # Every option preserves the exact Python-approved outcome.
    choices = [
        outcome,
        "In the quiet library, you pause. " + outcome,
        "You take a steady breath. " + outcome,
    ]

    try:
        with genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=20_000,
                retry_options=types.HttpRetryOptions(attempts=1),
            ),
        ) as client:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=(
                    "Choose one approved escape-room narration. "
                    "Return its index: 0, 1, or 2.\n"
                    + json.dumps(choices)
                ),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "choice": {"type": "INTEGER"},
                        },
                        "required": ["choice"],
                    },
                    thinking_config=types.ThinkingConfig(
                        thinking_level="LOW",
                    ),
                ),
            )

        result = json.loads(response.text or "{}")

        if not isinstance(result, dict):
            raise ValueError("Invalid response format")

        index = result.get("choice")

        if type(index) is not int or index not in range(len(choices)):
            raise ValueError("Invalid narration selection")

        # Display our approved text, never arbitrary model output.
        return choices[index], "Gemini-selected narration"

    except Exception:
        return outcome, "Local fallback: Gemini unavailable or invalid reply"