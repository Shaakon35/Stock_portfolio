#!/usr/bin/env python3
# =========================================================================
# SCORE BACKTEST — does the fundamentals signal predict forward returns?
# =========================================================================
# Validates the scoring thesis out-of-sample using POINT-IN-TIME data, so there
# is no look-ahead bias (the #1 way a backtest lies). For each past fiscal
# year-end we reconstruct the FUND-layer features *as they were known then*,
# measure the forward 1y and 3y return, and ask two questions:
#
#   1. Does ranking names by the FUND score rank-predict forward return?
#      -> Spearman rank Information Coefficient (IC), per-date and pooled.
#   2. Do top-scored names actually beat bottom-scored names?
#      -> quantile spread: avg forward EXCESS return, top third vs bottom third.
#
# Then it fits the feature weights (ridge, closed form) on the pooled panel to
# see which fundamentals actually drove returns, vs the scorer's hand-set
# weights. Excess return (vs an equal-weight basket of the same universe) strips
# out the macro tide so we measure the SIGNAL, not the year.
#
# WHY A PANEL (multiple as-of dates), not one snapshot: with a single date every
# stock shares one macro environment, so the dominant return driver is constant
# across the sample and a regression sees only noise (this is why a naive
# one-shot linear fit "doesn't work"). Pooling several rebalance dates lets the
# macro move average out and exposes the cross-sectional fundamental signal.
#
# SCOPE: FUND layer only (revenue growth, margins, FCF, the decel/accel trend).
# Valuation (PEG/PS) and momentum (200DMA) are NOT reconstructed here because
# they need point-in-time price+consensus; this isolates the business-quality
# thesis cleanly. If the FUND signal is weak we extend to a reconstructed P/S.
#
# DATA: stockanalysis.com, cached on disk so re-runs are deterministic & fast:
#   - /api/symbol/s/<T>/history?range=10Y&period=Monthly  -> adj-close monthly
#   - /stocks/<T>/financials/  embeds financialData JSON   -> per-FY fundamentals
# US tickers only (foreign exchange API paths 404); ~96 of the 103 names.
#
# USAGE:
#   python3 scoring/backtest.py --fetch     # populate the on-disk cache (slow)
#   python3 scoring/backtest.py             # run analysis from cache (fast)
# =========================================================================
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scoring.score_holdings import load_fundamentals, default_csv  # noqa: E402

CACHE = Path(__file__).resolve().parent / "_backtest_cache"
CACHE.mkdir(exist_ok=True)
_UA = {"User-Agent": "Mozilla/5.0"}

# As-of dates: fiscal year-ends we score at. Each needs >=1y of forward price
# for the 1y test; the earlier ones also support the 3y test.
ASOF_DATES = ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"]
# Benchmark proxy for excess return: an equal-weight basket of the universe
# itself (computed at run time), so "excess" = stock vs its own peer group.


# -------------------------------------------------------------------------
# Fetch + cache
# -------------------------------------------------------------------------
def _get(url):
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def fetch_prices(ticker):
    """Monthly adjusted-close history for a US ticker -> {date: adj_close}.
    Cached on disk as JSON. Returns {} on failure."""
    cf = CACHE / f"px_{ticker}.json"
    if cf.exists():
        return json.loads(cf.read_text())
    url = (f"https://stockanalysis.com/api/symbol/s/{ticker}"
           f"/history?range=10Y&period=Monthly")
    try:
        data = json.loads(_get(url)).get("data", [])
    except Exception as e:
        print(f"  [px] {ticker}: FAIL {e}")
        cf.write_text("{}")
        return {}
    out = {row["t"]: row["a"] for row in data if row.get("a") is not None}
    cf.write_text(json.dumps(out))
    print(f"  [px] {ticker}: {len(out)} monthly bars")
    return out


