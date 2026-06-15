# =========================================================================
# PORTFOLIO TARGET WEIGHTS (100% total)
# =========================================================================

MONTHLY_DEPOSIT = 1000.0  # Monthly fresh cash allocation in Euros
DEGIRO_FEE = 3.00         # Flat transaction fee

TARGET_WEIGHTS = {
    "XAIX.DE":           0.21,  # CHANGED: was 0.25 — trimmed 4% to fund OTHER_SATELLITE
    "SMHV.SW":               0.21,  # CHANGED: was 0.25 — trimmed 4% to fund OTHER_SATELLITE
    "QDVE.DE":            0.10,  # 10% S&P 500 Info Tech (Apple, MSFT, AVGO)
    "NUCLEAR_SATELLITE": 0.12,  # 12% Single Stock Nuclear Picking
    "QUANTUM_SATELLITE": 0.08,  # 8% Single Stock Quantum Speculative Rockets
    "CYBER_SATELLITE":   0.05,  # 5% Single Stock Cybersecurity Satellite
    "INDUSTRIAL_SATELLITE": 0.10,  # 10% Industrials & Defense (data center infra, nuclear defense)
    "SPECGROWTH_SATELLITE": 0.05,  # 5% Speculative Growth (high-growth semis, AI infra, aerospace)
    "OTHER_SATELLITE":   0.08,  # NEW: 8% Cross-sector diversifiers (MedTech, Defense, Battery S-curve)
}

# =========================================================================
# SUB-ALLOCATION BASKETS (each sums to 1.0 = 100% of its slice)
# =========================================================================

NUCLEAR_BASKET_TARGETS = {
    "CCJ":   0.36,  # CHANGED: was 0.40 — trimmed 4% to make room for APLD
    "GEV":   0.22,  # CHANGED: was 0.24 — trimmed 2% to make room for APLD
    "SRUUF": 0.16,  # 16% of Nuclear Slice
    "LEU":   0.12,  # 12% of Nuclear Slice
    "SMR":   0.04,  # 4% of Nuclear Slice
    "OKLO":  0.04,  # 4% of Nuclear Slice
    "APLD":  0.06,  # NEW: 6% — AI GPU data-center infra; nuclear-demand proxy (NOTE: not a pure nuclear name)
}

QUANTUM_BASKET_TARGETS = {
    "IONQ":  0.40,  # 40% of Quantum Slice
    "QNT":   0.25,  # 25% of Quantum Slice
    "QBTS":  0.25,  # 25% of Quantum Slice
    "RGTI":  0.10,  # 10% of Quantum Slice
    "QUBT":  0.00,  # Paused — weakest quantum thesis, no real IP, sell on any spike
    "XNDU":  0.00,  # Private Stage Gate
    "INFQ":  0.00,  # Private Stage Gate
    "HQ":    0.00,  # Private Stage Gate
}

CYBER_BASKET_TARGETS = {
    "CRWD":  0.80,  # 80% of Cyber Slice
    "PANW":  0.20,  # 20% of Cyber Slice
}

INDUSTRIAL_BASKET_TARGETS = {
    "BWXT":  0.40,  # 40% of Industrials Slice — Navy nuclear monopoly, SMR fuel
    "POWL":  0.25,  # 25% of Industrials Slice — Electrical switchgear, data center orders
    "VRT":   0.20,  # 20% of Industrials Slice — Data center power & cooling
    "FIX":   0.15,  # 15% of Industrials Slice — Data center HVAC & electrical buildout
}

SPECGROWTH_BASKET_TARGETS = {
    "RKLB":  0.30,  # 30% of Spec Growth Slice — Rocket Lab, satellite constellation
    "LSCC":  0.25,  # 25% of Spec Growth Slice — Lattice Semi, edge AI, automotive
    "CRDO":  0.25,  # 25% of Spec Growth Slice — Credo Tech, AI connectivity
    "VKTX":  0.20,  # 20% of Spec Growth Slice — Viking Therapeutics, GLP-1 obesity Phase III
}

