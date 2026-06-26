#!/usr/bin/env python3
# =========================================================================
# HOLDING SCORER — combines the owner's two strategies into one rating
# =========================================================================
# WHY: ranking on forecast mid-CAGR alone is circular (the forecast is a
# hand-authored opinion) and discards the min/max band and entry risk. This
# engine scores every holding on BOTH of the owner's real frameworks and an
# earnings-surprise correction, then blends them.
#
#   1. 8-POINT score (0-8)  — the owner's anti-momentum QUALITY/OWNERSHIP screen
#                             (SKILL.md line 662). Rewards small, profitable,
#                             accelerating, bottleneck, early, cheap, catalysed,
#                             trend-confirmed names. PENALISES "priced for
#                             perfection" and extended charts.
#   2. GROWTH score (0-10)  — return-maximising, momentum-TOLERANT. Forward
#                             revenue growth, forward EPS growth, forecast mid-
#                             CAGR, secular runway.
#   3. EPS-SURPRISE factor  — persistent beaters have consensus estimates that
#                             are systematically too LOW, so their forward
#                             growth AND their PEG are understated. We correct
#                             both upward (beaters look cheaper + faster than
#                             screened); persistent missers are corrected down.
#   4. COMPOSITE            — balanced blend of (1) and (2), EPS-corrected.
#
# REPRODUCIBILITY: the SCORING LOGIC is fully deterministic. Market data is NOT
# fetched live (the env's yfinance feed is date-corrupted). Instead it is read
# from a dated CSV snapshot (scoring/fundamentals_YYYY-MM-DD.csv) populated by
# hand from stockanalysis.com. Re-running the script on the same CSV always
# yields the same ranking. To refresh: copy the CSV to a new date, update the
# numbers, point --csv at it.
#
# USAGE:
#   PORTFOLIO_USE=ai python3 scoring/score_holdings.py
#   PORTFOLIO_USE=ai python3 scoring/score_holdings.py --csv scoring/fundamentals_2026-06-25.csv
#   PORTFOLIO_USE=ai python3 scoring/score_holdings.py --tilt growth   # growth-weighted composite
# =========================================================================

import argparse
import csv
import os
import sys
from pathlib import Path

# --- locate repo root so the script runs from anywhere ---
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("PORTFOLIO_USE", "ai")

from portfolio.AI_allocations import (  # noqa: E402
    TARGET_WEIGHTS, W1_SILICON_TARGETS, W2_POWER_TARGETS, W3_DCINFRA_TARGETS,
    W4_CLOUD_TARGETS, W5_SOFTWARE_TARGETS, W6_SPEC_TARGETS, STRATEGY, WATCHLIST,
)
from config.forecasts import WAVE_FORECASTS  # noqa: E402

# =========================================================================
# 0. PORTFOLIO MAP (weights + forecasts, pulled live from the source of truth)
# =========================================================================
_WAVES = [
    ("W1", "W1_SILICON", W1_SILICON_TARGETS),
    ("W2", "W2_POWER", W2_POWER_TARGETS),
    ("W3", "W3_DCINFRA", W3_DCINFRA_TARGETS),
    ("W4", "W4_CLOUD", W4_CLOUD_TARGETS),
    ("W5", "W5_SOFTWARE", W5_SOFTWARE_TARGETS),
    ("W6", "W6_SPEC", W6_SPEC_TARGETS),
]


def _forecast(ticker):
    """Return (min_cagr, max_cagr, mid) or (None, None, None)."""
    f = WAVE_FORECASTS.get(ticker)
    if not f:
        return (None, None, None)
    lo, hi = (f["min_rate"], f["max_rate"]) if isinstance(f, dict) else f
    if lo is None or hi is None:
        return (None, None, None)
    return (lo, hi, (lo + hi) / 2.0)


def portfolio_rows(include_watchlist=False):
    """Each held ticker with wave, sub-weight, book %, strategy, forecast band.
    With include_watchlist, also append WATCHLIST names (wave='WL', book=0)."""
    rows = {}
    for w, wk, basket in _WAVES:
        wv = TARGET_WEIGHTS[wk]
        for t, sw in basket.items():
            lo, hi, mid = _forecast(t)
            rows[t] = {
                "ticker": t, "wave": w, "sub": sw, "book_pct": sw * wv * 100,
                "strategy": STRATEGY.get(t, "?"), "held": True,
                "cagr_lo": lo, "cagr_hi": hi, "cagr_mid": mid,
                "wl_pos": None,
            }
    if include_watchlist:
        for t, v in WATCHLIST.items():
            if t in rows:
                continue  # already held; don't double-list
            cagr = v.get("cagr") if isinstance(v, dict) else None
            lo, hi = (cagr if cagr else (None, None))
            mid = (lo + hi) / 2.0 if (lo is not None and hi is not None) else None
            rows[t] = {
                "ticker": t, "wave": "WL", "sub": 0.0, "book_pct": 0.0,
                "strategy": (v.get("strategy") if isinstance(v, dict) else "?"),
                "held": False, "cagr_lo": lo, "cagr_hi": hi, "cagr_mid": mid,
                "wl_pos": (v.get("pos") if isinstance(v, dict) else None),
            }
    return rows


# =========================================================================
# 1. CYCLE POSITION (Point 5: "secular driver, early") — owner's own tags,
#    mirrored from the notebook's _CYCLE_POS so the two stay consistent.
# =========================================================================
CYCLE_POS = {
    "BESI.AS": "Early", "SMHN.DE": "Early", "SIMO": "Early/Mid",
    "CAMT": "Mid/Late", "000660.KS": "Mid/Late", "CDNS": "Mid",
    "ONTO": "Mid", "SMHV.SW": "Mid",
    "GEV": "Late", "CEG": "Late", "CCJ": "Mid", "OKLO": "Binary",
    "ETN": "Early", "PWR": "Early", "HUBB": "Early",
    "VRT": "Mid", "ANET": "Mid", "COHR": "Mid", "CRDO": "Mid/Late",
    "FN": "Mid", "ALAB": "Mid/Late",
    "DDOG": "Mid", "ZS": "Mid", "PLTR": "Mid", "NOW": "Mid",
    "CRWD": "Mid", "PANW": "Mid", "S": "Early", "SNOW": "Mid",
    "TMDX": "Early/Mid", "SYM": "Binary", "CRCL": "Binary",
    "AXON": "Mid", "IONQ": "Early", "RKLB": "Early", "LEU": "Early",
}
# Point 5 score: earlier in the secular wave = better for forward growth.
_CYCLE_P5 = {"Early": 1.0, "Early/Mid": 0.75, "Mid": 0.5,
             "Mid/Late": 0.25, "Late": 0.1, "Binary": 0.0}

