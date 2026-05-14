"""Command-line interface for envdiff."""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from envdiff.diff import diff_envs, has_differences, summary
from envdiff.exporter import export, OutputFormat
from envdiff.filter import filter_by_prefix, filter_by_regex, select_keys
from envdiff.formatter import format_diff, format_summary
from envdiff.parser import parse_env_file
from envdiff.process_env import get_current_env, get_process_env


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="envdiff",
        description="Compare environment variable sets across .env files and processes.",
    )
    p.add_argument("left", help="Left source: path to .env file or PID")
    p.add_argument("right", help="Right source: path to .env file, PID, or 'current'")
    p.add_argument("--prefix", metavar="PREFIX", action="append", dest="prefixes",
                   help="Keep only keys with this prefix (repeatable)")
    p.add_argument("--regex", metavar="PATTERN",
                   help="Keep only keys matching this regex")
    p.add_argument("--keys", metavar="KEY", nargs="+",
                   help="Keep only these specific keys")
    p.add_argument("--no-color", action="store_true", help="Disable colored output")
    p.add_argument("--summary", action="store_true", help="Print summary line only")
    p.add_argument(
        "--export",
        choices=["json", "csv", "shell"],
        metavar="FORMAT",
        help="Export diff in FORMAT (json, csv, shell) instead of human-readable output",
    )
    p.add_argument(
        "--export-target",
        choices=["left", "right"],
        default="right",
        help="Shell export target direction (default: right)",
    )
    return p


def _load_env(source: str) -> dict[str, str]:
    if source == "current":
        return get_current_env()
    if source.isdigit():
        return get_process_env(int(source))
    return parse_env_file(source)


def _apply_filters(
    env: dict[str, str],
    prefixes: Optional[list[str]],
    regex: Optional[str],
    keys: Optional[list[str]],
) -> dict[str, str]:
    if prefixes:
        env = filter_by_prefix(env, prefixes)
    if regex:
        env = filter_by_regex(env, regex)
    if keys:
        env = select_keys(env, keys)
    return env


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    left_env = _load_env(args.left)
    right_env = _load_env(args.right)

    left_env = _apply_filters(left_env, args.prefixes, args.regex, args.keys)
    right_env = _apply_filters(right_env, args.prefixes, args.regex, args.keys)

    result = diff_envs(left_env, right_env)

    if args.export:
        fmt: OutputFormat = args.export  # type: ignore[assignment]
        kwargs = {"target": args.export_target} if fmt == "shell" else {}
        print(export(result, fmt=fmt, **kwargs), end="")
        return 0

    if args.summary:
        print(format_summary(summary(result)))
    else:
        color = not args.no_color
        print(format_diff(result, left_label=args.left, right_label=args.right, color=color))

    return 1 if has_differences(result) else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
