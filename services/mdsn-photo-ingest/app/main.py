import logging
import os
from pathlib import Path

from flask import Flask, jsonify

from .adapters.simulate import SimulatedInboxWatcher
from .bluefolder_client import BlueFolderAttachmentClient
from .config import Settings
from .db import init_db
from .pipeline import IngestMessage, process_message


def configure_logging(level: str) -> None:
    if logging.getLogger().handlers:
        return
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def create_app() -> Flask:
    settings = Settings()
    configure_logging(settings.log_level)

    app = Flask(__name__)
    db_path = settings.data_dir / "mdsn_photo_ingest.db"
    init_db(db_path)

    bluefolder_client = BlueFolderAttachmentClient(api_key=os.getenv("BLUEFOLDER_API_KEY"))

    def handle_message(message: IngestMessage) -> None:
        process_message(message, db_path=db_path, bluefolder_client=bluefolder_client)

    if settings.mode == "simulate":
        watcher = SimulatedInboxWatcher(
            inbox_root=settings.dev_inbox,
            scan_interval=settings.scan_interval,
            on_message=handle_message,
        )
        watcher.start()
        # Keep reference on app to avoid premature GC.
        app.config["WATCHER"] = watcher

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "mode": settings.mode})

    @app.route("/")
    def index():
        return jsonify(
            {
                "service": "mdsn-photo-ingest",
                "mode": settings.mode,
                "data_dir": str(settings.data_dir),
                "dev_inbox": str(settings.dev_inbox),
            }
        )

    return app


app = create_app()
