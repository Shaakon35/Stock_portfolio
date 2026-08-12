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
#   PORTFOLIO_USE=ai python3 scoring/score_holdings.py --csv scoring/fundamentals_2026-08-04.csv
#   PORTFOLIO_USE=ai python3 scoring/score_holdings.py --blend growth --sort blend  # growth-weighted composite
# =========================================================================

import argparse
import csv
import datetime as _dt
import json
import os
import sys
from pathlib import Path

# --- locate repo root so the script runs from anywhere ---
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("PORTFOLIO_USE", "ai")

from portfolio.AI_allocations import (  # noqa: E402
    TARGET_WEIGHTS, W1_SILICON_TARGETS, W2_POWER_TARGETS, W3_DCINFRA_TARGETS,
    W4_CLOUD_TARGETS, W5_SOFTWARE_TARGETS, W6_SPEC_TARGETS, W7_DIVERSIFY_TARGETS,
    STRATEGY, WATCHLIST,
)
from portfolio.allocations import ETF_LOOK_THROUGH  # noqa: E402
from config.forecasts import WAVE_FORECASTS  # noqa: E402

# ETF book weights — SMHV.SW is the only ETF held in the AI book (a fixed 37.5%
# windfall). Its constituents (MU/TSM/LRCX/...) are therefore held INDIRECTLY:
# each carries an implied book% = (its weight inside SMHV) x (SMHV's book%).
# portfolio_rows() uses this to surface that pass-through exposure so the table
# shows e.g. MU ~5.4% / TSM ~2.8% instead of a misleading 0.00.
# NOTE (2026-06 model change): baskets now hold DIRECT book percentages
# (e.g. "SMHV.SW": 37.5 == 37.5% of book), so the ETF book FRACTION is just the
# basket value / 100 — no longer value * wave-weight.
_ETF_BOOK = {
    "SMHV.SW": W1_SILICON_TARGETS.get("SMHV.SW", 0.0) / 100.0,
}

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
    ("W7", "W7_DIVERSIFY", W7_DIVERSIFY_TARGETS),
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


def _etf_lookthrough_book():
    """Map each ETF constituent -> its implied INDIRECT book % via the ETFs held.

    For every ETF with a book weight in _ETF_BOOK, multiply each underlying's
    weight inside the ETF by the ETF's book %. A name held in several ETFs sums
    across them. Synthetic 'OTHER_*' buckets are skipped. Returns {ticker: pct}.
    """
    out = {}
    for etf, book_frac in _ETF_BOOK.items():
        holdings = ETF_LOOK_THROUGH.get(etf, {})
        for c, w in holdings.items():
            if c.startswith("OTHER"):
                continue
            out[c] = out.get(c, 0.0) + w * book_frac * 100
    return out


