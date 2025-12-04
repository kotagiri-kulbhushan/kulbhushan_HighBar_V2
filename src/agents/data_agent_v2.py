import pandas as pd
from pathlib import Path

class DataAgentV2:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        # config["data"]["path"] expected
        self.path = Path(self.config["data"]["path"])

    def load(self):
        print(f"\n[DATA] Loading data from: {self.path}")
        if not self.path.exists():
            raise FileNotFoundError(f"Data file not found: {self.path}")

        df = pd.read_csv(self.path, parse_dates=[self.config["data"].get("date_col", "date")], low_memory=False)
        print(f"[DATA] Loaded {len(df)} rows, columns: {list(df.columns)[:10]}")

        # Basic cleanup: column name normalization
        df.columns = [c.strip() for c in df.columns]

        # Ensure numeric types
        for col in ["impressions", "clicks", "spend", "purchases", "revenue", "purchase_value"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Fill missing columns with defaults if necessary
        if "impressions" not in df.columns:
            df["impressions"] = 0
        if "clicks" not in df.columns:
            df["clicks"] = 0
        if "spend" not in df.columns:
            df["spend"] = 0
        if "purchases" not in df.columns:
            df["purchases"] = 0
        # revenue/purchase_value fallback
        if "revenue" not in df.columns and "purchase_value" in df.columns:
            df["revenue"] = df["purchase_value"]
        if "revenue" not in df.columns:
            df["revenue"] = df["purchases"] * 0.0

        # Report sample
        print("[DATA] Sample rows:")
        print(df.head(3).to_string())

        return df

