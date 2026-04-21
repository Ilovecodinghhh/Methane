# Updated Methane Isotope Source Signatures

> **Compiled:** April 2026  
> **Method:** Literature synthesis from 7 major databases and review papers  
> **Distribution:** Truncated-normal (mean ± σ) replaces uniform ranges  

---

## Reference Publications

| # | Citation | DOI | Focus |
|---|---------|-----|-------|
| [1] | Sherwood, O.A., Schwietzke, S., Arling, V.A., Etiope, G. (2017). Global Inventory of Gas Geochemistry Data from Fossil Fuel, Microbial and Burning Sources, version 2017. *Earth Syst. Sci. Data*, 9, 639–656. | 10.5194/essd-9-639-2017 | Comprehensive global database (10,706 samples, 190 refs) |
| [2] | Douglas, P.M.J., et al. (2021). Global freshwater δ²H–CH₄ and its constraints on the global methane budget. *Biogeosciences*, 18, 3505–3527. | 10.5194/bg-18-3505-2021 | Latitudinally resolved δ²H; Monte Carlo flux-weighted assessment |
| [3] | Etiope, G., Ciotoli, G., Schwietzke, S., Schoell, M. (2019). Gridded maps of geological methane emissions and their isotopic signature. *Earth Syst. Sci. Data*, 11, 1–22. | 10.5194/essd-11-1-2019 | Geological seepage δ¹³C gridded maps |
| [4] | Menoud, M., et al. (2022). New contributions to the European Methane Isotope Database (EMID). *Earth Syst. Sci. Data*, 14, 4365–4386. | 10.5194/essd-14-4365-2022 | European source signatures, coal mine & waste measurements |
| [5] | Lan, X., et al. (2021). Improved constraints on global methane emissions and sinks using δ¹³C-CH₄. *Global Biogeochem. Cycles*, 35, e2021GB007000. | 10.1029/2021GB007000 | Gridded δ¹³C maps, inversion-optimised signatures |
| [6] | Singh, D., et al. (2026, preprint). Distinct dual-isotopic signatures of major methane sources in South Asia. *EGUsphere*. | 10.5194/egusphere-2026-411 | South Asian + global compiled dual-isotope (δ¹³C & δ²H) |
| [7] | Thanwerdas, J., et al. (2025, preprint). A global dataset of δ¹³C-CH₄ source signatures and associated uncertainties. *ESSD Preprints*. | 10.5194/essd-2025-668 | Gridded uncertainty propagation framework |

**Supplementary references (used within the primary papers):**

| Citation | Relevance |
|----------|-----------|
| Chang, J., et al. (2019). Revisiting enteric methane emissions from domestic ruminants. *Nat. Commun.*, 10, 3420. | C3/C4 diet-weighted ruminant δ¹³C |
| Ganesan, A.L., et al. (2018). Spatially resolved isotopic source signatures of wetland methane. *Geophys. Res. Lett.*, 45, 3737–3745. | Wetland δ¹³C spatial variability |
| Milkov, A.V., Etiope, G. (2018). Revised genetic diagrams for natural gases. *Org. Geochem.*, 125, 109–120. | Thermogenic vs microbial classification |
| Arndt, C., et al. (2022). Dairy farm δ¹³C signatures. *J. Geophys. Res. Biogeosci.*, 127, e2021JG006675. | Enteric vs manure isotope separation |
| Schwietzke, S., et al. (2016). Upward revision of global fossil fuel methane emissions. *Nature*, 538, 88–91. | Production-weighted fossil fuel δ¹³C |

---

## 1. MICROBIAL SOURCES

### 1.1 Landfill
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −56.0 | 4.9 | 56* | [1] Table 5 ("waste" = landfill + wastewater); [2] Table 1 |
| δ²H | −297 | 6 | 23* | [2] Table 1 ("landfills and waste") |

