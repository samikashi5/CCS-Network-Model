import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALLOC = ROOT / "allocation_results.csv"
SUMM  = ROOT / "summary_results.csv"
OUT   = ROOT / "figures"
OUT.mkdir(exist_ok=True)

alloc = pd.read_csv(ALLOC)
summ  = pd.read_csv(SUMM)

pipeline_cost = float(summ["pipeline_unit_cost_usd_per_ton_km"].iloc[0])
storage_cost  = float(summ["storage_cost_usd_per_ton"].iloc[0])

# derive per-source cost breakdown
alloc["transport_cost"] = alloc["flow_total_tons"] * pipeline_cost * alloc["L_km"]
alloc["storage_cost_usd"] = alloc["flow_total_tons"] * storage_cost

# short labels
alloc["label"] = alloc["source"].str.replace("Plant_", "").str.replace("_", " ")

colors = {
    "transport": "#2E86AB",
    "storage":   "#E84855",
    "flow":      "#3BB273",
}

# ── fig 1: CO2 flow by source ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(alloc["label"], alloc["flow_total_tons"] / 1e3,
              color=colors["flow"], edgecolor="white", linewidth=0.6)
ax.set_ylabel("CO₂ Flow (kt/yr)")
ax.set_title("Annual CO₂ Flow by Source")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
for bar, val in zip(bars, alloc["flow_total_tons"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
            f"{val/1e3:,.0f}", ha="center", va="bottom", fontsize=8.5)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
fig.savefig(OUT / "fig1_flow_by_source.png", dpi=150)
plt.close()
print("saved fig1")

# ── fig 2: stacked cost breakdown per source ──────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(alloc["label"], alloc["transport_cost"] / 1e6,
       label="Transport (pipeline)", color=colors["transport"], edgecolor="white")
ax.bar(alloc["label"], alloc["storage_cost_usd"] / 1e6,
       bottom=alloc["transport_cost"] / 1e6,
       label="Storage", color=colors["storage"], edgecolor="white")
ax.set_ylabel("Annual Cost (M USD/yr)")
ax.set_title("Annual Cost Breakdown by Source")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.1f}M"))
ax.legend(frameon=False, fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
fig.savefig(OUT / "fig2_cost_breakdown.png", dpi=150)
plt.close()
print("saved fig2")

# ── fig 3: transport cost per ton vs distance ─────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4))
cost_per_ton = alloc["transport_cost"] / alloc["flow_total_tons"]
sc = ax.scatter(alloc["L_km"], cost_per_ton, s=alloc["flow_total_tons"] / 3000,
                color=colors["transport"], edgecolors="white", linewidth=0.7, zorder=3)
for _, row in alloc.iterrows():
    ax.annotate(row["label"],
                (row["L_km"], row["transport_cost"] / row["flow_total_tons"]),
                textcoords="offset points", xytext=(6, 2), fontsize=8)
ax.set_xlabel("Pipeline Distance (km)")
ax.set_ylabel("Transport Cost (USD/tCO₂)")
ax.set_title("Transport Cost per Ton vs. Distance\n(bubble size = annual flow volume)")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
fig.savefig(OUT / "fig3_cost_vs_distance.png", dpi=150)
plt.close()
print("saved fig3")

# ── summary print ─────────────────────────────────────────────────────────────
total_cost = float(summ["objective_total_cost_usd_per_year"].iloc[0])
total_flow = float(summ["total_flow_tons_per_year"].iloc[0])
transport_total = alloc["transport_cost"].sum()
storage_total   = alloc["storage_cost_usd"].sum()
print(f"\ntotal cost:      ${total_cost:,.0f}/yr")
print(f"total flow:      {total_flow:,.0f} tCO2/yr")
print(f"transport share: {transport_total/total_cost*100:.1f}%")
print(f"storage share:   {storage_total/total_cost*100:.1f}%")
print(f"avg cost/ton:    ${total_cost/total_flow:.2f}")
