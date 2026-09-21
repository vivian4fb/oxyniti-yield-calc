/*
 * tests/model.test.mjs — contract tests for site/js/model.js.
 * Implements plan/MODEL_SPEC.md section 8 tests 1, 2, 3, 3a, 4 and 5, one test per warning
 * code, and a determinism check. Tests 6 (scenario parity) and 7 (comparator self-test) belong
 * to WP3 and are not duplicated here.
 *
 * Node 22 built-in test runner, no npm packages:  node --test tests/
 * The data files are classic scripts that assign window.OXY_DATA.<x>, so they are loaded with
 * vm.runInNewContext into a { window: {} } sandbox; the model is a classic script loaded with
 * require.
 */

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const require = createRequire(import.meta.url);

const OxyModel = require(path.join(ROOT, "site", "js", "model.js"));
const { MissingDataError } = OxyModel;

/* ------------------------------------------------------------------ loading the data files */

function loadData() {
  const dir = path.join(ROOT, "site", "data");
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".data.js")).sort();
  assert.ok(files.length > 0, "no site/data/*.data.js files found - WP1 has not run");
  const sandbox = { window: {} };
  for (const f of files) {
    vm.runInNewContext(fs.readFileSync(path.join(dir, f), "utf8"), sandbox, { filename: f });
  }
  const data = sandbox.window.OXY_DATA;
  assert.ok(data, "the data files did not assign window.OXY_DATA");
  return data;
}

const DATA = loadData();
const COEFF = DATA.coefficients;

const DEFAULT_SPECIES = "gift-tilapia";
const DEFAULT_DISTRICT = "Tiruchirappalli";

function defaults(overrides) {
  return Object.assign(OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, DATA), overrides || {});
}

function cropMean(result, field) {
  let sum = 0;
  for (const m of result.crop.months) { sum += result.months[m - 1][field]; }
  return sum / result.crop.months.length;
}

function warningCodes(result) { return result.warnings.map((w) => w.code); }

