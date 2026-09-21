# Deviations and supersessions log

*Every entry: date, what was superseded, by what, why, status. Append only; never edit history.*

## 2026-09-21 — Live-site ROI slider superseded by the capped model

- **Superseded:** the homepage slider on oxyniti.com (`website/Pages/Components/ProfitCalculatorSection.razor`)
  and the older static site (`vivian4fb.github.io/nbg`) compute
  `extra kg = acres × 2,500 kg/acre/year × 20–30 %`. That is a flat uplift with no species,
  season, density or district dependence, and its 20–30 % exceeds the internal claims ceiling
  of +18 % saleable kg recorded in `docs/make_charts.py` and `NBG/.claude/SALES_OVERRIDE.md`.
- **Replaced by:** `plan/MODEL_SPEC.md` section 5 — uplift = ceiling × crop-mean oxygen-stress
  relief, so +18 % is the maximum, reached only for a fully oxygen-limited pond.
- **Why:** `2_Business/CLAUDE.md` non-negotiable 2: outward claims must not exceed the internal
  model. The live slider has been in breach since 2026-07-22; this tool is the reconciliation.
- **Status:** the standalone tool applies the ceiling. The live site keeps 20–30 % until the
  tool is integrated; that gap stays open and is listed in `EXECUTION_PLAN.md` as an owner
  decision.

## 2026-09-21 — Site claims left as found

`+15 % survival`, `−15 % FCR`, `+30 % stocking density` and `2× DO` remain on the live site
(`ResultsSection.razor`, `llms.txt`, hero shell). The calculator's own copy quotes only the
+18 % internal ceiling and its decomposition (+12 % growth, +5 points survival). FCR gain is
an advanced toggle, default off, labelled UNTESTED. Whether the live site's four figures stay
is an owner decision, not a tool decision.

## 2026-09-21 — Internal GIFT tilapia economics are not in the PDF they cite

- **Found by:** the economics research pass (`research/economics_device_evidence.md`
  section 5.2), reading
  `https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/6.GIFT_Tilapia_culture_15.pdf`.
- **Recorded in the workspace:** `docs/NBG_Trichy_Prospecting_Report.md` section 4 and
  `docs/make_charts.py` (`chart_farmer_roi`): "capital ₹2.1 L, variable ₹5.76 L, 9,000 kg at
  ₹120/kg, 1 acre, net first-crop ₹2.15 L".
- **What the PDF says (1 ha):** capital ₹3.69 lakh, recurring ₹5.02 lakh per crop, 9,375 kg
  per crop at ₹75/kg, feed 73 % of opex. ₹5.76 lakh matches the intensive-carp model's two-crop
  recurring cost; ₹120/kg is the Oxyniti calculator's own default.
- **Consequence here:** the +18 % ceiling and its ₹1.53 L/acre/crop illustration are kept as
  the *internal calibration arithmetic* (spec section 8 test 2) with status ASSUMED; the
  calculator's baseline economics come from the per-hectare NABARD figures, converted per acre
  and labelled 2015 vintage. The prospecting report needs a supersession banner; that is an
  owner action listed in `EXECUTION_PLAN.md` section 7.

## 2026-09-21 — Oxygen supply modelled by mass balance, not by an assumed relief fraction

- **Superseded:** spec draft section 4.5 (relief fraction `f_relief = 0.8` ASSUMED).
- **Replaced by:** oxygen input capacity from the product pages (2 L/min and 6 L/min,
  VERIFIED) × density × purity × dissolved fraction, and unit sizing by the night-time deficit
  (spec sections 4.5 and 7).
- **Why:** a published flow rate is a physical bound; a relief fraction was a guess. The
  mass balance shows one 1.5 HP unit adds about 0.16 mg/L per night to a 1 acre × 1.5 m pond,
  which is why the tool reports "units needed" instead of assuming one unit relieves an acre.
- **Status:** purity and dissolved fraction remain ASSUMED until the OEM datasheet arrives.

## 2026-09-21 — Amendments A1–A5 after the first model run

- **Trigger:** WP2's first run of the model against the built data (29 tests green) showed
  (a) GIFT tilapia's growth DO threshold resolving to 1.9 mg/L from the range [0.8, 3.0];
  (b) Cuddalore's null station elevation making two districts throw; (c) a baseline of
  8,786 kg/acre/crop from compounding three range midpoints against a sourced yield of
  2,428–4,047; (d) at the published 2 L/min oxygen input, eight units' electricity
  (≈ ₹1.1 L per crop at ₹6.95/kWh) exceeding the extra fish (≈ ₹0.9 L) — negative profit at
  the defaults.
- **Superseded:** sizing to full relief (`n_auto`) as the default; density default = range
  midpoint; `do_minimum` = range midpoint.
- **Replaced by:** MODEL_SPEC.md amendments A1–A5 — growth threshold = high bound of a
  sourced range; coastal null elevation = 5 m ASSUMED; a yield-consistent default density
  (`density_default_per_acre`); profit-maximising sizing (`n_best`) with full-relief sizing
  (`n_relief`) shown beside it; datasheet override inputs for oxygen delivery and electrical
  input; warning `NO_PAYBACK_AT_PUBLISHED_O2` when no unit count pays back.
- **Why:** each is a data-definition or decision-level fix; none changes the ceiling or the
  physics. Finding (d) is not a defect in the tool — it is what the published product figure
  implies, and the owner decision list carries it.
- **Status:** applied by the owning agents (WP1 data, WP2 model, WP3 oracle) on 2026-09-21;
  verified when the parity comparison passes.
