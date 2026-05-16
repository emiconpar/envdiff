"""Apply a diff result as a patch to produce a merged env dict."""

from typing import Dict, Optional
from envdiff.diff import EnvDiffResult


class PatchError(Exception):
    """Raised when a patch cannot be applied cleanly."""


def apply_patch(
    base: Dict[str, str],
    diff: EnvDiffResult,
    strategy: str = "right",
) -> Dict[str, str]:
    """Apply *diff* to *base* and return the patched environment.

    strategy:
      - "right"  : additions and changes from the right side win (default)
      - "left"   : keep base values for changed keys; still add new keys
      - "error"  : raise PatchError on any changed key
    """
    if strategy not in ("right", "left", "error"):
        raise ValueError(f"Unknown strategy: {strategy!r}")

    result = dict(base)

    # Keys only in right — always add
    for key, value in diff.only_in_right.items():
        result[key] = value

    # Keys only in left — remove them (they were deleted on the right)
    for key in diff.only_in_left:
        result.pop(key, None)

    # Changed keys
    for key, (left_val, right_val) in diff.changed.items():
        if strategy == "error":
            raise PatchError(
                f"Conflict on key {key!r}: base={left_val!r}, patch={right_val!r}"
            )
        elif strategy == "right":
            result[key] = right_val
        # strategy == "left": keep existing value — no-op

    return result


def revert_patch(
    patched: Dict[str, str],
    diff: EnvDiffResult,
) -> Dict[str, str]:
    """Reverse a previously applied diff to recover the original env."""
    result = dict(patched)

    # Undo additions (only_in_right)
    for key in diff.only_in_right:
        result.pop(key, None)

    # Restore deletions (only_in_left)
    for key, value in diff.only_in_left.items():
        result[key] = value

    # Restore changed values to left side
    for key, (left_val, _right_val) in diff.changed.items():
        result[key] = left_val

    return result


def patch_summary(diff: EnvDiffResult) -> Dict[str, int]:
    """Return a count summary of what a patch would change."""
    return {
        "additions": len(diff.only_in_right),
        "deletions": len(diff.only_in_left),
        "modifications": len(diff.changed),
    }
