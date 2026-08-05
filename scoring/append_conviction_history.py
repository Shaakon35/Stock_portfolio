#!/usr/bin/env python3
"""Append a dated CONV snapshot to docs/conviction_history.json.

The dashboard's conviction.json is a POINT-IN-TIME view — it is overwritten on
every refresh, so it carries no history. This script accumulates one dated
CONV reading per ticker into a long-lived time-series file, so the score's
trajectory (not just its current value) becomes visible over time.

It is DETERMINISTIC and IDEMPOTENT per snapshot date: the date is derived from
the fundamentals CSV filename (fundamentals_<YYYY-MM-DD>.csv), NOT from "today",
so re-scoring an old snapshot writes to that snapshot's date and re-running the
same snapshot overwrites its entry in place rather than duplicating it. That
also makes it safe to seed the file from the committed dated snapshots in one
pass (see --seed-all).

Stored per (ticker, date): conv + the F/V/C layers + binding layer + coverage.
Price is NOT stored here — docs/plot_history.json already holds prices; this
file is purely the engine-produced conviction trajectory.

Usage:
    # append the current (newest) snapshot's scores
    PORTFOLIO_USE=ai python3 scoring/append_conviction_history.py

    # score a specific snapshot into its own date
    PORTFOLIO_USE=ai python3 scoring/append_conviction_history.py \
        --csv scoring/fundamentals_2026-06-25.csv

    # one-shot backfill from every committed dated snapshot
    PORTFOLIO_USE=ai python3 scoring/append_conviction_history.py --seed-all
"""
import argparse
import datetime as _dt
import glob
import json
import os
import re
import sys
from pathlib import Path

# allow "python3 scoring/append_conviction_history.py" from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scoring.score_holdings as S  # noqa: E402

HIST_PATH = Path(__file__).resolve().parent.parent / "docs" / "conviction_history.json"
_DATE_RE = re.compile(r"fundamentals_(\d{4}-\d{2}-\d{2})\.csv$")


def snapshot_date(csv_path):
    """Derive the snapshot's date (YYYY-MM-DD) from its filename.

    The date is the snapshot's own date, never wall-clock 'today', so seeding
    old snapshots lands each reading on the correct historical date.
    """
    m = _DATE_RE.search(str(csv_path))
    if not m:
        raise SystemExit(
            f"cannot derive a date from {csv_path!r} — expected "
            f"'fundamentals_<YYYY-MM-DD>.csv'"
        )
    return m.group(1)


def snapshot_scores(csv_path):
    """Return {ticker: {conv,F,V,C,bind,cov}} for one fundamentals snapshot."""
    _LAYER_KEY = {"FUND": "F", "VAL": "V", "CYCLE": "C"}
    out = {}
    for r in S.build_results(csv_path):
        if not r["has_data"]:
            # no-fundamentals rows (e.g. a physical-commodity trust) have no
            # meaningful CONV to trend — skip them from the history.
            continue
        out[r["ticker"]] = {
            "conv": round(r["conviction_unified"], 2),
            "F": round(r["layers"]["FUND"], 1),
            "V": round(r["layers"]["VAL"], 1),
            "C": round(r["layers"]["CYCLE"], 1),
            "bind": _LAYER_KEY.get(r["binding"], r["binding"]),
            "cov": round(r["coverage"] * 100),
        }
    return out


def load_history():
    if HIST_PATH.exists():
        with open(HIST_PATH) as fh:
            return json.load(fh)
    return {"schema": 1, "dates": [], "history": {}}


def append_snapshot(doc, date, scores):
    """Merge one dated snapshot into the history doc (idempotent per date)."""
    hist = doc.setdefault("history", {})
    for ticker, metrics in scores.items():
        hist.setdefault(ticker, {})[date] = metrics
    dates = set(doc.get("dates", [])) | {date}
    doc["dates"] = sorted(dates)
    return doc


def save_history(doc):
    doc["generated_utc"] = (
        _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    )
    doc["ticker_count"] = len(doc.get("history", {}))
    doc["snapshot_count"] = len(doc.get("dates", []))
    HIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HIST_PATH, "w") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)


def all_snapshots():
    """Every committed dated fundamentals snapshot, oldest first."""
    root = Path(__file__).resolve().parent
    files = sorted(glob.glob(str(root / "fundamentals_*.csv")))
    return [f for f in files if _DATE_RE.search(f)]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=None,
                    help="fundamentals snapshot to score (default: newest)")
    ap.add_argument("--seed-all", action="store_true",
                    help="backfill from every committed dated snapshot")
    args = ap.parse_args()

    if os.environ.get("PORTFOLIO_USE") != "ai":
        raise SystemExit("set PORTFOLIO_USE=ai (the scorer requires it)")

    doc = load_history()

    if args.seed_all:
        csvs = all_snapshots()
        for csv_path in csvs:
            date = snapshot_date(csv_path)
            scores = snapshot_scores(csv_path)
            append_snapshot(doc, date, scores)
            print(f"seeded {date}: {len(scores)} names  from {Path(csv_path).name}")
    else:
        csv_path = args.csv or S.default_csv()
        date = snapshot_date(csv_path)
        scores = snapshot_scores(csv_path)
        append_snapshot(doc, date, scores)
        print(f"appended {date}: {len(scores)} names  from {Path(csv_path).name}")

    save_history(doc)
    print(f"wrote {HIST_PATH.relative_to(HIST_PATH.parent.parent)}  "
          f"({doc['ticker_count']} tickers, {doc['snapshot_count']} snapshots: "
          f"{doc['dates'][0]}..{doc['dates'][-1]})")


if __name__ == "__main__":
    main()
