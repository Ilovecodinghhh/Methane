#!/usr/bin/env python3
"""
Methane Emission & Isotope Analysis (v3 — Literature-updated, truncated-normal MC)
====================================================================================
Updated isotope signatures from:
  [1] Sherwood et al. (2017)  – Global database (10,706 samples)
  [2] Douglas et al. (2021)   – Flux-weighted δ²H, Monte Carlo approach
  [3] Etiope et al. (2019)    – Geological seepage gridded δ¹³C
  [4] Menoud et al. (2022)    – European EMID database
  [5] Lan et al. (2021)       – Gridded δ¹³C maps for inversions
  [6] Singh et al. (2026, pre) – South Asian + global dual-isotope compilation
  [7] Thanwerdas et al. (2025) – Uncertainty propagation framework

Distribution: Truncated Normal (μ ± σ, truncated at ±3σ)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scienceplots
from scipy.stats import truncnorm
from pathlib import Path

plt.style.use(["science", "no-latex", "grid"])

np.random.seed(42)
BASE = Path(__file__).resolve().parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

N_MC = 10000  # increased for better convergence

# ── Updated isotope signatures: (mean, sigma) ────────────────────────────
# See references/ISOTOPE_VALUES.md for full citations and justification.
ISO = {
    # ── Microbial ──
    # Landfill: [1] Table 5 (waste), [2] Table 1
    "landfill":   {"d13C": (-56.0, 4.9),  "dD": (-297, 6)},
    # Livestock (enteric): [6] C3/C4-weighted global; [2] Table 1
    "livestock":  {"d13C": (-63.8, 2.4),   "dD": (-308, 28)},
    # Manure: Arndt et al. (2022); [2] Table 1 (combined)
    "manure":     {"d13C": (-50.0, 5.0),   "dD": (-308, 28)},
    # Rice: [1] Table 5; [2] Table 1
    "rice":       {"d13C": (-62.2, 3.9),   "dD": (-323, 20)},
    # Wastewater: [1]/[4] estimated; [2] inflated σ
    "wastewater": {"d13C": (-52.0, 6.0),   "dD": (-297, 20)},
    # Wetland: [2] flux-weighted global mean
    "wetland":    {"d13C": (-63.9, 3.3),   "dD": (-310, 25)},
    # ── Biomass Burning ──
    # Wildfire: [1] Table 5 (all BB); estimated δ²H
    "wildfire":   {"d13C": (-26.2, 4.8),   "dD": (-211, 30)},
    # Biofuel: [7] sub-sector variability; estimated δ²H
    "biofuel":    {"d13C": (-25.0, 5.0),   "dD": (-220, 35)},
    # ── Fossil Fuel ──
    # Oil & Gas: [1] Table 5 (conventional); [5] production-weighted
    "oil":        {"d13C": (-44.0, 10.7),  "dD": (-194, 50)},
    "gas":        {"d13C": (-44.0, 10.7),  "dD": (-194, 50)},
    # Coal: [1] Table 5; [4] EMID Silesia; compromise δ²H
    "coal":       {"d13C": (-49.5, 11.2),  "dD": (-210, 50)},
    # Geological: [3] emission-weighted; [2] Table 1
    "geological": {"d13C": (-49.0, 10.0),  "dD": (-189, 44)},
}

GROUPS = {
    "Microbial":       ["landfill", "livestock", "manure", "rice", "wastewater", "wetland"],
    "Biomass Burning": ["wildfire", "biofuel"],
    "Fossil Fuel":     ["oil", "gas", "coal", "geological"],
}

PRETTY = {
    "landfill": "Landfill", "livestock": "Livestock", "manure": "Manure",
    "rice": "Rice Paddies", "wastewater": "Wastewater", "wetland": "Wetland",
    "wildfire": "Wildfire", "biofuel": "Biofuel Burning",
    "oil": "Oil", "gas": "Natural Gas", "coal": "Coal", "geological": "Geological",
}

# ── Colour palettes ──────────────────────────────────────────────────────
COLORS_MICRO  = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02"]
COLORS_BB     = ["#e41a1c", "#ff7f00"]
COLORS_FF     = ["#377eb8", "#4daf4a", "#984ea3", "#a65628"]
GROUP_COLORS  = {"Microbial": "#1b9e77", "Biomass Burning": "#e41a1c", "Fossil Fuel": "#377eb8"}
CAT_COLORS = {}

# ── Truncated normal sampler ─────────────────────────────────────────────
def sample_truncnorm(mu, sigma, size):
    """Draw from N(mu, sigma) truncated at ±3σ."""
    a, b = -3, 3  # in units of sigma
    return truncnorm.rvs(a, b, loc=mu, scale=sigma, size=size)

# ── Read helpers (identical to v2) ────────────────────────────────────────
def read_livestock():
    df = pd.read_csv(BASE / "Microbial/monthly_livestock_emission.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")["CH4_Emission_Tg"].rename("emission")

def read_rice():
    df = pd.read_csv(BASE / "Microbial/monthly_rice_emission.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")["Emissions_Tg_per_month"].rename("emission")

def read_landfill():
    df = pd.read_csv(BASE / "Microbial/monthly_landfill_emission.csv", sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%d.%m.%Y")
    return df.set_index("time")["LDF_Tg"].rename("emission")

def read_wetland():
    df = pd.read_csv(BASE / "Microbial/monthly_wetland_emission.csv")
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")["global_total_Tg_month"].rename("emission")

def read_wastewater():
    df = pd.read_csv(BASE / "Microbial/monthly_wastewater_emission.csv", sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%d.%m.%Y")
    return df.set_index("time")["WWT_Tg"].rename("emission")

def read_manure():
    df = pd.read_csv(BASE / "Microbial/monthly_manure_emission.csv")
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")["CH4_MAN_monthly"].rename("emission")

def read_wildfire_emission():
    df = pd.read_csv(BASE / "Biomass Burning/Monthly_Wildfire_emission.csv", sep=";")
    years = df["time"].values
    dates = pd.to_datetime([f"{int(y)}-{int(round((y % 1)*12))+1:02d}-01" for y in years])
    return pd.Series(df["emission(Tg/Year)"].values, index=dates, name="emission")

def read_biofuel():
    df = pd.read_csv(BASE / "Biomass Burning/annually_biofuel_emission.csv", sep=";")
    rows = []
    for _, r in df.iterrows():
        yr = int(r["year"])
        monthly = r["emission_year_Tg_ch4"] / 12.0
        for m in range(1, 13):
            rows.append({"time": pd.Timestamp(yr, m, 1), "emission": monthly})
    return pd.DataFrame(rows).set_index("time")["emission"]

def read_fossil_fuel():
    df = pd.read_csv(BASE / "Fossil Fuel/monthly_coal_gas_oil_emission.csv", sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%d.%m.%Y")
    df = df.set_index("time")
    return {k: df[k].rename("emission") for k in ["coal", "gas", "oil"]}

def read_geological():
    return 21.1 / 12.0

# ── Load ──────────────────────────────────────────────────────────────────
print("Loading data...")
emissions = {}
emissions["landfill"]  = read_landfill()
emissions["livestock"] = read_livestock()
emissions["manure"]    = read_manure()
emissions["rice"]      = read_rice()
emissions["wastewater"]= read_wastewater()
emissions["wetland"]   = read_wetland()
emissions["wildfire"]  = read_wildfire_emission()
emissions["biofuel"]   = read_biofuel()
ff = read_fossil_fuel()
emissions["coal"] = ff["coal"]; emissions["gas"] = ff["gas"]; emissions["oil"] = ff["oil"]
all_dates = sorted(set().union(*(s.index for s in emissions.values())))
emissions["geological"] = pd.Series(read_geological(), index=pd.DatetimeIndex(all_dates), name="emission")

for k in emissions:
    s = emissions[k]
    s.index = s.index.to_period("M").to_timestamp()
    emissions[k] = s.groupby(s.index).mean()

for i, c in enumerate(GROUPS["Microbial"]):       CAT_COLORS[c] = COLORS_MICRO[i]
for i, c in enumerate(GROUPS["Biomass Burning"]): CAT_COLORS[c] = COLORS_BB[i]
for i, c in enumerate(GROUPS["Fossil Fuel"]):     CAT_COLORS[c] = COLORS_FF[i]

# ══════════════════════════════════════════════════════════════════════════
# TASK 1 — Emission plots (stacked area + lines, one figure per group)
# ══════════════════════════════════════════════════════════════════════════
print("\nTask 1: Emission plots...")

for gname, cats in GROUPS.items():
    frames = {c: emissions[c] for c in cats}
    merged = pd.concat(frames, axis=1, join="inner")

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                                          gridspec_kw={"height_ratios": [2, 1.2]})
    cols = [CAT_COLORS[c] for c in cats]
    labels = [PRETTY[c] for c in cats]
    ax_top.stackplot(merged.index, *[merged[c].values for c in cats],
                     labels=labels, colors=cols, alpha=0.85)
    ax_top.set_ylabel("CH$_4$ Emission (Tg month$^{-1}$)")
    ax_top.set_title(f"{gname} Sources — Monthly CH$_4$ Emissions", fontsize=12)
    ax_top.legend(loc="upper left", fontsize=7, ncol=min(3, len(cats)), framealpha=0.9)

    for c in cats:
        ax_bot.plot(merged.index, merged[c].values, label=PRETTY[c],
                    color=CAT_COLORS[c], linewidth=1)
    ax_bot.set_ylabel("Tg month$^{-1}$")
    ax_bot.set_xlabel("Year")
    ax_bot.legend(loc="upper left", fontsize=7, ncol=min(3, len(cats)), framealpha=0.9)

    plt.tight_layout()
    fig.savefig(OUT / f"emission_{gname.replace(' ','_')}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ emission_{gname.replace(' ','_')}.png")

fig, ax = plt.subplots(figsize=(10, 5))
for gname, cats in GROUPS.items():
    merged = pd.concat([emissions[c] for c in cats], axis=1, join="inner")
    total = merged.sum(axis=1)
    ax.plot(total.index, total.values, label=gname, color=GROUP_COLORS[gname], linewidth=1.2)
ax.set_ylabel("Total CH$_4$ Emission (Tg month$^{-1}$)")
ax.set_xlabel("Year")
ax.set_title("Monthly CH$_4$ Emissions by Source Group", fontsize=12)
ax.legend(framealpha=0.9)
plt.tight_layout()
fig.savefig(OUT / "emission_all_groups.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("  ✓ emission_all_groups.png")

# ══════════════════════════════════════════════════════════════════════════
# TASK 2 — Monte-Carlo: truncated-normal isotope, IQR (25th–75th)
# ══════════════════════════════════════════════════════════════════════════
print("\nTask 2: Truncated-normal Monte-Carlo isotope (IQR)...")

def compute_group_isotope_mc(cat_list, iso_key):
    frames = {c: emissions[c] for c in cat_list}
    merged_em = pd.concat(frames, axis=1, join="inner")
    dates = merged_em.index
    n = len(dates)

    weighted_sum = np.zeros((n, N_MC))
    total_em = np.zeros((n, N_MC))

    for cat in cat_list:
        em = merged_em[cat].values
        mu, sigma = ISO[cat][iso_key]
        iso_samples = sample_truncnorm(mu, sigma, (n, N_MC))
        weighted_sum += em[:, None] * iso_samples
        total_em += em[:, None]

    delta = weighted_sum / total_em

    return pd.DataFrame({
        "date": dates,
        f"{iso_key}_median": np.median(delta, axis=1),
        f"{iso_key}_mean":   np.mean(delta, axis=1),
        f"{iso_key}_q25":    np.percentile(delta, 25, axis=1),
        f"{iso_key}_q75":    np.percentile(delta, 75, axis=1),
        f"{iso_key}_std":    np.std(delta, axis=1),
    }).set_index("date")

results = {}
for gname, cats in GROUPS.items():
    print(f"  Processing {gname}...")
    d13C = compute_group_isotope_mc(cats, "d13C")
    dD   = compute_group_isotope_mc(cats, "dD")
    results[gname] = pd.concat([d13C, dD], axis=1)

# ══════════════════════════════════════════════════════════════════════════
# TASK 3 — Plot isotopes & save CSV
# ══════════════════════════════════════════════════════════════════════════
print("\nTask 3: Plotting isotopes & saving CSV...")

for gname, df in results.items():
    csv_path = OUT / f"isotope_{gname.replace(' ','_')}.csv"
    df.to_csv(csv_path)
    print(f"  ✓ {csv_path.name}")

    color_c = GROUP_COLORS[gname]
    color_d = {"Microbial": "#d95f02", "Biomass Burning": "#ff7f00", "Fossil Fuel": "#984ea3"}[gname]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.suptitle(f"{gname} — Emission-Weighted Isotope Signatures\n"
                 f"(Truncated-Normal MC, n = {N_MC:,}; shading = IQR 25th–75th)",
                 fontsize=11)

    ax1.plot(df.index, df["d13C_median"], color=color_c, linewidth=1, label="Median")
    ax1.fill_between(df.index, df["d13C_q25"], df["d13C_q75"],
                     alpha=0.3, color=color_c, label="IQR (25th–75th)")
    ax1.set_ylabel("$\\delta^{13}$C (‰ VPDB)")
    ax1.legend(loc="best", fontsize=8, framealpha=0.9)

    ax2.plot(df.index, df["dD_median"], color=color_d, linewidth=1, label="Median")
    ax2.fill_between(df.index, df["dD_q25"], df["dD_q75"],
                     alpha=0.3, color=color_d, label="IQR (25th–75th)")
    ax2.set_ylabel("$\\delta$D (‰ VSMOW)")
    ax2.set_xlabel("Year")
    ax2.legend(loc="best", fontsize=8, framealpha=0.9)

    plt.tight_layout()
    fig.savefig(OUT / f"isotope_{gname.replace(' ','_')}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ isotope_{gname.replace(' ','_')}.png")

# Save emission CSVs
for gname, cats in GROUPS.items():
    merged = pd.concat({c: emissions[c] for c in cats}, axis=1, join="inner")
    merged["total"] = merged.sum(axis=1)
    merged.to_csv(OUT / f"emission_{gname.replace(' ','_')}.csv")
    print(f"  ✓ emission_{gname.replace(' ','_')}.csv")

# ══════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "="*72)
print("SUMMARY — UPDATED ISOTOPE VALUES (Truncated-Normal)")
print("="*72)

for gname, cats in GROUPS.items():
    merged = pd.concat({c: emissions[c] for c in cats}, axis=1, join="inner")
    total = merged.sum(axis=1)
    annual = total.resample("YE").sum()
    iso_df = results[gname]

    print(f"\n── {gname} ──")
    print(f"  Emission (annual Tg):  mean={annual.mean():.1f}")
    for cat in cats:
        mu_c, sig_c = ISO[cat]["d13C"]
        mu_d, sig_d = ISO[cat]["dD"]
        print(f"    {PRETTY[cat]:18s}  δ¹³C = {mu_c:.1f} ± {sig_c:.1f}‰  "
              f"δD = {mu_d:.0f} ± {sig_d:.0f}‰")
    iqr_c = (iso_df["d13C_q75"] - iso_df["d13C_q25"]).mean()
    iqr_d = (iso_df["dD_q75"] - iso_df["dD_q25"]).mean()
    print(f"  Group δ¹³C:  median={iso_df['d13C_median'].mean():.1f}‰  IQR width={iqr_c:.1f}‰")
    print(f"  Group δD:    median={iso_df['dD_median'].mean():.1f}‰  IQR width={iqr_d:.1f}‰")

print("\n" + "="*72)
print("KEY IMPROVEMENTS OVER v2 (uniform)")
print("="*72)
print("""
1. WETLAND uncertainty collapsed: old uniform ±27.7‰ → truncated-normal σ=3.3‰ [2]
2. LIVESTOCK δ²H tightened: old range 210‰ → σ=28‰ (flux-weighted) [2,6]
3. LANDFILL δ²H very tight: σ=6‰ — one of the best-constrained sources [2]
4. GEOLOGICAL δ¹³C corrected lighter: −49‰ (was ~−38‰ in old literature) [3]
5. MANURE separated from livestock: δ¹³C ~14‰ heavier than enteric [Arndt 2022]
6. Truncated-normal distributions concentrate probability around observed means,
   yielding narrower IQR than uniform — better reflecting actual measurement spread.
""")

print("✅ All done! Results in:", OUT)
