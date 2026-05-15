"""Snapshot utilities for saving and loading environment variable sets."""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional


SNAPSHOT_VERSION = 1


def save_snapshot(
    env: Dict[str, str],
    path: str,
    label: Optional[str] = None,
) -> None:
    """Persist an environment variable mapping to a JSON snapshot file.

    Args:
        env: Mapping of variable names to values.
        path: Destination file path (will be created or overwritten).
        label: Optional human-readable label stored in the snapshot metadata.
    """
    payload = {
        "version": SNAPSHOT_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "label": label or "",
        "env": env,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")


def load_snapshot(path: str) -> Dict[str, str]:
    """Load an environment variable mapping from a JSON snapshot file.

    Args:
        path: Path to a snapshot file previously created by :func:`save_snapshot`.

    Returns:
        Mapping of variable names to values.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError: If the snapshot format is unrecognised or the version is
            unsupported.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Snapshot file not found: {path}")

    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)

    if not isinstance(payload, dict) or "env" not in payload:
        raise ValueError(f"Invalid snapshot format in: {path}")

    version = payload.get("version", 0)
    if version != SNAPSHOT_VERSION:
        raise ValueError(
            f"Unsupported snapshot version {version!r} in: {path}"
        )

    env = payload["env"]
    if not isinstance(env, dict):
        raise ValueError(f"'env' field must be a JSON object in: {path}")

    return {str(k): str(v) for k, v in env.items()}


def snapshot_metadata(path: str) -> Dict[str, str]:
    """Return metadata fields (version, created_at, label) from a snapshot."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Snapshot file not found: {path}")

    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)

    return {
        "version": str(payload.get("version", "")),
        "created_at": str(payload.get("created_at", "")),
        "label": str(payload.get("label", "")),
    }
