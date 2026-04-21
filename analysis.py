#!/usr/bin/env python3
"""
Methane Emission & Isotope Analysis (v2 — SciencePlots, IQR, polished)
========================================================================
1. Read all subcategory emission data, plot per big group (all categories on one figure).
2. Monte-Carlo weighted monthly isotope (δ13C & δD) per group with IQR (25th–75th).
3. Plot & save to CSV. Print summary statistics and suggestions.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scienceplots
from pathlib import Path

plt.style.use(["science", "no-latex", "grid"])

np.random.seed(42)
BASE = Path(__file__).resolve().parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

N_MC = 5000

# ── Colour palettes ──────────────────────────────────────────────────────
COLORS_MICRO  = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02"]
COLORS_BB     = ["#e41a1c", "#ff7f00"]
COLORS_FF     = ["#377eb8", "#4daf4a", "#984ea3", "#a65628"]
GROUP_COLORS  = {"Microbial": "#1b9e77", "Biomass Burning": "#e41a1c", "Fossil Fuel": "#377eb8"}
CAT_COLORS = {}

# ── Isotope ranges (‰) ───────────────────────────────────────────────────
ISO = {
    "landfill":   {"d13C": (-60, -40),    "dD": (-350, -250)},
    "livestock":  {"d13C": (-67.8, -54.6), "dD": (-360, -150)},
    "manure":     {"d13C": (-65, -45),     "dD": (-350, -300)},
    "rice":       {"d13C": (-70, -55),     "dD": (-390, -320)},
    "wastewater": {"d13C": (-60, -45),     "dD": (-360, -300)},
    "wetland":    {"d13C": (-73.6, -18.2), "dD": (-400, -300)},
    "wildfire":   {"d13C": (-26.7, -12.6), "dD": (-260, -170)},
    "biofuel":    {"d13C": (-26.7, -12.6), "dD": (-270, -190)},
    "oil":        {"d13C": (-65.0, -29.1), "dD": (-250, -120)},
    "gas":        {"d13C": (-65.0, -29.1), "dD": (-250, -100)},
    "coal":       {"d13C": (-64.1, -30.8), "dD": (-240, -110)},
    "geological": {"d13C": (-68.0, -24.3), "dD": (-300, -100)},
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

# ── Read helpers ──────────────────────────────────────────────────────────
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

# Normalise to month-start
for k in emissions:
    s = emissions[k]
    s.index = s.index.to_period("M").to_timestamp()
    emissions[k] = s.groupby(s.index).mean()

# Assign colours
for i, c in enumerate(GROUPS["Microbial"]):       CAT_COLORS[c] = COLORS_MICRO[i]
for i, c in enumerate(GROUPS["Biomass Burning"]): CAT_COLORS[c] = COLORS_BB[i]
for i, c in enumerate(GROUPS["Fossil Fuel"]):     CAT_COLORS[c] = COLORS_FF[i]

# ══════════════════════════════════════════════════════════════════════════
# TASK 1 — Emission stacked-area + line plot per group (one figure per group)
# ══════════════════════════════════════════════════════════════════════════
print("\nTask 1: Emission plots...")

for gname, cats in GROUPS.items():
    frames = {c: emissions[c] for c in cats}
    merged = pd.concat(frames, axis=1, join="inner")

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                                          gridspec_kw={"height_ratios": [2, 1.2]})

    # Top: stacked area
    cols = [CAT_COLORS[c] for c in cats]
    labels = [PRETTY[c] for c in cats]
    ax_top.stackplot(merged.index, *[merged[c].values for c in cats],
                     labels=labels, colors=cols, alpha=0.85)
    ax_top.set_ylabel("CH$_4$ Emission (Tg month$^{-1}$)")
    ax_top.set_title(f"{gname} Sources — Monthly CH$_4$ Emissions", fontsize=12)
    ax_top.legend(loc="upper left", fontsize=7, ncol=min(3, len(cats)), framealpha=0.9)

    # Bottom: individual lines
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

# Combined overview
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
# TASK 2 — Monte-Carlo isotope (IQR: 25th–75th)
# ══════════════════════════════════════════════════════════════════════════
print("\nTask 2: Monte-Carlo isotope calculation (IQR)...")

def compute_group_isotope_mc(cat_list, iso_key):
    frames = {c: emissions[c] for c in cat_list}
    merged_em = pd.concat(frames, axis=1, join="inner")
    dates = merged_em.index
    n = len(dates)

    weighted_sum = np.zeros((n, N_MC))
    total_em = np.zeros((n, N_MC))

    for cat in cat_list:
        em = merged_em[cat].values
        lo, hi = ISO[cat][iso_key]
        iso_samples = np.random.uniform(lo, hi, (n, N_MC))
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
    # Slightly different shade for dD
    color_d = {"Microbial": "#d95f02", "Biomass Burning": "#ff7f00", "Fossil Fuel": "#984ea3"}[gname]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.suptitle(f"{gname} — Emission-Weighted Isotope Signatures\n"
                 f"(Monte Carlo, n = {N_MC:,}; shading = IQR 25th–75th)",
                 fontsize=11)

    # δ13C
    ax1.plot(df.index, df["d13C_median"], color=color_c, linewidth=1, label="Median")
    ax1.fill_between(df.index, df["d13C_q25"], df["d13C_q75"],
                     alpha=0.3, color=color_c, label="IQR (25th–75th)")
    ax1.set_ylabel("$\\delta^{13}$C (‰ VPDB)")
    ax1.legend(loc="best", fontsize=8, framealpha=0.9)

    # δD
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
# Summary statistics & suggestions
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "="*72)
print("SUMMARY STATISTICS")
print("="*72)

for gname, cats in GROUPS.items():
    merged = pd.concat({c: emissions[c] for c in cats}, axis=1, join="inner")
    total = merged.sum(axis=1)
    annual = total.resample("YE").sum()
    iso_df = results[gname]

    print(f"\n── {gname} ──")
    print(f"  Emission (annual Tg):  mean={annual.mean():.1f}  "
          f"min={annual.min():.1f}  max={annual.max():.1f}")
    for cat in cats:
        s = merged[cat]
        ann = s.resample("YE").sum()
        frac = (ann / annual * 100)
        print(f"    {PRETTY[cat]:18s}  mean={ann.mean():7.1f} Tg/yr  ({frac.mean():5.1f}%)")

    print(f"  δ13C median (‰):  overall={iso_df['d13C_median'].mean():.1f}  "
          f"IQR width={( iso_df['d13C_q75'] - iso_df['d13C_q25'] ).mean():.1f}")
    print(f"  δD   median (‰):  overall={iso_df['dD_median'].mean():.1f}  "
          f"IQR width={( iso_df['dD_q75'] - iso_df['dD_q25'] ).mean():.1f}")

print("\n" + "="*72)
print("SUGGESTIONS FOR INTERPRETATION")
print("="*72)
print("""
1. ISOTOPE SEPARATION BETWEEN GROUPS
   - Biomass Burning has the most enriched δ13C (≈ −20‰), clearly distinct from
     Microbial (≈ −53‰) and Fossil Fuel (≈ −47‰). δ13C alone can separate
     biomass burning from the other two, but NOT microbial from fossil fuel.
   - δD adds discrimination: Microbial sources are the most D-depleted (≈ −315‰)
     while Fossil Fuel (≈ −180‰) and Biomass Burning (≈ −220‰) are heavier.
   → Use dual-isotope (δ13C vs δD) space to separate all three groups.

