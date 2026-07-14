"""Intrinsic value for the AI-allocation portfolio (AlphaSpread-style).

Reproduces AlphaSpread's intrinsic-value chart: market price vs an estimate of
fundamental value per share, plotted over the last ~5 years so you can see when
a stock traded above/below its worth.

METHOD (anchored-multiple, AlphaSpread-style)
---------------------------------------------
Intrinsic value = forward EPS x a fair P/E anchored to the stock's OWN
forward multiple, capped so only the extreme optimists get re-rated:

    fair_pe   = min(own_forward_PE, pe_ceiling)      # own_forward_PE = price/fwdEPS
    intrinsic = forwardEPS * fair_pe

WHY ANCHOR TO THE STOCK'S OWN MULTIPLE
    The market already prices each company's growth, quality and risk into its
    own multiple. Forcing a single "fair" P/E onto everyone re-rates a cyclical
    semiconductor at 6x up to ~20x and hallucinates +100%+ upside. Anchoring to
    the stock's own forward P/E and only CAPPING the extremes (e.g. names at
    40-80x forward earnings, like CCJ ~48x or ALAB ~84x, back toward ~21x)
    tracks AlphaSpread's intrinsic value with two parameters instead of a fit
    that overfits. Validated against eight anchors (CCJ, MSFT, NVDA, BESI.AS,
    ALAB, TLN, TSM, MU): ~5pp mean upside error, direction-correct on all eight.

DCF (secondary, shown for context, NOT blended by default)
    A 2-stage discounted cash flow on NORMALIZED (multi-year average) free cash
    flow is computed and reported so you can see when the two methods disagree,
    but multiples_weight defaults to 1.0 so it does not move the headline value.
    For ADRs whose financialCurrency differs from the price currency (e.g. TSM:
    FCF in TWD, price in USD) the DCF leg is skipped to avoid mixing currencies.
        dcf  = ( Σ stage1 FCF·(1+g)^n/(1+WACC)^n
               + Σ stage2 (growth fading to g_term)
               + TV/(1+WACC)^N  -  NetDebt ) / Shares
        WACC = CAPM: risk_free + beta·equity_premium (clamped)
        g    = tempered analyst earnings growth (fallback: FCF CAGR), capped

This approximates AlphaSpread; it does not reproduce it exactly (their formula
and data feeds are not public).

DATA (all from yfinance, no scraping)
-------------------------------------
    ticker.info      -> forwardEps, trailingEps, beta, earningsGrowth,
                        sharesOutstanding, totalDebt, totalCash, price
    ticker.cashflow  -> 'Free Cash Flow' row, up to ~4 fiscal years (DCF leg)
    ticker.history() -> price line (exact) for the chart

ELIGIBILITY
-----------
A stock is valued when EITHER leg is available: positive forward/trailing EPS
(multiples) OR positive free cash flow (DCF). Names with no FCF row still get a
multiples estimate (e.g. BESI.AS). Only names with neither positive earnings
nor positive FCF are reported as N/A. Use is_dcf_eligible() to check.

HISTORICAL LINE (approximate)
-----------------------------
yfinance gives only ~5 annual statements and NO point-in-time beta/debt, so the
historical intrinsic line reconstructs each past year's value using that year's
reported FCF but current-value approximations for beta/debt/shares. The PRICE
line is exact; the intrinsic line shows the right over/under-valued shape but
will not match AlphaSpread number-for-number.
"""

import numpy as np


# Pseudo-tickers used inside ETF_LOOK_THROUGH to represent the untracked
# remainder of an ETF's holdings. They are not real stocks -> never valued.
_ETF_REMAINDER = {"OTHER_SEMI", "OTHER_TECH", "OTHER_AI"}


