#!/usr/bin/env python3
"""Audit staged files for test-only content before a public PR.

The optional --unstage mode removes identified test-only paths from Git's index
without deleting them from the working tree. Mixed files are reported for
manual hunk-level review and are never automatically unstaged.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


TEST_PATH_PARTS = {
    "test",
    "tests",
    "__tests__",
    "spec",
    "specs",
    "__snapshots__",
    "snapshots",
    "fixtures",
    "test-fixtures",
    "coverage",
    "test-results",
    "playwright-report",
    "cypress",
}

TEST_NAME_RE = re.compile(r"(?:^|[._/-])(test|spec)(?:[._/-]|$)", re.IGNORECASE)
TEST_SCRIPT_RE = re.compile(r"(?:^|/)scripts/test-[^/]+$", re.IGNORECASE)
ARTIFACT_PARTS = {"coverage", "test-results", "playwright-report", "cypress/screenshots"}
ARTIFACT_SUFFIXES = (".snap", ".log")
DOCUMENT_SUFFIXES = {".md", ".mdx"}


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def staged_paths(repo: Path) -> list[str]:
    output = run_git(repo, "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRTUXB")
    return [path for path in output.split("\0") if path]


def classify(path: str) -> str | None:
    normalized = path.replace("\\", "/").lower().strip("/")
    parts = set(normalized.split("/"))
    name = normalized.rsplit("/", 1)[-1]

    if parts & ARTIFACT_PARTS or name.endswith(ARTIFACT_SUFFIXES):
        return "test artifact"
    if TEST_SCRIPT_RE.search(normalized):
        return "test script"
    if parts & TEST_PATH_PARTS:
        return "test-only path"
    if Path(name).suffix.lower() not in DOCUMENT_SUFFIXES and TEST_NAME_RE.search(name):
        return "test/spec file"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository path (default: current directory)")
    parser.add_argument(
        "--unstage",
        action="store_true",
        help="remove identified test-only paths from the index; never deletes working-tree files",
    )
    args = parser.parse_args()
    repo = Path(args.repo).resolve()

    try:
        root = Path(run_git(repo, "rev-parse", "--show-toplevel").strip()).resolve()
        paths = staged_paths(root)
    except (OSError, RuntimeError) as error:
        print(f"PR CLEAN AUDIT: ERROR: {error}", file=sys.stderr)
        return 2

    findings = [(path, classify(path)) for path in paths]
    findings = [(path, reason) for path, reason in findings if reason]

    if not findings:
        print("PR CLEAN AUDIT: PASS - no test-only staged paths detected")
        return 0

    print("PR CLEAN AUDIT: test-only staged paths detected")
    for path, reason in findings:
        print(f"- {reason}: {path}")

    if not args.unstage:
        print("Run again with --unstage to remove these paths from the index without deleting files.")
        return 1

    try:
        run_git(root, "restore", "--staged", "--", *(path for path, _ in findings))
    except RuntimeError as error:
        print(f"PR CLEAN AUDIT: ERROR while unstaging: {error}", file=sys.stderr)
        return 2

    print("PR CLEAN AUDIT: UNSTAGED identified paths; working-tree files were preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
