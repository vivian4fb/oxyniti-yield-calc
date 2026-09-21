# Oxyniti yield & profit calculator — Tamil Nadu ponds

A standalone static web tool that estimates the **extra saleable kilograms, the extra net profit
and the payback period** an OXY-Nano nano-bubble generator could deliver on one pond in one Tamil
Nadu district — and shows *why* the answer changes with species, season, stocking density and
district.

No build step, no framework, no npm. Open `index.html` and it runs.

*Built 2026-09-21. Integration and QA verified 2026-09-21 — see `../plan/QA_REPORT.md`.*

---

## What this tool is — and what it is not

**It is** a transparent, sourced estimator. Every number it shows carries a value, a unit, a status
(`VERIFIED` / `ASSUMED` / `UNTESTED` / `NOT_FOUND`), a date and a source, all listed in the
Assumptions panel on the page.

**It is not:**

- **Not a guarantee.** It is an illustration built on published coefficients and monthly climate
  normals, not a measurement of your pond.
- **Capped at +18 % extra saleable kilograms.** That ceiling is the internal Oxyniti model
  (+12 % growth and +5 percentage points survival at a typical 85 % baseline survival:
  1.12 × 0.90 / 0.85 = 1.186, clamped to 1.18). The calculator can never print more than that,
  and it reaches the cap only for a pond that is fully oxygen-limited in every crop month. This
  **supersedes** the 20–30 % flat slider still on the live oxyniti.com homepage; the supersession
  is logged in `../plan/DEVIATIONS.md`.
- **Not tuned to flatter the product.** At the oxygen input the product pages actually publish
  (2 L/min for the 1.5 HP unit), the default Tiruchirappalli GIFT-tilapia scenario returns a
  **negative** annual profit and blocks payback with the warning
  `NO_PAYBACK_AT_PUBLISHED_O2`. That result is correct arithmetic on the published figure and is
  left visible on purpose. It is the single strongest argument for getting the OEM datasheet
  oxygen delivery — see "What the owner still has to supply" below.
- **Not a substitute for a demo.** One measured DO reading from the farmer's own pond outranks
  every published range in here.

### Known limitations (also stated on the page)

- Monthly climate normals (IMD 1991–2020), not this year's weather.
- Linear growth and linear mortality through the crop; no disease, water-exchange or algal-crash
  model.
- The uplift is calibrated to an internal conservative model, not measured on the farmer's pond.
- Prices are the sourced range on the sourcing date; the farmer's own price overrides them.

---

## Running it locally

Either works. A server is only needed for the optional `?fixture=1` development path, which uses
`fetch`.

```sh
# 1. From a local server (recommended — map tiles and everything else behave normally)
cd site
python -m http.server 8765
#   then open http://127.0.0.1:8765/index.html

# 2. Straight from disk, with no server at all
#   open site/index.html in a browser
```

The data files are classic scripts that assign onto `window.OXY_DATA`, so the `file://` path
renders the full result — verified in QA at 1280 px with zero console errors.

**Map tiles and the Referer header (verified 2026-09-21).** OpenStreetMap's tile usage policy
requires every request to carry an HTTP `Referer`; without one the server answers HTTP 200 with
a 7 kB "Access blocked" image instead of the 30 kB tile. Browsers send no Referer for a page
opened from disk, so a `file://` open would show blocked tiles. `js/map.js` therefore uses
Esri's World Street Map tiles when the page runs from `file://`, and on `http(s)` it probes one
OSM tile and switches to the same fallback if the block image comes back. The page sets
`<meta name="referrer" content="strict-origin-when-cross-origin">` so the published site always
identifies itself to OSM. The district polygons and hotspots do not depend on tiles at all.

Query-string switches: `?theme=light` or `?theme=dark` pins the theme for that load;
`?fixture=1` loads a stored sample result instead of the live model (needs a server).

## Running the tests

