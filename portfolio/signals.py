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
# strategy: "hold_forever" | "cycle" | "catalyst"
#   hold_forever  — core positions, DCA monthly, never sell
#   cycle         — buy for the cycle (1-3y), sell when growth decelerates
#   catalyst      — binary event (<18m), sell on the outcome
#
# buy_target is NOT hardcoded — it's computed dynamically from live
# technical data (200-SMA, 50-SMA, support levels) each time you run.
#
# sell_target: take-profit price (based on analyst consensus Jun 2026)

ASSET_META = {
    # =================================================================
    # LONG-TERM HOLDS (3-10+ years) — never sell unless thesis breaks
    # =================================================================
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
    # CCJ: ~$103, analyst $129. Uranium deficit lasts to 2035+
    "CCJ": {
        "name": "Cameco",
        "basket": "Nuclear",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Uranium supply deficit to 2035+, monopoly miner — never sell",
    },
    # GEV: ~$934, analyst $1216. Grid modernization is a 20-year cycle
    "GEV": {
        "name": "GE Vernova",
        "basket": "Nuclear",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Grid modernization 20-year cycle + gas turbine + SMR — never sell",
    },
    # CRWD: ~$430, analyst $520. Cybersecurity spend only grows
    "CRWD": {
        "name": "CrowdStrike",
        "basket": "Cyber",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Cybersecurity platform moat, $10B ARR trajectory — never sell",
    },
    # PANW: ~$257, analyst $310. Enterprise security duopoly
    "PANW": {
        "name": "Palo Alto Networks",
        "basket": "Cyber",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Enterprise security duopoly, platformization — never sell",
    },
    # BWXT: $186, analyst $238. Navy nuclear monopoly, decades of contracts
    "BWXT": {
        "name": "BWX Technologies",
        "basket": "Industrial",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Navy nuclear monopoly + SMR fuel, decades of backlog — never sell",
    },
    # FIX: $1844, analyst $2026. Steady compounder, infrastructure backbone
    "FIX": {
        "name": "Comfort Systems USA",
        "basket": "Industrial",
        "strategy": "hold_forever",
        "sell_target": None,
        "sell_date": None,
        "catalyst": "Data center + infrastructure compounder, +31% YoY — never sell",
    },

    # =================================================================
    # CYCLE HOLDS (1-3 years) — sell when cycle peaks
    # =================================================================
    # SRUUF: ~$19, tracks uranium spot. Mid-cycle, spot ~$90/lb
    "SRUUF": {
        "name": "Sprott Physical Uranium",
        "basket": "Nuclear",
        "strategy": "cycle",
        "sell_target": 30.0,
        "sell_date": "2027-2028",
        "catalyst": "Mid-cycle: uranium spot ~$90/lb, sell when spot peaks >$120/lb",
    },
    # LEU: $162, analyst $200. HALEU ramp early cycle
    "LEU": {
        "name": "Centrus Energy",
        "basket": "Nuclear",
        "strategy": "cycle",
        "sell_target": 220.0,
        "sell_date": "2028-2029",
        "catalyst": "Early cycle: HALEU production ramp, DOE contracts through 2030",
    },
    # VRT: $301, analyst $377. Data center capex mid-cycle
    "VRT": {
        "name": "Vertiv Holdings",
        "basket": "Industrial",
        "strategy": "cycle",
        "sell_target": 420.0,
        "sell_date": "2028-2029",
        "catalyst": "Mid-cycle: DC power/cooling +29% YoY, capex wave runs to 2029",
    },
    # POWL: $285, analyst $316. Revenue growth decelerating (+4.5% vs +45%)
    "POWL": {
        "name": "Powell Industries",
        "basket": "Industrial",
        "strategy": "cycle",
        "sell_target": 350.0,
        "sell_date": "2027-2028",
        "catalyst": "Late-mid cycle: growth slowing +4.5% YoY, sell when backlog peaks",
    },
    # LSCC: $136, analyst $147. Recovery from -31% crash, early recovery
    "LSCC": {
        "name": "Lattice Semiconductor",
        "basket": "SpecGrowth",
        "strategy": "cycle",
        "sell_target": 175.0,
        "sell_date": "2027-2028",
        "catalyst": "Early recovery: bottomed 2024, +42% last Q, sell at prior peak revenue",
    },
    # CRDO: $207, analyst $256. Hyper-growth but priced for perfection
    "CRDO": {
        "name": "Credo Technology",
        "basket": "SpecGrowth",
        "strategy": "cycle",
        "sell_target": 300.0,
        "sell_date": "2027-2028",
        "catalyst": "Early-mid cycle: revenue tripled, sell when growth drops below 30%",
    },

    # =================================================================
    # EVENT-DRIVEN (<18 months) — sell on the catalyst outcome
    # =================================================================
    # SMR: ~$11, pre-revenue. Binary: deployment order or bust
    "SMR": {
        "name": "NuScale Power",
        "basket": "Nuclear",
        "strategy": "catalyst",
        "sell_target": 25.0,
        "sell_date": "2027-2029",
        "catalyst": "Sell on first SMR deployment order (TVA/RoPower)",
    },
    # OKLO: ~$55, pre-revenue. Binary: NRC license or bust
    "OKLO": {
        "name": "Oklo Inc.",
        "basket": "Nuclear",
        "strategy": "catalyst",
        "sell_target": 90.0,
        "sell_date": "2028-2030",
        "catalyst": "Sell on NRC license approval for Aurora reactor",
    },
    # IONQ: ~$45, revenue growing but speculative
    "IONQ": {
        "name": "IonQ",
        "basket": "Quantum",
        "strategy": "catalyst",
        "sell_target": 65.0,
        "sell_date": "2027-2028",
        "catalyst": "Sell on quantum revenue inflection or hype cycle peak",
    },
    # QNT: ~$47, Honeywell-backed
    "QNT": {
        "name": "Quantinuum",
        "basket": "Quantum",
        "strategy": "catalyst",
        "sell_target": 80.0,
        "sell_date": "2027-2028",
        "catalyst": "Sell on post-IPO re-rating or error correction milestone",
    },
    # QBTS: ~$10, speculative
    "QBTS": {
        "name": "D-Wave Quantum",
        "basket": "Quantum",
        "strategy": "catalyst",
        "sell_target": 18.0,
        "sell_date": "2027",
        "catalyst": "Sell on quantum advantage proof or momentum peak (RSI>70)",
    },
    # RGTI: ~$21, speculative
    "RGTI": {
        "name": "Rigetti Computing",
        "basket": "Quantum",
        "strategy": "catalyst",
        "sell_target": 30.0,
        "sell_date": "2027",
        "catalyst": "Sell on QPU scaling milestone or hype peak",
    },
    # QUBT: ~$10, paused allocation
    "QUBT": {
        "name": "Quantum Computing Inc.",
        "basket": "Quantum (paused)",
        "strategy": "catalyst",
        "sell_target": 16.0,
        "sell_date": "2027",
        "catalyst": "Sell on any spike — paused allocation, thin thesis",
    },
    # RKLB: $110, Neutron launch is the catalyst
    "RKLB": {
        "name": "Rocket Lab",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "sell_target": 150.0,
        "sell_date": "2027-2028",
        "catalyst": "Sell on Neutron first launch hype peak",
    },
    # VKTX: $28, Phase III data is the binary event
    "VKTX": {
        "name": "Viking Therapeutics",
        "basket": "SpecGrowth",
        "strategy": "catalyst",
        "sell_target": 95.0,
        "sell_date": "H1 2027",
        "catalyst": "Sell on Phase III VK2735 data readout — win or lose",
    },
}


