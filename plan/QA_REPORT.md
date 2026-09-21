# QA report — WP6 integration, defects and gate

*Written 2026-09-21 by the WP6 integration pass (Opus 5). Covers the state of the build at the
moment the gate went green. Every claim below is the verbatim output of a command run in this
session, or a file:line reference in the tree.*

**Verdict: the gate is green and the build is ready for the owner to publish.** Four gate
commands, exit code 0 on all four; 38 model tests pass; JS-vs-Python parity holds on every
numeric group of all 26 scenarios to 3.2 × 10⁻¹¹ or better; zero console errors across load and
twelve interactions, on both `http://` and `file://`; five defects found and fixed; two open
items, both owner decisions already on the `EXECUTION_PLAN.md` section 7 list.

---

## 1. Gate

| Command | Exit code | Result |
|---|---|---|
| `node --test tests/*.test.mjs` | 0 | 38 pass, 0 fail |
| `python tests/compare.py` | 0 | PASS — 26 scenarios, every group in the A7 contract |
| `python tests/compare.py --self-test` | 0 | PASS — the injected defect was detected |
| `python tests/compare.py --doonly` | 0 | PASS — max deviation 0.000488 mg/L |

Note on invocation: `node --test tests/` silently runs nothing on this Node build (v22.23.2); the
glob `tests/*.test.mjs` is required. Recorded in `site/README.md` so the next person does not
lose an hour to a green-looking no-op.

### 1.1 Model tests — verbatim tail

```
1..38
# tests 38
# suites 0
# pass 38
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 465.645
```

Test 38 is new in this pass — see defect D1 below.

### 1.2 Scenario parity — `python tests/compare.py`, exit code 0

Maximum deviation per output group, taken over all 26 scenarios in `tests/scenarios.json`
(contract: 1 × 10⁻⁶ relative, 1 × 10⁻⁹ absolute for `c_s_mg_l`, per `MODEL_SPEC.md` section 8
test 6 as pinned by amendment A7):

| group | max deviation over all 26 scenarios | mismatches |
|---|---|---|
| `months` | 3.231e-11 | 0 |
| `delta` | 8.057e-13 | 0 |
| `payback` | 8.056e-13 | 0 |
| `unit` | 7.867e-13 | 0 |
| `uplift` | 7.417e-13 | 0 |
| `crop` | 6.699e-13 | 0 |
| `with_oxy` | 1.445e-14 | 0 |
| `baseline` | 5.292e-16 | 0 |
| `station` | 0.000e+00 | 0 |
| `warnings` | 0.000e+00 | 0 |
| `error` | 0.000e+00 | 0 |

The worst group, `months`, is five orders of magnitude inside the contract. `station` and
`warnings` are exact-match groups (station name; warning code set), and `error` is the
fail-loud group (error class and field name) — all three agree exactly.

Final line:

```
PASS
```

### 1.3 Comparator self-test — exit code 0

```
1353 mismatch(es) against the mutated oracle, as expected.
Comparator correctly reported FAIL for the injected defect -> self-test result: PASS (exit 0).
```

### 1.4 DO saturation — exit code 0

```
max deviation: 0.000488 mg/L (tolerance 0.0005 mg/L)
PASS
```

All eighteen table cells (20 / 25 / 28 / 30 / 32 / 35 °C × 0 / 15 / 25 ppt) pass. The worst cell
is 28 °C / 15 ppt at 0.000488 mg/L, which is 98 % of the tolerance — tight, but the tolerance is
set by the 4-decimal rounding of the published verification table, not by the method.

### 1.5 Parity history within this session

The parity run was **not** green when WP6 started, and two of the three causes were resolved by
the owning packages while this pass ran:

1. First run (11:24): 200+ mismatches, all in `inputs_resolved`, `assumptions`, `payback.reason`
   and `warnings[].message` — fields amendment A7 places **outside** the contract. WP3 narrowed
   `tests/compare.py` at 11:25 and 11:26. WP6 waited rather than editing, per its brief.
2. Second run (11:26): `NameError: ABS_TOL_FLOOR` — `tests/compare.py` caught mid-edit. Waited.
3. Third run (11:27): two genuine residuals, both semantic, both resolved by amendment **A8**
   (pinned in `MODEL_SPEC.md` section 7 at 11:28). WP3 applied A8 to `tests/oracle.py`; WP6
   applied its second rule to `site/js/model.js` (defect D1).

