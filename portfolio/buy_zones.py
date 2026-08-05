# =========================================================================
# BUY-ZONE ENGINE — accumulation bands for held single stocks
# =========================================================================
# Standalone tool (NOT wired into the signals pipeline). It answers one
# question per held single stock: "what price range is a good place to buy?"
#
# TWO SOURCES OF TRUTH, in priority order:
#
#   1. MANUAL_ZONES  — hand-set bands you have identified from the chart.
#      These ALWAYS win. This is the dict to edit when you say "change the
#      zone for X" — nothing is auto-computed for a name that lives here.
#
#   2. auto-derived  — for every other held single, a low-support band is
#      derived from multi-year price history by finding swing lows that were
#      RETESTED (i.e. real, confirmed support), then clustering the lowest
#      ones into a band. If a name never retested a low (it bottomed once and
#      ran), there is NO confirmed support, so NO zone is set — deliberately.
#
# ETFs are excluded (you DCA them regardless of price).
#
# CAVEAT (see AGENTS.md): the yfinance feed in this environment is
# date-corrupted for some names. The auto bands are reproducible from
# whatever history the feed returns; treat the exact numbers as a guide and
# override with a MANUAL_ZONE whenever your own chart read is better.
#
# Run:
#     PORTFOLIO_USE=ai python3 -m portfolio.buy_zones
# or from a notebook:
#     from portfolio.buy_zones import build_zone_table, print_zone_report
#     print_zone_report()
# =========================================================================

import os

import numpy as np

try:
    import yfinance as yf
except Exception:  # pragma: no cover - yfinance always present in this env
    yf = None


# =========================================================================
# 1. MANUAL ZONES — hand-set, always win. EDIT THESE WHEN ASKED.
# =========================================================================
# Format: "TICKER": (low, high, "note")
# low/high are absolute prices (the currency the ticker trades in).
# The note is free text explaining the support read.
MANUAL_ZONES = {
    "ORCL": (120.0, 140.0,
             "Multi-year support shelf: floor ~120 (deep wick), "
             "130/140 the repeated bounce levels before the AI re-rate."),
    "NOW":  (70.0, 110.0,
             "Long accumulation shelf 70-110; 70 is the deep-value floor, "
             "110 the top of the buy band."),
    "FICO": (950.0, 1100.0,
             "Post-de-rate support: ~950 the low floor, ~1100 the top of "
             "the accumulation band after the pullback from the peak."),
}


# =========================================================================
# 2. AUTO-DERIVATION TUNABLES
# =========================================================================
# A buy zone is the RECENT accumulation shelf just below the current price —
# the level the stock pulls back to and retests in its CURRENT regime — not
# the pre-bull-run base from years ago (support at $23 is useless on a name
# that trades at $190). So support is derived from a recent window and only
# accepted if it sits within a sensible distance below the live price.
_HISTORY_PERIOD = "2y"     # fetch this much history...
_LOOKBACK_DAYS  = 378      # ...but derive support from ~18m of it (recent regime)
_MIN_DAYS       = 189      # need >= ~9m of closes or we won't guess a zone
_SWING_WIN      = 12       # a local min must be the lowest within +/- this many days
_CLUSTER_TOL    = 0.06     # swing lows within 6% of each other form one shelf
_MIN_TOUCHES    = 2        # a shelf must have been RETESTED >= twice to be "confirmed"
_MIN_BAND       = 0.05     # widen a too-tight cluster to at least a 5%-wide band
_MAX_BELOW      = 0.45     # ignore shelves more than 45% below price (not actionable)
_MIN_BELOW      = 0.0      # the shelf top must be at/below the current price

# ETFs / funds you DCA regardless of price — never get a buy zone.
_ETF_TICKERS = {"SMHV.SW", "XAIX.DE", "QDVE.DE"}


