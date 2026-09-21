# Tamil Nadu aquaculture geography — sourced findings

*Prepared 2026-09-21 for the Oxyniti hotspot map (Leaflet). British English. Every figure carries units, year and a source number [Sn] from the register in §11. Status labels: VERIFIED = read in the cited source on 2026-09-21; ASSUMED = inferred, reason stated; NOT_FOUND = looked for, not found (route stated). Deltas are computed here from the cited tables.*

## 0. Verdict

**The best district-level production data that exist in the public domain are the Department of Economics and Statistics (DES) *Statistical Hand Book of Tamil Nadu 2021-22*, Chapter 8, Tables 8.2 (marine) and 8.3 (inland), data year 2021-22, sourced from the Commissioner of Fisheries [S1]; no official district-wise table for 2022-23, 2023-24 or 2024-25 was found anywhere online (route: DES site, Fisheries Department site and its 2023-24/2024-25/2025-26 Policy Notes, data.gov.in, PIB, NFDB/DoF handbooks).** District-wise CAA-registered shrimp farms exist for early 2025 in the Fisheries Policy Note 2025-26, Table 4 [S3]. The freshwater core is the Cauvery delta: Thanjavur + Tiruvarur + Mayiladuthurai + Nagapattinam produced 80,914.25 t of the state's 211,548.35 t inland output in 2021-22 (38.2 %) [S1]. The brackish (shrimp) core is Nagapattinam–Mayiladuthurai–Thanjavur–Tiruvarur: 1,642 of 2,382 CAA-registered farms (68.9 %) and 3,153.26 of 4,569.63 ha water-spread area (69.0 %) [S3].

## 1. Boundary file (`tn_districts.geojson`)

| Item | Value | Status |
|---|---|---|
| Chosen source | geoBoundaries gbOpen, IND ADM2, boundaryID IND-ADM2-76128533, year represented 2021, build 12 Dec 2023, commit 9469f09; upstream Pathways Data Pvt. Ltd. / lgdirectory.gov.in [S25] | VERIFIED 2026-09-21 |
| Licence | **Open Data Commons Open Database License 1.0 (ODbL)** as returned by the geoBoundaries API `boundaryLicense` field for this layer — *not* CC BY 4.0 (the brief assumed CC BY; geoBoundaries publishes some country layers under other licences). Attribution to geoBoundaries and the upstream source is required; share-alike applies to derived databases. | VERIFIED 2026-09-21 |
| Feature count | 38 of 38 current districts (all six post-2019 districts present: Tenkasi, Kallakurichi, Chengalpattu, Ranipet, Tirupattur, Mayiladuthurai). Selected from the 735-feature India file by `shapeName` match plus bounding-box check; zero duplicate names, zero name collisions elsewhere in India. Counted with Python `json.load`. | VERIFIED 2026-09-21 |
| Name normalisation | `district` property set to the official English spelling (Chengalputtu → Chengalpattu, Thoothukkudi → Thoothukudi, Tirupathur → Tirupattur, Thiruvallur → Tiruvallur, Thiruvarur → Tiruvarur); the original `shapeName` kept as `source_name`. | VERIFIED |
| Size | 1,734,667 bytes raw subset → 1,505,507 bytes after rounding coordinates to 5 dp (≈ 1 m); 76,338 vertices; **under the 2 MB threshold, so no geometry simplification was applied** (Douglas–Peucker on independent polygons would open slivers along shared district edges). geoBoundaries' own topology-preserving simplified layer (403,021 bytes for the 38 districts) is available at the API's `simplifiedGeometryGeoJSON` URL if a lighter file is ever wanted. | VERIFIED |
| Rejected alternatives | udit-001/india-maps-data `tamil-nadu.geojson`: 37 features — Mayiladuthurai missing (still inside Nagapattinam), no licence stated (README: 'curated from publicly available sources'). datameet/maps: Census 2001/2011 districts only (32). HDX: the only India district layer listed is the same geoBoundaries data (`geoboundaries-admin-boundaries-for-india`, ODbL); `cod-ab-ind` does not exist. | VERIFIED 2026-09-21 |

## 2. State-level baseline

| Metric | Value | Year | Source | Status |
|---|---|---|---|---|
| Total fish production | 8.84 lakh t | 2023-24 | [S3] §1, §9 | VERIFIED |
| Marine fish production | 637,441.70 t (6.37 lakh t) | 2023-24 | [S6] item 10; [S3] | VERIFIED |
| Inland fish production | 246,576.21 t (2.47 lakh t) | 2023-24 | [S6] item 13; [S3] Table 3 | VERIFIED |
| Inland fish production (website figure) | 2.32 lakh t | 2023-24 | [S7] /InlandFisheries page (mirror and Wayback 2025-03-28) | VERIFIED — conflicts with the 2.47 lakh t above; see §9 |
| Marine fish production | 595,176.98 t | 2021-22 | [S1] Table 8.1 | VERIFIED |
| Inland fish production | 211,548.35 t (value Rs 4,824.28 crore) | 2021-22 | [S1] Table 8.1 | VERIFIED |
| Marine / inland | 583,031.05 t / 174,428.32 t | 2019-20 | [S2] Table 8.1 | VERIFIED |
| Total production series | 6.69, 6.82, 6.90, 7.57, 7.23, 8.06, 8.29 lakh t for 2016-17 … 2022-23 | 2016-17 to 2022-23 | [S13] p.3 chart | VERIFIED |
| CMFRI marine landings (calendar year) | 6.79 lakh t in 2024 (+20 % on 2023); 6.85 lakh t in 2025 (highest of all states) | 2024, 2025 | [S9]; CMFRI 2025 landings release (news reports only, not read at source) | 2024 VERIFIED; 2025 ASSUMED |
| Inland water resources | 385,761 ha = reservoirs 62,015.06 ha + brackish water 56,000 ha + others 267,746.14 ha | 2023-24 | [S6] item 1; [S1] Table 8.1 | VERIFIED |
| Reservoirs under fishery management | 62 (54 Fisheries Dept + 8 TNFDC), 56,075 ha; 636 irrigation tanks, 40,149 ha | 2024-25 | [S3] Table 3 | VERIFIED |
| Inland fisherfolk | 2.36 lakh | 2023-24 | [S3] Table 3; [S6] | VERIFIED |
| Shrimp farms registered with CAA | 2,382 farms, 4,569.63 ha water-spread area; 110 shrimp hatcheries (15.6 billion PL/yr capacity) | 'at present' (note dated 2025) | [S3] §6.1 and Tables 3-4 | VERIFIED |
| Tamil Nadu farmed-shrimp output | 0.41 lakh t (5th in India; national 11.61 lakh t) | 2023-24 | [S3] §6.1 | VERIFIED |

## 3. District-wise fish production

### 3.1 Inland fish production by district — 2021-22 versus 2019-20

Source: [S1] Table 8.3 'Estimated Inland Fish Production by Districts for the year 2021-22' (37 districts; Chennai not listed) and [S2] Table 8.3 for 2019-20 (32 pre-split districts). Both tables cite 'Commissioner of Fisheries, Chennai-35'. Deltas computed here; for districts split after 2019-20 the delta is against the parent district's 2019-20 figure and is shown on the parent line. 'Share' is the district's share of the state inland total (%).