def portfolio_rows(include_watchlist=False):
    """Each held ticker with wave, sub-weight, book %, strategy, forecast band.
    With include_watchlist, also append WATCHLIST names (wave='WL').

    Watchlist names that are ETF constituents (e.g. SMHV's TSM/LRCX/MU) are NOT
    book=0: they are held INDIRECTLY through the ETF, so they get an `etf_pct`
    (sum of weight-in-ETF x ETF-book%) surfaced as their book%, tagged wave='ET'.
    """
    rows = {}
    for w, wk, basket in _WAVES:
        # NOTE (2026-06 model change): basket values are now DIRECT book percent,
        # so book_pct is just the value (no longer sub-weight * wave-weight).
        for t, sw in basket.items():
            lo, hi, mid = _forecast(t)
            rows[t] = {
                "ticker": t, "wave": w, "sub": sw, "book_pct": sw,
                "strategy": STRATEGY.get(t, "?"), "held": True,
                "cagr_lo": lo, "cagr_hi": hi, "cagr_mid": mid,
                "wl_pos": None, "etf_pct": 0.0,
            }
    etf_book = _etf_lookthrough_book()
    if include_watchlist:
        for t, v in WATCHLIST.items():
            if t in rows:
                continue  # already held directly; don't double-list
            cagr = v.get("cagr") if isinstance(v, dict) else None
            lo, hi = (cagr if cagr else (None, None))
            mid = (lo + hi) / 2.0 if (lo is not None and hi is not None) else None
            ep = etf_book.get(t, 0.0)
            rows[t] = {
                "ticker": t, "wave": ("ET" if ep > 0 else "WL"), "sub": 0.0,
                "book_pct": ep, "etf_pct": ep,
                "strategy": (v.get("strategy") if isinstance(v, dict) else "?"),
                "held": ep > 0, "cagr_lo": lo, "cagr_hi": hi, "cagr_mid": mid,
                "wl_pos": (v.get("pos") if isinstance(v, dict) else None),
            }
    # ETF constituents that are NOT on the watchlist (e.g. MU) — still held
    # indirectly, so surface them too when watchlist scoring is on.
    if include_watchlist:
        for t, ep in etf_book.items():
            if t in rows or ep <= 0:
                continue
            lo, hi, mid = _forecast(t)
            rows[t] = {
                "ticker": t, "wave": "ET", "sub": 0.0,
                "book_pct": ep, "etf_pct": ep,
                "strategy": STRATEGY.get(t, "?"), "held": True,
                "cagr_lo": lo, "cagr_hi": hi, "cagr_mid": mid,
                "wl_pos": None,
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
    # Cycle-strategy holdings that were silently defaulting to "Mid" — tagged
    # deliberately so the CYCLE layer / 8-Point P5 reflect real wave position:
    #   APP  adtech software, extended multi-year run, growth maturing -> Mid/Late
    #   CLS  AI-hardware ODM riding datacenter capex, mid of buildout   -> Mid
    #   INOD small-cap AI data-prep services, ramp just beginning       -> Early/Mid
    #   NU   LatAm neobank still expanding (low penetration)            -> Early/Mid
    #   RDDT newly public, ad-monetization ramp early                   -> Early/Mid
    #   TLN  IPP power on datacenter-demand run, extended (cf CEG/GEV)   -> Late
    "APP": "Mid/Late", "CLS": "Mid", "INOD": "Early/Mid",
    "NU": "Early/Mid", "RDDT": "Early/Mid", "TLN": "Late",
    # Promoted from WATCHLIST to held cycle legs in the 2026-08 reshape (#14);
    # tagged to match the 'pos' they carried as watchlist entries:
    #   RHM.DE defense rearmament super-cycle (multi-year backlog) -> Mid
    #   WPM    gold/silver streaming, commodity-cyclical           -> Mid
    "RHM.DE": "Mid", "WPM": "Mid",
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


def untagged_cycle_holdings():
    """Return held cycle-strategy tickers with NO explicit CYCLE_POS tag.

    For a `cycle` name the wave position IS the thesis, so silently defaulting
    to "Mid" (via cycle_of) makes its CYCLE layer and 8-Point P5 meaningless.
    A held name always has wl_pos=None, so its only source of a real tag is
    CYCLE_POS — hence the check is CYCLE_POS membership, not cycle_of. Held
    `dca`/`catalyst` compounders are intentionally allowed to default (cycle
    position is not a meaningful axis for them), so they are NOT flagged.
    Returns a sorted list; empty == all cycle holdings deliberately tagged.
    """
    port = portfolio_rows(include_watchlist=False)  # held names only
    return sorted(
        t for t, info in port.items()
        if info.get("strategy") == "cycle" and t not in CYCLE_POS
    )


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


def _num_list(s):
    """Parse a pipe-separated series ('28.6|19.5|33.8') into a list of floats,
    skipping blanks. Returns [] for empty/missing. Used for rev_growth_hist."""
    s = (s or "").strip()
    if not s:
        return []
    out = []
    for part in s.split("|"):
        v = _num(part)
        if v is not None:
            out.append(v)
    return out


def load_fundamentals(path):
    out = {}
    with open(path, newline="") as fh:
        # Skip leading '#' comment lines so the real header row is used by DictReader.
        lines = [ln for ln in fh if not ln.lstrip().startswith("#")]
    for row in csv.DictReader(lines):
        t = (row.get("ticker") or "").strip()
        if not t or t.startswith("#"):
            continue
        rec = {k: _num(row.get(k)) for k in FUND_FIELDS if k != "ticker"}
        # rev_growth_hist is a pipe-separated trailing-FY YoY% series (most-recent
        # first), kept OUTSIDE the numeric FUND_FIELDS schema so it neither breaks
        # _num parsing nor inflates the data% coverage denominator. It powers the
        # multi-year trend baseline in _trend_adjust (median of the series).
        rec["rev_growth_hist"] = _num_list(row.get("rev_growth_hist"))
        # net_margin_hist is a pipe-separated trailing net-margin % series (TTM
        # first, then full FYs, newest-first), kept OUTSIDE the numeric
        # FUND_FIELDS schema like rev_growth_hist so it neither breaks _num
        # parsing nor inflates data%. It powers the margin-expansion sub-score
        # (_margin_trend) in the FUND + DCA quality blends.
        rec["net_margin_hist"] = _num_list(row.get("net_margin_hist"))
        out[t] = rec
    return out


# =========================================================================
# 3. EPS-SURPRISE CORRECTION
# =========================================================================
# Persistent beaters: consensus is too LOW -> their forward growth AND PEG are
# understated. We nudge forward-growth UP and PEG DOWN (cheaper) for beaters,
# and the reverse for missers. beat_rate in [0,1] (fraction of last ~8 qtrs
# beaten); streak is consecutive beats (caps the bonus). Neutral at 0.5.
# Correction is intentionally MILD (asymmetric: up to +12% for a perfect beater,
# down to -10% for a perfect misser — the streak bonus only adds on the upside)
# so it tilts, never dominates.
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


# --- GROWTH-BAND CONVENTION (why the same metric uses different (lo,hi)) -----
# Forward revenue and forward EPS growth are scored in several places, and the
# (lo,hi) band differs ON PURPOSE because each scorer asks a different question.
# The band sets what counts as "10%" vs "full marks"; a higher ceiling makes the
# SAME growth number score LOWER (it now has to clear a taller bar). The bands:
#
#   rev-growth band   eps-growth band   used by        rationale
#   --------------    ---------------   -----------    --------------------------
#   (5, 45)           (5, 50)           8-Point P3 /   the "ownership screen" bar:
#                                       FUND layer     a disciplined entry wants
#                                                      real but not frothy growth.
#   (5, 50)           (5, 60)           GROWTH score   the return-MAXIMISING bar:
#                                                      momentum-tolerant, so it
#                                                      keeps separating names that
#                                                      are already pinned at the
#                                                      top of the tighter screen.
#   (6, 25)           (6, 30)           DCA quality    DCA wants DURABLE, not
#                                                      explosive: a steady 25%
#                                                      compounder should max this
#                                                      axis; hypergrowth is not the
#                                                      job, so the ceiling is low.
#
# CONSEQUENCE / KNOWN LIMITATION: because the GROWTH ceiling (50/60) is higher
# than the 8-Point/FUND ceiling (45/50), the FUND-layer F score and the GROWTH
# score can rank the SAME pair of names in a slightly different order purely from
# the ceiling, even though both read the same underlying number. This is accepted
# (the two axes are meant to answer different questions), but it is the reason a
# name can look marginally "better on F than on GROWTH" or vice-versa. If the two
# axes ever need to agree, unify these bands.
# ----------------------------------------------------------------------------


# --- TREND adjustment: reward re-acceleration, PENALISE deceleration --------
# A forward growth number in isolation hides whether the business is speeding up
# or rolling over. CCJ's fwd_rev 7.4% looks merely "slow", but against its multi-
# year trend (~21% median, 38->21->11->7) it is a growth CLIFF the snapshot
# misses. This applies a single symmetric adjustment to any growth sub-score:
#   fwd materially ABOVE the trend -> re-acceleration BONUS  (the upside side)
#   fwd materially BELOW the trend -> deceleration PENALTY   (the downside side)
#
# BASELINE = the MEDIAN of the trailing multi-year YoY series (rev_growth_hist),
# NOT a single year. A one-year baseline is fragile for young hypergrowth names:
# CRDO printing 206% off a tiny base would brand *any* forward number a
# "collapse", and VRT's quiet multi-year ramp (14->28%) would read as flat. The
# median absorbs a single spiky year and captures the sustained trajectory, so:
#   - CCJ (38/21/11/7, med 21) vs fwd 7  -> correctly penalised (one-year missed it)
#   - VRT (14/14/21/17/28, med 17) vs fwd 28 -> correctly a re-accel BONUS
#   - CRDO (81/73/5/126/206, med 81) vs fwd 50 -> still decel, but -31 not -155
# Falls back to the single-year ttm_rev_growth when no history is present, and
# returns the score unchanged when neither baseline nor fwd is available.
#
# BASE-EFFECT DAMPING (the horizon-mismatch correction): `fwd` is a FORWARD 3Y
# CAGR while the baseline is a TRAILING per-year YoY. A name growing off a tiny
# base (ALAB 115/242/45, IONQ ~150 median) MUST show a lower forward CAGR — that
# is arithmetic (you cannot sustain triple-digit YoY), not deceleration. Judged
# raw, such names eat the full penalty for simply maturing. So the DECELERATION
# penalty is scaled DOWN when the trailing baseline sits in the base-effect zone
# (above _TREND_HOT_BASE), fading to ~0 by _TREND_HOT_FADE above it:
#   - CCJ (base 21)  -> base normal      -> full penalty kept (real slowdown)
#   - CRDO (base 81) -> mildly hot       -> penalty ~80% (still flagged)
#   - ALAB (base 115)-> hot              -> penalty ~45% (maturation, softened)
#   - IONQ (base 150)-> very hot         -> penalty ~10% (pure base effect)
# The damping applies to the DOWNSIDE ONLY: a re-acceleration bonus off a high
# base is still a genuine positive signal and is left at full strength.
#
# "Materially" is a deadband (_TREND_DEADBAND, pts of growth) so ordinary wobble
# does not move the score; magnitude scales with the gap up to a cap.
_TREND_DEADBAND = 5.0     # pts of growth: ignore gaps smaller than this
_TREND_FULL = 25.0        # pts: gap at/above this gets the full adjustment
_TREND_BONUS_MAX = 0.15   # max upward nudge (matches the old re-accel bonus)
_TREND_PENALTY_MAX = 0.25  # max downward nudge; decel is judged the harder risk
_TREND_HOT_BASE = 60.0    # trailing baseline above this is base-effect-dominated:
#                           a forward CAGR cannot be compared to it like-for-like
_TREND_HOT_FADE = 100.0   # pts above _TREND_HOT_BASE over which the decel penalty
#                           fades from full to ~0 (base 160+ -> penalty ~0)


def _decel_damping(base):
    """0..1 multiplier on the DECELERATION penalty. 1.0 when the trailing
    baseline is in the normal range (<= _TREND_HOT_BASE); fades linearly to 0
    as the baseline climbs _TREND_HOT_FADE pts beyond it. This neutralises the
    false 'cliff' that the forward-CAGR-vs-trailing-YoY horizon mismatch creates
    for names growing off a tiny base (see BASE-EFFECT DAMPING above)."""
    if base is None or base <= _TREND_HOT_BASE:
        return 1.0
    return max(0.0, 1.0 - (base - _TREND_HOT_BASE) / _TREND_HOT_FADE)


def _trend_baseline(f):
    """The trailing-growth baseline the forward forecast is judged against:
    the MEDIAN of the multi-year rev_growth_hist series (robust to one spiky
    year), or the single-year ttm_rev_growth when no history exists, or None."""
    hist = f.get("rev_growth_hist") or []
    if len(hist) >= 2:
        import statistics
        return statistics.median(hist)
    if len(hist) == 1:
        return hist[0]
    return f.get("ttm_rev_growth")


def _trend_adjust(score, fwd, f):
    """Nudge a 0..1 growth sub-score by fwd-vs-trend. Re-acceleration (fwd above
    the multi-year median) lifts it, deceleration cuts it, deadband ignores
    noise. The DECELERATION side is damped when the trailing baseline sits in the
    base-effect zone (a forward CAGR cannot be compared like-for-like to a triple-
    digit trailing YoY — see BASE-EFFECT DAMPING). `f` supplies the history."""
    if score is None or fwd is None:
        return score
    base = _trend_baseline(f)
    if base is None:
        return score                      # no trailing signal -> leave untouched
    gap = fwd - base                      # >0 accelerating, <0 decelerating
    if abs(gap) <= _TREND_DEADBAND:
        return score                      # within noise -> leave untouched
    # fraction of the way from the deadband edge to the full-effect threshold
    span = max(_TREND_FULL - _TREND_DEADBAND, 1e-9)
    mag = min((abs(gap) - _TREND_DEADBAND) / span, 1.0)
    if gap > 0:
        return min(1.0, score + mag * _TREND_BONUS_MAX)   # bonus: full strength
    # deceleration: scale the penalty down for base-effect-dominated names so a
    # maturing hypergrowth name is not falsely branded a "cliff" (Option D).
    damp = _decel_damping(base)
    return max(0.0, score - mag * _TREND_PENALTY_MAX * damp)


# --- MARGIN-EXPANSION sub-score: is profitability IMPROVING or COMPRESSING? --
# Level alone (the net_margin snapshot) cannot tell a -5%->+1% turnaround from a
# 20%->11% melt: both can print "low single-digit margin" today. Margin
# *trajectory* is one of the strongest forward-return signals there is — a
# business climbing the operating-leverage curve re-rates, one whose margins are
# rolling over de-rates. This reads the trailing net_margin_hist series (TTM
# first, then full FYs, newest-first — same shape as rev_growth_hist) and scores
# the DRIFT in margin POINTS from the older half of the window to the newer half:
#   expanding  (newer margins > older) -> high score (1.0 at +_MARGIN_FULL pts)
#   flat                               -> neutral 0.5 (inside the deadband)
#   compressing(newer < older)         -> low score  (0.0 at -_MARGIN_FULL pts)
# It is a SELF-CONTAINED 0..1 sub-score (unlike _trend_adjust, which nudges an
# existing growth band), blended at modest weight into FUND quality + DCA
# quality so margin direction informs "is this a good business?" without
# swamping the level term. Returns None when fewer than 2 points exist (no
# trajectory to read) so _blend drops it instead of faking a neutral.
_MARGIN_DEADBAND = 1.0    # pts of margin: ignore drift smaller than this (noise)
_MARGIN_FULL = 8.0        # pts: drift at/above this maps to the 0 or 1 extreme

# PROFITABILITY GATE (turnaround-illusion guard) — expansion reward only.
# The drift term alone rewards the SHAPE of the margin line, so a name going
# from -38% -> -14% net margin earns full "expanding" credit while it is STILL
# losing money. That is the base-effect / turnaround illusion (see SKILL.md
# Common Pitfalls Sec.10; it is why PD printed CONV 8.2 on -13.6% net margins).
# We gate the reward ABOVE 0.5 by the newer-half margin LEVEL: at/below
# _MARGIN_GATE_LO the expansion bonus is fully damped to neutral, ramping to
# full credit at/above _MARGIN_GATE_HI. Only the UPSIDE is gated — the
# compression penalty (drift<0) is left intact, exactly like _decel_damping
# only softens the downside of the revenue-trend term. A profitable expander
# (ANET 38%, DOCU 19%) is unaffected; a still-bleeding one (PD, AFRM, ASAN) is
# no longer flattered.
_MARGIN_GATE_LO = 0.0     # newer-half margin % at/below this: expansion reward -> 0
_MARGIN_GATE_HI = 8.0     # newer-half margin % at/above this: full expansion reward


def _margin_trend(f):
    """Score net-margin TRAJECTORY 0..1 (1=expanding, .5=flat, 0=compressing),
    or None when there is no usable history. Compares the mean of the newer half
    of net_margin_hist to the mean of the older half, in margin POINTS. The
    expansion (drift>0) reward is gated by the newer-half margin LEVEL so a
    still-unprofitable turnaround does not earn full marks (see the
    PROFITABILITY GATE note above)."""
    hist = f.get("net_margin_hist") or []
    if len(hist) < 2:
        return None                       # no trajectory -> let _blend drop it
    # series is newest-first; split into newer vs older halves (odd length: the
    # middle point is shared/ignored so each half is a clean recent/old sample).
    half = len(hist) // 2
    newer = hist[:half]
    older = hist[-half:]
    newer_mean = sum(newer) / len(newer)
    drift = newer_mean - (sum(older) / len(older))  # +expand / -compress
    if abs(drift) <= _MARGIN_DEADBAND:
        return 0.5                        # essentially flat -> neutral
    # map drift in [-_MARGIN_FULL, +_MARGIN_FULL] onto [0, 1] around 0.5
    norm = max(-1.0, min(1.0, drift / _MARGIN_FULL))
    raw = 0.5 + 0.5 * norm
    if drift > 0:
        # Gate the expansion bonus by how profitable the business ACTUALLY is
        # now — improving losses is not the same as expanding profits.
        gate = _band(newer_mean, _MARGIN_GATE_LO, _MARGIN_GATE_HI)
        gate = 0.0 if gate is None else gate
        return 0.5 + (raw - 0.5) * gate
    return raw                            # compression penalty untouched


# -------------------------------------------------------------------------
# GROSS-MARGIN QUALITY (inherent business-model quality, independent of net)
# -------------------------------------------------------------------------
# net_margin alone cannot separate a structurally premium model under temporary
# cost pressure from an inherently thin-margin commodity: SMCI (gross ~8%) and
# HUBS (gross ~84%) can both print a ~5% NET margin yet are completely different
# businesses, and a pre-profit SaaS name (SNOW ~67% gross / -24% net, RBRK ~81%
# / -20%) is branded "bad business" by the net-margin term despite an excellent
# model. Across the snapshot, gross and net correlate only ~0.21, so gross
# carries large INDEPENDENT signal the engine was discarding. This reads the
# gross_margin column (already in the CSV, scraped but previously unscored) as a
# self-contained 0..1 model-quality sub-score, blended at modest weight into
# FUND + DCA quality alongside the net-margin LEVEL and TRAJECTORY terms.
#   ~30% gross -> 0.0 (commodity/box-shifter)  ~80%+ -> 1.0 (premium model)
# Returns None when gross_margin is absent so _blend drops it (no faked neutral).
_GROSS_LO = 30.0     # gross margin %: floor of the scoring band (commodity)
_GROSS_HI = 80.0     # gross margin %: ceiling of the band (premium model)


def _gross_quality(f):
    """Score gross-margin LEVEL 0..1 (model quality), or None when absent.
    High gross = structurally premium business model, independent of whether the
    name is net-profitable yet — so a high-gross pre-profit compounder is not
    mis-scored as a low-quality business by net margin alone."""
    return _band(f.get("gross_margin"), _GROSS_LO, _GROSS_HI)


# -------------------------------------------------------------------------
# REVENUE CONSISTENCY (reliability of the growth series, not its level)
# -------------------------------------------------------------------------
# A name compounding 15/15/16/14 is a more reliable business than one printing
# 100/-50/80 even at the same MEAN/median growth — but the trend term only reads
# the median (level), never the DISPERSION. This scores the steadiness of the
# rev_growth_hist series via its coefficient of variation (stdev / |mean|), so a
# tight series scores high (safe/reliable) and a whipsaw series scores low. It
# uses data already in the CSV, sits OUTSIDE the numeric FUND_FIELDS schema (no
# data% impact), and feeds the FUND + DCA quality blends at low weight as a
# RELIABILITY signal — it rewards predictability, never penalises fast growth
# per se (a steady hypergrower still scores high).
#   CV <= _RC_TIGHT  -> 1.0 (metronomic)   CV >= _RC_LOOSE -> 0.0 (erratic)
# Returns None when fewer than 3 points exist (too short to judge variance).
_RC_MIN_POINTS = 3   # need >=3 FY points before variance is meaningful
_RC_TIGHT = 0.20     # coeff. of variation at/below this -> fully reliable (1.0)
_RC_LOOSE = 1.20     # coeff. of variation at/above this -> fully erratic  (0.0)


def _rev_consistency(f):
    """Score revenue-growth CONSISTENCY 0..1 (1=steady, 0=erratic), or None when
    the history is too short. Based on the coefficient of variation of the
    rev_growth_hist series — dispersion, not level — so it rewards reliability
    without penalising the SPEED of a steady compounder."""
    hist = f.get("rev_growth_hist") or []
    if len(hist) < _RC_MIN_POINTS:
        return None                       # too short to judge variance -> drop
    n = len(hist)
    mean = sum(hist) / n
    if abs(mean) < 1e-9:
        return None                       # mean ~0: CV undefined -> drop
    var = sum((x - mean) ** 2 for x in hist) / n     # population variance
    cv = (var ** 0.5) / abs(mean)                     # coefficient of variation
    # invert+clamp: tight CV -> 1.0, loose CV -> 0.0 (linear between the bands)
    return _band_inv(cv, _RC_TIGHT, _RC_LOOSE)


# -------------------------------------------------------------------------
# VALUATION CHEAPNESS — PEG (trough-damped) + ABSOLUTE P/S co-signal
# -------------------------------------------------------------------------
# The VAL layer and the 8-Point P6 point both answer "how much of the business
# is already in the price?". Historically both were PEG-FIRST with a P/S-vs-
# growth FALLBACK — i.e. when a PEG existed, P/S was never consulted. Two blind
# spots followed, both visible on BESI.AS (Aug-2026 snapshot):
#
#   1. ABSOLUTE price ignored. PEG = P/E / growth, so a name at 22x SALES can
#      still screen "cheap" purely because a big growth number shrinks its PEG.
#      P/S never registered. FIX: blend an ABSOLUTE, growth-independent P/S term
#      (_abs_ps_cheapness) in as a CO-SIGNAL alongside PEG, so a rich sales
#      multiple always pulls VAL down even when the PEG looks generous.
#
#   2. TROUGH PEGs flatter cyclicals. A cyclical's forward EPS growth spikes off
#      a depressed trough (BESI fwd EPS growth 161%), which mechanically crushes
#      its PEG toward zero and screens it "dirt cheap" exactly when earnings are
#      most depressed and the rebound is already consensus — the mirror image of
#      the peak-PEG trap. FIX: DAMP the PEG's cheapness toward neutral when a
#      CYCLICAL name's forward EPS growth is extreme (_trough_peg_damping),
#      mirroring the base-effect damping already applied to the trend penalty.
#
# Both terms use columns ALREADY in every CSV row (ps_ratio, gross_margin, peg,
# fwd_eps_growth) — no new sourcing, deterministic, auto-applies to all tickers.
# _val_cheapness() is the single shared computation both P6 and VAL now call, so
# they can never drift apart.

# --- absolute P/S co-signal (margin-normalized) ---
# Raw P/S is not comparable across business models: a 90%-gross software name
# legitimately earns a higher sales multiple than a 40%-gross hardware name. So
# the P/S is NORMALIZED by gross margin (a stable, through-cycle proxy for model
# quality — NOT growth, which is the trough-inflated number that caused the bug)
# before scoring. Bands are calibrated to the book's own distribution of the
# normalized ratio: ~p25 -> cheap (1.0), ~p90 -> expensive (0.0).
_ABSPS_GROSS_BASE = 50.0   # gross-margin baseline the P/S is normalized to
_ABSPS_LO = 3.0            # margin-normalized P/S at/below this -> cheap (1.0)
_ABSPS_HI = 20.0           # margin-normalized P/S at/above this -> expensive (0.0)


def _abs_ps_cheapness(f):
    """Absolute, growth-independent P/S cheapness 0..1 (1=cheap), or None when
    P/S is absent. P/S is gross-margin-normalized so premium models are allowed
    a higher multiple; the result is the co-signal that makes a rich SALES
    multiple register in VAL even when the PEG looks cheap."""
    ps = f.get("ps_ratio")
    if ps is None or ps <= 0:
        return None
    gm = f.get("gross_margin")
    if gm is not None and gm > 5:          # normalize by model quality
        ps = ps / (gm / _ABSPS_GROSS_BASE)  # high-gross names earn a higher P/S
    return _band_inv(ps, _ABSPS_LO, _ABSPS_HI)


# --- trough-PEG damping (mirror of the trend base-effect damping) ---
# A cyclical whose forward EPS growth is extreme is rebounding off a trough, so
# its low PEG is fake-cheap. The damping pulls that PEG cheapness toward neutral,
# fading from no-damping at _TROUGH_EPS_HOT to a floor as growth climbs
# _TROUGH_EPS_FADE points beyond it. Applies to CYCLICALS only (a stable-growth
# name at 100%+ EPS growth is a genuine hypergrower, not a trough rebound) and to
# the DOWNWARD (cheapness-reducing) direction only, exactly like _decel_damping.
_TROUGH_EPS_HOT = 100.0    # fwd EPS growth above this on a cyclical = trough snap
_TROUGH_EPS_FADE = 100.0   # pts beyond _HOT over which damping reaches its floor
_TROUGH_PEG_FLOOR = 0.2    # strongest damping: keep >=20% of the cheapness signal


def _trough_peg_damping(t, f):
    """0..1 multiplier applied to a cyclical's PEG cheapness (as pull-to-neutral
    strength). 1.0 = no damping. Only cyclicals with extreme forward EPS growth
    (a trough rebound) are damped; everything else is untouched."""
    if t not in _CYCLICAL:
        return 1.0
    g = f.get("fwd_eps_growth")
    if g is None or g <= _TROUGH_EPS_HOT:
        return 1.0
    frac = min(1.0, (g - _TROUGH_EPS_HOT) / _TROUGH_EPS_FADE)
    return 1.0 - frac * (1.0 - _TROUGH_PEG_FLOOR)


# cyclical multiples mislead at cycle extremes -> pull the whole cheapness score
# toward neutral (the softening that was previously inline in P6 and VAL).
_CYCLICAL_SOFTEN = 0.6
_VAL_PEG_W = 1.6      # weight of the PEG/PS-vs-growth leg in cheapness
_VAL_ABSPS_W = 1.0    # weight of the absolute margin-normalized P/S co-signal


def _val_cheapness(t, f):
    """Shared VAL/P6 cheapness 0..1 (1=cheap), or None when neither a PEG/PS-vs-
    growth leg nor an absolute P/S leg is available. Combines:
      * PEG-first (P/S-vs-growth fallback) leg, trough-damped for cyclicals, and
      * an absolute, margin-normalized P/S co-signal (always consulted),
    then softens the whole score toward neutral for cyclicals. This is the single
    source of truth both the 8-Point P6 and the VAL layer call."""
    peg = f.get("peg")
    if peg is not None:
        peg_leg = _band_inv(peg, 0.8, 3.5)
        damp = _trough_peg_damping(t, f)      # trough rebound -> pull to neutral
        if peg_leg is not None and damp < 1.0:
            peg_leg = 0.5 + (peg_leg - 0.5) * damp
    else:
        # Fallback: price/sales judged against forward growth (crude PEG-on-sales).
        ps = f.get("ps_ratio")
        if ps is None:
            peg_leg = None
        else:
            g = f.get("fwd_rev_growth")
            denom = max(g, 10.0) if g is not None else 25.0
            peg_leg = _band_inv(ps / (denom / 10.0), 1.0, 15.0)
    abs_leg = _abs_ps_cheapness(f)            # absolute P/S co-signal
    present = [(v, w) for v, w in ((peg_leg, _VAL_PEG_W), (abs_leg, _VAL_ABSPS_W))
               if v is not None]
    if not present:
        return None                           # nothing to score -> let caller drop
    cheap = sum(v * w for v, w in present) / sum(w for _, w in present)
    if t in _CYCLICAL:
        cheap = 0.5 + (cheap - 0.5) * _CYCLICAL_SOFTEN   # cycle-extreme softening
    return cheap


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
#   pct_below_52w_high - no clean 52w-high distance field; P8 uses 200DMA
#   eps_beat_rate      - /earnings/ estimate-vs-actual table 404s; unscrapable
#   eps_beat_streak    - same source gap as eps_beat_rate
# ttm_rev_growth was here but is in fact sourceable: the /financials/ page
# embeds a `financialData.revenueGrowth` JSON array (index 1 = latest FY YoY).
# It now powers the deceleration penalty, so it is a real, counted field; see
# the sourcing helper in section 6.
_UNSOURCEABLE = frozenset({
    "pct_below_52w_high", "eps_beat_rate", "eps_beat_streak",
})

# Names whose stockanalysis.com feed is SOURCE-CORRUPTED in this environment
# (wrong security's numbers served under the ticker). Any auto-scraper —
# --sync-csv AND --fill-ttm — must skip these so a run never overwrites a
# hand-curated row with garbage. MU's page currently reports ~$1.1T mktcap /
# 72% gross / 56% net / PEG 0.04 (an AI-designer profile, impossible for a
# memory maker). Its CSV row is therefore HAND-CURATED from real peer-
# calibrated figures; see the '# MU (hand-curated)' note in the snapshot header.
_SOURCE_CORRUPT = frozenset({"MU"})


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
    "renormalized away).\n"
    "  wv=ET = held INDIRECTLY via the SMHV.SW ETF; its book% is the pass-"
    "through weight\n"
    "        (constituent weight in SMHV x SMHV's 37.5% book), not a separate "
    "position.\n"
    "        Excluded from the wave averages so it is not double-counted with "
    "SMHV itself."
)

