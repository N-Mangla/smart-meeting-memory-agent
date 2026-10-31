# Smart Meeting Memory Agent

A small Python prototype that extracts meeting summaries and action items through the Gemini REST API, then saves results to a local JSON memory file. Built during the Google AI Agents Intensive program.

## What it does

- `TranscriptAnalyzer`: extracts topics, summaries, decisions, and risks.
- `ActionItemExtractor`: extracts tasks, owners, deadlines, priority, and status.
- `OrchestratorAgent`: coordinates both steps and saves the result through `MemoryManager`.
- `ReportGenerator`: exports Markdown and HTML reports from the example runner.

The repository uses a sequential Python pipeline with two Gemini calls, not independently deployed autonomous services. `main.py` is a placeholder; `test_orchestrator.py` is the executable sample runner, not a mocked automated unit test.

## Run locally

Use Python 3.10+ and a Gemini API key with access to the configured models.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment using `.venv\\Scripts\\activate`.

Create a `.env` file at the repository root:

```env
GEMINI_API_KEY=your_api_key_here
```

Then run:

```bash
python test_orchestrator.py
```

This makes live API requests (subject to Gemini access, quotas and model availability), appends a meeting record to `meeting_memory.json`, and writes `last_meeting.md` and `last_meeting.html`. Never commit real meeting transcripts, API keys, or other confidential material.

## Repository structure

```text
agents/
  transcript_analyzer.py
  action_item_extractor.py
  memory_manager.py
  orchestrator.py
tools/
  logger_tool.py
  pretty.py
  report_generator.py
test_orchestrator.py
meeting_memory.json
requirements.txt
```

The included `meeting_memory.json` contains example records. The repository currently lacks an offline mocked-test suite; successful local execution requires working API credentials and network access.

## Implementation notes

Model responses are parsed as JSON by the orchestrator. Gemini Flash is used by default, with a Pro fallback when the API returns 404. The local memory file is a demonstration of persistence, not a secure multi-user data store.

This project demonstrates experimental Python/LLM integration rather than production-level AI-agent infrastructure.
