#!/usr/bin/env python3
"""Point-in-time 2023 BACKTEST harness for the scoring engine.

Production equivalent:

    PORTFOLIO_USE=ai python3 scoring/score_holdings.py \
        --by-strategy --watchlist --sync-csv

This script reproduces that command's OUTPUT for an end-2023 vantage point,
reusing the REAL engine (`render_by_strategy`, `dca_*`, `conviction`, the layer
model, ...) so the scoring is byte-for-byte the same logic production runs. Only
the *inputs* are swapped for a frozen 2023 snapshot.

WHY A SEPARATE HARNESS (and not just `score_holdings.py --csv ...`):

  * The production `--sync-csv` flag LIVE-SCRAPES stockanalysis.com and writes
    fresh fundamentals into the CSV. In a backtest that is exactly wrong — it
    would inject *today's* (2026) numbers and destroy the point-in-time
    integrity the whole exercise depends on (see AGENTS.md: "NO post-2023
    data"). So here `--sync-csv` is REDEFINED as a point-in-time COVERAGE CHECK:
    it verifies the committed 2023 snapshot covers the backtest universe and
    reports any gaps, but never touches the network. Same intent (make sure the
    CSV is complete before scoring), zero look-ahead.

  * The backtest universe is a fixed historical set, not the live AI-allocation
    book. Batch-1 mega-caps map to the HELD book; batch-2 (#82-101) map to the
    WATCHLIST, so `--watchlist` adds the watchlist names on top of held exactly
    as production does.

The two frozen snapshots live next to this file and are committed to git:
    scoring/backtest/fundamentals_2023_held.csv       (held book)
    scoring/backtest/fundamentals_2023_watchlist.csv  (watchlist)
They are deliberately OUTSIDE scoring/ proper so the engine's default_csv()
glob (scoring/fundamentals_*.csv) never picks them up by accident.

Run:
    cd /workspaces/Stock_portfolio && PORTFOLIO_USE=ai python3 \
        scoring/backtest/score_holdings_2023.py --by-strategy --watchlist --sync-csv
"""
import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PORTFOLIO_USE", "ai")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import scoring.score_holdings as S  # noqa: E402

HERE = Path(__file__).resolve().parent
CSV_HELD = HERE / "fundamentals_2023_held.csv"
CSV_WATCH = HERE / "fundamentals_2023_watchlist.csv"

# ---------------------------------------------------------------------------
# Frozen end-2023 portfolio map (book%, strategy) — the backtest's stand-in for
# portfolio.AI_allocations as it would have looked in 2023. Held = batch-1
# mega-caps; watchlist = batch-2 (#82-101).
# ---------------------------------------------------------------------------
HELD_BOOK = {
    "NVDA": 12.33, "AAPL": 11.02, "MSFT": 7.32, "AMZN": 6.62, "GOOGL": 5.62,
    "GOOG": 5.22, "AVGO": 4.59, "TSLA": 3.77, "META": 3.69, "MU": 3.38,
    "WMT": 2.43, "AMD": 2.25, "ASML": 1.83, "INTC": 1.70, "AMAT": 1.32,
    "LRCX": 1.25, "CSCO": 1.19, "COST": 1.12, "ARM": 0.94, "KLAC": 0.86,
}
WATCH_BOOK = {
    "EXC": 0.13, "MCHP": 0.13, "ODFL": 0.12, "KDP": 0.12, "CCEP": 0.12,
    "TTWO": 0.12, "IDXX": 0.11, "ADSK": 0.11, "PYPL": 0.10, "ALNY": 0.10,
    "AXON": 0.10, "TRI": 0.10, "PAYX": 0.09, "ROP": 0.09, "WDAY": 0.08,
    "GEHC": 0.08, "MSTR": 0.08, "CPRT": 0.07, "KHC": 0.07, "DXCM": 0.07,
}

