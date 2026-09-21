# Tamil Nadu climate seasons, agro-climatic zones and the aquaculture calendar

Research notes for the Oxyniti yield/profit calculator. Compiled 2026-09-21. Every figure carries a status
label (VERIFIED = read in the cited source on 2026-09-21; SNIPPET = only seen in a search-engine excerpt of the
source, page itself not retrieved; ASSUMED = our modelling choice; NOT_FOUND = looked for and not found).
Companion files: `climate_normals.json` (IMD 1991-2020 station normals) and `do_physics.md`.

---

## (a) Seasons and the north-east monsoon share of annual rain

**Verdict: model the year as four IMD seasons; the north-east monsoon (Oct-Dec) delivers 48 % of the
state's annual rain, and on the coast 60-75 %.**

IMD's season definitions and the state-wide rainfall split (1971-2020 climatology) — VERIFIED 2026-09-21:

| Season (IMD) | Months | Share of Tamil Nadu annual rainfall |
|---|---|---|
| Winter | Jan-Feb | 2.7 % |
| Pre-monsoon (hot weather / summer) | Mar-May | 13.6 % |
| South-west monsoon | Jun-Sep | 35.7 % |
| Post-monsoon = north-east monsoon (NEM) | Oct-Dec | 48.0 % |

Source: IMD Pune, Climate Monitoring & Prediction Group, *Statement on Climate for the State of Tamil Nadu: 2022*,
p. 3: "Based on 1971-2020 climatology, Tamil Nadu state as a whole receives 2.7 % of its annual rainfall during
the winter season (Jan-Feb), 13.6 % during the Pre-Monsoon season (Mar-May), 35.7 % during the southwest
monsoon season (Jun-Sept) and 48 % during the Post-Monsoon season (Oct-Dec)."
https://poovulagu.org/wp-content/uploads/2023/04/Climate_Statement_2022_Tamil_Nadu_Draft.pdf (IMD document,
third-party mirror; the same seasonal shares are also given in IMD's Chapter 3 below).

