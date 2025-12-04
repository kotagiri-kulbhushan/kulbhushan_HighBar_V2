import json
from pathlib import Path
from datetime import datetime

class ReportAgentV2:
    def __init__(self, config, logger):
        self.logger = logger
        # Use configured reports path if present, else ./reports
        reports_path = config.get("paths", {}).get("reports", "reports")
        self.out_dir = Path(reports_path)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n[REPORT] Reports directory: {self.out_dir}")

    def save_json(self, insights, creatives, run_id):
        # Save both insights and creatives into separate files but include run metadata
        now = datetime.utcnow().isoformat()
        insights_payload = {
            "run_id": run_id,
            "generated_at": now,
            "insights": insights
        }
        creatives_payload = {
            "run_id": run_id,
            "generated_at": now,
            "creatives": creatives
        }

        insights_path = self.out_dir / f"insights_{run_id}.json"
        creatives_path = self.out_dir / f"creatives_{run_id}.json"

        with open(insights_path, "w", encoding="utf-8") as f:
            json.dump(insights_payload, f, indent=2, ensure_ascii=False)
        self.logger.info(agent="ReportAgentV2", event="insights_saved", path=str(insights_path))
        print(f"[REPORT] Saved insights -> {insights_path}")

        with open(creatives_path, "w", encoding="utf-8") as f:
            json.dump(creatives_payload, f, indent=2, ensure_ascii=False)
        self.logger.info(agent="ReportAgentV2", event="creatives_saved", path=str(creatives_path))
        print(f"[REPORT] Saved creatives -> {creatives_path}")

    def save_markdown(self, insights, creatives, run_id):
        md_path = self.out_dir / f"report_{run_id}.md"
        lines = []
        lines.append(f"# Kasparro FB Analyst — V2 Report\nGenerated: {datetime.utcnow().isoformat()}\n")

        if not insights:
            lines.append("No insights generated.\n")
        else:
            for ins in insights:
                camp = ins.get("campaign", "unknown")
                eval_obj = ins.get("evaluation") or ins.get("evaluator") or ins.get("evaluation", {})
                summary = eval_obj.get("summary", {}) if isinstance(eval_obj, dict) else {}
                details = eval_obj.get("details", {}) if isinstance(eval_obj, dict) else eval_obj.get("evidence", {})

                impact = summary.get("impact", "unknown")
                confidence = summary.get("confidence", "unknown")
                reasons = summary.get("reasons", "No reasons provided")

                lines.append(f"## Campaign: **{camp}**")
                lines.append(f"- **Impact**: {impact}")
                lines.append(f"- **Confidence**: {confidence}")
                lines.append(f"- **Reasons**: {reasons}\n")

                if isinstance(details, dict):
                    lines.append("### KPI Evidence")
                    for k, v in details.items():
                        lines.append(f"- {k}: {v}")
                    lines.append("")

        if creatives:
            lines.append("## Creative Suggestions\n")
            for block in creatives:
                # block may be list of ideas (per earlier code)
                if isinstance(block, list):
                    for idea in block:
                        camp = idea.get("campaign", "unknown")
                        lines.append(f"### Campaign: {camp}")
                        lines.append(f"- Idea: {idea.get('idea') or idea.get('issue') or str(idea)}")
                        lines.append(f"- Notes: {idea.get('reason', '')}")
                        lines.append("")
                elif isinstance(block, dict):
                    lines.append(str(block))

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        self.logger.info(agent="ReportAgentV2", event="markdown_saved", path=str(md_path))
        print(f"[REPORT] Saved markdown -> {md_path}")
