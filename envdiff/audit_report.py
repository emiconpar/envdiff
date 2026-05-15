"""Format audit results for human-readable output."""

from typing import Optional
from envdiff.auditor import AuditResult


def _red(text: str, color: bool) -> str:
    return f"\033[31m{text}\033[0m" if color else text


def _yellow(text: str, color: bool) -> str:
    return f"\033[33m{text}\033[0m" if color else text


def _green(text: str, color: bool) -> str:
    return f"\033[32m{text}\033[0m" if color else text


def format_audit_report(result: AuditResult, color: bool = True) -> str:
    """Return a formatted string describing the audit result."""
    lines = [f"Audit Report [{result.label}]"]
    lines.append("-" * 40)

    if result.forbidden_found:
        lines.append(_red("Forbidden keys found:", color))
        for key in result.forbidden_found:
            lines.append(f"  - {key}")

    if result.missing_required:
        lines.append(_yellow("Missing required keys:", color))
        for key in result.missing_required:
            lines.append(f"  - {key}")

    if result.plain_secrets:
        lines.append(_yellow("Possible plain-text secrets:", color))
        for key in result.plain_secrets:
            lines.append(f"  - {key}")

    if result.warnings:
        lines.append(_yellow("Warnings:", color))
        for warn in result.warnings:
            lines.append(f"  ! {warn}")

    if result.passed:
        lines.append(_green("PASSED — no critical issues found.", color))
    else:
        lines.append(_red("FAILED — audit issues detected.", color))

    return "\n".join(lines)


def audit_summary(result: AuditResult) -> str:
    """Return a one-line summary of the audit result."""
    status = "PASSED" if result.passed else "FAILED"
    issues = len(result.forbidden_found) + len(result.missing_required) + len(result.plain_secrets)
    return (
        f"[{result.label}] Audit {status}: "
        f"{issues} issue(s), {len(result.warnings)} warning(s)"
    )
