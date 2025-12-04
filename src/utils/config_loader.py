import yaml
from pathlib import Path

def load_config(path="config/config.yaml"):
    # Resolve relative to project root (two levels up from utils)
    root = Path(__file__).resolve().parents[1]
    cfg_path = root / path
    if not cfg_path.exists():
        # If not found, try project root (allow both src/config and root/config)
        alt = Path(__file__).resolve().parents[2] / path
        if alt.exists():
            cfg_path = alt
    if not cfg_path.exists():
        raise FileNotFoundError(f"[CONFIG ERROR] File not found: {cfg_path}")

    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


