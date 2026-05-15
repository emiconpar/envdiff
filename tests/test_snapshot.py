"""Tests for envdiff.snapshot — save/load environment snapshots."""

import json
import os
import pytest

from envdiff.snapshot import (
    load_snapshot,
    save_snapshot,
    snapshot_metadata,
    SNAPSHOT_VERSION,
)


SAMPLE_ENV = {"APP_ENV": "production", "DB_HOST": "localhost", "PORT": "5432"}


@pytest.fixture()
def snapshot_path(tmp_path):
    return str(tmp_path / "env.snapshot.json")


def test_save_creates_file(snapshot_path):
    save_snapshot(SAMPLE_ENV, snapshot_path)
    assert os.path.exists(snapshot_path)


def test_save_and_load_roundtrip(snapshot_path):
    save_snapshot(SAMPLE_ENV, snapshot_path)
    loaded = load_snapshot(snapshot_path)
    assert loaded == SAMPLE_ENV


def test_save_stores_version(snapshot_path):
    save_snapshot(SAMPLE_ENV, snapshot_path)
    with open(snapshot_path) as fh:
        data = json.load(fh)
    assert data["version"] == SNAPSHOT_VERSION


def test_save_stores_label(snapshot_path):
    save_snapshot(SAMPLE_ENV, snapshot_path, label="staging")
    with open(snapshot_path) as fh:
        data = json.load(fh)
    assert data["label"] == "staging"


def test_save_stores_created_at(snapshot_path):
    save_snapshot(SAMPLE_ENV, snapshot_path)
    with open(snapshot_path) as fh:
        data = json.load(fh)
    assert "created_at" in data and data["created_at"]


def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_snapshot("/nonexistent/path/env.json")


def test_load_invalid_format(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(["not", "a", "dict"]))
    with pytest.raises(ValueError, match="Invalid snapshot format"):
        load_snapshot(str(bad))


def test_load_unsupported_version(tmp_path):
    snap = tmp_path / "old.json"
    snap.write_text(json.dumps({"version": 99, "env": {}}))
    with pytest.raises(ValueError, match="Unsupported snapshot version"):
        load_snapshot(str(snap))


def test_load_env_not_dict(tmp_path):
    snap = tmp_path / "bad_env.json"
    snap.write_text(json.dumps({"version": SNAPSHOT_VERSION, "env": "oops"}))
    with pytest.raises(ValueError, match="'env' field must be a JSON object"):
        load_snapshot(str(snap))


def test_snapshot_metadata_returns_fields(snapshot_path):
    save_snapshot(SAMPLE_ENV, snapshot_path, label="ci")
    meta = snapshot_metadata(snapshot_path)
    assert meta["label"] == "ci"
    assert meta["version"] == str(SNAPSHOT_VERSION)
    assert meta["created_at"] != ""


def test_snapshot_metadata_file_not_found():
    with pytest.raises(FileNotFoundError):
        snapshot_metadata("/no/such/file.json")
