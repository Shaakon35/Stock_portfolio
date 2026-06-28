#!/usr/bin/env python3
"""2023-vintage classification + batching for the FULL AI-allocation universe.

This is the single source of truth for:
  * which AI-allocation names are backtestable to FY2023 (NEW_2023),
  * the 50-by-50 sourcing batches (BATCHES),
  * the POINT-IN-TIME strategy each name had in 2023 (STRATEGY_2023).

STRATEGY_2023 starts from each name's CURRENT strategy in
portfolio.AI_allocations and applies documented 2023 OVERRIDES where the name's
character was materially different then. The canonical example the user raised
is the reverse: NVDA was a *cycle* (buy-the-dip semi) name in 2023 and only
became a *dca* compounder later — so in the backtest NVDA is graded `cycle`.

The override RULE (consistently applied): a name that in 2023 was
GAAP-unprofitable, freshly public, or pre-inflection — i.e. an EVENT/turnaround
bet rather than a durable compounder or a clean cyclical — is graded `catalyst`
for 2023, regardless of how it is classified today. `lottery` names are also
mapped to `catalyst` because the engine's render_by_strategy only buckets
dca / cycle / catalyst.
"""

# ---------------------------------------------------------------------------
# NOT backtestable to FY2023 (post-2023 IPO / direct-listing / SPAC, or no
# company fundamentals at all). Excluded from sourcing; reported as skipped.
# ---------------------------------------------------------------------------
SKIP_NOT_2023 = sorted(set("""
CRCL CRWV RDDT ASTS RKLB RR SERV LUNR BKSY PL TEM AISP INFQ ACHR ARQQ
QSI QUBT RGTI RXRX VKTX XNDU HQ BOT LAES IREN CIFR ENVX OUST SRUUF SMHV.SW
OKLO NNE RBRK ALAB NBIS LAC GEV PENG SNDK QNT
""".split()))

# ---------------------------------------------------------------------------
# 2023 strategy OVERRIDES vs the current AI-allocation strategy.
# Each entry: TICKER -> ("strategy_2023", "why it differed in 2023").
# Only names whose 2023 character differs from today appear here; everything
# else inherits its current strategy (see STRATEGY_2023 builder below).
# ---------------------------------------------------------------------------
OVERRIDES_2023 = {
    # --- unprofitable / pre-inflection in 2023 -> catalyst (now cycle/dca) ---
    "SOFI": ("catalyst", "first GAAP profit only Q4-2023; a turnaround bet then"),
    "HOOD": ("catalyst", "unprofitable, post-meme restructuring through 2023"),
    "DKNG": ("catalyst", "still loss-making in 2023; path-to-profit story"),
    "TOST": ("catalyst", "GAAP-unprofitable in 2023; scaling bet"),
    "HIMS": ("catalyst", "tiny, only just breakeven in 2023; early-stage punt"),
    "COIN": ("catalyst", "deep crypto-winter losses in 2023; binary on cycle"),
    "U":    ("catalyst", "Unity loss-making + mgmt/restructuring turmoil 2023"),
    "PATH": ("catalyst", "UiPath GAAP-unprofitable in 2023; turnaround"),
    "GTLB": ("catalyst", "loss-making hypergrowth in 2023"),
    "MDB":  ("catalyst", "MongoDB GAAP-unprofitable in 2023; hypergrowth bet"),
    "NET":  ("catalyst", "Cloudflare GAAP-unprofitable in 2023; growth punt"),
    "FSLY": ("catalyst", "Fastly loss-making + decelerating in 2023"),
    "SNOW": ("catalyst", "Snowflake deeply GAAP-unprofitable in 2023 (was dca)"),
    "CELH": ("catalyst", "Celsius hyper-growth small-cap in 2023; momentum bet"),
    "NU":   ("catalyst", "Nubank only just turning profitable in 2023"),
    "SHOP": ("catalyst", "returned to profit only late-2023 after 2022 losses"),
    "DASH": ("catalyst", "DoorDash still GAAP-unprofitable in 2023"),
    "DUOL": ("catalyst", "barely breakeven, early-profit inflection in 2023"),
    "DOCS": ("catalyst", "small, growth-inflection name in 2023"),
    "ESTC": ("catalyst", "Elastic GAAP-unprofitable in 2023"),
    "OKTA": ("catalyst", "Okta GAAP-unprofitable + breach overhang in 2023"),
    "TTD":  ("catalyst", "high-multiple growth, momentum-driven in 2023"),
    "APP":  ("catalyst", "AppLovin mid-turnaround in 2023 before the AdTech ramp"),
    "SMCI": ("catalyst", "Supermicro pre-blowup AI-server momentum bet in 2023"),
    # --- speculative / lottery -> catalyst (engine buckets only 3 modes) ---
    "9880.HK": ("catalyst", "lottery class -> catalyst for the 8-point grid"),
    "AEHR": ("catalyst", "lottery class -> catalyst"),
    "QBTS": ("catalyst", "quantum lottery -> catalyst"),
    "BNTX": ("catalyst", "post-COVID earnings cliff; binary oncology pipeline"),
    "NVAX": ("catalyst", "going-concern / binary in 2023"),
    "CRSP": ("catalyst", "pre-approval gene-editing biotech in 2023"),
    "NTLA": ("catalyst", "pre-revenue gene-editing biotech in 2023"),
    "SMR":  ("catalyst", "NuScale pre-revenue SMR in 2023"),
    "IONQ": ("catalyst", "pre-revenue quantum in 2023"),
    "LEU":  ("catalyst", "Centrus enrichment, lumpy/binary in 2023"),
    "APLD": ("catalyst", "Applied Digital pre-scale data-center bet in 2023"),
    "SYM":  ("catalyst", "Symbotic early, lumpy, GAAP-unprofitable in 2023"),
}