def get_single_stocks(include_etf_lookthrough=True):
    """Return the ordered [(ticker, wave)] list for the live AI portfolio.

    Source of truth is ``AI_allocations.py`` (waves W1-W7), where each basket
    holds direct book percentages. Tickers with a 0 weight (cut / paused) are
    dropped so only live positions appear.

    Any holding that is itself an ETF (has an entry in
    ``allocations.ETF_LOOK_THROUGH``) is expanded into its underlying stocks
    when ``include_etf_lookthrough`` is True -- so e.g. the SMHV.SW sleeve
    becomes NVDA, AVGO, ASML, MU, AMD, ... The ETF's untracked remainder
    (OTHER_SEMI etc.) is skipped. This is why the report shows the big-cap
    silicon names even though they are held via the ETF, not as singles.
    """
    from portfolio.AI_allocations import ALL_BASKETS
    try:
        from portfolio.allocations import ETF_LOOK_THROUGH
    except Exception:
        ETF_LOOK_THROUGH = {}

    out = []  # list of (ticker, wave_label)
    seen = set()
    for wave, targets in ALL_BASKETS:
        label = wave.split("_", 1)[-1].title() if "_" in wave else wave
        for tk, w in targets.items():
            if not w or w <= 0:
                continue
            if include_etf_lookthrough and tk in ETF_LOOK_THROUGH:
                # Expand the ETF into its underlying holdings.
                for u in ETF_LOOK_THROUGH[tk]:
                    if u in _ETF_REMAINDER or u in seen:
                        continue
                    out.append((u, f"{label} (via {tk})"))
                    seen.add(u)
                continue
            if tk in seen:
                continue
            out.append((tk, label))
            seen.add(tk)
    return out


