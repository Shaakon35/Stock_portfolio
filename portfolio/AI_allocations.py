# =========================================================================
# AI FULL-STACK GROWTH PORTFOLIO — STANDALONE PROPOSAL
# =========================================================================
# Status: PROPOSAL ONLY. Not imported or wired into any notebook/pipeline.
# This is an alternative target restructured by AI value-chain "wave"
# (W1 silicon -> W6 speculative), built to maximize growth across the full
# AI stack rather than by the original sector taxonomy in allocations.py.
#
# Wave weights: W1 30 / W2 22 / W3 26 / W4 8 / W5 14 / W6 0 = 100% (Option C aggressive)
# CHANGED (Option C): concentrated into the AI-capex BOTTLENECK waves (W1/W3/W2)
#       which carry the best forecast 5Y returns; cut W4 Cloud and W5 Software
#       (lower upside) and zeroed W6 Spec. Prior mix was 23/18/18/15/18/8.
# PRIOR: W1 18 -> 23 and W4 20 -> 15 (net zero) after an exposure review —
#       MSFT/GOOGL were overweight (~5% each) while semis MU/AMD (held via
#       SMHV.SW inside W1) were too thin.
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
    "W1_SILICON":   0.4991,# CHANGED: 0.475 -> 0.4991 — grown so the 4 top-10 W1 singles
                           #          (ONTO/BESI/SIMO + one of CAMT) each clear 2% of book
                           #          while SMHV stays fixed at exactly 37.5%. NB: ONTO and
                           #          CAMT were swapped (2026-06) — ONTO now held, CAMT 0%.
    "W2_POWER":     0.1531,# CHANGED: 0.175 -> 0.1531 — ABBN.SW cut (2.19% book, only name
                           #          analysts call overvalued, slowest-growth ballast). Wave
                           #          shrunk by ABBN's book; the other 7 names keep their book.
    "W3_DCINFRA":   0.2045,# CHANGED: 0.2202 -> 0.2045 — ALAB trimmed (3.07% -> 1.5% book):
                           #          Mid/Late, 118x fwd P/E, the most stretched name held
                           #          (8-Point #6 fail). Freed book rotated to ZS in W5.
    "W4_CLOUD":     0.000, # WAVE ZEROED. Mega-cap cloud is capped by law-of-large-numbers
                           #          AND held passively elsewhere. Names kept at 0% book.
    "W5_SOFTWARE":  0.0833,# CHANGED: 0.0676 -> 0.0833 — absorbs the ALAB trim as new name ZS
                           #          (Zscaler, ~1.57% book): washed-out quality cyber (down
                           #          ~36-59%, PEG 1.23, 30% FCF margin), fills the cyber gap
                           #          left when S was cut. Mirror-image rotation of ALAB.
    "W6_SPEC":      0.060, # CHANGED: 0.03 -> 0.06 — GROWN so the highest-upside names IONQ
                           #          (+175% mid) and RKLB (+171%) get real ~1.5% slots, plus
                           #          TMDX 2.5% (uncorrelated decorrelator). Funded from W5.
}
# OPTION B (BOTTLENECK TILT) + SMHV WINDFALL — restructured 2026-06.
# Context: a 90k CHF SMHV.SW position (899 shares) is now a FIXED 37.5% of the
# 240k book. SMHV's top holdings (MU/AMD/AVGO/INTC/TSM/ASML/NVDA) already give
# full mega-cap silicon exposure, so the six overlapping singles (NVDA, AVGO,
# ASML, TSM, MU, AMD) are REMOVED from the basket — the ETF already provides
# their exposure, so no fresh money and no clutter. The remaining ~62.5% is
# tilted (Option B) toward the waves SMHV does NOT cover — POWER (W2) and
# DC-INFRA (W3) — and away from Cloud/Software.
# SMHV lives INSIDE W1 (~75% of the W1 basket); the surviving singles (ONTO,
# BESI.AS, SIMO, CDNS, SMHN.DE) make up the rest of W1 — all names SMHV's
# US-listed index under-covers or misses.
# Book-level mix: SMHV 37.5 / W1-singles 10 / W2 19 / W3 21 / W4 5 / W5 7.5 / W6 0.
# Wave-level mix: W1 47.5 / W2 19 / W3 21 / W4 5 / W5 7.5 / W6 0 = 100.

# =========================================================================
# SUB-ALLOCATION BASKETS (each sums to 1.0 = 100% of its wave slice)
# =========================================================================

