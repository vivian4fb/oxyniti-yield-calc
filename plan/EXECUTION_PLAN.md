# Oxyniti Yield & Profit Calculator — execution plan

*Written 2026-09-21 (Fable 5.1, research and planning). Executed by Opus 5 and Sonnet 5 agents.
Read `MODEL_SPEC.md` first; this file says who builds what, in what order, against which gate.*

## 1. Deliverable

A standalone static web tool at `site/` that runs from GitHub Pages **and** from a local
`file://` open, with no build step and no network dependency except OpenStreetMap tiles:

1. **Interactive Tamil Nadu map** (Leaflet 1.9.4, vendored) — 38 district polygons coloured by
   sourced inland fish production, hotspot markers for sourced clusters and public facilities,
   click a district to set the calculator's location.
2. **Calculator** — species, pond size, depth, density, stocking month, price, feed price,
   existing aeration, tariff, unit model, unit price, subsidy, run hours → extra harvest, extra
   profit, payback, as a low–high band; plus a 12-month seasonal strip (water temperature,
   thermal suitability, oxygen stress before/after) that explains the number.
3. **Assumptions panel** — every parameter with value, unit, status, date and source link.
4. **Lead capture** — a WhatsApp deep link to +91 96597 27477 (published on oxyniti.com,
   VERIFIED 2026-09-21 from `website/wwwroot/index.html`) carrying the scenario summary.
5. **Tests** — `node --test tests/` for the JS model; `python tests/compare.py` for JS-vs-Python
   parity with `--self-test`; both green is the gate.

Later integration into oxyniti.com (Blazor WASM on Azure Static Web Apps) is out of scope for
v1 but designed for: the model is one dependency-free classic script, the data are plain JS
data files, and Leaflet is the same version the site already vendors.

## 2. Ground rules for every agent

- Read `2_Business/CLAUDE.md` non-negotiables (quoted in `MODEL_SPEC.md` section 0). British
  English in every string the farmer sees. ₹, metric, `en-IN` number grouping.
- **Never run git anywhere under `C:\Users\vivia\Code2`.** Publishing is `deploy.ps1`, run by
  Vivian, into `C:\Users\vivia\Repos\`.
- **Fail loudly.** No default that is not in `coefficients.json` with a status label. A missing
  value throws `MissingDataError` (model) or renders as "—  not available: <reason>" (UI).
- No placeholder tokens (`TODO`, `YOUR_`, `XXXXX`, `info@`, `+91 98765`) anywhere under `site/`;
  `deploy.ps1` refuses to publish if it finds one.
- No new libraries. Leaflet is already vendored. Charts are hand-written inline SVG.
- Every file you create starts with a two-line header comment: purpose, and the spec section it
  implements.
- Do not edit files owned by another work package. Interfaces are fixed below; if one must
  change, write the change into `plan/DEVIATIONS.md` with the reason and tell the integrator.

## 3. Repository layout (fixed)

```
oxyniti_yield _calc/            (note the space in the folder name — always quote paths)
  plan/        MODEL_SPEC.md, EXECUTION_PLAN.md, DEVIATIONS.md, DATA_STATUS.md, QA_REPORT.md, coefficients.json
  research/    species_parameters.{md,json}, tn_aquaculture_geography.md, hotspots.json,
               tn_districts.geojson, climate_normals.json, tn_climate_seasons.md, do_physics.md,
               economics_device_evidence.md          (source of truth — never edited by builders)
  tools/       build_data.py                          (research → site/data, with validation)
  tests/       model.test.mjs, oracle.py, compare.py, scenarios.json, screenshots/
  site/
    index.html
    css/styles.css
    js/model.js  js/ui.js  js/charts.js  js/map.js  js/i18n.js
    data/species.data.js  climate.data.js  hotspots.data.js  tn_districts.data.js
         products.data.js  economics.data.js  coefficients.data.js
    vendor/leaflet/   assets/logo.svg  assets/logo-mark.svg  assets/favicon.svg
    README.md
  deploy.ps1
