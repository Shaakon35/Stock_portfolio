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

# NOTE (2026-06 MODEL CHANGE): the portfolio is now defined by DIRECT per-ticker
# book percentages inside each W*_TARGETS basket below (e.g. "AMZN": 2.0 means 2.0%
# of total book). The wave-level TARGET_WEIGHTS dict is no longer hand-maintained —
# it is AUTO-DERIVED from those baskets (see the computation just after ALL_BASKETS).
# This is the single source of truth: to change a holding's weight, edit its number
# in the basket; the wave total and TARGET_WEIGHTS follow automatically.
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
    # VALUES ARE DIRECT BOOK % (2026-06 model change): e.g. 2.0 == 2.0% of total book.
    # The trailing "# CHANGED: 0.x ->" notes below are HISTORICAL sub-weight values from the
    # old normalized model; the live number on each line is now a direct percent.
    "SMHV.SW":   31.0,# CHANGED: 37.5 -> 32.5 -> 31.0 (RESHAPE-TRIM 2026-08) — trimmed a total
                        # of 6.5% off the oversized ETF anchor to fund four genuine new
                        # diversifier LEGS: PODD (health-care), WPM (commodity/gold), AJG
                        # (financials) and ONON (consumer brand) in W7 — none of which the
                        # tech-heavy book had any exposure to. Reduces single-position
                        # concentration (the ETF still dominates at ~1/3 of book) and lowers
                        # correlation to the AI-capex cycle every other wave rides. This trims
                        # the fixed 90k CHF windfall's book WEIGHT, not the share count.
                        # Prior: 0.85227 -> 0.85656 (RIGHTSIZE 2026-06). NB: SMHV tracks a
                        # US-LISTED semi index, so it holds ZERO Samsung/SK Hynix — genuine new
                        # exposure, not a dup.
    # --- REMOVED 2026-06: NVDA/AVGO/ASML/TSM/MU/AMD dropped from the basket.
    #     They are SMHV's top holdings, so the ETF already gives full mega-cap
    #     exposure and holding them as 0.0 singles only cluttered the table. To
    #     re-add as a fresh-money single, restore a line here + a STRATEGY tag. ---
    # --- SURVIVING SINGLES. CAMT/BESI/SIMO are TOP-10 names. ONTO was TRIMMED
    #     (see below) and its 2% split into CAMT + BESI (now 3% book each). The
    #     three smaller names (SK Hynix/CDNS/SMHN) sit at ~1.47% book. ---
    "CAMT":      0.0,# CHANGED: 0.0602 -> 0.00 — SWAPPED with ONTO (2026-06). On current
                        # FORWARD data CAMT is the weaker of the two metrology names: slower
                        # (fwd rev +17.7% / EPS +18.1%) and far richer (PEG 2.97 vs ONTO's
                        # 1.17), and it sits Mid/LATE cycle (closer to peak). The earlier
                        # trim favoured CAMT on TRAILING numbers when ONTO was mid-trough;
                        # the forecasts have since flipped. 0% for easy re-add. Its bottleneck
                        # tag (HBM inspection/AOI) is its remaining edge.
    "ONTO":      0.0,# CHANGED: 0.0602 -> 0.00 — CUT (REBALANCE 2026-06). Scores AVOID
                        # (GROWTH 4.7, 8PT 4.30, binding CYC 4.5) and is REDUNDANT with BESI in
                        # the back-end complex (both inspect/measure adjacent steps). The book
                        # keeps the better, non-redundant leg (BESI, the bonding/assembly step,
                        # higher quality) and drops the duplicate metrology bet. 0% for easy
                        # re-add on a fresh trough. Its book funded the ANET/NOW growth.
    "BESI.AS":   2.5,# CHANGED: 3.5 -> 2.5 (FICO-ADD 2026-08) — TRIMMED 1.0% to help fund
                        # the new FICO W7 diversifier. Prior: 0.07955 -> 0.07995 (RIGHTSIZE
                        # 2026-06) — basket share rose
                        # to keep book UNCHANGED at 3.5% as the W1 wave shrank (0.4378 * 0.07995 =
                        # 0.035). Prior: 0.09724 -> 0.07955 (CONV-REBAL 2026-06) — TRIMMED to
                        # 3.5% book, off its outsized 4.27% to a conviction-
                        # set target. Still the largest single non-SMHV name. The sharpest
                        # cyclical in the sleeve. Scores
                        # PRIME (GROWTH 9.6, 8PT 6.13, no weak layer: F8.4/V5.8/C8.4). The Early,
                        # NON-peak name in the back-end complex: advanced packaging (hybrid bonding
                        # for HBM4+/chiplets), western CoWoS pure-play, the assembly step (not
                        # inspection), highest quality (63% GM, 33% FCF margin). Ramp still AHEAD
                        # while DRAM is at its peak. EUR-listed. CYCLE / Early. ~5.0% of book.
    "ADI":       2.8,# ROUNDED 2026-06: 2.78 -> 2.8. CHANGED: 0.06818 -> 0.06350 (RIGHTSIZE 2026-06) — TRIMMED to 2.78%
                        # book (0.4378 * 0.06350 = 0.0278) to balance the book (absorbs the 0.22%
                        # shortfall between the new-name grows and the core trims). Prior: 0.04862
                        # -> 0.06818 (CONV-REBAL 2026-06) — was 3.0% book, a conviction-set target (the highest-
                        # QUALITY KEEP-DCA ballast in the sleeve). Analog Devices
                        # — analog/industrial silicon,
                        # the highest-QUALITY KEEP-DCA ballast in this otherwise cycle-heavy sleeve
                        # (scorer 8.3, 37% gross, 26% net, $3.9B FCF, PEG ~1.3). NB: despite the DCA
                        # tag it behaves cyclically (FY24 earnings halved, FY26 doubled), so a deep
                        # drop is a discount on a real franchise. Loosely AI-thesis (industrial/edge).
    "SIMO":      0.0,# CHANGED: 0.04255 -> 0.00 — CUT (SIMO->RDDT ROTATION 2026-06). Silicon
                        # Motion — NAND/SSD controllers. Scores PRIME on raw GROWTH (8.0) but
                        # carries the [PEAK?] flag and the WEAKEST risk-adjusted profile of the
                        # held cyclicals: CONV 5.28, V 4.9 / C 4.6 — a low PEG that is fake-cheap
                        # on peak memory-cycle earnings (the SK-Hynix/Micron trap). Rotated into
                        # RDDT (W7, CONV 7.66, every layer >=8, a non-semi AI diversifier) — a
                        # strict risk-adjusted upgrade AND better book diversification. 0% for
                        # easy re-add on a fresh NAND trough. CYCLE / Early-Mid.
    "000660.KS": 0.0,# CHANGED: 0.0295 -> 0.00 — TRIMMED. SK Hynix rode the DRAM/HBM cycle
                        # to a record peak (+~900% / 52wk, MU memory GM ~74% = all-time high):
                        # graded Mid/Late, the cycle-trap zone where a 6-7x fwd P/E is the
                        # WARNING (peak earnings about to mean-revert), not the bargain. Book
                        # redeployed to BESI.AS (Early, ramp ahead). 0% for easy re-add on the
                        # first DRAM down-quarter / margin roll. CYCLE / Mid-Late.
    "CDNS":      0.0,# CHANGED: 0.0295 -> 0.00 — REMOVED (owner decision, 2026-06). Thesis
                        # was the EDA design-tool duopoly (w/ Synopsys), chip-DESIGN layer not
                        # in SMHV. Cut on VALUATION/momentum: rich entry (45x fwd P/E, PEG
                        # 3.16, 18x P/S) against ~13% revenue growth, and EPS growth had
                        # stalled (FY24 +0.8% / FY25 +5.5%) on margin compression (op margin
                        # 30.6% -> 28.2%). Revenue itself never stalled — this is a price/
                        # multiple call, not a quality call. Book redeployed to BESI.AS. The
                        # design-layer gap is now UNCOVERED in the book; SNPS remains on the
                        # watchlist as the re-add route. 0% for easy re-add on a de-rating.
    "SMHN.DE":   0.0,# CHANGED: 0.0295 -> 0.00 — CUT (REBALANCE 2026-06). SUSS MicroTec —
                        # advanced-packaging/bonding equipment, the SAME HBM4/CoWoS bottleneck as
                        # BESI.AS, so it was a DUPLICATE leg. Scores AVOID (GROWTH 3.4). The book
                        # keeps BESI (the higher-quality bonding name) and drops the redundant
                        # one. Frankfurt-listed (EUR). 0% for easy re-add.
    "SNPS":      1.5,# NEW (RESHAPE 2026-08) — 1.5% book, funded by the CRDO cut (W3).
                        # Synopsys — the OTHER half of the EDA chip-design duopoly (with the
                        # now-cut CDNS). This CLOSES the design-layer gap the CDNS removal note
                        # flagged as "UNCOVERED in the book": the silicon wave holds the whole
                        # supply chain (hardware, packaging, analog) but no chip-DESIGN software.
                        # Lowest-volatility name in the wave: metronomic ~15% revenue every year
                        # (recurring/subscription EDA), the opposite risk profile to the cyclical
                        # CRDO it replaces. Scores CONV 7.91 (well above ADI 6.67 / CRDO 5.02).
                        # 83% gross, absorbed ANSYS (ANSS). DCA — hold forever.
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
    # VALUES ARE DIRECT BOOK % (2026-06 model change): e.g. 2.0 == 2.0% of total book.
    # The trailing "# CHANGED: 0.x ->" notes below are HISTORICAL sub-weight values from the
    # old normalized model; the live number on each line is now a direct percent.
    "GEV":     2.0,# CHANGED: 0.22430 -> 0.21053 (RIGHTSIZE 2026-06) — TRIMMED to 2.0% book
                      # (0.095 * 0.21053 = 0.02, -0.4%) to fund the new-name grows. Prior: 0.18182
                      # -> 0.22430 (DECONC-OPT3 2026-06) — was 2.4% book. grid/gas turbines, HOLD
                      # FOREVER (Late but DCA — keep). KEEP-DCA 7.8.
    "CCJ":     2.0,# CHANGED: 0.22430 -> 0.21053 (RIGHTSIZE 2026-06) — TRIMMED to 2.0% book
                      # (-0.4%) to fund the new-name grows. NB: kept (not cut) — it is your ONLY
                      # uranium-MINER exposure (TLN is a power generator, not a miner). Prior:
                      # 0.18182 -> 0.22430 (DECONC-OPT3 2026-06) — was 2.4% book.
                      # uranium leader, HOLD FOREVER. KEEP-DCA 7.3.
    "CEG":     0.0,# CHANGED: 0.12 -> 0.00 — TRIMMED: below 200d / death cross (tech sell
                      # signal overrides thesis, pt 8). Kept at 0% for easy re-add.
    "ETN":     0.0,# CHANGED: 0.18182 -> 0.00 (TLN-CONSOL 2026-06) — CUT. Weakest W2 name
                      # (CONV 5.22, highest risk 5.5, worst PEG 3.11) and redundant with HUBB
                      # (same electrical-equipment exposure). Its 2.0% book consolidated into TLN.
                      # transmission/electrification, DCA. KEEP-DCA 6.3.
    "HUBB":    2.0,# CHANGED: 0.22430 -> 0.21053 (RIGHTSIZE 2026-06) — TRIMMED to 2.0% book
                      # (-0.4%) to fund the new-name grows. Prior: 0.18182 -> 0.22430 (DECONC-OPT3
                      # 2026-06) — was 2.4% book.
                      # transformers / grid gear — 2-4yr lead-times, early-cycle, DCA.
    "TLN":     3.0,# CHANGED: 3.5 -> 3.0 (FICO-ADD 2026-08) — TRIMMED 0.5% to help fund
                      # the new FICO W7 diversifier. Prior: 0.32710 -> 0.36842 (RIGHTSIZE 2026-06) — sub-share recomputed
                      # for the shrunken 9.5% wave; book UNCHANGED at 3.5% (0.095 * 0.36842 = 0.035).
                      # Prior: 0.45455 -> 0.32710 (DECONC-OPT3 2026-06) — was 5.0%
                      # book (0.11 * 0.45455 = 0.05) by absorbing ETN's freed 2.0%. CCJ kept (only
                      # rare-resource/uranium name in the book). Prior: 0.16667 -> 0.27273
                      # (CONV-REBAL 2026-06) — grown to 3.0%
                      # book (0.11 * 0.27273 = 0.03), the wave's top-CONV name (7.11). Talen Energy
                      # — nuclear generation CONTRACTED to data centers. Scores PRIME cycle (GROWTH
                      # 7.7, 8PT 5.07, V 9.4 — cheap + clean). On-thesis for the power wave: it
                      # monetizes the DC power-demand bottleneck directly. CYCLE — power-price/deal
                      # sensitive, buy dips / trim peaks.
    "PWR":     0.0,# CHANGED: 0.1298 -> 0.00 — CUT (REBALANCE 2026-06). Quanta — transmission
                      # contractor. Scores AVOID (GROWTH 4.0): the slowest-growth cyclical in the
                      # wave. Book rotated to TLN (PRIME, on-thesis) + the GEV/CCJ growth. 0% for
                      # easy re-add. CYCLE.
    "OKLO":    0.0,# CHANGED: 0.1039 -> 0.00 — CUT (REBALANCE 2026-06). Pre-revenue SMR.
                      # Scores AVOID with only 30% data coverage [GAP] and F=1.2 — effectively a
                      # blind bet, not a sized punt. Removed until either fundamentals exist or it
                      # earns a true lottery-stub slot. 0% for easy re-add. Catalyst / Binary.
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
    # VALUES ARE DIRECT BOOK % (2026-06 model change): e.g. 2.0 == 2.0% of total book.
    # The trailing "# CHANGED: 0.x ->" notes below are HISTORICAL sub-weight values from the
    # old normalized model; the live number on each line is now a direct percent.
    "VRT":   2.3,# ROUNDED 2026-06: 2.2801 -> 2.3. CHANGED: 0.14664 -> 0.16902 (COHR-CUT 2026-06) — renormalized after
                    # COHR cut to 0% (book ~unchanged at 2.28% since the wave shrank to 13.49%).
                    # Prior: 0.07997 -> 0.14664 (CONV-REBAL 2026-06) — GROWN to 2.27%
                    # book on the CONV gradient (CONV 6.46). Scores AVOID (GROWTH 5.8) but keeps a
                    # strong F=8.0, so trimmed not cut. Liquid cooling leader — CYCLE.
    "ANET":  2.5,# ROUNDED 2026-06: 2.4509 -> 2.5. CHANGED: 0.15762 -> 0.18168 (COHR-CUT 2026-06) — renormalized after
                    # COHR cut (book ~unchanged at 2.45%). Prior: 0.23991 -> 0.15762
                    # (CONV-REBAL 2026-06) — TRIMMED to 2.44%
                    # book on the CONV gradient (CONV 7.06). Still the best business in the wave
                    # (QUALITY 9.6) but its DCA-CONV is mid-pack here, so sized to the gradient.
                    # Arista — DC networking monopoly. 38% margin, $4.4B FCF, software moat. DCA.
    "CRDO":  0.0,# CHANGED: 2.0 -> 0.0 (RESHAPE 2026-08) — CUT. Lowest-CONV name in W3
                    # (CONV 5.02, MOMENTUM) and carries the [PEAK?] flag: its low PEG is
                    # FAKE-CHEAP on peak earnings + an extended chart (the SK-Hynix/Micron
                    # trap). Its ~2.0% book funds SNPS (W1), the higher-conviction EDA name
                    # that also fills the silicon wave's missing chip-design-software leg.
                    # Kept as a 0% stub with its STRATEGY tag for easy re-add if the
                    # hypergrowth thesis re-accelerates off a normal base. CYCLE.
    "COHR":  0.0,# CHANGED: 0.13243 -> 0.00 (COHR-CUT 2026-06) — CUT. Weakest blend in W3
                    # (low upside 6.4 + high risk 5.0, CONV 5.68) and redundant with CRDO/FN/CLS
                    # in optical/interconnect. Its ~2.05% book moved cross-wave to W5 (PLTR/APP).
                    # Coherent — optical; already ran, cyclical. MOMENTUM. CYCLE.
    "FN":    2.2,# ROUNDED 2026-06: 2.2199 -> 2.2. CHANGED: 0.14276 -> 0.16456 (COHR-CUT 2026-06) — renormalized after
                    # COHR cut (book ~unchanged at 2.22%). Prior: 0.21326 -> 0.14276
                    # (CONV-REBAL 2026-06) — TRIMMED to 2.21%
                    # book on the CONV gradient (CONV 6.27).
                    # Fabrinet — optical contract mfr; cleanest growth-at-reasonable-price name
                    # (QUALITY quadrant, 8PT 5.11, net cash). CYCLE / Mid.
    "ALAB":  0.0,# CHANGED: 2.0 -> 0.0 (RESHAPE 2026-08) — CUT. Second-lowest CONV in W3
                    # (CONV 5.12, MOMENTUM) with the binding risk on VALUATION (V 2.2): most
                    # stretched name held, ~118x fwd P/E, fails 8-Point #6 (priced for
                    # perfection). It is also redundant — the book already holds 5+ AI-
                    # connectivity/interconnect names in this wave. Its ~2.0% book rotates
                    # cross-wave to the RHM.DE defense diversifier (W7), swapping an
                    # expensive momentum semi for a tech-uncorrelated sector. Kept as a 0%
                    # stub with its STRATEGY tag for easy re-add. Astera Labs — CXL/PCIe
                    # retimers, highest-beta name in the sleeve. CYCLE / Mid.
    "CLS":   2.5,# ROUNDED 2026-06: 2.5112 -> 2.5. CHANGED: 0.16150 -> 0.18615 (COHR-CUT 2026-06) — renormalized after
                    # COHR cut + absorbs the tiny rounding residual (book ~unchanged at 2.51%).
                    # Prior: 0.09366 -> 0.16150 (CONV-REBAL 2026-06) — GROWN to 2.50%
                    # book, the gradient CEILING (top CONV 7.27 in the wave). Celestica — EMS for
                    # hyperscalers. Scores PRIME (CONV 7.27, GROWTH 7.6, 8PT 5.14) with
                    # the CHEAPEST valuation in the whole DC-infra sleeve (V 8.1): AI-
                    # datacenter exposure (custom 400G/800G networking + compute) at a
                    # hardware multiple. Sized at ~1.5% (not full ~2%) on POSITION RISK
                    # the scorer can't see: customer concentration (a few hyperscalers
                    # drive most CCS revenue — its own version of the PLTR concentration
                    # worry) and thin EMS margins (less cushion if volumes fall). The
                    # binding layer is CYC (cyclical capex). Clean on-thesis fit next to
                    # ANET/CRDO/COHR. CYCLE / Mid-Late — buy dips, trim into strength.
}

# --- WAVE 4: HYPERSCALER CLOUD (10% book) ---
# UNZEROED 2026-06 (W4-FUNDING): the wave was at 0% book ("held passively
# elsewhere"); restored to a 10% anchor sleeve because the scorer flags these as
# the highest-CONV DCA names on the whole board (every layer healthy, V often
# 10.0 — the cheapest large-cap quality available) AND the single best
# diversifier off the silicon-heavy book. Six EQUAL ~1.667%-book slots. NFLX
# promoted from the watchlist as the 6th name: a streaming DCA compounder (CONV
# 8.14), off-thesis vs the five cloud/AI-infra mega-caps but the same dca
# operating mode and a real consumer-internet diversifier. Funded by a pro-rata
# x0.84 trim of every other tradeable wave (SMHV held fixed at 37.5% book).
W4_CLOUD_TARGETS = {
    # VALUES ARE DIRECT BOOK % (2026-06 model change): e.g. 2.0 == 2.0% of total book.
    # The trailing "# CHANGED: 0.x ->" notes below are HISTORICAL sub-weight values from the
    # old normalized model; the live number on each line is now a direct percent.
    "MSFT":  2.0,# CHANGED: 0.17871 -> 0.18165 (RIGHTSIZE 2026-06) — set to 2.0% book
                    # (0.1101 * 0.18165 = 0.02, -0.25%). Azure + OpenAI.
                    # Cloud anchor, every layer >=5.9. CONV 7.97. dca.
    "GOOG":  0.0,# ZEROED 2026-06: 0.01 stub -> 0.0. CHANGED: 0.00079 -> 0.00091 (RIGHTSIZE 2026-06) — sub-share up (wave
                    # shrank); book UNCHANGED at the 0.01% stub. Prior: 0.16679 -> 0.00074
                    # (ORCL-CONSOL 2026-06) — cut to the stub; its ~2.24% reallocated to ORCL.
                    # Kept as an easy-re-add stub, not deleted. Gemini + TPU + Cloud. CONV 7.50.
                    # Class C (non-voting) — swapped from GOOGL 2026-06: same business, cheaper share.
    "AMZN":  2.0,# CHANGED: 0.17792 -> 0.18165 (RIGHTSIZE 2026-06) — set to 2.0% book
                    # (-0.24%). AWS + retail. CONV 7.15 (lowest in wave). dca.
    "META":  2.0,# CHANGED: 0.17871 -> 0.18165 (RIGHTSIZE 2026-06) — set to 2.0% book
                    # (-0.25%). Open models + ad-AI. V 10.0 (dead cheap). CONV 8.50. dca.
    "ORCL":  3.0,# CHANGED: 0.28515 -> 0.27248 (RIGHTSIZE 2026-06) — TRIMMED to 3.0% book
                    # (0.1101 * 0.27248 = 0.03, -0.59%) to fund the new-name grows. Prior: 0.33284
                    # -> 0.28515 (DECONC-OPT3 2026-06) — was 3.59% book.
                    # #1 DCA on the board (V 10.0, CONV 8.73, PEG 0.69, fastest cloud growth). dca.
    "NFLX":  2.0,# CHANGED: 0.17871 -> 0.18165 (RIGHTSIZE 2026-06) — set to 2.0% book
                    # (-0.25%). Streaming (Netflix) — scale + ad-tier +
                    # password monetization, FCF inflecting up. Quality DCA, CONV 8.14. dca.
}

# --- WAVE 5: AI SOFTWARE / APPS (8.83%) ---
# CHANGED (2026-06): AXON MOVED IN from W6, kept dca. A profitable public-safety
# SaaS monopoly (59% gross margin, sticky recurring revenue) is an application-
# layer name and belongs here, not in the speculative tail. It joins at its
# unchanged ~0.5% book; the existing names were renormalized so their book values
# are UNCHANGED (the wave grew by exactly AXON's book).
# Prior (growth-max pass): SNOW MOVED OUT to CRDO (W3) — weakest software name;
# four profitable anchors remain (PANW/CRWD/NOW/DDOG); PLTR & S kept at 0%.
W5_SOFTWARE_TARGETS = {
    # VALUES ARE DIRECT BOOK % (2026-06 model change): e.g. 2.0 == 2.0% of total book.
    # The trailing "# CHANGED: 0.x ->" notes below are HISTORICAL sub-weight values from the
    # old normalized model; the live number on each line is now a direct percent.
    "S":     0.0,# CUT. Only GAAP-UNPROFITABLE top-10 name (net income -$319M TTM,
                    # never had a profitable year); FCF-positive but turnaround unproven.
                    # Kept at 0% for easy re-add if the GAAP turn completes.
    "PANW":  0.0,# ZEROED 2026-06: 0.01 stub -> 0.0. CHANGED: 0.00113 -> 0.00102 (RIGHTSIZE 2026-06) — sub-share moved only
                    # because the wave grew to 9.82%; book UNCHANGED at the 0.01% stub. Security
                    # platform — biggest, cheapest, steadiest, but scores RICH (RICHNESS 0.90,
                    # CONV 3.02 — lowest DCA on the board): too extended to keep real book. Easy
                    # re-add once it de-rates. DCA.
    "CRWD":  0.0,# ZEROED 2026-06: 0.01 stub -> 0.0. CHANGED: 0.00113 -> 0.00102 (RIGHTSIZE 2026-06) — held at the 0.01%-
                    # book stub (sub-share moved only because the wave grew). AI cybersecurity.
                    # Scores RICH (RICHNESS 0.81, CONV 3.72) — same logic as PANW. Easy re-add. DCA.
    "NOW":   2.0,# CHANGED: 0.22676 -> 0.20367 (RIGHTSIZE 2026-06) — sub-share recomputed
                    # for the grown 9.82% wave; book UNCHANGED at 2.00% (0.0982 * 0.20367 = 0.020).
                    # Still a co-anchor with AXON. The best-value DCA name on
                    # the board: QUALITY 8.2 with RICHNESS 0.00 (cheapest possible on the gate),
                    # 22x fwd / 0.89 PEG, down ~50% on the year. Workflow AI (Now Assist),
                    # profitable. KEEP-DCA.
    "ZS":    0.0,# CHANGED: 0.1782 -> 0.00 — CUT (REBALANCE 2026-06). Zscaler scores AVOID
                    # (GROWTH 2.0) — the weakest software name held. Book rotated to NOW/AXON.
                    # 0% for easy re-add if the growth re-accelerates. CYCLE.
    "AXON":  2.4,# CHANGED: 0.27211 -> 0.24440 (RIGHTSIZE 2026-06) — sub-share recomputed for
                    # the grown 9.82% wave; book UNCHANGED at 2.4% (0.0982 * 0.24440 = 0.024).
                    # Prior: 0.30691 -> 0.27211 (PEGA-ADD 2026-06). Earlier: 0.28490 -> 0.30691 (DECONC-OPT3 2026-06).
                    # Co-anchor with NOW. Public-safety
                    # SaaS monopoly — 59% gross margin, sticky recurring revenue (evidence.com,
                    # Draft One AI), end-market that doesn't cycle. QUALITY 8.5, KEEP-DCA. Thin
                    # net/FCF is reinvestment by choice; hold through dips.
    "PLTR":  1.5,# CHANGED: 0.17007 -> 0.15275 (RIGHTSIZE 2026-06) — sub-share recomputed
                    # for the grown 9.82% wave; book UNCHANGED at 1.5% (0.0982 * 0.15275 = 0.015).
                    # Prior: 0.19182 -> 0.17007 (PEGA-ADD 2026-06). Earlier: 0.00199 -> 0.21368 (COHR-CUT 2026-06) — PROMOTED from the
                    # 0.01% stub to a 1.5% book starter, funded by the
                    # cross-wave move of COHR's freed weight. The HIGHEST-UPSIDE name on the whole
                    # board (upside 9.6, CONV 8.25, PRIME, F 10.0 / V 8.1 / C 6.4) — the business
                    # scores elite. Sized at a STARTER (not full) on POSITION RISK the scorer can't
                    # see: US-gov customer concentration (declining but still the larger base),
                    # Europe/France data-sovereignty pushback capping the international TAM, and a
                    # priced-for-perfection multiple (~60x+ sales) where a single lumpy gov quarter
                    # de-rates it. Bought into weakness as planned, never chased. CYCLE — trim/add.
    "APP":   1.9,# CHANGED: 0.21542 -> 0.19348 (RIGHTSIZE 2026-06) — sub-share recomputed for
                    # the grown 9.82% wave; book UNCHANGED at 1.9% (0.0982 * 0.19348 = 0.019).
                    # Prior: 0.24297 -> 0.21542 (PEGA-ADD 2026-06). Earlier: 0.19881 -> 0.21368 (COHR-CUT 2026-06). AppLovin: AXON AI ad engine, the
                    # most profitable grower benchmarked against the held book (64% net margin, 35%
                    # fwd rev, PEG 0.69 — cheaper than PLTR for comparable growth). SIZED as a
                    # starter on POSITION RISK the scorer can't see: single-engine adtech (one
                    # algorithm), P/S ~24 priced-for-perfection, regulatory/privacy tail. Same
                    # convex-bet discipline as PLTR — grow only on weakness. CYCLE — trim into strength.
    "SNOW":  0.0,# CHANGED: 0.1904 -> 0.00 — MOVED to CRDO (W3) on growth-max pass.
                    # Healed bubble hangover but slowest forecast of the survivors.
    "DDOG":  0.0,# CHANGED: 0.1602 -> 0.00 — CUT (REBALANCE 2026-06). AI observability.
                    # Scores AVOID (GROWTH 3.7) — weakest of the observability/sw cluster. Book
                    # rotated to NOW/AXON. 0% for easy re-add. CYCLE.
    "PEGA":  2.0,# CHANGED: 0.11338 -> 0.20367 (RIGHTSIZE 2026-06) — GROWN 1.0% -> 2.0% book
                    # (0.0982 * 0.20367 = 0.020), the conviction-set target (CONV 8.29 KEEP-DCA).
                    # Prior: NEW (PEGA-ADD 2026-06) — 1.0% book DCA starter,
                    # funded cross-wave from the halved W6 speculative tail. Pegasystems —
                    # enterprise AI workflow/decisioning (agentic-AI on a 40yr BPM/CRM base).
                    # Scores KEEP-DCA (CONV 8.22, QUALITY 8.1, RICHNESS 0.00 — maximally cheap on
                    # the gate): PE 16 / fwd 10.7, P/S 3.0, elite ROE 52% / ROIC 52%, strong FCF,
                    # de-rated ~-43% / -36% below 200DMA. The cheap-VALUE counterweight to the
                    # expensive growth names in the wave (PLTR P/S 49, APP P/S 24) and a diversifier
                    # off the AI-capex factor. Slower top-line (ttm rev +3.5%) is the trade-off —
                    # sized as ballast, not a growth kicker. DCA — buy on schedule.
}

