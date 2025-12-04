import logging
import json
from pathlib import Path
from datetime import datetime

class JSONLogger:
    def __init__(self, run_id="run", base_dir="logs"):
        self.run_id = run_id
        self.base_dir = Path(base_dir)
        self.run_dir = self.base_dir / f"run_{self.run_id}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        # Setup python logger
        self.logger = logging.getLogger(f"kasparro_{run_id}")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        # File handler: JSON lines
        fh = logging.FileHandler(self.run_dir / "agent_logs.jsonl", encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(fh)

        # Console handler for human readable
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fmt = logging.Formatter("%(levelname)s - %(message)s")
        ch.setFormatter(fmt)
        self.logger.addHandler(ch)

    def _log(self, level, **kwargs):
        # Build a simple JSON structure
        payload = {
            "ts": datetime.utcnow().isoformat(),
            "run_id": self.run_id,
            **kwargs
        }
        try:
            self.logger.log(level, json.dumps(payload, ensure_ascii=False))
        except Exception:
            # Fallback simple message
            self.logger.log(level, str(payload))

    def info(self, **kwargs):
        self._log(logging.INFO, **kwargs)

    def warn(self, **kwargs):
        self._log(logging.WARNING, **kwargs)

    def error(self, **kwargs):
        self._log(logging.ERROR, **kwargs)

    def close(self):
        # flush handlers
        for h in list(self.logger.handlers):
            try:
                h.flush()
                h.close()
            except Exception:
                pass
            self.logger.removeHandler(h)