```

## 4. Fixed interfaces

### 4.1 Data files (`site/data/*.data.js`)
Classic scripts (no `import`/`export`), each assigning one property on `window.OXY_DATA`
(created if absent), so the page works from `file://`. In Node they are loaded with
`vm.runInNewContext` by the tests. Every numeric field keeps the research envelope:

```js
{ "value": 28, "unit": "degC", "status": "VERIFIED", "date": "2026-09-21", "source": "https://..." }
// ranges: "value": [low, high]
// missing: "value": null, "status": "NOT_FOUND"
```

- `species.data.js` → `OXY_DATA.species = [ { id, common_name_en, common_name_ta, scientific_name,
  water_type, salinity_ppt, temp_optimum_c, temp_tolerable_c, do_minimum_mg_l, do_lethal_mg_l,
  stocking_density_per_acre, seed_size_g, culture_period_months, harvest_size_g, survival_pct,
  fcr, farmgate_price_inr_per_kg, seed_cost_inr_per_unit, feed_cost_inr_per_kg,
  other_cost_inr_per_acre_crop, crops_per_year_tn, stocking_month_tn_default,
  respiration_group, notes } ]`
- `climate.data.js` → `OXY_DATA.climate = { stations: [...as research...], district_station_map:
  { "Tiruchirappalli": "Tiruchirappalli", ... 38 entries } }`
- `hotspots.data.js` → `OXY_DATA.hotspots = [...as research...]`
- `tn_districts.data.js` → `OXY_DATA.districts = <GeoJSON FeatureCollection>` with
  `properties.district` normalised to the 38 official names, plus `properties.inland_production_t`
  and `properties.production_year` where sourced (null otherwise).
- `products.data.js` → `OXY_DATA.products = [ { id: "nbg-1.5hp", label: "Nano Bubble Generator
  1.5 HP", url, power_hp, power_kw_shaft, o2_input_lpm, price_inr, concentrator_kw,
  concentrator_price_inr, maintenance_pct_per_year, concentrator_required: true,
  claims: [ {text, url} ] } ]` — exactly the two products published on oxyniti.com
  (`economics_device_evidence.md` section 1.1); no invented 3 HP or 5 HP entry. Since A9 the
  owner figures and rough estimates in `plan/owner_inputs.json` are overlaid onto these fields
  (each keeping its own status and source).
- `economics.data.js` → `OXY_DATA.economics = { tariff_presets: [ {id, label, inr_per_kwh,
  fixed_inr_per_kw_per_month, status, source} ], subsidy_options: [ {label, pct, status,
  source} ], paddlewheel: { sae_field_kg_o2_per_kwh: [low, high], unit_price_inr_2hp,
  status, source }, run_hours_published: {value: [8, 12], status, source} }`
- Per-species `other_cost_inr_per_acre_crop` (in `species.data.js`) is derived by WP1 from the
  NABARD/TNAU 2015 model projects in `economics_device_evidence.md` section 5: opex − feed −
  seed − electricity, per ha ÷ 2.4711, per crop; status ASSUMED (2015 vintage), source the
  PDF URL; species without a model project get `null`.
- `coefficients.data.js` → `OXY_DATA.coefficients` = the contents of `plan/coefficients.json`.

### 4.2 Model (`site/js/model.js`)
Classic script exposing `window.OxyModel`; at the end:
`if (typeof module !== "undefined") module.exports = OxyModel;` so Node tests can `require` it.
Pure functions, no DOM, no `Date.now()`, no randomness.

```js
OxyModel.doSaturation(t_c, salinity_ppt, elevation_m)        // mg/L, spec 4.1
OxyModel.pondTemperature(t_air_c, coeff)                      // spec 2
OxyModel.thermalFactor(t_w_c, species)                        // 0..1, spec 3
OxyModel.evaluate(inputs, data) -> result                     // whole pipeline
OxyModel.MissingDataError                                     // class extends Error {field, species}
OxyModel.defaultsFor(species_id, district, data) -> inputs    // fills spec 1 defaults
```

`result` shape (all money in ₹, mass in kg, both `low` and `high` cases):
```js
{
  inputs_resolved: { <input id>: {value, unit, status, source} },
  station: { name, district, source },
  months: [ { m, t_air_c, t_w_c, c_s_mg_l, g_t, in_crop, biomass_kg, do_dawn_base, do_dawn_oxy, s_base, s_oxy } ],  // 12 entries
  crop: { months: [ints], size_factor, G_T, G_T_ref, ds },
  uplift: { low: {G, dS, fcr_factor, extra_kg_fraction, ceiling_clamped}, high: {...} },
  baseline: { n, S0, w0_g, w_h0_g, kg, revenue, feed, seed, other, elec, profit },
  with_oxy: { low: { S1, w_h1_g, kg, revenue, feed, seed, other, elec, profit }, high: {...} },
  delta: { low: { kg_crop, kg_year, revenue_crop, feed_crop, elec_crop, profit_crop, profit_year }, high: {...} },
  payback: { status: "ok" | "blocked", reason, capex, months_low, months_high },
  unit: { id, label, power_kw_shaft, power_kw_used, o2_input_lpm, o2_input_lpm_used, price_inr,
          concentrator_kw, concentrator_price_inr, maintenance_pct,
          n_units, n_best, n_relief, sizing: "auto" | "manual",
          o2_g_per_unit_night, supply_mg_l_per_unit_night, deficit_max_mg_l, status },
  // A9: delta.low/high also carry maintenance_year; OxyModel.compareStations(inputs, data) -> rows (spec A9.4)
  warnings: [ { code: "THERMAL_OUT_OF_RANGE" | "CEILING_CLAMPED" | "SIZING_CAPPED" | "CONCENTRATOR_POWER_UNKNOWN"
                     | "PRICE_OUT_OF_SOURCED_RANGE" | "NOT_OXYGEN_LIMITED" | "NO_PAYBACK_AT_PUBLISHED_O2", message, months? } ],
  assumptions: [ { id, label, value, unit, status, date, source } ]
}
```

### 4.3 UI ↔ model
`ui.js` owns the DOM and calls `OxyModel.evaluate` on every input change (debounced 50 ms).
`charts.js` exports `window.OxyCharts.renderSeasonStrip(el, result)` and
`renderWaterfall(el, result)`. `map.js` exports `window.OxyMap.init(el, data, { onDistrict })`
and `OxyMap.highlight(districtName)`. `i18n.js` exports `window.OxyI18n.t(key, fallback)` and
`setLang(code)`; strings live in `site/js/i18n.js` as `{ en: {...}, ta: {...} }`.

## 5. Work packages, owners, order

| WP | Owner | Depends on | Produces | Gate |
|---|---|---|---|---|
| WP0 Research + spec | Fable (done) | — | `research/*`, `plan/*` | files exist, JSON parses |
| WP1 Data build | Sonnet | WP0 | `tools/build_data.py`, `site/data/*.data.js`, `plan/DATA_STATUS.md` | script re-runnable; every NOT_FOUND listed; 38 districts mapped to a station |
| WP2 Model + tests | Opus | WP1 | `site/js/model.js`, `tests/model.test.mjs` | `node --test tests/` green; spec section 8 tests 1–5 |
| WP3 Oracle + comparator | Sonnet (must not read `model.js`) | WP1 | `tests/oracle.py`, `tests/compare.py`, `tests/scenarios.json` | `compare.py --self-test` FAILs on the injected defect |
| WP4 UI | Sonnet | WP1 (+ interface 4.2) | `site/index.html`, `css/styles.css`, `js/ui.js`, `js/charts.js`, `js/i18n.js` | renders at 360 / 768 / 1280 px; no horizontal scroll; assumptions panel complete |
| WP5 Map | Sonnet | WP1 | `site/js/map.js` | 38 polygons drawn; click sets district; legend carries source and year |
| WP6 Integration + QA | Opus | WP2–WP5 | fixes, `site/README.md`, `plan/QA_REPORT.md`, `tests/screenshots/*.png` | all tests green; `compare.py` parity ≤ 1e-6; screenshots reviewed; placeholder scan clean |
| WP7 Publish | Vivian | WP6 | GitHub Pages URL | `deploy.ps1` run by the owner |

WP2, WP3, WP4, WP5 run in parallel after WP1. WP4 and WP5 build against the interface in 4.2 and
a stub result until WP2 lands; WP6 replaces the stub.

## 6. Work package briefs

### WP1 — Data build (Sonnet)
- `tools/build_data.py` reads every file in `research/` and `plan/coefficients.json`, validates
  (every load-bearing field present with the envelope shape; ranges are `[low, high]` with
  `low <= high`; units are from the allowed list), and writes the seven `site/data/*.data.js`
  files. It must be deterministic and idempotent.
- District → station map: haversine from district headquarters (coordinates from
  `hotspots.json` district summaries; if a district has no coordinates there, look it up from
  the GeoJSON polygon centroid) to the nearest station; hill districts (The Nilgiris, and
  Dindigul's Kodaikanal taluk is *not* a district — keep Dindigul on the plains station) use the
  hill station. Write the map and its method into `DATA_STATUS.md`.
- Join production statistics to the GeoJSON by district name; report unmatched names. Do not
  simplify the geometry (per-ring Douglas–Peucker opens slivers on shared edges; the 1.5 MB
  file is acceptable). Record the ODbL licence and boundaryID in `DATA_STATUS.md`.
- Species ids: the research JSON has no `id`; assign stable slugs (`catla`, `rohu`, `mrigal`,
  `common-carp`, `grass-carp`, `silver-carp`, `gift-tilapia`, `pangasius`, `murrel`, `scampi`,
  `pearl-spot`, `improved-strains`, `vannamei`, `black-tiger`, `seabass`, `milkfish`,
  `grey-mullet`, `mud-crab`) and a `respiration_group` per species: `freshwater_fish`
  (carps, tilapia), `air_breathing_fish` (pangasius, murrel), `shrimp` (vannamei, black tiger,
  scampi), `brackish_fish` (seabass, milkfish, grey mullet, pearl spot), `crab` (mud crab).
- **Documented fallbacks (each applied value gets status ASSUMED and a `fallback_rule` note;
  nothing else is filled):**
  1. `temp_tolerable_c` null, or one bound null → missing low bound = `temp_optimum_c.low − 5`,
     missing high bound = `temp_optimum_c.high + 5`.
  2. `do_lethal_mg_l` null → group default from `plan/coefficients.json`
     (`species_group_defaults.<group>.do_lethal_mg_l`).
  3. `do_minimum_mg_l` null → group default `do_min_growth_mg_l`. For `air_breathing_fish`
     with a sourced value below 1.0 mg/L (pangasius 0.1 is a survival floor, not a growth
     threshold): move that value to `do_lethal_mg_l` (keep its status) and take the group
     `do_min_growth_mg_l` for growth, with the note "air-breather: survival floor reclassified".
  4. Ranges: the model uses the midpoint of `[low, high]`; a one-sided range `[x, null]` uses
     `x`. Never widen a range.
  5. `stocking_months_tn` null → `stocking_month_tn_default` = 7 (July) for freshwater species
     (the sourced carp pattern), and for brackish species the first month named in the text;
     when both are null use 7 and mark ASSUMED. Parse a sourced text like "July-August" to its
     first month.
  6. `farmgate_price_inr_per_kg`: default slider value = the low end of the sourced range when
     the source's `market_level` is retail, wholesale or unstated; the midpoint when it is
     farm-gate. Carry `as_of` into the UI label ("₹200/kg, Apr 2026, market level unstated").
  7. Cross-fill from `economics_device_evidence.md` where the species file is null and the
     economics file has a sourced figure (e.g. seabass survival 84.89 %, CMFRI TN cage survey
     2022-23; vannamei count-wise prices July 2023); cite the economics file's source.
  8. `seed_size_g` (needed by spec 4.2) is not in the research file: use 5 g for fish
     fingerlings, 0.01 g for shrimp post-larvae, 0.05 g for scampi post-larvae, 100 g for mud
     crab fattening stock, all ASSUMED with a note, and list them in `DATA_STATUS.md`.
- After the fallbacks, a species is **estimable** only if all of `temp_optimum_c`,
  `stocking_density_per_acre`, `culture_period_months`, `harvest_size_g`, `survival_pct`,
  `fcr`, `farmgate_price_inr_per_kg`, `seed_cost_inr_per_unit`, `feed_cost_inr_per_kg`,
  `crops_per_year_tn` are non-null. Others get `"estimable": false` and
  `"missing": [field, ...]`; the UI lists them greyed with the missing fields named, and still
  shows their sourced parameters in the species panel.
- `plan/DATA_STATUS.md`: one table per data file — field, count VERIFIED / ASSUMED / NOT_FOUND —
  the fallbacks applied (species, field, rule), and the estimable / not-estimable lists.

### WP2 — Model (Opus)
- Implement `MODEL_SPEC.md` sections 2–7 exactly in `site/js/model.js`, using only
  `OXY_DATA` and the inputs. Reference crop (section 3) is computed once per species and cached
  inside `evaluate`.
- `tests/model.test.mjs` (Node 22 built-in test runner, no npm): spec section 8 tests 1
  (against the USGS values quoted in `research/do_physics.md`), 2, 3, 4, 5, plus one test per
  warning code.
- Document every stated approximation in a comment block at the top of the file, with the spec
  section numbers.

### WP3 — Oracle and comparator (Sonnet)
- `tests/oracle.py`: an independent Python implementation of `MODEL_SPEC.md` written from the
  spec **without reading `site/js/model.js`**. Loads the same `site/data/*.data.js` files by
  stripping the `window.OXY_DATA.x =` prefix and `json.loads` on the remainder (the data
  builder writes strict JSON after the `=`). Prints `result` as JSON for a scenario file.
- `tests/scenarios.json`: 24 scenarios spanning every estimable species, at least 6 districts
  (including a coastal, a delta, an interior and a hill district), three densities and three
  stocking months, plus 3 fail-loud cases (null unit price; a species with a null DO threshold;
  a hill district out of thermal range).
- `tests/compare.py`: runs `node tests/run_scenarios.mjs` (write it: loads data + model, evaluates
  each scenario, prints JSON) and `oracle.py`, compares every numeric leaf at 1e-6 relative
  (1e-9 absolute for DO saturation), prints a table of max deviations per output group, exit
  code 1 on any miss. `--self-test`: copies `oracle.py` to a temp file, flips the sign of the
  Q10 exponent, runs the comparison, and must report FAIL; exit 1 if it does not.

### WP4 — UI (Sonnet)
- Theme: the "Deep Lagoon" tokens from the oxyniti.com static site that the owner's screenshot
  shows — ink `#041f26`, deep `#06333d`, aqua `#14d8c4`, cyan `#5ce1ff`, mango `#ffb03a`, coral
  `#ff6b4a`, text `#dcf2ee`; fonts Sora (display) / Manrope (body) / Catamaran + Noto Sans Tamil
  (Tamil) from Google Fonts. Provide a light theme via `prefers-color-scheme` and a toggle.
- Layout: header (logo, language toggle, theme toggle) → map + district card side by side →
  calculator card (inputs left, results right, matching the existing slider card's shape) →
  seasonal strip → assumptions panel (collapsible table) → "How this is calculated" → footer
  with data sources and licences. Single column below 900 px. 16 px gutters. No horizontal
  scroll at 360 px.
- Results: extra harvest band (kg/crop and kg/year), extra profit band (₹/crop, ₹/year),
  payback (months or the blocked reason), baseline harvest and profit for context, a warning
  list rendered from `result.warnings`, and the ceiling note from `MODEL_SPEC.md` section 5.
- Every number: `Intl.NumberFormat('en-IN')`; ₹ in lakh above 99,999 with one decimal.
- WhatsApp CTA: `https://wa.me/919659727477?text=<encoded summary>`; summary lists district,
  species, area, density, the low–high extra profit, and "from the Oxyniti yield calculator".
- Tamil: only the keys that already exist on the live site (`website/wwwroot/i18n/ta.json`:
  `roi.*`, `res.*`, `o.sp*`, `o.size*`, `f.species`) are shipped in `ta`; every new string
  falls back to English and the language toggle shows "தமிழ் (partial)". Do not machine-translate
  new strings — native review is an owner action.
- Charts (`charts.js`, inline SVG, no library): 12-month strip with three rows — water
  temperature line with the species optimum band shaded; thermal suitability cells (green,
  amber, red); paired bars for `s_base` and `s_oxy` with the crop window outlined. A profit
  waterfall: baseline profit → + extra revenue → − extra feed → − extra electricity → with
  OXY-Nano. Colours must read in both themes; label every axis with units.

### WP5 — Map (Sonnet)
- `OxyMap.init(el, OXY_DATA, { onDistrict })`: Leaflet map bounded to Tamil Nadu
  (approximately 8.0–13.6 °N, 76.2–80.4 °E), OpenStreetMap tiles with attribution, district
  polygons from `OXY_DATA.districts` as a choropleth on `inland_production_t` (five quantile
  classes; districts with null production hatched grey and labelled "no published figure"),
  hover tooltip (district, production t + year, station), click → `onDistrict(name)` and
  highlight. Hotspot markers from `OXY_DATA.hotspots` with type-specific symbols and a popup
  that shows `why_hotspot`, dominant species and the source links. A legend with the data year
  and source. `OxyMap.highlight(name)` for the select → map direction.
- Keyboard: districts reachable by the select; the map is progressive enhancement.
- Tiles are the only network call; if tiles fail to load the polygons still draw on a plain
  background.

### WP6 — Integration and QA (Opus)
- Replace the UI stub with the real model; run `node --test tests/`, `python tests/compare.py`
  and `python tests/compare.py --self-test`; fix defects in any file (log each fix in
  `QA_REPORT.md` with file and line).
- Screenshots with headless Chrome (`"C:\Program Files\Google\Chrome\Application\chrome.exe"
  --headless=new --screenshot=<path> --window-size=<w>,<h> --virtual-time-budget=8000 <url>`)
  at 360×800, 768×1024, 1280×900, served by `python -m http.server` from `site/`; also one
  screenshot opened via `file://` to prove the no-server path. Save to `tests/screenshots/`.
- Review the screenshots yourself (Read the PNG) for overlap, clipped text, unreadable
  contrast; fix and re-shoot.
- `site/README.md`: what it is, how to run locally, data sources with licences (GeoJSON
  licence verbatim), the claims ceiling, the list of ASSUMED coefficients, and how to update
  data (`python tools/build_data.py`).
- `plan/QA_REPORT.md`: test output verbatim, parity table, screenshot list, open defects.

## 7. Owner decisions and inputs still needed (Vivian)

1. **Oxygen delivery per model (kg O2/h, or L/min at stated purity) and the concentrator's
   power draw.** The site publishes "up to 2 L/min" (1.5 HP) and "up to 6 L/min" (4 HP). By
   mass balance that is about 0.16 mg/L per unit per 8 h night in a 1 acre × 1.5 m pond,
   against roughly 2 mg/L from one 2 HP paddlewheel — so the tool will size several units per
   acre unless the datasheet says otherwise. This is the decision that most changes the
   numbers.
2. **List prices per model.** Both product pages show ₹4,400, which reads as a placeholder;
   payback stays blocked until a real price is entered.
3. **Which models exist.** Home page and video say OXY-Nano 1.5 / 3 / 5 HP; the catalogue has
   1.5 HP and 4 HP. The tool offers the two published products only.
4. **Whether the live site's 20–30 % slider and the +30 % / −15 % / +15 % claims stay** —
   see `DEVIATIONS.md`. The literature found supports −7 to −9 % FCR, not −15 %.
5. **Prospecting report correction.** `docs/NBG_Trichy_Prospecting_Report.md` section 4
   attributes "capital ₹2.1 L, variable ₹5.76 L, 9,000 kg at ₹120/kg" to TNAU/NABARD; the
   PDF says ₹3.69 L, ₹5.02 L/crop, 9,375 kg/crop at ₹75/kg per hectare. A supersession
   banner is needed there (STANDARDS rule 7); not done by this tool.
6. **Run `deploy.ps1`** to publish (creates the public repo `vivian4fb/oxyniti-yield-calc`).
7. **Native Tamil review** before the Tamil toggle is promoted from "partial".
8. Any **measured demo-pond data** (DO before/after, farmer's actual yield and price) — one
   real row outranks every published range in this tool.

## 8. Data status (research complete 2026-09-21; per-field detail in `DATA_STATUS.md` after WP1)

| File | Content | Provenance | Notes |
|---|---|---|---|
| `species_parameters.json` | 18 species × 25 fields, 342 numeric cells: 201 VERIFIED, 39 ASSUMED, 102 NOT_FOUND | NABARD/TNAU 2015 model projects, FAO Tech. Paper 583 (Thanjavur survey), TN Scale of Finance 2024-25, MPEDA/CAA, FAO species sheets | `do_lethal_mg_l` missing for 16, `temp_tolerable_c` for 9 → WP1 fallbacks; prices dated and market-level flagged |
| `climate_normals.json` | 32 IMD stations, 1991–2020 monthly normals (tmax, tmin, rain, RH, cloud) | IMD Pune *Climatological Tables 1991–2020*, parsed from the PDF; 25 stations cross-checked exactly against Wikipedia's IMD tables | Kovilankulam PARTIAL; Cuddalore elevation null (IMD misprint) |
| `do_physics.md` | Benson & Krause 1984 coefficients read from the paper; Q10 tilapia 1.79, rohu 1.91–2.05; DO–growth literature; Boyd night budget; 13 nano-bubble studies inventoried | primary papers | vannamei Q10 NOT_FOUND (ASSUMED 2.0); carp DO–growth curve NOT_FOUND (tilapia proxy) |
| `tn_climate_seasons.md` | seasons and NEM share (48 %), TNAU seven zones with districts, shrimp calendar, pond-vs-air regression, TN pond temperature series | IMD, RMC Chennai, TNAU, MPEDA, peer-reviewed | official stocking months for carp/tilapia/murrel NOT_FOUND |
| `economics_device_evidence.md` | Oxyniti product specs and claims verbatim; TNERC tariff (LT III-A(1), ₹4.80/6.95 per kWh, effective 2025-07-01); PMMSY rates; paddlewheel prices and SAE; five NABARD crop models; prices; uplift evidence | oxyniti.com (prerendered), TNERC order and TANGEDCO statement, PMMSY booklet, NABARD PDFs, peer-reviewed trials | unit price placeholder ₹4,400; no pond-area rating; concentrator power NOT_FOUND |
| `tn_districts.geojson` | 38 districts, 1.5 MB, `district` normalised | geoBoundaries gbOpen IND ADM2 (IND-ADM2-76128533), **ODbL 1.0** | keep unsimplified (shared-edge slivers); attribution required |
| `hotspots.json` + `tn_aquaculture_geography.md` | 87 hotspots: 38 district summaries, 8 freshwater clusters, 7 brackish clusters, 28 seed farms/hatcheries, 6 reservoirs; 82 VERIFIED, 5 ASSUMED | DES Statistical Hand Book 2021-22 Tables 8.2/8.3 (district production), Fisheries Policy Note 2025-26 Tables 4, 7, 8 (CAA farms, seed farms), TNAU zones, CMFRI | no private farms or contacts; Chennai inland null; no official district table after 2021-22 exists |
