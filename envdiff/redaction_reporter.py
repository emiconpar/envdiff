"""Combines redaction with diff reporting for sanitized output."""

from envdiff.redactor import redact_env, sensitive_keys
from envdiff.diff import diff_envs, EnvDiffResult
from envdiff.formatter import format_diff, format_summary


def redact_and_diff(
    left: dict,
    right: dict,
    left_label: str = "left",
    right_label: str = "right",
    extra_sensitive: list = None,
) -> EnvDiffResult:
    """Redact both environments before diffing them.

    Args:
        left: First environment dict.
        right: Second environment dict.
        left_label: Label for the left side (unused in result but kept for API consistency).
        right_label: Label for the right side.
        extra_sensitive: Additional key substrings to treat as sensitive.

    Returns:
        EnvDiffResult computed on the redacted copies.
    """
    redacted_left = redact_env(left, extra_sensitive=extra_sensitive)
    redacted_right = redact_env(right, extra_sensitive=extra_sensitive)
    return diff_envs(redacted_left, redacted_right)


def format_redacted_diff(
    left: dict,
    right: dict,
    left_label: str = "left",
    right_label: str = "right",
    extra_sensitive: list = None,
    color: bool = True,
) -> str:
    """Return a formatted diff string with sensitive values masked.

    Args:
        left: First environment dict.
        right: Second environment dict.
        left_label: Display label for the left environment.
        right_label: Display label for the right environment.
        extra_sensitive: Additional key substrings to treat as sensitive.
        color: Whether to include ANSI color codes.

    Returns:
        Formatted diff string with redacted values.
    """
    result = redact_and_diff(
        left, right,
        left_label=left_label,
        right_label=right_label,
        extra_sensitive=extra_sensitive,
    )
    return format_diff(result, left_label=left_label, right_label=right_label, color=color)


def redacted_summary(
    left: dict,
    right: dict,
    extra_sensitive: list = None,
) -> str:
    """Return a one-line summary of differences after redaction.

    Args:
        left: First environment dict.
        right: Second environment dict.
        extra_sensitive: Additional key substrings to treat as sensitive.

    Returns:
        Summary string (e.g. '2 added, 1 removed, 3 changed').
    """
    result = redact_and_diff(left, right, extra_sensitive=extra_sensitive)
    return format_summary(result)


def list_redacted_keys(env: dict, extra_sensitive: list = None) -> list:
    """Return the list of keys that would be redacted in the given env.

    Args:
        env: Environment dict to inspect.
        extra_sensitive: Additional key substrings to treat as sensitive.

    Returns:
        Sorted list of key names that are considered sensitive.
    """
    return sorted(sensitive_keys(env, extra_sensitive=extra_sensitive))