STRATEGY = {
    # held (batch 1)
    "AAPL": "dca", "MSFT": "dca", "GOOGL": "dca", "GOOG": "dca", "AMZN": "dca",
    "META": "dca", "WMT": "dca", "COST": "dca", "CSCO": "dca",
    "NVDA": "cycle", "AVGO": "cycle", "AMD": "cycle", "ASML": "cycle",
    "INTC": "cycle", "AMAT": "cycle", "LRCX": "cycle", "KLAC": "cycle",
    "MU": "cycle", "ARM": "cycle", "TSLA": "cycle",
    # watchlist (batch 2)
    "EXC": "dca", "KDP": "dca", "CCEP": "dca", "IDXX": "dca", "TRI": "dca",
    "PAYX": "dca", "ROP": "dca", "GEHC": "dca", "KHC": "dca", "ODFL": "dca",
    "CPRT": "dca",
    "MCHP": "cycle",
    "TTWO": "catalyst", "ADSK": "catalyst", "PYPL": "catalyst",
    "ALNY": "catalyst", "AXON": "catalyst", "WDAY": "catalyst",
    "MSTR": "catalyst", "DXCM": "catalyst",
}

# Point-in-time engine tags as of end-2023 (cycle position / bottleneck owner
# tags / deep-cyclical PEG-trap softening). Injected as module globals so the
# REAL engine reads 2023 values, identical to how it reads CYCLE_POS etc. live.
CYCLE_2023 = {
    "NVDA": "Early", "AMD": "Early", "AVGO": "Mid", "ASML": "Early",
    "AMAT": "Mid", "LRCX": "Mid", "KLAC": "Mid", "MU": "Early",
    "ARM": "Early", "TSLA": "Mid", "INTC": "Mid", "MSFT": "Mid",
    "GOOGL": "Mid", "GOOG": "Mid", "META": "Mid", "AMZN": "Mid",
    "AAPL": "Mid/Late", "CSCO": "Late", "COST": "Mid", "WMT": "Mid",
    "MCHP": "Early", "TTWO": "Early", "ADSK": "Mid", "PYPL": "Mid",
    "ALNY": "Early", "AXON": "Early", "WDAY": "Mid", "MSTR": "Binary",
    "DXCM": "Early", "EXC": "Late", "KDP": "Mid", "CCEP": "Mid",
    "IDXX": "Mid", "TRI": "Mid", "PAYX": "Mid", "ROP": "Mid",
    "GEHC": "Mid", "KHC": "Late", "ODFL": "Mid", "CPRT": "Mid",
}
NECK_2023 = {
    "NVDA": 1.0, "ASML": 1.0, "AVGO": 1.0, "AMAT": 1.0, "LRCX": 1.0,
    "KLAC": 1.0, "ARM": 1.0, "MU": 0.5, "AMD": 0.5, "TSLA": 0.5,
    "MSFT": 0.5, "GOOGL": 0.5, "GOOG": 0.5, "META": 0.5, "AMZN": 0.5,
    "AAPL": 0.5, "COST": 0.5, "WMT": 0.5, "CSCO": 0.5, "INTC": 0.5,
    "IDXX": 1.0, "ODFL": 1.0, "CPRT": 1.0, "ROP": 0.5, "AXON": 1.0,
    "TRI": 0.5, "PAYX": 0.5, "ADSK": 1.0, "WDAY": 0.5, "DXCM": 0.5,
    "ALNY": 1.0, "MCHP": 0.5, "TTWO": 0.5, "PYPL": 0.5, "GEHC": 0.5,
    "EXC": 0.5, "KDP": 0.5, "CCEP": 0.5, "KHC": 0.5, "MSTR": 0.0,
}
# Deep cyclicals: PEG distorted by cycle position -> soften the valuation
# penalty (the trough/peak-PEG trap; the LRCX fix).
DEEP_CYCLICAL = {"MU", "LRCX", "AMAT", "KLAC", "ASML", "INTC", "MCHP"}


def backtest_rows(include_watchlist):
    """Stand-in for portfolio_rows(): build the frozen 2023 universe in the
    exact `info` shape render_by_strategy / the engine expects."""
    rows = {}
    for t, book in HELD_BOOK.items():
        rows[t] = {"ticker": t, "wave": "23", "sub": 0.0, "book_pct": book,
                   "etf_pct": 0.0, "strategy": STRATEGY[t], "held": True,
                   "cagr_lo": None, "cagr_hi": None, "cagr_mid": None,
                   "wl_pos": None}
    if include_watchlist:
        for t, book in WATCH_BOOK.items():
            rows[t] = {"ticker": t, "wave": "WL", "sub": 0.0, "book_pct": book,
                       "etf_pct": 0.0, "strategy": STRATEGY[t], "held": False,
                       "cagr_lo": None, "cagr_hi": None, "cagr_mid": None,
                       "wl_pos": CYCLE_2023.get(t)}
    return rows