# --- per-score explanations shown under each table -----------------------
# GROWTH + 8-POINT live on the two-axis grid (cycle/catalyst hunt + the main
# holding table); QUALITY + RICHNESS are the DCA rubric. Each metric is spelled
# out here so a reader can interpret a number without reading the source.
_GROWTH_8PT_FOOTNOTE = (
    "  GROWTH 0-10 (higher = faster, momentum-TOLERANT): a weighted blend of\n"
    "        forward revenue growth (45%), forward EPS growth (40%) and secular\n"
    "        runway (15%). All forward figures are EPS-surprise corrected (serial\n"
    "        beaters nudged up, missers down). It answers \"how much can this\n"
    "        compound?\" and does NOT punish an extended chart.\n"
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
    "  QUALITY 0-10 (higher = better business): durable margins, durable\n"
    "        forward revenue growth, forward EPS growth, free-cash-flow\n"
    "        positivity, and net-margin TRAJECTORY (expanding margins lift it,\n"
    "        compression cuts it — direction, not just level). Unlike 8PT it does\n"
    "        NOT penalise size or an extended chart — a proven large compounder is\n"
    "        meant to score well here. It answers \"is this still a great\n"
    "        business?\".\n"
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
    "    F=FUND  business quality (net+gross margin+margin-trend+growth+rev-consistency+FCF)  wins the LONG run\n"
    "    V=VAL   price vs the business (PEG + absolute P/S + extension) . mean-reverts (months)\n"
    "    C=CYC   cycle position + crowding (pos+neck+chart) .. drives the SHORT run / hype\n"
    "  bind = the BINDING (lowest) layer: the dominant risk you take buying here.\n"
    "  [PEAK?] = a cyclical/late name's low PEG is fake-cheap (peak earnings) on an\n"
    "          extended chart — the SK Hynix / Micron trap. Treat its VAL as a warning.\n"
    "  [MARG?] = an EARLY-cycle name whose net margin is COMPRESSING — tag and data\n"
    "          disagree (thesis unwinding or stale tag). VAL now blends an ABSOLUTE,\n"
    "          margin-normalized P/S so a rich SALES multiple registers even when the\n"
    "          PEG looks cheap, and a cyclical's TROUGH-inflated PEG is damped toward\n"
    "          neutral (mirror of the peak trap)."
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
    # P3 growth accelerating: fwd rev growth, EPS-surprise corrects the forward
    #     figure, then a symmetric TREND adjustment — re-acceleration lifts it,
    #     deceleration (fwd << ttm, the CCJ growth-cliff case) cuts it.
    fwd = f.get("fwd_rev_growth")
    fwd_corr = None if fwd is None else fwd * eps_f
    p3 = _band(fwd_corr, 5, 45)   # ownership-screen bar; see GROWTH-BAND CONVENTION
    p3 = _trend_adjust(p3, fwd, f)
    # P4 bottleneck (owner tag); unknown watchlist names -> neutral 0.3.
    p4 = BOTTLENECK.get(t, 0.3)
    # P5 secular & early (cycle position).
    p5 = _CYCLE_P5.get(cycle_of(t, info), 0.5)
    # P6 not priced for perfection. Shared cheapness (_val_cheapness): PEG-first
    #    (trough-damped for cyclicals) BLENDED with an absolute margin-normalized
    #    P/S co-signal, then softened toward neutral for cyclicals; falls back to
    #    P/S-vs-growth when no PEG so valuation discipline still applies instead
    #    of dropping the point. NB: the EPS-surprise factor is intentionally NOT
    #    applied here — it already lifts the growth inputs (P3), and PEG embeds
    #    EPS, so correcting both double-counts a single signal.
    p6 = _val_cheapness(t, f)
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

    # return-MAXIMISING bars (higher ceiling than the screen); see
    # GROWTH-BAND CONVENTION above for why these differ from P3 / FUND / DCA.
    g_rev = _band(fwd_corr, 5, 50)                       # forward revenue
    g_rev = _trend_adjust(g_rev, fwd, f)  # decel bites
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
    # FUND uses the same (lower) bars as the 8-Point screen, NOT the GROWTH
    # ceiling; see GROWTH-BAND CONVENTION above.
    fwd = f.get("fwd_rev_growth")
    l_rev = _band(None if fwd is None else fwd * eps_f, 5, 45)
    l_rev = _trend_adjust(l_rev, fwd, f)   # decel bites
    eps_g = f.get("fwd_eps_growth")
    l_eps = _band(None if eps_g is None else eps_g * eps_f, 5, 50)
    if fcf == 1:
        l_fcf = 1.0
    elif fcf == 0:
        l_fcf = 0.5 if (nm is not None and nm > 0) else 0.0
    else:
        l_fcf = None                                  # nothing known -> drop
    # margin TRAJECTORY (expanding/compressing); None when no history -> dropped
    l_mtrend = _margin_trend(f)
    # gross-margin LEVEL (model quality, independent of net) and revenue-growth
    # CONSISTENCY (reliability of the series); both None when absent -> dropped.
    l_gross = _gross_quality(f)
    l_rcons = _rev_consistency(f)
    fund10, _ = _blend([(l_margin, 3.5), (l_rev, 2.5), (l_eps, 2.0),
                        (l_fcf, 2.0), (l_mtrend, 1.5), (l_gross, 1.5),
                        (l_rcons, 1.0)], scale=10.0,
                       risk_penalize=spec)

    # --- VAL (Layer 2): how much of the business is already in the price -
    #     Higher = cheaper / fairer. Shared cheapness (_val_cheapness): PEG-first
    #     (trough-damped for cyclicals) BLENDED with an absolute margin-normalized
    #     P/S co-signal so a rich SALES multiple always registers (P/S-vs-growth
    #     fallback when no PEG), softened toward neutral for cyclicals (the
    #     peak/trough trap; see peak_trap). Plus distance above the 200DMA —
    #     extension IS paid-up optimism.
    v_peg = _val_cheapness(t, f)
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
# 4d. MARGIN-vs-CYCLE CONFLICT — an "Early" cyclical with FALLING margins.
# =========================================================================
# A name tagged EARLY in its cycle should have margins rising off the trough. A
# cyclical carrying an Early/Early-Mid tag while its net-margin trajectory is
# COMPRESSING is internally contradictory: either the tag is stale or the "early"
# thesis is already unwinding. BESI.AS is the case in point — tagged Early, yet
# net margin fell 37.7 -> 33.3 -> 30.6 -> 30.0 over the window. Like peak_trap,
# this ONLY annotates (adds a [MARG?] flag); it changes no score. It reuses the
# margin-trajectory signal the engine already computes (_margin_trend) and the
# cycle tag, so it needs no new data and applies uniformly to every ticker.
_MARGIN_FLAG_MAX = 0.4   # _margin_trend at/below this = clearly compressing
_MARGIN_FLAG_CYCLES = ("Early", "Early/Mid")   # tags that imply RISING margins


def margin_flag(t, f, info):
    """True when a name tagged EARLY in the cycle has a COMPRESSING net-margin
    trajectory — the tag and the data disagree. Annotation only (no score
    change); returns False when there is no margin history or the name is not
    an early-cycle cyclical."""
    if t not in _CYCLICAL and cycle_of(t, info) not in _MARGIN_FLAG_CYCLES:
        return False
    if cycle_of(t, info) not in _MARGIN_FLAG_CYCLES:
        return False
    mt = _margin_trend(f)
    return mt is not None and mt <= _MARGIN_FLAG_MAX


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
# 5a. CONVICTION — a CONTINUOUS rank that fixes the quadrant's step-function
# =========================================================================
# The quadrant() above is a step function on two axes only (GROWTH, 8PT). Two
# names a hair apart on a threshold get opposite labels (VRT 5.8 -> AVOID vs
# COHR 6.0 -> MOMENTUM) even when VRT is BETTER on F/V/C/8PT — the quadrant
# never reads the layer scores at all. CONVICTION collapses all five signals
# into one smooth 0..10 number so the ranking matches the actual numbers.
#
# Design (mirrors the book's own "binding-constraint" philosophy):
#   REWARD = upside   = 0.50*F + 0.50*GROWTH            (quality + compounding)
#   SAFETY = entry    = 0.35*V + 0.25*p8_10 + 0.20*C    (price-weighted) plus
#                       0.20*bind                        (extra weight on the
#                                                         WEAKEST layer -> it is
#                                                         penalised twice)
#   CONVICTION = sqrt(REWARD * SAFETY)   -- GEOMETRIC, not additive, so a great
#       business at a terrible entry (or vice-versa) CANNOT be papered over by
#       its strong axis. This is the multiplicative version of "the lowest
#       layer is the real risk", applied across reward vs safety.
#
# Two haircuts keep it honest, reusing flags the engine already computes:
#   * [PEAK?] -> x0.85  : a low PEG on peak earnings is fake-cheap; trim its rank
#   * data% < 75% (GAP) -> x coverage : a score on thin data is trusted less
# Both are multiplicative and deterministic, so two runs stay byte-identical.
_CONV_PEAK_HAIRCUT = 0.85        # [PEAK?] names: knock the fake-cheap rank down


def conviction(growth10, eight, layers, binding_val, peak, coverage):
    """Continuous 0..10 conviction rank. Higher = stronger risk-adjusted buy.

    Replaces the quadrant's cliff with a smooth score that DOES read the F/V/C
    layers. binding_val is the numeric value of the lowest layer (min F,V,C);
    coverage is the 0..1 data-completeness already on the record.
    """
    F = layers["FUND"]
    V = layers["VAL"]
    C = layers["CYCLE"]
    p8_10 = eight / 8.0 * 10.0            # rescale 8PT (0..8) onto 0..10

    reward = 0.50 * F + 0.50 * growth10
    safety = 0.35 * V + 0.25 * p8_10 + 0.20 * C + 0.20 * binding_val
    raw = (reward * safety) ** 0.5       # geometric mean, both must be decent

    if peak:
        raw *= _CONV_PEAK_HAIRCUT        # fake-cheap-on-peak -> rank lower
    if coverage < _GAP_THRESHOLD:
        raw *= coverage                  # thin data -> trust less
    return raw


_CONV_FOOTNOTE = (
    "  CONV 0-10 (higher = stronger risk-adjusted buy): a CONTINUOUS rank that\n"
    "        fixes the quadrant's step-function — it reads ALL five signals, not\n"
    "        just the two axes. REWARD = 0.50*F + 0.50*GROWTH (quality + how much\n"
    "        it can compound); SAFETY = 0.35*V + 0.25*8PT + 0.20*C + 0.20*bind\n"
    "        (entry quality, valuation-weighted, with the WEAKEST layer counted\n"
    "        twice). CONV = sqrt(REWARD * SAFETY) — GEOMETRIC, so a great business\n"
    "        at a terrible entry can't be papered over by its strong axis (the\n"
    "        multiplicative form of \"the lowest layer is the real risk\"). A\n"
    f"        [PEAK?] name is cut x{_CONV_PEAK_HAIRCUT} (fake-cheap on peak earnings) and a\n"
    "        sub-75%-data name is scaled by its coverage. Unlike the quadrant,\n"
    "        CONV ranks VRT above COHR when VRT is better on F/V/C/8PT."
)


def dca_conviction(quality10, layers, binding_val, richness, coverage):
    """Continuous 0..10 conviction rank for a DCA compounder.

    The cycle conviction() above is wrong for DCA names: it uses GROWTH (which a
    steady compounder does not have) and 8PT (which penalises size/extension —
    the exact bias that mis-grades compounders into AVOID). This variant keeps
    the SAME geometric REWARD x SAFETY skeleton but swaps the inputs for the
    ones that matter when you buy on a SCHEDULE:

        REWARD = durability   = 0.50*QUALITY + 0.50*F
        SAFETY = price entry  = 0.45*V + 0.35*(1-RICHNESS)*10 + 0.20*bind

    RICHNESS (the DCA price gate, 0=cheap..1=stretched) replaces 8PT: a stretched
    name is slowed, not skipped. Cycle position (C) enters only via 'bind' since
    market timing is irrelevant to scheduled buying. No [PEAK?] haircut — a
    peak-cycle flag is meaningless for a buy-forever name. Thin data still scales
    the score down so a number earned on guesses is trusted less.
    """
    F = layers["FUND"]
    V = layers["VAL"]
    cheapness = (1.0 - richness) * 10.0      # 0..1 richness -> 0..10 cheapness

    reward = 0.50 * quality10 + 0.50 * F
    safety = 0.45 * V + 0.35 * cheapness + 0.20 * binding_val
    raw = (reward * safety) ** 0.5           # same geometric mean as cycle CONV

    if coverage < _GAP_THRESHOLD:
        raw *= coverage                      # thin data -> trust less
    return raw


_DCA_CONV_FOOTNOTE = (
    "  CONV 0-10 (DCA variant, higher = stronger compounder to keep buying): the\n"
    "        same sqrt(REWARD * SAFETY) skeleton as the cycle CONV, but with the\n"
    "        inputs that matter for a SCHEDULED buy. REWARD = 0.50*QUALITY +\n"
    "        0.50*F (durability, not cyclical growth); SAFETY = 0.45*V +\n"
    "        0.35*(1-RICHNESS) + 0.20*bind (entry discipline — RICHNESS is the\n"
    "        DCA price gate, so a stretched name is SLOWED not skipped). 8PT and\n"
    "        the [PEAK?] haircut are dropped (they penalise the size/extension a\n"
    "        proven compounder is allowed to have); cycle position enters only via\n"
    "        bind. So a dead-cheap NOW can out-CONV a richer ANET even though ANET\n"
    "        is the better business — CONV ranks the BUY, QUALITY ranks the firm."
)


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
    q_growth = _trend_adjust(q_growth, fwd, f)  # decel bites; see GROWTH-BAND CONVENTION
    eps_g = f.get("fwd_eps_growth")
    q_eps = _band(None if eps_g is None else eps_g * eps_f, 6, 30)
    # margin TRAJECTORY: a DCA compounder with expanding margins is the ideal;
    # compression is an early crack. None when no history -> dropped by _blend.
    q_mtrend = _margin_trend(f)
    # gross-margin LEVEL (model quality, independent of net) and revenue-growth
    # CONSISTENCY (reliability) — both None when absent -> dropped by _blend.
    q_gross = _gross_quality(f)
    q_rcons = _rev_consistency(f)
    quality10, cov = _blend([(q_margin, 3.5), (q_growth, 2.5),
                             (q_eps, 2.0), (q_fcf, 2.0),
                             (q_mtrend, 1.5), (q_gross, 1.5),
                             (q_rcons, 1.0)], scale=10.0)

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
# 5c. STOCK ID CARD — deterministic archetype + watchlist action
# =========================================================================
# DataBourse-style scanners are useful when they do NOT replace the score but
# label the setup the score is looking at: compounder, cyclical rebound, late
# momentum, binary punt, etc. This turns the existing F/V/C layers, strategy tag,
# cycle tag and flags into a compact "ID card" and a mechanical watchlist action.
# The action is deliberately conservative: it is a triage instruction for names
# not yet owned, not a price target or an order generator.
def stock_archetype(r, f):
    """Classify the stock setup from already-computed deterministic signals."""
    t = r["ticker"]
    strat = r.get("strategy")
    F = r["layers"]["FUND"]
    V = r["layers"]["VAL"]
    C = r["layers"]["CYCLE"]
    growth = r["growth10"]
    pos = cycle_of(t, r)

    if not r.get("has_data"):
        return "Binary/no-data monitor" if pos == "Binary" else "No-fundamentals monitor"
    if r["coverage"] < _GAP_THRESHOLD:
        return "Thin-data punt"
    if r["peak"]:
        return "Peak-cycle trap"
    if r["marg"]:
        return "Cycle/margin conflict"

    if strat == "dca":
        q10, rich, _ = dca_quality(t, f)
        if rich >= 0.6:
            return "Rich compounder"
        if q10 >= 7.0:
            return "Quality compounder"
        if F < 4.5:
            return "Impaired compounder"
        return "DCA candidate"

    if strat == "cycle":
        if C <= 4.0 and V <= 5.0:
            return "Late momentum"
        if pos in ("Early", "Early/Mid") and F >= 6.0 and V >= 6.0:
            return "Early-cycle setup"
        if V >= 7.0 and growth >= 6.0:
            return "Cyclical rebound"
        if growth >= 7.0 and BOTTLENECK.get(t, 0.0) >= 0.5:
            return "Bottleneck grower"
        return "Cycle watch"

    if strat in ("catalyst", "lottery"):
        if pos == "Binary":
            return "Binary catalyst"
        if growth >= 7.0 and V >= 5.0:
            return "Catalyst setup"
        return "Speculative watch"

    return "Unclassified"


def watchlist_action(r):
    """Mechanical action for watch-only candidates.

    ADD means the setup clears score + entry gates. STARTER means the stock is
    eligible for a small position / deeper human thesis work. WAIT means the
    thesis can be right but the entry or cycle flag is wrong today. RESEARCH
    means data coverage is too thin to trust the rank. PASS means the current
    score does not justify watchlist attention.
    """
    if r.get("held") and r.get("book_pct", 0.0) > 0:
        return "HOLD"
    if not r.get("has_data") or r["coverage"] < _GAP_THRESHOLD:
        return "RESEARCH"
    if r["peak"] or r["marg"]:
        return "WAIT"

    grade = r["grade"]
    conv = r["conviction_unified"]
    F = r["layers"]["FUND"]
    V = r["layers"]["VAL"]
    C = r["layers"]["CYCLE"]

    if r.get("strategy") == "dca":
        if grade == "KEEP-DCA" and conv >= 8.0 and F >= 7.0 and V >= 7.0:
            return "ADD"
        if grade == "KEEP-DCA" and conv >= 7.2 and F >= 6.0 and V >= 6.0:
            return "STARTER"
        if grade == "RICH":
            return "WAIT"
        return "PASS"

    if grade == "PRIME" and conv >= 7.6 and F >= 6.0 and V >= 7.0 and C >= 5.0:
        return "ADD"
    if grade in ("PRIME", "MOMENTUM", "QUALITY") and conv >= 7.0:
        return "STARTER"
    if V < 4.0 or C < 4.0:
        return "WAIT"
    return "PASS"


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
# 6b. TTM REVENUE-GROWTH SOURCING — fills only the ttm_rev_growth column.
# =========================================================================
# Unlike the statistics page, the /financials/ page embeds a JSON blob with a
# `revenueGrowth:[...]` array (index 0 = TTM YoY, index 1 = latest full FY, ...).
# That TTM figure is the trailing rate the deceleration penalty compares the
# forward forecast against. This helper scrapes it for the requested tickers and
# writes it back into an EXISTING CSV in place, touching ONLY the
# ttm_rev_growth cell and preserving every other hand-curated value and the
# leading `#` comment header. Run via --fill-ttm; it is deliberately separate
# from --live (which overwrites the whole row from the thinner statistics page).
_FIN_EXCH = {  # foreign listings use /quote/<exch>/<code>/financials/
    "KS": ("krx", lambda code: code),       # Korea: 000660.KS -> krx/000660
    "HK": ("hkg", lambda code: code),       # Hong Kong: 1810.HK -> hkg/1810
    "DE": ("etr", lambda code: code),       # Xetra
    "AS": ("ams", lambda code: code),       # Amsterdam
    "SW": ("swx", lambda code: code),       # SIX Swiss
    "L":  ("lon", lambda code: code),       # London: SHEL.L -> lon/SHEL
    "T":  ("tyo", lambda code: code),       # Tokyo:  7203.T -> tyo/7203
    "PA": ("epa", lambda code: code),       # Paris:  MC.PA  -> epa/MC
    "TO": ("tsx", lambda code: code),       # Toronto: RY.TO -> tsx/RY
    "NS": ("nse", lambda code: code),       # India NSE: RELIANCE.NS -> nse/RELIANCE
    "AX": ("asx", lambda code: code),       # Australia ASX: BHP.AX -> asx/BHP
    "TW": ("tpe", lambda code: code),       # Taiwan TWSE: 2330.TW -> tpe/2330
    "MC": ("bme", lambda code: code),       # Spain BME (Madrid): ITX.MC -> bme/ITX
    "ST": ("sto", lambda code: code),       # Sweden Stockholm: SAND.ST -> sto/SAND
    "JO": ("jse", lambda code: code),       # South Africa JSE: NPN.JO -> jse/NPN
    "SR": ("tadawul", lambda code: code),   # Saudi Tadawul: 2222.SR -> tadawul/2222
}


def _fin_url(ticker):
    """Map a CSV ticker to its stockanalysis.com /financials/ URL."""
    if "." in ticker:
        code, suf = ticker.rsplit(".", 1)
        exch = _FIN_EXCH.get(suf.upper())
        if exch:
            return f"https://stockanalysis.com/quote/{exch[0]}/{exch[1](code)}/financials/"
    return f"https://stockanalysis.com/stocks/{ticker.lower()}/financials/"


_CSV_DATE_RE = __import__("re").compile(r"fundamentals_(\d{4}-\d{2}-\d{2})\.csv$")


def _restamp_header_date(comments, csv_path):
    """Return `comments` with the 'prices/close <Mon DD YYYY>' date rewritten to
    match the snapshot's own filename date. The refresh workflow copies the
    newest CSV to a new dated file and updates the numbers, but the leading
    comment line kept a stale close date; this keeps the snapshot self-
    describing. No-op if the filename carries no date or the line is absent.
    """
    import re
    m = _CSV_DATE_RE.search(str(csv_path))
    if not m:
        return comments
    try:
        d = _dt.date.fromisoformat(m.group(1))
    except ValueError:
        return comments
    stamp = d.strftime("%b %-d %Y")   # e.g. "Aug 3 2026"
    out = []
    for ln in comments:
        out.append(re.sub(r"(prices/close )([A-Z][a-z]{2} \d{1,2} \d{4})",
                          lambda mm: mm.group(1) + stamp, ln))
    return out


def ttm_growth_for(ticker):
    """Return (ttm, hist) for a ticker, or (None, []) on any failure.
    Parses financialData.revenueGrowth: index 0 is TTM YoY (the `ttm` scalar);
    indices 1.. are the trailing full-FY YoY series, most-recent first (`hist`),
    which feeds the multi-year median baseline in _trend_adjust."""
    import re
    import urllib.request
    url = _fin_url(ticker)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception:
        return None, []
    ttm, hist = _parse_series(html, "revenueGrowth")
    # FALLBACK (2026-08 site drift): stockanalysis.com's /financials/ page no
    # longer embeds the pre-computed `revenueGrowth:[..]` array (only the raw
    # `revenue:[..]` figures remain). When it is absent, derive the YoY series
    # ourselves from the raw annual revenue array so newly-synced rows still get
    # a trend baseline. Existing CSV rows are untouched (fill_ttm only rewrites
    # the targeted names), so this changes no previously-stored value.
    if ttm is None and not hist:
        ttm, hist = _revenue_yoy(html)
    return ttm, hist


def _revenue_yoy(html):
    """Derive (ttm_proxy, [FY YoY %]) from the raw annual `revenue:[..]` array on
    a /financials/ page. The first `revenue:[..]` match is the income-statement
    annual series, most-recent first. YoY_i = (r_i - r_{i+1}) / r_{i+1} * 100.
    Returns (None, []) if the array is missing or too short. The most-recent FY
    YoY doubles as the `ttm` single-year fallback baseline (see CSV schema note).
    """
    import re
    m = re.search(r"(?<![\w])revenue:\[([-.0-9,]+)\]", html)
    if not m:
        return None, []
    vals = []
    for part in m.group(1).split(","):
        v = _num(part.strip())
        if v is not None:
            vals.append(v)
    if len(vals) < 2:
        return None, []
    yoy = []
    for i in range(len(vals) - 1):
        prev = vals[i + 1]
        if prev:
            yoy.append(round((vals[i] - prev) / abs(prev) * 100, 2))
    if not yoy:
        return None, []
    return yoy[0], yoy


def _parse_series(html, key):
    """Pull a financialData array (key:[..]) from a /financials/ page and return
    (ttm_scalar, [trailing-FY series]) as percentages. index 0 = TTM, indices
    1.. = full FYs newest-first. Shared by revenueGrowth and profitMargin."""
    import re
    m = re.search(re.escape(key) + r":\[([^\]]+)\]", html)
    if not m:
        return None, []
    vals = []
    for part in m.group(1).split(","):
        v = _num(part.strip())
        vals.append(round(v * 100, 2) if v is not None else None)
    ttm = vals[0] if vals else None
    # FY series = everything after the TTM cell; drop blanks (e.g. the first
    # reporting year has no prior-year figure).
    hist = [v for v in vals[1:] if v is not None]
    return ttm, hist


def margin_hist_for(ticker):
    """Return (ttm_net_margin, [trailing net-margin series]) for a ticker, or
    (None, []) on any failure. Parses financialData.profitMargin (GAAP net
    margin) from the /financials/ page — same array shape as revenueGrowth.
    Feeds the margin-expansion sub-score (_margin_trend)."""
    import urllib.request
    url = _fin_url(ticker)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception:
        return None, []
    return _parse_series(html, "profitMargin")


def fill_ttm(csv_path, tickers):
    """Update the ttm_rev_growth scalar, the rev_growth_hist series (trailing-FY
    YoY) AND the net_margin_hist series (trailing net margin) for `tickers` in
    csv_path, in place. Preserves the `#` comment header and every other cell,
    and appends the rev_growth_hist / net_margin_hist columns to the header if
    the CSV predates them. Skips names that fail to fetch (existing values kept)."""
    with open(csv_path, newline="") as fh:
        raw = fh.readlines()
    comments = [ln for ln in raw if ln.lstrip().startswith("#")]
    data_lines = [ln for ln in raw if not ln.lstrip().startswith("#")]
    reader = csv.DictReader(data_lines)
    header = list(reader.fieldnames)
    if "rev_growth_hist" not in header:
        header.append("rev_growth_hist")     # extend older CSVs in place
    if "net_margin_hist" not in header:
        header.append("net_margin_hist")     # extend older CSVs in place
    rows = list(reader)
    want = set(tickers)
    n = 0
    for row in rows:
        t = (row.get("ticker") or "").strip()
        if t not in want:
            continue
        ttm, hist = ttm_growth_for(t)
        _, mhist = margin_hist_for(t)        # net-margin trajectory series
        if ttm is None and not hist and not mhist:
            print(f"  [ttm] {t}: no figure (kept existing '{row.get('ttm_rev_growth','')}')")
            continue
        if ttm is not None:
            row["ttm_rev_growth"] = f"{ttm}"
        row["rev_growth_hist"] = "|".join(f"{v}" for v in hist)
        if mhist:
            row["net_margin_hist"] = "|".join(f"{v}" for v in mhist)
        n += 1
        med = "n/a"
        if hist:
            import statistics
            med = f"{statistics.median(hist):.1f}"
        mt = _margin_trend({"net_margin_hist": mhist})
        mt_s = "n/a" if mt is None else f"{mt:.2f}"
        print(f"  [ttm] {t}: ttm={ttm}%  hist=[{row['rev_growth_hist']}]  "
              f"median={med}  margins=[{row.get('net_margin_hist','')}]  mtrend={mt_s}")
    # Force LF line endings. csv.writer defaults to a CRLF lineterminator; if
    # left at the default it emits "\r\n" which (with newline="") reaches disk
    # literally, flipping every line in the diff. Setting lineterminator="\n"
    # AND opening with newline="" (so Python does no extra translation) keeps
    # the file pure-LF, matching the hand-edited snapshot.
    comments = _restamp_header_date(comments, csv_path)
    with open(csv_path, "w", newline="") as fh:
        fh.writelines(comments)
        w = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"  [ttm] updated {n} rows in {csv_path}")
    return csv_path