# =========================================================================
# 3. HELD-UNIVERSE RESOLUTION (AI book)
# =========================================================================
def held_single_stocks():
    """Return the sorted list of held single stocks (ETFs excluded).

    Reads the AI allocation book (the scorer's canonical universe): every
    ticker that appears in a wave basket or carries a STRATEGY tag, minus the
    ETF sleeves.
    """
    from portfolio.AI_allocations import ALL_BASKETS, STRATEGY

    held = set()
    for _name, basket in ALL_BASKETS:
        held |= set(basket.keys())
    held |= set(STRATEGY.keys())
    held -= _ETF_TICKERS
    return sorted(held)


# =========================================================================
# 4. PRICE + SUPPORT DERIVATION
# =========================================================================
def _fetch_closes(ticker, period=_HISTORY_PERIOD):
    """Daily close series for a ticker, or an empty array on any failure."""
    if yf is None:
        return np.array([])
    for _attempt in range(2):
        try:
            hist = yf.Ticker(ticker).history(period=period, auto_adjust=True)
            closes = hist["Close"].dropna().to_numpy(dtype=float)
            if closes.size >= 2:
                return closes
        except Exception:
            pass
    return np.array([])


def _swing_lows(closes, win=None):
    if win is None:
        win = _SWING_WIN
    """Distinct swing-low prices (confirmed local minima).

    A point is a swing low if it is the minimum within +/- `win` days. Nearby
    troughs (< `win` apart) belong to the SAME dip and are merged (keeping the
    lower), so one V-bottom counts once, not many times.
    """
    n = closes.size
    idxs = []
    for i in range(win, n - win):
        window = closes[i - win:i + win + 1]
        if closes[i] == window.min():
            if idxs and (i - idxs[-1]) < win:
                # same dip — keep the lower of the two
                if closes[i] < closes[idxs[-1]]:
                    idxs[-1] = i
            else:
                idxs.append(i)
    return [float(closes[i]) for i in idxs]


def _cluster_at(troughs, anchor):
    """All troughs within _CLUSTER_TOL above `anchor` (one support shelf)."""
    return [t for t in troughs if anchor <= t <= anchor * (1.0 + _CLUSTER_TOL)]


def derive_support_zone(closes, lookback=None, swing_win=None, min_bars=None):
    """Derive the nearest actionable buy zone from a close series.

    Uses the recent regime (last `lookback` bars) and finds the HIGHEST swing-low
    shelf that (a) was retested >= _MIN_TOUCHES times and (b) sits at/just below
    the current price (within _MAX_BELOW). That nearest shelf is the band you
    actually get a chance to buy — not the pre-run all-time base.

    The defaults are tuned for DAILY closes. Pass `lookback`/`swing_win`/`min_bars`
    to run on a coarser series (e.g. WEEKLY closes from plot_history.json), so the
    dashboard bands are derived from exactly the data the chart draws.

    Returns (low, high, touches) or None. None means "no confirmed, actionable
    support": the name bottomed once and ran, only has stale deep-below support,
    or there isn't enough history — so no buy zone is set (by design).
    """
    lookback = _LOOKBACK_DAYS if lookback is None else lookback
    swing_win = _SWING_WIN if swing_win is None else swing_win
    min_bars = _MIN_DAYS if min_bars is None else min_bars

    if closes.size < min_bars:
        return None

    price = float(closes[-1])
    recent = closes[-lookback:] if closes.size > lookback else closes

    troughs = sorted(_swing_lows(recent, win=swing_win))
    if len(troughs) < _MIN_TOUCHES:
        return None

    floor_price = price * (1.0 - _MAX_BELOW)  # ignore shelves deeper than this

    # Walk candidate shelf anchors from HIGH to LOW; take the first (nearest to
    # price) that is confirmed (>= _MIN_TOUCHES) and within the actionable band.
    for anchor in sorted(troughs, reverse=True):
        if anchor > price * (1.0 + _CLUSTER_TOL):
            continue  # shelf is above the current price — not a buy zone
        if anchor < floor_price:
            break     # everything below here is too deep to be actionable
        cluster = _cluster_at(troughs, anchor)
        if len(cluster) < _MIN_TOUCHES:
            continue
        low = min(cluster)
        high = max(cluster)
        if high < low * (1.0 + _MIN_BAND):
            high = low * (1.0 + _MIN_BAND)
        # don't let the band top run above the current price
        high = min(high, price)
        if high <= low:
            continue
        return (round(low, 2), round(high, 2), len(cluster))

    return None