| District (2021-22) | Inland 2021-22 (t) | Share 2021-22 (%) | Inland 2019-20 (t) | Δ t | Δ % | Status |
|---|---:|---:|---:|---:|---:|---|
| Tiruvallur | 18,497.80 | 8.74 | 17,681.19 | 816.61 | +4.6 | VERIFIED |
| Kancheepuram (parent of Chengalpattu) | 5,501.83 | 2.60 | 14,818.28 (undivided) | 212.58 (combined 15,030.86 t) | +1.4 (combined) | VERIFIED |
| Chengalpattu (carved from Kancheepuram) | 9,529.03 | 4.50 | — (inside Kancheepuram) | — | — | VERIFIED |
| Vellore (parent of Ranipet, Tirupattur) | 221.56 | 0.10 | 1,550.86 (undivided) | 181.60 (combined 1,732.46 t) | +11.7 (combined) | VERIFIED |
| Ranipet (carved from Vellore) | 1,327.76 | 0.63 | — (inside Vellore) | — | — | VERIFIED |
| Tirupattur (carved from Vellore) | 183.14 | 0.09 | — (inside Vellore) | — | — | VERIFIED |
| Tiruvannamalai | 1,889.39 | 0.89 | 1,568.94 | 320.45 | +20.4 | VERIFIED |
| Cuddalore | 19,364.00 | 9.15 | 13,281.10 | 6,082.90 | +45.8 | VERIFIED |
| Viluppuram (parent of Kallakurichi) | 2,984.05 | 1.41 | 3,529.39 (undivided) | 1,587.39 (combined 5,116.78 t) | +45.0 (combined) | VERIFIED |
| Kallakurichi (carved from Viluppuram) | 2,132.73 | 1.01 | — (inside Viluppuram) | — | — | VERIFIED |
| Salem | 9,395.15 | 4.44 | 9,004.88 | 390.27 | +4.3 | VERIFIED |
| Namakkal | 6,849.18 | 3.24 | 7,232.53 | -383.35 | -5.3 | VERIFIED |
| Tiruppur | 452.22 | 0.21 | 448.59 | 3.63 | +0.8 | VERIFIED |
| Coimbatore | 569.50 | 0.27 | 356.35 | 213.15 | +59.8 | VERIFIED |
| Erode | 1,667.86 | 0.79 | 1,151.56 | 516.30 | +44.8 | VERIFIED |
| The Nilgiris | 6.26 | 0.00 | 6.64 | -0.38 | -5.7 | VERIFIED |
| Dharmapuri | 3,116.91 | 1.47 | 647.48 | 2,469.43 | +381.4 | VERIFIED |
| Krishnagiri | 13,005.79 | 6.15 | 8,714.60 | 4,291.19 | +49.2 | VERIFIED |
| Tiruchirappalli | 864.29 | 0.41 | 878.56 | -14.27 | -1.6 | VERIFIED |
| Karur | 522.96 | 0.25 | 516.84 | 6.12 | +1.2 | VERIFIED |
| Perambalur | 474.94 | 0.22 | 421.97 | 52.97 | +12.6 | VERIFIED |
| Ariyalur | 626.92 | 0.30 | 546.59 | 80.33 | +14.7 | VERIFIED |
| Pudukkottai | 4,126.62 | 1.95 | 3,937.00 | 189.62 | +4.8 | VERIFIED |
| Thanjavur | 46,125.64 | 21.80 | 40,094.43 | 6,031.21 | +15.0 | VERIFIED |
| Tiruvarur | 10,535.00 | 4.98 | 6,423.79 | 4,111.21 | +64.0 | VERIFIED |
| Mayiladuthurai (carved from Nagapattinam) | 19,301.25 | 9.12 | — (inside Nagapattinam) | — | — | VERIFIED |
| Nagapattinam (parent of Mayiladuthurai) | 4,952.36 | 2.34 | 19,778.48 (undivided) | 4,475.13 (combined 24,253.61 t) | +22.6 (combined) | VERIFIED |
| Madurai | 1,482.80 | 0.70 | 1,533.84 | -51.04 | -3.3 | VERIFIED |
| Theni | 2,105.43 | 1.00 | 2,003.58 | 101.85 | +5.1 | VERIFIED |
| Dindigul | 872.02 | 0.41 | 882.09 | -10.07 | -1.1 | VERIFIED |
| Virudhunagar | 1,204.10 | 0.57 | 1,267.27 | -63.17 | -5.0 | VERIFIED |
| Sivaganga | 758.80 | 0.36 | 356.99 | 401.81 | +112.6 | VERIFIED |
| Ramanathapuram | 4,569.92 | 2.16 | 2,788.90 | 1,781.02 | +63.9 | VERIFIED |
| Tirunelveli (parent of Tenkasi) | 1,562.51 | 0.74 | 2,017.10 (undivided) | 692.27 (combined 2,709.37 t) | +34.3 (combined) | VERIFIED |
| Tenkasi (carved from Tirunelveli) | 1,146.86 | 0.54 | — (inside Tirunelveli) | — | — | VERIFIED |
| Thoothukudi | 6,035.07 | 2.85 | 3,080.60 | 2,954.47 | +95.9 | VERIFIED |
| Kanniyakumari | 7,586.70 | 3.59 | 7,907.90 | -321.20 | -4.1 | VERIFIED |
| Chennai | not listed | — | 0.00 | — | — | NOT_FOUND in 2021-22 table; 0.00 t in 2019-20 [S2] |
| **State total** | **211,548.35** | 100.00 | 174,428.32 | 37,120.03 | +21.3 | VERIFIED |

Top eight inland districts 2021-22 [S1]: Thanjavur 46,126 t (21.8 %); Cuddalore 19,364 t (9.2 %); Mayiladuthurai 19,301 t (9.1 %); Tiruvallur 18,498 t (8.7 %); Krishnagiri 13,006 t (6.1 %); Tiruvarur 10,535 t (5.0 %); Chengalpattu 9,529 t (4.5 %); Salem 9,395 t (4.4 %). Together 68.9 % of the state.

### 3.2 Marine fish production by district — 2021-22, 2019-20 and CMFRI calendar-2024 landings

Sources: [S1] Table 8.2 (2021-22, 14 coastal districts, craft-wise; total 595,176.98 t); [S2] Table 8.2 (2019-20, 13 districts; total 583,031.05 t) — **in the 2019-20 PDF the 'Total' cells of Villupuram and Cuddalore are transposed** (Villupuram components 622.91 + 11,688.95 + 2,606.43 = 14,918.29 t = the printed 2.56 %; Cuddalore components sum to 49,253.79 t = the printed 8.45 %); the component sums are used here. CMFRI 2024 figures are calendar-year landings estimates reported by ICAR to Parliament [S9]; tonnes for the five districts given only as percentages are derived here as share × 6.79 lakh t (rounding uncertainty ≈ ±340 t) and are ASSUMED.

| District | Marine 2021-22 (t) | Share 2021-22 (%) | Marine 2019-20 (t) | Δ t (19-20→21-22) | CMFRI 2024 (t) | CMFRI 2024 share (%) | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| Chennai | 54,876.44 | 9.22 | 44,795.17 | 10,081.27 | 91,927 | 13.5 | VERIFIED |
| Tiruvallur | 32,435.20 | 5.45 | 27,649.78 | 4,785.42 | not reported | — | VERIFIED (2021-22); NOT_FOUND (2024) |
| Chengalpattu | 35,377.33 | 5.94 | 34,761.01 (as Kancheepuram) | 616.32 (vs Kancheepuram) | not reported | — | VERIFIED (2021-22); NOT_FOUND (2024) |
| Viluppuram | 18,213.90 | 3.06 | 14,918.29 | 3,295.61 | ≈ 38,703 (derived) | 5.7 | VERIFIED (2021-22); ASSUMED (2024 t) |
| Cuddalore | 61,893.06 | 10.40 | 49,253.79 | 12,639.27 | ≈ 25,123 (derived) | 3.7 | VERIFIED (2021-22); ASSUMED (2024 t) |
| Mayiladuthurai | 15,959.81 | 2.68 | — (inside Nagapattinam) | — | not reported | — | VERIFIED (2021-22); NOT_FOUND (2024) |
| Nagapattinam | 58,684.57 | 9.86 | 86,881.15 (undivided) | -12,236.77 (combined 74,644.38 t) | ≈ 26,481 (derived) | 3.9 | VERIFIED (2021-22); ASSUMED (2024 t) |
| Tiruvarur | 1,838.89 | 0.31 | 1,789.47 | 49.42 | not reported | — | VERIFIED (2021-22); NOT_FOUND (2024) |
| Thanjavur | 38,556.64 | 6.48 | 31,136.92 | 7,419.72 | ≈ 49,567 (derived) | 7.3 | VERIFIED (2021-22); ASSUMED (2024 t) |
| Pudukkottai | 49,003.01 | 8.23 | 46,169.00 | 2,834.01 | ≈ 67,221 (derived) | 9.9 | VERIFIED (2021-22); ASSUMED (2024 t) |
| Ramanathapuram | 82,961.31 | 13.94 | 87,909.70 | -4,948.39 | 87,140 | 12.8 | VERIFIED |
| Thoothukudi | 54,524.43 | 9.16 | 63,105.99 | -8,581.56 | 113,356 | 16.7 | VERIFIED |
| Tirunelveli | 9,713.13 | 1.63 | 9,610.80 | 102.33 | not reported | — | VERIFIED (2021-22); NOT_FOUND (2024) |
| Kanniyakumari | 81,139.26 | 13.63 | 85,049.98 | -3,910.72 | 157,280 | 23.2 | VERIFIED |
| **State total** | **595,176.98** | 100.00 | 583,031.05 | 12,145.93 | 679,000 | 100 | VERIFIED |

