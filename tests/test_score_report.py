"""Tests for envdiff.score_report."""

import pytest
from envdiff.scorer import EnvScore, score_env
from envdiff.score_report import (
    format_score_report,
    score_summary,
    format_comparison_report,
)


@pytest.fixture
def good_score():
    return EnvScore(label="prod", total=5, score=95, bonuses=["All values non-empty"])


@pytest.fixture
def bad_score():
    return EnvScore(
        label="dev",
        total=3,
        score=40,
        penalties=["2 plain secret(s) detected", "1 invalid key(s)"],
    )


def test_report_contains_label(good_score):
    report = format_score_report(good_score, color=False)
    assert "prod" in report


def test_report_contains_score(good_score):
    report = format_score_report(good_score, color=False)
    assert "95" in report


def test_report_contains_grade(good_score):
    report = format_score_report(good_score, color=False)
    assert "Grade: A" in report


def test_report_shows_bonus(good_score):
    report = format_score_report(good_score, color=False)
    assert "All values non-empty" in report


def test_report_shows_penalty(bad_score):
    report = format_score_report(bad_score, color=False)
    assert "plain secret" in report


def test_report_no_issues_message():
    result = EnvScore(label="x", total=2, score=100)
    report = format_score_report(result, color=False)
    assert "No issues" in report


def test_score_summary_format(good_score):
    summary = score_summary(good_score)
    assert "prod" in summary
    assert "95" in summary
    assert "A" in summary


def test_comparison_report_contains_both_labels(good_score, bad_score):
    report = format_comparison_report(good_score, bad_score, color=False)
    assert "prod" in report
    assert "dev" in report


def test_comparison_report_shows_winner(good_score, bad_score):
    report = format_comparison_report(good_score, bad_score, color=False)
    assert "Winner: prod" in report


def test_comparison_report_shows_delta(good_score, bad_score):
    report = format_comparison_report(good_score, bad_score, color=False)
    assert "+55" in report or "55" in report


def test_format_score_report_integration():
    env = {"APP": "test", "PORT": "3000"}
    result = score_env(env, label="staging")
    report = format_score_report(result, color=False)
    assert "staging" in report
    assert str(result.score) in report
