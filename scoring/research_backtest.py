#!/usr/bin/env python3
"""Research backtest — does QUALITY or CHEAPNESS predict forward stock returns?

RESEARCH ONLY. This file does not touch the scoring engine. It reuses the
point-in-time panel from `backtest.py` (same FUND score, same reconstructed
P/S, same 2021-2024 year-end entry dates) and slices it three ways. Use it to
judge how much to trust a signal before ever considering an engine change.

Findings it produced (US-only, ~2021-2024 unless noted, one bull regime):
  - CHEAPNESS (low P/S) predicts higher forward return — robust across years,
    horizons, strategy buckets and most cap sizes. The trustworthy signal.
  - QUALITY (FUND score) INVERTS at long horizons — high trailing quality ->
    lower forward return, worst in mega-caps. Real but weaker-sampled.
  - Cheap edge is strongest in large/mid-caps, ~zero in mega-caps; small-cap
    cheapness is a 1-year trade that fades by 3 years.

Sub-commands (run one or --all):
  --years        QUAL & CHEAP good-vs-bad spread split BY ENTRY YEAR
                 (1y / 2y / 3y horizons) — tests if 'quality inverts' is a
                 2022-crash-bounce fluke or a stable pattern.
  --price-2018   PRICE-ONLY signals (momentum / trend / contrarian) for the
                 2018/2019/2020 entries. The only pre-2021 evidence we have
                 (no financials reach that far back, but prices do), so it
                 covers the COVID crash with full 3-year forward returns.
  --category     QUAL & CHEAP spread BY STRATEGY and BY CAP SIZE on the full,
                 cap-balanced, fully-tagged universe (adds ~30 small/mid-caps
                 and tags every name; tags live HERE, not in production).

Data caveats (why not to re-tool the engine on this):
  - US-only. Foreign holdings (.KS/.AS/.DE/.HK) have no price feed here.
  - The 3-year horizon rests mostly on 2021 + 2022 entries.
  - One secular bull market (2016-2026); 'buy the dip' always paid in-sample.
  - Strategy tags for non-held names are heuristic, not hand-verified.

  python3 scoring/research_backtest.py --fetch   # populate cache first
  PORTFOLIO_USE=ai python3 scoring/research_backtest.py --all
"""
import argparse
import re
import statistics as st
from collections import defaultdict

import backtest as bt
from score_holdings import load_fundamentals, default_csv, STRATEGY


