import numpy as np

class EvaluatorAgentV2:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def evaluate_campaign(self, kpi_df):
        print("\n[EVAL] Evaluating KPIs...")

        try:
            recent_d = self.config["windows"]["recent_days"]
            base_d = self.config["windows"]["baseline_days"]

            recent = kpi_df.tail(recent_d)
            baseline = kpi_df.head(base_d)

            def pct(col):
                a = baseline[col].mean()
                b = recent[col].mean()
                if a == 0 or np.isnan(a):
                    return 0
                return (b - a) / a

            ctr_delta = pct("ctr")
            roas_delta = pct("roas")
            cpc_delta = pct("cpc")

            print("[EVAL] CTR delta =", ctr_delta)
            print("[EVAL] ROAS delta =", roas_delta)
            print("[EVAL] CPC delta =", cpc_delta)

            severity = 0
            reasons = []

            if ctr_delta < -0.20:
                severity += 1
                reasons.append(f"CTR dropped {ctr_delta:.2%}")

            if roas_delta < -0.15:
                severity += 1
                reasons.append(f"ROAS fell {roas_delta:.2%}")

            if cpc_delta > 0.20:
                severity += 1
                reasons.append(f"CPC increased {cpc_delta:.2%}")

            impact = "low"
            if severity == 1:
                impact = "medium"
            elif severity >= 2:
                impact = "high"

            result = {
                "summary": {
                    "impact": impact,
                    "severity": severity,
                    "reasons": reasons or ["No performance issues detected"],
                    "confidence": 0.7 if severity > 0 else 0.4
                },
                "evidence": {
                    "ctr_delta": float(ctr_delta),
                    "roas_delta": float(roas_delta),
                    "cpc_delta": float(cpc_delta)
                }
            }

            print("[EVAL] Final evaluation:", result)
            return result

        except Exception as e:
            print("[EVAL] ERROR:", e)
            return {
                "summary": {"impact": "low", "severity": 0, "reasons": ["evaluation_error"], "confidence": 0.1},
                "evidence": {}
            }
