class CreativeAgentV2:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def generate(self, campaign, eval_out, sample_messages):
        print("\n[CREATIVE] Generating creative ideas for:", campaign)

        impact = eval_out["summary"]["impact"]
        reasons = eval_out["summary"]["reasons"]

        ideas = []

        for r in reasons:
            ideas.append({
                "campaign": campaign,
                "issue": r,
                "idea": f"Test a new creative variation addressing: {r}"
            })

        print("[CREATIVE] Ideas generated:", ideas)
        return ideas
