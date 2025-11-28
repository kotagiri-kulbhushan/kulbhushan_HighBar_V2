import numpy as np

class InsightAgent:
    """
    Insight Agent:
    - Receives daily metrics per campaign
    - Compares last 7 days vs previous 7 days
    - Generates performance insights
    - Produces hypotheses with confidence scores
    """

    def __init__(self):
        pass

    def generate_insights(self, campaign_name, df_summary):
        """
        df_summary must contain:
        - recent_ctr
        - previous_ctr
        - recent_roas
        - previous_roas
        - ctr_change_pct
        - roas_change_pct
        """

        insights = {
            "campaign": campaign_name,
            "insights": [],
            "hypotheses": []
        }

        recent_ctr = df_summary["recent_ctr"]
        prev_ctr = df_summary["previous_ctr"]
        ctr_change = df_summary["ctr_change_pct"]

        recent_roas = df_summary["recent_roas"]
        prev_roas = df_summary["previous_roas"]
        roas_change = df_summary["roas_change_pct"]

        # -----------------------------
        # Insight 1: CTR Change
        # -----------------------------
        ctr_trend = ""
        if ctr_change < -0.05:
            ctr_trend = "CTR has significantly dropped."
        elif ctr_change > 0.05:
            ctr_trend = "CTR has significantly increased."
        else:
            ctr_trend = "CTR has remained relatively stable."

        insights["insights"].append({
            "metric": "CTR",
            "recent": float(recent_ctr),
            "previous": float(prev_ctr),
            "change_pct": float(ctr_change),
            "interpretation": ctr_trend
        })

        # -----------------------------
        # Insight 2: ROAS Change
        # -----------------------------
        roas_trend = ""
        if roas_change < -0.10:
            roas_trend = "ROAS has dropped significantly."
        elif roas_change > 0.10:
            roas_trend = "ROAS has increased significantly."
        else:
            roas_trend = "ROAS has remained stable."

        insights["insights"].append({
            "metric": "ROAS",
            "recent": float(recent_roas),
            "previous": float(prev_roas),
            "change_pct": float(roas_change),
            "interpretation": roas_trend
        })

        # -----------------------------
        # Generate Hypotheses
        # -----------------------------

        hypotheses = []

        # Hypothesis 1 — Creative Fatigue
        if ctr_change < -0.05:
            hypotheses.append({
                "hypothesis": "Creative fatigue leading to lower CTR.",
                "confidence": 0.8,
                "evidence": f"CTR dropped by {ctr_change:.2f}."
            })

        # Hypothesis 2 — Spend increased without returns
        if roas_change < -0.10:
            hypotheses.append({
                "hypothesis": "Increased spend without proportional returns.",
                "confidence": 0.75,
                "evidence": f"ROAS dropped by {roas_change:.2f}."
            })

        # Hypothesis 3 — Audience Saturation
        if ctr_change < -0.03 and roas_change < -0.05:
            hypotheses.append({
                "hypothesis": "Audience saturation or targeting inefficiency.",
                "confidence": 0.70,
                "evidence": "Both CTR and ROAS decreased together."
            })

        # Hypothesis 4 — Stable performance
        if len(hypotheses) == 0:
            hypotheses.append({
                "hypothesis": "No major performance issues detected.",
                "confidence": 0.50,
                "evidence": "CTR and ROAS changes are minimal."
            })

        insights["hypotheses"] = hypotheses

        return insights
