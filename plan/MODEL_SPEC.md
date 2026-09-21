# Oxyniti Yield & Profit Calculator — model specification v1

*Written 2026-09-21 by the research/planning pass (Fable 5.1). State: DRAFT until the research
files it cites exist and every coefficient below has a status label. Execution agents implement
this spec verbatim; where the spec and a research file disagree, the research file wins and the
disagreement is logged in `plan/DEVIATIONS.md`.*

## 0. What the tool answers

For one pond in one Tamil Nadu district: **how many extra saleable kilograms, how much extra net
profit, and how many months to pay back an OXY-Nano unit — and why the answer differs by
species, season, stocking density and district.**

Governing rules (from `2_Business/CLAUDE.md` and `NBG/.claude/SALES_OVERRIDE.md`):

1. **Claims ceiling: +18 % saleable kg.** The calculator can never output more than +18 % extra
   harvest. The ceiling is reached only when the pond is fully oxygen-limited in every month of
   the crop and the unit fully relieves it. The current site slider (20–30 % on a flat
   2,500 kg/acre/year) exceeds this ceiling; this tool supersedes it, and the supersession is
   logged in `plan/DEVIATIONS.md`.
2. **Every number carries units, a status (`VERIFIED` / `ASSUMED` / `UNTESTED` / `NOT_FOUND`), a
   date and a source.** The UI shows all of them in an Assumptions panel.
3. **Fail loudly.** A missing coefficient throws; a species with a `null` load-bearing field
   after the documented, labelled fallbacks in `EXECUTION_PLAN.md` WP1 cannot produce an
   estimate; a missing unit price blocks the payback output with the message "enter unit
   price". No silent defaults anywhere: every fallback value is ASSUMED, named, and shown.
4. **Never fabricate** a farm, contact or price. Hotspots are district-level statistics and
   named public facilities only.
5. British English (`en_GB`), ₹ and metric. Money is shown in ₹ with Indian grouping
   (`en-IN`), and in lakh above ₹99,999 (`₹1.53 L`).

## 1. Inputs

