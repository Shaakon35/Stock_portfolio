# Stock Portfolio

A Jupyter-notebook-based stock portfolio tracker and analysis dashboard. It fetches live market data via **yfinance**, runs portfolio audits, generates performance charts, and produces an HTML report — all from Google Colab or any Jupyter environment.

## Repository Structure

```
Stock_portfolio/
├── CONFIGURATION.ipynb   # Shared configuration (assets, tickers, styling, forecast models)
├── main.ipynb            # Portfolio audit — allocation targets, live prices, FX rates
├── PLOT.ipynb            # Chart generation and HTML report builder
├── PUMP.ipynb            # Speculative / small-cap stock watchlist dashboard
├── output/               # Generated reports and charts (git-ignored contents)
└── README.md
```

## Notebooks

### CONFIGURATION.ipynb

Central configuration imported by the other notebooks. Defines:

- **Asset universe** — ETFs and individual stocks grouped by theme (`[CORE]`, `[AI]`, `[TECH]`, `[NUC]`, `[QTM]`, `[CYBER]`, `[FIN]`, `[ENG]`).
- **Output paths** — `OUTPUT_PATH` for the generated HTML report (`Stock_report.html`).
- **Thematic styling** — per-asset colors and line styles for consistent charting.
- **CAGR forecast models** — growth-rate estimates, risk ratings, and cyclicality flags for every tracked asset.
- **Cache settings** — yfinance market data cache with configurable expiration.

### main.ipynb

Portfolio management and audit notebook:

- Defines **target allocation weights** and a monthly deposit amount (EUR).
- Tracks **current share counts** across all positions.
- Fetches **live prices** via yfinance and **FX rates** (USD/CHF, EUR/CHF).
- Runs `verify_allocations()` to check that sub-allocation matrices sum to 100%.
- Performs a **portfolio audit** — compares actual vs. target weights and flags positions that are not in an uptrend.

### PLOT.ipynb

Visualization and reporting:

- Pulls historical price data for all configured assets over multiple timeframes (6-month, 1-year).
- Generates **sector-grouped performance charts** with themed styling.
- Builds a self-contained **HTML report** with tabbed navigation, embedded charts, and a summary table.
- Writes the final report to `OUTPUT_PATH/Stock_report.html`.

### PUMP.ipynb

Speculative stock watchlist dashboard:

- Maintains a curated list of small-cap / high-volatility stocks with metadata (52-week range, analyst ratings, price targets, profitability).
- Tracks a **"pumped"** flag indicating whether a stock has already had its breakout move.
- Renders a formatted table for quick screening.

## Output

The `output/` directory is where generated artifacts (HTML reports, charts) are stored. Its contents are not committed to version control.

When running in Google Colab, the default output path points to Google Drive (`/content/drive/MyDrive/Stocks/output/`). Update `OUTPUT_PATH` in `CONFIGURATION.ipynb` to change the destination.

## Dependencies

| Package | Purpose |
|---|---|
| `yfinance` | Live stock/ETF price data from Yahoo Finance |
| `matplotlib` | Chart generation |
| `pandas` | Data manipulation |
| `numpy` | Numerical operations |
| `IPython` | Notebook display utilities |

Install with:

```bash
pip install yfinance matplotlib pandas numpy
```

## Usage

1. Open the notebooks in **Google Colab** (or any Jupyter environment).
2. Run `CONFIGURATION.ipynb` first to load shared config.
3. Run `main.ipynb` for the portfolio audit.
4. Run `PLOT.ipynb` to generate charts and the HTML report.
5. Run `PUMP.ipynb` for the speculative watchlist.

> When using Colab, mount Google Drive first so the HTML report can be saved to `OUTPUT_PATH`.

## Disclaimer

This project is for personal portfolio tracking only. It is **not financial advice**. Data is sourced from public APIs and may be delayed or inaccurate. Always do your own due diligence.
