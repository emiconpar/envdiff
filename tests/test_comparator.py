"""Tests for envdiff.comparator."""

import pytest
from envdiff.comparator import compare_many, unique_to_label, MultiDiffResult


@pytest.fixture
def three_envs():
    a = {"HOST": "localhost", "PORT": "8080", "ONLY_A": "yes"}
    b = {"HOST": "localhost", "PORT": "9090", "ONLY_B": "yes"}
    c = {"HOST": "localhost", "PORT": "8080", "ONLY_C": "yes"}
    return [a, b, c]


def test_compare_many_returns_multi_diff_result(three_envs):
    result = compare_many(three_envs)
    assert isinstance(result, MultiDiffResult)


def test_compare_many_default_labels(three_envs):
    result = compare_many(three_envs)
    assert result.labels == ["env0", "env1", "env2"]


def test_compare_many_custom_labels(three_envs):
    result = compare_many(three_envs, labels=["dev", "staging", "prod"])
    assert result.labels == ["dev", "staging", "prod"]


def test_compare_many_all_keys_collected(three_envs):
    result = compare_many(three_envs)
    assert result.all_keys == {"HOST", "PORT", "ONLY_A", "ONLY_B", "ONLY_C"}


def test_keys_in_all_returns_common_keys(three_envs):
    result = compare_many(three_envs)
    assert result.keys_in_all() == {"HOST", "PORT"}


def test_keys_missing_in_some(three_envs):
    result = compare_many(three_envs)
    missing = result.keys_missing_in_some()
    assert "ONLY_A" in missing
    assert "ONLY_B" in missing
    assert "ONLY_C" in missing
    assert "HOST" not in missing


def test_keys_with_conflicts_detects_differing_values(three_envs):
    result = compare_many(three_envs)
    assert "PORT" in result.keys_with_conflicts()
    assert "HOST" not in result.keys_with_conflicts()


def test_keys_consistent_returns_identical_keys(three_envs):
    result = compare_many(three_envs)
    assert result.keys_consistent() == {"HOST"}


def test_matrix_contains_correct_values(three_envs):
    result = compare_many(three_envs, labels=["a", "b", "c"])
    assert result.matrix["PORT"]["a"] == "8080"
    assert result.matrix["PORT"]["b"] == "9090"
    assert result.matrix["PORT"]["c"] == "8080"


def test_unique_to_label(three_envs):
    result = compare_many(three_envs, labels=["a", "b", "c"])
    assert unique_to_label(result, "a") == {"ONLY_A"}
    assert unique_to_label(result, "b") == {"ONLY_B"}
    assert unique_to_label(result, "c") == {"ONLY_C"}


def test_compare_many_empty_list():
    result = compare_many([])
    assert result.labels == []
    assert result.all_keys == set()


def test_compare_many_single_env():
    result = compare_many([{"A": "1"}])
    assert result.keys_in_all() == {"A"}
    assert result.keys_with_conflicts() == set()


def test_compare_many_label_length_mismatch():
    with pytest.raises(ValueError, match="Length of labels"):
        compare_many([{"A": "1"}, {"B": "2"}], labels=["only_one"])


def test_compare_two_identical_envs():
    env = {"X": "1", "Y": "2"}
    result = compare_many([env, env.copy()], labels=["left", "right"])
    assert result.keys_consistent() == {"X", "Y"}
    assert result.keys_with_conflicts() == set()
