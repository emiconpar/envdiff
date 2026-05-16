"""Tests for envdiff.scorer."""

import pytest
from envdiff.scorer import EnvScore, score_env, compare_scores


@pytest.fixture
def clean_env():
    return {
        "APP_NAME": "myapp",
        "APP_PORT": "8080",
        "APP_DEBUG": "false",
    }


def test_score_clean_env_is_high(clean_env):
    result = score_env(clean_env, label="clean")
    assert result.score >= 80


def test_score_label_is_set(clean_env):
    result = score_env(clean_env, label="production")
    assert result.label == "production"


def test_score_total_matches_env_size(clean_env):
    result = score_env(clean_env)
    assert result.total == len(clean_env)


def test_score_empty_env_returns_zero():
    result = score_env({})
    assert result.score == 0
    assert result.total == 0


def test_score_plain_secret_penalised():
    env = {"API_KEY": "abc123plaintext", "HOST": "localhost"}
    result = score_env(env)
    assert result.score < 100
    assert any("plain secret" in p for p in result.penalties)


def test_score_invalid_key_penalised():
    env = {"1INVALID": "value", "GOOD_KEY": "val"}
    result = score_env(env)
    assert result.score < 100
    assert any("invalid key" in p for p in result.penalties)


def test_score_empty_value_penalised():
    env = {"KEY": "", "OTHER": "val"}
    result = score_env(env)
    assert any("empty" in p for p in result.penalties)


def test_score_all_non_empty_bonus(clean_env):
    result = score_env(clean_env)
    assert any("non-empty" in b for b in result.bonuses)


def test_grade_a_for_high_score():
    s = EnvScore(label="x", total=5, score=95)
    assert s.grade == "A"


def test_grade_f_for_low_score():
    s = EnvScore(label="x", total=5, score=20)
    assert s.grade == "F"


def test_compare_scores_winner():
    left = EnvScore(label="left", total=3, score=90)
    right = EnvScore(label="right", total=3, score=70)
    comp = compare_scores(left, right)
    assert comp["winner"] == "left"
    assert comp["delta"] == 20


def test_compare_scores_right_wins():
    left = EnvScore(label="left", total=3, score=50)
    right = EnvScore(label="right", total=3, score=80)
    comp = compare_scores(left, right)
    assert comp["winner"] == "right"
