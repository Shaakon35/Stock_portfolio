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
        # Full beta (incl. adjustments + trailing intercept) for exact
        # out-of-sample prediction via predict_returns().
        "beta": beta.tolist(),
        "use_reduced": use_reduced,
        "use_adjustments": use_adjustments,
    }


def predict_returns(records, fit):
    """Predict returns for records using a fitted model (raw OLS prediction).

    Uses the full beta (factors + adjustments + intercept), so the output is
    in actual return-% units — suitable for RMSE/MAE against actual returns.
    """
    X, _, _ = _build_matrix(records, fit["use_reduced"], fit["use_adjustments"])
    beta = np.asarray(fit["beta"], dtype=float)
    return X @ beta


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
# REGRESSION ERROR METRICS (RMSE / MAE)
# =========================================================================

def rmse(y_true, y_pred):
    """Root mean squared error (in return-% units)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true, y_pred):
    """Mean absolute error (in return-% units)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean(np.abs(y_true - y_pred)))


# =========================================================================
# ROC / AUC (treats ranking as a binary classifier)
# =========================================================================

def roc_curve(scores, labels):
    """Compute ROC curve points (fpr, tpr) for binary labels.

    ``scores``: higher = more likely positive (the model's ranking).
    ``labels``: 1 for positive class, 0 for negative.
    Returns (fpr, tpr) arrays including the (0,0) and (1,1) endpoints.
    Pure numpy, no sklearn.
    """
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=int)

    order = np.argsort(-scores)  # descending score
    labels = labels[order]

    P = int(labels.sum())
    N = int(len(labels) - P)
    if P == 0 or N == 0:
        # Degenerate: only one class present
        return np.array([0.0, 1.0]), np.array([0.0, 1.0])

    tps = np.cumsum(labels)
    fps = np.cumsum(1 - labels)

    tpr = np.concatenate([[0.0], tps / P])
    fpr = np.concatenate([[0.0], fps / N])
    return fpr, tpr


def auc_score(scores, labels):
    """Area under the ROC curve.

    Equivalent to P(score(positive) > score(negative)) — the probability
    that a randomly chosen winner outranks a randomly chosen loser.
    Computed via the rank-based (Mann-Whitney U) formula, which handles
    ties correctly. Returns 0.5 for no skill, 1.0 for perfect ranking.
    """
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=int)

    P = int(labels.sum())
    N = int(len(labels) - P)
    if P == 0 or N == 0:
        return float("nan")

    # Average ranks (1..n), ties share the mean rank
    order = np.argsort(scores)
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    # Resolve ties to average rank
    _, inv, counts = np.unique(scores, return_inverse=True, return_counts=True)
    sums = np.zeros(len(counts))
    np.add.at(sums, inv, ranks)
    avg = sums / counts
    ranks = avg[inv]

    sum_pos = ranks[labels == 1].sum()
    auc = (sum_pos - P * (P + 1) / 2.0) / (P * N)
    return float(auc)


def binarize_returns(records, threshold=0.0):
    """Label each record 1 if its (preprocessed) return > threshold else 0.

    With sector-neutralized returns, threshold=0 means "beat the sector
    median" — i.e. a relative winner. This is the natural binary target
    for ROC/AUC on a stock-ranking model.
    """
    return np.array([1 if r["actual_return"] > threshold else 0
                     for r in records], dtype=int)


# =========================================================================
# CROSS-VALIDATION
# =========================================================================

