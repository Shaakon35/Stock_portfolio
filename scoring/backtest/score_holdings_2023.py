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

FULL UNIVERSE MODE (--universe):
    Scores the ENTIRE AI-allocation universe (204 backtestable names) from
    fundamentals_2023_universe.csv, each graded in its 2023-VINTAGE strategy
    (universe_2023.py: current strategy + documented 2023 overrides — e.g. NVDA
    was `cycle` in 2023, and SNOW/NU/SHOP/COIN/SOFI were `catalyst` turnaround
    bets then, not today's compounders). Post-2023 IPOs / no-fundamentals names
    are excluded (SKIP_NOT_2023). Forward estimates + 200DMA are blank on the
    historical pages, so the engine drops + reweights those sub-scores (data%
    reads ~70%, [GAP] flagged) and the score rests on the obtainable
    point-in-time fundamentals.

        PORTFOLIO_USE=ai python3 scoring/backtest/score_holdings_2023.py \
            --universe --by-strategy --sync-csv
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
CSV_UNIVERSE = HERE / "fundamentals_2023_universe.csv"


def _load_universe_module():
    """Import universe_2023.py by path (avoids the scoring/backtest.py name
    collision that shadows the package)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "universe_2023", HERE / "universe_2023.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

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

# ---------------------------------------------------------------------------
# REALIZED PRICES (for the optional --with-returns columns). These are OUTCOME
# data (post-2023) used ONLY to score the engine's 2023 calls — they never feed
# the scoring itself, so they cannot bias it.
#
#   ANCHOR_PX : split-adjusted "Last Close Price" from the source FY2023 ratios
#               column (same fiscal date the fundamentals came from).
#   CURR_PX   : "today" (2026-06-27) price from the live feed.
#   MAX_CLOSE : best RELIABLE fiscal-year-end close across 2023->now.
#
# DATA-INTEGRITY NOTE: this environment's LIVE feed is corrupt for many semis
# (reads 2-4x reality; MU ~10x; MSFT/META read LOW; KLAC whole series /10). The
# historical fiscal-year-end closes are internally consistent and reliable, so:
#   * RET23>now is FLAGGED (!) when the live feed is corrupt -> not a real return.
#   * MAX_CLOSE EXCLUDES the corrupt live column -> RET23>max is the trustworthy
#     realized-exit return (conservative: year-end closes understate intra-year
#     highs). Whole-series-corrupt names (MU, KLAC) are flagged outright.
# ---------------------------------------------------------------------------
ANCHOR_PX = {
    "NVDA": 61.03, "AAPL": 171.21, "MSFT": 340.54, "AMZN": 151.94,
    "GOOGL": 138.46, "GOOG": 138.46, "AVGO": 83.84, "TSLA": 248.48,
    "META": 353.96, "MU": 69.94, "AMD": 147.41, "ASML": 756.92,
    "INTC": 50.25, "AMAT": 131.30, "LRCX": 64.29, "CSCO": 52.09,
    "COST": 544.25, "ARM": 124.99, "KLAC": 48.50, "WMT": 55.08,
    "EXC": 35.90, "MCHP": 83.78, "ODFL": 202.67, "KDP": 33.32, "CCEP": 66.74,
    "TTWO": 119.30, "IDXX": 555.05, "ADSK": 253.81, "PYPL": 61.41,
    "ALNY": 191.41, "AXON": 258.33, "TRI": 196.56, "PAYX": 104.93,
    "ROP": 545.17, "WDAY": 291.07, "GEHC": 77.32, "MSTR": 63.16,
    "CPRT": 44.20, "KHC": 36.98, "DXCM": 124.09,
}
MAX_CLOSE = {
    # batch 1 -- corrupt live column dropped from the max
    "NVDA": 187.67, "AAPL": 283.78, "MSFT": 497.41, "AMZN": 232.69,
    "GOOGL": 337.39, "GOOG": 337.39, "AVGO": 369.63, "TSLA": 449.72,
    "META": 660.09, "MU": 122.00, "AMD": 214.16, "ASML": 1069.86,
    "INTC": 50.25, "AMAT": 228.75, "LRCX": 106.49, "CSCO": 68.69,
    "COST": 952.54, "ARM": 151.28, "KLAC": 89.57, "WMT": 119.14,
    # batch 2 -- live column here was reliable
    "EXC": 47.40, "MCHP": 89.71, "ODFL": 218.79, "KDP": 33.40, "CCEP": 101.59,
    "TTWO": 238.53, "IDXX": 676.53, "ADSK": 311.34, "PYPL": 85.35,
    "ALNY": 397.65, "AXON": 594.32, "TRI": 234.43, "PAYX": 157.91,
    "ROP": 545.17, "WDAY": 291.07, "GEHC": 82.02, "MSTR": 289.62,
    "CPRT": 52.33, "KHC": 36.98, "DXCM": 124.09,
}
CURR_PX = {
    "NVDA": 192.53, "AAPL": 283.78, "MSFT": 372.97, "AMZN": 232.69,
    "GOOGL": 337.39, "GOOG": 334.69, "AVGO": 365.02, "TSLA": 379.71,
    "META": 550.25, "MU": 1132.33, "AMD": 521.58, "ASML": 1794.62,
    "INTC": 128.32, "AMAT": 626.84, "LRCX": 379.09, "CSCO": 113.77,
    "COST": 952.54, "ARM": 334.27, "KLAC": 248.64, "WMT": 115.69,
    "EXC": 47.40, "MCHP": 87.93, "ODFL": 218.79, "KDP": 33.40, "CCEP": 101.59,
    "TTWO": 238.53, "IDXX": 551.50, "ADSK": 196.26, "PYPL": 44.29,
    "ALNY": 291.37, "AXON": 464.83, "TRI": 83.87, "PAYX": 99.90,
    "ROP": 338.31, "WDAY": 124.21, "GEHC": 65.76, "MSTR": 82.31,
    "CPRT": 30.55, "KHC": 23.70, "DXCM": 70.14,
}
# LIVE-feed corrupt -> RET23>now untrustworthy (flagged with '!').
LIVE_CORRUPT = {"AMD", "ASML", "INTC", "AMAT", "LRCX", "CSCO", "ARM",
                "MSFT", "META", "MU", "KLAC", "TRI"}
# WHOLE price series corrupt/scaled -> both return columns unreliable.
SERIES_CORRUPT = {"MU", "KLAC"}


def ret_now(t):
    """% from 2023 anchor to 'today'; flag when the live feed is corrupt."""
    if t in SERIES_CORRUPT:
        return " corrupt"
    a, c = ANCHOR_PX.get(t), CURR_PX.get(t)
    if a is None or c is None or a == 0:
        return "       -"
    return f"{(c / a - 1.0) * 100:+7.0f}%" + ("!" if t in LIVE_CORRUPT else "")


def ret_max(t):
    """% from 2023 anchor to best RELIABLE year-end close in-window."""
    if t in SERIES_CORRUPT:
        return " corrupt"
    a, m = ANCHOR_PX.get(t), MAX_CLOSE.get(t)
    if a is None or m is None or a == 0:
        return "       -"
    return f"{(m / a - 1.0) * 100:+7.0f}%"


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


def render_with_returns(results, fund):
    """Same grouped tables as the engine's render_by_strategy, with two extra
    OUTCOME columns appended: RET23>now and RET23>max. Reuses the engine's own
    cell helpers so the F/V/C/bind/data% columns are identical to production."""
    print("\n=== RATING BY STRATEGY + REALIZED RETURNS  "
          "(2023 backtest) ===")
    print("Each mode graded on its own rubric (engine logic); the last two "
          "columns are post-2023 OUTCOMES, never fed into scoring.")

    # ---- DCA ----
    dca = [r for r in results if r["strategy"] == "dca"]
    scored = []
    for r in dca:
        f = fund.get(r["ticker"], {})
        q10, rich, _ = S.dca_quality(r["ticker"], f)
        dconv = S.dca_conviction(q10, r["layers"], r["layers"][r["binding"]],
                                 rich, r["coverage"])
        scored.append((r, q10, rich, S.dca_grade(q10, rich, f), dconv))
    scored.sort(key=lambda x: -x[4])
    print("\n-- DCA (steady compounders; buy on schedule) "
          "--------------------------")
    print(f"   {'ticker':8s} {'wv':3s} {'book%':>5s} {'CONV':>5s} "
          f"{'QUALITY':>7s} {'RICHNESS':>8s} {'grade':9s} {'F':>4s} {'V':>4s} "
          f"{'C':>4s} {'bind':5s} {'data%':>5s} {'RET23>now':>9s} "
          f"{'RET23>max':>9s}")
    for r, q10, rich, grade, dconv in scored:
        t = r["ticker"]
        pk = " [PEAK?]" if r["peak"] else ""
        print(f"   {t:8s} {r['wave']:3s} {r['book_pct']:5.2f} {dconv:5.2f} "
              f"{q10:7.1f} {rich:8.2f} {grade:9s} {S._layer_cell(r['layers'])} "
              f"{S._LAYER_ABBR[r['binding']]:5s} {S._cov_cell(r['coverage'])} "
              f"{ret_now(t):>9s} {ret_max(t):>9s}{pk}")

    # ---- CYCLE & CATALYST ----
    for mode, title in [("cycle", "CYCLE (buy the dip / sell the rip)"),
                        ("catalyst", "CATALYST (event-driven punts)")]:
        grp = [r for r in results if r["strategy"] == mode]
        grp.sort(key=lambda r: -r["conviction"])
        print(f"\n-- {title} " + "-" * max(2, 46 - len(title)))
        print(f"   {'ticker':8s} {'wv':3s} {'book%':>5s} {'CONV':>5s} "
              f"{'GROWTH':>6s} {'8PT':>4s} {'quadrant':10s} {'F':>4s} "
              f"{'V':>4s} {'C':>4s} {'bind':5s} {'data%':>5s} "
              f"{'RET23>now':>9s} {'RET23>max':>9s}")
        for r in grp:
            t = r["ticker"]
            pk = " [PEAK?]" if r["peak"] else ""
            print(f"   {t:8s} {r['wave']:3s} {r['book_pct']:5.2f} "
                  f"{r['conviction']:5.2f} {r['growth10']:6.1f} "
                  f"{r['eight']:4.2f} {r['quad']:10s} "
                  f"{S._layer_cell(r['layers'])} "
                  f"{S._LAYER_ABBR[r['binding']]:5s} "
                  f"{S._cov_cell(r['coverage'])} "
                  f"{ret_now(t):>9s} {ret_max(t):>9s}{pk}")

    print("\n   RET23>now = anchor 2023 close -> today. '!' = LIVE feed corrupt "
          "in this env (semis 2-4x; MU ~10x; MSFT/META/TRI off) -> not real.")
    print("   RET23>max = anchor -> best RELIABLE fiscal-year-end close "
          "(corrupt live column excluded); conservative vs true intra-year highs.")
    print("   corrupt = whole price series unreliable (MU ~10x, KLAC /10).")
    print("   Returns are OUTCOME data only — they never feed the score.")


def universe_rows():
    """Build the full 204-name AI-allocation backtest universe from the
    committed snapshot + universe_2023 classifier. Returns (port, cycle, neck,
    deep_cyclical, strat_map)."""
    U = _load_universe_module()
    strat = U.build_strategy_2023()
    port = S.portfolio_rows(include_watchlist=True)  # for current book%/wave

    # Engine owner-tags for 2023. Default heuristic: WFE/foundry/memory semis
    # and AI-infra names are bottleneck owners (neck=1.0, cycle Early/Mid);
    # everything else neck=0.5 / Mid. The hand-curated 40-name tags override.
    SEMI = {"AMKR", "ASX", "CAMT", "COHR", "COHU", "CRDO", "DIOD", "ENTG",
            "FN", "FORM", "GFS", "ICHR", "KLIC", "LSCC", "MKSI", "MPWR",
            "MRVL", "MTSI", "NVMI", "ON", "ONTO", "POWI", "QCOM", "SANM",
            "SIMO", "TER", "TSEM", "TSM", "UMC", "AAOI", "CIEN", "LITE",
            "VRT", "CLS", "DELL", "HPQ", "NTAP", "STX", "WDC", "JBL", "AEHR",
            "000660.KS", "005930.KS", "BESI.AS", "1810.HK"}
    cyc, neck = {}, {}
    for t in strat:
        if t in SEMI:
            cyc[t], neck[t] = "Early", 1.0
        else:
            cyc[t], neck[t] = "Mid", 0.5
    # hand-curated 40-name tags win where present
    cyc.update(CYCLE_2023)
    neck.update(NECK_2023)
    deep = set(DEEP_CYCLICAL) | {"AMKR", "ASX", "GFS", "TSM", "UMC", "TSEM",
                                 "STX", "WDC", "TER", "ENTG", "KLIC", "ON",
                                 "MKSI", "000660.KS", "005930.KS", "BESI.AS"}

    rows = {}
    for t, st in strat.items():
        info = port.get(t, {})
        rows[t] = {"ticker": t, "wave": info.get("wave", "AI"), "sub": 0.0,
                   "book_pct": round(info.get("book_pct", 0.0), 2),
                   "etf_pct": 0.0, "strategy": st,
                   "held": bool(info.get("held")),
                   "cagr_lo": None, "cagr_hi": None, "cagr_mid": None,
                   "wl_pos": cyc.get(t)}
    return rows, cyc, neck, deep, strat


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
    ap.add_argument("--with-returns", action="store_true",
                    help="append realized RET23>now / RET23>max OUTCOME columns "
                         "(post-2023 prices; never fed into scoring). Implies "
                         "the by-strategy grouped view.")
    ap.add_argument("--universe", action="store_true",
                    help="score the FULL AI-allocation universe (204 names) from "
                         "fundamentals_2023_universe.csv, each in its 2023-vintage "
                         "strategy (universe_2023.py). Supersedes held/watchlist.")
    args = ap.parse_args()

    if args.universe:
        port, cyc, neck, deep, _ = universe_rows()
        S.CYCLE_POS, S.BOTTLENECK, S._CYCLICAL = cyc, neck, deep
        fund = dict(S.load_fundamentals(str(CSV_UNIVERSE)))
        if args.sync_csv:
            coverage_check(fund, list(port))
    else:
        # Inject the frozen 2023 owner tags so the REAL engine reads 2023 values.
        S.CYCLE_POS = CYCLE_2023
        S.BOTTLENECK = NECK_2023
        S._CYCLICAL = DEEP_CYCLICAL

        port = backtest_rows(include_watchlist=args.watchlist)

        # Load the frozen snapshot(s): held always; watchlist only when
        # requested (mirrors production loading held + watchlist if --watchlist).
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
    if args.with_returns:
        render_with_returns(results, fund)
    elif args.by_strategy:
        S.render_by_strategy(results, fund, args)
    else:
        print("\n(use --by-strategy for the grouped strategy view, or "
              "--with-returns to add the realized-return columns)")


if __name__ == "__main__":
    main()