| id | Label | Unit | Default | Range | Notes |
|---|---|---|---|---|---|
| `district` | District | — | Tiruchirappalli | 38 TN districts | Set by map click or select |
| `species` | Species | — | GIFT tilapia | `species.json` ids | Greyed out if load-bearing data is `null` |
| `area_acre` | Pond water area | acre | 1.0 | 0.25 – 10 (step 0.25) | 1 acre = 4,046.86 m² |
| `depth_m` | Average water depth | m | 1.5 | 0.8 – 2.5 (step 0.1) | Default status ASSUMED unless a research file gives a TN typical depth |
| `density_per_acre` | Stocking density | animals/acre | `density_default_per_acre` (yield-consistent, see amendment A3) else species mid | from min(sourced low, 0.5 × default) to max(sourced high, 1.5 × default) | Slider |
| `o2_input_lpm_override` | Oxygen delivery per unit (datasheet) | L/min | `null` | 0.5 – 60 | Advanced; `null` = the product page value; for the OEM figure once supplied |
| `power_kw_override` | Electrical input per unit (datasheet) | kW | `null` | 0.1 – 10 | Advanced; `null` = shaft kW from HP |
| `stock_month` | Stocking month | 1–12 | species TN default | 1–12 | Select |
| `price_inr_kg` | Farm-gate price | ₹/kg | species mid | species [low, high] ± 30 % | Slider |
| `feed_price_inr_kg` | Pellet feed price | ₹/kg | species/regional value | 20 – 120 | Slider |
| `bloom` | Pond colour (plankton bloom) | — | medium | light / medium / dense | Sets plankton respiration k_p (coefficients.json); shown with a one-line Secchi-disc hint |
| `existing_aeration_kw` | Existing aeration | kW | 0 | 0 – 15 | Select: none / 1 × 1 HP paddlewheel / 2 × 1 HP / 2 × 2 HP / custom kW |
| `existing_run_h` | Existing aeration hours | h/night | 8 | 0 – 24 | Only if existing aeration > 0 |
| `tariff_inr_kwh` | Electricity tariff | ₹/kWh | 6.95 | presets 0 / 4.80 / 6.95 / 8.00, or custom 0 – 12 | LT III-A(1) energy charge above 500 units per two months, effective 2025-07-01 (VERIFIED in `economics_device_evidence.md` section 2); 0 = LT IV allied-agriculture supply; 8.00 = LT III-B above 12 kW |
| `unit_model` | Nano-bubble generator | — | 1.5 HP | `products.json` ids (1.5 HP, 4 HP as published) | Select; the site's OXY-Nano 3 and 5 have no product page (NOT_FOUND) and are not offered |
| `n_units` | Number of units | count | auto | auto, or 1 – 20 | Auto = section 7 sizing; manual override shown against the auto value |
| `unit_price_inr` | Unit price | ₹ | `null` | ≥ 0 | The site shows ₹4,400 on both products, ASSUMED to be a placeholder; treated as `null`, which blocks payback until entered |
| `concentrator_kw` | Oxygen concentrator power | kW | `null` | 0 – 2 | The generator needs a PSA concentrator or cylinder (VERIFIED); its power draw is NOT_FOUND; `null` excludes it from electricity with warning `CONCENTRATOR_POWER_UNKNOWN` |
| `concentrator_price_inr` | Oxygen concentrator price | ₹ | product value (ASSUMED) | ≥ 0 | A9; one per unit ASSUMED |
| `maintenance_pct` | Maintenance per year | % of capex | 3 | 0 – 15 | A9, ASSUMED |
| `station_name` | City (climate station) | — | `null` = district's station | 32 IMD stations | A9; drives the crop climate; reference crop stays Tiruchirappalli |
| `subsidy_pct` | Subsidy on unit | % | 0 | 0 / 40 / 60 | PMMSY input-subsidy rates (VERIFIED); whether an aerator qualifies under "inputs" is NOT_FOUND, so the options are labelled UNTESTED |
| `run_h` | Run hours | h/night | 8 | 2 – 24 | Slider; 8–12 h/day is the published range for pond aerators (UNTESTED for TN) |
| `include_fcr_gain` | Apply FCR improvement | bool | false | — | Advanced toggle; −7 % at full relief (Mauladani et al. 2020, n = 1 pond per arm), labelled UNTESTED |

Units: 1 ha = 2.4711 acre; 1 t/ha = 404.69 kg/acre; 1 HP = 0.7457 kW.

## 2. Climate → pond water temperature

- Each district maps to one climate station in `climate.json` (`district_station_map`). The map
  is by nearest station to the district headquarters (haversine) unless the research notes give
  a better assignment (e.g. hill districts → Kodaikanal/Ooty station).
- Monthly mean air temperature: `T_air(m) = (tmax_c(m) + tmin_c(m)) / 2`.
- Pond water temperature: `T_w(m) = a + b · T_air(m)`. `a`, `b` come from
  `research/do_physics.md` / `tn_climate_seasons.md` section (d). If NOT_FOUND,
  `coefficients.json` carries `a = 0, b = 1` with status ASSUMED and the note "shallow tropical
  ponds track mean air temperature". The Assumptions panel shows whichever applies.
- Crop months: `stock_month, stock_month+1, …` for `culture_period_months` (mid of the species
  range, rounded), wrapping December → January.

## 3. Thermal suitability (growth-days factor)

Trapezoid on species limits, per month:

```
g_T(m) = 0                                   if T_w < Tt_lo or T_w > Tt_hi
       = (T_w - Tt_lo) / (To_lo - Tt_lo)     if Tt_lo <= T_w < To_lo
       = 1                                   if To_lo <= T_w <= To_hi
       = (Tt_hi - T_w) / (Tt_hi - To_hi)     if To_hi < T_w <= Tt_hi
```

`G_T(crop) = mean of g_T over the crop months`. The species' published harvest size and yield
are taken to describe the **reference crop**: the same species stocked in its TN default month
at the Tiruchirappalli station. So

```
size_factor = clamp( G_T(crop) / G_T(reference crop), 0.5, 1.10 )
w_h0 = harvest_size_g(mid) * size_factor
```

