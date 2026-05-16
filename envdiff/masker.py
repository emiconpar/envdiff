"""Mask or partially reveal environment variable values for safe display."""

from __future__ import annotations

DEFAULT_MASK = "***"
DEFAULT_REVEAL_CHARS = 4


def mask_value(value: str, mask: str = DEFAULT_MASK) -> str:
    """Fully mask a value."""
    return mask


def partial_mask(value: str, reveal_chars: int = DEFAULT_REVEAL_CHARS, mask: str = DEFAULT_MASK) -> str:
    """Reveal the last `reveal_chars` characters and mask the rest."""
    if not value:
        return mask
    if len(value) <= reveal_chars:
        return mask
    return mask + value[-reveal_chars:]


def mask_env(
    env: dict[str, str],
    keys: set[str],
    *,
    partial: bool = False,
    reveal_chars: int = DEFAULT_REVEAL_CHARS,
    mask: str = DEFAULT_MASK,
) -> dict[str, str]:
    """Return a copy of env with specified keys masked."""
    result = dict(env)
    for key in keys:
        if key in result:
            if partial:
                result[key] = partial_mask(result[key], reveal_chars=reveal_chars, mask=mask)
            else:
                result[key] = mask_value(result[key], mask=mask)
    return result


def masked_keys(env: dict[str, str], original: dict[str, str]) -> list[str]:
    """Return keys whose values differ between env and original (i.e. were masked)."""
    return [k for k in env if env[k] != original.get(k)]


def mask_summary(env: dict[str, str], original: dict[str, str]) -> dict[str, object]:
    """Return a summary dict describing masking applied."""
    masked = masked_keys(env, original)
    return {
        "total_keys": len(env),
        "masked_count": len(masked),
        "masked_keys": sorted(masked),
    }
