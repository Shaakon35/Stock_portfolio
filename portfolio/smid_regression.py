"""
Linear-regression factor weighting for the ranking model.

A faster alternative to the Spearman optimizer in ``smid_optimizer.py``.
Instead of searching for weights that maximize rank correlation, this fits

    return ~ w1*accel + w2*momentum + w3*growth + ... (+ adjustments)

directly via ordinary least squares (closed form, ``np.linalg.lstsq``).
The whole CV loop runs in seconds rather than minutes, and the coefficients
are directly interpretable: "a 1-point increase in <factor> predicts X% more
return".

Winsorizing of returns (capping at +/-cap%) is toggleable so you can compare
robust vs. raw fits. Disable it with ``--no-winsorize`` on the CLI or
``winsorize=False`` in code.

Shares preprocessing, metrics, factor definitions and reporting helpers with
``smid_optimizer`` so results are comparable across both approaches.

Usage (CLI):
    python -m portfolio.smid_regression                 # winsorize at +/-200%
    python -m portfolio.smid_regression --no-winsorize  # raw returns
    python -m portfolio.smid_regression --winsorize-cap 100
    python -m portfolio.smid_regression --metric pearson --per-strategy
"""

import argparse

import numpy as np

from portfolio.smid_data_fetcher import ADJUSTMENT_NAMES
from portfolio.smid_optimizer import (
    REDUCED_FACTORS,
    FULL_FACTORS,
    _compute_reduced_factors,
    preprocess,
    pearson,
    spearman,
    normalize_weights,
    round_weights,
    score_records,
    quintile_analysis,
    format_weights_table,
)


# =========================================================================
# DESIGN MATRIX
# =========================================================================

def _build_matrix(records, use_reduced=True, use_adjustments=False):
    """Build the (X, y, columns) design matrix from records.

    X has one column per factor (plus one per adjustment if requested) and a
    trailing intercept column. y is the actual (preprocessed) return.
    """
    factors = REDUCED_FACTORS if use_reduced else FULL_FACTORS
    columns = list(factors)
    if use_adjustments:
        columns = columns + list(ADJUSTMENT_NAMES)

    rows = []
    y = []
    for r in records:
        fvals = _compute_reduced_factors(r) if use_reduced else r
        row = [fvals.get(f, 0.0) for f in factors]
        if use_adjustments:
            row += [r.get(a, 0.0) for a in ADJUSTMENT_NAMES]
        row.append(1.0)  # intercept
        rows.append(row)
        y.append(r["actual_return"])

    X = np.asarray(rows, dtype=float)
    y = np.asarray(y, dtype=float)
    return X, y, columns


# =========================================================================
# FIT
# =========================================================================

def fit_regression(records, use_reduced=True, use_adjustments=False):
    """Closed-form OLS fit of returns on factor scores.

    Returns a dict with:
      - coefficients: raw OLS slope per factor (return-% per score point)
      - intercept:    OLS intercept
      - weights:      coefficients clipped at 0 and normalized to sum to 1
                      (comparable to optimizer output / ranking.py weights)
      - adj_multiplier: summed adjustment coefficient, for parity with the
                        optimizer's single ``adj_mult`` knob (0 if not used)
      - r_squared:    in-sample coefficient of determination
      - columns:      ordered factor (+adjustment) names
    """
    X, y, columns = _build_matrix(records, use_reduced, use_adjustments)

    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    coeffs = {columns[i]: float(beta[i]) for i in range(len(columns))}
    intercept = float(beta[-1])

    factors = REDUCED_FACTORS if use_reduced else FULL_FACTORS
    factor_coeffs = {f: coeffs[f] for f in factors}
    weights = normalize_weights(factor_coeffs, factors)

    if use_adjustments:
        adj_mult = float(np.mean([coeffs[a] for a in ADJUSTMENT_NAMES]))
    else:
        adj_mult = 0.0

    y_pred = X @ beta
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    return {
        "coefficients": factor_coeffs,
        "intercept": intercept,
        "weights": weights,
        "adj_multiplier": round(adj_mult, 4),
        "r_squared": round(r_squared, 4),
        "columns": columns,
    }


def evaluate(records, weights, adj_mult=0.0, metric="spearman", use_reduced=True):
    """Rank/linear correlation between weighted scores and actual returns."""
    if len(records) < 10:
        return -1.0
    scores = score_records(records, weights, adj_mult, use_reduced)
    returns = np.array([r["actual_return"] for r in records])
    if metric == "pearson":
        return pearson(scores, returns)
    return spearman(scores, returns)


# =========================================================================
# CROSS-VALIDATION
# =========================================================================