This makes the default scenario reproduce the sourced yield exactly and moves other scenarios
proportionally. Stated approximation: growth in a month scales linearly with the trapezoid;
no ration or photoperiod effects. A month with `g_T = 0` is shown red in the seasonal strip with
the message "outside the species' tolerable temperature — oxygen will not fix this".

## 4. Dissolved oxygen physics

### 4.1 Saturation
`C_s(T_w, S, P)` in mg/L from Benson & Krause (1984) as used by USGS DOTABLES, with the exact
coefficients and the salinity (ppt) and pressure terms written out in `research/do_physics.md`.
Pressure: 1 atm at sea level; hill stations use the elevation correction. Freshwater species
use `S = 0`; brackish species use the `salinity_ppt` default in `species.json`.

**Oracle:** the Python table in `research/do_physics.md` (20, 25, 28, 30, 32, 35 °C at 0 / 15 /
25 ppt). JS must match to 1e-9 mg/L against `tests/oracle.py` and to 0.02 mg/L against the
published USGS values.

### 4.2 Biomass through the crop
```
n = density_per_acre * area_acre
S(t) = 1 - (1 - S0) * t / T           (linear mortality over the crop; S0 = survival mid)
w(t) = w0 + (w_h - w0) * t / T        (linear growth in mass; w0 = seed size from species.json)
B(t) [kg] = n * S(t) * w(t) / 1000
```
Evaluate at the mid-point of each crop month. Stated approximation: linear growth and linear
mortality. (A von Bertalanffy curve is a v2 item; it changes the timing of stress, not its
crop mean, by more than a few percent only for very long crops.)

### 4.3 Night-time DO budget (Boyd-style)
Per crop month, well-mixed pond of volume `V [L] = area_m2 * depth_m * 1000`:

```
DO_dusk      = f_dusk * C_s                                 (f_dusk = 1.20, coefficients.json night_budget)
R_fish(m)    = B(m) * q(T_w) / V                            [mg/L/h]; B in kg, q in mg O2 per kg per h, V in litres
q(T_w)       = q_ref * Q10 ^ ((min(T_w, t_cap) - t_ref) / 10)   (per respiration_group in coefficients.json)
R_plankton   = k_p[bloom] * Q10_p ^ ((T_w - 25) / 10)       (bloom input: light / medium / dense -> 0.15 / 0.30 / 0.45 mg/L/h at 25 degC)
R_sed        = (k_sed / depth_m) * Q10_s ^ ((T_w - 25) / 10) [mg/L/h]
Supply_exist = existing_aeration_kw * SAE_pw * existing_run_h * 1e6 / V   [mg/L per night]  (SAE_pw = 1.0 kg O2/kWh field, coefficients.json)
D_diff       = 0.5 mg/L per night, added only while DO is below saturation
DO_dawn_base(m) = DO_dusk - h_night * (R_fish + R_plankton + R_sed) + Supply_exist + D_diff,  h_night = 11.5
```
Oxygen supply cannot raise DO above `C_s` (cap at saturation) and DO cannot go below 0. All
coefficients and their statuses are in `plan/coefficients.json`; the input `bloom` (default
medium) is the only new user-facing control this section adds.

Magnitude check (ASSUMED coefficients, May, Tiruchirappalli, T_w about 32.7 degC): a GIFT
pond at 16,000/acre reaches about 4.8 t/acre mid-crop, R_fish about 0.24 mg/L/h, plankton
0.42, sediment 0.10 -> 8.7 mg/L lost over the night against 9.0 mg/L at dusk: the unaerated pond
is at the lethal floor before dawn, which is why intensive tilapia ponds run paddlewheels. A
carp pond at 2,800/acre loses 6.7 mg/L and dawns at about 2.8 mg/L in May but 5.7 mg/L in
January. That seasonal contrast is the effect the calculator must show.

### 4.4 Oxygen stress index
Species thresholds from `species.json`: `do_min_mg_l` (feeding/growth suppressed below this)
and `do_lethal_mg_l`.

