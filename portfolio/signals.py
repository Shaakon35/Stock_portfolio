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
# ASSET METADATA — strategy, buy/sell targets, catalysts
# =========================================================================
# strategy: "hold_forever" | "accumulate" | "catalyst" | "swing"
#   hold_forever  — core ETFs, DCA monthly, never sell
#   accumulate    — buy dips to buy_target, sell at sell_target
#   catalyst      — binary event, buy before event, sell on outcome
#   swing         — speculative momentum, sell on exhaustion
#
# buy_target:  ideal entry price (buy at or below this)
# sell_target: take-profit price (sell at or above this)
# Both are based on analyst consensus, technicals, and fundamentals
# as of June 2026.

ASSET_META = {
    # --- ETFs (hold forever, DCA monthly) ---
    "XAIX.DE": {
        "name": "Xtrackers AI & Big Data",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "buy_target": None,       # DCA any price
        "sell_target": None,      # Never sell
        "sell_date": None,
        "catalyst": "Secular AI/data growth — DCA monthly, never sell",
    },
    "SMH": {
        "name": "VanEck Semiconductor",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "buy_target": None,
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Secular semi demand (AI, auto, IoT) — DCA monthly, never sell",
    },
    "IUIT.L": {
        "name": "iShares S&P 500 Info Tech",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "buy_target": None,
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Mega-cap tech compounding — DCA monthly, never sell",
    },

    # --- Nuclear (prices as of Jun 2026) ---
    # CCJ: ~$103, analyst target $129, 52w $59-$135
    "CCJ": {
        "name": "Cameco",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "buy_target": 90.0,
        "sell_target": 135.0,
        "sell_date": "2027-2028",
        "catalyst": "Uranium supply deficit, utility contract cycle 2026-2030",
    },
    # GEV: ~$934, analyst target $1216, 52w $459-$1182
    "GEV": {
        "name": "GE Vernova",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "buy_target": 850.0,
        "sell_target": 1200.0,
        "sell_date": "2028+",
        "catalyst": "Grid modernization + gas turbine + SMR deployment orders",
    },
    # SRUUF: ~$25, tracks uranium spot
    "SRUUF": {
        "name": "Sprott Physical Uranium",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "buy_target": 22.0,
        "sell_target": 38.0,
        "sell_date": "2027-2028",
        "catalyst": "Uranium spot price breakout above $120/lb",
    },
    # LEU: ~$100, analyst targets $120-$150
    "LEU": {
        "name": "Centrus Energy",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "buy_target": 85.0,
        "sell_target": 150.0,
        "sell_date": "2027-2028",
        "catalyst": "HALEU production ramp, DOE contracts",
    },
    # SMR: ~$11, BofA target $12, pre-revenue
    "SMR": {
        "name": "NuScale Power",
        "basket": "Nuclear",
        "strategy": "catalyst",
        "buy_target": 9.0,
        "sell_target": 25.0,
        "sell_date": "2027-2029",
        "catalyst": "First SMR deployment order (TVA/RoPower)",
    },
    # OKLO: ~$55, pre-revenue, NRC license pending
    "OKLO": {
        "name": "Oklo Inc.",
        "basket": "Nuclear",
        "strategy": "catalyst",
        "buy_target": 40.0,
        "sell_target": 90.0,
        "sell_date": "2028-2030",
        "catalyst": "NRC license approval for Aurora reactor",
    },

    # --- Quantum ---
    # IONQ: ~$45, revenue +755% YoY, RPO $470M
    "IONQ": {
        "name": "IonQ",
        "basket": "Quantum",
        "strategy": "swing",
        "buy_target": 35.0,
        "sell_target": 65.0,
        "sell_date": "2027-2028",
        "catalyst": "Enterprise quantum revenue inflection, gov contracts",
    },
    # QNT: ~$47, Honeywell-backed
    "QNT": {
        "name": "Quantinuum",
        "basket": "Quantum",
        "strategy": "catalyst",
        "buy_target": 38.0,
        "sell_target": 80.0,
        "sell_date": "2027-2028",
        "catalyst": "Post-IPO re-rating, error correction milestones",
    },
    # QBTS: ~$8, speculative
    "QBTS": {
        "name": "D-Wave Quantum",
        "basket": "Quantum",
        "strategy": "swing",
        "buy_target": 6.0,
        "sell_target": 15.0,
        "sell_date": "2027",
        "catalyst": "Annealing quantum advantage proof + revenue growth",
    },
    # RGTI: ~$15, speculative
    "RGTI": {
        "name": "Rigetti Computing",
        "basket": "Quantum",
        "strategy": "swing",
        "buy_target": 10.0,
        "sell_target": 22.0,
        "sell_date": "2027",
        "catalyst": "QPU chip scaling milestones, Ankaa-3",
    },
    # QUBT: ~$7, paused at 0% allocation
    "QUBT": {
        "name": "Quantum Computing Inc.",
        "basket": "Quantum (paused)",
        "strategy": "swing",
        "buy_target": 5.0,
        "sell_target": 14.0,
        "sell_date": "2027",
        "catalyst": "Thin-film lithium niobate photonics orders",
    },

    # --- Cyber ---
    # CRWD: ~$430, analyst targets $400-$500+
    "CRWD": {
        "name": "CrowdStrike",
        "basket": "Cyber",
        "strategy": "accumulate",
        "buy_target": 380.0,
        "sell_target": 520.0,
        "sell_date": "2028+",
        "catalyst": "Platform consolidation, $10B ARR trajectory",
    },
    # PANW: ~$257, analyst targets $250-$300
    "PANW": {
        "name": "Palo Alto Networks",
        "basket": "Cyber",
        "strategy": "accumulate",
        "buy_target": 230.0,
        "sell_target": 310.0,
        "sell_date": "2028+",
        "catalyst": "Platformization, NGS ARR growth",
    },

    # --- Industrial ---
    # BWXT: $186, analyst target $238, backlog +77% YoY
    "BWXT": {
        "name": "BWX Technologies",
        "basket": "Industrial",
        "strategy": "accumulate",
        "buy_target": 170.0,
        "sell_target": 260.0,
        "sell_date": "2028-2030",
        "catalyst": "Navy nuclear monopoly + SMR fuel + backlog +77% YoY",
    },
    # POWL: $285, analyst target $316
    "POWL": {
        "name": "Powell Industries",
        "basket": "Industrial",
        "strategy": "accumulate",
        "buy_target": 250.0,
        "sell_target": 380.0,
        "sell_date": "2027-2028",
        "catalyst": "Data center electrical switchgear backlog peak",
    },
    # VRT: $301, analyst target $377, revenue +36% YoY
    "VRT": {
        "name": "Vertiv Holdings",
        "basket": "Industrial",
        "strategy": "accumulate",
        "buy_target": 270.0,
        "sell_target": 420.0,
        "sell_date": "2027-2028",
        "catalyst": "Data center power/cooling, revenue +36% YoY, EPS +55%",
    },
    # FIX: $1844, analyst target $2026, revenue +31% YoY
    "FIX": {
        "name": "Comfort Systems USA",
        "basket": "Industrial",
        "strategy": "accumulate",
        "buy_target": 1700.0,
        "sell_target": 2200.0,
        "sell_date": "2028+",
        "catalyst": "Data center HVAC/electrical buildout, revenue +31% YoY",
    },

    # --- Speculative Growth ---
    # RKLB: $110, analyst target $105 (lagging), 52w high ~$150
    "RKLB": {
        "name": "Rocket Lab",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "buy_target": 85.0,
        "sell_target": 150.0,
        "sell_date": "2027-2028",
        "catalyst": "Neutron rocket first launch + constellation contracts",
    },
    # LSCC: $136, analyst target $147, recovery cycle
    "LSCC": {
        "name": "Lattice Semiconductor",
        "basket": "SpecGrowth",
        "strategy": "accumulate",
        "buy_target": 115.0,
        "sell_target": 175.0,
        "sell_date": "2027-2028",
        "catalyst": "Edge AI FPGA design win cycle, revenue +44% YoY recovery",
    },
    # CRDO: $207, analyst target $256, revenue +206% YoY
    "CRDO": {
        "name": "Credo Technology",
        "basket": "SpecGrowth",
        "strategy": "accumulate",
        "buy_target": 180.0,
        "sell_target": 300.0,
        "sell_date": "2027-2028",
        "catalyst": "AI data center connectivity, revenue +82% YoY forecast",
    },
    # VKTX: $28, analyst target $93, Phase III H1 2027
    "VKTX": {
        "name": "Viking Therapeutics",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "buy_target": 24.0,
        "sell_target": 95.0,
        "sell_date": "H1 2027",
        "catalyst": "Phase III VK2735 obesity data readout — binary event",
    },
}


