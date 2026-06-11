"""Rolling same-horizon window analysis for the cycle strategy.

The pooled 12/24/36-month dataset blends three different horizons measured
from a single base date, all inside one bull-market window. That makes the
model's edge look stronger and more stable than it may be out-of-sample.

This module instead uses SAME-horizon rolling windows (e.g. 3-year holds from
2020, 2021, 2022, 2023) so each cohort is directly comparable, and you can see
whether the top-ranked names beat the bottom-ranked names CONSISTENTLY across
years — or only in one lucky window.

Workflow:
  1. Fetch the data (slow; run once in Colab):
        from portfolio.smid_data_fetcher import fetch_windows
        fetch_windows(base_years=(2020,2021,2022,2023), hold_years=3,
                      strategies=("cycle",))
  2. Analyze:
        python -m portfolio.cycle_windows
     or, in a notebook:
        from portfolio.cycle_windows import run
        run()

Output: one TOP 5% vs BOTTOM 5% row per window, so a consistent positive
spread across windows = the edge is real; a spread that flips sign year to
year = the edge is just regime/momentum luck.
"""

import argparse

import numpy as np

from portfolio.smid_data_fetcher import load_window_csv
from portfolio.smid_regression import cross_validate, fit_regression
from portfolio.smid_optimizer import score_records


def _window_spread(recs, weights, adj_mult, use_reduced, top_frac):
    """Top vs bottom fraction stats for one window cohort."""
    n = len(recs)
    if n < max(20, int(round(1 / top_frac)) * 2):
        return None
    scores = score_records(recs, weights, adj_mult, use_reduced)
    returns = np.array([r["actual_return"] for r in recs])
    order = np.argsort(-scores)
    k = max(1, int(round(n * top_frac)))
    top = returns[order[:k]]
    bot = returns[order[-k:]]
    return {
        "n": n, "k": k,
        "top_avg": float(np.mean(top)),
        "top_med": float(np.median(top)),
        "top_pos": float(np.mean(top > 0) * 100),
        "bot_avg": float(np.mean(bot)),
        "bot_med": float(np.median(bot)),
        "spread": float(np.mean(top) - np.mean(bot)),
    }


