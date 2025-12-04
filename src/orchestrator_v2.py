import time
from datetime import datetime
from src.utils.config_loader import load_config
from src.utils.logger import JSONLogger

from src.agents.data_agent_v2 import DataAgentV2
from src.agents.planner_v2 import PlannerV2
from src.agents.insight_agent_v2 import InsightAgentV2
from src.agents.evaluator_agent_v2 import EvaluatorAgentV2
from src.agents.creative_agent_v2 import CreativeAgentV2
from src.agents.report_agent_v2 import ReportAgentV2


class OrchestratorV2:
    def __init__(self, config_path="config/config.yaml"):
        self.config = load_config(config_path)
        self.run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.logger = JSONLogger(self.run_id, self.config["logging"]["logs_dir"])

        print("\n[ORCH] Loaded config:", self.config)

        self.data_agent = DataAgentV2(self.config, self.logger)
        self.planner = PlannerV2(self.config, self.logger)
        self.insight = InsightAgentV2(self.config, self.logger)
        self.evaluator = EvaluatorAgentV2(self.config, self.logger)
        self.creative = CreativeAgentV2(self.config, self.logger)
        self.reporter = ReportAgentV2(self.config, self.logger)

    def run(self):
        t0 = time.time()

        df = self.data_agent.load()
        print("\n[ORCH] Data Loaded. Rows =", len(df))

        plan = self.planner.plan(df)
        print("[ORCH] Planned campaigns:", len(plan))

        all_insights = []
        all_creatives = []

        for task in plan:
            campaign = task["campaign_raw"]
            print("\n===============================")
            print("[ORCH] Processing campaign:", campaign)

            subdf = df[df["campaign_name"] == campaign]

            if len(subdf) < 3:
                print("[ORCH] Skipping — not enough rows")
                continue

            kpis = self.insight.compute_kpis(subdf)
            print("[ORCH] KPIs computed (head):")
            print(kpis.head())

            eval_out = self.evaluator.evaluate_campaign(kpis)
            print("[ORCH] Evaluation output:", eval_out)

            all_insights.append({"campaign": campaign, "evaluation": eval_out})

            impact = eval_out["summary"]["impact"]
            print("[ORCH] Impact =", impact)

            if impact in ("medium", "high"):
                print("[ORCH] Generating creatives NOW")
                creatives = self.creative.generate(
                    campaign,
                    eval_out,
                    sample_messages=subdf["creative_message"].dropna().tolist()[:5]
                )
                print("[ORCH] Generated creatives:", creatives)

                all_creatives.append(creatives)
            else:
                print("[ORCH] Skipping creatives — impact LOW")

        print("\n[ORCH] Saving JSON + Markdown...")
        self.reporter.save_json(all_insights, all_creatives, self.run_id)
        self.reporter.save_markdown(all_insights, all_creatives, self.run_id)

        print("🎉 Pipeline Finished Successfully.")
        return all_insights, all_creatives
