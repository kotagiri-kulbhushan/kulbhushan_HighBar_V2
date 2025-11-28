class PlannerAgent:
    """
    Planner Agent:
    - Takes the main instruction (ex: "analyze facebook ads")
    - Breaks it into a sequence of tasks
    - Each task will be executed by a specific agent
    """

    def __init__(self):
        pass

    def create_plan(self, user_request: str):
        """
        Returns an ordered list of tasks for the pipeline.
        """

        plan = [
            {
                "task": "load_data",
                "agent": "DataAgent",
                "description": "Load and clean the Facebook ads dataset."
            },
            {
                "task": "compute_daily_metrics",
                "agent": "DataAgent",
                "description": "Calculate CTR, ROAS, spend, impressions grouped by campaign and date."
            },
            {
                "task": "generate_insights",
                "agent": "InsightAgent",
                "description": "Analyze performance changes and generate hypotheses about ROAS/CTR."
            },
            {
                "task": "validate_insights",
                "agent": "EvaluatorAgent",
                "description": "Score insights, evaluate accuracy and assign confidence."
            },
            {
                "task": "generate_creatives",
                "agent": "CreativeAgent",
                "description": "Generate optimized ad creatives for low CTR campaigns."
            },
            {
                "task": "prepare_report",
                "agent": "ReportAgent",
                "description": "Combine insights and creatives into final report.md"
            }
        ]

        return plan
