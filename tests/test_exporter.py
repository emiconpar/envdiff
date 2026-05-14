"""Tests for envdiff.exporter module."""

from __future__ import annotations

import csv
import io
import json

import pytest

from envdiff.diff import EnvDiffResult
from envdiff.exporter import export_csv, export_json, export_shell, export


@pytest.fixture
def sample_result() -> EnvDiffResult:
    return EnvDiffResult(
        only_in_left={"OLD_KEY": "old_val"},
        only_in_right={"NEW_KEY": "new_val"},
        changed={"CHANGED": ("before", "after")},
        unchanged={"SAME": "same_val"},
    )


# --- JSON ---

def test_export_json_is_valid_json(sample_result):
    out = export_json(sample_result)
    data = json.loads(out)
    assert isinstance(data, dict)


def test_export_json_structure(sample_result):
    data = json.loads(export_json(sample_result))
    assert "only_in_left" in data
    assert "only_in_right" in data
    assert "changed" in data
    assert "unchanged" in data


def test_export_json_changed_has_left_right(sample_result):
    data = json.loads(export_json(sample_result))
    assert data["changed"]["CHANGED"] == {"left": "before", "right": "after"}


def test_export_json_indent(sample_result):
    out = export_json(sample_result, indent=4)
    assert "    " in out


# --- CSV ---

def test_export_csv_header(sample_result):
    out = export_csv(sample_result)
    reader = csv.reader(io.StringIO(out))
    header = next(reader)
    assert header == ["key", "status", "left", "right"]


def test_export_csv_removed_row(sample_result):
    out = export_csv(sample_result)
    assert "OLD_KEY,removed,old_val," in out


def test_export_csv_added_row(sample_result):
    out = export_csv(sample_result)
    assert "NEW_KEY,added,,new_val" in out


def test_export_csv_changed_row(sample_result):
    out = export_csv(sample_result)
    assert "CHANGED,changed,before,after" in out


# --- Shell ---

def test_export_shell_right_unsets_left_only(sample_result):
    out = export_shell(sample_result, target="right")
    assert "unset OLD_KEY" in out
    assert "export NEW_KEY='new_val'" in out


def test_export_shell_left_unsets_right_only(sample_result):
    out = export_shell(sample_result, target="left")
    assert "unset NEW_KEY" in out
    assert "export OLD_KEY='old_val'" in out


def test_export_shell_has_shebang(sample_result):
    out = export_shell(sample_result)
    assert out.startswith("#!/usr/bin/env sh")


# --- Dispatch ---

def test_export_dispatch_json(sample_result):
    out = export(sample_result, fmt="json")
    json.loads(out)  # should not raise


def test_export_dispatch_csv(sample_result):
    out = export(sample_result, fmt="csv")
    assert "status" in out


def test_export_dispatch_invalid_format(sample_result):
    with pytest.raises(ValueError, match="Unsupported export format"):
        export(sample_result, fmt="xml")  # type: ignore[arg-type]
