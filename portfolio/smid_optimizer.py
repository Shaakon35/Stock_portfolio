"""
80/20 Cross-Validated Weight Optimizer for the Ranking Model.

Improvements over v1:
1. Multi-period support (12, 24, 36 month lookbacks)
2. Winsorized returns (capped at ±200%) to reduce outlier impact
3. Reduced factors: merged upside+conviction → "analyst_sentiment",
   dropped long_term and cash_runway (optimizer set them to 0%)
4. Spearman rank correlation as optimization target
5. Sector-neutralized returns to find stock-level signals
"""

import numpy as np
from scipy.optimize import minimize
from portfolio.smid_data_fetcher import FACTOR_NAMES as ALL_FACTOR_NAMES, ADJUSTMENT_NAMES


# --- Factor reduction ---
# Merge upside + conviction → analyst_sentiment (average of both)
# Keep long_term but expect low weight; drop cash_runway
REDUCED_FACTORS = [
    "analyst_sentiment",  # merged: (upside + conviction) / 2
    "growth",
    "accel",
    "valuation",
    "entry",
    "momentum",
    "long_term",
]

FULL_FACTORS = ALL_FACTOR_NAMES


def _compute_reduced_factors(record):
    """Compute reduced factor values from a full record."""
    return {
        "analyst_sentiment": (record["upside"] + record["conviction"]) / 2,
        "growth": record["growth"],
        "accel": record["accel"],
        "valuation": record["valuation"],
        "entry": record["entry"],
        "momentum": record["momentum"],
        "long_term": record["long_term"],
    }


# =========================================================================
# PREPROCESSING
# =========================================================================

def winsorize_returns(records, cap=200.0):
    """Cap returns at +/-cap% to reduce outlier impact."""
    out = []
    n_capped = 0
    for r in records:
        r2 = dict(r)
        if r2["actual_return"] > cap:
            r2["actual_return"] = cap
            n_capped += 1
        elif r2["actual_return"] < -cap:
            r2["actual_return"] = -cap
            n_capped += 1
        out.append(r2)
    if n_capped > 0:
        print(f"  Winsorized {n_capped}/{len(records)} returns to +/-{cap}%")
    return out


def neutralize_by_sector(records):
    """Subtract sector median return from each stock's return.

    Forces the optimizer to find stock-level signals rather than
    learning "buy sector X, sell sector Y".
    """
    groups = {}
    for r in records:
        key = (r.get("basket", ""), r["period_months"])
        if key not in groups:
            groups[key] = []
        groups[key].append(r["actual_return"])

    medians = {k: np.median(v) for k, v in groups.items()}

    out = []
    for r in records:
        r2 = dict(r)
        key = (r2.get("basket", ""), r2["period_months"])
        r2["actual_return"] = r2["actual_return"] - medians[key]
        out.append(r2)

    print(f"  Sector-neutralized returns across {len(medians)} (basket, period) groups")
    return out


def preprocess(records, winsorize_cap=200.0, sector_neutral=True):
    """Apply all preprocessing steps."""
    out = winsorize_returns(records, cap=winsorize_cap)
    if sector_neutral:
        out = neutralize_by_sector(out)
    return out


# =========================================================================
# CORRELATION METRICS
# =========================================================================

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


# =========================================================================
# SCORING
# =========================================================================

def score_records(records, weights, adj_mult=0.0, use_reduced=True):
    """Compute composite scores for records given factor weights."""
    scores = []
    if use_reduced:
        for r in records:
            rf = _compute_reduced_factors(r)
            sc = sum(rf.get(f, 0) * weights.get(f, 0) for f in REDUCED_FACTORS)
            if adj_mult != 0:
                adj = sum(r.get(f, 0) for f in ADJUSTMENT_NAMES)
                sc += adj * adj_mult
            scores.append(sc)
    else:
        for r in records:
            sc = sum(r.get(f, 0) * weights.get(f, 0) for f in FULL_FACTORS)
            if adj_mult != 0:
                adj = sum(r.get(f, 0) for f in ADJUSTMENT_NAMES)
                sc += adj * adj_mult
            scores.append(sc)
    return np.array(scores)