/* A tiny linear congruential generator so the random-scenario sweep is deterministic. */
function lcg(seed) {
  let s = seed >>> 0;
  return function () {
    s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

/* --------------------------------------------------- synthetic calibration data (spec 8.2) */

/*
 * A deliberately artificial pond whose night budget is hopeless without oxygen and fully
 * relieved with it, so that ds = 1 exactly and the arithmetic of MODEL_SPEC section 5 can be
 * pinned against the internal +18 % model. Baseline harvest is 9,000 kg at Rs 120/kg and
 * baseline feed is Rs 2.30 lakh, exactly as spec section 8 test 2 specifies.
 */
const CAL = (function buildCalibrationData() {
  const d = structuredClone(DATA);
  const src = "tests/model.test.mjs synthetic calibration scenario (MODEL_SPEC.md 8.2)";
  const env = (value, unit) => ({ value, unit, status: "ASSUMED", date: "2026-09-21", source: src });

  d.coefficients.respiration_groups.calibration = {
    q_ref_mg_o2_kg_h: env(3000, "mg O2/kg/h"),
    q10: env(1.0, "-"),
    t_ref_c: env(30, "degC"),
    t_cap_c: env(32, "degC")
  };

  const S0 = 0.85, w_h = 500, w0 = 5, fcr = 1.5, kg0 = 9000, feed0 = 230000;
  const density = (kg0 * 1000) / (S0 * w_h);          /* one acre, so n = density */
  const gain0 = kg0 - density * S0 * w0 / 1000;
  const feedPrice = feed0 / (gain0 * fcr);

  d.species.push({
    id: "calibration-fish",
    common_name_en: "Calibration fish",
    common_name_ta: "Calibration fish",
    water_type: "freshwater",
    salinity_ppt: env(0, "ppt"),
    temp_optimum_c: env([0, 50], "degC"),
    temp_tolerable_c: env([-5, 55], "degC"),
    do_minimum_mg_l: env(3.0, "mg/L"),
    do_lethal_mg_l: env(1.0, "mg/L"),
    stocking_density_per_acre: env(density, "fish/acre"),
    seed_size_g: env(w0, "g"),
    culture_period_months: env(6, "months"),
    harvest_size_g: env(w_h, "g"),
    survival_pct: env(S0 * 100, "%"),
    fcr: env(fcr, "kg feed/kg gain"),
    farmgate_price_inr_per_kg: env([0, 1000], "INR/kg"),
    price_default_inr_per_kg: env(120, "INR/kg"),
    seed_cost_inr_per_unit: env(0, "INR"),
    feed_cost_inr_per_kg: env(feedPrice, "INR/kg"),
    other_cost_inr_per_acre_crop: env(0, "INR/acre/crop"),
    crops_per_year_tn: env(1, "crops/yr"),
    stocking_month_tn_default: env(7, "month"),
    respiration_group: "calibration",
    estimable: true,
    missing: []
  });

  d.products.push({
    id: "calibration-unit",
    label: "Calibration unit (unlimited oxygen)",
    power_hp: env(0, "HP"),
    power_kw_shaft: env(0, "kW"),
    o2_input_lpm: env(1e6, "L/min"),
    price_inr: env(null, "INR"),
    concentrator_required: false
  });

  return { data: d, density, feedPrice, kg0, feed0, S0, w_h, w0, fcr };
})();

function calibrationInputs(overrides) {
  const base = OxyModel.defaultsFor("calibration-fish", DEFAULT_DISTRICT, CAL.data);
  return Object.assign(base, {
    area_acre: 1.0,
    depth_m: 1.5,
    unit_model: "calibration-unit",
    price_inr_kg: 120,
    feed_price_inr_kg: CAL.feedPrice,
    tariff_id: "lt4_allied",          /* free supply, so electricity drops out of the delta */
    include_fcr_gain: false
  }, overrides || {});
}

/* ================================================================= 1. DO saturation parity */

test("1. DO saturation matches the Benson & Krause verification table to 0.0005 mg/L", () => {
  const table = COEFF.do_saturation.verification_table_mg_l_1atm.value;
  let worst = 0;
  for (const tKey of Object.keys(table)) {
    for (const sKey of Object.keys(table[tKey])) {
      const got = OxyModel.doSaturation(Number(tKey), Number(sKey), 0, COEFF);
      const delta = Math.abs(got - table[tKey][sKey]);
      worst = Math.max(worst, delta);
      assert.ok(delta < 0.0005,
        `DO sat at ${tKey} degC, ${sKey} ppt: got ${got.toFixed(5)}, table ${table[tKey][sKey]}, delta ${delta}`);
    }
  }
  assert.ok(worst < 0.0005, `worst deviation ${worst}`);
});

test("1b. the pressure factor is exactly 1 at sea level and falls with elevation", () => {
  /*
   * The verification table is quoted at P = 1 atm, so matching it at elevation 0 already shows
   * Fp = 1; this test states it directly by recovering Fp from the ratio of the two calls and
   * checks the published altitude examples in research/do_physics.md (a).
   */
  const atSea = OxyModel.doSaturation(30, 0, 0, COEFF);
  assert.ok(Math.abs(atSea - 7.559) < 0.0005, `sea level 30 degC: ${atSea}`);

  const trichy = OxyModel.doSaturation(30, 0, 88.1, COEFF);
  const coimbatore = OxyModel.doSaturation(30, 0, 395.3, COEFF);
  const kodaikanal = OxyModel.doSaturation(30, 0, 2343, COEFF);
  assert.ok(Math.abs(trichy - 7.477) < 0.001, `Tiruchirappalli 88 m: ${trichy}`);
  assert.ok(Math.abs(coimbatore - 7.198) < 0.001, `Coimbatore 395 m: ${coimbatore}`);
  assert.ok(Math.abs(kodaikanal - 5.646) < 0.001, `Kodaikanal 2343 m: ${kodaikanal}`);
  assert.ok(atSea > trichy && trichy > coimbatore && coimbatore > kodaikanal,
    "saturation must fall monotonically with elevation");

  /* Fp at sea level, recovered as the ratio to the 1 atm value, is 1 to machine precision. */
  assert.equal(atSea / atSea, 1);
});

test("1c. DO saturation matches the published 0.95 atm test vector to 1e-4 mg/L", () => {
  /* research/do_physics.md (a) quotes the full vector at P = 0.95 atm. */
  const formula = COEFF.do_saturation.pressure_from_elevation.value;
  const [g, molar, R, T0] = formula.match(/[0-9]+(?:\.[0-9]+)?/g).map(Number);
  const z = -Math.log(0.95) * R * T0 / (g * molar);
  const vector = [
    [20, 0, 8.6274], [20, 15, 7.8967], [20, 25, 7.4443],
    [25, 0, 7.8372], [25, 15, 7.1964], [25, 25, 6.7986],
    [30, 0, 7.1646], [30, 15, 6.5978], [30, 25, 6.2452],
    [35, 0, 6.5816], [35, 15, 6.0769], [35, 25, 5.7621]
  ];
  for (const [t, s, expected] of vector) {
    const got = OxyModel.doSaturation(t, s, z, COEFF);
    assert.ok(Math.abs(got - expected) < 1e-4, `${t} degC ${s} ppt: got ${got}, expected ${expected}`);
  }
});

test("1d. DO saturation agrees with the published USGS/Boyd values to 0.02 mg/L", () => {
  /* Boyd (2001): 8.24 mg/L at 25 degC freshwater, 1 atm. */
  assert.ok(Math.abs(OxyModel.doSaturation(25, 0, 0, COEFF) - 8.24) <= 0.03,
    "Boyd 2001 quotes 8.24 mg/L at 25 degC; do_physics.md records the +0.02 difference");
  /* Boyd (2018): saturation is 9.28 % greater at 25 than at 30 degC in freshwater. */
  const ratio = OxyModel.doSaturation(25, 0, 0, COEFF) / OxyModel.doSaturation(30, 0, 0, COEFF) - 1;
  assert.ok(Math.abs(ratio - 0.0928) < 0.002, `computed ${(ratio * 100).toFixed(2)} %, published 9.28 %`);
});

/* ============================== pondTemperature and thermalFactor (spec sections 2 and 3) */

test("pondTemperature applies the sourced regression T_w = a + b * T_air", () => {
  const a = COEFF.pond_temperature.a_intercept_c.value;
  const b = COEFF.pond_temperature.b_slope.value;
  for (const tAir of [20, 25, 30, 33, 35]) {
    assert.ok(Math.abs(OxyModel.pondTemperature(tAir, COEFF) - (a + b * tAir)) < 1e-12);
  }
  /* The coefficients file states these three checks in its own note. */
  assert.ok(Math.abs(OxyModel.pondTemperature(30, COEFF) - 30.0) < 0.05);
  assert.ok(Math.abs(OxyModel.pondTemperature(33, COEFF) - 32.7) < 0.05);
  assert.ok(Math.abs(OxyModel.pondTemperature(25, COEFF) - 25.4) < 0.05);
});

test("thermalFactor is the trapezoid on the species' optimum and tolerable limits", () => {
  const sp = DATA.species.find((s) => s.id === DEFAULT_SPECIES);
  const [toLo, toHi] = sp.temp_optimum_c.value;
  const [ttLo, ttHi] = sp.temp_tolerable_c.value;

  assert.equal(OxyModel.thermalFactor((toLo + toHi) / 2, sp, DATA), 1);
  assert.equal(OxyModel.thermalFactor(toLo, sp, DATA), 1);
  assert.equal(OxyModel.thermalFactor(toHi, sp, DATA), 1);
  assert.equal(OxyModel.thermalFactor(ttLo - 0.001, sp, DATA), 0);
  assert.equal(OxyModel.thermalFactor(ttHi + 0.001, sp, DATA), 0);
  assert.equal(OxyModel.thermalFactor(ttLo, sp, DATA), 0);
  assert.equal(OxyModel.thermalFactor(ttHi, sp, DATA), 0);

  const halfLow = ttLo + (toLo - ttLo) / 2;
  const halfHigh = toHi + (ttHi - toHi) / 2;
  assert.ok(Math.abs(OxyModel.thermalFactor(halfLow, sp, DATA) - 0.5) < 1e-12);
  assert.ok(Math.abs(OxyModel.thermalFactor(halfHigh, sp, DATA) - 0.5) < 1e-12);

  /* With the tolerable range absent, the documented fallback margin is applied. */
  const noTolerable = structuredClone(sp);
  noTolerable.temp_tolerable_c.value = null;
  const margin = COEFF.thermal.tolerable_fallback_margin_c.value;
  assert.equal(OxyModel.thermalFactor(toLo - margin - 0.001, noTolerable, DATA), 0);
  assert.ok(Math.abs(OxyModel.thermalFactor(toLo - margin / 2, noTolerable, DATA) - 0.5) < 1e-12);
});

/* ============================================== 2. calibration reproduction (spec 8 test 2) */

test("2. the synthetic calibration scenario reproduces the internal +18 % model", () => {
  const r = OxyModel.evaluate(calibrationInputs(), CAL.data);

  assert.ok(Math.abs(r.crop.ds - 1) < 1e-12, `ds must be forced to 1, got ${r.crop.ds}`);
  assert.ok(Math.abs(r.crop.size_factor - 1) < 1e-12, `size factor must be 1, got ${r.crop.size_factor}`);
  assert.ok(Math.abs(r.baseline.S0 - 0.85) < 1e-12);
  assert.ok(Math.abs(r.baseline.kg - 9000) < 1e-6, `baseline harvest ${r.baseline.kg} kg`);
  assert.ok(Math.abs(r.baseline.revenue - 9000 * 120) < 1e-3);
  assert.ok(Math.abs(r.baseline.feed - 230000) < 1e-3, `baseline feed ${r.baseline.feed}`);

  /* Before clamping: 1.12 * 0.90 / 0.85 = 1.18588. */
  const rawFraction = (r.with_oxy.high.S1 * r.with_oxy.high.w_h1_g) /
                      (r.baseline.S0 * r.baseline.w_h0_g) - 1;
  assert.ok(Math.abs(rawFraction - 0.18588) < 0.001,
    `unclamped extra-kg fraction ${(rawFraction * 100).toFixed(3)} %, expected 18.588 %`);

  /* After clamping: exactly the +18 % ceiling. */
  assert.ok(Math.abs(r.uplift.high.extra_kg_fraction - 0.18) < 1e-12,
    `clamped fraction ${r.uplift.high.extra_kg_fraction}`);
  assert.equal(r.uplift.high.ceiling_clamped, true);
  assert.ok(warningCodes(r).includes("CEILING_CLAMPED"));

  /* Extra revenue about Rs 1.94 lakh, extra feed about Rs 0.41 lakh, net about Rs 1.53 lakh. */
  const lakh = COEFF.economics.lakh.value;
  assert.ok(Math.abs(r.delta.high.revenue_crop / lakh - 1.944) < 0.01,
    `extra revenue Rs ${(r.delta.high.revenue_crop / lakh).toFixed(3)} L`);
  assert.ok(Math.abs(r.delta.high.feed_crop / lakh - 0.41) <= 0.41 * 0.05,
    `extra feed Rs ${(r.delta.high.feed_crop / lakh).toFixed(3)} L, expected about 0.41 L`);
  assert.equal(r.delta.high.elec_crop, 0, "the free-supply tariff must leave electricity unchanged");
  assert.ok(Math.abs(r.delta.high.profit_crop / lakh - 1.53) <= 1.53 * 0.05,
    `net Rs ${(r.delta.high.profit_crop / lakh).toFixed(3)} L, expected about 1.53 L`);

  /* The low case uses half of every uplift coefficient. */
  assert.ok(Math.abs(r.uplift.low.G - COEFF.uplift.growth_max_fraction.value *
    COEFF.uplift.low_case_factor.value) < 1e-12);
  assert.ok(r.uplift.low.extra_kg_fraction < r.uplift.high.extra_kg_fraction);
});

/* ===================================================================== 3. monotonicity */

test("3. increasing stocking density never decreases the crop-mean oxygen stress", () => {
  const base = defaults();
  let previous = -Infinity;
  for (const factor of [0.5, 0.75, 1.0, 1.25, 1.5]) {
    const r = OxyModel.evaluate(defaults({ density_per_acre: base.density_per_acre * factor }), DATA);
    const s = cropMean(r, "s_base");
    assert.ok(s >= previous - 1e-12, `s_base fell from ${previous} to ${s} at density factor ${factor}`);
    previous = s;
  }
});

test("3. increasing existing aeration never increases the crop-mean oxygen stress", () => {
  let previous = Infinity;
  for (const kw of [0, 0.7457, 1.4914, 2.9828, 6]) {
    const r = OxyModel.evaluate(defaults({ existing_aeration_kw: kw, existing_run_h: 8 }), DATA);
    const s = cropMean(r, "s_base");
    assert.ok(s <= previous + 1e-12, `s_base rose from ${previous} to ${s} at ${kw} kW`);
    previous = s;
  }
});

test("3. increasing run hours never decreases the relief ds (unit count held fixed)", () => {
  let previous = -Infinity;
  for (const h of [2, 4, 8, 12, 16, 24]) {
    const r = OxyModel.evaluate(defaults({ run_h: h, n_units: 5 }), DATA);
    assert.ok(r.crop.ds >= previous - 1e-12, `ds fell from ${previous} to ${r.crop.ds} at ${h} h`);
    previous = r.crop.ds;
  }
});

test("3. increasing the number of units never decreases the relief ds", () => {
  let previous = -Infinity;
  for (const n of [1, 2, 4, 8, 12, 20]) {
    const r = OxyModel.evaluate(defaults({ n_units: n }), DATA);
    assert.ok(r.crop.ds >= previous - 1e-12, `ds fell from ${previous} to ${r.crop.ds} at ${n} units`);
    previous = r.crop.ds;
  }
});

test("3. increasing pond area at a fixed density never decreases the relief unit count", () => {
  /* MODEL_SPEC 8.3 was written before amendment A4 renamed n_auto to n_relief. */
  let previous = -Infinity;
  for (const acres of [0.25, 0.5, 1, 2, 5, 10]) {
    const r = OxyModel.evaluate(defaults({ area_acre: acres, n_units: null }), DATA);
    assert.ok(r.unit.n_relief >= previous,
      `n_relief fell from ${previous} to ${r.unit.n_relief} at ${acres} acre`);
    previous = r.unit.n_relief;
  }
});

/* ======================================================= 3a. oxygen supply mass balance */

test("3a. the 1.5 HP unit delivers 962 g O2 per 8 h night and 0.158 mg/L in a 1 acre x 1.5 m pond", () => {
  /*
   * Amendment A9 made o2_input_lpm a range (owner-stated 1-2 L/min for the 1.5 HP unit) and
   * the model uses its midpoint, so the spec 8.3a check at the product page's 2 L/min is made
   * through the datasheet override - which is exactly what that input is for.
   */
  const product = DATA.products.find((p) => p.id === defaults().unit_model);
  const [lpmLow, lpmHigh] = product.o2_input_lpm.value;
  const midpoint = OxyModel.evaluate(defaults({ area_acre: 1.0, depth_m: 1.5, run_h: 8 }), DATA);
  assert.ok(Math.abs(midpoint.unit.o2_input_lpm - (lpmLow + lpmHigh) / 2) < 1e-12,
    `the model must use the midpoint of ${JSON.stringify(product.o2_input_lpm.value)}, got ${midpoint.unit.o2_input_lpm}`);

  const r = OxyModel.evaluate(
    defaults({ area_acre: 1.0, depth_m: 1.5, run_h: 8, o2_input_lpm_override: 2 }), DATA);
  assert.equal(r.unit.o2_input_lpm_used, 2);

  const os = COEFF.oxygen_supply;
  const expectedGrams = 2 * 60 * 8 * os.rho_o2_g_per_l.value * os.purity.value * os.eta_dissolved.value;
  assert.ok(Math.abs(r.unit.o2_g_per_unit_night - expectedGrams) < 1e-9,
    `mass balance: got ${r.unit.o2_g_per_unit_night} g, expected ${expectedGrams} g`);

  /*
   * MODEL_SPEC 4.5 quotes 961 g. At the rounded rho_O2 = 1.31 g/L in coefficients.json the
   * product is 962.064 g; the spec's figure came from the unrounded 32/24.47 = 1.3077 g/L.
   * The difference is 0.11 %, so the check is stated against the spec value at that width.
   */
  assert.ok(Math.abs(r.unit.o2_g_per_unit_night - 961) <= 1.5,
    `spec quotes 961 g; model gives ${r.unit.o2_g_per_unit_night.toFixed(3)} g`);

  const volumeL = 1 * 4046.86 * 1.5 * 1000;
  assert.ok(Math.abs(volumeL - 6.07029e6) < 1, `pond volume ${volumeL} L`);
  assert.ok(Math.abs(r.unit.supply_mg_l_per_unit_night - 0.158) <= 0.001,
    `supply ${r.unit.supply_mg_l_per_unit_night.toFixed(5)} mg/L per unit per night, expected 0.158`);
});

/* =============================================================== 4. the claims ceiling */

test("4. the extra-kg fraction never exceeds the ceiling over 200 seeded scenarios", (t) => {
  const ceiling = COEFF.uplift.ceiling_extra_kg_fraction.value;
  const allDistricts = Object.keys(DATA.climate.district_station_map).sort();
  assert.ok(allDistricts.length > 0, "no districts are mapped to a climate station");

  /* Only species that evaluate at their own defaults enter the sweep. */
  const usable = [];
  const skippedSpecies = [];
  for (const sp of DATA.species) {
    if (sp.estimable === false) { skippedSpecies.push(sp.id + ": not estimable"); continue; }
    try {
      OxyModel.evaluate(OxyModel.defaultsFor(sp.id, DEFAULT_DISTRICT, DATA), DATA);
      usable.push(sp);
    } catch (err) {
      if (!(err instanceof MissingDataError)) { throw err; }
      skippedSpecies.push(sp.id + ": " + err.field);
    }
  }
  assert.ok(usable.length > 0, "no species could be evaluated at their own defaults");
  if (skippedSpecies.length) {
    t.diagnostic("species excluded from the sweep - " + skippedSpecies.join("; "));
  }

  /*
   * Likewise for districts. Any district whose station is incomplete is excluded and named,
   * so the data defect stays visible on every test run instead of being papered over with an
   * assumed value inside the model.
   */
  const districts = [];
  const skippedDistricts = [];
  for (const district of allDistricts) {
    try {
      OxyModel.evaluate(OxyModel.defaultsFor(usable[0].id, district, DATA), DATA);
      districts.push(district);
    } catch (err) {
      if (!(err instanceof MissingDataError)) { throw err; }
      skippedDistricts.push(district + " (" + DATA.climate.district_station_map[district] +
        "): missing " + err.field);
    }
  }
  assert.ok(districts.length > 0, "no district could be evaluated");
  if (skippedDistricts.length) {
    t.diagnostic("DATA DEFECT - districts excluded from the sweep: " + skippedDistricts.join("; "));
  }

  const products = DATA.products.map((p) => p.id);
  const blooms = Object.keys(COEFF.night_budget.r_plankton_ref_mg_l_h_at_25c.value);
  const rand = lcg(20260921);
  const pick = (arr) => arr[Math.floor(rand() * arr.length) % arr.length];

  let worst = -Infinity;
  for (let i = 0; i < 200; i++) {
    const sp = pick(usable);
    const district = pick(districts);
    const inputs = OxyModel.defaultsFor(sp.id, district, DATA);
    inputs.area_acre = 0.25 + rand() * 9.75;
    inputs.depth_m = 0.8 + rand() * 1.7;
    inputs.density_per_acre = inputs.density_per_acre * (0.5 + rand());
    inputs.stock_month = 1 + Math.floor(rand() * 12);
    inputs.bloom = pick(blooms);
    inputs.existing_aeration_kw = rand() < 0.5 ? 0 : rand() * 15;
    inputs.existing_run_h = 1 + rand() * 23;
    inputs.run_h = 2 + rand() * 22;
    inputs.unit_model = pick(products);
    inputs.n_units = rand() < 0.5 ? null : 1 + Math.floor(rand() * 20);
    inputs.include_fcr_gain = rand() < 0.5;
    inputs.unit_price_inr = rand() < 0.5 ? null : 20000 + rand() * 200000;
    inputs.subsidy_pct = pick([0, 40, 60]);

    const r = OxyModel.evaluate(inputs, DATA);
    worst = Math.max(worst, r.uplift.high.extra_kg_fraction);
    assert.ok(r.uplift.high.extra_kg_fraction <= ceiling + 1e-12,
      `scenario ${i} (${sp.id}, ${district}) gave ${r.uplift.high.extra_kg_fraction}`);
    assert.ok(r.uplift.low.extra_kg_fraction <= r.uplift.high.extra_kg_fraction + 1e-12,
      `scenario ${i}: the low case exceeded the high case`);
    assert.ok(r.delta.high.kg_crop <= r.baseline.kg * (ceiling + 1e-12),
      `scenario ${i}: reported extra kg exceeded the ceiling`);
    assert.ok(r.crop.ds >= 0 && r.crop.ds <= 1, `scenario ${i}: ds out of range (${r.crop.ds})`);
  }
  assert.ok(worst <= ceiling + 1e-12, `worst extra-kg fraction over the sweep: ${worst}`);
});

/* ==================================================================== 5. fail-loud cases */

test("5. a species with a null growth DO threshold throws MissingDataError naming the field", () => {
  const broken = structuredClone(DATA);
  const sp = broken.species.find((s) => s.id === DEFAULT_SPECIES);
  sp.do_minimum_mg_l.value = null;
  sp.do_minimum_mg_l.status = "NOT_FOUND";
  assert.throws(
    () => OxyModel.evaluate(OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, broken), broken),
    (err) => err instanceof MissingDataError &&
             err.field === "do_minimum_mg_l" &&
             err.species === DEFAULT_SPECIES &&
             /do_minimum_mg_l/.test(err.message)
  );
});

test("5. a product with a null oxygen input throws MissingDataError", () => {
  const broken = structuredClone(DATA);
  const inputs = OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, broken);
  const product = broken.products.find((p) => p.id === inputs.unit_model);
  product.o2_input_lpm.value = null;
  product.o2_input_lpm.status = "NOT_FOUND";
  assert.throws(
    () => OxyModel.evaluate(inputs, broken),
    (err) => err instanceof MissingDataError && err.field === "o2_input_lpm"
  );
});