# =========================================================================
# TECHNICAL SIGNAL ENGINE
# =========================================================================

def compute_signals(ticker):
    """Compute technical signals for a single ticker."""
    try:
        data = yf.Ticker(ticker).history(period="1y")
        if data.empty or len(data) < 20:
            return None

        close = data['Close']
        price = float(close.iloc[-1])

        sma_50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else price
        sma_200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else price

        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain.iloc[-1] / loss.iloc[-1] if loss.iloc[-1] != 0 else 100
        rsi = 100 - (100 / (1 + rs))

        high_52w = float(close.max())
        low_52w = float(close.min())
        pct_from_high = ((price - high_52w) / high_52w) * 100

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

        return {
            "price": price,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "rsi": rsi,
            "pct_from_high": pct_from_high,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "trend": trend,
        }
    except Exception as e:
        print(f"  ⚠️ {ticker}: {e}")
        return None


def evaluate_buy(price, meta, signals):
    """Determine buy signal using buy_target + technicals."""
    strategy = meta["strategy"]
    buy_target = meta.get("buy_target")
    rsi = signals["rsi"]
    trend = signals["trend"]
    pct_from_high = signals["pct_from_high"]

    if strategy == "hold_forever":
        return "DCA", "Buy monthly regardless of price"

    if buy_target is None:
        return "NO TARGET", "—"

    pct_above_target = ((price - buy_target) / buy_target) * 100

    if price <= buy_target:
        return "BUY NOW", f"At/below target ${buy_target:.0f}"
    if pct_above_target < 5:
        return "BUY NOW", f"Near target ${buy_target:.0f} ({pct_above_target:+.0f}%)"
    if rsi < 30:
        return "BUY NOW", f"Oversold RSI {rsi:.0f} — buy the dip"
    if rsi < 40 and trend == "UPTREND":
        return "BUY DIP", f"RSI pullback ({rsi:.0f}) in uptrend"
    if pct_from_high < -20:
        return "BUY DIP", f"{pct_from_high:.0f}% off highs — scale in"
    if rsi > 70:
        return "WAIT", f"Overbought RSI {rsi:.0f} — wait for ${buy_target:.0f}"
    if pct_above_target > 15:
        return "WAIT", f"{pct_above_target:.0f}% above target ${buy_target:.0f}"

    return "BUY DIP", f"Scale in toward ${buy_target:.0f}"


