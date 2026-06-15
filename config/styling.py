# =========================================================================
# THEMATIC STYLING DICTIONARY
# Per-asset colors and line styles for chart rendering.
# Commenting out an asset in assets.py automatically disables it from
# the pipeline — its color entry here is simply ignored.
# =========================================================================

theme_styles = {
    # --- [NUC] NUCLEAR STOCK PICKING ---
    "[NUC] Cameco Corporation":              {"color": "#D4AF37", "linestyle": "-"},
    "[NUC] GE Vernova Inc.":                 {"color": "#B8860B", "linestyle": "--"},
    "[NUC] Sprott Physical Uranium":         {"color": "#FFD700", "linestyle": "-."},
    "[NUC] Centrus Energy Corp.":            {"color": "#CD7F32", "linestyle": ":"},
    "[NUC] NuScale Power":                   {"color": "#FF8C00", "linestyle": "-"},
    "[NUC] Oklo Inc.":                       {"color": "#E31B23", "linestyle": "--"},
    "[NUC] Applied Digital Corporation":     {"color": "#A0522D", "linestyle": "-."},  # NEW

    # --- [QTM] QUANTUM STOCK PICKING ---
    "[QTM] IonQ, Inc.":                      {"color": "#800080", "linestyle": "-"},
    "[QTM] D-Wave Quantum Inc.":             {"color": "#9370DB", "linestyle": "--"},
    "[QTM] Rigetti Computing, Inc.":         {"color": "#8A2BE2", "linestyle": "-."},
    "[QTM] Quantum Computing Inc.":          {"color": "#BA55D3", "linestyle": ":"},
    "[QTM] Xanadu Quantum Technologies":     {"color": "#DA70D6", "linestyle": "-"},
    "[QTM] Infleqtion":                      {"color": "#4B0082", "linestyle": "--"},
    "[QTM] Horizon Quantum Computing":       {"color": "#EE82EE", "linestyle": "-."},
    "[QTM] Quantinuum":                      {"color": "#46008B", "linestyle": ":"},

    # --- [CYBER] CYBERSECURITY ---
    "[CYBER] CrowdStrike Holdings, Inc.":    {"color": "#000000", "linestyle": "-"},
    "[CYBER] Palo Alto Networks, Inc.":      {"color": "#FF4500", "linestyle": "--"},

    # --- [CORE] CORE ETFs ---
    "[CORE] VanEck Semiconductor (40%)":     {"color": "#00008B", "linestyle": "-"},
    "[CORE] Invesco NASDAQ-100 (25%)":       {"color": "#4169E1", "linestyle": "--"},
    "[CORE] iShares S&P 500 Info Tech (22%)":{"color": "#00BFFF", "linestyle": "-."},
    "[CORE] Vanguard FTSE Dev World (13%)":  {"color": "#4682B4", "linestyle": ":"},

    # --- [AI] AI & ROBOTICS ETFs ---
    "[AI] ARK AI & Robotics":                {"color": "#800080", "linestyle": "-"},
    "[AI] Global X Robotics & AI":           {"color": "#9370DB", "linestyle": "--"},
    "[AI] Robo Global Robotics & Auto":      {"color": "#8A2BE2", "linestyle": "-."},
    "[AI] Xtrackers AI & Big Data":          {"color": "#BA55D3", "linestyle": ":"},
    "[AI] VanEck Quantum Computing":         {"color": "#DA70D6", "linestyle": "-"},

    # --- [TECH] MEGA CAP / STANDARD STOCKS ---
    "[TECH] NVIDIA Corporation":             {"color": "#76B900", "linestyle": "-"},
    "[TECH] Microsoft Corporation":          {"color": "#2F4F4F", "linestyle": "-"},
    "[TECH] Amazon.com, Inc.":               {"color": "#FF8C00", "linestyle": "-"},
    "[TECH] Apple Inc.":                     {"color": "#708090", "linestyle": "-"},
    "[TECH] Alphabet Inc.":                  {"color": "#4A5D6E", "linestyle": "--"},
    "[TECH] Oracle Corporation":             {"color": "#FF4500", "linestyle": "-"},
    "[TECH] ASML Holding N.V.":              {"color": "#008080", "linestyle": "-"},
    "[TECH] Tesla, Inc.":                    {"color": "#E31B23", "linestyle": "--"},
    "[TECH] Intel Corporation":              {"color": "#0071C5", "linestyle": "-."},
    "[TECH] Broadcom Inc.":                  {"color": "#CC0000", "linestyle": ":"},
    "[TECH] Advanced Micro Devices, Inc.":   {"color": "#ED1C24", "linestyle": "-"},
    "[TECH] Palantir Technologies Inc.":     {"color": "#3F4E4F", "linestyle": "--"},
    "[TECH] Marvell Technology, Inc.":       {"color": "#00A3E0", "linestyle": "-."},

    # --- OTHER SECTOR STOCKS ---
    "[FIN] Circle Internet Group":           {"color": "#A9A9A9", "linestyle": "-"},
    "[ENG] Chevron Corporation":             {"color": "#8B4513", "linestyle": "-"},
    "[ENG] Bloom Energy Corporation":        {"color": "#00FF00", "linestyle": "--"},
    "[HC] Roche Holding AG (CHF) (100%)":    {"color": "#006400", "linestyle": "-."},
    "[CORE] Roche Holding AG (CHF) (100%)":  {"color": "#006400", "linestyle": "-."},  # NEW: matches asset tag (was rendering black)

    # --- [IND] INDUSTRIALS & DEFENSE (NEW: backfilled — previously rendered black) ---
    "[IND] BWX Technologies, Inc.":          {"color": "#3F51B5", "linestyle": "-"},
    "[IND] Powell Industries, Inc.":         {"color": "#5C6BC0", "linestyle": "--"},
    "[IND] Vertiv Holdings Co":              {"color": "#1A237E", "linestyle": "-."},
    "[IND] Comfort Systems USA, Inc.":       {"color": "#7986CB", "linestyle": ":"},

    # --- [SPEC] SPECULATIVE GROWTH (NEW: backfilled — previously rendered black) ---
    "[SPEC] Rocket Lab USA, Inc.":           {"color": "#00ACC1", "linestyle": "-"},
    "[SPEC] Lattice Semiconductor Corp.":    {"color": "#00838F", "linestyle": "--"},
    "[SPEC] Credo Technology Group":         {"color": "#26C6DA", "linestyle": "-."},
    "[SPEC] Viking Therapeutics, Inc.":      {"color": "#006064", "linestyle": ":"},

    # --- [OTHER] CROSS-SECTOR DIVERSIFIERS (NEW) ---
    "[OTHER] TransMedics Group, Inc.":       {"color": "#2E7D32", "linestyle": "-"},   # MedTech — green
    "[OTHER] Axon Enterprise, Inc.":         {"color": "#455A64", "linestyle": "--"},  # Defense — slate
    "[OTHER] Enovix Corporation":            {"color": "#F9A825", "linestyle": "-."},  # Battery — amber
}

# =========================================================================
# HTML TAG COLORS (for report table row backgrounds)
# =========================================================================

HTML_TAG_COLORS = {
    "[CORE]":  "#EBF4FA",
    "[AI]":    "#F3E6F5",
    "[TECH]":  "#E3F2FD",
    "[FIN]":   "#ECEFF1",
    "[ENG]":   "#FFF3E0",
    "[HC]":    "#E8F5E9",
    "[NUC]":   "#FFF8DC",
    "[QTM]":   "#F8F8FF",
    "[CYBER]": "#FFEBEE",
    "[IND]":   "#E8EAF6",  # NEW: Industrials & Defense row background
    "[SPEC]":  "#E0F7FA",  # NEW: Speculative Growth row background
    "[OTHER]": "#F1F8E9",  # NEW: Cross-sector diversifiers row background
}


def get_row_bg_color(asset_name):
    """Return the HTML background color for a given asset name based on its tag."""
    for tag, color in HTML_TAG_COLORS.items():
        if tag in asset_name:
            return color
    return "#FFFFFF"
