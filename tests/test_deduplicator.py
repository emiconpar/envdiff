"""Tests for envdiff.deduplicator."""

import pytest
from envdiff.deduplicator import (
    find_duplicates,
    deduplicate,
    DeduplicationResult,
)


ENV_A = {"HOST": "localhost", "PORT": "5432", "DEBUG": "true"}
ENV_B = {"HOST": "prod.example.com", "PORT": "5432", "EXTRA": "yes"}
ENV_C = {"HOST": "staging.example.com", "TIMEOUT": "30"}


# --- find_duplicates ---

def test_find_duplicates_detects_differing_values():
    result = find_duplicates([ENV_A, ENV_B])
    assert "HOST" in result


def test_find_duplicates_ignores_identical_values():
    # PORT is the same in both — should NOT appear as a duplicate conflict
    result = find_duplicates([ENV_A, ENV_B])
    assert "PORT" not in result


def test_find_duplicates_unique_key_not_reported():
    result = find_duplicates([ENV_A, ENV_B])
    assert "DEBUG" not in result
    assert "EXTRA" not in result


def test_find_duplicates_three_sources():
    result = find_duplicates([ENV_A, ENV_B, ENV_C])
    assert "HOST" in result
    assert len(result["HOST"]) == 3


def test_find_duplicates_empty_inputs():
    assert find_duplicates([]) == {}
    assert find_duplicates([{}]) == {}


# --- deduplicate: last strategy ---

def test_deduplicate_last_strategy_last_wins():
    result = deduplicate([ENV_A, ENV_B], strategy="last")
    assert result.resolved["HOST"] == "prod.example.com"


def test_deduplicate_last_strategy_unique_keys_preserved():
    result = deduplicate([ENV_A, ENV_B], strategy="last")
    assert "DEBUG" in result.resolved
    assert "EXTRA" in result.resolved


def test_deduplicate_last_strategy_has_duplicates():
    result = deduplicate([ENV_A, ENV_B], strategy="last")
    assert result.has_duplicates is True
    assert result.duplicate_count == 1


# --- deduplicate: first strategy ---

def test_deduplicate_first_strategy_first_wins():
    result = deduplicate([ENV_A, ENV_B], strategy="first")
    assert result.resolved["HOST"] == "localhost"


def test_deduplicate_first_strategy_unique_keys_preserved():
    result = deduplicate([ENV_A, ENV_B], strategy="first")
    assert result.resolved["EXTRA"] == "yes"


# --- deduplicate: error strategy ---

def test_deduplicate_error_strategy_raises_on_conflict():
    with pytest.raises(ValueError, match="HOST"):
        deduplicate([ENV_A, ENV_B], strategy="error")


def test_deduplicate_error_strategy_no_conflict_passes():
    env1 = {"A": "1"}
    env2 = {"B": "2"}
    result = deduplicate([env1, env2], strategy="error")
    assert result.resolved == {"A": "1", "B": "2"}


# --- metadata ---

def test_deduplicate_label_stored():
    result = deduplicate([ENV_A, ENV_B], label="test-run")
    assert result.label == "test-run"


def test_deduplicate_strategy_stored():
    result = deduplicate([ENV_A, ENV_B], strategy="first")
    assert result.strategy == "first"


def test_deduplicate_unknown_strategy_raises():
    with pytest.raises(ValueError, match="Unknown strategy"):
        deduplicate([ENV_A], strategy="random")


def test_deduplicate_no_duplicates_has_duplicates_false():
    result = deduplicate([{"X": "1"}, {"Y": "2"}])
    assert result.has_duplicates is False
    assert result.duplicate_count == 0