def evaluate_sell(price, meta):
    """Determine sell signal using sell_target + strategy."""
    strategy = meta["strategy"]
    sell_target = meta.get("sell_target")
    sell_date = meta.get("sell_date", "")

    if strategy == "hold_forever":
        return "HOLD FOREVER", "Never sell — DCA only"

    if sell_target is None:
        return "NO TARGET", "—"

    pct_to_target = ((sell_target - price) / price) * 100

    if price >= sell_target:
        return "SELL NOW", f"At/above target ${sell_target:.0f}!"
    if pct_to_target < 10:
        return "NEAR TARGET", f"${sell_target:.0f} is {pct_to_target:.0f}% away — tighten stop"
    if strategy == "catalyst":
        return "SELL @ EVENT", f"Target ${sell_target:.0f} (+{pct_to_target:.0f}%) — {sell_date}"

    return "HOLD", f"Target ${sell_target:.0f} (+{pct_to_target:.0f}%) — sell by {sell_date}"


# =========================================================================
# MAIN: BUILD SIGNAL TABLE
# =========================================================================

def build_signal_table():
    """Fetch signals for all portfolio assets and return structured data."""
    print("Fetching signals for all portfolio assets...")

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

        buy_signal, buy_reason = evaluate_buy(signals["price"], meta, signals)
        sell_action, sell_detail = evaluate_sell(signals["price"], meta)

        results.append({
            "ticker": ticker,
            "name": meta["name"],
            "basket": meta["basket"],
            "strategy": meta["strategy"],
            "price": signals["price"],
            "buy_target": meta.get("buy_target"),
            "sell_target": meta.get("sell_target"),
            "rsi": signals["rsi"],
            "trend": signals["trend"],
            "pct_from_high": signals["pct_from_high"],
            "buy_signal": buy_signal,
            "buy_reason": buy_reason,
            "sell_action": sell_action,
            "sell_detail": sell_detail,
            "sell_date": meta.get("sell_date", ""),
            "catalyst": meta.get("catalyst", ""),
            "shares": my_current_shares.get(ticker, 0),
        })

    print(f"\nDone — {len(results)} assets analyzed.")
    return results
