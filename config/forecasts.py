# =========================================================================
# ETF CAGR FORECAST MODELS
# =========================================================================
# Framework: Forecasted CAGR = Base Index Return + Secular Alpha Premium
#            - Risk/Cyclicality Discount
#
# 1. BASELINE ANCHORING
#    - Global Equity (~8.2%): non-leveraged equity risk premium (VGWL)
#    - Tech / Growth (~14.2%–15.6%): 10-year mega-cap platform economics
#
# 2. SECULAR ALPHA PREMIUMS
#    - Capex Infrastructure: +2.0% to +4.0% (hardware, data nodes)
#    - Product Alpha & Defense: +1.0% to +3.0% (sovereign budgets, drugs)
#    - S-Curve Adoption: +5.0% to +10.0% (early-stage disruption)
#
# 3. RISK DISCOUNTS
#    - High-Beta Cyclicality: -1.5% to -4.0%
#    - Capital Burn: -2.0% to -5.0%
#    - Extreme Volatility Cap: macro/halving constraints
# =========================================================================

growth_forecast_models = {
    "[CORE] Vanguard FTSE Dev World (13%)":   {"rate": 8.2,  "risk": "Low (High Conf)",    "cyclic": "",    "loss_risk": "Low"},
    "[CORE] Invesco NASDAQ-100 (25%)":        {"rate": 14.2, "risk": "Med-Low (Stable)",   "cyclic": "",    "loss_risk": "Low"},
    "[CORE] iShares S&P 500 Info Tech (22%)": {"rate": 15.6, "risk": "Medium (Stable)",    "cyclic": "",    "loss_risk": "Low"},
    "[CORE] VanEck Semiconductor (40%)":      {"rate": 18.2, "risk": "Med-High (Beta)",    "cyclic": "Yes", "loss_risk": "Low-Med"},

    "[AI] ARK AI & Robotics":                 {"rate": 14.8, "risk": "Med-High (Beta)",    "cyclic": "",    "loss_risk": "Medium"},
    "[AI] Global X Robotics & AI":            {"rate": 15.1, "risk": "Med-High (Beta)",    "cyclic": "",    "loss_risk": "Medium"},
    "[AI] Robo Global Robotics & Auto":       {"rate": 12.9, "risk": "Medium (Stable)",    "cyclic": "",    "loss_risk": "Low"},
    "[AI] VanEck Quantum Computing":          {"rate": 24.5, "risk": "High (Speculative)", "cyclic": "",    "loss_risk": "High"},
    "[AI] Xtrackers AI & Big Data":           {"rate": 19.2, "risk": "Med-High (Volatile)","cyclic": "",    "loss_risk": "Low-Med"},

    "[GEN] ARK Genomic Revolution":           {"rate": 11.5, "risk": "High (Volatile)",    "cyclic": "",    "loss_risk": "High"},
    "[GEN] iShares Genomics Immunology":      {"rate": 10.8, "risk": "High (Volatile)",    "cyclic": "",    "loss_risk": "High"},

    "[DEF] VanEck Defense ETF":               {"rate": 12.4, "risk": "Low-Med (Sovereign)","cyclic": "",    "loss_risk": "Low"},
    "[INF] Pacer Data & Digital Infra":       {"rate": 16.8, "risk": "Medium (Capex Hub)", "cyclic": "Yes", "loss_risk": "Low"},
    "[MED] VanEck Biotech (GLP-1 Alpha)":     {"rate": 14.5, "risk": "Medium (Secular)",   "cyclic": "",    "loss_risk": "Medium"},

    "[SPEC] CoinShares BTC Mining":           {"rate": 26.5, "risk": "Extreme (Volatile)", "cyclic": "Yes", "loss_risk": "Extreme"},
    "[SPEC] First Trust Nasdaq Semi":         {"rate": 19.0, "risk": "High (Beta)",        "cyclic": "Yes", "loss_risk": "Medium"},
    "[SPEC] Global X Hydrogen":               {"rate": 10.2, "risk": "High (Speculative)", "cyclic": "Yes", "loss_risk": "High"},
    "[SPEC] iShares MSCI South Korea":        {"rate": 9.5,  "risk": "Med-High (Geopol)",  "cyclic": "Yes", "loss_risk": "Med-High"},
}

# =========================================================================
# INDIVIDUAL STOCK CAGR FORECAST MODELS
# =========================================================================

