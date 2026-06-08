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
}