def cross_validate(records, n_splits=5, test_size=0.2, metric="spearman",
                   seed=42, use_reduced=True, winsorize=True,
                   winsorize_cap=200.0, sector_neutral=True,
                   use_adjustments=False):
    """Repeated 80/20 cross-validation using OLS fits.

    Set ``winsorize=False`` to fit on raw returns (no +/-cap clipping).
    """
    factors = REDUCED_FACTORS if use_reduced else FULL_FACTORS

    print("Preprocessing...")
    cap = winsorize_cap if winsorize else float("inf")
    processed = preprocess(records, winsorize_cap=cap,
                           sector_neutral=sector_neutral)
    if not winsorize:
        print("  Winsorizing disabled (using raw returns)")

    rng = np.random.RandomState(seed)
    n = len(processed)
    test_n = int(n * test_size)

    split_results = []
    all_weights = []

    for split_idx in range(n_splits):
        indices = np.arange(n)
        rng.shuffle(indices)

        train_idx = indices[:n - test_n]
        test_idx = indices[n - test_n:]

        train = [processed[i] for i in train_idx]
        test = [processed[i] for i in test_idx]

        print(f"\n--- Split {split_idx+1}/{n_splits}: "
              f"train={len(train)}, test={len(test)} ---")

        fit = fit_regression(train, use_reduced=use_reduced,
                             use_adjustments=use_adjustments)
        weights = fit["weights"]
        adj_mult = fit["adj_multiplier"]

        train_corr = evaluate(train, weights, adj_mult, metric, use_reduced)
        oos_corr = evaluate(test, weights, adj_mult, metric, use_reduced)
        other_metric = "pearson" if metric == "spearman" else "spearman"
        oos_other = evaluate(test, weights, adj_mult, other_metric, use_reduced)

        rounded_w = round_weights(weights, factors)
        all_weights.append(rounded_w)

        result = {
            "split": split_idx + 1,
            "train_n": len(train),
            "test_n": len(test),
            "train_r_squared": fit["r_squared"],
            f"train_{metric}": round(train_corr, 4),
            f"test_{metric}": round(oos_corr, 4),
            f"test_{other_metric}": round(oos_other, 4),
            "adj_multiplier": round(adj_mult, 4),
            "weights": rounded_w,
        }
        split_results.append(result)

        print(f"  Train R^2:   {fit['r_squared']:+.4f}")
        print(f"  Train {metric}: {train_corr:+.4f}")
        print(f"  Test  {metric}: {oos_corr:+.4f}")
        print(f"  Test  {other_metric}: {oos_other:+.4f}")
        top3 = sorted(rounded_w.items(), key=lambda x: -x[1])[:3]
        print(f"  Top weights: {', '.join(f'{f}={v:.0%}' for f,v in top3)}")

    # Average weights across splits
    avg_weights = {f: float(np.mean([w[f] for w in all_weights])) for f in factors}
    avg_weights = round_weights(avg_weights, factors)

    avg_adj = float(np.mean([sr["adj_multiplier"] for sr in split_results]))

    test_corrs = [sr[f"test_{metric}"] for sr in split_results]
    train_corrs = [sr[f"train_{metric}"] for sr in split_results]
    r2s = [sr["train_r_squared"] for sr in split_results]

    return {
        "split_results": split_results,
        "avg_weights": avg_weights,
        "avg_adj_multiplier": round(avg_adj, 4),
        f"mean_test_{metric}": round(float(np.mean(test_corrs)), 4),
        f"std_test_{metric}": round(float(np.std(test_corrs)), 4),
        f"mean_train_{metric}": round(float(np.mean(train_corrs)), 4),
        "mean_train_r_squared": round(float(np.mean(r2s)), 4),
        "overfit_gap": round(float(np.mean(train_corrs) - np.mean(test_corrs)), 4),
        "n_splits": n_splits,
        "metric": metric,
        "factors_used": factors,
        "winsorize": winsorize,
        "winsorize_cap": winsorize_cap if winsorize else None,
    }


def strategy_cv(records, n_splits=5, metric="spearman", use_reduced=True,
                winsorize=True, winsorize_cap=200.0, sector_neutral=True,
                use_adjustments=False):
    """Run regression CV separately for each strategy type."""
    strategies = ["hold_forever", "cycle", "catalyst"]
    results = {}

    for strat in strategies:
        strat_records = [r for r in records if r["strategy"] == strat]
        print(f"\n{'='*60}")
        print(f"STRATEGY: {strat} ({len(strat_records)} observations)")
        print(f"{'='*60}")

        if len(strat_records) < 30:
            print("  Too few observations, skipping")
            results[strat] = None
            continue

        results[strat] = cross_validate(
            strat_records, n_splits=n_splits, metric=metric,
            use_reduced=use_reduced, winsorize=winsorize,
            winsorize_cap=winsorize_cap, sector_neutral=sector_neutral,
            use_adjustments=use_adjustments,
        )

    return results


