#!/usr/bin/env python3
"""Fill the three structurally-blank backtest fields with LOOK-AHEAD-CLEAN,
point-in-time-2023 values, editing fundamentals_2023_universe.csv in place.

The 2023 snapshot left fwd_rev_growth / fwd_eps_growth / pct_above_200dma blank
because the historical /financials/ pages carry no forward analyst estimates and
no daily price series. With all three absent, the engine's GROWTH score collapses
to its secular-runway tag (5/10) and the CYCLE (C) layer collapses to its cycle
tag (5/10) — see AGENTS.md and the backtest README. This script reconstructs the
three fields WITHOUT using any post-2023 data, so the GROWTH and CYCLE layers
vary continuously again while the backtest stays honest.

WHAT IS FILLED (and why each is look-ahead-clean):

  pct_above_200dma  — a PURE point-in-time technical. Computed from the trailing
      200 daily closes ENDING on the as-of date (2023-12-29, the FY2023 year-end),
      via stockanalysis.com's 5Y daily history API. The 200-day window ends on the
      as-of date, so no future price ever enters it. US names only: the foreign
      history endpoint is not cleanly reachable, so the ~10 foreign tickers are
      left blank (engine drops + reweights, exactly like a recent IPO with no
      200DMA).

  fwd_rev_growth    — a TRAILING-CAGR PROXY, not a true forward estimate. The
      genuine forward field would need the Dec-2023 analyst consensus, which is
      not archived anywhere reachable; using today's consensus would be look-ahead
      bias. Instead we use the geometric-mean CAGR of the already-sourced
      rev_growth_hist column (trailing full-FY rev YoY %, all <= FY2023). This is
      the growth a 2023 observer could actually compute from reported actuals.
      Labelled a proxy in the CSV header; it feeds the same band as the forward
      field so GROWTH/FUND stop collapsing.

  fwd_eps_growth    — a TRAILING-CAGR PROXY from epsDiluted ACTUALS restricted to
      fiscalYear <= 2023 (the forward 2024-2027 estimate columns on the page are
      explicitly excluded). CAGR from the earliest (>=2021) to the FY2023 actual.
      Sign-change cases (a loss year in either endpoint) yield no real CAGR and
      are left blank — an EPS CAGR across a sign flip is meaningless, not zero.

Editing policy (mirrors --fill-ttm in the production engine): preserve the `#`
comment header and EVERY other cell; only the three target columns are touched,
and only when a clean value is obtained (never overwrite an existing value with
a blank).

Usage:
    PORTFOLIO_USE=ai python3 scoring/backtest/fill_proxies_2023.py
    PORTFOLIO_USE=ai python3 scoring/backtest/fill_proxies_2023.py --dry-run
"""
import csv
import datetime
import importlib.util
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent

# reuse the fundamentals sourcer's URL/base + array helpers so the foreign
# exchange mapping and parsing stay in one place.
_spec = importlib.util.spec_from_file_location("src2023", HERE / "source_2023.py")
_src = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_src)

CSV_PATH = HERE / "fundamentals_2023_universe.csv"

# FY2023 fiscal-year-end: the as-of date for the 200DMA window. The last trading
# day on or before this date anchors the trailing-200 average.
ASOF = datetime.date(2023, 12, 29)
DMA_WINDOW = 200

# columns this script is allowed to write
_TARGETS = ("pct_above_200dma", "fwd_rev_growth", "fwd_eps_growth")


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")


# ---------------------------------------------------------------------------
# 1. pct_above_200dma — trailing-200 daily MA as of 2023-12-29 (US names)
# ---------------------------------------------------------------------------
def pct_above_200dma(ticker):
    """(price - 200DMA)/200DMA*100 as of ASOF, from the 5Y daily history.
    Returns None for foreign names (history endpoint not reachable) or when
    fewer than DMA_WINDOW closes precede the as-of date (too recently listed)."""
    if ticker in _src._FOREIGN_CODE:
        return None  # foreign history API not cleanly reachable; leave blank
    url = (f"https://stockanalysis.com/api/symbol/s/{ticker.upper()}"
           f"/history?range=5Y&period=Daily")
    try:
        d = json.loads(_get(url))
    except Exception:
        return None
    rows = d.get("data")
    if not isinstance(rows, list) or not rows:
        return None
    # rows are newest-first dicts {t: 'YYYY-MM-DD', c: close}; build oldest-first
    series = []
    for r in rows:
        try:
            series.append((datetime.date.fromisoformat(r["t"]), float(r["c"])))
        except (KeyError, ValueError, TypeError):
            continue
    series.sort(key=lambda x: x[0])
    # last index on or before the as-of date
    asof_idxs = [i for i, (dt, _) in enumerate(series) if dt <= ASOF]
    if not asof_idxs:
        return None
    idx = asof_idxs[-1]
    if idx + 1 < DMA_WINDOW:
        return None  # not enough history before as-of -> no 200DMA
    window = [c for _, c in series[idx - DMA_WINDOW + 1: idx + 1]]
    dma = sum(window) / len(window)
    if dma == 0:
        return None
    price = series[idx][1]
    return (price - dma) / dma * 100


