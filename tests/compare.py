# Compares tests/oracle.py against tests/run_scenarios.mjs (the real site/js/model.js) for scenario
# parity. Implements MODEL_SPEC.md section 8 test 6, exactly under amendment A7 (pinned 2026-09-21).
"""
Usage:
    python tests/compare.py               # full parity: node run_scenarios.mjs vs python oracle.py
    python tests/compare.py --self-test    # inject a defect into a copy of the oracle and confirm
                                            # the comparator reports FAIL (does not touch site/js/model.js)
    python tests/compare.py --doonly       # DO-saturation check against coefficients.json's table only

The A7 parity contract (MODEL_SPEC.md section 8 test 6) is narrower than "diff everything":
  - every numeric leaf of crop, uplift, baseline, with_oxy, delta, unit, payback: 1e-6 relative
  - months[].{t_air_c, t_w_c, c_s_mg_l, g_t, in_crop, biomass_kg, do_dawn_base, do_dawn_oxy,
    s_base, s_oxy} for all twelve months: 1e-6 relative (1e-9 absolute for c_s_mg_l)
  - payback.status and station.name: exact string match
  - warnings: equal SET of codes (order, message text and per-warning `months` are not compared)
  - error cases: equal error class and field name
  - inputs_resolved, assumptions and all other message/label wording: outside the contract,
    never compared (any string leaf inside a numeric group, e.g. unit.id/label/sizing/status or
    payback.reason, is skipped for the same reason).
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests"
ORACLE_PATH = TESTS_DIR / "oracle.py"
RUN_SCENARIOS_PATH = TESTS_DIR / "run_scenarios.mjs"
SCENARIOS_PATH = TESTS_DIR / "scenarios.json"
DEFAULT_DATA_DIR = ROOT / "site" / "data"
DEFAULT_MODEL_PATH = ROOT / "site" / "js" / "model.js"

REL_TOL = 1e-6
ABS_TOL_CS = 1e-9  # months[].c_s_mg_l only

NUMERIC_GROUPS = ["crop", "uplift", "baseline", "with_oxy", "delta", "unit", "payback"]
MONTH_FIELDS = ["t_air_c", "t_w_c", "c_s_mg_l", "g_t", "in_crop",
                "biomass_kg", "do_dawn_base", "do_dawn_oxy", "s_base", "s_oxy"]
REPORT_GROUPS = ["months", "crop", "uplift", "baseline", "with_oxy", "delta", "payback", "unit",
                  "station", "warnings"]


# --------------------------------------------------------------------------------------------------
# Running the two implementations
# --------------------------------------------------------------------------------------------------

def run_oracle(scenarios_path=SCENARIOS_PATH, oracle_path=ORACLE_PATH, data_dir=None):
    # data_dir is always passed explicitly: a mutated copy of oracle.py (--self-test) can live in a
    # temp directory, where the script's own __file__-relative default would resolve to nothing.
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    args = [sys.executable, str(oracle_path), str(scenarios_path), str(data_dir)]
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=env, cwd=str(ROOT))
    if proc.returncode != 0:
        raise RuntimeError(f"{oracle_path} failed (exit {proc.returncode}):\n{proc.stderr}")
    return json.loads(proc.stdout)


def run_node(scenarios_path=SCENARIOS_PATH, data_dir=None, model_path=None):
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR
    if model_path is None:
        model_path = DEFAULT_MODEL_PATH
    args = ["node", str(RUN_SCENARIOS_PATH), str(scenarios_path), str(data_dir), str(model_path)]
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=env, cwd=str(ROOT))
    if proc.returncode != 0:
        raise RuntimeError(f"node {RUN_SCENARIOS_PATH} failed (exit {proc.returncode}):\n{proc.stderr}")
    return json.loads(proc.stdout)


# --------------------------------------------------------------------------------------------------
# Structural / numeric diff over the A7 contract only.
# --------------------------------------------------------------------------------------------------

def rel_close(a, b):
    dev = abs(a - b)
    denom = max(abs(a), abs(b))
    rel = dev / denom if denom else 0.0
    return rel <= REL_TOL, rel


def diff_numeric_tree(a, b, path, group, mismatches, max_dev):
    """Recurses through one of the 7 whitelisted groups. Numbers: REL_TOL relative. Booleans and
    None: exact. payback.status: exact string (the one string A7 names explicitly). Any other
    string leaf (unit.id/label/sizing/status, payback.reason, ...) is outside the contract and is
    silently skipped, per A7 - it is free-text/labelling, not a computed value."""
    leaf_name = path[-1] if path else ""

    if group == "payback" and leaf_name == "status":
        if a != b:
            mismatches.append((group, list(path), f"payback.status mismatch: {a!r} != {b!r}"))
        return

    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())
        for k in sorted(keys, key=str):
            if k not in a:
                mismatches.append((group, path + [k], f"key '{k}' missing on oracle side"))
                continue
            if k not in b:
                mismatches.append((group, path + [k], f"key '{k}' missing on JS side"))
                continue
            diff_numeric_tree(a[k], b[k], path + [k], group, mismatches, max_dev)
        return

    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            mismatches.append((group, list(path), f"length mismatch: {len(a)} != {len(b)}"))
            return
        for i, (av, bv) in enumerate(zip(a, b)):
            diff_numeric_tree(av, bv, path + [i], group, mismatches, max_dev)
        return

    if isinstance(a, str) or isinstance(b, str):
        return  # label/id/reason/sizing-mode text: outside the A7 contract

    if isinstance(a, bool) or isinstance(b, bool):
        if a is not b:
            mismatches.append((group, list(path), f"bool mismatch: {a!r} != {b!r}"))
        return

    if a is None or b is None:
        if a is not b:
            mismatches.append((group, list(path), f"null mismatch: {a!r} != {b!r}"))
        return

    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        ok, dev = rel_close(float(a), float(b))
        if dev > max_dev.get(group, 0.0):
            max_dev[group] = dev
        if not ok:
            mismatches.append((group, list(path), f"numeric mismatch: {a!r} != {b!r} (dev {dev:.3e} rel)"))
        return

    mismatches.append((group, list(path), f"shape/type mismatch: {a!r} != {b!r}"))


def diff_months(a_months, b_months, mismatches, max_dev):
    group = "months"
    max_dev.setdefault(group, 0.0)
    if len(a_months) != len(b_months):
        mismatches.append((group, ["months"], f"length mismatch: {len(a_months)} != {len(b_months)}"))
        return
    for i, (am, bm) in enumerate(zip(a_months, b_months)):
        for field in MONTH_FIELDS:
            av, bv = am.get(field), bm.get(field)
            path = ["months", i, field]
            if field == "in_crop":
                if av is not bv:
                    mismatches.append((group, path, f"bool mismatch: {av!r} != {bv!r}"))
                continue
            if av is None or bv is None:
                if av is not bv:
                    mismatches.append((group, path, f"null mismatch: {av!r} != {bv!r}"))
                continue
            if field == "c_s_mg_l":
                dev = abs(float(av) - float(bv))
                if dev > max_dev[group]:
                    max_dev[group] = dev
                if dev > ABS_TOL_CS:
                    mismatches.append((group, path, f"numeric mismatch: {av!r} != {bv!r} (dev {dev:.3e} abs)"))
                continue
            ok, dev = rel_close(float(av), float(bv))
            if dev > max_dev[group]:
                max_dev[group] = dev
            if not ok:
                mismatches.append((group, path, f"numeric mismatch: {av!r} != {bv!r} (dev {dev:.3e} rel)"))


def diff_station(a_station, b_station, mismatches, max_dev):
    group = "station"
    max_dev.setdefault(group, 0.0)
    an, bn = (a_station or {}).get("name"), (b_station or {}).get("name")
    if an != bn:
        mismatches.append((group, ["station", "name"], f"string mismatch: {an!r} != {bn!r}"))


def diff_warnings(a_warnings, b_warnings, mismatches, max_dev):
    group = "warnings"
    max_dev.setdefault(group, 0.0)
    a_codes = {w.get("code") for w in (a_warnings or [])}
    b_codes = {w.get("code") for w in (b_warnings or [])}
    if a_codes != b_codes:
        mismatches.append((group, ["warnings"],
                            f"warning code set mismatch: oracle-only={sorted(a_codes - b_codes)} "
                            f"js-only={sorted(b_codes - a_codes)}"))


# A9.4: compareStations/compare_stations rows - "station name exact, error rows compared by
# station name only" (coordinator's message), everything else under the usual A7 numeric style.
ROWS_NUMERIC_FIELDS = ["elevation_m", "G_T", "size_factor", "harvest_size_g", "baseline_kg_crop",
                        "ds", "extra_kg_crop_high", "profit_year_high", "n_best"]


def diff_rows(a_rows, b_rows, mismatches, max_dev):
    group = "rows"
    max_dev.setdefault(group, 0.0)
    if len(a_rows) != len(b_rows):
        mismatches.append((group, ["rows"], f"length mismatch: {len(a_rows)} != {len(b_rows)}"))
        return
    for i, (ar, br) in enumerate(zip(a_rows, b_rows)):
        path_base = ["rows", i]
        a_station, b_station = ar.get("station"), br.get("station")
        if a_station != b_station:
            mismatches.append((group, path_base + ["station"], f"string mismatch: {a_station!r} != {b_station!r}"))

        a_err, b_err = "error" in ar, "error" in br
        if a_err or b_err:
            continue  # error rows: station name (checked above) only, per the coordinator's message

        for field in ROWS_NUMERIC_FIELDS:
            av, bv = ar.get(field), br.get(field)
            path = path_base + [field]
            if av is None or bv is None:
                if av is not bv:
                    mismatches.append((group, path, f"null mismatch: {av!r} != {bv!r}"))
                continue
            ok, dev = rel_close(float(av), float(bv))
            if dev > max_dev[group]:
                max_dev[group] = dev
            if not ok:
                mismatches.append((group, path, f"numeric mismatch: {av!r} != {bv!r} (dev {dev:.3e} rel)"))

        a_codes = set(ar.get("warnings") or [])
        b_codes = set(br.get("warnings") or [])
        if a_codes != b_codes:
            mismatches.append((group, path_base + ["warnings"],
                                f"warning code set mismatch: oracle-only={sorted(a_codes - b_codes)} "
                                f"js-only={sorted(b_codes - a_codes)}"))


def compare_result_sets(oracle_results, other_results, scenario_ids=None):
    """Returns (ok, report_rows, mismatches). report_rows: (scenario_id, group, max_dev|None, n_mismatches).
    Implements the A7 contract only (see module docstring) - inputs_resolved, assumptions and all
    free-text wording are never compared."""
    all_mismatches = []
    report_rows = []

    if len(oracle_results) != len(other_results):
        all_mismatches.append((None, [], f"result count mismatch: oracle {len(oracle_results)} != other {len(other_results)}"))
        return False, report_rows, all_mismatches

    for idx, (raw_a, raw_b) in enumerate(zip(oracle_results, other_results)):
        sid = scenario_ids[idx] if scenario_ids else str(idx)
        a_is_rows = isinstance(raw_a, dict) and "rows" in raw_a
        b_is_rows = isinstance(raw_b, dict) and "rows" in raw_b

        if a_is_rows or b_is_rows:
            if not (a_is_rows and b_is_rows):
                all_mismatches.append((sid, [], f"rows/non-rows mismatch: oracle={raw_a!r} other={raw_b!r}"))
                report_rows.append((sid, "rows", None, 1))
                continue
            scenario_mismatches = []
            max_dev = {}
            diff_rows(raw_a["rows"], raw_b["rows"], scenario_mismatches, max_dev)
            report_rows.append((sid, "rows", max_dev.get("rows", 0.0), len(scenario_mismatches)))
            all_mismatches.extend((sid, p, msg) for (_, p, msg) in scenario_mismatches)
            continue

        a_is_err = isinstance(raw_a, dict) and set(raw_a.keys()) == {"error"}
        b_is_err = isinstance(raw_b, dict) and set(raw_b.keys()) == {"error"}

        if a_is_err or b_is_err:
            if a_is_err and b_is_err:
                a_cls, _, a_field = raw_a["error"].partition(": ")
                b_cls, _, b_field = raw_b["error"].partition(": ")
                if a_cls != b_cls or a_field != b_field:
                    all_mismatches.append((sid, ["error"], f"error mismatch: {raw_a['error']!r} != {raw_b['error']!r}"))
                    report_rows.append((sid, "error", None, 1))
                else:
                    report_rows.append((sid, "error", 0.0, 0))
            else:
                all_mismatches.append((sid, [], f"error/ok mismatch: oracle={raw_a!r} other={raw_b!r}"))
                report_rows.append((sid, "error-vs-ok", None, 1))
            continue

        scenario_mismatches = []
        max_dev = {}

        for group in NUMERIC_GROUPS:
            a_val, b_val = raw_a.get(group), raw_b.get(group)
            if a_val is None and b_val is None:
                continue
            if a_val is None or b_val is None:
                scenario_mismatches.append((sid, [group], f"key '{group}' missing on one side"))
                continue
            diff_numeric_tree(a_val, b_val, [group], group, scenario_mismatches, max_dev)

        diff_months(raw_a.get("months", []), raw_b.get("months", []), scenario_mismatches, max_dev)
        diff_station(raw_a.get("station"), raw_b.get("station"), scenario_mismatches, max_dev)
        diff_warnings(raw_a.get("warnings"), raw_b.get("warnings"), scenario_mismatches, max_dev)

        for group in REPORT_GROUPS:
            n = sum(1 for m in scenario_mismatches if m[0] == group)
            report_rows.append((sid, group, max_dev.get(group, 0.0), n))

        all_mismatches.extend((sid, p, msg) for (_, p, msg) in scenario_mismatches)

    ok = len(all_mismatches) == 0
    return ok, report_rows, all_mismatches


def print_report(report_rows):
    print(f"{'scenario':34} {'group':16} {'max_dev':>12} {'mismatches':>11}")
    print("-" * 76)
    for sid, group, dev, n in report_rows:
        dev_s = "-" if dev is None else f"{dev:.3e}"
        flag = "  <-- MISS" if n else ""
        print(f"{sid:34} {group:16} {dev_s:>12} {n:>11}{flag}")


# --------------------------------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------------------------------

def full_parity():
    if not DEFAULT_MODEL_PATH.exists():
        print(f"site/js/model.js not found at {DEFAULT_MODEL_PATH} - parity pending WP6.")
        return 1
    oracle_results = run_oracle()
    js_results = run_node()
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    scenario_ids = [s["id"] for s in scenarios]

    ok, report_rows, mismatches = compare_result_sets(oracle_results, js_results, scenario_ids)
    print_report(report_rows)
    if not ok:
        print(f"\n{len(mismatches)} mismatch(es):")
        for sid, path, msg in mismatches[:200]:
            where = ".".join(str(p) for p in path) if path else "(top level)"
            print(f"  [{sid}] {where}: {msg}")
        print("\nFAIL")
        return 1
    print("\nPASS")
    return 0


def self_test():
    print("--self-test: copying tests/oracle.py to a temp file, flipping the sign of the Q10 exponent "
          "in fish_respiration_rate(), and comparing the mutated oracle's own output against the real "
          "oracle's own output for every scenario in tests/scenarios.json. No JS is run.")

    source = ORACLE_PATH.read_text(encoding="utf-8")
    target_line = "    exponent = (min(t_w, t_cap) - t_ref) / 10.0"
    if target_line not in source:
        print(f"FAIL: could not find the line to mutate ({target_line!r}) in {ORACLE_PATH}")
        return 1
    mutated_source = source.replace(target_line, "    exponent = -(min(t_w, t_cap) - t_ref) / 10.0", 1)

    with tempfile.TemporaryDirectory() as tmp:
        mutated_path = pathlib.Path(tmp) / "oracle_mutated.py"
        mutated_path.write_text(mutated_source, encoding="utf-8")
        print(f"Mutated copy written to {mutated_path}")

        reference_results = run_oracle(oracle_path=ORACLE_PATH)
        mutated_results = run_oracle(oracle_path=mutated_path)

    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    scenario_ids = [s["id"] for s in scenarios]
    ok, report_rows, mismatches = compare_result_sets(reference_results, mutated_results, scenario_ids)
    print_report(report_rows)

    if ok:
        print("\nFAIL: the self-test did not detect the injected defect (comparator reported PASS on "
              "the mutated oracle) - the comparator or the injection point is not sensitive enough.")
        return 1
    print(f"\n{len(mismatches)} mismatch(es) against the mutated oracle, as expected.")
    print("Comparator correctly reported FAIL for the injected defect -> self-test result: PASS (exit 0).")
    return 0


def doonly():
    coeffs = json.loads((ROOT / "plan" / "coefficients.json").read_text(encoding="utf-8"))
    table = coeffs["do_saturation"]["verification_table_mg_l_1atm"]["value"]

    sys.path.insert(0, str(TESTS_DIR))
    import oracle  # tests/oracle.py

    tol = 0.0005
    rows = []
    max_dev = 0.0
    all_ok = True
    for t_str, row in table.items():
        for s_str, expected in row.items():
            got = oracle.do_saturation(float(t_str), float(s_str), 1.0, coeffs["do_saturation"])
            dev = abs(got - expected)
            max_dev = max(max_dev, dev)
            ok = dev <= tol
            all_ok = all_ok and ok
            rows.append((t_str, s_str, expected, got, dev, ok))

    print("--doonly: oracle.do_saturation() vs coefficients.json verification_table_mg_l_1atm "
          f"(tolerance {tol} mg/L)")
    print(f"{'t_degC':>8} {'S_ppt':>8} {'expected':>10} {'got':>12} {'dev':>10} {'result':>7}")
    for t_str, s_str, expected, got, dev, ok in sorted(rows, key=lambda r: (float(r[0]), float(r[1]))):
        print(f"{t_str:>8} {s_str:>8} {expected:>10.4f} {got:>12.6f} {dev:>10.6f} {'OK' if ok else 'FAIL':>7}")
    print(f"\nmax deviation: {max_dev:.6f} mg/L (tolerance {tol} mg/L)")
    print("PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    if "--doonly" in args:
        return doonly()
    return full_parity()


if __name__ == "__main__":
    sys.exit(main())
