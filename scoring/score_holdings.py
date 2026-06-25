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
# CSV columns (all numeric unless noted; blank = unknown -> neutral score):
#   ticker, mktcap_b, fwd_rev_growth, ttm_rev_growth, fwd_eps_growth,
#   gross_margin, net_margin, fcf_positive(0/1), peg, pct_above_200dma,
#   pct_below_52w_high, eps_beat_rate(0..1), eps_beat_streak(int)
# =========================================================================
FUND_FIELDS = [
    "ticker", "mktcap_b", "fwd_rev_growth", "ttm_rev_growth", "fwd_eps_growth",
    "gross_margin", "net_margin", "fcf_positive", "peg", "pct_above_200dma",
    "pct_below_52w_high", "eps_beat_rate", "eps_beat_streak",
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
    """Linear 0..1 ramp; clamps outside [lo,hi]."""
    if x is None:
        return 0.5  # unknown -> neutral
    if hi == lo:
        return 0.5
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def _band_inv(x, lo, hi):
    """Inverse ramp: smaller x scores higher."""
    if x is None:
        return 0.5
    return 1.0 - _band(x, lo, hi)


# --- 8-POINT (each sub-score 0..1; summed *8/8 -> 0..8) ------------------
def score_8point(t, f, info):
    eps_f = eps_surprise_factor(f.get("eps_beat_rate"), f.get("eps_beat_streak"))

    # P1 small enough to multiply: smaller mkt cap better (log-ish via bands).
    p1 = _band_inv(f.get("mktcap_b"), 5, 300)
    # P2 profitable or turning: GAAP net margin>0 full; FCF+ only = 0.5.
    nm = f.get("net_margin")
    if nm is None:
        p2 = 0.5
    elif nm > 0:
        p2 = min(1.0, 0.6 + _band(nm, 0, 30) * 0.4)
    else:
        p2 = 0.5 if (f.get("fcf_positive") == 1) else 0.15
    # P3 growth accelerating: fwd rev growth, bonus if fwd>ttm (re-accel),
    #     EPS-surprise corrects the forward figure.
    fwd = f.get("fwd_rev_growth")
    fwd_corr = None if fwd is None else fwd * eps_f
    p3 = _band(fwd_corr, 5, 45)
    if fwd is not None and f.get("ttm_rev_growth") is not None:
        if fwd > f["ttm_rev_growth"]:
            p3 = min(1.0, p3 + 0.15)        # genuine re-acceleration
    # P4 bottleneck (owner tag); unknown watchlist names -> neutral 0.3.
    p4 = BOTTLENECK.get(t, 0.3)
    # P5 secular & early (cycle position).
    p5 = _CYCLE_P5.get(cycle_of(t, info), 0.5)
    # P6 not priced for perfection: PEG, corrected down for beaters; cyclicals
    #    get a softer penalty (snapshot PEG misleads at cycle extremes).
    peg = f.get("peg")
    peg_corr = None if peg is None else peg / eps_f   # beaters -> lower PEG
    p6 = _band_inv(peg_corr, 0.8, 3.5)
    if t in _CYCLICAL:
        p6 = 0.5 + (p6 - 0.5) * 0.6                   # pull toward neutral
    # P7 fresh catalyst.
    p7 = 1.0 if info["strategy"] == "catalyst" else (0.4 if info["strategy"] == "cycle" else 0.2)
    # P8 confirm trend / not extended: penalise far above 200dma; reward
    #    pullback from the 52w high (room to run, owner is anti-momentum).
    above = f.get("pct_above_200dma")
    p8a = _band_inv(above, 0, 80)         # 0% above = 1.0, 80%+ above = 0.0
    p8b = _band(f.get("pct_below_52w_high"), 0, 40)
    p8 = (p8a + p8b) / 2.0 if (above is not None or f.get("pct_below_52w_high") is not None) else 0.5

    parts = {"P1": p1, "P2": p2, "P3": p3, "P4": p4, "P5": p5, "P6": p6, "P7": p7, "P8": p8}
    return sum(parts.values()), parts, eps_f


# --- GROWTH (0..10), momentum-tolerant ----------------------------------
def score_growth(t, f, info):
    eps_f = eps_surprise_factor(f.get("eps_beat_rate"), f.get("eps_beat_streak"))
    fwd = f.get("fwd_rev_growth")
    fwd_corr = None if fwd is None else fwd * eps_f
    eps_g = f.get("fwd_eps_growth")
    eps_corr = None if eps_g is None else eps_g * eps_f

    g_rev = _band(fwd_corr, 5, 50)                       # forward revenue
    g_eps = _band(eps_corr, 5, 60)                       # forward EPS
    g_cagr = _band(info.get("cagr_mid"), 8, 22)          # the old forecast (now 1 of 4)
    g_sec = _CYCLE_P5.get(cycle_of(t, info), 0.5)        # secular runway
    # weights: growth-engine emphasises actual fwd numbers over the hand forecast
    score10 = (g_rev * 3.5 + g_eps * 3.0 + g_cagr * 2.0 + g_sec * 1.5)
    return score10, {"rev": g_rev, "eps": g_eps, "cagr": g_cagr, "sec": g_sec}


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
    """Classify a name on the two-axis grid (median-ish thresholds)."""
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
        results.append({**info, "eight": eight, "growth10": g10, "blend": blend,
                        "quad": quadrant(eight, g10), "eps_f": eps_f,
                        "p8": parts8, "pg": partsg, "has_data": t in fund})

    keyf = {"growth": lambda r: -r["growth10"],
            "eight": lambda r: -r["eight"],
            "blend": lambda r: -(r["blend"] or 0)}[args.sort]
    results.sort(key=keyf)

    # ----- two-score table (no forced blend) -----
    print(f"\n=== HOLDING RATING  (csv={Path(args.csv).name}, sort={args.sort}) ===")
    print("    Growth 0-10 (momentum-tolerant) | 8-Point 0-8 (anti-momentum) | "
          "Quadrant")
    hdr = f"{'rk':>2} {'ticker':10s} {'wv':3s} {'book%':>5s} " \
          f"{'GROWTH':>6s} {'8PT':>4s} {'quadrant':10s} {'epsF':>5s}"
    if args.blend:
        hdr += f" {'blend':>5s}"
    hdr += "  data"
    print(hdr)
    for i, r in enumerate(results, 1):
        line = f"{i:2d} {r['ticker']:10s} {r['wave']:3s} {r['book_pct']:5.2f} " \
               f"{r['growth10']:6.1f} {r['eight']:4.2f} {r['quad']:10s} " \
               f"{r['eps_f']:5.2f}"
        if args.blend:
            line += f" {r['blend']:5.2f}"
        line += f"   {'Y' if r['has_data'] else '-'}"
        print(line)

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
