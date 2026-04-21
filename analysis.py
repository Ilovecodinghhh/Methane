#!/usr/bin/env python3
"""
Methane Emission & Isotope Analysis
====================================
1. Read all subcategory emission data, aggregate by group, and plot.
2. Monte-Carlo weighted monthly isotope time series (δ13C and δD) per group.
3. Save results to CSV and plots to PNG.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

np.random.seed(42)

BASE = Path(__file__).resolve().parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

N_MC = 5000  # Monte-Carlo iterations

# ── Isotope ranges (per mil) ──────────────────────────────────────────────
ISO = {
    # Microbial
    "landfill":   {"d13C": (-60, -40),  "dD": (-350, -250)},
    "livestock":  {"d13C": (-67.8, -54.6), "dD": (-360, -150)},
    "manure":     {"d13C": (-65, -45),  "dD": (-350, -300)},
    "rice":       {"d13C": (-70, -55),  "dD": (-390, -320)},
    "wastewater": {"d13C": (-60, -45),  "dD": (-360, -300)},
    "wetland":    {"d13C": (-73.6, -18.2), "dD": (-400, -300)},
    # Biomass Burning
    "wildfire":   {"d13C": (-26.7, -12.6), "dD": (-260, -170)},
    "biofuel":    {"d13C": (-26.7, -12.6), "dD": (-270, -190)},
    # Fossil Fuel
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

# ── Helper: uniform Monte-Carlo samples ───────────────────────────────────
def mc_uniform(lo, hi, size):
    return np.random.uniform(lo, hi, size)

# ── Read helpers ──────────────────────────────────────────────────────────
def read_livestock():
    df = pd.read_csv(BASE / "Microbial/monthly_livestock_emission.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df.rename(columns={"Date": "time", "CH4_Emission_Tg": "emission"}).set_index("time")["emission"]

def read_rice():
    df = pd.read_csv(BASE / "Microbial/monthly_rice_emission.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df.rename(columns={"Date": "time", "Emissions_Tg_per_month": "emission"}).set_index("time")["emission"]

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
    # Decimal year → datetime
    years = df["time"].values
    dates = pd.to_datetime([f"{int(y)}-{int(round((y % 1) * 12)) + 1:02d}-01" for y in years])
    s = pd.Series(df["emission(Tg/Year)"].values, index=dates, name="emission")
    # Values are monthly Tg (12 per year, sum ≈ 30 Tg/yr consistent with literature)
    return s

def read_wildfire_d13C():
    df = pd.read_csv(BASE / "Biomass Burning/Monthly_Wildfire_d13C.csv", sep=";")
    years = df["time"].values
    dates = pd.to_datetime([f"{int(y)}-{int(round((y % 1) * 12)) + 1:02d}-01" for y in years])
    return pd.Series(df["Isotope value for the month"].values, index=dates, name="d13C_wildfire")

def read_biofuel():
    """Annual → monthly (÷12)."""
    df = pd.read_csv(BASE / "Biomass Burning/annually_biofuel_emission.csv", sep=";")
    rows = []
    for _, r in df.iterrows():
        yr = int(r["year"])
        monthly = r["emission_year_Tg_ch4"] / 12.0
        for m in range(1, 13):
            rows.append({"time": pd.Timestamp(yr, m, 1), "emission": monthly})
    s = pd.DataFrame(rows).set_index("time")["emission"]
    return s

def read_fossil_fuel():
    """Returns dict with coal, gas, oil Series."""
    df = pd.read_csv(BASE / "Fossil Fuel/monthly_coal_gas_oil_emission.csv", sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%d.%m.%Y")
    df = df.set_index("time")
    return {k: df[k].rename("emission") for k in ["coal", "gas", "oil"]}

def read_geological():
    """Constant 21.1 Tg/yr → monthly."""
    return 21.1 / 12.0  # Tg/month, constant

# ── Load all emissions ────────────────────────────────────────────────────
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
emissions["coal"] = ff["coal"]
emissions["gas"]  = ff["gas"]
emissions["oil"]  = ff["oil"]

# Geological: build a series spanning union of all dates
all_dates = sorted(set().union(*(s.index for s in emissions.values())))
geo_monthly = read_geological()
emissions["geological"] = pd.Series(geo_monthly, index=pd.DatetimeIndex(all_dates), name="emission")

# Also load the wildfire observed d13C for reference
wildfire_d13C_obs = read_wildfire_d13C()

# ── Normalise index to month-start ────────────────────────────────────────
for k in emissions:
    s = emissions[k]
    s.index = s.index.to_period("M").to_timestamp()
    emissions[k] = s.groupby(s.index).mean()  # deduplicate if any

# ══════════════════════════════════════════════════════════════════════════
# TASK 1 — Plot emission for each big group
# ══════════════════════════════════════════════════════════════════════════
print("Task 1: Plotting group emissions...")

for gname, cats in GROUPS.items():
    fig, axes = plt.subplots(len(cats), 1, figsize=(12, 3 * len(cats)),
                             sharex=False, squeeze=False)
    fig.suptitle(f"{gname} — Monthly CH₄ Emissions (Tg)", fontsize=14, y=1.01)
    for i, cat in enumerate(cats):
        ax = axes[i, 0]
        s = emissions[cat]
        ax.plot(s.index, s.values, linewidth=0.8)
        ax.set_ylabel("Tg / month")
        ax.set_title(cat.capitalize())
        ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(OUT / f"emission_{gname.replace(' ', '_')}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved emission_{gname.replace(' ', '_')}.png")

# Also a combined summary plot (one line per group)
fig, ax = plt.subplots(figsize=(14, 6))
for gname, cats in GROUPS.items():
    # Align to common index, sum
    frames = [emissions[c] for c in cats]
    merged = pd.concat(frames, axis=1, join="inner")
    total = merged.sum(axis=1)
    ax.plot(total.index, total.values, label=gname, linewidth=1)
ax.set_ylabel("Total CH₄ Emission (Tg / month)")
ax.set_title("Monthly CH₄ Emissions by Source Group")
ax.legend()
ax.grid(alpha=0.3)
fig.savefig(OUT / "emission_all_groups.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("  Saved emission_all_groups.png")

# ══════════════════════════════════════════════════════════════════════════
# TASK 2 — Monte-Carlo weighted isotope time series per group
# ══════════════════════════════════════════════════════════════════════════
print("Task 2: Monte-Carlo isotope calculation...")

def compute_group_isotope_mc(group_name, cat_list, iso_key):
    """
    For each month in the overlapping period, compute
        δ_group = Σ(emission_i * δ_i) / Σ(emission_i)
    where δ_i ~ Uniform(lo, hi) for each subcategory i.
    Returns DataFrame with columns: median, p5, p95, mean, std.
    """
    # Find common date range
    frames = {c: emissions[c] for c in cat_list}
    merged_em = pd.concat(frames, axis=1, join="inner")  # columns = cat names
    dates = merged_em.index
    n_months = len(dates)

    # MC array: (n_months, N_MC)
    weighted_sum = np.zeros((n_months, N_MC))
    total_em = np.zeros((n_months, N_MC))

    for cat in cat_list:
        em = merged_em[cat].values  # (n_months,)
        lo, hi = ISO[cat][iso_key]

        # For wildfire d13C we have observed monthly values — use them as the mean
        # with a small spread, but the task says use the range, so stick with uniform.
        iso_samples = mc_uniform(lo, hi, (n_months, N_MC))  # (n_months, N_MC)

        # emission is deterministic (from data); isotope is uncertain
        weighted_sum += em[:, None] * iso_samples
        total_em += em[:, None]

    delta_group = weighted_sum / total_em  # (n_months, N_MC)

    result = pd.DataFrame({
        "date": dates,
        f"{iso_key}_median": np.median(delta_group, axis=1),
        f"{iso_key}_mean":   np.mean(delta_group, axis=1),
        f"{iso_key}_p5":     np.percentile(delta_group, 5, axis=1),
        f"{iso_key}_p95":    np.percentile(delta_group, 95, axis=1),
        f"{iso_key}_std":    np.std(delta_group, axis=1),
    })
    return result.set_index("date")

results = {}
for gname, cats in GROUPS.items():
    print(f"  Processing {gname}...")
    d13C = compute_group_isotope_mc(gname, cats, "d13C")
    dD   = compute_group_isotope_mc(gname, cats, "dD")
    combined = pd.concat([d13C, dD], axis=1)
    results[gname] = combined

# ══════════════════════════════════════════════════════════════════════════
# TASK 3 — Plot & save CSV
# ══════════════════════════════════════════════════════════════════════════
print("Task 3: Plotting isotopes & saving CSV...")

for gname, df in results.items():
    # Save CSV
    csv_path = OUT / f"isotope_{gname.replace(' ', '_')}.csv"
    df.to_csv(csv_path)
    print(f"  Saved {csv_path.name}")

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    fig.suptitle(f"{gname} — Emission-Weighted Isotope Signatures (Monte Carlo, n={N_MC})",
                 fontsize=13)

    # δ13C
    ax1.plot(df.index, df["d13C_median"], color="C0", linewidth=1, label="Median")
    ax1.fill_between(df.index, df["d13C_p5"], df["d13C_p95"],
                     alpha=0.25, color="C0", label="5th–95th percentile")
    ax1.set_ylabel("δ¹³C (‰)")
    ax1.legend(loc="upper right")
    ax1.grid(alpha=0.3)

    # δD
    ax2.plot(df.index, df["dD_median"], color="C1", linewidth=1, label="Median")
    ax2.fill_between(df.index, df["dD_p5"], df["dD_p95"],
                     alpha=0.25, color="C1", label="5th–95th percentile")
    ax2.set_ylabel("δD (‰)")
    ax2.set_xlabel("Date")
    ax2.legend(loc="upper right")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    fig.savefig(OUT / f"isotope_{gname.replace(' ', '_')}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved isotope_{gname.replace(' ', '_')}.png")

# ── Also save group emission totals to CSV ────────────────────────────────
for gname, cats in GROUPS.items():
    frames = {c: emissions[c] for c in cats}
    merged = pd.concat(frames, axis=1, join="inner")
    merged["total"] = merged.sum(axis=1)
    csv_path = OUT / f"emission_{gname.replace(' ', '_')}.csv"
    merged.to_csv(csv_path)
    print(f"  Saved {csv_path.name}")

print("\n✅ All done! Results in:", OUT)