**A note on a mid-task coordinator message.** A message arrived stating that A8 rule 1 required
`NOT_OXYGEN_LIMITED` *not* to fire for scenario `murrel-vellore-mid-fcr`, and that `model.js`
"currently fires it on a lenient `ds` cutoff". Neither was true. `MODEL_SPEC.md` line 286 pins the
rule as "the crop-mean of `s_base` over the in-crop months is below 0.05"; `site/js/model.js:856`
already tested exactly that; and the measured crop-mean `s_base` for that scenario is
**0.03613**, which *is* below 0.05, so the warning must fire. `model.js` was therefore left
unchanged on rule 1 and the oracle was the side that moved. The spec was followed, not the
message. Flagged here because the message would have introduced a defect if applied literally.

---

## 2. Console-error check

**Method.** Headless Chrome (`--headless=new`) driven over the DevTools Protocol from a Node 22
script using the built-in `WebSocket`, with `Runtime`, `Log`, `Page` and `Network` domains
enabled. Every `Runtime.exceptionThrown`, every `Runtime.consoleAPICalled` of type `error`,
`warning` or `assert`, every `Log.entryAdded` at level error or warning, and every
`Network.loadingFailed` is captured and attributed to the interaction step that produced it.
Probe script: `<scratchpad>/cdp_probe.mjs` (temporary; not part of the deliverable).

**Proof the probe can catch an error.** Run with `--inject`, the probe injects
`window.__oxyNoSuchFunction__()` on a timer plus a `console.error`. Both were caught:

```
FINDINGS: 3
 - console.error | probe injection: deliberate console.error
 - UNCAUGHT EXCEPTION | TypeError: window.__oxyNoSuchFunction__ is not a function
 - console.error | MissingDataError          <-- a real page defect, D2 below
```

The third line was not injected. It is how defect D2 was found.

