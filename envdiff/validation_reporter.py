"""Human-readable reports for ValidationResult objects."""

from __future__ import annotations

from typing import Optional

from envdiff.validator import ValidationResult


def _red(text: str) -> str:
    return f"\033[31m{text}\033[0m"


def _yellow(text: str) -> str:
    return f"\033[33m{text}\033[0m"


def _green(text: str) -> str:
    return f"\033[32m{text}\033[0m"


def format_validation_report(
    result: ValidationResult,
    label: Optional[str] = None,
    color: bool = True,
) -> str:
    """Return a multi-line string describing errors and warnings."""
    lines: list[str] = []
    header = f"Validation report{f' for {label}' if label else ''}"
    lines.append(header)
    lines.append("-" * len(header))

    if result.is_valid and not result.has_warnings:
        ok = _green("OK — no issues found.") if color else "OK — no issues found."
        lines.append(ok)
        return "\n".join(lines)

    for error in result.errors:
        prefix = _red("ERROR") if color else "ERROR"
        lines.append(f"  {prefix}: {error}")

    for warning in result.warnings:
        prefix = _yellow("WARN") if color else "WARN"
        lines.append(f"  {prefix}: {warning}")

    return "\n".join(lines)


def validation_summary(result: ValidationResult, color: bool = True) -> str:
    """Return a single-line summary suitable for CLI output."""
    n_errors = len(result.errors)
    n_warnings = len(result.warnings)

    if n_errors == 0 and n_warnings == 0:
        msg = "Validation passed with no issues."
        return _green(msg) if color else msg

    parts = []
    if n_errors:
        part = f"{n_errors} error{'s' if n_errors != 1 else ''}"
        parts.append(_red(part) if color else part)
    if n_warnings:
        part = f"{n_warnings} warning{'s' if n_warnings != 1 else ''}"
        parts.append(_yellow(part) if color else part)

    return "Validation finished: " + ", ".join(parts) + "."