# NEW: Cross-sector diversifiers outside the existing sector taxonomy.
# Per SKILL.md "Sector Exploration Philosophy" — scan broadly for asymmetric
# setups beyond semis/AI/nuclear/quantum/cyber. These three open new sectors
# (MedTech, Defense, Battery) that are uncorrelated to the current clusters.
OTHER_BASKET_TARGETS = {
    "TMDX":  0.45,  # 45% — TransMedics, organ-transplant OCS monopoly [HC] — hold_forever, profitable S-curve
    "AXON":  0.45,  # 45% — Taser + Evidence.com SaaS moat [DEF] — hold_forever, recurring-revenue compounder
    "ENVX":  0.10,  # 10% — Enovix silicon-anode battery [BATTERY] — catalyst, binary S-curve, sized tiny
}

# Aggressive Profit-Taking Triggers (1.25x original for "Let Winners Run")
SELL_TRIGGER_CEILING = {
    "NUCLEAR_SATELLITE":     0.15,
    "QUANTUM_SATELLITE":     0.10,
    "CYBER_SATELLITE":       0.0625,
    "INDUSTRIAL_SATELLITE":  0.125,
    "SPECGROWTH_SATELLITE":  0.0625,
    "OTHER_SATELLITE":       0.10,    # NEW: 1.25 × 0.08 — let cross-sector diversifiers run
    "SMHV.SW":                   0.3125,
    "QDVE.DE":                0.125,
}

# =========================================================================
# CURRENT HOLDINGS (share counts)
# =========================================================================

my_current_shares = {
    "XAIX.DE": 45, "SMHV.SW": 22, "QDVE.DE": 5,
    "CCJ": 15, "GEV": 5, "SRUUF": 25, "LEU": 10, "SMR": 50, "OKLO": 30,
    "IONQ": 100, "QNT": 0, "QBTS": 250, "RGTI": 400, "QUBT": 150,
    "CRWD": 2, "PANW": 3,
    # Industrials & Defense — new positions (not yet purchased)
    "BWXT": 0, "POWL": 0, "VRT": 0, "FIX": 0,
    # Speculative Growth — new positions (not yet purchased)
    "RKLB": 0, "LSCC": 0, "CRDO": 0, "VKTX": 0,
    # NEW: Other / cross-sector diversifiers (not yet purchased)
    "TMDX": 0, "AXON": 0, "ENVX": 0,
    # NEW: APLD added to nuclear basket (not yet purchased)
    "APLD": 0,
}

# =========================================================================
# ETF LOOK-THROUGH (underlying stock exposures per ETF)
# =========================================================================

ETF_LOOK_THROUGH = {
    # CHANGED: refreshed top-10 holdings from Yahoo Finance (QDVE.DE/SMHV.SW/XAIX.DE)
    "SMHV.SW": {  # VanEck Semiconductor — top 10 = 79.79%
        "MU": 0.1433, "AMD": 0.1222, "AVGO": 0.0833, "INTC": 0.0802, "TSM": 0.0751,
        "ASML": 0.0740, "NVDA": 0.0723, "LRCX": 0.0563, "AMAT": 0.0513, "TXN": 0.0399,
        "OTHER_SEMI": 0.2021,
    },
    "QDVE.DE": {  # iShares S&P 500 Info Tech (Acc) — top 10 = 74.66%
        "NVDA": 0.2040, "AAPL": 0.1668, "MSFT": 0.1367, "AVGO": 0.0866, "MU": 0.0447,
        "AMD": 0.0344, "INTC": 0.0220, "CSCO": 0.0195, "LRCX": 0.0163, "ORCL": 0.0156,
        "OTHER_TECH": 0.2534,
    },
    "XAIX.DE": {  # Xtrackers AI & Big Data (Acc) — top 10 = 53.07%
        "MU": 0.0905, "005930.KS": 0.0833, "000660.KS": 0.0770, "INTC": 0.0492, "CSCO": 0.0413,
        "GOOGL": 0.0400, "AMZN": 0.0386, "AAPL": 0.0378, "NVDA": 0.0373, "ORCL": 0.0356,
        "OTHER_AI": 0.4694,  # remainder padded +0.0001 so weights sum to exactly 1.0
    },
}


