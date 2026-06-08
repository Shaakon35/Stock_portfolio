import pandas as pd
import matplotlib.pyplot as plt

from portfolio.allocations import (
    TARGET_WEIGHTS, MONTHLY_DEPOSIT, SELL_TRIGGER_CEILING,
    NUCLEAR_BASKET_TARGETS, QUANTUM_BASKET_TARGETS, CYBER_BASKET_TARGETS,
    INDUSTRIAL_BASKET_TARGETS, SPECGROWTH_BASKET_TARGETS,
    ETF_LOOK_THROUGH, my_current_shares,
)
from portfolio.helpers import is_in_uptrend, get_price


# =========================================================================
# PORTFOLIO AUDIT
# =========================================================================

def run_audit():
    """Fetch prices, compute drift, and print the portfolio audit."""
    print("🔄 Fetching market data...")

    category_labels = ["NUCLEAR_SATELLITE", "QUANTUM_SATELLITE", "CYBER_SATELLITE",
                       "INDUSTRIAL_SATELLITE", "SPECGROWTH_SATELLITE"]
    all_assets = set(
        list(TARGET_WEIGHTS.keys())
        + list(NUCLEAR_BASKET_TARGETS.keys())
        + list(QUANTUM_BASKET_TARGETS.keys())
        + list(CYBER_BASKET_TARGETS.keys())
        + list(INDUSTRIAL_BASKET_TARGETS.keys())
        + list(SPECGROWTH_BASKET_TARGETS.keys())
    )
    actual_tickers = [t for t in all_assets if t not in category_labels]

    prices = {t: get_price(t) for t in actual_tickers}

    portfolio_values = {
        asset: shares * prices.get(asset, 10.0)
        for asset, shares in my_current_shares.items()
    }
    nuclear_val = sum(portfolio_values.get(s, 0.0) for s in NUCLEAR_BASKET_TARGETS)
    quantum_val = sum(portfolio_values.get(s, 0.0) for s in QUANTUM_BASKET_TARGETS)
    cyber_val = sum(portfolio_values.get(s, 0.0) for s in CYBER_BASKET_TARGETS)
    industrial_val = sum(portfolio_values.get(s, 0.0) for s in INDUSTRIAL_BASKET_TARGETS)
    specgrowth_val = sum(portfolio_values.get(s, 0.0) for s in SPECGROWTH_BASKET_TARGETS)

    macro_values = {
        "XAIX.DE": portfolio_values.get("XAIX.DE", 0),
        "SMH": portfolio_values.get("SMH", 0),
        "IUIT.L": portfolio_values.get("IUIT.L", 0),
        "NUCLEAR_SATELLITE": nuclear_val,
        "QUANTUM_SATELLITE": quantum_val,
        "CYBER_SATELLITE": cyber_val,
        "INDUSTRIAL_SATELLITE": industrial_val,
        "SPECGROWTH_SATELLITE": specgrowth_val,
    }
    total_val = sum(macro_values.values())

    # --- Drift report ---
    print("\n📊 PORTFOLIO AUDIT")
    print(f"{'Asset':<20} | {'Current %':<10} | {'Target %':<10} | {'Drift':<10}")
    print("-" * 55)

    for asset, target_pct in TARGET_WEIGHTS.items():
        current_val = macro_values.get(asset, 0)
        current_pct = (current_val / total_val) * 100 if total_val > 0 else 0
        drift = current_pct - (target_pct * 100)
        print(f"{asset:<20} | {current_pct:>8.1f}% | {target_pct*100:>8.1f}% | {drift:>+8.1f}")

    print("=" * 55)

    # --- Sell / Buy engine ---
    print(f"\n📊 Total Value: €{total_val:.2f}")
    active_sales = False
    sell_orders = []

    for asset, val in macro_values.items():
        current_pct = val / total_val
        proxy_map = {
            "SMH": "SMH", "XAIX.DE": "SMH",
            "NUCLEAR_SATELLITE": list(NUCLEAR_BASKET_TARGETS.keys())[0],
            "INDUSTRIAL_SATELLITE": list(INDUSTRIAL_BASKET_TARGETS.keys())[0],
            "SPECGROWTH_SATELLITE": list(SPECGROWTH_BASKET_TARGETS.keys())[0],
        }
        proxy = proxy_map.get(asset, "CRWD")
        if is_in_uptrend(proxy):
            continue

        if asset in SELL_TRIGGER_CEILING and current_pct >= SELL_TRIGGER_CEILING[asset]:
            active_sales = True
            excess = val - (total_val * TARGET_WEIGHTS[asset])
            basket = {
                "NUCLEAR": NUCLEAR_BASKET_TARGETS,
                "QUANTUM": QUANTUM_BASKET_TARGETS,
                "CYBER": CYBER_BASKET_TARGETS,
                "INDUSTRIAL": INDUSTRIAL_BASKET_TARGETS,
                "SPECGROWTH": SPECGROWTH_BASKET_TARGETS,
            }
            for key in basket:
                if key in asset:
                    over_extended = max(
                        basket[key],
                        key=lambda s: (portfolio_values.get(s, 0) / val) - basket[key][s],
                    )
                    sell_orders.append(f"[SELL] {over_extended} (Excess: €{excess:.2f})")

    if active_sales:
        print(f"💰 PROFIT TAKING: {', '.join(sell_orders)}")

    chosen_buy = max(
        TARGET_WEIGHTS,
        key=lambda a: TARGET_WEIGHTS[a] - (macro_values.get(a, 0) / total_val),
    )
    print(f"📢 ACTION: Invest €{MONTHLY_DEPOSIT} into {chosen_buy}")

    return macro_values, portfolio_values, total_val


