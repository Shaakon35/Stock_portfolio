# =========================================================================
# AI FULL-STACK GROWTH PORTFOLIO — STANDALONE PROPOSAL
# =========================================================================
# Status: PROPOSAL ONLY. Not imported or wired into any notebook/pipeline.
# This is an alternative target restructured by AI value-chain "wave"
# (W1 silicon -> W6 speculative), built to maximize growth across the full
# AI stack rather than by the original sector taxonomy in allocations.py.
#
# Wave weights: W1 23 / W2 18 / W3 18 / W4 15 / W5 18 / W6 8 = 100%
# CHANGED: W1 18 -> 23 and W4 20 -> 15 (net zero) after an exposure review —
#       MSFT/GOOGL were overweight (~5% each) while semis MU/AMD (held via
#       SMHV.SW inside W1) were too thin. Shifting 5% from cloud to silicon
#       lifts the semi book without touching the other waves.
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
    "W1_SILICON":   0.23,  # CHANGED: 0.18 -> 0.23 — lift semis (esp. SMHV.SW: MU/AMD) per exposure review
    "W2_POWER":     0.18,  # Power & energy — youngest "boring" wave, best risk-adjusted
    "W3_DCINFRA":   0.18,  # Data-center infrastructure — cooling, networking, optical, construction
    "W4_CLOUD":     0.15,  # CHANGED: 0.20 -> 0.15 — trim MSFT/GOOGL overweight, fund W1
    "W5_SOFTWARE":  0.18,  # AI software / apps — earliest-innings monetization, highest growth
    "W6_SPEC":      0.08,  # Speculative / second-order — capped lottery + diversifiers
}

# =========================================================================
# SUB-ALLOCATION BASKETS (each sums to 1.0 = 100% of its wave slice)
# =========================================================================

# --- WAVE 1: SILICON / COMPUTE (23%) ---
# MU and AMD are explicit CYCLE picks (0.05 each), adding high-beta semi torque
# without diluting the dca compounders. BESI.AS (0.05) added as the advanced-
# packaging pure-play — the next silicon bottleneck after compute/HBM. All three
# funded by trimming the SMHV.SW ETF (0.40 -> 0.29), where the big-caps already
# sit. SMHV still anchors the sleeve, bringing fab equipment (LRCX/AMAT) and
# broad memory the single picks miss. Eleven names sum to 1.0.
# NB: MU/AMD/BESI.AS + the two Korean memory names (SK Hynix, Samsung) are CYCLE —
# trim near the ~2027-29 peak, not set-and-forget. The memory oligopoly (MU +
# SK Hynix + Samsung) crashes together when the DRAM/HBM cycle turns; sized small
# and deliberately for that reason. Korean names are KRX-listed (buy via IBKR).
W1_SILICON_TARGETS = {
    "SMHV.SW":   0.20,  # CHANGED: 0.29 -> 0.20 — trimmed to fund the two Korean memory
                        # names below. NB: SMHV tracks a US-LISTED semi index, so it
                        # holds ZERO Samsung/SK Hynix — these are genuine new exposure,
                        # not a duplicate. Memory-for-memory swap keeps the sleeve balanced.
    "NVDA":      0.18,  # GPU king — top conviction single
    "AVGO":      0.13,  # CHANGED: 0.14 -> 0.13
    "ASML":      0.11,  # CHANGED: 0.12 -> 0.11 — EUV lithography monopoly
    "MRVL":      0.09,  # CHANGED: 0.10 -> 0.09 — Custom AI ASICs / optical DSPs
    "TSM":       0.05,  # CHANGED: 0.06 -> 0.05 — foundry monopoly (also held inside the ETF)
    "MU":        0.05,  # memory/HBM cycle bet — tightest link in the AI supply chain
    "AMD":       0.05,  # #2 GPU cycle bet — high-beta semi torque
    "BESI.AS":   0.05,  # advanced packaging (hybrid bonding for HBM4+/chiplets) — the
                        # western CoWoS pure-play. EUR-listed (Amsterdam). CYCLE.
    "000660.KS": 0.05,  # NEW: SK Hynix — HBM LEADER (Nvidia's #1 HBM supplier), the purest
                        # HBM bet. KRX-listed (KRW), buy via Interactive Brokers. CYCLE / Mid.
    "005930.KS": 0.04,  # NEW: Samsung Electronics — memory + foundry, more diluted
                        # (conglomerate). KRX-listed (KRW). CYCLE / Mid. Sized below SK Hynix.
}