Subdivision normals (Tamil Nadu, Puducherry & Karaikal) — VERIFIED 2026-09-21 from RMC Chennai, *Report on
Northeast Monsoon 2024*, IMD Chennai Scientific Report IMDC-SR/18, March 2025, p. 4
(https://mausam.imd.gov.in/chennai/mcdata/ne_monsoon_2024.pdf):
- annual normal rainfall 921.4 mm; south-west monsoon normal 328.5 mm (36 %); NEM (Oct-Dec) normal 442.8 mm (48 %);
- normal date of NEM onset over coastal Tamil Nadu: 20 October (2024 onset 15 October; 2025 onset about 16 October per
  press reports, SNIPPET);
- NEM seasonal rainfall coefficient of variation 27 % ("high degree of variability");
- the NEM season is also "the primary cyclone season for the North Indian Ocean basin".

Monthly structure of the NEM (IMD, *Northeast Monsoon* monograph, Chapter 3, 1971-2020 subdivisional data) —
VERIFIED 2026-09-21: Oct 17 cm, Nov 18 cm, Dec 9 cm (39 / 41 / 20 % of the season); season 44 cm = 48 % of the
92 cm annual. "In Tamil Nadu, November gets as much rain as October. By December, the rainy season is practically
confined over extreme south Peninsula ... in December, rainfall activity is confined only to the coastal districts."
https://mausam.imd.gov.in/responsive/pdf_viewer_css/met1/Chapter-3%20page%2037-51/Chapter-3%20.pdf

Coastal versus interior — derived from the station normals in `climate_normals.json` (IMD 1991-2020),
COMPUTED 2026-09-21 as (Oct+Nov+Dec)/annual:

| Station (zone) | Annual mm | Oct-Dec share | Jun-Sep share |
|---|---|---|---|
| Pamban, Ramanathapuram (Southern, coast) | 952.8 | 74.7 % | 7.7 % |
| Thoothukudi (Southern, coast) | 682.5 | 71.5 % | 5.0 % |
| Nagapattinam (Cauvery Delta, coast) | 1349.0 | 71.1 % | 18.3 % |
| Karaikal (Delta, coast) | 1468.0 | 69.1 % | 19.7 % |
| Cuddalore (North Eastern, coast) | 1369.8 | 65.5 % | 25.4 % |
| Koradacheri, Tiruvarur (Delta, inland) | 1021.9 | 63.9 % | 26.1 % |
| Chennai Nungambakkam (North Eastern, coast) | 1376.8 | 62.2 % | 31.9 % |
| Thanjavur (Delta) | 1051.1 | 59.8 % | 30.6 % |
| Tiruchirappalli (Delta, interior) | 860.2 | 49.4 % | 35.8 % |
| Madurai city (Southern, interior) | 672.2 | 48.8 % | 32.4 % |
| Coimbatore (Western) | 618.5 | 53.2 % | 25.7 % |
| Vellore (North Eastern, interior) | 1050.1 | 38.9 % | 49.9 % |
| Salem (North Western) | 992.2 | 34.4 % | 47.4 % |
| Dharmapuri (North Western) | 942.0 | 36.6 % | 42.8 % |
| Ooty, Nilgiris (Hilly) | 1157.4 | 33.1 % | 46.1 % |
| Valparai, Anamalai (Hilly, west-facing) | 3538.0 | 13.2 % | 73.0 % |

Pattern: the east coast and the delta are NEM-dominated (60-75 %); the north-western interior (Vellore, Salem,
Dharmapuri) is SWM-dominated (43-50 %); the Nilgiris/Anamalai are SWM-dominated. The often-quoted "coastal
districts about 60 %, interior 40-50 %" statement from the IMD Chennai NE-monsoon web page could not be read
(imdchennai.gov.in refused connections on 2026-09-21; SNIPPET only) but is consistent with the station table.

Hottest month, from the same normals — COMPUTED 2026-09-21: May at almost every lowland station (April at
Coimbatore, Karur, Kamachipuram, Kanniyakumari; June at Nagapattinam and Thoothukudi). Lowland May means
(Tmax+Tmin)/2 are 30.7-33.2 degC; May Tmax 34.1 degC (Thondi) to 39.9 degC (Tiruttani).

## (b) The seven agro-climatic zones (TNAU)

Source: Tamil Nadu Agricultural University, *Tamil Nadu Agro Climatic Zones*,
https://tnau.ac.in/tamil-nadu-agro-climatic-zones/ — VERIFIED 2026-09-21 (district lists quoted verbatim; TNAU
uses the post-2019 district names).

| Zone | Districts (TNAU) | Rainfall / notes (TNAU) |
|---|---|---|
| 1. North Eastern | Kanchipuram, Chengalpet, Tiruvallur, Cuddalore, Villupuram, Kallakuruchi, Vellore, Tirupathur, Ranipet, Tiruvannamalai | 352 mm in the south-west monsoon; 200-day growing season; "prone to cyclonic damage" |
| 2. North Western | Dharmapuri, Salem, Namakkal | 400 mm via SWM; mean max 30-37 degC, mean min 19-25.5 degC; 180-day growing season |
| 3. Western | Erode, Coimbatore, Karur (part), Namakkal (part), Dindigul (part), Theni (part) | 715 mm annual, 49 % in the NEM |
| 4. Cauvery Delta | Tiruchi, Perambalur, Pudukottai (part), Thanjavur, Nagapattinam, Mayiladuthurai, Tiruvarur, Cuddalore (part) | 984 mm annual, "more than 50 per cent ... through Northeast monsoon rains"; rice predominant |
| 5. Southern | Madurai, Sivagangai, Ramanathapuram, Virudhunagar, Tirunelveli, Tenkasi, Thoothukudi | 857 mm annual; max 28-38.5 degC, min 21-27.5 degC |
| 6. High Rainfall | Kanniyakumari | 1420 mm in 64 rainy days |
| 7. Hilly and High Altitude | Nilgiris, Kodaikanal | 2124 mm annual; only 0.84 % of cultivated area irrigated |

