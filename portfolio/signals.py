import yfinance as yf
import numpy as np
from datetime import datetime

from portfolio.allocations import (
    TARGET_WEIGHTS,
    NUCLEAR_BASKET_TARGETS, QUANTUM_BASKET_TARGETS, CYBER_BASKET_TARGETS,
    INDUSTRIAL_BASKET_TARGETS, SPECGROWTH_BASKET_TARGETS,
    my_current_shares,
)


# =========================================================================
# ASSET METADATA — strategy, sell targets, catalysts
# =========================================================================
# strategy: "hold_forever" | "accumulate" | "catalyst" | "swing"
#   hold_forever  — core ETFs, DCA monthly, never sell
#   accumulate    — buy dips, sell at price target or when thesis breaks
#   catalyst      — binary event (FDA, contract, earnings), sell on event
#   swing         — speculative, sell on momentum exhaustion

ASSET_META = {
    # --- ETFs (hold forever, DCA) ---
    "XAIX.DE": {
        "name": "Xtrackers AI & Big Data",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Secular AI/data growth — no exit planned",
    },
    "SMH": {
        "name": "VanEck Semiconductor",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Secular semi demand (AI, auto, IoT) — no exit planned",
    },
    "IUIT.L": {
        "name": "iShares S&P 500 Info Tech",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Mega-cap tech compounding — no exit planned",
    },

    # --- Nuclear ---
    "CCJ": {
        "name": "Cameco",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "sell_target": 85.0,
        "sell_date": "2028+",
        "catalyst": "Uranium supply deficit, utility contract cycle 2026-2030",
    },
    "GEV": {
        "name": "GE Vernova",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "sell_target": 550.0,
        "sell_date": "2028+",
        "catalyst": "Grid modernization + SMR deployment orders",
    },
    "SRUUF": {
        "name": "Sprott Physical Uranium",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "sell_target": 35.0,
        "sell_date": "2027-2028",
        "catalyst": "Uranium spot price breakout above $120/lb",
    },
    "LEU": {
        "name": "Centrus Energy",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "sell_target": 150.0,
        "sell_date": "2027-2028",
        "catalyst": "HALEU production ramp, DOE contracts",
    },
    "SMR": {
        "name": "NuScale Power",
        "basket": "Nuclear",
        "strategy": "catalyst",
        "sell_target": 40.0,
        "sell_date": "2027-2029",
        "catalyst": "First SMR deployment order confirmation",
    },
    "OKLO": {
        "name": "Oklo Inc.",
        "basket": "Nuclear",
        "strategy": "catalyst",
        "sell_target": 60.0,
        "sell_date": "2028-2030",
        "catalyst": "NRC license approval for Aurora reactor",
    },

    # --- Quantum ---
    "IONQ": {
        "name": "IonQ",
        "basket": "Quantum",
        "strategy": "swing",
        "sell_target": 55.0,
        "sell_date": "2027-2028",
        "catalyst": "Enterprise quantum revenue inflection, gov contracts",
    },
    "QNT": {
        "name": "Quantinuum",
        "basket": "Quantum",
        "strategy": "catalyst",
        "sell_target": 80.0,
        "sell_date": "2027-2028",
        "catalyst": "Post-IPO re-rating, Honeywell backing",
    },
    "QBTS": {
        "name": "D-Wave Quantum",
        "basket": "Quantum",
        "strategy": "swing",
        "sell_target": 15.0,
        "sell_date": "2027",
        "catalyst": "Annealing quantum advantage proof + revenue growth",
    },
    "RGTI": {
        "name": "Rigetti Computing",
        "basket": "Quantum",
        "strategy": "swing",
        "sell_target": 18.0,
        "sell_date": "2027",
        "catalyst": "QPU chip scaling milestones",
    },
    "QUBT": {
        "name": "Quantum Computing Inc.",
        "basket": "Quantum (paused)",
        "strategy": "swing",
        "sell_target": 12.0,
        "sell_date": "2027",
        "catalyst": "Thin-film lithium niobate photonics orders",
    },

    # --- Cyber ---
    "CRWD": {
        "name": "CrowdStrike",
        "basket": "Cyber",
        "strategy": "accumulate",
        "sell_target": 500.0,
        "sell_date": "2028+",
        "catalyst": "Platform consolidation, $10B ARR trajectory",
    },
    "PANW": {
        "name": "Palo Alto Networks",
        "basket": "Cyber",
        "strategy": "accumulate",
        "sell_target": 280.0,
        "sell_date": "2028+",
        "catalyst": "Platformization, NGS ARR growth",
    },

    # --- Industrial ---
    "BWXT": {
        "name": "BWX Technologies",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 160.0,
        "sell_date": "2028-2030",
        "catalyst": "Navy nuclear monopoly + SMR fuel contracts",
    },
    "POWL": {
        "name": "Powell Industries",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 400.0,
        "sell_date": "2027-2028",
        "catalyst": "Data center electrical switchgear backlog peak",
    },
    "VRT": {
        "name": "Vertiv Holdings",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 160.0,
        "sell_date": "2027-2028",
        "catalyst": "Data center power/cooling capex cycle",
    },
    "FIX": {
        "name": "Comfort Systems USA",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 550.0,
        "sell_date": "2028+",
        "catalyst": "Data center HVAC/electrical buildout wave",
    },

    # --- Speculative Growth ---
    "RKLB": {
        "name": "Rocket Lab",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "sell_target": 40.0,
        "sell_date": "2027-2028",
        "catalyst": "Neutron rocket first launch + constellation contracts",
    },
    "LSCC": {
        "name": "Lattice Semiconductor",
        "basket": "SpecGrowth",
        "strategy": "accumulate",
        "sell_target": 80.0,
        "sell_date": "2027-2028",
        "catalyst": "Edge AI FPGA design win cycle recovery",
    },
    "CRDO": {
        "name": "Credo Technology",
        "basket": "SpecGrowth",
        "strategy": "accumulate",
        "sell_target": 90.0,
        "sell_date": "2027",
        "catalyst": "AI data center connectivity revenue 60%+ YoY growth",
    },
    "VKTX": {
        "name": "Viking Therapeutics",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "sell_target": 95.0,
        "sell_date": "H1 2027",
        "catalyst": "Phase III VK2735 obesity data readout",
    },
}


