#!/usr/bin/env python3
# =========================================================================
# INTRINSIC-VALUE EXPORTER — fair-value estimates for the dashboard's
# "Intrinsic" tab
# =========================================================================
# WHY: the GitHub Pages dashboard (docs/) is fully static and the browser can
# neither run yfinance nor fetch a valuation feed cross-origin. So — mirroring
# the conviction.json / plot_history.json pattern — this script computes the
# AlphaSpread-style intrinsic value ONCE, server-side, and writes
# docs/intrinsic.json for the page to load and render entirely client-side.
#
# It reads the ticker universe from docs/conviction.json (so the Intrinsic tab
# always covers exactly the names the Stock table shows) and, for every name,
# calls portfolio.intrinsic.compute_intrinsic_value — the same anchored-multiple
# model documented in intrinsic.ipynb:
#
#     fair_pe   = min(own_forward_PE, pe_ceiling)   # pe_ceiling = 21x
#     intrinsic = forward_EPS * fair_pe
#
# Each row stores the market price, the intrinsic value, the % upside, a
# +/-5% verdict, and the model inputs (fair P/E, DCF context value, sell-side
# analyst target range). Names with neither positive forward/trailing EPS nor
# positive free cash flow are marked eligible=false (shown as N/A on the page).
#
# Like export_plot_history.py this is NOT deterministic (it hits the live
# yfinance feed); it is a data-refresh utility. The scores in conviction.json
# remain the deterministic artifact. yfinance's per-share `.info` scalars
# (forwardEps, price, shares, beta) are correct on a CI runner even though the
# repo's dev-container price *series* feed is date-corrupted.
#
# Usage:
#   PORTFOLIO_USE=ai python3 scoring/export_intrinsic.py            # default paths
#   PORTFOLIO_USE=ai python3 scoring/export_intrinsic.py --tickers MSFT,NVDA

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Repo-root-relative defaults so the script works from anywhere, and so the
# `portfolio` package imports cleanly when run as a bare script.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_DEFAULT_IN = _REPO_ROOT / "docs" / "conviction.json"
_DEFAULT_OUT = _REPO_ROOT / "docs" / "intrinsic.json"


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


def _round(x, n=2):
    """Round a float for a compact JSON payload; pass None through."""
    if x is None:
        return None
    try:
        return round(float(x), n)
    except (TypeError, ValueError):
        return None


def _record(tk, **overrides):
    """Compute one intrinsic-value row for the dashboard.

    Returns a JSON-friendly dict. On any fetch/compute error the row is still
    emitted with eligible=false and a reason, so the tab can list the name.
    """
    from portfolio.intrinsic import compute_intrinsic_value, _verdict
    import yfinance as yf

    try:
        t = yf.Ticker(tk)
        try:
            info = t.info or {}
        except Exception:
            info = {}
        v = compute_intrinsic_value(tk, info=info, ticker_obj=t, **overrides)
        name = info.get("shortName") or info.get("longName") or tk
    except Exception as e:  # network / parse failure — emit an N/A row
        return {
            "ticker": tk, "name": tk, "eligible": False,
            "reason": f"error: {e}", "price": None, "intrinsic": None,
            "upside_pct": None, "verdict": "N/A", "fair_pe": None,
            "dcf_value": None, "multiples_value": None,
            "analyst_low": None, "analyst_mean": None, "analyst_high": None,
            "analyst_n": None,
        }

    assumptions = v.get("assumptions") or {}
    up = v.get("upside_pct")
    return {
        "ticker": tk,
        "name": name,
        "eligible": bool(v.get("eligible")),
        "reason": v.get("reason", ""),
        "price": _round(v.get("price")),
        "intrinsic": _round(v.get("intrinsic")),
        "upside_pct": _round(up, 1),
        "verdict": _verdict(up) if v.get("eligible") else "N/A",
        "fair_pe": _round(assumptions.get("fair_pe")),
        "dcf_value": _round(v.get("dcf_value")),
        "multiples_value": _round(v.get("multiples_value")),
        "analyst_low": _round(v.get("analyst_low")),
        "analyst_mean": _round(v.get("analyst_mean")),
        "analyst_high": _round(v.get("analyst_high")),
        "analyst_n": v.get("analyst_n"),
    }


def export_intrinsic(in_path=_DEFAULT_IN, out_path=_DEFAULT_OUT,
                     tickers=None, pause=0.2, **overrides):
    """Compute intrinsic value for every ticker in conviction.json and write
    the Intrinsic-tab payload to out_path. Returns the written payload dict."""
    if tickers is None:
        tickers = _tickers_from_conviction(in_path)

    records, eligible = [], 0
    for i, tk in enumerate(tickers, 1):
        rec = _record(tk, **overrides)
        records.append(rec)
        if rec["eligible"]:
            eligible += 1
        up = (f"{rec['upside_pct']:+.0f}%"
              if rec.get("upside_pct") is not None else "-")
        print(f"[{i:>3}/{len(tickers)}] {tk:14s} "
              f"{'OK ' if rec['eligible'] else 'N/A'} {up:>7}  "
              f"{rec.get('verdict', '')}")
        time.sleep(pause)  # be gentle on the endpoint

    payload = {
        "generated_utc": datetime.now(timezone.utc)
                          .strftime("%Y-%m-%d %H:%M UTC"),
        "method": "anchored-multiple",
        "pe_ceiling": 21.0,
        "band_pct": 5.0,
        "count": len(records),
        "eligible": eligible,
        "records": records,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    print(f"\nwrote {out_path}  ({len(records)} names, {eligible} valued)")
    return payload


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="in_path", default=str(_DEFAULT_IN),
                    help="conviction.json to read the ticker universe from")
    ap.add_argument("--out", dest="out_path", default=str(_DEFAULT_OUT),
                    help="output intrinsic.json path")
    ap.add_argument("--tickers", default=None,
                    help="comma-separated tickers to value instead of the "
                         "conviction.json universe")
    ap.add_argument("--pause", type=float, default=0.2,
                    help="seconds to sleep between requests")
    args = ap.parse_args(argv)
    tickers = ([t.strip().upper() for t in args.tickers.split(",")]
               if args.tickers else None)
    export_intrinsic(args.in_path, args.out_path,
                     tickers=tickers, pause=args.pause)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
