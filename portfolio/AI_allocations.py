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
# CHANGED: ETF sized up to a real diversified anchor (40% of sleeve) so it earns
# its place — SMHV brings memory (MU ~14%), AMD (~12%), and fab equipment
# (LRCX/AMAT ~11%) that the single-stock picks miss entirely. Direct singles
# trimmed to avoid double-paying on names already inside the ETF (esp. TSM).
# Six names renormalized to sum to 1.0.
W1_SILICON_TARGETS = {
    "SMHV.SW": 0.40,  # Diversified semi core — adds memory (MU), AMD, fab equipment
    "NVDA":    0.18,  # GPU king — top conviction single
    "AVGO":    0.14,  # Custom AI silicon / networking ASICs
    "ASML":    0.12,  # EUV lithography monopoly
    "MRVL":    0.10,  # Custom AI ASICs / optical DSPs
    "TSM":     0.06,  # Foundry monopoly (also held inside the ETF)
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
# CHANGED: re-added SNOW and NOW. Both fell on multiple-compression, not broken
# businesses — SNOW (16.6x sales, +$1.7B FCF, Cortex AI) is a worked-off bubble
# hangover; NOW (fwd P/E ~21, +13% GAAP, +$5.1B FCF, Now Assist) is a profitable
# compounder repriced in 2025. Both are AI-native and mean-reversion candidates.
# Six names renormalized to sum to 1.0; weighting reflects valuation risk —
# PANW/CRWD/NOW profitable anchors, PLTR capped (62x sales), DDOG cyclical.
W5_SOFTWARE_TARGETS = {
    "PANW":  0.20,  # Security platform — biggest, cheapest, steadiest (top pick)
    "CRWD":  0.18,  # AI cybersecurity — highest-quality platform
    "NOW":   0.18,  # Workflow AI (Now Assist) — profitable, cheap re-rating play
    "PLTR":  0.16,  # AI ops / defense platform — best growth, capped on valuation
    "SNOW":  0.14,  # Data-cloud + Cortex AI — healed bubble hangover
    "DDOG":  0.14,  # AI observability — purest AI-data, consumption-cyclical
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
# STRATEGY CLASSIFICATION — how to OPERATE each holding
# =========================================================================
# Three operating modes. The key difference is what a price DROP means and
# whether you are allowed to add more (average down) when it falls.
#
#   "dca"      — DCA / hold forever. Profitable, survivable businesses.
#                A drop is a DISCOUNT, not a warning.
#                BUY : every month on autopilot, regardless of price.
#                SELL: never (only to rebalance). Averaging down is SAFE.
#
#   "cycle"    — Buy-low / sell-high. Real, profitable businesses riding a
#                multi-year AI-capex wave that will eventually crest.
#                A drop is a DISCOUNT on a healthy cyclical.
#                BUY : on dips, accumulate (averaging down is OK).
#                SELL: gradually, near the CYCLE PEAK (~2027-2029) — when
#                      growth decelerates / valuation gets stretched / the
#                      capex wave rolls over. Take profits; do not "hold
#                      forever". Several here have already run 400-2600%.
#
#   "catalyst" — Binary event bet. Pre-revenue / unproven; can go to ZERO.
#                A drop may be the market correctly pricing in FAILURE.
#                BUY : ONCE, a small fixed size. DO NOT AVERAGE DOWN — adding
#                      to a falling catalyst name is throwing money into a hole.
#                SELL: at the specific EVENT (approval, signed contract,
#                      milestone), win or lose. Then walk away.
#
# Rule of thumb on a 40% drop:
#   dca/cycle -> buy more (discount on a real business).
#   catalyst  -> do nothing (the thesis may be breaking).
# =========================================================================

STRATEGY = {
    # --- W1 SILICON ---
    "SMHV.SW": "dca",       # Diversified ETF — buy monthly, never sell
    "NVDA":    "dca",       # Profitable mega-cap compounder
    "AVGO":    "dca",       # Profitable, dividend, ~$27B FCF
    "MRVL":    "dca",       # Profitable ASIC play, reasonable multiple
    "ASML":    "dca",       # EUV monopoly — secular grower; each cycle troughs higher
    "TSM":     "dca",       # Foundry monopoly — secular grower, sane valuation (~20x)

    # --- W2 POWER ---
    "GEV":     "dca",       # Grid supercycle — hold forever
    "CCJ":     "dca",       # Uranium structural deficit — hold forever
    "CEG":     "cycle",     # Nuclear utility — power-price sensitive
    "VST":     "cycle",     # Power merchant — sell at peak
    "POWL":    "cycle",     # +2657% — late-cycle switchgear, has a price target
    "OKLO":    "catalyst",  # Pre-revenue SMR — sell on NRC approval, never avg down

    # --- W3 DC-INFRA (mostly rides the capex cycle) ---
    "VRT":     "cycle",     # Cooling — sell when DC capex peaks ~2028-29
    "ANET":    "dca",       # Networking monopoly — 38% margin, $4.4B FCF, software moat
    "CRDO":    "cycle",     # +2127% hypergrowth — sell when growth <30%
    "COHR":    "cycle",     # Optical — already ran, cyclical
    "FIX":     "cycle",     # +2206% — late-cycle DC construction, sell at peak

    # --- W4 CLOUD (purest DCA wave) ---
    "MSFT":    "dca",       # Hold forever compounder
    "GOOGL":   "dca",       # Hold forever compounder
    "AMZN":    "dca",       # Hold forever
    "META":    "dca",       # Hold forever
    "ORCL":    "dca",       # Cloud-capacity compounder

    # --- W5 SOFTWARE ---
    "PANW":    "dca",       # Profitable platform — hold forever
    "CRWD":    "dca",       # Profitable platform, ~$1.9B FCF — hold forever
    "NOW":     "dca",       # Profitable (+13% GAAP, $5.1B FCF) — hold forever
    "SNOW":    "dca",       # FCF-positive, healed bubble hangover
    "PLTR":    "cycle",     # Best business but 62x sales — trim/add, not blind DCA
    "DDOG":    "cycle",     # Consumption model — buy dips, trim momentum spikes

    # --- W6 SPECULATIVE ---
    "AXON":    "dca",       # Public-safety monopoly — 59% gross margin, sticky SaaS;
                            # thin net/FCF is reinvestment by choice, not weak economics.
                            # Volatile but end-market doesn't cycle -> hold through dips.
    "TMDX":    "cycle",     # MedTech growth — momentum-sensitive
    "IONQ":    "catalyst",  # Quantum binary — size once, event-driven, no avg down
    "RKLB":    "catalyst",  # Space — size once, milestone-driven, no avg down
}

# =========================================================================
# VALIDATION
# =========================================================================

ALL_BASKETS = [
    ("W1_SILICON", W1_SILICON_TARGETS),
    ("W2_POWER", W2_POWER_TARGETS),
    ("W3_DCINFRA", W3_DCINFRA_TARGETS),
    ("W4_CLOUD", W4_CLOUD_TARGETS),
    ("W5_SOFTWARE", W5_SOFTWARE_TARGETS),
    ("W6_SPEC", W6_SPEC_TARGETS),
]


def verify_allocations():
    """Assert wave weights total 100%, each basket sums to 1.0, and every
    holding has a valid strategy classification."""
    assert abs(sum(TARGET_WEIGHTS.values()) - 1.0) < 1e-9, "Wave weights don't sum to 100%"
    valid_modes = {"dca", "cycle", "catalyst"}
    all_tickers = set()
    for name, basket in ALL_BASKETS:
        assert abs(sum(basket.values()) - 1.0) < 1e-9, f"{name} basket doesn't sum to 100%"
        all_tickers.update(basket.keys())

    # Every holding must be classified, and STRATEGY must not carry stragglers.
    missing = all_tickers - set(STRATEGY)
    assert not missing, f"Holdings missing a STRATEGY: {sorted(missing)}"
    extra = set(STRATEGY) - all_tickers
    assert not extra, f"STRATEGY has tickers not in any basket: {sorted(extra)}"
    bad = {t: m for t, m in STRATEGY.items() if m not in valid_modes}
    assert not bad, f"Invalid strategy modes: {bad}"


def tickers_by_strategy(mode):
    """Return the list of tickers operated under a given mode
    ('dca' | 'cycle' | 'catalyst')."""
    return sorted(t for t, m in STRATEGY.items() if m == mode)


if __name__ == "__main__":
    verify_allocations()
    print("verify_allocations(): PASS")
    for mode in ("dca", "cycle", "catalyst"):
        names = tickers_by_strategy(mode)
        print(f"  {mode:9s} ({len(names):2d}): {', '.join(names)}")