stock_forecast_models = {
    # --- TECH ---
    "[TECH] Alphabet Inc.":                  {"min_rate": 8.0,  "max_rate": 15.0, "risk": "Medium (Stable)",    "cyclic": "No",  "loss_risk": "Low"},
    "[TECH] Amazon.com, Inc.":               {"min_rate": 10.0, "max_rate": 18.0, "risk": "Medium (Capex)",     "cyclic": "Yes", "loss_risk": "Low-Med"},
    "[TECH] Apple Inc.":                     {"min_rate": 5.0,  "max_rate": 12.0, "risk": "Low (Stable)",       "cyclic": "No",  "loss_risk": "Low"},
    "[TECH] ASML Holding N.V.":              {"min_rate": 12.0, "max_rate": 22.0, "risk": "Medium (Moat)",      "cyclic": "Yes", "loss_risk": "Medium"},
    "[TECH] Intel Corporation":              {"min_rate": 2.0,  "max_rate": 14.0, "risk": "High (Turnaround)",  "cyclic": "Yes", "loss_risk": "Medium"},
    "[TECH] Microsoft Corporation":          {"min_rate": 10.0, "max_rate": 16.0, "risk": "Low (Stable)",       "cyclic": "No",  "loss_risk": "Low"},
    "[TECH] NVIDIA Corporation":             {"min_rate": 15.0, "max_rate": 30.0, "risk": "High (Hardware)",    "cyclic": "Yes", "loss_risk": "Medium"},
    "[TECH] Oracle Corporation":             {"min_rate": 8.0,  "max_rate": 15.0, "risk": "Medium (Cloud)",     "cyclic": "No",  "loss_risk": "Low-Med"},
    "[TECH] Tesla, Inc.":                    {"min_rate": 5.0,  "max_rate": 25.0, "risk": "High (Auto/AI)",     "cyclic": "Yes", "loss_risk": "High"},
    "[TECH] Broadcom Inc.":                  {"min_rate": 12.0, "max_rate": 20.0, "risk": "Low-Med (Moat)",     "cyclic": "No",  "loss_risk": "Low"},
    "[TECH] Advanced Micro Devices, Inc.":   {"min_rate": 10.0, "max_rate": 22.0, "risk": "High (Beta)",        "cyclic": "Yes", "loss_risk": "Medium"},
    "[TECH] Palantir Technologies Inc.":     {"min_rate": 14.0, "max_rate": 28.0, "risk": "High (Growth)",      "cyclic": "No",  "loss_risk": "Low-Med"},
    "[TECH] Marvell Technology, Inc.":       {"min_rate": 11.0, "max_rate": 24.0, "risk": "High (Electro)",     "cyclic": "Yes", "loss_risk": "Medium"},

    # --- FIN / ENG / HC ---
    "[FIN] Circle Internet Group":           {"min_rate": 15.0, "max_rate": 35.0, "risk": "High (Crypto)",      "cyclic": "Yes", "loss_risk": "High"},
    "[ENG] Chevron Corporation":             {"min_rate": 4.0,  "max_rate": 10.0, "risk": "Med (Commodity)",    "cyclic": "Yes", "loss_risk": "Medium"},
    "[ENG] Bloom Energy Corporation":        {"min_rate": 8.0,  "max_rate": 26.0, "risk": "High (Growth)",      "cyclic": "Yes", "loss_risk": "High"},
    "[HC] Roche Holding AG (CHF) (100%)":    {"min_rate": 5.0,  "max_rate": 10.0, "risk": "Low (Pharma)",       "cyclic": "No",  "loss_risk": "Low"},

    # --- NUC ---
    "[NUC] Cameco Corporation":              {"min_rate": 8.0,  "max_rate": 18.0, "risk": "Medium (Stable)",    "cyclic": "Yes", "loss_risk": "Medium"},
    "[NUC] GE Vernova Inc.":                 {"min_rate": 10.0, "max_rate": 20.0, "risk": "Medium (Capex)",     "cyclic": "Yes", "loss_risk": "Medium"},
    "[NUC] Sprott Physical Uranium":         {"min_rate": 6.0,  "max_rate": 15.0, "risk": "Low-Med (Asset)",    "cyclic": "Yes", "loss_risk": "Low"},
    "[NUC] Centrus Energy Corp.":            {"min_rate": 12.0, "max_rate": 25.0, "risk": "High (Geopol)",      "cyclic": "No",  "loss_risk": "High"},
    "[NUC] NuScale Power":                   {"min_rate": -10.0,"max_rate": 35.0, "risk": "Extreme (Burn)",     "cyclic": "No",  "loss_risk": "Extreme"},
    "[NUC] Oklo Inc.":                       {"min_rate": -15.0,"max_rate": 40.0, "risk": "Extreme (Burn)",     "cyclic": "No",  "loss_risk": "Extreme"},
    "[NUC] Applied Digital Corporation":     {"min_rate": -20.0,"max_rate": 40.0, "risk": "High (Capex Burn)",  "cyclic": "Yes", "loss_risk": "High"},  # NEW: AI GPU DC infra, unprofitable high-beta

    # --- QTM ---
    "[QTM] IonQ, Inc.":                      {"min_rate": -20.0, "max_rate": 45.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},
    "[QTM] D-Wave Quantum Inc.":             {"min_rate": -25.0, "max_rate": 35.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},
    "[QTM] Rigetti Computing, Inc.":         {"min_rate": -25.0, "max_rate": 30.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},
    "[QTM] Xanadu Quantum Technologies":     {"min_rate": -20.0, "max_rate": 50.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},
    "[QTM] Quantum Computing Inc.":          {"min_rate": -30.0, "max_rate": 25.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},
    "[QTM] Infleqtion":                      {"min_rate": -20.0, "max_rate": 45.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},
    "[QTM] Horizon Quantum Computing":       {"min_rate": -20.0, "max_rate": 45.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},
    "[QTM] Quantinuum":                      {"min_rate": -15.0, "max_rate": 40.0, "risk": "Extreme", "cyclic": "No", "loss_risk": "Extreme"},

    # --- CYBER ---
    "[CYBER] CrowdStrike Holdings, Inc.":    {"min_rate": 12.0, "max_rate": 26.0, "risk": "Medium (Moat)",     "cyclic": "No",  "loss_risk": "Low-Med"},
    "[CYBER] Palo Alto Networks, Inc.":      {"min_rate": 10.0, "max_rate": 22.0, "risk": "Low-Med (Stable)",  "cyclic": "No",  "loss_risk": "Low"},

    # --- IND (Industrials & Defense) ---
    "[IND] BWX Technologies, Inc.":          {"min_rate": 10.0, "max_rate": 18.0, "risk": "Low-Med (Monopoly)","cyclic": "No",  "loss_risk": "Low"},
    "[IND] Powell Industries, Inc.":         {"min_rate": 12.0, "max_rate": 24.0, "risk": "Med-High (Capex)",  "cyclic": "Yes", "loss_risk": "Medium"},
    "[IND] Vertiv Holdings Co":              {"min_rate": 14.0, "max_rate": 26.0, "risk": "Medium (DC Infra)", "cyclic": "Yes", "loss_risk": "Medium"},
    "[IND] Comfort Systems USA, Inc.":       {"min_rate": 10.0, "max_rate": 20.0, "risk": "Low-Med (Backlog)", "cyclic": "Yes", "loss_risk": "Low-Med"},

    # --- SPEC (Speculative Growth) ---
    "[SPEC] Rocket Lab USA, Inc.":           {"min_rate": 5.0,  "max_rate": 35.0, "risk": "High (Aerospace)",  "cyclic": "No",  "loss_risk": "High"},
    "[SPEC] Lattice Semiconductor Corp.":    {"min_rate": 8.0,  "max_rate": 22.0, "risk": "Med-High (Edge AI)","cyclic": "Yes", "loss_risk": "Medium"},
    "[SPEC] Credo Technology Group":         {"min_rate": 15.0, "max_rate": 35.0, "risk": "High (Growth)",     "cyclic": "Yes", "loss_risk": "Medium"},
    "[SPEC] Viking Therapeutics, Inc.":       {"min_rate": -30.0, "max_rate": 50.0, "risk": "High (Binary)",    "cyclic": "No",  "loss_risk": "High"},

    # --- OTHER (Cross-sector diversifiers: MedTech, Defense, Battery) ---
    "[OTHER] TransMedics Group, Inc.":       {"min_rate": 14.0,  "max_rate": 30.0, "risk": "Med-High (S-Curve)","cyclic": "No",  "loss_risk": "Medium"},   # NEW: profitable transplant monopoly, S-curve adoption
    "[OTHER] Axon Enterprise, Inc.":         {"min_rate": 12.0,  "max_rate": 25.0, "risk": "Low-Med (SaaS Moat)","cyclic": "No", "loss_risk": "Low-Med"},  # NEW: Taser + Evidence.com recurring revenue
    "[OTHER] Enovix Corporation":            {"min_rate": -35.0, "max_rate": 55.0, "risk": "Extreme (Binary)",  "cyclic": "No",  "loss_risk": "Extreme"},  # NEW: silicon-anode battery, binary S-curve
}