# =========================================================================
# shared helpers
# =========================================================================
def median(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def cap_bucket(b):
    if b is None:
        return "unknown"
    if b < 2:
        return "small (<2B)"
    if b < 10:
        return "mid (2-10B)"
    if b < 200:
        return "large (10-200B)"
    return "mega (>200B)"


def half_split_spread(rows, ret_key, sig):
    """Top-half vs bottom-half of `sig`; return (spread, n) where spread is the
    difference of the two halves' median forward return. Positive = high-`sig`
    names did better; negative = the signal inverts. None if n<6."""
    rs = [r for r in rows if r.get(ret_key) is not None and r.get(sig) is not None]
    if len(rs) < 6:
        return None, len(rs)
    rs.sort(key=lambda r: r[sig])
    h = len(rs) // 2
    lo = median([r[ret_key] for r in rs[:h]])
    hi = median([r[ret_key] for r in rs[h:]])
    return hi - lo, len(rs)


def _line(label, rows, ret_key, sig):
    sp, n = half_split_spread(rows, ret_key, sig)
    if sp is None:
        return f"   {label:<14} n={n:<3} (too few)"
    rs = sorted((r for r in rows
                 if r.get(ret_key) is not None and r.get(sig) is not None),
                key=lambda r: r[sig])
    h = len(rs) // 2
    lo = median([r[ret_key] for r in rs[:h]])
    hi = median([r[ret_key] for r in rs[h:]])
    tag = "INVERTS" if sp < 0 else "works  "
    return (f"   {label:<14} n={n:<3} "
            f"high={hi:+7.1%}  low={lo:+7.1%}  spread={sp:+7.1%}  [{tag}]")


def _fmt(sp):
    return f"{sp:+7.1%}" if sp is not None else "    n/a"


# =========================================================================
# the standard 2021-2024 panel, with a 2-year return and a cheapness score
# =========================================================================
def base_panel():
    fund = load_fundamentals(default_csv())
    tickers = [t for t in fund if "." not in t]
    ps_now = {t: fund[t].get("ps_ratio") for t in tickers}
    rows = bt.build_panel_plus(tickers, ps_now)
    px = {t: bt.fetch_prices(t) for t in tickers}
    for r in rows:
        p0 = bt._price_on_or_after(px[r["ticker"]], r["date"])
        p2 = bt._price_on_or_after(px[r["ticker"]], bt._shift_year(r["date"], 2))
        r["ret2y"] = (p2 / p0 - 1) if (p0 and p2) else None
        r["cheap"] = (-r["ps"]) if r.get("ps") is not None else None
    return fund, rows


# =========================================================================
# TEST 1 — by entry year (was _split_by_year.py)
# =========================================================================
def test_years(rows):
    by_date = defaultdict(list)
    for r in rows:
        by_date[r["date"]].append(r)

    print("=" * 72)
    print("TEST 1 — QUAL vs CHEAP, split BY ENTRY YEAR")
    print("Is 'high quality -> lower forward return' a 2022-crash fluke, or")
    print("stable? Top-half vs bottom-half median forward return.")
    print("=" * 72)

    for sig, title in [("score", "QUALITY (FUND score)"),
                       ("cheap", "CHEAPNESS (low P/S)")]:
        print(f"\n## {title}")
        for ret_key, hz in [("ret1y", "1-YEAR"), ("ret2y", "2-YEAR"),
                            ("ret3y", "3-YEAR")]:
            print(f"  -- {hz} forward --")
            for d in bt.ASOF_DATES:
                print(_line(f"entry {d[:4]}", by_date[d], ret_key, sig))
            print(_line("ALL DATES", rows, ret_key, sig))


# =========================================================================
# TEST 2 — price-only signals, 2018-2020 entries (was _price_only_2018.py)
# =========================================================================
_P2018_ENTRIES = ["2018-12-31", "2019-12-31", "2020-12-31"]


def _price_at(prices, date_str, tol_days=70):
    """Genuine price AT date_str (nearest close on/after, within tol_days).
    Returns None if the nearest forward price is too far — prevents forward-fill
    look-ahead, e.g. a 2021-listed name must NOT report a price for 2018."""
    from datetime import date
    y, m, d = (int(x) for x in date_str.split("-"))
    target = date(y, m, d)
    for k in sorted(prices):
        if k >= date_str:
            ky, km, kd = (int(x) for x in k.split("-"))
            return prices[k] if (date(ky, km, kd) - target).days <= tol_days else None
    return None


def _ma(prices, asof, months):
    ks = [k for k in sorted(prices) if k <= asof]
    if len(ks) < months:
        return None
    return sum(prices[k] for k in ks[-months:]) / months


def _high(prices, asof, months):
    ks = [k for k in sorted(prices) if k <= asof]
    if not ks:
        return None
    window = ks[-months:] if len(ks) >= months else ks
    return max(prices[k] for k in window)


def test_price_2018(tickers):
    rows = []
    for t in tickers:
        px = bt.fetch_prices(t)
        if not px:
            continue
        for asof in _P2018_ENTRIES:
            p0 = _price_at(px, asof)        # genuine entry price (no look-ahead)
            if not p0:
                continue
            p_prev = _price_at(px, bt._shift_year(asof, -1))
            mom = (p0 / p_prev - 1) if p_prev else None
            ma10 = _ma(px, asof, 10)
            trend = (p0 / ma10 - 1) if ma10 else None
            hi24 = _high(px, asof, 24)
            contr = -(p0 / hi24 - 1) if hi24 else None   # more below high = bigger
            p1 = bt._price_on_or_after(px, bt._shift_year(asof, 1))
            p3 = bt._price_on_or_after(px, bt._shift_year(asof, 3))
            rows.append({"ticker": t, "date": asof, "mom": mom, "trend": trend,
                         "contr": contr,
                         "ret1y": (p1 / p0 - 1) if p1 else None,
                         "ret3y": (p3 / p0 - 1) if p3 else None})

    by_date = defaultdict(list)
    for r in rows:
        by_date[r["date"]].append(r)

    print("\n" + "=" * 72)
    print("TEST 2 — PRICE-ONLY signals, 2018/2019/2020 entries (incl. COVID)")
    print("The only pre-2021 evidence (no financials that far back, prices do).")
    print(f"{len({r['ticker'] for r in rows})} US names x {len(_P2018_ENTRIES)}"
          f" entries = {len(rows)} observations")
    print("=" * 72)

    for sig, name in [("mom", "MOMENTUM (prior-12m)"),
                      ("trend", "TREND (vs 10-mo MA)"),
                      ("contr", "CONTRARIAN (below 24m high)")]:
        print(f"\n## {name}")
        for rk, hz in [("ret1y", "1-YEAR"), ("ret3y", "3-YEAR")]:
            print(f"  -- {hz} forward --")
            for d in _P2018_ENTRIES:
                print(_line(f"entry {d[:4]}", by_date[d], rk, sig))
            print(_line("ALL 3 YEARS", rows, rk, sig))


# =========================================================================
# TEST 3 — by strategy & cap, full tagged + balanced universe (was v2)
# =========================================================================
# Extra small/mid-cap names in the portfolio's themes (semis / power / AI /
# quantum / space), added to balance a large-cap-heavy universe.
_EXTRA = [
    "POWI", "SLAB", "DIOD", "RMBS", "AMBA", "CRUS", "SITM", "ALGM", "FORM",
    "ACLS", "MXL", "UCTT", "SMTC", "QRVO", "NXT", "BE", "FLNC", "AMSC",
    "INDI", "NVTS", "AI", "PATH", "GTLB", "CFLT", "ESTC", "AOSL", "LASR",
    "CEVA", "AEIS", "ENPH",
]

# Heuristic tagger (research-only — NOT written to production STRATEGY, which
# verify_allocations() requires to hold only held-basket tickers).
_CATALYST_HINTS = {
    "QBTS", "RGTI", "QUBT", "QNT", "IONQ",                  # quantum
    "ASTS", "RKLB", "LUNR", "RR", "SERV", "BOT",            # space / robotics
    "SMR", "NNE", "OKLO", "LEU",                            # SMR / nuclear pre-rev
    "RXRX", "VKTX", "TEM",                                  # biotech binary
    "ACHR",                                                 # eVTOL pre-rev
    "ENVX",                                                 # pre-scale battery
    "AI",                                                   # c3.ai story stock
}
_DCA_HINTS = {
    "POWI", "DIOD", "MCHP", "TXN", "QCOM", "SNPS", "CDNS", "PNR", "TER",
    "KLAC", "AMAT", "LRCX", "CSCO", "AAPL",
}


def tag(t, f):
    if t in STRATEGY:
        return STRATEGY[t]
    if t in _CATALYST_HINTS:
        return "catalyst"
    if t in _DCA_HINTS:
        return "dca"
    nm = f.get("net_margin")
    fcf = f.get("fcf_positive")
    mc = f.get("mktcap_b")
    if nm is not None and nm < -25 and (mc is not None and mc < 5):
        return "catalyst"                                  # pre-rev lossmaker
    if nm is not None and nm > 8 and fcf == 1:
        return "dca"                                       # durable compounder
    return "cycle"                                         # real but cyclical


def _ps_now_for(t):
    try:
        html = bt._get(f"https://stockanalysis.com/stocks/{t}/statistics/")
    except Exception:
        return None
    m = re.search(r"PS Ratio[^0-9-]*([0-9]+\.[0-9]+)", html)
    return float(m.group(1)) if m else None


def test_category(fund):
    base = [t for t in fund if "." not in t]
    print("\n" + "=" * 80)
    print("TEST 3 — QUAL vs CHEAP by STRATEGY & CAP (tagged + cap-balanced)")
    print("=" * 80)
    print("Fetching current P/S for extra small/mid-cap names...")
    for t in _EXTRA:
        if t in fund:
            continue
        psn = _ps_now_for(t)
        fin = bt.fetch_financials(t)
        rev_now = None
        if fin:
            fy = sorted(fin)
            rev_now = fin[fy[-1]].get("revenue") if fy else None
            last = fin[fy[-1]]
            nm = (last.get("profitMargin") or 0) * 100 \
                if last.get("profitMargin") is not None else None
            fcf = 1 if (last.get("fcf") or 0) > 0 else 0
        else:
            nm = fcf = None
        mc = (rev_now / 1e9 * psn) if (psn and rev_now) else None
        fund[t] = {"ps_ratio": psn, "mktcap_b": mc,
                   "net_margin": nm, "fcf_positive": fcf}

    tickers = base + [t for t in _EXTRA if t not in base]
    ps_now = {t: fund[t].get("ps_ratio") for t in tickers}
    rows = bt.build_panel_plus(tickers, ps_now)
    for r in rows:
        t = r["ticker"]
        r["strat"] = tag(t, fund[t])
        r["cap"] = cap_bucket(fund[t].get("mktcap_b"))
        r["cheap"] = (-r["ps"]) if r.get("ps") is not None else None

    names = {r["ticker"] for r in rows}
    new_names = names & set(_EXTRA)
    print(f"{len(names)} US names ({len(new_names)} newly added), "
          f"{len(rows)} observations (2021-2024 entries)")

    newly_tagged = sorted({(r["ticker"], r["strat"]) for r in rows
                           if r["ticker"] not in STRATEGY})
    by_st = defaultdict(list)
    for t, s in newly_tagged:
        by_st[s].append(t)
    print(f"\n## TAGGER OUTPUT — {len(newly_tagged)} names tagged in research")
    for s in ("dca", "cycle", "catalyst"):
        print(f"  {s:<9}({len(by_st[s])}): {', '.join(sorted(by_st[s]))}")

    def section(title, keyfn, order):
        print(f"\n## BY {title}")
        print(f"  {'category':<16} {'names':>5} {'obs':>4} | "
              f"{'QUAL 1y':>8} {'QUAL 3y':>8} | {'CHEAP 1y':>9} {'CHEAP 3y':>9}")
        print("  " + "-" * 76)
        groups = defaultdict(list)
        for r in rows:
            groups[keyfn(r)].append(r)
        keys = [k for k in order if k in groups] + \
               [k for k in groups if k not in order]
        for k in keys:
            g = groups[k]
            nn = len({r["ticker"] for r in g})
            q1, _ = half_split_spread(g, "ret1y", "score")
            q3, _ = half_split_spread(g, "ret3y", "score")
            c1, _ = half_split_spread(g, "ret1y", "cheap")
            c3, _ = half_split_spread(g, "ret3y", "cheap")
            print(f"  {k:<16} {nn:>5} {len(g):>4} | "
                  f"{_fmt(q1)} {_fmt(q3)} | {_fmt(c1)} {_fmt(c3)}")

    section("STRATEGY", lambda r: r["strat"], ["dca", "cycle", "catalyst"])
    section("MARKET-CAP SIZE", lambda r: r["cap"],
            ["small (<2B)", "mid (2-10B)", "large (10-200B)", "mega (>200B)"])

    print("\n## NAME COUNTS: strategy x size")
    sizes = ["small (<2B)", "mid (2-10B)", "large (10-200B)", "mega (>200B)"]
    by = defaultdict(set)
    for r in rows:
        by[(r["strat"], r["cap"])].add(r["ticker"])
    print(f"  {'':<11}" + "".join(f"{s.split()[0]:>9}" for s in sizes) + f"{'TOT':>6}")
    for stt in ("dca", "cycle", "catalyst"):
        cells = [len(by[(stt, sz)]) for sz in sizes]
        print(f"  {stt:<11}" + "".join(f"{c:>9}" for c in cells) + f"{sum(cells):>6}")

    print("\n  (spread = top-half median fwd return minus bottom-half;")
    print("   QUAL negative = quality inverts; CHEAP positive = cheap wins)")


# =========================================================================
def main():
    ap = argparse.ArgumentParser(
        description="Research backtest: does quality or cheapness predict "
                    "forward returns? RESEARCH ONLY — does not touch the scorer.")
    ap.add_argument("--fetch", action="store_true",
                    help="populate the price/financials cache, then exit")
    ap.add_argument("--years", action="store_true", help="TEST 1: by entry year")
    ap.add_argument("--price-2018", action="store_true",
                    help="TEST 2: price-only signals, 2018-2020 entries")
    ap.add_argument("--category", action="store_true",
                    help="TEST 3: by strategy & cap, tagged + balanced")
    ap.add_argument("--all", action="store_true", help="run all three tests")
    args = ap.parse_args()

    fund0 = load_fundamentals(default_csv())
    base_tickers = [t for t in fund0 if "." not in t]

    if args.fetch:
        bt.fetch_all(base_tickers + _EXTRA)
        return

    if not any((bt.CACHE / f"px_{t}.json").exists() for t in base_tickers):
        raise SystemExit("Cache empty. Run with --fetch first.")

    run_all = args.all or not (args.years or args.price_2018 or args.category)

    if args.years or run_all:
        _, rows = base_panel()
        test_years(rows)
    if args.price_2018 or run_all:
        test_price_2018(base_tickers)
    if args.category or run_all:
        # fresh fund dict so TEST 3's synthetic EXTRA rows don't leak elsewhere
        test_category(load_fundamentals(default_csv()))


if __name__ == "__main__":
    main()