# --- Valuation assumptions (override via compute_intrinsic_value kwargs) ---
#
# Calibrated to track AlphaSpread's "Base Case" intrinsic value. The estimate
# blends a forward-earnings multiple (dominant leg) with a 2-stage DCF on
# normalized free cash flow. Parameters below were fit by grid-search against
# five AlphaSpread anchor stocks (CCJ, MSFT, NVDA, BESI.AS, ALAB) spanning
# under/over-valued and low/high-beta cases; the fit is direction-correct on
# all five with ~20% RMSE on the intrinsic value.
#
# KEY IDEAS BEHIND THE CALIBRATION
#   * Forward EPS, not trailing, drives the multiples leg -- AlphaSpread prices
#     in next-year earnings. (Trailing P/E for these names ranged 22x-278x and
#     could not be reconciled with a single fair multiple.)
#   * The fair P/E is RISK-ADJUSTED: it shrinks as beta rises, so a high-beta
#     name (NVDA beta 2.2) is valued more cautiously than a low-beta one
#     (MSFT beta 1.13). This is what lets the model call MSFT undervalued and
#     NVDA overvalued at similar forward P/Es -- impossible with a flat P/E.
#         fair_pe = pe_base / (1 + pe_beta_k * (min(beta, beta_cap) - 1))
#   * FCF is NORMALIZED (multi-year average) before the DCF, so cyclical peak
#     cash flows (e.g. CCJ) don't inflate value.
DEFAULTS = {
    "risk_free": 0.043,        # ~10y treasury
    "equity_premium": 0.055,   # equity risk premium
    "wacc_min": 0.08,
    "wacc_max": 0.14,
    "terminal_growth": 0.025,  # long-run GDP-ish (stage-2 / terminal)
    # Stage 1: near-term growth, tempered and capped hard.
    "growth_cap": 0.12,        # cap projected growth at 12%/yr
    "stage1_years": 5,         # high-growth phase
    "stage2_years": 5,         # fade phase toward terminal growth
    "growth_haircut": 0.6,     # temper analyst/historical growth (mean-revert)
    "fcf_avg_years": 4,        # normalize FCF over up to N fiscal years
    # Multiples method: fair P/E ANCHORED to the stock's own forward P/E,
    # capped so only the extreme optimists get re-rated down. Two parameters,
    # fit against eight AlphaSpread anchors (5.4pp mean upside error, 8/8
    # direction-correct). See _fair_pe for the rationale.
    "pe_ceiling": 21.0,        # cap fair P/E (re-rate names priced above this)
    "pe_own_mult": 1.0,        # scale the stock's own forward P/E before cap
    "multiples_weight": 1.0,   # 1.0 => pure multiples (DCF shown but not blended)
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
    """True if a meaningful intrinsic value can be produced.

    Returns (eligible: bool, reason: str). A stock is valued when EITHER leg
    is available: positive free cash flow (for the DCF leg) OR positive
    forward/trailing EPS (for the multiples leg). This lets names with no
    yfinance FCF row (e.g. BESI.AS) still get a multiples-based estimate,
    while pre-profit / cash-burning names with neither remain N/A.
    """
    import yfinance as yf
    if ticker_obj is None:
        ticker_obj = yf.Ticker(ticker)
    if info is None:
        try:
            info = ticker_obj.info or {}
        except Exception:
            info = {}

    shares = info.get("sharesOutstanding")
    if not shares or shares <= 0:
        return False, "shares outstanding unknown"

    _, vals = _fcf_series(ticker_obj)
    has_fcf = bool(vals) and vals[0] > 0     # cashflow is newest-first
    eps_f = info.get("forwardEps")
    eps_t = info.get("trailingEps")
    has_eps = (eps_f is not None and eps_f > 0) or (eps_t is not None and eps_t > 0)

    if has_fcf or has_eps:
        return True, "ok"
    if vals and vals[0] <= 0 and not has_eps:
        return False, f"no positive FCF (${vals[0]/1e6:,.0f}M) or EPS"
    return False, "no free cash flow or earnings data"


def _estimate_growth(ticker_obj, info, cfg):
    """Conservative near-term growth estimate for stage 1 of the DCF.

    Prefers analyst forward earnings growth (what AlphaSpread's Base Case keys
    off), falls back to historical FCF CAGR, then revenue growth. The chosen
    figure is tempered by ``growth_haircut`` (analyst estimates for hot names
    are wildly optimistic) and hard-capped at ``growth_cap``.
    Returns a fraction (e.g. 0.10 for 10%/yr).
    """
    analyst = info.get("earningsGrowth")
    if analyst is not None and analyst > 0:
        growth = float(analyst)
    else:
        years, vals = _fcf_series(ticker_obj)
        hist = _cagr(list(reversed(vals))) if vals else None
        if hist is not None and hist > 0:
            growth = hist
        else:
            rg = info.get("revenueGrowth")
            growth = float(rg) if rg and rg > 0 else 0.05

    growth *= cfg["growth_haircut"]           # mean-revert optimistic estimates
    return float(min(max(growth, 0.0), cfg["growth_cap"]))


def _dcf_value(fcf, growth, wacc, cfg, net_debt, shares):
    """Two-stage DCF -> equity value per share.

    Stage 1: FCF grows at `growth` for stage1_years.
    Stage 2: growth fades linearly from `growth` to terminal growth over
             stage2_years (captures the reality that high growth decays).
    Terminal: Gordon growth on the final-year FCF.
    """
    g_term = cfg["terminal_growth"]
    if g_term >= wacc:
        g_term = wacc - 0.02

    pv = 0.0
    fcf_n = fcf
    yr = 0
    # Stage 1: constant high growth.
    for _ in range(cfg["stage1_years"]):
        yr += 1
        fcf_n *= (1 + growth)
        pv += fcf_n / (1 + wacc) ** yr
    # Stage 2: growth fades to terminal.
    s2 = cfg["stage2_years"]
    for j in range(1, s2 + 1):
        yr += 1
        g = growth + (g_term - growth) * (j / s2)
        fcf_n *= (1 + g)
        pv += fcf_n / (1 + wacc) ** yr
    # Terminal value on final-year FCF.
    terminal = fcf_n * (1 + g_term) / (wacc - g_term)
    pv += terminal / (1 + wacc) ** yr

    equity = pv - net_debt
    return float(equity / shares) if shares else None


def _fair_pe(info, cfg):
    """Fair P/E anchored to the stock's OWN forward P/E, capped at a ceiling.

        fair_pe = min(own_forward_PE * pe_own_mult, pe_ceiling)

    Rationale (learned from an overfit earlier version): the market already
    prices each company's growth, quality and risk into its own multiple, so a
    semiconductor at 6x and a software name at 20x should NOT be forced to a
    single "fair" multiple. AlphaSpread's intrinsic value tracks each stock's
    own forward P/E closely and mainly COMPRESSES the extreme optimists (e.g.
    CCJ ~48x, ALAB ~84x) back toward ~20x. This anchor-and-cap rule reproduces
    that with two parameters instead of inventing a target P/E.

    Returns None if a forward P/E can't be derived (no price or no forward EPS).
    """
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    eps_f = info.get("forwardEps")
    if not price or not eps_f or eps_f <= 0:
        return None
    own_pe = price / eps_f
    return float(min(own_pe * cfg["pe_own_mult"], cfg["pe_ceiling"]))


def _normalized_fcf(vals, cfg):
    """Average of the last N positive fiscal-year FCF values (cyclical smooth).

    ``vals`` is newest-first. Averaging over several years keeps a single
    peak-cycle year (e.g. a uranium miner's boom) from inflating the DCF.
    Returns None if there is no positive FCF.
    """
    n = cfg.get("fcf_avg_years", 4)
    window = [v for v in vals[:n] if v is not None and v > 0]
    if not window:
        return None
    return sum(window) / len(window)


def _multiples_value(info, cfg):
    """Earnings-multiple fair value per share: forward EPS x anchored fair P/E.

    Uses FORWARD EPS (AlphaSpread prices in next-year earnings) and a fair P/E
    anchored to the stock's own forward multiple (see ``_fair_pe``). Falls back
    to trailing EPS x the ceiling P/E only when no forward EPS exists. Returns
    None if no positive EPS is available.
    """
    eps_f = info.get("forwardEps")
    if eps_f is not None and eps_f > 0:
        fpe = _fair_pe(info, cfg)
        if fpe is not None:
            return float(eps_f * fpe)
    eps_t = info.get("trailingEps")
    if eps_t is not None and eps_t > 0:
        return float(eps_t * cfg["pe_ceiling"])
    return None


def compute_intrinsic_value(ticker, info=None, ticker_obj=None, **overrides):
    """Intrinsic value per share: 2-stage DCF blended with an earnings multiple.

    Mirrors AlphaSpread's "Base Case": intrinsic = w*multiples + (1-w)*DCF,
    with w = multiples_weight (default 0.5 => 50/50). This corrects the prior
    DCF-only estimate that overvalued cyclical/peak-FCF names.

    Returns a dict with intrinsic, dcf_value, multiples_value, upside_pct, and
    the key inputs. If DCF is not applicable (no positive FCF), intrinsic is
    None and reason explains why.
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
        "dcf_value": None, "multiples_value": None,
        # Sell-side analyst price targets (yfinance / stock-analysis feeds).
        "analyst_low": info.get("targetLowPrice"),
        "analyst_mean": info.get("targetMeanPrice"),
        "analyst_high": info.get("targetHighPrice"),
        "analyst_n": info.get("numberOfAnalystOpinions"),
    }
    if not eligible:
        return base

    years, vals = _fcf_series(ticker_obj)
    fcf_latest = vals[0] if vals else None
    fcf_norm = _normalized_fcf(vals, cfg) if vals else None
    growth = _estimate_growth(ticker_obj, info, cfg)
    wacc = _wacc_from_beta(info.get("beta"), cfg)
    shares = info.get("sharesOutstanding")
    net_debt = (info.get("totalDebt") or 0) - (info.get("totalCash") or 0)

    # DCF leg runs on normalized (averaged) FCF; skipped when no positive FCF.
    # Currency guard: for ADRs the financials can be reported in a different
    # currency than the price/shares (e.g. TSM: FCF in TWD, price/shares USD).
    # FCF/shares would then mix currencies and explode, so skip the DCF leg
    # when they disagree -- the multiples leg uses EPS in the price currency
    # and is unaffected.
    cur_price = info.get("currency")
    cur_fin = info.get("financialCurrency")
    currency_ok = not (cur_price and cur_fin and cur_price != cur_fin)

    dcf_v = None
    if fcf_norm is not None and currency_ok:
        dcf_v = _dcf_value(fcf_norm, growth, wacc, cfg, net_debt, shares)
    mult_v = _multiples_value(info, cfg)

    # Intrinsic is the multiples estimate (see DEFAULTS: multiples_weight=1.0).
    # DCF is computed and reported for context but not blended in by default,
    # because forcing a target multiple onto cyclicals (e.g. semis at 6x) via
    # DCF re-rating produced large, systematic overvaluation. When w < 1.0 the
    # two legs blend; the DCF-only fallback covers names with no forward EPS.
    w = cfg["multiples_weight"]
    if mult_v is not None and dcf_v is not None:
        intrinsic = w * mult_v + (1 - w) * dcf_v
    elif mult_v is not None:
        intrinsic = mult_v
    elif dcf_v is not None:
        intrinsic = dcf_v
    else:
        intrinsic = None

    upside = ((intrinsic - price) / price * 100.0) if (intrinsic and price) else None
    base.update({
        "intrinsic": intrinsic, "upside_pct": upside,
        "dcf_value": dcf_v, "multiples_value": mult_v,
        "wacc": wacc, "growth": growth, "fcf_latest": fcf_latest,
        "fcf_normalized": fcf_norm, "net_debt": net_debt, "shares": shares,
        "assumptions": {
            "terminal_growth": cfg["terminal_growth"], "beta": info.get("beta"),
            "stage1_years": cfg["stage1_years"], "stage2_years": cfg["stage2_years"],
            "fair_pe": _fair_pe(info, cfg), "multiples_weight": w,
        },
    })
    return base


def _dcf_per_share(fcf, growth, wacc, g_term, n_years, net_debt, shares):
    """Legacy single-stage DCF (kept for historical_intrinsic_series)."""
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
    shares = info.get("sharesOutstanding")
    net_debt = (info.get("totalDebt") or 0) - (info.get("totalCash") or 0)

    # Rolling growth: halved CAGR of FCF up to and including each year, so the
    # historical line uses the same tempered 2-stage DCF as the current value.
    out = []
    for i, (yr, fcf) in enumerate(pairs):
        if fcf is None or fcf <= 0 or not shares:
            continue
        window = [v for (_, v) in pairs[:i + 1]]
        g = _cagr(window)
        if g is None:
            g = 0.05
        g = float(min(max(g * cfg["growth_haircut"], 0.0), cfg["growth_cap"]))
        iv = _dcf_value(fcf, g, wacc, cfg, net_debt, shares)
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
                label="Intrinsic value (approx)")
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


def save_plot_png(val, out_dir):
    """Render a stock's chart to a PNG file. Returns the path, or None."""
    import base64
    import os
    b64 = plot_to_base64(val)
    if not b64:
        return None
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{val['ticker']}.png")
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))
    return path


