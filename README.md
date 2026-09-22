# Oxyniti yield and profit calculator for Tamil Nadu fish and shrimp ponds

A standalone, dependency-free web tool that estimates the extra harvest, extra profit and
payback from Oxyniti nano-bubble aeration for one pond, by species, district or city climate,
stocking month, stocking density, pond bloom and existing aeration, with an interactive map of
Tamil Nadu's aquaculture hotspots.

**Live page:** https://vivian4fb.github.io/oxyniti-yield-calc/

The estimate is illustrative and capped at Oxyniti's internal model of **+18 % saleable
kilograms**, reached only for a pond that is fully oxygen-limited in every crop month. It is
not a guarantee; Oxyniti verifies the effect on the farmer's own pond with a DO meter during
the free demo.

## Repository layout

| Path | What it holds |
|---|---|
| `site/` | The published page: `index.html`, `css/`, `js/` (model, page, charts, map, i18n, lead capture), `data/` (classic-script data files), vendored Leaflet 1.9.4, brand assets, and its own README with the data sources and licences |
| `plan/` | Model specification with amendments A1–A9, execution plan, coefficients with status labels, deviations log, data status, QA report, owner inputs |
| `research/` | The sourced data behind everything: species parameters, IMD 1991–2020 climate normals for 32 stations, dissolved-oxygen physics, economics and device evidence, district GeoJSON, hotspots |
| `tests/` | Node contract tests for the model, an independent Python oracle, a scenario set, a comparator with a self-test, and QA screenshots |
| `tools/build_data.py` | Rebuilds `site/data/` from `research/` and `plan/` deterministically |
| `tools/leads/` | Owner-side lead vetting (`vet_lead.py`) and report building (`make_report.py`); runbook in its README. Its `inbox/`, `reports/` and `ledger.jsonl` are git-ignored personal data |
| `.github/workflows/pages.yml` | Publishes `site/` to GitHub Pages on every push to `main` |

## Lead capture and the report gate

The page shows the extra-harvest band live and nothing else from the model. Extra profit,
payback, unit sizing, the oxygen budget and the charts are delivered as a written report,
requested through "Get my pond report" (name, Indian mobile, village, role, pond count,
consent) and sent by the owner **after vetting** the request for bots and competitors. Two
routes carry the request out of this static page: a WhatsApp deep link with a reference
code (always on) and an optional JSON endpoint set in `site/js/leads.config.js`. Design in
`plan/LEAD_CAPTURE.md`; owner runbook in `tools/leads/README.md`.

## Running it locally

```sh
cd site
python -m http.server 8765
# open http://127.0.0.1:8765/index.html
```

Opening `site/index.html` straight from disk also works: the page then uses Esri street tiles
for the basemap, because OpenStreetMap's tile servers require an HTTP Referer that browsers do
not send for local files.

## Tests

```sh
node --test tests/*.test.mjs          # 43 model contract tests + 14 lead-capture helper tests
python -m unittest tests/test_vet_lead.py   # lead vetting, reference decoding, report build (21)
node tests/smoke_leads.mjs            # headless-Chrome check of the gate and the form (serve site/ first)
python tests/compare.py               # JavaScript vs independent Python oracle, 29 scenarios
python tests/compare.py --self-test   # proves the comparator detects an injected defect
python tests/compare.py --doonly      # oxygen-solubility table check (Benson & Krause 1984)
```

## Status of every number

Every coefficient, species parameter and price carries a status label: `VERIFIED` (read on the
cited page or stated by the owner), `ASSUMED` (a modelling choice or an owner-authorised rough
estimate, with its basis), `UNTESTED` or `NOT_FOUND`. The page shows all of them in its
Assumptions panel. Unit prices and the concentrator price are rough estimates until the owner
replaces them; the 1.5 HP unit's oxygen input (1–2 L/min) and the concentrator's 230 V, 3 A
draw are owner-stated on 2026-09-21.

## Data licences

- District boundaries: geoBoundaries gbOpen IND ADM2 (boundaryID IND-ADM2-76128533), licensed
  under the **Open Database License (ODbL) 1.0**. The derived file `site/data/tn_districts.data.js`
  is therefore also made available under ODbL 1.0; attribution and share-alike apply to it.
- Basemap tiles: © OpenStreetMap contributors (ODbL), or Tiles © Esri when the page runs from disk.
- Climate normals: India Meteorological Department, Pune, Climatological Tables 1991–2020.
- District production: Department of Economics and Statistics, Statistical Hand Book of Tamil
  Nadu 2021–22, Tables 8.2 and 8.3; Fisheries Policy Note 2025–26, Tables 4, 7 and 8.
- Crop economics: NABARD/TNAU model bankable projects (2015); NFDB murrel model.
- Electricity: TNERC tariff orders, rates effective 1 July 2025.
- Oxygen solubility and respiration: Benson & Krause (1984); Leonard & Skov (2022); Brahmane et
  al. (2014); Boyd's night-time budget.

The full source list with links is in `site/README.md`. Code and text in this repository are
© Oxyniti 2026; no licence is granted for reuse of the code beyond viewing the published page.