Note on the 2023-24 marine total (637,441.70 t, [S6]) versus CMFRI 2024 (679,000 t, [S9]): different estimators (state Fisheries Department financial-year estimate versus ICAR-CMFRI calendar-year sample survey); a 41,558 t (6.5 %) gap between them is normal and is not a data error. Coastline by district (km) for context [S7 /MarineFisheries]: Ramanathapuram 236.8, Thoothukudi 163.5, Nagapattinam 117.0, Chengalpattu 87.2, Kanniyakumari 71.5, Mayiladuthurai 70.9, Cuddalore 57.5, Tirunelveli 48.9, Tiruvarur 47.2, Thanjavur 45.1, Pudukkottai 42.8, Viluppuram 40.7, Tiruvallur 27.9, Chennai 19.0; total 1,076.0.

### 3.3 Newer but undated district figures — central/delta districts (press)

DT Next, 11 Aug 2025 [S16], prints a table 'District — Quantity (in tonne) — Contribution in State (%)': Tiruchy 873 (0.38); Karur 552 (0.24); Perambalur 477 (0.21); Ariyalur 628 (0.27); Pudukkottai 4,213 (1.82); Thanjavur 46,157 (19.90); Tiruvarur 10,570 (4.56); Mayiladuthurai 12,328 (5.32); Nagapattinam 3,597 (1.55). **The article does not state the year or the issuing office.** 46,157 t ÷ 19.90 % = 231,945 t ≈ the 2.32 lakh t inland figure the Department publishes for 2023-24 [S7], so the table is most probably the Department's 2023-24 district estimate (ASSUMED; the same article says 'the Delta region contributes 35 per cent of total inland fish production' and quotes a state value of Rs 6,279 crore). Treat as ASSUMED 2023-24 until the source table is obtained.

### 3.4 Source-wise inland production 2021-22 [S1 Table 8.4]

Reservoirs 4,858.20 t; major irrigation tanks (perennial/long-seasonal) 43,233.29 t; short-seasonal tanks and ponds 67,661.35 t; intensive inland fish-culture tanks 6,873.12 t; **DFFDA tanks and private farms 19,085.91 t**; rivers, streams, canals 18,649.99 t; miscellaneous (brackish water and farms) 51,186.49 t; total 211,548.35 t. In 2019-20 [S2 Table 8.4] the FFDA line was 15,298.98 t and brackish 46,990.44 t of 174,428.32 t. **Implication for Oxyniti: pond and tank culture (short-seasonal tanks + intensive tanks + DFFDA/private farms ≈ 93,620 t, 44 % of inland output) is where aeration applies; reservoir capture (2.3 %) is not an aerator market.**

## 4. Registered shrimp farms (Coastal Aquaculture Authority) and brackish-water resources

### 4.1 District-wise CAA-registered shrimp farms — Fisheries Policy Note 2025-26, Table 4 [S3]

| District | Registered farms (no.) | Water-spread area (ha) | Share of farms (%) | Mean WSA per farm (ha) | Status |
|---|---:|---:|---:|---:|---|
| Nagapattinam | 710 | 1,245.31 | 29.8 | 1.75 | VERIFIED |
| Thanjavur | 361 | 735.07 | 15.2 | 2.04 | VERIFIED |
| Mayiladuthurai | 359 | 689.14 | 15.1 | 1.92 | VERIFIED |
| Tiruvarur | 212 | 483.74 | 8.9 | 2.28 | VERIFIED |
| Cuddalore | 188 | 311.48 | 7.9 | 1.66 | VERIFIED |
| Ramanathapuram | 161 | 389.27 | 6.8 | 2.42 | VERIFIED |
| Tiruvallur | 125 | 249.80 | 5.2 | 2.00 | VERIFIED |
| Viluppuram | 101 | 134.50 | 4.2 | 1.33 | VERIFIED |
| Chengalpattu | 81 | 102.29 | 3.4 | 1.26 | VERIFIED |
| Pudukkottai | 57 | 121.15 | 2.4 | 2.13 | VERIFIED |
| Thoothukudi | 26 | 107.38 | 1.1 | 4.13 | VERIFIED |
| Kanniyakumari | 1 | 0.50 | 0.0 | 0.50 | VERIFIED |
| **Total** | **2382** | **4,569.63** | 100.0 | 1.92 | VERIFIED (column sums check: 2382 farms, 4,569.63 ha) |

Districts with a coastline but absent from Table 4 (hence 0 registered farms in this register): Chennai, Tirunelveli. The register is the state's tabulation of CAA data 'at present' in a note published April 2025; the CAA's own per-district query pages linked from https://caa.gov.in/farms.html (12 Tamil Nadu districts) returned HTTP 404 on 2026-09-21 [S28], so the CAA site could not be used to count farms directly. The CAA launched its national 100 % farm-registration campaign at Nagapattinam on 14 Feb 2024 [S12], so registered counts are rising and lag the true farm count.

### 4.2 State-level series of CAA registrations (all VERIFIED; dates are publication dates)

| Publication | Farms | Area (ha) | Hatcheries | Districts |
|---|---:|---:|---:|---|
| Policy Note 2023-24 (2023) [S5] | 2,177 | 4,207.34 | 78 | — |
| DoF GoI Tamil Nadu deck (uploaded 2026-04, data undated) [S13] | 2,702 | 5,041.26 | 71 | 11 |
| Policy Note 2024-25 (2024) [S4] | 2,360 | 4,536.46 | 80 (capacity 15,665 million PL) | — |
| Policy Note 2025-26 (2025) [S3] | 2,382 | 4,569.63 | 110 (15.6 billion PL/yr) | 12 (Table 4) |
| fisheries.tn.gov.in /Aquaculture (Wayback 2025-03-19; mirror 2026-09) [S7] | 3,001 | 5,745.01 | 71 | 13 maritime districts |

The 3,001-farm / 5,745.01 ha figure on the website is the outlier; it is undated and is probably a cumulative ever-registered count, whereas the Policy Notes report currently valid registrations (ASSUMED reason). Use the Policy Note 2025-26 table for the map and say so.

### 4.3 Brackish-water area by district (resource, not farms) — fisheries.tn.gov.in /Aquaculture [S7]

| District | Brackish-water area (ha) |
|---|---:|
| Tiruvallur | 12,600 |
| Chengalpattu | 4,500 |
| Viluppuram | 8,100 |
| Cuddalore | 3,863 |
| Mayiladuthurai + Nagapattinam (one row in source) | 19,600 |
| Thanjavur | 5,500 |
| Tiruvarur | 3,500 |
| Pudukkottai | 400 |
| Ramanathapuram | 1,115 |
| Tirunelveli | 217 |
| Thoothukudi | 850 |
| Kanniyakumari | 355 |
| **Total** | **56,000** |