# =========================================================================
# 6c. CSV SYNC — add rows for AI-allocation names missing from the snapshot.
# =========================================================================
# Problem this solves: when names are added to portfolio/AI_allocations.py
# (held baskets or WATCHLIST) they have no fundamentals row, so they score on
# tags/forecast only (data = -). This scrapes the mechanically-available fields
# from stockanalysis.com for those missing names and APPENDS them, so the next
# score run has real data. It is deliberately conservative:
#   * default: add ONLY missing tickers; never touch an existing row.
#   * --overwrite: also re-scrape existing rows, but PRESERVE the hand-curated
#     judgement cells (net_margin operating-margin proxies, seeded eps_beat_*),
#     overwriting only the purely-mechanical fields.
#   * fwd_rev_growth / fwd_eps_growth (analyst 3Y forecasts) CANNOT be scraped
#     reliably (they render in SVG/obfuscated JSON), so they are left BLANK and
#     every name still needing them by hand is reported at the end.
#   * ttm_rev_growth / rev_growth_hist / net_margin_hist are intentionally left
#     for --fill-ttm (the dedicated financials-page scraper), not duplicated
#     here — run --fill-ttm after --sync-csv to populate them.
# FX: foreign market caps are reported in local currency; converted to USD
# billions with the same approximate rates documented in the CSV header.
_FX_PER_USD = {  # local currency units per 1 USD (divide local cap by this)
    "KRW": 1350.0,  # Korea (.KS)
    "HKD": 7.8,     # Hong Kong (.HK)
    "EUR": None,    # EUR is quoted USD-per-EUR; handled specially below
    "CHF": 0.90,    # approx CHF per USD (.SW)
    "GBP": 0.79,    # UK (.L) — note: mktcap reported in GBP, not pence
    "JPY": 157.0,   # Japan (.T)
    "CAD": 1.37,    # Canada (.TO)
    "INR": 83.5,    # India (.NS)
    "AUD": 1.52,    # Australia (.AX)
    "TWD": 32.5,    # Taiwan (.TW)
    "SEK": 10.6,    # Sweden (.ST)
    "ZAR": 18.2,    # South Africa (.JO)
    "SAR": 3.75,    # Saudi Arabia (.SR) — riyal is USD-pegged at 3.75
}
_EUR_USD = 1.08     # USD per 1 EUR (.AS / .DE / .MC listings priced in EUR)

