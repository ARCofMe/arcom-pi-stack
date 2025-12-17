import logging
import threading
import time
from pathlib import Path
from typing import Callable, Iterable, List, Set

from ..pipeline import IngestMessage

logger = logging.getLogger(__name__)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff"}


class SimulatedInboxWatcher:
    """
    Polls ./dev_inbox/<SRID>/ for images and feeds them into the pipeline.
    """

    def __init__(
        self,
        inbox_root: Path,
        scan_interval: float,
        on_message: Callable[[IngestMessage], None],
    ) -> None:
        self.inbox_root = inbox_root
        self.scan_interval = scan_interval
        self.on_message = on_message
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._seen: Set[Path] = set()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, name="dev-inbox-watcher", daemon=True)
        self._thread.start()
        logger.info("Simulated inbox watcher started. Watching %s", self.inbox_root)

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._poll_once()
            except Exception:  # pragma: no cover - guard rail for background loop
                logger.exception("Watcher encountered an error while polling %s", self.inbox_root)
            time.sleep(self.scan_interval)

    def _poll_once(self) -> None:
        for folder in sorted(self._iter_message_folders()):
            image_files = self._gather_images(folder)
            if not image_files:
                continue

            # Skip if none of the images are new since last pass.
            if all(path in self._seen for path in image_files):
                continue

            logger.info("Processing %s images found in %s", len(image_files), folder)
            for path in image_files:
                self._seen.add(path)

            message = IngestMessage(
                subject=folder.name,
                attachments=image_files,
                source="simulate",
                metadata={"hint": folder.name, "source_path": str(folder)},
            )
            self.on_message(message)

    def _iter_message_folders(self) -> Iterable[Path]:
        if not self.inbox_root.exists():
            return []
        return [p for p in self.inbox_root.iterdir() if p.is_dir()]

    def _gather_images(self, folder: Path) -> List[Path]:
        return [
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS
        ]