def coverage_check(fund, universe):
    """Point-in-time replacement for --sync-csv: NO network. Verify the frozen
    snapshot covers the backtest universe; report gaps for hand entry. Returns
    the list of names missing a fundamentals row."""
    missing = [t for t in universe if t not in fund]
    print("\n=== POINT-IN-TIME COVERAGE CHECK (--sync-csv, 2023 backtest) ===")
    print("    No live scrape (a 2023 backtest must not ingest 2026 data); this")
    print("    verifies the frozen snapshot covers the universe instead.")
    print(f"    universe={len(universe)}  covered={len(universe) - len(missing)}"
          f"  missing={len(missing)}")
    if missing:
        print("  (!) no 2023 fundamentals row for: " + ", ".join(missing))
        print("      add them to the appropriate scoring/backtest/"
              "fundamentals_2023_*.csv")
    else:
        print("  OK — every name in the backtest universe has a 2023 row.")
    return missing


def main():
    ap = argparse.ArgumentParser(
        description="Point-in-time 2023 backtest of the scoring engine "
                    "(mirrors score_holdings.py --by-strategy --watchlist "
                    "--sync-csv).")
    ap.add_argument("--by-strategy", action="store_true",
                    help="group output by strategy mode (DCA on quality+price, "
                         "cycle/catalyst on the growth/discipline grid) — the "
                         "real engine render_by_strategy")
    ap.add_argument("--watchlist", action="store_true",
                    help="also score the 2023 WATCHLIST (batch-2 names #82-101)")
    ap.add_argument("--sync-csv", action="store_true",
                    help="point-in-time COVERAGE CHECK of the frozen snapshot "
                         "(no network; a backtest must not scrape live data)")
    args = ap.parse_args()

    # Inject the frozen 2023 owner tags so the REAL engine reads 2023 values.
    S.CYCLE_POS = CYCLE_2023
    S.BOTTLENECK = NECK_2023
    S._CYCLICAL = DEEP_CYCLICAL

    port = backtest_rows(include_watchlist=args.watchlist)

    # Load the frozen snapshot(s): held always; watchlist only when requested
    # (mirrors production loading the held book + watchlist if --watchlist).
    fund = dict(S.load_fundamentals(str(CSV_HELD)))
    if args.watchlist:
        fund.update(S.load_fundamentals(str(CSV_WATCH)))

    if args.sync_csv:
        coverage_check(fund, list(port))

    # ----- score every name through the REAL engine path -----
    results = []
    for t, info in port.items():
        f = fund.get(t, {})
        eight, parts8, eps_f = S.score_8point(t, f, info)
        g10, partsg = S.score_growth(t, f, info)
        layers, binding = S.layer_scores(t, f, info)
        cov = S._coverage(f)
        peak = S.peak_trap(t, f, info)
        conv = S.conviction(g10, eight, layers, layers[binding], peak, cov)
        q10, rich, _ = S.dca_quality(t, f)
        conv_dca = S.dca_conviction(q10, layers, layers[binding], rich, cov)
        conv_unified = conv_dca if info.get("strategy") == "dca" else conv
        results.append({**info, "eight": eight, "growth10": g10, "blend": None,
                        "quad": S.quadrant(eight, g10), "eps_f": eps_f,
                        "p8": parts8, "pg": partsg, "has_data": t in fund,
                        "coverage": cov, "conviction": conv,
                        "conviction_dca": conv_dca,
                        "conviction_unified": conv_unified,
                        "layers": layers, "binding": binding, "peak": peak})

    results.sort(key=lambda r: -r["conviction_unified"])

    # Give render_by_strategy the args object it reads (.csv for the header).
    args.csv = "fundamentals_2023 (held + watchlist backtest)"
    if args.by_strategy:
        S.render_by_strategy(results, fund, args)
    else:
        print("\n(use --by-strategy for the grouped strategy view)")


if __name__ == "__main__":
    main()
