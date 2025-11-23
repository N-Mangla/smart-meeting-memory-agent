import os
import json
from datetime import datetime
from tools.logger_tool import Logger

MEMORY_FILE = "meeting_memory.json"


class MemoryManager:
    """
    Stores and retrieves long-term memory from all meetings.
    """

    def __init__(self):
        Logger.info("Initializing MemoryManager...")

        # Create memory file if not exists
        if not os.path.exists(MEMORY_FILE):
            Logger.warn(f"{MEMORY_FILE} not found. Creating new file.")
            with open(MEMORY_FILE, "w") as f:
                json.dump({"meetings": []}, f, indent=4)
        else:
            Logger.info("Memory file found.")

    def load_memory(self):
        Logger.info("Loading memory from file...")
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                Logger.info("Successfully loaded meeting memory.")
                return data
        except Exception as e:
            Logger.error(f"Error loading memory: {e}")
            raise

    def save_memory(self, data):
        Logger.info("Saving memory to file...")
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump(data, f, indent=4)
            Logger.info("Memory saved.")
        except Exception as e:
            Logger.error(f"Error saving memory: {e}")
            raise

    def add_meeting(self, topics, summary, decisions, risks, action_items):
        Logger.info("Adding new meeting record...")

        memory = self.load_memory()

        entry = {
            "id": datetime.now().strftime("%Y%m%d-%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "topics": topics,
            "summary": summary,
            "decisions": decisions,
            "risks": risks,
            "action_items": action_items
        }

        memory["meetings"].append(entry)
        self.save_memory(memory)

        Logger.info(f"Meeting saved with ID: {entry['id']}")
        return entry

    def get_all_meetings(self):
        Logger.info("Fetching all meetings...")
        memory = self.load_memory()
        return memory["meetings"]

    def get_last_meeting(self):
        Logger.info("Fetching last meeting...")
        memory = self.load_memory()

        if memory["meetings"]:
            Logger.info("Last meeting retrieved.")
            return memory["meetings"][-1]

        Logger.warn("No meetings found.")
        return None

    def search_action_items(self, keyword):
        Logger.info(f"Searching action items for keyword: '{keyword}'")

        memory = self.load_memory()
        results = []

        for meeting in memory["meetings"]:
            for item in meeting["action_items"]:
                if keyword.lower() in item["task"].lower():
                    results.append(item)

        Logger.info(f"Search completed. Found {len(results)} item(s).")
        return results
