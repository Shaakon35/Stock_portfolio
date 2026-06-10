"""
Multi-year weight optimizer for the ranking model.

Runs backtests across multiple lookback periods (1y through 5y) and finds
factor weights that maximize average Spearman correlation across all periods.
This prevents overfitting to a single year's market regime.

Usage (in Colab):
    from portfolio.optimizer import run_multi_year_optimization
    results = run_multi_year_optimization()
"""

import numpy as np
from itertools import product
from datetime import datetime, timedelta

from portfolio.ranking import (
    RANKING_UNIVERSE, STRATEGY_WEIGHTS,
    score_analyst_upside, score_revenue_quality, score_analyst_conviction,
    score_entry_position, score_momentum, score_valuation,
    score_long_term_health, score_cash_runway, score_revenue_acceleration,
    penalty_fragility, penalty_downside, bonus_profitability,
)
from portfolio.validation import (
    BACKTEST_EXTRA, fetch_historical_data,
)


# =========================================================================
# DATA COLLECTION
# =========================================================================

FACTOR_NAMES = [
    "upside", "growth", "accel", "valuation",
    "long_term", "cash_runway", "conviction", "entry", "momentum",
]

ADJUSTMENT_NAMES = ["profitability", "fragility", "downside"]


def _compute_factor_scores(data, meta):
    """Compute individual factor sub-scores (0-100) without weighting."""
    if data.get("error"):
        return None

    price = data["price"]

    scores = {
        "upside": score_analyst_upside(price, data["target"]),
        "growth": score_revenue_quality(
            data["rev_growth_pct"], data.get("total_revenue", 0)
        ),
        "accel": score_revenue_acceleration(
            data.get("rev_growth_pct"), data.get("prior_rev_growth_pct")
        ),
        "valuation": score_valuation(data.get("ps_ratio")),
        "long_term": score_long_term_health(
            price, data.get("high_2y"), data.get("history_years")
        ),
        "cash_runway": score_cash_runway(
            data.get("total_cash"), data.get("free_cash_flow"), data.get("eps")
        ),
        "conviction": score_analyst_conviction(
            data["recommendation"], data["num_analysts"]
        ),
        "entry": score_entry_position(price, data["high_52w"], data["low_52w"]),
        "momentum": score_momentum(price, data["sma_50"], data["sma_200"]),
    }

    adjustments = {
        "profitability": bonus_profitability(
            data.get("eps"), data.get("free_cash_flow"), data.get("market_cap")
        ),
        "fragility": penalty_fragility(meta.get("fragility", "none")),
        "downside": penalty_downside(meta.get("downside_if_fail", "low")),
    }

    return scores, adjustments


def collect_period_data(lookback_months):
    """Fetch historical data for one lookback period and compute factor scores.

    Returns list of dicts with factor scores and actual returns.
    """
    lookback_date = datetime.now() - timedelta(days=lookback_months * 30)

    universe = {}
    universe.update(RANKING_UNIVERSE)
    universe.update(BACKTEST_EXTRA)

    records = []
    total = len(universe)

    for i, (ticker, meta) in enumerate(universe.items()):
        print(f"  [{i+1}/{total}] {ticker}...", end="", flush=True)
        data = fetch_historical_data(ticker, lookback_date)

        if data.get("error"):
            print(f" ⚠️ {data['error']}")
            continue

        result = _compute_factor_scores(data, meta)
        if result is None:
            print(" ⚠️ scoring failed")
            continue

        scores, adjustments = result

        price_then = data["price"]
        price_now = data.get("price_now")
        if price_then and price_now and price_then > 0:
            actual_return = ((price_now - price_then) / price_then) * 100
        else:
            print(" ⚠️ no return data")
            continue

        records.append({
            "ticker": ticker,
            "strategy": meta["strategy"],
            "actual_return": round(actual_return, 2),
            **{f: round(scores[f], 1) for f in FACTOR_NAMES},
            **{f: adjustments[f] for f in ADJUSTMENT_NAMES},
        })
        print(f" ✓ ret={actual_return:+.1f}%")

    return records


