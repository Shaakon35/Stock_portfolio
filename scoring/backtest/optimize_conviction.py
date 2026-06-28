#!/usr/bin/env python3
"""Can re-weighting conviction() find a real signal in cycle / catalyst?

HONEST optimisation. With only n=54 cycle / n=29 catalyst names and 5-6 weights,
maximising in-sample correlation is trivial curve-fitting that predicts nothing.
So every candidate weight vector is judged by k-fold CROSS-VALIDATION (fit on
train folds, score on the held-out fold), and the OUT-OF-SAMPLE Spearman is what
we report. The in-sample number is shown too, purely to expose the overfit gap.

Target = Spearman rank corr between conviction and clean RET23>now (the rank is
what a buy threshold acts on; clean = live-corrupt names already dropped).

Weights searched (same skeleton as the engine's conviction()):
    reward = wF*F + wG*G
    safety = wV*V + w8*P8 + wC*C + wB*bind
    conv   = sqrt(reward * safety)
Weights are searched on a coarse grid, each leg renormalised to sum 1, so the
geometric mean stays comparable to the baseline scale.

Reads the feature table written by the inline builder (see build_features()).
Usage:  PORTFOLIO_USE=ai python3 scoring/backtest/optimize_conviction.py
"""
import importlib.util
import itertools
import json
import random
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
random.seed(0)  # deterministic search

# baseline weights from the live engine conviction()
BASE_REWARD = {"F": 0.50, "G": 0.50}
BASE_SAFETY = {"V": 0.35, "P8": 0.25, "C": 0.20, "bind": 0.20}


def build_features():
    """Score the universe through the real engine, join to clean RET23>now."""
    S = _load("S", HERE.parents[1] / "scoring" / "score_holdings.py")
    sys.argv = ["x", "--universe"]
    H = _load("H", HERE / "score_holdings_2023.py")
    port, cyc, neck, deep, _ = H.universe_rows()
    S.CYCLE_POS, S.BOTTLENECK, S._CYCLICAL = cyc, neck, deep
    fund = dict(S.load_fundamentals(str(H.CSV_UNIVERSE)))
    H.load_universe_prices()

    def rnow(t):
        if t in H.SERIES_CORRUPT or t in H.LIVE_CORRUPT:
            return None
        a, c = H.ANCHOR_PX.get(t), H.CURR_PX.get(t)
        if a is None or c is None or a == 0:
            return None
        return (c / a - 1.0) * 100

    feats = []
    for t, info in port.items():
        f = fund.get(t, {})
        eight, _, _ = S.score_8point(t, f, info)
        g10, _ = S.score_growth(t, f, info)
        layers, binding = S.layer_scores(t, f, info)
        r = rnow(t)
        if r is None:
            continue
        feats.append({"t": t, "strat": info.get("strategy"),
                      "F": layers["FUND"], "V": layers["VAL"],
                      "C": layers["CYCLE"], "G": g10,
                      "P8": eight / 8.0 * 10.0, "bind": layers[binding],
                      "ret": r})
    return feats


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = st.mean(xs), st.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    return cov / (sx * sy) if sx and sy else 0.0