# --- WAVE 2: POWER & ENERGY (18%) ---
# CHANGED: deepened the generation -> transmission rotation. Removed late-cycle
# POWL & VST (both +400%, sell-at-peak names that give back post-peak) and
# trimmed CEG. Funded early-cycle TRANSMISSION: bumped ETN/PWR and added HUBB
# (transformers) + ABBN.SW (HVDC / EU grid). GEV kept at 0.23 despite being
# "Late" — it's DCA (grid supercycle to 2035+), survives the cycle, rides the
# next leg. This tracks the bottleneck migration: "make electrons" (generation,
# now late) -> "move electrons" (transmission, now early). Eight names sum to 1.0.
# NB: ETN/HUBB/ABBN.SW are DCA (quality compounders); PWR is CYCLE (high-beta).
#
# REMOVED (kept commented for easy re-add): late-cycle names trimmed out of the
# rotation. To restore, uncomment here AND in STRATEGY below, then renormalize
# the basket back to 1.0.
#   "POWL":  0.07,   # switchgear — LATE-cycle, already +389% (CYCLE)
#   "VST":   0.07,   # merchant power — LATE-cycle, already ran (CYCLE)
W2_POWER_TARGETS = {
    "GEV":     0.23,  # grid/gas turbines, HOLD FOREVER (Late but DCA — keep)
    "CCJ":     0.17,  # uranium leader, HOLD FOREVER
    "CEG":     0.12,  # CHANGED: 0.20 -> 0.12 — trimmed late-cycle nuclear utility
    "ETN":     0.12,  # CHANGED: 0.10 -> 0.12 — transmission/electrification, DCA
    "HUBB":    0.10,  # NEW: transformers / grid gear — 2-4yr lead-times, early-cycle, DCA
    "PWR":     0.09,  # CHANGED: 0.07 -> 0.09 — builds transmission lines, CYCLE
    "OKLO":    0.09,  # SMR catalyst (binary)
    "ABBN.SW": 0.08,  # NEW: HVDC / transformers (EU) — long-distance grid bottleneck,
                      # adds CHF/EU diversification. DCA.
}