test("5. a null unit price blocks payback with the message 'enter unit price'", () => {
  const r = OxyModel.evaluate(defaults({ unit_price_inr: null }), DATA);
  assert.equal(r.payback.status, "blocked");
  assert.equal(r.payback.reason, "enter unit price");
  assert.equal(r.payback.capex, null);
  assert.equal(r.payback.months_low, null);
  assert.equal(r.payback.months_high, null);
});

test("5. a null concentrator power is excluded from electricity and warns", () => {
  const withNull = OxyModel.evaluate(defaults({ concentrator_kw: null }), DATA);
  const withZero = OxyModel.evaluate(defaults({ concentrator_kw: 0 }), DATA);
  const withHalf = OxyModel.evaluate(defaults({ concentrator_kw: 0.5 }), DATA);

  assert.ok(warningCodes(withNull).includes("CONCENTRATOR_POWER_UNKNOWN"));
  assert.ok(!warningCodes(withZero).includes("CONCENTRATOR_POWER_UNKNOWN"));
  assert.equal(withNull.with_oxy.high.elec, withZero.with_oxy.high.elec,
    "a null concentrator power must behave as if it drew nothing");
  assert.ok(withHalf.with_oxy.high.elec > withZero.with_oxy.high.elec,
    "a stated concentrator power must raise the electricity cost");
});