# Point 4 ("demand > supply" — genuine bottleneck the name sits in front of).
# Owner-tagged: 1.0 = pure-play chokepoint, 0.5 = strong position, 0.0 = none.
BOTTLENECK = {
    "BESI.AS": 1.0, "SMHN.DE": 1.0, "CAMT": 1.0, "CRDO": 1.0, "ALAB": 1.0,
    "COHR": 1.0, "FN": 0.5, "VRT": 1.0, "ANET": 0.5, "SIMO": 0.5,
    "CDNS": 1.0, "GEV": 1.0, "CCJ": 1.0, "ETN": 0.5, "HUBB": 0.5,
    "PWR": 0.5, "OKLO": 0.5, "NOW": 0.5, "ZS": 0.5, "CRWD": 0.5,
    "PANW": 0.5, "DDOG": 0.5, "TMDX": 0.5, "AXON": 0.5, "IONQ": 0.5,
    "RKLB": 0.5, "SYM": 0.5, "SMHV.SW": 0.5, "SNOW": 0.5, "S": 0.5,
    "PLTR": 0.5, "ONTO": 0.5, "000660.KS": 0.5, "CEG": 0.5, "CRCL": 0.0,
    "LEU": 0.5,
}

# Cyclical names judge valuation on normalized earnings, not snapshot P/E
# (Point 6 trough/peak trap). Used to soften the PEG penalty for cyclicals.
_CYCLICAL = {t for t, m in STRATEGY.items() if m == "cycle"}


def cycle_of(t, info):
    """Resolve a name's cycle position: explicit CYCLE_POS first, then the
    watchlist's own 'pos' tag, then 'Mid' as neutral default."""
    return CYCLE_POS.get(t) or info.get("wl_pos") or "Mid"


# =========================================================================
# 2. FUNDAMENTALS SNAPSHOT (dated CSV from stockanalysis.com)
# =========================================================================
# CSV columns (all numeric unless noted; blank = unknown -> dropped/renormalized
# by _blend, not faked-neutral):
#   ticker, mktcap_b, fwd_rev_growth, ttm_rev_growth, fwd_eps_growth,
#   gross_margin, net_margin, fcf_positive(0/1), peg, ps_ratio,
#   pct_above_200dma, pct_below_52w_high, eps_beat_rate(0..1), eps_beat_streak(int)
#   ps_ratio: price/sales; valuation fallback for P6 when peg is absent
#            (loss-makers / pre-revenue names have no PEG).
# =========================================================================
FUND_FIELDS = [
    "ticker", "mktcap_b", "fwd_rev_growth", "ttm_rev_growth", "fwd_eps_growth",
    "gross_margin", "net_margin", "fcf_positive", "peg", "ps_ratio",
    "pct_above_200dma", "pct_below_52w_high", "eps_beat_rate", "eps_beat_streak",
]