# =========================================================================
# TECHNICAL SIGNAL ENGINE
# =========================================================================

def compute_signals(ticker):
    """Compute buy/sell technical signals for a single ticker.

    Returns dict with:
      price, sma_50, sma_200, rsi_14, pct_from_52w_high, pct_from_52w_low,
      trend, buy_signal, buy_reason
    """
    try:
        data = yf.Ticker(ticker).history(period="1y")
        if data.empty or len(data) < 20:
            return None

        close = data['Close']
        price = float(close.iloc[-1])

        # Moving averages
        sma_50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else price
        sma_200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else price

        # RSI-14
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain.iloc[-1] / loss.iloc[-1] if loss.iloc[-1] != 0 else 100
        rsi = 100 - (100 / (1 + rs))

        # 52-week range
        high_52w = float(close.max())
        low_52w = float(close.min())
        pct_from_high = ((price - high_52w) / high_52w) * 100
        pct_from_low = ((price - low_52w) / low_52w) * 100

        # Trend classification
        if len(close) >= 200:
            if price > sma_200 and sma_50 > sma_200:
                trend = "UPTREND"
            elif price < sma_200 and sma_50 < sma_200:
                trend = "DOWNTREND"
            else:
                trend = "NEUTRAL"
        elif len(close) >= 50:
            trend = "UPTREND" if price > sma_50 else "NEUTRAL"
        else:
            trend = "N/A"

        # Buy signal logic
        buy_signal, buy_reason = _evaluate_buy(price, sma_50, sma_200, rsi, pct_from_high, trend)

        return {
            "price": price,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "rsi": rsi,
            "pct_from_high": pct_from_high,
            "pct_from_low": pct_from_low,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "trend": trend,
            "buy_signal": buy_signal,
            "buy_reason": buy_reason,
        }
    except Exception as e:
        print(f"  ⚠️ {ticker}: {e}")
        return None


