"""Score environment variable sets based on quality heuristics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from envdiff.auditor import audit_env
from envdiff.validator import validate_keys


@dataclass
class EnvScore:
    label: str
    total: int
    score: int  # 0-100
    penalties: List[str] = field(default_factory=list)
    bonuses: List[str] = field(default_factory=list)

    @property
    def grade(self) -> str:
        if self.score >= 90:
            return "A"
        if self.score >= 75:
            return "B"
        if self.score >= 60:
            return "C"
        if self.score >= 40:
            return "D"
        return "F"


def score_env(env: Dict[str, str], label: str = "env") -> EnvScore:
    """Compute a quality score for an environment variable set."""
    total = len(env)
    penalties: List[str] = []
    bonuses: List[str] = []
    deductions = 0

    if total == 0:
        return EnvScore(label=label, total=0, score=0, penalties=["No keys found"])

    # Validation penalties
    vresult = validate_keys(env)
    if vresult.errors:
        deductions += min(30, len(vresult.errors) * 5)
        penalties.append(f"{len(vresult.errors)} invalid key(s)")
    if vresult.warnings:
        deductions += min(20, len(vresult.warnings) * 3)
        penalties.append(f"{len(vresult.warnings)} empty value(s)")

    # Audit penalties
    aresult = audit_env(env)
    if aresult.plain_secrets:
        deductions += min(40, len(aresult.plain_secrets) * 10)
        penalties.append(f"{len(aresult.plain_secrets)} plain secret(s) detected")
    if aresult.missing_required:
        deductions += min(20, len(aresult.missing_required) * 5)
        penalties.append(f"{len(aresult.missing_required)} missing required key(s)")
    if aresult.forbidden_keys:
        deductions += min(20, len(aresult.forbidden_keys) * 5)
        penalties.append(f"{len(aresult.forbidden_keys)} forbidden key(s)")

    # Bonuses
    non_empty = sum(1 for v in env.values() if v.strip())
    if non_empty == total:
        bonuses.append("All values non-empty")

    score = max(0, 100 - deductions)
    return EnvScore(label=label, total=total, score=score, penalties=penalties, bonuses=bonuses)


def compare_scores(left: EnvScore, right: EnvScore) -> Dict[str, object]:
    """Return a comparison summary of two EnvScore objects."""
    return {
        "left": {"label": left.label, "score": left.score, "grade": left.grade},
        "right": {"label": right.label, "score": right.score, "grade": right.grade},
        "winner": left.label if left.score >= right.score else right.label,
        "delta": left.score - right.score,
    }
