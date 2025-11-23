import datetime
import json
import os

LOG_FILE = "agent_logs.log"

class Logger:
    @staticmethod
    def _write(message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")

    @staticmethod
    def info(msg: str):
        Logger._write(f"INFO: {msg}")

    @staticmethod
    def warn(msg: str):
        Logger._write(f"WARNING: {msg}")

    @staticmethod
    def error(msg: str):
        Logger._write(f"ERROR: {msg}")

    @staticmethod
    def log_json(title: str, obj: dict):
        Logger._write(f"{title}: {json.dumps(obj, indent=2)}")
