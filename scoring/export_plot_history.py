#!/usr/bin/env python3
# =========================================================================
# PLOT-HISTORY EXPORTER — price series for the dashboard's Plot tab
# =========================================================================
# WHY: the GitHub Pages dashboard (docs/) is fully static and the browser can
# neither run yfinance nor fetch a price API cross-origin (Yahoo sends no CORS
# headers; stooq now gates requests behind a JS proof-of-work). So — mirroring
# the conviction.json pattern — this script pre-fetches price history ONCE,
# server-side, and writes docs/plot_history.json for the page to load and draw
# entirely client-side.
#
# It reads the ticker universe from docs/conviction.json (so the Plot tab
# always covers exactly the names the table shows), fetches ~5y of WEEKLY
# closes per ticker from Yahoo's chart endpoint (weekly keeps the payload
# small over a 5-year window while still rendering smoothly for 1w..all), and
# stores each series as {ticker: {"t": [ISO dates], "c": [closes]}}.
#
# Unlike the scoring engine this is NOT deterministic (it hits the live feed);
# it is a data-refresh utility, run when the dashboard's price history should
# be updated. The scores in conviction.json remain the deterministic artifact.
#
# Usage:
#   python3 scoring/export_plot_history.py            # default paths
#   python3 scoring/export_plot_history.py --interval 1d   # daily (bigger)
#   python3 scoring/export_plot_history.py --range 10y

import argparse
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Repo-root-relative defaults so the script works from anywhere.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_IN = _REPO_ROOT / "docs" / "conviction.json"
_DEFAULT_OUT = _REPO_ROOT / "docs" / "plot_history.json"

_CHART_URL = ("https://query1.finance.yahoo.com/v8/finance/chart/"
              "{ticker}?range={range}&interval={interval}")
# A browser UA is required — the endpoint 429s bare/script agents.
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; plot-history-exporter)"}

# Conviction ticker -> Yahoo chart symbol, for names whose feed symbol differs
# from the ticker used in the scorer/watchlist.
_YAHOO_ALIASES = {}


def _tickers_from_conviction(path):
    """Ticker universe = every record in conviction.json (deduped, ordered)."""
    payload = json.loads(Path(path).read_text())
    seen, out = set(), []
    for rec in payload.get("records", []):
        t = rec.get("ticker")
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _fetch_history(ticker, rng, interval, retries=3, delay=1.0):
    """(dates, closes) parallel lists for a ticker, or ([], []) on failure.
    Rows with a null close (holiday gaps) are dropped so the series is clean."""
    symbol = _YAHOO_ALIASES.get(ticker, ticker)
    url = _CHART_URL.format(ticker=symbol, range=rng, interval=interval)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=_HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                doc = json.load(resp)
            result = doc["chart"]["result"][0]
            ts = result.get("timestamp") or []
            closes = result["indicators"]["quote"][0].get("close") or []
            dates, vals = [], []
            for t, c in zip(ts, closes):
                if c is None:
                    continue
                dates.append(datetime.fromtimestamp(t, timezone.utc)
                             .strftime("%Y-%m-%d"))
                vals.append(round(float(c), 4))
            if vals:
                return dates, vals
        except (urllib.error.URLError, urllib.error.HTTPError,
                KeyError, IndexError, ValueError, TimeoutError):
            pass
        if attempt < retries - 1:
            time.sleep(delay)
    return [], []


def export_plot_history(in_path=_DEFAULT_IN, out_path=_DEFAULT_OUT,
                        rng="5y", interval="1wk", pause=0.25):
    """Fetch price history for every ticker in conviction.json and write the
    Plot-tab payload to out_path. Returns the written payload dict."""
    tickers = _tickers_from_conviction(in_path)
    history, failed = {}, []
    for i, tk in enumerate(tickers, 1):
        dates, closes = _fetch_history(tk, rng, interval)
        if closes:
            history[tk] = {"t": dates, "c": closes}
        else:
            failed.append(tk)
        print(f"[{i:>3}/{len(tickers)}] {tk:14s} "
              f"{'OK ' + str(len(closes)) + ' pts' if closes else 'FAILED'}")
        time.sleep(pause)  # be gentle on the endpoint

    payload = {
        "generated_utc": datetime.now(timezone.utc)
                          .strftime("%Y-%m-%d %H:%M UTC"),
        "range": rng,
        "interval": interval,
        "count": len(history),
        "missing": failed,
        "history": history,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    print(f"\nwrote {out_path}  ({len(history)} series, "
          f"{len(failed)} missing)")
    if failed:
        print("missing:", ", ".join(failed))
    return payload


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="in_path", default=str(_DEFAULT_IN),
                    help="conviction.json to read the ticker universe from")
    ap.add_argument("--out", dest="out_path", default=str(_DEFAULT_OUT),
                    help="output plot_history.json path")
    ap.add_argument("--range", default="5y",
                    help="history window (e.g. 1y, 5y, 10y, max)")
    ap.add_argument("--interval", default="1wk",
                    help="sampling interval (1d, 1wk, 1mo)")
    ap.add_argument("--pause", type=float, default=0.25,
                    help="seconds to sleep between requests")
    args = ap.parse_args()
    export_plot_history(args.in_path, args.out_path,
                        args.range, args.interval, args.pause)


if __name__ == "__main__":
    main()
