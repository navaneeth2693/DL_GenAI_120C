import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).with_name(".env"))
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Missing GEMINI_API_KEY in .env")
else:
    started = time.monotonic()

    try:
        print("Testing a small JSON response...", flush=True)

        with genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=60_000,
                retry_options=types.HttpRetryOptions(attempts=1),
            ),
        ) as client:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents="Say hello. Set escaped to false.",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "message": {"type": "STRING"},
                            "escaped": {"type": "BOOLEAN"},
                        },
                        "required": ["message", "escaped"],
                    },
                    thinking_config=types.ThinkingConfig(
                        thinking_level="LOW",
                    ),
                ),
            )

        print("Response:", response.text)

    except Exception as error:
        print("Error type:", type(error).__name__)
        print("Details:", str(error).replace(api_key, "[REDACTED]"))

    finally:
        elapsed = time.monotonic() - started
        print(f"Elapsed time: {elapsed:.1f} seconds")