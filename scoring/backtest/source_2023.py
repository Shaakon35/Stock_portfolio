#!/usr/bin/env python3
"""Automated POINT-IN-TIME FY2023 fundamentals sourcer for the backtest.

Reuses the SAME data source the engine uses (stockanalysis.com /financials/
pages with the embedded `financialData` arrays) but pins every metric to the
FY2023 column, located by the `fiscalYear` / `datekey` arrays on each page (the
column whose label is 2023, or whose datekey starts with 2023). This is the
real point-in-time data — no look-ahead, no live (TTM/2026) column.

Per ticker it pulls:
  /financials/                      -> revenue, revenueGrowth(+hist),
                                       grossMargin, profitMargin(+hist), netIncome
  /financials/ratios/               -> pegRatio, ps, marketCap, lastClosePrice
  /financials/cash-flow-statement/  -> fcf (sign -> fcf_positive)

and writes a CSV row in the engine's schema. fwd_rev_growth / fwd_eps_growth /
pct_above_200dma / eps_beat_* are left blank (not on the historical pages); the
engine drops blank sub-scores and redistributes weight (per AGENTS.md), so the
score rests on the obtainable point-in-time fields.

Usage:
    PORTFOLIO_USE=ai python3 scoring/backtest/source_2023.py TICKER [TICKER...]
    PORTFOLIO_USE=ai python3 scoring/backtest/source_2023.py --batch 1
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# foreign-exchange URL mapping (mirrors score_holdings._FIN_EXCH conventions)
_EXCH = {
    "KS": ("krx", lambda c: c.split(".")[0] if "." in c else c),
    "HK": ("hkg", lambda c: c.lstrip("0") or "0"),
    "AS": ("ams", lambda c: c),
    "DE": ("etr", lambda c: c),
    "SW": ("swx", lambda c: c),
}
# FX -> USD (AGENTS.md rates) and per-ticker reporting currency for the
# foreign-mktcap derivation (ps x revenue x FX).
_FX = {"KRW": 1 / 1350.0, "HKD": 1 / 7.8, "EUR": 1.08, "USD": 1.0}
_CCY = {
    "000660.KS": "KRW", "005930.KS": "KRW",
    "0700.HK": "HKD", "1810.HK": "HKD", "9618.HK": "HKD", "9880.HK": "HKD",
    "9988.HK": "HKD", "BESI.AS": "EUR", "SIE.DE": "EUR", "SMHN.DE": "EUR",
}

# explicit KRX/HK numeric codes
_FOREIGN_CODE = {
    "000660.KS": ("krx", "000660"), "005930.KS": ("krx", "005930"),
    "0700.HK": ("hkg", "0700"), "1810.HK": ("hkg", "1810"),
    "9618.HK": ("hkg", "9618"), "9880.HK": ("hkg", "9880"),
    "9988.HK": ("hkg", "9988"), "BESI.AS": ("ams", "BESI"),
    "SIE.DE": ("etr", "SIE"), "SMHN.DE": ("etr", "SMHN"),
}


def _base(ticker):
    if ticker in _FOREIGN_CODE:
        ex, code = _FOREIGN_CODE[ticker]
        return f"https://stockanalysis.com/quote/{ex}/{code}"
    return f"https://stockanalysis.com/stocks/{ticker.lower()}"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")


def _num(s):
    s = s.strip().strip('"')
    if s in ("", "null", "-", "N/A"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _arr(html, key):
    """Return the raw list for `key:[...]` (strings stripped) or []."""
    m = re.search(re.escape(key) + r":\[([^\]]+)\]", html)
    if not m:
        return []
    return [p.strip() for p in m.group(1).split(",")]


def _fy_index(html, year="2023"):
    """Index of the FY2023 column via fiscalYear, else datekey starting 2023."""
    fy = _arr(html, "fiscalYear")
    for i, v in enumerate(fy):
        if v.strip().strip('"') == year:
            return i
    dk = _arr(html, "datekey")
    for i, v in enumerate(dk):
        if v.strip().strip('"').startswith(year):
            return i
    return None


def _at(html, key, idx, pct=False, scale=1.0):
    a = _arr(html, key)
    if idx is None or idx >= len(a):
        return None
    v = _num(a[idx])
    if v is None:
        return None
    return v * (100 if pct else 1) * scale


def _series_from(html, key, idx):
    """Full-FY series from index idx onward (newest-first), as percentages."""
    a = _arr(html, key)
    if idx is None:
        return []
    out = []
    for v in a[idx:]:
        n = _num(v)
        out.append(round(n * 100, 2) if n is not None else None)
    return [v for v in out if v is not None]


def scrape_2023(ticker):
    """Return a CSV-schema dict for ticker's FY2023 column, or None on failure."""
    base = _base(ticker)
    try:
        inc = _get(base + "/financials/")
    except Exception as e:
        print(f"  [src] {ticker}: financials fetch FAILED ({type(e).__name__})")
        return None
    idx = _fy_index(inc)
    if idx is None:
        print(f"  [src] {ticker}: no FY2023 column on financials page")
        return None

    revenue = _at(inc, "revenue", idx)
    gross_m = _at(inc, "grossMargin", idx, pct=True)
    net_m = _at(inc, "profitMargin", idx, pct=True)
    rev_hist = _series_from(inc, "revenueGrowth", idx)
    nm_hist = _series_from(inc, "profitMargin", idx)
    ttm_rev = rev_hist[0] if rev_hist else None

    peg = ps = mktcap = None
    try:
        rat = _get(base + "/financials/ratios/")
        ridx = _fy_index(rat)
        peg = _at(rat, "pegRatio", ridx)
        ps = _at(rat, "ps", ridx)
        mktcap = _at(rat, "marketCap", ridx)
    except Exception:
        pass
    if mktcap and ps is None and revenue:
        ps = round(mktcap / revenue, 2)
    # Foreign / ADR pages carry no marketCap array; derive it from
    # ps x FY2023 revenue (reporting currency) and FX-convert to USD.
    if mktcap is None and ps and revenue:
        fx = _FX.get(_CCY.get(ticker, "USD"), 1.0)
        mktcap = ps * revenue * fx

    fcf_pos = ""
    try:
        cf = _get(base + "/financials/cash-flow-statement/")
        cidx = _fy_index(cf)
        fcf = _at(cf, "fcf", cidx)
        if fcf is not None:
            fcf_pos = "1" if fcf > 0 else "0"
    except Exception:
        pass

    mktcap_b = round(mktcap / 1e9, 2) if mktcap else ""
    row = {
        "ticker": ticker,
        "mktcap_b": mktcap_b,
        "fwd_rev_growth": "",          # not on historical pages -> blank
        "ttm_rev_growth": ttm_rev if ttm_rev is not None else "",
        "fwd_eps_growth": "",          # blank
        "gross_margin": round(gross_m, 2) if gross_m is not None else "",
        "net_margin": round(net_m, 2) if net_m is not None else "",
        "fcf_positive": fcf_pos,
        "peg": round(peg, 2) if peg is not None else "",
        "ps_ratio": round(ps, 2) if ps is not None else "",
        "pct_above_200dma": "",        # blank
        "pct_below_52w_high": "",      # structurally unsourceable
        "eps_beat_rate": "",
        "eps_beat_streak": "",
        "rev_growth_hist": "|".join(f"{v}" for v in rev_hist),
        "net_margin_hist": "|".join(f"{v}" for v in nm_hist),
    }
    print(f"  [src] {ticker}: mktcap={mktcap_b}B gm={row['gross_margin']} "
          f"nm={row['net_margin']} peg={row['peg']} ps={row['ps_ratio']} "
          f"fcf={fcf_pos} ttm={row['ttm_rev_growth']} "
          f"revhist=[{row['rev_growth_hist'][:30]}]")
    return row


