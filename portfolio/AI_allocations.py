# =========================================================================
# AI FULL-STACK GROWTH PORTFOLIO — STANDALONE PROPOSAL
# =========================================================================
# Status: PROPOSAL ONLY. Not imported or wired into any notebook/pipeline.
# This is an alternative target restructured by AI value-chain "wave"
# (W1 silicon -> W6 speculative), built to maximize growth across the full
# AI stack rather than by the original sector taxonomy in allocations.py.
#
# Wave weights: W1 18 / W2 18 / W3 18 / W4 20 / W5 18 / W6 8 = 100%
# NOTE: the requested 18/18/16/20/18/8 summed to 98%; the spare 2% was added
#       to W3 (DC-Infra, high-growth/moderate-risk) to reach 100% without
#       inflating the speculative sleeve.
#
# To evaluate later, mirror the structure of allocations.py (theme colors,
# forecasts, notebook wiring). Intentionally NOT done yet.
# =========================================================================

MONTHLY_DEPOSIT = 1000.0  # Monthly fresh cash allocation in Euros
DEGIRO_FEE = 3.00         # Flat transaction fee

# =========================================================================
# WAVE-LEVEL TARGET WEIGHTS (100% total)
# =========================================================================

TARGET_WEIGHTS = {
    "W1_SILICON":   0.18,  # Silicon / compute — picks-and-shovels (trimmed vs prior overweight)
    "W2_POWER":     0.18,  # Power & energy — youngest "boring" wave, best risk-adjusted
    "W3_DCINFRA":   0.18,  # Data-center infrastructure — cooling, networking, optical, construction
    "W4_CLOUD":     0.20,  # Hyperscaler cloud — durable mega-cap compounders
    "W5_SOFTWARE":  0.18,  # AI software / apps — earliest-innings monetization, highest growth
    "W6_SPEC":      0.08,  # Speculative / second-order — capped lottery + diversifiers
}

# =========================================================================
# SUB-ALLOCATION BASKETS (each sums to 1.0 = 100% of its wave slice)
# =========================================================================

# --- WAVE 1: SILICON / COMPUTE (18%) ---
W1_SILICON_TARGETS = {
    "SMHV.SW": 0.2778,  # Broad semiconductor ETF — one-line diversified silicon core
    "NVDA":    0.2222,  # GPU king
    "AVGO":    0.1667,  # Custom AI silicon / networking ASICs
    "ASML":    0.1667,  # EUV lithography monopoly
    "TSM":     0.1666,  # Foundry monopoly
}

# --- WAVE 2: POWER & ENERGY (18%) ---
W2_POWER_TARGETS = {
    "GEV":   0.25,    # Grid/gas turbines, HOLD FOREVER
    "CEG":   0.2222,  # Constellation — nuclear utility powering data centers
    "CCJ":   0.1944,  # Uranium leader, HOLD FOREVER
    "POWL":  0.1111,  # Electrical switchgear
    "OKLO":  0.1111,  # SMR catalyst (binary)
    "VST":   0.1112,  # Vistra — power + data-center energy
}

# --- WAVE 3: DC INFRASTRUCTURE (18%) ---
W3_DCINFRA_TARGETS = {
    "VRT":   0.2222,  # Liquid cooling leader
    "ANET":  0.2222,  # Arista — data-center networking
    "CRDO":  0.2222,  # Optical/copper interconnect
    "FIX":   0.1667,  # DC construction / HVAC
    "COHR":  0.1667,  # Coherent — optical components / transceivers
}

# --- WAVE 4: HYPERSCALER CLOUD (20%) ---
W4_CLOUD_TARGETS = {
    "MSFT":  0.25,  # Azure + OpenAI
    "GOOGL": 0.25,  # Gemini + TPU + Cloud
    "AMZN":  0.20,  # AWS
    "META":  0.15,  # Open models + ad-AI
    "ORCL":  0.15,  # Cloud-capacity winner
}

# --- WAVE 5: AI SOFTWARE / APPS (18%) ---
# CHANGED: removed SNOW and NOW — flat/negative 5Y, weak risk-adjusted odds
# (SNOW unprofitable bubble-hangover; NOW actively crashing -56% off 2025 high).
# Remaining proven platform compounders renormalized to sum to 1.0.
W5_SOFTWARE_TARGETS = {
    "PLTR":  0.3077,  # AI ops / defense platform
    "CRWD":  0.3077,  # AI cybersecurity
    "PANW":  0.2308,  # Security platform
    "DDOG":  0.1538,  # AI observability
}

# --- WAVE 6: SPECULATIVE / SECOND-ORDER (8%) ---
# CHANGED: removed ENVX — -47% 5Y, -81% off ATH, ~50% odds toward $0/dilution.
# Remaining names renormalized to sum to 1.0.
W6_SPEC_TARGETS = {
    "AXON":  0.3333,  # Defense/policing AI (profitable anchor)
    "TMDX":  0.2667,  # MedTech non-AI diversifier
    "IONQ":  0.2000,  # Quantum — revenue leader only
    "RKLB":  0.2000,  # Space / autonomy
}

# =========================================================================
# VALIDATION
# =========================================================================

def verify_allocations():
    """Assert wave weights total 100% and each basket sums to 1.0."""
    assert abs(sum(TARGET_WEIGHTS.values()) - 1.0) < 1e-9, "Wave weights don't sum to 100%"
    for name, basket in [
        ("W1_SILICON", W1_SILICON_TARGETS),
        ("W2_POWER", W2_POWER_TARGETS),
        ("W3_DCINFRA", W3_DCINFRA_TARGETS),
        ("W4_CLOUD", W4_CLOUD_TARGETS),
        ("W5_SOFTWARE", W5_SOFTWARE_TARGETS),
        ("W6_SPEC", W6_SPEC_TARGETS),
    ]:
        assert abs(sum(basket.values()) - 1.0) < 1e-9, f"{name} basket doesn't sum to 100%"


if __name__ == "__main__":
    verify_allocations()
    print("verify_allocations(): PASS")
