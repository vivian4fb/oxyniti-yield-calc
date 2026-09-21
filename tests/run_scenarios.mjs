// Runs the real site/js/model.js against tests/scenarios.json and prints results as JSON, in the
// same shape as tests/oracle.py's output, for tests/compare.py to diff. MODEL_SPEC.md sections 1-7.
//
// Usage: node tests/run_scenarios.mjs [scenarios.json] [data_dir] [model.js]

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..");

function loadOxyData(dataDir) {
  // Classic scripts assign window.OXY_DATA.<name> = ...; vm.runInContext with window === the
  // sandbox's global object reproduces the file:// / browser load order (EXECUTION_PLAN.md 4.1).
  const sandbox = { console };
  sandbox.window = sandbox;
  vm.createContext(sandbox);

  if (!fs.existsSync(dataDir)) {
    throw new Error(`data directory not found: ${dataDir}`);
  }
  const files = fs.readdirSync(dataDir).filter((f) => f.endsWith(".data.js")).sort();
  if (files.length === 0) {
    throw new Error(`no *.data.js files found in ${dataDir}`);
  }
  for (const f of files) {
    const code = fs.readFileSync(path.join(dataDir, f), "utf8");
    vm.runInContext(code, sandbox, { filename: f });
  }
  if (!sandbox.window.OXY_DATA) {
    throw new Error(`OXY_DATA was never populated by ${dataDir}`);
  }
  return sandbox.window.OXY_DATA;
}

function loadModel(modelPath) {
  // model.js is a classic browser script that also exports itself for Node
  // (EXECUTION_PLAN.md 4.2: "if (typeof module !== 'undefined') module.exports = OxyModel;").
  // Give it a `window` to assign to in case it references window before reaching that guard.
  if (typeof global.window === "undefined") {
    global.window = global;
  }
  return require(modelPath);
}

function formatError(err) {
  const className = err && err.constructor ? err.constructor.name : "Error";
  const field = err && err.field !== undefined && err.field !== null ? err.field : err && err.message;
  return `${className}: ${field}`;
}

function main() {
  const argv = process.argv.slice(2);
  const scenariosPath = path.resolve(argv[0] || path.join(__dirname, "scenarios.json"));
  const dataDir = path.resolve(argv[1] || path.join(projectRoot, "site", "data"));
  const modelPath = path.resolve(argv[2] || path.join(projectRoot, "site", "js", "model.js"));

  const OxyModel = loadModel(modelPath);
  const data = loadOxyData(dataDir);
  const scenarios = JSON.parse(fs.readFileSync(scenariosPath, "utf8"));

  const results = scenarios.map((scenario) => {
    try {
      if (scenario.mode === "compare_stations") {
        // A9.4: OxyModel.compareStations(inputs, data) -> rows; wrapped the same way as
        // tests/oracle.py's compare_stations() output so tests/compare.py can diff them.
        const rows = OxyModel.compareStations(scenario.inputs, data);
        return { rows };
      }
      return OxyModel.evaluate(scenario.inputs, data);
    } catch (err) {
      return { error: formatError(err) };
    }
  });

  process.stdout.write(JSON.stringify(results));
}

main();
