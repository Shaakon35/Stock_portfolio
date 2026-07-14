"""DCF intrinsic value for the AI-allocation single stocks (AlphaSpread-style).

Reproduces the core of AlphaSpread's intrinsic-value chart: market price vs a
discounted-cash-flow (DCF) estimate of value per share, plotted over the last
~5 years so you can see when a stock traded above/below its fundamental worth.

METHOD (absolute DCF only)
--------------------------
    IntrinsicValue/share =
        ( Σ_{n=1..N} FCF·(1+g)^n / (1+WACC)^n            # projected FCF, discounted
          + TV / (1+WACC)^N                              # discounted terminal value
          - NetDebt ) / SharesOutstanding

    TV (terminal value) = FCF·(1+g)^N · (1+g_term) / (WACC - g_term)
    NetDebt             = TotalDebt - TotalCash
    WACC                = CAPM: risk_free + beta·equity_premium  (clamped 7-15%)
    g (growth)          = historical FCF CAGR, clamped to [0, growth_cap]
    g_term              = long-run terminal growth (default 2.5%)

DATA (all from yfinance, no scraping)
-------------------------------------
    ticker.cashflow           -> 'Free Cash Flow' row, up to 5 fiscal years
    ticker.info               -> beta, sharesOutstanding, totalDebt, totalCash
    ticker.history(...)       -> price line (exact) for the chart

ELIGIBILITY
-----------
DCF is only meaningful for companies with POSITIVE, existing free cash flow.
Pre-profit / cash-burning names (many quantum/space/biotech picks) and tickers
with no FCF data are reported as N/A and skipped -- no misleading number, no
plot. Use is_dcf_eligible() to check.

HISTORICAL LINE (approximate)
-----------------------------
yfinance gives only ~5 annual statements and NO point-in-time beta/debt, so the
historical intrinsic line reconstructs each past year's value using that year's
reported FCF but current-value approximations for beta/debt/shares. The PRICE
line is exact; the intrinsic line shows the right over/under-valued shape but
will not match AlphaSpread number-for-number.
"""

import numpy as np


# --- Single-stock universe: the AI-allocation satellite baskets only ---
# (ETFs and ETF look-through underlyings are intentionally excluded.)
def get_single_stocks():
    """Return the ordered list of single-stock tickers from the allocations.

    Baskets are flattened; tickers with a 0.0 target (paused / private stage)
    are dropped so the notebook only shows live positions.
    """
    from portfolio.allocations import (
        NUCLEAR_BASKET_TARGETS, QUANTUM_BASKET_TARGETS, CYBER_BASKET_TARGETS,
        INDUSTRIAL_BASKET_TARGETS, SPECGROWTH_BASKET_TARGETS,
    )
    baskets = [
        ("Nuclear", NUCLEAR_BASKET_TARGETS),
        ("Quantum", QUANTUM_BASKET_TARGETS),
        ("Cyber", CYBER_BASKET_TARGETS),
        ("Industrial", INDUSTRIAL_BASKET_TARGETS),
        ("SpecGrowth", SPECGROWTH_BASKET_TARGETS),
    ]
    out = []  # list of (ticker, basket_name)
    seen = set()
    for name, targets in baskets:
        for tk, w in targets.items():
            if w and w > 0 and tk not in seen:
                out.append((tk, name))
                seen.add(tk)
    return out


# --- DCF assumptions (override via compute_intrinsic_value kwargs) ---
DEFAULTS = {
    "risk_free": 0.043,        # ~10y treasury
    "equity_premium": 0.05,    # historical equity risk premium
    "wacc_min": 0.07,
    "wacc_max": 0.15,
    "terminal_growth": 0.025,  # long-run GDP-ish
    "growth_cap": 0.25,        # cap projected FCF growth at 25%/yr
    "projection_years": 10,
}


def _wacc_from_beta(beta, cfg):
    """CAPM cost of equity, clamped. Used as the discount rate.

    We use cost of equity (not full WACC with debt) as a simple, robust
    discount rate; it is conservative for low-debt tech names and avoids
    needing a reliable cost-of-debt estimate.
    """
    if beta is None or beta <= 0:
        beta = 1.0
    r = cfg["risk_free"] + beta * cfg["equity_premium"]
    return float(min(max(r, cfg["wacc_min"]), cfg["wacc_max"]))


def _fcf_series(ticker_obj):
    """Return (years, fcf_values) newest-first from the annual cash flow stmt.

    Returns ([], []) if no Free Cash Flow row exists.
    """
    try:
        cf = ticker_obj.cashflow
    except Exception:
        return [], []
    if cf is None or "Free Cash Flow" not in cf.index:
        return [], []
    row = cf.loc["Free Cash Flow"]
    years, vals = [], []
    for col, v in row.items():
        if v is None or (isinstance(v, float) and np.isnan(v)):
            continue
        years.append(int(str(col)[:4]))
        vals.append(float(v))
    return years, vals


