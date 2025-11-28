import random

class CreativeAgent:
    """
    Creative Agent:
    - Detects low CTR campaigns
    - Generates improved creatives (hooks, headlines, descriptions)
    - Output used for creatives.json
    """

    def __init__(self, ctr_threshold=0.01):
        self.ctr_threshold = ctr_threshold  # 1% CTR

    def generate_creatives(self, campaign_name, df_campaign):
        """
        df_campaign = filtered rows belonging to a single campaign.
        """

        impressions = df_campaign["impressions"].sum()
        clicks = df_campaign["clicks"].sum()

        ctr = clicks / impressions if impressions > 0 else 0

        # If CTR is good → no creatives needed
        if ctr >= self.ctr_threshold:
            return None

        # Extract existing creative messages
        messages = df_campaign["creative_message"].dropna().astype(str).tolist()

        if len(messages) == 0:
            messages = ["High-quality comfort wear for daily use."]

        # Use a few keyword patterns from existing texts
        keywords = self.extract_keywords(messages)

        # Generate new creatives
        creatives = {
            "campaign": campaign_name,
            "ctr": float(ctr),
            "headline_variations": self.generate_headlines(keywords),
            "hook_variations": self.generate_hooks(keywords),
            "description_variations": self.generate_descriptions(keywords)
        }

        return creatives

    # ---------------------------
    # Keyword Extraction
    # ---------------------------
    def extract_keywords(self, messages):
        words = []

        for msg in messages:
            for w in msg.lower().split():
                cleaned = w.strip(".,!?:;\"'()")
                if len(cleaned) > 3:
                    words.append(cleaned)

        if not words:
            return ["comfort", "fit", "premium"]

        # Return top keywords
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1

        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        top = [w for w, c in sorted_words[:5]]

        # Fallback
        return top or ["comfort", "fit", "premium"]

    # ---------------------------
    # Headline Generator
    # ---------------------------
    def generate_headlines(self, keywords):
        base = [
            f"Experience true {keywords[0]} today.",
            f"Engineered for unmatched {keywords[0]}.",
            f"Your perfect {keywords[0]} fit awaits.",
            f"Designed for comfort. Built for performance."
        ]
        return base

    # ---------------------------
    # Hook Generator
    # ---------------------------
    def generate_hooks(self, keywords):
        hooks = [
            "Feel the difference instantly.",
            "Made for all–day confidence.",
            f"Upgrade your {keywords[0]} experience.",
            f"Say goodbye to discomfort — hello to {keywords[0]}!"
        ]
        return hooks

    # ---------------------------
    # Description Generator
    # ---------------------------
    def generate_descriptions(self, keywords):
        desc = [
            f"Our new collection combines premium fabric with everyday {keywords[0]}.",
            f"Engineered for durability, breathability, and maximum {keywords[0]}.",
            f"Perfect for workouts, daily wear, and long hours — enjoy pure {keywords[0]}.",
        ]
        return desc
