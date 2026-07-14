"""DCF intrinsic value for the AI-allocation portfolio (AlphaSpread-style).

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
# Calibrated to track AlphaSpread's "Base Case": a 2-stage DCF blended 50/50
# with an earnings-multiple valuation. Earlier defaults (flat 25% growth for
# 10 years, DCF only) overvalued cyclical/peak-FCF names by ~5-6x; these are
# deliberately conservative.
DEFAULTS = {
    "risk_free": 0.043,        # ~10y treasury
    "equity_premium": 0.055,   # equity risk premium
    "wacc_min": 0.08,
    "wacc_max": 0.14,
    "terminal_growth": 0.025,  # long-run GDP-ish (stage-2 / terminal)
    # Stage 1: near-term growth, tempered and capped hard.
    "growth_cap": 0.12,        # cap projected growth at 12%/yr (was 25%)
    "stage1_years": 5,         # high-growth phase (was 10)
    "stage2_years": 5,         # fade phase toward terminal growth
    "growth_haircut": 0.5,     # use only half of historical CAGR (mean-revert)
    # Multiples method.
    "fair_pe": 18.0,           # baseline fair P/E applied to normalized EPS
    "multiples_weight": 0.5,   # blend: 0.5 => 50% DCF + 50% multiples
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


def _estimate_growth(ticker_obj, info, cfg):
    """Conservative near-term growth estimate for stage 1 of the DCF.

    Blends historical FCF CAGR (halved to mean-revert away from cyclical
    peaks) with analyst earnings growth when available, then hard-caps it.
    Returns a fraction (e.g. 0.10 for 10%/yr).
    """
    years, vals = _fcf_series(ticker_obj)
    hist = _cagr(list(reversed(vals))) if vals else None
    if hist is not None:
        hist = hist * cfg["growth_haircut"]   # temper peak-cycle CAGR

    analyst = info.get("earningsGrowth")
    if analyst is not None and analyst > 0:
        analyst = min(float(analyst), 0.30)

    candidates = [g for g in (hist, analyst) if g is not None and g > 0]
    if candidates:
        growth = sum(candidates) / len(candidates)
    else:
        rg = info.get("revenueGrowth")
        growth = float(rg) if rg else 0.05

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


def _multiples_value(info, cfg):
    """Earnings-multiple fair value per share: normalized EPS x fair P/E.

    Uses the lower of trailing and forward EPS (conservative) times a fair
    P/E. Returns None if EPS is missing or non-positive.
    """
    eps_t = info.get("trailingEps")
    eps_f = info.get("forwardEps")
    eps_candidates = [e for e in (eps_t, eps_f) if e is not None and e > 0]
    if not eps_candidates:
        return None
    eps = min(eps_candidates)      # conservative
    return float(eps * cfg["fair_pe"])


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
    }
    if not eligible:
        return base

    years, vals = _fcf_series(ticker_obj)
    fcf_latest = vals[0]
    growth = _estimate_growth(ticker_obj, info, cfg)
    wacc = _wacc_from_beta(info.get("beta"), cfg)
    shares = info.get("sharesOutstanding")
    net_debt = (info.get("totalDebt") or 0) - (info.get("totalCash") or 0)

    dcf_v = _dcf_value(fcf_latest, growth, wacc, cfg, net_debt, shares)
    mult_v = _multiples_value(info, cfg)

    # Blend: 50/50 when both exist, else whichever is available.
    w = cfg["multiples_weight"]
    if dcf_v is not None and mult_v is not None:
        intrinsic = w * mult_v + (1 - w) * dcf_v
    elif dcf_v is not None:
        intrinsic = dcf_v
    elif mult_v is not None:
        intrinsic = mult_v
    else:
        intrinsic = None

    upside = ((intrinsic - price) / price * 100.0) if (intrinsic and price) else None
    base.update({
        "intrinsic": intrinsic, "upside_pct": upside,
        "dcf_value": dcf_v, "multiples_value": mult_v,
        "wacc": wacc, "growth": growth, "fcf_latest": fcf_latest,
        "net_debt": net_debt, "shares": shares,
        "assumptions": {
            "terminal_growth": cfg["terminal_growth"], "beta": info.get("beta"),
            "stage1_years": cfg["stage1_years"], "stage2_years": cfg["stage2_years"],
            "fair_pe": cfg["fair_pe"], "multiples_weight": w,
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

def _print_table(results):
    """Print a sorted valuation table to stdout."""
    def _key(v):
        up = v.get("upside_pct")
        return (0, -up) if (v["eligible"] and up is not None) else (1, 0)

    ordered = sorted(results, key=_key)
    print(f"\n{'Ticker':<8}{'Basket':<20}{'Price':>9}{'DCF':>9}{'Mult':>9}"
          f"{'Intrinsic':>10}{'Upside':>8}  Verdict")
    print("-" * 88)
    for v in ordered:
        up = v.get("upside_pct")
        price = f"${v['price']:,.2f}" if v.get("price") else "-"
        if v["eligible"] and up is not None:
            dcf = f"${v['dcf_value']:,.2f}" if v.get("dcf_value") else "-"
            mult = f"${v['multiples_value']:,.2f}" if v.get("multiples_value") else "-"
            iv = f"${v['intrinsic']:,.2f}"
            up_s = f"{up:+.0f}%"
            verdict = "Undervalued" if up > 0 else "Overvalued"
        else:
            dcf = mult = iv = up_s = "-"
            verdict = f"N/A ({v.get('reason','')})"
        print(f"{v['ticker']:<8}{v.get('basket',''):<20}{price:>9}{dcf:>9}"
              f"{mult:>9}{iv:>10}{up_s:>8}  {verdict}")


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