def verify_allocations():
    """Assert that all allocation matrices sum correctly."""
    total_target = sum(TARGET_WEIGHTS.values())
    assert abs(sum(NUCLEAR_BASKET_TARGETS.values()) - 1.0) < 1e-9, "Nuclear basket doesn't sum to 100%"
    assert abs(sum(QUANTUM_BASKET_TARGETS.values()) - 1.0) < 1e-9, "Quantum basket doesn't sum to 100%"
    assert abs(sum(CYBER_BASKET_TARGETS.values()) - 1.0) < 1e-9, "Cyber basket doesn't sum to 100%"
    assert abs(sum(INDUSTRIAL_BASKET_TARGETS.values()) - 1.0) < 1e-9, "Industrial basket doesn't sum to 100%"
    assert abs(sum(SPECGROWTH_BASKET_TARGETS.values()) - 1.0) < 1e-9, "Spec Growth basket doesn't sum to 100%"
    assert abs(sum(OTHER_BASKET_TARGETS.values()) - 1.0) < 1e-9, "Other basket doesn't sum to 100%"  # NEW


# =========================================================================
# WATCHLIST — discussed but NOT held (no target weight, 0% of book)
# =========================================================================
# Names reviewed during portfolio analysis but deliberately left out, with the
# reason they were excluded. Kept here for reference so the rationale isn't lost.
#
# Schema per entry:
#   "strategy"  — hold_forever | cycle | catalyst | lottery_ticket
#                 (lottery_ticket = catalyst with ->$0 / -70%+ binary downside)
#   "area"      — sector/basket the name would map to if ever added
#   "note"      — why it's on the bench (not in the portfolio)
#
# NOTE: This is documentation only. These tickers have NO target weight and are
# excluded from verify_allocations(). Move an entry into a basket above to buy.

WATCHLIST_EXCLUDED = {
    "KTOS": {
        "strategy": "cycle",
        "area":     "Industrial / Defense",
        "note":     "Autonomous military drones. CHANGED: KTOS dropped out of XAIX.DE "
                    "top holdings (latest look-through), so the prior 'already held "
                    "indirectly' overlap no longer applies. Now a clean candidate — "
                    "consider for INDUSTRIAL if adding defense exposure.",
    },
    "IREN": {
        "strategy": "cycle",
        "area":     "Industrial (AI compute + Bitcoin mining)",
        "note":     "SMALL/SKIP — crypto-correlated beta is new uncorrelated risk, "
                    "not diversification. Profitable but lower quality than VRT/POWL.",
    },
    "CIFR": {
        "strategy": "cycle",
        "area":     "Industrial (Bitcoin mining pivoting to AI)",
        "note":     "SKIP — unprofitable (-$2.32 EPS), crypto-dependent, weaker than "
                    "every industrial incumbent already held.",
    },
    "LUNR": {
        "strategy": "lottery_ticket",
        "area":     "SpecGrowth / Space",
        "note":     "Lunar landers. SKIP — RKLB owns the space slot and dominates it: "
                    "LUNR is lower-quality AND higher-risk (-70%+ vs RKLB -30-50%).",
    },
    "SERV": {
        "strategy": "lottery_ticket",
        "area":     "SpecGrowth / Robotics",
        "note":     "Sidewalk delivery robots. SKIP/TINY — $600M micro-cap, -$2.05 EPS. "
                    "'Nvidia-backed' = small passive stake, not a deal. Hype-driven; "
                    "sell into RSI>70 spikes if ever bought. ~1% max.",
    },
    "ACHR": {
        "strategy": "lottery_ticket",
        "area":     "SpecGrowth / Transportation (eVTOL)",
        "note":     "eVTOL air taxi. SKIP/TINY — worst risk on the list (->$0). "
                    "Triple-gated: FAA cert + manufacturing + demand. Event = FAA Type "
                    "Certification (~2026-2028, likely slips); sell 50% into cert hype. "
                    "~1% max.",
    },
}