def fetch_financials(ticker):
    """Per-fiscal-year fundamentals for a US ticker. Cached on disk.
    Returns {datekey: {revenueGrowth, profitMargin, operatingMargin, fcf,
    fcfMargin, revenue}} keyed by FY-end date string."""
    cf = CACHE / f"fin_{ticker}.json"
    if cf.exists():
        return json.loads(cf.read_text())
    url = f"https://stockanalysis.com/stocks/{ticker}/financials/"
    try:
        html = _get(url)
    except Exception as e:
        print(f"  [fin] {ticker}: FAIL {e}")
        cf.write_text("{}")
        return {}
    out = _parse_financials(html)
    cf.write_text(json.dumps(out))
    print(f"  [fin] {ticker}: {len(out)} fiscal years")
    return out


def _arr(block, key):
    """Pull a numeric array `key:[...]` out of the financialData JS blob."""
    m = re.search(re.escape(key) + r":\[([^\]]*)\]", block)
    if not m:
        return []
    vals = []
    for p in m.group(1).split(","):
        p = p.strip()
        if p in ("", "null"):
            vals.append(None)
        else:
            try:
                vals.append(float(p))
            except ValueError:
                vals.append(None)
    return vals


def _parse_financials(html):
    i = html.find("financialData")
    if i < 0:
        return {}
    block = html[i:i + 8000]
    m = re.search(r"datekey:\[([^\]]*)\]", block)
    if not m:
        return {}
    dates = [d.strip().strip('"') for d in m.group(1).split(",")]
    series = {k: _arr(block, k) for k in
              ("revenueGrowth", "profitMargin", "operatingMargin",
               "grossMargin", "fcf", "fcfMargin", "revenue", "netIncome")}
    out = {}
    for idx, dk in enumerate(dates):
        if dk == "TTM":
            continue                      # skip the partial TTM column
        rec = {}
        for k, arr in series.items():
            rec[k] = arr[idx] if idx < len(arr) else None
        out[dk] = rec
    return out


def fetch_all(tickers):
    for i, t in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] {t}")
        fetch_prices(t)
        fetch_financials(t)
        time.sleep(0.3)                   # be polite to the source


# -------------------------------------------------------------------------
# Point-in-time features + forward returns
# -------------------------------------------------------------------------
def _price_on_or_after(prices, date_str):
    """Nearest monthly adj-close on/after date_str (forward fill). None if the
    history does not extend that far."""
    keys = sorted(prices)
    for k in keys:
        if k >= date_str:
            return prices[k]
    return None


def _shift_year(date_str, years):
    y, m, d = date_str.split("-")
    return f"{int(y) + years:04d}-{m}-{d}"


def pit_features(fin, asof):
    """Reconstruct FUND-layer features known AT `asof` (a FY-end date). Uses the
    fiscal year ending on/just before asof as 'trailing', and the prior years
    for the median-trend baseline. Returns None if that FY is missing."""
    fy_dates = sorted([d for d in fin if d <= asof], reverse=True)
    if not fy_dates:
        return None
    latest = fy_dates[0]
    rec = fin[latest]
    rg = rec.get("revenueGrowth")
    if rg is None:
        return None
    # multi-year trailing revenue-growth series (for the trend signal), oldest
    # excluded so the median mirrors the live scorer's rev_growth_hist median.
    hist = [fin[d].get("revenueGrowth") for d in fy_dates[1:]
            if fin[d].get("revenueGrowth") is not None]
    median_g = float(np.median(hist)) if hist else rg
    # prefer operating margin when profit margin is distorted/negative but ops
    # are positive (mirrors the live operating-margin proxy rule).
    pm = rec.get("profitMargin")
    om = rec.get("operatingMargin")
    margin = pm
    if (pm is None or pm < 0) and (om is not None and om > 0):
        margin = om
    fcf = rec.get("fcf")
    return {
        "rev_growth": rg * 100 if rg is not None else None,
        "margin": margin * 100 if margin is not None else None,
        "fcf_pos": 1.0 if (fcf is not None and fcf > 0) else 0.0,
        "trend": (rg - median_g) * 100,           # >0 accel, <0 decel
        "fcf_margin": (rec.get("fcfMargin") or 0.0) * 100,
    }


