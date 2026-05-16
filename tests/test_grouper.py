"""Tests for envdiff.grouper."""

import pytest
from envdiff.grouper import (
    group_by_prefix,
    group_by_mapping,
    group_sizes,
    largest_group,
    flatten_groups,
)


@pytest.fixture
def sample_env():
    return {
        "APP_HOST": "localhost",
        "APP_PORT": "8080",
        "DB_HOST": "db.local",
        "DB_PORT": "5432",
        "SECRET": "s3cr3t",
    }


def test_group_by_prefix_creates_correct_groups(sample_env):
    groups = group_by_prefix(sample_env)
    assert "APP" in groups
    assert "DB" in groups


def test_group_by_prefix_app_contains_correct_keys(sample_env):
    groups = group_by_prefix(sample_env)
    assert "APP_HOST" in groups["APP"]
    assert "APP_PORT" in groups["APP"]


def test_group_by_prefix_no_delimiter_goes_to_empty_group(sample_env):
    groups = group_by_prefix(sample_env)
    assert "" in groups
    assert "SECRET" in groups[""]


def test_group_by_prefix_depth_two():
    env = {"AWS_S3_BUCKET": "my-bucket", "AWS_S3_REGION": "us-east-1", "AWS_EC2_ID": "i-123"}
    groups = group_by_prefix(env, depth=2)
    assert "AWS_S3" in groups
    assert "AWS_EC2" in groups
    assert len(groups["AWS_S3"]) == 2


def test_group_by_prefix_custom_delimiter():
    env = {"APP.HOST": "localhost", "APP.PORT": "80", "DB.HOST": "db"}
    groups = group_by_prefix(env, delimiter=".")
    assert "APP" in groups
    assert "DB" in groups


def test_group_by_mapping_assigns_correct_group(sample_env):
    mapping = {"database": ["DB_HOST", "DB_PORT"], "app": ["APP_HOST", "APP_PORT"]}
    groups = group_by_mapping(sample_env, mapping)
    assert "DB_HOST" in groups["database"]
    assert "APP_PORT" in groups["app"]


def test_group_by_mapping_unknown_key_goes_to_default(sample_env):
    mapping = {"app": ["APP_HOST", "APP_PORT"]}
    groups = group_by_mapping(sample_env, mapping)
    assert "SECRET" in groups["other"]
    assert "DB_HOST" in groups["other"]


def test_group_by_mapping_custom_default_group(sample_env):
    mapping = {"app": ["APP_HOST"]}
    groups = group_by_mapping(sample_env, mapping, default_group="misc")
    assert "misc" in groups
    assert "SECRET" in groups["misc"]


def test_group_sizes_returns_correct_counts(sample_env):
    groups = group_by_prefix(sample_env)
    sizes = group_sizes(groups)
    assert sizes["APP"] == 2
    assert sizes["DB"] == 2
    assert sizes[""] == 1


def test_largest_group_identifies_correct_group():
    groups = {"a": {"X": "1", "Y": "2", "Z": "3"}, "b": {"W": "4"}}
    assert largest_group(groups) == "a"


def test_largest_group_empty_returns_none():
    assert largest_group({}) is None


def test_flatten_groups_restores_all_keys(sample_env):
    groups = group_by_prefix(sample_env)
    flat = flatten_groups(groups)
    assert flat == sample_env


def test_flatten_groups_empty_input():
    assert flatten_groups({}) == {}
