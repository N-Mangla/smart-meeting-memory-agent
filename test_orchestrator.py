from agents.orchestrator import OrchestratorAgent
from tools.logger_tool import Logger
from tools.pretty import pretty_json
from tools.report_generator import ReportGenerator


if __name__ == "__main__":
    Logger.info("Starting orchestrator test run...")

    agent = OrchestratorAgent()

    # Sample transcript
    sample_transcript = """
    Alice will finish the client report by Tuesday.
    Bob will prepare slides for Friday's presentation.
    Neha will update the API documentation before Monday.
    """

    Logger.info("Sending sample transcript to OrchestratorAgent...")

    # Run the full meeting pipeline
    result = agent.process_meeting(sample_transcript)

    Logger.info("Orchestrator pipeline completed. Printing final structured output...\n")

    print(pretty_json(result))

    # --------------------------------------------
    # Export HTML + Markdown reports
    # --------------------------------------------
    Logger.info("Exporting meeting reports...")

    md_file = ReportGenerator.to_markdown(result, filename="last_meeting.md")
    html_file = ReportGenerator.to_html(result, filename="last_meeting.html")

    Logger.info(f"Report files generated:")
    Logger.info(f" Markdown : {md_file}")
    Logger.info(f" HTML :     {html_file}")

    print("\nReports saved:")
    print(f"✔ {md_file}")
    print(f"✔ {html_file}")
