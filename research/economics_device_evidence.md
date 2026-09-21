# Oxyniti yield/profit/payback calculator — economics and device evidence

*Compiled 2026-09-21. Every figure carries units, its source URL and a status label:*
*VERIFIED = the page or PDF was read directly on 2026-09-21; UNTESTED = seen only in a search
snippet, a third-party summary or an unverifiable listing; ASSUMED = derived by arithmetic or
inference from a verified figure (the derivation is shown); NOT_FOUND = looked for and not found.*
*Nothing below is invented. Where a number is missing it says so.*

Scratch copies of every PDF and page text read for this file are in the session scratchpad
(`...\scratchpad\`: `tnerc_2024_mirror.pdf`, `tangedco_onepage.png`, `pmmsy_book.pdf`,
`nfdb_guidelines.pdf`, `tnau_*.pdf`, `gift_tilapia_tnau.pdf`, `nfdb_murrel.pdf`,
`ipb_nanobubble2.pdf`, `tranduy2008.pdf`, `mallya2007.pdf`, `cmfri_seabass_2025.pdf`).

---

## 1. Oxyniti product line (https://www.oxyniti.com/)

Pages read on 2026-09-21: `/`, `/products`, `/products/type/Nano-Bubble%20Generator`,
`/technology`, `/aquaculture-oxygenation`, `/ras-oxygenation`, `/faqs`, `/about`,
`/llms.txt`, `/sitemap.xml`, `/robots.txt`, `/product/nano-bubble-generator-1.5-HP`,
`/product/nano-bubble-generator-4-hp`. The site is a Blazor app but every page above is
server-prerendered: `curl` returned full text (home 54 kB; product pages ≈6 kB). No page returned
an empty shell. `/products/type/Nano-Bubble%20Generator` renders the home-page copy plus the FAQ,
not a catalogue.

### 1.1 Models — what the site actually states

**Verdict: the site names three models (OXY-Nano-1.5, -3, -5) but publishes specifications for
only two products (1.5 HP and 4 HP), and the only price shown (₹4400 on both) is a placeholder.**

| Item | 1.5 HP page | 4 HP page | Status |
|---|---|---|---|
| Product name | "Nano Bubble Generator 1.5 HP" | "Nano Bubble Generator 4 HP" | VERIFIED 2026-09-21 |
| URL | https://www.oxyniti.com/product/nano-bubble-generator-1.5-HP | https://www.oxyniti.com/product/nano-bubble-generator-4-hp | VERIFIED 2026-09-21 |
| Pump | "CRI MHC series pumps", stainless-steel horizontal multistage centrifugal | "CRI MHS-16", stainless-steel horizontal multistage high-flow | VERIFIED 2026-09-21 |
| Motor | "1.5 HP, 3-Phase, 440 V"; copper winding, thermal protection, Class F, IP44 | "4 HP, 3-Phase, 440 V"; same motor features | VERIFIED 2026-09-21 |
| kW | not stated; 1.5 HP × 0.7457 = 1.12 kW shaft | not stated; 4 HP × 0.7457 = 2.98 kW shaft | ASSUMED 2026-09-21 (electrical input will be higher by 1/motor-efficiency; no efficiency stated) |
| Oxygen input | "Oxygen Input Capacity: Up to 2 LPM"; "Compatible With: PSA oxygen concentrator / oxygen cylinder" | "Oxygen Input Capacity: Up to 6 LPM" | VERIFIED 2026-09-21 |
| Pond area / volume served | not stated | not stated | NOT_FOUND 2026-09-21 |
| Bubble size | "Typically <100 nm" | "typically <100 nm" | VERIFIED 2026-09-21 |
| Max liquid temp / suction lift | +65 °C / 1.5 m | +85 °C / 1.5 m | VERIFIED 2026-09-21 |
| Connections | "common: 1–1.5 inch" | "typically 1.5–2 inch" | VERIFIED 2026-09-21 |
| Price shown | "₹4400" | "₹4400" | VERIFIED text 2026-09-21; ASSUMED to be a placeholder (identical on both, below the cost of the named CRI pump alone) |
| Warranty | not stated | not stated | NOT_FOUND 2026-09-21 |
| Applications | aquaculture ponds, hydroponics, small wastewater units, R&D | commercial aquaculture (shrimp, fish), industrial wastewater, lake remediation, large hydroponics | VERIFIED 2026-09-21 |

Calculator implications that follow directly from the product pages:
- An external oxygen source (PSA concentrator or cylinder) is part of the system; its capital and
  running cost is not on the site — NOT_FOUND 2026-09-21. The calculator must carry it as an input.
- There is no 3 HP or 5 HP product page and no OXY-Nano model page; the sitemap
  (https://www.oxyniti.com/sitemap.xml, lastmod 2026-09-08) lists exactly two `/product/` URLs —
  VERIFIED 2026-09-21.
- `/robots.txt` disallows `/cart`, `/checkout`, `/payment`, `/orders`, `/my-demos` — an
  e-commerce/ordering flow exists on the site — VERIFIED 2026-09-21.

Home page (https://www.oxyniti.com/) model text, verbatim: "Three power options — Choose the
model that matches your pond and available power supply. OXY-Nano-1.5 / OXY-Nano-3 / OXY-Nano-5";
video JSON-LD: "Explore Oxyniti's nano-bubble technology and the OXY-Nano 1.5, 3 and 5 HP
solutions in this complete product overview" (contentUrl
https://www.oxyniti.com/videos/oxy-nano-series.mp4, duration PT6M53S, uploadDate 2026-08-17)
— VERIFIED 2026-09-21.

### 1.2 Performance claims on the site, verbatim, with page

| Claim (verbatim) | Page | Status |
|---|---|---|
| "2× Dissolved oxygen uplift" | https://www.oxyniti.com/ (results block) | VERIFIED 2026-09-21 (vendor claim) |
| "+15% Higher survival rate" | https://www.oxyniti.com/ | VERIFIED 2026-09-21 (vendor claim) |
| "−15% Feed conversion ratio" | https://www.oxyniti.com/ | VERIFIED 2026-09-21 (vendor claim) |
| "+30% Stocking density potential" | https://www.oxyniti.com/ | VERIFIED 2026-09-21 (vendor claim) |
| "*Figures are typical ranges reported in published nano-bubble aquaculture studies and field trials; results vary with species, pond condition and management." | https://www.oxyniti.com/ | VERIFIED 2026-09-21 |
| "2× More dissolved oxygen*", "<200nm Bubble size — stays for days", "1 Day Install — fits any pond" | https://www.oxyniti.com/ (hero) | VERIFIED 2026-09-21 |
| "By 4 AM, dissolved oxygen can fall below 2 mg/L — the danger zone for every farmed species." | https://www.oxyniti.com/ | VERIFIED 2026-09-21 |
| Profit calculator defaults: "Pond size 1 acre; Farm-gate price ₹120/kg; Estimated extra harvest +500 – 750 kg / year; Estimated extra revenue ₹60,000 – ₹90,000. Illustrative only — assumes a semi-intensive baseline of ~2,500 kg/acre/year and a 20–30% yield uplift from improved DO, survival and FCR (range reported in published nano-bubble aquaculture studies)." | https://www.oxyniti.com/ (#profit-calculator) | VERIFIED 2026-09-21 |
| "Typical ranges reported in published nano-bubble aquaculture studies and field trials: around 2× higher dissolved oxygen, +15% survival rate, and -15% feed conversion ratio, which opens up roughly +30% stocking density." | https://www.oxyniti.com/faqs and https://www.oxyniti.com/llms.txt | VERIFIED 2026-09-21 |
| Species: "Tilapia/GIFT, Murrel, Pangasius, freshwater prawn, carp polyculture, and biofloc/RAS systems — on almost any pond, with install completed in about a day." | https://www.oxyniti.com/faqs | VERIFIED 2026-09-21 |
| "bubbles under 200 nanometres across"; "Neutral buoyancy keeps bubbles suspended"; no quantified DO, energy or model figures | https://www.oxyniti.com/technology | VERIFIED 2026-09-21 |
| "100+ Installations across India"; "<200 nm"; stainless steel; no prices/warranty | https://www.oxyniti.com/about | VERIFIED 2026-09-21 |
| "Currently serving Tamil Nadu and South India" / "Currently piloting across South India" | https://www.oxyniti.com/faqs, https://www.oxyniti.com/ | VERIFIED 2026-09-21 |
| Contact "+91 96597 27477" | JSON-LD on home page; llms.txt | VERIFIED 2026-09-21 |

`/aquaculture-oxygenation` and `/ras-oxygenation` carry no model, price, warranty or
percentage claims ("sub-200nm" only) — VERIFIED 2026-09-21.

### 1.3 Internal inconsistencies on the site (for the calculator team to resolve)

1. Model line: 1.5/3/5 HP (home, video, JSON-LD) vs 1.5 HP and 4 HP (only product pages).
2. Bubble size: "<200 nm" (home, technology, about) vs "typically <100 nm" (both product pages).
3. Price: "₹4400" on both product pages.
4. Footprint: "100+ Installations across India" (about) vs "Currently piloting across South India" (home).
5. The results block calls the four figures "typical ranges … reported in published … studies";
   §7 below shows what the peer-reviewed literature actually supports.

---

## 2. Electricity — TANGEDCO/TNPDCL tariff for fish or prawn farming

**Verdict: a stand-alone fish/prawn farm in Tamil Nadu is billed under LT Tariff III-A(1)
(Cottage & Micro Industries) if its contracted load is ≤ 12 kW, at ₹4.80/kWh up to 500 units
per two months and ₹6.95/kWh above that (consumer-payable, effective 1 July 2025). Fish/prawn
culture is free (LT IV, fully subsidised) only when carried out as an allied activity alongside
agriculture on the same service. Loads above 12 kW fall to LT III-B at ₹8.00–8.25/kWh.**

### 2.1 Category (TNERC Tariff Order T.O. No. 6 of 2024, dated 15-07-2024, effective 01-07-2024)

Source: TNERC "Determination of Tariff for Distribution for FY 2024-25", official URL
https://www.tnerc.tn.gov.in/Orders/files/TO-Order%20No%206150720240650.pdf (connection timed
out 2026-09-21); read from the mirror copy
https://www.eqmagpro.com/wp-content/uploads/2024/07/TO-Order-No-6150720241000_compressed.pdf
(55 pp., header "TNERC – T.O.No.6 of 2024, Dt.15-07-2024") — VERIFIED 2026-09-21.

| Clause | Text (verbatim) | Meaning for a fish farm |
|---|---|---|
| §3.2.11 (p. 44) | "Low Tension Tariff III-A (1): (Cottage & Micro Industries)"; §3.2.11.1 "The contracted load for supply under this tariff category shall not exceed 12 kW." | Category for small farms |
| §3.2.11.7 (p. 45) | "This tariff is also applicable for sericulture, floriculture, horticulture, mushroom cultivation, cattle farming, poultry & bird farming and fish/prawn culture." | Fish/prawn culture explicitly named — VERIFIED 2026-09-21 |
| §3.2.13.1 (p. 47) | "All industries covered under LT III A(1) and III A(2) shall also fall under this tariff category [III-B] if the connected load of such services exceed 12 kW." | >12 kW → LT III-B |
| §3.2.14.1 (p. 49) | "…fish/prawn culture carried out as allied activities of agriculture along with agriculture activities, etc., shall be construed as agricultural activities." (LT Tariff IV, "To be fully subsidised by the Government") | Free supply only when allied to an agricultural connection — VERIFIED 2026-09-21; whether a given pond qualifies is at the licensee's discretion — ASSUMED |
| §3.1.2 (p. 26) | HT Tariff I list includes "…Poultry & Bird farming and Fish/prawn/shrimp culture" | HT farms → HT-I |
| pp. 44, 47, 49 | "For FY 2025-26 to FY 2026-27: The applicable tariff (both fixed and energy charge) for FY 2024-25 shall undergo an inflation based adjustment, as per para 6.2.1 of T.O.No.7 of 2022 dt.09.09.2022. The revision will be effective from 01st July of each of the subsequent years of the control period." | Annual CPI-linked revision each 1 July |

FY 2024-25 rates as determined (same order, VERIFIED 2026-09-21):

| Category | Fixed charge | Energy charge |
|---|---|---|
| LT III-A(1) | ₹75/kW/month | 480 paise/kWh for 0–250 units/month (0–500 bimonthly); 695 paise/kWh from 251 units/month (501+ bimonthly) |
| LT III-B | ₹81/kW/month (0–50 kW); ₹160 (50–112 kW); ₹589 (>112 kW) | 800 paise/kWh ("partly subsidised by the Government") |
| LT IV (agriculture) | ₹3805/HP/annum till meter installed; nil after | 480 paise/kWh on metering; "To be fully subsidised by the Government" |
| LT V (commercial) | ₹107/kW/month | 645 paise/kWh (≤50 units/month); 1015 paise/kWh above |

Whether the III-A(1) 250-unit slab is telescopic or applies to all units once exceeded is not
stated in the order text — UNTESTED 2026-09-21; the calculator should treat units above 500 per
two months at ₹6.95/kWh and flag the assumption.

### 2.2 Current rates (TNERC Suo-motu Order No. 6 of 2025, dated 30.06.2025, effective 01.07.2025)

Official order URL https://www.tnerc.tn.gov.in/Orders/files/TO-Order%20No6300620252131.pdf
("Determination of Tariff for distribution for FY 2025-26") — download failed three times on
2026-09-21 (connection dropped). Rates read instead from TANGEDCO's own "ONE PAGE STATEMENT ON
TARIFF RATES AS IN THE TNERC ORDER NO: SMT.No.6 of 2025 DT:30.06.2025 — Revised Tariff rates with
effect from 01.07.2025" (scanned image, http://exam.tnebnet.org/exambooks/IAO1T.pdf) —
VERIFIED 2026-09-21 (official secondary copy).

| Category | TNERC-fixed energy charge | Payable by consumer after Govt subsidy | Fixed charge (fixed / payable) |
|---|---|---|---|
| LT III-A(1) Cottage & Micro Industries, up to 500 units bimonthly | ₹4.95/unit | **₹4.80/unit** | ₹154/kW per two months / ₹150/kW |
| LT III-A(1), above 500 units bimonthly | ₹7.15/unit | **₹6.95/unit** | as above |
| LT III-B Industries, 0–50 kW | ₹8.25/unit | ₹8.00/unit | ₹168/kW per two months / ₹162/kW |
| LT III-B, 50–112 kW | ₹8.25/unit | ₹8.25/unit | ₹330/kW per two months |
| LT III-B, >112 kW (CT) | ₹8.25/unit | ₹8.25/unit | ₹608/kW/month |
| LT IV Agriculture & allied, metered | ₹4.95/unit | **₹0.00** (fully subsidised) | ₹3925/HP/annum till meter → ₹0 |
| LT V Commercial ≤100 units bimonthly | ₹6.65/unit | ₹6.45/unit | — |
| LT V Commercial >100 units | ₹10.45/unit | ₹10.15 (101–500) / ₹10.45 (>500) | ₹220–608/kW |
| HT I Industries | ₹7.50/unit | ₹7.50/unit | ₹608/kVA/month |

Delta vs FY 2024-25: TNERC-fixed III-A(1) rose 480→495 paise (+3.1 %) and 695→715 paise
(+2.9 %); III-B 800→825 paise (+3.1 %); the Government subsidy absorbs the rise for III-A(1)
and the 0–50 kW III-B slab, so the **consumer-payable III-A(1) rate is unchanged at ₹4.80/₹6.95**
— ASSUMED (arithmetic on the two verified tables) 2026-09-21. Third-party calculators
(https://tneb.billcalculator.in/tneb-tariff-rates/, https://pwrnxt.in/blog/tamil-nadu-ci-tariff-decoded)
quote the TNERC-fixed ₹4.95/₹7.15/₹8.25 as if payable — UNTESTED; use the TANGEDCO statement.

FY 2026-27 revision (due 1 July 2026): no TNERC order of 2026 located; a third-party guide dated
20 Sep 2026 states it "has not yet been notified"
(https://thediscombill.com/guides/tamil-nadu-electricity-tariff-july-2026/) — UNTESTED 2026-09-21.
Electricity tax of 5 % ad valorem on industrial consumption is cited by PWRNXT — UNTESTED 2026-09-21.

Worked example (ASSUMED 2026-09-21): a 1.5 HP unit drawing ≈1.3 kW electrical (1.12 kW shaft ÷
0.85 motor efficiency, efficiency not published) for 10 h/day × 30 d = 390 kWh/month = 780 units
per two months → above the 500-unit slab → ≈ ₹6.95/kWh → ≈ ₹2,700/month energy charge plus
fixed charge ≈ ₹150/kW × 1.3 kW per two months ≈ ₹100/month. The same unit on an LT IV allied
connection costs ₹0. A 5 HP unit (≈4.4 kW electrical) for 10 h/day ≈ 1,320 kWh/month ≈ ₹9,200/month
on III-A(1). All three of these are calculator defaults to expose, not facts.

### 2.3 Hours per day aerators run

| Statement | Source | Status |
|---|---|---|
| Vannamei, W. Bengal: "1-3 no of paddle wheel aerators of 1 HP and one spiral paddle wheel aerators … Aerators are under operation around 8-12 hours per day … during entire culture period" (0.1–0.3 ha ponds, 70–150 PL/m²) | Behera, Engormix, 3 Nov 2016, https://en.engormix.com/aquaculture/aquaculture-management/management-practice-vannamei-shrimp_a39569/ | VERIFIED 2026-09-21 |
| Fish ponds: "permissible to turn off aerators after mid-morning and not turn them back on until early evening"; shrimp: aeration "usually can be reduced from mid-morning until early evening"; target DO "should not fall below 4 mg/L" | Boyd, Global Seafood Advocate, 1 Jul 2014, https://www.globalseafood.org/advocate/species-pond-size-define-aeration-approaches/ | VERIFIED 2026-09-21 |
| Shrimp energy budget: "aerators operated in ponds for an average of 16 hours a day during an 80-day grow-out period"; "Small, electric motors use about 1 kWhr … per horsepower-hour" | Boyd, Global Seafood Advocate, 6 Jan 2020, https://www.globalseafood.org/advocate/energy-use-in-aquaculture-pond-aeration-part-1/ | VERIFIED 2026-09-21 |
| Tilapia earthen ponds, Bangladesh: blower aeration "for 9 hours daily when oxygen depletion occurs" | Sultana et al. 2017, https://www.banglajol.info/index.php/JBAU/article/view/33536 | VERIFIED 2026-09-21 |
| Tamil Nadu-specific published run-hours for fish or prawn ponds | — | NOT_FOUND 2026-09-21; the 6–10 h night-time figure used internally is consistent with the 8–12 h and 9 h figures above — ASSUMED |

---

## 3. Subsidies

### 3.1 PMMSY (Pradhan Mantri Matsya Sampada Yojana), CSS beneficiary-oriented components

Source: Department of Fisheries booklet "Pradhan Mantri Matsya Sampada Yojana" (2020), Table 1,
https://static.pib.gov.in/WriteReadData/userfiles/PMMSY%20BookEnglish.pdf (booklet pp. 10–12)
— VERIFIED 2026-09-21. Column headers: "Unit cost (Rs. lakhs) | Governmental Assistance
General (40%) | SC/ST/Women (60%)".

| Sl | Activity (verbatim) | Unit | Unit cost | Assistance general 40 % | SC/ST/Women 60 % |
|---|---|---|---|---|---|
| 3 | Construction of New Rearing ponds (nursery/seed rearing ponds) | ha | ₹7.00 lakh | ₹2.80 lakh | ₹4.20 lakh |
| 4 | Construction of New Grow-out ponds | ha | ₹7.00 lakh | ₹2.80 lakh | ₹4.20 lakh |
| 5 | Inputs for fresh water Aquaculture including Composite fish culture, Scampi, Pangasius, Tilapia etc. | ha | ₹4.00 lakh | ₹1.60 lakh | ₹2.40 lakh |
| 7 | Construction of New ponds for Brackish Water Aquaculture (+ up to ₹2 lakh/ha extra if polythene-lined) | ha | ₹8.00 lakh | ₹3.20 lakh | ₹4.80 lakh |
| 9 | Inputs for Brackish Water Aquaculture | ha | ₹6.00 lakh | ₹2.40 lakh | ₹3.60 lakh |
| 11 | Construction of Biofloc ponds for Brackish water/Saline/Alkaline areas including inputs | printed "0.1 Ha." | ₹18 lakh | ₹7.20 lakh | ₹10.80 lakh |
| 12 | Construction of Biofloc ponds for Freshwater areas including inputs cost | printed "0.1 Ha." | ₹14.00 lakh | ₹5.60 lakh | ₹8.40 lakh |

- Aerators / oxygen systems as a stand-alone PMMSY line: the booklet contains no occurrence of
  "aerator/aeration" (0 hits in 36 pp.) — VERIFIED absence 2026-09-21. Whether aerators are an
  admissible item inside "Inputs for fresh water Aquaculture" (₹4 lakh/ha) is stated only in the
  full Operational Guidelines (https://nfdb.gov.in/PDF/PMMSY-Guidelines24-June2020.pdf and
  https://dof.gov.in/sites/default/files/2020-12/guidelines.pdf), neither of which downloaded
  (timeout / HTTP 404) — NOT_FOUND 2026-09-21.
- J&K Fisheries' PMMSY "Pattern of Financial Assistance" lists "Aeration system (air/oxygen)"
  among eligible RAS/biofloc components
  (https://fisheries.jk.gov.in/PMMSY/PMMSY-Pattern%20of%20Financial%20Assistance.pdf) — VERIFIED 2026-09-21.
- Biofloc unit conflict: the PIB booklet prints the unit as "0.1 Ha." while Puducherry Fisheries
  describes ₹14 lakh "per hectare" (https://fisheries.py.gov.in/…) — UNTESTED; check the
  Operational Guidelines before using.
- PMMSY scheme period was 2020-21 to 2024-25 (₹20,050 crore outlay); continuation status for
  2025-26 onward in Tamil Nadu — NOT_FOUND 2026-09-21.

### 3.2 NFDB (legacy guidelines, Ministry of Agriculture era)

Source: "Guidelines for NFDB Schemes", https://fisheries.jk.gov.in/Download/NFDB_Guidelines.pdf
(230 pp.) — VERIFIED text 2026-09-21; currency of these schemes after PMMSY — UNTESTED.

| Scheme | Aerator line | Assistance |
|---|---|---|
| §2.6 New ponds for brackishwater finfish culture, unit cost ₹2,40,000/ha | "Aerators 50,000" | 25 % of unit cost (max ₹60,000); SC/ST 30 % (max ₹72,000) |
| §2.7 Modification of existing shrimp farm for finfish, unit cost ₹2,00,000/ha | "Aerators 50,000" | 25 % (max ₹50,000); SC/ST 30 % (max ₹60,000) |
| §2.5 Additional infrastructure for SPF shrimp farms, 5 ha, unit cost ₹15,00,000 | "Aerators 5,00,000" | see guideline |
| §2.09 Cage culture of brackishwater finfish in ponds, unit cost ₹10,00,000 | "Aerators 1,00,000" | 25 % (max ₹2.50 lakh/ha); SC/ST 30 % (max ₹3.00 lakh/ha) |
| Freshwater pond aerator line | — | NOT_FOUND 2026-09-21 |

### 3.3 Tamil Nadu state schemes

- TN Fisheries & Fishermen Welfare Department deck "Fisheries Schemes and Initiatives Tamil Nadu"
  (hosted by DoF, uploaded 2026-04,
  https://www.dof.gov.in/static/uploads/2026/04/b345ace3bcb986b555c4a2316db55053.pdf): no
  aerator, oxygen or nano-bubble item (0 hits); lists PMMSY cage culture (455 cages, ₹1,705.29
  lakh), seaweed, deep-sea vessels, river ranching — VERIFIED 2026-09-21.
- TN Fisheries website (https://www.fisheries.tn.gov.in/WhatWeDo, /Aquaculture) refused
  connections on 2026-09-21; the search snippet says assistance is provided "for construction of
  new freshwater finfish hatcheries, fish rearing ponds, grow out ponds including inputs,
  freshwater bio-floc ponds, RAS and fish feed mills" — UNTESTED 2026-09-21.
- A Tamil Nadu subsidy specifically for aerators or nano-bubble/oxygen systems — NOT_FOUND 2026-09-21.

---

## 4. Incumbent aeration

### 4.1 Paddlewheel prices in India (listings, read 2026-09-21)

| Unit | Price | Seller / location | Other stated data | Source | Status |
|---|---|---|---|---|---|
| 2 HP paddlewheel, 4–6 paddles, 3-phase 220–440 V | ₹35,000 | Sagar Aqua Culture Pvt Ltd, Kotda Sangani, Rajkot | 1-year warranty; "Oxygenate Capability 2.5-2.8 kg O2/hrs" (spec table also says 1.8 kg/h); "Power consumption 1.25 units/hour"; 105 kg | https://www.indiamart.com/proddetail/shrimp-farming-aerator-19060900412.html | VERIFIED 2026-09-21 (listing; title says 3 hp, spec says 2 hp) |
| 1 HP surface floating, 2 paddles, 0.75 kW, 415 V 3-phase | ₹28,000 | Sagar Aqua Culture, Rajkot | 1-year warranty; "0.27 units per hour" (implausible for 0.75 kW — treat as unreliable) | https://www.indiamart.com/proddetail/1hp-fish-pond-aerator-6426193048.html | VERIFIED 2026-09-21 |
| 2 HP 4-paddle | ₹35,600 | Coimbatore seller | — | https://dir.indiamart.com/impcat/paddle-wheel-aerator.html | VERIFIED listing page 2026-09-21 |
| 2 HP 4-paddle | ₹36,000–38,500 | Rajkot, Karnal, Hisar sellers | — | same listing page | VERIFIED 2026-09-21 |
| 1 HP 2-paddle | ₹25,000–28,000 | Gharaunda, Guntur, Bhimavaram | — | same listing page | VERIFIED 2026-09-21 |
| 3 HP 6-paddle | ₹43,000 | Kotda Sangani | — | same listing page | VERIFIED 2026-09-21 |
| 2 HP 4-paddle (Chennai maker) | price not shown | Synergy Spray Systems, Chennai | 1-year warranty; "0.13 / 0.25 kgO2/h" as listed (implausibly low) | https://synergyspray.com/product/2hp-4-paddle-wheel-aerator/ | VERIFIED 2026-09-21 |
| 2 HP long-arm aerator (NABARD model assumption, 2015) | ₹35,000 each, 4 per ha | NABARD/TNAU vannamei model | — | https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/5.Culture_of_Vannamei_white_legged_shrimp_15.pdf | VERIFIED 2026-09-21 |
| 1 HP (0.75 kW) ring blower, 2,000 LPM, 24 kPa | ₹16,200 | Grenco Engineers, West Bengal | — | https://www.indiamart.com/proddetail/grand-pg-750-sunsun-1-0-hp-ring-blower-for-fish-pond-biofloc-tank-aquaculture-23767925473.html | UNTESTED 2026-09-21 (search snippet) |

Calculator default: **2 HP paddlewheel ₹35,000–36,500 (Tamil Nadu/Gujarat listings, Sept 2026);
1 HP ₹25,000–28,000** — VERIFIED listings, ASSUMED as representative.

### 4.2 Oxygen transfer (SOTR / SAE)

| Statement | Source | Status |
|---|---|---|
| Commercial paddlewheels (Ahmad & Boyd 1988 design): "SAE values of 4.5 to 5.5 pounds O2/hp-hour" = 2.04–2.49 kg O2 per hp·h = **2.7–3.3 kg O2/kWh** (÷0.7457); "under field conditions … about 1.5 to 2.5 pounds O2/hp-hour" = 0.68–1.13 kg per hp·h = 0.9–1.5 kg O2/kWh; diffusers in shallow ponds 1–3 lb/hp·h = 0.6–1.8 kg O2/kWh; vertical pumps 2–4 lb/hp·h; pump-sprayers 1.5–3.5 lb/hp·h; catfish industry 1.5–2 hp/acre rising to 2–3 hp/acre | Tucker (Mississippi State), The Fish Site "Pond Aeration", https://thefishsite.com/articles/pond-aeration | VERIFIED 2026-09-21; kg/kWh conversions ASSUMED (1 hp = 0.7457 kW, 1 lb = 0.4536 kg) |
| 2 HP paddlewheel SOTR maximum 3.79 ± 0.30 kg O2/h at 30 ‰ salinity; freshwater lower | Vinatea & Carvalho 2007, Aquacultural Engineering 37:73–78, https://www.sciencedirect.com/science/article/abs/pii/S0144860907000234 | UNTESTED 2026-09-21 (search snippet; page blocked) |
| Indian paddlewheel test tank 4 × 4 × 1.5 m: maximum SAE 1.019 kg O2/kWh at 160 rpm; least-cost speed 80 rpm for IMC ponds ≤ 700 m³ | "Effect of rotational speeds of paddle wheel aerator on aeration cost", https://www.academia.edu/31122792/ | UNTESTED 2026-09-21 |
| For Indian major carp ponds > 5,000 m³, 1-hp and 2-hp paddlewheels are the efficient choice; cascade aerators for < 1,000 m³ | "Selection of aerators for intensive aquacultural pond", Aquacultural Engineering 2013, https://www.sciencedirect.com/science/article/abs/pii/S0144860913000617 | UNTESTED 2026-09-21 |
| Vendor listing: 2 HP unit "2.5–2.8 kg O2/h" | Sagar (above) | VERIFIED listing, vendor claim |
| CIBA-published SOTR/SAE for Indian paddlewheels | — | NOT_FOUND 2026-09-21 |

### 4.3 Aerator numbers per area

| Statement | Source | Status |
|---|---|---|
| Shrimp: "about 1 hp of aeration is needed for each 10 kg/ha increment of daily feed input"; ≈15 hp/ha at end of crop for 6,000 kg/ha (18 hp/ha with safety margin); tilapia "0.5 hp or 0.75 hp" per 10 kg/ha feed increment | Boyd 2014 (Advocate, URL in §2.3) | VERIFIED 2026-09-21 |
| "each 300- to 500-kg increment of shrimp production requires 1 hp" (2.0–3.3 hp/t) | Boyd 2020 (Advocate, URL in §2.3) | VERIFIED 2026-09-21 |
| Vannamei W. Bengal: 1–3 × 1 HP paddlewheels + 1 spiral aerator per 0.1–0.3 ha pond; yields 12–24 t/ha/crop; survival 70–90 % | Behera 2016, Engormix (URL in §2.3) | VERIFIED 2026-09-21 |
| NABARD vannamei model: 4 × 2 HP long-arm aerators per ha at 50 PL/m² | TNAU/NABARD 2015 (URL in §4.1) | VERIFIED 2026-09-21 |
| CAA recommends stocking up to 60 PL/m²; vendor rule 16–24 HP/ha for intensive vannamei | https://aeroxyaeration.com/shrimp-pond-aeration-calculator/ (vendor) | UNTESTED 2026-09-21 |
| Freshwater fish ponds in Tamil Nadu: typical paddlewheels per acre | — | NOT_FOUND 2026-09-21; Boyd's tilapia rule (0.5–0.75 hp per 10 kg/ha/day feed) is the only defensible default — ASSUMED |

---

## 5. Cost structure of a crop (Tamil Nadu / South India model projects)

All NABARD/TNAU models below are 1 ha, dated 2015 ("indicative"), and carry no aeration
electricity line unless stated. Per-acre figures = per-ha ÷ 2.471 (ASSUMED conversion).

### 5.1 Carp polyculture (composite fish culture), NABARD/TNAU 2015, 1 ha, one 12-month crop
https://www.agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/2.composite.pdf — VERIFIED 2026-09-21

| Head | ₹ | Share |
|---|---|---|
| Capital: site 7,000; pond construction 60,000; 3 HP diesel pump 30,000; sluices 8,000; store room 45,000; nets 12,000; misc 6,000 | **1,68,000** | — |
| Seed: catla 2,000 + rohu 1,500 + mrigal 1,500 @ ₹5 | 25,000 | 17.8 % of opex |
| Feed 6,000 kg @ ₹14 | 84,000 | 59.9 % |
| Lime 500 kg @ ₹7; SSP 250 kg; urea 125 kg; cow dung 10 t @ ₹800 | 14,125 | 10.1 % |
| Drying/desilting/ploughing | 6,000 | |
| Harvesting 4,000 kg @ ₹1.5; misc | 11,000 | |
| Labour / electricity / lease | none itemised | NOT_FOUND in model |
| **Operational cost per crop** | **1,40,125** | (₹56,700/acre ASSUMED) |
| Production: 85 % survival, 1.1 kg, **4,675 kg/ha/yr** (1,892 kg/acre); farm-gate **₹55/kg**; gross ₹2.57 lakh; NPV ₹2.67 lakh, BCR 1.34, IRR 63 % | | |

Intensive carp (catla + rohu, 6-month crops, 2/yr), NABARD/TNAU 2015, 1 ha,
https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/4.Intensive_fish_culture_15.pdf — VERIFIED 2026-09-21:
capital ₹3,02,500 (incl. 5 HP diesel pump 60,000; store 1,50,000); opex per crop ₹2,88,075 —
seed 6,250 stunted yearlings (200–250 g) @ ₹10 = 62,500 (21.7 %); feed 12,000 kg rice bran/oil
cake/cotton-seed cake @ ₹13.6 = 1,63,200 (56.7 %); lime/SSP/urea/poultry litter 9,375; watch & ward
6 months @ ₹3,500 = 21,000; harvesting 7,000; misc 15,000; drying 10,000. Production 5,000 kg/crop
(80 % survival, 1 kg), farm-gate **₹70/kg**, ₹3.5 lakh/crop; IRR 80 %.

### 5.2 GIFT tilapia, NABARD/TNAU 2015, 1 ha, 6-month crop, 2 crops/yr
https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/6.GIFT_Tilapia_culture_15.pdf (11 pp., "GIFT 2015") — VERIFIED 2026-09-21

| Head | ₹ per crop | Share |
|---|---|---|
| Capital: site 4,000; pond 75,000; 5 HP diesel pump 60,000; sluices 10,000; store/office 400 sq ft 1,20,000; biosecurity 75,000; nets/misc 25,000 | **3,69,000** (one-off) | — |
| Seed 25,000 fry @ ₹3 | 75,000 | 14.9 % |
| Feed 13,125 kg @ ₹28 | 3,67,500 | 73.2 % |
| Lime 500 kg @ ₹5; SSP 250 kg; urea 125 kg; poultry litter/cow dung 5 t | 9,375 | 1.9 % |
| Watch & ward + feeding, 6 months @ ₹3,500 | 21,000 | 4.2 % |
| Harvesting 9,375 kg @ ₹1 | 9,375 | 1.9 % |
| Drying/desilting/watering 10,000; misc 10,000 | 20,000 | 4.0 % |
| Electricity / aeration / lease | none itemised | NOT_FOUND in model |
| **Operational cost per crop** | **5,02,250** | (₹2,03,200/acre ASSUMED) |
| Production: 25,000 stocked, 75 % survival, 500 g → **9,375 kg/ha/crop** (3,794 kg/acre/crop; 7,588 kg/acre/yr for 2 crops); implied FCR 13,125/9,375 = 1.40; farm-gate **₹75/kg**; income ₹7.03 lakh/crop; NPW ₹17.85 lakh @15 %, BCR 1.31, IRR > 50 % | | |

**Check of the internal model ("capital ₹2.1 lakh, variable ₹5.76 lakh, 9,000 kg at ₹120/kg,
1 acre"): not supported by this PDF.** The PDF is per hectare: capital ₹3.69 lakh, variable
₹5.02 lakh per crop, 9,375 kg per crop at ₹75/kg. Scaled to one acre it is capital ₹1.49 lakh,
variable ₹2.03 lakh per crop (₹4.06 lakh/yr), 3,794 kg per crop. "₹5.76 lakh" equals the
intensive-carp model's two-crop recurring cost per ha (2 × ₹2,88,075 = ₹5,76,150) — the internal
figure appears to have been taken from the wrong PDF. "₹120/kg" is Oxyniti's own calculator
default, not a NABARD figure. Also note the Oxyniti calculator's "~2,500 kg/acre/year
semi-intensive baseline" is one-third of this model's 7,588 kg/acre/yr — VERIFIED comparison 2026-09-21.

### 5.3 Pangasius (P. sutchi), NABARD/TNAU 2015, 1 ha, one crop/yr
https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/3.Pangassius_culture_15.pdf — VERIFIED 2026-09-21

| Head | ₹ | Share |
|---|---|---|
| Capital: site 4,000; pond 75,000; 5 HP diesel pump 60,000; sluices 7,000; nets 6,500; misc 4,500 | **1,57,000** | — |
| Seed 13,000 @ ₹1 | 13,000 | 2.3 % |
| Feed 30,000 kg @ ₹14.6 (GN oil cake 6 t @ ₹25,000/t + rice bran 24 t @ ₹12,000/t; "FCR 2:1") | 4,38,000 | 78.6 % |
| **Pumping charges (electricity/diesel) 12 months @ ₹5,000** | 60,000 | 10.8 % |
| Watch & ward 12 months @ ₹2,000 | 24,000 | 4.3 % |
| Lime 2,500; drying 4,500; misc incl. harvesting 15,000 | 22,000 | 3.9 % |
| **Operational cost per crop** | **5,57,000** | (₹2,25,400/acre ASSUMED) |
| Production: 90 % survival, 1.5 kg → **15,210 kg/ha/yr**; farm-gate **₹50/kg**; ₹7.605 lakh; NPW ₹10.11 lakh, BCR 1.30, IRR > 50 % | | |

### 5.4 Murrel (Channa striata), NFDB/ICAR-CIFA "Murrel culture in ponds", 5 × 0.2 ha = 1 ha, 8–10 months
https://static.vikaspedia.in/mediastorage/document/Murrel_Culture_in_Ponds.pdf (also
https://nfdb.gov.in/PDF/05_Murrel%20Culture%20in%20Ponds.pdf) — VERIFIED 2026-09-21; booklet undated (UNTESTED year)

| Head | ₹ lakh | Share |
|---|---|---|
| Capital: earthwork 1.50; pond lining 5.00; farmstead 0.50; 2 × 1 HP pumps 0.30; nets 0.20; electrification 0.30; misc 0.20 | **8.00** | — |
| Seed 10,000 fingerlings (5–8 cm) @ ₹7 | 0.70 | 7.4 % |
| Feed 7.35 t @ ₹100/kg (40 % CP; FCR 1.5) | 7.35 | 77.4 % |
| Manpower 1 @ ₹8,000/month × 10 | 0.80 | 8.4 % |
| **Electricity and fuel (lump sum)** | 0.35 | 3.7 % |
| Harvesting 0.10; misc 0.20 | 0.30 | 3.2 % |
| **Recurring cost per crop** | **9.50** | (₹3.84 lakh/acre ASSUMED) |
| Production: 70 % survival, 700 g → **4.90 t/ha**; selling price **₹400/kg**; gross ₹19.60 lakh; net ₹4.30 lakh after depreciation 1.20, interest 2.10, repayment 2.50 and next-crop opex | | |

### 5.5 L. vannamei, NABARD/TNAU 2015, 1 ha, 4-month crop, 2 crops/yr, 50 PL/m²
https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/5.Culture_of_Vannamei_white_legged_shrimp_15.pdf — VERIFIED 2026-09-21

| Head | ₹ per crop | Share |
|---|---|---|
| Capital: earthwork 60,000; inlet 15,000; outlet 15,000; main sluice 35,000; pump house 30,000; office/lab 1,05,000; watchman shed 27,500; 5 HP pump 65,000; **4 × 2 HP long-arm aerators @ 35,000 = 1,40,000**; electrical/transformer 60,000; reservoir 60,000; crab fencing 60,000; bird net 70,000; lab equipment 75,000; misc 30,000 | **8,47,500** (one-off) | — |
| PL 5,00,000 @ ₹0.75 | 3,75,000 | 24.9 % |
| Feed 14,875 kg @ ₹60 (FCR 1.40) | 8,92,500 | 59.3 % |
| **Electricity/power charges** | 65,000 | 4.3 % |
| Labour: supervisor 40,000; mechanic 26,000; 2 watchmen 40,000 | 1,06,000 | 7.0 % |
| Chemicals/manures 10,000; repairs 20,000; harvesting 10,625 kg @ ₹1; office/misc 25,000 | 65,625 | 4.4 % |
| Lease | none itemised | NOT_FOUND in model |
| **Operational cost per crop** | **15,04,125** | (₹6.09 lakh/acre ASSUMED) |
| Production: 85 % survival, 25 g → **10,625 kg/ha/crop**; price **₹175/kg**; 2 crops → ₹37.19 lakh/yr; NPW ₹30.03 lakh, BCR 1.18, IRR > 50 % | | |

Tamil Nadu farm-survey vannamei economics (Nagapattinam; Narkis et al., AJAEES 2021,
https://journalajaees.com/index.php/AJAEES/article/view/1222; PDF at
https://ageconsearch.umn.edu/record/358126/files/Narkis39102021AJAEES75289.pdf) — both blocked
(HTTP 202/403) → NOT_FOUND 2026-09-21. TN farmer break-even quoted July 2023: ₹330/kg (40 count),
₹290/kg (60 count), ₹250/kg (100 count) — Benison Media 7 Jul 2023,
https://benisonmedia.com/flat-vannamei-prices-leave-indian-farmers-eating-costs-in-painful-year/ — VERIFIED 2026-09-21.

### 5.6 Asian seabass, ICAR-CIBA/CMFRI survey Apr 2022–Mar 2023 (Geetha et al. 2025, CMFRI eprint ch. 5)
https://eprints.cmfri.org.in/19157/1/Impact%20of%20Technologies%20and%20Policies%20on%20Marine%20and%20Inland%20Fish%20Culture%20Systems%20in%20India_2025_Shinoj%20Parappurathu.pdf — VERIFIED 2026-09-21

Tamil Nadu = cage culture (₹/m³/yr): capital 3,994; seed 339; feed 4,003; labour 1,563; misc 314;
interest 740; total cost 7,792; production 19.91 kg/m³/yr; gross income 9,980 → implied
≈ ₹500/kg (ASSUMED 9,980 ÷ 19.91); net 2,187; break-even price ₹391.39/kg; FCR 6.33; survival 84.89 %.
Andhra pond culture (₹/ha/yr): total cost 35,42,711; feed 15,96,613 (45 %); production 13,677 kg;
gross 60,22,599 → implied ₹440/kg (ASSUMED); net 24,44,498; break-even ₹200.36/kg.

---

## 6. Farm-gate prices, Tamil Nadu 2025–2026 (farm-gate vs retail distinguished)

**Verdict: a count-wise 2025–26 Tamil Nadu vannamei table and 2025–26 TN farm-gate prices for
carp, tilapia, pangasius, murrel, scampi and pearl spot were not found in any citable source.
The nearest citable figures are below; the calculator must expose price as a user input.**

| Species | Figure | Type | Source | Status |
|---|---|---|---|---|
| Vannamei, Tamil Nadu, July 2023 | 30 ct ₹400; 40 ct ₹300; 60 ct ₹240; 80 ct ₹220; 100 ct ₹200 /kg | farm-gate | Benison Media 7 Jul 2023 (URL §5.5) | VERIFIED 2026-09-21 (dated) |
| Vannamei, Andhra, July 2023 wk 27 | 30 ct ₹440; 40 ct ₹340; 60 ct ₹290; 80 ct ₹270; 100 ct ₹240 /kg | farm-gate | same | VERIFIED 2026-09-21 |
| Vannamei, Andhra, Dec 2020 wk 53 | 30 ct ₹460; 40 ct ₹380; 60 ct ₹300; 80 ct ₹250; 100 ct ₹220 /kg | farm-gate | https://www.worldseafoodshanghai.com/en/xinwenmeiti/2226.html (dated 30 Dec 2020) | VERIFIED 2026-09-21 (old) |
| Vannamei, Andhra (W. Godavari), May 2026 | 100 ct ₹270 → ₹235 → ₹220 /kg within one week | farm-gate | Undercurrent News 25 May 2026, https://www.undercurrentnews.com/2026/05/25/india-shrimp-farmers-protest-falling-prices-rising-feed-costs/ | VERIFIED 2026-09-21 |
| Vannamei, Andhra, Jan 2026 | +₹5/kg across most sizes, second consecutive week; no levels | farm-gate | https://www.ocean-treasure.com/news/global-shrimp-prices-split-in-early-2026-as-india-rises-and-china-softens-post-holiday/ (14 Jan 2026) | VERIFIED 2026-09-21 |
| Vannamei, Tamil Nadu 2025–26 by count | — | — | — | NOT_FOUND 2026-09-21 (search aggregators re-dated the 2023 Aquaconnect figures as 2026; do not use) |
| Rohu / catla / mrigal, Nagapattinam, Apr 2026 | "expected to be sold at Rs 350 to 400 per kg against the normal price of Rs 200 to Rs 250 per kg" (farmer Selvaraj) | farmer-quoted; retail/farm-gate not stated | DT Next 25 Apr 2026, https://www.dtnext.in/news/chennai/pricey-freshwater-fish-fail-to-compensate-for-seafood-demand | VERIFIED quote 2026-09-21; price type UNTESTED |
| Rohu / catla (model) | ₹55/kg (composite, 1.1 kg fish); ₹70/kg (intensive, 1 kg fish) | farm-gate | NABARD/TNAU 2015 (§5.1) | VERIFIED (2015 vintage) |
| Common carp, TN 2025–26 | — | — | — | NOT_FOUND 2026-09-21 |
| GIFT tilapia, Odisha, June 2022 | wholesaler buys "around Rs 110 per kg"; retail "Rs 160-170 per kg"; GIFT 20–30 % below carp | farm-gate vs retail | The Fish Site 24 Jun 2022, https://thefishsite.com/articles/can-gift-gain-ground-in-eastern-india-odisha | VERIFIED 2026-09-21 |
| Tilapia, India wholesale, May–Jun 2025 | monthly average ₹158.5/kg (max ₹400, min ₹0 — noisy series) | wholesale aggregate | https://www.commoditymarketlive.com/fish-price/tilapia | VERIFIED page 2026-09-21; methodology UNTESTED |
| Tilapia, Tamil Nadu, 21 Sep 2026 | ₹200/kg ("Jalebi Meen"); prawn ₹300/kg | market (type unstated) | https://rates.goldenchennai.com/fish-price/tamil-nadu-fish-price-today/ | VERIFIED page 2026-09-21; UNTESTED as farm-gate |
| Tilapia (model / vendor default) | ₹75/kg (NABARD 2015); ₹120/kg (Oxyniti calculator default) | farm-gate | §5.2; https://www.oxyniti.com/ | VERIFIED 2026-09-21 |
| Pangasius, Andhra | farm-gate ₹71.5–80/kg (2018); ₹77.08/kg (2019); model ₹50/kg (2015) | farm-gate | https://www.cwejournal.org/vol11no3/delineation-of-supply-chain-of-pangasius-in-india-a-case-of-andhra-pradesh ; https://www.was.org/Meeting/Program/PaperDetail/154045 | UNTESTED 2026-09-21 (snippets); 2025–26 NOT_FOUND |
| Murrel | "sold in open markets at Rs.400-500 per kg"; model selling price ₹400/kg | market / model | NFDB booklet (§5.4) | VERIFIED 2026-09-21 (undated) |
| Murrel, India wholesale, May 2025 | monthly average ₹196.9/kg (max ₹444) | wholesale aggregate | https://www.commoditymarketlive.com/fish-price/murrel | VERIFIED page 2026-09-21; methodology UNTESTED |
| Murrel farm-gate 2025 | "₹200 to ₹300 per kg" | farm-gate (vendor blog) | https://www.agrifarming.in/murrel-fish-farming-project-report-cost-profits | UNTESTED 2026-09-21 |
| Freshwater prawn (scampi) | Kolkata ₹500–800/kg; Assam farmers ≈ ₹1,200/kg | retail / farmer-quoted | https://www.fishmarketindia.in/scampi-prawns-price/ ; https://thefishsite.com/articles/giant-river-prawns-prove-their-worth-in-assam | UNTESTED 2026-09-21; TN farm-gate NOT_FOUND |
| Seabass, Tamil Nadu cages 2022-23 | implied ≈ ₹500/kg (gross ÷ production); break-even ₹391/kg | farm-gate (derived) | CMFRI 2025 (§5.6) | ASSUMED derivation from VERIFIED table |
| Seabass, TN cage (earlier) | farm-gate ₹380/kg; cost ₹190/kg | farm-gate | https://eprints.cmfri.org.in/6053/1/3._Kan.pdf | UNTESTED 2026-09-21 (snippet, undated) |
| Pearl spot (karimeen), Kumarakom, Kerala, 30 Dec 2025 | A+ (>250 g) ₹600/kg (was 680); A (>150 g) ₹500 (580); B (>100 g) ₹320 (450); C ₹240 (270) | society selling price (retail-side, not paid to fishers) | Onmanorama, https://www.onmanorama.com/news/kerala/2025/12/30/karimeen-prices-vembanad-lake.html | VERIFIED 2026-09-21 |
| Pearl spot, Tamil Nadu farm-gate | — | — | — | NOT_FOUND 2026-09-21 |

Official series that exist but were not reachable on 2026-09-21: DoAC retail rohu price,
Coimbatore (CEIC mirror, HTTP 403); Agmarknet has no fish commodity series for TN — UNTESTED.

---

## 7. Evidence for yield / FCR / survival uplift from improved DO

### 7.1 Peer-reviewed nano-bubble trials

| # | Study | Species / system | Design (n, duration) | Effect | Peer-reviewed? | Status |
|---|---|---|---|---|---|---|
| 1 | Rahmawati AI et al. 2021, "Enhancement of Penaeus vannamei shrimp growth using nanobubble in indoor raceway pond", Aquaculture and Fisheries 6(3):277–282, DOI 10.1016/j.aaf.2020.03.005 | vannamei, 50 m² indoor raceway, 680 shrimp/m³, nanobubble vs diffuser aerator (paddlewheel in both) | 81 days; replicates not in abstract (NOT_FOUND) | DO significantly higher; survival "reached 95%"; ABW 15.1 ± 1.8 g; "total harvest and productivity have doubled to 436 kg and 8.7 kg/m³"; FCR and total virus-bacteria decreased (no % in abstract); NB size 82.38 nm | Yes (KeAi/Elsevier journal) | VERIFIED abstract (Semantic Scholar) 2026-09-21; full text blocked (HTTP 403) |
| 2 | Mauladani S, Rahmawati AI et al. 2020, "Economic feasibility study of L. vannamei shrimp farming: nanobubble investment…", Jurnal Akuakultur Indonesia 19(1):30–38, DOI 10.19027/jai.19.1.30-38, https://journal.ipb.ac.id/index.php/jai/article/view/29645 | vannamei, 800 m² HDPE ponds, 400 PL/m², one nanobubble pond vs one non-nanobubble pond | 56 days; n = 1 pond per treatment (Table 1) | Harvest 2,255 vs 1,884 kg (**+19.7 %**); survival **92 vs 75 %** (+17 points); FCR **1.3 vs 1.4** (−7.1 %); investment IDR 182.9 M, payback 4 cycles, IRR 18 %, B/C 1.26 | Yes (Indonesian national journal) | VERIFIED full text 2026-09-21 |
| 3 | Gymnastiar AA et al. 2025, "The role of Pure Nano Oxygen Bubbles in the nitrogen cycle of tilapia biofloc systems", Chemosphere 384:144522, DOI 10.1016/j.chemosphere.2025.144522 | Nile tilapia, biofloc tanks, BFT-PNOB vs BFT | 56 days; replicates not in abstract (NOT_FOUND) | DO 7.72 vs 6.67 mg/L (+15.7 %); final weight **57.13 vs 48.08 g (+18.8 %)**; "greater survival rate" (no number); FCR 1.04 vs 1.14 (−8.8 %) per AquaHoy summary (UNTESTED) | Yes | VERIFIED abstract 2026-09-21; FCR figure UNTESTED (https://aquahoy.com/nanobubbles-enhance-the-biofloc-system-tilapia-farming/) |
| 4 | Mahasri G et al. 2018, IOP Conf. Ser. EES 137:012046, DOI 10.1088/1755-1315/137/1/012046 | Nile tilapia, tanks (8 fish, 24.5 cm) | short-term DO test | DO 6.5 → 25 mg/L in 30 min (0.61 ppm/min); decay 3.08 ppm/day without fish; no growth/survival data | Conference proceedings (peer-reviewed by IOP) | VERIFIED abstract 2026-09-21 |
| 5 | Galang DP, …, Mahasri G et al. 2019, IOP Conf. Ser. EES 236:012014, DOI 10.1088/1755-1315/236/1/012014 | vannamei, tanks, nanobubble vs aerator | 30 days, factorial CRD; n not in abstract | DO 3.9–10.8 ppm (NB) vs 2.81–4.65 ppm (aerator) — ratio 1.4–2.3×; O2 consumption 1.10–6.84 mg O2/g/h; no growth/survival data | Conference proceedings | VERIFIED abstract 2026-09-21 |
| 6 | Nghia NH et al. 2022, "Effect of nanobubbles (oxygen, ozone) on the Pacific white shrimp, Vibrio parahaemolyticus and water quality under lab conditions", Fish Aquat Sci 25(8):429, DOI 10.47853/FAS.2022.e39 (RIA1, Bac Ninh, Vietnam) | vannamei, 100 L tanks, 15 ‰ | 20 shrimp/tank × 3 replicates × 2 experiments, 21 days | O2-NB DO ≈ 16.8 mg/L vs 5.3 control; no significant growth gain for O2-NB reported (control gain 0.787 ± 0.044 g); O3-NB lowered Vibrio mortality odds (n.s.) with minimal gill damage; O3 macrobubbles harmful | Yes | VERIFIED 2026-09-21 (https://www.e-fas.org/archive/view_article?pid=fas-25-8-429) |
| 7 | "Effects of hyperoxia during oxygen nanobubble treatment on innate immunity, growth performance, gill histology, and gut microbiome in Nile tilapia", Fish & Shellfish Immunology 2023, https://www.sciencedirect.com/science/article/abs/pii/S1050464823006770 | Nile tilapia, tanks | 26 days long-term exposure | "no apparent adverse effects on water quality, fish growth, and survival"; no gas-bubble disease — i.e. safety shown, no growth uplift reported | Yes | UNTESTED 2026-09-21 (search snippet; page blocked) |
| 8 | Xu et al. 2022, Microorganisms 10:1302, DOI 10.3390/microorganisms10071302 (Panjin, China) | vannamei, 500 m² ponds, 40/m², 1 kW nano-aerator vs 1 kW turbo aerator | 14 weeks | microbial diversity ↑, pathogens ↓; **no DO, survival, yield or FCR reported** | Yes | VERIFIED 2026-09-21 (https://pmc.ncbi.nlm.nih.gov/articles/PMC9317398/) |
| 9 | Common carp larvae O2/O3 nanobubbles, Aquaculture 2025, https://www.sciencedirect.com/science/article/abs/pii/S0044848625001784 | hatchery/larvae, not grow-out | — | best fry survival 94.07 ± 0.90 % | Yes | UNTESTED 2026-09-21 (snippet) |
| 10 | Yaparatne S et al. 2024, review, Sci Total Environ 931:172687, DOI 10.1016/j.scitotenv.2024.172687 | review | — | states air/O2 NBs raise productivity, growth, harvest and survival (no pooled effect size) | Yes (review) | UNTESTED 2026-09-21 (snippet) |
| — | Nano-bubble trials on pangasius or Indian major carp grow-out; Speece-cone tilapia RAS chapter (Springer 2025, access blocked); ICAR-CIFA / ICAR-CIBA nano-bubble trials | — | — | — | — | NOT_FOUND 2026-09-21 |

### 7.2 General DO–growth literature (aeration or DO level, not nano-bubble specific)

| Study | Species / system | Design | Effect | Status |
|---|---|---|---|---|
| Tran-Duy A, Schrama JW, van Dam AA, Verreth JAJ 2008, Aquaculture 275:152–162, DOI 10.1016/j.aquaculture.2007.12.024, PDF https://www.ecowin.org/pdf/documents/Tran-Duy%202008%20tilapia%20DO%20consumption.pdf | Nile tilapia, tanks, DO ≈ 3.0 vs 5.6 mg/L, fed to satiation | 3 tanks per treatment; 50 small (21 g) or 9 big (147 g) fish per tank; 25-day ad libitum period | Small fish growth 1.24 → 1.75 g/fish/d (**+41 %**), feed intake 1.54 → 2.15 g/d (+40 %), final weight 52.6 → 65.0 g; big fish growth 2.99 → 4.23 g/d (**+41 %**), intake 4.43 → 6.08 g/d (+37 %); oxygen effect P < 0.01; survival 100 % in all tanks; FCR row not extracted | VERIFIED full text 2026-09-21; % deltas ASSUMED (arithmetic on Table 2) |
| Abdel-Tawwab M et al. 2015, Aquaculture International, DOI 10.1007/s10499-015-9882-y | Nile tilapia 3.7 g and 12.9 g, 90 L aquaria, DO 0.1–1.5 / 2.5–3.0 / 6.0–6.5 mg/L | quadruplicates, 12 weeks, then A. hydrophila challenge | growth and feed intake "adversely affected by low DO"; post-challenge mortality highest at low DO, none at normal DO in larger fish; effect sizes not in abstract | VERIFIED abstract 2026-09-21; numbers NOT_FOUND |
| Abdel-Tawwab M et al. 2014, J Appl Aquacult 26:340–355, DOI 10.1080/10454438.2014.959830 | Nile tilapia, DO 1.0–1.5 / 2.5–3.0 / 6.0–6.5 mg/L × 2 densities | — | growth, feed intake, survival reduced below ≈50 % saturation | UNTESTED 2026-09-21 (snippet) |
| Boyd CE & Hanson T 2010, "Dissolved oxygen concentrations in pond aquaculture", Global Seafood Advocate, https://www.globalseafood.org/advocate/dissolved-oxygen-concentrations-pond-aquaculture/ | catfish (Auburn, USDA-Mississippi), shrimp (Claude Peteet Mariculture Center), tilapia (Honduras) | pond trials | Catfish: survival, production and FCR better where minimum daily DO ≥ 3.5 mg/L; USDA: more feed and growth with DO ≥ 3 mg/L, FCR unaffected down to 2 mg/L. **Shrimp: minimum DO 2.32 / 2.96 / 3.89 mg/L → survival 42 / 55 / 61 %, production 2,976 / 3,631 / 3,975 kg/ha, FCR 2.64 / 2.21 / 1.96** (i.e. +19 survival points, +33.6 % yield, −25.8 % FCR from 2.3 to 3.9 mg/L). Tilapia: aerated ponds gave larger fish and higher production | VERIFIED 2026-09-21; deltas ASSUMED (arithmetic) |
| Boyd CE 2014 (Advocate, §2.3 URL) | warm-water ponds | — | DO "should not fall below 4 mg/L"; older 2 mg/L standard called outdated | VERIFIED 2026-09-21 |
| Sultana T, Haque MM, Salam MA, Alam MM 2017, J Bangladesh Agril Univ 15(1):113–122, DOI 10.3329/jbau.v15i1.33536 | tilapia, earthen ponds, 300 fish/decimal, blower 9 h/day | 3 aerated vs 3 non-aerated ponds, ≈100 days (May–Sep 2016) | DO 7.23 vs 2.33 mg/L; production **9,581.87 vs 6,490.80 kg/ha/100 d (+47.6 %)**; SGR 2.54 vs 2.42 %/d; survival/FCR not reported | VERIFIED 2026-09-21 (abstract + article page) |
| Mallya YJ 2007, "The effects of dissolved oxygen on fish growth in aquaculture", UNU-FTP, https://www.grocentre.is/static/gro/publication/58/document/yovita07prf.pdf | Atlantic halibut 20–50 g, recirculation tanks at 60/80/100/120/140 % O2 saturation | replicated, 2 weeks | growth and FCR better at 80–120 % saturation; FCR worse at 60 % and 140 %; lowest FCR at 120 %; numbers only in figures | VERIFIED PDF 2026-09-21 (not peer-reviewed: training-programme report) |
| Boyd CE & Tucker CS 1998, Pond Aquaculture Water Quality Management (book) | — | — | not consulted directly; the Boyd 2010/2014 articles above are the same author's summaries | NOT_FOUND (direct quote) 2026-09-21 |

### 7.3 Vendor-published claims (kept separate)

- Oxyniti: "2× DO, +15 % survival, −15 % FCR, +30 % stocking density", "20–30 % yield uplift" — vendor, VERIFIED text 2026-09-21 (§1.2).
- AEROXY "16–24 HP/ha" — aerator vendor, UNTESTED.
- AquaHoy summaries of Gymnastiar 2025 — trade media, UNTESTED for the FCR figure.

### 7.4 How the site's four headline figures map onto the evidence (VERIFIED comparison 2026-09-21)

| Site figure | Best peer-reviewed support | Gap |
|---|---|---|
| 2× dissolved oxygen | Galang 2019: 1.4–2.3× vs aerator (tanks); Mahasri 2018: 6.5 → 25 mg/L (3.8×, tanks, no fish load); Sultana 2017: 3.1× (aeration vs none, ponds) | Supported in tanks; no pond-scale nano-bubble DO series found |
| +15 % survival | Mauladani 2020: 75 → 92 % (+17 points, n = 1 pond each); Rahmawati 2021: "reached 95 %" (control not in abstract); Boyd & Hanson 2010 shrimp: 42 → 61 % from raising minimum DO 2.3 → 3.9 mg/L | Supported for shrimp; no tilapia/carp/pangasius pond number |
| −15 % FCR | Mauladani 2020: 1.4 → 1.3 (−7 %); Gymnastiar 2025: 1.14 → 1.04 (−9 %, UNTESTED); Boyd & Hanson shrimp DO trial: −26 % | **−15 % is not matched by any nano-bubble trial found; −7 to −9 % is** |
| +30 % stocking density | no trial varied density; Rahmawati 2021 doubled productivity at fixed density | NOT_FOUND |
| 20–30 % yield uplift (calculator) | Mauladani +19.7 % (pond, shrimp); Gymnastiar +18.8 % weight (tank, tilapia); Sultana +47.6 % (aeration vs none) | Lower bound ≈ +19 % is supported for shrimp ponds and tilapia tanks |

---

## 8. Conflicts between sources (summary)

1. Oxyniti model line 1.5/3/5 HP (home, video) vs product catalogue 1.5 HP and 4 HP.
2. Oxyniti bubble size "<200 nm" (home/technology/about) vs "<100 nm" (product pages).
3. Oxyniti price "₹4400" on both product pages — placeholder; no real price on the site.
4. Oxyniti "100+ Installations across India" (about) vs "Currently piloting across South India" (home).
5. Oxyniti "−15 % FCR" vs −7 % to −9 % in the nano-bubble trials found.
6. Oxyniti calculator baseline 2,500 kg/acre/yr vs NABARD GIFT model 7,588 kg/acre/yr.
7. Internal GIFT model (₹2.1 L capital, ₹5.76 L variable, 9,000 kg, ₹120/kg, 1 acre) vs the cited
   PDF (₹3.69 L, ₹5.02 L/crop, 9,375 kg/crop, ₹75/kg, 1 ha).
8. TNERC-fixed ₹4.95/₹7.15/₹8.25 (quoted by calculator websites) vs consumer-payable
   ₹4.80/₹6.95/₹8.00 after Government subsidy (TANGEDCO one-page statement).
9. PMMSY biofloc unit "0.1 Ha" (PIB booklet) vs "per hectare" (Puducherry Fisheries).
10. Sagar 1 HP aerator "0.27 units/hour" vs its 0.75 kW motor; Synergy 2 HP "0.13/0.25 kg O2/h"
    vs Boyd's 2–3 kg O2 per hp·h — treat listing SOTR figures as unreliable.
11. Search aggregators presented the July 2023 Aquaconnect vannamei prices as "2026" data.
12. Sagar 2 HP listing gives both "2.5–2.8 kg O2/h" and "1.8 kg/hour" on the same page.
