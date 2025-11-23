import os
import requests
from dotenv import load_dotenv
from tools.logger_tool import Logger


# -------------------------------------------------------
# Load API Key
# -------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    Logger.error("GEMINI_API_KEY missing in .env")
    raise RuntimeError("GEMINI_API_KEY missing in .env")

Logger.info("Gemini API Key loaded successfully.")


# -------------------------------------------------------
# Internal REST caller with logging
# -------------------------------------------------------
def call_gemini(prompt: str, model: str = "models/gemini-2.5-flash") -> str:
    """
    Sends a prompt to Gemini over REST and returns the text output.
    Automatically falls back to gemini-2.5-pro if flash is unavailable.
    """

    Logger.info(f"call_gemini() → Model selected: {model}")
    Logger.info("Sending request to Gemini API...")

    url = f"https://generativelanguage.googleapis.com/v1/{model}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
    except Exception as e:
        Logger.error(f"Network error while contacting Gemini: {e}")
        raise

    # Fallback if flash unavailable
    if response.status_code == 404:
        Logger.warn(f"{model} returned 404 — switching to gemini-2.5-pro")

        if model != "models/gemini-2.5-pro":
            return call_gemini(prompt, model="models/gemini-2.5-pro")

    try:
        response.raise_for_status()
    except Exception as e:
        Logger.error(f"Gemini API returned an error: {str(e)}")
        raise

    data = response.json()

    # Log the full JSON response from Gemini
    Logger.log_json("Gemini Raw Response", data)

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        Logger.info("Successfully extracted text from Gemini response.")
        return text
    except Exception as e:
        Logger.error(f"Unexpected Gemini response format: {e}")
        raise


# -------------------------------------------------------
# Transcript Analyzer Agent with logging
# -------------------------------------------------------
class TranscriptAnalyzer:
    """
    Agent 1:
    Reads raw meeting text and extracts:
    - Key topics
    - Major decisions
    - Discussion summary
    """

    def analyze(self, transcript: str) -> dict:
        Logger.info("TranscriptAnalyzer started processing transcript.")
        Logger.info(f"Transcript length: {len(transcript)} characters")

        prompt = f"""
        You are an AI Meeting Transcript Analyzer.

        Extract the following from the transcript:
        1. Key topics (3-6 bullet points)
        2. Summary (4- 6 lines)
        3. Decisions taken (if any)
        4. Risks or concerns (if any)

        Return output as valid JSON ONLY in this structure:

        {{
        "topics": [...],
        "summary": "...",
        "decisions": [...],
        "risks": [...]
        }}

        Transcript:
        \"\"\"
        {transcript}
        \"\"\"
        """

        Logger.info("Sending transcript to Gemini for analysis...")

        raw_output = call_gemini(prompt)

        Logger.info("TranscriptAnalyzer received response from Gemini.")
        Logger.info("Returning raw JSON output from Gemini.")

        return raw_output


# -------------------------------------------------------
# Debug run
# -------------------------------------------------------
if __name__ == "__main__":
    sample_transcript = """
    Alice will finish the client report by Tuesday.
    Bob will prepare slides for the Friday presentation.
    The team discussed API integrations and next sprint planning.
    """

    Logger.info("Running TranscriptAnalyzer debug mode...")
    analyzer = TranscriptAnalyzer()
    print(analyzer.analyze(sample_transcript))