# --- WAVE 6: SPECULATIVE / SECOND-ORDER (5.5%) ---
# CHANGED (2026-06): AXON MOVED OUT to W5 — it was the lone hold-forever DCA name
# in the speculative sleeve (a profitable public-safety SaaS monopoly belongs in
# AI Software/Apps, not the convex tail). The wave shrank by AXON's ~0.5% book;
# the four survivors (TMDX/IONQ/RKLB/SYM) were renormalized so their book values
# are UNCHANGED. Prior: wave grown 3% -> 6% to give IONQ (+175% mid) and RKLB
# (+171%) real ~1.0% slots alongside TMDX 2.5% (profitable, uncorrelated).
# These are the portfolio's convex tail — small absolute size, large payoff skew.
W6_SPEC_TARGETS = {
    # VALUES ARE DIRECT BOOK % (2026-06 model change): e.g. 2.0 == 2.0% of total book.
    # The trailing "# CHANGED: 0.x ->" notes below are HISTORICAL sub-weight values from the
    # old normalized model; the live number on each line is now a direct percent.
    "TMDX":  0.8,# ROUNDED 2026-06: 0.75 -> 0.8. CHANGED: 0.375 -> 0.21429 (RIGHTSIZE 2026-06) — sub-share recomputed for
                      # the grown 3.5% wave; book UNCHANGED at 0.75% (0.035 * 0.21429 = 0.0075).
                      # Prior: 0.25 -> 0.375 (PEGA/INOD-FUND 2026-06). Earlier: 0.50 -> 0.25 (CONV-REBAL 2026-06).
                      # MedTech organ-transport, profitable, off-radar, non-AI diversifier. QUALITY
                      # quadrant (8PT 5.34). TOP-10 name.
    # --- AXON MOVED 2026-06 to W5 (AI Software/Apps), kept dca. It is a profitable
    #     monopoly, not a speculative punt; it never fit the convex-tail sleeve. ---
    "IONQ":  0.5,# CHANGED: 0.25 -> 0.14286 (RIGHTSIZE 2026-06) — sub-share recomputed for
                      # the grown 3.5% wave; book UNCHANGED at 0.5% (0.035 * 0.14286 = 0.005).
                      # Prior: 0.50 -> 0.25 (ALNY-ADD 2026-06). Still a wave anchor and a well-graded
                      # punt: PRIME catalyst (GROWTH 6.5, 8PT 6.28, C 8.5). Quantum revenue leader;
                      # +175% mid (highest forecast). Catalyst/convex.
    "ALNY":  2.0,# CHANGED: 0.25 -> 0.57143 (RIGHTSIZE 2026-06) — GROWN 0.5% -> 2.0% book
                      # (0.035 * 0.57143 = 0.02), now the tail's anchor — its CONV 8.23 PRIME is by
                      # far the highest-graded name in W6 (F 9.0 / V 9.7). Prior: NEW (ALNY-ADD
                      # 2026-06) — 0.5% book catalyst starter. Alnylam — RNAi therapeutics platform
                      # scaling to profitability; binary on label-expansion / readout catalysts.
                      # Off-thesis vs the AI tail (a biotech), but the same convex-bet discipline:
                      # size on data, never average down. CATALYST / Binary.
    "RKLB":  0.0,# ZEROED 2026-06: 0.01 stub -> 0.0. CHANGED: 0.005 -> 0.00286 (RIGHTSIZE 2026-06) — sub-share moved only
                      # because the wave grew; book UNCHANGED at the 0.01% stub (0.035 * 0.00286 =
                      # 0.0001). Prior: 0.125 -> 0.005 (RKLB-CUT 2026-06) — CUT to a 0.01% book stub.
                      # Scores AVOID (GROWTH 4.6); the
                      # asymmetric space punt is parked, not grown. Kept as an easy-re-add stub,
                      # not deleted. Space/autonomy. Catalyst — size once, no avg down.
    "SYM":   0.0,# CHANGED: 0.2 -> 0.0 (RESHAPE 2026-08) — CUT. Lowest-CONV holding on the
                      # entire board (CONV 3.85, AVOID): GAAP-unprofitable (net -$28M TTM,
                      # fails 8-Point #2) + lumpy/customer-concentrated (Walmart). Its tiny
                      # 0.24% book helps fund the new NBIX diversifier (W7). Kept as a 0%
                      # stub with its STRATEGY tag for easy re-add if it turns profitable.
                      # Symbotic — warehouse/logistics robotics (physical-AI). CATALYST / Binary.
    "CRCL":  0.0,  # Circle (USDC) — held windfall (147 shares), TARGET 0%. Parked to
                      # track/manage down, NOT to add to. Catalyst.
    "LEU":   0.0,  # Centrus Energy — HALEU/uranium enrichment for advanced reactors
                      # (SMR fuel-supply bottleneck). TARGET 0% — watch-only stub so it
                      # shows in the basket; re-size if the enrichment thesis firms up.
                      # Catalyst / Binary (policy/contract-driven, pre-scale economics).
}

# --- WAVE 7: DIVERSIFIERS (7%) — OFF the AI value chain (NEW 2026-06) ---
# These two names deliberately break the book's single-factor bet on AI capex.
# Everything in W1-W6 rises and falls with the same AI-infrastructure cycle; a
# capex air-pocket would hit all of them at once. LLY (pharma) and NU (LatAm
# fintech) are uncorrelated to that cycle, so they are the structural hedge that
# most improves multi-year, drawdown-adjusted compounding. They live in a
# SEPARATE sleeve so the AI wave taxonomy (W1-W6) stays clean — they are NOT an
# AI thesis and should not be read as one.
#   LLY  — KEEP-DCA (QUALITY 9.2, RICHNESS 0.19): the incretin (tirzepatide ->
#          orforglipron) compounder; growth driver runs to ~2036+ patents.
#   NU   — PRIME cycle (GROWTH 7.7, 8PT 6.22): every layer >=8, the best-balanced
#          PRIME name on the whole board. Digital bank, EM-consumer cyclical.
#   RDDT — QUALITY cycle (CONV 7.66, no layer <8: F8.2/V10.0/C8.0): social ad
#          ramp + AI data-licensing optionality. NOT a chip — an AI-economy play
#          that diversifies the silicon-heavy book. Early, high-beta.
W7_DIVERSIFY_TARGETS = {
    # VALUES ARE DIRECT BOOK % (2026-06 model change): e.g. 2.0 == 2.0% of total book.
    # The trailing "# CHANGED: 0.x ->" notes below are HISTORICAL sub-weight values from the
    # old normalized model; the live number on each line is now a direct percent.
    "LLY":   2.0,# CHANGED: 0.29762 -> 0.22472 (RIGHTSIZE 2026-06) — TRIMMED to 2.0% book
                      # (0.089 * 0.22472 = 0.02, -0.5%) to fund the new-name grows. Prior: 0.33784
                      # -> 0.29762 (INOD-ADD 2026-06). Eli Lilly — pharma compounder, fully
                      # uncorrelated to AI capex. KEEP-DCA. Watch: orforglipron Phase 3 + mfg build.
    "NU":    2.5,# CHANGED: 0.29762 -> 0.28090 (RIGHTSIZE 2026-06) — sub-share recomputed
                      # for the grown 8.9% wave; book UNCHANGED at 2.5% (0.089 * 0.28090 = 0.025).
                      # Prior: 0.33784 -> 0.29762 (INOD-ADD 2026-06). Nubank — LatAm digital bank. PRIME cycle, every
                      # layer strong. EM-consumer/credit cyclical — buy dips, trim manias.
    "RDDT":  2.4,# CHANGED: 0.28571 -> 0.26966 (RIGHTSIZE 2026-06) — sub-share recomputed
                    # for the grown 8.9% wave; book UNCHANGED at 2.4% (0.089 * 0.26966 = 0.024).
                    # Prior: 0.32432 -> 0.28571 (INOD-ADD 2026-06) — grown to 2.4% book.
                      # Reddit — social ads + AI data-licensing (selling 20y of human conversation
                      # to LLM labs). Scores CONV 7.66 (3rd-highest cycle name on the board) with
                      # NO binding layer below 8.0 (F8.2/V10.0/C8.0): cheap, not extended, good
                      # business — a rare triple. Funded by the SIMO cut. A non-semi AI-economy
                      # play that diversifies the silicon-heavy book. CYCLE / Early — high-beta,
                      # young public co; buy dips, trim manias.
    "INOD":  1.5,# CHANGED: 2.0 -> 1.5 (FICO-ADD 2026-08) — TRIMMED 0.5% to help fund
                      # the new FICO W7 diversifier (net-zero within W7). Prior: 0.11905 -> 0.22472 (RIGHTSIZE 2026-06) — GROWN 1.0% -> 2.0% book
                      # (0.089 * 0.22472 = 0.02), the conviction-set target (CONV 7.25 PRIME).
                      # Prior: NEW (INOD-ADD 2026-06) — 1.0% book cycle starter,
                      # funded cross-wave from the halved W6 speculative tail. Innodata — AI data
                      # engineering (annotation / LLM training-data prep) selling into the labs'
                      # capex. Scores the HIGHEST conviction of the new names (CONV 8.47, PRIME):
                      # profitable + net-cash ($113M, D/E 0.03), high-ROIC (171%), 42% gross / 14%
                      # net margin, FCF +$62M, margin trajectory turned -15% -> +13%. A non-semi
                      # AI-supply-chain diversifier next to LLY/NU/RDDT. High-beta (2.83); analyst
                      # 3Y rev a modest 11% (decel off a hypergrowth base) but Strong Buy, PT +60%.
                      # CYCLE / Early — buy dips, trim manias.
    "FICO":  2.0,# NEW (FICO-ADD 2026-08) — 2.0% book, funded 1.0% from BESI.AS (W1),
                      # 0.5% from TLN (W2), 0.5% from INOD (W7). Fair Isaac — credit-scoring
                      # near-monopoly (the FICO score is embedded in ~90% of US lending
                      # decisions) + ML-native fraud/decision analytics (Falcon, bank-specific
                      # AI models). Off the AI-capex value chain: revenue tracks lending
                      # volumes + score pricing, NOT the GPU buildout — a structural hedge for
                      # the silicon-heavy book, like LLY/NU. Scores the HIGHEST conviction on
                      # the board (CONV 8.98): F 8.5 / V 9.6 / q10 9.3, 85% gross / 34% net,
                      # accelerating revenue, screened CHEAP (PEG 0.75, ~24% below 200DMA).
                      # DCA / hold-forever. RISK: single-product concentration + regulatory /
                      # VantageScore overhang on mortgage-score pricing (the reason it's cheap).
    "NBIX":  1.5,# NEW (RESHAPE 2026-08) — 1.5% book, funded by the SYM cut (W6) + part of
                      # the ALAB cut (W3). Neurocrine — Ingrezza-led neuroscience pharma. The
                      # HIGHEST-CONV non-held name on the whole board (CONV 8.61, beaten only
                      # by FICO among held names): steady ~20-30% revenue, net margin expanding
                      # 8->21%, a dirt-cheap 0.35 PEG, already profitable. A NEW therapeutic
                      # area (CNS/neuroscience) the book has zero exposure to, and a far LESS
                      # binary pharma name than the W6 catalyst punts (a real earnings stream,
                      # not a readout lottery). Off the AI-capex value chain — a structural
                      # diversifier like LLY/FICO. DCA — hold-forever quality compounder.
    "RHM.DE": 1.2,# NEW (RESHAPE 2026-08) — 1.2% book, funded by the rest of the ALAB cut
                      # (W3). Rheinmetall — European defense leader. Adds a whole TECH-
                      # UNCORRELATED sector the book lacks: revenue tracks multi-year gov't
                      # rearmament backlogs, not the GPU/AI-capex cycle every other wave rides.
                      # ACCELERATING (trailing rev 13->29%, forecasts toward 40%+) at a cheap
                      # 0.7 PEG; CONV 7.82 PRIME. The trade-off vs the ALAB semi it replaces:
                      # lower margin (~7% net, defense manufacturing) but a genuine new risk
                      # factor instead of a 6th AI-connectivity name. CYCLE / Mid — the cycle
                      # here is a structural spending super-cycle, so buy dips, trim manias.
    "PODD":  2.0,# NEW (RESHAPE-TRIM 2026-08) — 2.0% book, funded by the SMHV.SW trim
                      # (37.5->32.5%). Insulet (Omnipod) — the tubeless-insulin-pump half of a
                      # new HEALTH-CARE leg (pairs with the diabetes/GLP-1 tailwind behind LLY).
                      # CONV 8.50: steady ~20-30% revenue, net margin inflecting up hard
                      # (0->10->20%), and trading ~28% BELOW its 200-day (a growing, margin-
                      # expanding business on a pullback). Off the AI-capex chain. DCA.
    "WPM":   1.5,# NEW (RESHAPE-TRIM 2026-08) — 1.5% book, funded by the SMHV.SW trim.
                      # Wheaton Precious Metals — gold/silver STREAMING (royalty model, not a
                      # miner: ~65% net margin, no operating/dev risk). The book's ONLY
                      # precious-metals exposure — a commodity hedge uncorrelated to tech, with
                      # gold as its own risk driver. CONV 7.84. NB commodity-cyclical: revenue
                      # swings with the metal price (history -11..+80%), so this is a hedge/
                      # diversifier, not a smooth compounder. CYCLE — buy dips, trim manias.
    "AJG":   1.5,# NEW (RESHAPE-TRIM 2026-08) — 1.5% book, funded by the SMHV.SW trim.
                      # Arthur J. Gallagher — insurance BROKER (fee-based, not underwriting).
                      # The defensive FINANCIALS leg the book lacked: recession-resistant mid-
                      # teens compounding, zero correlation to the AI-capex cycle. CONV 7.57.
                      # A ballast holding — low drama, steady reward. DCA — hold-forever.
    "ONON":  1.5,# NEW (RESHAPE-TRIM 2026-08) — 1.5% book, funded by a further SMHV.SW
                      # trim (32.5 -> 31.0%). On Holding — premium running shoes/apparel. The
                      # book's ONLY consumer-brand / discretionary name — maximum diversification
                      # value (a whole new demand driver, uncorrelated to tech/AI-capex). CONV
                      # 8.24 AND a genuinely CHEAP entry: V 10.0 on PEG 0.81 / P/S 3.2, trading
                      # ~7% BELOW its 200-day. ~30% revenue growth, FCF+. DCA — hold-forever.
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
    "ADI":       "dca",     # Analog Devices — analog/industrial silicon, quality compounder; hold forever (NB: cyclical, a drop is a discount)
    "SNPS":      "dca",     # NEW (RESHAPE 2026-08). Synopsys — EDA chip-design duopoly (w/ CDNS); recurring/subscription, metronomic ~15% growth, hold forever. Closes the design-layer gap left by the CDNS cut.

    # --- W2 POWER ---
    "GEV":     "dca",       # Grid supercycle — hold forever
    "CCJ":     "dca",       # Uranium structural deficit — hold forever
    "ETN":     "dca",       # Transmission/electrification — quality compounder, hold forever
    "HUBB":    "dca",       # Transformers/grid gear — 2-4yr lead-times, quality, hold forever
    "CEG":     "cycle",     # Nuclear utility — power-price sensitive
    # CUT: ABBN.SW (was "dca") — only overvalued name (analysts -13%), slowest ballast;
    #      book split to FN (W3) + NOW (W5). Re-add here + in W2_POWER_TARGETS if restored.
    "PWR":     "cycle",     # CUT to 0% (REBALANCE 2026-06, AVOID G4.0) — tag kept for re-add
    "TLN":     "cycle",     # NEW 2026-06: Talen — nuclear power contracted to data centers; PRIME cycle, on-thesis. Buy dips, trim peaks
    "OKLO":    "catalyst",  # CUT to 0% (REBALANCE 2026-06, AVOID + 30% data) — tag kept for re-add
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
    "CLS":     "cycle",     # Celestica — hyperscaler EMS; cheapest DC-infra name (V 9.3) but customer-concentrated + thin margins. Buy dips, trim strength.
    "S":       "cycle",     # SentinelOne — AI-native cyber, just-turned-profitable; buy dips, trim at peak
    # REMOVED from basket (kept commented for easy re-add — see W3_DCINFRA_TARGETS):
    #   "FIX":     "cycle",     # +2206% — late-cycle DC construction (removed)

    # --- W4 CLOUD (purest DCA wave) ---
    "MSFT":    "dca",       # Hold forever compounder
    "GOOG":    "dca",       # Hold forever compounder (Class C, swapped from GOOGL 2026-06)
    "AMZN":    "dca",       # Hold forever
    "META":    "dca",       # Hold forever
    "ORCL":    "dca",       # Cloud-capacity compounder
    "NFLX":    "dca",       # Streaming compounder — promoted from watchlist 2026-06 into W4

    # --- W5 SOFTWARE ---
    "PANW":    "dca",       # Profitable platform — hold forever
    "CRWD":    "dca",       # Profitable platform, ~$1.9B FCF — hold forever
    "NOW":     "dca",       # Profitable (+13% GAAP, $5.1B FCF) — hold forever
    "ZS":      "cycle",     # Zscaler — zero-trust/SASE cyber; washed-out, FCF+ but GAAP-light; buy dips
    "AXON":    "dca",       # MOVED from W6 (2026-06). Public-safety monopoly — 59% gross margin,
                            # sticky SaaS; thin net/FCF is reinvestment by choice, not weak
                            # economics. End-market doesn't cycle -> hold through dips.
    "SNOW":    "dca",       # FCF-positive, healed bubble hangover
    "PEGA":    "dca",       # NEW (2026-06). Pegasystems — enterprise AI workflow/decisioning; cheap quality compounder (PE 16, ROIC 52%), buy on schedule
    "PLTR":    "cycle",     # Best business but 62x sales — trim/add, not blind DCA
    "APP":     "cycle",     # NEW (2026-06). AppLovin AI ad engine — high momentum/beta, single-
                            # engine adtech at ~24x sales. Trim into strength, never chase. CYCLE.
    "DDOG":    "cycle",     # Consumption model — buy dips, trim momentum spikes

    # --- W6 SPECULATIVE ---
    "TMDX":    "cycle",     # MedTech growth — momentum-sensitive
    "IONQ":    "catalyst",  # Quantum binary — size once, event-driven, no avg down
    "ALNY":    "catalyst",  # NEW (2026-06). Alnylam RNAi — biotech binary on label-expansion/readouts; size on data, no avg down
    "RKLB":    "catalyst",  # Space — size once, milestone-driven, no avg down
    "SYM":     "catalyst",  # Symbotic — robotics, GAAP-unprofitable + lumpy; size once, no avg down
    "CRCL":    "catalyst",  # Circle — held windfall, target 0%; manage down, never avg in
    "LEU":     "catalyst",  # Centrus — HALEU enrichment, policy/contract-driven; watch-only 0%

    # --- W7 DIVERSIFIERS (off the AI value chain) ---
    "LLY":     "dca",       # Eli Lilly — pharma compounder (tirzepatide/orforglipron), hold forever; uncorrelated to AI capex
    "NU":      "cycle",     # Nubank — LatAm digital bank; EM-consumer/credit cyclical, buy dips / trim manias
    "RDDT":    "cycle",     # Reddit — social ads + AI data-licensing; non-semi AI diversifier, Early/high-beta, buy dips / trim manias
    "INOD":    "cycle",     # NEW (2026-06). Innodata — AI data-engineering / LLM training-data prep; non-semi AI-supply-chain diversifier, Early/high-beta, buy dips / trim manias
    "FICO":    "dca",       # NEW (2026-08). Fair Isaac — credit-scoring near-monopoly; off the AI-capex value chain, hold-forever quality compounder, a drop is a discount
    "NBIX":    "dca",       # NEW (RESHAPE 2026-08). Neurocrine — Ingrezza-led neuroscience pharma; off the AI-capex value chain, profitable + cheap (PEG 0.35), hold-forever compounder, a drop is a discount
    "RHM.DE":  "cycle",     # NEW (RESHAPE 2026-08). Rheinmetall — European defense; tech-uncorrelated, rides a structural rearmament super-cycle, buy dips / trim manias
    "PODD":    "dca",       # NEW (RESHAPE-TRIM 2026-08). Insulet (Omnipod) — insulin pumps; new health-care leg, ~25% growth + expanding margins, hold-forever compounder, a drop is a discount
    "WPM":     "cycle",     # NEW (RESHAPE-TRIM 2026-08). Wheaton — gold/silver streaming; the book's only precious-metals hedge, commodity-cyclical, buy dips / trim manias
    "AJG":     "dca",       # NEW (RESHAPE-TRIM 2026-08). Arthur J. Gallagher — insurance broker; defensive financials ballast, recession-resistant mid-teens compounder, a drop is a discount
    "ONON":    "dca",       # NEW (RESHAPE-TRIM 2026-08). On Holding — premium footwear/apparel; the book's only consumer-brand leg, ~30% growth, cheap entry (V 10.0), hold-forever compounder, a drop is a discount
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
    ("W7_DIVERSIFY", W7_DIVERSIFY_TARGETS),
]

# =========================================================================
# WAVE-LEVEL TARGET WEIGHTS — AUTO-DERIVED (do not hand-edit)
# =========================================================================
# As of the 2026-06 model change, baskets hold DIRECT book percentages
# (e.g. "AMZN": 2.0 == 2.0% of book). The wave weight is simply the sum of its
# tickers, expressed as a FRACTION of total book (e.g. W1 == 0.4378) to keep the
# same semantics every downstream consumer already expects. Edit a ticker's
# number in its basket and this follows automatically.
TARGET_WEIGHTS = {
    name: sum(basket.values()) / 100.0
    for name, basket in ALL_BASKETS
}