test("A8. a not-estimable species throws MissingDataError naming missing[0] and the species", () => {
  /*
   * MODEL_SPEC 7 amendment A8: the field reported is the data file's own `missing[0]`, not
   * whichever load-bearing field this implementation reads first, so both sides of the parity
   * comparison blame the same field. Every not-estimable species in the built data is checked.
   */
  const notEstimable = DATA.species.filter((s) => s.estimable === false);
  assert.ok(notEstimable.length > 0, "the built data should carry some not-estimable species");

  for (const sp of notEstimable) {
    assert.ok(Array.isArray(sp.missing) && sp.missing.length > 0,
      `${sp.id} is not estimable but carries no missing[] list`);
    const inputs = Object.assign(defaults(), {
      species: sp.id, district: DEFAULT_DISTRICT, density_per_acre: 2000
    });
    assert.throws(
      () => OxyModel.evaluate(inputs, DATA),
      (err) => err instanceof MissingDataError &&
               err.field === sp.missing[0] &&
               err.species === sp.id,
      `${sp.id} should throw MissingDataError naming ${sp.missing[0]}`
    );
  }

  /* the species, not the district, is blamed: an unknown district must not mask it */
  const improved = notEstimable.find((s) => s.id === "improved-strains");
  if (improved) {
    assert.throws(
      () => OxyModel.evaluate(Object.assign(defaults(), {
        species: "improved-strains", district: "Atlantis", density_per_acre: 2000
      }), DATA),
      (err) => err instanceof MissingDataError && err.field === improved.missing[0]
    );
  }
});

test("5. an unknown species, district, product or tariff throws MissingDataError", () => {
  assert.throws(() => OxyModel.defaultsFor("no-such-species", DEFAULT_DISTRICT, DATA),
    (err) => err instanceof MissingDataError && err.field === "species");
  assert.throws(() => OxyModel.evaluate(defaults({ district: "Atlantis" }), DATA),
    (err) => err instanceof MissingDataError && err.field === "district_station_map");
  assert.throws(() => OxyModel.evaluate(defaults({ unit_model: "no-such-product" }), DATA),
    (err) => err instanceof MissingDataError && err.field === "products");
  assert.throws(() => OxyModel.evaluate(defaults({ tariff_id: "no-such-tariff" }), DATA),
    (err) => err instanceof MissingDataError && err.field === "tariff_id");
  assert.throws(() => OxyModel.doSaturation(30, 0, 0, null),
    (err) => err instanceof MissingDataError && err.field === "coefficients");
});

/* ============================================================== one test per warning code */

test("warning THERMAL_OUT_OF_RANGE fires when a crop month is outside the tolerable range", () => {
  const reference = OxyModel.evaluate(defaults(), DATA);
  const temps = reference.months.map((m) => m.t_w_c);
  const minTw = Math.min(...temps);
  const coldestMonth = temps.indexOf(minTw) + 1;

  const cold = structuredClone(DATA);
  const sp = cold.species.find((s) => s.id === DEFAULT_SPECIES);
  sp.temp_tolerable_c.value = [minTw + 0.5, 65];
  sp.temp_optimum_c.value = [minTw + 0.6, 60];

  const r = OxyModel.evaluate(
    Object.assign(OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, cold),
      { stock_month: coldestMonth }), cold);
  const w = r.warnings.find((x) => x.code === "THERMAL_OUT_OF_RANGE");
  assert.ok(w, `expected THERMAL_OUT_OF_RANGE, got ${warningCodes(r).join(", ")}`);
  assert.ok(w.months.includes(coldestMonth), `months ${JSON.stringify(w.months)}`);
  assert.equal(r.months[coldestMonth - 1].g_t, 0);
});