# =========================================================================
# 5. STATUS vs ZONE
# =========================================================================
def _zone_status(price, low, high):
    """Classify a live price against a buy zone."""
    if price is None or not np.isfinite(price):
        return "NO PRICE", "—"
    if price < low:
        pct = (low - price) / low * 100
        return "BELOW ZONE", f"{pct:.0f}% under floor ${low:,.0f} — deep value / thesis check"
    if price <= high:
        return "IN ZONE", f"BUY — inside ${low:,.0f}-${high:,.0f}"
    pct = (price - high) / high * 100
    return "ABOVE ZONE", f"{pct:.0f}% above ${high:,.0f} — wait for pullback"


# =========================================================================
# 6. BUILD + REPORT
# =========================================================================
def build_zone_table(tickers=None):
    """Compute the buy-zone row for each held single stock.

    Each row: ticker, source (manual|auto|none), low, high, price, status,
    detail, touches, note.
    """
    if tickers is None:
        tickers = held_single_stocks()

    rows = []
    for ticker in tickers:
        closes = _fetch_closes(ticker)
        price = float(closes[-1]) if closes.size else None

        if ticker in MANUAL_ZONES:
            low, high, note = MANUAL_ZONES[ticker]
            source, touches = "manual", None
        else:
            zone = derive_support_zone(closes)
            if zone is None:
                low = high = None
                source, touches, note = "none", None, "no confirmed support"
            else:
                low, high, touches = zone
                source = "auto"
                note = f"retested support x{touches}"

        if low is None:
            status, detail = "NO ZONE", "no confirmed support — not set"
        else:
            status, detail = _zone_status(price, low, high)

        rows.append({
            "ticker": ticker,
            "source": source,
            "low": low,
            "high": high,
            "price": price,
            "status": status,
            "detail": detail,
            "touches": touches,
            "note": note,
        })
    return rows


def print_zone_report(tickers=None):
    """Print a plain-text buy-zone report for held single stocks."""
    rows = build_zone_table(tickers)

    order = {"IN ZONE": 0, "BELOW ZONE": 1, "ABOVE ZONE": 2,
             "NO ZONE": 3, "NO PRICE": 4}
    rows.sort(key=lambda r: (order.get(r["status"], 9), r["ticker"]))

    hdr = f"{'TICKER':<9}{'SRC':<7}{'PRICE':>10}{'BUY ZONE':>20}  {'STATUS':<11} DETAIL"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        price = f"{r['price']:,.2f}" if r["price"] is not None else "n/a"
        if r["low"] is not None:
            zone = f"{r['low']:,.0f} - {r['high']:,.0f}"
        else:
            zone = "—"
        print(f"{r['ticker']:<9}{r['source']:<7}{price:>10}{zone:>20}  "
              f"{r['status']:<11} {r['detail']}")

    n_manual = sum(1 for r in rows if r["source"] == "manual")
    n_auto = sum(1 for r in rows if r["source"] == "auto")
    n_none = sum(1 for r in rows if r["source"] == "none")
    print("-" * len(hdr))
    print(f"{len(rows)} held singles — {n_manual} manual, {n_auto} auto, "
          f"{n_none} no-confirmed-support.")
    return rows


if __name__ == "__main__":
    os.environ.setdefault("PORTFOLIO_USE", "ai")
    print_zone_report()
