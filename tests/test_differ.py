"""Tests for envdiff.differ module."""
import pytest
from envdiff.differ import build_side_by_side, SideBySideDiff, SideBySideRow


@pytest.fixture
def left_env():
    return {"APP_HOST": "localhost", "APP_PORT": "8080", "DB_PASS": "secret"}


@pytest.fixture
def right_env():
    return {"APP_HOST": "prod.example.com", "APP_PORT": "8080", "NEW_KEY": "hello"}


def test_build_returns_side_by_side_diff(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    assert isinstance(result, SideBySideDiff)


def test_labels_are_stored(left_env, right_env):
    result = build_side_by_side(left_env, right_env, left_label="dev", right_label="prod")
    assert result.left_label == "dev"
    assert result.right_label == "prod"


def test_added_key_detected(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    keys = [r.key for r in result.added()]
    assert "NEW_KEY" in keys


def test_removed_key_detected(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    keys = [r.key for r in result.removed()]
    assert "DB_PASS" in keys


def test_changed_key_detected(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    keys = [r.key for r in result.changed()]
    assert "APP_HOST" in keys


def test_unchanged_key_detected(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    keys = [r.key for r in result.unchanged()]
    assert "APP_PORT" in keys


def test_added_row_has_none_left(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    row = next(r for r in result.added() if r.key == "NEW_KEY")
    assert row.left_value is None
    assert row.right_value == "hello"


def test_removed_row_has_none_right(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    row = next(r for r in result.removed() if r.key == "DB_PASS")
    assert row.right_value is None
    assert row.left_value == "secret"


def test_exclude_unchanged(left_env, right_env):
    result = build_side_by_side(left_env, right_env, include_unchanged=False)
    assert all(r.status != "unchanged" for r in result.rows)


def test_rows_sorted_alphabetically(left_env, right_env):
    result = build_side_by_side(left_env, right_env)
    keys = [r.key for r in result.rows]
    assert keys == sorted(keys)


def test_identical_envs_all_unchanged():
    env = {"A": "1", "B": "2"}
    result = build_side_by_side(env, env)
    assert len(result.unchanged()) == 2
    assert len(result.changed()) == 0
    assert len(result.added()) == 0
    assert len(result.removed()) == 0
