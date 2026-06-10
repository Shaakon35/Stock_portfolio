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


def _fetch_period(universe, lookback_months, existing_keys, batch_size=50):
    """Fetch data for one lookback period. Returns (new_records, errors)."""
    lookback_date = datetime.now() - timedelta(days=lookback_months * 30)
    records = []
    errors = []
    total = len(universe)

    print(f"\n{'='*60}")
    print(f"PERIOD: {lookback_months} months (lookback={lookback_date.strftime('%Y-%m-%d')})")
    print(f"{'='*60}")

    for i, (ticker, meta) in enumerate(universe.items()):
        key = (ticker, lookback_months)
        if key in existing_keys:
            continue
        print(f"  [{i+1}/{total}] {ticker}...", end="", flush=True)

        try:
            data = fetch_historical_data(ticker, lookback_date)
        except Exception as e:
            print(f" ERROR: {e}")
            errors.append((ticker, str(e)))
            continue

        if data.get("error"):
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
        if not price_then or not price_now or price_then <= 0:
            print(" skip: no price data")
            errors.append((ticker, "no price data"))
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

    print(f"  -> {len(records)} valid / {len(errors)} errors")
    return records, errors


def fetch_all(lookback_months=12, csv_path=None, force_refresh=False, batch_size=50,
              periods=None):
    """Fetch data for all ~700 tickers across one or more lookback periods.

    Args:
        lookback_months: single period (used if periods is None)
        csv_path: output CSV path
        force_refresh: if True, refetch everything
        batch_size: pause every N tickers to avoid rate limits
        periods: list of lookback months, e.g. [12, 24, 36]

    Returns:
        list of record dicts (all periods combined)
    """
    csv_path = csv_path or DEFAULT_CSV
    if periods is None:
        periods = [lookback_months]

    universe = get_full_universe()

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
