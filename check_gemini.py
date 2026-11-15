import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load .env from the same folder as this script.
load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key missing. Check GEMINI_API_KEY in your .env file.")
else:
    try:
        with genai.Client(api_key=api_key) as client:
            models = list(client.models.list())

        print("Connected successfully!")
        print("Models supporting content generation:")

        for model in models:
            if "generateContent" in (model.supported_actions or []):
                print(model.name)

    except Exception as error:
        print("Connection failed.")
        print("Error type:", type(error).__name__)
        print("Error code:", getattr(error, "code", "Not available"))