Named brackish systems [S5 p.21]: Pulicat lake, Araniar, Ennore, Muttukadu backwater (Tiruvallur/Chennai/Chengalpattu); Pazhayar, Pitchavaram, Coleroon, Gedilam (Cuddalore/Mayiladuthurai); Muthupet lagoon (Tiruvarur/Thanjavur); Punnakayal (Thoothukudi); Manakudi, Thengapattinam (Kanniyakumari). Species cultured in shrimp ponds: giant tiger shrimp *Penaeus monodon* and white-leg shrimp *Penaeus (Litopenaeus) vannamei* [S7]; CIBA resource mapping identified 10,088 ha suitable for coastal aquaculture [S3]. PMMSY shrimp support: Rs 23.68 crore sanctioned for shrimp-farming development (Policy Note 2024-25 [S4]); five-year coastal-aquaculture allocation Rs 24.94 crore incl. 100 ha new shrimp farms and 53 biofloc ponds [S3 Table 6]. MPEDA publishes no district register of farms; NaCSA society lists were not found online (NOT_FOUND).

## 5. Agro-climatic zones of Tamil Nadu (TNAU)

### 5.1 As published on the TNAU page 'Tamil Nadu Agro Climatic Zones' [S15a] (uses post-2019 district names) — VERIFIED 2026-09-21

| Zone | Districts (quoted) | Altitude; annual rainfall |
|---|---|---|
| North Eastern Zone | Kanchipuram, Chengalpet, Tiruvallur, Cuddalore, Villupuram, Kallakuruchi, Vellore, Tirupathur, Ranipet, Tiruvannamalai | 100-200 m; 1,105 mm |
| North Western Zone | Dharmapuri, Salem, Namakkal | 200-600 m; 875 mm |
| Western Zone | Erode, Coimbatore, Karur (part), Namakkal (part), Dindigul (part), Theni (part) | 200-600 m; 715 mm |
| Cauvery Delta Zone | Tiruchi, Perambalur, Pudukottai (part), Thanjavur, Nagapattinam, Mayiladuthurai, Tiruvarur, Cuddalore (part) | 100-200 m; 984 mm |
| Southern Zone | Madurai, Sivagangai, Ramanathapuram, Virudhunagar, Tirunelveli, Tenkasi, Thoothukudi | 100-600 m; 857 mm |
| High Rainfall Zone | Kanniyakumari | 100-2,000 m; 1,420 mm |
| Hilly and High Altitude Zone | Nilgiris, Kodaikanal | > 2,000 m; 2,124 mm |

### 5.2 Older TNAU Agritech table (source line: tnhorticulture.tn.gov.in; pre-2019 district names) [S15b] — VERIFIED 2026-09-21

| Zone | Districts (quoted) | Soil types |
|---|---|---|
| North Eastern Zone | Kancheepuram, Tiruvallur, Cuddalore, Vellore, Villupuram and Tirunvannamalai | Red sandy loam, clay loam, saline coastal alluvium |
| North Western Zone | Dharmapuri, Krishnagiri, Salem and Namakkal (part) | Non-calcareous red, non-calcareous brown, calcareous black |
| Western Zone | Erode, Coimbatore, Tiruppur, Theni, Karur (part), Namakkal (part), Dindigul, Perambalur and Ariyalur (part) | Red loamy, black |
| Cauvery Delta | Thanjavur, Nagapattinam, Tiruvarur, Trichy and parts of Karur, Ariyalur, Pudukkottai and Cuddalore | Red loamy, alluvium |
| Southern Zone | Madurai, Sivagangai, Ramanathapuram, Virudhunagar, Tirunelveli and Thoothukudi | Coastal alluvium, black, red sandy, deep red |
| High Rainfall | Kanyakumari | Saline coastal alluvium, deep red loam |
| Hilly | The Nilgiris and Kodaikanal (Dindigul) | Lateritic |

### 5.3 Zone assignment for all 38 districts (for the map layer)

| District | Zone | Status / note |
|---|---|---|
| Ariyalur | Cauvery Delta (part) / Western (part) | ASSUMED — not on the TNAU 2024 page; the older TNAU Agritech table puts Ariyalur in both zones |
| Chengalpattu | North Eastern | VERIFIED |
| Chennai | North Eastern | ASSUMED — urban district, not listed on either TNAU page; lies inside the NE zone footprint |
| Coimbatore | Western | VERIFIED |
| Cuddalore | North Eastern (main) / Cauvery Delta (part) | VERIFIED |
| Dharmapuri | North Western | VERIFIED |
| Dindigul | Western (part) / Hilly (Kodaikanal) | VERIFIED |
| Erode | Western | VERIFIED |
| Kallakurichi | North Eastern | VERIFIED |
| Kancheepuram | North Eastern | VERIFIED |
| Kanniyakumari | High Rainfall | VERIFIED |
| Karur | Western (part) / Cauvery Delta (part) | VERIFIED (Western part on TNAU 2024 page; delta part only on the older table) |
| Krishnagiri | North Western | ASSUMED — omitted from the TNAU 2024 page (carved from Dharmapuri in 2004); NW zone on the older TNAU Agritech table |
| Madurai | Southern | VERIFIED |
| Mayiladuthurai | Cauvery Delta | VERIFIED |
| Nagapattinam | Cauvery Delta | VERIFIED |
| Namakkal | North Western (main) / Western (part) | VERIFIED |
| Perambalur | Cauvery Delta | VERIFIED (TNAU 2024); older table says Western — conflict |
| Pudukkottai | Cauvery Delta (part) | VERIFIED (part); remainder unassigned on TNAU pages |
| Ramanathapuram | Southern | VERIFIED |
| Ranipet | North Eastern | VERIFIED |
| Salem | North Western | VERIFIED |
| Sivaganga | Southern | VERIFIED |
| Tenkasi | Southern | VERIFIED |
| Thanjavur | Cauvery Delta | VERIFIED |
| The Nilgiris | Hilly and High Altitude | VERIFIED |
| Theni | Western (part) | VERIFIED (part); remainder unassigned |
| Thoothukudi | Southern | VERIFIED |
| Tiruchirappalli | Cauvery Delta | VERIFIED |
| Tirunelveli | Southern | VERIFIED |
| Tirupattur | North Eastern | VERIFIED |
| Tiruppur | Western | ASSUMED — not on the TNAU 2024 page (carved from Coimbatore/Erode 2009); Western on the older TNAU Agritech table |
| Tiruvallur | North Eastern | VERIFIED |
| Tiruvannamalai | North Eastern | VERIFIED |
| Tiruvarur | Cauvery Delta | VERIFIED |
| Vellore | North Eastern | VERIFIED |
| Viluppuram | North Eastern | VERIFIED |
| Virudhunagar | Southern | VERIFIED |

The TN Agrisnet (Department of Agriculture) zone page was fetched via Wayback (2025-04-02) but renders client-side and carried no zone text; the NIC-hosted PDF (tnagrisnet.tn.gov.in/dashboard/report/01_05.pdf) refused connections from this network. NOT_FOUND as a third source.

## 6. Freshwater aquaculture clusters and government fish seed farms / hatcheries

### 6.1 Government fish seed production centres — early fry, 2024-25 (Policy Note 2025-26, Table 7 [S3]) with 2022-23 comparison (Policy Note 2023-24, Table 5 [S5])

| District | Centre | Early fry 2024-25 (lakh) | Early fry 2022-23 (lakh) | Δ (lakh) | Status |
|---|---|---:|---:|---:|---|
| Tirunelveli | Manimuthar | 861 | 1,495.00 | -634.00 | VERIFIED |
| Thanjavur | Karanthai & Thatankulam (two centres, one row) | 718 | 727.00 | -9.00 | VERIFIED |
| Tiruvarur | Nallikkottai | 121 | 50.50 | 70.50 | VERIFIED |
| Karur | Thirukampuliyur | 402 | 367.00 | 35.00 | VERIFIED |
| Erode | Bhavanisagar | 2,026 | 1,920.00 | 106.00 | VERIFIED |
| Salem | Mettur Dam | 2,115 | 1,872.00 | 243.00 | VERIFIED |
| Krishnagiri | Krishnagiri (Amur carp) | 80 | 60.00 | 20.00 | VERIFIED |
| Tiruvallur | Poondi | 197 | 276.80 | -79.80 | VERIFIED |
| Theni | Manjalar (GIFT; figure is fingerlings) | 3 | 4.12 | -1.12 | VERIFIED |
| Tiruvannamalai | Sathanur (TNFDC) | 84 | 122.50 | -38.50 | VERIFIED |
| Cuddalore | Lalpet | 206 | not operating / not listed | — | VERIFIED |
| Dharmapuri | Hogenakkal | 125 | not operating / not listed | — | VERIFIED |
| Tenkasi | Ramanadhi | 120 | not operating / not listed | — | VERIFIED |
| **Total** | 14 centres (13 Dept + 1 TNFDC) | **7,058** (excl. fingerlings) | 6,894.92 (10 centres) | +163.08 | VERIFIED |

