import os
from pathlib import Path


class Settings:
    """Lightweight settings object sourced from environment variables."""

    def __init__(self) -> None:
        self.mode = os.getenv("INGEST_MODE", "simulate")
        self.port = int(os.getenv("MDSN_PORT", "5055"))
        self.data_dir = Path(os.getenv("DATA_DIR", "/data"))
        self.dev_inbox = Path(os.getenv("DEV_INBOX", "/app/dev_inbox"))
        self.scan_interval = float(os.getenv("MDSN_SCAN_INTERVAL", "5"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Make sure the data directory exists for sqlite and other local state.
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.dev_inbox.mkdir(parents=True, exist_ok=True)
