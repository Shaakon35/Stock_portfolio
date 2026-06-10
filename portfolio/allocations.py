# =========================================================================
# PORTFOLIO TARGET WEIGHTS (100% total)
# =========================================================================

MONTHLY_DEPOSIT = 1000.0  # Monthly fresh cash allocation in Euros
DEGIRO_FEE = 3.00         # Flat transaction fee

TARGET_WEIGHTS = {
    "XAIX.DE":           0.25,  # 25% Core AI & Big Data Index
    "SMHV.SW":               0.25,  # 25% Core Semiconductors (NVIDIA, ASML, TSMC)
    "QDVE.DE":            0.10,  # 10% S&P 500 Info Tech (Apple, MSFT, AVGO)
    "NUCLEAR_SATELLITE": 0.12,  # 12% Single Stock Nuclear Picking
    "QUANTUM_SATELLITE": 0.08,  # 8% Single Stock Quantum Speculative Rockets
    "CYBER_SATELLITE":   0.05,  # 5% Single Stock Cybersecurity Satellite
    "INDUSTRIAL_SATELLITE": 0.10,  # 10% Industrials & Defense (data center infra, nuclear defense)
    "SPECGROWTH_SATELLITE": 0.05,  # 5% Speculative Growth (high-growth semis, AI infra, aerospace)
}

# =========================================================================
# SUB-ALLOCATION BASKETS (each sums to 1.0 = 100% of its slice)
# =========================================================================

NUCLEAR_BASKET_TARGETS = {
    "CCJ":   0.40,  # 40% of Nuclear Slice
    "GEV":   0.24,  # 24% of Nuclear Slice
    "SRUUF": 0.16,  # 16% of Nuclear Slice
    "LEU":   0.12,  # 12% of Nuclear Slice
    "SMR":   0.04,  # 4% of Nuclear Slice
    "OKLO":  0.04,  # 4% of Nuclear Slice
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

# Aggressive Profit-Taking Triggers (1.25x original for "Let Winners Run")
SELL_TRIGGER_CEILING = {
    "NUCLEAR_SATELLITE":     0.15,
    "QUANTUM_SATELLITE":     0.10,
    "CYBER_SATELLITE":       0.0625,
    "INDUSTRIAL_SATELLITE":  0.125,
    "SPECGROWTH_SATELLITE":  0.0625,
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
}

# =========================================================================
# ETF LOOK-THROUGH (underlying stock exposures per ETF)
# =========================================================================

ETF_LOOK_THROUGH = {
    "SMHV.SW": {
        "TSM": 0.1009, "ASML": 0.1008, "NVDA": 0.0992, "AVGO": 0.0959, "MU": 0.0829,
        "AMD": 0.0801, "AMAT": 0.0647, "LRCX": 0.0629, "INTC": 0.0513, "TXN": 0.0422,
        "OTHER_SEMI": 0.2191,
    },
    "QDVE.DE": {
        "NVDA": 0.2301, "AAPL": 0.1853, "MSFT": 0.1536, "AVGO": 0.0820, "MU": 0.0212,
        "PLTR": 0.0187, "AMD": 0.0185, "CSCO": 0.0171, "AMAT": 0.0152, "LRCX": 0.0149,
        "OTHER_TECH": 0.2434,
    },
    "XAIX.DE": {
        "TSLA": 0.0934, "TER": 0.0730, "AMD": 0.0669, "PLTR": 0.0552, "TSM": 0.0412,
        "KTOS": 0.0380, "META": 0.0370, "SHOP": 0.0367, "GOOGL": 0.0353, "RBLX": 0.0304,
        "OTHER_AI": 0.4929,
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