# --- WAVE 1: SILICON / COMPUTE (23%) ---
# SMHV.SW anchors the sleeve (~75% of W1) and already carries the mega-cap silicon
# the ETF's index covers — MU 14.3%, AMD 12.2%, AVGO 8.3%, INTC 8.0%, TSM 7.5%,
# ASML 7.4%, NVDA 7.2%, plus fab equipment (LRCX 5.6% / AMAT 5.1%) and analog
# (TXN). Those names are NOT held as singles — the ETF gives full exposure.
# The surviving SINGLES are the segments SMHV under-covers or misses: back-end
# packaging/inspection (ONTO, BESI.AS, SMHN.DE), NAND controllers (SIMO), and
# EDA design tools (CDNS). They are the fresh-money tilt on top of the ETF core.
# NB: ONTO/BESI.AS/SIMO are CYCLE — trim near the ~2027-29 peak, not set-and-
# forget. BESI's hybrid-bonding ramp is Early (ahead of the DRAM peak); SIMO's
# NAND cycle is a separate, lagged one. Sized small and deliberately. The EUR/
# Frankfurt names (BESI.AS, SMHN.DE) are bought via IBKR.
W1_SILICON_TARGETS = {
    "SMHV.SW":   0.7511,# CHANGED: 0.79 -> 0.7511 — the 90k CHF windfall (899 shares) held
                        # FIXED at exactly 37.5% of book (= 0.7511 of the 49.91% W1 wave).
                        # NB: SMHV tracks a US-LISTED semi index, so it holds ZERO
                        # Samsung/SK Hynix — those are genuine new exposure, not a dup.
    # --- REMOVED 2026-06: NVDA/AVGO/ASML/TSM/MU/AMD dropped from the basket.
    #     They are SMHV's top holdings, so the ETF already gives full mega-cap
    #     exposure and holding them as 0.0 singles only cluttered the table. To
    #     re-add as a fresh-money single, restore a line here + a STRATEGY tag. ---
    # --- SURVIVING SINGLES. CAMT/BESI/SIMO are TOP-10 names. ONTO was TRIMMED
    #     (see below) and its 2% split into CAMT + BESI (now 3% book each). The
    #     three smaller names (SK Hynix/CDNS/SMHN) sit at ~1.47% book. ---
    "CAMT":      0.0000,# CHANGED: 0.0602 -> 0.00 — SWAPPED with ONTO (2026-06). On current
                        # FORWARD data CAMT is the weaker of the two metrology names: slower
                        # (fwd rev +17.7% / EPS +18.1%) and far richer (PEG 2.97 vs ONTO's
                        # 1.17), and it sits Mid/LATE cycle (closer to peak). The earlier
                        # trim favoured CAMT on TRAILING numbers when ONTO was mid-trough;
                        # the forecasts have since flipped. 0% for easy re-add. Its bottleneck
                        # tag (HBM inspection/AOI) is its remaining edge.
    "ONTO":      0.0602,# CHANGED: 0.00 -> 0.0602 — SWAPPED with CAMT (2026-06). The
                        # trough-rebound is now IN the forward numbers: fwd rev +24.1%,
                        # fwd EPS +33.5%, and the cheapest metrology name on PEG (1.17 vs
                        # CAMT 2.97). Mid-cycle (vs CAMT Mid/Late) so more runway. Scores
                        # GROWTH 4.72 vs CAMT 2.89. The redundancy (both see/measure) is
                        # resolved by keeping the better grower; BESI (bonding) stays the
                        # non-redundant, highest-quality leg. ~3.0% of book.
    "BESI.AS":   0.0896,# CHANGED: 0.0601 -> 0.0896 — absorbs the SK Hynix trim (1.47% book)
                        # on top of the earlier ONTO split. BESI is the Early, NON-peak add
                        # candidate in the back-end complex: advanced packaging (hybrid
                        # bonding for HBM4+/chiplets), western CoWoS pure-play, the assembly
                        # step (not inspection), highest quality (63% GM, 33% FCF margin).
                        # Its ramp is still AHEAD while DRAM is at its peak. EUR-listed.
                        # CYCLE / Early. Now ~4.47% of book.
    "SIMO":      0.0401,# TOP-10: Silicon Motion — NAND/SSD controllers. Fills the missing
                        # memory sub-segment. NAND is a SEPARATE, lagged cycle (not DRAM).
                        # Profitable, ~39x. CYCLE / Early-Mid. 2.0% of book.
    "000660.KS": 0.0000,# CHANGED: 0.0295 -> 0.00 — TRIMMED. SK Hynix rode the DRAM/HBM cycle
                        # to a record peak (+~900% / 52wk, MU memory GM ~74% = all-time high):
                        # graded Mid/Late, the cycle-trap zone where a 6-7x fwd P/E is the
                        # WARNING (peak earnings about to mean-revert), not the bargain. Book
                        # redeployed to BESI.AS (Early, ramp ahead). 0% for easy re-add on the
                        # first DRAM down-quarter / margin roll. CYCLE / Mid-Late.
    "CDNS":      0.0295,# Cadence — EDA design-tool duopoly (w/ Synopsys). The chip-DESIGN
                        # layer; not in SMHV. Secular high-margin compounder. ~1.47% book.
    "SMHN.DE":   0.0295,# SUSS MicroTec — advanced-packaging/bonding equipment, SAME HBM4/
                        # CoWoS bottleneck as BESI.AS. Frankfurt-listed (EUR). ~1.47% book.
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
# CHANGED: ABBN.SW CUT entirely (was 0.1250 basket / 2.19% book). It was the only
# holding analysts rated overvalued (-13% to PT), slowest-growth ballast (13% EPS gr,
# net debt). Its book split half -> FN (W3) and half -> NOW (W5). The wave shrank by
# ABBN's book; the 7 survivors were renormalized so their book values are UNCHANGED.
# Kept commented for easy re-add (restore here + in STRATEGY, then renormalize to 1.0).
#   "ABBN.SW": 0.1250,# HVDC / transformers (EU) — long-distance grid, DCA
W2_POWER_TARGETS = {
    "GEV":     0.2338,# grid/gas turbines, HOLD FOREVER (Late but DCA — keep)
    "CCJ":     0.2078,# uranium leader, HOLD FOREVER
    "CEG":     0.0000,# CHANGED: 0.12 -> 0.00 — TRIMMED: below 200d / death cross (tech sell
                      # signal overrides thesis, pt 8). Kept at 0% for easy re-add.
    "ETN":     0.1688,# transmission/electrification, DCA
    "HUBB":    0.1559,# transformers / grid gear — 2-4yr lead-times, early-cycle, DCA
    "PWR":     0.1298,# builds transmission lines, CYCLE
    "OKLO":    0.1039,# SMR catalyst (binary)
}

# --- WAVE 3: DC INFRASTRUCTURE (18%) ---
# CHANGED: removed late-cycle FIX (DC construction, +291% — sell-at-peak) and
# replaced it one-for-one with NVT (nVent — electrical enclosures + liquid
# cooling), an early-cycle DCA name covering both power-management and cooling.
#
# REMOVED (kept commented for easy re-add). To restore, uncomment here AND in
# STRATEGY below, then renormalize the basket back to 1.0.
#   "FIX":   0.1667,  # DC construction / HVAC — LATE-cycle, already +291% (CYCLE)
# Option B (de-concentrate): flattened toward equal weight to lower single-name
# risk across the sleeve.
W3_DCINFRA_TARGETS = {
    "VRT":   0.1611,# CHANGED: 0.1496 -> 0.1611 — renorm (book UNCHANGED) as the ALAB trim
                    # shrank the wave. Liquid cooling leader — CYCLE.
    "ANET":  0.1611,# CHANGED: 0.1496 -> 0.1611 — renorm (book unchanged). Arista — DC
                    # networking monopoly, DCA.
    "CRDO":  0.3133,# CHANGED: 0.2909 -> 0.3133 — renorm only (book UNCHANGED at ~6.41%, still
                    # the largest non-SMHV position). Growth-max pass folded SNOW + COHR trim
                    # into CRDO (+472M net income, +206% rev, +60/+200 forecast). CYCLE (top-10).
    "COHR":  0.0979,# CHANGED: 0.0909 -> 0.0979 — renorm (book unchanged, ~2.0%). CYCLE.
    "FN":    0.1932,# CHANGED: 0.1794 -> 0.1932 — renorm (book UNCHANGED at ~3.95%). Fabrinet —
                    # optical contract mfr; cleanest growth-at-reasonable-price name (28% EPS
                    # gr, net cash). CYCLE / Mid.
    "ALAB":  0.0734,# CHANGED: 0.1396 -> 0.0734 — TRIMMED to ~1.5% book (was 3.07%). Mid/Late,
                    # 118x fwd P/E, analysts -36%: most stretched name held, fails 8-Point #6
                    # (priced for perfection). Book rotated to ZS (W5). Astera Labs —
                    # AI connectivity pure-play (CXL/PCIe retimers),
                    # highest-beta name in the sleeve. CYCLE / Mid — bottleneck is young
                    # but the stock already ran +500%/2y, so remaining runway = Mid.
                    # CHANGED 2026-06: S (SentinelOne) MOVED OUT to W5 (it's a software/cyber
                    # name). Growth-max pass: SNOW + COHR trim folded into CRDO; 6 names
                    # renormalized to sum to 1.0.
}

# --- WAVE 4: HYPERSCALER CLOUD (20%) ---
W4_CLOUD_TARGETS = {
    "MSFT":  0.20,  # Azure + OpenAI
    "GOOGL": 0.20,  # Gemini + TPU + Cloud
    "AMZN":  0.20,  # AWS
    "META":  0.20,  # Open models + ad-AI
    "ORCL":  0.20,  # Cloud-capacity winner
}

# --- WAVE 5: AI SOFTWARE / APPS (5.66%) ---
# CHANGED (growth-max pass): SNOW MOVED OUT to CRDO (W3) — it was the weakest
# software name (slowest forecast, multiple-compression hangover) and CRDO is the
# sleeve's proven hyper-grower. The wave was also trimmed to fund W6 growth.
# Four profitable anchors remain (PANW/CRWD/NOW/DDOG); PLTR & S kept at 0%.
W5_SOFTWARE_TARGETS = {
    "S":     0.0000,# CUT. Only GAAP-UNPROFITABLE top-10 name (net income -$319M TTM,
                    # never had a profitable year); FCF-positive but turnaround unproven.
                    # Kept at 0% for easy re-add if the GAAP turn completes.
    "PANW":  0.1699,# CHANGED: 0.2095 -> 0.1699 — renorm (book unchanged) as ZS was added to
                    # the wave. Security platform — biggest, cheapest, steadiest.
    "CRWD":  0.1700,# CHANGED: 0.2096 -> 0.1700 — renorm (book unchanged). AI cybersecurity.
    "NOW":   0.3014,# CHANGED: 0.3716 -> 0.3014 — renorm (book UNCHANGED at ~2.51%). Most
                    # mispriced quality held: 22x fwd / 0.89 PEG, down ~50% on the year.
                    # Workflow AI (Now Assist), profitable. CYCLE / Mid.
    "ZS":    0.1889,# NEW: ~1.57% book. Zscaler — zero-trust / SASE cyber. Washed-out quality
                    # (down ~36-59%, RSI ~43, PEG 1.23, 30% FCF margin, $3.5B ARR +25%);
                    # agentic-AI security catalyst live. Mirror-image rotation from ALAB;
                    # fills the cyber gap left when S was cut. CYCLE / Mid. Promoted from
                    # WATCHLIST. Stage entry on a 50-SMA reclaim ("size on confirmation").
    "PLTR":  0.0000,# TRIMMED: below 200d / death cross (tech sell signal, pt 8).
                    # Kept at 0% for easy re-add.
    "SNOW":  0.0000,# CHANGED: 0.1904 -> 0.00 — MOVED to CRDO (W3) on growth-max pass.
                    # Healed bubble hangover but slowest forecast of the survivors.
    "DDOG":  0.1698,# CHANGED: 0.2093 -> 0.1698 — renorm (book unchanged). AI observability.
}

# --- WAVE 6: SPECULATIVE / SECOND-ORDER (6%) ---
# CHANGED (growth-max pass): wave grown 3% -> 6% (funded from W5) so the two
# highest-upside names get real slots: IONQ (+175% mid) and RKLB (+171%) sized
# to ~1.5% book each, alongside TMDX 2.5% (profitable, uncorrelated decorrelator).
# These are the portfolio's convex tail — small absolute size, large payoff skew.
W6_SPEC_TARGETS = {
    "TMDX":  0.4166,  # TOP-10 name; 0.4166 x 6% = 2.5% book. MedTech organ-transport,
                      # profitable, off-radar, non-AI diversifier.
    "AXON":  0.0833,  # Defense/policing AI (profitable anchor) — small spec slice (0.5%)
    "IONQ":  0.1667,  # CHANGED: 0.25 -> 0.1667 — trimmed to 1.0% book to fund SYM.
                      # Quantum revenue leader; +175% mid (highest forecast). Lottery/convex.
    "RKLB":  0.1667,  # CHANGED: 0.25 -> 0.1667 — trimmed to 1.0% book to fund SYM.
                      # Space/autonomy; +171% mid. Lottery/convex tail alongside IONQ.
    "SYM":   0.1667,  # NEW 2026-06: Symbotic — warehouse/logistics automation robotics
                      # (physical-AI). 1.0% book, funded by trimming IONQ+RKLB. Real
                      # business ($2.5B rev, +$749M FCF) so HIGHER quality than the pre-rev
                      # lottery names it sits beside — but GAAP-unprofitable (net -$28M TTM,
                      # fails Pt 2) + lumpy/customer-concentrated (Walmart), so it lives in
                      # the convex tail. CATALYST / Binary — size tiny, never average down.
    "CRCL":  0.0000,  # Circle (USDC) — held windfall (147 shares), TARGET 0%. Parked to
                      # track/manage down, NOT to add to. Catalyst.
    "LEU":   0.0000,  # Centrus Energy — HALEU/uranium enrichment for advanced reactors
                      # (SMR fuel-supply bottleneck). TARGET 0% — watch-only stub so it
                      # shows in the basket; re-size if the enrichment thesis firms up.
                      # Catalyst / Binary (policy/contract-driven, pre-scale economics).
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
    # NVDA/AVGO/ASML/TSM/MU/AMD removed from the basket (SMHV covers them) — no
    # STRATEGY tags either, so verify_allocations() stays clean.
    "SIMO":    "cycle",     # Silicon Motion — NAND/SSD controllers; memory-cycle, trim at peak
    "BESI.AS":   "cycle",   # Advanced packaging — single-tech bet (hybrid bonding); trim at peak
    "000660.KS": "cycle",   # SK Hynix — HBM leader; same memory cycle as MU, trim at peak
    "CAMT":      "cycle",   # Camtek — HBM inspection/AOI bottleneck; high-beta, trim near peak
    "CDNS":      "dca",     # Cadence — EDA duopoly, secular high-margin compounder, hold forever
    "ONTO":      "cycle",   # Onto — metrology/inspection, high-beta WFE; Mid-cycle, buy dips, trim at peak
    "SMHN.DE":   "cycle",   # SUSS MicroTec — packaging/bonding equipment, high-beta; trim near peak

    # --- W2 POWER ---
    "GEV":     "dca",       # Grid supercycle — hold forever
    "CCJ":     "dca",       # Uranium structural deficit — hold forever
    "ETN":     "dca",       # Transmission/electrification — quality compounder, hold forever
    "HUBB":    "dca",       # Transformers/grid gear — 2-4yr lead-times, quality, hold forever
    "CEG":     "cycle",     # Nuclear utility — power-price sensitive
    # CUT: ABBN.SW (was "dca") — only overvalued name (analysts -13%), slowest ballast;
    #      book split to FN (W3) + NOW (W5). Re-add here + in W2_POWER_TARGETS if restored.
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
    "FN":      "cycle",     # Fabrinet — optical contract mfr; cyclical, buy dips, trim at peak
    "ALAB":    "cycle",     # Astera — AI connectivity pure-play, high-beta; Mid-cycle (+500%/2y), trim when growth <30%
    "S":       "cycle",     # SentinelOne — AI-native cyber, just-turned-profitable; buy dips, trim at peak
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
    "ZS":      "cycle",     # Zscaler — zero-trust/SASE cyber; washed-out, FCF+ but GAAP-light; buy dips
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
    "SYM":     "catalyst",  # Symbotic — robotics, GAAP-unprofitable + lumpy; size once, no avg down
    "CRCL":    "catalyst",  # Circle — held windfall, target 0%; manage down, never avg in
    "LEU":     "catalyst",  # Centrus — HALEU enrichment, policy/contract-driven; watch-only 0%
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
#
# DATA INVARIANTS (enforced by validate_watchlist() below; keeps the Category
# table honest so it never oversells a risky name):
#   1. DEBT-FUNDED / PRE-REVENUE / SHRINKING businesses must be pos="Binary"
#      with a NEGATIVE cagr low end. They are not "cycle/Early" growth ramps —
#      the upside is leveraged, the downside is loss of capital.
#      (e.g. APLD, CRWV, SMR, INTC, 1810.HK.)
#   2. pos="Binary" => cagr[0] < 0  (a binary outcome must show its downside).
#   3. strategy="catalyst"/"lottery" => pos should be "Binary" (event/punt risk).
#   4. A name's cagr band must not contradict its own note (e.g. a note saying
#      "rev shrinking" cannot pair with an all-positive band).
# =========================================================================

WATCHLIST = {
    # --- Memory / storage (HBM + NAND/HDD) — the deepest-cyclical corner ---
    # NB: MU promoted to a held W1 CYCLE pick (see W1_SILICON_TARGETS) — removed here.
    "SNDK": {
        "pos":      "Late",
        "cagr":     (2, 15),
        "strategy": "cycle",
        "area":     "Memory / NAND (SanDisk)",
        "note":     "SKIP/late — +251% rev is the NAND cycle at its PEAK, trading "
                    "near 52w high. Deep-cyclical commodity. Buying here = buying the "
                    "top. Covered indirectly anyway.",
    },
    "WDC": {
        "pos":      "Late",
        "cagr":     (2, 14),
        "strategy": "cycle",
        "area":     "Storage / HDD (Western Digital)",
        "note":     "SKIP — +46% rev / 55% net flatters a cycle top. Commodity HDD/"
                    "NAND, near 52w high. Classic late-cycle trap.",
    },
    "STX": {
        "pos":      "Late",
        "cagr":     (2, 14),
        "strategy": "cycle",
        "area":     "Storage / HDD (Seagate)",
        "note":     "SKIP — same as WDC: deep-cyclical HDD at cycle peak near highs.",
    },

    # --- Compute / IP / connectivity ---
    "ARM": {
        "pos":      "Mid",
        "cagr":     (10, 24),
        "strategy": "cycle",
        "area":     "Chip IP / architecture",
        "note":     "Only name that fills a UNIQUE gap (royalty IP, ~95% gross). Elite "
                    "moat BUT 129x fwd P/E / 86x sales — pricier than PLTR. Dip-only, "
                    "tiny size; NEVER DCA at this multiple. Treat as CYCLE/conviction.",
    },
    # NB: AMD promoted to a held W1 CYCLE pick (see W1_SILICON_TARGETS) — removed here.
    "QCOM": {
        "pos":      "Late",
        "cagr":     (3, 10),
        "strategy": "cycle",
        "area":     "Mobile / edge-AI chips",
        "note":     "SKIP — cheap (20x P/E, $9.6B FCF) but rev -4%: Apple designing it "
                    "out. 'Cheap for a reason' value trap, not a growth thesis.",
    },
    "ADI": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     "Analog / industrial chips",
        "note":     "Highest-QUALITY new name (37% rev, 26% net, $3.9B FCF, 28x). "
                    "Would be DCA-grade — but only loosely AI-thesis (industrial). "
                    "Consider only if widening beyond pure AI-infra.",
    },

    # --- Fab equipment ('picks of the picks') — all inside SMHV.SW ---
    "KLAC": {
        "pos":      "Mid",
        "cagr":     (9, 17),
        "strategy": "dca",
        "area":     "Fab inspection equipment",
        "note":     "High quality (36% net, $2.9B FCF). DCA-grade oligopoly, but "
                    "already held via SMHV.SW (equipment ~11% of ETF). Redundant direct.",
    },
    "LRCX": {
        "pos":      "Mid",
        "cagr":     (9, 17),
        "strategy": "dca",
        "area":     "Fab etch/deposition equipment",
        "note":     "Quality (31% net, $4.4B FCF). Same as KLAC — already inside the "
                    "ETF; only add direct for concentrated equipment conviction.",
    },
    "AMAT": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     "Fab equipment (broadest)",
        "note":     "Quality (29% net). Inside SMHV.SW already. Redundant direct.",
    },
    # NB: ONTO promoted to a held W1 CYCLE pick (see W1_SILICON_TARGETS) — removed here.
    # NB: SMHN.DE promoted to a held W1 CYCLE pick (see W1_SILICON_TARGETS) — removed here.
    "MTSI": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8.4, 18.1),
        "area":     "RF/analog + optical semis (MACOM)",
        "note":     "Blend of defense RF + datacenter optical — less pure AI-bottleneck "
                    "than ONTO/SMHN (now held). Decent but least differentiated of the "
                    "equipment candidates. Lower priority; consider only if widening the sleeve.",
    },

    # --- Legacy / off-thesis large caps ---
    "AAPL": {
        "pos":      "Mid",
        "cagr":     (6, 11),
        "strategy": "dca",
        "area":     "Consumer hardware / services",
        "note":     "DCA-grade ($101B FCF!) but it's a CONSUMER play, not AI-infra. "
                    "Belongs in a core portfolio, not this AI book. Off-thesis.",
    },
    "CSCO": {
        "pos":      "Late",
        "cagr":     (4, 9),
        "strategy": "dca",
        "area":     "Legacy networking",
        "note":     "SKIP — you already hold ANET (faster, higher-margin competitor). "
                    "Redundant and slower-growth.",
    },
    "TXN": {
        "pos":      "Mid",
        "cagr":     (6, 13),
        "strategy": "cycle",
        "area":     "Analog / industrial chips",
        "note":     "SKIP — analog/industrial, barely an AI play. Inside ETF anyway.",
    },
    "INTC": {
        "pos":      "Binary",
        "cagr":     (-15, 18),
        "strategy": "lottery",
        "area":     "Legacy CPU / foundry turnaround",
        "note":     "AVOID/lottery — UNPROFITABLE (-6% net, -$8.3B FCF, 76x P/E, 7% "
                    "rev). Foundry turnaround is a BINARY gamble, not an investment "
                    "(tagged Binary, not Late, to reflect the all-or-nothing outcome).",
    },

    # --- Korea memory (HBM leaders) — access friction ---
    "005930.KS": {
        "pos":      "Mid",
        "cagr":     (3.7, 17.1),
        "strategy": "cycle",
        "area":     "Memory / diversified (Samsung)",
        "note":     "HBM + broad semi at 6x P/E — cheap. But Korea-listed (FX/access "
                    "friction on EU brokers). Better captured via a broad ex-US semi "
                    "ETF than bought direct.",
    },
    "000660.KS": {
        "pos":      "Mid",
        "cagr":     (4.6, 22.9),
        "strategy": "cycle",
        "area":     "Memory / HBM leader (SK hynix)",
        "note":     "Purest HBM leader (+198% rev, 57% net, 6x P/E) — but it's the "
                    "memory cycle peaking. Korea-listed access friction. Watch, "
                    "don't chase at the top.",
    },

    # --- Non-semi: consumer / China ---
    "1810.HK": {
        "pos":      "Binary",
        "cagr":     (-8, 16),
        "strategy": "cycle",
        "area":     "Consumer electronics / EV (Xiaomi)",
        "note":     "OFF-THESIS — cheap (14x P/E) but rev -11% (SHRINKING), so the "
                    "band low end is negative (turnaround may fail). China consumer/EV "
                    "turnaround bet, not AI value-chain. + China geopolitical risk, "
                    "HK/OTC access. Keep in a SEPARATE sleeve if at all.",
    },

    # --- EDA / chip-design software (a structural gap nothing else covers) ---
    "CDNS": {
        "pos":      "Mid",
        "cagr":     (9.9, 18.1),
        "strategy": "dca",
        "area":     "Chip-design software (EDA)",
        "note":     "DCA-grade. The tools every chip is designed with — software "
                    "moat NOT in your book or the ETF. 86% gross, 21% net, $1.5B FCF. "
                    "Cadence/Synopsys are the EDA duopoly; ~41x P/E so not cheap.",
    },
    "SNPS": {
        "pos":      "Mid",
        "cagr":     (9.9, 18.1),
        "strategy": "dca",
        "area":     "Chip-design software (EDA)",
        "note":     "DCA-grade. Other half of the EDA duopoly. 83% gross, 42% rev, "
                    "$3.5B FCF, ~26x fwd P/E. NB it absorbed ANSYS (ANSS) — the "
                    "ANSS ticker is gone, exposure now lives here.",
    },
    "TER": {
        "pos":      "Mid",
        "cagr":     (7, 16),
        "strategy": "cycle",
        "area":     "Chip test equipment",
        "note":     "Complements the LRCX/AMAT equipment angle. 87% rev is the test "
                    "cycle recovering (cyclical), 23% net. Buy on down-cycles, not at "
                    "the peak; not in the ETF top holdings.",
    },

    # --- AI-native cloud / GPU rental ---
    "CRWV": {
        "pos":      "Binary",
        "cagr":     (-10, 32),
        "strategy": "catalyst",
        "area":     "AI-native cloud / GPU rental (CoreWeave)",
        "note":     "Pure-play AI compute rental — directly on-thesis but HIGH-BETA "
                    "binary: 112% rev yet -26% net and -$8.6B FCF (massive debt-funded "
                    "GPU capex). Sell/scale on execution catalysts; size tiny, never "
                    "average down. Borderline lottery.",
    },

    # --- Defense / crypto-adjacent industrials ---
    "KTOS": {
        "pos":      "Mid",
        "cagr":     (8, 18),
        "strategy": "cycle",
        "area":     "Industrial / Defense",
        "note":     "Autonomous military drones. CHANGED: KTOS dropped out of XAIX.DE "
                    "top holdings (latest look-through), so the prior 'already held "
                    "indirectly' overlap no longer applies. Now a clean candidate — "
                    "consider for INDUSTRIAL if adding defense exposure. NB thin FCF "
                    "(2% net) -> momentum-like, treat as CYCLE.",
    },
    "IREN": {
        "pos":      "Binary",
        "cagr":     (-25, 40),
        "strategy": "lottery",
        "area":     "Industrial (AI compute + Bitcoin mining)",
        "note":     "SMALL/SKIP — crypto-correlated beta is new uncorrelated risk, "
                    "not diversification. Negative FCF (-$2.3B). Lottery, not cycle.",
    },
    "CIFR": {
        "pos":      "Binary",
        "cagr":     (-25, 38),
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
        "pos":      "Mid",
        "cagr":     (8, 18),
        "strategy": "cycle",
        "area":     "Silicon / low-power FPGAs (Lattice)",
        "note":     "CLEANEST add of the batch — a real chip company, not a story "
                    "stock. Low-power FPGAs for AI-edge. Cyclical: buy dips, trim "
                    "into the next semi peak. Not in SMHV.SW top holdings.",
    },

    # Power / infra (datacenter electricity + hosting)
    "APLD": {
        "pos":      "Binary",
        "cagr":     (-12, 32),
        "strategy": "catalyst",
        "area":     "AI datacenter hosting / HPC leases (Applied Digital)",
        "note":     "SAME risk profile as CRWV — capex-heavy, DEBT-FUNDED GPU "
                    "leasing. The fat upside is leveraged, not free: it depends on "
                    "AI capex staying hot + continued refinancing + key contracts "
                    "holding. Binary, not cycle — buy tiny like a catalyst, NEVER "
                    "average down. Wide band includes a real negative low end.",
    },
    "BWXT": {
        "pos":      "Early",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     "Power / nuclear components (naval reactors + SMR parts)",
        "note":     "The PROFITABLE nuclear name — naval reactors + SMR components, "
                    "real earnings. Powers the AI-datacenter electricity thesis and "
                    "is DCA-able, unlike the pre-revenue SMR crowd.",
    },
    "LEU": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (8.4, 22.9),
        "area":     "Nuclear fuel / HALEU enrichment (Centrus)",
        "note":     "Only US HALEU enricher; real revenue. Fits 'AI needs power' via "
                    "the fuel cycle. Cyclical commodity-linked — buy down-cycles, not "
                    "at highs.",
    },
    "SMR": {
        "pos":      "Binary",
        "cagr":     (-13, 32),
        "strategy": "catalyst",
        "area":     "Nuclear / small modular reactors (NuScale)",
        "note":     "Pre-revenue. Binary on first commercial reactor. One-and-done "
                    "catalyst bet — size tiny, NEVER average down.",
    },
    "SRUUF": {
        "pos":      "Binary",
        "cagr":     (-5, 18),
        "strategy": "cycle",
        "area":     "Uranium commodity trust (Sprott Physical Uranium)",
        "note":     "OFF-STRATEGY mechanically — a COMMODITY trust tracking U3O8 "
                    "price, not an equity, so the CAGR band is a COMMODITY price "
                    "scenario (symmetric, real negative low end), not an earnings "
                    "forecast. Proxy for the nuclear thesis but behaves like the "
                    "metal. Separate sleeve if at all.",
    },

    # Quantum pile-on — one catalyst ticket (IONQ) is already held
    "RGTI": {
        "pos":      "Binary",
        "cagr":     (-25, 45),
        "strategy": "lottery",
        "area":     "Quantum computing (Rigetti)",
        "note":     "Pre-revenue quantum. You already hold IONQ as the quantum "
                    "catalyst ticket; adding more just smears one lottery bet across "
                    "many. If you want ONE more, this is the pick — size tiny.",
    },
    "QBTS": {
        "pos":      "Binary",
        "cagr":     (-25, 45),
        "strategy": "lottery",
        "area":     "Quantum computing (D-Wave)",
        "note":     "Pre-revenue quantum (annealing). Same logic as RGTI — redundant "
                    "with IONQ. Lottery only.",
    },
    "QUBT": {
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "strategy": "lottery",
        "area":     "Quantum computing (Quantum Computing Inc.)",
        "note":     "Micro-cap pre-revenue quantum. Pure lottery; max noise, no edge "
                    "over the IONQ position. Skip unless punting.",
    },
    "QNT": {
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "strategy": "lottery",
        "area":     "Quantum computing",
        "note":     "Speculative quantum name. Redundant with the IONQ quantum "
                    "ticket. Lottery only — tiny or skip.",
    },
    "XNDU": {
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "strategy": "lottery",
        "area":     "Quantum computing (Xanadu)",
        "note":     "Pre-revenue photonic quantum. Lottery; same smearing problem as "
                    "the rest of the quantum pile. Skip unless punting.",
    },
    "INFQ": {
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "strategy": "lottery",
        "area":     "Quantum computing",
        "note":     "Speculative quantum name. Redundant with IONQ. Lottery only.",
    },
    "HQ": {
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "strategy": "lottery",
        "area":     "Quantum computing",
        "note":     "Speculative quantum name. Redundant with IONQ. Lottery only.",
    },

    # Off-thesis — tracked for completeness, NOT AI value-chain
    "ENVX": {
        "pos":      "Binary",
        "cagr":     (-20, 35),
        "strategy": "lottery",
        "area":     "Battery tech (Enovix)",
        "note":     "OFF-THESIS — silicon-anode batteries, not the AI value chain. "
                    "Pre-profit. Belongs in a separate energy/tech sleeve.",
    },
    "VKTX": {
        "pos":      "Binary",
        "cagr":     (-25, 40),
        "strategy": "lottery",
        "area":     "Biotech / GLP-1 (Viking Therapeutics)",
        "note":     "OFF-THESIS — GLP-1 obesity biotech, ZERO AI linkage. Pure sector "
                    "drift; binary on trial data. Does not belong in this AI book.",
    },

    # --- Off-thesis space / robotics moonshots (RKLB already owns the space slot) ---
    "LUNR": {
        "pos":      "Binary",
        "cagr":     (-25, 38),
        "strategy": "lottery",
        "area":     "Space / lunar landers (Intuitive Machines)",
        "note":     "OFF-THESIS — NASA commercial lunar landers. RKLB already owns the "
                    "space slot and is higher-quality; LUNR is lower-quality AND higher-"
                    "risk (-70%+ binary). Not AI value-chain. Lottery only.",
    },
    "SERV": {
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "strategy": "lottery",
        "area":     "Robotics / sidewalk delivery (Serve Robotics)",
        "note":     "OFF-THESIS — sidewalk delivery robots, ~$600M micro-cap, deeply "
                    "unprofitable (-$2.05 EPS). 'Nvidia-backed' = tiny passive stake, "
                    "not a deal. Hype-driven binary. Lottery; size tiny or skip.",
    },
    "ACHR": {
        "pos":      "Binary",
        "cagr":     (-25, 40),
        "strategy": "lottery",
        "area":     "eVTOL air taxi (Archer Aviation)",
        "note":     "OFF-THESIS — eVTOL air taxi, ->$0 risk. Triple-gated: FAA cert + "
                    "manufacturing + demand. Not AI value-chain. Pure lottery.",
    },

    # --- AI cluster integration (W1/W3 seam) ---
    "PENG": {
        "pos":      "Mid",
        "cagr":     (8, 18),
        "strategy": "cycle",
        "area":     "AI cluster integration / advanced memory (Penguin Solutions)",
        "note":     "ON-THESIS — ex-SGH; builds HPC/AI clusters + advanced memory "
                    "integration, the 'who assembles the GPU clusters' layer the book "
                    "is thin on (W1/W3 seam). PROFITABLE, not a story stock, but "
                    "smaller/less-proven than held names and demand is cyclical — buy "
                    "dips, trim at peak. Watchlist-first.",
    },

    # --- Transmission / cooling — considered for rotation, NOT added ---
    "SIE.DE": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (8.4, 16.0),
        "area":     "Grid / transmission (EU, Siemens)",
        "note":     "SKIPPED — diluted conglomerate: grid is one segment of a giant "
                    "industrial, so low beta to the actual bottleneck. HUBB/ABBN.SW "
                    "(now held) are cleaner transmission pure-plays at the same forecast.",
    },
    "PNR": {
        "strategy": "dca",
        "pos":      "Early",
        "cagr":     (7.0, 14.9),
        "area":     "Water / thermal (Pentair)",
        "note":     "SKIPPED — Early and not-run, but weak AI thesis: broad water "
                    "company, datacenter cooling is a small revenue slice. VRT (held) "
                    "is the better cooling pure-play.",
    },

    # --- Cybersecurity (new screen) — CRWD/PANW too big (fail Pt 1); CYBR
    #     absorbed by PANW's ~$25B CyberArk deal (closed Feb 2026). S is HELD
    #     in W5. These are the genuinely new, framework-relevant cyber names. ---
    # PROMOTED to held: ZS (Zscaler) — moved into W5_SOFTWARE_TARGETS at ~1.57% book,
    # funded by the ALAB trim. Removed from WATCHLIST. Re-add here if it is ever cut to 0%.
    "RBRK": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (15, 30),
        "area":     "AI-data security / cyber-resilience (Rubrik)",
        "note":     "AI-data protection + cyber-resilience, expanding into unstructured/"
                    "AI-data. Strong momentum, likely still pre-/just-profit (Group 1). "
                    "Early — add on dips, but unproven profitability: keep tiny.",
    },
    "NET": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (12, 24),
        "area":     "Edge + security (Cloudflare)",
        "note":     "Broadest AI-infra + security angle, but bigger and EXPENSIVE "
                    "(rich multiple). Quality compounder — dip-only, never DCA at this "
                    "valuation. Watchlist until a real pullback.",
    },
    "OKTA": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8, 18),
        "area":     "Identity for the agentic-AI era (Okta)",
        "note":     "Identity for AI agents; mid-cap, more REASONABLE valuation but "
                    "SLOWER growth than peers. Solid Pt-6 value angle, weaker Pt-3. "
                    "Watchlist-grade.",
    },

    # --- Packaging / optical / semi picks-and-shovels (new screen) ---
    #     ONTO, FN, SIMO are now HELD in W1/W3 — not repeated here. (CAMT was
    #     swapped to 0% in favour of ONTO; it stays in W1_SILICON_TARGETS as an
    #     easy re-add, so it is not listed as a fresh watchlist idea either.)
    "KLIC": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (8, 22),
        "area":     "HBM bonding / TCB (Kulicke & Soffa)",
        "note":     "HBM thermo-compression bonding pick-and-shovel. Cyclical at/near "
                    "trough — Pt-6 trough thesis applies (low TTM earnings = setup). "
                    "Buy the down-cycle, trim into the HBM ramp.",
    },
    "NVMI": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (9, 20),
        "area":     "Metrology (Nova)",
        "note":     "Process-control metrology — same picks-and-shovels seam as held "
                    "ONTO. Profitable, quality, but partly covered via SMHV.SW "
                    "equipment slice. Watchlist for concentrated metrology conviction.",
    },
    "AMKR": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (7, 18),
        "area":     "Advanced packaging / test (Amkor)",
        "note":     "OSAT advanced-packaging/test — direct AI-packaging exposure. "
                    "Profitable but lower-margin, capex-heavy and cyclical. Buy dips, "
                    "trim at peak; cleaner packaging beta than the equipment names.",
    },
    "AAOI": {
        "strategy": "cycle",
        "pos":      "Late",
        "cagr":     (3, 18),
        "area":     "Optical components (Applied Optoelectronics)",
        "note":     "Optical with THIN profit and high volatility. Torque on the AI-"
                    "optical cycle but quality is low vs held COHR/FN/CRDO. Late/"
                    "trader-grade — tiny size only, never DCA.",
    },
    "AEHR": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-20, 35),
        "area":     "Test / burn-in (Aehr Test Systems)",
        "note":     "TINY test/burn-in name surfaced in passing. Highly customer-"
                    "concentrated and lumpy — a single design-win swings the P&L. "
                    "Binary micro-cap punt; size tiny or skip.",
    },
    "ICHR": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (6, 18),
        "area":     "Semi equipment subsystems (Ichor)",
        "note":     "Surfaced in passing. Fluid-delivery subsystems supplier to the "
                    "fab-equipment makers — deep-cyclical, thin-margin second-derivative "
                    "play. Trough-cycle only; lower quality than the held names.",
    },

    # --- Neocloud / AI infrastructure (new screen) ---
    "NBIS": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (15, 35),
        "area":     "Neocloud / GPU cloud (Nebius)",
        "note":     "RARE profitable hypergrowth neocloud — unlike DEBT-FUNDED CRWV/"
                    "APLD it is actually making money, which is why it's cycle/Early "
                    "not Binary. Capex-cyclical and competitive; size on confirmation.",
    },

    # --- AI health / drug discovery (new screen) ---
    "TEM": {
        "strategy": "catalyst",
        "pos":      "Binary",
        "cagr":     (-15, 40),
        "area":     "AI diagnostics (Tempus AI)",
        "note":     "AI diagnostics, Group-1 PRE-PROFIT growth story. Real AI linkage "
                    "(genomic data + models) but unprofitable and execution-gated — "
                    "binary on the path to profit. Catalyst sizing, never average down.",
    },
    "RXRX": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "area":     "AI drug discovery (Recursion)",
        "note":     "AI drug discovery, CASH-BURNING and pipeline-binary. Lottery-ish: "
                    "the upside needs a clinical/platform win AND continued funding. "
                    "->$0 risk if burn outruns catalysts. Tiny punt or skip.",
    },

    # --- Physical AI / robotics ('next boom' — mostly speculative) ---
    "VPG": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (6, 18),
        "area":     "Robotics / semi sensors (Vishay Precision Group)",
        "note":     "UNDER-RADAR and PROFITABLE precision-sensor maker (robotics/semi). "
                    "Best-quality name in the physical-AI bucket — real earnings, not a "
                    "story. Cyclical/industrial; buy dips. Watchlist-first.",
    },
    "MCHP": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (7, 16),
        "area":     "Robotics-enabler MCUs (Microchip)",
        "note":     "Mid-large MCU/analog supplier — robotics & embedded enabler. "
                    "Cyclical, currently working off an inventory down-cycle (Pt-6 "
                    "trough angle). Quality but lower torque; buy the trough.",
    },
    "9880.HK": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-30, 50),
        "area":     "Humanoid robotics (UBTECH, HK-listed)",
        "note":     "PURE-PLAY humanoid, HK-listed, PRE-PROFIT. Maximum thematic "
                    "torque on the physical-AI boom but binary on commercialization + "
                    "cash. Currency/listing risk too. Lottery — size tiny.",
    },
    "OUST": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "area":     "Lidar (Ouster)",
        "note":     "Lidar for autonomy/robotics. Improving but still unprofitable in a "
                    "brutally competitive, commoditizing segment. Binary on a margin "
                    "turn; lottery sizing only.",
    },
    "RR": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-35, 50),
        "area":     "Service robots (Richtech Robotics)",
        "note":     "MICRO-CAP service-robot lottery. Tiny revenue, deeply unprofitable, "
                    "hype-driven. Classic ->$0 binary punt — size minimal or skip.",
    },
    "BOT": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-25, 40),
        "area":     "Robotics fund / private exposure (RoboStrategy CEF)",
        "note":     "Closed-end fund holding PRIVATE robotics names — a way to get "
                    "pre-IPO physical-AI exposure. Watch the NAV discount/premium and "
                    "fees. Not a single-stock thesis; treat as a speculative basket.",
    },

    # --- Space (new screen) ---
    "ASTS": {
        "strategy": "catalyst",
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "area":     "Satellite-to-phone (AST SpaceMobile)",
        "note":     "Near PRE-REVENUE, capital-intensive constellation build. Binary on "
                    "satellite launches + carrier deals + funding. RKLB (held) owns the "
                    "cleaner space slot; ASTS is a higher-risk catalyst punt.",
    },

    # --- Nuclear SMR (new screen) — SMR (NuScale) already on the list above. ---
    "NNE": {
        "strategy": "catalyst",
        "pos":      "Binary",
        "cagr":     (-20, 38),
        "area":     "Nuclear / small modular reactors (Nano Nuclear)",
        "note":     "PRE-REVENUE SMR, same profile as SMR/NuScale: binary on first "
                    "commercial reactor + licensing, debt/dilution-funded. One-and-done "
                    "catalyst bet — size tiny, NEVER average down.",
    },
}


def validate_watchlist():
    """Enforce the WATCHLIST data invariants (see header). Returns a list of
    violation strings; empty list means clean. Machine-checkable subset:
      (2) pos=='Binary'  => cagr low end < 0
      (3) strategy in {catalyst, lottery} => pos == 'Binary'
    Invariants (1) and (4) are judgement calls, documented for the maintainer.
    """
    problems = []
    for t, d in WATCHLIST.items():
        pos = d.get("pos")
        cagr = d.get("cagr")
        strat = d.get("strategy")
        if pos == "Binary" and cagr is not None and cagr[0] >= 0:
            problems.append(
                f"{t}: pos=Binary but cagr low end {cagr[0]}>=0 "
                f"(a binary must show its downside)")
        if strat in ("catalyst", "lottery") and pos not in (None, "Binary"):
            problems.append(
                f"{t}: strategy={strat} but pos={pos} (event/punt risk "
                f"should be Binary)")
    return problems


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