def _evaluate_buy(price, sma_50, sma_200, rsi, pct_from_high, trend):
    """Determine buy timing signal based on technicals."""
    # Strong buy: oversold + near support
    if rsi < 30 and pct_from_high < -25:
        return "BUY NOW", "Oversold (RSI<30) + >25% off highs"
    if rsi < 35 and trend == "UPTREND":
        return "BUY NOW", f"RSI pullback in uptrend ({rsi:.0f})"
    # Good entry: price near SMA-200 support in uptrend
    if trend == "UPTREND" and abs(price - sma_200) / sma_200 < 0.03:
        return "BUY NOW", "Testing 200-SMA support in uptrend"
    # Decent entry: moderate pullback
    if pct_from_high < -15 and trend != "DOWNTREND":
        return "BUY DIP", f"{pct_from_high:.0f}% off highs — accumulate"
    # Uptrend but extended
    if trend == "UPTREND" and rsi > 70:
        return "WAIT", f"Overbought (RSI {rsi:.0f}) — wait for pullback"
    if trend == "UPTREND" and pct_from_high > -5:
        return "WAIT", "Near 52w high — wait for 5-10% dip"
    # Uptrend, reasonable entry
    if trend == "UPTREND":
        return "BUY NOW", "Uptrend, reasonable entry"
    # Downtrend
    if trend == "DOWNTREND":
        return "WAIT", "Downtrend — wait for SMA-200 reclaim"
    # Neutral
    return "BUY DIP", "Neutral trend — scale in on weakness"


def compute_sell_signal(ticker, meta, signals):
    """Determine sell timing based on strategy + target price."""
    if meta["strategy"] == "hold_forever":
        return "HOLD FOREVER", "DCA monthly, never sell"

    price = signals["price"]
    target = meta.get("sell_target")

    if target is None:
        return "NO TARGET", "—"

    pct_to_target = ((target - price) / price) * 100

    if price >= target:
        return "SELL NOW", f"At/above target ${target:.0f}"
    if pct_to_target < 10:
        return "NEAR TARGET", f"${target:.0f} ({pct_to_target:+.0f}%) — tighten stop"
    if meta["strategy"] == "catalyst":
        return f"SELL @ EVENT", f"${target:.0f} ({pct_to_target:+.0f}%) — {meta['sell_date']}"

    return f"TARGET ${target:.0f}", f"{pct_to_target:+.0f}% upside — hold until {meta['sell_date']}"


# =========================================================================
# MAIN: BUILD SIGNAL TABLE
# =========================================================================

def build_signal_table():
    """Fetch signals for all portfolio assets and return structured data."""
    print("Fetching signals for all portfolio assets...")

    # Collect all active tickers (skip 0-allocation quantum names)
    skip_tickers = {"XNDU", "INFQ", "HQ"}
    all_tickers = [t for t in my_current_shares.keys() if t not in skip_tickers]

    results = []
    for ticker in all_tickers:
        meta = ASSET_META.get(ticker)
        if not meta:
            print(f"  ⚠️ {ticker}: no metadata, skipping")
            continue

        print(f"  {ticker}...", end=" ")
        signals = compute_signals(ticker)
        if signals is None:
            print("failed")
            continue
        print(f"${signals['price']:.2f}")

        sell_action, sell_detail = compute_sell_signal(ticker, meta, signals)

        results.append({
            "ticker": ticker,
            "name": meta["name"],
            "basket": meta["basket"],
            "strategy": meta["strategy"],
            "price": signals["price"],
            "rsi": signals["rsi"],
            "trend": signals["trend"],
            "pct_from_high": signals["pct_from_high"],
            "buy_signal": signals["buy_signal"],
            "buy_reason": signals["buy_reason"],
            "sell_action": sell_action,
            "sell_detail": sell_detail,
            "sell_target": meta.get("sell_target"),
            "catalyst": meta.get("catalyst", ""),
            "shares": my_current_shares.get(ticker, 0),
        })

    print(f"\nDone — {len(results)} assets analyzed.")
    return results
