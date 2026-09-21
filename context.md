# 2_Business/NBG/oxyniti_yield _calc — context

*Updated 2026-09-21. State: ACTIVE*

## What this is

A standalone yield, profit and payback calculator for Tamil Nadu fish and shrimp ponds, with
an interactive district map of aquaculture hotspots, built to showcase on GitHub Pages and to
integrate into oxyniti.com later. It supersedes the flat 20–30 % slider on the live site with
a model capped at the internal +18 % saleable-kg ceiling and driven by a night-time
dissolved-oxygen budget per crop month, so the answer depends on species, district climate,
stocking month, density, pond bloom, existing aeration and the unit's oxygen delivery.

The folder name carries a stray space before `_calc`. Always quote the path.

## Read order

1. `plan/EXECUTION_PLAN.md` — who built what, fixed interfaces, gates, owner decisions (§7).
2. `plan/MODEL_SPEC.md` — the model, equation by equation, amendments A1–A8, contract tests.
3. `plan/DEVIATIONS.md` — supersessions: the live slider, the prospecting report's tilapia
   economics (not in the PDF cited), the mass-balance oxygen model, amendments.
4. `plan/QA_REPORT.md` and `plan/DATA_STATUS.md` — gate results and per-field data quality.
5. `research/` — the sourced data. Source of truth; builders never edit it.

## Constraints

- Every figure carries units, a status label and a date; ASSUMED values are shown in the UI.
- Fail loudly: a null unit price blocks payback; a species missing a load-bearing field is
  listed but not estimable (7 of 18 are estimable).
- Never fabricate a farm, contact or price. Hotspots are district statistics and public
  facilities only (87 entries, 82 VERIFIED).
- No git anywhere under Code2. Publishing is `deploy.ps1`, run by Vivian, into
  `C:\Users\vivia\Repos\oxyniti-yield-calc`.

## State

*Measured 2026-09-21.* **Built and gated, not yet published.** `node --test tests/*.test.mjs`
38/38; `python tests/compare.py` exit 0 on 26 scenarios (JS vs independent Python oracle,
numeric deviations ≤ 3e-11); self-test and DO-table checks pass; console-error sweep clean on
`http://` and `file://`; screenshots at 360/768/1280 in `tests/screenshots/`. Site 2.5 MB.

Default scenario (GIFT tilapia, Tiruchirappalli, 1 acre, 5,965/acre): extra harvest
13–26 kg/crop, extra profit negative, no payback at the published 2 L/min oxygen input and
LT III-A tariff. That is the finding, not a defect.

## Next

Vivian: supply the OEM oxygen delivery per model, the concentrator power draw and real unit
prices (Advanced inputs accept the first two now); decide the live-site claims; run
`deploy.ps1`. Then a native Tamil review before the language toggle leaves "partial".
