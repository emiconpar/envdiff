"""Tests for envdiff.reporter module."""

from envdiff.reporter import conflict_report, merge_summary


ENV_A = {"FOO": "1", "SHARED": "from_a", "ONLY_A": "a"}
ENV_B = {"BAR": "2", "SHARED": "from_b", "ONLY_B": "b"}
ENV_C = {"SHARED": "from_c", "ONLY_C": "c"}


def test_conflict_report_no_conflicts():
    env1 = {"A": "1"}
    env2 = {"B": "2"}
    report = conflict_report([env1, env2])
    assert "No conflicts" in report


def test_conflict_report_shows_conflicting_key():
    report = conflict_report([ENV_A, ENV_B])
    assert "SHARED" in report


def test_conflict_report_shows_values():
    report = conflict_report([ENV_A, ENV_B])
    assert "from_a" in report
    assert "from_b" in report


def test_conflict_report_uses_labels():
    report = conflict_report([ENV_A, ENV_B], labels=["prod", "staging"])
    assert "prod" in report
    assert "staging" in report


def test_conflict_report_default_labels():
    report = conflict_report([ENV_A, ENV_B])
    assert "env[0]" in report
    assert "env[1]" in report


def test_conflict_report_counts_conflicts():
    report = conflict_report([ENV_A, ENV_B])
    assert "1 conflict" in report


def test_conflict_report_multiple_conflicts():
    env1 = {"X": "1", "Y": "a"}
    env2 = {"X": "2", "Y": "b"}
    report = conflict_report([env1, env2])
    assert "2 conflict" in report


def test_conflict_report_color_no_crash():
    report = conflict_report([ENV_A, ENV_B], use_color=True)
    assert "SHARED" in report


def test_conflict_report_no_conflict_color():
    env1 = {"A": "1"}
    report = conflict_report([env1], use_color=True)
    assert "No conflicts" in report


def test_merge_summary_total_keys():
    summary = merge_summary([ENV_A, ENV_B])
    # FOO, SHARED, ONLY_A, BAR, ONLY_B = 5
    assert summary["total_keys"] == 5


def test_merge_summary_conflict_keys():
    summary = merge_summary([ENV_A, ENV_B])
    assert summary["conflict_keys"] == 1


def test_merge_summary_clean_keys():
    summary = merge_summary([ENV_A, ENV_B])
    assert summary["clean_keys"] == 4


def test_merge_summary_no_conflicts():
    env1 = {"A": "1"}
    env2 = {"B": "2"}
    summary = merge_summary([env1, env2])
    assert summary["conflict_keys"] == 0
    assert summary["clean_keys"] == 2
