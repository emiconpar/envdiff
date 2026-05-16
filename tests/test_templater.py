"""Tests for envdiff.templater and envdiff.template_report."""

from __future__ import annotations

import pytest

from envdiff.templater import (
    find_unrendered,
    render_env_template,
    render_template,
    template_summary,
)
from envdiff.template_report import format_template_report, template_summary_line


# ---------------------------------------------------------------------------
# render_template
# ---------------------------------------------------------------------------

def test_render_template_replaces_known_key():
    result = render_template("hello {{ NAME }}", {"NAME": "world"})
    assert result == "hello world"


def test_render_template_leaves_unknown_key():
    result = render_template("{{ MISSING }}", {})
    assert result == "{{ MISSING }}"


def test_render_template_multiple_placeholders():
    result = render_template("{{ A }}-{{ B }}", {"A": "foo", "B": "bar"})
    assert result == "foo-bar"


def test_render_template_no_placeholders():
    assert render_template("plain value", {"X": "1"}) == "plain value"


def test_render_template_whitespace_inside_braces():
    result = render_template("{{  KEY  }}", {"KEY": "val"})
    assert result == "val"


# ---------------------------------------------------------------------------
# render_env_template
# ---------------------------------------------------------------------------

def test_render_env_template_renders_values():
    template_env = {"URL": "http://{{ HOST }}:{{ PORT }}", "NAME": "app"}
    context = {"HOST": "localhost", "PORT": "8080"}
    result = render_env_template(template_env, context)
    assert result["URL"] == "http://localhost:8080"
    assert result["NAME"] == "app"


def test_render_env_template_keys_unchanged():
    template_env = {"{{ KEY }}": "value"}  # key with placeholder — key never touched
    result = render_env_template(template_env, {"KEY": "X"})
    assert "{{ KEY }}" in result


# ---------------------------------------------------------------------------
# find_unrendered
# ---------------------------------------------------------------------------

def test_find_unrendered_returns_keys_with_placeholders():
    env = {"A": "resolved", "B": "still {{ MISSING }}"}
    assert find_unrendered(env) == ["B"]


def test_find_unrendered_empty_when_all_resolved():
    env = {"A": "ok", "B": "also ok"}
    assert find_unrendered(env) == []


# ---------------------------------------------------------------------------
# template_summary
# ---------------------------------------------------------------------------

def test_template_summary_rendered_count():
    original = {"A": "{{ X }}", "B": "static"}
    rendered = {"A": "hello", "B": "static"}
    s = template_summary(original, rendered, label="test")
    assert s["rendered_count"] == 1
    assert s["unrendered_count"] == 0
    assert "A" in s["rendered_keys"]


def test_template_summary_unrendered_count():
    original = {"A": "{{ X }}"}
    rendered = {"A": "{{ X }}"}  # not resolved
    s = template_summary(original, rendered)
    assert s["unrendered_count"] == 1


# ---------------------------------------------------------------------------
# format_template_report
# ---------------------------------------------------------------------------

def test_format_report_contains_label():
    original = {"A": "{{ X }}"}
    rendered = {"A": "value"}
    s = template_summary(original, rendered, label="prod")
    report = format_template_report(s, color=False)
    assert "prod" in report


def test_format_report_shows_rendered_key():
    original = {"DB_URL": "{{ HOST }}"}
    rendered = {"DB_URL": "localhost"}
    s = template_summary(original, rendered)
    report = format_template_report(s, color=False)
    assert "DB_URL" in report


def test_template_summary_line_all_resolved():
    original = {"A": "{{ X }}"}
    rendered = {"A": "done"}
    s = template_summary(original, rendered, label="env")
    line = template_summary_line(s, color=False)
    assert "all resolved" in line


def test_template_summary_line_with_unrendered():
    original = {"A": "{{ X }}"}
    rendered = {"A": "{{ X }}"}
    s = template_summary(original, rendered, label="env")
    line = template_summary_line(s, color=False)
    assert "unrendered" in line
