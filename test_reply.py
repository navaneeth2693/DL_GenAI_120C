import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).with_name(".env"))
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Missing GEMINI_API_KEY in .env")
else:
    try:
        with genai.Client(api_key=api_key) as client:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=(
                    "Welcome the player to a locked library "
                    "in two short sentences."
                ),
            )

        print(response.text or "The model returned no text.")

    except Exception as error:
        print("Generation failed.")
        print("Error type:", type(error).__name__)
        print("Error code:", getattr(error, "code", "Not available"))
        details = str(error).replace(api_key, "[REDACTED]")
        print("Details:", details)