# =========================================================================
# EXPOSURE MATRIX (ETF look-through)
# =========================================================================

def build_exposure_matrix():
    """Build and display the underlying stock exposure matrix."""
    exposure_ledger = []

    for etf, micro_allocations in ETF_LOOK_THROUGH.items():
        macro_weight = TARGET_WEIGHTS[etf]
        for stock, sub_weight in micro_allocations.items():
            exposure_ledger.append({
                "Stock/Asset": stock,
                "Net Weight": macro_weight * sub_weight,
                "Source Component": etf,
            })

    for stock, sub_weight in NUCLEAR_BASKET_TARGETS.items():
        exposure_ledger.append({
            "Stock/Asset": stock,
            "Net Weight": TARGET_WEIGHTS["NUCLEAR_SATELLITE"] * sub_weight,
            "Source Component": "NUCLEAR",
        })

    for stock, sub_weight in QUANTUM_BASKET_TARGETS.items():
        exposure_ledger.append({
            "Stock/Asset": stock,
            "Net Weight": TARGET_WEIGHTS["QUANTUM_SATELLITE"] * sub_weight,
            "Source Component": "QUANTUM",
        })

    for stock, sub_weight in CYBER_BASKET_TARGETS.items():
        exposure_ledger.append({
            "Stock/Asset": stock,
            "Net Weight": TARGET_WEIGHTS["CYBER_SATELLITE"] * sub_weight,
            "Source Component": "CYBER",
        })

    for stock, sub_weight in INDUSTRIAL_BASKET_TARGETS.items():
        exposure_ledger.append({
            "Stock/Asset": stock,
            "Net Weight": TARGET_WEIGHTS["INDUSTRIAL_SATELLITE"] * sub_weight,
            "Source Component": "INDUSTRIAL",
        })

    for stock, sub_weight in SPECGROWTH_BASKET_TARGETS.items():
        exposure_ledger.append({
            "Stock/Asset": stock,
            "Net Weight": TARGET_WEIGHTS["SPECGROWTH_SATELLITE"] * sub_weight,
            "Source Component": "SPECGROWTH",
        })

    df = pd.DataFrame(exposure_ledger)
    summary_df = df.groupby("Stock/Asset").agg({
        "Net Weight": "sum",
        "Source Component": lambda x: list(set(x)),
    }).reset_index()
    summary_df = summary_df.sort_values(by="Net Weight", ascending=False).reset_index(drop=True)

    # --- Render matplotlib table ---
    HEX_COLORS = {
        "SMH":        "#E6F0FA",
        "IUIT.L":     "#E6F7F9",
        "XAIX.DE":    "#E6F4EA",
        "NUCLEAR":    "#FCF7E6",
        "QUANTUM":    "#FAE6FA",
        "CYBER":      "#FCE8E6",
        "INDUSTRIAL": "#E8EAF6",
        "SPECGROWTH": "#E0F7FA",
    }
    HEX_MULTI = "#F3E6FA"

    SOURCE_LABELS = {
        "SMH":        "Core Semiconductors (SMH)",
        "IUIT.L":     "S&P 500 Info Tech (IUIT.L)",
        "XAIX.DE":    "AI & Big Data Index (XAIX.DE)",
        "NUCLEAR":    "Satellite Layer (NUCLEAR)",
        "QUANTUM":    "Satellite Layer (QUANTUM)",
        "CYBER":      "Satellite Layer (CYBER)",
        "INDUSTRIAL": "Satellite Layer (INDUSTRIAL)",
        "SPECGROWTH": "Satellite Layer (SPECGROWTH)",
    }

    table_data = []
    row_colors = []

    for _, row in summary_df.iterrows():
        sources = row["Source Component"]
        weight_str = f"{row['Net Weight'] * 100:.2f}%"

        if len(sources) > 1:
            source_label = f"Cross-ETF Overlap ({', '.join(sorted(sources))})"
            cell_color = HEX_MULTI
        else:
            src = sources[0]
            source_label = SOURCE_LABELS.get(src, src)
            cell_color = HEX_COLORS.get(src, "#FFFFFF")

        table_data.append([row["Stock/Asset"], weight_str, source_label])
        row_colors.append([cell_color] * 3)

    fig, ax_table = plt.subplots(figsize=(12, len(summary_df) * 0.35 + 1))
    ax_table.axis('off')

    columns = ["Underlying Stock / Asset", "Net Portfolio Weight (%)", "Primary Asset Origin Component"]
    display_table = ax_table.table(
        cellText=table_data, colLabels=columns, loc='center',
        cellLoc='left', colWidths=[0.25, 0.20, 0.55], cellColours=row_colors,
    )

    for j in range(len(columns)):
        cell = display_table[0, j]
        cell.set_facecolor('#2C3E50')
        cell.get_text().set_color('white')
        cell.get_text().set_weight('bold')
        cell.set_height(0.04)

    display_table.auto_set_font_size(False)
    display_table.set_fontsize(10)
    display_table.scale(1.25, 1.45)
    plt.show()

    return summary_df