# ---------------------------------------------------------------------------
# 2. fwd_rev_growth proxy — geometric-mean CAGR of the trailing rev_growth_hist
#    (already in the CSV; no network). All entries are <= FY2023 by construction.
# ---------------------------------------------------------------------------
def rev_cagr_proxy(rev_growth_hist):
    ys = []
    for x in (rev_growth_hist or "").split("|"):
        x = x.strip()
        if x:
            try:
                ys.append(float(x))
            except ValueError:
                return None
    if not ys:
        return None
    prod = 1.0
    for y in ys:
        prod *= (1 + y / 100.0)
    if prod <= 0:
        return None  # cumulative wipeout -> CAGR undefined
    return (prod ** (1.0 / len(ys)) - 1) * 100.0


# ---------------------------------------------------------------------------
# 3. fwd_eps_growth proxy — CAGR of epsDiluted ACTUALS, fiscalYear <= 2023 only
#    (forward 2024-2027 estimate columns on the page are excluded).
# ---------------------------------------------------------------------------
def eps_cagr_proxy(ticker):
    if ticker in _src._FOREIGN_CODE:
        return None  # foreign EPS series inconsistently formatted; skip
    try:
        h = _get(_src._base(ticker) + "/financials/")
    except Exception:
        return None
    fy = _src._arr(h, "fiscalYear")
    eps = _src._arr(h, "epsDiluted")
    pairs = []
    for y, v in zip(fy, eps):
        try:
            yi = int(y.strip().strip('"'))
        except ValueError:
            continue
        if yi > 2023:
            continue  # exclude forward estimate columns
        vv = _src._num(v)
        if vv is None:
            continue
        pairs.append((yi, vv))
    pairs.sort()
    if len(pairs) < 2:
        return None
    (y0, v0), (y1, v1) = pairs[0], pairs[-1]
    if v0 <= 0 or v1 <= 0:
        return None  # CAGR across a sign change is meaningless -> blank
    n = y1 - y0
    if n <= 0:
        return None
    return ((v1 / v0) ** (1.0 / n) - 1) * 100.0


def _fmt(v):
    """Two-decimal string; blank stays blank."""
    return "" if v is None else f"{v:.2f}"


def main():
    dry = "--dry-run" in sys.argv

    raw = CSV_PATH.read_text()
    comment_lines, body_lines = [], []
    for ln in raw.splitlines(keepends=True):
        (comment_lines if ln.startswith("#") else body_lines).append(ln)

    reader = csv.DictReader(io.StringIO("".join(body_lines)))
    header = list(reader.fieldnames)
    rows = list(reader)

    filled = {c: 0 for c in _TARGETS}
    skipped_foreign = 0
    for r in rows:
        t = r["ticker"].strip()

        # rev proxy from the existing column (no network) — only if currently blank
        if not (r.get("fwd_rev_growth") or "").strip():
            v = rev_cagr_proxy(r.get("rev_growth_hist"))
            if v is not None:
                r["fwd_rev_growth"] = _fmt(v)
                filled["fwd_rev_growth"] += 1

        # 200DMA (network) — only if currently blank
        if not (r.get("pct_above_200dma") or "").strip():
            v = pct_above_200dma(t)
            if v is not None:
                r["pct_above_200dma"] = _fmt(v)
                filled["pct_above_200dma"] += 1
            elif t in _src._FOREIGN_CODE:
                skipped_foreign += 1

        # EPS proxy (network) — only if currently blank
        if not (r.get("fwd_eps_growth") or "").strip():
            v = eps_cagr_proxy(t)
            if v is not None:
                r["fwd_eps_growth"] = _fmt(v)
                filled["fwd_eps_growth"] += 1

        print(f"  [fill] {t:10s} "
              f"rev={r.get('fwd_rev_growth') or '-':>7s} "
              f"eps={r.get('fwd_eps_growth') or '-':>7s} "
              f"200dma={r.get('pct_above_200dma') or '-':>7s}")
        if t not in _src._FOREIGN_CODE:
            time.sleep(0.15)  # be polite to the source

    print(f"\n  filled: rev={filled['fwd_rev_growth']} "
          f"eps={filled['fwd_eps_growth']} "
          f"200dma={filled['pct_above_200dma']} "
          f"(foreign 200dma left blank: {skipped_foreign})")

    if dry:
        print("  --dry-run: CSV not written")
        return

    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=header)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in header})
    CSV_PATH.write_text("".join(comment_lines) + out.getvalue())
    print(f"  wrote {CSV_PATH.name} (preserved {len(comment_lines)} # header "
          f"lines, {len(rows)} rows)")


if __name__ == "__main__":
    main()