State produced 69.73 crore early fry in 2024-25 [S3 §7.1]; species: Indian major carps (catla, rohu, mrigal), Jayanthi rohu, Amur carp, GIF tilapia, murrel, calbasu, common carp [S3 §7.1]. Pure-line brood-stock facilities at Mettur Dam and Bhavanisagar Government fish farms; departmental fish feed mill in Thanjavur district [S5 §6.1]. GIFT hatcheries: Krishnagiri Govt Fish Farm (25 lakh/yr) and Manjalar Govt Fish Farm, Theni (combined 35 lakh/yr); three more at Barur (Krishnagiri), Agaram (Cuddalore), Chembarambakkam (Kancheepuram) and one planned at Nallikottai (Tiruvarur), total 85 lakh/yr [S3 §7.10.4]. Native-species hatcheries sanctioned (Rs 4.40 crore): pearl-spot at Parangipettai (Cuddalore), calbasu at Agarapettai (Thanjavur), Cauvery carp at Mettur (Salem) [S5 §6.6]. Fish brood banks at Lalpet (Cuddalore) and Ramanathi (Tenkasi) under PMMSY 2020-21, Rs 10 crore, completed [S5 §6.8.8]. Marine finfish (sea bass) seed-rearing centre at Mandapam, Ramanathapuram (CARD) [S3 §6.2].

### 6.2 Government fish seed rearing centres — fingerlings, 2024-25 (Policy Note 2025-26, Table 8 [S3])

| # | Centre | District | Fingerlings 2024-25 (lakh) |
|---:|---|---|---:|
| 1 | Bhavanisagar | Erode | 33 |
| 2 | Pungar Fish Farm | Erode | 50 |
| 3 | National Fish Seed Farm | Erode | 86 |
| 4 | Mettur Dam | Salem | 100 |
| 5 | Anaimaduvu | Salem | 6 |
| 6 | AIIRLIVAS | Salem | 12 |
| 7 | Krishnagiri | Krishnagiri | 157 |
| 8 | Pambar | Krishnagiri | 13 |
| 9 | Kelavarapalli | Krishnagiri | 7 |
| 10 | Barur (GIFT) | Krishnagiri | 5 |
| 11 | Hogenakkal | Dharmapuri | 10 |
| 12 | Chinnar | Dharmapuri | 30 |
| 13 | Neithalur | Thanjavur | 33 |
| 14 | Agarapettai | Thanjavur | 26 |
| 15 | Karanthai | Thanjavur | 14 |
| 16 | Thirumangalakottai | Thanjavur | 12 |
| 17 | Chembarampakkam | Kancheepuram | 11 |
| 18 | Athur | Chengalpattu | 32 |
| 19 | Poondi | Tiruvallur | 14 |
| 20 | Vidur | Viluppuram | 17 |
| 21 | Lalpet | Cuddalore | 33 |
| 22 | Agaram | Cuddalore | 9 |
| 23 | Mordhana | Vellore | 12 |
| 24 | Nallikkottai | Tiruvarur | 10 |
| 25 | Thattamanaipatti | Pudukkottai | 11 |
| 26 | Kurungalur | Pudukkottai | 3 |
| 27 | Karuvidaicherry | Pudukkottai | 3 |
| 28 | Asoor | Tiruchirappalli | 10 |
| 29 | Kulithalai | Karur | 3 |
| 30 | Thirukampuliyur | Karur | 14 |
| 31 | Vaigai | Theni | 24 |
| 32 | Manjalar | Theni | 19 |
| 33 | Sathaiyar | Madurai | 11 |
| 34 | Pilavakkal | Virudhunagar | 26 |
| 35 | Vembakkottai | Virudhunagar | 7 |
| 36 | Anaipatti | Dindigul | 30 |
| 37 | Palar Porandalar | Dindigul | 13 |
| 38 | Piravalur | Sivaganga | 9 |
| 39 | Manimuthar | Tirunelveli | 38 |
| 40 | Kuniyur | Tirunelveli | 10 |
| 41 | Gadana | Tenkasi | 22 |
| 42 | Ramanadhi | Tenkasi | 9 |
| 43 | Pechiparai | Kanniyakumari | 4 |
| 44 | Chittar-I | Kanniyakumari | 7 |
| 45 | Chittar-II | Kanniyakumari | 3 |
| 46 | Kadamba | Thoothukudi | 3 |
| | **Sub-total, Fisheries Department (46 centres)** | | **1,011** |
| 47 | Palar Porandalar (TNFDC) | Dindigul | 2 |
| 48 | Amaravathy (TNFDC) | Tiruppur | 3 |
| 49 | Tirumurthy (TNFDC) | Tiruppur | 8 |
| 50 | Aliyar (TNFDC) | Coimbatore | 15 |
| 51 | Sathanur (TNFDC) | Tiruvannamalai | 11 |
| | **Sub-total, TNFDC (5 centres)** | | **39** |
| | **Grand total** | | **1,050** |

Counts by district (Department centres): Krishnagiri 4 (157 + 13 + 7 + 5 = 182 lakh, the largest rearing output of any district), Thanjavur 4 (85 lakh), Erode 3 (169 lakh), Salem 3 (118 lakh), Kanniyakumari 3, Pudukkottai 3, Cuddalore 2, Dharmapuri 2, Theni 2, Tirunelveli 2, Tenkasi 2, Virudhunagar 2, Dindigul 2, Karur 2, then one each in Kancheepuram, Chengalpattu, Tiruvallur, Viluppuram, Vellore, Tiruvarur, Tiruchirappalli, Madurai, Sivaganga, Thoothukudi. District pages add detail: Krishnagiri — 'KRP Dam fish seed rearing centre at Krishnagiri, Pampar at Uthangakarai, Kellaverapalli at Hosur' [S20]; Dharmapuri — rearing centres at Hogenakkal and Panchapally-Chinnar, 6 reservoirs of 840.38 ha, 586 tanks (14,000 ha), 24 seed-rearing cages at Thoppaiyar reservoir under NADP, district production 2,863.81 t (2016-17) [S19]; Chengalpattu — rearing centre at Athur village, Kolavoi reservoir with 82 cages (58 of 6 × 4 m, 24 of 4 × 4 m) [S18]; Tiruvarur — Government seed production-cum-rearing centre at Nallikottai, Mannargudi taluk; 4 private seed production centres, 30 private rearing centres, 650 private fish farms on 950 ha; 154 CAA-registered shrimp farms (page undated) [S17].

### 6.3 Named freshwater clusters (evidence-based)

