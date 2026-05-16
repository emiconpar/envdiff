"""Multi-env comparator: compare more than two env dicts at once."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

EnvMap = Dict[str, str]


@dataclass
class MultiDiffResult:
    """Result of comparing multiple environment maps."""

    labels: List[str]
    all_keys: Set[str] = field(default_factory=set)
    # key -> {label -> value}  (only labels where key is present)
    matrix: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def keys_in_all(self) -> Set[str]:
        """Return keys present in every env."""
        return {
            k for k, presence in self.matrix.items()
            if set(presence.keys()) == set(self.labels)
        }

    def keys_missing_in_some(self) -> Set[str]:
        """Return keys absent from at least one env."""
        return self.all_keys - self.keys_in_all()

    def keys_with_conflicts(self) -> Set[str]:
        """Return keys present in all envs but with differing values."""
        result: Set[str] = set()
        for key in self.keys_in_all():
            values = set(self.matrix[key].values())
            if len(values) > 1:
                result.add(key)
        return result

    def keys_consistent(self) -> Set[str]:
        """Return keys present in all envs with identical values."""
        return self.keys_in_all() - self.keys_with_conflicts()


def compare_many(
    envs: List[EnvMap],
    labels: Optional[List[str]] = None,
) -> MultiDiffResult:
    """Compare a list of env dicts and return a MultiDiffResult.

    Args:
        envs: List of environment variable dicts to compare.
        labels: Optional display labels; defaults to "env0", "env1", …

    Returns:
        A MultiDiffResult capturing the full comparison matrix.
    """
    if not envs:
        return MultiDiffResult(labels=[])

    resolved_labels = labels if labels else [f"env{i}" for i in range(len(envs))]
    if len(resolved_labels) != len(envs):
        raise ValueError("Length of labels must match length of envs.")

    all_keys: Set[str] = set()
    for env in envs:
        all_keys.update(env.keys())

    matrix: Dict[str, Dict[str, str]] = {k: {} for k in all_keys}
    for label, env in zip(resolved_labels, envs):
        for key, value in env.items():
            matrix[key][label] = value

    return MultiDiffResult(
        labels=resolved_labels,
        all_keys=all_keys,
        matrix=matrix,
    )


def unique_to_label(result: MultiDiffResult, label: str) -> Set[str]:
    """Return keys that exist exclusively in the env identified by *label*."""
    return {
        k for k, presence in result.matrix.items()
        if list(presence.keys()) == [label]
    }