# =========================================================================
# CLI
# =========================================================================

def _verdict(upside_pct, band=5.0):
    """Verdict string with a neutral band around fair value.

    Within +/- ``band`` percent the stock is called Fairly valued -- this is
    the common case now that fair P/E is anchored to the stock's own multiple,
    so many names sit right at intrinsic value.
    """
    if upside_pct is None:
        return "N/A"
    if upside_pct > band:
        return "Undervalued"
    if upside_pct < -band:
        return "Overvalued"
    return "Fairly valued"


def _print_table(results):
    """Print a sorted valuation table to stdout."""
    def _key(v):
        up = v.get("upside_pct")
        return (0, -up) if (v["eligible"] and up is not None) else (1, 0)

    ordered = sorted(results, key=_key)

    def _money(x):
        return f"${x:,.2f}" if x is not None else "-"

    print(f"\n{'Ticker':<8}{'Basket':<18}{'Price':>9}{'DCF':>9}{'Mult':>9}"
          f"{'Intrinsic':>10}{'Upside':>7}  {'AnLow':>8}{'AnMean':>8}"
          f"{'AnHigh':>8}  Verdict")
    print("-" * 112)
    for v in ordered:
        up = v.get("upside_pct")
        price = _money(v.get("price"))
        if v["eligible"] and up is not None:
            dcf = _money(v.get("dcf_value"))
            mult = _money(v.get("multiples_value"))
            iv = _money(v.get("intrinsic"))
            up_s = f"{up:+.0f}%"
            verdict = _verdict(up)
        else:
            dcf = mult = iv = up_s = "-"
            verdict = f"N/A ({v.get('reason','')})"
        a_lo = _money(v.get("analyst_low"))
        a_mid = _money(v.get("analyst_mean"))
        a_hi = _money(v.get("analyst_high"))
        print(f"{v['ticker']:<8}{v.get('basket',''):<18}{price:>9}{dcf:>9}"
              f"{mult:>9}{iv:>10}{up_s:>7}  {a_lo:>8}{a_mid:>8}{a_hi:>8}  "
              f"{verdict}")


