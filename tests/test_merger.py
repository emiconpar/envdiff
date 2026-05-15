"""Tests for envdiff.merger module."""

import pytest
from envdiff.merger import merge_envs, merge_conflicts, MergeConflictError


ENV_A = {"FOO": "1", "BAR": "hello", "SHARED": "from_a"}
ENV_B = {"BAZ": "2", "SHARED": "from_b", "EXTRA": "yes"}
ENV_C = {"SHARED": "from_c", "ONLY_C": "c"}


def test_merge_right_strategy_last_wins():
    result = merge_envs([ENV_A, ENV_B], strategy="right")
    assert result["SHARED"] == "from_b"


def test_merge_left_strategy_first_wins():
    result = merge_envs([ENV_A, ENV_B], strategy="left")
    assert result["SHARED"] == "from_a"


def test_merge_combines_unique_keys():
    result = merge_envs([ENV_A, ENV_B])
    assert "FOO" in result
    assert "BAR" in result
    assert "BAZ" in result
    assert "EXTRA" in result


def test_merge_error_strategy_raises_on_conflict():
    with pytest.raises(MergeConflictError) as exc_info:
        merge_envs([ENV_A, ENV_B], strategy="error")
    assert exc_info.value.key == "SHARED"
    assert "from_a" in exc_info.value.values
    assert "from_b" in exc_info.value.values


def test_merge_skip_strategy_omits_conflicts():
    result = merge_envs([ENV_A, ENV_B], strategy="skip")
    assert "SHARED" not in result
    assert "FOO" in result
    assert "BAZ" in result


def test_merge_empty_list_returns_empty():
    assert merge_envs([]) == {}


def test_merge_single_env_returns_copy():
    result = merge_envs([ENV_A])
    assert result == ENV_A
    assert result is not ENV_A


def test_merge_three_envs_right_strategy():
    result = merge_envs([ENV_A, ENV_B, ENV_C], strategy="right")
    assert result["SHARED"] == "from_c"
    assert result["ONLY_C"] == "c"


def test_merge_no_conflict_same_value():
    env1 = {"KEY": "same"}
    env2 = {"KEY": "same"}
    result = merge_envs([env1, env2], strategy="error")
    assert result["KEY"] == "same"


def test_merge_conflicts_returns_only_differing_keys():
    conflicts = merge_conflicts([ENV_A, ENV_B, ENV_C])
    assert "SHARED" in conflicts
    assert set(conflicts["SHARED"]) == {"from_a", "from_b", "from_c"}
    assert "FOO" not in conflicts


def test_merge_conflicts_no_conflicts_returns_empty():
    env1 = {"A": "1"}
    env2 = {"B": "2"}
    assert merge_conflicts([env1, env2]) == {}


def test_merge_conflict_error_message_contains_key():
    err = MergeConflictError("MY_KEY", ["val1", "val2"])
    assert "MY_KEY" in str(err)