def cross_validate(records, n_splits=5, test_size=0.2, metric="spearman",
                   seed=42, use_reduced=True, winsorize=True,
                   winsorize_cap=200.0, sector_neutral=True,
                   use_adjustments=False, min_test_size=15):
    """Repeated 80/20 cross-validation using OLS fits.

    Set ``winsorize=False`` to fit on raw returns (no +/-cap clipping).

    ``min_test_size`` guards against tiny test folds: with very few test
    points the rank correlation snaps to +/-1 and is meaningless. If the
    held-out fold would be smaller than this, the whole run is treated as
    insufficient data and ``None`` is returned (callers handle None).
    """
    factors = REDUCED_FACTORS if use_reduced else FULL_FACTORS

    n = len(records)
    test_n = int(n * test_size)
    if test_n < min_test_size:
        print(f"  Insufficient data: test fold would be {test_n} "
              f"(< min_test_size={min_test_size}). Skipping — results would "
              f"be statistical noise. Fetch more tickers.")
        return None

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

        # RMSE / MAE on actual return-% (raw OLS prediction)
        y_test = np.array([r["actual_return"] for r in test])
        y_pred = predict_returns(test, fit)
        test_rmse = rmse(y_test, y_pred)
        test_mae = mae(y_test, y_pred)

        # AUC: can the score rank winners (return > 0) above losers?
        labels = binarize_returns(test, threshold=0.0)
        test_scores = score_records(test, weights, adj_mult, use_reduced)
        test_auc = auc_score(test_scores, labels)

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
            "test_rmse": round(test_rmse, 2),
            "test_mae": round(test_mae, 2),
            "test_auc": round(test_auc, 4) if test_auc == test_auc else None,
            "adj_multiplier": round(adj_mult, 4),
            "weights": rounded_w,
        }
        split_results.append(result)

        print(f"  Train R^2:   {fit['r_squared']:+.4f}")
        print(f"  Train {metric}: {train_corr:+.4f}")
        print(f"  Test  {metric}: {oos_corr:+.4f}")
        print(f"  Test  {other_metric}: {oos_other:+.4f}")
        print(f"  Test  RMSE:  {test_rmse:.1f}%   MAE: {test_mae:.1f}%   "
              f"AUC: {test_auc:.4f}")
        top3 = sorted(rounded_w.items(), key=lambda x: -x[1])[:3]
        print(f"  Top weights: {', '.join(f'{f}={v:.0%}' for f,v in top3)}")

    # Average weights across splits
    avg_weights = {f: float(np.mean([w[f] for w in all_weights])) for f in factors}
    avg_weights = round_weights(avg_weights, factors)

    avg_adj = float(np.mean([sr["adj_multiplier"] for sr in split_results]))

    test_corrs = [sr[f"test_{metric}"] for sr in split_results]
    train_corrs = [sr[f"train_{metric}"] for sr in split_results]
    r2s = [sr["train_r_squared"] for sr in split_results]
    rmses = [sr["test_rmse"] for sr in split_results]
    maes = [sr["test_mae"] for sr in split_results]
    aucs = [sr["test_auc"] for sr in split_results if sr["test_auc"] is not None]

    return {
        "split_results": split_results,
        "avg_weights": avg_weights,
        "avg_adj_multiplier": round(avg_adj, 4),
        f"mean_test_{metric}": round(float(np.mean(test_corrs)), 4),
        f"std_test_{metric}": round(float(np.std(test_corrs)), 4),
        f"mean_train_{metric}": round(float(np.mean(train_corrs)), 4),
        "mean_train_r_squared": round(float(np.mean(r2s)), 4),
        "mean_test_rmse": round(float(np.mean(rmses)), 2),
        "std_test_rmse": round(float(np.std(rmses)), 2),
        "mean_test_mae": round(float(np.mean(maes)), 2),
        "mean_test_auc": round(float(np.mean(aucs)), 4) if aucs else None,
        "std_test_auc": round(float(np.std(aucs)), 4) if aucs else None,
        "overfit_gap": round(float(np.mean(train_corrs) - np.mean(test_corrs)), 4),
        "n_splits": n_splits,
        "metric": metric,
        "factors_used": factors,
        "winsorize": winsorize,
        "winsorize_cap": winsorize_cap if winsorize else None,
    }


def strategy_cv(records, n_splits=5, metric="spearman", use_reduced=True,
                winsorize=True, winsorize_cap=200.0, sector_neutral=True,
                use_adjustments=False, min_test_size=15, min_observations=100):
    """Run regression CV separately for each strategy type.

    A strategy is skipped unless it has at least ``min_observations`` rows.
    Per-strategy results below ~100 observations are dominated by noise (a
    20% test fold has too few points for a stable rank correlation), so they
    are reported as insufficient data rather than misleading +/-1.0 values.
    """
    strategies = ["hold_forever", "cycle", "catalyst"]
    results = {}

    for strat in strategies:
        strat_records = [r for r in records if r["strategy"] == strat]
        print(f"\n{'='*60}")
        print(f"STRATEGY: {strat} ({len(strat_records)} observations)")
        print(f"{'='*60}")

        if len(strat_records) < min_observations:
            print(f"  Insufficient data ({len(strat_records)} < "
                  f"{min_observations}), skipping — too few for a stable "
                  f"out-of-sample estimate.")
            results[strat] = None
            continue

        results[strat] = cross_validate(
            strat_records, n_splits=n_splits, metric=metric,
            use_reduced=use_reduced, winsorize=winsorize,
            winsorize_cap=winsorize_cap, sector_neutral=sector_neutral,
            use_adjustments=use_adjustments, min_test_size=min_test_size,
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

    if cv_result is None:
        print("\nNot enough data for a valid cross-validation. "
              "Fetch more tickers (set MAX_TICKERS=None / --max-tickers).")
        return 1

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
