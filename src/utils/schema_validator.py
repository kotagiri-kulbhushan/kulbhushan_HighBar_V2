from typing import Dict
import pandas as pd

class SchemaError(Exception): pass
class DataQualityError(Exception): pass

EXPECTED_SCHEMA_V1 = {
    "campaign_name": "object",
    "adset_name": "object",
    "date": "datetime64[ns]",
    "spend": "float64",
    "impressions": "int64",
    "clicks": "int64",
    "purchases": "int64",
    "revenue": "float64",
    "creative_message": "object",
    "audience_type": "object",
    "platform": "object",
    "country": "object"
}

def validate_schema(df: pd.DataFrame, expected: Dict, allow_extra=True):
    missing = [c for c in expected.keys() if c not in df.columns]
    if missing:
        raise SchemaError(f"Missing columns: {missing}")
    # check dtypes for columns present
    # coerce date separately
    # Return cleaned df
    return df