```sh
# JS model — Node 22 built-in runner, no npm. Note the glob: `node --test tests/` does not work
# on this Node build.
node --test tests/*.test.mjs

# JS-vs-Python parity against the independent oracle (MODEL_SPEC.md section 8 test 6)
python tests/compare.py

# the comparator's own self-test: injects a defect into a copy of the oracle and must report FAIL
python tests/compare.py --self-test

# dissolved-oxygen saturation against the published verification table only
python tests/compare.py --doonly
```

All four green is the release gate. Set `PYTHONIOENCODING=utf-8` if your console is not already
UTF-8, since the scenarios carry Tamil species names.

---

## The model in five sentences

1. Each district is mapped to its nearest IMD climate station, and each month's mean air
   temperature is converted to pond water temperature by a published shallow-pond regression.
2. A trapezoid on the species' tolerable and optimum temperature limits gives a monthly
   growth-suitability score, whose crop average — relative to the same species stocked in its
   default month at Tiruchirappalli — scales the published harvest size up or down.
3. For each crop month the pond's dusk dissolved oxygen (Benson & Krause 1984 saturation, times a
   bloom factor) is drawn down overnight by fish, plankton and sediment respiration and topped up
   by any existing aeration and diffusion, giving the dawn oxygen the stock actually experiences,
   and hence an oxygen-stress index between the species' growth threshold and its lethal limit.
4. The nano-bubble unit adds oxygen strictly by mass balance from its published litres-per-minute
   rating, purity and dissolved fraction, so the crop-mean **relief** it achieves — not an assumed
   percentage — drives the uplift, which is converted to extra growth and extra survival and
   clamped at the +18 % ceiling.
