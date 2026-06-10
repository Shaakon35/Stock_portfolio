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

        # Profitability data (auto-fetched for Option B)
        eps = info.get("trailingEps")
        free_cash_flow = info.get("freeCashflow")

        # Dilution: compare current shares to prior year
        shares_outstanding = info.get("sharesOutstanding", 0)
        # yfinance doesn't give historical shares easily, so we check
        # floatShares vs sharesOutstanding as a proxy for recent dilution
        float_shares = info.get("floatShares", 0)
        implied_lockup = 0
        if shares_outstanding and float_shares and shares_outstanding > 0:
            implied_lockup = ((shares_outstanding - float_shares) / shares_outstanding) * 100

        # SMA from history (fetch 2y for accurate 200-SMA)
        hist = t.history(period="2y")
        sma_50 = None
        sma_200 = None
        if len(hist) >= 50:
            sma_50 = hist["Close"].rolling(50).mean().iloc[-1]
        if len(hist) >= 200:
            sma_200 = hist["Close"].rolling(200).mean().iloc[-1]

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
            "shares_outstanding": shares_outstanding,
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
    "upside":     0.30,
    "growth":     0.25,
    "conviction": 0.15,
    "entry":      0.15,
    "momentum":   0.15,
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

    # --- Positive factors (0-100 each, weighted to sum ~80 max) ---
    s_upside = score_analyst_upside(price, data["target"])
    s_growth = score_revenue_quality(
        data["rev_growth_pct"], data.get("total_revenue", 0)
    )
    s_conviction = score_analyst_conviction(
        data["recommendation"], data["num_analysts"]
    )
    s_entry = score_entry_position(price, data["high_52w"], data["low_52w"])
    s_momentum = score_momentum(price, data["sma_50"], data["sma_200"])

    base_score = (
        s_upside * WEIGHTS["upside"]
        + s_growth * WEIGHTS["growth"]
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