def collect_all_periods(periods_months=None):
    """Collect factor scores for multiple lookback periods.

    Args:
        periods_months: list of lookback periods in months.
            Default: [12, 24, 36, 48, 60] (1y through 5y)

    Returns:
        dict mapping period_months -> list of stock records
    """
    if periods_months is None:
        periods_months = [12, 24, 36, 48, 60]

    all_data = {}
    for months in periods_months:
        years = months / 12
        print(f"\n{'='*60}")
        print(f"COLLECTING DATA: {years:.0f}-year lookback ({months} months)")
        print(f"{'='*60}")
        records = collect_period_data(months)
        all_data[months] = records
        print(f"  → {len(records)} stocks with valid data")

    return all_data


# =========================================================================
# OPTIMIZATION ENGINE
# =========================================================================

def _spearman_correlation(x, y):
    """Compute Spearman rank correlation between two arrays."""
    n = len(x)
    if n < 5:
        return 0.0

    # Rank both arrays
    def rank(arr):
        sorted_idx = np.argsort(arr)
        ranks = np.empty_like(sorted_idx, dtype=float)
        ranks[sorted_idx] = np.arange(1, n + 1)
        return ranks

    rx = rank(np.array(x, dtype=float))
    ry = rank(np.array(y, dtype=float))

    d = rx - ry
    d2_sum = np.sum(d ** 2)
    return 1 - (6 * d2_sum) / (n * (n**2 - 1))


def _compute_weighted_scores(records, weights, adj_mult=0.0):
    """Compute composite scores for a set of records given weights."""
    scores = []
    for r in records:
        sc = sum(r[f] * weights[f] for f in FACTOR_NAMES)
        adj = sum(r[f] for f in ADJUSTMENT_NAMES)
        sc += adj * adj_mult
        scores.append(sc)
    return scores


def _evaluate_weights(all_data, weights, adj_mult=0.0):
    """Compute average Spearman correlation across all periods."""
    correlations = []
    for months, records in all_data.items():
        if len(records) < 10:
            continue
        scores = _compute_weighted_scores(records, weights, adj_mult)
        returns = [r["actual_return"] for r in records]
        corr = _spearman_correlation(scores, returns)
        correlations.append(corr)

    if not correlations:
        return -1.0
    return np.mean(correlations)


def factor_correlations(all_data):
    """Compute per-factor Spearman correlations for each period.

    Returns dict of factor -> list of (period, correlation) tuples.
    """
    results = {}
    for f in FACTOR_NAMES + ADJUSTMENT_NAMES:
        results[f] = []
        for months, records in sorted(all_data.items()):
            if len(records) < 10:
                continue
            vals = [r[f] for r in records]
            rets = [r["actual_return"] for r in records]
            corr = _spearman_correlation(vals, rets)
            results[f].append((months, corr))
    return results