# ---------------------------------------------------------------------------
# The 208 backtestable NEW names (full AI-allocation universe minus the
# already-covered 40 and minus SKIP_NOT_2023), split into 50-by-50 batches.
# ---------------------------------------------------------------------------
BATCH1 = [
    "000660.KS", "005930.KS", "0700.HK", "1810.HK", "9618.HK", "9880.HK",
    "9988.HK", "AAOI", "ABNB", "ADBE", "ADI", "ADYEY", "AEHR", "AEIS", "ALB",
    "AMGN", "AMKR", "ANET", "ANF", "APLD", "APP", "ASX", "AXP", "BDC",
    "BESI.AS", "BHP", "BLK", "BMY", "BNTX", "BSX", "BWXT", "CAMT", "CAT",
    "CCJ", "CDNS", "CEG", "CELH", "CIEN", "CLS", "CMG", "COHR", "COHU",
    "COIN", "CRDO", "CRM", "CRSP", "CRWD", "CVX", "CYBR", "DASH",
]
BATCH2 = [
    "DDOG", "DE", "DELL", "DHR", "DIOD", "DKNG", "DOCS", "DUK", "DUOL", "ELF",
    "EME", "EMR", "ENPH", "ENTG", "ESTC", "ETN", "FCX", "FI", "FIX", "FLR",
    "FN", "FORM", "FSLR", "FSLY", "FTNT", "GD", "GE", "GFS", "GILD",
    "GRMN", "GS", "GTLB", "HIMS", "HON", "HOOD", "HPQ", "HUBB", "HUBS", "HWM",
    "ICHR", "INFY", "INTU", "IONQ", "ISRG", "JBL", "JPM", "KLIC", "KO", "KTOS",
]
BATCH3 = [
    "LEU", "LIN", "LITE", "LLY", "LMT", "LNT", "LSCC", "MA", "MDB", "MDT",
    "MELI", "MKSI", "MMM", "MPWR", "MRVL", "MS", "MTSI", "MYRG", "NEE", "NET",
    "NFLX", "NKE", "NOC", "NOW", "NRG", "NTAP", "NTLA", "NU", "NUE", "NVAX",
    "NVMI", "NVO", "OKTA", "ON", "ONTO", "ORCL", "OXY", "PANW", "PATH", "PDD",
    "PFE", "PG", "PH", "PLTR", "PNR", "POWI", "POWL", "PSTG", "PWR",
]
BATCH4 = [
    "QBTS", "QCOM", "RIO", "ROK", "RTX", "S", "SANM", "SAP", "SBUX",
    "SHEL", "SHOP", "SIE.DE", "SIMO", "SMCI", "SMHN.DE", "SMR", "SNOW",
    "SNPS", "SO", "SOFI", "SPOT", "SQM", "SRE", "STLD", "STX", "SYK", "SYM",
    "TDG", "TEAM", "TECK", "TER", "TGT", "TLN", "TMDX", "TMO", "TOST", "TSEM",
    "TSM", "TTD", "TXN", "U", "UBER", "UMC", "UNH", "UNP", "URI", "V", "VPG",
    "VRT", "VRTX", "VST", "WDC", "WM", "XOM", "XYZ", "ZS",
]
BATCHES = [BATCH1, BATCH2, BATCH3, BATCH4]
NEW_2023 = [t for b in BATCHES for t in b]


def build_strategy_2023():
    """Current strategy with the documented 2023 overrides applied. Imported
    lazily so this module has no hard dependency at import time."""
    import os
    import sys
    from pathlib import Path
    os.environ.setdefault("PORTFOLIO_USE", "ai")
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import scoring.score_holdings as S
    port = S.portfolio_rows(include_watchlist=True)
    out = {}
    for t in NEW_2023:
        if t in OVERRIDES_2023:
            out[t] = OVERRIDES_2023[t][0]
        else:
            cur = port.get(t, {}).get("strategy", "cycle")
            out[t] = "catalyst" if cur == "lottery" else cur
    return out


if __name__ == "__main__":
    s = build_strategy_2023()
    from collections import Counter
    print("backtestable NEW names:", len(NEW_2023))
    print("skipped (not 2023):", len(SKIP_NOT_2023), SKIP_NOT_2023)
    print("2023 strategy mix:", dict(Counter(s.values())))
    print("overrides applied:", len(OVERRIDES_2023))