# --- WAVE 3: DC INFRASTRUCTURE (18%) ---
# CHANGED: removed late-cycle FIX (DC construction, +291% — sell-at-peak) and
# replaced it one-for-one with NVT (nVent — electrical enclosures + liquid
# cooling), an early-cycle DCA name covering both power-management and cooling.
#
# REMOVED (kept commented for easy re-add). To restore, uncomment here AND in
# STRATEGY below, then renormalize the basket back to 1.0.
#   "FIX":   0.1667,  # DC construction / HVAC — LATE-cycle, already +291% (CYCLE)
W3_DCINFRA_TARGETS = {
    "VRT":   0.2222,  # Liquid cooling leader
    "ANET":  0.2222,  # Arista — data-center networking
    "CRDO":  0.2222,  # Optical/copper interconnect
    "COHR":  0.1667,  # Coherent — optical components / transceivers
    "NVT":   0.1667,  # NEW: nVent — DC enclosures + liquid cooling, early-cycle, DCA
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
    "MU":        "cycle",   # Memory/HBM — violently cyclical; buy dips, trim at peak
    "AMD":       "cycle",   # #2 GPU — high-beta; trim near cycle peak, don't blind-DCA
    "BESI.AS":   "cycle",   # Advanced packaging — single-tech bet (hybrid bonding); trim at peak
    "000660.KS": "cycle",   # SK Hynix — HBM leader; same memory cycle as MU, trim at peak
    "005930.KS": "cycle",   # Samsung — memory+foundry; same memory cycle, trim at peak

    # --- W2 POWER ---
    "GEV":     "dca",       # Grid supercycle — hold forever
    "CCJ":     "dca",       # Uranium structural deficit — hold forever
    "ETN":     "dca",       # Transmission/electrification — quality compounder, hold forever
    "HUBB":    "dca",       # Transformers/grid gear — 2-4yr lead-times, quality, hold forever
    "ABBN.SW": "dca",       # HVDC/transformers (EU) — long-distance grid, hold forever
    "CEG":     "cycle",     # Nuclear utility — power-price sensitive
    "PWR":     "cycle",     # Transmission contractor — high-beta backlog play, trim at peak
    "OKLO":    "catalyst",  # Pre-revenue SMR — sell on NRC approval, never avg down
    # REMOVED from baskets (kept commented for easy re-add — see W2_POWER_TARGETS):
    #   "VST":     "cycle",     # Power merchant — sell at peak (late-cycle, removed)
    #   "POWL":    "cycle",     # +2657% — late-cycle switchgear (removed)

    # --- W3 DC-INFRA (mostly rides the capex cycle) ---
    "VRT":     "cycle",     # Cooling — sell when DC capex peaks ~2028-29
    "ANET":    "dca",       # Networking monopoly — 38% margin, $4.4B FCF, software moat
    "CRDO":    "cycle",     # +2127% hypergrowth — sell when growth <30%
    "COHR":    "cycle",     # Optical — already ran, cyclical
    "NVT":     "dca",       # nVent — DC enclosures + liquid cooling, early-cycle, hold forever
    # REMOVED from basket (kept commented for easy re-add — see W3_DCINFRA_TARGETS):
    #   "FIX":     "cycle",     # +2206% — late-cycle DC construction (removed)

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


# =========================================================================
# WATCHLIST — NOT HELD. Names to check from time to time.
# =========================================================================
# These are candidates / monitors, deliberately OUTSIDE the wave baskets so
# they do not affect any weight. Each carries a tentative strategy tag using
# the same vocabulary as STRATEGY, plus one extra:
#
#   "lottery" — speculative micro-bet with binary/blow-up risk. Like
#               "catalyst" but with NO clean single event to sell into —
#               pure asymmetric punt. Size tiny or skip; never average down.
#
# Most are already captured indirectly via the SMHV.SW ETF in W1 — the tag
# notes that so you don't double-pay. "verify_allocations" intentionally
# ignores this dict; it's a notebook for the eye, not part of the portfolio.
# =========================================================================

WATCHLIST = {
    # --- Memory / storage (HBM + NAND/HDD) — the deepest-cyclical corner ---
    # NB: MU promoted to a held W1 CYCLE pick (see W1_SILICON_TARGETS) — removed here.
    "SNDK": {
        "strategy": "cycle",
        "area":     "Memory / NAND (SanDisk)",
        "note":     "SKIP/late — +251% rev is the NAND cycle at its PEAK, trading "
                    "near 52w high. Deep-cyclical commodity. Buying here = buying the "
                    "top. Covered indirectly anyway.",
    },
    "WDC": {
        "strategy": "cycle",
        "area":     "Storage / HDD (Western Digital)",
        "note":     "SKIP — +46% rev / 55% net flatters a cycle top. Commodity HDD/"
                    "NAND, near 52w high. Classic late-cycle trap.",
    },
    "STX": {
        "strategy": "cycle",
        "area":     "Storage / HDD (Seagate)",
        "note":     "SKIP — same as WDC: deep-cyclical HDD at cycle peak near highs.",
    },

    # --- Compute / IP / connectivity ---
    "ARM": {
        "strategy": "cycle",
        "area":     "Chip IP / architecture",
        "note":     "Only name that fills a UNIQUE gap (royalty IP, ~95% gross). Elite "
                    "moat BUT 129x fwd P/E / 86x sales — pricier than PLTR. Dip-only, "
                    "tiny size; NEVER DCA at this multiple. Treat as CYCLE/conviction.",
    },
    # NB: AMD promoted to a held W1 CYCLE pick (see W1_SILICON_TARGETS) — removed here.
    "QCOM": {
        "strategy": "cycle",
        "area":     "Mobile / edge-AI chips",
        "note":     "SKIP — cheap (20x P/E, $9.6B FCF) but rev -4%: Apple designing it "
                    "out. 'Cheap for a reason' value trap, not a growth thesis.",
    },
    "ADI": {
        "strategy": "dca",
        "area":     "Analog / industrial chips",
        "note":     "Highest-QUALITY new name (37% rev, 26% net, $3.9B FCF, 28x). "
                    "Would be DCA-grade — but only loosely AI-thesis (industrial). "
                    "Consider only if widening beyond pure AI-infra.",
    },

    # --- Fab equipment ('picks of the picks') — all inside SMHV.SW ---
    "KLAC": {
        "strategy": "dca",
        "area":     "Fab inspection equipment",
        "note":     "High quality (36% net, $2.9B FCF). DCA-grade oligopoly, but "
                    "already held via SMHV.SW (equipment ~11% of ETF). Redundant direct.",
    },
    "LRCX": {
        "strategy": "dca",
        "area":     "Fab etch/deposition equipment",
        "note":     "Quality (31% net, $4.4B FCF). Same as KLAC — already inside the "
                    "ETF; only add direct for concentrated equipment conviction.",
    },
    "AMAT": {
        "strategy": "dca",
        "area":     "Fab equipment (broadest)",
        "note":     "Quality (29% net). Inside SMHV.SW already. Redundant direct.",
    },

    # --- Legacy / off-thesis large caps ---
    "AAPL": {
        "strategy": "dca",
        "area":     "Consumer hardware / services",
        "note":     "DCA-grade ($101B FCF!) but it's a CONSUMER play, not AI-infra. "
                    "Belongs in a core portfolio, not this AI book. Off-thesis.",
    },
    "CSCO": {
        "strategy": "dca",
        "area":     "Legacy networking",
        "note":     "SKIP — you already hold ANET (faster, higher-margin competitor). "
                    "Redundant and slower-growth.",
    },
    "TXN": {
        "strategy": "cycle",
        "area":     "Analog / industrial chips",
        "note":     "SKIP — analog/industrial, barely an AI play. Inside ETF anyway.",
    },
    "INTC": {
        "strategy": "lottery",
        "area":     "Legacy CPU / foundry turnaround",
        "note":     "AVOID/lottery — UNPROFITABLE (-6% net, -$8.3B FCF, 76x P/E, 7% "
                    "rev). Foundry turnaround is a binary gamble, not an investment.",
    },

    # --- Korea memory (HBM leaders) — access friction ---
    "005930.KS": {
        "strategy": "cycle",
        "area":     "Memory / diversified (Samsung)",
        "note":     "HBM + broad semi at 6x P/E — cheap. But Korea-listed (FX/access "
                    "friction on EU brokers). Better captured via a broad ex-US semi "
                    "ETF than bought direct.",
    },
    "000660.KS": {
        "strategy": "cycle",
        "area":     "Memory / HBM leader (SK hynix)",
        "note":     "Purest HBM leader (+198% rev, 57% net, 6x P/E) — but it's the "
                    "memory cycle peaking. Korea-listed access friction. Watch, "
                    "don't chase at the top.",
    },

    # --- Non-semi: consumer / China ---
    "1810.HK": {
        "strategy": "cycle",
        "area":     "Consumer electronics / EV (Xiaomi)",
        "note":     "OFF-THESIS — cheap (14x P/E) but rev -11% (shrinking). It's a "
                    "China consumer/EV turnaround bet, not AI value-chain. + China "
                    "geopolitical risk, HK/OTC access. Keep in a SEPARATE sleeve if at all.",
    },

    # --- EDA / chip-design software (a structural gap nothing else covers) ---
    "CDNS": {
        "strategy": "dca",
        "area":     "Chip-design software (EDA)",
        "note":     "DCA-grade. The tools every chip is designed with — software "
                    "moat NOT in your book or the ETF. 86% gross, 21% net, $1.5B FCF. "
                    "Cadence/Synopsys are the EDA duopoly; ~41x P/E so not cheap.",
    },
    "SNPS": {
        "strategy": "dca",
        "area":     "Chip-design software (EDA)",
        "note":     "DCA-grade. Other half of the EDA duopoly. 83% gross, 42% rev, "
                    "$3.5B FCF, ~26x fwd P/E. NB it absorbed ANSYS (ANSS) — the "
                    "ANSS ticker is gone, exposure now lives here.",
    },
    "TER": {
        "strategy": "cycle",
        "area":     "Chip test equipment",
        "note":     "Complements the LRCX/AMAT equipment angle. 87% rev is the test "
                    "cycle recovering (cyclical), 23% net. Buy on down-cycles, not at "
                    "the peak; not in the ETF top holdings.",
    },

    # --- AI-native cloud / GPU rental ---
    "CRWV": {
        "strategy": "catalyst",
        "area":     "AI-native cloud / GPU rental (CoreWeave)",
        "note":     "Pure-play AI compute rental — directly on-thesis but HIGH-BETA "
                    "binary: 112% rev yet -26% net and -$8.6B FCF (massive debt-funded "
                    "GPU capex). Sell/scale on execution catalysts; size tiny, never "
                    "average down. Borderline lottery.",
    },

    # --- Defense / crypto-adjacent industrials ---
    "KTOS": {
        "strategy": "cycle",
        "area":     "Industrial / Defense",
        "note":     "Autonomous military drones. CHANGED: KTOS dropped out of XAIX.DE "
                    "top holdings (latest look-through), so the prior 'already held "
                    "indirectly' overlap no longer applies. Now a clean candidate — "
                    "consider for INDUSTRIAL if adding defense exposure. NB thin FCF "
                    "(2% net) -> momentum-like, treat as CYCLE.",
    },
    "IREN": {
        "strategy": "lottery",
        "area":     "Industrial (AI compute + Bitcoin mining)",
        "note":     "SMALL/SKIP — crypto-correlated beta is new uncorrelated risk, "
                    "not diversification. Negative FCF (-$2.3B). Lottery, not cycle.",
    },
    "CIFR": {
        "strategy": "lottery",
        "area":     "Industrial (Bitcoin mining pivoting to AI)",
        "note":     "SKIP — rev -29%, negative FCF (-$2.9B), crypto-dependent, weaker "
                    "than every industrial incumbent already held. Pure lottery.",
    },

    # --- From the SECTOR portfolio satellites — net-new AI-thesis checks ---
    # Cross-referenced against held STRATEGY: names already in the wave book
    # (CCJ, GEV, OKLO, IONQ, CRWD, PANW, POWL, VRT, FIX, RKLB, CRDO, TMDX,
    # AXON) are deliberately omitted here to avoid double-listing.

    # Silicon (W1) candidates — real chip companies
    "LSCC": {
        "strategy": "cycle",
        "area":     "Silicon / low-power FPGAs (Lattice)",
        "note":     "CLEANEST add of the batch — a real chip company, not a story "
                    "stock. Low-power FPGAs for AI-edge. Cyclical: buy dips, trim "
                    "into the next semi peak. Not in SMHV.SW top holdings.",
    },

    # Power / infra (datacenter electricity + hosting)
    "APLD": {
        "strategy": "cycle",
        "area":     "AI datacenter hosting / HPC leases (Applied Digital)",
        "note":     "Direct AI compute-buildout play (CoreWeave-style HPC leases). "
                    "Volatile, capex-heavy — buy weakness, trim on hype. On-thesis "
                    "for the power/infra leg.",
    },
    "BWXT": {
        "strategy": "dca",
        "area":     "Power / nuclear components (naval reactors + SMR parts)",
        "note":     "The PROFITABLE nuclear name — naval reactors + SMR components, "
                    "real earnings. Powers the AI-datacenter electricity thesis and "
                    "is DCA-able, unlike the pre-revenue SMR crowd.",
    },
    "LEU": {
        "strategy": "cycle",
        "area":     "Nuclear fuel / HALEU enrichment (Centrus)",
        "note":     "Only US HALEU enricher; real revenue. Fits 'AI needs power' via "
                    "the fuel cycle. Cyclical commodity-linked — buy down-cycles, not "
                    "at highs.",
    },
    "SMR": {
        "strategy": "catalyst",
        "area":     "Nuclear / small modular reactors (NuScale)",
        "note":     "Pre-revenue. Binary on first commercial reactor. One-and-done "
                    "catalyst bet — size tiny, NEVER average down.",
    },
    "SRUUF": {
        "strategy": "cycle",
        "area":     "Uranium commodity trust (Sprott Physical Uranium)",
        "note":     "OFF-STRATEGY mechanically — a COMMODITY trust tracking U3O8 "
                    "price, not an equity. Proxy for the nuclear-power thesis but "
                    "behaves like the metal, not a company. Separate sleeve if at all.",
    },

    # Quantum pile-on — one catalyst ticket (IONQ) is already held
    "RGTI": {
        "strategy": "lottery",
        "area":     "Quantum computing (Rigetti)",
        "note":     "Pre-revenue quantum. You already hold IONQ as the quantum "
                    "catalyst ticket; adding more just smears one lottery bet across "
                    "many. If you want ONE more, this is the pick — size tiny.",
    },
    "QBTS": {
        "strategy": "lottery",
        "area":     "Quantum computing (D-Wave)",
        "note":     "Pre-revenue quantum (annealing). Same logic as RGTI — redundant "
                    "with IONQ. Lottery only.",
    },
    "QUBT": {
        "strategy": "lottery",
        "area":     "Quantum computing (Quantum Computing Inc.)",
        "note":     "Micro-cap pre-revenue quantum. Pure lottery; max noise, no edge "
                    "over the IONQ position. Skip unless punting.",
    },
    "QNT": {
        "strategy": "lottery",
        "area":     "Quantum computing",
        "note":     "Speculative quantum name. Redundant with the IONQ quantum "
                    "ticket. Lottery only — tiny or skip.",
    },
    "XNDU": {
        "strategy": "lottery",
        "area":     "Quantum computing (Xanadu)",
        "note":     "Pre-revenue photonic quantum. Lottery; same smearing problem as "
                    "the rest of the quantum pile. Skip unless punting.",
    },
    "INFQ": {
        "strategy": "lottery",
        "area":     "Quantum computing",
        "note":     "Speculative quantum name. Redundant with IONQ. Lottery only.",
    },
    "HQ": {
        "strategy": "lottery",
        "area":     "Quantum computing",
        "note":     "Speculative quantum name. Redundant with IONQ. Lottery only.",
    },

    # Off-thesis — tracked for completeness, NOT AI value-chain
    "ENVX": {
        "strategy": "lottery",
        "area":     "Battery tech (Enovix)",
        "note":     "OFF-THESIS — silicon-anode batteries, not the AI value chain. "
                    "Pre-profit. Belongs in a separate energy/tech sleeve.",
    },
    "VKTX": {
        "strategy": "lottery",
        "area":     "Biotech / GLP-1 (Viking Therapeutics)",
        "note":     "OFF-THESIS — GLP-1 obesity biotech, ZERO AI linkage. Pure sector "
                    "drift; binary on trial data. Does not belong in this AI book.",
    },

    # --- Off-thesis space / robotics moonshots (RKLB already owns the space slot) ---
    "LUNR": {
        "strategy": "lottery",
        "area":     "Space / lunar landers (Intuitive Machines)",
        "note":     "OFF-THESIS — NASA commercial lunar landers. RKLB already owns the "
                    "space slot and is higher-quality; LUNR is lower-quality AND higher-"
                    "risk (-70%+ binary). Not AI value-chain. Lottery only.",
    },
    "SERV": {
        "strategy": "lottery",
        "area":     "Robotics / sidewalk delivery (Serve Robotics)",
        "note":     "OFF-THESIS — sidewalk delivery robots, ~$600M micro-cap, deeply "
                    "unprofitable (-$2.05 EPS). 'Nvidia-backed' = tiny passive stake, "
                    "not a deal. Hype-driven binary. Lottery; size tiny or skip.",
    },
    "ACHR": {
        "strategy": "lottery",
        "area":     "eVTOL air taxi (Archer Aviation)",
        "note":     "OFF-THESIS — eVTOL air taxi, ->$0 risk. Triple-gated: FAA cert + "
                    "manufacturing + demand. Not AI value-chain. Pure lottery.",
    },

    # --- AI cluster integration (W1/W3 seam) ---
    "PENG": {
        "strategy": "cycle",
        "area":     "AI cluster integration / advanced memory (Penguin Solutions)",
        "note":     "ON-THESIS — ex-SGH; builds HPC/AI clusters + advanced memory "
                    "integration, the 'who assembles the GPU clusters' layer the book "
                    "is thin on (W1/W3 seam). PROFITABLE, not a story stock, but "
                    "smaller/less-proven than held names and demand is cyclical — buy "
                    "dips, trim at peak. Watchlist-first.",
    },
}


def watchlist_by_strategy(mode):
    """Return watchlist tickers tentatively tagged with a given mode
    ('dca' | 'cycle' | 'catalyst' | 'lottery')."""
    return sorted(t for t, d in WATCHLIST.items() if d["strategy"] == mode)


if __name__ == "__main__":
    verify_allocations()
    print("verify_allocations(): PASS")
    print("\nHELD — by strategy:")
    for mode in ("dca", "cycle", "catalyst"):
        names = tickers_by_strategy(mode)
        print(f"  {mode:9s} ({len(names):2d}): {', '.join(names)}")
    print("\nWATCHLIST (not held) — by tentative strategy:")
    for mode in ("dca", "cycle", "catalyst", "lottery"):
        names = watchlist_by_strategy(mode)
        if names:
            print(f"  {mode:9s} ({len(names):2d}): {', '.join(names)}")
