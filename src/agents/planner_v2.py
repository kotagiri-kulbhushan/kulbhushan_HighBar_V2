class PlannerV2:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def plan(self, df):
        """
        Simple planner: return unique campaign names as tasks.
        Each task is a dict with metadata consumed by orchestrator.
        """
        campaigns = df["campaign_name"].dropna().unique().tolist()
        tasks = []
        print(f"\n[PLANNER] Found {len(campaigns)} unique campaigns (first 10): {campaigns[:10]}")
        for c in campaigns:
            tasks.append({"campaign_raw": c})
        return tasks
