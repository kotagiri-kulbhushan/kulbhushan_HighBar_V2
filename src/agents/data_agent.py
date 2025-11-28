import pandas as pd

class DataAgent:
    """
    The DataAgent handles:
    - loading the CSV file
    - cleaning the data
    - computing basic metrics (CTR, ROAS)
    - preparing summary tables for the Insight Agent
    """
    
    def __init__(self, path: str):
        self.path = path

    def load(self):
        """Loads the dataset and parses the date column."""
        df = pd.read_csv(self.path, parse_dates=["date"])
        return df

    def compute_daily_metrics(self, df):
        """
        Groups by campaign_name and date to compute:
        - impressions
        - clicks
        - spend
        - revenue
        - CTR (clicks / impressions)
        - ROAS (revenue / spend)
        """
        
        grouped = df.groupby(["campaign_name", "date"]).agg({
            "impressions": "sum",
            "clicks": "sum",
            "spend": "sum",
            "revenue": "sum"
        }).reset_index()

        # Prevent division errors
        grouped["ctr"] = grouped["clicks"] / grouped["impressions"].replace(0, 1)
        grouped["roas"] = grouped["revenue"] / grouped["spend"].replace(0, 1)

        return grouped

    def window_summary(self, df, days=7):
        """
        Computes last N days vs previous N days metrics.
        This summary will be used by the Insight Agent.
        """
        df = df.sort_values("date")

        if len(df) < days * 2:
            return None

        recent = df.tail(days)
        previous = df.tail(days * 2).head(days)

        summary = {
            "recent_ctr": recent["ctr"].mean(),
            "previous_ctr": previous["ctr"].mean(),
            "recent_roas": recent["roas"].mean(),
            "previous_roas": previous["roas"].mean(),
            "ctr_change_pct": (
                (recent["ctr"].mean() - previous["ctr"].mean()) /
                (previous["ctr"].mean() + 1e-6)
            ),
            "roas_change_pct": (
                (recent["roas"].mean() - previous["roas"].mean()) /
                (previous["roas"].mean() + 1e-6)
            )
        }

        return summary