# Map the CSV ticker suffix to the local currency of its market-cap figure.
_SUFFIX_CCY = {
    "KS": "KRW", "HK": "HKD", "AS": "EUR", "DE": "EUR", "SW": "CHF",
    "L": "GBP", "T": "JPY", "PA": "EUR", "TO": "CAD", "NS": "INR", "AX": "AUD",
    "TW": "TWD", "MC": "EUR", "ST": "SEK", "JO": "ZAR", "SR": "SAR",
}

# DMA200-GUARD: max plausible |price − 200DMA| / 200DMA, in %. A real chart is
# at most a few hundred % above its 200-day average; a six-figure reading means
# the feed served price and 200DMA in mismatched scales/units (seen on some KRX
# names, e.g. 000660.KS). scrape_stats() rejects anything past this and leaves
# the cell blank so the scorer drops the sub-point instead of clamping junk.
_DMA200_SANE = 1000.0


def _stats_url(ticker):
    """stockanalysis.com /statistics/ URL for a CSV ticker (US or foreign)."""
    if "." in ticker:
        code, suf = ticker.rsplit(".", 1)
        exch = _FIN_EXCH.get(suf.upper())
        if exch:
            return f"https://stockanalysis.com/quote/{exch[0]}/{exch[1](code)}/statistics/"
    return f"https://stockanalysis.com/stocks/{ticker.lower()}/statistics/"