**Steps exercised** (each followed by a 900 ms settle, on top of the page's 50 ms debounce):
load; species → catla; **district by map click** (a `MouseEvent` dispatched on a Leaflet polygon
path); district by select → Nagapattinam; district by select → The Nilgiris (hill, out of thermal
range); density slider to max and to min; **every** tariff preset in turn (`lt4_allied`,
`lt3a1_low`, `lt3a1_high`, `lt3b`, `custom`); a custom tariff of ₹9.50/kWh; reset to defaults with
a unit price of ₹45,000 (the payback path); language toggle to Tamil and back; theme toggle.

**Result after the fixes below:**

```
FINDINGS: 0
failedRequests: []
```

Zero uncaught exceptions, zero console errors or warnings, zero failed requests — on
`http://127.0.0.1:8765/index.html` and, separately, on
`file:///C:/Users/vivia/Code2/2_Business/NBG/oxyniti_yield%20_calc/site/index.html`.

**`file://` (no server).** Identical numbers to the served page, `window.OxyModel` ready, 48
assumption rows, both chart SVGs drawn, 125 interactive map paths (38 district polygons + 87
hotspot markers), zero errors. The data files are classic scripts, so nothing depends on `fetch`
except the optional `?fixture=1` path.

---

## 3. Defects found and fixed

| # | File:line | What | Why it mattered |
|---|---|---|---|
| D1 | `site/js/model.js:528-541` | A species with `estimable === false` now throws `MissingDataError` naming `species.missing[0]` and the species id, checked before the district is resolved. Previously the model named whichever load-bearing field it happened to read first (`survival_pct`). | Amendment A8 rule 2. It was the last parity mismatch: the oracle blamed `temp_optimum_c` (the data file's order), `model.js` blamed `survival_pct`. Two implementations must blame the same field or the fail-loud contract means nothing. Test added at `tests/model.test.mjs:507-541`, covering all eleven not-estimable species and the "species, not district, is blamed" case. |
| D2 | `site/js/ui.js:938-957` and `site/js/ui.js:673-687` | Choosing the "Custom" electricity tariff while the box was empty sent neither `tariff_id` nor `tariff_inr_kwh`, so `evaluate()` threw `MissingDataError` and the entire results card was replaced by "Missing data: no electricity tariff was supplied (expected tariff_id or tariff_inr_kwh)". The box is now seeded with the rate that was on screen (`state.lastTariffPresetId`, set in `applyTariffToControls`), and a genuinely missing tariff renders as "Enter an electricity tariff in ₹ per kWh, or choose one of the published tariffs." | Found by the console probe. A farmer who opens the Custom option has done nothing wrong and should not lose the estimate, let alone to developer wording. No silent default is introduced: the seeded rate is a sourced preset value that was already displayed, and it is visible in the box being edited. |
| D3 | `site/js/ui.js:360-375` | The stocking-density slider snapped the model's default to the nearest `min + k·step`, so GIFT tilapia opened at **5,982**/acre instead of the amendment-A3 default of **5,965**/acre. `min` is now shifted onto the same grid as the default (capped so it stays non-negative). | The page's opening scenario was not the scenario `OxyModel.defaultsFor()` resolved — a 0.29 % drift between the model and the page on the first thing anyone sees. Now exact. |
| D4 | `site/js/ui.js:71-89` (`fmtINR`, `bandJoin`), `:700-705`, `:844` | A loss printed as `₹-13,336` and was joined with an en-dash into `₹-13,336–₹-12,850`, which is close to unreadable. The sign now leads the symbol as a true minus (U+2212) glued to it with a word joiner (U+2060, so a line break can never separate them), and the band separator becomes "to" whenever either end is negative: **`−₹13,336 to −₹12,850`**. | The negative result *is* the headline finding of this tool. It has to be legible, and a dash-vs-minus ambiguity in a loss figure is exactly the kind of thing that gets misread in a sales conversation. |
| D5 | `site/css/styles.css:199-206` (`.results-card .btn-ghost`), `:356-362` (`.footer-logo`), `site/js/map.js:284-296` and `:322-332` (legend) | Three contrast and layout faults found by reading the screenshots: (a) the results card keeps the dark gradient in **both** themes, so "Copy summary" — styled from `--fg-strong`/`--border` — went dark-on-dark in light mode; the palette inside that card is now pinned to the dark one. (b) `assets/logo.svg` carries a `#073B43` wordmark drawn for a light background and all but vanished on the dark footer panel; the brand asset is untouched and now sits on a light plate. (c) the map legend was 230 px wide over a ~328 px map at 360 px; below 480 px the hotspot colour key is replaced by "Tap a marker for hotspot details." and the legend narrows to 164 px, keeping the production classes and the source/year footnote. | (a) and (b) made real controls and the brand mark unreadable in a shipped theme. (c) was reported by WP4 and is the fix its brief nominated. |

Also changed, not defects: the one-line sensitivity finding was added under the sizing block
(`site/index.html:264`, `site/css/styles.css:296-303`, string `results.sensitivity` in
`site/js/i18n.js`); a `?theme=light` / `?theme=dark` query hook was added
(`site/js/ui.js:140-151`) so both themes can be screenshotted deterministically; the twelve-entry
source list was written into `<ul id="data-sources">` (`site/index.html:376-389`); and three
stray `+18%` were aligned to `+18 %` to match `MODEL_SPEC.md` and the `i18n` strings.

No model coefficient and no part of the ceiling was touched. No file under `research/` was
edited. In `plan/`, only this file was created.

---

## 4. Screenshots

In `tests/screenshots/`. All shot with headless Chrome. **Method note:** `--window-size=360,800`
does **not** produce a 360 px viewport on this platform — Chrome clamps the window and the page
lays out at 512 CSS px, so the PNG is a crop and every narrow-screen rule silently fails to apply.
The first 360 px shots of this pass were wrong for exactly that reason. The shots below use
`Emulation.setDeviceMetricsOverride` + `Page.captureScreenshot` over CDP, which gives the exact
viewport; each run also reports `document.documentElement.scrollWidth` so horizontal overflow is
measured, not eyeballed.

| File | Viewport | What was checked |
|---|---|---|
| `wp6_360x800.png` | 360 × 800, dark | Header, map and district card at the narrowest target. `scrollWidth` 360 = viewport, **no horizontal scroll**. Legend 164 px with the hotspot key hidden (D5c); tile attribution wraps to two lines and stays legible. |
| `wp6_360x2600.png` | 360 × 2600, dark | Whole input column. Every label, slider readout and hint reads; stocking density shows **5,965 /acre** (D3); no overlap; select text truncation is native and acceptable. |
| `wp6_360x2600_results.png` | 360 × 2600, dark, scrolled to `#results-card` | Results, sensitivity note, both warnings, ceiling note, both charts, the collapsed Assumptions panel. Sizing sub-line reads "Best number of units for profit: 1 · Units for full pre-dawn relief: 7 · 0.16 mg/L/unit/night · worst-month deficit 1.04 mg/L" — `n_best` and `n_relief` both present as amendment A4 requires. |
| `wp6_360x2600_light.png` | 360 × 2600, light, scrolled to `#results-card` | Same region in the light theme after D4 and D5a. "Copy summary" now legible; the minus stays glued to ₹ across the line break; chart colours read in both themes. |
| `wp6_360x2600_footer.png` | 360 × 2600, dark, scrolled to the footer | "How this is calculated", known limitations and all twelve source lines with their licences. |
| `wp6_768x1400.png` | 768 × 1400, dark | Single-column breakpoint below 900 px. `scrollWidth` 768; no overlap; the legend returns to its full 230 px form above 480 px. |
| `wp6_1280x1800.png` | 1280 × 1800, dark | Two-column desktop layout: map beside the district card, inputs beside results. `scrollWidth` 1280. |
| `wp6_1280x1800_light.png` | 1280 × 1800, light | The light theme at desktop width, after the contrast fixes. |
| `wp6_1280x900_footer.png` | 1280 × 900, dark, scrolled to the footer | The footer logo on its light plate (D5b) and the two-column source list. |
| `wp6_file_1280x1800.png` | 1280 × 1800, `file://` | The no-server path renders identically, including the map and both charts. |

The only elements wider than the viewport at 360 px are the rows of the assumptions table, which
lives inside `.assumptions-table-wrap` and scrolls within its own box — the document itself does
not scroll horizontally at any tested width.

---

## 5. Content checks

| Check | Result |
|---|---|
| Ceiling note from `MODEL_SPEC.md` section 5 present | Yes — `site/index.html:272` and `results.ceiling_note` in `site/js/i18n.js:93`, with the +12 % / +5 points decomposition and "Not a guarantee". |
| Every warning code has a plain-English sentence | Yes — all seven codes emitted by `site/js/model.js` (`THERMAL_OUT_OF_RANGE`, `CEILING_CLAMPED`, `SIZING_CAPPED`, `CONCENTRATOR_POWER_UNKNOWN`, `PRICE_OUT_OF_SOURCED_RANGE`, `NOT_OXYGEN_LIMITED`, `NO_PAYBACK_AT_PUBLISHED_O2`) map through `WARNING_KEYS` to a `warning.*` string in `site/js/i18n.js:156-162`. |
| Assumptions table lists every ASSUMED coefficient used | Yes — 48 rows render for the default scenario. `plan/coefficients.json` holds 69 envelope entries (56 ASSUMED, 11 VERIFIED, 2 UNTESTED); the panel shows those the evaluation actually consumed, plus the resolved species and tariff values, each with status, date and source. All 56 ASSUMED coefficients are tabulated in `site/README.md`. |
| WhatsApp link | `https://wa.me/919659727477?text=<encoded summary>` — `site/js/ui.js:855`, with the bare form as the `href` fallback in `site/index.html:275`. |
| Placeholder scan (`YOUR_`, `XXXXX`, `TODO`, `info@`, `+91 98765`) under `site/` | Clean — `grep -rnE` returns nothing, including the new `site/README.md`. |
| `deploy.ps1 -DryRun` | Parses and passes its own placeholder gate; printed the nine publish steps and the target URL `https://vivian4fb.github.io/oxyniti-yield-calc/`. Not run without `-DryRun` — publishing is the owner's action. |
| British English | `colour`, `licences`, `optimum`, `normals`, `metre`-free (the page uses `m`); no `color`/`license`/`optimize`/`behavior` in any prose string. The only matches are CSS property names and the abbreviation "DO meter" (dissolved-oxygen meter). |
| `en-IN` grouping and lakh above 99,999 | `fmtNum`, `fmtKg` and `fmtINR` all use `Intl.NumberFormat('en-IN')`; `fmtINR` switches to lakh with one decimal above ₹99,999 (`₹1.5 L`), sign-leading for losses. Verified on screen: `3,238 kg`, `₹70,709`, `5,965 /acre`. |
| Sensitivity line present | Yes, one sentence, under the sizing block — `site/index.html:264`. |

---

## 6. The default scenario, as the page renders it

GIFT tilapia · Tiruchirappalli · 1.00 acre · 1.5 m · 5,965/acre · July stocking · medium bloom ·
₹110/kg · ₹55/kg feed · no existing aeration · LT III-A(1) above 500 units (₹6.95/kWh) ·
1.5 HP unit · auto sizing · 8 h/night:

- **Extra harvest** 13 kg–26 kg per crop · 33 kg–66 kg per year
- **Extra profit** −₹13,336 to −₹12,850 per crop · −₹33,339 to −₹32,124 per year
- **Payback** "Enter unit price" with no price; "No extra profit at these inputs" once a price is
  entered — blocked either way
- **Units** 1 × Nano Bubble Generator 1.5 HP; best for profit 1, full pre-dawn relief would need
  7; 0.16 mg/L per unit per night against a worst-month deficit of 1.04 mg/L
- **Baseline, for context** 3,238 kg harvest, ₹70,709 profit
- **Warnings** `CONCENTRATOR_POWER_UNKNOWN`, `NO_PAYBACK_AT_PUBLISHED_O2`

The negative result is correct arithmetic on the published 2 L/min figure and has been left
untouched and visible. Nothing was tuned to hide it.

---

## 7. Open items

1. **The product's published oxygen input cannot pay for its own electricity.** At 2 L/min the
   1.5 HP unit adds 0.16 mg/L per night to a 1 acre × 1.5 m pond, against a worst-month deficit
   of 1.04 mg/L; seven units would relieve the pond, and one is the profit-maximising count only
   because every count loses money. **Not a defect in the tool** — it is what the published figure
   implies. Closing it needs the OEM datasheet oxygen delivery (kg O₂/h per model) and the
   concentrator's power draw. `EXECUTION_PLAN.md` section 7 item 1; the Advanced panel already
   accepts both overrides.
2. **Unit price is unknown, so payback is blocked on every scenario.** Both product pages show
   ₹4,400, treated as a placeholder. `EXECUTION_PLAN.md` section 7 item 2.
3. *(Not blocking, carried from earlier packages)* Tamil is partial by design — the toggle reads
   "தமிழ் (partial)" and new strings fall back to English pending native review
   (`EXECUTION_PLAN.md` section 7 item 7). The `docs/NBG_Trichy_Prospecting_Report.md` supersession
   banner (section 7 item 5) is outside this tool and remains outstanding.

No defect found in this pass was left unfixed.

## Post-QA edits by the coordinating session (2026-09-21)

- `site/js/map.js`: added `zoomSnap: 0.25` so `fitBounds` frames Tamil Nadu instead of snapping out to zoom 6; moved the legend control from bottom-right to bottom-left so it no longer covers the Cauvery delta coast. Re-ran `node --test tests/*.test.mjs` (38/38), `python tests/compare.py` (PASS) and the placeholder scan (clean); screenshot `tests/screenshots/final_map_1280x720.png`.

## Map fixes after owner review (2026-09-21, coordinating session)

- Owner screenshot showed OpenStreetMap "Access blocked" tiles. Cause established with curl: without an HTTP Referer the OSM tile server returns HTTP 200 with a 6,987 B block image; with any Referer (GitHub Pages, localhost, oxyniti.com) it returns the 29,734 B tile. A page opened from `file://` sends no Referer. Fix in `site/js/map.js`: `referrerPolicy: strict-origin-when-cross-origin` on the tile layer, Esri World Street Map as the basemap for `file://` pages, and a one-tile probe on `http(s)` that switches to the same fallback if the block image is served (CARTO was tried first and rejected: it watermarks Referer-less requests "API key required"). `site/index.html` gained a referrer meta tag.
- Map enlarged: `.map-grid` is now single-column, `#map` height `clamp(460px, 72vh, 780px)` (380 px below 900 px), district card restyled as a strip under the map.
- Verified: `tests/screenshots/final2_http_1280x1000.png` (OSM tiles over http), `final3_file_1280x1000.png` (Esri tiles from file://), `final2_http_768x1100.png`; Chrome stderr log clean of Uncaught/TypeError on both paths; `node --test` 38/38; `python tests/compare.py` PASS; placeholder scan clean.
