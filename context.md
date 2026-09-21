# 2_Business/NBG/oxyniti_yield _calc — context

*Updated 2026-09-21. State: ACTIVE*

## What this is

A standalone yield, profit and payback calculator for Tamil Nadu fish and shrimp ponds, with
an interactive district map of aquaculture hotspots and a city-by-city growth comparison.
Live at **https://vivian4fb.github.io/oxyniti-yield-calc/** from the public repository
`github.com/vivian4fb/oxyniti-yield-calc`, which is **this folder as a child git repository**
(created 2026-09-21 at Vivian's request; the parent Code2 stays policy-only). It supersedes the
flat 20–30 % slider on oxyniti.com with a model capped at the internal +18 % saleable-kg
ceiling and driven by a night-time dissolved-oxygen budget per crop month.

The folder name carries a stray space before `_calc`. Always quote the path.

## Read order

1. `plan/EXECUTION_PLAN.md` — who built what, fixed interfaces, gates, owner decisions (§7).
2. `plan/MODEL_SPEC.md` — the model, equation by equation, amendments A1–A9, contract tests.
3. `plan/owner_inputs.json` — Vivian's figures of 2026-09-21 and the rough estimates he
   authorised, each with status and basis. `plan/DEVIATIONS.md` — every supersession.
4. `plan/QA_REPORT.md` and `plan/DATA_STATUS.md` — gate results and per-field data quality.
5. `research/` — the sourced data. Source of truth; builders never edit it.

## Constraints

- Every figure carries units, a status label and a date; ASSUMED values are shown in the UI.
- Fail loudly: a species missing a load-bearing field is listed but not estimable (7 of 18).
- Never fabricate a farm, contact or price; prices here are owner-authorised rough estimates
  labelled ASSUMED until replaced.
- Git is allowed **inside this folder only** (Vivian's instruction 2026-09-21); publish with
  `deploy.ps1` (commit + push; GitHub Actions deploys `site/`). Never git elsewhere in Code2.

## State

*Measured 2026-09-21.* Built, gated and published. `node --test tests/*.test.mjs` 43/43;
`python tests/compare.py` exit 0 on 29 scenarios against the independent Python oracle;
self-test and solubility checks pass; Chrome console clean; screenshots in `tests/screenshots/`.

Default scenario (GIFT tilapia, Tiruchirappalli, 1 acre, 5,965/acre, 1.5 L/min per unit):
extra harvest 10–20 kg/crop, extra profit about −₹0.57 L/year, no payback. At 20 L/min per unit
on an intensively stocked pond one unit pays back in about 25 months. The oxygen delivery per
unit is the number that decides the business case.

## Next

Vivian: replace the ASSUMED prices with real quotes; get the OEM oxygen delivery in kg O2/h;
decide the live-site claims (`DEVIATIONS.md`); native Tamil review; then integrate into
oxyniti.com. Data refinement: GIFT tilapia's tolerable range is the FAO lethal pair [11, 42],
so hill stations penalise growth through the size factor rather than a warning.