def verify_allocations():
    """Assert the per-ticker book percentages total 100%, the derived wave
    weights total 1.0, and every holding has a valid strategy classification.

    NOTE (2026-06 model change): baskets now hold DIRECT book percentages
    (e.g. "AMZN": 2.0 == 2.0% of book), and TARGET_WEIGHTS is auto-derived as
    the per-wave sum / 100. So the invariant is on the GRAND total across all
    baskets (= 100%), not on each basket individually. Tolerance is loosened to
    1e-6 because the numbers are now hand-edited percentages, not machine-
    normalized sub-weights."""
    book_total = sum(sum(b.values()) for _, b in ALL_BASKETS)
    assert abs(book_total - 100.0) < 1e-6, f"Book doesn't sum to 100% (got {book_total})"
    assert abs(sum(TARGET_WEIGHTS.values()) - 1.0) < 1e-6, "Wave weights don't sum to 100%"
    valid_modes = {"dca", "cycle", "catalyst"}
    all_tickers = set()
    for name, basket in ALL_BASKETS:
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
    "MU": {
        "pos":      "Mid",
        "cagr":     (10, 30),
        "strategy": "cycle",
        "area":     "Memory / DRAM+HBM (Micron) — LARGE",
        "note":     "Held INDIRECTLY — SMHV's #1 holding (~14.3% of the ETF, "
                    "~5.4% of book). HBM/DRAM supercycle leader; same memory "
                    "cycle as SK Hynix. Deep-cyclical commodity — buy dips, trim "
                    "near peak. Listed here so the look-through book% renders.",
    },
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
    # NB: ADI promoted to a held W1 DCA pick (see W1_SILICON_TARGETS) — removed here.
    #     Took the slot CDNS vacated (~1.47% book). Highest-quality name in the book.

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
    "ON": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (8, 26),
        "area":     "Power semis — EV + industrial (ON Semiconductor)",
        "note":     "Cyclical-trough recovery: rev bottomed after -15% downcycle, now "
                    "re-accelerating (+8% rev / +32% EPS off the trough), 40% gross "
                    "margin, FCF+. But fwd P/E ~38 (trough-depressed E) and avg analyst "
                    "target sits BELOW price — recovery already partly priced. Real-moat "
                    "power-semi franchise; the return is in the NEXT up-cycle, not 12mo.",
    },
    "SMCI": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (10, 30),
        "area":     "AI server hardware / integration (Super Micro)",
        "note":     "High-octane AI-server box builder: rev +80% this year, fwd P/E only "
                    "~12 — cheap on headline. BUT gross margin collapsing (18%->8%) and "
                    "FCF -$5.5B (buying revenue with margin + working capital). Low-moat "
                    "assembler, Hold consensus, bimodal targets (-53% to +83%). High-risk "
                    "cycle punt, NOT a quality compounder.",
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
    # SNPS PROMOTED (RESHAPE 2026-08) to W1_SILICON_TARGETS at 1.5% book (funded
    #     by the CRDO cut) — it closes the chip-design (EDA) gap the CDNS removal
    #     left uncovered. Removed from WATCHLIST; re-add here if it is ever cut to 0%.
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
    "KEEL": {
        "pos":      "Binary",
        "cagr":     (-30, 40),
        "strategy": "lottery",
        "area":     "BTC mining pivoting to HPC/AI datacenters (Keel Infrastructure)",
        "note":     "SKIP/lottery — same profile as CIFR: a bitcoin miner bolting on "
                    "an HPC/AI-datacenter narrative. Deeply UNPROFITABLE (net margin "
                    "~-121% TTM), microcap, +ve rev off a tiny base (ttm +52%) but "
                    "erratic history. Crypto-correlated beta is new uncorrelated risk, "
                    "not AI diversification. Binary punt — size tiny, never average down.",
    },
    "ONDS": {
        "pos":      "Binary",
        "cagr":     (-35, 45),
        "strategy": "lottery",
        "area":     "Autonomous drones + rail/industrial wireless (Ondas)",
        "note":     "SKIP/lottery — pre-scale dual play (Ondas Autonomous Systems "
                    "drones + Ondas Networks rail wireless). Explosive % rev (ttm "
                    "+793%) is pure base effect off a microcap revenue line; still "
                    "deeply UNPROFITABLE with lumpy, contract-dependent orders. "
                    "All-or-nothing on defense/rail adoption — binary, size tiny.",
    },
    "BULL": {
        "pos":      "Mid",
        "cagr":     (8, 25),
        "strategy": "cycle",
        "area":     "Online brokerage / trading platform (Webull)",
        "note":     "Retail-brokerage SPAC — rev +47% but margins swing around "
                    "breakeven (net ~-3% TTM, positive in some years), so earnings "
                    "track the retail-trading cycle, not a secular AI bottleneck. "
                    "Off-thesis (fintech, not AI value-chain) and pre-consistent-"
                    "profit. Cyclical: watch-only, accumulate on risk-off washouts.",
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
    "POWL": {
        "pos":      "Mid",
        "cagr":     (8, 18),
        "strategy": "cycle",
        "area":     "Power / electrical switchgear (Powell Industries)",
        "note":     "Profitable switchgear maker riding data-center + grid orders; "
                    "real earnings and backlog, not a story stock. Capex-cyclical — "
                    "buy dips, trim into the buildout peak.",
    },
    "FIX": {
        "pos":      "Mid",
        "cagr":     (10, 20),
        "strategy": "cycle",
        "area":     "Datacenter HVAC + electrical buildout (Comfort Systems)",
        "note":     "Mechanical/electrical contractor levered to data-center "
                    "construction; profitable with a large backlog. Late-ish cycle — "
                    "buy dips, sell into the capex peak.",
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
    "NVDA": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 35),
        "area":     "AI accelerators (Nvidia) — LARGE",
        "note":     "AI-capex bellwether; owned indirectly via SMHV.SW. Cycle/Mid — "
                    "trim into the capex peak, not hold-forever.",
    },
    "AVGO": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (12, 22),
        "area":     "Custom AI silicon + networking (Broadcom) — LARGE",
        "note":     "AI ASIC + VMware software annuity, fat FCF, dividend grower. "
                    "Quality compounder; overlaps SMHV.SW.",
    },
    "TSM": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (15, 25),
        "area":     "Leading-edge foundry (Taiwan Semi) — LARGE",
        "note":     "Whole AI supply chain depends on it; near-monopoly at the leading "
                    "edge. Geopolitical tail risk the only knock.",
    },
    "AMD": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (15, 35),
        "area":     "GPU/CPU #2 (AMD) — LARGE",
        "note":     "MI-series share-gainer vs NVDA; high beta to the same capex wave. "
                    "Cyclical, trim at peak. Overlaps SMHV.SW.",
    },
    "ASML": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (12, 25),
        "area":     "EUV litho monopoly (ASML) — LARGE",
        "note":     "Sole EUV supplier — deepest bottleneck in the stack. WFE-cyclical "
                    "(China + memory). Buy dips, trim at peak.",
    },
    "MRVL": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 35),
        "area":     "Custom AI silicon + optical DSP (Marvell)",
        "note":     "Custom-compute + electro-optics levered to hyperscaler capex. "
                    "ELITE business (F 9.7, highest in the DC-infra complex) but a "
                    "BAD entry right now: CONV 5.78, binding CYC 3.0 (extended + "
                    "crowded), V 4.0 (expensive), fails 8PT discipline (4.15). Also "
                    "REDUNDANT with AVGO/CRDO/COHR/ALAB already held — same AI-"
                    "connectivity factor, no new exposure. Watch-only: re-rate when "
                    "the chart cools (CYC recovers) and it isn't a 5th correlated "
                    "cyclical. High-beta; accumulate on a real dip, not here.",
    },
    "MPWR": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (15, 28),
        "area":     "Power-management IC for AI servers (Monolithic Power)",
        "note":     "Power delivery into GPU boards — high-margin, capex-levered. "
                    "Cyclical, quality; accumulate on dips.",
    },
    "GFS": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8, 20),
        "area":     "Specialty foundry (GlobalFoundries)",
        "note":     "Trailing-edge/specialty nodes (auto, RF, power). Cheaper, less "
                    "AI-direct than TSM; cyclical auto+industrial demand.",
    },
    "ENTG": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (10, 22),
        "area":     "Semicap materials/purity (Entegris)",
        "note":     "Consumable materials + filtration — picks-and-shovels WFE with "
                    "recurring revenue. Cyclical but stickier than tools.",
    },
    "TSLA": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (10, 35),
        "area":     "EV + autonomy/robotics (Tesla) — LARGE",
        "note":     "Auto-cyclical today, robotaxi/Optimus optionality tomorrow. "
                    "Valuation prices the optionality; high-beta cycle.",
    },
    "CRM": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (9, 16),
        "area":     "Enterprise SaaS / CRM (Salesforce) — LARGE",
        "note":     "Agentforce AI upsell on a huge installed base. Mature, FCF-rich, "
                    "cheaper than peers. DCA-grade compounder.",
    },
    "ADBE": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (9, 16),
        "area":     "Creative + document SaaS (Adobe) — LARGE",
        "note":     "Firefly GenAI on a wide moat; de-rated on AI-disruption fear, now "
                    "cheap-but-quality. DCA.",
    },
    "INTU": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (12, 18),
        "area":     "Fintech SaaS (Intuit) — LARGE",
        "note":     "TurboTax/QuickBooks + AI assistant; durable SMB lock-in, high "
                    "margins. Quality DCA, rarely cheap.",
    },
    "SNOW": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (20, 40),
        "area":     "Data cloud (Snowflake)",
        "note":     "Consumption-model data platform riding the AI data wave; improving "
                    "margins. Held? no — monitor for cycle add.",
    },
    "MDB": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (18, 35),
        "area":     "Developer database (MongoDB)",
        "note":     "Atlas cloud growth + AI app backends. Just-turning-profitable, "
                    "high-beta; cycle/Early.",
    },
    "FTNT": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 18),
        "area":     "Network security (Fortinet)",
        "note":     "Firewall + SASE, self-funded FCF machine, hardware-refresh "
                    "cyclicality. Quality DCA at a fair price.",
    },
    "CYBR": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 30),
        "area":     "Identity security (CyberArk)",
        "note":     "Privileged-access + machine-identity leader; secular identity "
                    "tailwind. Cycle/Mid, accumulate on dips.",
    },
    "TTD": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 30),
        "area":     "Ad-tech DSP (The Trade Desk)",
        "note":     "Open-internet ad buying + CTV; AI-optimized bidding. High-beta to "
                    "ad cycle; trim at peak.",
    },
    "SHOP": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 32),
        "area":     "Commerce platform (Shopify)",
        "note":     "Merchant GMV + payments; consumer-cyclical but secular SMB "
                    "e-commerce. Cycle/Mid.",
    },
    # APP (AppLovin) PROMOTED to held 2026-06 — moved into W5_SOFTWARE_TARGETS at
    # 1.0% book (funded from NOW+AXON). Removed from the watchlist so it isn't
    # double-listed; re-add here if it is ever cut back to 0%.
    "HUBS": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (14, 22),
        "area":     "SMB marketing SaaS (HubSpot)",
        "note":     "AI Breeze upsell, durable SMB CRM. Quality growth, rarely cheap; "
                    "DCA on weakness.",
    },
    "WDAY": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (12, 18),
        "area":     "HR/finance SaaS (Workday)",
        "note":     "Sticky enterprise back-office suite + AI agents. Mature, FCF-rich. "
                    "DCA.",
    },
    "TEAM": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (16, 26),
        "area":     "Dev collaboration SaaS (Atlassian)",
        "note":     "Jira/Confluence cloud migration + AI (Rovo). Founder-led, "
                    "high-beta; cycle/Mid.",
    },
    "GTLB": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (20, 35),
        "area":     "DevSecOps platform (GitLab)",
        "note":     "Single-app DevSecOps + AI (Duo). Small, high-growth, "
                    "near-breakeven; cycle/Early.",
    },
    "V": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 15),
        "area":     "Payment network (Visa) — LARGE",
        "note":     "Toll-booth on global card spend; ~50% margins, "
                    "recession-resilient. Premier DCA compounder.",
    },
    "MA": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (11, 16),
        "area":     "Payment network (Mastercard) — LARGE",
        "note":     "Same toll-booth model as Visa with a slightly faster growth tilt. "
                    "DCA.",
    },
    "FI": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 16),
        "area":     "Merchant acquiring (Fiserv/Clover)",
        "note":     "Clover POS growth + payments scale; cheaper than networks. "
                    "Cheap-but-quality DCA.",
    },
    "ADYEY": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 30),
        "area":     "Payments platform (Adyen)",
        "note":     "Single-platform global acquiring; high incremental margins. "
                    "Growth-cyclical to consumer spend; cycle/Mid.",
    },
    "XYZ": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (12, 28),
        "area":     "Fintech / Cash App (Block)",
        "note":     "Cash App + Square ecosystem, BTC optionality. Consumer-cyclical, "
                    "execution-gated; cycle/Mid.",
    },
    "HOOD": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (15, 40),
        "area":     "Retail brokerage (Robinhood)",
        "note":     "Crypto + options + cash sweep; highly sensitive to retail risk "
                    "appetite and rates. High-beta cycle.",
    },
    "SOFI": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (18, 40),
        "area":     "Digital bank (SoFi)",
        "note":     "Bank-charter lending + tech platform; rate- and credit-cyclical. "
                    "Cycle/Early, volatile.",
    },
    # NU — PROMOTED to held (W7 Diversifiers, 2026-06 rebalance). Removed from
    #      the watchlist; see W7_DIVERSIFY_TARGETS + STRATEGY.
    "COIN": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (10, 45),
        "area":     "Crypto exchange (Coinbase)",
        "note":     "Levered to crypto volume + price; revenue swings violently with "
                    "the cycle. High-beta cycle, trim into mania.",
    },
    # LLY — PROMOTED to held (W7 Diversifiers, 2026-06 rebalance). Removed from
    #      the watchlist; see W7_DIVERSIFY_TARGETS + STRATEGY.
    "ISRG": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (12, 18),
        "area":     "Surgical robotics (Intuitive Surgical) — LARGE",
        "note":     "da Vinci installed-base razor/blade model; secular procedure "
                    "growth. Quality DCA, rarely cheap.",
    },
    "UNH": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 15),
        "area":     "Managed care (UnitedHealth) — LARGE",
        "note":     "Integrated insurer + Optum; de-rated on regulatory/cost fears — "
                    "cheap-but-quality value. DCA.",
    },
    "CLOV": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (10, 25),
        "area":     "Medicare Advantage insurer (Clover Health) — small-cap",
        "note":     "MA insurer turnaround: rev ~$2.2B, FCF+ ($55M ttm), net cash, "
                    "no debt — but GAAP-unprofitable (-2.6% net = op margin, no "
                    "distortion) and high-beta (2.42). Cheap on sales (P/S 1.0) with "
                    "fwd rev ~24% / EPS ramp; margin trajectory improving. Speculative "
                    "small-cap, ad/MCR-cycle sensitive — buy dips, size small.",
    },
    "TMO": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (8, 14),
        "area":     "Life-science tools (Thermo Fisher) — LARGE",
        "note":     "Picks-and-shovels for pharma/biotech R&D; bioprocessing cycle "
                    "bottoming. DCA value.",
    },
    "DHR": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (8, 14),
        "area":     "Life-science / diagnostics (Danaher)",
        "note":     "Bioprocessing + diagnostics, recurring consumables. De-rated, "
                    "cheap-but-quality. DCA.",
    },
    "VRTX": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 18),
        "area":     "Biotech (Vertex)",
        "note":     "CF monopoly + non-opioid pain (Journavx) + pipeline. Profitable, "
                    "durable; quality DCA.",
    },
    "CRSP": {
        "strategy": "catalyst",
        "pos":      "Binary",
        "cagr":     (-25, 45),
        "area":     "Gene editing (CRISPR Therapeutics)",
        "note":     "Casgevy launch + pipeline; binary on commercial ramp and trial "
                    "readouts. Catalyst — never average down.",
    },
    "NTLA": {
        "strategy": "catalyst",
        "pos":      "Binary",
        "cagr":     (-30, 45),
        "area":     "In-vivo gene editing (Intellia)",
        "note":     "Pre-commercial CRISPR; binary on pivotal data + first approvals. "
                    "Catalyst sizing only.",
    },
    "HIMS": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 40),
        "area":     "Telehealth (Hims & Hers)",
        "note":     "DTC telehealth + compounded GLP-1; regulatory + competitive risk. "
                    "High-beta cycle.",
    },
    "GE": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 16),
        "area":     "Aerospace engines (GE Aerospace) — LARGE",
        "note":     "Commercial-engine aftermarket annuity; secular air-travel growth. "
                    "Quality industrial DCA.",
    },
    "RTX": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (8, 13),
        "area":     "Defense + aerospace (RTX) — LARGE",
        "note":     "Pratt engines + missiles/defense backlog. Cheap-but-quality, "
                    "dividend. DCA.",
    },
    "LMT": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (6, 11),
        "area":     "Defense prime (Lockheed Martin)",
        "note":     "F-35 + missiles backlog; cheap, high-yield defensive ballast. Slow "
                    "DCA value.",
    },
    "PH": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (9, 15),
        "area":     "Motion/flow control (Parker Hannifin)",
        "note":     "Diversified industrial with aerospace mix; serial compounder. DCA.",
    },
    "ROK": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8, 16),
        "area":     "Factory automation (Rockwell)",
        "note":     "Industrial automation + reshoring; capex-cyclical. Cycle/Mid, buy "
                    "dips.",
    },
    "DE": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (6, 14),
        "area":     "Ag + construction machinery (Deere)",
        "note":     "Precision-ag autonomy optionality on a deep ag-cycle trough. "
                    "Cyclical value; cycle/Mid.",
    },
    "VST": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8, 25),
        "area":     "Power merchant (Vistra)",
        "note":     "Nuclear + gas fleet levered to AI-datacenter power demand + power "
                    "prices. Late-ish cycle; trim at peak.",
    },
    "NRG": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8, 22),
        "area":     "Integrated power (NRG Energy)",
        "note":     "Retail + generation levered to power-price upcycle and DC demand. "
                    "Cyclical; cycle/Mid.",
    },
    # TLN — PROMOTED to held (W2 Power, 2026-06 rebalance). Removed from the
    #      watchlist; see W2_POWER_TARGETS + STRATEGY.
    "FSLR": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (10, 25),
        "area":     "Solar manufacturing (First Solar)",
        "note":     "US thin-film solar with IRA tailwind + policy risk. "
                    "Capex/policy-cyclical; cycle/Mid.",
    },
    "ENPH": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (10, 30),
        "area":     "Solar microinverters (Enphase)",
        "note":     "Residential solar, rate-sensitive demand; deeply cyclical and "
                    "beaten down. Cycle, high-beta.",
    },
    "XOM": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (4, 9),
        "area":     "Integrated oil major (Exxon) — LARGE",
        "note":     "Cheap, high-yield commodity ballast; buybacks. Slow DCA value, "
                    "commodity-cyclical underneath.",
    },
    "FCX": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (6, 20),
        "area":     "Copper miner (Freeport-McMoRan)",
        "note":     "Copper levered to electrification + datacenter buildout; classic "
                    "deep-cyclical. Cycle, trim at peak.",
    },
    "ALB": {
        "strategy": "cycle",
        "pos":      "Late",
        "cagr":     (5, 30),
        "area":     "Lithium (Albemarle)",
        "note":     "Lithium trough play; EV-demand + price cyclical, currently "
                    "depressed. Cyclical value; cycle.",
    },
    "LIN": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (8, 13),
        "area":     "Industrial gases (Linde) — LARGE",
        "note":     "Wide-moat industrial gas oligopoly with contracted volumes. "
                    "Premier defensive DCA.",
    },
    "COST": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (9, 14),
        "area":     "Membership warehouse (Costco) — LARGE",
        "note":     "Membership-fee annuity + traffic moat; recession-resilient. "
                    "Quality DCA, perennially pricey.",
    },
    "WMT": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (7, 12),
        "area":     "Retail + ads/commerce (Walmart) — LARGE",
        "note":     "Scale moat + high-margin ad/membership flywheel. Defensive DCA "
                    "compounder.",
    },
    "MELI": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 30),
        "area":     "LatAm e-commerce + fintech (MercadoLibre)",
        "note":     "Dominant LatAm commerce + Mercado Pago; EM-cyclical, high-growth. "
                    "Cycle/Mid.",
    },
    "SBUX": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (7, 13),
        "area":     "Coffee retail (Starbucks)",
        "note":     "Turnaround on a durable brand; de-rated, cheap-but-quality. DCA "
                    "value.",
    },
    "NKE": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (7, 13),
        "area":     "Athletic apparel (Nike)",
        "note":     "Beaten-down brand-moat turnaround; cheap vs history. DCA value, "
                    "execution-gated.",
    },
    "CMG": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (12, 18),
        "area":     "Fast-casual restaurants (Chipotle)",
        "note":     "Unit-growth + pricing power; high-quality, premium multiple. DCA "
                    "on weakness.",
    },
    "PG": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (5, 9),
        "area":     "Consumer staples (Procter & Gamble) — LARGE",
        "note":     "Brand-moat defensive ballast, dividend king. Slow DCA, low beta.",
    },
    "KO": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (5, 9),
        "area":     "Beverages (Coca-Cola) — LARGE",
        "note":     "Defensive staple, pricing power, dividend aristocrat. Low-beta DCA "
                    "ballast.",
    },
    # NFLX (Netflix) PROMOTED 2026-06 into W4_CLOUD_TARGETS at ~1.667% book (a 6th
    # equal slot in the unzeroed cloud sleeve). Streaming DCA compounder, CONV 8.14.
    # Removed from the watchlist so it isn't double-listed.
    "SPOT": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (15, 28),
        "area":     "Audio streaming (Spotify)",
        "note":     "Price hikes + margin expansion on a huge user base. "
                    "Growth-cyclical; cycle/Mid.",
    },
    # RDDT (Reddit) PROMOTED 2026-06 to W7_DIVERSIFY_TARGETS at ~2.0% book (the
    # SIMO->RDDT rotation). Removed from the watchlist so it isn't double-listed.
    "DASH": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 30),
        "area":     "Delivery marketplace (DoorDash)",
        "note":     "Category-leading delivery + new verticals; consumer-cyclical. "
                    "Cycle/Mid.",
    },
    "ABNB": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 18),
        "area":     "Travel marketplace (Airbnb)",
        "note":     "Asset-light travel platform, strong FCF; travel-cyclical. Quality "
                    "DCA on dips.",
    },
    "UBER": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 28),
        "area":     "Mobility + delivery (Uber)",
        "note":     "Profitable network-effect platform + AV optionality. "
                    "Consumer-cyclical; cycle/Mid.",
    },
    "QSI": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-40, 50),
        "area":     "Quantum sensing/sequencing (Quantum-Si)",
        "note":     "Micro-cap protein-sequencing lottery; tiny revenue, cash-burn. "
                    "Pure asymmetric punt — size minimal or skip.",
    },
    "LAES": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-40, 55),
        "area":     "Post-quantum security (SEALSQ)",
        "note":     "PQC-crypto + semiconductor micro-cap; hype-driven, deeply "
                    "unprofitable. Lottery — size minimal.",
    },
    "ARQQ": {
        "strategy": "lottery",
        "pos":      "Binary",
        "cagr":     (-40, 55),
        "area":     "Quantum-safe encryption (Arqit)",
        "note":     "Pre-scale quantum encryption micro-cap; going-concern risk. "
                    "Lottery punt only.",
    },
    "PL": {
        "strategy": "catalyst",
        "pos":      "Binary",
        "cagr":     (-30, 40),
        "area":     "Earth-observation satellites (Planet Labs)",
        "note":     "Data-subscription space play; binary on enterprise/defense "
                    "contract ramp + cash burn. Catalyst sizing.",
    },
    "BKSY": {
        "strategy": "catalyst",
        "pos":      "Binary",
        "cagr":     (-35, 45),
        "area":     "Radar imaging satellites (BlackSky)",
        "note":     "Defense/intel imaging; binary on contract wins + constellation "
                    "funding. Catalyst — never average down.",
    },
    "STLD": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (4, 16),
        "area":     "Steel mini-mill (Steel Dynamics)",
        "note":     "Low-cost steel levered to reshoring/construction; deep-cyclical, "
                    "cheap. Cycle, buy troughs.",
    },
    "NUE": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (4, 15),
        "area":     "Steel (Nucor)",
        "note":     "Best-in-class steel cyclical; cheap at mid-cycle, dividend. "
                    "Cycle/Mid, buy weakness.",
    },
    "CAT": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (6, 14),
        "area":     "Construction/mining machinery (Caterpillar) — LARGE",
        "note":     "Global capex bellwether + datacenter/power gensets. Cyclical "
                    "quality; cycle/Mid.",
    },
    "UNP": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (6, 11),
        "area":     "Class-I railroad (Union Pacific)",
        "note":     "Wide-moat rail oligopoly, pricing power. Cyclical-defensive DCA, "
                    "dividend.",
    },
    "WM": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (7, 12),
        "area":     "Waste management (Waste Management)",
        "note":     "Local-monopoly waste + recycling; inflation pass-through. "
                    "Defensive DCA compounder.",
    },
    "ELF": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (15, 30),
        "area":     "Mass cosmetics (e.l.f. Beauty)",
        "note":     "Share-gaining value beauty brand; consumer-cyclical, "
                    "momentum-rich. Cycle/Mid.",
    },
    "CELH": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (15, 35),
        "area":     "Energy drinks (Celsius)",
        "note":     "High-growth energy-drink share gainer; distribution-cyclical, "
                    "volatile. Cycle/Mid.",
    },
    "DKNG": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 35),
        "area":     "Online sports betting (DraftKings)",
        "note":     "US OSB/iGaming duopoly scaling to profitability; "
                    "consumer-cyclical. Cycle/Mid.",
    },
    "ANF": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (6, 18),
        "area":     "Apparel retail (Abercrombie)",
        "note":     "Brand-turnaround retailer, cheap, momentum; deeply "
                    "consumer-cyclical. Cycle, volatile.",
    },
    "TOST": {
        "strategy": "cycle",
        "pos":      "Early",
        "cagr":     (18, 35),
        "area":     "Restaurant fintech (Toast)",
        "note":     "POS + payments for restaurants, scaling profitability; "
                    "SMB-cyclical. Cycle/Early.",
    },
    "DOCS": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (14, 22),
        "area":     "Healthcare SaaS network (Doximity)",
        "note":     "Profitable physician network + pharma ads; high-margin, niche "
                    "moat. Quality DCA/cycle.",
    },
    "9988.HK": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8, 22),
        "area":     "China cloud + commerce (Alibaba)",
        "note":     "Cheap China megacap + AI-cloud re-acceleration; regulatory/geo "
                    "risk. Deep-value cycle.",
    },
    "0700.HK": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 18),
        "area":     "China gaming + fintech (Tencent)",
        "note":     "Wide-moat games + WeChat + AI; cheap vs growth, geo risk. "
                    "DCA/value for China sleeve.",
    },
    "SAP": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (10, 16),
        "area":     "Enterprise ERP cloud (SAP) — LARGE",
        "note":     "ERP cloud migration + AI (Joule); durable, FCF-rich EU megacap. "
                    "DCA.",
    },
    "NVO": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (8, 18),
        "area":     "Pharma / GLP-1 (Novo Nordisk)",
        "note":     "Ozempic/Wegovy franchise; de-rated on competition — "
                    "cheap-but-quality. DCA value.",
    },
    "SHEL": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (4, 9),
        "area":     "Integrated energy (Shell)",
        "note":     "Cheap, high-yield European energy ballast; buybacks. Slow DCA "
                    "value, commodity-cyclical.",
    },
    "INFY": {
        "strategy": "dca",
        "pos":      "Mid",
        "cagr":     (7, 13),
        "area":     "IT services (Infosys)",
        "note":     "AI-services + cheap, high-ROIC EM IT outsourcer; dividend. DCA "
                    "value, demand-cyclical.",
    },
    "9618.HK": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (8, 18),
        "area":     "China e-commerce + logistics (JD.com)",
        "note":     "Cheap China commerce/logistics; consumer + geo cyclical. "
                    "Deep-value cycle.",
    },

    # =====================================================================
    # BROAD SCREEN (2026-06) — candidates beyond the core AI value chain.
    # Added on owner request. These widen the watchlist into adjacent and
    # off-thesis sectors (healthcare, financials, miners, defense, consumer,
    # energy). Tentative tags only — NOT held, do not affect any weight.
    # cagr bands are rough forward 3-5Y estimates for screening, not
    # forecasts. Refine pos/cagr/note before promoting any name into a wave.
    # Names already present upstream (Block=XYZ, Alibaba=9988.HK, JD=9618.HK,
    # and ~29 overlaps) were dropped to avoid duplicates.
    # =====================================================================
    "FSLY": {"strategy": "cycle",    "pos": "Mid",      "cagr": (3, 28),
             "area": "Edge cloud / CDN (Fastly)",
             "note": "Edge compute platform; execution-challenged, washed-out. "
                     "Speculative cyclical recovery, not a compounder."},
    "ESTC": {"strategy": "cycle",    "pos": "Mid",      "cagr": (10, 22),
             "area": "Search / analytics + vector (Elastic)",
             "note": "Search + vector-DB layer for RAG/AI. Profitable-ish, "
                     "consumption model; buy dips."},
    "MSTR": {"strategy": "catalyst", "pos": "Binary",   "cagr": (-40, 60),
             "area": "Bitcoin treasury vehicle (MicroStrategy)",
             "note": "Leveraged BTC proxy via convertible debt. Outcome is the "
                     "BTC cycle + financing — Binary. Size tiny, never avg down."},
    "AISP": {"strategy": "catalyst", "pos": "Binary",   "cagr": (-50, 80),
             "area": "Edge-AI defense video surveillance (Airship AI)",
             "note": "Micro-cap, contract-dependent. Binary on defense awards + "
                     "funding. Lottery-grade punt — size tiny, never avg down."},
    "PATH": {"strategy": "cycle",    "pos": "Mid",      "cagr": (8, 25),
             "area": "AI-native RPA (UiPath)",
             "note": "Robotic process automation pivoting to agentic AI. "
                     "Turnaround cyclical — buy dips on execution proof."},
    "DUOL": {"strategy": "dca",      "pos": "Mid",      "cagr": (18, 30),
             "area": "Consumer LLM-localized learning app (Duolingo)",
             "note": "Gamified learning monetizing LLM features; high growth, "
                     "FCF+. Quality consumer compounder."},
    "U":    {"strategy": "cycle",    "pos": "Mid",      "cagr": (5, 28),
             "area": "RT3D engine / spatial compute (Unity)",
             "note": "Real-time 3D engine; post-reset turnaround, lumpy. "
                     "Cyclical recovery bet — buy dips."},
    "PYPL": {"strategy": "dca",      "pos": "Mid",      "cagr": (6, 14),
             "area": "Payments turnaround (PayPal)",
             "note": "Cheap value with large FCF; margin/branded-checkout "
                     "turnaround. DCA-grade value compounder."},

    # --- Semis, Specialized Silicon & Equipment ---
    "POWI": {"strategy": "cycle",    "pos": "Mid",      "cagr": (8, 20),
             "area": "High-voltage gate drivers (Power Integrations)",
             "note": "HV drivers for energy infra; cyclical analog. Buy dips."},
    "DIOD": {"strategy": "cycle",    "pos": "Mid",      "cagr": (6, 18),
             "area": "Discrete/analog silicon (Diodes Inc)",
             "note": "Auto/industrial discretes; deep-cyclical analog. "
                     "Buy trough, trim peak."},
    "COHU": {"strategy": "cycle",    "pos": "Early/Mid","cagr": (5, 25),
             "area": "Back-end test handlers (Cohu)",
             "note": "Semi test/handling, thermal subsystems; early-cycle "
                     "back-end. High-beta — buy dips."},
    "FORM": {"strategy": "cycle",    "pos": "Mid",      "cagr": (8, 22),
             "area": "Probe cards (FormFactor)",
             "note": "Advanced probe cards for HBM/HD silicon verification; "
                     "bottleneck-adjacent. CYCLE."},
    "AEIS": {"strategy": "cycle",    "pos": "Mid",      "cagr": (8, 20),
             "area": "Precision power for etch/depo (Advanced Energy)",
             "note": "Plasma power conversion for WFE; cyclical equipment. "
                     "Buy dips with the WFE cycle."},
    "MKSI": {"strategy": "cycle",    "pos": "Mid",      "cagr": (6, 18),
             "area": "Vacuum/laser subsystems (MKS Instruments)",
             "note": "Subsystems for advanced nodes; levered to WFE cycle + "
                     "debt. Cyclical — buy dips."},
    "UMC":  {"strategy": "cycle",    "pos": "Mid/Late", "cagr": (2, 12),
             "area": "Mature-node foundry (United Microelectronics)",
             "note": "Commodity mature-node foundry; deep-cyclical, low-growth. "
                     "Trough-buy only."},
    "ASX":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (5, 15),
             "area": "OSAT / advanced packaging (ASE Technology)",
             "note": "Global OSAT leader; advanced packaging tailwind but "
                     "cyclical/commodity. Buy dips. (Was listed as ASEH.)"},
    "TSEM": {"strategy": "cycle",    "pos": "Mid",      "cagr": (6, 18),
             "area": "Analog/RF specialty foundry (Tower Semi)",
             "note": "Specialty analog/RF foundry; cyclical. Buy dips."},

    # --- Hardware, Datacenter Infrastructure & Optics ---
    "NTAP": {"strategy": "dca",      "pos": "Mid",      "cagr": (4, 12),
             "area": "Enterprise data storage (NetApp)",
             "note": "Storage management; FCF+, dividend. Slow DCA-grade, "
                     "AI-data tailwind optional."},
    "PSTG": {"strategy": "cycle",    "pos": "Mid",      "cagr": (10, 22),
             "area": "All-flash arrays for AI (Pure Storage)",
             "note": "High-perf flash for AI clusters; growthier cyclical. "
                     "Buy dips."},
    "HPQ":  {"strategy": "dca",      "pos": "Late",     "cagr": (2, 8),
             "area": "PC/print client devices (HP Inc)",
             "note": "Defensive value; AI-PC refresh optional upside. "
                     "Low-growth DCA/value, high yield."},
    "DELL": {"strategy": "cycle",    "pos": "Mid",      "cagr": (8, 18),
             "area": "Tier-1 AI server integrator (Dell)",
             "note": "Scale liquid-cooled AI servers; thin-margin integrator, "
                     "cyclical. Buy dips, watch margin."},
    "LITE": {"strategy": "cycle",    "pos": "Mid",      "cagr": (10, 28),
             "area": "Optical components (Lumentum)",
             "note": "Short-reach AI optics; cyclical optical supplier. "
                     "Buy dips with the optics cycle."},
    "CIEN": {"strategy": "cycle",    "pos": "Mid",      "cagr": (6, 18),
             "area": "Coherent optical transport (Ciena)",
             "note": "DC-interconnect + telco transport; lumpy cyclical. "
                     "Buy dips."},
    "BDC":  {"strategy": "dca",      "pos": "Mid",      "cagr": (6, 14),
             "area": "Industrial networking / cabling (Belden)",
             "note": "High-speed data cabling for industrial/DC; steady "
                     "compounder. DCA-grade."},
    # CLS (Celestica) PROMOTED 2026-06 to W3_DCINFRA_TARGETS as a 0% held re-add
    # candidate (see basket). Removed from the watchlist so it isn't double-listed.
    "JBL":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (8, 18),
             "area": "Electronics manufacturing (Jabil)",
             "note": "Diversified EMS/lifecycle mfg; cyclical, buyback-driven. "
                     "Buy dips. (Was listed as JABIL.)"},
    "SANM": {"strategy": "cycle",    "pos": "Mid",      "cagr": (5, 15),
             "area": "Integrated mfg (Sanmina)",
             "note": "EMS for defense/computing; cyclical, modest growth. "
                     "Buy dips."},
    "EMR":  {"strategy": "dca",      "pos": "Mid",      "cagr": (8, 15),
             "area": "Process automation + cooling controls (Emerson)",
             "note": "Automation + liquid-cooling valves; quality industrial "
                     "compounder. DCA-grade."},
    "GRMN": {"strategy": "dca",      "pos": "Mid",      "cagr": (6, 12),
             "area": "Proprietary hardware / GPS telemetry (Garmin)",
             "note": "High-margin niche hardware; net cash, steady. "
                     "DCA-grade compounder."},

    # --- Grid Electrification, Utilities & Materials ---
    "NEE":  {"strategy": "dca",      "pos": "Mid",      "cagr": (6, 12),
             "area": "Clean-energy generation (NextEra)",
             "note": "Largest renewables + regulated utility; secular grid "
                     "demand. DCA-grade."},
    "SO":   {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 9),
             "area": "Nuclear/gas base-load utility (Southern Co)",
             "note": "Regulated base-load; new nuclear online. Slow DCA yield "
                     "compounder."},
    "DUK":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 8),
             "area": "Regulated grid utility (Duke Energy)",
             "note": "Large regulated grid; DC-load tailwind. Slow DCA yield."},
    "SRE":  {"strategy": "dca",      "pos": "Mid",      "cagr": (6, 10),
             "area": "Regulated infra + LNG (Sempra)",
             "note": "Regulated T&D tracking industrial demand. DCA-grade."},
    "LNT":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 8),
             "area": "Regulated utility (Alliant Energy)",
             "note": "Solid regulated compounder; DC pipeline. Slow DCA yield."},
    "HON":  {"strategy": "dca",      "pos": "Mid",      "cagr": (6, 12),
             "area": "Industrial + building controls (Honeywell)",
             "note": "Diversified high-margin industrial; steady. DCA-grade."},
    "MMM":  {"strategy": "dca",      "pos": "Late",     "cagr": (2, 8),
             "area": "Diversified manufacturing (3M)",
             "note": "Deep-value turnaround, high yield, litigation overhang. "
                     "DCA/value — slow."},
    "URI":  {"strategy": "cycle",    "pos": "Mid/Late", "cagr": (6, 15),
             "area": "Equipment rental (United Rentals)",
             "note": "Industrial fleet leasing; construction-cycle proxy. "
                     "CYCLE — buy dips, trim at peak."},
    "EME":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (10, 20),
             "area": "Electrical/mechanical construction (EMCOR)",
             "note": "DC + electrification contractor; backlog-driven cyclical. "
                     "Buy dips."},
    "MYRG": {"strategy": "cycle",    "pos": "Early/Mid","cagr": (8, 20),
             "area": "Transmission-line contractor (MYR Group)",
             "note": "Specialized grid T&D contractor; early-cycle build. "
                     "High-beta — buy dips."},
    "FLR":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (6, 18),
             "area": "Engineering / infra constructor (Fluor)",
             "note": "Macro EPC for energy/infra; lumpy cyclical. Buy dips."},

    # --- Aerospace, Sovereignty & Defense Infrastructure ---
    "NOC":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 11),
             "area": "Strategic bombers / space (Northrop)",
             "note": "Long-cycle strategic programs (B-21) + space. DCA-grade "
                     "defense prime."},
    "GD":   {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 11),
             "area": "Marine + land combat systems (General Dynamics)",
             "note": "Subs/combat vehicles + Gulfstream. Durable backlog. "
                     "DCA-grade."},
    "HWM":  {"strategy": "dca",      "pos": "Mid",      "cagr": (10, 18),
             "area": "Jet-engine component castings (Howmet)",
             "note": "Aero structural castings; aftermarket-rich. Quality "
                     "compounder — DCA-grade."},
    "TDG":  {"strategy": "dca",      "pos": "Mid",      "cagr": (10, 16),
             "area": "Proprietary aero aftermarket (TransDigm)",
             "note": "High-margin sole-source aftermarket parts; serial "
                     "compounder (levered). DCA-grade."},
    "PDD":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (10, 25),
             "area": "Cross-border value commerce (PDD / Temu)",
             "note": "High-growth value marketplace; China + trade risk. "
                     "Cyclical-growth — buy dips."},

    # --- Secular Healthcare, MedTech & Biopharma Ballast ---
    "AMGN": {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 10),
             "area": "Biologics platform (Amgen)",
             "note": "Large biologic base + obesity optionality. DCA-grade "
                     "yield compounder."},
    "GILD": {"strategy": "dca",      "pos": "Mid",      "cagr": (4, 9),
             "area": "Anti-viral cash generator (Gilead)",
             "note": "Cheap, high-yield, HIV/oncology. DCA/value."},
    "BMY":  {"strategy": "dca",      "pos": "Late",     "cagr": (2, 8),
             "area": "Oncology portfolio (Bristol Myers)",
             "note": "Washed-out, patent-cliff overhang, high yield. "
                     "DCA/value — slow."},
    "PFE":  {"strategy": "dca",      "pos": "Late",     "cagr": (2, 8),
             "area": "Diversified pharma (Pfizer)",
             "note": "Depressed post-COVID value, high yield, pipeline doubts. "
                     "DCA/value."},
    "SYK":  {"strategy": "dca",      "pos": "Mid",      "cagr": (8, 13),
             "area": "Orthopedics / hospital tech (Stryker)",
             "note": "Dominant ortho + hospital ecosystem. DCA-grade "
                     "compounder."},
    "MDT":  {"strategy": "dca",      "pos": "Mid",      "cagr": (4, 9),
             "area": "Diversified medical devices (Medtronic)",
             "note": "Broad device portfolio, high yield, steady. DCA-grade. "
                     "(Tag was 'mca' in the source list — read as dca.)"},
    "BSX":  {"strategy": "dca",      "pos": "Mid",      "cagr": (10, 16),
             "area": "Interventional medtech (Boston Scientific)",
             "note": "High-growth cardio/interventional. Quality compounder — "
                     "DCA-grade."},

    # --- Financial Networks & Commodity Infrastructure ---
    "JPM":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 10),
             "area": "Fortress bank franchise (JPMorgan)",
             "note": "Best-in-class diversified bank. DCA-grade, rate/credit "
                     "cyclical underneath."},
    "GS":   {"strategy": "cycle",    "pos": "Mid",      "cagr": (5, 14),
             "area": "Investment bank / markets (Goldman Sachs)",
             "note": "Capital-markets cyclical; earnings swing with the cycle. "
                     "Buy dips, trim booms."},
    "MS":   {"strategy": "cycle",    "pos": "Mid",      "cagr": (5, 12),
             "area": "Wealth mgmt + IB (Morgan Stanley)",
             "note": "Wealth-management scale + cyclical IB. Buy dips."},
    "AXP":  {"strategy": "dca",      "pos": "Mid",      "cagr": (8, 14),
             "area": "Premium credit network (American Express)",
             "note": "Closed-loop premium network; affluent base. DCA-grade, "
                     "mild credit cyclicality."},
    "BLK":  {"strategy": "dca",      "pos": "Mid",      "cagr": (8, 14),
             "area": "Asset-management anchor (BlackRock)",
             "note": "Institutional flow + ETF (iShares) capture. DCA-grade "
                     "compounder."},
    "TECK": {"strategy": "cycle",    "pos": "Mid",      "cagr": (5, 20),
             "area": "Copper expansion miner (Teck Resources)",
             "note": "Copper growth pipeline. Commodity CYCLE — buy dips."},
    "BHP":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (3, 12),
             "area": "Diversified major miner (BHP)",
             "note": "Bulk commodities + copper; cyclical, high yield. "
                     "Buy trough."},
    "RIO":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (2, 10),
             "area": "Iron ore / bauxite major (Rio Tinto)",
             "note": "Tier-1 iron ore + copper growth. Commodity CYCLE, "
                     "high yield — buy trough."},
    "LAC":  {"strategy": "catalyst", "pos": "Binary",   "cagr": (-40, 50),
             "area": "Nevada lithium development (Lithium Americas)",
             "note": "Dev-stage physical lithium (Thacker Pass); binary on "
                     "financing/permits/price. Size tiny, never avg down."},
    "SQM":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (3, 18),
             "area": "Low-cost lithium brine (SQM)",
             "note": "Low-cost brine producer; lithium price cyclical. "
                     "Buy trough."},
    "TGT":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (2, 10),
             "area": "Discretionary retail (Target)",
             "note": "Discretionary-spend recovery candidate; execution risk. "
                     "Cyclical-value — buy dips."},
    "CVX":  {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 9),
             "area": "Integrated supermajor (Chevron)",
             "note": "Permian-dense supermajor; FCF + dividend. DCA/value "
                     "yield."},
    "OXY":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (3, 15),
             "area": "Upstream + carbon capture (Occidental)",
             "note": "Leveraged upstream oil + CCUS optionality. Oil-price "
                     "CYCLE — buy dips."},
    "NVAX": {"strategy": "catalyst", "pos": "Binary",   "cagr": (-50, 60),
             "area": "Vaccine adjuvant platform (Novavax)",
             "note": "Binary on partnership/pipeline milestones; cash-burn "
                     "risk. Size tiny, never avg down."},
    "BNTX": {"strategy": "catalyst", "pos": "Binary",   "cagr": (-30, 50),
             "area": "mRNA oncology platform (BioNTech)",
             "note": "Cash-rich but binary on oncology readouts. Catalyst "
                     "punt — size on data, never avg down."},

    # --- Nasdaq-100 quality compounders & cyclicals added 2026-06 (owner
    #     request). These widen the watchlist into mega-cap staples, payments,
    #     industrials, healthcare and media adjacent to the AI book. Fundamentals
    #     are sourced at full coverage via `score_holdings.py --sync-csv`; the
    #     cagr band here is notebook metadata only (dropped from scoring per
    #     AGENTS.md). Strategy/pos tags follow the same vocabulary as above.

    "PEP":  {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 8),
             "area": "Global snacks + beverages (PepsiCo)",
             "note": "Defensive staples compounder; pricing power + dividend. "
                     "DCA/value yield."},
    "TMUS": {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 9),
             "area": "US wireless carrier (T-Mobile)",
             "note": "Post-merger FCF inflection; buybacks. Steady compounder "
                     "— DCA."},
    "BKNG": {"strategy": "dca",      "pos": "Mid",      "cagr": (8, 15),
             "area": "Online travel (Booking Holdings)",
             "note": "Asset-light travel platform; high FCF margin + buybacks. "
                     "DCA-grade compounder."},
    "MAR":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 12),
             "area": "Asset-light hotel franchisor (Marriott)",
             "note": "Fee-based lodging compounder; cyclical demand but "
                     "capital-light. DCA/quality."},
    "MNST": {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 12),
             "area": "Energy drinks (Monster Beverage)",
             "note": "High-margin beverage compounder; net-cash balance sheet. "
                     "DCA/quality."},
    "ADP":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 10),
             "area": "Payroll / HCM outsourcing (ADP)",
             "note": "Sticky recurring payroll franchise + float income. "
                     "DCA-grade compounder."},
    "CSX":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (2, 9),
             "area": "Eastern US freight rail (CSX)",
             "note": "Rail duopoly; volumes track the industrial cycle. "
                     "Cyclical-quality — buy dips."},
    "CMCSA": {"strategy": "dca",     "pos": "Mid",      "cagr": (1, 6),
              "area": "Cable / broadband + media (Comcast)",
              "note": "Broadband cash machine; media drag. Value/FCF — DCA on "
                      "weakness."},
    "MDLZ": {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 8),
             "area": "Global snacking (Mondelez)",
             "note": "Defensive staples compounder; pricing power. DCA/value "
                     "yield."},
    "ORLY": {"strategy": "dca",      "pos": "Mid",      "cagr": (6, 12),
             "area": "Auto-parts retail (O'Reilly)",
             "note": "Counter-cyclical retailer; relentless buybacks. "
                     "DCA-grade compounder."},
    "AEP":  {"strategy": "dca",      "pos": "Mid",      "cagr": (4, 8),
             "area": "Regulated electric utility (American Electric Power)",
             "note": "Regulated rate-base growth + datacenter load tailwind. "
                     "DCA/yield."},
    "NXPI": {"strategy": "cycle",    "pos": "Mid",      "cagr": (5, 13),
             "area": "Automotive / industrial semis (NXP)",
             "note": "Auto + industrial analog; tracks the semi cycle. "
                     "Cyclical-quality — buy dips."},
    "CTAS": {"strategy": "dca",      "pos": "Mid",      "cagr": (7, 12),
             "area": "Uniform rental / facility services (Cintas)",
             "note": "Route-density compounder; recurring B2B revenue. "
                     "DCA-grade quality."},
    "WBD":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (0, 10),
             "area": "Studios + streaming (Warner Bros. Discovery)",
             "note": "De-levering media turnaround; FCF-driven. Cyclical-value "
                     "— buy dips, watch debt."},
    "ROST": {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 11),
             "area": "Off-price apparel retail (Ross Stores)",
             "note": "Off-price compounder; resilient through downturns. "
                     "DCA/quality."},
    "REGN": {"strategy": "dca",      "pos": "Mid",      "cagr": (4, 12),
             "area": "Biotech (Regeneron)",
             "note": "Profitable biotech with deep pipeline + Eylea/Dupixent "
                     "franchise. DCA/quality."},
    "PCAR": {"strategy": "cycle",    "pos": "Mid",      "cagr": (2, 9),
             "area": "Heavy-truck manufacturer (Paccar)",
             "note": "Class-8 truck cycle; strong balance sheet + parts annuity. "
                     "Cyclical — buy trough."},
    "BKR":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (3, 12),
             "area": "Oilfield services + LNG equipment (Baker Hughes)",
             "note": "LNG/energy-tech capex cycle. Cyclical-value — buy dips."},
    "FAST": {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 11),
             "area": "Industrial distribution (Fastenal)",
             "note": "Vending/onsite industrial supply compounder; high ROIC. "
                     "DCA-grade quality."},
    "EA":   {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 9),
             "area": "Video-game publisher (Electronic Arts)",
             "note": "Sports-franchise annuity + live services. Steady "
                     "compounder — DCA."},
    "XEL":  {"strategy": "dca",      "pos": "Mid",      "cagr": (4, 8),
             "area": "Regulated utility (Xcel Energy)",
             "note": "Regulated rate-base + renewables build-out. DCA/yield."},
    "FANG": {"strategy": "cycle",    "pos": "Mid",      "cagr": (2, 14),
             "area": "Permian E&P (Diamondback Energy)",
             "note": "Low-cost Permian shale; FCF + variable dividend. "
                     "Oil-price CYCLE — buy dips."},
    "FER":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 12),
             "area": "Toll roads + infrastructure (Ferrovial)",
             "note": "Managed-lanes concession compounder; inflation-linked "
                     "tolls. DCA/infrastructure."},
    "EXC":  {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 8),
             "area": "Regulated T&D utility (Exelon)",
             "note": "Pure regulated wires; rate-base growth. DCA/yield."},
    "TTWO": {"strategy": "catalyst", "pos": "Binary",   "cagr": (-20, 40),
             "area": "Video-game publisher (Take-Two)",
             "note": "GTA VI release is the catalyst; slips/flop are the "
                     "downside. Event-driven — size on the launch."},
    "KDP":  {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 8),
             "area": "Coffee + beverages (Keurig Dr Pepper)",
             "note": "Defensive staples compounder; dividend. DCA/value yield."},
    "ODFL": {"strategy": "cycle",    "pos": "Mid",      "cagr": (3, 11),
             "area": "Less-than-truckload freight (Old Dominion)",
             "note": "Best-in-class LTL margins; freight-cycle volumes. "
                     "Cyclical-quality — buy dips."},
    "CCEP": {"strategy": "dca",      "pos": "Mid",      "cagr": (3, 8),
             "area": "Coca-Cola bottler EU/APAC (CCEP)",
             "note": "Defensive bottling franchise; steady FCF + dividend. "
                     "DCA/value yield."},
    "IDXX": {"strategy": "dca",      "pos": "Mid",      "cagr": (7, 13),
             "area": "Veterinary diagnostics (Idexx)",
             "note": "Razor/razorblade vet-diagnostics compounder; high "
                     "recurring margin. DCA/quality."},
    "ADSK": {"strategy": "dca",      "pos": "Mid",      "cagr": (8, 14),
             "area": "Design / CAD software (Autodesk)",
             "note": "Sticky subscription CAD franchise; high FCF margin. "
                     "DCA-grade compounder."},
    "ALNY": {"strategy": "catalyst", "pos": "Binary",   "cagr": (-30, 60),
             "area": "RNAi therapeutics (Alnylam)",
             "note": "RNAi platform scaling to profitability; binary on "
                     "label expansions/readouts. Catalyst — size on data."},
    "TRI":  {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 10),
             "area": "Legal / tax info services (Thomson Reuters)",
             "note": "Recurring professional-information franchise + AI "
                     "products. DCA-grade compounder."},
    "PAYX": {"strategy": "dca",      "pos": "Mid",      "cagr": (5, 10),
             "area": "SMB payroll / HR (Paychex)",
             "note": "Sticky SMB payroll + float income. DCA-grade compounder."},
    "ROP":  {"strategy": "dca",      "pos": "Mid",      "cagr": (7, 13),
             "area": "Vertical-market software conglomerate (Roper)",
             "note": "Acquisitive niche-software compounder; high recurring "
                     "FCF. DCA/quality."},
    "GEHC": {"strategy": "dca",      "pos": "Mid",      "cagr": (4, 10),
             "area": "Medical imaging (GE HealthCare)",
             "note": "Imaging install-base + service annuity. Quality "
                     "compounder — DCA."},
    "KHC":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (0, 6),
             "area": "Packaged food (Kraft Heinz)",
             "note": "Cheap staples turnaround; brand-relevance risk. "
                     "Value/DCA — buy on weakness."},
    "DXCM": {"strategy": "dca",      "pos": "Mid",      "cagr": (8, 16),
             "area": "Continuous glucose monitors (Dexcom)",
             "note": "CGM device + recurring-sensor razor/razorblade growth. "
                     "DCA-grade quality."},
    "CPRT": {"strategy": "dca",      "pos": "Mid",      "cagr": (7, 13),
             "area": "Salvage-vehicle auctions (Copart)",
             "note": "Two-sided salvage-auction network; high-margin moat. "
                     "DCA-grade compounder."},
    "KKR":  {"strategy": "cycle",    "pos": "Mid",      "cagr": (8, 18),
             "area": "Alternative-asset manager (KKR)",
             "note": "PE / credit / insurance compounder; fee-related earnings "
                     "steady but carry + balance-sheet marks track the market "
                     "cycle. Cyclical-quality — buy dips."},

    # =====================================================================
    # INTERNATIONAL LARGE-CAPS (added 2026-06-29) — 136 names across UK/
    # Japan/France/Canada/Switzerland/India/Australia, sourced into the
    # fundamentals CSV. Watch-only monitors OUTSIDE the wave baskets (no
    # weight effect). Mature blue-chips -> dca (quality compounders) or
    # cycle (banks/energy/miners/industrials); none are catalyst/lottery.
    # =====================================================================
    # --- UK (.L) ---
    "AZN.L": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "Pharma (AstraZeneca) — UK",
             "note": "Oncology/biopharma pipeline compounder. DCA-grade quality."},
    "SHEL.L": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Integrated oil & gas (Shell) — UK",
             "note": "Energy major; cash-return + buybacks, commodity-cyclical. Buy dips."},
    "HSBA.L": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Global bank (HSBC) — UK",
             "note": "Asia-tilted lender; rate/credit-cycle earnings. Cyclical-value."},
    "ULVR.L": {"strategy": "dca", "pos": "Mid", "cagr": (2, 6),
             "area": "Consumer staples (Unilever) — UK",
             "note": "Global brand portfolio; defensive compounder. DCA-grade."},
    "BP.L": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Integrated oil & gas (BP) — UK",
             "note": "Energy major; transition + buybacks, commodity-cyclical. Buy dips."},
    "RIO.L": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 10),
             "area": "Diversified miner (Rio Tinto) — UK",
             "note": "Iron ore/copper; deep commodity cycle. Buy dips, trim at peak."},
    "GSK.L": {"strategy": "dca", "pos": "Mid", "cagr": (3, 9),
             "area": "Pharma (GSK) — UK",
             "note": "Vaccines + specialty pharma. Defensive quality — DCA."},
    "DGE.L": {"strategy": "dca", "pos": "Mid", "cagr": (2, 7),
             "area": "Spirits (Diageo) — UK",
             "note": "Premium-spirits brand moat; near-term destock. DCA on weakness."},
    "REL.L": {"strategy": "dca", "pos": "Mid", "cagr": (5, 10),
             "area": "Analytics/info (RELX) — UK",
             "note": "Data/analytics subscription compounder. DCA-grade quality."},
    "BATS.L": {"strategy": "dca", "pos": "Mid", "cagr": (0, 5),
             "area": "Tobacco (BAT) — UK",
             "note": "High-yield staples; volume decline vs NGP transition. Value/DCA."},
    "GLEN.L": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 12),
             "area": "Mining + trading (Glencore) — UK",
             "note": "Diversified miner/marketer; deep commodity cycle. Buy dips."},
    "LSEG.L": {"strategy": "dca", "pos": "Mid", "cagr": (5, 11),
             "area": "Exchange/data (LSEG) — UK",
             "note": "Exchange + data (Refinitiv) annuity. Quality compounder — DCA."},
    "NG.L": {"strategy": "dca", "pos": "Mid", "cagr": (4, 9),
             "area": "Utility (National Grid) — UK",
             "note": "Regulated T&D utility; rate-base growth. Defensive DCA."},
    "BA.L": {"strategy": "cycle", "pos": "Mid", "cagr": (6, 14),
             "area": "Defense (BAE Systems) — UK",
             "note": "Defense budgets rising; multi-year backlog. Cyclical-quality."},
    "RR.L": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 12),
             "area": "Aero engines (Rolls-Royce) — UK",
             "note": "Engine + aftermarket turnaround; civil-aero cycle. Buy dips."},
    "VOD.L": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 6),
             "area": "Telecom (Vodafone) — UK",
             "note": "European telecom; restructuring, thin margins. Value/turnaround."},
    "BARC.L": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (Barclays) — UK",
             "note": "UK + IB lender; rate/credit-cycle earnings. Cyclical-value."},
    "LLOY.L": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (Lloyds) — UK",
             "note": "UK retail/mortgage lender; rate-cycle NIM. Cyclical-value."},
    "PRU.L": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 12),
             "area": "Insurer (Prudential) — UK",
             "note": "Asia life-insurance growth; market-cyclical. Cyclical-quality."},
    "TSCO.L": {"strategy": "dca", "pos": "Mid", "cagr": (1, 5),
             "area": "Grocer (Tesco) — UK",
             "note": "UK grocery leader; thin-margin defensive. DCA-grade staple."},
    # --- Japan (.T) ---
    "7203.T": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 7),
             "area": "Autos (Toyota) — Japan",
             "note": "Global #1 automaker; hybrid leader, auto-cyclical. Buy dips."},
    "6758.T": {"strategy": "dca", "pos": "Mid", "cagr": (2, 8),
             "area": "Electronics/entertainment (Sony) — Japan",
             "note": "Games/imaging/music portfolio; quality compounder. DCA."},
    "8306.T": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 9),
             "area": "Bank (MUFG) — Japan",
             "note": "Megabank; Japan rate normalization tailwind. Cyclical-value."},
    "6861.T": {"strategy": "dca", "pos": "Mid", "cagr": (8, 15),
             "area": "Factory automation (Keyence) — Japan",
             "note": "High-margin sensor/FA moat; secular automation. DCA quality."},
    "9984.T": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 15),
             "area": "Tech holding (SoftBank Group) — Japan",
             "note": "Vision Fund + Arm stake; NAV/market-cyclical. Cyclical punt."},
    "6098.T": {"strategy": "dca", "pos": "Mid", "cagr": (7, 13),
             "area": "HR/recruiting (Recruit) — Japan",
             "note": "Indeed/recruiting + matching platforms. Quality compounder — DCA."},
    "9983.T": {"strategy": "dca", "pos": "Mid", "cagr": (8, 15),
             "area": "Apparel retail (Fast Retailing/Uniqlo) — Japan",
             "note": "Uniqlo global expansion; brand compounder. DCA-grade."},
    "8035.T": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 20),
             "area": "Semicap (Tokyo Electron) — Japan",
             "note": "WFE leader; rides the chip-capex cycle. Cyclical growth."},
    "4063.T": {"strategy": "cycle", "pos": "Mid", "cagr": (6, 14),
             "area": "Chemicals/silicon (Shin-Etsu) — Japan",
             "note": "Silicon wafers + PVC; semi + housing cycle. Cyclical-quality."},
    "6501.T": {"strategy": "dca", "pos": "Mid", "cagr": (4, 10),
             "area": "Conglomerate (Hitachi) — Japan",
             "note": "Digital/energy/rail; restructuring compounder. DCA-grade."},
    "7974.T": {"strategy": "dca", "pos": "Mid", "cagr": (3, 12),
             "area": "Games (Nintendo) — Japan",
             "note": "Switch + IP franchise; hit-cycle but cash-rich. DCA quality."},
    "9433.T": {"strategy": "dca", "pos": "Mid", "cagr": (2, 7),
             "area": "Telecom (KDDI) — Japan",
             "note": "Mobile + finance; high-yield defensive. DCA-grade."},
    "8058.T": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Trading house (Mitsubishi Corp) — Japan",
             "note": "Diversified trading/commodities; Buffett-held. Cyclical-value."},
    "6902.T": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Auto parts (Denso) — Japan",
             "note": "Toyota-linked components; auto/EV cycle. Cyclical-quality."},
    "4519.T": {"strategy": "dca", "pos": "Mid", "cagr": (4, 10),
             "area": "Pharma (Chugai) — Japan",
             "note": "Roche-linked biopharma; royalty + pipeline. DCA-grade."},
    "6594.T": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 12),
             "area": "Motors (Nidec) — Japan",
             "note": "Precision/EV motors; auto-EV cyclical. Cyclical growth."},
    "8316.T": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 9),
             "area": "Bank (Sumitomo Mitsui/SMFG) — Japan",
             "note": "Megabank; rate-normalization tailwind. Cyclical-value."},
    "9432.T": {"strategy": "dca", "pos": "Mid", "cagr": (2, 6),
             "area": "Telecom (NTT) — Japan",
             "note": "Fixed + mobile incumbent; high-yield defensive. DCA-grade."},
    "8001.T": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Trading house (Itochu) — Japan",
             "note": "Consumer-tilted trading house; Buffett-held. Cyclical-value."},
    "7267.T": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 7),
             "area": "Autos (Honda) — Japan",
             "note": "Autos + motorcycles; auto-cyclical, EV transition. Buy dips."},
    # --- France (.PA) ---
    "VU.PA": {"strategy": "dca", "pos": "Mid", "cagr": (10, 20),
             "area": "Retail IoT / electronic shelf labels (Vusion, ex-SES-imagotag) — France",
             "note": "PROFITABLE small-cap (net margin ~9.7% TTM, turned positive) "
                     "scaling digital shelf-label / retail-IoT platforms — an edge-"
                     "compute + data play adjacent to the AI-in-retail thesis. Rev "
                     "+54% ttm off recurring hardware+SaaS. Quality-growth compounder "
                     "if margins keep climbing — DCA on dips. Euronext Paris (EUR)."},
    "ALSTI.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 20),
             "area": "Datacenter cooling / air-handling & containment (STIF) — France",
             "note": "PROFITABLE French micro-cap (net margin ~13% TTM) in industrial "
                     "ventilation / thermal containment — levered to datacenter cooling "
                     "buildout (the same physical bottleneck as VRT). Rev +48% ttm, "
                     "expanding margins, but tiny + order-lumpy, so cyclical: buy dips, "
                     "trim manias. Euronext Paris (EUR)."},
    "MC.PA": {"strategy": "dca", "pos": "Mid", "cagr": (4, 11),
             "area": "Luxury (LVMH) — France",
             "note": "Luxury house portfolio; brand moat, demand-cyclical. DCA on dips."},
    "OR.PA": {"strategy": "dca", "pos": "Mid", "cagr": (5, 10),
             "area": "Beauty (L'Oreal) — France",
             "note": "Global beauty leader; defensive compounder. DCA-grade."},
    "RMS.PA": {"strategy": "dca", "pos": "Mid", "cagr": (8, 14),
             "area": "Luxury (Hermes) — France",
             "note": "Ultra-premium scarcity moat; pricing power. DCA quality."},
    "TTE.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Integrated oil & gas (TotalEnergies) — France",
             "note": "Energy major + LNG/renewables. Commodity-cyclical. Buy dips."},
    "SAN.PA": {"strategy": "dca", "pos": "Mid", "cagr": (4, 10),
             "area": "Pharma (Sanofi) — France",
             "note": "Immunology (Dupixent) + vaccines. Defensive quality — DCA."},
    "AIR.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Aerospace (Airbus) — France",
             "note": "Commercial-aircraft duopoly; multi-year backlog. Cyclical-quality."},
    "SU.PA": {"strategy": "dca", "pos": "Mid", "cagr": (7, 12),
             "area": "Electrical/automation (Schneider) — France",
             "note": "Grid + data-center electrification. Quality compounder — DCA."},
    "EL.PA": {"strategy": "dca", "pos": "Mid", "cagr": (6, 11),
             "area": "Eyewear (EssilorLuxottica) — France",
             "note": "Lens + frames vertical moat. Quality compounder — DCA."},
    "AI.PA": {"strategy": "dca", "pos": "Mid", "cagr": (4, 9),
             "area": "Industrial gas (Air Liquide) — France",
             "note": "Gas-supply annuity moat; defensive. DCA-grade compounder."},
    "BNP.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 9),
             "area": "Bank (BNP Paribas) — France",
             "note": "Eurozone universal bank; rate/credit-cycle earnings. Cyclical-value."},
    "CS.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 10),
             "area": "Insurer (AXA) — France",
             "note": "Global P&C/life insurer; market-cyclical. Cyclical-value."},
    "DG.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Construction/concessions (Vinci) — France",
             "note": "Toll roads + airports + construction. Cyclical-quality."},
    "SAF.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Aero propulsion (Safran) — France",
             "note": "Engine + aftermarket; civil-aero cycle. Cyclical-quality."},
    "BN.PA": {"strategy": "dca", "pos": "Mid", "cagr": (2, 6),
             "area": "Food (Danone) — France",
             "note": "Dairy/water/nutrition staples. Defensive DCA-grade."},
    "KER.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Luxury (Kering/Gucci) — France",
             "note": "Luxury turnaround; Gucci-dependent, cyclical. Value/turnaround."},
    "CAP.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 10),
             "area": "IT services (Capgemini) — France",
             "note": "IT consulting/integration; demand-cyclical. Cyclical-quality."},
    "LR.PA": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "Aero/cybersecurity (Thales) — France",
             "note": "Defense + cyber + avionics. Cyclical-quality compounder."},
    "ENGI.PA": {"strategy": "dca", "pos": "Mid", "cagr": (3, 8),
             "area": "Utility (Engie) — France",
             "note": "Power/gas + renewables utility. Defensive DCA-grade."},
    "ORA.PA": {"strategy": "dca", "pos": "Mid", "cagr": (1, 5),
             "area": "Telecom (Orange) — France",
             "note": "European telecom incumbent; high-yield. DCA-grade defensive."},
    # --- Canada (.TO) ---
    "RY.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 10),
             "area": "Bank (Royal Bank of Canada) — Canada",
             "note": "Largest Canadian bank; rate/credit-cycle. Cyclical-quality."},
    "TD.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (TD) — Canada",
             "note": "Canada + US retail bank; AML overhang. Cyclical-value."},
    "ENB.TO": {"strategy": "dca", "pos": "Mid", "cagr": (3, 8),
             "area": "Midstream energy (Enbridge) — Canada",
             "note": "Pipeline + utility toll annuity; high yield. DCA-grade."},
    "BN.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 18),
             "area": "Alt-asset manager (Brookfield) — Canada",
             "note": "Infra/RE/credit compounder; market-cyclical marks. Cyclical-quality."},
    "CNR.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 9),
             "area": "Railroad (Canadian National) — Canada",
             "note": "Class-I rail duopoly; volume-cyclical moat. Cyclical-quality."},
    "CP.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (6, 12),
             "area": "Railroad (Canadian Pacific/KCS) — Canada",
             "note": "Rail network + KCS Mexico synergy. Cyclical-quality."},
    "BMO.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 9),
             "area": "Bank (Bank of Montreal) — Canada",
             "note": "Canada + US Midwest bank; rate-cycle. Cyclical-value."},
    "CNQ.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 10),
             "area": "Oil & gas E&P (Canadian Natural) — Canada",
             "note": "Long-life oil sands; commodity-cyclical, high return. Buy dips."},
    "BNS.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (Scotiabank) — Canada",
             "note": "Canada + LatAm lender; rate/EM-cycle. Cyclical-value."},
    "TRP.TO": {"strategy": "dca", "pos": "Mid", "cagr": (3, 8),
             "area": "Midstream energy (TC Energy) — Canada",
             "note": "Gas pipeline + power toll annuity; yield. DCA-grade."},
    "SU.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 10),
             "area": "Integrated oil (Suncor) — Canada",
             "note": "Oil sands + refining/retail; commodity-cyclical. Buy dips."},
    "ATD.TO": {"strategy": "dca", "pos": "Mid", "cagr": (5, 11),
             "area": "Convenience retail (Couche-Tard) — Canada",
             "note": "Global c-store roll-up compounder. DCA-grade."},
    "CM.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 9),
             "area": "Bank (CIBC) — Canada",
             "note": "Canadian retail/commercial bank; rate-cycle. Cyclical-value."},
    "MFC.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 10),
             "area": "Insurer (Manulife) — Canada",
             "note": "Life insurance + Asia growth; market-cyclical. Cyclical-value."},
    "CSU.TO": {"strategy": "dca", "pos": "Mid", "cagr": (12, 22),
             "area": "Software roll-up (Constellation Software) — Canada",
             "note": "Serial VMS acquirer; high-ROIC compounder. DCA quality."},
    "TRI.TO": {"strategy": "dca", "pos": "Mid", "cagr": (6, 11),
             "area": "Info/analytics (Thomson Reuters) — Canada",
             "note": "Legal/tax data subscription annuity. Quality compounder — DCA."},
    "FNV.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
             "area": "Gold royalties (Franco-Nevada) — Canada",
             "note": "Precious-metals royalty/streaming; gold-cyclical. Cyclical-quality."},
    "NTR.TO": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 10),
             "area": "Fertilizer (Nutrien) — Canada",
             "note": "Potash + nitrogen + retail; ag-commodity cycle. Buy dips."},
    # --- Switzerland (.SW) ---
    "NESN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (2, 6),
             "area": "Consumer staples (Nestle) — Switzerland",
             "note": "Global food/beverage brand moat. Defensive DCA-grade."},
    "ROG.SW": {"strategy": "dca", "pos": "Mid", "cagr": (2, 8),
             "area": "Pharma (Roche) — Switzerland",
             "note": "Oncology + diagnostics; pipeline-driven. Defensive quality — DCA."},
    "NOVN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (3, 8),
             "area": "Pharma (Novartis) — Switzerland",
             "note": "Innovative-medicines pure-play. Defensive quality — DCA."},
    "UBSG.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 10),
             "area": "Bank (UBS) — Switzerland",
             "note": "Wealth mgmt + CS integration; market-cyclical. Cyclical-quality."},
    "ZURN.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 9),
             "area": "Insurer (Zurich) — Switzerland",
             "note": "Global P&C/life insurer; high-yield. Cyclical-quality."},
    "ABBN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "Electrification/automation (ABB) — Switzerland",
             "note": "Grid + robotics + electrification. Quality compounder — DCA."},
    "LONN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (8, 15),
             "area": "CDMO/pharma services (Lonza) — Switzerland",
             "note": "Biologics contract manufacturing; secular outsourcing. DCA growth."},
    "SIKA.SW": {"strategy": "dca", "pos": "Mid", "cagr": (6, 11),
             "area": "Specialty chemicals (Sika) — Switzerland",
             "note": "Construction chemicals roll-up compounder. DCA-grade."},
    "GIVN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (4, 9),
             "area": "Flavors/fragrances (Givaudan) — Switzerland",
             "note": "F&F duopoly; sticky formulation moat. Quality compounder — DCA."},
    "ALC.SW": {"strategy": "dca", "pos": "Mid", "cagr": (5, 10),
             "area": "Eye care (Alcon) — Switzerland",
             "note": "Surgical + vision-care devices. Quality compounder — DCA."},
    "CFR.SW": {"strategy": "dca", "pos": "Mid", "cagr": (4, 11),
             "area": "Luxury (Richemont/Cartier) — Switzerland",
             "note": "Hard-luxury jewelry/watches; brand moat. DCA on dips."},
    "SREN.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 8),
             "area": "Reinsurer (Swiss Re) — Switzerland",
             "note": "Global reinsurance; rate-cycle + cat risk. Cyclical-value."},
    "HOLN.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Building materials (Holcim) — Switzerland",
             "note": "Cement/aggregates; construction-cyclical. Cyclical-value."},
    "GEBN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (4, 9),
             "area": "Sanitary systems (Geberit) — Switzerland",
             "note": "Plumbing-systems moat; construction-tilted. DCA-grade."},
    "PGHN.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (6, 14),
             "area": "Private markets (Partners Group) — Switzerland",
             "note": "PE/infra asset manager; fee + carry cyclical. Cyclical-quality."},
    "SLHN.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 9),
             "area": "Insurer (Swiss Life) — Switzerland",
             "note": "Life insurance + asset mgmt; market-cyclical. Cyclical-value."},
    "SOON.SW": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "Hearing aids (Sonova) — Switzerland",
             "note": "Hearing-device + audiology moat. Quality compounder — DCA."},
    "BAER.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 10),
             "area": "Private bank (Julius Baer) — Switzerland",
             "note": "Pure-play wealth mgmt; market-cyclical AUM. Cyclical-value."},
    "LISN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (3, 8),
             "area": "Specialty food (Lindt) — Switzerland",
             "note": "Premium-chocolate brand moat; pricing power. DCA quality."},
    "SCMN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (1, 5),
             "area": "Telecom (Swisscom) — Switzerland",
             "note": "Swiss telecom incumbent + Italy; high-yield. DCA-grade defensive."},
    # --- India (.NS) ---
    "RELIANCE.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Conglomerate (Reliance) — India",
             "note": "Energy + telecom (Jio) + retail; mixed cyclical. Cyclical growth."},
    "TCS.NS": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "IT services (TCS) — India",
             "note": "Global IT outsourcing leader; high-ROIC. DCA-grade compounder."},
    "HDFCBANK.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 18),
             "area": "Bank (HDFC Bank) — India",
             "note": "Top Indian private bank; structural credit growth. Cyclical-quality."},
    "BHARTIARTL.NS": {"strategy": "dca", "pos": "Mid", "cagr": (8, 15),
             "area": "Telecom (Bharti Airtel) — India",
             "note": "India + Africa mobile; ARPU + data growth. DCA-grade growth."},
    "ICICIBANK.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 18),
             "area": "Bank (ICICI Bank) — India",
             "note": "Leading private bank; structural credit growth. Cyclical-quality."},
    "INFY.NS": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "IT services (Infosys) — India",
             "note": "Global IT outsourcing; high-ROIC. DCA-grade compounder."},
    "SBIN.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Bank (State Bank of India) — India",
             "note": "Largest public-sector bank; credit-cycle leverage. Cyclical-value."},
    "LT.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Engineering/construction (Larsen & Toubro) — India",
             "note": "Infra/EPC + IT; India-capex cycle. Cyclical-quality."},
    "ITC.NS": {"strategy": "dca", "pos": "Mid", "cagr": (5, 11),
             "area": "Tobacco/FMCG (ITC) — India",
             "note": "Cigarettes + FMCG + hotels; high-yield. DCA-grade staple."},
    "HINDUNILVR.NS": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "Consumer staples (Hindustan Unilever) — India",
             "note": "Indian FMCG leader; rural-recovery play. DCA-grade."},
    "BAJFINANCE.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (18, 28),
             "area": "NBFC lender (Bajaj Finance) — India",
             "note": "Consumer-credit growth machine; credit-cycle risk. Cyclical growth."},
    "MARUTI.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Autos (Maruti Suzuki) — India",
             "note": "India passenger-car leader; auto-cyclical. Cyclical-quality."},
    "SUNPHARMA.NS": {"strategy": "dca", "pos": "Mid", "cagr": (8, 14),
             "area": "Pharma (Sun Pharma) — India",
             "note": "India + US specialty generics/branded. DCA-grade quality."},
    "KOTAKBANK.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 18),
             "area": "Bank (Kotak Mahindra) — India",
             "note": "Private bank; structural credit growth. Cyclical-quality."},
    "AXISBANK.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 18),
             "area": "Bank (Axis Bank) — India",
             "note": "Private-sector lender; credit-cycle growth. Cyclical-quality."},
    "TITAN.NS": {"strategy": "dca", "pos": "Mid", "cagr": (12, 20),
             "area": "Jewelry/retail (Titan) — India",
             "note": "Organized jewelry + watches; consumption growth. DCA growth."},
    "ULTRACEMCO.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Cement (UltraTech) — India",
             "note": "India cement leader; infra-capex cycle. Cyclical-quality."},
    "ASIANPAINT.NS": {"strategy": "dca", "pos": "Mid", "cagr": (8, 14),
             "area": "Paints (Asian Paints) — India",
             "note": "Decorative-paint distribution moat; new competition. DCA-grade."},
    "WIPRO.NS": {"strategy": "dca", "pos": "Mid", "cagr": (4, 10),
             "area": "IT services (Wipro) — India",
             "note": "Global IT outsourcing; turnaround. DCA-grade compounder."},
    "ONGC.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 10),
             "area": "Oil & gas E&P (ONGC) — India",
             "note": "State-owned upstream; commodity + policy cyclical. Cyclical-value."},
    # --- Australia (.AX) ---
    "BHP.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 12),
             "area": "Diversified miner (BHP) — Australia",
             "note": "Iron ore + copper; deep commodity cycle. Buy dips, trim peak."},
    "CBA.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (Commonwealth Bank) — Australia",
             "note": "Largest Aussie bank; rate/housing-cycle. Cyclical-value."},
    "CSL.AX": {"strategy": "dca", "pos": "Mid", "cagr": (8, 14),
             "area": "Biotech/plasma (CSL) — Australia",
             "note": "Plasma therapies + vaccines; secular moat. DCA-grade quality."},
    "NAB.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (National Australia Bank) — Australia",
             "note": "Business-lending tilt; rate-cycle. Cyclical-value."},
    "WBC.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (Westpac) — Australia",
             "note": "Aussie retail/mortgage lender; rate-cycle. Cyclical-value."},
    "ANZ.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (ANZ) — Australia",
             "note": "Aussie + NZ + institutional bank; rate-cycle. Cyclical-value."},
    "FMG.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 12),
             "area": "Iron ore (Fortescue) — Australia",
             "note": "Pure-play iron ore + green-H2 optionality. Commodity-cyclical."},
    "WES.AX": {"strategy": "dca", "pos": "Mid", "cagr": (4, 9),
             "area": "Retail conglomerate (Wesfarmers) — Australia",
             "note": "Bunnings + Kmart retail compounder. DCA-grade."},
    "MQG.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 12),
             "area": "Investment bank/asset mgr (Macquarie) — Australia",
             "note": "Infra asset mgmt + markets; cyclical earnings. Cyclical-quality."},
    "GMG.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 15),
             "area": "Industrial REIT (Goodman Group) — Australia",
             "note": "Logistics + data-center development; rate-cyclical. Cyclical growth."},
    "WOW.AX": {"strategy": "dca", "pos": "Mid", "cagr": (2, 6),
             "area": "Grocer (Woolworths) — Australia",
             "note": "Australian grocery leader; defensive staple. DCA-grade."},
    "TLS.AX": {"strategy": "dca", "pos": "Mid", "cagr": (2, 6),
             "area": "Telecom (Telstra) — Australia",
             "note": "Australian mobile incumbent; high-yield. DCA-grade defensive."},
    "TCL.AX": {"strategy": "dca", "pos": "Mid", "cagr": (4, 9),
             "area": "Toll roads (Transurban) — Australia",
             "note": "Toll-road concession annuity; inflation-linked. DCA-grade."},
    "WDS.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 10),
             "area": "LNG/oil (Woodside) — Australia",
             "note": "LNG + oil; commodity-cyclical, high yield. Buy dips."},
    "ALL.AX": {"strategy": "dca", "pos": "Mid", "cagr": (8, 15),
             "area": "Gaming/tech (Aristocrat) — Australia",
             "note": "Slot machines + digital gaming; high-margin. DCA-grade growth."},
    "REA.AX": {"strategy": "dca", "pos": "Mid", "cagr": (8, 15),
             "area": "Property portal (REA Group) — Australia",
             "note": "Dominant real-estate listings platform. Quality compounder — DCA."},
    "COL.AX": {"strategy": "dca", "pos": "Mid", "cagr": (2, 6),
             "area": "Grocer (Coles) — Australia",
             "note": "Australian grocery #2; defensive staple. DCA-grade."},
    "STO.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 12),
             "area": "Oil & gas (Santos) — Australia",
             "note": "LNG + oil E&P; commodity-cyclical. Cyclical-value."},
    "QBE.AX": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 9),
             "area": "Insurer (QBE) — Australia",
             "note": "Global P&C insurer; rate-cycle + cat risk. Cyclical-value."},

    # =====================================================================
    # WORLD TOP-MARKETS BATCH (added 2026-08-04) — 41 large-caps filling the
    # gaps for the world's #2..#20 stock markets by total cap that were thin
    # or absent above: China (mainland + HK + ADRs), Germany (Xetra),
    # Netherlands (Amsterdam), Taiwan (TWSE), Spain (BME), Brazil (ADRs),
    # Sweden (Stockholm), South Africa (JSE), Saudi Arabia (Tadawul), plus
    # Korea depth. Watch-only monitors OUTSIDE the wave baskets (no weight
    # effect); sourced into the fundamentals CSV via --sync-csv. Mature
    # blue-chips -> dca (quality compounders) or cycle (banks/energy/miners/
    # autos/industrials); none are catalyst/lottery. De-duplicated against the
    # names already present above (e.g. Alibaba is 9988.HK, ASML/SAP/Adyen
    # already listed, so their ADRs are intentionally omitted).
    # =====================================================================
    # --- China (US-listed ADRs) ---
    "BABA": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 15),
             "area": "E-commerce/cloud (Alibaba ADR) — China",
             "note": "Taobao/Tmall + Alibaba Cloud; AI-cloud reaccel vs China-macro "
                     "+ ADR/regulatory risk. Also trades as 9988.HK. Cyclical-value."},
    "JD": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 12),
             "area": "E-commerce/logistics (JD.com ADR) — China",
             "note": "Self-op retail + logistics; thin-margin, China-consumer "
                     "cyclical. ADR/regulatory risk. Cyclical-value."},
    "BIDU": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 12),
             "area": "Search/AI/cloud (Baidu ADR) — China",
             "note": "Search + Ernie LLM + Apollo autonomous; AI optionality vs "
                     "ad-cycle + ADR risk. Cyclical-value."},
    "NTES": {"strategy": "dca", "pos": "Mid", "cagr": (4, 12),
             "area": "Games (NetEase ADR) — China",
             "note": "PC/mobile games portfolio; cash-rich, high-margin. Hit-cycle "
                     "but quality. DCA-grade (China/ADR risk noted)."},
    "LI": {"strategy": "cycle", "pos": "Early", "cagr": (5, 25),
             "area": "EV maker (Li Auto ADR) — China",
             "note": "EREV/EV SUVs; profitable among China EV pack but price-war "
                     "cyclical + ADR risk. Cyclical growth."},
    "TCOM": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 18),
             "area": "Online travel (Trip.com ADR) — China",
             "note": "China + outbound travel-recovery leader; consumer-cyclical + "
                     "ADR risk. Cyclical growth."},
    "YUMC": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "Restaurants (Yum China ADR) — KFC/Pizza Hut China",
             "note": "KFC/Pizza Hut China operator; store-count compounder, "
                     "cash-generative. DCA-grade (China/ADR risk noted)."},
    # --- China / HK-native (.HK) ---
    "3690.HK": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 20),
             "area": "Local services/delivery (Meituan) — China",
             "note": "Food delivery + local commerce super-app; margin vs "
                     "competition, China-consumer cyclical. Cyclical growth."},
    "1211.HK": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 25),
             "area": "EV + batteries (BYD) — China",
             "note": "World EV-volume leader + battery vertical integration; "
                     "price-war cyclical. Cyclical growth."},
    "2015.HK": {"strategy": "cycle", "pos": "Early", "cagr": (5, 25),
             "area": "EV maker (Li Auto H-share) — China",
             "note": "H-share line of Li Auto (also LI ADR); China EV price-war "
                     "cyclical. Cyclical growth."},
    # --- Germany (Xetra, .DE) ---
    "ALV.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 9),
             "area": "Insurer/asset mgr (Allianz) — Germany",
             "note": "Global insurer + PIMCO asset mgmt; rate/market-cyclical. "
                     "Cyclical-quality."},
    "DTE.DE": {"strategy": "dca", "pos": "Mid", "cagr": (3, 8),
             "area": "Telecom (Deutsche Telekom) — Germany",
             "note": "T-Mobile US stake + European telecom; steady cash. "
                     "DCA-grade defensive."},
    "IFX.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
             "area": "Semiconductors (Infineon) — Germany",
             "note": "Auto + power/industrial chips; EV/electrification secular vs "
                     "auto-inventory cycle. Cyclical growth."},
    "MBG.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Autos (Mercedes-Benz) — Germany",
             "note": "Premium autos; margin vs China + EV-transition cyclical. "
                     "Cyclical-value."},
    "BMW.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Autos (BMW) — Germany",
             "note": "Premium autos; EV ramp vs auto-demand cycle. Cyclical-value."},
    # RHM.DE PROMOTED (RESHAPE 2026-08) to W7_DIVERSIFY_TARGETS at 1.2% book
    #     (funded by the ALAB cut) — adds a tech-uncorrelated defense sleeve the
    #     book lacked. Removed from WATCHLIST; re-add here if it is ever cut to 0%.
    "MUV2.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 9),
             "area": "Reinsurance (Munich Re) — Germany",
             "note": "Global reinsurer; rate-cycle + cat exposure. Cyclical-quality."},
    "BAS.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Chemicals (BASF) — Germany",
             "note": "Diversified chemicals; deep industrial/energy-cost cycle. "
                     "Cyclical-value."},
    # --- Netherlands (Amsterdam, .AS) ---
    "ASM.AS": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 25),
             "area": "Semicap/ALD (ASM International) — Netherlands",
             "note": "Atomic-layer-deposition leader; rides the leading-edge "
                     "chip-capex cycle. Cyclical growth."},
    "PRX.AS": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
             "area": "Tech holding (Prosus) — Netherlands",
             "note": "Tencent stake + global consumer-internet holding; NAV/market-"
                     "cyclical + China exposure. Cyclical-value."},
    "INGA.AS": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Bank (ING) — Netherlands",
             "note": "European retail/commercial lender; rate/credit-cycle. "
                     "Cyclical-value."},
    "HEIA.AS": {"strategy": "dca", "pos": "Mid", "cagr": (3, 8),
             "area": "Brewer (Heineken) — Netherlands",
             "note": "Global beer brand portfolio; defensive staple. DCA-grade."},
    "WKL.AS": {"strategy": "dca", "pos": "Mid", "cagr": (5, 10),
             "area": "Info services (Wolters Kluwer) — Netherlands",
             "note": "Professional info + software subscriptions; recurring-revenue "
                     "compounder. DCA-grade quality."},
    # --- Taiwan (TWSE, .TW) ---
    "2454.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 20),
             "area": "Fabless SoC (MediaTek) — Taiwan",
             "note": "Smartphone/edge-AI SoCs; rides handset + AI-edge cycle. "
                     "Cyclical growth."},
    "2317.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
             "area": "Electronics contract mfg (Foxconn/Hon Hai) — Taiwan",
             "note": "Apple assembler pivoting to AI-server ODM; thin-margin, "
                     "capex/demand cyclical. Cyclical-value."},
    # --- Spain (BME, .MC) ---
    "ITX.MC": {"strategy": "dca", "pos": "Mid", "cagr": (5, 11),
             "area": "Apparel retail (Inditex/Zara) — Spain",
             "note": "Zara fast-fashion global compounder; high-margin, net-cash. "
                     "DCA-grade quality."},
    "IBE.MC": {"strategy": "dca", "pos": "Mid", "cagr": (4, 9),
             "area": "Utility (Iberdrola) — Spain",
             "note": "Regulated networks + renewables; rate-base growth. Defensive "
                     "DCA-grade."},
    "SAN": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 9),
             "area": "Bank (Banco Santander ADR) — Spain",
             "note": "Euro + LatAm retail lender; rate/credit-cycle + FX. "
                     "Cyclical-value."},
    "BBVA": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 9),
             "area": "Bank (BBVA ADR) — Spain",
             "note": "Spain + Mexico/LatAm lender; rate/EM-credit cycle. "
                     "Cyclical-value."},
    # --- Brazil (US-listed ADRs) ---
    "VALE": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 12),
             "area": "Iron ore/nickel miner (Vale ADR) — Brazil",
             "note": "Iron ore + base metals; deep China-demand commodity cycle. "
                     "Buy dips, trim peak."},
    "ITUB": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 10),
             "area": "Bank (Itaú Unibanco ADR) — Brazil",
             "note": "Largest LatAm private bank; Brazil rate/credit cycle + FX. "
                     "Cyclical-value."},
    "PBR": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 10),
             "area": "Integrated oil (Petrobras ADR) — Brazil",
             "note": "State-influenced oil major; high yield, commodity + policy "
                     "cyclical. Cyclical-value."},
    "ABEV": {"strategy": "dca", "pos": "Mid", "cagr": (2, 7),
             "area": "Brewer (Ambev ADR) — Brazil",
             "note": "AB InBev LatAm brewer; defensive staple + FX. DCA-grade."},
    # --- Sweden (Stockholm, .ST) ---
    "SAND.ST": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 10),
             "area": "Mining/cutting tools (Sandvik) — Sweden",
             "note": "Mining equipment + tooling; industrial + mining-capex cycle. "
                     "Cyclical-quality."},
    # --- Sweden (US-listed ADR) ---
    "ERIC": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Telecom equipment (Ericsson ADR) — Sweden",
             "note": "5G RAN gear; carrier-capex cyclical, thin margins. "
                     "Cyclical-value/turnaround."},
    # --- South Africa (JSE, .JO) ---
    "NPN.JO": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
             "area": "Tech holding (Naspers) — South Africa",
             "note": "Tencent stake + Prosus parent; NAV/discount + China exposure. "
                     "Cyclical-value."},
    # --- Saudi Arabia (Tadawul, .SR) ---
    "2222.SR": {"strategy": "cycle", "pos": "Mid", "cagr": (0, 8),
             "area": "Integrated oil (Saudi Aramco) — Saudi Arabia",
             "note": "World's largest oil producer; high dividend, oil-price + OPEC "
                     "policy cyclical. Cyclical-value."},
    # --- Korea (KRX, .KS) — depth beyond Samsung/SK Hynix ---
    "005380.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Autos (Hyundai Motor) — South Korea",
             "note": "Global automaker; EV push vs auto-demand cycle + FX. "
                     "Cyclical-value."},
    "051910.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 12),
             "area": "Chemicals/EV batteries (LG Chem) — South Korea",
             "note": "Petrochemicals + LG Energy Solution battery stake; EV-battery "
                     "+ chemical cycle. Cyclical growth."},
    "035420.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
             "area": "Internet/search (Naver) — South Korea",
             "note": "Korea search + commerce + webtoon; ad-cycle + AI optionality. "
                     "Cyclical growth."},
    "000270.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 8),
             "area": "Autos (Kia) — South Korea",
             "note": "Hyundai-affiliate automaker; EV ramp vs auto cycle + FX. "
                     "Cyclical-value."},

    # --- AI data-engineering (training-data prep for LLM labs) ---
    "INOD": {"strategy": "cycle", "pos": "Early", "cagr": (10, 30),
             "area": "AI data engineering (Innodata) — LLM training-data prep",
             "note": "Profitable, net-cash ($113M, D/E 0.03), high-ROIC (171%) "
                     "data-annotation / training-data shop selling into the LLM "
                     "labs' capex. 42% gross / 14% net margin, FCF +$62M. "
                     "High-beta (2.83) AI-derivative — analyst 3Y rev forecast a "
                     "modest 11% (decel off a hypergrowth base), but Strong Buy, "
                     "PT +60%. A non-semi AI-supply-chain diversifier. Buy dips / "
                     "trim manias — cycle."},

    # --- AI semiconductor / IP gems (small/mid-cap, not in the SMHV ETF) ---
    "RMBS": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 25),
             "area": "Memory-interface IP (Rambus) — HBM/DDR5 chips + IP licensing",
             "note": "Profitable (ROE 18%, ROIC 33%), net cash, +94%/yr. Sells the "
                     "memory-interface chips & IP that HBM/DDR5 (the AI-memory "
                     "bottleneck) needs. Richly valued (P/S 18, PE 59) — cyclical "
                     "with the memory cycle. Buy dips / trim peaks."},
    "SITM": {"strategy": "cycle", "pos": "Early", "cagr": (20, 40),
             "area": "MEMS timing / precision clocks (SiTime) — datacenter+AI",
             "note": "Hypergrowth (+234%/yr), net cash, current ratio 12. MEMS "
                     "silicon timing (clock chips) replacing legacy quartz in AI "
                     "servers/networking. Marginally GAAP-unprofitable (reinvesting) "
                     "but not pre-revenue/shrinking — Early high-beta (2.92). "
                     "VERY rich (P/S 49). Buy deep dips only."},
    "AMBA": {"strategy": "cycle", "pos": "Mid", "cagr": (15, 35),
             "area": "Edge-AI vision SoCs (Ambarella) — cameras/auto/robotics",
             "note": "Edge-AI inference chips for cameras, autonomous & robotics. "
                     "Net cash, FCF-positive, GAAP-unprofitable (reinvesting). "
                     "AI-inference-at-the-edge pure-play, high-beta (2.15). P/S 7. "
                     "Cyclical recovery name — buy dips."},
    "ALGM": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 25),
             "area": "Magnetic/current sensors (Allegro Micro) — auto/industrial",
             "note": "Magnetic position & current-sensor ICs for EV/auto + "
                     "industrial automation. +94%/yr off a cyclical trough; ROIC "
                     "positive, PEG 1.56, some net debt (D/E 0.32). Auto/industrial "
                     "semi cycle — buy dips, trim into strength."},
    "CRUS": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
             "area": "Audio / mixed-signal (Cirrus Logic) — the CHEAP quality name",
             "note": "Profitable + CHEAP (PE 18.6, P/S 3.7, ROIC 27.5%), net cash, "
                     "buying back stock. Audio/mixed-signal — Apple-concentrated, so "
                     "cyclical with the handset cycle; expanding into laptop/AI-PC "
                     "power. Lower-beta (1.14) value-tech. Buy dips."},

    # --- AI software / applications (profitable, cheaper than the mega-SaaS) ---
    "PEGA": {"strategy": "dca", "pos": "Mid", "cagr": (8, 20),
             "area": "Enterprise AI workflow automation (Pegasystems)",
             "note": "Profitable + CHEAP (PE 16, fwd 10.7, P/S 3.0), elite ROE 52% "
                     "/ ROIC 52%, strong FCF. Agentic-AI workflow/decisioning for "
                     "large enterprises. Low-beta (0.84) quality compounder that "
                     "de-rated -43% — a DCA-grade value name. Buy on schedule."},
    "DV":   {"strategy": "cycle", "pos": "Mid", "cagr": (10, 20),
             "area": "AI ad-verification (DoubleVerify) — adtech measurement",
             "note": "Profitable, PEG 0.63 (cheap), fwd PE 9.9, net cash, FCF+. "
                     "AI-driven ad fraud/brand-safety measurement across CTV/social. "
                     "De-rated -26%; growth intact. Adtech-cyclical (ad-budget "
                     "sensitive). Buy dips / trim manias."},
    "ZETA": {"strategy": "cycle", "pos": "Mid", "cagr": (15, 25),
             "area": "AI marketing cloud / CDP (Zeta Global) — adtech",
             "note": "AI-driven marketing cloud + CDP (data-driven customer "
                     "acquisition). FCF+ ($200M ttm, 14% FCF margin) and net cash, "
                     "op margin +2.2%, but slightly GAAP-negative (-1.6% net) after "
                     "interest, on heavy dilution (+15.7% shares/yr). PEG 0.73, "
                     "P/S 3.9, fwd rev +22%. Margin trajectory sharply improving "
                     "(-54%->-7% net over 4y). Adtech-cyclical (ad-budget sensitive), "
                     "beta 1.37, 13% short. Buy dips / trim manias; watch dilution."},

    # --- Pre-/near-pre-profit AI punts (Binary — size tiny or skip, never avg down) ---
    "SOUN": {"strategy": "lottery", "pos": "Binary", "cagr": (-50, 60),
             "area": "Voice / conversational AI (SoundHound AI)",
             "note": "Pure-play voice AI (auto, drive-thru, call-centers). "
                     "GAAP-unprofitable (ROE -39%), heavy dilution (+13% shares/yr), "
                     "37% of float sold short, beta 2.74. P/S 15 on an unproven "
                     "model — a binary high-beta punt. Tiny size or skip; never "
                     "average down."},
    "BBAI": {"strategy": "lottery", "pos": "Binary", "cagr": (-50, 50),
             "area": "AI/defense analytics (BigBear.ai)",
             "note": "AI decision-intelligence for defense/gov. GAAP-unprofitable "
                     "(ROE -58%), severe dilution (+66% shares/yr), beta 3.08, "
                     "29% short. Lottery ticket on a defense-AI contract ramp — "
                     "binary outcome. Tiny size or skip; never average down."},

    # --- Global quality-compounder monitors (2026-08 conviction hunt) ---
    #     Sourced live from stockanalysis.com and scored via the DCA rubric; NOT
    #     held, added so their conviction renders on the dashboard. Quality/growth
    #     businesses (non-Binary) across several markets outside the AI-semi core.
    "FICO": {"strategy": "dca", "pos": "Mid", "cagr": (12, 22),
             "area": "Credit scoring / decision analytics (Fair Isaac, US)",
             "note": "Credit-scoring near-monopoly: the FICO score is embedded in "
                     "US lending. 34% net margin, high-quality recurring revenue, "
                     "and screened CHEAP on valuation (V 9.6) — the rare elite "
                     "business not priced for perfection. Top conviction of the hunt."},
    "MSCI": {"strategy": "dca", "pos": "Mid", "cagr": (8, 16),
             "area": "Index licensing / ESG+analytics (MSCI, US)",
             "note": "Index-licensing toll-road (41% net margin). Recurring, "
                     "price-inelastic fees on assets tracking its indices. "
                     "Quality compounder; valuation full but not extreme."},
    "SPGI": {"strategy": "dca", "pos": "Mid", "cagr": (7, 15),
             "area": "Ratings + market data (S&P Global, US)",
             "note": "Ratings duopoly (with MCO) + Market Intelligence data. "
                     "31% net margin, wide moat. Great business at a fair-to-rich "
                     "price — DCA-grade, not a deep-value entry."},
    "SE":   {"strategy": "dca", "pos": "Early/Mid", "cagr": (12, 28),
             "area": "SE-Asia e-commerce / gaming / fintech (Sea Ltd, Singapore)",
             "note": "Shopee + Garena + SeaMoney across Southeast Asia. Turned "
                     "profitable after the growth-at-all-costs era; screens cheap "
                     "on valuation. Higher EM/execution risk — monitor, size small."},
    "GLBE": {"strategy": "dca", "pos": "Early/Mid", "cagr": (18, 32),
             "area": "Cross-border e-commerce enablement (Global-E, Israel)",
             "note": "Picks-and-shovels for international D2C checkout (Shopify "
                     "partner). High quality (Q 8.5), durable growth. Smaller-cap "
                     "monitor — coverage ~80%, watch the trend series."},
    "MNDY": {"strategy": "dca", "pos": "Early/Mid", "cagr": (18, 30),
             "area": "Work-management SaaS (Monday.com, Israel)",
             "note": "Horizontal work-OS SaaS, now GAAP-profitable with strong "
                     "net retention. Durable-growth compounder screening cheap on "
                     "valuation. Monitor — SaaS competition is fierce."},
    "NTES": {"strategy": "dca", "pos": "Mid", "cagr": (8, 16),
             "area": "Games / online services (NetEase, China)",
             "note": "China's #2 games publisher (30% net margin), strong cash "
                     "generation. Cheap on China discount. Monitor — ADR/VIE + "
                     "China regulatory overhang; size accordingly."},
    "LULU": {"strategy": "dca", "pos": "Mid", "cagr": (8, 16),
             "area": "Premium athletic apparel (Lululemon, US/Canada)",
             "note": "Premium brand, high gross margin, strong ROIC. Screened "
                     "cheap after a de-rating (V 9.4). Monitor — apparel is "
                     "fashion-cyclical and US growth has matured."},

    # --- Second hunt batch (2026-08, QC'd). Tags reflect the QC findings:
    #     gold-royalty names are CYCLE (revenue tracks the metal, not durable
    #     growth); the rest DCA. Notes carry each name's QC caveat verbatim. ---
    "NDAQ": {"strategy": "dca", "pos": "Mid", "cagr": (7, 15),
             "area": "Exchange + market data/tech (Nasdaq, US)",
             "note": "QC: CLEAN — 100% coverage, real PEG, stable margins. "
                     "Exchange + recurring data/tech revenue. Honestly-scored "
                     "quality at a fair price (CONV ~7.4). One of the two most "
                     "trustworthy finds of the batch."},
    "VEEV": {"strategy": "dca", "pos": "Mid", "cagr": (10, 18),
             "area": "Life-sciences cloud / vertical SaaS (Veeva, US)",
             "note": "QC: CLEAN — 100% coverage, no flags. Near-monopoly vertical "
                     "SaaS for pharma. Durable-growth compounder (CONV ~7.8). The "
                     "other most trustworthy find of the batch."},
    "GMAB": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
             "area": "Antibody therapeutics (Genmab, Denmark)",
             "note": "QC: mostly clean (90% cov) but fwd_eps ~-33% (earnings "
                     "expected to FALL) and no PEG, so the high V leans on a low "
                     "P/S. Verify the EPS trajectory before trusting CONV ~7.5."},
    # WPM PROMOTED (RESHAPE-TRIM 2026-08) to W7_DIVERSIFY_TARGETS at 1.5% book
    #     (funded by the SMHV.SW trim) — the book's only precious-metals/commodity
    #     hedge. Removed from WATCHLIST; re-add here if it is ever cut to 0%.
    "ARGX": {"strategy": "catalyst", "pos": "Binary", "cagr": (-10, 40),
             "area": "Immunology / FcRn antibodies (argenx, Belgium)",
             "note": "QC: DO NOT TRUST THE SCORE. Biotech that JUST flipped "
                     "profitable — margin_hist [37|-23|-159|-76], rev_hist off a "
                     "tiny base (185%!), no PEG (P/S fallback). The high CONV ~8.3 "
                     "is the base-effect / turnaround ILLUSION the engine warns "
                     "about. Tagged catalyst; investigate, do not size on the number."},
    "VRSN": {"strategy": "dca", "pos": "Mid", "cagr": (5, 11),
             "area": ".com/.net domain registry (Verisign, US)",
             "note": "QC: the HONEST one. Real monopoly (88% gross/50% net, full "
                     "history) scored MID (CONV ~5.6) because it's fully/richly "
                     "valued (+15% above 200DMA) and only grows ~6%. Correctly "
                     "un-fooled — a great business is not a great BUY at this price."},
    "MKTX": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
             "area": "Electronic bond trading (MarketAxess, US)",
             "note": "QC: clean data, honest MID score (CONV ~5.5). PEG ~4 "
                     "(expensive) + decelerating revenue. Correctly not exciting — "
                     "quality franchise, unattractive entry."},

    # ===================================================================
    # 2026-08 third hunt — scored through score_holdings.py, NOT eyeballed.
    # Every CONV below is the ACTUAL engine output (binding layer noted).
    # Reality check baked in: this anti-momentum engine caps mature quality
    # names ~7.2-7.6; the only 8+ are high-growth SaaS turnarounds that carry
    # a NEG-MARGIN-HIST signal (the base-effect/turnaround illusion — see
    # SKILL.md Common Pitfalls §10). NONE is a clean, durable 8+.
    # -------------------------------------------------------------------
    # --- clean quality compounders (no illusion signal; CONV mid-7s) ---
    # AJG PROMOTED (RESHAPE-TRIM 2026-08) to W7_DIVERSIFY_TARGETS at 1.5% book
    #     (funded by the SMHV.SW trim) — the defensive financials-broker ballast
    #     leg the book lacked. Removed from WATCHLIST; re-add here if cut to 0%.
    "ICE":  {"strategy": "dca", "pos": "Mid", "cagr": (7, 13),
             "area": "Exchanges + mortgage data (Intercontinental Exch, US)",
             "note": "QC: CLEAN. CONV 7.23 (CYC binding), 100% cov. Exchange "
                     "+ data annuity; honest score, no turnaround flag."},
    "ZTS":  {"strategy": "dca", "pos": "Mid", "cagr": (7, 13),
             "area": "Animal health / vaccines (Zoetis, US)",
             "note": "QC: CLEAN. CONV 7.18 (CYC binding), 100% cov. Durable "
                     "franchise; capped by rich valuation, not data gaps."},
    "PGR":  {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
             "area": "Auto/P&C insurance (Progressive, US)",
             "note": "QC: CLEAN-ish. CONV 7.17 (FUN binding) at 80% cov "
                     "(insurer margins partly blank). Best-in-class underwriter."},
    "PAYC": {"strategy": "dca", "pos": "Mid", "cagr": (8, 16),
             "area": "Cloud payroll/HCM (Paycom, US)",
             "note": "QC: CLEAN. CONV 7.17 (CYC binding), 100% cov, no NEG "
                     "flag — genuinely profitable SaaS. Honest quality score."},
    "HSY":  {"strategy": "dca", "pos": "Mid", "cagr": (4, 10),
             "area": "Confectionery (Hershey, US)",
             "note": "QC: CLEAN. CONV 7.04 (FUN binding), 100% cov. Staple "
                     "compounder; low growth caps the FUND layer, no illusion."},
    "VRSK": {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "Insurance data/analytics (Verisk, US)",
             "note": "QC: CLEAN. CONV 6.59 (FUN binding), 100% cov. Data "
                     "annuity; honest mid score, richly valued."},
    "CME":  {"strategy": "dca", "pos": "Mid", "cagr": (5, 11),
             "area": "Derivatives exchange (CME Group, US)",
             "note": "QC: CLEAN. CONV 6.52 (CYC binding), 100% cov. Rate-"
                     "volatility annuity; honest, no turnaround flag."},
    "AON":  {"strategy": "dca", "pos": "Mid", "cagr": (7, 13),
             "area": "Insurance brokerage/consulting (Aon, US)",
             "note": "QC: CLEAN. CONV 6.49 (FUN binding), 100% cov. Broker "
                     "peer of AJG; honest mid-high score."},
    "YUM":  {"strategy": "dca", "pos": "Mid", "cagr": (6, 12),
             "area": "QSR franchising (Yum! Brands, US)",
             "note": "QC: CLEAN. CONV 6.49 (FUN binding), 100% cov. Asset-"
                     "light franchise royalty; honest, no illusion."},
    # --- profitable-but-pricey / honest MID names (kept for coverage) ---
    "ABBV": {"strategy": "dca", "pos": "Mid", "cagr": (5, 11),
             "area": "Biopharma (AbbVie, US)",
             "note": "QC: CLEAN. CONV 6.88 (FUN binding), 100% cov. Post-"
                     "Humira pipeline; honest score, patent-cliff risk in note."},

    # --- high-growth SaaS: 8+ ONLY because of a turnaround base effect ---
    #     Each has NEG-MARGIN-HIST (just flipped profitable). Treat the score
    #     as the base-effect illusion SKILL.md §10 warns about — NOT durable.
    "PD":   {"strategy": "dca", "pos": "Mid", "cagr": (5, 20),
             "area": "Incident/ops automation (PagerDuty, US)",
             "note": "QC: turnaround-illusion name. Pre-fix it printed CONV 8.2 "
                     "on -13.6% net margins (rewarded for improving losses, not "
                     "real profit). The margin-trend profitability gate now damps "
                     "that: CONV 7.87 (was 8.20), still-negative margins no longer "
                     "earn full expansion credit. Even so, treat as monitor-only — "
                     "unproven micro-cap that just squeaked toward breakeven."},
    "BRZE": {"strategy": "dca", "pos": "Mid", "cagr": (10, 25),
             "area": "Customer-engagement SaaS (Braze, US)",
             "note": "QC: CONV 7.96 (CYC binding) but NEG-MARGIN-HIST — barely "
                     "profitable, score flattered by the turnaround base effect. "
                     "Real growth is there (~25%) but the 8 is not durable yet."},
    "AFRM": {"strategy": "catalyst", "pos": "Binary", "cagr": (-15, 40),
             "area": "Buy-now-pay-later (Affirm, US)",
             "note": "QC: CONV 7.88 (CYC binding) is a NEG-MARGIN-HIST credit-"
                     "cycle turnaround — BNPL P&L swings with charge-offs and "
                     "rates. Tagged catalyst/Binary (downside is real). The 8 is "
                     "an illusion; treat as a binary macro bet."},
    "PINS": {"strategy": "dca", "pos": "Mid", "cagr": (8, 20),
             "area": "Visual-discovery ad platform (Pinterest, US)",
             "note": "QC: CONV 7.80 (CYC binding), NEG-MARGIN-HIST (recent "
                     "GAAP-profit flip). Ad-cyclical; score flattered by the "
                     "turnaround base. Durable score mid-6s."},
    "APPF": {"strategy": "dca", "pos": "Mid", "cagr": (10, 22),
             "area": "Property-management SaaS (AppFolio, US)",
             "note": "QC: CONV 7.75 (CYC binding), NEG-MARGIN-HIST. Real "
                     "vertical-SaaS growth but the 7.8 leans on the profit-flip "
                     "base effect. Monitor; not a clean durable 8."},
    "DOCU": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
             "area": "E-signature / agreements (DocuSign, US)",
             "note": "QC: CONV 7.71 (CYC binding), NEG-MARGIN-HIST + very rich "
                     "VAL 9.9. Post-COVID normaliser that just turned GAAP-"
                     "profitable; score flattered by the base effect."},
    "ASAN": {"strategy": "dca", "pos": "Mid", "cagr": (8, 18),
             "area": "Work-management SaaS (Asana, US)",
             "note": "QC: CONV 7.58 (CYC binding), NEG-MARGIN-HIST, 90% cov. "
                     "Still burning on GAAP; the score is the turnaround "
                     "illusion. Founder-led but unproven durability."},
    "FRSH": {"strategy": "dca", "pos": "Mid", "cagr": (10, 20),
             "area": "CX/ITSM SaaS (Freshworks, US)",
             "note": "QC: CONV 7.54 (CYC binding), NEG-MARGIN-HIST. Recent "
                     "profit flip inflates the score; real ~18% growth. Durable "
                     "read is mid-6s. Monitor."},
    "SNAP": {"strategy": "catalyst", "pos": "Binary", "cagr": (-20, 35),
             "area": "Social/AR ad platform (Snap, US)",
             "note": "QC: CONV 7.34 (FUN binding), NEG-MARGIN-HIST — chronically "
                     "unprofitable, ad-cyclical, heavy dilution. Tagged "
                     "catalyst/Binary: the score is a turnaround HOPE, downside "
                     "is real. Do not trust as a quality name."},
    "WIX":  {"strategy": "dca", "pos": "Mid", "cagr": (10, 18),
             "area": "Website-building SaaS (Wix, Israel)",
             "note": "QC: CONV 7.05 (FUN binding), NEG-MARGIN-HIST. Just turned "
                     "FCF/GAAP positive; score flattered by the flip. Honest "
                     "durable read mid-6s."},
    "NCNO": {"strategy": "dca", "pos": "Mid", "cagr": (8, 18),
             "area": "Cloud banking software (nCino, US)",
             "note": "QC: CONV 7.04 (FUN binding), NEG-MARGIN-HIST, 90% cov. "
                     "Vertical SaaS turnaround; the 7 is the base-effect illusion."},
    "RBLX": {"strategy": "catalyst", "pos": "Binary", "cagr": (-15, 35),
             "area": "UGC gaming platform (Roblox, US)",
             "note": "QC: CONV 6.77 (FUN binding), NEG-MARGIN-HIST, 90% cov. "
                     "Persistently unprofitable on GAAP, bookings-driven. Tagged "
                     "catalyst/Binary — the score is a growth bet, not quality."},
    "DLO":  {"strategy": "cycle", "pos": "Mid", "cagr": (10, 25),
             "area": "Emerging-markets payments (DLocal, Uruguay)",
             "note": "QC: CONV 6.77 (CYC binding), 90% cov, no NEG flag but "
                     "EM-FX/regulatory cyclical (take-rate compresses). Tagged "
                     "cycle. Honest mid score; real growth, real EM risk."},

    # =====================================================================
    # WORLD EX-US CANDIDATE BATCH (2026-08-04) — new non-US large/mid caps
    # sourced to widen the ex-US bench. All resolved on stockanalysis.com and
    # were wired into the CSV via `--sync-csv`; each carries a tentative tag so
    # `--by-strategy --watchlist` grades it and the CSV<->WATCHLIST coverage
    # gate stays clean. Tags: quality compounders -> dca; banks/energy/miners/
    # autos/memory/semi-cap/industrial cyclicals -> cycle. Notes are the thesis
    # PRE-scoring (no CONV yet) — refine after the first score pass.
    # ---- Japan (.T) ----
    "6857.T": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 25),
               "area": "Semi ATE / test (Advantest, Japan)",
               "note": "SoC/HBM tester duopoly with Teradyne; AI-test cyclical."},
    "6146.T": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 25),
               "area": "Semi dicing/grinding (Disco, Japan)",
               "note": "Near-monopoly back-end dicing/grinding tools; WFE cyclical."},
    "6920.T": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 25),
               "area": "EUV mask inspection (Lasertec, Japan)",
               "note": "Sole EUV actinic mask-inspection supplier; rich, cyclical."},
    "6981.T": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 18),
               "area": "MLCC / electronic components (Murata, Japan)",
               "note": "MLCC leader; component cycle tied to handset/auto/AI."},
    "6762.T": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 18),
               "area": "Electronic components (TDK, Japan)",
               "note": "MLCC + batteries (ATL); components/handset cyclical."},
    "6367.T": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
               "area": "HVAC (Daikin, Japan)",
               "note": "Global HVAC leader; heat-pump/data-center cooling secular."},
    "7741.T": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
               "area": "Optics / EUV-blanks / medical (Hoya, Japan)",
               "note": "EUV mask blanks + endoscope optics; high-margin compounder."},
    "6273.T": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
               "area": "Factory pneumatics (SMC, Japan)",
               "note": "Global pneumatics leader; automation secular, mild cyclical."},
    "4568.T": {"strategy": "dca", "pos": "Mid", "cagr": (6, 16),
               "area": "Pharma / oncology ADC (Daiichi Sankyo, Japan)",
               "note": "Enhertu ADC franchise; oncology growth compounder."},
    "4543.T": {"strategy": "dca", "pos": "Mid", "cagr": (5, 12),
               "area": "Medical devices (Terumo, Japan)",
               "note": "Cardiovascular/blood-management devices; steady compounder."},
    "6954.T": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 18),
               "area": "Factory automation / robots (Fanuc, Japan)",
               "note": "CNC + industrial-robot leader; capex-cyclical."},
    "6503.T": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 14),
               "area": "Industrial / power / automation (Mitsubishi Electric)",
               "note": "Grid + factory automation; industrial cyclical."},
    "8766.T": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 12),
               "area": "P&C insurance (Tokio Marine, Japan)",
               "note": "Largest JP P&C insurer; rate-driven, mild cyclical."},
    "4901.T": {"strategy": "dca", "pos": "Mid", "cagr": (4, 12),
               "area": "Imaging / healthcare / materials (Fujifilm, Japan)",
               "note": "Bio-CDMO + imaging pivot; diversified compounder."},

    # ---- Taiwan (.TW) ----
    "2308.TW": {"strategy": "dca", "pos": "Mid", "cagr": (8, 20),
                "area": "Power / EV / cooling (Delta Electronics, Taiwan)",
                "note": "Power-supply + liquid-cooling AI-datacenter beneficiary."},
    "2382.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 25),
                "area": "AI server ODM (Quanta, Taiwan)",
                "note": "Top AI-server ODM (GB200 racks); ODM-margin cyclical."},
    "6669.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 30),
                "area": "AI server / rack (Wiwynn, Taiwan)",
                "note": "Hyperscaler AI-rack ODM; hypergrowth but ODM-thin margin."},
    "2379.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (6, 18),
                "area": "Connectivity / comms chips (Realtek, Taiwan)",
                "note": "Ethernet/WiFi/audio fabless; chip-cycle sensitive."},
    "3034.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 16),
                "area": "Display-driver / SoC (Novatek, Taiwan)",
                "note": "DDIC + TDDI fabless; display/handset cyclical."},
    "3008.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 16),
                "area": "Smartphone optics (Largan, Taiwan)",
                "note": "High-end phone lens leader; handset-cycle, rich margin."},
    "3711.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (6, 18),
                "area": "OSAT packaging/test (ASE, Taiwan)",
                "note": "Largest OSAT; advanced-packaging (CoWoS) cyclical."},
    "2891.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 12),
                "area": "Bank / financial (CTBC, Taiwan)",
                "note": "Large TW financial holding; rate/credit cyclical."},
    "2412.TW": {"strategy": "dca", "pos": "Mid", "cagr": (2, 7),
                "area": "Telecom (Chunghwa Telecom, Taiwan)",
                "note": "Incumbent telecom; low-growth defensive dividend."},
    "2357.TW": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 14),
                "area": "PC / AI hardware (Asustek, Taiwan)",
                "note": "PC + AI-server boards; consumer-hardware cyclical."},

    # ---- Korea (.KS) ----
    "207940.KS": {"strategy": "dca", "pos": "Mid", "cagr": (10, 25),
                  "area": "Biopharma CDMO (Samsung Biologics, Korea)",
                  "note": "World-scale antibody CDMO; secular capacity ramp."},
    "006400.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 25),
                  "area": "EV batteries (Samsung SDI, Korea)",
                  "note": "Prismatic EV/ESS cells; battery-demand cyclical."},
    "373220.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 30),
                  "area": "EV batteries (LG Energy Solution, Korea)",
                  "note": "Largest ex-China EV-cell maker; IRA-driven cyclical ramp."},
    "068270.KS": {"strategy": "dca", "pos": "Mid", "cagr": (8, 20),
                  "area": "Biosimilars (Celltrion, Korea)",
                  "note": "Biosimilar leader; pipeline-driven growth compounder."},
    "105560.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 12),
                  "area": "Bank (KB Financial, Korea)",
                  "note": "Top KR bank holding; rate/credit cyclical, cheap."},
    "005490.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 15),
                  "area": "Steel / battery materials (POSCO, Korea)",
                  "note": "Steel + lithium/cathode pivot; deep cyclical."},
    "012330.KS": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 12),
                  "area": "Auto parts (Hyundai Mobis, Korea)",
                  "note": "Hyundai/Kia module + EV-parts supplier; auto cyclical."},

    # ---- Hong Kong (.HK) ----
    "1299.HK": {"strategy": "dca", "pos": "Mid", "cagr": (8, 18),
                "area": "Pan-Asia life insurance (AIA, Hong Kong)",
                "note": "Structural Asia life-insurance compounder; VNB growth."},
    "0388.HK": {"strategy": "dca", "pos": "Mid", "cagr": (6, 16),
                "area": "Exchange operator (HKEX, Hong Kong)",
                "note": "HK bourse monopoly; ADT/IPO-cyclical toll-road."},
    "1024.HK": {"strategy": "cycle", "pos": "Mid", "cagr": (8, 22),
                "area": "Short-video / ads (Kuaishou, China)",
                "note": "#2 China short-video; ad + e-commerce, China-ad cyclical."},
    "9868.HK": {"strategy": "cycle", "pos": "Early", "cagr": (5, 40),
                "area": "EV maker (XPeng, China)",
                "note": "China smart-EV; strong deliveries, thin/negative margin — "
                        "cyclical ramp, watch profitability."},
    "2020.HK": {"strategy": "dca", "pos": "Mid", "cagr": (6, 16),
                "area": "Sportswear (Anta Sports, China)",
                "note": "China sportswear leader (Anta/FILA/Amer); brand compounder."},
    "0175.HK": {"strategy": "cycle", "pos": "Mid", "cagr": (6, 20),
                "area": "Autos / EV (Geely, China)",
                "note": "China auto + Zeekr/Lynk EV brands; auto-cycle sensitive."},
    "0883.HK": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 12),
                "area": "Oil & gas E&P (CNOOC, China)",
                "note": "Low-cost offshore E&P; oil-price cyclical, big dividend."},
    "2331.HK": {"strategy": "dca", "pos": "Mid", "cagr": (5, 14),
                "area": "Sportswear (Li Ning, China)",
                "note": "China domestic sportswear brand; consumer-discretionary."},

    # ---- Germany (.DE) ----
    "ADS.DE": {"strategy": "dca", "pos": "Mid", "cagr": (6, 16),
               "area": "Sportswear (Adidas, Germany)",
               "note": "Global #2 sportswear; post-Yeezy brand-recovery compounder."},
    "DB1.DE": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
               "area": "Exchange / market infra (Deutsche Boerse)",
               "note": "Diversified exchange + data; toll-road compounder."},
    "BEI.DE": {"strategy": "dca", "pos": "Mid", "cagr": (4, 10),
               "area": "Consumer staples (Beiersdorf, Germany)",
               "note": "Nivea/Eucerin skincare; defensive staples compounder."},
    "DHL.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 12),
               "area": "Logistics (DHL Group, Germany)",
               "note": "Global express/freight; trade-volume cyclical, dividend."},
    "MRK.DE": {"strategy": "dca", "pos": "Mid", "cagr": (5, 12),
               "area": "Pharma / life-science / electronics (Merck KGaA)",
               "note": "Diversified science: pharma + lab tools + semi materials."},
    "HEN3.DE": {"strategy": "dca", "pos": "Mid", "cagr": (3, 10),
                "area": "Consumer / adhesives (Henkel, Germany)",
                "note": "Adhesives + beauty/laundry; defensive staples."},
    "P911.DE": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 12),
                "area": "Luxury autos (Porsche AG, Germany)",
                "note": "Luxury-auto brand; premium margin but auto-cycle sensitive."},

    # ---- Netherlands (.AS) ----
    "ADYEN.AS": {"strategy": "dca", "pos": "Mid", "cagr": (15, 30),
                 "area": "Payments platform (Adyen, Netherlands)",
                 "note": "Single-platform global acquirer; high-growth, high-margin."},
    "PHIA.AS": {"strategy": "dca", "pos": "Mid", "cagr": (3, 10),
                "area": "Health-tech / imaging (Philips, Netherlands)",
                "note": "Medical imaging + monitoring; post-recall turnaround."},
    "AD.AS": {"strategy": "dca", "pos": "Mid", "cagr": (2, 7),
              "area": "Grocery retail (Ahold Delhaize, Netherlands)",
              "note": "US/EU grocery; defensive low-growth staples compounder."},
    "DSFIR.AS": {"strategy": "dca", "pos": "Mid", "cagr": (4, 12),
                 "area": "Nutrition / flavors (DSM-Firmenich, NL/CH)",
                 "note": "Nutrition + fragrance/flavor merger; specialty compounder."},

    # ---- Switzerland (.SW) ----
    "STMN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (8, 16),
                "area": "Dental implants (Straumann, Switzerland)",
                "note": "Global dental-implant leader; secular high-margin compounder."},
    "TEMN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (5, 14),
                "area": "Core-banking software (Temenos, Switzerland)",
                "note": "Bank core-software; SaaS transition, sticky recurring."},
    "UHR.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 12),
               "area": "Luxury watches (Swatch Group, Switzerland)",
               "note": "Watch brands (Omega/Swatch); China-luxury cyclical."},
    "SGSN.SW": {"strategy": "dca", "pos": "Mid", "cagr": (3, 10),
                "area": "Testing / inspection (SGS, Switzerland)",
                "note": "Global TIC leader; steady toll-road compounder."},
    "KNIN.SW": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 12),
                "area": "Freight forwarding (Kuehne+Nagel, Switzerland)",
                "note": "Sea/air freight forwarder; freight-rate cyclical."},

    # ---- France (.PA) ----
    "HO.PA": {"strategy": "dca", "pos": "Mid", "cagr": (5, 14),
              "area": "Defense / aerospace / digital (Thales, France)",
              "note": "Defense electronics + cyber; EU-rearmament secular."},
    "DSY.PA": {"strategy": "dca", "pos": "Mid", "cagr": (6, 15),
               "area": "Engineering / PLM software (Dassault Systemes)",
               "note": "3DEXPERIENCE PLM + Medidata; sticky software compounder."},
    "RI.PA": {"strategy": "dca", "pos": "Mid", "cagr": (3, 10),
              "area": "Spirits (Pernod Ricard, France)",
              "note": "#2 global spirits; brand compounder, China-luxury sensitive."},
    "ML.PA": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 10),
              "area": "Tires (Michelin, France)",
              "note": "Premium tire leader; auto/replacement-cycle sensitive."},
    "VIE.PA": {"strategy": "dca", "pos": "Mid", "cagr": (3, 10),
               "area": "Water / waste / energy (Veolia, France)",
               "note": "Environmental-services utility; regulated defensive."},

    # ---- United Kingdom (.L) ----
    "SGE.L": {"strategy": "dca", "pos": "Mid", "cagr": (5, 13),
              "area": "SME accounting software (Sage, UK)",
              "note": "SMB cloud accounting/payroll; sticky recurring SaaS."},
    "EXPN.L": {"strategy": "dca", "pos": "Mid", "cagr": (5, 12),
               "area": "Credit data / analytics (Experian, UK)",
               "note": "Credit-bureau duopoly + data/analytics; toll-road compounder."},
    "AAL.L": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 15),
              "area": "Diversified miner (Anglo American, UK)",
              "note": "Copper/PGM/iron miner; commodity-price deep cyclical."},
    "RKT.L": {"strategy": "dca", "pos": "Mid", "cagr": (2, 8),
              "area": "Consumer health / hygiene (Reckitt, UK)",
              "note": "Lysol/Durex/Mucinex staples; defensive, turnaround."},
    "CPG.L": {"strategy": "dca", "pos": "Mid", "cagr": (5, 12),
              "area": "Contract catering (Compass Group, UK)",
              "note": "Global #1 food-services outsourcer; steady compounder."},
    "STAN.L": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 12),
               "area": "EM bank (Standard Chartered, UK)",
               "note": "Asia/ME/Africa-focused bank; rate/EM-credit cyclical."},
    "NWG.L": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 10),
              "area": "UK bank (NatWest Group, UK)",
              "note": "UK retail/commercial bank; rate-cyclical, buyback-heavy."},

    # ---- Canada (.TO) ----
    "DOL.TO": {"strategy": "dca", "pos": "Mid", "cagr": (8, 15),
               "area": "Discount retail (Dollarama, Canada)",
               "note": "Dollar-store compounder + Dollarcity LatAm; defensive growth."},
    "IFC.TO": {"strategy": "dca", "pos": "Mid", "cagr": (5, 13),
               "area": "P&C insurance (Intact Financial, Canada)",
               "note": "Leading Canadian P&C insurer; disciplined compounder."},
    "WSP.TO": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
               "area": "Engineering / consulting (WSP Global, Canada)",
               "note": "Global E&C roll-up; infrastructure-spend secular."},
    "L.TO": {"strategy": "dca", "pos": "Mid", "cagr": (3, 9),
             "area": "Grocery / pharmacy (Loblaw, Canada)",
             "note": "Canada's largest grocer + Shoppers; defensive staples."},

    # ---- Australia (.AX) ----
    "WTC.AX": {"strategy": "dca", "pos": "Mid", "cagr": (12, 28),
               "area": "Logistics software (WiseTech, Australia)",
               "note": "CargoWise freight-forwarding SaaS; high-margin compounder."},
    "XRO.AX": {"strategy": "dca", "pos": "Mid", "cagr": (12, 25),
               "area": "SMB accounting SaaS (Xero, Australia)",
               "note": "Cloud accounting for SMBs; ARR compounder, rule-of-40."},
    "PME.AX": {"strategy": "dca", "pos": "Mid", "cagr": (15, 30),
               "area": "Medical imaging software (Pro Medicus, Australia)",
               "note": "Radiology PACS/Visage SaaS; ~70% margin hypergrowth, rich."},
    "COH.AX": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
               "area": "Hearing implants (Cochlear, Australia)",
               "note": "Cochlear-implant leader; secular high-margin compounder."},

    # ---- India (.NS) ----
    "HCLTECH.NS": {"strategy": "dca", "pos": "Mid", "cagr": (6, 14),
                   "area": "IT services (HCL Technologies, India)",
                   "note": "Top-3 India IT + software products; steady compounder."},
    "DMART.NS": {"strategy": "dca", "pos": "Mid", "cagr": (12, 22),
                 "area": "Value retail (Avenue Supermarts/DMart, India)",
                 "note": "Hypermarket compounder; India-consumption secular, rich."},
    "ETERNAL.NS": {"strategy": "cycle", "pos": "Early", "cagr": (15, 40),
                   "area": "Food delivery / quick-commerce (Eternal/Zomato)",
                   "note": "India food-delivery + Blinkit q-commerce; hypergrowth, "
                           "profitability young — watch q-commerce burn."},
    "HAL.NS": {"strategy": "dca", "pos": "Mid", "cagr": (8, 20),
               "area": "Defense aerospace (Hindustan Aeronautics, India)",
               "note": "India military-aircraft monopoly; indigenization order book."},
    "POWERGRID.NS": {"strategy": "dca", "pos": "Mid", "cagr": (5, 12),
                     "area": "Power transmission (Power Grid Corp, India)",
                     "note": "Regulated transmission monopoly; steady RoE, dividend."},
    "NTPC.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 14),
                "area": "Power generation (NTPC, India)",
                "note": "India's largest power producer + renewables pivot; utility."},
    "COALINDIA.NS": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 10),
                     "area": "Coal mining (Coal India)",
                     "note": "State coal monopoly; commodity/volume cyclical, dividend."},

    # ---- Sweden (.ST) ----
    "EVO.ST": {"strategy": "dca", "pos": "Mid", "cagr": (10, 22),
               "area": "Live-casino B2B (Evolution AB, Sweden)",
               "note": "Live-dealer iGaming supplier; ~60% margin compounder, "
                       "regulatory/grey-market overhang."},

    # ---- Spain (.MC) ----
    "AMS.MC": {"strategy": "dca", "pos": "Mid", "cagr": (8, 16),
               "area": "Travel tech / GDS (Amadeus, Spain)",
               "note": "Airline GDS + IT solutions; travel-recovery compounder."},
    "CLNX.MC": {"strategy": "dca", "pos": "Mid", "cagr": (5, 14),
                "area": "Telecom towers (Cellnex, Spain)",
                "note": "European tower leader; contracted cash flows, debt-heavy."},
    "AENA.MC": {"strategy": "dca", "pos": "Mid", "cagr": (3, 10),
                "area": "Airport operator (Aena, Spain)",
                "note": "Spanish airport monopoly; traffic-driven infra compounder."},

    # ---- Saudi Arabia (.SR) ----
    "1120.SR": {"strategy": "cycle", "pos": "Mid", "cagr": (5, 15),
                "area": "Bank (Al Rajhi Bank, Saudi Arabia)",
                "note": "Largest Islamic bank; Saudi-credit growth, rate cyclical."},
    "2010.SR": {"strategy": "cycle", "pos": "Mid", "cagr": (2, 12),
                "area": "Chemicals (SABIC, Saudi Arabia)",
                "note": "Global petrochemical major; commodity-chem deep cyclical."},

    # ---- South Africa (.JO) ----
    "CPI.JO": {"strategy": "cycle", "pos": "Mid", "cagr": (10, 22),
               "area": "Digital bank (Capitec, South Africa)",
               "note": "SA retail-bank disruptor; high-growth, credit-cyclical."},
    "FSR.JO": {"strategy": "cycle", "pos": "Mid", "cagr": (4, 12),
               "area": "Bank (FirstRand, South Africa)",
               "note": "SA banking group (FNB/RMB); rate/credit cyclical."},
    "MTN.JO": {"strategy": "cycle", "pos": "Mid", "cagr": (3, 15),
               "area": "Telecom (MTN Group, South Africa)",
               "note": "Pan-Africa mobile + fintech; EM-FX/regulatory cyclical."},
    # CONV-MAXIMISING HUNT (2026-08-04) — 122 US/global names sourced &
    # scored through score_holdings.py, ranked by CONV, then QC'd per
    # SKILL.md sec.10 (APPN dropped: corrupt net_margin_hist). Deep
    # cyclicals (miners/energy) tagged 'cycle'; quality compounders 'dca'.
    # Notes carry the illusion caveat for any trough-PEG / margin-flip name.
    # =====================================================================
    # NBIX PROMOTED (RESHAPE 2026-08) to W7_DIVERSIFY_TARGETS at 1.5% book (funded
    #     by the SYM cut + part of the ALAB cut) — highest-CONV non-held name on the
    #     board (8.61), adds a neuroscience-pharma diversifier off the AI-capex chain.
    #     Removed from WATCHLIST; re-add here if it is ever cut to 0%.
    # PODD PROMOTED (RESHAPE-TRIM 2026-08) to W7_DIVERSIFY_TARGETS at 2.0% book
    #     (funded by the SMHV.SW trim) — anchors a new health-care leg (Omnipod
    #     insulin pumps). Removed from WATCHLIST; re-add here if cut to 0%.
    # ONON PROMOTED (RESHAPE-TRIM 2026-08) to W7_DIVERSIFY_TARGETS at 1.5% book
    #     (funded by a further SMHV.SW trim) — the book's only consumer-brand leg.
    #     Removed from WATCHLIST; re-add here if it is ever cut to 0%.
    "CARS": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Auto marketplace (Cars.com)',
        "note":     'Small-cap auto-listings SaaS; steady low-teens rev, FCF+. margin_hist noisy but positive.',
    },
    "FIS": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Fintech / payments infra (Fidelity Natl Info)',
        "note":     'Payments/banking-software giant; cheap (PEG 0.52), FCF+, single-digit rev. Value compounder.',
    },
    "MTCH": {
        "pos":      "Mid",
        "cagr":     (6, 14),
        "strategy": "dca",
        "area":     'Online dating platforms (Match Group)',
        "note":     'Tinder/Hinge owner; high 73% gross, ~19% net, cheap PEG 0.86. Flat rev is the risk — quality-cheap, not growth.',
    },
    "YELP": {
        "pos":      "Mid",
        "cagr":     (6, 14),
        "strategy": "dca",
        "area":     'Local-business marketplace (Yelp)',
        "note":     '90% gross local-ads platform; FCF+, cheap PEG 0.88. Slow rev; buy-back driven EPS.',
    },
    "KGC": {
        "pos":      "Mid",
        "cagr":     (8, 20),
        "strategy": "cycle",
        "area":     'Gold miner (Kinross Gold)',
        "note":     'Deep-cyclical gold; F 9.2 on gold-price windfall. margin_hist flips (-16% FY) = commodity cycle, not quality. Buy dips, trim near peak.',
    },
    "RGLD": {
        "pos":      "Mid",
        "cagr":     (8, 18),
        "strategy": "cycle",
        "area":     'Gold royalty (Royal Gold)',
        "note":     'Royalty model, 87% gross / 49% net, FCF+. Higher-quality gold exposure than a miner but still gold-price cyclical.',
    },
    "TW": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Fixed-income trading venue (Tradeweb)',
        "note":     'Electronic-trading network; ~25% rev, high margin, FCF+. Structural e-trading share gainer.',
    },
    "HALO": {
        "pos":      "Mid",
        "cagr":     (10, 20),
        "strategy": "dca",
        "area":     'Drug-delivery platform (Halozyme)',
        "note":     'ENHANZE royalty engine; high margin, FCF+, PEG cheap. Royalty concentration is the risk.',
    },
    "OMC": {
        "pos":      "Mid",
        "cagr":     (5, 11),
        "strategy": "dca",
        "area":     'Advertising holding co (Omnicom)',
        "note":     'Ad agency; cheap PEG 0.62, FCF+. margin_hist flat-to-flip; low-growth value. IPG merger pending.',
    },
    "DSGX": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Supply-chain SaaS (Descartes Systems)',
        "note":     'Logistics-network software; consistent low-20s rev, high margin, FCF+. Quiet compounder.',
    },
    "GWRE": {
        "pos":      "Mid",
        "cagr":     (12, 20),
        "strategy": "dca",
        "area":     'P&C insurance SaaS (Guidewire)',
        "note":     'Insurance-core cloud migration; ~20% rev accelerating, FCF+. margin_hist turning positive — early expander.',
    },
    "AR": {
        "pos":      "Mid",
        "cagr":     (6, 20),
        "strategy": "cycle",
        "area":     'Natural gas E&P (Antero Resources)',
        "note":     'Appalachian gas; deep-cyclical, F 7.2 on gas-price rebound. margin_hist flips sign = commodity cycle. Buy dips only.',
    },
    "CBOE": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Options exchange (Cboe Global)',
        "note":     'Derivatives-exchange oligopoly; high margin, FCF+, steady. Vol-franchise moat.',
    },
    "RMD": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Sleep/respiratory devices (ResMed)',
        "note":     'CPAP/sleep-apnea leader; high margin, FCF+, cheap after GLP-1 fear. Quality medtech compounder.',
    },
    "BL": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Accounting-automation SaaS (BlackLine)',
        "note":     'Financial-close software; FCF+, margins turning up. margin_hist flip = recent profit inflection (mild base effect).',
    },
    "CPAY": {
        "pos":      "Mid",
        "cagr":     (9, 16),
        "strategy": "dca",
        "area":     'Corporate-payments (Corpay, ex-FLEETCOR)',
        "note":     'Fleet/B2B payments; high margin, FCF+, PEG cheap. Steady compounder.',
    },
    "JAZZ": {
        "pos":      "Mid",
        "cagr":     (6, 14),
        "strategy": "dca",
        "area":     'Biopharma (Jazz Pharmaceuticals)',
        "note":     'Epidiolex/oncology; cheap PEG 0.18 — but that PEG rests on 202% fwd-EPS off a trough. Trough-PEG illusion; real value is mid, not top-tier.',
    },
    "BSY": {
        "pos":      "Mid",
        "cagr":     (10, 17),
        "strategy": "dca",
        "area":     'Infrastructure-engineering SaaS (Bentley)',
        "note":     'Civil-infra design software; ~11% rev, high margin, FCF+. Niche compounder.',
    },
    "AEM": {
        "pos":      "Mid",
        "cagr":     (8, 18),
        "strategy": "cycle",
        "area":     'Gold miner (Agnico Eagle)',
        "note":     'Best-in-class gold miner; F 9.1 on gold windfall, margins expanding. Still gold-price cyclical — trim near peak.',
    },
    "RJF": {
        "pos":      "Mid",
        "cagr":     (7, 14),
        "strategy": "dca",
        "area":     'Wealth mgmt / broker-dealer (Raymond James)',
        "note":     'Advisor-network franchise; FCF+, cheap. Rate/market-cyclical earnings.',
    },
    "WMG": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Music-rights major (Warner Music)',
        "note":     'Recorded-music/publishing catalog; FCF+, streaming-royalty annuity. Slow but durable.',
    },
    "PTC": {
        "pos":      "Mid",
        "cagr":     (9, 16),
        "strategy": "dca",
        "area":     'Industrial/CAD-PLM SaaS (PTC Inc.)',
        "note":     'CAD/PLM + IoT; high margin, FCF+, recurring. Steady enterprise compounder.',
    },
    "EOG": {
        "pos":      "Mid",
        "cagr":     (5, 16),
        "strategy": "cycle",
        "area":     'Oil & gas E&P (EOG Resources)',
        "note":     "Best-in-class shale; 27% net, FCF+, cheap. Deep-cyclical oil — buy weakness, don't chase.",
    },
    "ITT": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Diversified industrial (ITT Inc.)',
        "note":     'Flow/motion/connectors; FCF+, steady mid-teens returns. Quality industrial.',
    },
    "APH": {
        "pos":      "Mid",
        "cagr":     (10, 17),
        "strategy": "dca",
        "area":     'Connectors / interconnect (Amphenol)',
        "note":     'Broad connector leader; ~50% rev on AI/datacom, FCF+. Cyclical-industrial but high quality.',
    },
    "DT": {
        "pos":      "Mid",
        "cagr":     (12, 20),
        "strategy": "dca",
        "area":     'Observability SaaS (Dynatrace)',
        "note":     'APM/observability; ~20% rev, high margin, FCF+. Durable enterprise software.',
    },
    "PEN": {
        "pos":      "Mid",
        "cagr":     (12, 20),
        "strategy": "dca",
        "area":     'Neurovascular devices (Penumbra)',
        "note":     'Stroke/thrombectomy devices; ~20% rev, FCF+. Category-leader medtech.',
    },
    "CVLT": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Data-protection SaaS (Commvault)',
        "note":     'Backup/cyber-resilience; recurring rev, FCF+, margins up. Turnaround-to-SaaS working.',
    },
    "UTHR": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Rare-disease biopharma (United Therapeutics)',
        "note":     'Pulmonary-hypertension franchise + org-manufacturing optionality; FCF+, cheap. Pipeline concentration risk.',
    },
    "NICE": {
        "pos":      "Mid",
        "cagr":     (9, 16),
        "strategy": "dca",
        "area":     'Contact-center SaaS (NICE Ltd)',
        "note":     'CX/analytics cloud; high margin, FCF+, cheap. Cloud-transition compounder.',
    },
    "FOUR": {
        "pos":      "Mid",
        "cagr":     (12, 22),
        "strategy": "dca",
        "area":     'Payments (Shift4)',
        "note":     'Integrated-payments scaler; FCF+, cheap PEG 0.49. margin_hist flip = recent profit ramp (mild base effect).',
    },
    "NVT": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Electrical-infra / enclosures (nVent)',
        "note":     'Electrification/datacenter enclosures; FCF+, steady. Cyclical-industrial quality.',
    },
    "EXEL": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Oncology biopharma (Exelixis)',
        "note":     'Cabometyx franchise + pipeline; FCF+, cheap. Single-drug concentration risk.',
    },
    "GPN": {
        "pos":      "Mid",
        "cagr":     (6, 13),
        "strategy": "dca",
        "area":     'Payments (Global Payments)',
        "note":     'Merchant-acquiring; cheap PEG 0.7, FCF+. Consolidation/margin story.',
    },
    "CCCS": {
        "pos":      "Early/Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Insurance-claims SaaS (CCC Intelligent)',
        "note":     'Auto-claims network; recurring rev, FCF+. margin_hist noisy — early expander. CYCLE layer thin.',
    },
    "EXPE": {
        "pos":      "Mid",
        "cagr":     (7, 14),
        "strategy": "dca",
        "area":     'Online travel (Expedia)',
        "note":     'OTA scale; FCF+, cheap, buy-back heavy. Travel-cyclical demand.',
    },
    "FIVE": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Discount retail (Five Below)',
        "note":     'Teen-value retailer; unit-growth story, FCF+. Consumer-discretionary cyclical.',
    },
    "OTEX": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Enterprise info-mgmt (OpenText)',
        "note":     'Content/data software roll-up; FCF+, cheap. Debt-funded M&A; rev lumpy (TTM -10%).',
    },
    "TPR": {
        "pos":      "Mid",
        "cagr":     (6, 13),
        "strategy": "dca",
        "area":     'Accessible-luxury (Tapestry)',
        "note":     'Coach/Kate Spade; FCF+, cheap, brand turnaround. Consumer-discretionary cyclical.',
    },
    "DVN": {
        "pos":      "Mid",
        "cagr":     (5, 15),
        "strategy": "cycle",
        "area":     'Oil & gas E&P (Devon Energy)',
        "note":     'Shale oil+gas; FCF+, high net, cheap. Deep-cyclical — margin_hist flips with oil. Buy dips.',
    },
    "WEX": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Fleet/corporate payments (WEX Inc.)',
        "note":     'Fleet-card + benefits payments; FCF+, cheap. Fuel-price-sensitive.',
    },
    "SPSC": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Retail-supply-chain SaaS (SPS Commerce)',
        "note":     'EDI/fulfillment network; ~20% rev, FCF+, high margin. Durable niche compounder.',
    },
    "KEYS": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Electronic test & measure (Keysight)',
        "note":     'T&M instruments; FCF+, high margin. Capex-cyclical but quality.',
    },
    "NYT": {
        "pos":      "Mid",
        "cagr":     (8, 14),
        "strategy": "dca",
        "area":     'Digital news subscription (NY Times)',
        "note":     'Subscription-first media; FCF+, growing digital-sub base. Durable content annuity.',
    },
    "LPLA": {
        "pos":      "Mid",
        "cagr":     (9, 16),
        "strategy": "dca",
        "area":     'Independent-advisor platform (LPL Financial)',
        "note":     'Advisor-custody scaler; FCF+, cheap. Rate/market-cyclical.',
    },
    "YOU": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Identity-security SaaS (Clear Secure)',
        "note":     'Biometric-identity network; FCF+, high margin. margin_hist noisy — narrow moat/adoption risk.',
    },
    "BIRK": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Footwear brand (Birkenstock)',
        "note":     'Premium-sandal brand; high margin, FCF+, cheap post-IPO. Single-brand concentration.',
    },
    "STE": {
        "pos":      "Mid",
        "cagr":     (8, 14),
        "strategy": "dca",
        "area":     'Sterilization / medical (STERIS)',
        "note":     'Infection-prevention + surgical; FCF+, recurring. Durable healthcare-industrial.',
    },
    "QTWO": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Digital-banking SaaS (Q2 Holdings)',
        "note":     'Community-bank digital platform; recurring rev, FCF+, margins turning up. Early expander.',
    },
    "RELY": {
        "pos":      "Mid",
        "cagr":     (12, 22),
        "strategy": "dca",
        "area":     'Cross-border remittance (Remitly)',
        "note":     'Digital remittance scaler; FCF+, PEG 0.26 on trough — margin_hist negative, early profit inflection. CYCLE layer thin.',
    },
    "PCTY": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Payroll/HCM SaaS (Paylocity)',
        "note":     'Mid-market HCM; ~15% rev, FCF+, high margin. Durable compounder.',
    },
    "CARG": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Auto marketplace (CarGurus)',
        "note":     'US car-shopping platform; FCF+, cheap. Dealer-ad cyclicality.',
    },
    "CCI": {
        "pos":      "Mid",
        "cagr":     (5, 11),
        "strategy": "dca",
        "area":     'Cell-tower REIT (Crown Castle)',
        "note":     'US tower/fiber REIT; high margin, cheap after fiber-sale reset. Rate-sensitive; rev shrinking near-term.',
    },
    "GSHD": {
        "pos":      "Mid",
        "cagr":     (12, 22),
        "strategy": "dca",
        "area":     'Insurance brokerage (Goosehead)',
        "note":     'Franchise P&C brokerage; ~20% rev, FCF+, high margin. Growth-broker, richer multiple.',
    },
    "KNSL": {
        "pos":      "Mid",
        "cagr":     (12, 20),
        "strategy": "dca",
        "area":     'Specialty insurer (Kinsale Capital)',
        "note":     'E&S-insurance compounder; high ROE, FCF+, ~25% rev. Best-in-class underwriter.',
    },
    "DECK": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Footwear brands (Deckers)',
        "note":     'HOKA/UGG owner; FCF+, high margin, cheap after pullback. Brand-cyclical demand.',
    },
    "TYL": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Government SaaS (Tyler Technologies)',
        "note":     'Local-gov software near-monopoly; FCF+, recurring. Durable but richly valued.',
    },
    "BROS": {
        "pos":      "Early/Mid",
        "cagr":     (12, 22),
        "strategy": "dca",
        "area":     'Drive-thru coffee (Dutch Bros)',
        "note":     'Unit-growth coffee chain; FCF+, high-teens rev. Execution/expansion risk — richer VAL.',
    },
    "GRAB": {
        "pos":      "Early/Mid",
        "cagr":     (12, 25),
        "strategy": "dca",
        "area":     'SE-Asia super-app (Grab Holdings)',
        "note":     'Ride/delivery/fintech platform; ~20% rev, FCF turning +. margin_hist deeply negative history — early profit inflection, EM risk.',
    },
    "AMP": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Wealth/asset mgmt (Ameriprise)',
        "note":     'Advice + asset-mgmt; FCF+, cheap, buy-backs. Market/rate-cyclical.',
    },
    "GEN": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Consumer cyber (Gen Digital / Norton)',
        "note":     'Norton/Avast consumer security; high margin, FCF+, cheap. Slow-growth cash cow.',
    },
    "ALRM": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Smart-home SaaS (Alarm.com)',
        "note":     'Connected-property platform; recurring rev, FCF+. Steady niche compounder.',
    },
    "RYAN": {
        "pos":      "Mid",
        "cagr":     (12, 20),
        "strategy": "dca",
        "area":     'Insurance brokerage (Ryan Specialty)',
        "note":     'Wholesale-specialty broker; ~20% rev, FCF+. Growth-broker, richer VAL absorbed.',
    },
    "WING": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'QSR franchise (Wingstop)',
        "note":     'Asset-light wing franchise; high margin, FCF+, strong unit growth. Rich multiple.',
    },
    "EGHT": {
        "pos":      "Mid",
        "cagr":     (5, 14),
        "strategy": "dca",
        "area":     'UCaaS (8x8)',
        "note":     'Cloud-comms; FCF+ turnaround, cheap. margin_hist negative — deleveraging small-cap, execution risk. data 80%.',
    },
    "NEM": {
        "pos":      "Mid",
        "cagr":     (6, 16),
        "strategy": "cycle",
        "area":     'Gold miner (Newmont)',
        "note":     'Largest gold miner; F on gold windfall, margin_hist flips = commodity cycle. Buy dips, trim near peak.',
    },
    "MEDP": {
        "pos":      "Mid",
        "cagr":     (10, 18),
        "strategy": "dca",
        "area":     'Clinical-research CRO (Medpace)',
        "note":     'Full-service CRO; high margin, FCF+, ~15% rev. Biotech-funding-cyclical demand.',
    },
    "TT": {
        "pos":      "Mid",
        "cagr":     (8, 14),
        "strategy": "dca",
        "area":     'HVAC / climate (Trane Technologies)',
        "note":     'Datacenter/commercial HVAC; FCF+, secular cooling demand. Cyclical-industrial quality.',
    },
    "EVTC": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'LatAm payments (EVERTEC)',
        "note":     'Puerto-Rico/LatAm payment rails; high margin, FCF+, cheap. Geographic concentration.',
    },
    "TRV": {
        "pos":      "Mid",
        "cagr":     (5, 11),
        "strategy": "dca",
        "area":     'P&C insurer (Travelers)',
        "note":     'Large commercial/personal P&C; FCF+, cheap. Underwriting/rate-cyclical.',
    },
    "BOX": {
        "pos":      "Mid",
        "cagr":     (6, 13),
        "strategy": "dca",
        "area":     'Content-cloud SaaS (Box Inc.)',
        "note":     'Enterprise content platform; FCF+, cheap, margins up. Slow but profitable SaaS.',
    },
    "AZO": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Auto-parts retail (AutoZone)',
        "note":     'DIY/commercial parts; high ROIC, FCF+, buy-back machine. Defensive-cyclical retail.',
    },
    "PRI": {
        "pos":      "Mid",
        "cagr":     (8, 14),
        "strategy": "dca",
        "area":     'Life insurance / distribution (Primerica)',
        "note":     'Middle-market life + investments; FCF+, cheap. Recruiting-driven distribution.',
    },
    "DKS": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     "Sporting-goods retail (Dick's)",
        "note":     'Omnichannel sporting goods; FCF+, cheap, buy-backs. Discretionary-cyclical retail.',
    },
    "LNG": {
        "pos":      "Mid",
        "cagr":     (6, 16),
        "strategy": "cycle",
        "area":     'LNG export (Cheniere Energy)',
        "note":     'US LNG-export leader; FCF+, contracted cash flows. margin_hist flips with gas — cyclical. Buy dips.',
    },
    "JCI": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Building controls (Johnson Controls)',
        "note":     'Smart-building/HVAC controls; FCF+, datacenter tailwind. Cyclical-industrial.',
    },
    "TRIP": {
        "pos":      "Mid",
        "cagr":     (6, 14),
        "strategy": "dca",
        "area":     'Travel-reviews platform (Tripadvisor)',
        "note":     'Travel-media + Viator; FCF+, very cheap. Slow legacy, Viator growth optionality.',
    },
    "MCO": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     "Ratings / analytics (Moody's)",
        "note":     'Ratings duopoly + analytics; high margin, FCF+. Issuance-cyclical but wide moat.',
    },
    "VLO": {
        "pos":      "Mid",
        "cagr":     (4, 14),
        "strategy": "cycle",
        "area":     'Refining (Valero Energy)',
        "note":     'Largest independent refiner; FCF+, cheap — but PEG 0.4 rests on 283% trough-EPS rebound. Deep-cyclical refining. Buy troughs only.',
    },
    "GNRC": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "cycle",
        "area":     'Backup power / gensets (Generac)',
        "note":     'Home/commercial generators; FCF+, storm-demand cyclical. Energy-transition optionality.',
    },
    "RPD": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Cloud security (Rapid7)',
        "note":     'SIEM/vuln-mgmt; FCF+, very cheap. margin_hist flip = recent profit inflection; growth decelerating.',
    },
    "ZI": {
        "pos":      "Mid",
        "cagr":     (6, 14),
        "strategy": "dca",
        "area":     'B2B sales-intel SaaS (ZoomInfo)',
        "note":     'GTM data platform; FCF+, high margin, dirt-cheap. Rev stalled — cheap-for-a-reason risk. CYCLE thin.',
    },
    "WAT": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Lab instruments (Waters Corp)',
        "note":     'Chromatography/mass-spec; high margin, FCF+, recurring consumables. Capex-cyclical demand.',
    },
    "BR": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Fintech infra (Broadridge)',
        "note":     'Investor-comms + trade processing; FCF+, recurring. Durable back-office utility.',
    },
    "RL": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Luxury apparel (Ralph Lauren)',
        "note":     'Premium-brand turnaround; FCF+, cheap, brand-elevation working. Discretionary-cyclical.',
    },
    "RGA": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Life reinsurer (Reinsurance Group)',
        "note":     'Global life/health reinsurer; FCF+, very cheap. Mortality/rate-sensitive.',
    },
    "NVS": {
        "pos":      "Mid",
        "cagr":     (6, 11),
        "strategy": "dca",
        "area":     'Big pharma (Novartis)',
        "note":     'Diversified innovative pharma; high margin, FCF+, cheap. Patent-cliff/pipeline risk.',
    },
    "AMT": {
        "pos":      "Mid",
        "cagr":     (5, 11),
        "strategy": "dca",
        "area":     'Cell-tower REIT (American Tower)',
        "note":     'Global tower REIT; high margin, FCF+. Rate-sensitive; EM-tower exposure.',
    },
    "PSX": {
        "pos":      "Mid",
        "cagr":     (4, 13),
        "strategy": "cycle",
        "area":     'Refining / midstream (Phillips 66)',
        "note":     'Refining + midstream + chemicals; FCF+, cheap — PEG 0.24 on 226% trough-EPS. Deep-cyclical. Buy troughs.',
    },
    "JKHY": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Bank-tech (Jack Henry)',
        "note":     'Community-bank core processing; FCF+, recurring. Durable but slow.',
    },
    "BRO": {
        "pos":      "Mid",
        "cagr":     (8, 14),
        "strategy": "dca",
        "area":     'Insurance brokerage (Brown & Brown)',
        "note":     'Mid-market P&C broker; FCF+, ~15% organic. Serial-acquirer compounder, richer VAL.',
    },
    "BIO": {
        "pos":      "Mid",
        "cagr":     (5, 12),
        "strategy": "dca",
        "area":     'Life-science tools (Bio-Rad)',
        "note":     'Diagnostics + life-science instruments; FCF+, cheap. margin_hist volatile (Sartorius stake). data 80%.',
    },
    "FDS": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Financial-data SaaS (FactSet)',
        "note":     'Analytics/data terminal; high margin, FCF+, recurring. Bloomberg-lite compounder.',
    },
    "WMS": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Water-mgmt infra (Advanced Drainage)',
        "note":     'Stormwater/drainage systems; FCF+, infra tailwind. Construction-cyclical.',
    },
    "EW": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Structural-heart devices (Edwards Lifesciences)',
        "note":     'TAVR/heart-valve leader; high margin, FCF+, cheap after guide reset. Category-leader medtech.',
    },
    "VICI": {
        "pos":      "Mid",
        "cagr":     (6, 11),
        "strategy": "dca",
        "area":     'Gaming/experiential REIT (VICI Properties)',
        "note":     'Casino/experiential net-lease; 70% margin, FCF+, cheap. Rate-sensitive; tenant-concentrated.',
    },
    "O": {
        "pos":      "Mid",
        "cagr":     (5, 10),
        "strategy": "dca",
        "area":     'Net-lease REIT (Realty Income)',
        "note":     'Monthly-dividend net-lease; FCF+, cheap, durable. Rate-sensitive; VAL binds.',
    },
    "GIB": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'IT services (CGI Inc.)',
        "note":     'IT consulting roll-up; FCF+, cheap, steady margins. M&A-driven compounding.',
    },
    "PRGS": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Infra software (Progress Software)',
        "note":     'DevTools/infra roll-up; high margin, FCF+, cheap. Debt-funded M&A; low organic growth.',
    },
    "AFL": {
        "pos":      "Mid",
        "cagr":     (5, 10),
        "strategy": "dca",
        "area":     'Supplemental insurer (Aflac)',
        "note":     'Japan/US supplemental life+health; FCF+, cheap, buy-backs. Yen/rate-sensitive.',
    },
    "LOGI": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'PC/peripheral hardware (Logitech)',
        "note":     'Mice/keyboards/webcams; FCF+, cheap, net cash. Consumer-hardware cyclical.',
    },
    "DBX": {
        "pos":      "Mid",
        "cagr":     (4, 10),
        "strategy": "dca",
        "area":     'File-sync SaaS (Dropbox)',
        "note":     'Cloud-storage cash cow; FCF+, very cheap, buy-backs. Flat rev — value, not growth.',
    },
    "QLYS": {
        "pos":      "Mid",
        "cagr":     (8, 14),
        "strategy": "dca",
        "area":     'Cloud security (Qualys)',
        "note":     'Vuln-mgmt/compliance; high margin, FCF+, cheap. Slower growth than peers.',
    },
    "TENB": {
        "pos":      "Mid",
        "cagr":     (8, 15),
        "strategy": "dca",
        "area":     'Exposure-mgmt security (Tenable)',
        "note":     'Vuln/exposure platform; FCF+, cheap. margin_hist negative — recent profit inflection. CYCLE thin.',
    },
    "VICR": {
        "pos":      "Mid",
        "cagr":     (8, 18),
        "strategy": "cycle",
        "area":     'Power-conversion modules (Vicor)',
        "note":     'High-density power for AI/datacenter; ~26% rev rebound. Small-cap cyclical semi — lumpy, VAL binds.',
    },
    "LII": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'HVAC (Lennox International)',
        "note":     'Residential/commercial HVAC; FCF+, high ROIC. Housing/replacement-cyclical.',
    },
    "GL": {
        "pos":      "Mid",
        "cagr":     (5, 11),
        "strategy": "dca",
        "area":     'Life insurer (Globe Life)',
        "note":     'Middle-income life+health; FCF+, very cheap, buy-backs. Underwriting-sensitive.',
    },
    "CACI": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Defense IT (CACI International)',
        "note":     'Gov/defense-tech services; FCF+, cheap, backlog-driven. Budget-cyclical.',
    },
    "CB": {
        "pos":      "Mid",
        "cagr":     (5, 11),
        "strategy": "dca",
        "area":     'P&C insurer (Chubb)',
        "note":     'Global commercial P&C leader; FCF+, cheap. Best-in-class underwriter; rate-cyclical.',
    },
    "TWLO": {
        "pos":      "Mid",
        "cagr":     (8, 16),
        "strategy": "dca",
        "area":     'Comms API (Twilio)',
        "note":     'CPaaS messaging platform; FCF+ turnaround, cheap. margin_hist negative — early profit inflection.',
    },
    "CNC": {
        "pos":      "Mid",
        "cagr":     (5, 14),
        "strategy": "dca",
        "area":     'Managed care (Centene)',
        "note":     'Medicaid/ACA managed care; very cheap — PEG 0.36 on trough-EPS rebound. Policy/margin risk; TTM net negative.',
    },
    "LKQ": {
        "pos":      "Mid",
        "cagr":     (5, 11),
        "strategy": "dca",
        "area":     'Auto-parts distribution (LKQ Corp)',
        "note":     'Aftermarket/recycled parts; FCF+, dirt-cheap. Auto-repair-cyclical; data 80%.',
    },
    "EQT": {
        "pos":      "Mid",
        "cagr":     (5, 16),
        "strategy": "cycle",
        "area":     'Natural gas E&P (EQT Corp)',
        "note":     'Largest US gas producer; FCF+, integrated midstream. margin_hist flips with gas — cyclical. Buy dips.',
    },
    "CR": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Diversified industrial (Crane Co.)',
        "note":     'Aerospace/fluid-handling; FCF+, steady. Cyclical-industrial quality.',
    },
    "ORI": {
        "pos":      "Mid",
        "cagr":     (5, 10),
        "strategy": "dca",
        "area":     'Title/specialty insurer (Old Republic)',
        "note":     'Title + general insurance; FCF+, very cheap, buy-backs. Housing/underwriting-cyclical.',
    },
    "XYL": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Water infra (Xylem)',
        "note":     'Water pumps/treatment/metering; FCF+, secular water tailwind. Capex-cyclical.',
    },
    "IR": {
        "pos":      "Mid",
        "cagr":     (7, 13),
        "strategy": "dca",
        "area":     'Flow/industrial (Ingersoll Rand)',
        "note":     'Compressors/pumps/vacuum; FCF+, serial acquirer. Cyclical-industrial compounder.',
    },
    "DOV": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Diversified industrial (Dover Corp)',
        "note":     'Multi-industrial (pumps/refrigeration/marking); FCF+, steady. Cyclical-industrial.',
    },
    "ULTA": {
        "pos":      "Mid",
        "cagr":     (6, 12),
        "strategy": "dca",
        "area":     'Beauty retail (Ulta Beauty)',
        "note":     'Beauty-specialty retailer; FCF+, cheap, buy-backs. Discretionary-cyclical.',
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