*Notes:* Sherwood [1] and Douglas [2] lump landfill and wastewater as "waste". The δ¹³C = −56.0‰ is the unweighted mean of 56 measurements. Douglas [2] reports a very tight δ²H uncertainty (σ = 6‰), suggesting consistent values across sites. EMID [4] European landfill data are broadly consistent.

### 1.2 Livestock (Enteric Fermentation)
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −63.8 | 2.4 | 171+ | [6] global C3/C4 biomass-weighted (70%/30%); confirmed by Chang et al. (2019): −64.9 [−67.7, −62.2]‰ |
| δ²H | −311 | 46 | 79+ | [6] global mean; [2] Table 1: −308 ± 28‰ |

*Notes:* The δ¹³C depends strongly on C3 vs C4 diet. Pure C3-fed cattle: ~−67‰; C4-dominant (tropical): ~−55 to −57‰ (Brownlow et al. 2017; Nisbet et al. 2022). The C3/C4-weighted global mean of −63.8‰ [6] is the best current estimate. δ²H shows no clear C3/C4 dependence but large variability (σ = 46‰ from [6], or 28‰ from [2]). We adopt σ = 28‰ from Douglas [2] as the flux-weighted assessment, which is more appropriate for budget work.

### 1.3 Manure
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −50.0 | 5.0 | ~20 | Arndt et al. (2022): manure lagoon δ¹³C = −49.5 to −40.5‰ (enriched ~14‰ vs enteric) |
| δ²H | −308 | 28 | — | [2] Table 1 (lumped with enteric as "enteric + manure"); no separate δ²H data for manure alone |

*Notes:* Manure CH₄ is isotopically **distinct** from enteric fermentation — δ¹³C is consistently ~14 ± 2‰ more enriched (heavier) than enteric at the same farm (Arndt et al. 2022). This is because manure decomposition involves acetoclastic methanogenesis in an open system, whereas rumen methanogenesis uses CO₂ reduction. Few studies report δ²H for manure separately; we use the combined enteric+manure value from [2] as a proxy.

### 1.4 Rice Paddies
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −62.2 | 3.9 | 253 | [1] Table 5; [5] uses similar gridded values |
| δ²H | −323 | 20 | 139 | [1] Table 5: mean = −323‰; [2] Table 1: −324 ± 8‰ for tropical rice |

*Notes:* Rice paddy δ¹³C is relatively well-constrained (σ = 3.9‰) with measurements dominantly from Asia. δ²H from Douglas [2] specifically for tropical rice (<30°N) is −324 ± 8‰, very consistent with Sherwood's global mean. We adopt σ = 20‰ (wider than Douglas's tropical estimate) to account for global variability including subtropical and temperate paddies.

### 1.5 Wastewater
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −52.0 | 6.0 | — | Estimated from [1] "waste" category and [4] EMID European wastewater data |
| δ²H | −297 | 20 | — | [2] Table 1 ("landfills and waste"); inflated σ for wastewater-only |

*Notes:* Wastewater is rarely measured separately from landfill in isotope databases. EMID [4] European measurements and urban studies (Bucharest, Ho Chi Minh City) suggest wastewater δ¹³C may be slightly more enriched than landfill. We estimate −52.0‰ as an intermediate value. The δ²H uncertainty is inflated from Douglas's σ = 6‰ to σ = 20‰ to reflect the scarcity of wastewater-specific measurements.

### 1.6 Wetland
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −63.9 | 3.3 | 556 | [2] flux-weighted global mean; [1] Table 5: −61.5 ± 5.4‰ (unweighted) |
| δ²H | −310 | 25 | 173 | [2] flux-weighted global mean |

*Notes:* Wetland isotope signatures show strong **latitudinal dependence** [2]:
- Tropical (<30°N): δ¹³C = −64.4 ± 1.9‰, δ²H = −301 ± 15‰
- Temperate (30–60°N): δ¹³C = −61.8 ± 2.6‰, δ²H = −324 ± 14‰
- Boreal (>60°N): δ¹³C = −62.7 ± 3.0‰, δ²H = −374 ± 10‰

