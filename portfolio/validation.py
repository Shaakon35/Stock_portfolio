import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

from portfolio.ranking import (
    RANKING_UNIVERSE, STRATEGY_WEIGHTS, RISK_ADJUSTMENTS,
    score_analyst_upside, score_revenue_quality, score_analyst_conviction,
    score_entry_position, score_momentum, score_valuation,
    score_long_term_health, score_cash_runway,
    penalty_fragility, penalty_downside, bonus_profitability,
)

# =========================================================================
# EXTRA STOCKS for broader backtest validation
# =========================================================================

BACKTEST_EXTRA = {
    "NVDA":  {"name": "Nvidia",             "basket": "Core ETF",    "strategy": "hold_forever", "what": "AI GPU monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "AAPL":  {"name": "Apple",              "basket": "Core ETF",    "strategy": "hold_forever", "what": "Consumer electronics + services ecosystem",
              "fragility": "none",      "downside_if_fail": "low"},
    "MSFT":  {"name": "Microsoft",          "basket": "Core ETF",    "strategy": "hold_forever", "what": "Cloud + enterprise software + AI",
              "fragility": "none",      "downside_if_fail": "low"},
    "AMZN":  {"name": "Amazon",             "basket": "Core ETF",    "strategy": "hold_forever", "what": "Cloud (AWS) + e-commerce + AI",
              "fragility": "none",      "downside_if_fail": "low"},
    "GOOGL": {"name": "Alphabet",           "basket": "Core ETF",    "strategy": "hold_forever", "what": "Search + cloud + AI + YouTube",
              "fragility": "none",      "downside_if_fail": "low"},
    "META":  {"name": "Meta",               "basket": "Core ETF",    "strategy": "hold_forever", "what": "Social media + metaverse + AI",
              "fragility": "none",      "downside_if_fail": "low"},
    "ASML":  {"name": "ASML",               "basket": "Core ETF",    "strategy": "hold_forever", "what": "EUV lithography monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "TSM":   {"name": "TSMC",               "basket": "Core ETF",    "strategy": "hold_forever", "what": "Semiconductor foundry monopoly",
              "fragility": "political", "downside_if_fail": "moderate"},
    "AMD":   {"name": "AMD",                "basket": "Core ETF",    "strategy": "cycle",        "what": "CPU + GPU + data center chips",
              "fragility": "none",      "downside_if_fail": "low"},
    "MRVL":  {"name": "Marvell",            "basket": "Core ETF",    "strategy": "cycle",        "what": "Custom AI silicon + networking",
              "fragility": "none",      "downside_if_fail": "low"},
    "PLTR":  {"name": "Palantir",           "basket": "Core ETF",    "strategy": "cycle",        "what": "AI/ML data analytics platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "TSLA":  {"name": "Tesla",              "basket": "Core ETF",    "strategy": "cycle",        "what": "EVs + energy + autonomy + AI",
              "fragility": "political", "downside_if_fail": "moderate"},
    "MU":    {"name": "Micron",             "basket": "Core ETF",    "strategy": "cycle",        "what": "DRAM + NAND memory for AI servers",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "SNOW":  {"name": "Snowflake",          "basket": "Core ETF",    "strategy": "cycle",        "what": "Cloud data warehouse + AI analytics",
              "fragility": "none",      "downside_if_fail": "low"},
    "NET":   {"name": "Cloudflare",         "basket": "Cyber",       "strategy": "cycle",        "what": "Edge computing + CDN + security",
              "fragility": "none",      "downside_if_fail": "low"},
    "COIN":  {"name": "Coinbase",           "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Crypto exchange + custody",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "ANET":  {"name": "Arista Networks",    "basket": "Industrial",  "strategy": "hold_forever", "what": "Data center networking switches",
              "fragility": "none",      "downside_if_fail": "low"},
    "UBER":  {"name": "Uber",               "basket": "Core ETF",    "strategy": "hold_forever", "what": "Ride-hailing + delivery + freight",
              "fragility": "none",      "downside_if_fail": "low"},
    "SQ":    {"name": "Block",              "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Payments + Cash App + Bitcoin",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "SHOP":  {"name": "Shopify",            "basket": "Core ETF",    "strategy": "cycle",        "what": "E-commerce platform for SMBs",
              "fragility": "none",      "downside_if_fail": "low"},
    # --- Top performers last 12 months (for validation breadth) ---
    "APP":   {"name": "AppLovin",           "basket": "SpecGrowth",  "strategy": "cycle",        "what": "AI-powered mobile ad tech platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "HOOD":  {"name": "Robinhood",          "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Commission-free trading platform",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "MSTR":  {"name": "MicroStrategy",      "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Bitcoin treasury company",
              "fragility": "macro",     "downside_if_fail": "severe"},
    "AFRM":  {"name": "Affirm",             "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Buy-now-pay-later fintech",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "DUOL":  {"name": "Duolingo",           "basket": "Core ETF",    "strategy": "hold_forever", "what": "AI language learning platform — monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "CELH":  {"name": "Celsius",            "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Energy drink challenger brand",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "HIMS":  {"name": "Hims & Hers",        "basket": "MedTech",     "strategy": "cycle",        "what": "Telehealth + direct-to-consumer pharma",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "SMCI":  {"name": "Super Micro",        "basket": "Industrial",  "strategy": "cycle",        "what": "AI server hardware manufacturer",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "CAVA":  {"name": "Cava Group",         "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Fast-casual Mediterranean restaurant chain",
              "fragility": "none",      "downside_if_fail": "low"},
    "RDDT":  {"name": "Reddit",             "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Social media + AI data licensing",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "VST":   {"name": "Vistra",             "basket": "Nuclear",     "strategy": "cycle",        "what": "Nuclear + natural gas power generation",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "CEG":   {"name": "Constellation Energy","basket": "Nuclear",    "strategy": "hold_forever", "what": "Largest US nuclear fleet operator",
              "fragility": "none",      "downside_if_fail": "low"},
    "TLN":   {"name": "Talen Energy",       "basket": "Nuclear",     "strategy": "cycle",        "what": "Nuclear + data center power provider",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "AVGO":  {"name": "Broadcom",           "basket": "Core ETF",    "strategy": "hold_forever", "what": "AI networking + VMware + custom silicon",
              "fragility": "none",      "downside_if_fail": "low"},
    "GRAB":  {"name": "Grab Holdings",      "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Southeast Asia super-app (ride/food/fintech)",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "SOFI":  {"name": "SoFi Technologies", "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Digital banking + lending + investing",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "TOST":  {"name": "Toast",              "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Restaurant management SaaS + payments",
              "fragility": "none",      "downside_if_fail": "low"},
    "IBKR":  {"name": "Interactive Brokers", "basket": "Core ETF",   "strategy": "hold_forever", "what": "Global electronic brokerage",
              "fragility": "none",      "downside_if_fail": "low"},
    "SPOT":  {"name": "Spotify",            "basket": "Core ETF",    "strategy": "hold_forever", "what": "Audio streaming monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "ARM":   {"name": "ARM Holdings",       "basket": "Core ETF",    "strategy": "hold_forever", "what": "CPU architecture IP licensing monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "DASH":  {"name": "DoorDash",           "basket": "Core ETF",    "strategy": "cycle",        "what": "Food delivery + logistics platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "TTD":   {"name": "The Trade Desk",     "basket": "Core ETF",    "strategy": "cycle",        "what": "Programmatic digital advertising platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "LLY":   {"name": "Eli Lilly",          "basket": "MedTech",     "strategy": "hold_forever", "what": "GLP-1 obesity/diabetes drugs — Mounjaro/Zepbound",
              "fragility": "none",      "downside_if_fail": "low"},
    "DKNG":  {"name": "DraftKings",         "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Online sports betting + iGaming",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "ONON":  {"name": "On Holding",         "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Premium running shoes + athleisure",
              "fragility": "none",      "downside_if_fail": "low"},
    "BIRK":  {"name": "Birkenstock",        "basket": "SpecGrowth",  "strategy": "hold_forever", "what": "Iconic sandal brand — pricing power",
              "fragility": "none",      "downside_if_fail": "low"},
    "OSCR":  {"name": "Oscar Health",       "basket": "MedTech",     "strategy": "cycle",        "what": "Tech-driven health insurance",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "MNDY":  {"name": "Monday.com",         "basket": "Core ETF",    "strategy": "cycle",        "what": "Work management SaaS platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "FOUR":  {"name": "Shift4 Payments",    "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Integrated payment processing",
              "fragility": "none",      "downside_if_fail": "low"},
    "TWLO":  {"name": "Twilio",             "basket": "Core ETF",    "strategy": "cycle",        "what": "Cloud communications APIs",
              "fragility": "none",      "downside_if_fail": "low"},
}


# =========================================================================
# HISTORICAL DATA FETCHING
# =========================================================================

def fetch_historical_data(ticker, lookback_date):
    """Fetch stock data as it would have appeared on lookback_date.

    Uses historical prices and financials to reconstruct the ranking
    inputs from a past date. Analyst target/consensus use current values
    as a proxy (not available historically via yfinance).

    Args:
        ticker: stock ticker
        lookback_date: datetime — the "as of" date for the backtest

    Returns:
        dict with same keys as ranking.fetch_stock_data, plus 'price_now'
    """
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}

        # --- Historical price on lookback_date ---
        # Fetch a window around the lookback date to ensure we get a trading day
        start = lookback_date - timedelta(days=10)
        end = lookback_date + timedelta(days=5)
        hist_window = t.history(start=start, end=end)
        if hist_window.empty:
            return {"error": f"no price data around {lookback_date.date()}"}

        close = hist_window["Close"].dropna()
        if close.empty:
            return {"error": "no close prices"}

        # Get the last price on or before lookback_date
        mask = close.index <= lookback_date.strftime("%Y-%m-%d 23:59:59")
        if hasattr(close.index, 'tz') and close.index.tz is not None:
            from pandas import Timestamp
            cutoff = Timestamp(lookback_date).tz_localize(close.index.tz)
            mask = close.index <= cutoff
        prices_before = close[mask]
        if prices_before.empty:
            price_then = float(close.iloc[0])
        else:
            price_then = float(prices_before.iloc[-1])

        # --- Current price (for return calculation) ---
        hist_now = t.history(period="5d")
        close_now = hist_now["Close"].dropna()
        price_now = float(close_now.iloc[-1]) if not close_now.empty else None

        # --- Historical SMAs (need 2y of data ending at lookback_date) ---
        hist_start = lookback_date - timedelta(days=800)
        hist_2y = t.history(start=hist_start, end=lookback_date + timedelta(days=1))
        hist_close = hist_2y["Close"].dropna() if not hist_2y.empty else None

        sma_50 = None
        sma_200 = None
        high_2y = None
        history_years = None
        if hist_close is not None and len(hist_close) > 0:
            if len(hist_close) >= 50:
                sma_50 = float(hist_close.rolling(50).mean().iloc[-1])
            if len(hist_close) >= 200:
                sma_200 = float(hist_close.rolling(200).mean().iloc[-1])
            high_2y = float(hist_close.max())
            history_years = len(hist_close) / 252.0

        # --- Historical 52w range ---
        hist_52w = hist_close.iloc[-252:] if hist_close is not None and len(hist_close) >= 252 else hist_close
        high_52w = float(hist_52w.max()) if hist_52w is not None and len(hist_52w) > 0 else None
        low_52w = float(hist_52w.min()) if hist_52w is not None and len(hist_52w) > 0 else None

        # --- Revenue growth from quarterly financials (reconstruct TTM) ---
        rev_growth = None
        total_revenue = None
        try:
            qf = t.quarterly_income_stmt
            if qf is not None and "Total Revenue" in qf.index and len(qf.columns) >= 5:
                # Find quarters that were available at lookback_date
                # Quarterly reports are typically available ~45 days after quarter end
                avail_cols = [c for c in qf.columns if c <= lookback_date + timedelta(days=45)]
                if len(avail_cols) >= 8:
                    recent_4 = sum(qf.loc["Total Revenue", avail_cols[:4]])
                    prior_4 = sum(qf.loc["Total Revenue", avail_cols[4:8]])
                    if prior_4 and prior_4 > 0 and recent_4 and recent_4 > 0:
                        rev_growth = ((recent_4 - prior_4) / prior_4) * 100
                        total_revenue = recent_4
        except Exception:
            pass

        # Fall back to info if quarterly didn't work
        if rev_growth is None:
            rg = info.get("revenueGrowth")
            rev_growth = (rg * 100) if rg is not None else None
            if not total_revenue:
                total_revenue = info.get("totalRevenue", 0)

        # --- Valuation: compute historical P/S ---
        ps_ratio = None
        if total_revenue and total_revenue > 0:
            shares = info.get("sharesOutstanding")
            if shares and shares > 0:
                ps_ratio = (price_then * shares) / total_revenue

        # Fall back to current P/S if we couldn't compute historical
        if ps_ratio is None:
            ps_ratio = info.get("priceToSalesTrailing12Months")

        # --- Cash and profitability (use current as proxy) ---
        eps = info.get("trailingEps")
        free_cash_flow = info.get("freeCashflow")
        total_cash = info.get("totalCash")
        market_cap = info.get("marketCap")

        # --- Analyst data (current as proxy — not available historically) ---
        target = info.get("targetMeanPrice")
        rec = info.get("recommendationKey", "none")
        num_analysts = info.get("numberOfAnalystOpinions", 0)

        return {
            "price": price_then,
            "price_now": price_now,
            "target": target,
            "recommendation": rec,
            "num_analysts": num_analysts or 0,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "market_cap": market_cap,
            "total_revenue": total_revenue,
            "rev_growth_pct": rev_growth,
            "eps": eps,
            "free_cash_flow": free_cash_flow,
            "ps_ratio": ps_ratio,
            "total_cash": total_cash,
            "high_2y": high_2y,
            "history_years": round(history_years, 1) if history_years else None,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "error": None,
        }

    except Exception as e:
        return {"error": str(e)}


# =========================================================================
# BACKTEST ENGINE
# =========================================================================

def compute_backtest_score(data, meta):
    """Same as compute_composite but works with historical data."""
    if data.get("error"):
        return 0, {}

    price = data["price"]
    strategy = meta.get("strategy", "hold_forever")
    w = STRATEGY_WEIGHTS.get(strategy, STRATEGY_WEIGHTS["hold_forever"])

    s_upside = score_analyst_upside(price, data["target"])
    s_growth = score_revenue_quality(
        data["rev_growth_pct"], data.get("total_revenue", 0)
    )
    s_valuation = score_valuation(data.get("ps_ratio"))
    s_long_term = score_long_term_health(
        price, data.get("high_2y"), data.get("history_years")
    )
    s_cash = score_cash_runway(
        data.get("total_cash"), data.get("free_cash_flow"), data.get("eps")
    )
    s_conviction = score_analyst_conviction(
        data["recommendation"], data["num_analysts"]
    )
    s_entry = score_entry_position(price, data["high_52w"], data["low_52w"])
    s_momentum = score_momentum(price, data["sma_50"], data["sma_200"])

    base_score = (
        s_upside * w["upside"]
        + s_growth * w["growth"]
        + s_valuation * w["valuation"]
        + s_long_term * w["long_term"]
        + s_cash * w["cash_runway"]
        + s_conviction * w["conviction"]
        + s_entry * w["entry"]
        + s_momentum * w["momentum"]
    )

    p_fragility = penalty_fragility(meta.get("fragility", "none"))
    p_downside = penalty_downside(meta.get("downside_if_fail", "low"))
    b_profit = bonus_profitability(
        data.get("eps"), data.get("free_cash_flow"), data.get("market_cap")
    )

    composite = base_score + b_profit + p_fragility + p_downside
    composite = max(0, min(100, composite))

    breakdown = {
        "upside": round(s_upside, 1),
        "growth": round(s_growth, 1),
        "valuation": round(s_valuation, 1),
        "long_term": round(s_long_term, 1),
        "cash_runway": round(s_cash, 1),
        "conviction": round(s_conviction, 1),
        "entry": round(s_entry, 1),
        "momentum": round(s_momentum, 1),
        "profitability": b_profit,
        "fragility": p_fragility,
        "downside": p_downside,
    }

    return round(composite, 1), breakdown


def run_backtest(lookback_months=12):
    """Run the ranking model on historical data and compare with actual returns.

    Args:
        lookback_months: how many months ago to simulate (default 12)

    Returns:
        list of dicts with ranking, score, actual return, sorted by score desc
    """
    lookback_date = datetime.now() - timedelta(days=lookback_months * 30)

    # Combine ranking universe + extra stocks
    universe = {}
    universe.update(RANKING_UNIVERSE)
    universe.update(BACKTEST_EXTRA)

    results = []

    for ticker, meta in universe.items():
        data = fetch_historical_data(ticker, lookback_date)

        if data.get("error"):
            print(f"  ⚠️ {ticker}: {data['error']}")
            continue

        score, breakdown = compute_backtest_score(data, meta)

        # Actual return
        price_then = data["price"]
        price_now = data.get("price_now")
        if price_then and price_now and price_then > 0:
            actual_return = ((price_now - price_then) / price_then) * 100
        else:
            actual_return = None

        results.append({
            "ticker": ticker,
            "name": meta["name"],
            "basket": meta["basket"],
            "strategy": meta["strategy"],
            "what": meta["what"],
            "price_then": round(price_then, 2),
            "price_now": round(price_now, 2) if price_now else None,
            "actual_return_pct": round(actual_return, 1) if actual_return is not None else None,
            "score": score,
            "breakdown": breakdown,
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    # Assign ranks
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results


def compute_validation_stats(results):
    """Compute validation metrics from backtest results.

    Returns dict with:
    - quintile_returns: avg return per quintile (top 20%, next 20%, etc.)
    - top5_avg, top10_avg, bottom10_avg: avg returns for key groups
    - correlation: rank correlation between score and return
    - hit_rate: % of top-half stocks that beat bottom-half average
    """
    # Filter out stocks with no return data
    valid = [r for r in results if r["actual_return_pct"] is not None]
    if len(valid) < 10:
        return {"error": "Not enough data for validation"}

    n = len(valid)

    # Quintile analysis (5 groups)
    q_size = n // 5
    quintiles = {}
    for i in range(5):
        start = i * q_size
        end = start + q_size if i < 4 else n
        group = valid[start:end]
        avg_ret = np.mean([r["actual_return_pct"] for r in group])
        avg_score = np.mean([r["score"] for r in group])
        quintiles[f"Q{i+1}"] = {
            "label": ["Top 20%", "20-40%", "40-60%", "60-80%", "Bottom 20%"][i],
            "avg_return": round(avg_ret, 1),
            "avg_score": round(avg_score, 1),
            "stocks": [r["ticker"] for r in group],
        }

    # Key group averages
    top5 = valid[:5]
    top10 = valid[:10]
    bottom10 = valid[-10:]

    top5_avg = round(np.mean([r["actual_return_pct"] for r in top5]), 1)
    top10_avg = round(np.mean([r["actual_return_pct"] for r in top10]), 1)
    bottom10_avg = round(np.mean([r["actual_return_pct"] for r in bottom10]), 1)

    # Rank correlation (Spearman)
    scores = [r["score"] for r in valid]
    returns = [r["actual_return_pct"] for r in valid]
    # Simple rank correlation
    score_ranks = np.argsort(np.argsort([-s for s in scores])) + 1
    return_ranks = np.argsort(np.argsort([-r for r in returns])) + 1
    n_v = len(valid)
    d_sq = sum((sr - rr) ** 2 for sr, rr in zip(score_ranks, return_ranks))
    spearman = 1 - (6 * d_sq) / (n_v * (n_v ** 2 - 1))

    # Hit rate: % of top-half that beat median return
    median_return = np.median(returns)
    top_half = valid[:n // 2]
    hits = sum(1 for r in top_half if r["actual_return_pct"] > median_return)
    hit_rate = round((hits / len(top_half)) * 100, 1)

    # Win rate: % of top 10 that had positive returns
    top10_positive = sum(1 for r in top10 if r["actual_return_pct"] > 0)
    win_rate = round((top10_positive / len(top10)) * 100, 1)

    return {
        "quintiles": quintiles,
        "top5_avg_return": top5_avg,
        "top10_avg_return": top10_avg,
        "bottom10_avg_return": bottom10_avg,
        "spearman_correlation": round(spearman, 3),
        "hit_rate": hit_rate,
        "win_rate_top10": win_rate,
        "total_stocks": n,
    }