def _num(s):
    s = (s or "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_fundamentals(path):
    out = {}
    with open(path, newline="") as fh:
        # Skip leading '#' comment lines so the real header row is used by DictReader.
        lines = [ln for ln in fh if not ln.lstrip().startswith("#")]
    for row in csv.DictReader(lines):
        t = (row.get("ticker") or "").strip()
        if not t or t.startswith("#"):
            continue
        out[t] = {k: _num(row.get(k)) for k in FUND_FIELDS if k != "ticker"}
    return out


# =========================================================================
# 3. EPS-SURPRISE CORRECTION
# =========================================================================
# Persistent beaters: consensus is too LOW -> their forward growth AND PEG are
# understated. We nudge forward-growth UP and PEG DOWN (cheaper) for beaters,
# and the reverse for missers. beat_rate in [0,1] (fraction of last ~8 qtrs
# beaten); streak is consecutive beats (caps the bonus). Neutral at 0.5.
# Correction is intentionally MILD (max +-12%) so it tilts, never dominates.
# =========================================================================
def eps_surprise_factor(beat_rate, streak):
    if beat_rate is None:
        return 1.0
    base = (beat_rate - 0.5) * 0.20          # +-0.10 at the extremes
    streak_bonus = min(max(streak or 0, 0), 8) / 8.0 * 0.02  # up to +0.02
    return 1.0 + base + (streak_bonus if beat_rate >= 0.5 else 0.0)


# =========================================================================
# 4. SCORING PRIMITIVES (deterministic, bounded 0..1 each)
# =========================================================================
def _band(x, lo, hi):
    """Linear 0..1 ramp; clamps outside [lo,hi].

    Returns None for missing input (NOT a neutral 0.5). A blanket 0.5 default
    subsidises bad names with no data and penalises great names with a single
    gap; instead, missing sub-scores are dropped and their weight is
    redistributed across the present ones by _blend(). See _blend.
    """
    if x is None:
        return None  # unknown -> let _blend renormalize, don't fake-neutral it
    if hi == lo:
        return None
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def _band_inv(x, lo, hi):
    """Inverse ramp: smaller x scores higher. None propagates as missing."""
    b = _band(x, lo, hi)
    return None if b is None else 1.0 - b


def _band_inv_log(x, lo, hi):
    """Inverse ramp on a log10 scale: smaller x scores higher, falloff even
    across orders of magnitude. Used for market cap so a $40B and a $250B name
    are separated and there is no cliff at the top of the range. None propagates
    as missing (so _blend renormalizes), matching _band."""
    if x is None or x <= 0 or lo <= 0 or hi <= lo:
        return None
    import math
    t = (math.log10(x) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    return max(0.0, min(1.0, 1.0 - t))


_MISSING_PENALTY = 0.15  # speculative bucket: a data gap IS a red flag


def _blend(components, scale=1.0, risk_penalize=False):
    """Weighted aggregate with two missing-data policies (the hybrid model).

    components: iterable of (value_or_None, weight).

    risk_penalize=False  (CORE assets — DCA / established cycle):
        Missing components are DROPPED and their weight is redistributed across
        the present ones (weighted MEAN * scale). A quality name is not punished
        because a feed intermittently dropped one forward field; the remaining
        data safely carries the score.

    risk_penalize=True   (SPECULATIVE assets — W6 spec / Binary cycle):
        Missing components are NOT dropped. Each contributes a fixed penalty
        (_MISSING_PENALTY) at full weight and the denominator stays the full
        weight. An opaque, non-reporting lottery name is therefore suppressed
        rather than flattered — a gap is treated as a structural risk.

    Returns (score, coverage) where coverage = present_weight / total_weight
    in BOTH modes (so the gap is always visible). If nothing is present and we
    are not risk-penalizing, returns (0.5 * scale, 0.0) — an explicit neutral
    the 0.0 coverage flags as unknown.
    """
    total_w = sum(w for _, w in components)
    if total_w == 0:
        return 0.5 * scale, 0.0
    present = [(v, w) for v, w in components if v is not None]
    pres_w = sum(w for _, w in present)
    coverage = pres_w / total_w

    if risk_penalize:
        # Denominator fixed at total weight; missing -> penalty, not dropped.
        num = sum(v * w for v, w in present) \
            + sum(_MISSING_PENALTY * w for v, w in components if v is None)
        return (num / total_w) * scale, coverage

    if pres_w == 0:
        return 0.5 * scale, 0.0
    mean = sum(v * w for v, w in present) / pres_w
    return mean * scale, coverage


# Names whose data gaps are a RED FLAG, not noise: the speculative tail (W6) and
# binary-outcome bets. For these, missing fundamentals are penalized, not
# renormalized away (see _blend risk_penalize).
def _is_speculative(t, info):
    return info.get("wave") == "W6" or cycle_of(t, info) == "Binary"


# Columns that exist in the schema but are NOT obtainable from the source at
# scale, so they are excluded from the coverage denominator. Counting them
# would cap every name's data% well below 100% no matter how complete its real
# data is (the source has no scrapable field for them), making [GAP] fire on
# fully-sourced names and rendering the flag meaningless. They are still scored
# when seeded by hand (e.g. eps_beat for documented serial beaters); excluding
# them here only changes the coverage metric, not the scoring.
#   ttm_rev_growth     - statistics page exposes no trailing-YoY field
#   pct_below_52w_high - no clean 52w-high distance field; P8 uses 200DMA
#   eps_beat_rate      - /earnings/ estimate-vs-actual table 404s; unscrapable
#   eps_beat_streak    - same source gap as eps_beat_rate
_UNSOURCEABLE = frozenset({
    "ttm_rev_growth", "pct_below_52w_high", "eps_beat_rate", "eps_beat_streak",
})


def _coverage(f):
    """Fraction of OBTAINABLE fundamental fields actually present (0..1).
    Reported alongside each score so a number earned on real data is visibly
    distinct from one propped up by defaults. The denominator counts only
    fields that can actually be sourced (see _UNSOURCEABLE): a name with every
    obtainable fact present reads ~100%, and [GAP] therefore means genuinely
    thin data — not the unavoidable absence of fields no source provides."""
    fields = [k for k in FUND_FIELDS
              if k != "ticker" and k not in _UNSOURCEABLE]
    if not fields:
        return 0.0
    return sum(1 for k in fields if f.get(k) is not None) / len(fields)


# Coverage below this is flagged with a GAP marker in the output tables.
_GAP_THRESHOLD = 0.75
_GAP_FOOTNOTE = (
    "  data% = share of fundamentals present; scores are renormalized over "
    "present metrics.\n"
    f"  [GAP] = coverage < {_GAP_THRESHOLD:.0%}: score rests on thin data — "
    "trust it less (and for\n"
    "        speculative W6/Binary names the gap is penalised, not "
    "renormalized away)."
)

# --- per-score explanations shown under each table -----------------------
# GROWTH + 8-POINT live on the two-axis grid (cycle/catalyst hunt + the main
# holding table); QUALITY + RICHNESS are the DCA rubric. Each metric is spelled
# out here so a reader can interpret a number without reading the source.
_GROWTH_8PT_FOOTNOTE = (
    "  GROWTH 0-10 (higher = faster, momentum-TOLERANT): a weighted blend of\n"
    "        forward revenue growth (35%), forward EPS growth (30%), the hand-\n"
    "        authored forecast mid-CAGR (20%) and secular runway (15%). All\n"
    "        forward figures are EPS-surprise corrected (serial beaters nudged\n"
    "        up, missers down). It answers \"how much can this compound?\" and\n"
    "        does NOT punish an extended chart.\n"
    "  8PT 0-8 (higher = more disciplined, ANTI-momentum): the owner's 8-point\n"
    "        ownership screen — P1 small mkt-cap, P2 profitable/turning, P3\n"
    "        accelerating growth, P4 bottleneck moat, P5 secular & early, P6\n"
    "        NOT priced for perfection (low PEG), P7 fresh catalyst, P8 not\n"
    "        extended vs 200DMA. Each sub-point is 0..1, summed to 0..8. It\n"
    "        answers \"is this still a cheap, early, sane entry?\" and PENALISES\n"
    "        rich, crowded, far-above-trend names — the opposite bias to GROWTH.\n"
    "  quadrant = the two crossed (GROWTH>=6 & 8PT>=5 -> PRIME; high growth but\n"
    "        extended -> MOMENTUM; disciplined but slow -> QUALITY; neither ->\n"
    "        AVOID). epsF = the EPS-surprise multiplier applied to forward data."
)
_DCA_FOOTNOTE = (
    "  QUALITY 0-10 (higher = better business): durable margins (35%), durable\n"
    "        forward revenue growth (25%), forward EPS growth (20%) and free-\n"
    "        cash-flow positivity (20%). Unlike 8PT it does NOT penalise size or\n"
    "        an extended chart — a proven large compounder is meant to score\n"
    "        well here. It answers \"is this still a great business?\".\n"
    "  RICHNESS 0-1 (0 = cheap .. 1 = stretched): a normalized PRICE index, not\n"
    "        a score to maximise. It is the mean of two 0..1 bands — PEG (1.0->0,\n"
    "        4.0+->1) and distance above the 200DMA (0%->0, 60%+->1). It stays on\n"
    "        a 0..1 scale (not 0..10) because it is a GATE, not a ranking axis:\n"
    "        >=0.6 trips the RICH grade. It answers \"is the price ahead of the\n"
    "        business?\".\n"
    "  grade = QUALITY + RICHNESS combined: KEEP-DCA (durable & fairly priced),\n"
    "        RICH (great business but price extended -> slow the buys), IMPAIRED\n"
    "        (quality cracking -> pause / reduce)."
)


def _cov_cell(coverage):
    """Format a coverage value for a table cell, flagging low coverage."""
    cell = f"{coverage * 100:4.0f}%"
    return f"{cell} [GAP]" if coverage < _GAP_THRESHOLD else cell


# --- LAYER + PEAK presentation (re-expresses scores; changes none of them) ---
_LAYER_FOOTNOTE = (
    "  layers (0-10, higher=SAFER on that layer) decompose the score by the "
    "force that moves price:\n"
    "    F=FUND  business quality (margins+growth+FCF) ...... wins the LONG run\n"
    "    V=VAL   price vs the business (PEG/PS + extension) . mean-reverts (months)\n"
    "    C=CYC   cycle position + crowding (pos+neck+chart) .. drives the SHORT run / hype\n"
    "  bind = the BINDING (lowest) layer: the dominant risk you take buying here.\n"
    "  [PEAK?] = a cyclical/late name's low PEG is fake-cheap (peak earnings) on an\n"
    "          extended chart — the SK Hynix / Micron trap. Treat its VAL as a warning."
)


def _layer_cell(layers):
    """Compact 'F V C' triple for a table cell, each 0..10 to one decimal."""
    return (f"{layers['FUND']:4.1f} {layers['VAL']:4.1f} "
            f"{layers['CYCLE']:4.1f}")


# --- 8-POINT (each sub-score 0..1; summed *8/8 -> 0..8) ------------------
def score_8point(t, f, info):
    eps_f = eps_surprise_factor(f.get("eps_beat_rate"), f.get("eps_beat_streak"))

    # P1 small enough to multiply: smaller mkt cap better, on a LOG scale so the
    #    penalty is smooth across orders of magnitude instead of a hard cliff at
    #    $300B (a $40B and a $250B name should differ; $310B and $3T should too).
    #    $5B -> 1.0, $3T -> 0.0, evenly spaced in log10 between.
    p1 = _band_inv_log(f.get("mktcap_b"), 5, 3000)
    # P2 profitable or turning: GAAP net margin>0 full; FCF+ only = 0.5.
    #     Missing margin -> None (dropped by _blend), NOT a faked neutral.
    nm = f.get("net_margin")
    if nm is None:
        p2 = None
    elif nm > 0:
        p2 = min(1.0, 0.6 + _band(nm, 0, 30) * 0.4)
    else:
        p2 = 0.5 if (f.get("fcf_positive") == 1) else 0.15
    # P3 growth accelerating: fwd rev growth, bonus if fwd>ttm (re-accel),
    #     EPS-surprise corrects the forward figure.
    fwd = f.get("fwd_rev_growth")
    fwd_corr = None if fwd is None else fwd * eps_f
    p3 = _band(fwd_corr, 5, 45)
    if p3 is not None and fwd is not None and f.get("ttm_rev_growth") is not None:
        if fwd > f["ttm_rev_growth"]:
            p3 = min(1.0, p3 + 0.15)        # genuine re-acceleration
    # P4 bottleneck (owner tag); unknown watchlist names -> neutral 0.3.
    p4 = BOTTLENECK.get(t, 0.3)
    # P5 secular & early (cycle position).
    p5 = _CYCLE_P5.get(cycle_of(t, info), 0.5)
    # P6 not priced for perfection. PEG first; when PEG is absent (loss-makers,
    #    pre-revenue) fall back to P/S-vs-growth so valuation discipline still
    #    applies instead of dropping the point. Cyclicals get a softer penalty
    #    (snapshot multiples mislead at cycle extremes). NB: the EPS-surprise
    #    factor is intentionally NOT applied here — it already lifts the growth
    #    inputs (P3), and PEG embeds EPS, so correcting both double-counts a
    #    single signal.
    peg = f.get("peg")
    if peg is not None:
        p6 = _band_inv(peg, 0.8, 3.5)
    else:
        # Fallback: price/sales judged against forward growth. A high P/S is only
        # "priced for perfection" if growth doesn't justify it, so scale the P/S
        # bands by the growth rate (ps/growth ~ a crude PEG-on-sales). Returns
        # None (point dropped/penalised by _blend) only when P/S is also absent.
        ps = f.get("ps_ratio")
        if ps is None:
            p6 = None
        else:
            g = f.get("fwd_rev_growth")
            denom = max(g, 10.0) if g is not None else 25.0
            ps_to_growth = ps / (denom / 10.0)        # normalise: 10% growth -> raw P/S
            p6 = _band_inv(ps_to_growth, 1.0, 15.0)   # cheap on sales -> high score
    if p6 is not None and t in _CYCLICAL:
        p6 = 0.5 + (p6 - 0.5) * 0.6                   # pull toward neutral
    # P7 fresh catalyst.
    p7 = 1.0 if info["strategy"] == "catalyst" else (0.4 if info["strategy"] == "cycle" else 0.2)
    # P8 confirm trend / not extended: penalise far above 200dma; reward
    #    pullback from the 52w high (room to run, owner is anti-momentum).
    above = f.get("pct_above_200dma")
    p8a = _band_inv(above, 0, 80)         # 0% above = 1.0, 80%+ above = 0.0
    p8b = _band(f.get("pct_below_52w_high"), 0, 40)
    if p8a is None and p8b is None:
        p8 = None                          # both missing -> drop the point
    else:
        p8, _ = _blend([(p8a, 1.0), (p8b, 1.0)])

    # Sum-of-8 stays on a 0..8 scale. CORE names: missing data-driven points are
    # dropped and their weight redistributed. SPECULATIVE names: missing points
    # are penalised (a data gap is a structural red flag, not noise).
    spec = _is_speculative(t, info)
    parts = {"P1": p1, "P2": p2, "P3": p3, "P4": p4, "P5": p5, "P6": p6, "P7": p7, "P8": p8}
    eight, _cov = _blend([(v, 1.0) for v in parts.values()], scale=8.0,
                         risk_penalize=spec)
    return eight, parts, eps_f


# --- GROWTH (0..10), momentum-tolerant ----------------------------------
def score_growth(t, f, info):
    eps_f = eps_surprise_factor(f.get("eps_beat_rate"), f.get("eps_beat_streak"))
    fwd = f.get("fwd_rev_growth")
    fwd_corr = None if fwd is None else fwd * eps_f
    eps_g = f.get("fwd_eps_growth")
    eps_corr = None if eps_g is None else eps_g * eps_f

    g_rev = _band(fwd_corr, 5, 50)                       # forward revenue
    g_eps = _band(eps_corr, 5, 60)                       # forward EPS
    g_sec = _CYCLE_P5.get(cycle_of(t, info), 0.5)        # secular runway
    # The hand-authored forecast mid-CAGR was dropped: it is a subjective input,
    # and scoring on it is the exact circularity this engine set out to avoid
    # (see module docstring). The growth score now rests only on observable
    # forward analyst numbers + the secular-runway tag. CORE names: missing
    # components drop out and weight is redistributed (no faked 0.5).
    # SPECULATIVE names: missing fwd numbers are penalised so opaque lottery
    # tickets are suppressed, not flattered.
    score10, cov = _blend([(g_rev, 4.5), (g_eps, 4.0),
                           (g_sec, 1.5)], scale=10.0,
                          risk_penalize=_is_speculative(t, info))
    return score10, {"rev": g_rev, "eps": g_eps,
                     "sec": g_sec, "coverage": cov}


# =========================================================================
# 4b. LAYER DECOMPOSITION — collapse the sub-scores into the three forces that
#     actually move a price, so a glance shows WHERE a name's risk lives.
# =========================================================================
# Every metric in this engine answers one of three questions. The scores appear
# to "disagree" only because they sit on different layers, each dominant over a
# different horizon:
#
#   FUND  (Layer 1) "Is the business actually good?"        long-run driver
#                   margins + forward rev/eps growth + FCF
#   VAL   (Layer 2) "Is the price fair for that business?"  mean-reverts (months)
#                   PEG (P/S fallback) + distance above the 200DMA
#   CYCLE (Layer 3) "Where in the boom/bust + how crowded?" short-run driver/hype
#                   cycle position + bottleneck + chart extension
#
# Each is a 0..10 score where HIGHER = SAFER on that layer (good business /
# fair price / early-and-uncrowded). The BINDING layer is the lowest of the
# three — the dominant risk you are actually taking when you buy. This re-
# expresses the existing sub-scores; it changes none of them. It exists so the
# "the numbers contradict each other" overwhelm becomes a single legible read:
# a great business (high FUND) bought too dear (low VAL) or too late (low CYCLE)
# tells you precisely which way it can hurt you.
# =========================================================================
_LAYER_ABBR = {"FUND": "FUN", "VAL": "VAL", "CYCLE": "CYC"}


def layer_scores(t, f, info):
    """Return ({FUND,VAL,CYCLE}: 0..10, higher=safer) and the binding (lowest)
    layer name. Re-uses the same primitives as the 8-Point / Growth scores so
    the layers never contradict the underlying numbers — they only regroup
    them by the force each one represents."""
    eps_f = eps_surprise_factor(f.get("eps_beat_rate"), f.get("eps_beat_streak"))
    spec = _is_speculative(t, info)

    # --- FUND (Layer 1): business quality, momentum-neutral --------------
    nm = f.get("net_margin")
    fcf = f.get("fcf_positive")
    if nm is None:
        l_margin = None
    elif nm > 0:
        l_margin = min(1.0, 0.55 + _band(nm, 0, 30) * 0.45)
    else:
        l_margin = 0.4 if fcf == 1 else 0.1
    fwd = f.get("fwd_rev_growth")
    l_rev = _band(None if fwd is None else fwd * eps_f, 5, 45)
    eps_g = f.get("fwd_eps_growth")
    l_eps = _band(None if eps_g is None else eps_g * eps_f, 5, 50)
    if fcf == 1:
        l_fcf = 1.0
    elif fcf == 0:
        l_fcf = 0.5 if (nm is not None and nm > 0) else 0.0
    else:
        l_fcf = None                                  # nothing known -> drop
    fund10, _ = _blend([(l_margin, 3.5), (l_rev, 2.5), (l_eps, 2.0),
                        (l_fcf, 2.0)], scale=10.0, risk_penalize=spec)

    # --- VAL (Layer 2): how much of the business is already in the price -
    #     Higher = cheaper / fairer. PEG first (P/S-vs-growth fallback), plus
    #     distance above the 200DMA — extension IS paid-up optimism. Cyclical
    #     PEG is softened toward neutral (the peak/trough trap; see peak_trap).
    peg = f.get("peg")
    if peg is not None:
        v_peg = _band_inv(peg, 0.8, 3.5)
    else:
        ps = f.get("ps_ratio")
        if ps is None:
            v_peg = None
        else:
            g = f.get("fwd_rev_growth")
            denom = max(g, 10.0) if g is not None else 25.0
            v_peg = _band_inv(ps / (denom / 10.0), 1.0, 15.0)
    if v_peg is not None and t in _CYCLICAL:
        v_peg = 0.5 + (v_peg - 0.5) * 0.6
    v_ext = _band_inv(f.get("pct_above_200dma"), 0, 80)
    val10, _ = _blend([(v_peg, 1.6), (v_ext, 1.0)], scale=10.0)

    # --- CYCLE (Layer 3): position in the wave + crowding ----------------
    #     Higher = earlier / less extended / sits on a real bottleneck. Built
    #     from owner cycle tags (always present) so this layer is never blank.
    c_pos = _CYCLE_P5.get(cycle_of(t, info), 0.5)
    c_neck = BOTTLENECK.get(t, 0.3)
    c_ext = _band_inv(f.get("pct_above_200dma"), 0, 100)
    cyc10, _ = _blend([(c_pos, 1.5), (c_neck, 1.0), (c_ext, 1.0)], scale=10.0)

    layers = {"FUND": fund10, "VAL": val10, "CYCLE": cyc10}
    binding = min(layers, key=layers.get)             # lowest = dominant risk
    return layers, binding


# =========================================================================
# 4c. PEAK-EARNINGS TRAP — a low PEG on a late-cycle name is FAKE-cheap.
# =========================================================================
# A cyclical's PEG divides today's price by PEAK-cycle earnings, so it screens
# absurdly cheap exactly when it is most dangerous: when normalised earnings
# arrive, that "cheap" multiple is revealed as a peak multiple and the price
# de-rates. The memory/storage complex is the canonical case (SK Hynix, Samsung,
# Micron, WDC, Seagate, SanDisk all show sub-1 PEGs on hugely extended charts).
#
# The flag fires on two paths so it does not depend on a name being hand-tagged:
#   1. TAGGED late-cycle (cycle/Mid-Late/Late) + low PEG + extended chart.
#   2. STRUCTURAL signature — a PEG this far below 1 simply is not seen on a
#      healthy stable-growth name; paired with an extended chart it is the
#      fingerprint of peak-cycle earnings, tag or not. This catches the untagged
#      memory/storage watchlist names (SNDK, WDC, STX, Samsung, ...).
# It does NOT change any score; it only annotates, so a fake-cheap VAL score is
# called out instead of trusted.
# =========================================================================
_PEAK_TAG_PEG = 1.0      # tagged late-cycle: PEG <= this ...
_PEAK_TAG_EXT = 60.0     #   ... AND chart >= this % above 200DMA
_PEAK_DEEP_PEG = 0.5     # untagged: a PEG this low is almost only a peak signal
_PEAK_DEEP_EXT = 50.0    #   ... with a moderately extended chart
_PEAK_LOW_PEG = 0.75     # untagged: a merely-low PEG ...
_PEAK_LOW_EXT = 100.0    #   ... needs a steeper extension to qualify


def peak_trap(t, f, info):
    """True when a cyclical / late-cycle name's low PEG is fake-cheap (peak
    earnings) and the chart is extended — the SK Hynix / Micron trap."""
    peg = f.get("peg")
    ext = f.get("pct_above_200dma")
    if peg is None or ext is None:
        return False
    late = (t in _CYCLICAL) or (cycle_of(t, info) in ("Mid/Late", "Late"))
    if late and peg <= _PEAK_TAG_PEG and ext >= _PEAK_TAG_EXT:
        return True
    if peg <= _PEAK_DEEP_PEG and ext >= _PEAK_DEEP_EXT:
        return True
    if peg <= _PEAK_LOW_PEG and ext >= _PEAK_LOW_EXT:
        return True
    return False


# =========================================================================
# 5. OPTIONAL BLEND (off by default — owner wants the two scores kept separate)
# =========================================================================
def composite(eight, growth10, tilt):
    """Optional blend of 8-Point (0..8 -> 0..10) and Growth (0..10). Only used
    when --blend is passed; by default the two scores are reported side by side
    with NO blend, so the growth/discipline trade-off stays the owner's call."""
    eight10 = eight / 8.0 * 10.0
    if tilt == "growth":
        w_g, w_q = 0.65, 0.35
    elif tilt == "quality":
        w_g, w_q = 0.35, 0.65
    else:  # balanced
        w_g, w_q = 0.50, 0.50
    return growth10 * w_g + eight10 * w_q


def quadrant(eight, growth10):
    """Classify a name on the two-axis grid (median-ish thresholds).

    NOTE: PRIME == small + cheap + accelerating, i.e. the CYCLE/CATALYST
    archetype. A DCA name (a proven, often large, richly-valued compounder you
    buy on schedule) can almost never reach PRIME and will tend to land in
    AVOID — NOT because it is bad, but because this grid asks the wrong question
    of it. Use strategy_grade() / the --by-strategy view to judge DCA fairly.
    """
    hi_q = eight >= 5.0          # 8-Point >= 5/8 == disciplined/quality
    hi_g = growth10 >= 6.0       # Growth >= 6/10 == high growth
    if hi_g and hi_q:
        return "PRIME"           # high growth AND passes discipline -> size up
    if hi_g and not hi_q:
        return "MOMENTUM"        # high growth but extended/expensive -> cap/starter
    if hi_q and not hi_g:
        return "QUALITY"         # disciplined but slower -> ballast
    return "AVOID"               # neither -> trim/skip


# =========================================================================
# 5b. STRATEGY-AWARE GRADING — judge each name by the JOB it does
# =========================================================================
# The Growth/8-Point grid above is built for the cycle/catalyst hunt (small +
# cheap + accelerating). DCA names do a different job: be a durable compounder
# you buy on a schedule regardless of price. Grading them on "is it small and
# exploding" is a category error. Each mode therefore gets its own rubric.
#
#   DCA      -> KEEP-DCA / RICH / IMPAIRED   (quality + valuation sanity)
#   CYCLE    -> reuse the two-axis quadrant  (where in the cycle / how cheap)
#   CATALYST -> reuse the two-axis quadrant  (is the punt's upside intact)
# =========================================================================
def dca_quality(t, f):
    """DCA quality on its own terms (0..10): durable margins + cash + steady
    growth. Ignores the small-cap and momentum penalties that unfairly sink
    proven compounders. Returns (quality10, richness, parts)."""
    eps_f = eps_surprise_factor(f.get("eps_beat_rate"), f.get("eps_beat_streak"))

    # --- QUALITY (is it still a great business?) ---
    #     Missing inputs propagate as None and are dropped by _blend (their
    #     weight is redistributed), instead of being faked to a neutral 0.5.
    nm = f.get("net_margin")
    fcf = f.get("fcf_positive")
    if nm is None:
        q_margin = None
    elif nm > 0:
        q_margin = min(1.0, 0.55 + _band(nm, 0, 30) * 0.45)
    else:
        q_margin = 0.4 if fcf == 1 else 0.1
    if fcf == 1:
        q_fcf = 1.0
    elif fcf == 0:
        q_fcf = 0.5 if (nm is not None and nm > 0) else 0.0
    elif nm is not None:                         # no FCF flag, infer from margin
        q_fcf = 0.5 if nm > 0 else 0.0
    else:
        q_fcf = None                             # nothing known -> drop it
    fwd = f.get("fwd_rev_growth")
    fwd_corr = None if fwd is None else fwd * eps_f
    q_growth = _band(fwd_corr, 6, 25)          # DCA wants durable, not explosive
    eps_g = f.get("fwd_eps_growth")
    q_eps = _band(None if eps_g is None else eps_g * eps_f, 6, 30)
    quality10, cov = _blend([(q_margin, 3.5), (q_growth, 2.5),
                             (q_eps, 2.0), (q_fcf, 2.0)], scale=10.0)

    # --- RICHNESS (is the price ahead of the business?) 0=cheap .. 1=stretched
    # PEG used raw: eps_f already lifts the growth side of the quality score, so
    # applying it to PEG too would double-count the same surprise signal. Fall
    # back to P/S when PEG is absent so the richness leg is not silently dropped.
    peg = f.get("peg")
    if peg is not None:
        r_peg = _band(peg, 1.0, 4.0)           # PEG 1 -> 0, 4+ -> 1
    else:
        ps = f.get("ps_ratio")
        r_peg = _band(ps, 3.0, 20.0)           # cheap on sales -> low richness
    above = f.get("pct_above_200dma")
    r_dma = _band(above, 0, 60)                # 0% above -> 0, 60%+ -> 1
    richness, _ = _blend([(r_peg, 1.0), (r_dma, 1.0)])

    return quality10, richness, {
        "margin": q_margin, "growth": q_growth, "eps": q_eps, "fcf": q_fcf,
        "r_peg": r_peg, "r_dma": r_dma, "coverage": cov}


def dca_grade(quality10, richness, f):
    """KEEP-DCA / RICH / IMPAIRED from DCA quality + richness."""
    nm = f.get("net_margin")
    impaired = (quality10 < 4.0) or (nm is not None and nm < 0
                                     and f.get("fcf_positive") != 1)
    if impaired:
        return "IMPAIRED"        # business cracking -> pause/reduce the DCA
    if richness >= 0.6:
        return "RICH"            # quality intact but price extended -> slow buys
    return "KEEP-DCA"            # durable and reasonably priced -> keep buying


def strategy_grade(r, f):
    """Route a row to the rubric that matches its job. Returns (grade, primary
    score 0..10) where primary is DCA-quality for dca, else the Growth score."""
    if r["strategy"] == "dca":
        q10, rich, _ = dca_quality(r["ticker"], f)
        return dca_grade(q10, rich, f), q10, rich
    return r["quad"], r["growth10"], None


# =========================================================================
# 6. LIVE REFRESH (optional) — fetch from stockanalysis.com and write a CSV
# =========================================================================
# Off by default. The committed CSV is the reproducible cache; --live overwrites
# it from the web (best-effort; the site's HTML can change, so failures fall
# back to whatever the CSV already holds). Intentionally light: it only fills
# the numeric fields it can parse, leaving blanks (-> neutral) otherwise.
def live_refresh(tickers, out_csv):
    import re
    import urllib.request

    def fetch(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", "ignore")

    def pct(html, label):
        m = re.search(re.escape(label) + r"\s*</td>\s*<td[^>]*>\s*(-?[\d.]+)%",
                      html, re.I)
        return m.group(1) if m else ""

    rows = []
    for t in tickers:
        slug = t.lower().split(".")[0]
        try:
            stats = fetch(f"https://stockanalysis.com/stocks/{slug}/statistics/")
        except Exception as e:
            print(f"  [live] {t}: fetch failed ({e}); keeping cached row")
            continue
        rows.append({
            "ticker": t,
            "mktcap_b": "", "fwd_rev_growth": "", "ttm_rev_growth": "",
            "fwd_eps_growth": "", "gross_margin": pct(stats, "Gross Margin"),
            "net_margin": pct(stats, "Profit Margin"),
            "fcf_positive": "", "peg": "", "pct_above_200dma": "",
            "pct_below_52w_high": "", "eps_beat_rate": "", "eps_beat_streak": "",
        })
        print(f"  [live] {t}: fetched")
    if rows:
        with open(out_csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=FUND_FIELDS)
            w.writeheader()
            w.writerows(rows)
        print(f"  [live] wrote {len(rows)} rows -> {out_csv}")
    return out_csv


# =========================================================================
# 7. RUN
# =========================================================================
def default_csv():
    """Pick the most recent scoring/fundamentals_*.csv."""
    cands = sorted(Path(ROOT, "scoring").glob("fundamentals_*.csv"))
    return str(cands[-1]) if cands else None


def render_by_strategy(results, fund, args):
    """Output grouped by strategy mode, each judged on its own rubric."""
    print(f"\n=== RATING BY STRATEGY  (csv={Path(args.csv).name}) ===")
    print("Each mode is graded on the job it does — DCA on quality+price, "
          "cycle/catalyst on the growth/discipline grid.")

    # ---- DCA: quality + valuation, NOT small/explosive ----
    dca = [r for r in results if r["strategy"] == "dca"]
    dca_scored = []
    for r in dca:
        f = fund.get(r["ticker"], {})
        q10, rich, _ = dca_quality(r["ticker"], f)
        dca_scored.append((r, q10, rich, dca_grade(q10, rich, f)))
    dca_scored.sort(key=lambda x: -x[1])
    print("\n-- DCA (steady compounders; buy on schedule) "
          "--------------------------")
    print(f"   {'ticker':10s} {'wv':3s} {'book%':>5s} {'QUALITY':>7s} "
          f"{'RICHNESS':>8s} {'grade':9s} {'F':>4s} {'V':>4s} {'C':>4s} "
          f"{'bind':5s} {'data%':>5s}")
    for r, q10, rich, grade in dca_scored:
        peak = " [PEAK?]" if r["peak"] else ""
        print(f"   {r['ticker']:10s} {r['wave']:3s} {r['book_pct']:5.2f} "
              f"{q10:7.1f} {rich:8.2f} {grade:9s} {_layer_cell(r['layers'])} "
              f"{_LAYER_ABBR[r['binding']]:5s} "
              f"{_cov_cell(r['coverage'])}{peak}")
    for grade, desc in [("KEEP-DCA", "durable + reasonably priced -> keep buying"),
                        ("RICH", "quality intact but price extended -> slow buys"),
                        ("IMPAIRED", "business cracking -> pause / reduce")]:
        names = [r["ticker"] for r, _, _, g in dca_scored if g == grade]
        print(f"     {grade:9s} ({len(names):2d}) {desc}")
        if names:
            print(f"               {', '.join(names)}")
    print()
    print(_DCA_FOOTNOTE)

    # ---- CYCLE & CATALYST: the existing two-axis grid is appropriate ----
    for mode, title in [("cycle", "CYCLE (buy the dip / sell the rip)"),
                        ("catalyst", "CATALYST (event-driven punts)")]:
        grp = [r for r in results if r["strategy"] == mode]
        print(f"\n-- {title} "
              + "-" * max(2, 46 - len(title)))
        print(f"   {'ticker':10s} {'wv':3s} {'book%':>5s} {'GROWTH':>6s} "
              f"{'8PT':>4s} {'quadrant':10s} {'F':>4s} {'V':>4s} {'C':>4s} "
              f"{'bind':5s} {'data%':>5s}")
        for r in grp:
            peak = " [PEAK?]" if r["peak"] else ""
            print(f"   {r['ticker']:10s} {r['wave']:3s} {r['book_pct']:5.2f} "
                  f"{r['growth10']:6.1f} {r['eight']:4.2f} {r['quad']:10s} "
                  f"{_layer_cell(r['layers'])} "
                  f"{_LAYER_ABBR[r['binding']]:5s} "
                  f"{_cov_cell(r['coverage'])}{peak}")

    print()
    print(_GROWTH_8PT_FOOTNOTE)
    print(_GAP_FOOTNOTE)
    print(_LAYER_FOOTNOTE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=default_csv(), help="fundamentals snapshot CSV")
    ap.add_argument("--live", action="store_true",
                    help="refresh the CSV from stockanalysis.com before scoring "
                         "(best-effort; falls back to cache on failure)")
    ap.add_argument("--watchlist", action="store_true",
                    help="also score WATCHLIST names (re-add / new-idea candidates)")
    ap.add_argument("--include-zero", action="store_true",
                    help="also score held 0%% stubs")
    ap.add_argument("--blend", choices=["balanced", "growth", "quality"],
                    help="ALSO show an optional blended composite (default: off — "
                         "two scores are kept separate)")
    ap.add_argument("--sort", choices=["growth", "eight", "blend"], default="growth",
                    help="rank by Growth (default), 8-Point, or the blend")
    ap.add_argument("--by-strategy", action="store_true",
                    help="group output by strategy mode and grade each on its OWN "
                         "rubric (DCA judged on quality+price, not small/explosive)")
    args = ap.parse_args()

    port = portfolio_rows(include_watchlist=args.watchlist)

    if args.live:
        target = args.csv or str(Path(ROOT, "scoring",
                                      "fundamentals_live.csv"))
        live_refresh([t for t in port if t != "SMHV.SW"], target)
        args.csv = target

    if not args.csv or not Path(args.csv).exists():
        sys.exit("No fundamentals CSV found. Create scoring/fundamentals_YYYY-MM-DD.csv "
                 "(see header in this file for columns) or pass --live.")

    fund = load_fundamentals(args.csv)

    results = []
    for t, info in port.items():
        if t == "SMHV.SW":
            continue  # fixed windfall, excluded per owner instruction
        if info["held"] and info["book_pct"] == 0 and not args.include_zero \
                and not args.watchlist:
            continue
        f = fund.get(t, {})
        eight, parts8, eps_f = score_8point(t, f, info)
        g10, partsg = score_growth(t, f, info)
        blend = composite(eight, g10, args.blend) if args.blend else None
        layers, binding = layer_scores(t, f, info)
        results.append({**info, "eight": eight, "growth10": g10, "blend": blend,
                        "quad": quadrant(eight, g10), "eps_f": eps_f,
                        "p8": parts8, "pg": partsg, "has_data": t in fund,
                        "coverage": _coverage(f),
                        "layers": layers, "binding": binding,
                        "peak": peak_trap(t, f, info)})

    keyf = {"growth": lambda r: -r["growth10"],
            "eight": lambda r: -r["eight"],
            "blend": lambda r: -(r["blend"] or 0)}[args.sort]
    results.sort(key=keyf)

    if args.by_strategy:
        render_by_strategy(results, fund, args)
        return

    # ----- two-score table (no forced blend) -----
    print(f"\n=== HOLDING RATING  (csv={Path(args.csv).name}, sort={args.sort}) ===")
    print("    Growth 0-10 (momentum-tolerant) | 8-Point 0-8 (anti-momentum) | "
          "Quadrant")
    hdr = f"{'rk':>2} {'ticker':10s} {'wv':3s} {'book%':>5s} " \
          f"{'GROWTH':>6s} {'8PT':>4s} {'quadrant':10s} {'epsF':>5s}"
    if args.blend:
        hdr += f" {'blend':>5s}"
    hdr += f" {'F':>4s} {'V':>4s} {'C':>4s} {'bind':5s} {'data%':>5s}"
    print(hdr)
    for i, r in enumerate(results, 1):
        line = f"{i:2d} {r['ticker']:10s} {r['wave']:3s} {r['book_pct']:5.2f} " \
               f"{r['growth10']:6.1f} {r['eight']:4.2f} {r['quad']:10s} " \
               f"{r['eps_f']:5.2f}"
        if args.blend:
            line += f" {r['blend']:5.2f}"
        peak = " [PEAK?]" if r["peak"] else ""
        line += f" {_layer_cell(r['layers'])} " \
                f"{_LAYER_ABBR[r['binding']]:5s} " \
                f"{_cov_cell(r['coverage'])}{peak}"
        print(line)
    print()
    print(_GROWTH_8PT_FOOTNOTE)
    print(_GAP_FOOTNOTE)
    print(_LAYER_FOOTNOTE)

    # ----- quadrant summary -----
    print("\n=== QUADRANTS ===")
    for q, desc in [("PRIME", "high growth AND disciplined -> size up"),
                    ("MOMENTUM", "high growth, extended/expensive -> starter/cap"),
                    ("QUALITY", "disciplined but slower -> ballast"),
                    ("AVOID", "neither -> trim / skip")]:
        names = [r["ticker"] for r in results if r["quad"] == q]
        print(f"  {q:9s} ({len(names):2d}) {desc}")
        if names:
            print(f"            {', '.join(names)}")

    # ----- wave-level averages (held movable sleeve only) -----
    print("\n=== WAVE AVERAGES (book-weighted, held, ex-SMHV) ===")
    agg = {}
    for r in results:
        if not r["held"] or r["book_pct"] == 0:
            continue
        a = agg.setdefault(r["wave"], [0.0, 0.0, 0.0])
        a[0] += r["book_pct"] * r["growth10"]
        a[1] += r["book_pct"] * r["eight"]
        a[2] += r["book_pct"]
    for w in sorted(agg):
        g, e, tot = agg[w]
        print(f"  {w}: book={tot:5.2f}%  growth={g/tot:4.1f}  8pt={e/tot:4.2f}"
              if tot else f"  {w}: (no book)")

    missing = [r["ticker"] for r in results if not r["has_data"]]
    if missing:
        print(f"\n(!) No fundamentals row (scored on forecast/tags only, "
              f"{len(missing)}): {', '.join(missing)}")


if __name__ == "__main__":
    main()