def _quote_price(ticker):
    """Current price for a ticker, or None. US names use the clean quotes API;
    foreign listings decode the price out of the SvelteKit __data.json blob."""
    import json
    import urllib.request

    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", "ignore")

    try:
        if "." not in ticker:
            d = json.loads(get(
                f"https://stockanalysis.com/api/quotes/s/{ticker.upper()}"))
            return d.get("data", {}).get("p")
        # foreign: /quote/<exch>/<code>/__data.json holds a flattened array; the
        # quote sub-object maps key 'p' to an INDEX into the same data list.
        code, suf = ticker.rsplit(".", 1)
        exch = _FIN_EXCH.get(suf.upper())
        if not exch:
            return None
        d = json.loads(get(
            f"https://stockanalysis.com/quote/{exch[0]}/{exch[1](code)}/__data.json"))
        for node in d.get("nodes", []):
            data = node.get("data")
            if not isinstance(data, list):
                continue
            for el in data:
                if isinstance(el, dict) and "p" in el and "h52" in el:
                    idx = el["p"]
                    if isinstance(idx, int) and idx < len(data):
                        return data[idx]
        return None
    except Exception:
        return None


def _stat_cell(html, label):
    """Pull a single statistics-table value by row label. Uses the LAST match of
    '>label<' so the stat row wins over the same words in the page nav, then
    grabs the next title="..." (the unrounded value)."""
    import re
    idx = html.rfind(">" + label + "<")
    if idx < 0:
        idx = html.rfind(label)
    if idx < 0:
        return None
    m = re.search(r'title="([^"]+)"', html[idx:idx + 280])
    return m.group(1) if m else None


def _clean_num(s):
    """'4,041,226,003,400' / '27.152%' / '2.632' -> float, or None."""
    if s is None:
        return None
    s = s.replace(",", "").replace("%", "").strip()
    return _num(s)


def _forecast_url(ticker):
    """stockanalysis.com /forecast/ URL for a CSV ticker (US or foreign)."""
    if "." in ticker:
        code, suf = ticker.rsplit(".", 1)
        exch = _FIN_EXCH.get(suf.upper())
        if exch:
            return f"https://stockanalysis.com/quote/{exch[0]}/{exch[1](code)}/forecast/"
    return f"https://stockanalysis.com/stocks/{ticker.lower()}/forecast/"


def scrape_forecast(ticker):
    """Scrape forward analyst growth from the /forecast/ page.

    Returns (fwd_rev_growth, fwd_eps_growth) as strings (blank if unavailable).

    NOTE on what is actually free: stockanalysis.com paywalls the multi-year
    (2027/2028+) estimates as "[PRO]", so the 3-YEAR forward CAGR the CSV schema
    nominally wants is NOT scrapable. What IS free is the NEXT-FY analyst
    consensus average, embedded in the page JSON as
        revenueGrowth:{"<FY-end>":{avg:<pct>,low:..,high:..}, "<next>":"[PRO]"..}
        epsGrowth:{"<FY-end>":{avg:<pct>,...}, ...}
    We take that nearest-FY `avg` as the forward proxy — a reasonable, fully
    reproducible stand-in for the gated 3Y figure, and far better than blank.
    Hand-edit the cell afterwards if you have a true 3Y number."""
    import re
    import urllib.request

    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", "ignore")

    try:
        html = get(_forecast_url(ticker))
    except Exception as e:
        print(f"  [sync] {ticker}: forecast fetch failed ({e})")
        return "", ""

    def first_avg(key):
        # Match  key:{"YYYY-MM-DD":{avg:<number>  — the nearest free FY estimate.
        m = re.search(
            re.escape(key) + r':\{"[^"]+":\{avg:(-?\d+(?:\.\d+)?)', html)
        return f"{float(m.group(1)):.2f}" if m else ""

    return first_avg("revenueGrowth"), first_avg("epsGrowth")


def scrape_stats(ticker):
    """Scrape the mechanically-available fundamentals for one ticker from the
    statistics page (+ quotes price + financials FCF sign + forecast growth).
    Returns a dict of CSV cells (strings; blank where unavailable). fwd_* are
    sourced from the /forecast/ page's nearest-FY analyst consensus (see
    scrape_forecast for the [PRO]-paywall caveat)."""
    import re
    import urllib.request

    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", "ignore")

    try:
        html = get(_stats_url(ticker))
    except Exception as e:
        print(f"  [sync] {ticker}: statistics fetch failed ({e})")
        return None

    # market cap -> USD billions (FX-convert foreign caps)
    cap_raw = _clean_num(_stat_cell(html, "Market Cap"))
    mktcap_b = ""
    if cap_raw is not None:
        usd = cap_raw
        if "." in ticker:
            ccy = _SUFFIX_CCY.get(ticker.rsplit(".", 1)[1].upper())
            if ccy == "EUR":
                usd = cap_raw * _EUR_USD
            elif ccy and _FX_PER_USD.get(ccy):
                usd = cap_raw / _FX_PER_USD[ccy]
        mktcap_b = f"{usd / 1e9:.2f}"

    gross = _clean_num(_stat_cell(html, "Gross Margin"))
    net = _clean_num(_stat_cell(html, "Profit Margin"))
    peg = _clean_num(_stat_cell(html, "PEG Ratio"))
    ps = _clean_num(_stat_cell(html, "PS Ratio"))
    dma200 = _clean_num(_stat_cell(html, "200-Day Moving Average"))

    # pct above/below the 200DMA needs the current price
    pct_200 = ""
    price = _quote_price(ticker)
    if price is not None and dma200:
        pct = (price - dma200) / dma200 * 100
        # Sanity guard: some foreign feeds (e.g. KRX 000660.KS) serve the price
        # and the 200DMA in mismatched scales/units, yielding an absurd distance
        # (six-figure %). A real chart is at most a few hundred % above its
        # 200DMA, so reject anything past _DMA200_SANE and leave the cell blank —
        # _band() then drops the sub-point and redistributes its weight rather
        # than clamping a junk value to the floor. See the DMA200-GUARD note.
        if abs(pct) <= _DMA200_SANE:
            pct_200 = f"{pct:.1f}"
        else:
            print(f"  [sync] {ticker}: 200DMA distance {pct:.0f}% implausible "
                  f"(price/200DMA scale mismatch?) — leaving blank")

    # FCF sign from the financials page fcf[] array (index 0 = TTM/latest)
    fcf_pos = ""
    try:
        fin = get(_fin_url(ticker))
        m = re.search(r"(?<![\w])fcf:\[([^\]]+)\]", fin)
        if m:
            first = _num(m.group(1).split(",")[0])
            if first is not None:
                fcf_pos = "1" if first > 0 else "0"
    except Exception:
        pass

    # forward analyst growth (nearest-FY consensus avg; see scrape_forecast)
    fwd_rev, fwd_eps = scrape_forecast(ticker)

    return {
        "ticker": ticker,
        "mktcap_b": mktcap_b,
        "fwd_rev_growth": fwd_rev,     # nearest-FY analyst consensus (proxy)
        "ttm_rev_growth": "",          # leave for --fill-ttm
        "fwd_eps_growth": fwd_eps,     # nearest-FY analyst consensus (proxy)
        "gross_margin": "" if gross is None else f"{gross}",
        "net_margin": "" if net is None else f"{net}",
        "fcf_positive": fcf_pos,
        "peg": "" if peg is None else f"{peg}",
        "ps_ratio": "" if ps is None else f"{ps}",
        "pct_above_200dma": pct_200,
        "pct_below_52w_high": "",      # CSV convention: left blank (P8 uses 200DMA)
        "eps_beat_rate": "",           # hand-seeded only
        "eps_beat_streak": "",         # hand-seeded only
        "rev_growth_hist": "",         # leave for --fill-ttm
        "net_margin_hist": "",         # leave for --fill-ttm
    }


