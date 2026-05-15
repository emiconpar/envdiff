"""Integration tests combining merger and reporter."""

import pytest
from envdiff.merger import merge_envs, merge_conflicts, MergeConflictError
from envdiff.reporter import conflict_report, merge_summary


def test_merge_then_report_clean():
    env1 = {"A": "1", "B": "2"}
    env2 = {"C": "3", "D": "4"}
    merged = merge_envs([env1, env2])
    assert len(merged) == 4
    report = conflict_report([env1, env2])
    assert "No conflicts" in report


def test_merge_skip_then_verify_report():
    env1 = {"X": "old", "SAFE": "yes"}
    env2 = {"X": "new", "SAFE": "yes"}
    merged = merge_envs([env1, env2], strategy="skip")
    assert "X" not in merged
    assert merged["SAFE"] == "yes"

    report = conflict_report([env1, env2])
    assert "X" in report
    assert "SAFE" not in report


def test_summary_reflects_merge_skip():
    env1 = {"A": "1", "B": "conflict"}
    env2 = {"C": "3", "B": "different"}
    summary = merge_summary([env1, env2])
    merged = merge_envs([env1, env2], strategy="skip")
    assert summary["conflict_keys"] == 1
    assert "B" not in merged


def test_three_way_merge_right_with_report():
    env1 = {"K": "v1"}
    env2 = {"K": "v2"}
    env3 = {"K": "v3"}
    merged = merge_envs([env1, env2, env3], strategy="right")
    assert merged["K"] == "v3"
    conflicts = merge_conflicts([env1, env2, env3])
    assert "K" in conflicts
    assert len(conflicts["K"]) == 3


def test_error_strategy_with_labels_in_report():
    env1 = {"SECRET": "abc"}
    env2 = {"SECRET": "xyz"}
    with pytest.raises(MergeConflictError):
        merge_envs([env1, env2], strategy="error", labels=["prod", "dev"])
    report = conflict_report([env1, env2], labels=["prod", "dev"])
    assert "prod" in report
    assert "dev" in report
    assert "SECRET" in report