| Cluster (name used on the map) | Districts | Evidence | Status |
|---|---|---|---|
| Cauvery delta carp belt | Thanjavur, Tiruvarur, Mayiladuthurai, Nagapattinam (+ Pudukkottai, Tiruchirappalli fringe) | 80,914.25 t inland in 2021-22 = 38.2 % of state [S1]; Thanjavur alone 46,125.64 t (21.8 %); DT Next 2025: 'Delta region contributes 35 per cent', species murrel, rohu, catla, mrigal, common carp, grass carp [S16]; Tiruvarur page: 650 private farms / 950 ha, IMC and Chinese carps [S17]; TNJFU Thanjavur Centre for Sustainable Aquaculture at Soorakottai on the Thanjavur–Pattukkottai road, 'Aquaculture Service Centre in Cauvery Delta Region', TN-IAMP Cauvery sub-basin 2019-25 [S22]; seed farms Karanthai, Thatankulam, Nallikottai, Neithalur, Agarapettai, Thirumangalakottai [S3] | VERIFIED |
| Cuddalore–Veeranam belt | Cuddalore (Kattumannarkoil/Lalpet, Parangipettai), Kallakurichi, Viluppuram | Cuddalore 19,364.00 t in 2021-22 (9.15 %, 2nd largest district, +45.8 % on 2019-20) [S1]; Lalpet seed production (206 lakh fry) and Agaram, Vidur rearing; Lalpet brood bank; pearl-spot hatchery Parangipettai; Veeranam reservoir 3,885 ha [S3, S5, S23] | VERIFIED |
| Northern tank belt (Poondi–Chembarambakkam–Kolavai) | Tiruvallur, Chengalpattu, Kancheepuram | 33,528.66 t combined in 2021-22 (15.8 %) [S1]; Poondi seed production centre (197 lakh fry) and rearing; Chembarampakkam and Athur rearing centres; cage units at Poondi (24 cages, tilapia and pangasius, TNJFU DIVA) and Kolavai lake (32 HDPE cages) [S21]; state fisheries department cage trial at Poondi 2014-15 (12 cages) [S24] | VERIFIED |
| Mettur–Bhavanisagar reservoir and seed hub | Salem, Erode, Namakkal | Mettur Dam farm 2,115 lakh fry and Bhavanisagar 2,026 lakh fry = 58.7 % of all government early fry 2024-25 [S3]; pure-line brood stock at both [S5]; Salem 9,395.15 t + Namakkal 6,849.18 t + Erode 1,667.86 t = 17,912.19 t inland 2021-22 [S1]; Stanley reservoir 15,346 ha, Bhavanisagar 7,728 ha [S23, S8] | VERIFIED |
| Krishnagiri–Dharmapuri (KRP) GIFT-tilapia belt | Krishnagiri, Dharmapuri | Krishnagiri 13,005.79 t inland 2021-22 (6.15 %, +49.2 % on 2019-20) + Dharmapuri 3,116.91 t (+381 %) [S1]; GIFT hatchery at Krishnagiri Govt Fish Farm and Barur; rearing at Pambar, Kelavarapalli, Hogenakkal, Chinnar [S3, S20, S19]; KRP reservoir 1,248 ha [S23] | VERIFIED |
| Southern reservoir-fed belt | Kanniyakumari, Thoothukudi, Tirunelveli, Tenkasi, Theni | Kanniyakumari 7,586.70 t, Thoothukudi 6,035.07 t (+95.9 % on 2019-20) [S1]; Manimuthar seed production (861 lakh fry), Ramanadhi (120), Manjalar GIFT hatchery; Pechiparai, Chittar-I/II rearing; Kadamba tank (Thoothukudi) [S3] | VERIFIED |
| Madurai ornamental-fish cluster (PMMSY notified) | Madurai | Ornamental Fisheries cluster, Madurai — one of 34 clusters notified nationally by DoF GoI [S14]; SOP for ornamental fisheries in Madurai launched 2024 [S11]; ~80 ornamental farmers and ~120 traders in and around Madurai; Vavidaimaruthur village hub with 13 integrated units in a single cluster; brood bank proposed [S3 §7.11] | VERIFIED |
| Kolathur ornamental hub | Chennai | Kolathur: >2,000 families incl. 450 ornamental fish farmers and 300 traders; ~400 species; turnover > Rs 200 crore/yr; Ornamental Fish Trade Centre sanctioned Rs 50 crore [S3 §7.11; S5 §6.13] | VERIFIED |

## 7. FFDA / DFFDA and PMMSY cluster or district announcements

- District Fish Farmers Development Agencies (DFFDA): 37 agencies, chaired by District Collectors, Assistant Director of Fisheries as CEO; 7,502 fish farms on ≈ 5,580 ha registered with DFFDAs; 106 irrigation tanks allotted to seven DFFDAs [S3 §7.6; S6 item 2]. The 2023-24 note said 'DFFDA in 38 Districts except Chennai' [S5 §6.2] — i.e. 37 (VERIFIED, wording conflict only). DFFDA was formed by merging FFDA and the Brackish-water FFDA [S17]. FFDA-line production: 15,298.98 t (2019-20) → 19,085.91 t (2021-22) [S2, S1]. Twelfth Plan baseline: ~5,000 ha under FFDA freshwater aquaculture; 5 government seed production centres (402.5 million fry potential) and 33 rearing centres in 2012 [S27] — now 14 and 46 + 5.
- PMMSY, Tamil Nadu: 48 projects, Rs 1,156.15 crore, GoI share Rs 448.65 crore, FY 2020-21 to 2024-25 [S10]. One Integrated Aquapark approved for Tamil Nadu at Rs 127.71 crore (GoI share Rs 75.16 crore) [S10, Annexure I]; the Policy Note 2025-26 describes a 'Multipurpose Seaweed Park' sanctioned at exactly Rs 127.71 crore with Hub I (seaweed seed production park) at Valamavur, Ramanathapuram district and Hub II (processing park) at Gandarvakottai, Pudukkottai district [S3 §6.2.2] — same cost, so this is the aquapark (identification ASSUMED, cost match VERIFIED).
- PMMSY clusters naming Tamil Nadu districts: Ornamental Fisheries cluster, Madurai [S14, S11]. No seaweed, shrimp, cage or freshwater PMMSY cluster is notified for Tamil Nadu on the DoF cluster map (NOT_FOUND; the seaweed cluster is Lakshadweep).
- Climate-Resilient Coastal Fishermen Villages: 16 Tamil Nadu villages selected (names in PIB Annexure I, not district-tagged in the release) [S9].
- Integrated Development of Reservoir project, Rs 11.08 crore (PMMSY 2020-21), cage culture in five reservoirs: Policy Note 2025-26 names Anaimaduvu Dam (Salem), Krishnagiri Dam (Krishnagiri), Chittar Dam (Kanniyakumari), Bhavanisagar Dam (Erode), Sathanur Dam (Tiruvannamalai) [S3 §7.10.5]; the 2023-24 note listed Mettur Dam, Bhavanisagar, Sathanur, Krishnagiri and Chittar [S5 §6.8.9] — Mettur was replaced by Anaimaduvu (conflict, both VERIFIED as printed). PMMSY also funds floating seed-rearing and grow-out cages (Rs 4.60 crore) and landing centres/kiosks (Rs 2.50 crore) in 'five reservoirs' [S5 §7.4.3-7.4.4].
- New government farms sanctioned (state schemes, Policy Note 2023-24 §7.5): seed rearing centres at Kadamba (Thoothukudi) and Vadakkenendhal (Kallakurichi) Rs 10 crore; hatchery at Andiyappanur Odai reservoir (Tirupattur) Rs 5 crore; Palar Porandalar farm (Dindigul) Rs 5 crore; modernisation at Nallikottai (Tiruvarur) and Thirukkampuliyur (Karur); trout farm at Avalanche (Nilgiris) Rs 2.50 crore; Nagapattinam government seed-rearing centre under TN-IAMP; Gadana (Tenkasi) rearing centre in progress 2024-25 [S3 §7.12].
- TN-IAMP (World Bank) fisheries component since 2018-19: 45 sub-basins per the 2025-26 note versus 66 sub-basins per the 2023-24 note (conflict, both VERIFIED as printed); 2024-25 outputs: 717 seasonal tanks (≈ 26,139 ha) stocked, fish culture in 1,258 farm ponds, 88 seed-rearing-cum-culture farms, 100 seed-rearing cage units and 15 grow-out cage units [S3 §7.12].
- Seaweed (mariculture, for completeness): ~2,000 families in Nagapattinam, Tiruvarur, Thanjavur, Pudukkottai, Ramanathapuram, Thoothukudi and Kanniyakumari; 13,500–16,500 t/yr Kappaphycus [S3 §6.2.1]. Open-sea cages: 422 supplied to coastal fisherfolk (Rs 18.33 crore) [S3 §6.2.3].

## 8. Reservoirs and major tanks used for reservoir or cage fisheries

### 8.1 TNFDC-managed reservoirs (30-year lease) — tnfdc.in [S8] and fisheries.tn.gov.in/TNFDC [S7]

