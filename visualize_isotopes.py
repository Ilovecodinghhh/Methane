#!/usr/bin/env python3
"""
Isotope Signature Visualization — δ¹³C and δD for all 12 categories + group summaries.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scienceplots
from matplotlib.patches import Ellipse
from pathlib import Path

plt.style.use(["science", "no-latex", "grid"])

BASE = Path(__file__).resolve().parent
OUT = BASE / "output"

# ── Isotope values (mean, sigma) ─────────────────────────────────────────
ISO = {
    "Landfill":       {"d13C": (-56.0, 4.9),  "dD": (-297, 6),    "group": "Microbial"},
    "Livestock":      {"d13C": (-63.8, 2.4),  "dD": (-308, 28),   "group": "Microbial"},
    "Manure":         {"d13C": (-50.0, 5.0),  "dD": (-308, 28),   "group": "Microbial"},
    "Rice Paddies":   {"d13C": (-62.2, 3.9),  "dD": (-323, 20),   "group": "Microbial"},
    "Wastewater":     {"d13C": (-52.0, 6.0),  "dD": (-297, 20),   "group": "Microbial"},
    "Wetland":        {"d13C": (-63.9, 3.3),  "dD": (-310, 25),   "group": "Microbial"},
    "Wildfire":       {"d13C": (-26.2, 4.8),  "dD": (-211, 30),   "group": "Biomass Burning"},
    "Biofuel":        {"d13C": (-25.0, 5.0),  "dD": (-220, 35),   "group": "Biomass Burning"},
    "Oil":            {"d13C": (-44.0, 10.7), "dD": (-194, 50),   "group": "Fossil Fuel"},
    "Natural Gas":    {"d13C": (-44.0, 10.7), "dD": (-194, 50),   "group": "Fossil Fuel"},
    "Coal":           {"d13C": (-49.5, 11.2), "dD": (-210, 50),   "group": "Fossil Fuel"},
    "Geological":     {"d13C": (-49.0, 10.0), "dD": (-189, 44),   "group": "Fossil Fuel"},
}

GROUP_COLORS = {"Microbial": "#1b9e77", "Biomass Burning": "#e41a1c", "Fossil Fuel": "#377eb8"}
MARKERS = {"Microbial": "o", "Biomass Burning": "s", "Fossil Fuel": "D"}

# ══════════════════════════════════════════════════════════════════════════
# FIGURE 1: Dual-isotope scatter (δ¹³C vs δD) with 1σ and 2σ ellipses
# ══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 8))

for name, vals in ISO.items():
    g = vals["group"]
    mu_c, sig_c = vals["d13C"]
    mu_d, sig_d = vals["dD"]

    # 2σ ellipse (light)
    ell2 = Ellipse((mu_c, mu_d), width=4*sig_c, height=4*sig_d,
                   facecolor=GROUP_COLORS[g], alpha=0.08, edgecolor="none")
    ax.add_patch(ell2)

    # 1σ ellipse
    ell1 = Ellipse((mu_c, mu_d), width=2*sig_c, height=2*sig_d,
                   facecolor=GROUP_COLORS[g], alpha=0.2, edgecolor=GROUP_COLORS[g],
                   linewidth=0.8, linestyle="--")
    ax.add_patch(ell1)

    # Center point
    ax.scatter(mu_c, mu_d, color=GROUP_COLORS[g], marker=MARKERS[g],
               s=60, zorder=5, edgecolors="white", linewidths=0.5)
    
    # Label
    offset_x = 1.5 if mu_c > -55 else -1.5
    ha = "left" if mu_c > -55 else "right"
    ax.annotate(name, (mu_c, mu_d), fontsize=7,
                xytext=(offset_x, 5), textcoords="offset points",
                ha=ha, va="bottom", color=GROUP_COLORS[g], fontweight="bold")

# Legend for groups
for g in GROUP_COLORS:
    ax.scatter([], [], color=GROUP_COLORS[g], marker=MARKERS[g], s=60, label=g)
ax.plot([], [], color="gray", linestyle="--", linewidth=0.8, label="1$\\sigma$ ellipse")

ax.set_xlabel("$\\delta^{13}$C (‰ VPDB)", fontsize=11)
ax.set_ylabel("$\\delta$D (‰ VSMOW)", fontsize=11)
ax.set_title("Dual-Isotope Source Signatures of Methane — All Categories\n"
             "(ellipses = 1$\\sigma$ dashed, 2$\\sigma$ shaded)", fontsize=12)
ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
ax.set_xlim(-82, -8)
ax.set_ylim(-420, -100)

plt.tight_layout()
fig.savefig(OUT / "isotope_dual_scatter.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("✓ isotope_dual_scatter.png")

# ══════════════════════════════════════════════════════════════════════════
# FIGURE 2: δ¹³C bar chart with error bars, grouped by source group
# ══════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

groups_ordered = ["Microbial", "Biomass Burning", "Fossil Fuel"]
names_by_group = {g: [n for n, v in ISO.items() if v["group"] == g] for g in groups_ordered}
all_names = []
for g in groups_ordered:
    all_names.extend(names_by_group[g])

y_pos = np.arange(len(all_names))
colors = [GROUP_COLORS[ISO[n]["group"]] for n in all_names]

# δ¹³C
means_c = [ISO[n]["d13C"][0] for n in all_names]
sigs_c = [ISO[n]["d13C"][1] for n in all_names]
ax1.barh(y_pos, means_c, xerr=sigs_c, color=colors, alpha=0.8,
         edgecolor="white", linewidth=0.5, capsize=3, error_kw={"linewidth": 1})
ax1.set_yticks(y_pos)
ax1.set_yticklabels(all_names, fontsize=9)
ax1.set_xlabel("$\\delta^{13}$C (‰ VPDB)")
ax1.set_title("$\\delta^{13}$C Source Signatures (mean ± 1$\\sigma$)")
ax1.invert_yaxis()
# Add group separators
cumul = 0
for g in groups_ordered[:-1]:
    cumul += len(names_by_group[g])
    ax1.axhline(cumul - 0.5, color="gray", linewidth=0.5, linestyle=":")

# δD
means_d = [ISO[n]["dD"][0] for n in all_names]
sigs_d = [ISO[n]["dD"][1] for n in all_names]
ax2.barh(y_pos, means_d, xerr=sigs_d, color=colors, alpha=0.8,
         edgecolor="white", linewidth=0.5, capsize=3, error_kw={"linewidth": 1})
ax2.set_yticks(y_pos)
ax2.set_yticklabels(all_names, fontsize=9)
ax2.set_xlabel("$\\delta$D (‰ VSMOW)")
ax2.set_title("$\\delta$D Source Signatures (mean ± 1$\\sigma$)")
ax2.invert_yaxis()
cumul = 0
for g in groups_ordered[:-1]:
    cumul += len(names_by_group[g])
    ax2.axhline(cumul - 0.5, color="gray", linewidth=0.5, linestyle=":")

plt.tight_layout()
fig.savefig(OUT / "isotope_signatures_bars.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("✓ isotope_signatures_bars.png")

# ══════════════════════════════════════════════════════════════════════════
# FIGURE 3: Group-level emission-weighted time series comparison (all 3 groups on same axes)
# ══════════════════════════════════════════════════════════════════════════
iso_data = {}
for gname in groups_ordered:
    gkey = gname.replace(" ", "_")
    df = pd.read_csv(OUT / f"isotope_{gkey}.csv", index_col="date", parse_dates=True)
    iso_data[gname] = df

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
fig.suptitle("Emission-Weighted Isotope Signatures — All Groups Compared\n"
             "(Truncated-Normal MC, n = 10,000; shading = IQR)", fontsize=12)

for gname in groups_ordered:
    df = iso_data[gname]
    c = GROUP_COLORS[gname]
    
    ax1.plot(df.index, df["d13C_median"], color=c, linewidth=1, label=gname)
    ax1.fill_between(df.index, df["d13C_q25"], df["d13C_q75"], alpha=0.15, color=c)
    
    ax2.plot(df.index, df["dD_median"], color=c, linewidth=1, label=gname)
    ax2.fill_between(df.index, df["dD_q25"], df["dD_q75"], alpha=0.15, color=c)

ax1.set_ylabel("$\\delta^{13}$C (‰ VPDB)")
ax1.legend(loc="center right", fontsize=9, framealpha=0.9)
ax2.set_ylabel("$\\delta$D (‰ VSMOW)")
ax2.set_xlabel("Year")
ax2.legend(loc="center right", fontsize=9, framealpha=0.9)

plt.tight_layout()
fig.savefig(OUT / "isotope_all_groups_comparison.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("✓ isotope_all_groups_comparison.png")

print("\n✅ All visualization done!")