# =========================================================================
# AI WAVE FORECAST MODELS (ticker-keyed)
# =========================================================================
# Per-ticker CAGR ranges (min/max %) for the AI value-chain wave allocation
# in portfolio/AI_allocations.py. Ticker-keyed (not display-name keyed) because
# the wave baskets reference bare tickers (e.g. "NVDA", "GOOGL").
#
# METHODOLOGY — these CAGRs are NOT independent guesses. They are BACK-SOLVED
# from per-ticker 5-YEAR TOTAL-RETURN intervals (the disciplined, mean-
# reversion-aware artifact). For each ticker:
#       CAGR = (1 + total_5y/100) ** (1/5) - 1
# so that portfolio_overview.ipynb's Growth tab — which compounds the CAGR
# over 5y as (1+CAGR)**5 - 1 — reproduces the source 5Y interval EXACTLY.
# The "5Y" comment on each line is the source-of-truth total return; the CAGR
# is derived from it. This keeps the Growth tab and the 5Y reasoning table in
# lockstep (one source of truth) instead of two tables that disagree.
#
# 29 tickers come straight from the 5Y reasoning table. The 5 wave-only names
# without an entry there (MRVL, MU, AMD, NOW, SNOW) were assigned 5Y intervals
# in the same disciplined style, then back-solved identically.
WAVE_FORECASTS = {
    # --- W1 SILICON ---
    "SMHV.SW": {"min_rate": 9.9,  "max_rate": 17.1},  # 5Y +60/+120% — diversified semi ETF, lower variance
    "NVDA":    {"min_rate": 9.9,  "max_rate": 20.1},  # 5Y +60/+150% — AI GPU demand, priced-in but dominant
    "AVGO":    {"min_rate": 9.9,  "max_rate": 19.1},  # 5Y +60/+140% — custom AI silicon + software
    "ASML":    {"min_rate": 8.4,  "max_rate": 18.1},  # 5Y +50/+130% — EUV monopoly, cyclical orders
    "MRVL":    {"min_rate": 8.4,  "max_rate": 21.1},  # 5Y +50/+160% — custom ASIC/optical DSP (est.)
    "TSM":     {"min_rate": 11.2, "max_rate": 21.1},  # 5Y +70/+160% — foundry monopoly, fair valuation
    "MU":        {"min_rate": 3.7,  "max_rate": 22.0},  # 5Y +20/+170% — memory/HBM, violently cyclical (est.)
    "AMD":       {"min_rate": 8.4,  "max_rate": 22.0},  # 5Y +50/+170% — #2 GPU, high beta (est.)
    "BESI.AS":   {"min_rate": 9.9,  "max_rate": 22.9},  # 5Y +60/+180% — advanced packaging pure-play, high-beta single-tech (est.)
    "000660.KS": {"min_rate": 4.6,  "max_rate": 22.9},  # 5Y +25/+180% — SK Hynix, HBM leader, same memory cycle as MU (est.)
    "005930.KS": {"min_rate": 3.7,  "max_rate": 17.1},  # 5Y +20/+120% — Samsung, diluted conglomerate, lower beta (est.)
    "CDNS":      {"min_rate": 9.9,  "max_rate": 18.1},  # 5Y +60/+130% — EDA duopoly, secular high-margin compounder (est.)
    "ONTO":      {"min_rate": 9.9,  "max_rate": 21.1},  # 5Y +60/+160% — metrology/inspection, high-beta WFE, mid-cycle (est.)
    "SMHN.DE":   {"min_rate": 9.9,  "max_rate": 24.6},  # 5Y +60/+200% — adv-packaging/bonding equip, same HBM bottleneck as BESI, early-cycle (est.)

    # --- W2 POWER ---
    "GEV":     {"min_rate": 12.5, "max_rate": 24.6},  # 5Y +80/+200% — grid/turbine supercycle
    "CEG":     {"min_rate": 9.9,  "max_rate": 21.1},  # 5Y +60/+160% — nuclear utility powering DCs
    "CCJ":     {"min_rate": 11.2, "max_rate": 22.9},  # 5Y +70/+180% — uranium supply deficit to 2035
    "ETN":     {"min_rate": 8.4,  "max_rate": 16.0},  # 5Y +50/+110% — transmission/electrification, quality compounder (est.)
    "HUBB":    {"min_rate": 8.4,  "max_rate": 16.0},  # 5Y +50/+110% — transformers/grid gear, 2-4yr lead-times, early (est.)
    "ABBN.SW": {"min_rate": 8.4,  "max_rate": 17.1},  # 5Y +50/+120% — HVDC/transformers (EU), grid buildout (est.)
    "PWR":     {"min_rate": 9.9,  "max_rate": 21.1},  # 5Y +60/+160% — transmission contractor, early-cycle backlog (est.)
    "OKLO":    {"min_rate": -12.9,"max_rate": 32.0},  # 5Y -50/+300% — SMR catalyst, pre-revenue (binary)
    # REMOVED from baskets (kept for reference / easy re-add):
    #   "POWL":    {"min_rate": 5.4,  "max_rate": 14.9},  # 5Y +30/+100% — switchgear, late-cycle
    #   "VST":     {"min_rate": 8.4,  "max_rate": 20.1},  # 5Y +50/+150% — power merchant, late-cycle

    # --- W3 DC-INFRA ---
    "VRT":     {"min_rate": 11.2, "max_rate": 22.9},  # 5Y +70/+180% — liquid cooling leader, capex wave
    "ANET":    {"min_rate": 9.9,  "max_rate": 20.1},  # 5Y +60/+150% — DC networking, profitable
    "CRDO":    {"min_rate": 9.9,  "max_rate": 24.6},  # 5Y +60/+200% — optical interconnect, hypergrowth
    "NVT":     {"min_rate": 8.4,  "max_rate": 18.1},  # 5Y +50/+130% — DC enclosures + liquid cooling, early-cycle (est.)
    # REMOVED from basket (kept for reference / easy re-add):
    #   "FIX":     {"min_rate": 5.4,  "max_rate": 16.0},  # 5Y +30/+110% — DC construction, late-cycle
    "COHR":    {"min_rate": 8.4,  "max_rate": 21.1},  # 5Y +50/+160% — optical components
    "ALAB":    {"min_rate": 9.9,  "max_rate": 27.2},  # 5Y +60/+230% — AI connectivity pure-play; mid-cycle (already +500%/2y) (est.)
    "APH":     {"min_rate": 8.4,  "max_rate": 16.0},  # 5Y +50/+110% — diversified interconnect compounder (est.)

    # --- W4 CLOUD ---
    "MSFT":    {"min_rate": 8.4,  "max_rate": 16.0},  # 5Y +50/+110% — Azure+OpenAI, durable compounder
    "GOOGL":   {"min_rate": 8.4,  "max_rate": 17.1},  # 5Y +50/+120% — Gemini+TPU+Cloud, cheap
    "AMZN":    {"min_rate": 8.4,  "max_rate": 17.1},  # 5Y +50/+120% — AWS re-acceleration
    "META":    {"min_rate": 7.0,  "max_rate": 16.0},  # 5Y +40/+110% — ad-AI + open models
    "ORCL":    {"min_rate": 7.0,  "max_rate": 17.1},  # 5Y +40/+120% — cloud-capacity surprise winner

    # --- W5 SOFTWARE ---
    "PANW":    {"min_rate": 8.4,  "max_rate": 18.1},  # 5Y +50/+130% — security platform, profitable
    "CRWD":    {"min_rate": 9.9,  "max_rate": 19.1},  # 5Y +60/+140% — cybersecurity platform, profitable
    "NOW":     {"min_rate": 8.4,  "max_rate": 18.1},  # 5Y +50/+130% — workflow AI compounder (est.)
    "PLTR":    {"min_rate": 7.0,  "max_rate": 20.1},  # 5Y +40/+150% — AI ops leader, very expensive
    "SNOW":    {"min_rate": 7.0,  "max_rate": 20.1},  # 5Y +40/+150% — data-cloud + Cortex (est.)
    "DDOG":    {"min_rate": 7.0,  "max_rate": 18.1},  # 5Y +40/+130% — AI observability, growth re-accel

    # --- W6 SPECULATIVE ---
    "AXON":    {"min_rate": 9.9,  "max_rate": 21.1},  # 5Y +60/+160% — defense/policing AI SaaS moat
    "TMDX":    {"min_rate": 8.4,  "max_rate": 22.9},  # 5Y +50/+180% — transplant monopoly, S-curve
    "IONQ":    {"min_rate": -12.9,"max_rate": 38.0},  # 5Y -50/+400% — quantum leader, pre-profit (binary)
    "RKLB":    {"min_rate": 7.0,  "max_rate": 32.0},  # 5Y +40/+300% — Neutron launch catalyst
    "CRCL":    {"min_rate": -20.0,"max_rate": 35.0},  # 5Y -67/+350% — Circle/USDC stablecoin rails; held windfall, target 0% (binary)
}