| Reservoir | District | Water spread (ha) |
|---|---|---:|
| Aliyar Reservoir | Coimbatore | 646 |
| Amaravathy Reservoir | Tiruppur | 906 |
| Bhavanisagar Reservoir | Erode | 7,728 |
| Palar Poranthalar Reservoir | Dindigul | 629 |
| Perumpallam Reservoir | Erode | 65 |
| Sathanur Dam | Tiruvannamalai | 2,000 |
| Thirumoorthy Reservoir | Tiruppur | 445 |
| Uppar Dam Reservoir | Erode | 445 |
| **Total (8)** | | **12,864** |

TNFDC seed-rearing area: 4.85 ha (tnfdc.in) versus 2.83 ha (fisheries.tn.gov.in/TNFDC page) — conflict; ornamental-fish centres at Aliyar and Thirumoorthy Nagar [S8].

### 8.2 Other reservoirs named in the sources

| Reservoir | District | Water spread (ha) [S23, FAO 1995] | Fisheries role in current sources |
|---|---|---:|---|
| Mettur (Stanley) | Salem | 15,346 (115 t/yr (1993)) | largest reservoir fishery; Mettur Dam Govt fish farm 2,115 lakh fry 2024-25, pure-line brood stock, Cauvery-carp hatchery [S3, S5] |
| Bhavanisagar | Erode (then 'Periyar') | 7,876 (179 t/yr avg) | TNFDC-managed (7,728 ha per TNFDC); seed farm 2,026 lakh fry; in the 5-reservoir cage project [S3, S8] |
| Amaravathy | Tiruppur (then Coimbatore) | 850 (112 t/yr) | TNFDC (906 ha per TNFDC); rearing centre [S8, S3] |
| Sathanur | Tiruvannamalai | 2,010 (126 t/yr) | TNFDC (2,000 ha per TNFDC); seed production 84 lakh fry; 5-reservoir cage project [S3, S8] |
| Veeranam | Cuddalore (then South Arcot) | 3,885 (36 t/yr) | Cuddalore irrigation tank; no current departmental activity found (NOT_FOUND) |
| Poondi | Tiruvallur (then Chengalpattu-MGR) | 3,263 (15 t/yr) | Poondi seed production centre 197 lakh fry; TNJFU DIVA cage unit 24 cages; departmental cage trial 2014-15 [S3, S21, S24] |
| Vaigai | Theni (then Madurai) | 2,419 (24 t/yr) | Vaigai rearing centre 24 lakh fingerlings [S3] |
| Pechiparai | Kanniyakumari | 1,515 (9 t/yr) | Pechiparai rearing centre; farm improved under NADP 2021-22 [S3, S5] |
| Krishnagiri (KRP) | Krishnagiri (then Dharmapuri) | 1,248 (47 t/yr) | KRP rearing centre; Krishnagiri GIFT hatchery; 5-reservoir cage project [S3, S20] |
| Anaimaduvu | Salem | not in FAO list | rearing centre; renovation Rs 70 lakh (NADP 2021-22); 5-reservoir cage project [S3, S5] |
| Chittar I & II | Kanniyakumari | not in FAO list | rearing centres; 5-reservoir cage project [S3] |
| Kolavai (Kolavoi) lake | Chengalpattu | not in FAO list | 82 cages (district page) / 32 HDPE cages (TNJFU DIVA) for tilapia and carp [S18, S21] |
| Thoppaiyar | Dharmapuri | not in FAO list | 24 seed-rearing cages under NADP [S19] |
| Manjalar | Theni | not in FAO list | GIFT hatchery (15 lakh/yr) [S5, S3] |

Reservoir counts: 62 under the Fisheries Department (54) and TNFDC (8), 56,075 ha; 27 reservoirs under lease in 2024-25 earning Rs 6.63 crore; nine more reservoirs identified for transfer from the Water Resources Department [S3 §7.3]. The Department also manages 636 irrigation tanks (486 intensive fish-culture tanks, 106 DFFDA tanks, 22 Palani tanks in Dindigul, 21 rural demonstration tanks, Kadamba tank in Thoothukudi) [S3 Table 9].

## 9. Conflicts between sources (all figures as printed)

- Inland production 2023-24: 2.47 lakh t (246,576.21 t) in the Policy Note 2025-26 and Fisheries-at-a-Glance 2023-24 [S3, S6] versus 2.32 lakh t on the Department's Inland Fisheries web page [S7]. The Policy Note is the later, tabled document; use 2.47 lakh t and footnote the web figure.
- Total production 2023-24: 8.84 lakh t [S3] = 6.37 + 2.47; web/press '8.83 lakh t' (rounding).
- Marine 2024: 6.37 lakh t (Dept, FY 2023-24) versus 6.79 lakh t (CMFRI, calendar 2024) [S6, S9] — different estimators and periods.
- CAA shrimp farms: 2,177 (2023) → 2,360 (2024) → 2,382 (2025) in Policy Notes; 2,702 in the DoF GoI deck; 3,001 on the Department web page [S5, S4, S3, S13, S7]. Hatcheries 71 / 78 / 80 / 110 across the same sources.
- Five-reservoir cage project: Mettur listed in the 2023-24 note, Anaimaduvu in the 2025-26 note [S5, S3].
- TN-IAMP sub-basins: 66 (2023-24 note) versus 45 (2025-26 note) [S5, S3].
- DFFDA count: '38 districts except Chennai' (2023-24) versus 37 (2024-25 Glance, 2025-26 note) — same meaning.
- TNFDC seed-rearing area: 4.85 ha (tnfdc.in) versus 2.83 ha (fisheries.tn.gov.in/TNFDC) [S8, S7].
- Kolavai lake cages: 82 (Chengalpattu district page, undated) versus 32 HDPE cages (TNJFU DIVA page) [S18, S21] — possibly different operators or dates.
- DES 2019-20 marine table: Villupuram/Cuddalore totals transposed in the PDF (see §3.2).
- Agro-climatic zones: Perambalur is Cauvery Delta on the TNAU 2024 page but Western on the older Agritech table; Krishnagiri, Tiruppur, Ariyalur absent from the 2024 page [S15a, S15b].
- Reservoir areas: FAO 1995 (Bhavanisagar 7,876 ha; Sathanur 2,010; Amaravathy 850) versus TNFDC (7,728; 2,000; 906) [S23, S8] — different survey dates and full-reservoir-level conventions.
- Sathanur Dam coordinates: Wikipedia infobox 12.1334 N, 78.9468 E versus OpenStreetMap 12.1832 N, 78.8503 E (≈ 12 km apart); OSM used, because it agrees with the dam's position on the Thenpennai river west of Tiruvannamalai (ASSUMED).

## 10. Not found or declined

- District-wise inland or marine production for any year after 2021-22 from an official table: NOT_FOUND (DES 2022-23/2023-24 handbook chapters not published online as of 2026-09-21; the 2023-24, 2024-25 and 2025-26 Policy Notes carry no district production annexure; data.gov.in holds only the 2017 and 2018 handbook extracts; indiastat/indiastatdistricts are paywalled and were not used).
- District-wise count or area of shrimp farms from the CAA's own register: NOT_FOUND online (query endpoint returns 404); the state's tabulation in the Policy Note 2025-26 is used instead. MPEDA/NaCSA district lists: NOT_FOUND.
- Species composition by district: NOT_FOUND; only state-level species lists exist [S3, S7, S16].
- Coordinates for Palar Porandalar, Uppar and Perumpallam-adjacent farms, Pambar, Chinnar, Agaram, Asoor, Anaipatti, Kuniyur, Gadana, Ramanadhi, Piravalur, Kadamba, Thattamanaipatti, Kurungalur, Karuvidaicherry, Sathaiyar, Vembakkottai, Thirumangalakottai, Neithalur, AIIRLIVAS, Pungar, National Fish Seed Farm (Bhavanisagar), Andiyappanur Odai, Vadakkenendhal, Athur (Chengalpattu), Soorakottai, Vavidaimaruthur, Thoppaiyar: not resolvable to a point from Wikipedia or OSM Nominatim on 2026-09-21; these centres are listed in §6.2 but are not plotted as separate hotspots (declined rather than guessed).
- Private farms, hatcheries, owners and contacts: deliberately not listed (rule 3). The Nagapattinam Aquaculture Farmers Association (NAFA) is mentioned in a PIB release [S12] as an association only.

