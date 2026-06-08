"""
watchlist_verifier.py
---------------------------------------------------------------------------
Compares the fundamentals stored in your watchlist table against live data
pulled from Yahoo Finance (via yfinance), and flags where they disagree.

Run locally:
    pip install yfinance
    python watchlist_verifier.py

It imports WATCHLIST_STOCKS from your existing watchlist file. By default it
expects that file to be importable as `config.watchlist` (the repo's standard
location). If running from a different folder, adjust WATCHLIST_MODULE below.

Note on Yahoo: yfinance reads from an unofficial Yahoo endpoint, so it can
occasionally return gaps or break after a Yahoo-side change. Missing fields
are shown as "n/a" rather than guessed.
---------------------------------------------------------------------------
"""

import os
import sys
import time
import importlib

import yfinance as yf

# ---------------------------- config ---------------------------------------
# Default: import from the repo's config/watchlist.py
# If you copied watchlist data to a standalone file, change this to its module name
WATCHLIST_MODULE = "config.watchlist"
PAUSE_BETWEEN_TICKERS = 0.4          # seconds between calls, to be gentle on Yahoo
PCT_DIFF_THRESHOLD = 25.0            # % gap that triggers a "differs" flag
# ---------------------------------------------------------------------------

# Ensure the repo root is on the path so config/ is importable
try:
    REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
except NameError:
    REPO_ROOT = os.getcwd()
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def load_watchlist():
    """Import the WATCHLIST_STOCKS list from your watchlist file."""
    try:
        module = importlib.import_module(WATCHLIST_MODULE)
        return module.WATCHLIST_STOCKS
    except ImportError:
        raise SystemExit(
            f"Could not import '{WATCHLIST_MODULE}'. Put this script in the same "
            f"folder as your watchlist file, or edit WATCHLIST_MODULE at the top."
        )


def parse_number(raw):
    """Turn a messy table string ('75B', '+56.5%', '11,067x', '—') into a float.
    Returns None when there's nothing meaningful to compare against."""
    if raw is None:
        return None
    s = str(raw).strip()
    if s in ("", "—", "N/A", "Pre-rev", "Neg"):
        return None
    # drop decorative characters
    for ch in ("$", "+", ",", "%", "x", "~", "*", " "):
        s = s.replace(ch, "")
    # handle magnitude suffixes (T/B/M/K)
    multiplier = 1.0
    if s and s[-1] in ("T", "B", "M", "K"):
        multiplier = {"T": 1e12, "B": 1e9, "M": 1e6, "K": 1e3}[s[-1]]
        s = s[:-1]
    try:
        return float(s) * multiplier
    except ValueError:
        return None


def pct(fraction):
    """Yahoo gives margins/growth as fractions (0.354). Convert to percent."""
    return fraction * 100 if isinstance(fraction, (int, float)) else None


def fetch_live(ticker):
    """Pull the fields we care about from Yahoo. Returns {field: value or None}."""
    tk = yf.Ticker(ticker)
    try:
        info = tk.info or {}
    except Exception:
        info = {}

    def g(key):
        val = info.get(key)
        return val if isinstance(val, (int, float)) else None

    live = {
        "price":         g("currentPrice") or g("regularMarketPrice"),
        "mkt_cap":       g("marketCap"),
        "pe":            g("trailingPE"),
        "eps":           g("trailingEps"),
        "net_income":    g("netIncomeToCommon"),
        "profit_margin": pct(g("profitMargins")),
        "gross_margin":  pct(g("grossMargins")),
        "rev_growth":    pct(g("revenueGrowth")),
        "w52_low":       g("fiftyTwoWeekLow"),
        "w52_high":      g("fiftyTwoWeekHigh"),
    }

    # fallback for price / market cap if the main .info call came back thin
    if live["price"] is None or live["mkt_cap"] is None:
        try:
            fast = tk.fast_info
            live["price"] = live["price"] or fast.get("lastPrice")
            live["mkt_cap"] = live["mkt_cap"] or fast.get("marketCap")
        except Exception:
            pass

    return live


def status_flag(table_val, live_val):
    """Compare a parsed table number with the live number, return a status word."""
    if table_val is None or live_val is None:
        return "?"  # nothing to compare
    # a sign flip is the most important signal (e.g. profitable vs not)
    if (table_val < 0) != (live_val < 0):
        return "SIGN FLIP"
    # avoid unstable ratios when the baseline is ~zero
    if abs(table_val) < 1e-9:
        return "ok" if abs(live_val) < 1e-9 else "differs"
    pct_diff = abs(live_val - table_val) / abs(table_val) * 100
    return "differs" if pct_diff > PCT_DIFF_THRESHOLD else "ok"


def fmt_big(x):
    """Format large numbers as e.g. 74.98B."""
    for suffix, size in (("T", 1e12), ("B", 1e9), ("M", 1e6)):
        if abs(x) >= size:
            return f"{x / size:.2f}{suffix}"
    return f"{x:,.0f}"


def fmt(field, value):
    """Human-readable formatting of a live value for printing."""
    if value is None:
        return "n/a"
    if field in ("mkt_cap", "net_income"):
        return fmt_big(value)
    if field in ("profit_margin", "gross_margin", "rev_growth"):
        return f"{value:.1f}%"
    if field == "pe":
        return f"{value:.1f}x"
    return f"{value:,.2f}"


# (table key, printed label) for each field we verify
FIELDS = [
    ("price",         "price"),
    ("mkt_cap",       "market cap"),
    ("pe",            "PE (trailing)"),
    ("eps",           "EPS"),
    ("net_income",    "net income"),
    ("profit_margin", "profit margin"),
    ("gross_margin",  "gross margin"),
    ("rev_growth",    "rev growth"),
    ("w52_low",       "52w low"),
    ("w52_high",      "52w high"),
]

MARKERS = {"ok": "  ", "differs": "~ ", "SIGN FLIP": "! ", "?": "? "}


def main():
    stocks = load_watchlist()
    flagged = {}  # ticker -> list of problem fields

    for stock in stocks:
        ticker = stock["ticker"]
        print("=" * 64)
        print(f"{ticker:6} {stock.get('company', '')}")
        print("-" * 64)

        live = fetch_live(ticker)

        for key, label in FIELDS:
            table_raw = stock.get(key, "—")
            table_num = parse_number(table_raw)
            live_num = live.get(key)
            flag = status_flag(table_num, live_num)

            print(
                f"{MARKERS[flag]}{label:14} "
                f"table={str(table_raw):>12}   "
                f"live={fmt(key, live_num):>12}   {flag}"
            )

            if flag in ("SIGN FLIP", "differs"):
                flagged.setdefault(ticker, []).append(f"{label} ({flag})")

        time.sleep(PAUSE_BETWEEN_TICKERS)

    # ------------------------------ summary --------------------------------
    print("\n" + "=" * 64)
    print("SUMMARY — where your table disagrees with live data")
    print("=" * 64)
    if not flagged:
        print("No significant discrepancies found.")
    else:
        for ticker, problems in flagged.items():
            print(f"\n{ticker}:")
            for problem in problems:
                print(f"   - {problem}")
        print(
            "\nReading the flags:"
            "\n  '~ differs'   on price / market cap is usually just market"
            "\n                movement since your table date — not an error."
            "\n  '! SIGN FLIP' (PE, EPS, net income) is the one to take"
            "\n                seriously: it usually means profitable vs not."
        )


if __name__ == "__main__":
    main()