def evaluate(records, weights, adj_mult=0.0, metric="spearman", use_reduced=True):
    """Correlation between weighted scores and actual returns."""
    if len(records) < 10:
        return -1.0
    scores = score_records(records, weights, adj_mult, use_reduced)
    returns = np.array([r["actual_return"] for r in records])
    if metric == "pearson":
        return pearson(scores, returns)
    return spearman(scores, returns)


# =========================================================================
# WEIGHT UTILITIES
# =========================================================================

def normalize_weights(w, factors=None):
    """Normalize weight dict to sum to 1.0."""
    if factors is None:
        factors = list(w.keys())
    total = sum(abs(w.get(f, 0)) for f in factors)
    if total <= 0:
        n = len(factors)
        return {f: 1.0 / n for f in factors}
    return {f: max(0, w.get(f, 0)) / total for f in factors}


def round_weights(w, factors=None, granularity=0.05):
    """Round weights to nearest granularity and renormalize."""
    if factors is None:
        factors = list(w.keys())
    rounded = {}
    for f in factors:
        r = round(w.get(f, 0) / granularity) * granularity
        rounded[f] = max(0.0, r)
    total = sum(rounded.values())
    if total <= 0:
        return {f: 1.0 / len(factors) for f in factors}
    rounded = {f: v / total for f, v in rounded.items()}
    diff = 1.0 - sum(rounded.values())
    if abs(diff) > 0.001:
        max_f = max(rounded, key=rounded.get)
        rounded[max_f] += diff
    return {f: round(v, 4) for f, v in rounded.items()}


# =========================================================================
# OPTIMIZER
# =========================================================================

def optimize_weights(train_records, metric="spearman", reg_strength=0.01,
                     use_reduced=True):
    """Find optimal weights using scipy minimize + coordinate descent."""
    factors = REDUCED_FACTORS if use_reduced else FULL_FACTORS
    n_factors = len(factors)
    equal_w = 1.0 / n_factors

    best_corr = -1.0
    best_weights = {f: equal_w for f in factors}
    best_adj = 0.0

    for adj_mult in [0.0, 0.5, 1.0]:
        def objective(x):
            w = {factors[i]: x[i] for i in range(n_factors)}
            w = normalize_weights(w, factors)
            corr = evaluate(train_records, w, adj_mult, metric, use_reduced)
            reg = reg_strength * sum((x[i] - equal_w)**2 for i in range(n_factors))
            return -(corr - reg)

        for seed in range(5):
            rng = np.random.RandomState(seed)
            x0 = rng.dirichlet(np.ones(n_factors))
            bounds = [(0.0, 1.0)] * n_factors
            try:
                result = minimize(objective, x0, method="L-BFGS-B", bounds=bounds,
                                  options={"maxiter": 500, "ftol": 1e-8})
                w = {factors[i]: result.x[i] for i in range(n_factors)}
                w = normalize_weights(w, factors)
                corr = evaluate(train_records, w, adj_mult, metric, use_reduced)
                if corr > best_corr:
                    best_corr = corr
                    best_weights = w
                    best_adj = adj_mult
            except Exception:
                pass

    # Coordinate descent refinement
    current_w = dict(best_weights)
    improved = True
    iters = 0
    while improved and iters < 30:
        improved = False
        iters += 1
        for f in factors:
            best_val = current_w[f]
            best_c = evaluate(train_records, normalize_weights(current_w, factors),
                              best_adj, metric, use_reduced)
            for pct in range(0, 61):
                old = current_w[f]
                current_w[f] = pct / 100.0
                test_w = normalize_weights(current_w, factors)
                c = evaluate(train_records, test_w, best_adj, metric, use_reduced)
                if c > best_c + 0.0001:
                    best_c = c
                    best_val = pct / 100.0
                current_w[f] = old
            if abs(best_val - current_w[f]) > 0.005:
                current_w[f] = best_val
                current_w = normalize_weights(current_w, factors)
                improved = True

    final_corr = evaluate(train_records, current_w, best_adj, metric, use_reduced)
    if final_corr > best_corr:
        best_weights = current_w
        best_corr = final_corr

    return best_weights, best_adj, best_corr


