import os

# =========================================================================
# OUTPUT & CACHE SETTINGS
# =========================================================================
OUTPUT_PATH = "/content/drive/MyDrive/Stocks/output/"
HTML_FILE = os.path.join(OUTPUT_PATH, "Stock_report.html")
HTML = True

CACHE_FILE = "yfinance_market_cache.pkl"
CACHE_EXPIRATION_HOURS = 1

# Default timeframes (in years) for chart rendering
TIMEFRAMES = [0.5, 1]