# =========================================================================
# CLI
# =========================================================================

def _parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Linear-regression factor weighting (OLS) for the ranking model.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--csv", default=None,
                   help="Path to cached data CSV (defaults to output/smid_optimization_data.csv)")
    p.add_argument("--max-tickers", type=int, default=None,
                   help="Limit tickers when fetching (only used if no CSV cache exists)")

    cap = p.add_mutually_exclusive_group()
    cap.add_argument("--winsorize-cap", type=float, default=200.0,
                     help="Cap returns at +/- this percent before fitting")
    cap.add_argument("--no-winsorize", dest="winsorize", action="store_false",
                     help="Disable winsorizing; fit on raw returns")
    p.set_defaults(winsorize=True)

    p.add_argument("--no-sector-neutral", dest="sector_neutral",
                   action="store_false",
                   help="Disable sector neutralization of returns")
    p.set_defaults(sector_neutral=True)

    p.add_argument("--metric", choices=["spearman", "pearson"],
                   default="spearman", help="Out-of-sample reporting metric")
    p.add_argument("--n-splits", type=int, default=5,
                   help="Number of 80/20 CV splits")
    p.add_argument("--seed", type=int, default=42, help="RNG seed for splits")
    p.add_argument("--full-factors", action="store_true",
                   help="Use all 9 factors instead of the 7 reduced ones")
    p.add_argument("--with-adjustments", action="store_true",
                   help="Include profitability/fragility/downside adjustments in the fit")
    p.add_argument("--per-strategy", action="store_true",
                   help="Also run a separate fit per strategy")
    p.add_argument("--quintiles", action="store_true",
                   help="Print quintile analysis on raw returns with fitted weights")
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)

    # Lazy import so fetching deps aren't required just to import the module.
    from portfolio.smid_data_fetcher import load_csv, fetch_all

    records = load_csv(args.csv) if args.csv else load_csv()
    if not records:
        print("No cached data found; fetching (this can take a while)...")
        records = fetch_all(periods=[12, 24, 36], force_refresh=False,
                            max_tickers=args.max_tickers)

    if not records:
        print("No records available. Aborting.")
        return 1

    use_reduced = not args.full_factors

    print(f"\nLoaded {len(records)} records.")
    print(f"Winsorize: {'OFF (raw returns)' if not args.winsorize else f'+/-{args.winsorize_cap}%'}")
    print(f"Sector-neutral: {args.sector_neutral}")
    print(f"Factors: {'9 full' if args.full_factors else '7 reduced'}"
          f"{' + adjustments' if args.with_adjustments else ''}")

    cv_result = cross_validate(
        records, n_splits=args.n_splits, metric=args.metric, seed=args.seed,
        use_reduced=use_reduced, winsorize=args.winsorize,
        winsorize_cap=args.winsorize_cap, sector_neutral=args.sector_neutral,
        use_adjustments=args.with_adjustments,
    )

    metric = cv_result["metric"]
    print(f"\n{'='*60}")
    print("SUMMARY (regression, all strategies pooled)")
    print(f"{'='*60}")
    print(f"Mean test {metric}:  {cv_result[f'mean_test_{metric}']:+.4f} "
          f"(+/-{cv_result[f'std_test_{metric}']:.4f})")
    print(f"Mean train {metric}: {cv_result[f'mean_train_{metric}']:+.4f}")
    print(f"Mean train R^2:     {cv_result['mean_train_r_squared']:+.4f}")
    print(f"Overfit gap:        {cv_result['overfit_gap']:+.4f}")
    print(f"Adj multiplier:     {cv_result['avg_adj_multiplier']:.4f}")
    print(f"\nOptimal weights:")
    for f in cv_result["factors_used"]:
        print(f"  {f:<22} {cv_result['avg_weights'][f]*100:>5.1f}%")

    if args.per_strategy:
        strat_results = strategy_cv(
            records, n_splits=args.n_splits, metric=args.metric,
            use_reduced=use_reduced, winsorize=args.winsorize,
            winsorize_cap=args.winsorize_cap, sector_neutral=args.sector_neutral,
            use_adjustments=args.with_adjustments,
        )
        print(format_weights_table(cv_result, strat_results))

    if args.quintiles:
        print("\n=== QUINTILE ANALYSIS (raw returns, fitted weights) ===")
        quintile_analysis(
            records, cv_result["avg_weights"],
            adj_mult=cv_result["avg_adj_multiplier"],
            use_reduced=use_reduced,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