# =========================================================================
# CROSS-VALIDATION
# =========================================================================

def cross_validate(records, n_splits=5, test_size=0.2, metric="spearman",
                   seed=42, use_reduced=True, winsorize_cap=200.0,
                   sector_neutral=True):
    """Repeated 80/20 cross-validation with preprocessing."""
    factors = REDUCED_FACTORS if use_reduced else FULL_FACTORS

    print("Preprocessing...")
    processed = preprocess(records, winsorize_cap=winsorize_cap,
                           sector_neutral=sector_neutral)

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

        print(f"\n--- Split {split_idx+1}/{n_splits}: train={len(train)}, test={len(test)} ---")

        weights, adj_mult, train_corr = optimize_weights(
            train, metric=metric, use_reduced=use_reduced
        )

        oos_corr = evaluate(test, weights, adj_mult, metric, use_reduced)
        other_metric = "pearson" if metric == "spearman" else "spearman"
        oos_other = evaluate(test, weights, adj_mult, other_metric, use_reduced)

        rounded_w = round_weights(weights, factors)
        all_weights.append(rounded_w)

        result = {
            "split": split_idx + 1,
            "train_n": len(train),
            "test_n": len(test),
            f"train_{metric}": round(train_corr, 4),
            f"test_{metric}": round(oos_corr, 4),
            f"test_{other_metric}": round(oos_other, 4),
            "adj_multiplier": round(adj_mult, 2),
            "weights": rounded_w,
        }
        split_results.append(result)

        print(f"  Train {metric}: {train_corr:+.4f}")
        print(f"  Test  {metric}: {oos_corr:+.4f}")
        print(f"  Test  {other_metric}: {oos_other:+.4f}")
        top3 = sorted(rounded_w.items(), key=lambda x: -x[1])[:3]
        print(f"  Top weights: {', '.join(f'{f}={v:.0%}' for f,v in top3)}")

    # Average weights
    avg_weights = {}
    for f in factors:
        avg_weights[f] = np.mean([w[f] for w in all_weights])
    avg_weights = round_weights(avg_weights, factors)

    avg_adj = np.mean([sr["adj_multiplier"] for sr in split_results])

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
        "factors_used": factors,
    }


def strategy_cv(records, n_splits=5, metric="spearman", use_reduced=True,
                winsorize_cap=200.0, sector_neutral=True):
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

        results[strat] = cross_validate(
            strat_records, n_splits=n_splits, metric=metric,
            use_reduced=use_reduced, winsorize_cap=winsorize_cap,
            sector_neutral=sector_neutral,
        )

    return results


# =========================================================================
# REPORTING
# =========================================================================

def format_weights_table(cv_result, strat_results=None):
    """Format results as a readable table."""
    lines = []
    metric = cv_result["metric"]
    factors = cv_result["factors_used"]

    lines.append("\n" + "="*70)
    lines.append("OPTIMIZED WEIGHTS (averaged across CV splits)")
    lines.append("="*70)

    w = cv_result["avg_weights"]
    lines.append(f"\nOverall (all strategies pooled):")
    lines.append(f"  Mean test {metric}: {cv_result[f'mean_test_{metric}']:+.4f} "
                 f"(+/-{cv_result[f'std_test_{metric}']:.4f})")
    lines.append(f"  Overfit gap: {cv_result['overfit_gap']:+.4f}")
    lines.append(f"  Adj multiplier: {cv_result['avg_adj_multiplier']:.2f}")
    lines.append("")

    header = f"  {'Factor':<22} {'Weight':>8}  {'Pct':>6}"
    lines.append(header)
    lines.append("  " + "-"*38)
    for f in factors:
        lines.append(f"  {f:<22} {w[f]:>8.4f}  {w[f]*100:>5.1f}%")

    if strat_results:
        for strat, sr in strat_results.items():
            if sr is None:
                continue
            lines.append(f"\n{strat}:")
            sw = sr["avg_weights"]
            lines.append(f"  Mean test {metric}: {sr[f'mean_test_{metric}']:+.4f} "
                         f"(+/-{sr[f'std_test_{metric}']:.4f})")
            lines.append(f"  Overfit gap: {sr['overfit_gap']:+.4f}")
            lines.append("")
            lines.append(header)
            lines.append("  " + "-"*38)
            for f in factors:
                lines.append(f"  {f:<22} {sw[f]:>8.4f}  {sw[f]*100:>5.1f}%")

    return "\n".join(lines)