def _rank(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    return _pearson(_rank(xs), _rank(ys))


def conv_of(row, rw, sw):
    reward = sum(rw[k] * row[k] for k in rw)
    safety = sum(sw[k] * row[k] for k in sw)
    if reward <= 0 or safety <= 0:
        return 0.0
    return (reward * safety) ** 0.5


def score_set(rows, rw, sw):
    cs = [conv_of(r, rw, sw) for r in rows]
    rs = [r["ret"] for r in rows]
    return spearman(cs, rs)


def _norm(d):
    s = sum(d.values())
    return {k: v / s for k, v in d.items()} if s else d


def candidate_weights(step=0.25):
    """Coarse grid over reward (F,G) and safety (V,P8,C,bind) simplices."""
    grid = [round(x * step, 3) for x in range(0, int(1 / step) + 1)]
    reward_opts = []
    for wf in grid:
        wg = round(1 - wf, 3)
        if wg < 0:
            continue
        reward_opts.append({"F": wf, "G": wg})
    safety_opts = []
    for wv, w8, wc in itertools.product(grid, repeat=3):
        wb = round(1 - wv - w8 - wc, 3)
        if wb < 0 or wb > 1:
            continue
        safety_opts.append({"V": wv, "P8": w8, "C": wc, "bind": wb})
    return reward_opts, safety_opts


def kfold_indices(n, k, seed=0):
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    return [idx[i::k] for i in range(k)]


def cv_best(rows, k=5, repeats=5):
    """Nested CV: for each fold, search weights on TRAIN, score on TEST.
    Returns mean out-of-sample Spearman across folds*repeats, plus the most-
    frequently-best weights (for reporting)."""
    reward_opts, safety_opts = candidate_weights()
    oos = []
    for rep in range(repeats):
        folds = kfold_indices(len(rows), k, seed=rep)
        for fi in range(k):
            test = [rows[i] for i in folds[fi]]
            train = [rows[i] for j, f in enumerate(folds) if j != fi
                     for i in f]
            if len(train) < 5 or len(test) < 2:
                continue
            best, best_s = None, -2
            for rw in reward_opts:
                for sw in safety_opts:
                    s = score_set(train, rw, sw)
                    if s > best_s:
                        best_s, best = s, (rw, sw)
            oos.append(score_set(test, best[0], best[1]))
    return (st.mean(oos) if oos else 0.0,
            st.pstdev(oos) if len(oos) > 1 else 0.0)


def insample_best(rows):
    reward_opts, safety_opts = candidate_weights()
    best, best_s = None, -2
    for rw in reward_opts:
        for sw in safety_opts:
            s = score_set(rows, rw, sw)
            if s > best_s:
                best_s, best = s, (rw, sw)
    return best, best_s


def main():
    feats = build_features()
    cats = {c: [r for r in feats if r["strat"] == c]
            for c in ("dca", "cycle", "catalyst")}

    print("\n" + "=" * 70)
    print("CONVICTION RE-WEIGHTING — honest (cross-validated) optimisation")
    print("target: Spearman(conviction, clean RET23>now)")
    print("=" * 70)

    for cat, rows in cats.items():
        n = len(rows)
        base = score_set(rows, BASE_REWARD, BASE_SAFETY)
        (rw, sw), insamp = insample_best(rows)
        cv_mean, cv_sd = cv_best(rows)
        # baseline under the SAME CV protocol (fixed weights, just score test folds)
        base_oos = []
        for rep in range(5):
            for fi, fold in enumerate(kfold_indices(n, 5, seed=rep)):
                test = [rows[i] for i in fold]
                if len(test) >= 2:
                    base_oos.append(score_set(test, BASE_REWARD, BASE_SAFETY))
        base_cv = st.mean(base_oos) if base_oos else 0.0

        print(f"\n--- {cat.upper()}  (n={n}) ---")
        print(f"  baseline weights : Spearman in-sample = {base:+.3f}   "
              f"CV out-of-sample = {base_cv:+.3f}")
        print(f"  BEST-FIT weights : Spearman in-sample = {insamp:+.3f}   "
              "<- SEDUCTIVE (overfit)")
        print(f"  optimised (CV)   :                              "
              f"CV out-of-sample = {cv_mean:+.3f} +/- {cv_sd:.3f}")
        gap = insamp - cv_mean
        print(f"  overfit gap      : {gap:+.3f}  "
              f"(in-sample minus honest CV)")
        improve = cv_mean - base_cv
        verdict = ("REAL signal" if improve > 0.10 and cv_mean > 0.10
                   else "marginal" if improve > 0.03
                   else "NO real gain (noise / overfit)")
        print(f"  best-fit weights : reward {rw}  safety {sw}")
        print(f"  VERDICT          : {verdict}  "
              f"(CV improvement over baseline = {improve:+.3f})")


if __name__ == "__main__":
    main()