def _cagr(values_old_to_new):
    """Compound annual growth rate from an oldest->newest ordered list."""
    vals = [v for v in values_old_to_new]
    if len(vals) < 2:
        return None
    first, last = vals[0], vals[-1]
    if first is None or last is None or first <= 0 or last <= 0:
        return None
    n = len(vals) - 1
    return (last / first) ** (1.0 / n) - 1.0


def is_dcf_eligible(info=None, ticker_obj=None, ticker=None):
    """True if DCF can produce a meaningful value (positive, existing FCF).

    Returns (eligible: bool, reason: str). Pass either a yfinance Ticker or a
    ticker string. A stock is eligible only if the MOST RECENT free cash flow
    is positive and shares outstanding are known.
    """
    import yfinance as yf
    if ticker_obj is None:
        ticker_obj = yf.Ticker(ticker)
    if info is None:
        try:
            info = ticker_obj.info or {}
        except Exception:
            info = {}

    years, vals = _fcf_series(ticker_obj)
    if not vals:
        return False, "no free cash flow data"
    # cashflow columns are newest-first -> vals[0] is latest
    if vals[0] <= 0:
        return False, f"latest FCF negative (${vals[0]/1e6:,.0f}M)"
    shares = info.get("sharesOutstanding")
    if not shares or shares <= 0:
        return False, "shares outstanding unknown"
    return True, "ok"


def compute_intrinsic_value(ticker, info=None, ticker_obj=None, **overrides):
    """Compute the current DCF intrinsic value per share for one ticker.

    Returns a dict:
        {eligible, reason, ticker, price, intrinsic, upside_pct,
         wacc, growth, fcf_latest, net_debt, shares, assumptions}
    If not eligible, intrinsic is None and reason explains why.
    """
    import yfinance as yf
    cfg = {**DEFAULTS, **overrides}
    if ticker_obj is None:
        ticker_obj = yf.Ticker(ticker)
    if info is None:
        try:
            info = ticker_obj.info or {}
        except Exception:
            info = {}

    price = info.get("currentPrice") or info.get("regularMarketPrice")

    eligible, reason = is_dcf_eligible(info, ticker_obj, ticker)
    base = {
        "ticker": ticker, "price": price, "eligible": eligible,
        "reason": reason, "intrinsic": None, "upside_pct": None,
    }
    if not eligible:
        return base

    years, vals = _fcf_series(ticker_obj)          # newest-first
    fcf_latest = vals[0]
    old_to_new = list(reversed(vals))              # oldest-first for CAGR
    growth = _cagr(old_to_new)
    if growth is None:
        # fall back to revenue growth, then a modest default
        rg = info.get("revenueGrowth")
        growth = float(rg) if rg is not None else 0.08
    growth = float(min(max(growth, 0.0), cfg["growth_cap"]))

    beta = info.get("beta")
    wacc = _wacc_from_beta(beta, cfg)
    g_term = cfg["terminal_growth"]
    # Guard: terminal growth must be below discount rate.
    if g_term >= wacc:
        g_term = wacc - 0.02

    shares = info.get("sharesOutstanding")
    net_debt = (info.get("totalDebt") or 0) - (info.get("totalCash") or 0)

    intrinsic = _dcf_per_share(
        fcf_latest, growth, wacc, g_term, cfg["projection_years"],
        net_debt, shares)

    upside = ((intrinsic - price) / price * 100.0) if price else None
    base.update({
        "intrinsic": intrinsic, "upside_pct": upside, "wacc": wacc,
        "growth": growth, "fcf_latest": fcf_latest, "net_debt": net_debt,
        "shares": shares,
        "assumptions": {
            "terminal_growth": g_term, "beta": beta,
            "projection_years": cfg["projection_years"],
        },
    })
    return base


def _dcf_per_share(fcf, growth, wacc, g_term, n_years, net_debt, shares):
    """Core DCF math -> intrinsic value per share."""
    pv_fcf = 0.0
    fcf_n = fcf
    for n in range(1, n_years + 1):
        fcf_n = fcf * (1 + growth) ** n
        pv_fcf += fcf_n / (1 + wacc) ** n
    terminal = fcf_n * (1 + g_term) / (wacc - g_term)
    pv_terminal = terminal / (1 + wacc) ** n_years
    equity_value = pv_fcf + pv_terminal - net_debt
    return float(equity_value / shares) if shares else None