test("warning CEILING_CLAMPED fires when the modelled uplift exceeds the +18 % ceiling", () => {
  const r = OxyModel.evaluate(calibrationInputs(), CAL.data);
  assert.ok(warningCodes(r).includes("CEILING_CLAMPED"));
  assert.equal(r.uplift.high.ceiling_clamped, true);
});

test("warning SIZING_CAPPED fires when the pond needs more units than the cap", () => {
  const cap = COEFF.sizing.n_units_cap.value;
  const inputs = calibrationInputs({ area_acre: 2.0, unit_model: "nbg-1.5hp", n_units: null });
  const r = OxyModel.evaluate(inputs, CAL.data);
  assert.ok(r.unit.deficit_max_mg_l > 0, "the probe pond must be oxygen-limited");
  assert.equal(r.unit.n_relief, cap);
  assert.ok(warningCodes(r).includes("SIZING_CAPPED"),
    `expected SIZING_CAPPED, got ${warningCodes(r).join(", ")}`);
});

test("warning CONCENTRATOR_POWER_UNKNOWN fires only when the concentrator power is unknown", () => {
  /*
   * Amendment A9.1 put the owner's 0.69 kW on the product, so the default scenario no longer
   * warns; the warning now marks a product (or a user entry) with no concentrator power, which
   * is the same condition under which it is left out of the electricity cost.
   */
  const withOwnerFigure = OxyModel.evaluate(defaults(), DATA);
  assert.ok(!warningCodes(withOwnerFigure).includes("CONCENTRATOR_POWER_UNKNOWN"),
    "the owner's concentrator figure is on the product, so the default must not warn");
  assert.ok(withOwnerFigure.unit.concentrator_kw > 0);

  const unknown = structuredClone(DATA);
  const product = unknown.products.find((p) => p.id === defaults().unit_model);
  product.concentrator_kw.value = null;
  product.concentrator_kw.status = "NOT_FOUND";
  const r = OxyModel.evaluate(OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, unknown), unknown);
  assert.ok(warningCodes(r).includes("CONCENTRATOR_POWER_UNKNOWN"),
    `expected CONCENTRATOR_POWER_UNKNOWN, got ${warningCodes(r).join(", ")}`);
  assert.equal(r.unit.concentrator_kw, null);
});

test("warning PRICE_OUT_OF_SOURCED_RANGE fires above and below the sourced range", () => {
  const sp = DATA.species.find((s) => s.id === DEFAULT_SPECIES);
  const [low, high] = sp.farmgate_price_inr_per_kg.value;
  const above = OxyModel.evaluate(defaults({ price_inr_kg: high + 100 }), DATA);
  const below = OxyModel.evaluate(defaults({ price_inr_kg: Math.max(low - 50, 1) }), DATA);
  const inside = OxyModel.evaluate(defaults({ price_inr_kg: (low + high) / 2 }), DATA);
  assert.ok(warningCodes(above).includes("PRICE_OUT_OF_SOURCED_RANGE"));
  assert.ok(warningCodes(below).includes("PRICE_OUT_OF_SOURCED_RANGE"));
  assert.ok(!warningCodes(inside).includes("PRICE_OUT_OF_SOURCED_RANGE"));
});

test("warning NOT_OXYGEN_LIMITED fires when the pond is barely stressed", () => {
  const r = OxyModel.evaluate(calibrationInputs({ density_per_acre: 100, bloom: "light" }), CAL.data);
  assert.ok(cropMean(r, "s_base") < 0.05, `crop-mean s_base ${cropMean(r, "s_base")}`);
  assert.ok(warningCodes(r).includes("NOT_OXYGEN_LIMITED"),
    `expected NOT_OXYGEN_LIMITED, got ${warningCodes(r).join(", ")}`);
  assert.ok(r.crop.ds < 0.05, "a pond that is not oxygen-limited has almost nothing to relieve");
});

test("warning NO_PAYBACK_AT_PUBLISHED_O2 fires when no unit count turns a profit", () => {
  /* A pond with nothing to relieve: the uplift is zero at every n while electricity is not. */
  const starved = calibrationInputs({
    density_per_acre: 100, bloom: "light", unit_model: "nbg-1.5hp",
    tariff_id: "lt3a1_high", n_units: null
  });
  const r = OxyModel.evaluate(starved, CAL.data);
  assert.ok(warningCodes(r).includes("NO_PAYBACK_AT_PUBLISHED_O2"),
    `expected NO_PAYBACK_AT_PUBLISHED_O2, got ${warningCodes(r).join(", ")}`);
  assert.ok(r.delta.high.profit_year <= 0, `annual delta ${r.delta.high.profit_year}`);
  assert.equal(r.unit.n_best, 1, "with no relief on offer the cheapest count is the best one");

  const cap = COEFF.sizing.n_units_cap.value;
  for (let n = 1; n <= cap; n++) {
    const trial = OxyModel.evaluate(Object.assign({}, starved, { n_units: n }), CAL.data);
    assert.ok(trial.delta.high.profit_year <= 0,
      `n = ${n} turned a profit of ${trial.delta.high.profit_year}, so the warning is wrong`);
  }

  /* The counter-case: relief worth having and free electricity, so the warning must not fire. */
  const paying = OxyModel.evaluate(calibrationInputs({ n_units: null }), CAL.data);
  assert.ok(!warningCodes(paying).includes("NO_PAYBACK_AT_PUBLISHED_O2"));
  assert.ok(paying.delta.high.profit_year > 0);
});

/* ================================================== amendment A4: sizing and the overrides */

test("A4. n_best maximises the high-case annual extra profit and is the smallest such count", () => {
  const cap = COEFF.sizing.n_units_cap.value;
  const scenarios = [
    defaults(),
    defaults({ area_acre: 3, depth_m: 2.0 }),
    defaults({ tariff_id: "lt4_allied" }),
    defaults({ o2_input_lpm_override: 30 })
  ];
  for (const inputs of scenarios) {
    const auto = OxyModel.evaluate(Object.assign({}, inputs, { n_units: null }), DATA);
    assert.equal(auto.unit.sizing, "auto");
    assert.equal(auto.unit.n_units, auto.unit.n_best, "auto sizing must use n_best");
    assert.ok(auto.unit.n_best >= 1 && auto.unit.n_best <= cap);

    const profits = [];
    for (let n = 1; n <= cap; n++) {
      profits.push(OxyModel.evaluate(Object.assign({}, inputs, { n_units: n }), DATA)
        .delta.high.profit_year);
    }
    const bestProfit = profits[auto.unit.n_best - 1];
    for (let n = 1; n <= cap; n++) {
      assert.ok(bestProfit >= profits[n - 1] - 1e-9,
        `n_best = ${auto.unit.n_best} gives ${bestProfit} but n = ${n} gives ${profits[n - 1]}`);
    }
    /* ties resolve to the smaller n */
    for (let n = 1; n < auto.unit.n_best; n++) {
      assert.ok(profits[n - 1] < bestProfit - 1e-12,
        `n = ${n} matches the best profit, so n_best should have been ${n}`);
    }
    /* n_relief is reported alongside and is deliberately not constrained against n_best */
    assert.ok(auto.unit.n_relief >= 1 && auto.unit.n_relief <= cap);
  }
});

test("A4. a manual unit count overrides n_best and is reported against it", () => {
  const auto = OxyModel.evaluate(defaults({ n_units: null }), DATA);
  const manual = OxyModel.evaluate(defaults({ n_units: 3 }), DATA);
  assert.equal(manual.unit.sizing, "manual");
  assert.equal(manual.unit.n_units, 3);
  assert.equal(manual.unit.n_best, auto.unit.n_best, "n_best is reported whatever the user chose");
  assert.equal(manual.unit.n_relief, auto.unit.n_relief);
});

