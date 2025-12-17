import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .bluefolder_client import BlueFolderAttachmentClient
from .db import write_audit_entry

logger = logging.getLogger(__name__)


@dataclass
class IngestMessage:
    subject: str
    attachments: List[Path]
    source: str
    metadata: Dict[str, str] = field(default_factory=dict)


def parse_srid(text: str) -> Optional[str]:
    """Return the first 4+ digit number found in the provided text."""
    match = re.search(r"(\d{4,})", text)
    return match.group(1) if match else None


def process_images(image_paths: List[Path]) -> List[Path]:
    """
    Placeholder for the real image processing pipeline (resize, normalize, etc).
    """
    # TODO: perform real image processing before uploading.
    logger.info("Processed %s images (placeholder).", len(image_paths))
    return image_paths


def process_message(
    message: IngestMessage,
    db_path: Path,
    bluefolder_client: BlueFolderAttachmentClient,
) -> Dict[str, str]:
    srid = parse_srid(message.subject) or parse_srid(message.metadata.get("hint", ""))
    status = "processed"
    notes: List[str] = []

    if not srid:
        status = "missing_srid"
        notes.append("No SRID detected in subject or metadata.")
        logger.warning("Skipping message without SRID. Subject=%s", message.subject)
        write_audit_entry(
            db_path,
            {"srid": srid or "", "source": message.source, "status": status, "notes": "; ".join(notes)},
        )
        return {"status": status, "notes": "; ".join(notes)}

    try:
        processed_images = process_images(message.attachments)
        attach_note = bluefolder_client.attach_images(
            srid=srid, image_paths=[str(path) for path in processed_images]
        )
        notes.append(attach_note)
        logger.info("Finished message for SRID %s from %s", srid, message.source)
    except Exception as exc:  # pragma: no cover - guard rail for unexpected failures
        status = "error"
        notes.append(f"Pipeline failed: {exc}")
        logger.exception("Failed to process message for SRID %s", srid)

    write_audit_entry(
        db_path,
        {"srid": srid, "source": message.source, "status": status, "notes": "; ".join(notes)},
    )
    return {"status": status, "notes": "; ".join(notes)}