The flux-weighted mean (−63.9‰) is dominated by tropical wetlands (~115 Tg/yr of 149 Tg/yr total). The old range of −73.6 to −18.2‰ was far too wide — the actual flux-weighted σ is only 3.3‰ [2]. Caveat: C4-dominated wetlands are underrepresented, which may bias δ¹³C low [2].

---

## 2. BIOMASS BURNING SOURCES

### 2.1 Wildfire
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −26.2 | 4.8 | 907 | [1] Table 5 (all biomass burning); [7] gridded maps |
| δ²H | −211 | 30 | 4 | [1] Table 5 (n = 4 only); estimated σ |

*Notes:* The δ¹³C bimodality reflects C3 (forests: ~ −28‰) vs C4 (savannas: ~ −16 to −12‰) vegetation. The mean of −26.2‰ is appropriate for the global mix. Senegal C3 fires: −28.5 ± 0.8‰; African C4 savanna fires: ~ −18‰ (Fisher et al. 2020). **δ²H is very poorly constrained** (only 4 measurements globally in [1]). The σ = 30‰ is a conservative estimate.

### 2.2 Biofuel Burning
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −25.0 | 5.0 | — | [7] notes biofuel burning has higher sub-sector uncertainty than wildfire; [1] uses same BB category |
| δ²H | −220 | 35 | — | Estimated; no separate biofuel δ²H measurements in literature |

*Notes:* Biofuel burning (crop residues, dung cakes, wood fuel) has similar δ¹³C to wildfire but potentially more variable due to diverse fuel types. Thanwerdas et al. [7] identifies biofuel as the main driver of BB sector uncertainty. The δ²H is even less constrained than wildfire — we assign σ = 35‰.

---

## 3. FOSSIL FUEL SOURCES

### 3.1 Oil (Oil-associated gas)
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −44.0 | 10.7 | 6079* | [1] Table 5 ("conventional oil & gas"); [5] production-weighted gridded maps |
| δ²H | −194 | 50 | 1969* | [1] Table 5 |

*Notes:* Sherwood [1] combines conventional oil-associated and natural gas (n = 6,079 for δ¹³C). The δ¹³C distribution is left-skewed due to microbial and low-maturity thermogenic gas (e.g., West Siberia Basin: −51.8‰ [1]). Schwietzke et al. (2016) derived a production-weighted fossil fuel δ¹³C of −44‰. Cannot separate oil from gas isotopically in the database — they are geologically co-produced.

### 3.2 Natural Gas
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −44.0 | 10.7 | 6079* | [1] Table 5 (same pool as oil) |
| δ²H | −194 | 50 | 1969* | [1] Table 5 |

*Notes:* Same as oil (see §3.1). Shale gas is distinct: δ¹³C = −42.5 ± 6.7‰, δ²H = −167 ± ?‰ [1] (more enriched in both isotopes). If your emission inventory separates conventional from shale gas, use the shale-specific values.

### 3.3 Coal
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −49.5 | 11.2 | 1402 | [1] Table 5 |
| δ²H | −210 | 50 | 511 | [1] Table 5: mean = −232‰; [4] Silesian coal mines: −184 ± 32‰; compromise estimate |

*Notes:* Coal CH₄ is **bimodal** — roughly evenly split between thermogenic (δ¹³C ~ −40 to −30‰, δ²H ~ −180 to −150‰) and microbial (δ¹³C ~ −59 to −80‰, δ²H ~ −310‰ e.g. Powder River Basin) origins [1]. A single Gaussian is a poor representation. The Menoud [4] EMID Silesian coal data (δ¹³C = −49.8 ± 5.7‰, δ²H = −184 ± 32‰) reflects predominantly thermogenic European coal. The global mean from [1] (δ²H = −232‰) includes microbial coal. We use −210‰ as a compromise.

