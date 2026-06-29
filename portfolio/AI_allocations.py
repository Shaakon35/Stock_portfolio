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
    "W1_SILICON":   0.44,  # CHANGED: 0.43904 -> 0.44 (CONV-REBAL 2026-06). Hand-set book targets:
                           #          SMHV pinned 37.5% + BESI 3.5% + ADI 3.0% = 44.0% wave. Owner
                           #          conviction sizing (BESI trimmed off its outsized 4.27%, ADI
                           #          grown). Prior: 0.438 (SW-CUT). SMHV basket share = 0.375/0.44
                           #          = 0.85227 to keep the CHF windfall pinned at 37.5% book.
    "W2_POWER":     0.11,  # CHANGED: 0.12808 -> 0.11 (CONV-REBAL 2026-06). Hand-set book: TLN 3%
                           #          (highest CONV in wave) + GEV/HUBB/CCJ/ETN 2% each = 11.0%.
                           #          Prior: 0.126 (SW-CUT). PWR (AVOID G4.0) and OKLO (AVOID, 30%
                           #          data [GAP], F1.2 — a blind bet) CUT. Added TLN (Talen) —
                           #          PRIME cycle (G7.7/8PT5.07, V9.4): nuclear power contracted to
                           #          data centers, on-thesis for the power wave.
    "W3_DCINFRA":   0.1548,# CHANGED: 0.16016 -> 0.1548 (CONV-REBAL 2026-06). Hand-set CONV
                           #          gradient: CLS 2.5% (top CONV 7.27) down to ALAB 2.0% (low
                           #          CONV 5.52), linear in CONV between = 15.48%. Prior: 0.1428
                           #          (SW-CUT). CRDO TRIMMED from the book's #1 line (6.41%) to in-line
                           #          (~3.5%): it is MOMENTUM [PEAK?] — fake-cheap on peak earnings,
                           #          most $ in the highest mean-reversion risk. VRT trimmed (AVOID
                           #          G5.8). ANET grown (QUALITY 9.6, best all-round name). FN/COHR/
                           #          ALAB kept.
    "W4_CLOUD":     0.1349,# CHANGED: 0.10165 -> 0.1349 (CONV-REBAL 2026-06). Wave absorbs ALL the
                           #          book freed by trimming the rest to conviction targets — the
                           #          5 highest-CONV DCA names on the board live here. ~Equal slots
                           #          2.25% each (AMZN 2.24%, lowest CONV, shaved 0.01 to hit exactly
                           #          100.00). Prior: 0.10 (SW-CUT). Wave UNZEROED to a 10%
                           #          anchor sleeve — the scorer's highest-CONV DCA names (ORCL
                           #          8.73, META 8.50, MSFT 7.97, GOOGL 7.50, AMZN 7.15) plus NFLX
                           #          (streaming DCA, CONV 8.14) promoted from the watchlist as a
                           #          6th equal slot. Six ~1.667% book slots. Funded by a pro-rata
                           #          x0.84 trim of every other tradeable wave (SMHV held fixed at
                           #          37.5% book). Mega-cap cloud is the cheapest large-cap quality
                           #          on the board and the single best diversifier off the silicon-
                           #          heavy book the scorer points to.
    "W5_SOFTWARE":  0.0503,# CHANGED: 0.05153 -> 0.0503 (CONV-REBAL 2026-06). Hand-set: NOW 2.5%
                           #          + AXON 2.5% + the three 0.01% stubs (PANW/CRWD/PLTR) = 5.03%.
                           #          Prior: 0.0756 (SW-CUT). NOW is the wave anchor (QUALITY 8.2 /
                           #          RICHNESS 0.00, best-value DCA on the board); AXON the public-
                           #          safety SaaS monopoly (QUALITY 8.5). ZS/DDOG/S/SNOW remain at 0%.
    "W6_SPEC":      0.04,  # CHANGED: 0.04269 -> 0.04 (CONV-REBAL 2026-06). Hand-set: IONQ 2%
                           #          (top catalyst CONV) + TMDX 1% + SYM/RKLB 0.5% lottery stubs
                           #          = 4.0%. Prior: 0.042 (SW-CUT). The convex tail stays small.
                           #          RKLB (AVOID) and SYM (GAAP-unprofitable Binary) SHRUNK to 0.5%
                           #          lottery stubs; IONQ (PRIME catalyst 6.5/6.28) grown. TMDX
                           #          kept. The convex tail stays small.
    "W7_DIVERSIFY": 0.07,  # CHANGED: 0.07685 -> 0.07 (CONV-REBAL 2026-06). Hand-set: LLY 2.5% +
                           #          NU 2.5% + RDDT 2.0% = 7.0%. Prior: 0.0756 (SW-CUT)
                           #          diversifiers that break the book's single-factor AI-capex
                           #          bet. LLY (pharma, KEEP-DCA 9.2/0.19) + NU (fintech, PRIME
                           #          cycle 7.7/6.22, every layer >=8) + RDDT (NEW — social/AI
                           #          data-licensing, CONV 7.66, no layer <8). All uncorrelated to
                           #          AI capex — the biggest structural improvement for multi-year
                           #          compounding. The SIMO cut funded RDDT here. Kept in a
                           #          SEPARATE sleeve so the AI wave taxonomy (W1-W6) stays intact.
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
    "SMHV.SW":   0.8522727273,# CHANGED: 0.85414 -> 0.85227 (CONV-REBAL 2026-06) — the
                        # 90k CHF windfall (899 shares) held FIXED at exactly 37.5% of book
                        # (= 0.85616 of the 43.8% W1 wave; 0.438 * 0.85616 = 0.375). The W1 wave
                        # shrank again (BESI/ADI singles took the x0.84 W4-funding trim), so SMHV's
                        # basket share rose to keep its book pinned at 37.5%. NB: SMHV tracks a
                        # US-LISTED semi index, so it holds ZERO Samsung/SK Hynix — genuine new
                        # exposure, not a dup.
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
    "ONTO":      0.0000,# CHANGED: 0.0602 -> 0.00 — CUT (REBALANCE 2026-06). Scores AVOID
                        # (GROWTH 4.7, 8PT 4.30, binding CYC 4.5) and is REDUNDANT with BESI in
                        # the back-end complex (both inspect/measure adjacent steps). The book
                        # keeps the better, non-redundant leg (BESI, the bonding/assembly step,
                        # higher quality) and drops the duplicate metrology bet. 0% for easy
                        # re-add on a fresh trough. Its book funded the ANET/NOW growth.
    "BESI.AS":   0.0795454545,# CHANGED: 0.09724 -> 0.07955 (CONV-REBAL 2026-06) — TRIMMED to
                        # 3.5% book (0.44 * 0.07955 = 0.035), off its outsized 4.27% to a conviction-
                        # set target. Still the largest single non-SMHV name. The sharpest
                        # cyclical in the sleeve. Scores
                        # PRIME (GROWTH 9.6, 8PT 6.13, no weak layer: F8.4/V5.8/C8.4). The Early,
                        # NON-peak name in the back-end complex: advanced packaging (hybrid bonding
                        # for HBM4+/chiplets), western CoWoS pure-play, the assembly step (not
                        # inspection), highest quality (63% GM, 33% FCF margin). Ramp still AHEAD
                        # while DRAM is at its peak. EUR-listed. CYCLE / Early. ~5.0% of book.
    "ADI":       0.0681818182,# CHANGED: 0.04862 -> 0.06818 (CONV-REBAL 2026-06) — GROWN to
                        # 3.0% book (0.44 * 0.06818 = 0.03), a conviction-set target (the highest-
                        # QUALITY KEEP-DCA ballast in the sleeve). Analog Devices
                        # — analog/industrial silicon,
                        # the highest-QUALITY KEEP-DCA ballast in this otherwise cycle-heavy sleeve
                        # (scorer 8.3, 37% gross, 26% net, $3.9B FCF, PEG ~1.3). NB: despite the DCA
                        # tag it behaves cyclically (FY24 earnings halved, FY26 doubled), so a deep
                        # drop is a discount on a real franchise. Loosely AI-thesis (industrial/edge).
    "SIMO":      0.0000,# CHANGED: 0.04255 -> 0.00 — CUT (SIMO->RDDT ROTATION 2026-06). Silicon
                        # Motion — NAND/SSD controllers. Scores PRIME on raw GROWTH (8.0) but
                        # carries the [PEAK?] flag and the WEAKEST risk-adjusted profile of the
                        # held cyclicals: CONV 5.28, V 4.9 / C 4.6 — a low PEG that is fake-cheap
                        # on peak memory-cycle earnings (the SK-Hynix/Micron trap). Rotated into
                        # RDDT (W7, CONV 7.66, every layer >=8, a non-semi AI diversifier) — a
                        # strict risk-adjusted upgrade AND better book diversification. 0% for
                        # easy re-add on a fresh NAND trough. CYCLE / Early-Mid.
    "000660.KS": 0.0000,# CHANGED: 0.0295 -> 0.00 — TRIMMED. SK Hynix rode the DRAM/HBM cycle
                        # to a record peak (+~900% / 52wk, MU memory GM ~74% = all-time high):
                        # graded Mid/Late, the cycle-trap zone where a 6-7x fwd P/E is the
                        # WARNING (peak earnings about to mean-revert), not the bargain. Book
                        # redeployed to BESI.AS (Early, ramp ahead). 0% for easy re-add on the
                        # first DRAM down-quarter / margin roll. CYCLE / Mid-Late.
    "CDNS":      0.0000,# CHANGED: 0.0295 -> 0.00 — REMOVED (owner decision, 2026-06). Thesis
                        # was the EDA design-tool duopoly (w/ Synopsys), chip-DESIGN layer not
                        # in SMHV. Cut on VALUATION/momentum: rich entry (45x fwd P/E, PEG
                        # 3.16, 18x P/S) against ~13% revenue growth, and EPS growth had
                        # stalled (FY24 +0.8% / FY25 +5.5%) on margin compression (op margin
                        # 30.6% -> 28.2%). Revenue itself never stalled — this is a price/
                        # multiple call, not a quality call. Book redeployed to BESI.AS. The
                        # design-layer gap is now UNCOVERED in the book; SNPS remains on the
                        # watchlist as the re-add route. 0% for easy re-add on a de-rating.
    "SMHN.DE":   0.0000,# CHANGED: 0.0295 -> 0.00 — CUT (REBALANCE 2026-06). SUSS MicroTec —
                        # advanced-packaging/bonding equipment, the SAME HBM4/CoWoS bottleneck as
                        # BESI.AS, so it was a DUPLICATE leg. Scores AVOID (GROWTH 3.4). The book
                        # keeps BESI (the higher-quality bonding name) and drops the redundant
                        # one. Frankfurt-listed (EUR). 0% for easy re-add.
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
    "GEV":     0.1818181818,# CHANGED: 0.26667 -> 0.18182 (CONV-REBAL 2026-06) — set to 2.0% book
                      # (0.11 * 0.18182 = 0.02). grid/gas turbines, HOLD FOREVER (Late but DCA —
                      # keep). KEEP-DCA 7.8.
    "CCJ":     0.1818181818,# CHANGED: 0.23333 -> 0.18182 (CONV-REBAL 2026-06) — set to 2.0% book.
                      # uranium leader, HOLD FOREVER. KEEP-DCA 7.3.
    "CEG":     0.0000,# CHANGED: 0.12 -> 0.00 — TRIMMED: below 200d / death cross (tech sell
                      # signal overrides thesis, pt 8). Kept at 0% for easy re-add.
    "ETN":     0.1818181818,# CHANGED: 0.17333 -> 0.18182 (CONV-REBAL 2026-06) — set to 2.0% book.
                      # transmission/electrification, DCA. KEEP-DCA 6.3.
    "HUBB":    0.1818181818,# CHANGED: 0.16 -> 0.18182 (CONV-REBAL 2026-06) — set to 2.0% book.
                      # transformers / grid gear — 2-4yr lead-times, early-cycle, DCA.
    "TLN":     0.2727272727,# CHANGED: 0.16667 -> 0.27273 (CONV-REBAL 2026-06) — grown to 3.0%
                      # book (0.11 * 0.27273 = 0.03), the wave's top-CONV name (7.11). Talen Energy
                      # — nuclear generation CONTRACTED to data centers. Scores PRIME cycle (GROWTH
                      # 7.7, 8PT 5.07, V 9.4 — cheap + clean). On-thesis for the power wave: it
                      # monetizes the DC power-demand bottleneck directly. CYCLE — power-price/deal
                      # sensitive, buy dips / trim peaks.
    "PWR":     0.0000,# CHANGED: 0.1298 -> 0.00 — CUT (REBALANCE 2026-06). Quanta — transmission
                      # contractor. Scores AVOID (GROWTH 4.0): the slowest-growth cyclical in the
                      # wave. Book rotated to TLN (PRIME, on-thesis) + the GEV/CCJ growth. 0% for
                      # easy re-add. CYCLE.
    "OKLO":    0.0000,# CHANGED: 0.1039 -> 0.00 — CUT (REBALANCE 2026-06). Pre-revenue SMR.
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
    "VRT":   0.146640826873,# CHANGED: 0.07997 -> 0.14664 (CONV-REBAL 2026-06) — GROWN to 2.27%
                    # book on the CONV gradient (CONV 6.46). Scores AVOID (GROWTH 5.8) but keeps a
                    # strong F=8.0, so trimmed not cut. Liquid cooling leader — CYCLE.
    "ANET":  0.157622739018,# CHANGED: 0.23991 -> 0.15762 (CONV-REBAL 2026-06) — TRIMMED to 2.44%
                    # book on the CONV gradient (CONV 7.06). Still the best business in the wave
                    # (QUALITY 9.6) but its DCA-CONV is mid-pack here, so sized to the gradient.
                    # Arista — DC networking monopoly. 38% margin, $4.4B FCF, software moat. DCA.
    "CRDO":  0.129844961240,# CHANGED: 0.18660 -> 0.12984 (CONV-REBAL 2026-06) — TRIMMED to 2.01%
                    # book on the CONV gradient (CONV 5.54, near the bottom). It scores MOMENTUM with the
                    # [PEAK?] flag: low PEG is FAKE-CHEAP on peak earnings + an extended chart —
                    # the SK-Hynix/Micron trap. Having the MOST money in the highest mean-
                    # reversion risk was backwards; the gain is banked into ANET/NOW. Still a
                    # real hypergrowth business — trim, don't cut. CYCLE — sell when growth <30%.
    "COHR":  0.132428940568,# CHANGED: 0.10663 -> 0.13243 (CONV-REBAL 2026-06) — set to 2.05%
                    # book on the CONV gradient (CONV 5.68).
                    # Coherent — optical; already ran, cyclical. MOMENTUM. CYCLE.
    "FN":    0.142764857881,# CHANGED: 0.21326 -> 0.14276 (CONV-REBAL 2026-06) — TRIMMED to 2.21%
                    # book on the CONV gradient (CONV 6.27).
                    # Fabrinet — optical contract mfr; cleanest growth-at-reasonable-price name
                    # (QUALITY quadrant, 8PT 5.11, net cash). CYCLE / Mid.
    "ALAB":  0.129198966408,# CHANGED: 0.07997 -> 0.12920 (CONV-REBAL 2026-06) — set to 2.00% book,
                    # the gradient FLOOR (lowest CONV 5.52 in the wave). Mid/Late,
                    # 118x fwd P/E, analysts -36%: most stretched name held, fails 8-Point #6
                    # (priced for perfection). Book rotated to ZS (W5). Astera Labs —
                    # AI connectivity pure-play (CXL/PCIe retimers),
                    # highest-beta name in the sleeve. CYCLE / Mid — bottleneck is young
                    # but the stock already ran +500%/2y, so remaining runway = Mid.
                    # CHANGED 2026-06: S (SentinelOne) MOVED OUT to W5 (it's a software/cyber
                    # name). Growth-max pass: SNOW + COHR trim folded into CRDO; 6 names
                    # renormalized to sum to 1.0.
    "CLS":   0.161498708010,# CHANGED: 0.09366 -> 0.16150 (CONV-REBAL 2026-06) — GROWN to 2.50%
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
    "MSFT":  0.1667902150,# Azure + OpenAI. Cloud anchor, every layer >=5.9. CONV 7.97. 2.25% book. dca.
    "GOOG":  0.1667902150,# Gemini + TPU + Cloud. Search/cloud/AI. CONV 7.50. 2.25% book. dca.
                    # Class C (non-voting) — swapped from GOOGL 2026-06: same business, cheaper share.
    "AMZN":  0.1660489251,# AWS + retail. CONV 7.15 (lowest in wave). 2.24% book — shaved 0.01 off
                    # the equal 2.25% so the whole book hits exactly 100.00. dca.
    "META":  0.1667902150,# Open models + ad-AI. V 10.0 (dead cheap). CONV 8.50. 2.25% book. dca.
    "ORCL":  0.1667902150,# Cloud-capacity winner. #1 DCA on the board — V 10.0. CONV 8.73. 2.25% book. dca.
    "NFLX":  0.1667902150,# Streaming (Netflix) — scale + ad-tier + password monetization, FCF
                    # inflecting up. Quality DCA at a premium multiple, CONV 8.14. The off-thesis
                    # consumer-internet leg of the sleeve. 2.25% book. dca.
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
    "S":     0.0000,# CUT. Only GAAP-UNPROFITABLE top-10 name (net income -$319M TTM,
                    # never had a profitable year); FCF-positive but turnaround unproven.
                    # Kept at 0% for easy re-add if the GAAP turn completes.
    "PANW":  0.0019880716,# CHANGED: 0.00194 -> 0.00199 (CONV-REBAL 2026-06) — held at the 0.01%-
                    # book stub (basket share moved only because the wave shrank). Security platform
                    # — biggest, cheapest, steadiest, but scores RICH (RICHNESS 0.90, CONV 3.02 —
                    # lowest DCA on the board): price too extended to keep real book. Easy re-add
                    # once it de-rates. DCA.
    "CRWD":  0.0019880716,# CHANGED: 0.00194 -> 0.00199 (CONV-REBAL 2026-06) — held at the 0.01%-
                    # book stub. AI cybersecurity. Scores RICH (RICHNESS 0.81, CONV 3.72) — same
                    # logic as PANW, too extended to keep real book. Easy re-add once it de-rates. DCA.
    "NOW":   0.4970178926,# CHANGED: 0.66279 -> 0.49702 (CONV-REBAL 2026-06) — set to 2.50% book
                    # (0.0503 * 0.49702 = 0.025), co-anchor with AXON. The best-value DCA name on
                    # the board: QUALITY 8.2 with RICHNESS 0.00 (cheapest possible on the gate),
                    # 22x fwd / 0.89 PEG, down ~50% on the year. Workflow AI (Now Assist),
                    # profitable. KEEP-DCA.
    "ZS":    0.0000,# CHANGED: 0.1782 -> 0.00 — CUT (REBALANCE 2026-06). Zscaler scores AVOID
                    # (GROWTH 2.0) — the weakest software name held. Book rotated to NOW/AXON.
                    # 0% for easy re-add if the growth re-accelerates. CYCLE.
    "AXON":  0.4970178926,# CHANGED: 0.33139 -> 0.49702 (CONV-REBAL 2026-06) — GROWN to 2.50%
                    # book, co-anchor with NOW. Public-safety
                    # SaaS monopoly — 59% gross margin, sticky recurring revenue (evidence.com,
                    # Draft One AI), end-market that doesn't cycle. QUALITY 8.5, KEEP-DCA. Thin
                    # net/FCF is reinvestment by choice; hold through dips.
    "PLTR":  0.0019880716,# CHANGED: 0.00194 -> 0.00199 (CONV-REBAL 2026-06) — held at the 0.01%-
                    # book tracking stub. The HIGHEST-CONVICTION cycle name on the
                    # whole board (CONV 8.25, PRIME, F 10.0 / V 8.1 / C 6.4) — the business scores
                    # elite — but kept at a token 0.01% NOT on quality, on POSITION RISK the scorer
                    # can't see: US-gov customer concentration (declining but still the larger
                    # base), Europe/France data-sovereignty pushback capping the international TAM,
                    # and a priced-for-perfection multiple (~60x+ sales) where a single lumpy gov
                    # quarter de-rates it. Grow into a SMALL starter (~1.5% book) bought on
                    # weakness, never chased. CYCLE — trim/add, not blind DCA.
    "SNOW":  0.0000,# CHANGED: 0.1904 -> 0.00 — MOVED to CRDO (W3) on growth-max pass.
                    # Healed bubble hangover but slowest forecast of the survivors.
    "DDOG":  0.0000,# CHANGED: 0.1602 -> 0.00 — CUT (REBALANCE 2026-06). AI observability.
                    # Scores AVOID (GROWTH 3.7) — weakest of the observability/sw cluster. Book
                    # rotated to NOW/AXON. 0% for easy re-add. CYCLE.
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
    "TMDX":  0.25,    # CHANGED: 0.50 -> 0.25 (CONV-REBAL 2026-06) — set to 1.0% book (0.04 * 0.25).
                      # MedTech organ-transport, profitable, off-radar, non-AI diversifier. QUALITY
                      # quadrant (8PT 5.34). TOP-10 name.
    # --- AXON MOVED 2026-06 to W5 (AI Software/Apps), kept dca. It is a profitable
    #     monopoly, not a speculative punt; it never fit the convex-tail sleeve. ---
    "IONQ":  0.5,     # CHANGED: 0.30 -> 0.50 (CONV-REBAL 2026-06) — GROWN to 2.0% book (0.04 * 0.5),
                      # the wave anchor and best-graded punt you own: PRIME catalyst (GROWTH 6.5,
                      # 8PT 6.28, C 8.5). Quantum revenue leader; +175% mid (highest forecast).
                      # Catalyst/convex.
    "RKLB":  0.125,   # CHANGED: 0.10 -> 0.125 (CONV-REBAL 2026-06) — 0.5% book lottery
                      # stub. Scores AVOID (GROWTH 4.6); kept tiny as an asymmetric space punt,
                      # not grown. Space/autonomy. Catalyst — size once, no avg down.
    "SYM":   0.125,   # CHANGED: 0.10 -> 0.125 (CONV-REBAL 2026-06) — 0.5% book lottery
                      # stub. Symbotic — warehouse/logistics robotics (physical-AI). QUALITY
                      # quadrant but GAAP-unprofitable (net -$28M TTM, fails Pt 2) + lumpy/
                      # customer-concentrated (Walmart), so it stays a tiny convex-tail bet.
                      # CATALYST / Binary — size tiny, never average down.
    "CRCL":  0.0000,  # Circle (USDC) — held windfall (147 shares), TARGET 0%. Parked to
                      # track/manage down, NOT to add to. Catalyst.
    "LEU":   0.0000,  # Centrus Energy — HALEU/uranium enrichment for advanced reactors
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
    "LLY":   0.3571428571,# CHANGED: 0.44444 -> 0.35714 (CONV-REBAL 2026-06) — set to 2.5% book
                      # (0.07 * 0.35714 = 0.025). Eli Lilly — pharma compounder, fully
                      # uncorrelated to AI capex. KEEP-DCA. Watch: orforglipron Phase 3 + mfg build.
    "NU":    0.3571428571,# CHANGED: 0.33333 -> 0.35714 (CONV-REBAL 2026-06) — set to 2.5% book
                      # (0.07 * 0.35714 = 0.025). Nubank — LatAm digital bank. PRIME cycle, every
                      # layer strong. EM-consumer/credit cyclical — buy dips, trim manias.
    "RDDT":  0.2857142857,# CHANGED: 0.22222 -> 0.28571 (CONV-REBAL 2026-06) — 2.0% book (0.07 * 0.28571 = 0.02).
                      # Reddit — social ads + AI data-licensing (selling 20y of human conversation
                      # to LLM labs). Scores CONV 7.66 (3rd-highest cycle name on the board) with
                      # NO binding layer below 8.0 (F8.2/V10.0/C8.0): cheap, not extended, good
                      # business — a rare triple. Funded by the SIMO cut. A non-semi AI-economy
                      # play that diversifies the silicon-heavy book. CYCLE / Early — high-beta,
                      # young public co; buy dips, trim manias.
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
    "PLTR":    "cycle",     # Best business but 62x sales — trim/add, not blind DCA
    "DDOG":    "cycle",     # Consumption model — buy dips, trim momentum spikes

    # --- W6 SPECULATIVE ---
    "TMDX":    "cycle",     # MedTech growth — momentum-sensitive
    "IONQ":    "catalyst",  # Quantum binary — size once, event-driven, no avg down
    "RKLB":    "catalyst",  # Space — size once, milestone-driven, no avg down
    "SYM":     "catalyst",  # Symbotic — robotics, GAAP-unprofitable + lumpy; size once, no avg down
    "CRCL":    "catalyst",  # Circle — held windfall, target 0%; manage down, never avg in
    "LEU":     "catalyst",  # Centrus — HALEU enrichment, policy/contract-driven; watch-only 0%

    # --- W7 DIVERSIFIERS (off the AI value chain) ---
    "LLY":     "dca",       # Eli Lilly — pharma compounder (tirzepatide/orforglipron), hold forever; uncorrelated to AI capex
    "NU":      "cycle",     # Nubank — LatAm digital bank; EM-consumer/credit cyclical, buy dips / trim manias
    "RDDT":    "cycle",     # Reddit — social ads + AI data-licensing; non-semi AI diversifier, Early/high-beta, buy dips / trim manias
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
    "APP": {
        "strategy": "cycle",
        "pos":      "Mid",
        "cagr":     (18, 35),
        "area":     "Mobile ad-tech / AI engine (AppLovin)",
        "note":     "AXON AI ad engine drove a huge re-rate. High momentum + high beta "
                    "— cyclical, trim into strength.",
    },
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