5. Extra harvest at the farm-gate price, less the extra feed and the extra electricity (including
   the tariff's fixed charge), gives the extra profit per crop and per year, and payback divides
   the capital cost less subsidy by that annual figure — blocked whenever the unit price is
   unknown or the annual gain is not positive.

The equations, the amendments (A1–A8) and the contract tests are in
[`../plan/MODEL_SPEC.md`](../plan/MODEL_SPEC.md). Deviations from earlier published claims are
logged in [`../plan/DEVIATIONS.md`](../plan/DEVIATIONS.md); per-field data provenance is in
[`../plan/DATA_STATUS.md`](../plan/DATA_STATUS.md).

---

## Data sources and licences

| Data | Source | Licence / terms |
|---|---|---|
| District boundaries (38 polygons) | **geoBoundaries gbOpen IND ADM2**, boundaryID `IND-ADM2-76128533`, boundaryYearRepresented 2021, commit `9469f09`; upstream Pathways Data Pvt. Ltd. / lgdirectory.gov.in. <https://www.geoboundaries.org/api/current/gbOpen/IND/ADM2/> | **Open Data Commons Open Database License 1.0 (ODbL)**, as stated by the geoBoundaries API for this layer. Attribution to geoBoundaries **and** the upstream source is required, and the **share-alike** term applies to the boundary data and to any derived database. The geometry is shipped unsimplified: per-ring Douglas–Peucker opens slivers along shared district edges. |
| Base map tiles | OpenStreetMap, <https://www.openstreetmap.org/copyright> | © OpenStreetMap contributors, ODbL. Attribution is rendered on the map and must stay. |
| Monthly climate normals (32 stations, 1991–2020) | IMD Pune, *Climatological Tables of Observatories in India 1991–2020* (9th ed., 2022). <https://www.imdpune.gov.in/library/public/Climatological%20Tables%201991-2020.pdf> | Government of India publication; cited in full. |
| District inland fish production | DES, *Statistical Hand Book of Tamil Nadu 2021-22*, Tables 8.2 and 8.3. <https://www.tn.gov.in/deptst/fisheries.pdf> | Government of Tamil Nadu publication. No official district table after 2021-22 exists. |
| CAA-registered farms, seed farms, hatcheries | TN Fisheries *Policy Note 2025-26*, Tables 4, 7 and 8. <https://cms.tn.gov.in/cms_migrated/document/docfiles/fisheries_e_pn_2025_26.pdf> | Government of Tamil Nadu publication. Public facilities only — no private farms and no contacts. |
| Agro-climatic zones | TNAU seven-zone classification. <https://agritech.tnau.ac.in/agriculture/agri_soilresource_agroclimate.html> | TNAU publication. |
| Crop costs, yields, survival, FCR | NABARD / TNAU 2015 model projects (GIFT tilapia, pangasius, intensive fish culture, vannamei, composite carp), e.g. <https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/6.GIFT_Tilapia_culture_15.pdf> | Public model projects. **2015 vintage — status ASSUMED.** The page says "2015 model costs — replace with your own". |
| Electricity tariff | TNERC tariff orders, LT III-A(1) (₹4.80 / ₹6.95 per kWh, ₹75/kW/month fixed) and LT IV allied-agriculture supply, effective 2025-07-01. <https://www.tnerc.tn.gov.in/Orders/files/TO-Order%20No6300620252131.pdf> | Regulatory order. Slab treatment is UNTESTED. |
| Subsidy rates | PMMSY, <https://static.pib.gov.in/WriteReadData/userfiles/PMMSY%20BookEnglish.pdf> | Whether an aerator qualifies under "inputs" is **NOT_FOUND**, so the 40 % / 60 % options are labelled UNTESTED. |
| Oxygen saturation | Benson & Krause (1984), coefficients as used by USGS DOTABLES. <https://water.usgs.gov/water-resources/software/DOTABLES/> | Published method; the page reproduces the USGS table to 0.0005 mg/L. |
| Night oxygen budget, respiration rates, DO–growth thresholds | Boyd (pond dynamics); Romaire, Boyd & Collis 1978; Leonard & Skov 2022 (tilapia SMR); Bett & Vinatea 2009 and Kir et al. 2023 (vannamei); see `../research/do_physics.md`. | Peer-reviewed; per-coefficient statuses in `../plan/coefficients.json`. |
| Uplift evidence | Mauladani et al. 2020 (vannamei, +19.7 % harvest, survival 75 → 92 %, FCR 1.4 → 1.3, **n = 1 pond per arm**); Rahmawati et al. 2021 (vannamei raceway); Gymnastiar et al. 2025 (tilapia biofloc, +18.8 % final weight); Tran-Duy et al. 2008 (Nile tilapia, DO 3.0 → 5.6 mg/L, growth +41 %); Boyd & Hanson 2010 (shrimp, survival 42 → 61 %, yield +34 %); Nghia et al. 2022 and Xu et al. 2022 (no growth gain reported). Full table with designs and statuses in `../research/economics_device_evidence.md` section 7. | Peer-reviewed. The +12 % / +5 point calibration sits **below** every positive trial found, which is the point of the ceiling. |
| Product specifications and claims | oxyniti.com product pages — 1.5 HP "up to 2 L/min" and 4 HP "up to 6 L/min" oxygen input. <https://www.oxyniti.com/product/nano-bubble-generator-1.5-HP> | Publisher's own pages, read 2026-09-21. The OXY-Nano 3 and 5 named in the homepage video have no product page (NOT_FOUND) and are **not** offered by this tool. |

Leaflet 1.9.4 is vendored in `vendor/leaflet/` under its BSD-2-Clause licence.

No farm, contact, measurement or price in this tool is invented. Hotspots are district-level
statistics and named public facilities only.

---

## Rebuilding the data

`site/data/*.data.js` is generated — never hand-edit it. Edit the files in `research/` or
`plan/coefficients.json`, then:

```sh
python tools/build_data.py
```

The script is deterministic and idempotent: it validates every load-bearing field against the
envelope shape, applies the documented fallbacks (each one labelled ASSUMED with its rule), maps
all 38 districts to a climate station, and rewrites `plan/DATA_STATUS.md` with the per-field
VERIFIED / ASSUMED / NOT_FOUND counts. Re-run the tests afterwards.

Seven of the eighteen species are **estimable** — catla, rohu, mrigal, GIFT tilapia, pangasius,
murrel and vannamei. The other eleven are listed in the species panel with their sourced
parameters and the exact fields that are missing; asking the model for an estimate on one of them
raises `MissingDataError` naming that field.

---

## ASSUMED coefficients

Every coefficient below is a **judgement, not a measurement** — 56 of the 69 entries in
`../plan/coefficients.json` (11 are VERIFIED, 2 UNTESTED). All are shown in the page's Assumptions
panel with their sources. Dated 2026-09-21 unless the source says otherwise.

| Coefficient | Value | Unit | Source (abridged) |
|---|---|---|---|
| `do_saturation.pressure_from_elevation` | P_atm = exp(-9.80665 * 0.0289644 * z_m / (8.31447 * 288.15)) | — | research/do_physics.md (a): standard atmosphere as in LakeMetabolizer; adequate for TN lowlands, matters only for the Nilgiris... |
| `pond_temperature.a_intercept_c` | 2.32 | degC | research/tn_climate_seasons.md (d): Bangladesh nursery-pond regression water = 0.922*air + 2.32, r = 0.976 (VERIFIED regression... |
| `pond_temperature.b_slope` | 0.922 | degC per degC | same regression |
| `night_budget.h_night` | 11.5 | h | Tamil Nadu dusk (~18:30) to dawn (~06:00); do_physics.md worked example uses 11 h |
| `night_budget.f_dusk` | 1.2 | fraction of saturation at dusk | research/do_physics.md (d): Boyd worked example, dusk at 120 % saturation in a green pond |
| `night_budget.d_diff_mg_l_per_night` | 0.5 | mg/L per night, applied only while DO < saturation | research/do_physics.md (d): diffusion from air 'seldom exceeds 1 mg/L during a single night' (Boyd); half taken |
| `night_budget.r_plankton_ref_mg_l_h_at_25c` | (table) | mg/L/h at 25 degC, by bloom density input | research/do_physics.md (d): k_p 0.1-0.5 mg/L/h at 25 degC from Secchi depth / chlorophyll (Boyd); plankton is 75-80 % of night... |
| `night_budget.q10_plankton` | 2.0 | - | generic biological Q10; do_physics.md (d) |
| `night_budget.k_sed_g_o2_m2_h` | 0.15 | g O2/m^2/h; R_sed = k_sed / depth_m | research/do_physics.md (d): k_s 0.02-0.4 g O2/m^2/h (Boyd's <1 to 10 mg/L/day band) |
| `night_budget.q10_sed` | 2.0 | - | generic biological Q10 |
| `night_budget.t_ref_c` | 25 | degC | reference temperature for the plankton and sediment terms |
| `respiration_groups.freshwater_fish.q_ref_mg_o2_kg_h` | 300 | mg O2/kg/h at 30 degC, routine fed rate | research/do_physics.md (b): tilapia SMR 170-200 mg O2/kg/h at 30-32 degC (Leonard & Skov 2022, interpolated); routine fed rates... |
| `respiration_groups.freshwater_fish.t_ref_c` | 30 | degC | do_physics.md (b) model form |
| `respiration_groups.freshwater_fish.t_cap_c` | 32 | degC | do_physics.md (b): cap the temperature term at the species' upper optimum (tilapia 32 degC) |
| `respiration_groups.air_breathing_fish.q_ref_mg_o2_kg_h` | 200 | mg O2/kg/h at 30 degC taken from the water | pangasius and murrel take part of their oxygen from air; water-column demand set at two thirds of the freshwater-fish value; no... |
| `respiration_groups.air_breathing_fish.q10` | 2.0 | - | generic; no measured value found |
| `respiration_groups.air_breathing_fish.t_ref_c` | 30 | degC | as above |
| `respiration_groups.air_breathing_fish.t_cap_c` | 32 | degC | as above |
| `respiration_groups.shrimp.q_ref_mg_o2_kg_h` | 450 | mg O2/kg/h at 30 degC | research/do_physics.md (b): L. vannamei juveniles specific consumption rises 20 -> 30 degC (Bett & Vinatea 2009, coefficients n... |
| `respiration_groups.shrimp.q10` | 2.0 | - | do_physics.md (b) verdict: use Q10 = 2 up to 30 degC and hold flat above; no verified vannamei Q10 |
| `respiration_groups.shrimp.t_ref_c` | 30 | degC | as above |
| `respiration_groups.shrimp.t_cap_c` | 30 | degC | Kir et al. 2023: standard metabolism falls with temperature within 25-30 degC; held flat above 30 |
| `respiration_groups.brackish_fish.q_ref_mg_o2_kg_h` | 300 | mg O2/kg/h at 30 degC | freshwater-fish value reused; no seabass/milkfish/mullet measurement found (NOT_FOUND) |
| `respiration_groups.brackish_fish.q10` | 1.9 | - | freshwater-fish value reused |
| `respiration_groups.brackish_fish.t_ref_c` | 30 | degC | as above |
| `respiration_groups.brackish_fish.t_cap_c` | 32 | degC | as above |
| `respiration_groups.crab.q_ref_mg_o2_kg_h` | 150 | mg O2/kg/h at 30 degC | mud crab metabolic rate is lower than fish and partly aerial; no measurement found (NOT_FOUND) |
| `respiration_groups.crab.q10` | 2.0 | - | generic |
| `respiration_groups.crab.t_ref_c` | 30 | degC | as above |
| `respiration_groups.crab.t_cap_c` | 32 | degC | as above |
| `species_group_defaults.freshwater_fish.do_min_growth_mg_l` | 3.0 | mg/L | research/do_physics.md (c): feed intake plateau at 3.0 mg/L for tilapia <100 g, catfish, carp proxy |
| `species_group_defaults.freshwater_fish.do_lethal_mg_l` | 1.0 | mg/L | do_physics.md (c): f = 0 below 1.0 with mortality risk; common carp verified 0.3-0.5 (species file) |
| `species_group_defaults.air_breathing_fish.do_min_growth_mg_l` | 2.0 | mg/L | air-breathers feed at lower DO; growth response to DO weakly evidenced (NOT_FOUND); set below the fish plateau |
| `species_group_defaults.air_breathing_fish.do_lethal_mg_l` | 0.5 | mg/L | pangasius survives 0.1 mg/L (species file, FAO); 0.5 taken as the practical floor for growth accounting |
| `species_group_defaults.shrimp.do_lethal_mg_l` | 1.5 | mg/L | Boyd & Hanson 2010: survival 42 % at minimum DO 2.3 mg/L; floor placed at 1.5 |
| `species_group_defaults.brackish_fish.do_min_growth_mg_l` | 4.0 | mg/L | seabass and mullet 4.0 mg/L in the species file; reused for milkfish and pearl spot where null |
| `species_group_defaults.brackish_fish.do_lethal_mg_l` | 1.0 | mg/L | milkfish verified 0.1-0.4 (species file); 1.0 taken as a conservative floor |
| `species_group_defaults.crab.do_min_growth_mg_l` | 3.0 | mg/L | no measurement found (NOT_FOUND) |
| `species_group_defaults.crab.do_lethal_mg_l` | 1.0 | mg/L | no measurement found (NOT_FOUND) |
| `uplift.growth_max_fraction` | 0.12 | fraction of harvest size at full relief | MODEL_SPEC.md 5: internal +18 % ceiling decomposed as +12 % growth and +5 points survival at 85 % baseline survival |
| `uplift.survival_points_max` | 0.05 | absolute survival fraction at full relief | as above |
| `uplift.ceiling_extra_kg_fraction` | 0.18 | fraction | NBG/.claude/SALES_OVERRIDE.md claims ceiling; docs/make_charts.py |
| `uplift.low_case_factor` | 0.5 | multiplier on the three coefficients for the low case | MODEL_SPEC.md 5 |
| `uplift.survival_cap` | 0.98 | fraction | MODEL_SPEC.md 5 |
| `oxygen_supply.rho_o2_g_per_l` | 1.31 | g/L, oxygen gas at 25 degC and 1 atm | ideal gas: 32 g/mol / 24.47 L/mol; ASSUMED to be the concentrator's rating condition |
| `oxygen_supply.purity` | 0.9 | fraction O2 in the concentrator output | typical PSA concentrator 90-93 %; OEM figure NOT_FOUND |
| `oxygen_supply.eta_dissolved` | 0.85 | fraction of injected oxygen that dissolves and stays | nano-bubbles (<200 nm) do not rise and burst; OEM transfer efficiency NOT_FOUND (economics_device_evidence.md 1) |
| `oxygen_supply.worked_check` | 1.5 HP, 2 L/min, 8 h -> 2*60*8*1.31*0.90*0.85 = 961 g O2/night; 1 acre x 1.5 m = 6.070e... | — | MODEL_SPEC.md 4.5 |
| `paddlewheel.sae_field_kg_o2_per_kwh` | 1.0 | kg O2 per kWh under field conditions | economics_device_evidence.md 4.2: Boyd/Tucker field 1.5-2.5 lb O2/hp-h = 0.9-1.5 kg O2/kWh; Indian tank test 1.02 kg O2/kWh; 1.... |
| `sizing.n_units_cap` | 20 | units | MODEL_SPEC.md 7 |
| `thermal.tolerable_fallback_margin_c` | 5 | degC beyond the optimum bound when the tolerable bound is null | EXECUTION_PLAN.md WP1 fallback 1 |
| `thermal.size_factor_clamp` | [0.5, 1.1] | - | MODEL_SPEC.md 3 |
| `seed_size_g.fish_fingerling` | 5 | g | EXECUTION_PLAN.md WP1 fallback 8; typical 3-8 g fingerlings |
| `seed_size_g.shrimp_pl` | 0.01 | g | PL10-PL15 post-larvae |
| `seed_size_g.scampi_pl` | 0.05 | g | post-larvae |
| `seed_size_g.crab_fattening_stock` | 100 | g | water crabs stocked for fattening |

The three that move the answer most are `oxygen_supply.purity`, `oxygen_supply.eta_dissolved` and
`oxygen_supply.rho_o2_g_per_l` — together they set how much oxygen one unit actually delivers, and
the OEM has not published any of them.

---

## What the owner still has to supply

These are the inputs that would change the numbers most (`../plan/EXECUTION_PLAN.md` section 7,
items 1–3):

1. **Oxygen delivery per model, in kg O₂/h or L/min at a stated purity — and the concentrator's
   power draw.** The site publishes "up to 2 L/min" (1.5 HP) and "up to 6 L/min" (4 HP). By mass
   balance that is about 0.16 mg/L per unit per 8 h night in a 1 acre × 1.5 m pond, against
   roughly 2 mg/L from a single 2 HP paddlewheel. On the published figure the tool sizes several
   units per acre and still cannot pay them back. **This is the decision that most changes the
   numbers.** The concentrator's power draw is NOT_FOUND, so it is currently excluded from the
   electricity cost and the running cost shown is a lower bound (warning
   `CONCENTRATOR_POWER_UNKNOWN`).
2. **Real list prices per model.** Both product pages show ₹4,400, which reads as a placeholder,
   so unit price is treated as unknown and **payback stays blocked until a real price is entered**.
3. **Which models actually exist.** The homepage and video say OXY-Nano 1.5 / 3 / 5 HP; the
   catalogue has 1.5 HP and 4 HP. The tool offers only the two with published product pages.

Also open: native Tamil review (the toggle reads "தமிழ் (partial)" until then — new strings fall
back to English and are deliberately not machine-translated), and any measured demo-pond data.

---

## Lead capture

The results card links to WhatsApp on **+91 96597 27477** (published on oxyniti.com, verified
2026-09-21) as `https://wa.me/919659727477?text=<encoded scenario summary>`. The summary carries
the district, species, area, density and the low–high extra profit band, so the reply can start
from the farmer's own numbers.

---

## Publishing

`deploy.ps1` copies `site/` to a repository **outside** this workspace, commits, pushes and
enables GitHub Pages. It refuses to publish if it finds a placeholder token anywhere under
`site/`. Run it yourself:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy.ps1 -DryRun   # print the steps
powershell -ExecutionPolicy Bypass -File .\deploy.ps1           # publish
```
