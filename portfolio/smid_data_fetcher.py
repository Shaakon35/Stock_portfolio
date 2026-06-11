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
from portfolio.helpers import DELISTED_OVERRIDES


FACTOR_NAMES = [
    "upside", "growth", "accel", "valuation",
    "long_term", "cash_runway", "conviction", "entry", "momentum",
]

ADJUSTMENT_NAMES = ["profitability", "fragility", "downside"]

# Row status: "ok" = real data point used in analysis,
# "not_found" = lookup failed/delisted-without-history; kept only so re-runs
# skip the ticker instead of re-querying yfinance every time.
STATUS_OK = "ok"
STATUS_NOT_FOUND = "not_found"

CSV_COLUMNS = (
    ["ticker", "strategy", "basket", "period_months", "price_then", "price_now", "actual_return"]
    + FACTOR_NAMES
    + ADJUSTMENT_NAMES
    + ["status", "note"]
)

# Resolve to absolute path so it works regardless of working directory
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_CSV = os.path.join(_REPO_ROOT, "output", "smid_optimization_data.csv")
# Ensure output directory exists
os.makedirs(os.path.join(_REPO_ROOT, "output"), exist_ok=True)


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
# NOTE: Acquisitions and confirmed bankruptcies now live in
# DELISTED_OVERRIDES (portfolio/helpers.py), which is checked FIRST in the
# fetch loop. Acquired tickers get their REAL buyout return there instead of
# the -100% this dict hardcodes. The entries below are the remaining
# "near-dead"/delisted names not yet curated into the overrides. Several of
# these (FATE, STEM, EDIT, SKLZ, SPIR, PSNY) actually still TRADE, so the
# -100% here overstates the loss — review and migrate to DELISTED_OVERRIDES.
KNOWN_DEAD = {
    "WOLF":  {12: 8.00, 24: 18.00, 36: 30.00},   # Wolfspeed, bankrupt 2025
    "PLBY":  {12: 0.50, 24: 2.00, 36: 3.00},      # Playboy, delisted
    "FATE":  {12: 2.00, 24: 3.00, 36: 5.00},      # Fate Therapeutics, near-dead (still trades)
    "STEM":  {12: 0.30, 24: 0.80, 36: 3.00},      # Stem Inc, near-dead (still trades)
    "EDIT":  {12: 1.50, 24: 3.00, 36: 8.00},      # Editas Medicine, near-dead (still trades)
    "SKLZ":  {12: 3.00, 24: 6.00, 36: 8.00},      # Skillz, near-dead (still trades)
    "MNTS":  {12: 0, 24: 0, 36: 5.00},            # Momentus, delisted
    "SPIR":  {12: 5.00, 24: 8.00, 36: 1.50},      # Spire Global (still trades)
    "PSNY":  {12: 0, 24: 1.00, 36: 3.00},         # Polestar, near-dead (still trades)
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
        "status": STATUS_OK,
    }


def _make_acquired_record(ticker, meta, lookback_months, price_then, payout, note=""):
    """Create a record for an acquired stock using its REAL buyout return.

    Shareholders received cash/stock in the buyout, so the return is
    (payout - price_then) / price_then, NOT -100%. Mislabeling these as
    total losses poisons the training data (a profitable exit looks like a
    wipeout), so we compute the actual outcome here.
    """
    actual_return = (payout - price_then) / price_then * 100.0
    return {
        "ticker": ticker,
        "strategy": meta["strategy"],
        "basket": meta.get("basket", ""),
        "period_months": lookback_months,
        "price_then": round(price_then, 2),
        "price_now": round(payout, 2),
        "actual_return": round(actual_return, 2),
        **{f: 50.0 for f in FACTOR_NAMES},  # neutral scores (data scrubbed)
        **{"profitability": 0, "fragility": -10, "downside": -10},
        "status": STATUS_OK,
        "note": (note or "")[:120],
    }