# =========================================================================
# TECHNICAL SIGNAL ENGINE
# =========================================================================

def compute_signals(ticker, sell_target=None):
    """Compute technical signals for a single ticker.

    Returns price, SMAs, RSI, 52w range, trend, and a dynamic buy_target.
    sell_target is passed through to ensure buy_target stays below it.
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

        # Dynamic buy target (constrained by sell_target)
        buy_target = compute_buy_target(
            price, sma_50, sma_200, low_52w, trend, len(close),
            sell_target=sell_target,
        )

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


def compute_buy_target(price, sma_50, sma_200, low_52w, trend, data_len,
                       sell_target=None):
    """Compute a dynamic buy target from live technical data.

    Logic:
    - UPTREND:  buy near the 50-SMA (short-term support in a rising market)
    - NEUTRAL:  buy near the 200-SMA (major support level)
    - DOWNTREND: buy near the 52w low + 10% buffer (wait for bottom)
    - If not enough data for SMA-200, use SMA-50 or 52w low

    Safety rails:
    - Floor: never below 52w low (it actually traded there)
    - Cap: always at least 5% discount from current price
    - Never above 80% of sell_target (must leave room for profit)
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

    # Never above 80% of sell_target (must leave room for profit)
    if sell_target is not None and sell_target > 0:
        target = min(target, sell_target * 0.80)

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
    if strategy == "cycle":
        return "SELL @ PEAK", f"Target ${sell_target:,.0f} (+{pct_to_target:.0f}%) — sell by {sell_date}"

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
        sell_target = meta.get("sell_target")
        signals = compute_signals(ticker, sell_target=sell_target)
        if signals is None:
            print("failed")
            continue

        # Warn if sell target is stale (below current price)
        warn = ""
        if sell_target and signals["price"] >= sell_target:
            warn = "  ⚠️ SELL TARGET STALE"
        print(f"${signals['price']:.2f}  buy@${signals['buy_target']:,.2f}{warn}")

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
