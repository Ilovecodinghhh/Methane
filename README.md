# Methane Source Attribution Using Stable Isotopes

A global methane (CH₄) emission and isotope analysis project. Monthly emission data from 12 subcategories are aggregated into three main source groups, and emission-weighted isotopic signatures (δ¹³C and δD) are estimated using Monte Carlo simulation with literature-derived uncertainties.

---

## Table of Contents

- [Background](#background)
- [Source Groups & Categories](#source-groups--categories)
- [Repository Structure](#repository-structure)
- [Data Description](#data-description)
- [Analysis Pipeline](#analysis-pipeline)
- [Isotope Source Signatures](#isotope-source-signatures)
- [Key Results](#key-results)
- [How to Run](#how-to-run)
- [References](#references)

---

## Background

Different methane sources carry distinct **stable isotope fingerprints** in their carbon (¹³C/¹²C, reported as δ¹³C) and hydrogen (D/H, reported as δD) ratios. These fingerprints allow atmospheric scientists to attribute observed methane to specific source types — a technique central to constraining the global methane budget.

This project:
1. Compiles monthly emission time series for all major CH₄ sources
2. Assigns literature-based isotope signatures (mean ± σ) to each source
3. Uses **Monte Carlo simulation** (truncated-normal, n = 10,000) to propagate isotope uncertainties
4. Produces emission-weighted monthly isotope time series for each source group

**Units:** Emissions in **Tg CH₄**, isotope values in **‰ (per mil)**

---

## Source Groups & Categories

Methane sources are divided into three main groups based on formation process:

| Group | Categories | Formation Process |
|-------|-----------|-------------------|
| **Microbial** | Landfill, Livestock, Manure, Rice Paddies, Wastewater, Wetland | Methanogenesis by archaea under anaerobic conditions |
| **Biomass Burning** | Wildfire, Biofuel Burning | Incomplete combustion of organic matter |
| **Fossil Fuel** | Oil, Natural Gas, Coal, Geological Seepage | Thermogenic decomposition of buried organic matter (+ some microbial) |

---

## Repository Structure

```
Methane/
├── analysis.py                  # Main analysis script (run this)
├── README.md                    # This file
│
├── Microbial/                   # Monthly emission data (microbial sources)
│   ├── monthly_landfill_emission.csv
│   ├── monthly_livestock_emission.csv
│   ├── monthly_manure_emission.csv
│   ├── monthly_rice_emission.csv
│   ├── monthly_wastewater_emission.csv
│   └── monthly_wetland_emission.csv
│
├── Biomass Burning/             # Emission + observed δ¹³C data
│   ├── Monthly_Wildfire_emission.csv
│   ├── Monthly_Wildfire_d13C.csv
│   └── annually_biofuel_emission.csv
│
├── Fossil Fuel/                 # Coal, gas, oil emission + geological constant
│   ├── monthly_coal_gas_oil_emission.csv
│   └── Geological_emission.txt
│
├── output/                      # Generated plots and CSV results
│   ├── emission_*.png / .csv    # Emission time series (per group + combined)
│   └── isotope_*.png / .csv     # Isotope time series with IQR uncertainty
│
└── references/                  # Literature sources
    ├── ISOTOPE_VALUES.md        # Full documentation of all isotope values with citations
    └── *.pdf                    # 7 downloaded reference papers
```

---

## Data Description

### Emission Data

| Source | File | Time Range | Format Notes |
|--------|------|------------|-------------|
| Landfill | `Microbial/monthly_landfill_emission.csv` | Monthly | Semicolon-delimited, `dd.mm.yyyy` dates |
| Livestock | `Microbial/monthly_livestock_emission.csv` | Monthly | Comma-delimited |
| Manure | `Microbial/monthly_manure_emission.csv` | Monthly | Comma-delimited |
| Rice | `Microbial/monthly_rice_emission.csv` | Monthly | Comma-delimited |
| Wastewater | `Microbial/monthly_wastewater_emission.csv` | Monthly | Semicolon-delimited, `dd.mm.yyyy` dates |
| Wetland | `Microbial/monthly_wetland_emission.csv` | Monthly | Comma-delimited |
| Wildfire | `Biomass Burning/Monthly_Wildfire_emission.csv` | Monthly | Semicolon-delimited, decimal-year time |
| Biofuel | `Biomass Burning/annually_biofuel_emission.csv` | Annual → Monthly (÷12) | Semicolon-delimited |
| Coal/Gas/Oil | `Fossil Fuel/monthly_coal_gas_oil_emission.csv` | Monthly | Semicolon-delimited, `dd.mm.yyyy` dates |
| Geological | `Fossil Fuel/Geological_emission.txt` | Constant | 21.1 Tg/yr (÷12 for monthly) |

---

## Analysis Pipeline

The script `analysis.py` performs three tasks:

### Task 1 — Emission Plots

For each of the three source groups, a two-panel figure is generated:
- **Top panel:** Stacked area chart showing all subcategories
- **Bottom panel:** Individual line plots for each subcategory
- **Combined:** An overview plot comparing total emissions across all three groups

### Task 2 — Monte Carlo Isotope Calculation

For each month in the overlapping time period:

1. Each subcategory's isotope value is sampled from a **truncated-normal distribution** (μ ± σ, clipped at ±3σ), drawn from literature values
2. The group-level isotope signature is calculated as the **emission-weighted mean**:

$$\delta_{\text{group}} = \frac{\sum_{i} E_i \cdot \delta_i}{\sum_{i} E_i}$$

where $E_i$ is the emission of subcategory $i$ and $\delta_i$ is its sampled isotope value.

3. This is repeated **10,000 times** per month to build uncertainty distributions
4. Statistics extracted: median, mean, 25th percentile (Q1), 75th percentile (Q3), standard deviation

### Task 3 — Output

- **Plots:** Median line with IQR (25th–75th percentile) shading for both δ¹³C and δD
- **CSVs:** Full monthly time series with all statistics
- Publication-quality styling via [SciencePlots](https://github.com/garrettj403/SciencePlots)

---

## Isotope Source Signatures

All values are derived from peer-reviewed literature (see [`references/ISOTOPE_VALUES.md`](references/ISOTOPE_VALUES.md) for detailed citations per category).

### Microbial Sources

| Category | δ¹³C (‰ VPDB) | δD (‰ VSMOW) | Key Reference |
|----------|----------------|---------------|---------------|
| Landfill | −56.0 ± 4.9 | −297 ± 6 | Sherwood et al. (2017); Douglas et al. (2021) |
| Livestock | −63.8 ± 2.4 | −308 ± 28 | Singh et al. (2026); Chang et al. (2019) |
| Manure | −50.0 ± 5.0 | −308 ± 28 | Arndt et al. (2022) |
| Rice Paddies | −62.2 ± 3.9 | −323 ± 20 | Sherwood et al. (2017) |
| Wastewater | −52.0 ± 6.0 | −297 ± 20 | Menoud et al. (2022) |
| Wetland | −63.9 ± 3.3 | −310 ± 25 | Douglas et al. (2021) — flux-weighted |

### Biomass Burning Sources

| Category | δ¹³C (‰ VPDB) | δD (‰ VSMOW) | Key Reference |
|----------|----------------|---------------|---------------|
| Wildfire | −26.2 ± 4.8 | −211 ± 30 | Sherwood et al. (2017) |
| Biofuel Burning | −25.0 ± 5.0 | −220 ± 35 | Thanwerdas et al. (2025) |

### Fossil Fuel Sources

| Category | δ¹³C (‰ VPDB) | δD (‰ VSMOW) | Key Reference |
|----------|----------------|---------------|---------------|
| Oil | −44.0 ± 10.7 | −194 ± 50 | Sherwood et al. (2017) |
| Natural Gas | −44.0 ± 10.7 | −194 ± 50 | Sherwood et al. (2017) |
| Coal | −49.5 ± 11.2 | −210 ± 50 | Sherwood et al. (2017); Menoud et al. (2022) |
| Geological | −49.0 ± 10.0 | −189 ± 44 | Etiope et al. (2019); Douglas et al. (2021) |

---

## Key Results

### Emission-Weighted Group Signatures

| Group | δ¹³C Median (‰) | δ¹³C IQR Width (‰) | δD Median (‰) | δD IQR Width (‰) |
|-------|------------------|---------------------|----------------|-------------------|
| **Microbial** | −61.5 | 2.4 | −308 | 18.5 |
| **Biomass Burning** | −25.8 | 4.8 | −214 | 30.9 |
| **Fossil Fuel** | −46.3 | 7.4 | −198 | 33.8 |

### Interpretation

- **δ¹³C alone** separates Biomass Burning (−26‰) from the other two groups, but Microbial (−62‰) and Fossil Fuel (−46‰) have overlapping tails
- **δD adds discrimination:** Microbial is most D-depleted (−308‰) vs Fossil Fuel (−198‰) and Biomass Burning (−214‰)
- **Dual-isotope space** (δ¹³C vs δD) provides clear separation of all three groups
- **Seasonality** is driven primarily by microbial sources (rice + wetland peak in boreal summer)
- **Fossil fuel** shows a steady upward emission trend, dominated by natural gas growth
- **Microbial group** has the tightest isotope uncertainty despite being the largest emitter (~384 Tg/yr), thanks to well-constrained wetland and livestock signatures

---

## How to Run

### Requirements

```bash
pip install numpy pandas matplotlib scipy scienceplots
```

### Run

```bash
cd Methane/
python analysis.py
```

All outputs are saved to the `output/` directory.

### Output Files

| File | Description |
|------|-------------|
| `emission_Microbial.png` | Stacked area + line plot for microbial subcategories |
| `emission_Biomass_Burning.png` | Same for biomass burning |
| `emission_Fossil_Fuel.png` | Same for fossil fuel |
| `emission_all_groups.png` | Combined group comparison |
| `isotope_Microbial.png` | δ¹³C and δD time series with IQR (microbial) |
| `isotope_Biomass_Burning.png` | Same for biomass burning |
| `isotope_Fossil_Fuel.png` | Same for fossil fuel |
| `*.csv` | Corresponding numeric data for all plots |

---

## References

Full citation details and per-category justifications are in [`references/ISOTOPE_VALUES.md`](references/ISOTOPE_VALUES.md).

| # | Reference | DOI |
|---|-----------|-----|
| 1 | Sherwood, O.A., et al. (2017). Global Inventory of Gas Geochemistry Data. *ESSD*, 9, 639–656. | [10.5194/essd-9-639-2017](https://doi.org/10.5194/essd-9-639-2017) |
| 2 | Douglas, P.M.J., et al. (2021). Geographic variability in freshwater methane δ²H. *Biogeosciences*, 18, 3505–3527. | [10.5194/bg-18-3505-2021](https://doi.org/10.5194/bg-18-3505-2021) |
| 3 | Etiope, G., et al. (2019). Gridded maps of geological methane emissions. *ESSD*, 11, 1–22. | [10.5194/essd-11-1-2019](https://doi.org/10.5194/essd-11-1-2019) |
| 4 | Menoud, M., et al. (2022). European Methane Isotope Database (EMID). *ESSD*, 14, 4365–4386. | [10.5194/essd-14-4365-2022](https://doi.org/10.5194/essd-14-4365-2022) |
| 5 | Lan, X., et al. (2021). Improved constraints on global methane emissions using δ¹³C-CH₄. *GBC*, 35, e2021GB007000. | [10.1029/2021GB007000](https://doi.org/10.1029/2021GB007000) |
| 6 | Singh, D., et al. (2026, preprint). Dual-isotopic signatures of methane sources in South Asia. *EGUsphere*. | [10.5194/egusphere-2026-411](https://doi.org/10.5194/egusphere-2026-411) |
| 7 | Thanwerdas, J., et al. (2025, preprint). Global dataset of δ¹³C-CH₄ source signatures. *ESSD Preprints*. | [10.5194/essd-2025-668](https://doi.org/10.5194/essd-2025-668) |

---

## License

Data and analysis scripts in this repository are for research purposes.