# Fields --overwrite is allowed to replace on an EXISTING row. Deliberately
# excludes net_margin (may hold an operating-margin proxy), eps_beat_rate /
# eps_beat_streak (hand-seeded), and the *_hist series (owned by --fill-ttm),
# so re-syncing never clobbers a curated judgement cell. fwd_* are refreshable:
# they are now auto-sourced (nearest-FY consensus), so a re-sync should keep
# them current — but a hand-entered true-3Y value will be overwritten, so omit
# them from --overwrite if you have curated those cells.
_SYNC_OVERWRITE_FIELDS = (
    "mktcap_b", "gross_margin", "fcf_positive", "peg", "ps_ratio",
    "pct_above_200dma", "fwd_rev_growth", "fwd_eps_growth",
)


def sync_csv(csv_path, wanted, overwrite=False):
    """Append fundamentals rows for `wanted` tickers missing from csv_path (and,
    with overwrite=True, refresh the mechanical fields on existing rows while
    preserving curated cells). Preserves the leading '#' header and LF endings.
    Returns the list of tickers still missing fwd_rev_growth/fwd_eps_growth so
    the caller can report what still needs hand entry."""
    with open(csv_path, newline="") as fh:
        raw = fh.readlines()
    comments = [ln for ln in raw if ln.lstrip().startswith("#")]
    data_lines = [ln for ln in raw if not ln.lstrip().startswith("#")]
    reader = csv.DictReader(data_lines)
    header = list(reader.fieldnames)
    for col in ("ps_ratio", "rev_growth_hist", "net_margin_hist"):
        if col not in header:
            header.append(col)            # extend older CSVs in place
    rows = list(reader)
    have = {(r.get("ticker") or "").strip() for r in rows}

    missing = [t for t in wanted if t not in have]
    existing = [t for t in wanted if t in have] if overwrite else []

    added, refreshed, fwd_todo = [], [], []
    for t in missing:
        rec = scrape_stats(t)
        if rec is None:
            continue
        rows.append({k: rec.get(k, "") for k in header})
        added.append(t)
        # fwd_* are now auto-sourced; only flag a row for hand entry if the
        # forecast scrape came back empty (e.g. no analyst coverage / [PRO]).
        if not (rec.get("fwd_rev_growth") and rec.get("fwd_eps_growth")):
            fwd_todo.append(t)
        print(f"  [sync] +{t}: mktcap={rec['mktcap_b']} gm={rec['gross_margin']} "
              f"nm={rec['net_margin']} peg={rec['peg']} ps={rec['ps_ratio']} "
              f"200dma%={rec['pct_above_200dma']} fcf={rec['fcf_positive']} "
              f"fwdRev={rec['fwd_rev_growth'] or '-'} "
              f"fwdEps={rec['fwd_eps_growth'] or '-'}")

    if overwrite:
        by_ticker = {(r.get("ticker") or "").strip(): r for r in rows}
        for t in existing:
            rec = scrape_stats(t)
            if rec is None:
                continue
            row = by_ticker[t]
            for f in _SYNC_OVERWRITE_FIELDS:
                if rec.get(f, "") != "":
                    row[f] = rec[f]
            refreshed.append(t)
            print(f"  [sync] ~{t}: refreshed mechanical fields "
                  f"(curated net_margin/eps_beat preserved)")

    # Force LF (same rationale as fill_ttm — avoid CRLF flipping the whole diff).
    comments = _restamp_header_date(comments, csv_path)
    with open(csv_path, "w", newline="") as fh:
        fh.writelines(comments)
        w = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"  [sync] added {len(added)}, refreshed {len(refreshed)} "
          f"-> {csv_path}")
    return fwd_todo, added


# =========================================================================
# 7. RUN
# =========================================================================
def default_csv():
    """Pick the most recent scoring/fundamentals_*.csv."""
    cands = sorted(Path(ROOT, "scoring").glob("fundamentals_*.csv"))
    return str(cands[-1]) if cands else None


def _clip(s, n):
    """Fixed-width CLI cell with a visible ellipsis when text is too long."""
    s = str(s)
    if len(s) <= n:
        return s
    return s[:max(0, n - 1)] + "…"


def render_watchlist_actions(results):
    """Print watch-only / re-add candidates with their deterministic action."""
    watch = [
        r for r in results
        if not (r.get("held") and r.get("book_pct", 0.0) > 0)
    ]
    if not watch:
        return

    priority = {"ADD": 0, "STARTER": 1, "WAIT": 2, "RESEARCH": 3, "PASS": 4}
    watch.sort(key=lambda r: (priority.get(r["watch_action"], 9),
                              -r["conviction_unified"]))
    print("\n-- WATCHLIST ACTIONS (scanner triage) "
          "--------------------------------")
    print(f"   {'ticker':10s} {'strategy':8s} {'action':8s} {'CONV':>5s} "
          f"{'grade':9s} {'archetype':24s} {'F':>4s} {'V':>4s} "
          f"{'C':>4s} {'bind':5s} {'data%':>5s}")
    for r in watch:
        flags = (" [PEAK?]" if r["peak"] else "") + (" [MARG?]" if r["marg"] else "")
        print(f"   {r['ticker']:10s} {r['strategy']:8s} "
              f"{r['watch_action']:8s} {r['conviction_unified']:5.2f} "
              f"{r['grade']:9s} {_clip(r['archetype'], 24):24s} "
              f"{_layer_cell(r['layers'])} {_LAYER_ABBR[r['binding']]:5s} "
              f"{_cov_cell(r['coverage'])}{flags}")


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
        dconv = dca_conviction(q10, r["layers"], r["layers"][r["binding"]],
                               rich, r["coverage"])
        dca_scored.append((r, q10, rich, dca_grade(q10, rich, f), dconv))
    dca_scored.sort(key=lambda x: -x[4])           # rank by DCA CONVICTION
    print("\n-- DCA (steady compounders; buy on schedule) "
          "--------------------------")
    print(f"   {'ticker':10s} {'wv':3s} {'book%':>5s} {'CONV':>5s} "
          f"{'QUALITY':>7s} {'RICHNESS':>8s} {'grade':9s} {'F':>4s} {'V':>4s} "
          f"{'C':>4s} {'bind':5s} {'data%':>5s}")
    for r, q10, rich, grade, dconv in dca_scored:
        flags = (" [PEAK?]" if r["peak"] else "") + (" [MARG?]" if r["marg"] else "")
        print(f"   {r['ticker']:10s} {r['wave']:3s} {r['book_pct']:5.2f} "
              f"{dconv:5.2f} "
              f"{q10:7.1f} {rich:8.2f} {grade:9s} {_layer_cell(r['layers'])} "
              f"{_LAYER_ABBR[r['binding']]:5s} "
              f"{_cov_cell(r['coverage'])}{flags}")
    for grade, desc in [("KEEP-DCA", "durable + reasonably priced -> keep buying"),
                        ("RICH", "quality intact but price extended -> slow buys"),
                        ("IMPAIRED", "business cracking -> pause / reduce")]:
        names = [r["ticker"] for r, _, _, g, _ in dca_scored if g == grade]
        print(f"     {grade:9s} ({len(names):2d}) {desc}")
        if names:
            print(f"               {', '.join(names)}")
    print()
    print(_DCA_FOOTNOTE)
    print(_DCA_CONV_FOOTNOTE)

    # ---- CYCLE & CATALYST: the two-axis grid, now RANKED by CONVICTION ----
    # The quadrant label is kept (it still answers "which corner?") but the rows
    # are ordered by the continuous CONV score so neighbours that the quadrant
    # splits apart on a threshold sit next to each other by true strength.
    for mode, title in [("cycle", "CYCLE (buy the dip / sell the rip)"),
                        ("catalyst", "CATALYST (event-driven punts)")]:
        grp = [r for r in results if r["strategy"] == mode]
        grp.sort(key=lambda r: -r["conviction"])      # rank by CONVICTION
        print(f"\n-- {title} "
              + "-" * max(2, 46 - len(title)))
        print(f"   {'ticker':10s} {'wv':3s} {'book%':>5s} {'CONV':>5s} "
              f"{'GROWTH':>6s} {'8PT':>4s} {'quadrant':10s} {'F':>4s} {'V':>4s} "
              f"{'C':>4s} {'bind':5s} {'data%':>5s}")
        for r in grp:
            flags = (" [PEAK?]" if r["peak"] else "") + (" [MARG?]" if r["marg"] else "")
            print(f"   {r['ticker']:10s} {r['wave']:3s} {r['book_pct']:5.2f} "
                  f"{r['conviction']:5.2f} "
                  f"{r['growth10']:6.1f} {r['eight']:4.2f} {r['quad']:10s} "
                  f"{_layer_cell(r['layers'])} "
                  f"{_LAYER_ABBR[r['binding']]:5s} "
                  f"{_cov_cell(r['coverage'])}{flags}")

    render_watchlist_actions(results)

    print()
    print(_GROWTH_8PT_FOOTNOTE)
    print(_CONV_FOOTNOTE)
    print(_GAP_FOOTNOTE)
    print(_LAYER_FOOTNOTE)


def build_results(csv_path):
    """Score the full held+watchlist universe and return the list of per-name
    result dicts (the same structure main() builds), sorted by unified
    conviction descending. Factored out of main() so the JSON exporter and any
    other consumer score every name identically to the CLI table.
    """
    port = portfolio_rows(include_watchlist=True)
    fund = load_fundamentals(csv_path)
    # Guard: a held cycle-strategy name with no explicit CYCLE_POS tag silently
    # defaults to "Mid", making its CYCLE layer / 8-Point P5 uninformative — the
    # opposite of what a cycle trade needs. Warn so the gap can't reappear
    # unnoticed (dca/catalyst holdings are allowed to default; see the function).
    _untagged = untagged_cycle_holdings()
    if _untagged:
        print("WARNING: held cycle-strategy names missing an explicit CYCLE_POS "
              f"tag (defaulting to 'Mid'): {', '.join(_untagged)}",
              file=sys.stderr)
    results = []
    for t, info in port.items():
        if t == "SMHV.SW":
            continue  # fixed windfall, excluded per owner instruction
        f = fund.get(t, {})
        eight, parts8, eps_f = score_8point(t, f, info)
        g10, partsg = score_growth(t, f, info)
        layers, binding = layer_scores(t, f, info)
        cov = _coverage(f)
        peak = peak_trap(t, f, info)
        marg = margin_flag(t, f, info)
        conv = conviction(g10, eight, layers, layers[binding], peak, cov)
        q10, rich, _ = dca_quality(t, f)
        conv_dca = dca_conviction(q10, layers, layers[binding], rich, cov)
        conv_unified = conv_dca if info.get("strategy") == "dca" else conv
        grade, _prim, _rich = strategy_grade(
            {**info, "quad": quadrant(eight, g10), "growth10": g10}, f)
        rec = {**info, "eight": eight, "growth10": g10,
               "quad": quadrant(eight, g10), "eps_f": eps_f,
               "has_data": t in fund, "coverage": cov,
               "conviction": conv, "conviction_dca": conv_dca,
               "conviction_unified": conv_unified, "grade": grade,
               "layers": layers, "binding": binding, "peak": peak,
               "marg": marg}
        rec["archetype"] = stock_archetype(rec, f)
        rec["watch_action"] = watchlist_action(rec)
        results.append(rec)
    results.sort(key=lambda r: -r["conviction_unified"])
    return results


