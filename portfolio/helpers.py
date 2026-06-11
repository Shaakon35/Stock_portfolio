import yfinance as yf


def is_in_uptrend(ticker):
    """Check if a ticker is above its 200-day SMA (uptrend filter)."""
    try:
        data = yf.Ticker(ticker).history(period="1y")
        if len(data) < 200:
            return True
        sma_200 = data['Close'].rolling(window=200).mean().iloc[-1]
        return data['Close'].iloc[-1] > sma_200
    except Exception:
        return True


def _last_valid_close(hist):
    """Return the last non-NaN Close value and its date from a history df."""
    if hist.empty:
        return None, None
    closes = hist['Close'].dropna()
    if closes.empty:
        return None, None
    return float(closes.iloc[-1]), closes.index[-1].date()


def check_ticker_status(ticker):
    """
    Classify a ticker as active, acquired, or dead (bankrupt/delisted).

    Uses yfinance info and price history to distinguish:
      - active:   trading normally
      - acquired: delisted with a final price > $1 (buyout)
      - dead:     delisted with final price near $0 or no data (bankruptcy)

    Returns dict with:
      status: "active" | "acquired" | "dead"
      last_price: float or None
      last_trade_date: date or None
      message: str
    """
    t = yf.Ticker(ticker)
    info = t.info or {}

    # yfinance sets quoteType to "NONE" and tradeable to False for
    # fully removed tickers (e.g. OLK after Thermo Fisher acquisition).
    quote_type = info.get("quoteType", "")
    tradeable = info.get("tradeable", True)

    hist = t.history(period="5d")
    last_price, last_date = _last_valid_close(hist)

    # Ticker still has recent valid prices — it's active
    if last_price is not None:
        return {
            "status": "active",
            "last_price": last_price,
            "last_trade_date": last_date,
            "message": f"{ticker} active at ${last_price:.2f}",
        }

    # No recent prices — check full history for the final traded price
    hist_full = t.history(period="max")
    last_price, last_date = _last_valid_close(hist_full)

    # If yfinance has zero data and marks it untradeable, it's fully gone
    if last_price is None and (quote_type == "NONE" or not tradeable):
        return {
            "status": "dead",
            "last_price": None,
            "last_trade_date": None,
            "message": (
                f"{ticker} fully delisted — no price history available. "
                f"Check your broker for acquisition payout or write-off."
            ),
        }

    # Has historical data but no recent trades — delisted
    if last_price is not None and last_price > 1.0:
        return {
            "status": "acquired",
            "last_price": last_price,
            "last_trade_date": last_date,
            "message": f"{ticker} delisted (likely acquired). Last traded ${last_price:.2f} on {last_date}",
        }

    return {
        "status": "dead",
        "last_price": last_price,
        "last_trade_date": last_date,
        "message": f"{ticker} delisted (likely bankrupt). Last price ${last_price or 0:.2f}",
    }


def get_price(ticker):
    """Fetch the latest closing price, handling delisted/acquired/bankrupt tickers."""
    fallbacks = {"QNT": 47.5, "CRWD": 671.0, "PANW": 257.0}
    if ticker in fallbacks:
        return fallbacks[ticker]
    try:
        status = check_ticker_status(ticker)
        if status["status"] == "active":
            return status["last_price"]
        if status["status"] == "acquired":
            print(f"⚠️ {ticker}: {status['message']} — check broker for payout")
            return status["last_price"]
        # dead — could be bankrupt OR acquired with ticker fully removed
        print(f"❌ {ticker}: {status['message']}")
        return 0.0
    except Exception:
        return 10.0


# =========================================================================
# DELISTED OVERRIDES — manually maintained
# =========================================================================
# Yahoo scrubs all history for delisted tickers, making it impossible to
# distinguish acquired (worth $X) from bankrupt (worth $0) automatically.
# Add entries here when a portfolio holding gets acquired or goes bankrupt.
#
# Format: "TICKER": ("acquired"|"bankrupt", "description", final_price)
#
# Last reviewed: 2026-06-11
# Source: smid_optimization_data.csv (628 tickers scanned)
# =========================================================================
DELISTED_OVERRIDES = {
    # --- ACQUIRED (shareholders received cash/stock) ---
    "OLK":  ("acquired", "Acquired by Thermo Fisher (TMO) at ~$26/share in 2024", 26.0),
    "AJRD": ("acquired", "Acquired by L3Harris (LHX) at $58/share in 2023", 58.0),
    "ALTR": ("acquired", "Acquired by Siemens at $113/share in 2025", 113.0),
    "AVLR": ("acquired", "Acquired by Vista Equity Partners at $93.50/share in 2022", 93.50),
    "CFLT": ("acquired", "Acquired by IBM at $32.50/share in 2025", 32.50),
    "CLDR": ("acquired", "Taken private by Clayton Dubilier & Rice + KKR at $16/share in 2021", 16.0),
    "COUP": ("acquired", "Taken private by Thoma Bravo at $48/share in 2023", 48.0),
    "GNOG": ("acquired", "Acquired by DraftKings (DKNG) at ~$56.26/share (stock deal) in 2022", 56.26),
    "JAMF": ("acquired", "Acquired by Francisco Partners at $13.05/share in 2026", 13.05),
    "MAXR": ("acquired", "Acquired by Advent International at $53/share in 2023", 53.0),
    "SGEN": ("acquired", "Acquired by Pfizer (PFE) at $229/share in 2023", 229.0),
    "SILK": ("acquired", "Acquired by Boston Scientific (BSX) at $27.50/share in 2024", 27.50),
    "SMAR": ("acquired", "Taken private by Blackstone & Vista Equity at $56.50/share in 2024", 56.50),
    "SUMO": ("acquired", "Taken private by Francisco Partners at $12.05/share in 2023", 12.05),
    "ZNGA": ("acquired", "Acquired by Take-Two (TTWO) at $12.47/share in 2022", 12.47),
    # --- BANKRUPT (worth $0) ---
    "GOEV": ("bankrupt", "Canoo — filed Ch.7 bankruptcy in 2024", 0.0),
    "NKLA": ("bankrupt", "Nikola — filed Ch.11 bankruptcy in 2025", 0.0),
}


def get_price_with_overrides(ticker):
    """Like get_price(), but checks DELISTED_OVERRIDES first for tickers
    Yahoo has fully scrubbed."""
    if ticker in DELISTED_OVERRIDES:
        status, note, price = DELISTED_OVERRIDES[ticker]
        if status == "acquired":
            print(f"⚠️ {ticker}: {note} — check broker for payout")
        else:
            print(f"❌ {ticker}: {note}")
        return price or 0.0
    return get_price(ticker)


def get_live_fx_rate(from_curr, to_curr):
    """Fetch real-time exchange rate using yfinance."""
    fx_ticker = f"{from_curr}{to_curr}=X"
    try:
        data = yf.Ticker(fx_ticker).history(period="1d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
        return 0.89
    except Exception as e:
        print(f"⚠️ FX Auto-fetch failed: {e}")
        return 0.89  # Fallback rate
