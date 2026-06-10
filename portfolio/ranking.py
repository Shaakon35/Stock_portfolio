import yfinance as yf
import numpy as np
from datetime import datetime

# =========================================================================
# RANKING UNIVERSE — all stocks to rank (existing + candidates)
# Add new tickers here with their metadata.
# The engine fetches live price/analyst/revenue data from Yahoo Finance.
# =========================================================================

RANKING_UNIVERSE = {
    # --- NUCLEAR ---
    # fragility: "none" = diversified/monopoly, "political" = gov/policy dependent,
    #            "macro" = commodity/rate dependent, "binary" = single event pass/fail
    # downside_if_fail: "low" = -15% max, "moderate" = -30-50%, "severe" = -70%+, "zero" = goes to $0
    "CCJ":   {"name": "Cameco",              "basket": "Nuclear",     "strategy": "hold_forever", "what": "Uranium mining — largest Western producer",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # uranium price dependent
    "GEV":   {"name": "GE Vernova",          "basket": "Nuclear",     "strategy": "hold_forever", "what": "Grid electrification, gas/wind turbines",
              "fragility": "none",      "downside_if_fail": "low"},        # diversified energy giant
    "SRUUF": {"name": "Sprott Uranium Trust", "basket": "Nuclear",    "strategy": "cycle",        "what": "Physical uranium trust — tracks U3O8 price",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # pure commodity play
    "LEU":   {"name": "Centrus Energy",      "basket": "Nuclear",     "strategy": "cycle",        "what": "Uranium enrichment, HALEU fuel for SMRs",
              "fragility": "political", "downside_if_fail": "moderate"},   # DOE contracts, policy
    "SMR":   {"name": "NuScale Power",       "basket": "Nuclear",     "strategy": "catalyst",     "what": "Small modular reactor — only NRC-approved SMR design",
              "fragility": "binary",    "downside_if_fail": "severe"},     # needs deployment order
    "OKLO":  {"name": "Oklo",                "basket": "Nuclear",     "strategy": "catalyst",     "what": "Advanced fission microreactor — Sam Altman backed",
              "fragility": "binary",    "downside_if_fail": "severe"},     # NRC license pending
    # --- QUANTUM ---
    "IONQ":  {"name": "IonQ",                "basket": "Quantum",     "strategy": "catalyst",     "what": "Trapped-ion quantum computing — revenue leader",
              "fragility": "binary",    "downside_if_fail": "severe"},     # quantum advantage proof
    "QNT":   {"name": "Quantinuum",          "basket": "Quantum",     "strategy": "catalyst",     "what": "Trapped-ion quantum (Honeywell) — IPO Jun 2026",
              "fragility": "binary",    "downside_if_fail": "moderate"},   # Honeywell backing = floor
    "QBTS":  {"name": "D-Wave Quantum",      "basket": "Quantum",     "strategy": "catalyst",     "what": "Quantum annealing + gate-model dual platform",
              "fragility": "binary",    "downside_if_fail": "severe"},     # quantum advantage proof
    "RGTI":  {"name": "Rigetti Computing",   "basket": "Quantum",     "strategy": "catalyst",     "what": "Superconducting quantum — modular chiplet architecture",
              "fragility": "binary",    "downside_if_fail": "severe"},     # quantum advantage proof
    # --- CYBER ---
    "CRWD":  {"name": "CrowdStrike",         "basket": "Cyber",       "strategy": "hold_forever", "what": "Endpoint cybersecurity platform — #1 market share",
              "fragility": "none",      "downside_if_fail": "low"},        # thousands of customers
    "PANW":  {"name": "Palo Alto Networks",  "basket": "Cyber",       "strategy": "hold_forever", "what": "Enterprise network security — AI-driven",
              "fragility": "none",      "downside_if_fail": "low"},        # enterprise duopoly
    # --- INDUSTRIAL ---
    "BWXT":  {"name": "BWX Technologies",    "basket": "Industrial",  "strategy": "hold_forever", "what": "Navy nuclear reactors — sole-source monopoly",
              "fragility": "none",      "downside_if_fail": "low"},        # 60-year navy contracts
    "POWL":  {"name": "Powell Industries",   "basket": "Industrial",  "strategy": "cycle",        "what": "Electrical switchgear for data centers",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # capex cycle dependent
    "VRT":   {"name": "Vertiv Holdings",     "basket": "Industrial",  "strategy": "cycle",        "what": "Data center cooling and power infrastructure",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # capex cycle dependent
    "FIX":   {"name": "Comfort Systems USA", "basket": "Industrial",  "strategy": "hold_forever", "what": "Data center HVAC and electrical contracting",
              "fragility": "none",      "downside_if_fail": "low"},        # diversified contracts
    # --- SPECGROWTH ---
    "RKLB":  {"name": "Rocket Lab",          "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Rockets + space systems — Neutron launch pending",
              "fragility": "binary",    "downside_if_fail": "moderate"},   # Neutron launch, but Electron works
    "LSCC":  {"name": "Lattice Semi",        "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Low-power FPGAs for edge AI and automotive",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # semi cycle
    "CRDO":  {"name": "Credo Technology",    "basket": "SpecGrowth",  "strategy": "cycle",        "what": "AI data center connectivity (optical + electrical)",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # AI capex cycle
    "VKTX":  {"name": "Viking Therapeutics", "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "GLP-1 obesity/NASH drug — Phase III",
              "fragility": "binary",    "downside_if_fail": "zero"},       # FDA approval or bust
    # --- NEW CANDIDATES ---
    "KTOS":  {"name": "Kratos Defense",      "basket": "Industrial",  "strategy": "cycle",        "what": "Autonomous military drones, hypersonic systems",
              "fragility": "political", "downside_if_fail": "moderate"},   # defense budget dependent
    "SERV":  {"name": "Serve Robotics",      "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Autonomous sidewalk delivery robots — Nvidia backed",
              "fragility": "binary",    "downside_if_fail": "severe"},     # regulatory + scale proof
    "ENVX":  {"name": "Enovix",              "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Silicon anode batteries — 2x energy density",
              "fragility": "binary",    "downside_if_fail": "severe"},     # mass production proof
    "APLD":  {"name": "Applied Digital",     "basket": "Industrial",  "strategy": "cycle",        "what": "AI GPU data center infrastructure",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # AI capex cycle
    "TMDX":  {"name": "TransMedics",         "basket": "MedTech",     "strategy": "hold_forever", "what": "Organ transplant logistics — monopoly OCS system",
              "fragility": "none",      "downside_if_fail": "low"},        # FDA-approved monopoly
    "IREN":  {"name": "IREN Limited",        "basket": "Industrial",  "strategy": "cycle",        "what": "AI cloud compute + Bitcoin mining infrastructure",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # BTC price + AI capex
    "AXON":  {"name": "Axon Enterprise",     "basket": "Defense",     "strategy": "hold_forever", "what": "Taser + body cams + AI evidence management",
              "fragility": "none",      "downside_if_fail": "low"},        # monopoly, gov customers
    "CIFR":  {"name": "Cipher Digital",      "basket": "Industrial",  "strategy": "cycle",        "what": "Bitcoin mining pivoting to AI data centers",
              "fragility": "macro",     "downside_if_fail": "moderate"},   # BTC price dependent
    "LUNR":  {"name": "Intuitive Machines",  "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Lunar landers — NASA commercial lunar partner",
              "fragility": "binary",    "downside_if_fail": "severe"},     # mission success dependent
    "ACHR":  {"name": "Archer Aviation",     "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "eVTOL air taxi — FAA certification pending",
              "fragility": "binary",    "downside_if_fail": "zero"},       # FAA cert or bust, pre-revenue
}

# Tickers to skip (private, no data, ETFs)
SKIP_TICKERS = {"XNDU", "INFQ", "HQ", "XAIX.DE", "SMHV.SW", "QDVE.DE"}


# =========================================================================
# SCORING FUNCTIONS — each returns 0-100
# =========================================================================

def score_analyst_upside(price, target_price):
    """Score based on analyst target upside. 0% = 0, 50%+ = 100.
    Returns 50 (neutral) when no analyst target exists."""
    if not price or price <= 0:
        return 50
    if not target_price:
        return 50
    upside_pct = ((target_price - price) / price) * 100
    # Negative upside = 0, cap at 50% = 100
    # Most stocks have 10-40% analyst upside; 50%+ is exceptional
    return max(0, min(100, upside_pct * (100 / 50)))


def score_revenue_quality(rev_growth_pct, total_revenue):
    """Score revenue quality: growth weighted by revenue scale.

    Raw growth from a tiny base is misleading (+3000% from $300K is less
    meaningful than +50% from $500M). We use log(revenue) as a multiplier
    so larger-base growth scores higher.

    Returns 50 (neutral) when data is missing — avoids penalizing
    pre-revenue companies that simply have no data.

    Scale factor: log10(revenue_in_millions)
      $1M   → 0.0    (no credit)
      $10M  → 1.0
      $100M → 2.0
      $1B   → 3.0
      $10B  → 4.0
    """
    # No data → neutral score (don't penalize missing data)
    if rev_growth_pct is None:
        return 50
    if not total_revenue or total_revenue <= 0:
        return 50

    # Confirmed negative growth → score 0-30 based on severity
    if rev_growth_pct <= 0:
        # -50% or worse = 0, 0% = 30
        return max(0, 30 + rev_growth_pct * (30 / 50))

    import math
    rev_millions = total_revenue / 1e6
    if rev_millions < 1:
        scale = 0
    else:
        scale = math.log10(rev_millions)  # 0-4 range

    # Normalize: growth capped at 50%, scale capped at 3 (=$1B)
    # Most good stocks grow 10-40% YoY; 50%+ is exceptional
    growth_norm = min(100, rev_growth_pct * (100 / 50))
    scale_norm = min(1.0, scale / 3.0)  # $1B+ = full credit

    # Blend: 60% raw growth + 40% scale-adjusted
    return growth_norm * (0.6 + 0.4 * scale_norm)


def score_analyst_conviction(recommendation, num_analysts):
    """Score based on analyst consensus + coverage depth."""
    rec_scores = {
        "strongBuy": 100, "strong_buy": 100,
        "buy": 75,
        "hold": 40,
        "sell": 10, "underperform": 10,
        "strongSell": 0, "strong_sell": 0,
    }
    base = rec_scores.get(recommendation, 40)
    # Bonus for more analysts (more reliable signal)
    # 1-3 analysts = 0.6x, 10+ = 1.0x, 20+ = 1.1x
    if num_analysts >= 20:
        coverage_mult = 1.1
    elif num_analysts >= 10:
        coverage_mult = 1.0
    elif num_analysts >= 5:
        coverage_mult = 0.85
    else:
        coverage_mult = 0.6
    return min(100, base * coverage_mult)


def score_entry_position(price, high_52w, low_52w):
    """Score based on position in 52w range. Near low = 100, near high = 0."""
    if not high_52w or not low_52w or high_52w == low_52w:
        return 50
    position = (high_52w - price) / (high_52w - low_52w)
    return max(0, min(100, position * 100))


def score_momentum(price, sma_50, sma_200):
    """Score based on trend alignment. Full uptrend = 100, downtrend = 0."""
    if not sma_50 or not sma_200:
        return 50
    if price > sma_50 and price > sma_200 and sma_50 > sma_200:
        return 100  # Strong uptrend
    elif price > sma_200 and sma_50 > sma_200:
        return 80   # Uptrend, minor pullback
    elif price > sma_200:
        return 60   # Above long-term support
    elif price > sma_50:
        return 40   # Short-term bounce in downtrend
    elif sma_50 < sma_200:
        return 10   # Death cross
    else:
        return 30   # Neutral


def score_valuation(ps_ratio):
    """Score based on Price-to-Sales ratio. Lower = cheaper = better.

    P/S < 3  → 100 (deep value)
    P/S 3-10 → 70-100 (reasonable for growth)
    P/S 10-30 → 30-70 (expensive, needs high growth to justify)
    P/S 30-60 → 10-30 (very expensive)
    P/S > 60 → 0-10 (extreme, priced for perfection)

    Returns 50 (neutral) for pre-revenue or missing data.
    """
    if ps_ratio is None or ps_ratio <= 0:
        return 50
    if ps_ratio < 3:
        return 100
    elif ps_ratio < 10:
        # 3 → 100, 10 → 70 (linear)
        return 100 - (ps_ratio - 3) * (30 / 7)
    elif ps_ratio < 30:
        # 10 → 70, 30 → 30 (linear)
        return 70 - (ps_ratio - 10) * (40 / 20)
    elif ps_ratio < 60:
        # 30 → 30, 60 → 5 (linear)
        return 30 - (ps_ratio - 30) * (25 / 30)
    else:
        return 5


def score_long_term_health(price, high_2y, history_years):
    """Score based on price vs 2-year high.

    Measures structural health: a stock near its 2y high is healthy,
    one at 10% of its 2y high is likely dying.

    Only applies penalty when stock has 3+ years of history to avoid
    penalizing SPACs/IPOs for inflated early prices.

    Returns 50 (neutral) when insufficient history.
    """
    if not high_2y or not price or price <= 0:
        return 50
    if history_years is not None and history_years < 3:
        return 50  # Too young — SPAC/IPO noise

    pct_of_high = (price / high_2y) * 100

    if pct_of_high >= 80:
        return 100  # Near highs — healthy
    elif pct_of_high >= 60:
        return 75   # Moderate pullback
    elif pct_of_high >= 40:
        return 50   # Significant decline
    elif pct_of_high >= 20:
        return 25   # Severe decline
    else:
        return 5    # Structural collapse (<20% of 2y high)


def score_cash_runway(total_cash, free_cash_flow, eps):
    """Score based on years of cash remaining at current burn rate.

    Only relevant for unprofitable companies (EPS <= 0).
    Profitable companies get 80 (good but not max — cash still matters).

    runway > 10y → 100 (no concern)
    5-10y → 80
    3-5y  → 60
    2-3y  → 40
    1-2y  → 20
    < 1y  → 0 (imminent dilution or death)

    Returns 50 (neutral) when data is missing.
    """
    # Profitable companies don't need cash runway analysis
    if eps is not None and eps > 0:
        return 80

    if total_cash is None or total_cash <= 0:
        return 50  # No data
    if free_cash_flow is None:
        return 50  # No data

    # Positive FCF = generating cash, no runway concern
    if free_cash_flow >= 0:
        return 90

    # Burning cash — compute years of runway
    burn_rate = abs(free_cash_flow)
    if burn_rate == 0:
        return 50
    runway_years = total_cash / burn_rate

    if runway_years > 10:
        return 100
    elif runway_years > 5:
        return 80
    elif runway_years > 3:
        return 60
    elif runway_years > 2:
        return 40
    elif runway_years > 1:
        return 20
    else:
        return 0


# =========================================================================
# RISK PENALTY FUNCTIONS — reduce score for fragile/risky stocks
# =========================================================================

def penalty_fragility(fragility):
    """Penalty based on thesis fragility (manual tag).
    none = 0, political/macro = -5, binary = -10."""
    penalties = {
        "none": 0,
        "political": -5,
        "macro": -5,
        "binary": -10,
    }
    return penalties.get(fragility, 0)


def penalty_downside(downside_if_fail):
    """Penalty based on downside if thesis fails (manual tag).
    low = 0, moderate = -5, severe = -8, zero = -12."""
    penalties = {
        "low": 0,
        "moderate": -5,
        "severe": -8,
        "zero": -12,
    }
    return penalties.get(downside_if_fail, 0)


def bonus_profitability(eps, free_cash_flow, market_cap):
    """Bonus/penalty based on profitability and cash position.
    Profitable = +5, breakeven = 0, burning cash = -5.
    Auto-fetched from Yahoo Finance (Option B)."""
    if eps and eps > 0:
        return 5  # profitable
    if free_cash_flow and market_cap:
        # Cash burn rate: if FCF is negative, how many years of runway?
        if free_cash_flow < 0:
            burn_years = abs(market_cap / free_cash_flow) if free_cash_flow != 0 else 99
            if burn_years < 2:
                return -8  # less than 2 years runway = danger
            elif burn_years < 5:
                return -3  # tight but manageable
    if eps and eps < 0:
        return -5  # unprofitable
    return 0  # unknown / breakeven


def penalty_dilution(shares_growth_pct):
    """Penalty for share dilution. >10% YoY dilution = -5, >20% = -8."""
    if not shares_growth_pct:
        return 0
    if shares_growth_pct > 20:
        return -8
    elif shares_growth_pct > 10:
        return -5
    elif shares_growth_pct > 5:
        return -2
    return 0


# =========================================================================
# DATA FETCHING
# =========================================================================

def fetch_stock_data(ticker):
    """Fetch all data needed for ranking from Yahoo Finance."""
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}

        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        target = info.get("targetMeanPrice")
        rec = info.get("recommendationKey", "hold")
        num_analysts = info.get("numberOfAnalystOpinions", 0)
        high_52w = info.get("fiftyTwoWeekHigh")
        low_52w = info.get("fiftyTwoWeekLow")
        market_cap = info.get("marketCap", 0)

        # Revenue growth — try info first, fallback to quarterly financials
        total_revenue = info.get("totalRevenue", 0)
        rev_growth = info.get("revenueGrowth")  # YoY as decimal (0.25 = 25%)

        # Fallback: compute YoY from quarterly income statement
        if rev_growth is None:
            try:
                qf = t.quarterly_income_stmt
                if qf is not None and "Total Revenue" in qf.index and len(qf.columns) >= 5:
                    # Sum last 4 quarters (TTM) vs prior 4 quarters
                    recent_4 = qf.loc["Total Revenue"].iloc[:4].sum()
                    prior_4 = qf.loc["Total Revenue"].iloc[4:8].sum()
                    if prior_4 and prior_4 > 0 and recent_4 and recent_4 > 0:
                        rev_growth = (recent_4 - prior_4) / prior_4
                        if not total_revenue:
                            total_revenue = recent_4
            except Exception:
                pass

        # Profitability data
        eps = info.get("trailingEps")
        free_cash_flow = info.get("freeCashflow")

        # Valuation
        ps_ratio = info.get("priceToSalesTrailing12Months")

        # Cash position (for runway calculation)
        total_cash = info.get("totalCash")

        # SMA + 2y high from history
        hist = t.history(period="2y")
        close = hist["Close"].dropna() if not hist.empty else None
        sma_50 = None
        sma_200 = None
        high_2y = None
        history_years = None
        if close is not None and len(close) > 0:
            if len(close) >= 50:
                sma_50 = close.rolling(50).mean().iloc[-1]
            if len(close) >= 200:
                sma_200 = close.rolling(200).mean().iloc[-1]
            high_2y = float(close.max())
            # Estimate years of history from trading days (~252/year)
            history_years = len(close) / 252.0

        return {
            "price": price,
            "target": target,
            "recommendation": rec,
            "num_analysts": num_analysts,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "market_cap": market_cap,
            "total_revenue": total_revenue,
            "rev_growth_pct": (rev_growth * 100) if rev_growth is not None else None,
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
# COMPOSITE SCORE
# =========================================================================

# Weights — adjust these to change ranking priorities
# Positive factors sum to 1.0, penalties are subtracted after
WEIGHTS = {
    "upside":      0.15,
    "growth":      0.20,
    "valuation":   0.15,   # P/S ratio — lower = cheaper
    "long_term":   0.10,   # price vs 2y high — structural health
    "cash_runway": 0.10,   # years of cash left — survival risk
    "conviction":  0.10,
    "entry":       0.10,
    "momentum":    0.10,
    # Risk adjustments (applied as penalties/bonuses to final score)
    "profitability_bonus": 5,    # +5 if profitable, -5 if not, -8 if burning cash
    "fragility_penalty": 10,     # max -10 for binary thesis
    "downside_penalty": 12,      # max -12 for goes-to-zero risk
}

def compute_composite(data, meta):
    """Compute composite score (0-100) from fetched data + manual risk tags.

    Score = weighted_positive_factors + profitability_bonus
            - fragility_penalty - downside_penalty
    Clamped to 0-100.
    """
    if data.get("error"):
        return 0, {}

    price = data["price"]

    # --- Positive factors (0-100 each, weighted to sum to 100) ---
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
        s_upside * WEIGHTS["upside"]
        + s_growth * WEIGHTS["growth"]
        + s_valuation * WEIGHTS["valuation"]
        + s_long_term * WEIGHTS["long_term"]
        + s_cash * WEIGHTS["cash_runway"]
        + s_conviction * WEIGHTS["conviction"]
        + s_entry * WEIGHTS["entry"]
        + s_momentum * WEIGHTS["momentum"]
    )

    # --- Risk adjustments (penalties/bonuses) ---
    p_fragility = penalty_fragility(meta.get("fragility", "none"))
    p_downside = penalty_downside(meta.get("downside_if_fail", "low"))
    b_profit = bonus_profitability(
        data.get("eps"), data.get("free_cash_flow"), data.get("market_cap")
    )

    # Final score
    composite = base_score + b_profit + p_fragility + p_downside

    # Clamp to 0-100
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


# =========================================================================
# MAIN: BUILD RANKING TABLE
# =========================================================================

def build_ranking():
    """Fetch data and rank all stocks in RANKING_UNIVERSE.

    Returns list of dicts sorted by composite score (descending).
    """
    results = []

    for ticker, meta in RANKING_UNIVERSE.items():
        if ticker in SKIP_TICKERS:
            continue

        data = fetch_stock_data(ticker)

        if data.get("error"):
            print(f"  ⚠️ {ticker}: {data['error']}")
            results.append({
                "ticker": ticker,
                "name": meta["name"],
                "basket": meta["basket"],
                "strategy": meta["strategy"],
                "what": meta["what"],
                "price": 0,
                "target": 0,
                "upside_pct": 0,
                "rev_growth_pct": None,
                "ps_ratio": None,
                "cash_runway_years": None,
                "pct_of_2y_high": None,
                "recommendation": "—",
                "num_analysts": 0,
                "market_cap_b": 0,
                "high_52w": 0,
                "low_52w": 0,
                "composite": 0,
                "breakdown": {},
                "error": data["error"],
            })
            continue

        composite, breakdown = compute_composite(data, meta)

        upside_pct = 0
        if data["price"] and data["target"]:
            upside_pct = ((data["target"] - data["price"]) / data["price"]) * 100

        # Compute derived display fields
        ps = data.get("ps_ratio")
        cash = data.get("total_cash")
        fcf = data.get("free_cash_flow")
        h2y = data.get("high_2y")
        cash_runway_y = None
        if cash and fcf and fcf < 0:
            cash_runway_y = round(cash / abs(fcf), 1)
        elif data.get("eps") and data["eps"] > 0:
            cash_runway_y = 99.0  # profitable, no burn
        pct_2y = round((data["price"] / h2y) * 100, 0) if h2y and h2y > 0 else None

        results.append({
            "ticker": ticker,
            "name": meta["name"],
            "basket": meta["basket"],
            "strategy": meta["strategy"],
            "what": meta["what"],
            "fragility": meta.get("fragility", "none"),
            "downside_if_fail": meta.get("downside_if_fail", "low"),
            "price": round(data["price"], 2),
            "target": round(data["target"], 2) if data["target"] else 0,
            "upside_pct": round(upside_pct, 1),
            "rev_growth_pct": round(data["rev_growth_pct"], 1) if data["rev_growth_pct"] is not None else None,
            "ps_ratio": round(ps, 1) if ps else None,
            "cash_runway_years": cash_runway_y,
            "pct_of_2y_high": pct_2y,
            "eps": data.get("eps"),
            "recommendation": data["recommendation"],
            "num_analysts": data["num_analysts"],
            "market_cap_b": round(data["market_cap"] / 1e9, 1) if data["market_cap"] else 0,
            "high_52w": data["high_52w"] or 0,
            "low_52w": data["low_52w"] or 0,
            "composite": composite,
            "breakdown": breakdown,
            "error": None,
        })

    # Sort by composite score descending
    results.sort(key=lambda x: x["composite"], reverse=True)

    # Add rank
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results
