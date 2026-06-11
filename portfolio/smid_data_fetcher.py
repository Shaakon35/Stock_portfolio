"""
Fetch factor scores + forward returns for ~700 small/mid-cap stocks.

Lookback: mid-2025 (scores computed as-of that date).
Forward return: from mid-2025 to today.
Output: CSV at output/smid_optimization_data.csv

Reuses scoring functions from portfolio.ranking and historical data
reconstruction from portfolio.validation.
"""

import os
import csv
import time
import traceback
import numpy as np
from datetime import datetime, timedelta

from portfolio.ranking import (
    score_analyst_upside, score_revenue_quality, score_analyst_conviction,
    score_entry_position, score_momentum, score_valuation,
    score_long_term_health, score_cash_runway, score_revenue_acceleration,
    penalty_fragility, penalty_downside, bonus_profitability,
)
from portfolio.validation import fetch_historical_data
from portfolio.smid_universe import get_full_universe


FACTOR_NAMES = [
    "upside", "growth", "accel", "valuation",
    "long_term", "cash_runway", "conviction", "entry", "momentum",
]

ADJUSTMENT_NAMES = ["profitability", "fragility", "downside"]

CSV_COLUMNS = (
    ["ticker", "strategy", "basket", "period_months", "price_then", "price_now", "actual_return"]
    + FACTOR_NAMES
    + ADJUSTMENT_NAMES
)

DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "..", "output", "smid_optimization_data.csv")


def _num(val, default=None):
    """Coerce a value to float, returning default if it can't be converted."""
    if val is None:
        return default
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def compute_factor_scores(data, meta):
    """Compute 0-100 factor sub-scores from historical data."""
    if data.get("error"):
        return None

    price = _num(data.get("price"))
    if not price or price <= 0:
        return None
    scores = {
        "upside": score_analyst_upside(price, _num(data.get("target"))),
        "growth": score_revenue_quality(
            _num(data.get("rev_growth_pct")), _num(data.get("total_revenue"), 0)
        ),
        "accel": score_revenue_acceleration(
            _num(data.get("rev_growth_pct")), _num(data.get("prior_rev_growth_pct"))
        ),
        "valuation": score_valuation(_num(data.get("ps_ratio"))),
        "long_term": score_long_term_health(
            price, _num(data.get("high_2y")), _num(data.get("history_years"))
        ),
        "cash_runway": score_cash_runway(
            _num(data.get("total_cash")), _num(data.get("free_cash_flow")), _num(data.get("eps"))
        ),
        "conviction": score_analyst_conviction(
            data.get("recommendation", "none"), _num(data.get("num_analysts"), 0)
        ),
        "entry": score_entry_position(price, _num(data.get("high_52w")), _num(data.get("low_52w"))),
        "momentum": score_momentum(price, _num(data.get("sma_50")), _num(data.get("sma_200"))),
    }

    adjustments = {
        "profitability": bonus_profitability(
            _num(data.get("eps")), _num(data.get("free_cash_flow")), _num(data.get("market_cap"))
        ),
        "fragility": penalty_fragility(meta.get("fragility", "none")),
        "downside": penalty_downside(meta.get("downside_if_fail", "moderate")),
    }

    return scores, adjustments


# Stocks that were delisted/bankrupt and Yahoo has purged their data.
# Approximate prices at various lookback dates, sourced from historical records.
# Format: ticker -> {lookback_months: approximate_price_then}
KNOWN_DEAD = {
    "NKLA":  {12: 1.50, 24: 0.80, 36: 1.20},   # Nikola, delisted 2025
    "GOEV":  {12: 1.80, 24: 1.50, 36: 3.50},    # Canoo, bankrupt 2025
    "WOLF":  {12: 8.00, 24: 18.00, 36: 30.00},   # Wolfspeed, bankrupt 2025
    "CFLT":  {12: 25.00, 24: 28.00, 36: 30.00},  # Confluent, acquired/delisted
    "SGEN":  {12: 0, 24: 0, 36: 175.00},          # Seagen, acquired by Pfizer 2023
    "ALTR":  {12: 0, 24: 0, 36: 50.00},           # Altair, acquired 2024
    "MAXR":  {12: 0, 24: 0, 36: 52.00},           # Maxar, acquired 2023
    "AJRD":  {12: 0, 24: 0, 36: 58.00},           # Aerojet, acquired 2023
    "CLDR":  {12: 0, 24: 0, 36: 16.00},           # Cloudera, taken private
    "ZNGA":  {12: 0, 24: 0, 36: 9.00},            # Zynga, acquired by Take-Two
    "AVLR":  {12: 0, 24: 0, 36: 90.00},           # Avalara, acquired
    "COUP":  {12: 0, 24: 0, 36: 80.00},           # Coupa, acquired by Thoma Bravo
    "SUMO":  {12: 0, 24: 0, 36: 12.00},           # Sumo Logic, acquired
    "SMAR":  {12: 0, 24: 48.00, 36: 40.00},       # Smartsheet, acquired 2024
    "JAMF":  {12: 0, 24: 18.00, 36: 17.00},       # JAMF, acquired 2025
    "SILK":  {12: 0, 24: 0, 36: 45.00},           # Silk Road Medical, acquired
    "GNOG":  {12: 0, 24: 0, 36: 10.00},           # Golden Nugget Online, merged
    "PLBY":  {12: 0.50, 24: 2.00, 36: 3.00},      # Playboy, delisted
    "FATE":  {12: 2.00, 24: 3.00, 36: 5.00},      # Fate Therapeutics, near-dead
    "STEM":  {12: 0.30, 24: 0.80, 36: 3.00},      # Stem Inc, near-dead
    "EDIT":  {12: 1.50, 24: 3.00, 36: 8.00},      # Editas Medicine, near-dead
    "SKLZ":  {12: 3.00, 24: 6.00, 36: 8.00},      # Skillz, near-dead
    "MNTS":  {12: 0, 24: 0, 36: 5.00},            # Momentus, delisted
    "SPIR":  {12: 5.00, 24: 8.00, 36: 1.50},      # Spire Global
    "PSNY":  {12: 0, 24: 1.00, 36: 3.00},         # Polestar, near-dead
}
# price=0 means the stock didn't exist at that lookback (already acquired/merged)


