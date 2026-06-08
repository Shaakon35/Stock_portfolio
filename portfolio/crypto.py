import yfinance as yf

from portfolio.helpers import get_live_fx_rate

# =========================================================================
# TACTICAL CRYPTO ASSET DEPLOYMENT ENGINE (CHF DENOMINATED)
# =========================================================================

MONTHLY_DEPOSIT_CHF = 1000.0

CRYPTO_TARGET_WEIGHTS = {
    "BTC-USD":    0.40,
    "ETH-USD":    0.25,
    "SOL-USD":    0.15,
    "RENDER-USD": 0.05,
    "LINK-USD":   0.05,
    "XRP-USD":    0.00,
    # "CHSB-USD": 0.00
}

my_current_crypto = {
    "BTC-USD":    0.15,
    "ETH-USD":    4.43,
    "SOL-USD":    74.0,
    # "CHSB-USD": 10000.0,
    "RENDER-USD": 713.0,
    "LINK-USD":   144.96,
    "XRP-USD":    871.0,
}


def run_crypto_engine():
    """Fetch crypto prices, compute drift, and recommend the next buy."""
    USD_TO_CHF = get_live_fx_rate("USD", "CHF")

    crypto_prices_usd = {}
    print("\n🌐 Syncing Crypto Chain Prices...")

    # 2. Fetch Prices in USD
    for ticker in CRYPTO_TARGET_WEIGHTS.keys():
        try:
            ticker_obj = yf.Ticker(ticker)
            data = ticker_obj.history(period="1d")
            if not data.empty:
                crypto_prices_usd[ticker] = float(data['Close'].iloc[-1])
            else:
                crypto_prices_usd[ticker] = 0.01
        except Exception as e:
            print(f"❌ Error fetching {ticker}: {e}")
            crypto_prices_usd[ticker] = 0.01

    # 3. Calculate values
    crypto_values_usd = {
        c: my_current_crypto.get(c, 0) * crypto_prices_usd.get(c, 0)
        for c in CRYPTO_TARGET_WEIGHTS.keys()
    }
    total_crypto_value_usd = sum(crypto_values_usd.values())

    # 4. Identify Drift
    chosen_crypto_buy = None
    max_crypto_drift = -999.0

    for crypto_asset, target_pct in CRYPTO_TARGET_WEIGHTS.items():
        # Avoid division by zero
        c_pct = crypto_values_usd[crypto_asset] / total_crypto_value_usd if total_crypto_value_usd > 0 else 0
        c_drift = target_pct - c_pct
        if c_drift > max_crypto_drift:
            max_crypto_drift = c_drift
            chosen_crypto_buy = crypto_asset

    # 5. Output
    if chosen_crypto_buy:
        price_usd = crypto_prices_usd[chosen_crypto_buy]
        price_chf = price_usd * USD_TO_CHF
        units_to_buy = MONTHLY_DEPOSIT_CHF / price_chf

        print("\n" + "=" * 60)
        print(f"🟪 CRYPTO ACTION (CHF Denominated): Buy '{chosen_crypto_buy}'")
        print(f"   Exchange Rate Used: 1 USD = {USD_TO_CHF:.4f} CHF")
        print(f"   Execution Price: {price_chf:.2f} CHF per unit")
        print(f"   Target Purchase Volume: {units_to_buy:.4f} tokens")
        print(f"   Total Investment: {MONTHLY_DEPOSIT_CHF:.2f} CHF")
        print("=" * 60)

    return crypto_values_usd, chosen_crypto_buy
