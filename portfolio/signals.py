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
#   accumulate    — buy dips, sell at sell_target
#   catalyst      — binary event, sell on outcome
#   swing         — speculative momentum, sell on exhaustion
#
# buy_target is NOT hardcoded — it's computed dynamically from live
# technical data (200-SMA, 50-SMA, support levels) each time you run.
#
# sell_target: take-profit price (based on analyst consensus Jun 2026)

ASSET_META = {
    # --- ETFs (hold forever, DCA monthly) ---
    "XAIX.DE": {
        "name": "Xtrackers AI & Big Data",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Secular AI/data growth — DCA monthly, never sell",
    },
    "SMH": {
        "name": "VanEck Semiconductor",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Secular semi demand (AI, auto, IoT) — DCA monthly, never sell",
    },
    "IUIT.L": {
        "name": "iShares S&P 500 Info Tech",
        "basket": "Core ETF",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Mega-cap tech compounding — DCA monthly, never sell",
    },

    # --- Nuclear ---
    "CCJ": {
        "name": "Cameco",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "sell_target": 135.0,
        "sell_date": "2027-2028",
        "catalyst": "Uranium supply deficit, utility contract cycle 2026-2030",
    },
    "GEV": {
        "name": "GE Vernova",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "sell_target": 1200.0,
        "sell_date": "2028+",
        "catalyst": "Grid modernization + gas turbine + SMR deployment orders",
    },
    "SRUUF": {
        "name": "Sprott Physical Uranium",
        "basket": "Nuclear",
        "strategy": "accumulate",
        "sell_target": 38.0,
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
        "sell_target": 25.0,
        "sell_date": "2027-2029",
        "catalyst": "First SMR deployment order (TVA/RoPower)",
    },
    "OKLO": {
        "name": "Oklo Inc.",
        "basket": "Nuclear",
        "strategy": "catalyst",
        "sell_target": 90.0,
        "sell_date": "2028-2030",
        "catalyst": "NRC license approval for Aurora reactor",
    },

    # --- Quantum ---
    "IONQ": {
        "name": "IonQ",
        "basket": "Quantum",
        "strategy": "swing",
        "sell_target": 65.0,
        "sell_date": "2027-2028",
        "catalyst": "Enterprise quantum revenue inflection, gov contracts",
    },
    "QNT": {
        "name": "Quantinuum",
        "basket": "Quantum",
        "strategy": "catalyst",
        "sell_target": 80.0,
        "sell_date": "2027-2028",
        "catalyst": "Post-IPO re-rating, error correction milestones",
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
        "sell_target": 22.0,
        "sell_date": "2027",
        "catalyst": "QPU chip scaling milestones, Ankaa-3",
    },
    "QUBT": {
        "name": "Quantum Computing Inc.",
        "basket": "Quantum (paused)",
        "strategy": "swing",
        "sell_target": 14.0,
        "sell_date": "2027",
        "catalyst": "Thin-film lithium niobate photonics orders",
    },

    # --- Cyber ---
    "CRWD": {
        "name": "CrowdStrike",
        "basket": "Cyber",
        "strategy": "accumulate",
        "sell_target": 520.0,
        "sell_date": "2028+",
        "catalyst": "Platform consolidation, $10B ARR trajectory",
    },
    "PANW": {
        "name": "Palo Alto Networks",
        "basket": "Cyber",
        "strategy": "accumulate",
        "sell_target": 310.0,
        "sell_date": "2028+",
        "catalyst": "Platformization, NGS ARR growth",
    },

    # --- Industrial ---
    "BWXT": {
        "name": "BWX Technologies",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 260.0,
        "sell_date": "2028-2030",
        "catalyst": "Navy nuclear monopoly + SMR fuel + backlog +77% YoY",
    },
    "POWL": {
        "name": "Powell Industries",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 380.0,
        "sell_date": "2027-2028",
        "catalyst": "Data center electrical switchgear backlog peak",
    },
    "VRT": {
        "name": "Vertiv Holdings",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 420.0,
        "sell_date": "2027-2028",
        "catalyst": "Data center power/cooling, revenue +36% YoY, EPS +55%",
    },
    "FIX": {
        "name": "Comfort Systems USA",
        "basket": "Industrial",
        "strategy": "accumulate",
        "sell_target": 2200.0,
        "sell_date": "2028+",
        "catalyst": "Data center HVAC/electrical buildout, revenue +31% YoY",
    },

    # --- Speculative Growth ---
    "RKLB": {
        "name": "Rocket Lab",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "sell_target": 150.0,
        "sell_date": "2027-2028",
        "catalyst": "Neutron rocket first launch + constellation contracts",
    },
    "LSCC": {
        "name": "Lattice Semiconductor",
        "basket": "SpecGrowth",
        "strategy": "accumulate",
        "sell_target": 175.0,
        "sell_date": "2027-2028",
        "catalyst": "Edge AI FPGA design win cycle, revenue +44% YoY recovery",
    },
    "CRDO": {
        "name": "Credo Technology",
        "basket": "SpecGrowth",
        "strategy": "accumulate",
        "sell_target": 300.0,
        "sell_date": "2027-2028",
        "catalyst": "AI data center connectivity, revenue +82% YoY forecast",
    },
    "VKTX": {
        "name": "Viking Therapeutics",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "sell_target": 95.0,
        "sell_date": "H1 2027",
        "catalyst": "Phase III VK2735 obesity data readout — binary event",
    },
}