def fund_score(feat):
    """A transparent 0..1 FUND score from point-in-time features, using the same
    spirit as score_holdings' FUND layer: margin + growth + FCF + trend tilt.
    Kept simple and explicit so the backtest result is interpretable."""
    def band(x, lo, hi):
        if x is None:
            return 0.5
        return max(0.0, min(1.0, (x - lo) / (hi - lo)))
    s_margin = band(feat["margin"], 0, 30)
    s_growth = band(feat["rev_growth"], 5, 45)
    s_fcf = feat["fcf_pos"]
    base = 0.40 * s_margin + 0.30 * s_growth + 0.20 * s_fcf + 0.10 * 0.5
    # symmetric trend tilt, same shape as the live _trend_adjust
    t = feat["trend"]
    if t > 5:
        base += min((t - 5) / 20.0, 1.0) * 0.15
    elif t < -5:
        base -= min((-t - 5) / 20.0, 1.0) * 0.25
    return max(0.0, min(1.0, base))


# -------------------------------------------------------------------------
# Stats (numpy-only: no scipy/sklearn)
# -------------------------------------------------------------------------
def _rankdata(a):
    """Average-rank (ties shared), like scipy.stats.rankdata."""
    a = np.asarray(a, float)
    order = a.argsort()
    ranks = np.empty(len(a), float)
    ranks[order] = np.arange(1, len(a) + 1)
    # average ties
    _, inv, counts = np.unique(a, return_inverse=True, return_counts=True)
    sums = np.zeros(len(counts))
    np.add.at(sums, inv, ranks)
    return (sums / counts)[inv]


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return float("nan")
    rx, ry = _rankdata(x), _rankdata(y)
    rx -= rx.mean(); ry -= ry.mean()
    d = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d else float("nan")