def export_json(csv_path, out_path):
    """Write conviction.json for the web dashboard. One record per scored name
    with the fields the card grid renders: ticker, wave, book%, strategy,
    held, CONV, grade, F/V/C layers, binding layer, coverage, peak flag.
    """
    results = build_results(csv_path)
    _LAYER_KEY = {"FUND": "F", "VAL": "V", "CYCLE": "C"}
    records = []
    for r in results:
        records.append({
            "ticker": r["ticker"],
            "wave": r["wave"],
            "held": bool(r["held"]) and r["book_pct"] > 0,
            "book_pct": round(r["book_pct"], 2),
            "strategy": r["strategy"],
            "conv": round(r["conviction_unified"], 2),
            "grade": r["grade"],
            "F": round(r["layers"]["FUND"], 1),
            "V": round(r["layers"]["VAL"], 1),
            "C": round(r["layers"]["CYCLE"], 1),
            "binding": _LAYER_KEY.get(r["binding"], r["binding"]),
            "coverage": round(r["coverage"] * 100),
            "peak": bool(r["peak"]),
            "marg": bool(r["marg"]),
            "archetype": r["archetype"],
            "watch_action": r["watch_action"],
            "has_data": bool(r["has_data"]),
        })
    payload = {
        "generated_utc": _dt.datetime.now(_dt.timezone.utc)
                            .strftime("%Y-%m-%d %H:%M UTC"),
        "csv": Path(csv_path).name,
        "count": len(records),
        "held_count": sum(1 for x in records if x["held"]),
        "records": records,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"wrote {out_path}  ({len(records)} names, "
          f"{payload['held_count']} held)  from {payload['csv']}")


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
    ap.add_argument("--sort", choices=["growth", "eight", "blend", "conviction"],
                    default="growth",
                    help="rank by Growth (default), 8-Point, the blend, or the "
                         "continuous CONVICTION score")
    ap.add_argument("--by-strategy", action="store_true",
                    help="group output by strategy mode and grade each on its OWN "
                         "rubric (DCA judged on quality+price, not small/explosive)")
    ap.add_argument("--json", nargs="?", const="docs/conviction.json",
                    metavar="PATH", default=None,
                    help="export the full held+watchlist scoring to JSON for the "
                         "web dashboard (default path: docs/conviction.json) and "
                         "exit")
    ap.add_argument("--fill-ttm", action="store_true",
                    help="scrape ttm_rev_growth from stockanalysis.com /financials/ "
                         "and write it into the CSV in place (powers the "
                         "deceleration penalty); preserves all other cells")
    ap.add_argument("--sync-csv", action="store_true",
                    help="scrape & APPEND fundamentals rows for AI-allocation names "
                         "(held + watchlist) missing from the CSV; never edits "
                         "existing rows. fwd_rev_growth/fwd_eps_growth are "
                         "auto-sourced (nearest-FY analyst consensus) and the "
                         "ttm/hist series are auto-filled for the new rows, so "
                         "no manual --fill-ttm step is needed. MU is skipped "
                         "(source-corrupted feed) with a warning.")
    ap.add_argument("--no-fill-ttm", action="store_true",
                    help="with --sync-csv, do NOT auto-fill the ttm/hist series "
                         "for new rows (leaves them blank for a later --fill-ttm)")
    ap.add_argument("--overwrite", action="store_true",
                    help="with --sync-csv, ALSO re-scrape existing rows, refreshing "
                         "only mechanical fields (mktcap, gross_margin, peg, "
                         "ps_ratio, fcf, 200dma%%) while PRESERVING curated cells "
                         "(net_margin proxies, seeded eps_beat_*)")
    args = ap.parse_args()

    if args.json is not None:
        if not args.csv or not Path(args.csv).exists():
            sys.exit("--json needs an existing fundamentals CSV.")
        export_json(args.csv, args.json)
        return

    port = portfolio_rows(include_watchlist=True if args.sync_csv else args.watchlist)

    if args.sync_csv:
        if not args.csv or not Path(args.csv).exists():
            sys.exit("--sync-csv needs an existing CSV (it appends to it).")
        # full AI-allocation universe (held baskets + watchlist), minus names
        # with no usable statistics page:
        #   SMHV.SW — the no-fundamentals windfall ETF (scored on tags only).
        #   SRUUF   — physical-commodity trust, no company fundamentals (404).
        #   MU      — stockanalysis.com's Micron snapshot is SOURCE-CORRUPTED
        #             (reports ~$1.28T mktcap / PEG 0.05); ingesting it poisons
        #             the CSV, so MU is scored on forecast/tags only (data = -).
        #             See AGENTS.md "Notes on interpreting results".
        _SYNC_SKIP = ("SMHV.SW", "SRUUF") + tuple(sorted(_SOURCE_CORRUPT))
        targets = [t for t in port if t not in _SYNC_SKIP]
        # Warn for any skipped name actually present in the universe, so a sync
        # run is explicit about what it deliberately did NOT scrape/add.
        _skipped = [t for t in _SYNC_SKIP if t in port]
        if "MU" in _skipped:
            print("  [sync] (!) SKIPPING MU — stockanalysis.com's Micron feed is "
                  "SOURCE-CORRUPTED (reports ~$1.28T mktcap / PEG 0.05). MU is "
                  "scored on forecast/tags only (data = -). See AGENTS.md.")
        for _t in _skipped:
            if _t != "MU":
                print(f"  [sync] (i) skipping {_t} (no usable statistics page).")
        fwd_todo, added = sync_csv(args.csv, targets, overwrite=args.overwrite)
        # Auto-fill the trailing series for the rows we just added, so a single
        # --sync-csv produces fully-populated rows (no manual --fill-ttm step).
        # Scoped to `added` only, so this stays fast (it does NOT rescan the
        # whole watchlist). Skip with --no-fill-ttm.
        if added and not args.no_fill_ttm:
            print(f"\n  [sync] auto-filling ttm/hist series for {len(added)} "
                  f"new row(s): {', '.join(added)}")
            fill_ttm(args.csv, added)
        if fwd_todo:
            print("\n(!) fwd_rev_growth / fwd_eps_growth had no free analyst "
                  f"estimate for {len(fwd_todo)} name(s) — enter by hand:")
            print("    " + ", ".join(fwd_todo))
            print("    Source: stockanalysis.com/stocks/<TICKER>/forecast/ "
                  "(the multi-year 3Y figure is [PRO]-gated; the nearest-FY "
                  "consensus is auto-sourced when present).")
        return

    if args.fill_ttm:
        if not args.csv or not Path(args.csv).exists():
            sys.exit("--fill-ttm needs an existing CSV (it updates in place).")
        # held book + watchlist if requested, minus the no-fundamentals windfall
        # and the source-corrupted names (MU) whose hand-curated series must not
        # be clobbered by the corrupted /financials/ page.
        targets = [t for t in port
                   if t != "SMHV.SW" and t not in _SOURCE_CORRUPT]
        if any(t in _SOURCE_CORRUPT for t in port):
            print("  [ttm] (!) SKIPPING " +
                  ", ".join(sorted(t for t in _SOURCE_CORRUPT if t in port)) +
                  " — source-corrupted feed; hand-curated series preserved.")
        fill_ttm(args.csv, targets)
        return

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
        cov = _coverage(f)
        peak = peak_trap(t, f, info)
        marg = margin_flag(t, f, info)
        conv = conviction(g10, eight, layers, layers[binding], peak, cov)
        # DCA names get the schedule-appropriate variant; the unified conviction
        # routes each name to the rubric that matches its job so a single column
        # / --sort is apples-to-apples across strategies.
        q10, rich, _ = dca_quality(t, f)
        conv_dca = dca_conviction(q10, layers, layers[binding], rich, cov)
        conv_unified = conv_dca if info.get("strategy") == "dca" else conv
        rec = {**info, "eight": eight, "growth10": g10, "blend": blend,
               "quad": quadrant(eight, g10), "eps_f": eps_f,
               "p8": parts8, "pg": partsg, "has_data": t in fund,
               "coverage": cov, "conviction": conv,
               "conviction_dca": conv_dca,
               "conviction_unified": conv_unified,
               "layers": layers, "binding": binding,
               "peak": peak, "marg": marg}
        grade, _prim, _rich = strategy_grade(rec, f)
        rec["grade"] = grade
        rec["archetype"] = stock_archetype(rec, f)
        rec["watch_action"] = watchlist_action(rec)
        results.append(rec)

    keyf = {"growth": lambda r: -r["growth10"],
            "eight": lambda r: -r["eight"],
            "blend": lambda r: -(r["blend"] or 0),
            "conviction": lambda r: -r["conviction_unified"]}[args.sort]
    results.sort(key=keyf)

    if args.by_strategy:
        render_by_strategy(results, fund, args)
        return

    # ----- two-score table (no forced blend) -----
    print(f"\n=== HOLDING RATING  (csv={Path(args.csv).name}, sort={args.sort}) ===")
    print("    Growth 0-10 (momentum-tolerant) | 8-Point 0-8 (anti-momentum) | "
          "Quadrant")
    hdr = f"{'rk':>2} {'ticker':10s} {'wv':3s} {'book%':>5s} {'CONV':>5s} " \
          f"{'GROWTH':>6s} {'8PT':>4s} {'quadrant':10s} {'epsF':>5s}"
    if args.blend:
        hdr += f" {'blend':>5s}"
    hdr += f" {'F':>4s} {'V':>4s} {'C':>4s} {'bind':5s} {'data%':>5s}"
    print(hdr)
    for i, r in enumerate(results, 1):
        # CONV is strategy-aware: DCA names show the schedule-appropriate variant
        # (marked 'd'); cycle/catalyst show the entry variant. This keeps the
        # column consistent with --sort conviction, which uses the same value.
        is_dca = r.get("strategy") == "dca"
        conv_mark = "d" if is_dca else " "
        line = f"{i:2d} {r['ticker']:10s} {r['wave']:3s} {r['book_pct']:5.2f} " \
               f"{r['conviction_unified']:5.2f}{conv_mark}" \
               f"{r['growth10']:6.1f} {r['eight']:4.2f} {r['quad']:10s} " \
               f"{r['eps_f']:5.2f}"
        if args.blend:
            line += f" {r['blend']:5.2f}"
        flags = (" [PEAK?]" if r["peak"] else "") + (" [MARG?]" if r["marg"] else "")
        line += f" {_layer_cell(r['layers'])} " \
                f"{_LAYER_ABBR[r['binding']]:5s} " \
                f"{_cov_cell(r['coverage'])}{flags}"
        print(line)
    print()
    print("  CONV column: a trailing 'd' marks a DCA name scored with the DCA "
          "conviction variant (QUALITY+RICHNESS); others use the cycle variant.")
    print(_GROWTH_8PT_FOOTNOTE)
    print(_CONV_FOOTNOTE)
    print(_DCA_CONV_FOOTNOTE)
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
    print("\n=== WAVE AVERAGES (book-weighted, held movable sleeve, "
          "ex-SMHV & ex-ETF-lookthrough) ===")
    agg = {}
    for r in results:
        if not r["held"] or r["book_pct"] == 0:
            continue
        if r["wave"] == "ET":
            continue  # ETF pass-through: same money as SMHV, would double-count
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
