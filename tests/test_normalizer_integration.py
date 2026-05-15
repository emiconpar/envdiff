"""Integration tests combining normalizer with parser and diff."""

import pytest
from envdiff.normalizer import normalize_env, find_case_conflicts
from envdiff.parser import parse_env_string
from envdiff.diff import diff_envs, has_differences


ENV_A = """
db_host=localhost
db_port=5432
app_name=  MyApp  
"""

ENV_B = """
DB_HOST=localhost
DB_PORT=5432
APP_NAME=MyApp
"""


def test_normalize_before_diff_eliminates_case_differences():
    left = parse_env_string(ENV_A)
    right = parse_env_string(ENV_B)
    left_norm = normalize_env(left)
    right_norm = normalize_env(right)
    result = diff_envs(left_norm, right_norm)
    assert not has_differences(result)


def test_without_normalization_case_diff_detected():
    left = parse_env_string(ENV_A)
    right = parse_env_string(ENV_B)
    result = diff_envs(left, right)
    # lowercase keys won't match uppercase keys without normalization
    assert has_differences(result)


def test_normalize_strips_value_whitespace_before_diff():
    left = parse_env_string("APP_NAME=  MyApp  ")
    right = parse_env_string("APP_NAME=MyApp")
    left_norm = normalize_env(left)
    right_norm = normalize_env(right)
    result = diff_envs(left_norm, right_norm)
    assert not has_differences(result)


def test_find_case_conflicts_after_parse():
    raw = parse_env_string("foo=1\nFOO=2\nBAR=3")
    conflicts = find_case_conflicts(raw)
    assert "FOO" in conflicts
    assert len(conflicts["FOO"]) == 2


def test_normalize_env_then_diff_detects_real_change():
    left = parse_env_string("DB_HOST=localhost")
    right = parse_env_string("DB_HOST=remotehost")
    left_norm = normalize_env(left)
    right_norm = normalize_env(right)
    result = diff_envs(left_norm, right_norm)
    assert has_differences(result)
    assert "DB_HOST" in result.changed