def run(by_strategy=False, save_dir=None, tickers=None, **overrides):
    """Compute intrinsic values for the single-stock universe and print them.

    Args:
        by_strategy: group the printed output by basket (strategy).
        save_dir: if set, also write a PNG chart per stock to this directory.
        tickers: optional explicit list of tickers (overrides the universe).
        overrides: DCF assumption overrides (risk_free, growth_cap, ...).

    Returns the list of result dicts.
    """
    if tickers:
        stocks = [(t, "") for t in tickers]
    else:
        stocks = get_single_stocks()

    print(f"Computing DCF intrinsic value for {len(stocks)} stocks...")
    results = []
    for tk, basket in stocks:
        try:
            v = analyze_ticker(tk, basket, **overrides)
        except Exception as e:
            v = {"ticker": tk, "basket": basket, "name": tk, "eligible": False,
                 "reason": f"error: {e}", "price": None, "intrinsic": None,
                 "upside_pct": None, "price_dates": [], "price_closes": [],
                 "hist_intrinsic": []}
        results.append(v)
        tag = "OK " if v["eligible"] else "N/A"
        up = f"{v['upside_pct']:+.0f}%" if v.get("upside_pct") is not None else "-"
        print(f"  {tk:<8} {tag} {up:>8}  {v.get('reason','')}")
        if save_dir:
            p = save_plot_png(v, save_dir)
            if p:
                print(f"           chart -> {p}")

    if by_strategy:
        baskets = []
        for v in results:
            if v.get("basket") not in baskets:
                baskets.append(v.get("basket"))
        for b in baskets:
            print(f"\n===== {b or 'Ungrouped'} =====")
            _print_table([v for v in results if v.get("basket") == b])
    else:
        _print_table(results)

    return results


