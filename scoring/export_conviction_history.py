#!/usr/bin/env python3
# =========================================================================
# CONVICTION-HISTORY EXPORTER — score series for the dashboard Conviction tab
# =========================================================================
# WHY: the GitHub Pages dashboard is fully static. The browser cannot run the
# Python scorer, so this script precomputes the conviction score across every
# dated fundamentals snapshot and writes docs/conviction_history.json.
#
# The exporter deliberately reuses score_holdings.build_results(), so each point
# is scored by the same deterministic engine as docs/conviction.json. Missing
# historical rows are skipped rather than plotted as fake zero scores.
#
# Usage:
#   PORTFOLIO_USE=ai python3 scoring/export_conviction_history.py

import argparse
import datetime as _dt
import json
import re
from pathlib import Path

import score_holdings as S


_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_FUND_DIR = _REPO_ROOT / "scoring"
_DEFAULT_OUT = _REPO_ROOT / "docs" / "conviction_history.json"
_CSV_RE = re.compile(r"fundamentals_(\d{4}-\d{2}-\d{2})\.csv$")
_LAYER_KEY = {"FUND": "F", "VAL": "V", "CYCLE": "C"}


def _dated_csvs(fund_dir):
    """Return [(date, path)] for fundamentals_YYYY-MM-DD.csv snapshots."""
    out = []
    for p in Path(fund_dir).glob("fundamentals_*.csv"):
        m = _CSV_RE.match(p.name)
        if m:
            out.append((m.group(1), p))
    return sorted(out)


def export_conviction_history(fund_dir=_DEFAULT_FUND_DIR, out_path=_DEFAULT_OUT):
    """Score every dated fundamentals snapshot and write the dashboard payload."""
    snapshots = _dated_csvs(fund_dir)
    history = {}
    dates = []

    for date, csv_path in snapshots:
        dates.append(date)
        rows = S.build_results(str(csv_path))
        for r in rows:
            if not r.get("has_data"):
                continue
            tk = r["ticker"]
            entry = history.setdefault(tk, {
                "t": [], "c": [], "F": [], "V": [], "C": [],
                "wave": r.get("wave"),
                "strategy": r.get("strategy"),
                "held": bool(r.get("held")) and r.get("book_pct", 0) > 0,
                "book_pct": round(r.get("book_pct", 0), 2),
            })
            entry["t"].append(date)
            entry["c"].append(round(r["conviction_unified"], 2))
            entry["F"].append(round(r["layers"]["FUND"], 1))
            entry["V"].append(round(r["layers"]["VAL"], 1))
            entry["C"].append(round(r["layers"]["CYCLE"], 1))
            # Keep the latest metadata in case wave/held status changed.
            entry["wave"] = r.get("wave")
            entry["strategy"] = r.get("strategy")
            entry["held"] = bool(r.get("held")) and r.get("book_pct", 0) > 0
            entry["book_pct"] = round(r.get("book_pct", 0), 2)

    ordered = dict(sorted(history.items()))
    payload = {
        "generated_utc": _dt.datetime.now(_dt.timezone.utc)
                            .strftime("%Y-%m-%d %H:%M UTC"),
        "source": "scoring/fundamentals_YYYY-MM-DD.csv",
        "snapshot_count": len(snapshots),
        "dates": dates,
        "count": len(ordered),
        "history": ordered,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    print(f"wrote {out_path}  ({len(ordered)} names, "
          f"{len(snapshots)} snapshots)")
    return payload


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fund-dir", default=str(_DEFAULT_FUND_DIR),
                    help="directory containing fundamentals_YYYY-MM-DD.csv")
    ap.add_argument("--out", default=str(_DEFAULT_OUT),
                    help="output conviction_history.json path")
    args = ap.parse_args()
    export_conviction_history(args.fund_dir, args.out)


if __name__ == "__main__":
    main()