def optimize_weights(all_data, step=0.05, adj_steps=None):
    """Grid search for optimal weights across all periods.

    Uses a two-phase approach:
    1. Coarse grid (step size) over all weight combinations
    2. Coordinate descent refinement

    Args:
        all_data: output of collect_all_periods()
        step: grid step size (default 0.05 = 5%)
        adj_steps: adjustment multipliers to test (default [0, 0.5, 1.0])

    Returns:
        dict with best weights, correlations per period, and analysis
    """
    if adj_steps is None:
        adj_steps = [0.0, 0.25, 0.5, 1.0]

    n_factors = len(FACTOR_NAMES)
    n_steps = int(1.0 / step)

    print(f"\n{'='*60}")
    print(f"PHASE 1: Coarse grid search (step={step})")
    print(f"{'='*60}")

    # Generate weight combinations summing to 1.0
    best_corr = -1.0
    best_weights = {}
    best_adj = 0.0
    combos_tested = 0

    # Use recursive generation for efficiency
    def _search(idx, remaining, current_weights):
        nonlocal best_corr, best_weights, best_adj, combos_tested

        if idx == n_factors - 1:
            w = remaining * step
            current_weights[FACTOR_NAMES[idx]] = w
            combos_tested += 1

            for adj_mult in adj_steps:
                corr = _evaluate_weights(all_data, current_weights, adj_mult)
                if corr > best_corr:
                    best_corr = corr
                    best_weights = dict(current_weights)
                    best_adj = adj_mult
            return

        for v in range(remaining + 1):
            current_weights[FACTOR_NAMES[idx]] = v * step
            _search(idx + 1, remaining - v, current_weights)

    _search(0, n_steps, {})
    print(f"  Tested {combos_tested} weight combinations × {len(adj_steps)} adj multipliers")
    print(f"  Best avg Spearman: {best_corr:.3f} (adj_mult={best_adj})")

    # Phase 2: Coordinate descent refinement
    print(f"\n{'='*60}")
    print(f"PHASE 2: Coordinate descent refinement")
    print(f"{'='*60}")

    current_w = dict(best_weights)
    current_adj = best_adj
    improved = True
    iteration = 0

    while improved and iteration < 30:
        improved = False
        iteration += 1

        for f in FACTOR_NAMES:
            best_val = current_w[f]
            best_c = _evaluate_weights(all_data, current_w, current_adj)

            for try_pct in range(0, 81):  # 0% to 80% in 1% steps
                try_val = try_pct / 100.0
                old_val = current_w[f]
                current_w[f] = try_val

                # Renormalize
                total = sum(current_w.values())
                if total == 0:
                    current_w[f] = old_val
                    continue
                test_w = {k: v / total for k, v in current_w.items()}

                corr = _evaluate_weights(all_data, test_w, current_adj)
                if corr > best_c:
                    best_c = corr
                    best_val = try_val
                current_w[f] = old_val

            if best_val != current_w[f]:
                current_w[f] = best_val
                total = sum(current_w.values())
                if total > 0:
                    current_w = {k: v / total for k, v in current_w.items()}
                improved = True

        # Also try different adj multipliers
        for try_adj in [x / 10.0 for x in range(-10, 21)]:
            corr = _evaluate_weights(all_data, current_w, try_adj)
            if corr > best_c:
                best_c = corr
                current_adj = try_adj
                improved = True

    best_corr = _evaluate_weights(all_data, current_w, current_adj)
    print(f"  Converged after {iteration} iterations")
    print(f"  Best avg Spearman: {best_corr:.3f}")

    # Round to nearest 5% for practical use
    rounded_w = {}
    for f in FACTOR_NAMES:
        r = round(current_w[f] * 20) / 20  # round to 0.05
        rounded_w[f] = max(0.0, r)
    # Renormalize
    total = sum(rounded_w.values())
    if total > 0:
        rounded_w = {k: round(v / total, 2) for k, v in rounded_w.items()}
    # Fix rounding to sum to exactly 1.0
    diff = 1.0 - sum(rounded_w.values())
    if abs(diff) > 0.001:
        max_f = max(rounded_w, key=rounded_w.get)
        rounded_w[max_f] = round(rounded_w[max_f] + diff, 2)

    rounded_corr = _evaluate_weights(all_data, rounded_w, current_adj)

    # Per-period breakdown
    period_corrs = {}
    for months, records in sorted(all_data.items()):
        if len(records) < 10:
            continue
        scores = _compute_weighted_scores(records, rounded_w, current_adj)
        returns = [r["actual_return"] for r in records]
        corr = _spearman_correlation(scores, returns)
        period_corrs[months] = round(corr, 3)

    return {
        "weights_exact": {k: round(v, 4) for k, v in current_w.items()},
        "weights_rounded": rounded_w,
        "adj_multiplier": current_adj,
        "avg_spearman_exact": round(best_corr, 3),
        "avg_spearman_rounded": round(rounded_corr, 3),
        "per_period_spearman": period_corrs,
        "n_stocks_per_period": {m: len(r) for m, r in all_data.items()},
    }


# =========================================================================
# MAIN ENTRY POINT
# =========================================================================