def run(csv_path=None, top_frac=0.05, winsorize=True, winsorize_cap=200.0,
        use_reduced=True, sector_neutral=True, n_splits=5, seed=42):
    """Load window data, fit one pooled cycle weight set, print per-window spread.

    The weights are fit ONCE on all windows pooled (cross-validated for an
    honest out-of-sample Spearman), then applied to each window so the
    top/bottom comparison uses a single consistent model. This isolates the
    real question: does the SAME model rank winners above losers in every year?
    """
    records = load_window_csv(csv_path)
    if not records:
        print("No window data found. Run fetch_windows(...) first "
              "(see module docstring).")
        return 1

    records = [r for r in records if r["strategy"] == "cycle"]
    if not records:
        print("No cycle records in window CSV.")
        return 1

    windows = sorted({r["window"] for r in records},
                     key=lambda w: int(w.split("->")[0]))
    counts = {w: sum(1 for r in records if r["window"] == w) for w in windows}
    hold = records[0].get("hold_years", "?")

    print(f"\n{'='*64}")
    print(f"CYCLE ROLLING WINDOWS  ({hold}-year holds)")
    print(f"{'='*64}")
    print(f"Windows: {counts}")
    print(f"Total cycle observations: {len(records)}")

    # --- One pooled, cross-validated fit across all windows ---
    cv = cross_validate(
        records, n_splits=n_splits, metric="spearman", seed=seed,
        use_reduced=use_reduced, winsorize=winsorize,
        winsorize_cap=winsorize_cap, sector_neutral=sector_neutral,
    )
    if cv is None:
        print("\nNot enough data for cross-validation across windows.")
        return 1

    weights = cv["avg_weights"]
    adj_mult = cv["avg_adj_multiplier"]
    print(f"\nPooled cycle weights (out-of-sample test spearman "
          f"{cv['mean_test_spearman']:+.4f} +/-{cv['std_test_spearman']:.4f}):")
    for f, w in weights.items():
        if w > 0:
            print(f"  {f:<22} {w*100:>5.1f}%")

    # --- Per-window top vs bottom spread ---
    pct = int(round(top_frac * 100))
    print(f"\n{'='*64}")
    print(f"TOP {pct}% vs BOTTOM {pct}% PER WINDOW (raw returns, same weights)")
    print(f"{'='*64}")
    print(f"{'Window':<12} {'n':>4} {'TOP avg':>9} {'TOP med':>9} "
          f"{'TOP %pos':>9} {'BOT avg':>9} {'spread':>9}")
    print("-" * 64)

    rows = []
    for w in windows:
        recs = [r for r in records if r["window"] == w]
        s = _window_spread(recs, weights, adj_mult, use_reduced, top_frac)
        rows.append((w, s))
        if s is None:
            print(f"{w:<12} {len(recs):>4}   (too few for {pct}% buckets)")
            continue
        print(f"{w:<12} {s['n']:>4} {s['top_avg']:>+8.1f}% {s['top_med']:>+8.1f}% "
              f"{s['top_pos']:>8.0f}% {s['bot_avg']:>+8.1f}% {s['spread']:>+8.1f}%")

    # Pooled across all windows for reference.
    s_all = _window_spread(records, weights, adj_mult, use_reduced, top_frac)
    if s_all:
        print("-" * 64)
        print(f"{'ALL pooled':<12} {s_all['n']:>4} {s_all['top_avg']:>+8.1f}% "
              f"{s_all['top_med']:>+8.1f}% {s_all['top_pos']:>8.0f}% "
              f"{s_all['bot_avg']:>+8.1f}% {s_all['spread']:>+8.1f}%")

    # --- Verdict: is the edge consistent? ---
    valid = [s for _, s in rows if s is not None]
    if valid:
        spreads = [s["spread"] for s in valid]
        n_pos = sum(1 for sp in spreads if sp > 0)
        print(f"\n{'='*64}")
        print("CONSISTENCY CHECK")
        print(f"{'='*64}")
        print(f"  Windows where TOP {pct}% beat BOTTOM {pct}%: "
              f"{n_pos}/{len(spreads)}")
        print(f"  Spread range: {min(spreads):+.1f}%  to  {max(spreads):+.1f}%")
        print(f"  Mean spread:  {np.mean(spreads):+.1f}%  "
              f"(median {np.median(spreads):+.1f}%)")
        if n_pos == len(spreads):
            print("  => Edge held in EVERY window. Strongest possible "
                  "evidence the\n     ranking is real, not one-regime luck.")
        elif n_pos >= len(spreads) - 1:
            print("  => Edge held in all but one window. Reasonably robust, "
                  "but\n     watch the year it failed.")
        else:
            print("  => Edge flipped in multiple windows. The model is likely "
                  "riding\n     whatever theme was hot, not a durable signal. "
                  "Be cautious.")
        print("\n  Note: averages are inflated by a few big winners; the median "
              "is\n  the typical pick. A positive spread on AVG but flat/negative "
              "TOP\n  median means 'a few rockets', not 'broadly better picks'.")

    return 0


def _parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", default=None, help="Window CSV path")
    p.add_argument("--top-frac", type=float, default=0.05,
                   help="Top/bottom fraction (default 0.05 = top/bottom 5%%)")
    cap = p.add_mutually_exclusive_group()
    cap.add_argument("--winsorize-cap", type=float, default=200.0,
                     help="Cap returns at +/- this percent before fitting")
    cap.add_argument("--no-winsorize", dest="winsorize", action="store_false",
                     help="Fit on raw returns")
    p.set_defaults(winsorize=True)
    p.add_argument("--no-sector-neutral", dest="sector_neutral",
                   action="store_false")
    p.set_defaults(sector_neutral=True)
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    return run(csv_path=args.csv, top_frac=args.top_frac,
               winsorize=args.winsorize, winsorize_cap=args.winsorize_cap,
               sector_neutral=args.sector_neutral)


if __name__ == "__main__":
    raise SystemExit(main())