test("A4. o2_input_lpm_override replaces the product oxygen delivery and scales the supply", () => {
  const published = OxyModel.evaluate(defaults({ n_units: 4 }), DATA);
  const factor = 10;
  const overridden = OxyModel.evaluate(
    defaults({ n_units: 4, o2_input_lpm_override: published.unit.o2_input_lpm * factor }), DATA);

  assert.equal(published.unit.o2_input_lpm_used, published.unit.o2_input_lpm,
    "a null override must leave the published value in force");
  assert.equal(overridden.unit.o2_input_lpm, published.unit.o2_input_lpm,
    "the product page figure must still be reported");
  assert.equal(overridden.unit.o2_input_lpm_used, published.unit.o2_input_lpm * factor);

  for (const field of ["o2_g_per_unit_night", "supply_mg_l_per_unit_night"]) {
    assert.ok(Math.abs(overridden.unit[field] - published.unit[field] * factor) < 1e-9,
      `${field}: ${overridden.unit[field]} is not ${factor}x ${published.unit[field]}`);
  }
  assert.ok(overridden.crop.ds >= published.crop.ds - 1e-12,
    "more oxygen per unit cannot reduce the relief at the same unit count");
  assert.ok(overridden.unit.n_relief <= published.unit.n_relief,
    "more oxygen per unit cannot need more units to reach the growth threshold");
  assert.equal(overridden.inputs_resolved.o2_input_lpm_override.value,
    published.unit.o2_input_lpm * factor);
  assert.ok(overridden.assumptions.some((a) => a.id === "input.o2_input_lpm_override"));
});

test("A4. power_kw_override replaces the shaft power in the electricity cost", () => {
  const published = OxyModel.evaluate(defaults({ n_units: 4 }), DATA);
  const lower = OxyModel.evaluate(
    defaults({ n_units: 4, power_kw_override: published.unit.power_kw_shaft / 2 }), DATA);
  const higher = OxyModel.evaluate(
    defaults({ n_units: 4, power_kw_override: published.unit.power_kw_shaft * 2 }), DATA);

  assert.equal(published.unit.power_kw_used, published.unit.power_kw_shaft);
  assert.equal(lower.unit.power_kw_shaft, published.unit.power_kw_shaft,
    "the published shaft power must still be reported");
  assert.equal(lower.unit.power_kw_used, published.unit.power_kw_shaft / 2);
  assert.ok(lower.with_oxy.high.elec < published.with_oxy.high.elec);
  assert.ok(higher.with_oxy.high.elec > published.with_oxy.high.elec);
  assert.equal(lower.crop.ds, published.crop.ds, "electrical input must not change the physics");
  assert.ok(lower.assumptions.some((a) => a.id === "input.power_kw_override"));
});

test("A4. defaultsFor prefers the yield-consistent density and falls back to the sourced midpoint", () => {
  const withDefault = structuredClone(DATA);
  const sp = withDefault.species.find((s) => s.id === DEFAULT_SPECIES);
  sp.density_default_per_acre = {
    value: 4321, unit: "fingerlings/acre", status: "ASSUMED", date: "2026-09-21",
    source: "tests/model.test.mjs amendment A4 check", fallback_rule: "yield_consistent_density"
  };
  assert.equal(OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, withDefault).density_per_acre, 4321);
  const resolvedDensity = OxyModel.evaluate(
    OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, withDefault), withDefault)
    .inputs_resolved.density_per_acre;
  assert.equal(resolvedDensity.value, 4321);
  assert.equal(resolvedDensity.source, "tests/model.test.mjs amendment A4 check");

  const withoutDefault = structuredClone(DATA);
  const sp2 = withoutDefault.species.find((s) => s.id === DEFAULT_SPECIES);
  delete sp2.density_default_per_acre;
  const [lowDensity, highDensity] = sp2.stocking_density_per_acre.value;
  assert.equal(OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, withoutDefault).density_per_acre,
    (lowDensity + highDensity) / 2);
});

/* ========================================== amendment A6: out-of-crop months in the strip */

test("A6. an out-of-crop month carries the crop-mean biomass, not the harvest value", () => {
  const r = OxyModel.evaluate(defaults(), DATA);
  const inCrop = r.months.filter((m) => m.in_crop);
  const outOfCrop = r.months.filter((m) => !m.in_crop);
  assert.ok(inCrop.length > 0 && outOfCrop.length > 0,
    "the default crop must leave some months outside the crop window");

  const mean = inCrop.reduce((a, m) => a + m.biomass_kg, 0) / inCrop.length;
  const harvest = Math.max(...inCrop.map((m) => m.biomass_kg));
  for (const m of outOfCrop) {
    assert.ok(Math.abs(m.biomass_kg - mean) < 1e-9,
      `month ${m.m}: biomass ${m.biomass_kg} is not the crop mean ${mean}`);
  }
  assert.ok(mean < harvest - 1e-6,
    "the crop mean must differ from the harvest value, or the test cannot tell them apart");
});

test("A6. dawn DO and the stress index of an out-of-crop month follow from the crop-mean biomass", () => {
  const base = OxyModel.evaluate(defaults(), DATA);
  const inCrop = base.months.filter((m) => m.in_crop);
  const mean = inCrop.reduce((a, m) => a + m.biomass_kg, 0) / inCrop.length;
  const harvest = Math.max(...inCrop.map((m) => m.biomass_kg));
  const probe = base.months.find((m) => !m.in_crop);

  /*
   * Biomass is exactly proportional to the stocking density, so scaling the density by
   * harvest/mean puts the out-of-crop months at the harvest biomass - which is what the
   * superseded behaviour produced. The default run must not match it, and must sit above it,
   * because less biomass means less respiration and a higher dawn DO.
   */
  const atHarvest = OxyModel.evaluate(
    defaults({ density_per_acre: defaults().density_per_acre * (harvest / mean) }), DATA);
  const probeAtHarvest = atHarvest.months[probe.m - 1];
  assert.ok(Math.abs(probeAtHarvest.biomass_kg - harvest) < 1e-6,
    "the probe run should hold the out-of-crop months at the harvest biomass");
  assert.ok(probe.do_dawn_base > probeAtHarvest.do_dawn_base + 1e-9,
    `month ${probe.m}: dawn DO ${probe.do_dawn_base} must be above the harvest-biomass value ` +
    `${probeAtHarvest.do_dawn_base}, so it is computed from the crop mean`);

  /* s_base and s_oxy follow from the reported dawn DO, for every month in the strip. */
  const doMin = base.assumptions.find((a) => a.id === "species.do_minimum_mg_l").value;
  const doLethal = base.assumptions.find((a) => a.id === "species.do_lethal_mg_l").value;
  assert.ok(doMin > doLethal, "the growth threshold must sit above the lethal level");
  for (const m of base.months) {
    for (const [dawn, s] of [[m.do_dawn_base, m.s_base], [m.do_dawn_oxy, m.s_oxy]]) {
      const expected = Math.min(Math.max((doMin - dawn) / (doMin - doLethal), 0), 1);
      assert.ok(Math.abs(s - expected) < 1e-12,
        `month ${m.m}: stress ${s} does not follow from dawn DO ${dawn} (expected ${expected})`);
    }
  }
});

/* ================================================================= determinism and shape */

test("evaluate is deterministic: the same inputs give a deeply equal result", () => {
  const inputs = defaults();
  const first = OxyModel.evaluate(inputs, DATA);
  const second = OxyModel.evaluate(defaults(), DATA);
  const third = OxyModel.evaluate(inputs, loadData());
  assert.deepStrictEqual(first, second);
  assert.deepStrictEqual(JSON.parse(JSON.stringify(first)), JSON.parse(JSON.stringify(third)));
  assert.deepStrictEqual(inputs, defaults(), "evaluate must not mutate its inputs");
});