```
s(m) = clamp( (do_min - DO_dawn(m)) / (do_min - do_lethal), 0, 1 )
```
`s = 0`: dawn DO at or above the species' growth threshold — no oxygen limitation, no benefit.
`s = 1`: dawn DO at or below the lethal level. Months outside the crop window are computed for
the display strip but excluded from the crop means. **Pinned 2026-09-21 (amendment A6):** for
a month outside the crop window, `biomass_kg` is the crop-mean biomass (the arithmetic mean of
the in-crop monthly biomasses), so the strip shows the seasonal oxygen effect at a
representative stocking; `do_dawn_*` and `s_*` for those months follow from that biomass.

### 4.5 With the nano-bubble generator — oxygen mass balance
The product pages publish an oxygen input capacity per unit (`o2_input_lpm`: 2 L/min for the
1.5 HP, 6 L/min for the 4 HP — VERIFIED 2026-09-21, `economics_device_evidence.md` section 1.1)
fed from a PSA concentrator or cylinder. The oxygen a unit can add per night is therefore
bounded by mass balance, not by pump power:

```
m_O2_per_unit [g/night] = o2_input_lpm * 60 * run_h * rho_O2 * purity * eta_nb
  rho_O2  = 1.31 g/L       oxygen gas density at 25 degC, 1 atm (ASSUMED rating condition of the concentrator)
  purity  = 0.90           PSA concentrator output purity (ASSUMED; cylinder = 1.0)
  eta_nb  = 0.85           fraction of injected oxygen that ends up dissolved (ASSUMED; nano-bubbles do not
                           rise and burst, so this is high, but the OEM figure is NOT_FOUND)
Supply_oxy [mg/L per night] = n_units * m_O2_per_unit * 1000 / V
DO_dawn_oxy(m) = min( DO_dawn_base(m) + Supply_oxy, C_s )
```
Worked check the tests must reproduce: 1.5 HP unit, 2 L/min, 8 h, 1.31 g/L, purity 0.90,
eta 0.85 → 961 g O2 per night; in a 1 acre × 1.5 m pond (V = 6.07 × 10^6 L) that is
0.158 mg/L per unit per night. A 2 HP paddlewheel at Boyd's field rate of about 1 kg O2/kWh
adds roughly 12 kg per 8 h night, about 2 mg/L in the same pond. **The published 2 L/min
therefore relieves a 1 acre semi-intensive pond only with several units; the calculator says
so through section 7 sizing rather than hiding it.** This is the single most important thing
the owner must confirm against the OEM datasheet (oxygen delivery in kg O2/h per model).

All three coefficients live in `coefficients.json` with status ASSUMED and are listed in the
Assumptions panel. There is no fallback path: if `o2_input_lpm` is null for the chosen model the
model throws `MissingDataError`.

Crop-mean relief: `ds = mean over crop months of ( s_base(m) - s_oxy(m) )`, in [0, 1].

## 5. Uplift — capped at the internal model

Calibration to the internal +18 % model (`docs/make_charts.py`, `chart_farmer_roi`): the
+18 % is decomposed as **+12 % growth** and **+5 percentage points survival** at a typical 85 %
baseline survival: `1.12 * 0.90 / 0.85 = 1.186`.

```
G       = 0.12 * ds                       growth (harvest size) uplift, fraction
dS      = 0.05 * ds                       survival uplift, absolute
S1      = min(S0 + dS, 0.98)
w_h1    = w_h0 * (1 + G)
FCR1    = FCR0 * (1 - 0.07 * ds)  if include_fcr_gain else FCR0     (UNTESTED; default off; -7 % is Mauladani et al. 2020)
```

Evidence context (all in `economics_device_evidence.md` section 7): Mauladani et al. 2020
(vannamei, 800 m² ponds, one pond per arm): harvest +19.7 %, survival 75 → 92 %, FCR 1.4 → 1.3;
Boyd & Hanson 2010 (shrimp ponds, minimum DO 2.3 → 3.9 mg/L): survival 42 → 61 %, yield +34 %,
FCR −26 %; Tran-Duy et al. 2008 (Nile tilapia tanks, DO 3.0 → 5.6 mg/L): growth +41 %. The
+12 % / +5 point calibration sits below every one of these, which is the point of the ceiling.
Reported as a band: **low case** uses half the coefficients (0.06, 0.025, 0.05); **high case**
uses the full ones. By construction the high case never exceeds +18.6 % at S0 = 0.85 and
lower survival baselines produce slightly more (e.g. S0 = 0.70 → +20 %); clamp the reported
extra-kg fraction at **0.18** and set `ceiling_clamped: true` in the result so the UI can say
"capped at the internal model".

