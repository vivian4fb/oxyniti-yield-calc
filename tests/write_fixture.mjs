/*
 * tests/write_fixture.mjs — writes tests/fixtures/result.example.json.
 * Purpose: give the UI work package (WP4) a real OxyModel.evaluate result for the default
 * scenario (GIFT tilapia, Tiruchirappalli, 1 acre, every other input at its MODEL_SPEC
 * section 1 default) to render against, instead of a hand-written stub.
 *
 * Run:  node tests/write_fixture.mjs
 * The output is deterministic: the model is pure and the inputs come from OxyModel.defaultsFor.
 */

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const require = createRequire(import.meta.url);

const OxyModel = require(path.join(ROOT, "site", "js", "model.js"));

const dataDir = path.join(ROOT, "site", "data");
const sandbox = { window: {} };
for (const file of fs.readdirSync(dataDir).filter((f) => f.endsWith(".data.js")).sort()) {
  vm.runInNewContext(fs.readFileSync(path.join(dataDir, file), "utf8"), sandbox, { filename: file });
}
const data = sandbox.window.OXY_DATA;
if (!data) { throw new Error("the data files did not assign window.OXY_DATA - has WP1 run?"); }

const SPECIES = "gift-tilapia";
const DISTRICT = "Tiruchirappalli";

const inputs = OxyModel.defaultsFor(SPECIES, DISTRICT, data);
const result = OxyModel.evaluate(inputs, data);

const outDir = path.join(ROOT, "tests", "fixtures");
fs.mkdirSync(outDir, { recursive: true });
const outFile = path.join(outDir, "result.example.json");
/* The file is exactly what evaluate returns, so the UI can render it as a live result. */
fs.writeFileSync(outFile, JSON.stringify(result, null, 2) + "\n", "utf8");

const lakh = data.coefficients.economics.lakh.value;
process.stdout.write(
  "wrote " + path.relative(ROOT, outFile) + "\n" +
  "  species            " + SPECIES + " at " + DISTRICT + " (" + result.station.name + ")\n" +
  "  crop months        " + result.crop.months.join(", ") +
  "   size factor " + result.crop.size_factor.toFixed(4) + "\n" +
  "  relief ds          " + result.crop.ds.toFixed(4) + "\n" +
  "  baseline harvest   " + result.baseline.kg.toFixed(1) + " kg/crop\n" +
  "  extra kg/crop      low " + result.delta.low.kg_crop.toFixed(1) +
  "   high " + result.delta.high.kg_crop.toFixed(1) + "\n" +
  "  extra profit/crop  low Rs " + (result.delta.low.profit_crop / lakh).toFixed(3) +
  " L   high Rs " + (result.delta.high.profit_crop / lakh).toFixed(3) + " L\n" +
  "  extra profit/year  low Rs " + (result.delta.low.profit_year / lakh).toFixed(3) +
  " L   high Rs " + (result.delta.high.profit_year / lakh).toFixed(3) + " L\n" +
  "  units              n_units " + result.unit.n_units + " (" + result.unit.sizing +
  "), n_best " + result.unit.n_best + ", n_relief " + result.unit.n_relief + "\n" +
  "                     " + result.unit.o2_input_lpm_used + " L/min used, " +
  result.unit.power_kw_used + " kW used, " +
  result.unit.supply_mg_l_per_unit_night.toFixed(4) + " mg/L per unit per night\n" +
  "  maintenance/year   Rs " + (result.delta.high.maintenance_year === null
    ? "not available" : result.delta.high.maintenance_year.toFixed(0)) +
  "   capex Rs " + (result.payback.capex === null ? "not available" : result.payback.capex.toFixed(0)) + "\n" +
  "  payback            " + result.payback.status +
  (result.payback.reason ? " - " + result.payback.reason : "") +
  (result.payback.months_high === null ? ""
    : "  " + result.payback.months_high.toFixed(1) + " to " +
      (result.payback.months_low === null ? "never" : result.payback.months_low.toFixed(1)) + " months") + "\n" +
  "  warnings           " + (result.warnings.map((w) => w.code).join(", ") || "none") + "\n"
);