2. LARGE UNCERTAINTY IN MICROBIAL SIGNATURES
   - Wetland δ13C spans −73.6 to −18.2‰ — this alone dominates the IQR.
   - Wetland is also the largest microbial emitter (~160 Tg/yr).
   → Narrowing wetland isotope constraints would most improve group-level estimates.
   → Consider region-specific or biome-specific wetland isotope values.

3. FOSSIL FUEL SUBCATEGORIES OVERLAP
   - Oil, gas, coal, and geological all share very similar δ13C and δD ranges.
   - Their isotopic separation is poor; source attribution within fossil fuel
     requires additional tracers (e.g., ethane/methane ratio, 14C, clumped isotopes).

4. TEMPORAL TRENDS
   - Microbial emissions show strong seasonality (rice + wetland peak in boreal summer).
   - Fossil Fuel emissions show a steady upward trend (gas growth).
   - Biomass Burning is relatively stable.
   → Seasonal isotope variations are driven mainly by the microbial group;
     this can be leveraged for top-down inversion studies.

5. MONTE CARLO APPROACH
   - Uniform distributions are conservative (maximum entropy for bounded ranges).
   - If literature provides means ± σ, switching to truncated-normal would
     tighten the IQR and better reflect the actual knowledge state.
   - Consider correlating isotope values with emission magnitude if data permits.

6. PRACTICAL RECOMMENDATIONS
   - For atmospheric modelling: report emission-weighted isotope signatures
     with IQR as the uncertainty band (this analysis).
   - For source attribution: combine δ13C and δD in a Keeling-plot or
     Bayesian mixing model framework.
   - Priority measurement targets: wetland-specific δ13C, livestock δD
     (current range −360 to −150‰ is very broad).
""")

print("✅ All done! Results in:", OUT)
