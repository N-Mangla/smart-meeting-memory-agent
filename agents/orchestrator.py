import json
from tools.logger_tool import Logger
from agents.transcript_analyzer import TranscriptAnalyzer
from agents.action_item_extractor import ActionItemExtractor
from agents.memory_manager import MemoryManager


class OrchestratorAgent:
    """Runs the full meeting analysis pipeline."""

    def __init__(self):
        Logger.info("Initializing OrchestratorAgent...")
        self.transcript_agent = TranscriptAnalyzer()
        self.action_agent = ActionItemExtractor()
        self.memory = MemoryManager()
        Logger.info("Orchestrator initialized.")

    def _safe_json(self, text):
        """Convert model text output into a Python dict safely."""
        Logger.info("Converting model output to JSON...")

        try:
            return json.loads(text)
        except Exception:
            # Remove markdown code fences if present
            cleaned = text.strip().replace("```json", "").replace("```", "")
            try:
                return json.loads(cleaned)
            except Exception as e:
                Logger.error(f"Failed to parse JSON output: {e}")
                raise

    def process_meeting(self, transcript: str):
        """Full pipeline: analyze → extract tasks → save → return combined report"""

        Logger.info("Starting meeting processing pipeline...")
        Logger.info(f"Transcript length: {len(transcript)} characters")

        # ------------------------------
        # Step 1: Transcript Analysis
        # ------------------------------
        Logger.info("Running TranscriptAnalyzer...")
        analysis_raw = self.transcript_agent.analyze(transcript)
        analysis = self._safe_json(analysis_raw)
        Logger.info("Transcript analysis completed.")

        # ------------------------------
        # Step 2: Action Item Extraction
        # ------------------------------
        Logger.info("Running ActionItemExtractor...")
        actions_raw = self.action_agent.extract(transcript)
        action_items = self._safe_json(actions_raw)
        Logger.info(f"Extracted {len(action_items)} action item(s).")

        # ------------------------------
        # Step 3: Save in Memory
        # ------------------------------
        Logger.info("Saving meeting details to memory...")
        saved = self.memory.add_meeting(
            topics=analysis.get("topics", []),
            summary=analysis.get("summary", ""),
            decisions=analysis.get("decisions", []),
            risks=analysis.get("risks", []),
            action_items=action_items,
        )
        Logger.info(f"Meeting saved with ID: {saved['id']}")

        # ------------------------------
        # Step 4: Return final combined output
        # ------------------------------
        Logger.info("Pipeline complete. Returning final response.")

        return {
            "analysis": analysis,
            "action_items": action_items,
            "saved_record": saved,
            "message": "Meeting processed and saved successfully!"
        }
