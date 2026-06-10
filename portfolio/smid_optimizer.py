"""
80/20 Cross-Validated Weight Optimizer for the Ranking Model.

Optimizes factor weights to maximize Pearson correlation between
composite score and actual forward returns.

Anti-overfitting measures:
- 80/20 train/test split (repeated 5x with different seeds)
- Weight smoothing (5% granularity)
- Regularization toward equal weights
- Reports both train and test correlations to detect overfitting
"""

import numpy as np
from scipy.optimize import minimize
from portfolio.smid_data_fetcher import FACTOR_NAMES, ADJUSTMENT_NAMES


def pearson(x, y):
    """Pearson correlation coefficient."""
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    if len(x) < 5:
        return 0.0
    mx, my = np.mean(x), np.mean(y)
    sx, sy = np.std(x), np.std(y)
    if sx == 0 or sy == 0:
        return 0.0
    return np.mean((x - mx) * (y - my)) / (sx * sy)


def spearman(x, y):
    """Spearman rank correlation."""
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)
    if n < 5:
        return 0.0
    def _rank(arr):
        s = np.argsort(arr)
        r = np.empty_like(s, dtype=float)
        r[s] = np.arange(1, n + 1)
        return r
    rx, ry = _rank(x), _rank(y)
    d2 = np.sum((rx - ry) ** 2)
    return 1 - (6 * d2) / (n * (n**2 - 1))


def score_records(records, weights, adj_mult=1.0):
    """Compute composite scores for records given factor weights."""
    scores = []
    for r in records:
        sc = sum(r[f] * weights.get(f, 0) for f in FACTOR_NAMES)
        adj = sum(r[f] for f in ADJUSTMENT_NAMES)
        sc += adj * adj_mult
        scores.append(sc)
    return np.array(scores)


def evaluate(records, weights, adj_mult=1.0, metric="pearson"):
    """Correlation between weighted scores and actual returns."""
    if len(records) < 10:
        return -1.0
    scores = score_records(records, weights, adj_mult)
    returns = np.array([r["actual_return"] for r in records])
    if metric == "pearson":
        return pearson(scores, returns)
    return spearman(scores, returns)


def normalize_weights(w):
    """Normalize weight dict to sum to 1.0."""
    total = sum(abs(v) for v in w.values())
    if total <= 0:
        n = len(w)
        return {k: 1.0 / n for k in w}
    return {k: max(0, v) / total for k, v in w.items()}


def round_weights(w, granularity=0.05):
    """Round weights to nearest granularity and renormalize."""
    rounded = {}
    for f in FACTOR_NAMES:
        r = round(w.get(f, 0) / granularity) * granularity
        rounded[f] = max(0.0, r)
    total = sum(rounded.values())
    if total <= 0:
        return {f: 1.0 / len(FACTOR_NAMES) for f in FACTOR_NAMES}
    rounded = {k: v / total for k, v in rounded.items()}
    # Fix rounding
    diff = 1.0 - sum(rounded.values())
    if abs(diff) > 0.001:
        max_f = max(rounded, key=rounded.get)
        rounded[max_f] += diff
    return {k: round(v, 4) for k, v in rounded.items()}


def optimize_weights(train_records, metric="pearson", reg_strength=0.01):
    """Find optimal weights using scipy minimize + coordinate descent.

    Uses L-BFGS-B with bounds [0, 1] for each factor weight.
    Adds L2 regularization toward equal weights to prevent overfitting.

    Returns (best_weights, best_adj_mult, train_correlation).
    """
    n_factors = len(FACTOR_NAMES)
    equal_w = 1.0 / n_factors

    best_corr = -1.0
    best_weights = {f: equal_w for f in FACTOR_NAMES}
    best_adj = 1.0

    for adj_mult in [0.0, 0.5, 1.0, 1.5]:
        def objective(x):
            w = {FACTOR_NAMES[i]: x[i] for i in range(n_factors)}
            w = normalize_weights(w)
            corr = evaluate(train_records, w, adj_mult, metric)
            # L2 regularization toward equal weights
            reg = reg_strength * sum((x[i] - equal_w)**2 for i in range(n_factors))
            return -(corr - reg)

        # Multiple random starts
        for seed in range(5):
            rng = np.random.RandomState(seed)
            x0 = rng.dirichlet(np.ones(n_factors))
            bounds = [(0.0, 1.0)] * n_factors

            try:
                result = minimize(objective, x0, method="L-BFGS-B", bounds=bounds,
                                  options={"maxiter": 500, "ftol": 1e-8})
                w = {FACTOR_NAMES[i]: result.x[i] for i in range(n_factors)}
                w = normalize_weights(w)
                corr = evaluate(train_records, w, adj_mult, metric)
                if corr > best_corr:
                    best_corr = corr
                    best_weights = w
                    best_adj = adj_mult
            except Exception:
                pass

    # Coordinate descent refinement (1% steps)
    current_w = dict(best_weights)
    improved = True
    iters = 0
    while improved and iters < 30:
        improved = False
        iters += 1
        for f in FACTOR_NAMES:
            best_val = current_w[f]
            best_c = evaluate(train_records, normalize_weights(current_w), best_adj, metric)
            for pct in range(0, 61):
                old = current_w[f]
                current_w[f] = pct / 100.0
                test_w = normalize_weights(current_w)
                c = evaluate(train_records, test_w, best_adj, metric)
                if c > best_c + 0.0001:  # require meaningful improvement
                    best_c = c
                    best_val = pct / 100.0
                current_w[f] = old
            if abs(best_val - current_w[f]) > 0.005:
                current_w[f] = best_val
                current_w = normalize_weights(current_w)
                improved = True

    final_corr = evaluate(train_records, current_w, best_adj, metric)
    if final_corr > best_corr:
        best_weights = current_w
        best_corr = final_corr

    return best_weights, best_adj, best_corr