## 6. Economics per crop

```
kg0 = n * S0 * w_h0 / 1000               kg1 = n * S1 * w_h1 / 1000
gain0 = kg0 - n * S0 * w0 / 1000         gain1 = kg1 - n * S1 * w0 / 1000
Revenue  = kg * price_inr_kg
Feed     = gain * FCR * feed_price_inr_kg
Seed     = n * seed_cost_inr_per_unit
Other    = other_cost_inr_per_acre_crop * area_acre      (lime, fertiliser, labour, lease, harvest; from economics research per species)
Elec0    = existing_aeration_kw * existing_run_h * days * tariff
P_unit   = power_kw_shaft (HP * 0.7457) + (concentrator_kw if not null else 0)
Elec1    = Elec0 + n_units * P_unit * run_h * days * tariff + fixed_charge
fixed_charge = n_units * power_kw_shaft * fixed_inr_per_kw_per_month * culture_period_months   (LT III-A(1) fixed charge, VERIFIED; 0 when tariff preset is LT IV)
days     = culture_period_months * 30.4
Profit0  = Revenue0 - Feed0 - Seed - Other - Elec0
Profit1  = Revenue1 - Feed1 - Seed - Other - Elec1
dProfit_crop = Profit1 - Profit0
dProfit_year = dProfit_crop * crops_per_year_tn
capex    = n_units * unit_price_inr * (1 - subsidy_pct / 100)
payback_months = capex / (dProfit_year / 12)             (blocked if unit_price_inr is null or dProfit_year <= 0)
```
Outputs carry both the low and the high case. Baseline profit is shown so the farmer sees the
uplift in the context of the crop, and it is labelled with the status of `Other`.

`Other` per species comes from the NABARD/TNAU 2015 model projects in
`economics_device_evidence.md` section 5 (opex minus feed minus seed minus electricity, per ha,
converted to per acre), status ASSUMED because the vintage is 2015; the UI says "2015 model
costs — replace with your own".

## 7. Unit sizing by oxygen deficit

There is no published pond-area rating (NOT_FOUND), so sizing is by the night-time budget of
section 4:

```
deficit(m)   = max( do_min - DO_dawn_base(m), 0 )            [mg/L] per crop month
deficit_max  = max over crop months of deficit(m)
n_relief     = ceil( deficit_max * V / (m_O2_per_unit * 1000) )   units, minimum 1, capped at 20
n_best       = argmax over n in 1..cap of delta.high.profit_year(n); ties -> the smaller n
```
`n_relief` is the number of units that lifts the worst crop month's dawn DO to the species'
growth threshold. `n_best` is the number that maximises the high-case annual extra profit
(uplift saturates at the ceiling while electricity grows linearly, so the search is a plain
scan over 1..20, evaluating sections 4.5–6 for each n). **Auto sizing uses `n_best`**; the
result reports `n_units`, `n_best`, `n_relief` and `sizing` ("auto" or "manual"). If the best
annual extra profit is not positive, warning `NO_PAYBACK_AT_PUBLISHED_O2` says: "At the
published oxygen input of this product the extra fish do not cover the electricity for any
number of units; enter the datasheet oxygen delivery under Advanced." If `n_relief` hits the
cap, warning `SIZING_CAPPED` says the pond is larger than this product line can relieve at the
published oxygen input. A manual `n_units` overrides `n_best`.

`m_O2_per_unit` uses `o2_input_lpm_override` when it is not null, and the electricity uses
`power_kw_override` when it is not null; both appear in the Assumptions panel as user-entered.

### Amendments of 2026-09-21 (after WP2 first run) — binding
- **A1 (data, WP1):** where `do_minimum_mg_l` is a range, the growth threshold is its **high
  bound** (the low bound is a tolerance figure); WP1 writes the scalar with `fallback_rule:
  "do_min_high_bound"` and keeps the range in the note.