COLUMNS = ["ticker", "mktcap_b", "fwd_rev_growth", "ttm_rev_growth",
           "fwd_eps_growth", "gross_margin", "net_margin", "fcf_positive",
           "peg", "ps_ratio", "pct_above_200dma", "pct_below_52w_high",
           "eps_beat_rate", "eps_beat_streak", "rev_growth_hist",
           "net_margin_hist"]


UNIVERSE_CSV = Path(__file__).resolve().parent / "fundamentals_2023_universe.csv"


def _append_to_csv(rows, order):
    """Append `rows` (dict ticker->record) to the universe CSV in `order`,
    preserving the leading '#' header and skipping tickers already present."""
    import csv
    raw = UNIVERSE_CSV.read_text().splitlines(keepends=True)
    comments = [ln for ln in raw if ln.lstrip().startswith("#")]
    data = [ln for ln in raw if not ln.lstrip().startswith("#")]
    have = set()
    if data:
        for r in csv.DictReader(data):
            have.add((r.get("ticker") or "").strip())
    existing = list(csv.DictReader(data)) if data else []
    added = 0
    for t in order:
        if t in rows and t not in have:
            existing.append({k: rows[t].get(k, "") for k in COLUMNS})
            added += 1
    with open(UNIVERSE_CSV, "w", newline="") as fh:
        fh.writelines(comments)
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(existing)
    print(f"  [csv] appended {added} rows -> {UNIVERSE_CSV.name} "
          f"(total {len(existing)})")


def main():
    args = sys.argv[1:]
    append = False
    if args and args[0] == "--append":
        append = True
        args = args[1:]
    if args and args[0] == "--batch":
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "universe_2023", Path(__file__).resolve().parent / "universe_2023.py")
        U = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(U)
        tickers = U.BATCHES[int(args[1]) - 1]
    else:
        tickers = args
    out = {}
    fails = []
    for i, t in enumerate(tickers, 1):
        row = scrape_2023(t)
        if row:
            out[t] = row
        else:
            fails.append(t)
        time.sleep(0.3)
    if append:
        _append_to_csv(out, tickers)
    print("\n===JSON===")
    print(json.dumps({"rows": out, "fails": fails}))


if __name__ == "__main__":
    main()