# =========================================================================
# TECHNICAL SIGNAL ENGINE
# =========================================================================

def compute_signals(ticker):
    """Compute technical signals for a single ticker.

    Returns price, SMAs, RSI, 52w range, trend, and a dynamic buy_target.
    """
    try:
        data = yf.Ticker(ticker).history(period="1y")
        if data.empty or len(data) < 20:
            return None

        close = data['Close']
        price = float(close.iloc[-1])

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

        # Dynamic buy target
        buy_target = compute_buy_target(price, sma_50, sma_200, low_52w, trend, len(close))

        return {
            "price": price,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "rsi": rsi,
            "pct_from_high": pct_from_high,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "trend": trend,
            "buy_target": buy_target,
        }
    except Exception as e:
        print(f"  ⚠️ {ticker}: {e}")
        return None


def compute_buy_target(price, sma_50, sma_200, low_52w, trend, data_len):
    """Compute a dynamic buy target from live technical data.

    Logic:
    - UPTREND:  buy near the 50-SMA (short-term support in a rising market)
    - NEUTRAL:  buy near the 200-SMA (major support level)
    - DOWNTREND: buy near the 52w low + 10% buffer (wait for bottom)
    - If not enough data for SMA-200, use SMA-50 or 52w low

    The target is always floored at the 52w low (never below where it
    actually traded) and capped at 95% of current price (always a discount).
    """
    # Pick the primary support level based on trend
    if trend == "UPTREND":
        # In uptrend, the 50-SMA acts as dynamic support
        primary = sma_50
    elif trend == "NEUTRAL":
        # In neutral, the 200-SMA is the key level
        if data_len >= 200:
            primary = sma_200
        else:
            primary = sma_50
    else:
        # In downtrend, target near 52w low with a 10% buffer above it
        primary = low_52w * 1.10

    # Secondary: midpoint between 52w low and 200-SMA (a "value zone")
    if data_len >= 200:
        value_zone = (low_52w + sma_200) / 2
    else:
        value_zone = (low_52w + sma_50) / 2

    # Take the higher of primary and value_zone (don't set unrealistically low)
    target = max(primary, value_zone)

    # Floor: never below 52w low (it actually traded there)
    target = max(target, low_52w)

    # Cap: always at least a 5% discount from current price
    target = min(target, price * 0.95)

    return round(target, 2)


def evaluate_buy(price, meta, signals):
    """Determine buy signal using dynamic buy_target + technicals."""
    strategy = meta["strategy"]
    buy_target = signals.get("buy_target")
    rsi = signals["rsi"]
    trend = signals["trend"]
    pct_from_high = signals["pct_from_high"]

    if strategy == "hold_forever":
        return "DCA", "Buy monthly regardless of price"

    if buy_target is None:
        return "NO TARGET", "—"

    pct_above_target = ((price - buy_target) / buy_target) * 100

    # At or below the computed buy zone
    if price <= buy_target:
        return "BUY NOW", f"At/below support ${buy_target:,.0f}"
    if pct_above_target < 5:
        return "BUY NOW", f"Near support ${buy_target:,.0f} ({pct_above_target:+.0f}%)"

    # Oversold override — buy regardless of target
    if rsi < 30:
        return "BUY NOW", f"Oversold RSI {rsi:.0f}"

    # RSI pullback in uptrend
    if rsi < 40 and trend == "UPTREND":
        return "BUY DIP", f"RSI pullback ({rsi:.0f}) in uptrend"

    # Big drawdown from highs
    if pct_from_high < -20:
        return "BUY DIP", f"{pct_from_high:.0f}% off highs — scale in"

    # Overbought — wait
    if rsi > 70:
        return "WAIT", f"Overbought RSI {rsi:.0f} — wait for ${buy_target:,.0f}"

    # Far above support
    if pct_above_target > 20:
        return "WAIT", f"{pct_above_target:.0f}% above support ${buy_target:,.0f}"

    return "BUY DIP", f"Scale in toward ${buy_target:,.0f}"


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
        return "SELL NOW", f"At/above target ${sell_target:,.0f}!"
    if pct_to_target < 10:
        return "NEAR TARGET", f"${sell_target:,.0f} is {pct_to_target:.0f}% away — tighten stop"
    if strategy == "catalyst":
        return "SELL @ EVENT", f"Target ${sell_target:,.0f} (+{pct_to_target:.0f}%) — {sell_date}"

    return "HOLD", f"Target ${sell_target:,.0f} (+{pct_to_target:.0f}%) — sell by {sell_date}"


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
        print(f"${signals['price']:.2f}  buy@${signals['buy_target']:,.2f}")

        buy_signal, buy_reason = evaluate_buy(signals["price"], meta, signals)
        sell_action, sell_detail = evaluate_sell(signals["price"], meta)

        results.append({
            "ticker": ticker,
            "name": meta["name"],
            "basket": meta["basket"],
            "strategy": meta["strategy"],
            "price": signals["price"],
            "buy_target": signals["buy_target"],
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
