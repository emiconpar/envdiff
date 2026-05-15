"""Audit environment variable sets for security and compliance issues."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Keys that should never be committed or exposed
FORBIDDEN_PATTERNS = ["PRIVATE_KEY", "AWS_SECRET", "DATABASE_URL", "MASTER_KEY"]

# Keys expected to be present in a production-ready environment
REQUIRED_KEYS = ["APP_ENV", "LOG_LEVEL"]


@dataclass
class AuditResult:
    label: str
    forbidden_found: List[str] = field(default_factory=list)
    missing_required: List[str] = field(default_factory=list)
    plain_secrets: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.forbidden_found and not self.missing_required and not self.plain_secrets


def _looks_like_plain_secret(key: str, value: str) -> bool:
    """Heuristic: secret-like key with a short, non-placeholder value."""
    secret_hints = ("SECRET", "PASSWORD", "TOKEN", "KEY", "PASS", "AUTH")
    if not any(hint in key.upper() for hint in secret_hints):
        return False
    if value.startswith("${") or value.startswith("${") or not value:
        return False
    return len(value) < 64


def audit_env(
    env: Dict[str, str],
    label: str = "env",
    forbidden_patterns: Optional[List[str]] = None,
    required_keys: Optional[List[str]] = None,
) -> AuditResult:
    """Run an audit on an environment variable mapping."""
    forbidden_patterns = forbidden_patterns if forbidden_patterns is not None else FORBIDDEN_PATTERNS
    required_keys = required_keys if required_keys is not None else REQUIRED_KEYS

    result = AuditResult(label=label)

    for key in env:
        for pattern in forbidden_patterns:
            if pattern.upper() in key.upper():
                result.forbidden_found.append(key)
                break

    for req in required_keys:
        if req not in env:
            result.missing_required.append(req)

    for key, value in env.items():
        if _looks_like_plain_secret(key, value):
            result.plain_secrets.append(key)

    if env.get("APP_ENV", "").lower() == "production":
        for key, value in env.items():
            if not value:
                result.warnings.append(f"Empty value for '{key}' in production")

    return result