def ridge(X, y, lam=1.0):
    """Closed-form ridge on standardised X (returns standardised coefs)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1.0
    Xs = (X - mu) / sd
    ys = (y - y.mean())
    n, p = Xs.shape
    A = Xs.T @ Xs + lam * np.eye(p)
    coef = np.linalg.solve(A, Xs.T @ ys)
    pred = Xs @ coef
    ss_res = ((ys - pred) ** 2).sum()
    ss_tot = (ys ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")
    return coef, r2


# -------------------------------------------------------------------------
# Build panel + analyse
# -------------------------------------------------------------------------
FEATURE_NAMES = ["rev_growth", "margin", "fcf_pos", "trend", "fcf_margin"]


def build_panel(tickers):
    """Return list of obs dicts: ticker, date, features..., score, ret1y, ret3y,
    plus per-date excess returns computed against the universe mean."""
    rows = []
    for t in tickers:
        prices = fetch_prices(t)
        fin = fetch_financials(t)
        if not prices or not fin:
            continue
        for asof in ASOF_DATES:
            feat = pit_features(fin, asof)
            if feat is None:
                continue
            p0 = _price_on_or_after(prices, asof)
            if not p0:
                continue
            p1 = _price_on_or_after(prices, _shift_year(asof, 1))
            p3 = _price_on_or_after(prices, _shift_year(asof, 3))
            ret1 = (p1 / p0 - 1) if p1 else None
            ret3 = (p3 / p0 - 1) if p3 else None
            rows.append({
                "ticker": t, "date": asof, **feat,
                "score": fund_score(feat), "ret1y": ret1, "ret3y": ret3,
            })
    _add_excess(rows, "ret1y")
    _add_excess(rows, "ret3y")
    return rows


def _add_excess(rows, key):
    """Per-date demeaning: excess_<key> = ret - mean(ret of that date)."""
    by_date = {}
    for r in rows:
        if r.get(key) is not None:
            by_date.setdefault(r["date"], []).append(r[key])
    means = {d: float(np.mean(v)) for d, v in by_date.items()}
    for r in rows:
        r[f"x_{key}"] = (r[key] - means[r["date"]]
                         if r.get(key) is not None and r["date"] in means
                         else None)


def _ic_by_date(rows, ret_key):
    out = {}
    dates = sorted({r["date"] for r in rows})
    for d in dates:
        sub = [r for r in rows if r["date"] == d and r.get(ret_key) is not None]
        if len(sub) >= 5:
            out[d] = (spearman([r["score"] for r in sub],
                               [r[ret_key] for r in sub]), len(sub))
    return out


def _quantile_spread(rows, ret_key):
    sub = [r for r in rows if r.get(ret_key) is not None]
    if len(sub) < 9:
        return None
    sub.sort(key=lambda r: r["score"])
    n = len(sub)
    bottom = sub[: n // 3]
    top = sub[-(n // 3):]
    tb = np.mean([r[ret_key] for r in top])
    bb = np.mean([r[ret_key] for r in bottom])
    return tb, bb, tb - bb, len(top), len(bottom)


def analyse(rows):
    print("\n" + "=" * 70)
    print("SCORE BACKTEST — FUND-layer signal vs forward return (point-in-time)")
    print("=" * 70)
    print(f"panel: {len(rows)} observations "
          f"({len({r['ticker'] for r in rows})} names x {len(ASOF_DATES)} dates)")

    for ret_key, xkey, label in [("ret1y", "x_ret1y", "1-YEAR"),
                                 ("ret3y", "x_ret3y", "3-YEAR")]:
        print(f"\n----- {label} forward return -----")
        # rank IC per date (raw return) + pooled excess IC
        ic = _ic_by_date(rows, ret_key)
        if ic:
            for d, (v, n) in ic.items():
                print(f"  IC {d}: {v:+.3f}  (n={n})")
            vals = [v for v, _ in ic.values()]
            print(f"  mean per-date rank IC: {np.mean(vals):+.3f}")
        sub = [r for r in rows if r.get(xkey) is not None]
        if len(sub) >= 5:
            pooled = spearman([r["score"] for r in sub],
                              [r[xkey] for r in sub])
            print(f"  pooled rank IC (excess return): {pooled:+.3f}  "
                  f"(n={len(sub)})")
        # quantile spread on excess return
        qs = _quantile_spread([{**r, xkey: r.get(xkey)} for r in rows
                               if r.get(xkey) is not None], xkey)
        if qs:
            tb, bb, sp, nt, nb = qs
            print(f"  top-third excess ret:    {tb:+.1%}  (n={nt})")
            print(f"  bottom-third excess ret: {bb:+.1%}  (n={nb})")
            print(f"  TOP - BOTTOM spread:     {sp:+.1%}")

    # learned weights on pooled excess 1y (most data)
    print("\n----- learned weights (ridge on pooled excess 1y return) -----")
    sub = [r for r in rows if r.get("x_ret1y") is not None]
    X = [[r[f] if r[f] is not None else 0.0 for f in FEATURE_NAMES]
         for r in sub]
    y = [r["x_ret1y"] for r in sub]
    coef, r2 = ridge(X, y, lam=5.0)
    order = np.argsort(-np.abs(coef))
    for i in order:
        print(f"  {FEATURE_NAMES[i]:12s} std-coef {coef[i]:+.3f}")
    print(f"  in-sample R^2: {r2:.3f}")
    print("  (sign = direction of association with beating the peer group;")
    print("   magnitude = relative importance. Compare with the scorer's")
    print("   hand-set FUND weights: margin .40 / growth .30 / fcf .20.)")


# =========================================================================
# MULTI-SIGNAL TEST (extension B) — reconstruct valuation + momentum and rank
# every candidate signal by how well it predicts forward return.
# =========================================================================
# Point-in-time P/S is back-cast without needing historical share counts:
#     P/S(D) = ps_now * (price(D)/price_now) * (revenue_now/revenue(D))
# The price ratio uses adjusted closes (splits cancel); revenue ratio comes from
# the financials series; ps_now is today's P/S from the live CSV. Dilution
# between D and now is the only unmodelled term and is second-order for ranking.
# Prior-12m price change gives a momentum signal. We then score a panel of
# candidate signals on the SAME observations so they are directly comparable.

def _norm01(vals):
    """Min-max a list to 0..1 (None-safe; constant -> 0.5)."""
    xs = [v for v in vals if v is not None]
    if not xs:
        return [0.5 for _ in vals]
    lo, hi = min(xs), max(xs)
    if hi == lo:
        return [0.5 for _ in vals]
    return [((v - lo) / (hi - lo)) if v is not None else 0.5 for v in vals]


def build_panel_plus(tickers, ps_now):
    """Panel with reconstructed P/S and prior-12m momentum added per obs."""
    rows = []
    for t in tickers:
        prices = fetch_prices(t)
        fin = fetch_financials(t)
        if not prices or not fin:
            continue
        psn = ps_now.get(t)
        rev_now = None
        # newest FY revenue = the 'now' revenue anchor
        fy_all = sorted(fin)
        if fy_all:
            rev_now = fin[fy_all[-1]].get("revenue")
        p_now = _price_on_or_after(prices, "2026-01-01") or \
            (prices[max(prices)] if prices else None)
        for asof in ASOF_DATES:
            feat = pit_features(fin, asof)
            if feat is None:
                continue
            p0 = _price_on_or_after(prices, asof)
            if not p0:
                continue
            # reconstructed point-in-time P/S
            ps_d = None
            fy_dates = sorted([d for d in fin if d <= asof], reverse=True)
            rev_d = fin[fy_dates[0]].get("revenue") if fy_dates else None
            if psn and rev_now and rev_d and p_now and rev_d > 0:
                ps_d = psn * (p0 / p_now) * (rev_now / rev_d)
            # prior-12m momentum (return INTO the as-of date)
            p_prev = _price_on_or_after(prices, _shift_year(asof, -1))
            mom = (p0 / p_prev - 1) if p_prev else None
            p1 = _price_on_or_after(prices, _shift_year(asof, 1))
            p3 = _price_on_or_after(prices, _shift_year(asof, 3))
            rows.append({
                "ticker": t, "date": asof, **feat,
                "score": fund_score(feat),
                "ps": ps_d, "mom": mom,
                "ret1y": (p1 / p0 - 1) if p1 else None,
                "ret3y": (p3 / p0 - 1) if p3 else None,
            })
    _add_excess(rows, "ret1y")
    _add_excess(rows, "ret3y")
    return rows


def _signal_values(rows):
    """Build the candidate signals per row. Higher signal = expected higher
    return. Returns dict: signal_name -> list aligned with rows (None allowed)."""
    fund = [r["score"] for r in rows]
    cheap = [(-r["ps"]) if r["ps"] is not None else None for r in rows]  # low PS = good
    growth = [r["rev_growth"] for r in rows]
    margin = [r["margin"] for r in rows]
    trend = [r["trend"] for r in rows]
    mom = [r["mom"] for r in rows]
    contrarian = [-s for s in fund]                       # inverse of quality
    rev_mom = [r["mom"] for r in rows]
    # quality x cheap: combine normalised ranks (only where both present)
    nf = _norm01(fund)
    nc = _norm01([r["ps"] for r in rows])                 # high PS=1
    qxc = [nf[i] * (1 - nc[i]) for i in range(len(rows))]  # good & cheap
    # cheap minus momentum chasers etc. keep set focused:
    return {
        "FUND (quality)": fund,
        "CHEAP (low P/S)": cheap,
        "QUALITY x CHEAP": qxc,
        "CONTRARIAN (-quality)": contrarian,
        "MOMENTUM (prior 12m)": mom,
        "GROWTH (rev)": growth,
        "MARGIN": margin,
        "TREND (accel)": trend,
    }


def _sig_ic(sig, rows, ret_key):
    pairs = [(s, r[ret_key]) for s, r in zip(sig, rows)
             if s is not None and r.get(ret_key) is not None]
    if len(pairs) < 8:
        return float("nan"), 0
    xs, ys = zip(*pairs)
    return spearman(xs, ys), len(pairs)


def _sig_spread(sig, rows, ret_key):
    pairs = [(s, r[ret_key]) for s, r in zip(sig, rows)
             if s is not None and r.get(ret_key) is not None]
    if len(pairs) < 9:
        return float("nan")
    pairs.sort(key=lambda p: p[0])
    n = len(pairs)
    bot = [p[1] for p in pairs[: n // 3]]
    top = [p[1] for p in pairs[-(n // 3):]]
    return float(np.median(top) - np.median(bot))


def analyse_multi(rows):
    print("\n" + "=" * 74)
    print("MULTI-SIGNAL TEST — every angle ranked by predictive signal")
    print("=" * 74)
    print(f"panel: {len(rows)} obs ({len({r['ticker'] for r in rows})} US names "
          f"x up to {len(ASOF_DATES)} dates)")
    sigs = _signal_values(rows)
    # use EXCESS returns (peer-demeaned) so we measure the signal, not the year
    results = []
    for name, sig in sigs.items():
        ic1, n1 = _sig_ic(sig, rows, "x_ret1y")
        ic3, n3 = _sig_ic(sig, rows, "x_ret3y")
        sp1 = _sig_spread(sig, rows, "x_ret1y")
        sp3 = _sig_spread(sig, rows, "x_ret3y")
        results.append((name, ic1, ic3, sp1, sp3, n1))
    # rank by 3y IC (the score's design horizon), then 1y
    results.sort(key=lambda r: (-(r[2] if r[2] == r[2] else -9),
                                -(r[1] if r[1] == r[1] else -9)))
    print(f"\n  {'signal':24s}{'IC 1y':>8s}{'IC 3y':>8s}"
          f"{'spread1y':>10s}{'spread3y':>10s}")
    print("  " + "-" * 60)
    for name, ic1, ic3, sp1, sp3, n in results:
        print(f"  {name:24s}{ic1:+8.3f}{ic3:+8.3f}"
              f"{sp1:+9.0%}{sp3:+9.0%}")
    print("\n  IC = Spearman rank correlation of signal vs forward EXCESS return.")
    print("  Positive = signal works (high signal -> higher return).")
    print("  Negative = signal inverts (high signal -> LOWER return).")
    print("  spread = median(top third) - median(bottom third) excess return.")

    # ridge on the full feature set incl valuation + momentum
    print("\n----- ridge: full feature set vs excess 1y return -----")
    feats = ["rev_growth", "margin", "fcf_pos", "trend", "fcf_margin",
             "ps", "mom"]
    def _ok(r):
        if r.get("x_ret1y") is None:
            return False
        for f in feats:
            v = r.get(f)
            if v is None or not np.isfinite(v):
                return False
        return True
    sub = [r for r in rows if _ok(r)]
    X = [[float(r[f]) for f in feats] for r in sub]
    y = [r["x_ret1y"] for r in sub]
    coef, r2 = ridge(X, y, lam=5.0)
    for i in np.argsort(-np.abs(coef)):
        print(f"  {feats[i]:12s} std-coef {coef[i]:+.3f}")
    print(f"  in-sample R^2: {r2:.3f}  (n={len(sub)})")


def analyse_combo(rows):
    """Test the top-2 signals (CHEAP + TREND) combined at several weightings,
    vs each alone, to find the blend with the most forward-return signal. Both
    inputs are converted to per-date percentile ranks (0..1) so they are on the
    same scale before blending; higher = more attractive."""
    print("\n" + "=" * 74)
    print("COMBINED SIGNAL — CHEAP (low P/S) + TREND (accelerating) blends")
    print("=" * 74)

    # per-date percentile rank so cross-date pooling is fair
    def pct_by_date(rows, getter, invert=False):
        out = {}
        by_d = {}
        for i, r in enumerate(rows):
            v = getter(r)
            if v is not None and np.isfinite(v):
                by_d.setdefault(r["date"], []).append((i, v))
        ranks = [None] * len(rows)
        for d, lst in by_d.items():
            vals = sorted(lst, key=lambda p: p[1])
            n = len(vals)
            for rank, (i, _) in enumerate(vals):
                p = rank / (n - 1) if n > 1 else 0.5
                ranks[i] = (1 - p) if invert else p
        return ranks

    cheap_r = pct_by_date(rows, lambda r: r["ps"], invert=True)   # low PS -> high
    trend_r = pct_by_date(rows, lambda r: r["trend"])             # high trend -> high

    print(f"\n  {'blend (cheap:trend)':24s}{'IC 1y':>8s}{'IC 3y':>8s}"
          f"{'spr1y':>8s}{'spr3y':>8s}")
    print("  " + "-" * 56)
    best = None
    for w in [1.0, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.0]:
        combo = []
        for i in range(len(rows)):
            c, t = cheap_r[i], trend_r[i]
            if c is None and t is None:
                combo.append(None)
            elif c is None:
                combo.append(t)
            elif t is None:
                combo.append(c)
            else:
                combo.append(w * c + (1 - w) * t)
        ic1, _ = _sig_ic(combo, rows, "x_ret1y")
        ic3, _ = _sig_ic(combo, rows, "x_ret3y")
        sp1 = _sig_spread(combo, rows, "x_ret1y")
        sp3 = _sig_spread(combo, rows, "x_ret3y")
        label = (f"{w:.0%} cheap / {1-w:.0%} trend")
        avg_ic = np.nanmean([ic1, ic3])
        print(f"  {label:24s}{ic1:+8.3f}{ic3:+8.3f}{sp1:+8.0%}{sp3:+8.0%}")
        if best is None or avg_ic > best[1]:
            best = (label, avg_ic, ic1, ic3, sp1, sp3)
    print(f"\n  BEST avg-IC blend: {best[0]}  (IC1y {best[2]:+.3f}, "
          f"IC3y {best[3]:+.3f}, spread1y {best[4]:+.0%}, spread3y {best[5]:+.0%})")
    print("  (vs CHEAP alone = 100% cheap row; TREND alone = 0% cheap row)")


def analyse_by_strategy(rows):
    """Re-run the signal ranking SEPARATELY within each strategy bucket (dca /
    cycle / catalyst) to check whether 'cheapness wins' holds per-strategy or is
    only a pooled artifact. Tags come from the live STRATEGY map."""
    from scoring.score_holdings import STRATEGY
    print("\n" + "=" * 74)
    print("PER-STRATEGY SIGNAL TEST — does the conclusion hold within each bucket?")
    print("=" * 74)
    for strat in ["dca", "cycle", "catalyst"]:
        sub = [r for r in rows if STRATEGY.get(r["ticker"]) == strat]
        names = {r["ticker"] for r in sub}
        print(f"\n----- {strat.upper()}  ({len(names)} names, {len(sub)} obs) -----")
        if len(sub) < 12:
            print("  (too few observations for a stable read)")
        sigs = _signal_values(sub)
        rank = []
        for name, sig in sigs.items():
            ic1, n1 = _sig_ic(sig, sub, "x_ret1y")
            ic3, _ = _sig_ic(sig, sub, "x_ret3y")
            rank.append((name, ic1, ic3, n1))
        rank.sort(key=lambda r: -(np.nanmean([r[1], r[2]])
                                  if not (r[1] != r[1] and r[2] != r[2]) else -9))
        print(f"  {'signal':24s}{'IC 1y':>8s}{'IC 3y':>8s}{'n':>5s}")
        for name, ic1, ic3, n in rank:
            print(f"  {name:24s}{ic1:+8.3f}{ic3:+8.3f}{n:5d}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fetch", action="store_true",
                    help="populate the on-disk cache from stockanalysis.com")
    ap.add_argument("--multi", action="store_true",
                    help="run the multi-signal test (extension B): reconstruct "
                         "valuation + momentum and rank every candidate signal")
    ap.add_argument("--combo", action="store_true",
                    help="test CHEAP+TREND combined at several weightings")
    ap.add_argument("--by-strategy", action="store_true",
                    help="rank signals separately within dca / cycle / catalyst")
    ap.add_argument("--csv", default=default_csv())
    args = ap.parse_args()

    fund = load_fundamentals(args.csv)
    tickers = [t for t in fund if "." not in t]   # US only (price API)

    if args.fetch:
        fetch_all(tickers)
        return

    if not any((CACHE / f"px_{t}.json").exists() for t in tickers):
        sys.exit("Cache empty. Run with --fetch first.")

    if args.multi or args.combo or args.by_strategy:
        ps_now = {t: fund[t].get("ps_ratio") for t in tickers}
        rows = build_panel_plus(tickers, ps_now)
        if args.multi:
            analyse_multi(rows)
        if args.combo:
            analyse_combo(rows)
        if args.by_strategy:
            analyse_by_strategy(rows)
        return

    rows = build_panel(tickers)
    analyse(rows)


if __name__ == "__main__":
    main()
