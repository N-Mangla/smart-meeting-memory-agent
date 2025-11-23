import json
from datetime import datetime
from tools.pretty import pretty_json


class ReportGenerator:
    """Exports meeting results as HTML or Markdown."""

    @staticmethod
    def to_markdown(result, filename=None):
        """Generate a Markdown report for the meeting."""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

        md = []
        md.append(f"# Meeting Summary Report\n")
        md.append(f"**Generated:** {datetime.now().isoformat()}\n")

        md.append("## Key Topics")
        for t in result["analysis"]["topics"]:
            md.append(f"- {t}")

        md.append("\n## Summary")
        md.append(result["analysis"]["summary"])

        md.append("\n## Decisions")
        if result["analysis"]["decisions"]:
            for d in result["analysis"]["decisions"]:
                md.append(f"- {d}")
        else:
            md.append("_None_")

        md.append("\n## Risks")
        if result["analysis"]["risks"]:
            for r in result["analysis"]["risks"]:
                md.append(f"- {r}")
        else:
            md.append("_None_")

        md.append("\n## Action Items")
        if result["action_items"]:
            for item in result["action_items"]:
                md.append(f"- **{item['task']}** — {item['owner']} (Due: {item['due_date']}) [Priority: {item['priority']}]")
        else:
            md.append("_No action items extracted._")

        # Save file
        with open(filename, "w") as f:
            f.write("\n".join(md))

        return filename

    @staticmethod
    def to_html(result, filename=None):
        """Generate a simple HTML report for the meeting."""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"

        html = f"""
        <html>
        <head>
            <title>Meeting Summary</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .section {{ margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>Meeting Summary Report</h1>
            <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>

            <div class="section">
                <h2>Key Topics</h2>
                <ul>
                    {''.join(f"<li>{t}</li>" for t in result['analysis']['topics'])}
                </ul>
            </div>

            <div class="section">
                <h2>Summary</h2>
                <p>{result['analysis']['summary']}</p>
            </div>

            <div class="section">
                <h2>Decisions</h2>
                <ul>
                    {''.join(f"<li>{d}</li>" for d in result['analysis']['decisions']) or '<li>None</li>'}
                </ul>
            </div>

            <div class="section">
                <h2>Risks</h2>
                <ul>
                    {''.join(f"<li>{r}</li>" for r in result['analysis']['risks']) or '<li>None</li>'}
                </ul>
            </div>

            <div class="section">
                <h2>Action Items</h2>
                <ul>
                    {''.join(f"<li><strong>{a['task']}</strong> — {a['owner']} (Due: {a['due_date']})</li>" for a in result['action_items']) or '<li>No action items extracted.</li>'}
                </ul>
            </div>

        </body>
        </html>
        """

        with open(filename, "w") as f:
            f.write(html)

        return filename
