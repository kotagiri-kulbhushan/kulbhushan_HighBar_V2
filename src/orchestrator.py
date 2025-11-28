import json
import os
import pandas as pd

from src.agents.data_agent import DataAgent
from src.agents.planner import PlannerAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent


class Orchestrator:
    """
    Orchestrator:
    - Executes all agents in correct order
    - Produces insights.json, creatives.json, report.md
    - Represents full agentic pipeline logic
    """

    def __init__(self, data_path):
        self.data_agent = DataAgent(data_path)
        self.planner = PlannerAgent()
        self.insight_agent = InsightAgent()
        self.evaluator = EvaluatorAgent()
        self.creative_agent = CreativeAgent()

        # Output locations
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)

    # ----------------------------------------------------------
    # Run the full pipeline
    # ----------------------------------------------------------
    def run(self):
        print("\n🚀 Starting AI Agentic Pipeline...\n")

        # 1. Load dataset
        df = self.data_agent.load()
        print("✔ Dataset loaded.")

        # 2. Compute daily metrics per campaign
        daily_metrics = self.data_agent.compute_daily_metrics(df)
        print("✔ Daily metrics computed.")

        # 3. Group campaigns
        campaign_names = daily_metrics["campaign_name"].unique()

        all_insights = []
        all_creatives = []

        # ----------------------------------------------------------
        # Process each campaign one by one
        # ----------------------------------------------------------
        for campaign in campaign_names:
            print(f"\n📌 Processing Campaign: {campaign}")

            camp_df = daily_metrics[daily_metrics["campaign_name"] == campaign]

            # Window summary (last 7d vs previous 7d)
            summary = self.data_agent.window_summary(camp_df, days=7)

            if summary is None:
                print("   Skipped (not enough data).")
                continue

            # -----------------------------
            # Generate Insights
            # -----------------------------
            insights = self.insight_agent.generate_insights(campaign, summary)
            print("   ✔ Insights Generated.")
            all_insights.append(insights)

            # -----------------------------
            # Evaluate Hypotheses
            # -----------------------------
            evaluated = self.evaluator.evaluate(
                campaign, summary, insights["hypotheses"]
            )
            insights["evaluated_hypotheses"] = evaluated
            print("   ✔ Hypotheses Evaluated.")

            # -----------------------------
            # Generate Creatives (if needed)
            # -----------------------------
            df_original = df[df["campaign_name"] == campaign]
            creatives = self.creative_agent.generate_creatives(campaign, df_original)

            if creatives:
                print("   ✔ Creative suggestions generated.")
                all_creatives.append(creatives)
            else:
                print("   — CTR OK, no new creatives needed.")

        # ----------------------------------------------------------
        # Save insights.json
        # ----------------------------------------------------------
        with open(os.path.join(self.reports_dir, "insights.json"), "w") as f:
            json.dump(all_insights, f, indent=4)
        print("\n✔ insights.json saved.")

        # ----------------------------------------------------------
        # Save creatives.json
        # ----------------------------------------------------------
        with open(os.path.join(self.reports_dir, "creatives.json"), "w") as f:
            json.dump(all_creatives, f, indent=4)
        print("✔ creatives.json saved.")

        # ----------------------------------------------------------
        # Create report.md
        # ----------------------------------------------------------
        self.generate_report(all_insights, all_creatives)
        print("✔ report.md generated.")

        print("\n🎉 Pipeline completed successfully!\n")

    # ----------------------------------------------------------
    # Report Generator
    # ----------------------------------------------------------
    def generate_report(self, insights, creatives):
        report_path = os.path.join(self.reports_dir, "report.md")

        lines = ["# Kasparro AI Assignment Report\n"]

        lines.append("## 🔍 Campaign Insights\n")
        for item in insights:
            lines.append(f"### Campaign: {item['campaign']}")
            for hyp in item["evaluated_hypotheses"]:
                lines.append(f"- **Hypothesis:** {hyp['hypothesis']}")
                lines.append(f"  - Confidence: {hyp['final_confidence']:.2f}")
                lines.append(f"  - Validation: {hyp['validation']}")
            lines.append("")

        lines.append("\n## 🎨 Creative Recommendations\n")
        for c in creatives:
            lines.append(f"### Campaign: {c['campaign']}")
            lines.append("**Headlines:**")
            for h in c["headline_variations"]:
                lines.append(f"- {h}")
            lines.append("\n**Hooks:**")
            for h in c["hook_variations"]:
                lines.append(f"- {h}")
            lines.append("\n**Descriptions:**")
            for d in c["description_variations"]:
                lines.append(f"- {d}")
            lines.append("")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

