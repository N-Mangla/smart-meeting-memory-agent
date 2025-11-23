import os
import requests
from dotenv import load_dotenv
from tools.logger_tool import Logger

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    Logger.error("GEMINI_API_KEY missing in .env")
    raise RuntimeError("GEMINI_API_KEY missing in .env")


# ------------------------------
# Internal REST caller
# ------------------------------
def call_gemini(prompt: str, model: str = "models/gemini-2.5-flash") -> str:
    Logger.info(f"call_gemini() → Using model: {model}")

    url = f"https://generativelanguage.googleapis.com/v1/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
    except Exception as e:
        Logger.error(f"Network error while calling Gemini: {e}")
        raise

    # Fallback to Pro if Flash not available
    if response.status_code == 404:
        Logger.warn(f"{model} unavailable → switching to gemini-2.5-pro")
        return call_gemini(prompt, model="models/gemini-2.5-pro")

    try:
        response.raise_for_status()
    except Exception as e:
        Logger.error(f"Gemini API error: {e}")
        raise

    data = response.json()
    Logger.log_json("Gemini Raw Response", data)

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        Logger.info("Successfully extracted model text.")
        return text
    except Exception as e:
        Logger.error(f"Unexpected response format: {e}")
        raise


# ------------------------------
# Agent 2: Action Item Extractor
# ------------------------------
class ActionItemExtractor:
    def extract(self, text: str) -> str:
        Logger.info("ActionItemExtractor started.")
        Logger.info(f"Input text length: {len(text)} characters")

        prompt = f"""
        You are an AI Action Item Extractor for meetings.

        From the following text, identify all action items.

        For each action:
        - "task": what needs to be done
        - "owner": who will do it ("" if unclear)
        - "due_date": natural language date ("" if not mentioned)
        - "priority": High / Medium / Low
        - "status": always "pending"

        Return ONLY valid JSON. No markdown.

        Text:
        \"\"\"
        {text}
        \"\"\"
        """

        Logger.info("Sending request to Gemini...")
        result = call_gemini(prompt)
        Logger.info("ActionItemExtractor finished processing.")

        return result


# Debug run
if __name__ == "__main__":
    Logger.info("Debug run for ActionItemExtractor...")

    sample_text = """
    Alice will finish the client report by Tuesday.
    Bob must prepare the slides for the Friday presentation.
    Neha will update the API documentation before Monday.
    We discussed redesigning the dashboard but did not assign an owner.
    """

    extractor = ActionItemExtractor()
    print(extractor.extract(sample_text))
