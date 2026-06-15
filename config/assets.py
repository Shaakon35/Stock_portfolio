# =========================================================================
# ETF UNIVERSE
# =========================================================================
etfs = {
    # --- CORE ETFs ---
    "[CORE] Invesco NASDAQ-100 (25%)": "EQQQ.L",
    "[CORE] VanEck Semiconductor (40%)": "SMHV.SW",
    "[CORE] Vanguard FTSE Dev World (13%)": "V3AA.L",
    "[CORE] S&P 500 Info Tech (22%)": "QDVE.DE",

    # --- AI & ROBOTICS ETFs ---
    "[AI] ARK AI & Robotics": "ARKI.L",
    "[AI] Global X Robotics & AI": "BOTZ",
    "[AI] Robo Global Robotics & Auto": "ROBO",
    "[AI] VanEck Quantum Computing": "QNTM.L",
    "[AI] Xtrackers AI & Big Data": "XAIX.SW",

    # --- GENOMICS ETFs ---
    # "[GEN] ARK Genomic Revolution": "ARKG",
    # "[GEN] iShares Genomics Immunology": "IDNA",

    # --- SECTOR / THEMATIC ETFs ---
    # "[DEF] VanEck Defense ETF": "DFNS.L",
    # "[INF] Pacer Data & Digital Infra": "SRVR",
    # "[MED] VanEck Biotech (GLP-1 Alpha)": "BBH",

    # --- SPECULATIVE ETFs ---
    # "[SPEC] iShares MSCI South Korea": "EWY",
    # "[SPEC] First Trust Nasdaq Semi": "FTXL",
    # "[SPEC] Global X Hydrogen": "HYDR",
    # "[SPEC] CoinShares BTC Mining": "WGMI",
}

# =========================================================================
# SINGLE STOCK UNIVERSE
# =========================================================================
single_stocks = {
    # --- CORE stock ---
    "[CORE] Roche Holding AG (CHF) (100%)": "RO.SW",

    # --- [TECH] MEGA CAP / STANDARD STOCKS ---
    "[TECH] Alphabet Inc.": "GOOG",
    "[TECH] Amazon.com, Inc.": "AMZN",
    "[TECH] Apple Inc.": "AAPL",
    "[TECH] ASML Holding N.V.": "ASML",
    "[TECH] Intel Corporation": "INTC",
    "[TECH] Microsoft Corporation": "MSFT",
    "[TECH] NVIDIA Corporation": "NVDA",
    "[TECH] Oracle Corporation": "ORCL",
    "[TECH] Tesla, Inc.": "TSLA",
    "[TECH] Broadcom Inc.": "AVGO",
    "[TECH] Advanced Micro Devices, Inc.": "AMD",
    "[TECH] Palantir Technologies Inc.": "PLTR",
    "[TECH] Marvell Technology, Inc.": "MRVL",

    # --- [FIN] FINANCIALS / STABLE ---
    "[FIN] Circle Internet Group": "CRCL",

    # --- [ENG] ENERGY ---
    "[ENG] Chevron Corporation": "CVX",
    "[ENG] Bloom Energy Corporation": "BE",

    # --- [NUC] NUCLEAR STOCK PICKING BACKBONE ---
    "[NUC] Cameco Corporation": "CCJ",
    "[NUC] GE Vernova Inc.": "GEV",
    "[NUC] Sprott Physical Uranium": "SRUUF",
    "[NUC] Centrus Energy Corp.": "LEU",
    "[NUC] NuScale Power": "SMR",
    "[NUC] Oklo Inc.": "OKLO",
    "[NUC] Applied Digital Corporation": "APLD",  # NEW: AI GPU data-center infra (nuclear-demand proxy)

    # --- [QTM] PURE-PLAY QUANTUM COMPUTING BASKET ---
    "[QTM] IonQ, Inc.": "IONQ",
    "[QTM] D-Wave Quantum Inc.": "QBTS",
    "[QTM] Rigetti Computing, Inc.": "RGTI",
    "[QTM] Xanadu Quantum Technologies": "XNDU",
    "[QTM] Quantum Computing Inc.": "QUBT",
    "[QTM] Infleqtion": "INFQ",
    "[QTM] Horizon Quantum Computing": "HQ",
    "[QTM] Quantinuum": "QNT",

    # --- [CYBER] CYBERSECURITY SATELLITE ENGINE ---
    "[CYBER] CrowdStrike Holdings, Inc.": "CRWD",
    "[CYBER] Palo Alto Networks, Inc.": "PANW",

    # --- [IND] INDUSTRIALS & DEFENSE SATELLITE ---
    "[IND] BWX Technologies, Inc.": "BWXT",
    "[IND] Powell Industries, Inc.": "POWL",
    "[IND] Vertiv Holdings Co": "VRT",
    "[IND] Comfort Systems USA, Inc.": "FIX",

    # --- [SPEC] SPECULATIVE GROWTH SATELLITE ---
    "[SPEC] Rocket Lab USA, Inc.": "RKLB",
    "[SPEC] Lattice Semiconductor Corp.": "LSCC",
    "[SPEC] Credo Technology Group": "CRDO",
    "[SPEC] Viking Therapeutics, Inc.": "VKTX",

    # --- [OTHER] CROSS-SECTOR DIVERSIFIERS (MedTech, Defense, Battery) ---
    "[OTHER] TransMedics Group, Inc.": "TMDX",   # NEW: organ-transplant OCS monopoly (MedTech)
    "[OTHER] Axon Enterprise, Inc.": "AXON",     # NEW: Taser + Evidence.com SaaS moat (Defense)
    "[OTHER] Enovix Corporation": "ENVX",        # NEW: silicon-anode battery S-curve (Battery)
}

# =========================================================================
# DERIVED LOOKUPS
# =========================================================================
all_groups = {
    "ETFs": etfs,
    "Stocks": single_stocks,
}

ticker_to_name = {
    **{v: k for k, v in etfs.items()},
    **{v: k for k, v in single_stocks.items()},
}

current_tickers = list(ticker_to_name.keys())