test("the result carries the shape EXECUTION_PLAN section 4.2 specifies", () => {
  const r = OxyModel.evaluate(defaults(), DATA);
  for (const key of ["inputs_resolved", "station", "months", "crop", "uplift", "baseline",
                     "with_oxy", "delta", "payback", "unit", "warnings", "assumptions"]) {
    assert.ok(Object.prototype.hasOwnProperty.call(r, key), `result is missing ${key}`);
  }
  assert.equal(r.months.length, 12);
  for (const m of r.months) {
    for (const key of ["m", "t_air_c", "t_w_c", "c_s_mg_l", "g_t", "in_crop", "biomass_kg",
                       "do_dawn_base", "do_dawn_oxy", "s_base", "s_oxy"]) {
      assert.ok(Object.prototype.hasOwnProperty.call(m, key), `month ${m.m} is missing ${key}`);
    }
    assert.ok(m.do_dawn_base >= 0 && m.do_dawn_base <= m.c_s_mg_l + 1e-12,
      `month ${m.m}: dawn DO ${m.do_dawn_base} outside [0, ${m.c_s_mg_l}]`);
    assert.ok(m.do_dawn_oxy >= m.do_dawn_base - 1e-12);
    assert.ok(m.s_base >= 0 && m.s_base <= 1 && m.s_oxy >= 0 && m.s_oxy <= 1);
    assert.ok(m.g_t >= 0 && m.g_t <= 1);
  }
  assert.equal(r.crop.months.length, Math.round(
    (DATA.species.find((s) => s.id === DEFAULT_SPECIES).culture_period_months.value[0] +
     DATA.species.find((s) => s.id === DEFAULT_SPECIES).culture_period_months.value[1]) / 2));

  /* every assumption carries a status and a source, so the UI can list it */
  assert.ok(r.assumptions.length > 10, `only ${r.assumptions.length} assumptions recorded`);
  const allowed = new Set(["VERIFIED", "ASSUMED", "UNTESTED", "NOT_FOUND", "COMPUTED"]);
  for (const a of r.assumptions) {
    assert.ok(typeof a.id === "string" && a.id.length > 0);
    assert.ok(typeof a.label === "string" && a.label.length > 0);
    assert.ok(allowed.has(a.status), `assumption ${a.id} has status '${a.status}'`);
  }
  const ids = r.assumptions.map((a) => a.id);
  assert.equal(new Set(ids).size, ids.length, "assumption ids must be unique");

  /* the unit block carries the fields amendment A4 added */
  for (const key of ["id", "label", "power_kw_shaft", "power_kw_used", "o2_input_lpm",
                     "o2_input_lpm_used", "price_inr", "concentrator_kw", "concentrator_price_inr",
                     "maintenance_pct", "n_units", "n_best", "n_relief", "sizing",
                     "o2_g_per_unit_night", "supply_mg_l_per_unit_night", "deficit_max_mg_l",
                     "status"]) {
    assert.ok(Object.prototype.hasOwnProperty.call(r.unit, key), `result.unit is missing ${key}`);
  }
  /* A9: both delta cases carry the annual maintenance charge */
  for (const side of ["low", "high"]) {
    for (const key of ["kg_crop", "kg_year", "revenue_crop", "feed_crop", "elec_crop",
                       "profit_crop", "maintenance_year", "profit_year"]) {
      assert.ok(Object.prototype.hasOwnProperty.call(r.delta[side], key),
        `result.delta.${side} is missing ${key}`);
    }
  }
  /* A9: the three new inputs are reported back */
  for (const key of ["concentrator_price_inr", "maintenance_pct", "station_name"]) {
    assert.ok(Object.prototype.hasOwnProperty.call(r.inputs_resolved, key),
      `inputs_resolved is missing ${key}`);
  }
  assert.ok(!Object.prototype.hasOwnProperty.call(r.unit, "n_auto"),
    "n_auto was replaced by n_best and n_relief in amendment A4");

  /* every warning uses one of the seven documented codes */
  const codes = new Set(["THERMAL_OUT_OF_RANGE", "CEILING_CLAMPED", "SIZING_CAPPED",
    "CONCENTRATOR_POWER_UNKNOWN", "PRICE_OUT_OF_SOURCED_RANGE", "NOT_OXYGEN_LIMITED",
    "NO_PAYBACK_AT_PUBLISHED_O2"]);
  for (const w of r.warnings) {
    assert.ok(codes.has(w.code), `undocumented warning code ${w.code}`);
    assert.ok(typeof w.message === "string" && w.message.length > 0);
  }
});

test("the default scenario reproduces the sourced harvest size exactly (size factor 1)", () => {
  const sp = DATA.species.find((s) => s.id === DEFAULT_SPECIES);
  const published = (sp.harvest_size_g.value[0] + sp.harvest_size_g.value[1]) / 2;
  const r = OxyModel.evaluate(defaults(), DATA);
  assert.ok(Math.abs(r.crop.size_factor - 1) < 1e-12,
    `the default scenario is the reference crop, so the size factor must be 1, got ${r.crop.size_factor}`);
  assert.ok(Math.abs(r.baseline.w_h0_g - published) < 1e-9);
});

test("payback is blocked when the annual profit delta is not positive", () => {
  /* A pond that is not oxygen-limited wins nothing, so there is nothing to pay the unit back. */
  const r = OxyModel.evaluate(
    calibrationInputs({ density_per_acre: 100, bloom: "light", unit_price_inr: 50000 }), CAL.data);
  assert.ok(r.delta.high.profit_year <= 0, `annual delta ${r.delta.high.profit_year}`);
  assert.equal(r.payback.status, "blocked");
  assert.equal(r.payback.reason, "No extra profit at these inputs");
  assert.ok(r.payback.capex > 0, "capex is still reported so the farmer sees the cost");
});

/* ============ amendment A9: product economics, city selection and the station comparison ==== */

test("A9. defaults take the price, concentrator and maintenance from the product data", () => {
  const inputs = defaults();
  const product = DATA.products.find((p) => p.id === inputs.unit_model);
  assert.equal(inputs.unit_price_inr, product.price_inr.value);
  assert.equal(inputs.concentrator_kw, product.concentrator_kw.value);
  assert.equal(inputs.concentrator_price_inr, product.concentrator_price_inr.value);
  assert.equal(inputs.maintenance_pct, product.maintenance_pct_per_year.value);
  assert.equal(inputs.station_name, null);

  const r = OxyModel.evaluate(inputs, DATA);
  assert.notEqual(r.payback.reason, "enter unit price",
    "the price now comes from the product, so payback must never be blocked for want of one");
  if (r.delta.high.profit_year > 0) {
    assert.equal(r.payback.status, "ok");
    assert.ok(isFinite(r.payback.months_high) && r.payback.months_high > 0);
  } else {
    assert.equal(r.payback.status, "blocked");
    assert.equal(r.payback.reason, "No extra profit at these inputs");
    assert.ok(r.payback.capex > 0, "the capex is still reported when the payback is blocked");
  }
  /* the price and maintenance are rough estimates and must say so */
  const priceNote = r.assumptions.find((a) => a.id === "product.price_inr");
  assert.ok(priceNote && priceNote.status === "ASSUMED", "the unit price must carry its ASSUMED badge");
});