def historical_intrinsic_series(ticker, info=None, ticker_obj=None, **overrides):
    """Approximate intrinsic value per share for each reported fiscal year.

    For each year with reported FCF, recompute DCF using that year's FCF but
    current beta/net-debt/shares (yfinance has no point-in-time values for
    those). Returns a list of (year:int, intrinsic:float) oldest-first.

    Only years where the DCF is positive and finite are returned.
    """
    import yfinance as yf
    cfg = {**DEFAULTS, **overrides}
    if ticker_obj is None:
        ticker_obj = yf.Ticker(ticker)
    if info is None:
        try:
            info = ticker_obj.info or {}
        except Exception:
            info = {}

    years, vals = _fcf_series(ticker_obj)   # newest-first
    if not vals:
        return []
    pairs = list(zip(years, vals))
    pairs.sort(key=lambda p: p[0])          # oldest-first

    beta = info.get("beta")
    wacc = _wacc_from_beta(beta, cfg)
    g_term = cfg["terminal_growth"]
    if g_term >= wacc:
        g_term = wacc - 0.02
    shares = info.get("sharesOutstanding")
    net_debt = (info.get("totalDebt") or 0) - (info.get("totalCash") or 0)

    # Rolling growth estimate: CAGR of FCF up to and including each year.
    out = []
    for i, (yr, fcf) in enumerate(pairs):
        if fcf is None or fcf <= 0 or not shares:
            continue
        window = [v for (_, v) in pairs[:i + 1]]
        g = _cagr(window)
        if g is None:
            g = 0.08
        g = float(min(max(g, 0.0), cfg["growth_cap"]))
        iv = _dcf_per_share(fcf, g, wacc, g_term, cfg["projection_years"],
                            net_debt, shares)
        if iv is not None and np.isfinite(iv) and iv > 0:
            out.append((yr, iv))
    return out


def fetch_price_history(ticker, years=6, ticker_obj=None):
    """Monthly close price history for the chart. Returns (dates, closes)."""
    import yfinance as yf
    if ticker_obj is None:
        ticker_obj = yf.Ticker(ticker)
    try:
        hist = ticker_obj.history(period=f"{years}y", interval="1mo")
    except Exception:
        return [], []
    if hist is None or hist.empty:
        return [], []
    close = hist["Close"].dropna()
    return list(close.index), [float(v) for v in close.values]


def analyze_ticker(ticker, basket="", **overrides):
    """One-stop: fetch + compute everything needed for a stock's tab.

    Returns a dict with the valuation, historical intrinsic series, and price
    history. Safe to call for ineligible tickers (they get eligible=False and
    still return price history so the tab can show the price line).
    """
    import yfinance as yf
    t = yf.Ticker(ticker)
    try:
        info = t.info or {}
    except Exception:
        info = {}

    val = compute_intrinsic_value(ticker, info=info, ticker_obj=t, **overrides)
    val["basket"] = basket
    val["name"] = info.get("shortName") or info.get("longName") or ticker

    dates, closes = fetch_price_history(ticker, ticker_obj=t)
    val["price_dates"] = dates
    val["price_closes"] = closes

    if val["eligible"]:
        val["hist_intrinsic"] = historical_intrinsic_series(
            ticker, info=info, ticker_obj=t, **overrides)
    else:
        val["hist_intrinsic"] = []
    return val


# =========================================================================
# PLOTTING  (AlphaSpread-style: price line vs intrinsic-value line)
# =========================================================================

def plot_to_base64(val):
    """Render a price-vs-intrinsic chart for one stock, return base64 PNG.

    Blue line = market price (exact). Green step line = approximate historical
    intrinsic value. A dashed marker shows today's intrinsic value. Returns an
    empty string if there's no price history to plot.
    """
    import base64
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    dates = val.get("price_dates") or []
    closes = val.get("price_closes") or []
    if not dates or not closes:
        return ""

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(dates, closes, color="#1f77b4", lw=2, label="Market price")

    hist = val.get("hist_intrinsic") or []
    if hist:
        import datetime as _dt
        hy = [_dt.datetime(y, 12, 31) for (y, _) in hist]
        hv = [v for (_, v) in hist]
        ax.step(hy, hv, where="post", color="#2ca02c", lw=2,
                label="Intrinsic value (DCF, approx)")
        ax.scatter(hy, hv, color="#2ca02c", s=25, zorder=5)

    intrinsic = val.get("intrinsic")
    if intrinsic is not None and np.isfinite(intrinsic):
        ax.axhline(intrinsic, color="#2ca02c", ls="--", lw=1.2, alpha=0.7)
        ax.annotate(f"IV ${intrinsic:,.2f}",
                    xy=(dates[-1], intrinsic), xytext=(6, 0),
                    textcoords="offset points", va="center",
                    color="#2ca02c", fontsize=9, fontweight="bold")

    price = val.get("price")
    up = val.get("upside_pct")
    title = f"{val.get('ticker','')}  —  {val.get('name','')}"
    if val["eligible"] and price and intrinsic is not None:
        tag = "undervalued" if up and up > 0 else "overvalued"
        title += f"\nPrice ${price:,.2f}  |  IV ${intrinsic:,.2f}  |  {up:+.0f}% ({tag})"
    else:
        title += f"\nDCF N/A — {val.get('reason','')}"

    ax.set_title(title, fontsize=11, loc="left")
    ax.set_ylabel("Per share ($)")
    ax.grid(True, alpha=0.25)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=90)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")