def _parse_args(argv=None):
    import argparse
    p = argparse.ArgumentParser(
        description="DCF intrinsic value for AI-allocation single stocks.")
    p.add_argument("--by-strategy", action="store_true",
                   help="Group output by basket/strategy")
    p.add_argument("--save-charts", metavar="DIR", default=None,
                   help="Also write a PNG chart per stock to DIR "
                        "(e.g. output/intrinsic)")
    p.add_argument("--tickers", default=None,
                   help="Comma-separated tickers to value instead of the "
                        "full universe")
    p.add_argument("--growth-cap", type=float, default=None,
                   help="Cap projected FCF growth (e.g. 0.25 = 25%%/yr)")
    p.add_argument("--terminal-growth", type=float, default=None,
                   help="Long-run terminal growth rate (e.g. 0.025)")
    p.add_argument("--risk-free", type=float, default=None,
                   help="Risk-free rate for the CAPM discount rate")
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    overrides = {}
    if args.growth_cap is not None:
        overrides["growth_cap"] = args.growth_cap
    if args.terminal_growth is not None:
        overrides["terminal_growth"] = args.terminal_growth
    if args.risk_free is not None:
        overrides["risk_free"] = args.risk_free
    tickers = ([t.strip().upper() for t in args.tickers.split(",")]
               if args.tickers else None)
    run(by_strategy=args.by_strategy, save_dir=args.save_charts,
        tickers=tickers, **overrides)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
