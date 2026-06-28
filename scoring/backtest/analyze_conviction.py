#!/usr/bin/env python3
"""Does conviction predict realized return? Correlation + threshold test on the
2023 backtest universe, scored through the REAL engine and joined to outcomes.

Answers the practical question: "should I only buy names with conviction > X?"

RETURN COLUMNS (the choice matters):
  RET23>now  — anchor(2023) -> today. The REAL realized return, but this env's
               live feed is corrupt for ~41 names (semis 2-4x, MU/KLAC whole
               series). We use ONLY the clean (unflagged) subset for the real
               test, so a corrupt 4x print can't masquerade as alpha.
  RET23>max  — anchor -> best reliable year-end close in-window. This is a PEAK,
               not an exit you could realize, so its win-rate is ~100% for every
               bucket and it CANNOT discriminate conviction. Reported only to
               show that — never use it for a buy threshold.

Correlation is reported per CATEGORY (dca/cycle/catalyst): pooling them mixes
return scales (catalyst punts swing far wider than DCA compounders), which
washes any signal out to ~0.

Usage:
    PORTFOLIO_USE=ai python3 scoring/backtest/analyze_conviction.py
"""
import importlib.util
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = st.mean(xs), st.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    return cov / (sx * sy) if sx and sy else None


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


def _spearman(xs, ys):
    return _pearson(_rank(xs), _rank(ys))


def _summ(vals):
    if not vals:
        return 0, 0.0, 0.0, 0.0
    win = sum(1 for v in vals if v > 0) / len(vals) * 100
    return len(vals), st.mean(vals), st.median(vals), win


def build_rows():
    """Score every universe name through the engine, join to realized returns.
    Returns list of dicts: ticker, strat, conv, now (clean only else None),
    max (reliable peak)."""
    S = _load("S", HERE.parents[1] / "scoring" / "score_holdings.py")
    sys.argv = ["x", "--universe"]
    H = _load("H", HERE / "score_holdings_2023.py")

    port, cyc, neck, deep, _ = H.universe_rows()
    S.CYCLE_POS, S.BOTTLENECK, S._CYCLICAL = cyc, neck, deep
    fund = dict(S.load_fundamentals(str(H.CSV_UNIVERSE)))
    H.load_universe_prices()

    def raw_now(t):
        if t in H.SERIES_CORRUPT:
            return None  # whole series unreliable
        if t in H.LIVE_CORRUPT:
            return None  # live feed corrupt -> not a real return
        a, c = H.ANCHOR_PX.get(t), H.CURR_PX.get(t)
        if a is None or c is None or a == 0:
            return None
        return (c / a - 1.0) * 100

    def raw_max(t):
        if t in H.SERIES_CORRUPT:
            return None
        a, m = H.ANCHOR_PX.get(t), H.MAX_CLOSE.get(t)
        if a is None or m is None or a == 0:
            return None
        return (m / a - 1.0) * 100

    rows = []
    for t, info in port.items():
        f = fund.get(t, {})
        eight, _, _ = S.score_8point(t, f, info)
        g10, _ = S.score_growth(t, f, info)
        layers, binding = S.layer_scores(t, f, info)
        cov = S._coverage(f)
        peak = S.peak_trap(t, f, info)
        conv = S.conviction(g10, eight, layers, layers[binding], peak, cov)
        q10, rich, _ = S.dca_quality(t, f)
        conv_dca = S.dca_conviction(q10, layers, layers[binding], rich, cov)
        cu = conv_dca if info.get("strategy") == "dca" else conv
        rows.append({"t": t, "strat": info.get("strategy"), "conv": cu,
                     "now": raw_now(t), "max": raw_max(t)})
    return rows


def main():
    rows = build_rows()
    clean = [r for r in rows if r["now"] is not None]   # REAL realized returns

    print(f"\n=== conviction vs RET23>now (real realized, clean n={len(clean)}) ===")
    xs = [r["conv"] for r in clean]
    ys = [r["now"] for r in clean]
    print(f"  pooled Pearson  r = {_pearson(xs, ys):+.3f}  "
          f"Spearman = {_spearman(xs, ys):+.3f}   "
          "(pooling mixes return scales -> ~0)")
    print("  per category:")
    for cat in ("dca", "cycle", "catalyst"):
        sub = [r for r in clean if r["strat"] == cat]
        if len(sub) < 3:
            print(f"    {cat:9s} n={len(sub)} (too few)")
            continue
        xs = [r["conv"] for r in sub]
        ys = [r["now"] for r in sub]
        print(f"    {cat:9s} n={len(sub):3d}  Pearson={_pearson(xs, ys):+.3f}  "
              f"Spearman={_spearman(xs, ys):+.3f}")

    print(f"\n=== THRESHOLD TEST on RET23>now (real realized) ===")
    print(f"{'bucket':>10s} {'n':>4s} {'mean':>7s} {'median':>7s} {'win%':>6s}")
    for label, sub in [
            ("ALL", clean),
            ("CONV>7", [r for r in clean if r["conv"] > 7]),
            ("CONV<=7", [r for r in clean if r["conv"] <= 7]),
            ("CONV>6.5", [r for r in clean if r["conv"] > 6.5]),
            ("CONV<=6.5", [r for r in clean if r["conv"] <= 6.5])]:
        n, m, md, w = _summ([r["now"] for r in sub])
        print(f"{label:>10s} {n:>4d} {m:>+6.0f}% {md:>+6.0f}% {w:>5.0f}%")

    print(f"\n=== PER-CATEGORY: CONV>7 vs CONV<=7 (RET23>now median) ===")
    for cat in ("dca", "cycle", "catalyst"):
        sub = [r for r in clean if r["strat"] == cat]
        hi = [r["now"] for r in sub if r["conv"] > 7]
        lo = [r["now"] for r in sub if r["conv"] <= 7]
        mh = f"{st.median(hi):+6.0f}%" if hi else "    n/a"
        ml = f"{st.median(lo):+6.0f}%" if lo else "    n/a"
        verdict = ("HELPS" if hi and lo and st.median(hi) > st.median(lo)
                   else "INVERTS" if hi and lo else "-")
        print(f"  {cat:9s} CONV>7: n={len(hi):2d} med={mh}   |  "
              f"CONV<=7: n={len(lo):2d} med={ml}   -> {verdict}")

    # show that RET23>max cannot discriminate (peak -> ~100% win everywhere)
    mx = [r for r in rows if r["max"] is not None]
    print(f"\n=== why NOT RET23>max: it's a PEAK (n={len(mx)}) ===")
    print(f"{'bucket':>10s} {'n':>4s} {'median':>7s} {'win%':>6s}")
    for label, sub in [("CONV>7", [r for r in mx if r["conv"] > 7]),
                       ("CONV<=7", [r for r in mx if r["conv"] <= 7])]:
        n, m, md, w = _summ([r["max"] for r in sub])
        print(f"{label:>10s} {n:>4d} {md:>+6.0f}% {w:>5.0f}%   "
              "(~100% win both sides -> useless for a threshold)")


if __name__ == "__main__":
    main()
