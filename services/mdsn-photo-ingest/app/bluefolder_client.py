from typing import List, Optional

try:
    # Preferred import when the git submodule is installed in editable mode.
    from bluefolder_api.client import BlueFolderClient  # type: ignore
except Exception:  # pragma: no cover - fallback for when editable install is not available
    BlueFolderClient = None  # type: ignore


class BlueFolderAttachmentClient:
    """
    Wrapper that hides the optional dependency so the pipeline code can stay simple.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key
        self.client = None
        if BlueFolderClient and api_key:
            self.client = BlueFolderClient(api_key=api_key)

    def attach_images(self, srid: str, image_paths: List[str]) -> str:
        """
        Placeholder for attaching images to BlueFolder service requests.

        Returns a human-readable note to persist in the audit log.
        """
        if not self.client:
            return (
                "TODO: Attach images to BlueFolder (api key required, "
                "pip install -e /libs/bluefolder-api)."
            )

        # TODO: wire up real attachment calls against BlueFolder once credentials are available.
        # This method should upload the provided images to the service request identified by srid.
        return "BlueFolder attachment placeholder executed (no-op)."
