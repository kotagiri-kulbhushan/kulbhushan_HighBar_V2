# src/agents/insight_agent_v2.py
import pandas as pd
import numpy as np

class InsightAgentV2:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def _resolve_purchase_value_column(self, df):
        """
        Try multiple column names to find a column representing total revenue/purchase value.
        Common names: purchase_value, revenue, revenue_value, total_revenue
        Returns column name or None.
        """
        candidates = ["purchase_value", "revenue", "revenue_value", "total_revenue", "purchase_value_usd"]
        for c in candidates:
            if c in df.columns:
                return c
        return None

    def compute_kpis(self, df):
        """
        Compute CTR, CPC, ROAS and return a dataframe with KPI columns added.
        This version is defensive about missing columns and prints debug info.
        """
        print("\n[INSIGHT] Computing KPIs for campaign...")

        df = df.copy()

        # Ensure numeric types for main columns
        for col in ["impressions", "clicks", "spend", "purchases"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            else:
                # create with zeros if missing
                df[col] = 0

        # Resolve purchase/revenue column (flexible)
        revenue_col = self._resolve_purchase_value_column(df)
        if revenue_col:
            print(f"[INSIGHT] Using revenue column: '{revenue_col}'")
            df["purchase_value"] = pd.to_numeric(df[revenue_col], errors="coerce")
        else:
            # if revenue missing but purchases exists, try to infer per-unit value from 'revenue' absence
            print("[INSIGHT] No explicit revenue column found. Falling back: purchase_value = purchases * 0.0")
            df["purchase_value"] = df.get("purchases", 0) * 0.0

        # Compute CTR: clicks / impressions
        # avoid division-by-zero by replacing zeros with NaN
        df["ctr"] = df["clicks"] / df["impressions"].replace({0: np.nan})
        # Compute CPC: spend / clicks
        df["cpc"] = df["spend"] / df["clicks"].replace({0: np.nan})
        # Compute ROAS: purchase_value / spend
        df["roas"] = df["purchase_value"] / df["spend"].replace({0: np.nan})

        # Fill infinite values (if any) with NaN then keep as-is
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Round KPIs for readability
        df["ctr"] = df["ctr"].round(4)
        df["cpc"] = df["cpc"].round(2)
        df["roas"] = df["roas"].round(2)

        print("[INSIGHT] KPIs computed. Sample:")
        cols_to_show = [c for c in ["date","spend","impressions","clicks","ctr","cpc","purchases","purchase_value","roas"] if c in df.columns]
        print(df[cols_to_show].head().to_string())

        return df