### 3.4 Geological Seepage
| Isotope | Mean (‰) | σ (‰) | N | Primary source |
|---------|----------|-------|---|---------------|
| δ¹³C | −49.0 | 10.0 | 1000+ | [3] emission-weighted global mean: −49‰ (onshore seeps: −46.6‰, submarine: −59‰, microseepage: −51.4‰, geothermal: −30.6‰) |
| δ²H | −189 | 44 | — | [2] Table 1 ("geological onshore") |

*Notes:* Etiope et al. [3] showed the geological δ¹³C is **much lighter** than previously assumed (−38‰ in older studies → −49‰ updated). This is because geological seepage includes substantial microbial gas from sedimentary basins, not just thermogenic gas. The δ²H = −189 ± 44‰ from [2] has very large uncertainty.

---

## 4. Summary Comparison: Old vs Updated

| Category | Old δ¹³C range | **New δ¹³C (mean ± σ)** | Old δ²H range | **New δ²H (mean ± σ)** |
|----------|----------------|--------------------------|----------------|--------------------------|
| Landfill | −60 to −40 | **−56.0 ± 4.9** | −350 to −250 | **−297 ± 6** |
| Livestock | −67.8 to −54.6 | **−63.8 ± 2.4** | −360 to −150 | **−308 ± 28** |
| Manure | −65 to −45 | **−50.0 ± 5.0** | −350 to −300 | **−308 ± 28** |
| Rice | −70 to −55 | **−62.2 ± 3.9** | −390 to −320 | **−323 ± 20** |
| Wastewater | −60 to −45 | **−52.0 ± 6.0** | −360 to −300 | **−297 ± 20** |
| Wetland | −73.6 to −18.2 | **−63.9 ± 3.3** | −400 to −300 | **−310 ± 25** |
| Wildfire | −26.7 to −12.6 | **−26.2 ± 4.8** | −260 to −170 | **−211 ± 30** |
| Biofuel | −26.7 to −12.6 | **−25.0 ± 5.0** | −270 to −190 | **−220 ± 35** |
| Oil | −65.0 to −29.1 | **−44.0 ± 10.7** | −250 to −120 | **−194 ± 50** |
| Gas | −65.0 to −29.1 | **−44.0 ± 10.7** | −250 to −100 | **−194 ± 50** |
| Coal | −64.1 to −30.8 | **−49.5 ± 11.2** | −240 to −110 | **−210 ± 50** |
| Geological | −68.0 to −24.3 | **−49.0 ± 10.0** | −300 to −100 | **−189 ± 44** |

### Key changes from old values:
1. **Wetland δ¹³C dramatically narrowed**: old range 55.4‰ wide → new σ = 3.3‰. This is the single largest improvement, driven by Douglas et al. [2] flux-weighted analysis.
2. **Livestock δ²H tightened**: old range 210‰ wide → new σ = 28‰. The old range was unrealistically broad.
3. **Manure δ¹³C shifted heavier**: −50‰ vs old midpoint of −55‰. Manure is isotopically distinct from enteric fermentation.
4. **Geological δ¹³C revised lighter**: −49‰ vs old assumptions of −38‰ (Etiope 2019 [3]).
5. **Landfill δ²H much tighter**: old range 100‰ → new σ = 6‰. Very well constrained.

---

## 5. Monte Carlo Implementation Notes

**Distribution:** Truncated Normal(μ, σ), truncated at ±3σ.

**Rationale (Suggestion 5 from v1 analysis):**  
- Uniform distributions assume maximum ignorance — every value in the range is equally likely.  
- The literature provides mean ± SD, indicating measurements cluster around the mean.  
- Truncated-normal concentrates 50% of probability within the IQR (μ ± 0.67σ), yielding tighter and more realistic uncertainty bands.  
- The truncation at ±3σ prevents unphysical tails while preserving >99.7% of the distribution.

**Caveat:** Coal CH₄ is genuinely bimodal (thermogenic + microbial). A single Gaussian is a simplification. A mixture model would be more appropriate but requires specifying the mixing fraction, which varies by region.
