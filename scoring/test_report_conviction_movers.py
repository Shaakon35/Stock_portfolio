#!/usr/bin/env python3
# =========================================================================
# Regression tests for the conviction-movers report's previous-snapshot
# resolver.
# =========================================================================
# WHY: the weekly refresh workflow once emailed a false all-zeros movers
# report. Root cause: actions/checkout defaults to a SHALLOW depth-1 clone, so
# git log contained only this run's own refresh commit. resolve_previous_from_
# git() then fell back to that single commit as "previous" and the report
# diffed the current snapshot against ITSELF — 0 movers, 0 held, 0 new.
#
# These tests pin the hardened behaviour: the resolver must never return a
# candidate whose content is identical to the current snapshot. When only the
# self-identical tip is available (the shallow-clone case) it must return
# (None, None) so the caller falls back to an honest baseline email instead of
# a silent self-diff.
#
# Pure stdlib (matches the scorer + report convention — no pip installs). Run:
#   python3 scoring/test_report_conviction_movers.py
# =========================================================================

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scoring.report_conviction_movers as R


def _snapshot(date_str, conv):
    """Build a minimal conviction.json payload with one ticker at `conv`."""
    return {
        "generated_utc": f"{date_str} 06:38 UTC",
        "csv": f"fundamentals_{date_str}.csv",
        "count": 1,
        "held_count": 1,
        "records": [
            {"ticker": "TEST", "conv": conv, "held": True,
             "F": 5.0, "V": 5.0, "C": 5.0},
        ],
    }


class _GitRepo:
    """A throwaway git repo with a controllable docs/conviction.json history."""

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._run("git", "init", "-q")
        self._run("git", "config", "user.email", "t@t.t")
        self._run("git", "config", "user.name", "t")
        (self.root / "docs").mkdir()

    def _run(self, *args):
        subprocess.run(args, cwd=self.root, check=True,
                       capture_output=True, text=True)

    def commit_snapshot(self, date_str, conv, subject=None):
        payload = _snapshot(date_str, conv)
        (self.root / "docs" / "conviction.json").write_text(
            json.dumps(payload))
        self._run("git", "add", "docs/conviction.json")
        self._run("git", "commit", "-q", "-m",
                  subject or f"Refresh conviction data ({date_str})")
        return payload

    def close(self):
        self._tmp.cleanup()


class ResolvePreviousTest(unittest.TestCase):
    def setUp(self):
        self.repo = _GitRepo()
        # Point the module's repo root at our throwaway repo.
        self._orig_root = R._REPO_ROOT
        R._REPO_ROOT = self.repo.root

    def tearDown(self):
        R._REPO_ROOT = self._orig_root
        self.repo.close()

    def _cur_by(self, payload):
        return R._records_by_ticker(payload)

    def test_shallow_clone_only_tip_returns_none(self):
        """Shallow depth-1 clone: only the current refresh commit exists.

        The resolver must NOT return that self-identical tip (which would diff
        the snapshot against itself); it must return (None, None) so the caller
        falls back to baseline mode.
        """
        cur = self.repo.commit_snapshot("2026-08-17", conv=8.0)
        content, sha = R.resolve_previous_from_git(
            "2026-08-17", self._cur_by(cur))
        self.assertIsNone(content)
        self.assertIsNone(sha)

    def test_prefers_earlier_different_dated_refresh(self):
        """Full history: pick the newest refresh with a different date stamp."""
        self.repo.commit_snapshot("2026-08-10", conv=6.0)
        prev = self.repo.commit_snapshot("2026-08-12", conv=7.0)
        cur = self.repo.commit_snapshot("2026-08-17", conv=8.0)
        content, sha = R.resolve_previous_from_git(
            "2026-08-17", self._cur_by(cur))
        self.assertIsNotNone(content)
        # Should be the 08-12 snapshot (newest with a DIFFERENT date), not the
        # 08-17 tip.
        self.assertEqual(
            R._records_by_ticker(content)["TEST"]["conv"],
            prev["records"][0]["conv"])

    def test_same_date_but_different_content_is_used(self):
        """A same-DATE earlier commit with genuinely different content (e.g. an
        intra-day re-run) is still a valid previous — it must be used via the
        fallback loop rather than skipped as a self-diff."""
        older = self.repo.commit_snapshot(
            "2026-08-17", conv=6.5, subject="Refresh conviction data (2026-08-17)")
        cur = self.repo.commit_snapshot(
            "2026-08-17", conv=8.0, subject="Refresh conviction data (2026-08-17)")
        content, sha = R.resolve_previous_from_git(
            "2026-08-17", self._cur_by(cur))
        self.assertIsNotNone(content)
        self.assertEqual(
            R._records_by_ticker(content)["TEST"]["conv"],
            older["records"][0]["conv"])

    def test_no_current_by_preserves_legacy_behaviour(self):
        """Without a current map (legacy callers) the resolver still returns a
        candidate — it just can't detect the self-diff. Guards against an
        accidental hard dependency on the new argument."""
        self.repo.commit_snapshot("2026-08-12", conv=7.0)
        cur = self.repo.commit_snapshot("2026-08-17", conv=8.0)
        content, sha = R.resolve_previous_from_git("2026-08-17")
        self.assertIsNotNone(content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