def _make_dead_record(ticker, meta, lookback_months, price_then=1.0):
    """Create a record for a delisted/dead stock with -100% return and neutral scores."""
    return {
        "ticker": ticker,
        "strategy": meta["strategy"],
        "basket": meta.get("basket", ""),
        "period_months": lookback_months,
        "price_then": round(price_then, 2),
        "price_now": 0.0,
        "actual_return": -100.0,
        **{f: 50.0 for f in FACTOR_NAMES},  # neutral scores
        **{"profitability": 0, "fragility": -10, "downside": -10},
    }


def _try_get_historical_price(ticker, lookback_date):
    """Try to get the stock's price at lookback_date from price history.

    Returns price or None. Works even for delisted stocks if Yahoo
    still has their historical data.
    """
    import yfinance as yf
    try:
        t = yf.Ticker(ticker)
        start = lookback_date - timedelta(days=10)
        end = lookback_date + timedelta(days=10)
        hist = t.history(start=start, end=end)
        if hist is not None and len(hist) > 0:
            return float(hist["Close"].iloc[-1])
    except Exception:
        pass
    return None


def _fetch_period(universe, lookback_months, existing_keys, batch_size=50):
    """Fetch data for one lookback period. Returns (new_records, errors).

    Survivorship bias fix: stocks that existed at lookback_date but are
    now delisted/dead are included with -100% return and neutral factor
    scores. This prevents the model from ignoring the worst outcomes.
    """
    lookback_date = datetime.now() - timedelta(days=lookback_months * 30)
    records = []
    errors = []
    dead_count = 0
    total = len(universe)

    print(f"\n{'='*60}")
    print(f"PERIOD: {lookback_months} months (lookback={lookback_date.strftime('%Y-%m-%d')})")
    print(f"{'='*60}")

    for i, (ticker, meta) in enumerate(universe.items()):
        key = (ticker, lookback_months)
        if key in existing_keys:
            continue
        print(f"  [{i+1}/{total}] {ticker}...", end="", flush=True)

        # Check known-dead list first
        if ticker in KNOWN_DEAD:
            known_price = KNOWN_DEAD[ticker].get(lookback_months, 0)
            if known_price and known_price > 0:
                records.append(_make_dead_record(ticker, meta, lookback_months, known_price))
                dead_count += 1
                print(f" DEAD/KNOWN (was ${known_price:.0f}) ret=-100%")
                continue
            elif known_price == 0:
                # Stock didn't exist at this lookback (already acquired)
                print(f" skip: not yet listed/already acquired at this lookback")
                continue

        try:
            data = fetch_historical_data(ticker, lookback_date)
        except Exception as e:
            # Stock might be delisted — check if it had a price at lookback
            hist_price = _try_get_historical_price(ticker, lookback_date)
            if hist_price and hist_price > 0:
                records.append(_make_dead_record(ticker, meta, lookback_months, hist_price))
                dead_count += 1
                print(f" DEAD (was ${hist_price:.0f}, now delisted) ret=-100%")
            else:
                print(f" ERROR: {e}")
                errors.append((ticker, str(e)))
            continue

        if data.get("error"):
            # Check if "no price data" means delisted vs never existed
            hist_price = _try_get_historical_price(ticker, lookback_date)
            if hist_price and hist_price > 0:
                records.append(_make_dead_record(ticker, meta, lookback_months, hist_price))
                dead_count += 1
                print(f" DEAD (was ${hist_price:.0f}, now gone) ret=-100%")
            else:
                print(f" skip: {data['error']}")
                errors.append((ticker, data["error"]))
            continue

        result = compute_factor_scores(data, meta)
        if result is None:
            print(" skip: scoring failed")
            errors.append((ticker, "scoring failed"))
            continue

        scores, adjustments = result

        price_then = data["price"]
        price_now = data.get("price_now")
        if not price_then or price_then <= 0:
            print(" skip: no historical price")
            errors.append((ticker, "no historical price"))
            continue

        if not price_now:
            # Had a price then but no current price → likely delisted
            records.append(_make_dead_record(ticker, meta, lookback_months, price_then))
            dead_count += 1
            print(f" DEAD (was ${price_then:.0f}, no current price) ret=-100%")
            continue

        actual_return = ((price_now - price_then) / price_then) * 100

        records.append({
            "ticker": ticker,
            "strategy": meta["strategy"],
            "basket": meta.get("basket", ""),
            "period_months": lookback_months,
            "price_then": round(price_then, 2),
            "price_now": round(price_now, 2),
            "actual_return": round(actual_return, 2),
            **{f: round(scores[f], 1) for f in FACTOR_NAMES},
            **{a: adjustments[a] for a in ADJUSTMENT_NAMES},
        })
        print(f" ${price_then:.0f}→${price_now:.0f} ret={actual_return:+.1f}%")

        if (i + 1) % batch_size == 0:
            print(f"  ... pausing 2s (rate limit) ...")
            time.sleep(2)

    print(f"  -> {len(records)} valid ({dead_count} dead/delisted) / {len(errors)} errors")
    return records, errors