## 11. Source register (all read on 2026-09-21 unless stated)

| # | Document | URL | Access note |
|---|---|---|---|
| S1 | Department of Economics and Statistics, Government of Tamil Nadu — *Statistical Hand Book of Tamil Nadu 2021-22*, Chapter 8 Fisheries (Tables 8.1–8.5), pp. 209-213 | https://www.des.tn.gov.in/sites/default/files/2024-11/08%20fisheries.pdf | direct download (111,604 bytes); text extracted with PyMuPDF |
| S2 | DES — Statistical Hand Book, Chapter 8 Fisheries with 2019-20 data (Tables 8.1–8.5, pp. 202-206) | https://www.tn.gov.in/deptst/fisheries.pdf (archived copy https://web.archive.org/web/20221011154656/https://www.tn.gov.in/deptst/fisheries.pdf) | tn.gov.in timed out from this network; Wayback copy of 11 Oct 2022 used |
| S3 | Government of Tamil Nadu — *Fisheries and Fishermen Welfare Policy Note 2025-26*, Demand No. 7 (Anitha R. Radhakrishnan), 2025; 208 pp. | https://cms.tn.gov.in/cms_migrated/document/docfiles/fisheries_e_pn_2025_26.pdf (archived https://web.archive.org/web/20250412014436/https://cms.tn.gov.in/cms_migrated/document/docfiles/fisheries_e_pn_2025_26.pdf) | cms.tn.gov.in unreachable; Wayback 12 Apr 2025 |
| S4 | *Fisheries and Fishermen Welfare Policy Note 2024-25*, 198 pp. | https://www.fisheries.tn.gov.in/includes/assets/cms_uploads/pdf/glance/Fisheries_and_FW-Policy_Note_-_Eng_9466.pdf | fisheries.tn.gov.in refused connections; identical path on the department's development mirror tnfisheries.demodev.in served the PDF (1,931,659 bytes) |
| S5 | *Fisheries and Fishermen Welfare Policy Note 2023-24*, 181 pp. | https://cms.tn.gov.in/sites/default/files/documents/fisheries_e_pn_2023_24.pdf (archived https://web.archive.org/web/20240104090039/https://cms.tn.gov.in/sites/default/files/documents/fisheries_e_pn_2023_24.pdf) | Wayback 4 Jan 2024 |
| S6 | Tamil Nadu Fisheries Department — *Tamil Nadu Fisheries at a Glance 2023-24* (4 pp.) | https://www.fisheries.tn.gov.in/includes/assets/cms_uploads/pdf/glance/FISHERIES_AT_A_GLANCE_2023-24_9604.pdf | via the demodev mirror |
| S7 | fisheries.tn.gov.in pages: /Aquaculture, /InlandFisheries, /MarineFisheries, /TNFDC, /WhatWeDo | https://www.fisheries.tn.gov.in/Aquaculture (archived https://web.archive.org/web/20250319160031/https://www.fisheries.tn.gov.in/Aquaculture); /InlandFisheries archived 2025-03-28; /MarineFisheries archived 2025-01-20; mirror https://tnfisheries.demodev.in/ | Wayback copies and mirror compared; identical text |
| S8 | Tamil Nadu Fisheries Development Corporation Ltd website | https://www.tnfdc.in/ | WebFetch |
| S9 | PIB, Ministry of Fisheries, AH&D — 'Fisheries Infrastructure under PMMSY in Tamil Nadu', Release ID 2146836, 22 Jul 2025 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2146836 | curl; contains the ICAR-CMFRI 2024 district landings |
| S10 | PIB — 'Aquaculture parks established under PMMSY', Release ID 2078380, 28 Nov 2024 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2078380 | curl |
| S11 | PIB — 'Year End Review 2024: Department of Fisheries', Release ID 2083813, 12 Dec 2024 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2083813 | curl |
| S12 | PIB — 'Coastal Aquaculture Authority … flags off National Campaign … from Nagapattinam', Release ID 2005946, 14 Feb 2024 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2005946 | curl |
| S13 | Department of Fisheries, GoI — 'Fisheries Schemes and Initiatives: Tamil Nadu' (30-slide deck, uploaded April 2026; data undated, production chart to 2022-23) | https://www.dof.gov.in/static/uploads/2026/04/b345ace3bcb986b555c4a2316db55053.pdf | curl |
| S14 | PMMSY — Clusters map | https://pmmsy.dof.gov.in/static/cluster/newcluster.html | WebFetch |
| S15a | TNAU — 'Tamil Nadu Agro Climatic Zones' | https://tnau.ac.in/tamil-nadu-agro-climatic-zones/ | WebFetch |
| S15b | TNAU Agritech Portal — 'Types of Soil – Agroclimatic Zones' (source line tnhorticulture.tn.gov.in) | https://agritech.tnau.ac.in/agriculture/agri_soilresource_agroclimate.html | curl |
| S16 | DT Next, 'High potential for inland aquafarming visible in TN', 11 Aug 2025 | https://www.dtnext.in/news/tamilnadu/high-potential-for-inland-aquafarming-visible-in-tn-842891 | WebFetch (press; year of table not stated) |
| S17 | Tiruvarur District (NIC) — Department of Fisheries page | https://tiruvarur.nic.in/departments/fisheries/ | curl |
| S18 | Chengalpattu District (NIC) — Fisheries page | https://chengalpattu.nic.in/departments/fisheries/ | WebFetch |
| S19 | Dharmapuri District (NIC) — Fisheries page | https://dharmapuri.nic.in/departments/fisheries-department/ | curl |
| S20 | Krishnagiri District (NIC) — Fisheries page | https://krishnagiri.nic.in/departments/fisheries/ | curl |
| S21 | TNJFU — Directorate of Incubation and Vocational Training in Aquaculture (DIVA) | https://www.tnjfu.ac.in/directorates/diva/ | WebFetch |
| S22 | TNJFU — Thanjavur Centre for Sustainable Aquaculture | https://www.tnjfu.ac.in/directorates/dsa/thanjavurcesa/ | WebFetch |
| S23 | FAO Fisheries Technical Paper 345 (1995), 'Reservoir fisheries of India', ch. 2 Tamil Nadu | https://www.fao.org/4/v5930e/v5930e03.htm | WebFetch |
| S24 | Current World Environment 10(3), 2015, 'Environmental Impact of Cage Culture on Poondi Reservoir, Tamil Nadu' | http://www.cwejournal.org/vol10no3/environmental-impact-of-cage-culture-on-poondi-reservoir-tamil-nadu | WebFetch |
| S25 | geoBoundaries API, gbOpen IND ADM2 | https://www.geoboundaries.org/api/current/gbOpen/IND/ADM2/ | curl; GeoJSON from github.com/wmgeolab/geoBoundaries commit 9469f09 |
| S26 | Coordinates: English Wikipedia (MediaWiki API prop=coordinates; {{coord}} templates where the API had none) and OpenStreetMap Nominatim | https://en.wikipedia.org/w/api.php ; https://nominatim.openstreetmap.org/ | each hotspot states which |
| S27 | Tamil Nadu Twelfth Five Year Plan, §3.8 Fisheries (TNAU Agritech copy) | https://agritech.tnau.ac.in/12th_fyp_tn/2.%20Agriculture%20and%20Allied%20Sectors/2_8.pdf | WebFetch (PDF text) |
| S28 | Coastal Aquaculture Authority — Farms page (per-district query links) | https://caa.gov.in/farms.html | curl; district result pages 404 on 2026-09-21 |

*Files in this folder: `tn_districts.geojson` (boundaries), `hotspots.json` (map points derived only from the findings above), this note. Prepared 2026-09-21; nothing here was fabricated — every number traces to the register.*
