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
    "CCJ":   {"name": "Cameco",              "basket": "Nuclear",     "strategy": "hold_forever", "what": "Uranium mining — largest Western producer"},
    "GEV":   {"name": "GE Vernova",          "basket": "Nuclear",     "strategy": "hold_forever", "what": "Grid electrification, gas/wind turbines"},
    "SRUUF": {"name": "Sprott Uranium Trust", "basket": "Nuclear",    "strategy": "cycle",        "what": "Physical uranium trust — tracks U3O8 price"},
    "LEU":   {"name": "Centrus Energy",      "basket": "Nuclear",     "strategy": "cycle",        "what": "Uranium enrichment, HALEU fuel for SMRs"},
    "SMR":   {"name": "NuScale Power",       "basket": "Nuclear",     "strategy": "catalyst",     "what": "Small modular reactor — only NRC-approved SMR design"},
    "OKLO":  {"name": "Oklo",                "basket": "Nuclear",     "strategy": "catalyst",     "what": "Advanced fission microreactor — Sam Altman backed"},
    # --- QUANTUM ---
    "IONQ":  {"name": "IonQ",                "basket": "Quantum",     "strategy": "catalyst",     "what": "Trapped-ion quantum computing — revenue leader"},
    "QNT":   {"name": "Quantinuum",          "basket": "Quantum",     "strategy": "catalyst",     "what": "Trapped-ion quantum (Honeywell) — IPO Jun 2026"},
    "QBTS":  {"name": "D-Wave Quantum",      "basket": "Quantum",     "strategy": "catalyst",     "what": "Quantum annealing + gate-model dual platform"},
    "RGTI":  {"name": "Rigetti Computing",   "basket": "Quantum",     "strategy": "catalyst",     "what": "Superconducting quantum — modular chiplet architecture"},
    # --- CYBER ---
    "CRWD":  {"name": "CrowdStrike",         "basket": "Cyber",       "strategy": "hold_forever", "what": "Endpoint cybersecurity platform — #1 market share"},
    "PANW":  {"name": "Palo Alto Networks",  "basket": "Cyber",       "strategy": "hold_forever", "what": "Enterprise network security — AI-driven"},
    # --- INDUSTRIAL ---
    "BWXT":  {"name": "BWX Technologies",    "basket": "Industrial",  "strategy": "hold_forever", "what": "Navy nuclear reactors — sole-source monopoly"},
    "POWL":  {"name": "Powell Industries",   "basket": "Industrial",  "strategy": "cycle",        "what": "Electrical switchgear for data centers"},
    "VRT":   {"name": "Vertiv Holdings",     "basket": "Industrial",  "strategy": "cycle",        "what": "Data center cooling and power infrastructure"},
    "FIX":   {"name": "Comfort Systems USA", "basket": "Industrial",  "strategy": "hold_forever", "what": "Data center HVAC and electrical contracting"},
    # --- SPECGROWTH ---
    "RKLB":  {"name": "Rocket Lab",          "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Rockets + space systems — Neutron launch pending"},
    "LSCC":  {"name": "Lattice Semi",        "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Low-power FPGAs for edge AI and automotive"},
    "CRDO":  {"name": "Credo Technology",    "basket": "SpecGrowth",  "strategy": "cycle",        "what": "AI data center connectivity (optical + electrical)"},
    "VKTX":  {"name": "Viking Therapeutics", "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "GLP-1 obesity/NASH drug — Phase III"},
    # --- NEW CANDIDATES ---
    "KTOS":  {"name": "Kratos Defense",      "basket": "Industrial",  "strategy": "cycle",        "what": "Autonomous military drones, hypersonic systems"},
    "SERV":  {"name": "Serve Robotics",      "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Autonomous sidewalk delivery robots — Nvidia backed"},
    "ENVX":  {"name": "Enovix",              "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Silicon anode batteries — 2x energy density"},
    "APLD":  {"name": "Applied Digital",     "basket": "Industrial",  "strategy": "cycle",        "what": "AI GPU data center infrastructure"},
    "TMDX":  {"name": "TransMedics",         "basket": "MedTech",     "strategy": "hold_forever", "what": "Organ transplant logistics — monopoly OCS system"},
    "IREN":  {"name": "IREN Limited",        "basket": "Industrial",  "strategy": "cycle",        "what": "AI cloud compute + Bitcoin mining infrastructure"},
    "AXON":  {"name": "Axon Enterprise",     "basket": "Defense",     "strategy": "hold_forever", "what": "Taser + body cams + AI evidence management"},
    "CIFR":  {"name": "Cipher Digital",      "basket": "Industrial",  "strategy": "cycle",        "what": "Bitcoin mining pivoting to AI data centers"},
    "LUNR":  {"name": "Intuitive Machines",  "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Lunar landers — NASA commercial lunar partner"},
    "ACHR":  {"name": "Archer Aviation",     "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "eVTOL air taxi — FAA certification pending"},
}

# Tickers to skip (private, no data, ETFs)
SKIP_TICKERS = {"XNDU", "INFQ", "HQ", "XAIX.DE", "SMHV.SW", "QDVE.DE"}


# =========================================================================
# SCORING FUNCTIONS — each returns 0-100
# =========================================================================

def score_analyst_upside(price, target_price):
    """Score based on analyst target upside. 0% = 0, 100%+ = 100."""
    if not target_price or not price or price <= 0:
        return 0
    upside_pct = ((target_price - price) / price) * 100
    # Negative upside = 0, cap at 300% = 100
    return max(0, min(100, upside_pct * (100 / 300)))


def score_revenue_growth(current_rev, prior_rev):
    """Score based on YoY revenue growth. 0% = 0, 100%+ = 50, 500%+ = 100."""
    if not current_rev or not prior_rev or prior_rev <= 0:
        return 0
    growth_pct = ((current_rev - prior_rev) / prior_rev) * 100
    if growth_pct <= 0:
        return 0
    # Cap at 500% = 100
    return min(100, growth_pct * (100 / 500))


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

        # Revenue growth from quarterly data
        current_rev = info.get("totalRevenue", 0)
        rev_growth = info.get("revenueGrowth")  # YoY as decimal (0.25 = 25%)

        # SMA from history
        hist = t.history(period="1y")
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
            "rev_growth_pct": (rev_growth * 100) if rev_growth else 0,
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
WEIGHTS = {
    "upside":     0.30,
    "growth":     0.25,
    "conviction": 0.15,
    "entry":      0.15,
    "momentum":   0.15,
}

def compute_composite(data):
    """Compute composite score (0-100) from fetched data."""
    if data.get("error"):
        return 0, {}

    price = data["price"]
    s_upside = score_analyst_upside(price, data["target"])
    s_growth = score_revenue_growth(
        100 + data["rev_growth_pct"], 100  # normalize growth % to ratio
    ) if data["rev_growth_pct"] > 0 else 0
    s_conviction = score_analyst_conviction(
        data["recommendation"], data["num_analysts"]
    )
    s_entry = score_entry_position(price, data["high_52w"], data["low_52w"])
    s_momentum = score_momentum(price, data["sma_50"], data["sma_200"])

    composite = (
        s_upside * WEIGHTS["upside"]
        + s_growth * WEIGHTS["growth"]
        + s_conviction * WEIGHTS["conviction"]
        + s_entry * WEIGHTS["entry"]
        + s_momentum * WEIGHTS["momentum"]
    )

    breakdown = {
        "upside": round(s_upside, 1),
        "growth": round(s_growth, 1),
        "conviction": round(s_conviction, 1),
        "entry": round(s_entry, 1),
        "momentum": round(s_momentum, 1),
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

        print(f"  Fetching {ticker}...")
        data = fetch_stock_data(ticker)

        if data.get("error"):
            print(f"  ⚠️ {ticker} failed: {data['error']}")
            results.append({
                "ticker": ticker,
                "name": meta["name"],
                "basket": meta["basket"],
                "strategy": meta["strategy"],
                "what": meta["what"],
                "price": 0,
                "target": 0,
                "upside_pct": 0,
                "rev_growth_pct": 0,
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

        composite, breakdown = compute_composite(data)

        upside_pct = 0
        if data["price"] and data["target"]:
            upside_pct = ((data["target"] - data["price"]) / data["price"]) * 100

        results.append({
            "ticker": ticker,
            "name": meta["name"],
            "basket": meta["basket"],
            "strategy": meta["strategy"],
            "what": meta["what"],
            "price": round(data["price"], 2),
            "target": round(data["target"], 2) if data["target"] else 0,
            "upside_pct": round(upside_pct, 1),
            "rev_growth_pct": round(data["rev_growth_pct"], 1),
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
