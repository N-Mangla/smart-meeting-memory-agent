# Smart Meeting Memory Agent

A lightweight multi-agent system that analyzes meeting transcripts, extracts action items, and stores long-term meeting memory.  
This project was built as part of the Google AI Agents Intensive program using Gemini 2.5 Flash/Pro.

# Why I Built This

During stand-ups, client calls, and planning meetings, it’s easy to forget:

* who committed to what  
* deadlines  
* decisions taken  
* risks  
* follow-ups  

I wanted a simple tool that could take a meeting transcript and turn it into structured, useful information — automatically.

# System Overview

The project is designed as four small cooperating agents:

# 1. Transcript Analyzer (Agent 1)
Understands the meeting and extracts:
* topics
* summary
* decisions
* risks

# 2. Action Item Extractor (Agent 2)
Finds all actionable items, including:
* tasks
* owners
* due dates
* priority
* status

# 3. Memory Manager (Agent 3)
Stores all past meetings in persistent JSON memory
so you can query past tasks or review history.

# 4. Orchestrator (Agent 4)
Runs the entire end-to-end pipeline:
* analyzes the transcript  
* extracts action items  
* saves results  
* returns a final combined report  


# Project Structure
smart_meeting_memory_agent/
│
├── agents/
│ ├── transcript_analyzer.py
│ ├── action_item_extractor.py
│ ├── memory_manager.py
│ └── orchestrator.py
│
├── tools/
│ ├── logger_tool.py
│ └── pretty.py
│ └── report_generator.py
│
├── meeting_memory.json
└── README.md


# How to Run

1. Set your Google API key in `.env`:
GEMINI_API_KEY=your_key_here

2. Run the orchestrator:

```python
from agents.orchestrator import OrchestratorAgent

agent = OrchestratorAgent()
result = agent.process_meeting(transcript_text)
print(result)

Example Output
{
  "topics": [...],
  "summary": "...",
  "decisions": [...],
  "risks": [...],
  "action_items": [...]
}

Features

Works on any meeting transcript
Uses Gemini 2.5 Flash / Pro (fallback mechanism built-in)
Automatic long-term memory
Clean JSON output
Simple, modular, and easy to extend

Notes

This project intentionally keeps everything lightweight and readable.
Focus is on clarity and usefulness, not complexity.