Note: Ariyalur (carved from Perambalur) and Krishnagiri (from Dharmapuri) are not named on the TNAU page; in
`climate_normals.json` Ariyalur is placed in the Cauvery Delta zone (ASSUMED).

## (c) The aquaculture calendar in Tamil Nadu

**Verdict: shrimp has a documented two-crop calendar (summer crop stocked Mar-Apr, monsoon crop stocked Jul-Aug);
vannamei is officially "year-round"; freshwater fish in the delta run continuous partial-harvest cycles. No
official month-by-month stocking calendar for carp, tilapia or murrel in Tamil Nadu was found — that part is
modelled, not sourced.**

### Shrimp (Penaeus monodon and Litopenaeus vannamei)

MPEDA, *Shrimp cropping pattern* (https://mpeda.gov.in/?page_id=645) — VERIFIED 2026-09-21:

| State | Species | Crop | Stocking | Harvest |
|---|---|---|---|---|
| Tamil Nadu | P. monodon | 1 (summer) | Mar-Apr | Jun-Jul |
| Tamil Nadu | P. monodon | 2 (monsoon) | Jul-Aug | Oct-Nov |
| Tamil Nadu | L. vannamei | "year round" | Jan-Dec | Jan-Dec |
| Andhra Pradesh | P. monodon | 1 / 2 | Jan-Mar / Jul-Aug | May-Jun / Sep-Nov |

MPEDA's wording: for vannamei "the general trend is to go for year round culture with no distinct crop season
except in some places"; for tiger shrimp "two crops are practiced in scientific farms viz. the dominant summer crop
followed by a monsoon crop". A trade review of India's 2021 crop states two vannamei cycles, Feb-Jun and
Jul-Oct, with farmers "generally reluctant to go for a second cycle, fearing diseases" (Aquaculture Asia Pacific,
Sep/Oct 2022 — SNIPPET, page not retrieved).

Farmer crop calendar from the ICAR-CIBA/NACA AquaClimate case study (Krishna district, Andhra Pradesh — not Tamil
Nadu, but the same east-coast two-crop logic) — VERIFIED 2026-09-21 (Muralidhar et al. 2012,
https://library.enaca.org/emerging_issues/climate_change/india-shrimp-climate-change-ebook.pdf): pond preparation
and drying in the dry months Jan-Feb (crop 1) and May-Jun (crop 2); water filling and bloom development Feb-Mar and
Jul-Sep; harvest May-Jun and Nov-Dec; "diseases were more during monsoon and post monsoon period. Hence in most of
the areas second crop was not a successful one"; floods, cyclones and high tides are the unusual events "in the
months of May and November"; summer peak temperatures May-Jun (air 50 degC recorded in 2007).

Tamil Nadu vannamei parameters (TNAU/NABARD model project *Culture of white legged shrimp, L. vannamei*, 2015,
https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/5.Culture_of_Vannamei_white_legged_shrimp_15.pdf) —
VERIFIED 2026-09-21: reaches 20 g in 100-120 days depending on density; "Dissolved oxygen levels above 4.5 ppm are
required for optimal growth"; "growth at 30 degC is much higher than at 25 degC. The optimal range of temperature for
the species is between 30 and 34 degC. At 20 degC growth virtually stops"; uniform growth at 10-40 ppt. Caution: the
30-34 degC optimum is TNAU's statement; laboratory work puts the metabolic optimum at 25-30 degC (Kir et al. 2023,
see `do_physics.md`) — treat TNAU's upper bound as UNTESTED.

Observed Tamil Nadu shrimp-farm conditions — VERIFIED 2026-09-21:
- Vellar estuary, Cuddalore district, Apr-Aug 2014 (crop 1): water 27-32 degC, DO 3-5.2 mg/L, salinity 15-38 psu,
  pH 7.8-8.7, survival 80-90 %, FCR 1.39-1.40, ABW 20-34 g, production 3,200-4,689 kg per pond
  (Suriya, Shanmugasundaram & Mayavu 2016, Int. J. Curr. Res. Biol. Med. 1(5):26-32,
  https://darshanpublishers.com/ijcrbm/pdfcopy/2016/aug2016/ijcrbm4.pdf).
- Thoothukudi district farms, Sep 2013-Apr 2014: water 26.5-29.5 degC, DO 3.5-7.3 (printed as ml/l), salinity
  36.5-42.5 ppt (Poonkodi et al. 2016, J. Exp. Zool. India 19(1):195-200,
  https://connectjournals.com/file_full_text/2430901H_195-200.pdf). The paper cites Jayasankar & Muthu (1983) for
  a pond low of 25 degC "attained due to cloudy weather".
- Shrimp farms in Nagapattinam district sit "only 1 meter or less above mean sea level", ponds 0.5-1.1 ha and
  0.9-1.4 m deep; farmers rank floods, cyclones and heavy/torrential rain as the three major threats (Jayanthi,
  Muralidhar, Kumaran & Vijayan, ICAR-CIBA, Global Seafood Advocate, 23 Oct 2017,
  https://www.globalseafood.org/advocate/shrimp-farm-design-improvements-india/).
- A 40-year (1961-2000) trend analysis of Nagapattinam shrimp-area weather found a significant warming trend in
  maximum temperature but "trend does not exist for rainfall" (Ashok Kumar, Muralidhar, Jayanthi & Kumaran 2013,
  J. Agrometeorology 15(2):129-134, https://doi.org/10.54386/jam.v15i2.1459).

### Carp polyculture (catla, rohu, mrigal, common carp, grass carp)

- TNAU/NABARD *Intensive fish culture* model (2015,
  https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/4.Intensive_fish_culture_15.pdf) — VERIFIED 2026-09-21:
  catla and rohu; "Harvesting is generally done at the end of 6 months, when the fishes attain average weight of
  1 to 1.25 kg. A production of 5-6 tons/ha can be obtained in a year"; "two crops are possible in a year"; pond
  depth 1.5-2.0 m, minimum 1.0 m; "even seasonal ponds can also be utilised for short duration fish culture".
  Stocking of 50-100 g fingerlings at 5,000/ha (or 250 g at 6,250/ha) and 10-12 month rearing appear in TNAU's
  composite-culture documents (SNIPPET).
- Cauvery-delta practice (DTNext, 11 Aug 2025, S.J. Michael Collins,
  https://www.dtnext.in/news/tamilnadu/high-potential-for-inland-aquafarming-visible-in-tn-842891) — VERIFIED
  2026-09-21: murrel, rohu, catla, mrigal, common carp and grass carp in freshwater ponds across Tiruchy, Thanjavur,
  Tiruvarur, Mayiladuthurai, Nagapattinam and Pudukkottai; fingerlings to about 700 g in a year minimum; "fish over
  500 g are harvested every 3-4 months, with simultaneous stocking with fingerlings"; delta supplies 35 % of Tamil
  Nadu's inland fish; state production 2.32 lakh t.
- Indian reference system (Andhra Pradesh, Nair & Salin 2007, Global Seafood Advocate,
  https://www.globalseafood.org/advocate/carp-polyculture-in-india/) — VERIFIED 2026-09-21: 8,000-10,000 fingerlings/ha
  (catla:rohu 1:10), partial harvest at 6 and 9 months, complete harvest at 12 months, 10-13 t/ha/yr.
- Explicit Tamil Nadu stocking months for carp: NOT_FOUND 2026-09-21 (TNAU, Fisheries Department and district
  pages give species and densities but no calendar; fisheries.tn.gov.in refused connections). Modelling assumption
  (ASSUMED): perennial ponds are stocked year-round with partial harvests every 3-4 months (DTNext); seasonal tanks
  fill in the NEM (Oct-Dec), are stocked Nov-Jan and harvested before they dry in May-Jun — consistent with the murrel
  source below ("harvested during the summer months ... in irrigation tanks").

### Tilapia (GIFT / sex-reversed Nile tilapia)

- Government of India, Department of Fisheries, *Guidelines for Responsible Farming of Tilapia in India* (April 2020,
  https://www.dof.gov.in/static/uploads/2025/08/5b11d46b28883fbf74f4738caae739ab.pdf) — VERIFIED 2026-09-21: stock
  sex-reversed seed > 10 g at 5 nos/m2; CIFA demonstrations "production levels of 5-6 MT per crop of 4-6 months
  duration"; farms must hold biosecurity "even in situations like flooding".
- TNAU/NABARD *GIFT Tilapia culture* (2015,
  https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/6.GIFT_Tilapia_culture_15.pdf) — VERIFIED 2026-09-21:
  nursery rearing in hapas for at least one month at 50-75 fry/m2, then grow-out at 3-5 nos/m2; commercial feed FCR
  1.25-1.5. Stocking months: not specified (NOT_FOUND).

### Murrel (striped snakehead, Channa striata)

- Boini, Gunakar & Bakshi 2024, *Recent Advances in Murrel (Snakehead) Fish Farming in India*, Acta Scientific
  Veterinary Sciences 6(11):29-35 (https://actascientific.com/ASVS/pdf/ASVS-06-0940.pdf) — VERIFIED 2026-09-21:
  stocking 400-600 fingerlings/ha in irrigation tanks, 10,000-12,000/ha in exclusive culture ponds; "murrel fish is
  harvested during the summer months, when the fish attains a marketable size in irrigation tanks"; 150-250 kg/ha/yr in
  tanks, 8-10 t/ha/yr in fed culture ponds; spawns naturally in the south-west monsoon and also in the north-east
  monsoon; induced breeding on cool cloudy days at 25-30 degC; air-breathing, "ability to withstand low dissolved
  oxygen". Grow-out of 5-8 cm fingerlings at 10,000/ha to 600-700 g in 8-10 months appears in NFDB/Vikaspedia
  guidance (SNIPPET; both pages unreachable on 2026-09-21).

### Freshwater prawn (Macrobrachium rosenbergii)

- TNAU Agritech *Freshwater prawn* page (https://agritech.tnau.ac.in/fishery/fish_freshwaterprawn.html) — VERIFIED
  2026-09-21: water temperature 28-31 degC; DO 3-7 ppm; 4,000-50,000 PL/ha; culture period 6-8 months (monoculture)
  or 8-12 months (polyculture); Tamil Nadu 192 ha / 144 t in the state table. Stocking months not specified.
- Soundarapandian, Balamurugan & Samuel 2008, Int. J. Zool. Res. 4(2):72-76
  (https://scialert.net/fulltext/?doi=ijzr.2008.72.76) — VERIFIED 2026-09-21: Parangipettai (Cuddalore district),
  193-day grow-out after a 45-day nursery, 33,000 PL/ha monoculture (561 kg/ha) or 25,000/ha + 1,000 fish/ha
  polyculture (361-381 kg/ha prawn + 500 kg/ha fish); water 27-31 degC and DO 4.0-6.0 ppm throughout.

### Monsoon and cyclone flood risk in the Cauvery delta and the north coast

- Cyclone Gaja, 16 Nov 2018: Nagapattinam among the worst-hit; winds about 120 km/h and coastal flooding; aqua-farming
  households in Avarikadu lost nets and had ponds polluted (Caritas India / ReliefWeb,
  https://reliefweb.int/report/india/fishnets-distributed-cyclone-gaja-affected-aqua-farmers; CMFRI impact study,
  Shyam Salim et al. 2022, Indian J. Geo-Marine Sci.) — VERIFIED 2026-09-21 (secondary).
- Cyclone Nivar, 25 Nov 2020: "the state's delta region ... Thanjavur, Nagapattinam and Tiruvarur, suffered the most"
  (Mongabay-India, Dec 2020,
  https://india.mongabay.com/2020/12/though-cyclone-nivar-had-a-soft-landing-floods-hit-coastal-districts/) — VERIFIED.
- Cyclone Fengal, 30 Nov-1 Dec 2024: 2,11,139 ha of agricultural/horticultural land inundated; Villupuram, Cuddalore,
  Kallakurichi, Tiruvannamalai worst hit; over 160 water bodies in Villupuram breached (News on AIR, 2 Dec 2024;
  Wikipedia "Cyclone Fengal") — VERIFIED (secondary). Aquaculture-specific loss figures: NOT_FOUND.
- Cyclone Mandous, 6-10 Dec 2022, crossed the north Tamil Nadu coast near Mamallapuram (IMD Statement 2022) — VERIFIED.
- The IMD normals confirm the exposure: Nov rainfall normals are 373.6 mm (Chennai), 389.5 mm (Cuddalore), 446.2 mm
  (Nagapattinam), 493.4 mm (Karaikal) and 288.7 mm (Thanjavur) (`climate_normals.json`, VERIFIED 2026-09-21).

## (d) Pond water temperature versus air temperature

**Verdict: over weeks, pond mean water temperature equals mean air temperature within about +1 degC; ponds damp
the diurnal swing to roughly two-thirds of the air swing. Code it as T_water(month) = T_air_mean(month) + 0.5 degC
with +/-1 degC uncertainty (ASSUMED), or with the Bangladesh regression below.**

Published statements and regressions:
- Boyd, C.E. 2010, *Examining water temperature in aquaculture*, Global Seafood Advocate
  (https://www.globalseafood.org/advocate/examining-water-temperature-aquaculture/) — VERIFIED 2026-09-21: "When
  considered over periods longer than several days, water temperature closely tracks air temperature"; brief cool
  spells do not change pond temperature much, but after several days the pond equilibrates with the air; keep ponds
  shallower than 2.0 m to limit stratification; a Polish study found 1 degC change in mean seasonal temperature alters
  intensive common-carp production by 1,000 kg/ha.
- FAO, *Site selection for aquaculture: physical features of water* (https://www.fao.org/4/ac174e/AC174E02.htm) —
  VERIFIED 2026-09-21: "There is usually a close correlation between air temperature and pond water temperature,
  though usually pond temperatures do not fluctuate as greatly as air temperature"; 1 m ponds destratify at night,
  1.5-2 m ponds at Auburn stayed stratified through the warm months; in some tropical ponds surface water can reach
  near 40 degC and fall near 20 degC in the same day.
- Nile tilapia nursery pond, Cumilla, Bangladesh, 0.25 ha, 1.5-1.7 m deep, 1,461 daily readings (bioRxiv preprint
  2026, https://www.biorxiv.org/content/10.64898/2026.08.01.742243v1) — VERIFIED 2026-09-21 (preprint, not peer
  reviewed): daily mean water = 0.922 x air + 2.32 degC, r = 0.976 (R2 = 0.952); mean water 27.61 +/- 4.68 degC versus
  air 27.45 +/- 4.95 degC (difference +0.16 degC); diurnal range water 5.96 degC versus air 8.66 degC; coupling weaker
  in winter (r = 0.776).
- Tilapia broodfish pond, Mymensingh, Bangladesh, Feb 2021-Jan 2022 (Siddique, Mahalder, Haque & Ahammad 2024,
  Heliyon 10(18):e37717, https://doi.org/10.1016/j.heliyon.2024.e37717) — VERIFIED 2026-09-21: monthly water
  20.81-31.23 degC against air 18.93-30.12 degC (water about 1-2 degC above air at both ends of the range); cross-
  correlation 0.845 at lag 0; DO 7.09-10.65 mg/L.
- Energy-balance model (Gao-Merrick) driven by NASA POWER climate data for ponds at Khulna and Sylhet, Bangladesh
  (Frontiers in Climate 2024, https://doi.org/10.3389/fclim.2024.1440671) — VERIFIED 2026-09-21: daily predicted versus
  observed water temperature R2 = 0.88 with slope near 1 and intercept near 0 at Khulna; R2 = 0.70 at Sylhet where
  extreme rain events caused sharp cooling spikes; seasonal amplitude of water temperature under 3 degC at these sites.
- 2.6 ha earthen pond, 1.5-2.5 m deep, Nanjing, China, August 2023 (Li, Feng, Qian & Wei 2025, PLOS ONE 20(1):e0317523,
  https://doi.org/10.1371/journal.pone.0317523) — VERIFIED 2026-09-21: "daily average water temperature in the pond is
  no more than 1 degC higher than the average air temperature"; diurnal water range about 2 degC; water peak lags the
  air peak by several hours and the lag grows with depth; night-time water column near-isothermal.
- A claimed sensitivity of "0.87-0.94 degC water per 1 degC air (Ali et al. 2016)" appeared only in a search-engine
  summary; the cited papers do not contain it — NOT_VERIFIED, do not use.

Rain events: a rain shower is "5 to 6 degC lower than the environment" and pond temperature "generally decreases by
3 to 5 degC" (Buike 2018, see (f)) — VERIFIED, Ecuador context.

## (e) Reported pond water temperatures in Tamil Nadu by season

**Verdict: the only Tamil Nadu pond series found span 26.5-32 degC; nobody has published a peak-summer (Apr-Jun)
water series for an interior Tamil Nadu fish pond, so summer pond temperature must be estimated from air normals.**

| Site | Period | Water temperature | DO | Source / status |
|---|---|---|---|---|
| Village pond, Thittai, Thanjavur district | Jul 2015-Jun 2016, seasonal sampling | 26.9-31.9 degC | 6.5-7.9 mg/L | Dinesh Kumar, Karthik & Rajakumar 2017, J. Entomol. Zool. Stud. 5(4):1232-1238 (https://www.entomoljournal.com/archives/2017/vol5issue4/PartP/5-4-74-223.pdf) — VERIFIED 2026-09-21 (note the paper's "salinity 10-19 ppt" for a freshwater pond is implausible; treat other values with care) |
| Vannamei farms, Vellar estuary, Cuddalore | Apr-Aug 2014 | 27-32 degC | 3-5.2 mg/L | Suriya et al. 2016 — VERIFIED |
| Vannamei farms, Thoothukudi district | Sep 2013-Apr 2014 | 26.5-29.5 degC | 3.5-7.3 (units as printed) | Poonkodi et al. 2016 — VERIFIED |
| Freshwater prawn ponds, Parangipettai, Cuddalore | 193-day crop | 27-31 degC | 4.0-6.0 ppm | Soundarapandian et al. 2008 — VERIFIED |
| Interior carp ponds (Tiruchirappalli, Salem, Vellore) in Apr-Jun | — | NOT_FOUND | — | searched 2026-09-21 |

Estimate for the calculator (ASSUMED, from `climate_normals.json` and section (d)): May mean air temperature at
lowland stations is 30.7-33.2 degC, so a 1-1.5 m earthen pond in May should average 31-34 degC with afternoon
surface readings of 34-36 degC; December-January means of 24-26 degC give pond means of 24-27 degC. These are
derived, not measured.

## (f) Known seasonal fish-kill and low-DO periods in Tamil Nadu

**Verdict: the documented Tamil Nadu kills are mostly pollution-triggered; the pre-dawn summer DO crash and the
first-rain / cloudy-spell crash are well described mechanistically but almost never reported from Tamil Nadu farms
by name. Treat the summer (Apr-Jun) and the monsoon cloudy-spell (Jul-Sep, Oct-Nov) windows as the risk seasons.**

Tamil Nadu incidents (all secondary reports, compiled by SANDRP from named newspapers):
- Vellore Fort moat, 23 Apr 2022: mass fish death; officials cited oxygen depletion worsened by 40 degC heat and
  unauthorised sewage inflow (The Hindu, via SANDRP 2022,
  https://sandrp.in/2022/11/20/wfd-2022-mass-fish-deaths-in-lakes-ponds-in-india/) — VERIFIED 2026-09-21 (secondary).
- Bhavanisagar reservoir, Erode, 29 Apr 2024: dead fish floating as water level fell with no inflow from the Nilgiris
  catchment (Afternoon News, via SANDRP 2024,
  https://sandrp.in/2024/11/21/wfd-2024-mass-fish-kill-in-indian-rivers-wetlands-continue/) — VERIFIED (secondary).
- Farm well, Villarasampatti, Erode, 4 Nov 2025 (fifth event; a 2024 event attributed to "oxygen depletion and
  pollution"); Kanirowther lake, Erode, 12 Jun 2025 (textile effluent); Ponneri lake, Villupuram, 27 May 2025
  (industrial waste, "hundreds of fish", fishermen's losses in lakhs) (SANDRP 2025,
  https://sandrp.in/2025/11/23/wfd-2025-mass-fish-death-in-lakes-ponds-in-india/) — VERIFIED (secondary).
- Aquaculture-farm DO kills reported from Tamil Nadu with dates: NOT_FOUND 2026-09-21 (searches of news and CIBA
  material returned only generic guidance).

Mechanisms and neighbouring-state evidence:
- Summer heat: Goa 2024 heat wave, 2-5 % fish mortality in lakes and ponds with water levels 67-75 cm below the ideal
  1-1.5 m (Mint, June 2024, via ICSF, https://icsf.net/newss/india-dead-in-the-water-how-heatwaves-are-killing-fish/)
  — VERIFIED (secondary). Telangana fisheries officials advise partial harvest in summer because falling water
  levels lower DO and cause mass deaths (Deccan Chronicle, May 2026) — SNIPPET.
- First rains: Bengaluru lakes, May-Jun 2022 — first showers wash organic matter into lakes, microbial decay
  consumes DO (SANDRP 2022) — VERIFIED (secondary).
- Rain and cloudy spells on shrimp ponds (Buike 2018, Global Seafood Advocate,
  https://www.globalseafood.org/advocate/rainy-season-effects-on-shrimp-grow-out-ponds/; repeated for India by
  Skretting India, 30 Jul 2022) — VERIFIED 2026-09-21: pond temperature drops 3-5 degC; feed intake falls about 10 %
  per degC; DO "can reach dangerous levels (equal or less than 3 ppm) in less than half an hour"; mortality of 3-50 %
  "typically occurs two to three days after the rains"; recommended: cut feed 70 % during rain, hold DO above 4 ppm.
- Warm cloudy weather: "During periods of warm, cloudy weather most ponds may need continuous aeration for several
  days" (SRAC pond-aeration fact sheet via The Fish Site, https://thefishsite.com/articles/pond-aeration-1) — VERIFIED.
- ICAR-CIBA Technical Advisory No. 7, *Soil and water quality management for shrimp farming*
  (https://ciba.res.in/wp-content/uploads/2020/06/Soil-and-water-quality.pdf) — VERIFIED 2026-09-21: monitor
  temperature, pH, salinity, DO and transparency routinely; pH 7.5-8.5 and not varying more than 0.5 in a day;
  salinity change not exceeding 5 ppt in a day. (No explicit seasonal DO advisory in the document.)
- AquaClimate (AP) projections: the May-June temperature peak "poses significant risks such as increase in salinity
  and thermal stratification resulting in dissolved oxygen problems in culture ponds" (Muralidhar et al. 2012) — VERIFIED.

Risk windows for the calculator (ASSUMED 2026-09-21, from the above): (1) Apr-Jun pre-dawn DO minima at 31-34 degC
water and low saturation; (2) Jul-Sep and Oct-Nov cloudy/rainy spells (photosynthesis collapse plus temperature and
salinity shocks); (3) Oct-Dec flood/cyclone losses on the coast and delta; (4) Dec-Jan low temperatures slow growth
of vannamei and tilapia but are the safest DO period.

---

Sources not reachable on 2026-09-21 (recorded so nobody re-tries them blindly): imdchennai.gov.in (connection
refused), fisheries.tn.gov.in (connection refused), nfdb.gov.in (DNS failure), vikaspedia murrel page (empty body),
web.archive.org (blocked by the fetch tool).