def run_multi_year_optimization(periods_months=None, step=0.05):
    """Full pipeline: collect data across periods, analyze, optimize.

    Args:
        periods_months: lookback periods in months (default [12, 24, 36, 48, 60])
        step: grid search step size (default 0.05)

    Returns:
        dict with optimized weights and analysis
    """
    # Step 1: Collect data
    all_data = collect_all_periods(periods_months)

    # Step 2: Per-factor correlations
    print(f"\n{'='*60}")
    print("FACTOR-RETURN CORRELATIONS BY PERIOD")
    print(f"{'='*60}")
    fcorrs = factor_correlations(all_data)
    print(f"{'Factor':<16}", end="")
    periods = sorted(all_data.keys())
    for m in periods:
        print(f"  {m//12}y", end="")
    print("   Avg")
    print("-" * (16 + len(periods) * 6 + 8))

    for f in FACTOR_NAMES + ADJUSTMENT_NAMES:
        print(f"{f:<16}", end="")
        corrs = [c for _, c in fcorrs[f]]
        for _, c in fcorrs[f]:
            print(f" {c:+.2f}", end="")
        avg_c = np.mean(corrs) if corrs else 0
        print(f"  {avg_c:+.3f}")

    # Step 3: Optimize
    result = optimize_weights(all_data, step=step)

    # Step 4: Print results
    print(f"\n{'='*60}")
    print("OPTIMIZATION RESULTS")
    print(f"{'='*60}")
    print(f"\nAvg Spearman (exact):   {result['avg_spearman_exact']:.3f}")
    print(f"Avg Spearman (rounded): {result['avg_spearman_rounded']:.3f}")
    print(f"Adjustment multiplier:  {result['adj_multiplier']}")

    print(f"\nOptimized weights (rounded to 5%):")
    for f in FACTOR_NAMES:
        pct = result['weights_rounded'][f] * 100
        bar = "█" * int(pct / 2.5)
        print(f"  {f:<14} {pct:5.1f}%  {bar}")

    print(f"\nPer-period Spearman:")
    for m, corr in sorted(result['per_period_spearman'].items()):
        n = result['n_stocks_per_period'][m]
        print(f"  {m//12}y lookback: {corr:+.3f}  (n={n})")

    # Step 5: Compare with current weights
    print(f"\n{'='*60}")
    print("COMPARISON: Current vs Optimized")
    print(f"{'='*60}")
    for strat in ["hold_forever", "cycle", "catalyst"]:
        current_w = STRATEGY_WEIGHTS[strat]
        curr_corr = _evaluate_weights(all_data, current_w, 1.0)
        opt_corr = _evaluate_weights(all_data, result['weights_rounded'], result['adj_multiplier'])
        print(f"  {strat:<14}: current={curr_corr:+.3f}  optimized={opt_corr:+.3f}  delta={opt_corr-curr_corr:+.3f}")

    # Step 6: Suggest strategy-specific weights
    print(f"\n{'='*60}")
    print("STRATEGY-SPECIFIC OPTIMIZATION")
    print(f"{'='*60}")
    strategy_weights = {}
    for strat in ["hold_forever", "cycle", "catalyst"]:
        # Filter data to only stocks of this strategy
        strat_data = {}
        for m, records in all_data.items():
            strat_records = [r for r in records if r["strategy"] == strat]
            if len(strat_records) >= 5:
                strat_data[m] = strat_records

        if len(strat_data) < 2:
            print(f"  {strat}: insufficient data for optimization")
            strategy_weights[strat] = result['weights_rounded']
            continue

        strat_result = optimize_weights(strat_data, step=0.10)  # coarser for smaller samples
        strategy_weights[strat] = strat_result['weights_rounded']

        print(f"\n  {strat} (n={sum(len(r) for r in strat_data.values())} stock-periods):")
        print(f"    Avg Spearman: {strat_result['avg_spearman_rounded']:.3f}")
        for f in FACTOR_NAMES:
            pct = strat_result['weights_rounded'][f] * 100
            if pct > 0:
                print(f"    {f:<14} {pct:5.1f}%")

    result["strategy_weights"] = strategy_weights
    result["all_data"] = all_data

    return result