def _make_not_found_record(ticker, meta, lookback_months, note=""):
    """Create a placeholder for a ticker whose data couldn't be fetched.

    Marked status="not_found" so resume logic skips it on re-runs instead of
    re-querying yfinance. Excluded from analysis by load_csv() default.
    """
    return {
        "ticker": ticker,
        "strategy": meta["strategy"],
        "basket": meta.get("basket", ""),
        "period_months": lookback_months,
        "price_then": 0.0,
        "price_now": 0.0,
        "actual_return": 0.0,
        **{f: 0.0 for f in FACTOR_NAMES},
        **{a: 0.0 for a in ADJUSTMENT_NAMES},
        "status": STATUS_NOT_FOUND,
        "note": (note or "")[:120],
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
    not_found_count = 0
    total = len(universe)

    print(f"\n{'='*60}")
    print(f"PERIOD: {lookback_months} months (lookback={lookback_date.strftime('%Y-%m-%d')})")
    print(f"{'='*60}")

    for i, (ticker, meta) in enumerate(universe.items()):
        key = (ticker, lookback_months)
        if key in existing_keys:
            continue
        print(f"  [{i+1}/{total}] {ticker}...", end="", flush=True)

        # Delisted overrides take priority: acquisitions get their REAL
        # buyout return (not -100%); bankruptcies get -100%.
        if ticker in DELISTED_OVERRIDES:
            od_status, od_note, od_payout = DELISTED_OVERRIDES[ticker]
            price_then = _try_get_historical_price(ticker, lookback_date)

            if od_status == "acquired":
                if price_then and price_then > 0:
                    rec = _make_acquired_record(
                        ticker, meta, lookback_months, price_then,
                        od_payout, od_note)
                    records.append(rec)
                    dead_count += 1
                    print(f" ACQUIRED (was ${price_then:.0f} -> "
                          f"${od_payout:.2f}) ret={rec['actual_return']:+.0f}%")
                else:
                    # No price at this lookback => didn't trade yet / already
                    # acquired by then. Skip (cache so re-runs don't retry).
                    records.append(_make_not_found_record(
                        ticker, meta, lookback_months,
                        "acquired; no price at this lookback"))
                    not_found_count += 1
                    print(f" skip: acquired, no price at this lookback")
                continue

            # bankrupt -> genuine total loss
            bk_price = price_then if (price_then and price_then > 0) else 1.0
            records.append(_make_dead_record(
                ticker, meta, lookback_months, bk_price))
            dead_count += 1
            print(f" BANKRUPT (was ${bk_price:.0f}) ret=-100%")
            continue

        # Legacy known-dead list (kept for tickers not in the curated overrides)
        if ticker in KNOWN_DEAD:
            known_price = KNOWN_DEAD[ticker].get(lookback_months, 0)
            if known_price and known_price > 0:
                records.append(_make_dead_record(ticker, meta, lookback_months, known_price))
                dead_count += 1
                print(f" DEAD/KNOWN (was ${known_price:.0f}) ret=-100%")
                continue
            elif known_price == 0:
                # Stock didn't exist at this lookback (already acquired)
                records.append(_make_not_found_record(
                    ticker, meta, lookback_months,
                    "not yet listed/already acquired"))
                not_found_count += 1
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
                records.append(_make_not_found_record(
                    ticker, meta, lookback_months, str(e)))
                not_found_count += 1
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
                records.append(_make_not_found_record(
                    ticker, meta, lookback_months, str(data["error"])))
                not_found_count += 1
                print(f" skip: {data['error']}")
                errors.append((ticker, data["error"]))
            continue

        result = compute_factor_scores(data, meta)
        if result is None:
            records.append(_make_not_found_record(
                ticker, meta, lookback_months, "scoring failed"))
            not_found_count += 1
            print(" skip: scoring failed")
            errors.append((ticker, "scoring failed"))
            continue

        scores, adjustments = result

        price_then = data["price"]
        price_now = data.get("price_now")
        if not price_then or price_then <= 0:
            records.append(_make_not_found_record(
                ticker, meta, lookback_months, "no historical price"))
            not_found_count += 1
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

    n_ok = sum(1 for r in records if r.get("status", STATUS_OK) == STATUS_OK)
    print(f"  -> {n_ok} valid ({dead_count} dead/delisted) / "
          f"{not_found_count} not-found (cached as skip) / {len(errors)} errors")
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

    # Resume support: load existing CSV (including not_found placeholders so
    # we skip previously-failed tickers), track (ticker, period) pairs.
    all_records = []
    existing_keys = set()
    if not force_refresh and os.path.exists(csv_path):
        existing = load_csv(csv_path, include_not_found=True)
        if existing:
            all_records = existing
            existing_keys = {(r["ticker"], r["period_months"]) for r in existing}
            # Check which periods are complete (ok rows vs cached skips)
            for pm in periods:
                n_ok = sum(1 for r in existing
                           if r["period_months"] == pm
                           and r.get("status", STATUS_OK) == STATUS_OK)
                n_skip = sum(1 for r in existing
                             if r["period_months"] == pm
                             and r.get("status") == STATUS_NOT_FOUND)
                print(f"  Period {pm}mo: {n_ok} records cached"
                      f"{f' (+{n_skip} not-found skipped)' if n_skip else ''}")

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

    # Split usable rows from not_found placeholders. The CSV keeps both
    # (so re-runs skip failed tickers); analysis only sees usable rows.
    usable = [r for r in all_records
              if r.get("status", STATUS_OK) == STATUS_OK]
    n_skipped = len(all_records) - len(usable)

    period_counts = {}
    for r in usable:
        pm = r["period_months"]
        period_counts[pm] = period_counts.get(pm, 0) + 1
    print(f"\nTotal: {len(usable)} usable records"
          f"{f' ({n_skipped} not-found cached in CSV)' if n_skipped else ''}")
    print(f"Per period: {period_counts}")

    return usable


def save_csv(records, path=None):
    """Save records to CSV."""
    path = path or DEFAULT_CSV
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def load_csv(path=None, include_not_found=False):
    """Load records from CSV.

    By default returns only usable (status="ok") rows for analysis.
    Set include_not_found=True to also get the "not_found" placeholders
    (used internally by resume logic to know which tickers to skip).

    Backward compatible: rows from CSVs written before the status column
    are treated as status="ok".
    """
    path = path or DEFAULT_CSV
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        reader = csv.DictReader(f)
        records = []
        n_not_found = 0
        for row in reader:
            status = row.get("status") or STATUS_OK
            row["status"] = status
            row["note"] = row.get("note") or ""
            row["period_months"] = int(row["period_months"])
            row["price_then"] = float(row["price_then"])
            row["price_now"] = float(row["price_now"])
            row["actual_return"] = float(row["actual_return"])
            for fn in FACTOR_NAMES:
                row[fn] = float(row[fn])
            for an in ADJUSTMENT_NAMES:
                row[an] = float(row[an])
            if status == STATUS_NOT_FOUND:
                n_not_found += 1
                if not include_not_found:
                    continue
            records.append(row)

    suffix = f" (+{n_not_found} not-found skipped)" if n_not_found and not include_not_found else ""
    print(f"Loaded {len(records)} records from {path}{suffix}")
    return records


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    records = fetch_all(lookback_months=12, force_refresh=force)
    print(f"\nTotal records: {len(records)}")