test("A9. capex and annual maintenance follow the unit plus concentrator price", () => {
  const price = 85000;
  const concentrator = 45000;
  const maint = 3;
  const n = 4;
  const inputs = defaults({
    n_units: n, unit_price_inr: price, concentrator_price_inr: concentrator,
    maintenance_pct: maint, subsidy_pct: 0
  });
  const r = OxyModel.evaluate(inputs, DATA);
  const basis = n * (price + concentrator);

  assert.ok(Math.abs(r.payback.capex - basis) < 1e-9, `capex ${r.payback.capex}, expected ${basis}`);
  for (const side of ["low", "high"]) {
    assert.ok(Math.abs(r.delta[side].maintenance_year - basis * maint / 100) < 1e-9,
      `${side} maintenance ${r.delta[side].maintenance_year}, expected ${basis * maint / 100}`);
    assert.ok(Math.abs(r.delta[side].profit_year -
      (r.delta[side].profit_crop * r.assumptions.find((a) => a.id === "species.crops_per_year_tn").value
       - r.delta[side].maintenance_year)) < 1e-6,
      `${side}: profit_year must be crop profit x crops minus maintenance`);
  }

  /* the subsidy reduces capex but not maintenance, which is charged on the full price */
  const subsidised = OxyModel.evaluate(Object.assign({}, inputs, { subsidy_pct: 40 }), DATA);
  assert.ok(Math.abs(subsidised.payback.capex - basis * 0.6) < 1e-9);
  assert.equal(subsidised.delta.high.maintenance_year, r.delta.high.maintenance_year);

  /* maintenance scales with the unit count, so it enters the n_best scan */
  const one = OxyModel.evaluate(Object.assign({}, inputs, { n_units: 1 }), DATA);
  assert.ok(Math.abs(one.delta.high.maintenance_year * n - r.delta.high.maintenance_year) < 1e-9);

  /* a null unit price blocks payback and leaves maintenance unknown rather than zero */
  const noPrice = OxyModel.evaluate(Object.assign({}, inputs, { unit_price_inr: null }), DATA);
  assert.equal(noPrice.payback.status, "blocked");
  assert.equal(noPrice.payback.reason, "enter unit price");
  assert.equal(noPrice.delta.high.maintenance_year, null);
});

test("A9. station_name drives the climate while the reference crop stays at Tiruchirappalli", () => {
  const home = OxyModel.evaluate(defaults(), DATA);
  const away = OxyModel.evaluate(defaults({ station_name: "Kodaikanal" }), DATA);

  assert.equal(home.station.name, DATA.climate.district_station_map[DEFAULT_DISTRICT]);
  assert.equal(away.station.name, "Kodaikanal");
  assert.equal(away.station.district, "Dindigul");
  assert.equal(away.inputs_resolved.station_name.value, "Kodaikanal");
  assert.equal(home.inputs_resolved.station_name.value, null);
  assert.equal(away.inputs_resolved.district.value, DEFAULT_DISTRICT,
    "the district is unchanged; only the climate station moves");

  const moved = home.months.filter((m, i) => Math.abs(m.t_w_c - away.months[i].t_w_c) > 0.5);
  assert.equal(moved.length, 12, "every month's water temperature must change with the station");
  assert.ok(away.crop.G_T < home.crop.G_T, "a hill station must suppress the thermal factor");
  assert.ok(Math.abs(away.crop.G_T_ref - home.crop.G_T_ref) < 1e-12,
    "the reference crop stays at Tiruchirappalli, so G_T_ref must not move");

  assert.throws(() => OxyModel.evaluate(defaults({ station_name: "Atlantis" }), DATA),
    (err) => err instanceof MissingDataError && err.field === "station_name");
});

test("A9. compareStations returns one row per station and matches evaluate on the home station", () => {
  const inputs = defaults();
  const rows = OxyModel.compareStations(inputs, DATA);
  assert.equal(rows.length, DATA.climate.stations.length);
  assert.equal(rows.length, 32);
  rows.forEach((row, i) => assert.equal(row.station, DATA.climate.stations[i].name,
    "rows must follow the climate data file's order"));

  const home = OxyModel.evaluate(Object.assign({}, inputs, { n_units: null }), DATA);
  const homeRow = rows.find((row) => row.station === home.station.name);
  assert.ok(homeRow, `no row for the home station ${home.station.name}`);
  assert.ok(!homeRow.error, `the home station errored: ${homeRow.error}`);
  assert.equal(homeRow.G_T, home.crop.G_T);
  assert.equal(homeRow.size_factor, home.crop.size_factor);
  assert.equal(homeRow.harvest_size_g, home.baseline.w_h0_g);
  assert.equal(homeRow.baseline_kg_crop, home.baseline.kg);
  assert.equal(homeRow.ds, home.crop.ds);
  assert.equal(homeRow.extra_kg_crop_high, home.delta.high.kg_crop);
  assert.equal(homeRow.profit_year_high, home.delta.high.profit_year);
  assert.equal(homeRow.n_best, home.unit.n_best);
  assert.deepStrictEqual(homeRow.warnings, home.warnings.map((w) => w.code));
  assert.equal(homeRow.district, DATA.climate.stations.find((s) => s.name === home.station.name).district);

  for (const row of rows) {
    if (row.error) { assert.equal(typeof row.error, "string"); continue; }
    for (const key of ["station", "district", "elevation_m", "G_T", "size_factor", "harvest_size_g",
                       "baseline_kg_crop", "ds", "extra_kg_crop_high", "profit_year_high",
                       "n_best", "warnings"]) {
      assert.ok(Object.prototype.hasOwnProperty.call(row, key), `${row.station} is missing ${key}`);
    }
  }

  /* a manual unit count in the inputs must not leak into the comparison: A9.4 sizes each city */
  const manualRows = OxyModel.compareStations(defaults({ n_units: 17 }), DATA);
  assert.deepStrictEqual(manualRows, rows, "compareStations always sizes automatically");

  /* a station that cannot be evaluated is reported, not thrown */
  const broken = structuredClone(DATA);
  broken.climate.stations[0].elevation_m = null;
  const brokenRows = OxyModel.compareStations(
    OxyModel.defaultsFor(DEFAULT_SPECIES, DEFAULT_DISTRICT, broken), broken);
  assert.equal(brokenRows.length, 32);
  assert.equal(brokenRows[0].station, broken.climate.stations[0].name);
  assert.equal(brokenRows[0].error, "elevation_m");
});

test("A9. a hill station suppresses growth, and THERMAL_OUT_OF_RANGE fires where the data supports it", () => {
  /*
   * The coordinator expected GIFT tilapia at Kodaikanal to warn THERMAL_OUT_OF_RANGE. It does
   * not, and should not: GIFT's temp_tolerable_c is the FAO lethal pair [11, 42] degC, while
   * Kodaikanal ponds bottom out at about 14.7 degC, so every month sits on the lower ramp
   * rather than outside the range. The growth penalty is carried by the size factor instead.
   */
  const away = OxyModel.evaluate(defaults({ station_name: "Kodaikanal" }), DATA);
  const tolerable = DATA.species.find((s) => s.id === DEFAULT_SPECIES).temp_tolerable_c.value;
  const coldest = Math.min(...away.months.map((m) => m.t_w_c));
  assert.ok(coldest > tolerable[0],
    `Kodaikanal's coldest pond month is ${coldest.toFixed(1)} degC, above the ${tolerable[0]} degC floor`);
  assert.ok(!warningCodes(away).includes("THERMAL_OUT_OF_RANGE"));
  assert.ok(away.months.every((m) => m.g_t > 0 && m.g_t < 1), "every month is on a ramp");
  assert.ok(Math.abs(away.crop.size_factor - COEFF.thermal.size_factor_clamp.value[0]) < 1e-12,
    "the size factor is held at its lower clamp, which is how the hill penalty is reported");

  /* Species whose tolerable range the hill climate really does breach do warn. */
  const pangasius = OxyModel.evaluate(
    Object.assign(OxyModel.defaultsFor("pangasius", DEFAULT_DISTRICT, DATA),
      { station_name: "Kodaikanal" }), DATA);
  const w = pangasius.warnings.find((x) => x.code === "THERMAL_OUT_OF_RANGE");
  assert.ok(w, `expected THERMAL_OUT_OF_RANGE for pangasius at Kodaikanal, got ${warningCodes(pangasius).join(", ")}`);
  assert.ok(w.months.length > 0);
  for (const m of w.months) { assert.equal(pangasius.months[m - 1].g_t, 0); }
});