- **A2 (data, WP1):** a station with `elevation_m = null` within 10 km of the coast gets 5 m,
  ASSUMED, with the IMD misprint noted; any other null elevation stays NOT_FOUND and the
  district maps to the nearest station that has an elevation, so no district throws.
- **A3 (data, WP1):** `density_default_per_acre = yield_mid_per_crop / (survival_mid/100 ×
  harvest_size_mid_g/1000)`, where a yield published per year is divided by the crops-per-year
  midpoint; status ASSUMED, `fallback_rule: "yield_consistent_density"`, with the sourced
  density range and the kg it would imply recorded in the note. This anchors the baseline to
  the sourced yield instead of compounding three range midpoints (GIFT: 8,786 kg/acre/crop
  against a sourced 2,428–4,047).
- **A4 (model and oracle):** `defaultsFor` uses `density_default_per_acre` when present; the
  two override inputs above; sizing per this section (`n_best`, `n_relief`,
  `NO_PAYBACK_AT_PUBLISHED_O2`).
- **A5 (spec slips confirmed by WP2):** the low case multiplies each of the three coefficients
  by `low_case_factor` (so FCR low = 0.035); the oxygen worked check is 962 g at
  rho = 1.31 g/L.
- **A8 (pinned after the parity run):** warning `NOT_OXYGEN_LIMITED` fires if and only if the
  crop-mean of `s_base` over the in-crop months is below 0.05 (it describes the pond, so it
  does not depend on `n_units`). When a species has `estimable === false`, `MissingDataError`
  names `species.missing[0]` (the data file's order) and the species id. Both sides of the
  parity comparison implement these two rules.
- **A9 (owner inputs of 2026-09-21, city selection, full payback) — binding:**
  1. *Data.* `plan/owner_inputs.json` is overlaid onto the products by WP1: `o2_input_lpm`
     becomes a range (1.5 HP: [1, 2] VERIFIED owner-stated; 4 HP: [3, 6] ASSUMED) and the
     model uses its midpoint; each product gains `concentrator_kw` (0.69 kW = 230 V × 3 A,
     owner-stated, PF 1.0 ASSUMED; 4 HP 1.0 kW ASSUMED), `price_inr` (₹85,000 / ₹1,60,000,
     ASSUMED rough estimates with their basis), `concentrator_price_inr` (₹45,000 / ₹90,000,
     ASSUMED) and `maintenance_pct_per_year` (3 %, ASSUMED). Warning
     `CONCENTRATOR_POWER_UNKNOWN` therefore fires only if a product's `concentrator_kw` is null.
  2. *Inputs.* `unit_price_inr` and `concentrator_kw` default to the product values (so payback
     is no longer blocked by default; the price carries its ASSUMED badge). New inputs:
     `concentrator_price_inr` (default = product value), `maintenance_pct` (default 3),
     `station_name` (default null = the district's station; any of the 32 stations may be
     chosen so a city's climate drives the crop). The reference crop of section 3 stays at the
     Tiruchirappalli station regardless of `station_name`.
  3. *Economics.* `capex = n_units × (unit_price_inr + concentrator_price_inr) × (1 − subsidy_pct/100)`;
     `Maint_year = n_units × (unit_price_inr + concentrator_price_inr) × maintenance_pct/100`;
     `dProfit_year = dProfit_crop × crops_per_year_tn − Maint_year` (both cases);
     `payback_months = capex / (dProfit_year / 12)`, blocked with reason "No extra profit at
     these inputs" when `dProfit_year_high <= 0`, and with reason "enter unit price" only when
     `unit_price_inr` is null. `n_best` maximises this `dProfit_year` (high case). The result
     carries `delta.*.maintenance_year` and `unit.concentrator_price_inr`, `unit.maintenance_pct`.
  4. *City comparison.* `OxyModel.compareStations(inputs, data)` evaluates the same inputs with
     `station_name` set to each station in `climate.stations` in file order (auto sizing), and
     returns rows `{ station, district, elevation_m, G_T, size_factor, harvest_size_g,
     baseline_kg_crop, ds, extra_kg_crop_high, profit_year_high, n_best, warnings: [codes] }`;
     a station that throws yields `{ station, error }`. The oracle implements
     `compare_stations` identically; parity compares the two scenarios in `tests/scenarios.json`
     that set `station_name` (Kodaikanal and Nagapattinam) and one `compare_stations` call on the
     default inputs under the A7 numeric contract.

## 8. Contract tests (the definition of done for the model)

1. **DO saturation parity** — JS vs Python oracle over T = 0…40 °C step 1, S in {0, 15, 25, 35}
   ppt: max |delta| < 1e-9 mg/L. JS vs published USGS values at 20 / 25 / 30 °C, 0 ppt:
   |delta| ≤ 0.02.
2. **Calibration reproduction (synthetic scenario)** — with `ds` forced to 1, FCR gain off,
   S0 = 0.85 and inputs chosen so the baseline harvest is 9,000 kg at ₹120/kg, the extra
   saleable kg must be +18.6 % ± 0.1 % (1.12 × 0.90 / 0.85) before clamping and exactly
   +18.0 % after, extra revenue ≈ ₹1.94 L, and, with feed priced so that baseline feed is
   ₹2.30 L, extra feed ≈ ₹0.41 L and net ≈ ₹1.53 L ± 5 %. These are the arithmetic of the
   internal model in `docs/make_charts.py`; the test pins the calculator's arithmetic to it.
   The economics in that internal model are ASSUMED, not TNAU/NABARD (see `DEVIATIONS.md`).
3. **Monotonicity** — increasing `density_per_acre` never decreases `s_base`; increasing
   `existing_aeration_kw` never increases `s_base`; increasing `run_h` or `n_units` never
   decreases `ds`; increasing `area_acre` at fixed density never decreases `n_auto`.
3a. **Oxygen supply check** — 1.5 HP, 2 L/min, 8 h, defaults → 961 g O2/night ± 1 g and
   0.158 mg/L ± 0.001 in a 1 acre × 1.5 m pond.
4. **Ceiling** — over 200 random scenarios, `extra_kg_fraction_high <= 0.18 + 1e-12`.
5. **Fail-loud** — a species with `do_min_mg_l = null` throws `MissingDataError` naming the
   field; a product with `o2_input_lpm = null` throws; `unit_price_inr = null` yields
   `payback: { status: "blocked", reason: "enter unit price" }`; `concentrator_kw = null`
   produces warning `CONCENTRATOR_POWER_UNKNOWN` and excludes it from electricity.
6. **Scenario parity** — the scenarios in `tests/scenarios.json` (species × district × density ×
   stock month, plus overrides and fail-loud cases) evaluated by JS and by the independent
   Python oracle agree under this contract (pinned 2026-09-21, amendment A7): every numeric
   leaf of `crop`, `uplift`, `baseline`, `with_oxy`, `delta`, `unit` and `payback` to 1e-6
   relative; `months[].t_air_c, t_w_c, c_s_mg_l, g_t, in_crop` for all twelve months and
   `months[].biomass_kg, do_dawn_base, do_dawn_oxy, s_base, s_oxy` for every month (A6 makes
   out-of-crop months comparable) to 1e-6 relative (1e-9 absolute for `c_s_mg_l`);
   `payback.status` and `station.name` exactly; `warnings` as an equal set of codes; error
   cases as an equal error class and field name. `inputs_resolved`, `assumptions` and message
   wording are outside the contract.
7. **Comparator self-test** — `tests/compare.py --self-test` injects a defect (Q10 exponent sign
   flipped in a copy of the oracle) and must report FAIL.

## 9. Known limitations to state in the UI

- Monthly climate normals, not this year's weather.
- Linear growth and mortality; no disease, no water exchange, no algal crash model.
- Uplift is calibrated to an internal conservative model, not measured on the farmer's pond.
- Prices are the sourced range on the sourcing date; the farmer's own price overrides.

*Status of this document: ASSUMED coefficients are enumerated in `coefficients.json` once the
research files land; nothing above is VERIFIED until the contract tests pass.*