def cross_validate(records, n_splits=5, test_size=0.2, metric="pearson", seed=42):
    """Repeated 80/20 cross-validation.

    For each split:
    - Randomly shuffle and split 80% train / 20% test
    - Optimize weights on train
    - Evaluate on test (out-of-sample)

    Returns dict with per-split results, averaged weights, and summary stats.
    """
    rng = np.random.RandomState(seed)
    n = len(records)
    test_n = int(n * test_size)
    train_n = n - test_n

    split_results = []
    all_weights = []

    for split_idx in range(n_splits):
        # Shuffle with different seed each split
        indices = np.arange(n)
        rng.shuffle(indices)

        train_idx = indices[:train_n]
        test_idx = indices[train_n:]

        train = [records[i] for i in train_idx]
        test = [records[i] for i in test_idx]

        print(f"\n--- Split {split_idx+1}/{n_splits}: train={len(train)}, test={len(test)} ---")

        # Optimize on train
        weights, adj_mult, train_corr = optimize_weights(train, metric=metric)

        # Evaluate on test (out-of-sample)
        oos_corr = evaluate(test, weights, adj_mult, metric)
        oos_spearman = evaluate(test, weights, adj_mult, "spearman")

        rounded_w = round_weights(weights)
        all_weights.append(rounded_w)

        result = {
            "split": split_idx + 1,
            "train_n": len(train),
            "test_n": len(test),
            f"train_{metric}": round(train_corr, 4),
            f"test_{metric}": round(oos_corr, 4),
            "test_spearman": round(oos_spearman, 4),
            "adj_multiplier": round(adj_mult, 2),
            "weights": rounded_w,
        }
        split_results.append(result)

        print(f"  Train {metric}: {train_corr:+.4f}")
        print(f"  Test  {metric}: {oos_corr:+.4f}")
        print(f"  Test  spearman: {oos_spearman:+.4f}")
        top3 = sorted(rounded_w.items(), key=lambda x: -x[1])[:3]
        print(f"  Top weights: {', '.join(f'{f}={v:.0%}' for f,v in top3)}")

    # Average weights across splits
    avg_weights = {}
    for f in FACTOR_NAMES:
        avg_weights[f] = np.mean([w[f] for w in all_weights])
    avg_weights = round_weights(avg_weights)

    avg_adj = np.mean([sr["adj_multiplier"] for sr in split_results])

    # Summary
    test_corrs = [sr[f"test_{metric}"] for sr in split_results]
    train_corrs = [sr[f"train_{metric}"] for sr in split_results]

    return {
        "split_results": split_results,
        "avg_weights": avg_weights,
        "avg_adj_multiplier": round(avg_adj, 2),
        f"mean_test_{metric}": round(np.mean(test_corrs), 4),
        f"std_test_{metric}": round(np.std(test_corrs), 4),
        f"mean_train_{metric}": round(np.mean(train_corrs), 4),
        "overfit_gap": round(np.mean(train_corrs) - np.mean(test_corrs), 4),
        "n_splits": n_splits,
        "metric": metric,
    }


def strategy_cv(records, n_splits=5, metric="pearson"):
    """Run CV separately for each strategy type."""
    strategies = ["hold_forever", "cycle", "catalyst"]
    results = {}

    for strat in strategies:
        strat_records = [r for r in records if r["strategy"] == strat]
        print(f"\n{'='*60}")
        print(f"STRATEGY: {strat} ({len(strat_records)} observations)")
        print(f"{'='*60}")

        if len(strat_records) < 30:
            print(f"  Too few observations, skipping")
            results[strat] = None
            continue

        results[strat] = cross_validate(strat_records, n_splits=n_splits, metric=metric)

    return results


def format_weights_table(cv_result, strat_results=None):
    """Format results as a readable table."""
    lines = []
    lines.append("\n" + "="*70)
    lines.append("OPTIMIZED WEIGHTS (averaged across CV splits)")
    lines.append("="*70)

    # Overall
    w = cv_result["avg_weights"]
    metric = cv_result["metric"]
    lines.append(f"\nOverall (all strategies pooled):")
    lines.append(f"  Mean test {metric}: {cv_result[f'mean_test_{metric}']:+.4f} "
                 f"(±{cv_result[f'std_test_{metric}']:.4f})")
    lines.append(f"  Overfit gap: {cv_result['overfit_gap']:+.4f}")
    lines.append(f"  Adj multiplier: {cv_result['avg_adj_multiplier']:.2f}")
    lines.append("")

    header = f"  {'Factor':<14} {'Weight':>8}  {'Pct':>6}"
    lines.append(header)
    lines.append("  " + "-"*30)
    for f in FACTOR_NAMES:
        lines.append(f"  {f:<14} {w[f]:>8.4f}  {w[f]*100:>5.1f}%")

    # Per-strategy
    if strat_results:
        for strat, sr in strat_results.items():
            if sr is None:
                continue
            lines.append(f"\n{strat}:")
            sw = sr["avg_weights"]
            lines.append(f"  Mean test {metric}: {sr[f'mean_test_{metric}']:+.4f} "
                         f"(±{sr[f'std_test_{metric}']:.4f})")
            lines.append(f"  Overfit gap: {sr['overfit_gap']:+.4f}")
            lines.append("")
            lines.append(header)
            lines.append("  " + "-"*30)
            for f in FACTOR_NAMES:
                lines.append(f"  {f:<14} {sw[f]:>8.4f}  {sw[f]*100:>5.1f}%")

    return "\n".join(lines)
