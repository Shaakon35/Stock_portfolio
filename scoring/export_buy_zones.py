#!/usr/bin/env python3
# =========================================================================
# BUY-ZONE EXPORTER — accumulation bands for the dashboard's Plot tab
# =========================================================================
# WHY: the dashboard (docs/) is fully static and cannot run yfinance or the
# support-derivation logic in the browser. So — mirroring the plot_history /
# conviction pattern — this script computes each held single stock's buy zone
# ONCE, server-side, and writes docs/buy_zones.json for the page to shade.
#
# It reuses portfolio.buy_zones as the single source of truth:
#   * MANUAL_ZONES   — hand-set bands (ORCL / NOW / FICO), always win.
#   * auto-derived   — nearest confirmed support shelf, computed HERE from the
#                      already-committed docs/plot_history.json (WEEKLY closes),
#                      so the shaded band is derived from exactly the series the
#                      chart draws. Names with no confirmed support get no zone.
#
# The band is stored as ABSOLUTE prices {low, high}. The frontend rebases them
# to % of the chosen window's first price (matching the chart's rebase) when it
# shades — so one JSON works for every range without re-export.
#
# Usage:
#   PORTFOLIO_USE=ai python3 scoring/export_buy_zones.py
#   PORTFOLIO_USE=ai python3 scoring/export_buy_zones.py --history docs/plot_history.json
#
# NOT deterministic in the sense that MANUAL_ZONES/allocations can change, but
# it hits NO live feed — it reads only committed JSON, so re-running on the same
# inputs is byte-stable.

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_DEFAULT_HISTORY = _REPO_ROOT / "docs" / "plot_history.json"
_DEFAULT_OUT = _REPO_ROOT / "docs" / "buy_zones.json"

# WEEKLY-tuned support params (plot_history.json is 1wk closes: ~52 bars/yr).
# ~18 months of weekly bars for the recent regime; a swing low must be the
# lowest within +/- ~5 weeks; need ~9 months of history to attempt a zone.
_WK_LOOKBACK = 78   # ~18 months of weekly bars
_WK_SWING    = 5    # +/- 5 weeks defines a weekly swing low
_WK_MINBARS  = 39   # ~9 months of weekly bars minimum


def build_zones(history_path):
    """Return {ticker: {low, high, source, touches, note}} for held singles."""
    os.environ.setdefault("PORTFOLIO_USE", "ai")
    # Imported here so PORTFOLIO_USE is set before AI_allocations loads.
    from portfolio.buy_zones import (
        MANUAL_ZONES, derive_support_zone, held_single_stocks,
    )

    payload = json.loads(Path(history_path).read_text())
    hist = payload.get("history", {})

    singles = held_single_stocks()
    zones = {}
    n_manual = n_auto = n_none = 0

    for ticker in singles:
        if ticker in MANUAL_ZONES:
            low, high, note = MANUAL_ZONES[ticker]
            zones[ticker] = {
                "low": round(float(low), 2),
                "high": round(float(high), 2),
                "source": "manual",
                "touches": None,
                "note": note,
            }
            n_manual += 1
            continue

        entry = hist.get(ticker)
        if not entry or not entry.get("c"):
            n_none += 1
            continue

        closes = np.asarray(entry["c"], dtype=float)
        closes = closes[np.isfinite(closes)]
        zone = derive_support_zone(
            closes, lookback=_WK_LOOKBACK, swing_win=_WK_SWING,
            min_bars=_WK_MINBARS,
        )
        if zone is None:
            n_none += 1
            continue

        low, high, touches = zone
        zones[ticker] = {
            "low": low,
            "high": high,
            "source": "auto",
            "touches": touches,
            "note": f"retested support x{touches}",
        }
        n_auto += 1

    return zones, (len(singles), n_manual, n_auto, n_none)


def export_buy_zones(history_path, out_path):
    zones, (n_singles, n_manual, n_auto, n_none) = build_zones(history_path)
    out = {
        "generated_utc": datetime.now(timezone.utc)
                          .strftime("%Y-%m-%d %H:%M UTC"),
        "source_history": Path(history_path).name,
        "count": len(zones),
        "zones": zones,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    # sort_keys so the file is stable across runs (clean git diffs).
    with open(out_path, "w") as fh:
        json.dump(out, fh, separators=(",", ":"), sort_keys=True)
    print(f"wrote {out_path}  ({len(zones)} zones: "
          f"{n_manual} manual, {n_auto} auto; "
          f"{n_none}/{n_singles} singles without a zone)")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--history", default=str(_DEFAULT_HISTORY),
                    help="plot_history.json to derive auto zones from")
    ap.add_argument("--out", default=str(_DEFAULT_OUT),
                    help="output buy_zones.json path")
    args = ap.parse_args()
    export_buy_zones(args.history, args.out)


if __name__ == "__main__":
    main()
