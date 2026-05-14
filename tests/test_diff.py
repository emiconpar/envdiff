"""Tests for envdiff.diff module."""

import pytest

from envdiff.diff import diff_envs, EnvDiffResult


LEFT = {"APP": "web", "DEBUG": "true", "PORT": "8080", "SHARED": "same"}
RIGHT = {"APP": "api", "HOST": "0.0.0.0", "PORT": "8080", "SHARED": "same"}


def test_only_in_left():
    result = diff_envs(LEFT, RIGHT)
    assert "DEBUG" in result.only_in_left
    assert result.only_in_left["DEBUG"] == "true"


def test_only_in_right():
    result = diff_envs(LEFT, RIGHT)
    assert "HOST" in result.only_in_right


def test_changed_values():
    result = diff_envs(LEFT, RIGHT)
    assert "APP" in result.changed
    assert result.changed["APP"] == ("web", "api")


def test_unchanged_values():
    result = diff_envs(LEFT, RIGHT)
    assert "PORT" in result.unchanged
    assert "SHARED" in result.unchanged


def test_has_differences_true():
    result = diff_envs(LEFT, RIGHT)
    assert result.has_differences is True


def test_has_differences_false():
    env = {"KEY": "value"}
    result = diff_envs(env, env)
    assert result.has_differences is False


def test_ignore_keys():
    result = diff_envs(LEFT, RIGHT, ignore_keys=["APP", "DEBUG", "HOST"])
    assert "APP" not in result.changed
    assert "DEBUG" not in result.only_in_left
    assert "HOST" not in result.only_in_right


def test_summary_with_differences():
    result = diff_envs(LEFT, RIGHT)
    summary = result.summary
    assert "only in left" in summary
    assert "only in right" in summary
    assert "changed" in summary


def test_empty_envs():
    result = diff_envs({}, {})
    assert not result.has_differences
    assert result.summary == "no variables found"