def quintile_analysis(records, weights, adj_mult=0.0, use_reduced=True):
    """Compute quintile performance breakdown."""
    scores = score_records(records, weights, adj_mult, use_reduced)
    returns = np.array([r["actual_return"] for r in records])

    order = np.argsort(-scores)
    n = len(order)
    q_size = n // 5

    labels = ["Top 20%", "20-40%", "40-60%", "60-80%", "Bottom 20%"]
    quintiles = {}

    for i, label in enumerate(labels):
        start = i * q_size
        end = start + q_size if i < 4 else n
        idx = order[start:end]
        q_ret = returns[idx]
        quintiles[label] = {
            "avg_return": round(float(np.mean(q_ret)), 1),
            "median_return": round(float(np.median(q_ret)), 1),
            "pct_positive": round(float(np.mean(q_ret > 0) * 100), 0),
            "n": len(idx),
        }

    bot_ret = quintiles["Bottom 20%"]["avg_return"]
    print(f"\n{'Quintile':<12} {'Avg Ret':>8} {'Med Ret':>8} {'%Pos':>6} {'vs Bot20':>10}")
    print("-" * 50)
    for label in labels:
        q = quintiles[label]
        spread = f"{q['avg_return'] - bot_ret:+.1f}%" if label != "Bottom 20%" else "---"
        print(f"{label:<12} {q['avg_return']:>+7.1f}% {q['median_return']:>+7.1f}% "
              f"{q['pct_positive']:>5.0f}% {spread:>10}")

    return quintiles


def bucket_analysis(records, weights, adj_mult=0.0, use_reduced=True, n_buckets=20):
    """Rank-bucket performance breakdown with arbitrary granularity.

    ``n_buckets=20`` gives 5% buckets, ``n_buckets=5`` reproduces quintiles.
    Buckets are ordered best-score first. Each bucket's average return is
    compared against the bottom bucket ("vs Bot"), so a positive spread means
    the model's higher-ranked names beat its lowest-ranked names.
    """
    scores = score_records(records, weights, adj_mult, use_reduced)
    returns = np.array([r["actual_return"] for r in records])

    order = np.argsort(-scores)
    n = len(order)
    if n < n_buckets:
        print(f"  (only {n} records; need >= {n_buckets} for {n_buckets} buckets)")
        return {}

    # Even split with remainder distributed to the first buckets.
    base, rem = divmod(n, n_buckets)
    edges = []
    pos = 0
    for i in range(n_buckets):
        size = base + (1 if i < rem else 0)
        edges.append((pos, pos + size))
        pos += size

    step = 100.0 / n_buckets
    buckets = {}
    for i, (start, end) in enumerate(edges):
        idx = order[start:end]
        b_ret = returns[idx]
        top_pct = round(i * step)
        bot_pct = round((i + 1) * step)
        label = f"{top_pct}-{bot_pct}%"
        buckets[label] = {
            "avg_return": round(float(np.mean(b_ret)), 1),
            "median_return": round(float(np.median(b_ret)), 1),
            "pct_positive": round(float(np.mean(b_ret > 0) * 100), 0),
            "n": len(idx),
        }

    labels = list(buckets.keys())
    bot_label = labels[-1]
    bot_ret = buckets[bot_label]["avg_return"]
    print(f"\n{'Bucket':<10} {'n':>4} {'Avg Ret':>9} {'Med Ret':>9} {'%Pos':>6} {'vs Bot':>9}")
    print("-" * 52)
    for label in labels:
        b = buckets[label]
        spread = f"{b['avg_return'] - bot_ret:+.1f}%" if label != bot_label else "---"
        print(f"{label:<10} {b['n']:>4} {b['avg_return']:>+8.1f}% "
              f"{b['median_return']:>+8.1f}% {b['pct_positive']:>5.0f}% {spread:>9}")

    return buckets