def fetch_all(lookback_months=12, csv_path=None, force_refresh=False, batch_size=50,
              periods=None, max_tickers=None):
    """Fetch data for tickers across one or more lookback periods.

    Args:
        lookback_months: single period (used if periods is None)
        csv_path: output CSV path
        force_refresh: if True, refetch everything
        batch_size: pause every N tickers to avoid rate limits
        periods: list of lookback months, e.g. [12, 24, 36]
        max_tickers: limit to first N tickers (for quick test runs)

    Returns:
        list of record dicts (all periods combined)
    """
    csv_path = csv_path or DEFAULT_CSV
    if periods is None:
        periods = [lookback_months]

    universe = get_full_universe()
    if max_tickers:
        # Take a diverse sample: pick evenly across strategies
        tickers = list(universe.keys())[:max_tickers]
        universe = {t: universe[t] for t in tickers}
        print(f"*** TEST MODE: limited to {len(universe)} tickers ***")

    # Resume support: load existing CSV, track (ticker, period) pairs
    all_records = []
    existing_keys = set()
    if not force_refresh and os.path.exists(csv_path):
        existing = load_csv(csv_path)
        if existing:
            all_records = existing
            existing_keys = {(r["ticker"], r["period_months"]) for r in existing}
            # Check which periods are complete
            for pm in periods:
                n = sum(1 for k in existing_keys if k[1] == pm)
                print(f"  Period {pm}mo: {n} records cached")

    if force_refresh:
        all_records = []
        existing_keys = set()

    # Fetch each period
    for pm in periods:
        new_records, errors = _fetch_period(universe, pm, existing_keys, batch_size)
        all_records.extend(new_records)
        # Save after each period
        save_csv(all_records, csv_path)
        print(f"  Saved {len(all_records)} total records to {csv_path}")

    # Summary
    period_counts = {}
    for r in all_records:
        pm = r["period_months"]
        period_counts[pm] = period_counts.get(pm, 0) + 1
    print(f"\nTotal: {len(all_records)} records")
    print(f"Per period: {period_counts}")

    return all_records


def save_csv(records, path=None):
    """Save records to CSV."""
    path = path or DEFAULT_CSV
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def load_csv(path=None):
    """Load records from CSV."""
    path = path or DEFAULT_CSV
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        reader = csv.DictReader(f)
        records = []
        for row in reader:
            row["period_months"] = int(row["period_months"])
            row["price_then"] = float(row["price_then"])
            row["price_now"] = float(row["price_now"])
            row["actual_return"] = float(row["actual_return"])
            for fn in FACTOR_NAMES:
                row[fn] = float(row[fn])
            for an in ADJUSTMENT_NAMES:
                row[an] = float(row[an])
            records.append(row)

    print(f"Loaded {len(records)} records from {path}")
    return records


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    records = fetch_all(lookback_months=12, force_refresh=force)
    print(f"\nTotal records: {len(records)}")
