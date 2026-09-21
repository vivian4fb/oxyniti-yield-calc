# Dissolved-oxygen physics for the Oxyniti yield calculator

Model specification and source notes. Compiled 2026-09-21. Status labels: VERIFIED = read in the cited source
on 2026-09-21; COMPUTED = calculated here in Python (`do_verify.py`, listing at the end); SNIPPET = seen only in a
search-engine excerpt; ASSUMED = modelling choice; NOT_FOUND = searched, not found. British units: mg/L, degC, ppt,
atm.

---

## (a) Oxygen solubility: Benson & Krause (1984) as used by USGS DOTABLES

**Verdict: code Eq. 32 of Benson & Krause (1984) with the mg/L constant, the Setschenow salinity term, and the
USGS pressure factor. All three pieces were verified against the primary paper on 2026-09-21; the numeric table
below is the test oracle for the JavaScript port.**

Primary source: Benson, B.B. & Krause, D. Jr. (1984). The concentration and isotopic fractionation of oxygen dissolved
in freshwater and seawater in equilibrium with the atmosphere. *Limnology and Oceanography* 29(3):620-632,
https://doi.org/10.4319/lo.1984.29.3.0620 (PDF read at
https://ecowin.org/pdf/documents/Benson%20&%20Krause%201984%20oxygen%20saturation%20L&O.pdf). USGS adopted these
equations in Office of Water Quality Technical Memorandum 2011.03 and in DOTABLES
(https://water.usgs.gov/water-resources/software/DOTABLES/); both USGS pages refused connections on 2026-09-21, so
the USGS-specific pressure form was verified numerically against the paper's own Table 9 instead (see below).

### Temperature dependence at 1 atm, freshwater (Eq. 32, mg/L form) — VERIFIED 2026-09-21

With T in kelvin (T = t_degC + 273.15):

    ln C* = -139.34411 + 1.575701e5 / T - 6.642308e7 / T^2 + 1.243800e10 / T^3 - 8.621949e11 / T^4

C* is the "unit standard atmospheric concentration": O2 in mg/L in water in equilibrium with water-saturated air at a
total pressure of 1 atm. The paper gives Eq. 32 with first constant -135.90205 for umol/dm3 and states "for C* in
mg/liter (equivalent to Table 7) we substitute (-139.34411) for the first constant".

### Salinity term (Setschenow term of the same Eq. 32) — VERIFIED 2026-09-21

    ln C*(S) = ln C*(0) - S * (0.017674 - 10.754 / T + 2140.7 / T^2)

S is practical salinity (for brackish ponds use ppt; the difference from PSU is negligible at this precision). Valid
0-40 salinity, 0-40 degC per the paper's abstract. The equivalent factor used by USGS is
Fs = exp(-S (0.017674 - 10.754/T + 2140.7/T^2)).

### Pressure / altitude correction — VERIFIED 2026-09-21 against Benson & Krause 1984 Table 9

USGS/DOTABLES form (Benson & Krause 1980, 1984):

    Fp = [(P - u) (1 - theta P)] / [(1 - u) (1 - theta)]
    DO_sat(t, S, P) = C*(t, S) * Fp

where P = total (barometric) pressure in atm, u = saturation vapour pressure of water in atm, and theta is the
second-virial-coefficient term:

    theta = 0.000975 - 1.426e-5 t + 6.436e-8 t^2          (t in degC)
    u     = exp(11.8571 - 3840.70 / T - 216961 / T^2)      (atm, T in kelvin)

theta is verified: the paper's table of constants lists "(1 - theta) = 0.999025 + 1.426e-5 t - 6.436e-8 t^2"
(Benson et al. 1979). The vapour-pressure form gives 23.759 mmHg at 25 degC against the reference 23.756 mmHg, and
the Antoine form used by the LakeMetabolizer R package (u = 10^(8.10765 - 1750.286/(235 + t)) mmHg, USGS memos
81.11/81.15; https://github.com/GLEON/LakeMetabolizer, R/o2.at.sat.R) gives 23.756 mmHg — COMPUTED 2026-09-21. The
bracketed quantity Fp/P reproduces Benson & Krause's Table 9 at nine (P, t) points to within 0.0001 (worst case
P = 0.5 atm, t = 10 degC: computed 0.9881 versus 0.9882) — COMPUTED 2026-09-21. The paper notes the bracket "depends
very little upon salinity", so the same Fp is used for brackish water.

Barometric pressure from station elevation (standard atmosphere, as in LakeMetabolizer) — ASSUMED adequate for
Tamil Nadu lowlands:

    P(atm) = exp(-9.80665 * 0.0289644 * z_m / (8.31447 * 288.15))

Tamil Nadu ponds are within 0-400 m (Fp = 1.000 to 0.952); only the Nilgiris/Kodaikanal (2,250-2,340 m,
Fp about 0.75) need the correction to matter.

### Verification table — COMPUTED 2026-09-21 with `do_verify.py` (test oracle for the JavaScript)

DO saturation, mg/L, total pressure 1.000 atm (sea level):

| t degC | S = 0 ppt | S = 15 ppt | S = 25 ppt | drop 0 -> 25 ppt |
|---|---|---|---|---|
| 20 | 9.092 | 8.322 | 7.846 | 13.7 % |
| 25 | 8.263 | 7.588 | 7.168 | 13.3 % |
| 28 | 7.828 | 7.201 | 6.811 | 13.0 % |
| 30 | 7.559 | 6.961 | 6.589 | 12.8 % |
| 32 | 7.305 | 6.734 | 6.379 | 12.7 % |
| 35 | 6.949 | 6.416 | 6.084 | 12.5 % |

Full test vector (t, S, P_atm -> mg/L, four decimals) including P = 0.95 atm:
20,0,1.00,9.0924 | 20,0,0.95,8.6274 | 20,15,1.00,8.3223 | 20,15,0.95,7.8967 | 20,25,1.00,7.8455 | 20,25,0.95,7.4443 |
25,0,1.00,8.2635 | 25,0,0.95,7.8372 | 25,15,1.00,7.5878 | 25,15,0.95,7.1964 | 25,25,1.00,7.1684 | 25,25,0.95,6.7986 |
28,0,1.00,7.8278 | 28,0,0.95,7.4215 | 28,15,1.00,7.2005 | 28,15,0.95,6.8267 | 28,25,1.00,6.8105 | 28,25,0.95,6.4570 |
30,0,1.00,7.5588 | 30,0,0.95,7.1646 | 30,15,1.00,6.9609 | 30,15,0.95,6.5978 | 30,25,1.00,6.5888 | 30,25,0.95,6.2452 |
32,0,1.00,7.3050 | 32,0,0.95,6.9219 | 32,15,1.00,6.7344 | 32,15,0.95,6.3813 | 32,25,1.00,6.3790 | 32,25,0.95,6.0445 |
35,0,1.00,6.9493 | 35,0,0.95,6.5816 | 35,15,1.00,6.4164 | 35,15,0.95,6.0769 | 35,25,1.00,6.0840 | 35,25,0.95,5.7621

Altitude examples at 30 degC, freshwater — COMPUTED: sea level 7.559 mg/L; Tiruchirappalli 88 m 7.477 mg/L
(P 0.990 atm); Coimbatore 395 m 7.198 mg/L (P 0.954 atm); Kodaikanal 2,343 m 5.646 mg/L (P 0.758 atm).

Independent cross-checks — COMPUTED against VERIFIED published statements: Boyd (2001) gives 8.24 mg/L at 25 degC
freshwater (computed 8.263, +0.02 mg/L) and 5.61 mg/L at 35 degC / 35 ppt (computed 5.77, +0.16 mg/L — Boyd's figure
evidently comes from an older table; the 2.8 % discrepancy is outside our tolerance and is noted, not resolved);
Boyd (2018) states saturation is "9.28 percent greater at 25 degC than at 30 degC in freshwater" (computed 9.32 %).

Percent saturation of a measured DO: %sat = 100 * DO_measured / DO_sat(t, S, P). Warm-water thresholds in (c) are
often quoted as % saturation because saturation itself falls 14 % from 20 to 30 degC and 13 % from 0 to 25 ppt.

## (b) Oxygen consumption versus temperature (Q10)

**Verdict: use Q10 = 1.8-2.0 for fish between 25 and 34 degC (tilapia 1.79 measured; rohu 1.9-2.05 measured);
for L. vannamei no verified Q10 was retrievable — use Q10 = 2 up to 30 degC and hold flat above (ASSUMED), because
the best available study finds standard metabolism falling with temperature inside the 25-30 degC optimum.**

| Species | Value | Conditions | Source / status |
|---|---|---|---|
| Nile tilapia | Q10 = 1.79 for standard metabolic rate; SMR 79.8 mg O2/kg/h at 18 degC to 255.1 at 38 degC; SMR flat 18-22 degC, steepest at the top of the range; aerobic-scope optimum 26.0 degC, 80 %-scope range 19.5-32.1 degC; CTmax 38.8 degC | six acclimation temperatures 18-38 degC | Leonard & Skov 2022, J. Thermal Biol. 105:103206, https://doi.org/10.1016/j.jtherbio.2022.103206 (PubMed 35393047) — VERIFIED 2026-09-21 |
| Nile tilapia (Tabasco line) | Q10 for MO2 "typical for fish over the range 25-35 degC of 1.5-2.0"; Pcrit 12-17 mmHg at 25-30 degC, 20-25 mmHg at 35 degC | larvae to 250 g adults, 25/30/35 degC | Burggren et al. 2019, J. Fish Biol. 94:732-744, https://doi.org/10.1111/jfb.13945 (PubMed 30847924) — VERIFIED |
| Rohu (Labeo rohita, early fry 0.1 g) | oxygen consumption 110.75, 126.57, 146.22, 166.47 mg O2/kg/h at 28, 30, 32, 34 degC; Q10 = 1.94 (28-30), 2.05 (30-32), 1.91 (32-34 degC); best growth 30-32 degC, lowest FCR at 30 degC; CTmax 42.9-45.4 degC | 40-day acclimation, 3 replicates | Brahmane et al. 2014, Afr. J. Agric. Res., https://doi.org/10.5897/ajar2013.7299 — VERIFIED 2026-09-21 (abstract) |
| Rohu and common carp fingerlings | acclimation at three temperatures, oxygen consumption measured | — | Chatterjee et al. 2004, J. Thermal Biol. 29:265-270, https://doi.org/10.1016/j.jtherbio.2004.05.001 — exists, abstract NOT retrievable (publisher-withheld); numbers NOT_FOUND |
| Common carp | Q10 of cardiac output 1.7 and heart rate 2.6 between 6 and 15 degC (normoxia); not an O2-consumption Q10 | cold-acclimated fish | Stecyk & Farrell 2002, J. Exp. Biol. 205:759-768, https://doi.org/10.1242/jeb.205.6.759 — VERIFIED; use only as a plausibility check |
| Litopenaeus vannamei | standard metabolic rate measured at 15, 20, 25, 30 degC and 10, 20, 30 ppt; "optimal temperature range ... is the 25-30 degC range, where a decrease in standard metabolism is determined with increasing temperature"; CTmin-CTmax 7.2-41.9 degC; salinity has a large effect on SMR | juveniles | Kir et al. 2023, J. Thermal Biol. 112:103429, https://doi.org/10.1016/j.jtherbio.2022.103429 (PubMed 36796886) — VERIFIED (abstract; no Q10 number given) |
| L. vannamei juveniles 2, 6, 12 g | specific oxygen consumption (mg O2/g/h) rises with temperature 20 -> 25 -> 30 degC and is disturbed by salinity extremes; regression equations provided for aeration design | 20/25/30 degC x 1/13/25/37 ppt | Bett & Vinatea 2009, Braz. J. Oceanogr. 57(4):305-314, https://doi.org/10.1590/s1679-87592009000400005 — VERIFIED (abstract; coefficients not in abstract) |
| L. vannamei postlarvae | maximum consumption 14.36 ug O2/L/h per PL at 35 degC and 25 psu, minimum 0.07 at 20 degC and 5 psu; optimum 25-30 degC and 15-25 psu | 15-35 degC x 5-45 psu | Pina-Valdez et al. 2015, Bol. Inst. Pesca 41(1):89-101 — VERIFIED (abstract); also Villarreal, Hinojosa & Naranjo 1994, Comp. Biochem. Physiol. 108A:331-336, https://doi.org/10.1016/0300-9629(94)90103-1 (abstract not retrievable) |
| L. vannamei adults | "Q10 0.62 between 20 and 30 degC, 2.5 between 30 and 35 degC, 1.88 over the full range" | acclimation study | attributed by a search summary to Gonzalez et al. 2010 (J. Thermal Biol. 35:218-224) — SNIPPET, NOT_VERIFIED; do not cite |

Model form (ASSUMED): R_fish(t) = R_ref * Q10^((t - t_ref)/10) with t_ref = 30 degC and R_ref from the species'
routine rate; cap the temperature term at the species' upper optimum (tilapia 32 degC, vannamei 30 degC) and add a
stress penalty beyond CTmax minus 5 degC. Magnitudes: tilapia SMR at 30-32 degC is about 170-200 mg O2/kg/h
(interpolated from Leonard & Skov's 79.8-255.1 range, COMPUTED); routine fed rates are typically 2-3 x SMR (ASSUMED).

## (c) Dissolved oxygen versus feed intake and growth

**Verdict: growth and feeding are unaffected above about 3 mg/L (roughly 40-50 % saturation at 28-32 degC) for
tilapia and channel catfish; large tilapia keep gaining feed intake up to about 5.5 mg/L; shrimp survival and
FCR improve up to about 4 mg/L minimum, but a 2024 pond trial found no yield benefit from aerating above a 2.5 mg/L
set-point. Carp have no usable published curve.**

### Nile tilapia
- Tsadik & Kutty 1987 (FAO/ARAC, https://www.fao.org/4/ac168e/ac168e00.htm) — VERIFIED 2026-09-21: at 28 degC,
  reducing DO from about 90 % to about 20 % air saturation (7 to 1.5 mg/L) cut food consumed by 40 % and assimilated
  by 60 %; relative growth rate 0.032-0.034 (high DO, 7 mg/L), 0.014 (medium, 3.4 mg/L), 0.004-0.006 (low, 1.1-1.3
  mg/L); FCR 1.45-1.52, 2.35 and 4.53-6.75 respectively; the authors put the threshold for "considerable production
  reduction" at about 50 % air saturation, i.e. 3.5-4.0 mg/L at 28 degC.
- Tran-Duy, Schrama, van Dam & Verreth 2008, Aquaculture 275:152-162,
  https://doi.org/10.1016/j.aquaculture.2007.12.024 — VERIFIED (abstract): fish of 21 g and 147 g at 3.0 versus
  5.6 mg/L; feed intake and growth significantly higher at 5.6 mg/L (P < 0.01); effect larger in big fish (gill-area
  allometry).
- Tran-Duy, van Dam & Schrama 2011, Aquaculture Research, https://doi.org/10.1111/j.1365-2109.2011.02882.x —
  VERIFIED (abstract): feed intake of fish < 100 g levels off at DO 3 mg/L; for fish > 200 g intake kept rising from
  2.6 to 6.0 mg/L, incipient DO about 5.5 mg/L.
- Boyd & Hanson 2010, Global Seafood Advocate
  (https://www.globalseafood.org/advocate/dissolved-oxygen-concentrations-pond-aquaculture/) — VERIFIED: "at
  concentrations below 50 percent of saturation, growth rates declined and became progressively less as the
  minimum dissolved-oxygen concentrations decreased"; 50 % saturation is about 4 mg/L at 26 degC; tilapia ponds
  aerated to 10 % and 30 % saturation gave larger fish and higher production than unaerated ponds, without a clear
  survival difference; "the response of culture species appears to be affected primarily by the lowest dissolved
  oxygen concentration during the night".

### Channel catfish (classic pond reference)
- Torrans 2008, N. Am. J. Aquacult. 70:371-381, https://doi.org/10.1577/A07-102.1, summarised by the author in
  Global Seafood Advocate, 1 Jan 2011
  (https://www.globalseafood.org/advocate/oxygen-management-improves-channel-catfish-growth-fcr/) — VERIFIED: with
  minimum morning DO held at 1.6-5.0 mg/L in 0.1-0.4 ha ponds, feed consumption was unaffected until DO fell below
  3.0 mg/L, was 6 % lower with aeration delayed to 2.5 mg/L, and 45 % lower at an average morning minimum of 1.6 mg/L;
  37 g fingerlings reached 0.77 kg in a season at high DO but only 0.54 kg at 1.6 mg/L; FCR showed no relationship
  to DO within 1.6-5.0 mg/L; each extra production year adds 12-24 % mortality at 1-2 %/month.
- Boyd & Hanson 2010 — VERIFIED: 36 % saturation (2.91 mg/L) and 60 % (4.85 mg/L) fish consumed and grew less than
  at 100 %; Auburn ponds did better in survival, production and FCR "where average minimum daily oxygen
  concentrations did not fall below 3.5 mg/L"; USDA work found FCR unaffected by minima as low as 2 mg/L but "fish
  ate more and grew better in ponds where dissolved oxygen levels did not fall below 3 mg/L".
- Boyd 2001, Global Seafood Advocate (https://www.globalseafood.org/advocate/water-quality-standards-dissolved-oxygen/)
  — VERIFIED: < 0.5 mg/L small fish survive only brief exposure; 0.5-1.5 mg/L most species die in hours to days;
  1.5-5.0 mg/L stress, disease susceptibility and slow growth; > 5 mg/L desirable; GAA standard minimum 3 mg/L, target
  4 mg/L. Boyd 2018: "concentrations below 1.0-1.5 mg/L for a few hours can kill warmwater animals"; below 3 mg/L
  stresses shrimp and warm-water fish.

### Litopenaeus vannamei
- Seidman & Lawrence 1985 (J. World Maricult. Soc. 16:333-346): growth of P. vannamei and P. monodon "significantly
  reduced" below 2 mg/L; feeding and moult frequency also affected; critical respiratory level 1.17-1.91 mg/L for
  0.06 g postlarvae — SNIPPET (cited through later papers; original not retrieved).
- Boyd & Hanson 2010 penaeid pond data — VERIFIED: minimum DO 2.32 / 2.96 / 3.89 mg/L gave survival 42 / 55 / 61 %,
  production 2,976 / 3,631 / 3,975 kg/ha and FCR 2.64 / 2.21 / 1.96.
- Araujo et al. 2024, Aquaculture, https://doi.org/10.1016/j.aquaculture.2024.741376 — VERIFIED (abstract): 16 earthen
  ponds of 0.1 ha, 25 shrimp/m2, 79-81 days, automatic aeration set-points 2.5, 3.5 and 4.5 mg/L (6/5/5 ponds): no
  significant difference in growth, feed input or productivity (final weight 33.3-33.6 g, yields 7,500-8,500 kg/ha);
  higher set-points cost significantly more electricity "with no discernible benefit". This is the key sceptical
  datum: above a 2.5 mg/L floor, extra oxygen bought no yield in that system.
- TNAU/NABARD 2015 model: "dissolved oxygen levels above 4.5 ppm are required for optimal growth" — VERIFIED as a
  statement, no data behind it.
- Kuruma shrimp (P. japonicus) in RAS at 15.0 versus 7.5 mg/L (oxygen nano-bubbles): SGR, FCR, moult rate and
  survival "significantly improved" — Chen et al. 2025 (see (e)); effect sizes not in the abstract.

### Common carp and Indian major carps
- Quantitative DO-growth or DO-feed-intake curves for Cyprinus carpio, Labeo rohita or Catla catla: NOT_FOUND
  2026-09-21 (PubMed, OpenAlex, Semantic Scholar searches). Available evidence: Verma et al. 2024, Fish Physiol.
  Biochem. 50:1171-1187, https://doi.org/10.1007/s10695-024-01329-2 — VERIFIED (abstract): rohu held 30 days at
  3-4 ppm (versus > 5 ppm) showed impaired haematology and gill, liver, kidney and brain histopathology; common carp
  survive 1.5-1.8 mg/L for days by switching to protein catabolism (Comp. Biochem. Physiol. A 2014, SNIPPET).
  Indian carp culture guidance simply states DO "should ideally be about 5 mg/L" (SNIPPET). For the calculator, apply
  the tilapia curve to carps as a proxy (ASSUMED) and flag it.

### Suggested response function (ASSUMED 2026-09-21, fitted to the numbers above)
Let D = pre-dawn minimum DO (mg/L) at the pond temperature. Feed-intake multiplier f(D):
f = 1.00 for D >= 3.0 (tilapia < 100 g, catfish, carp proxy); f = 0.94 at 2.5; f = 0.55 at 1.6; f = 0.4-0.6 at 1.3-1.5
(Tsadik & Kutty); f = 0 below 1.0 with mortality risk. For tilapia > 200 g raise the plateau to 5.5 mg/L with a
linear ramp from 2.6 mg/L (Tran-Duy 2011). For vannamei: survival and FCR penalties below about 3.9 mg/L (Boyd &
Hanson table) but no growth gain above 2.5-3.5 mg/L set-points (Araujo 2024); the calculator should therefore price
the survival/FCR effect, not a growth bonus, when comparing aeration options.

## (d) Night-time DO decline in earthen ponds

**Verdict: pre-dawn DO = dusk DO minus overnight respiration of plankton, fish and sediment, plus a small
diffusion term; plankton respiration is 75-80 % of the loss in fertilised ponds. Typical total loss is 0.3-1.2
mg/L per hour, so a pond supersaturated at dusk in May can reach 2-3 mg/L by 05:00.**

Boyd's prediction method — the reference formulation:
- Boyd, Romaire & Johnston 1978, *Predicting early morning dissolved oxygen concentrations in channel catfish ponds*,
  Trans. Am. Fish. Soc. 107(3):484-492, https://doi.org/10.1577/1548-8659(1978)107<484:PEMDOC>2.0.CO;2 — abstract
  page returned 403 on 2026-09-21; content VERIFIED via the indexed abstract text: the night-time model sums plankton
  respiration, fish respiration, mud respiration and O2 diffusion; "consumption of O2 by planktonic communities ...
  could be predicted from chemical oxygen demand (COD) and temperature, and ... Secchi disk visibility could be used
  to estimate these parameters". The graphical version reads the expected dawn DO from Secchi depth, temperature, fish
  biomass and % saturation at dusk.
- Romaire, Boyd & Collis 1978, *Predicting nighttime dissolved oxygen decline in ponds used for tilapia culture*,
  Trans. Am. Fish. Soc. 107(6):804-808, https://doi.org/10.1577/1548-8659(1978)107<804:PNDODI>2.0.CO;2 — same access
  status; indexed abstract: plankton respiration averaged 75 % (unmanured) and 80 % (manured) of total night DO loss;
  model average absolute deviation 0.49 and 0.38 mg/L.

Magnitudes:
- Boyd 2018, *Dissolved oxygen dynamics*, Global Seafood Advocate
  (https://www.globalseafood.org/advocate/dissolved-oxygen-dynamics/) — VERIFIED: night budget for an intensive US
  channel-catfish pond: fish respiration 60, water-column respiration 120, sediment respiration 42 kg O2/ha/night,
  mechanical aeration 112 kg O2/ha/night; "daily oxygen consumption by sediment may range from less than 1 mg/L to as
  much as 10 mg/L"; diffusion from air "seldom exceeds 1 mg/L during a single night". COMPUTED conversion at 1.2 m
  depth: 60 / 120 / 42 kg/ha/night = 5.0 / 10.0 / 3.5 mg/L per night — those are 15 t/ha catfish ponds; a Tamil
  Nadu carp pond at 3-6 t/ha would carry a proportionally smaller fish term.
- SRAC pond-aeration fact sheet (via The Fish Site, https://thefishsite.com/articles/pond-aeration-1) — VERIFIED:
  "In a typical 15-acre catfish pond, the total oxygen consumed in respiration by fish, plankton and sediment during
  the summer may range from 100 to more than 200 pounds of oxygen per hour" (COMPUTED: 7.5-15 kg O2/ha/h = 0.62-1.25
  mg/L/h at 1.2 m); most of the demand is plankton and sediment, not fish; farmers start aerators at 3-5 mg/L;
  commercial ponds need 500-1,000 aerator-hours per summer; warm cloudy weather can require continuous aeration for
  days.
- Boyd, Torrans & Tucker 2018, J. World Aquacult. Soc. 49:7-70, https://doi.org/10.1111/jwas.12469 — the definitive
  review of DO and aeration in catfish ponds (abstract not retrievable; cite for method).

Model to code (ASSUMED 2026-09-21, structure from Boyd; parameters to be calibrated on Oxyniti logger data):

    DO_dawn = DO_dusk - (R_plankton + R_fish + R_sed) * h_night + D_diff
    R_plankton (mg/L/h) = k_p * Q10p^((t-25)/10), k_p from Secchi depth or chlorophyll (0.1-0.5 mg/L/h at 25 degC)
    R_fish (mg/L/h)     = B (kg/m3) * r_fish(t) (g O2/kg/h) / 1000, r_fish from (b)
    R_sed (mg/L/h)      = k_s / depth_m, k_s 0.02-0.4 g O2/m2/h (Boyd's < 1 to 10 mg/L/day band)
    D_diff (mg/L/night) <= 1 (positive only when DO < saturation)

Worked example (ASSUMED): Tiruchirappalli, May, water 33 degC, DO_sat = 7.19 mg/L (COMPUTED, P = 0.99 atm); dusk at
120 % saturation = 8.6 mg/L; 11-hour night at 0.5 mg/L/h total respiration = 5.5 mg/L loss; dawn = 3.1 mg/L
(43 % saturation) — right at the feeding threshold in (c). The same pond in January (water 25 degC, dusk 9.9 mg/L at
120 %, respiration 0.35 mg/L/h) reaches 6.1 mg/L at dawn. That contrast is the seasonal effect the calculator must
carry.

## (e) Nano-bubble and micro-bubble results in aquaculture — sceptical inventory

**Verdict: the peer-reviewed evidence is small-scale and mostly Indonesian RAS/raceway work with one or three
replicates; effect sizes on yield are large in the shrimp raceway study but come from a single pond pair; the one
well-replicated marine RAS trial found no growth, survival or FCR effect and no DO increase. Vendor pond claims are
unquantified or unreplicated. Do not put a nano-bubble yield uplift into the calculator without Oxyniti's own
paired-pond data.**

| Study | Species / system | Design | Reported effects | Status |
|---|---|---|---|---|
| Rahmawati et al. 2020, Aquaculture and Fisheries, https://doi.org/10.1016/j.aaf.2020.03.005 | L. vannamei, 50 m2 indoor raceway ponds, 81 days, 680 shrimp/m3 | two treatments (nano-bubble vs diffuser) — replicate number not stated in abstract, apparently one pond each | DO significantly higher; total virus-bacteria and FCR lower; survival 95 %; ABW 15.1 +/- 1.8 g; "total harvest and productivity have doubled to 436 kg and 8.7 kg/m3" | peer-reviewed; VERIFIED (abstract); n effectively 1 |
| Mauladani et al. 2020, J. Akuakultur Indonesia 19(1):30-38, https://doi.org/10.19027/jai.19.1.30-38 | L. vannamei, 800 m2 HDPE-lined pond, 400 shrimp/m2, 56 days | nano-bubble vs non-nano-bubble pond | survival "increased to 92 %", harvest 2,255 kg; payback 4 cycles; economics only | peer-reviewed (Indonesian journal); VERIFIED (abstract); n = 1 pond pair; control values not in abstract |
| Galang et al. 2019, IOP Conf. Ser. Earth Environ. Sci. | L. vannamei, nano-bubble vs aerator tanks, 0-30 days | factorial CRD | DO and oxygen-consumption differences (values not in abstract; a secondary summary cites 10.8 mg/L peak vs 4.65 mg/L control, SNIPPET) | conference paper; VERIFIED (abstract exists) |
| Mahasri et al. 2018 (Indonesian conference paper) | Nile tilapia culture media | 2 treatments | DO raised from 6.5 to 25 mg/L in 30 minutes (0.61 ppm/min) | conference paper; VERIFIED (abstract); no growth data |
| Heriyati et al. 2022, Trends in Sciences 19(6):6251, https://doi.org/10.48048/tis.2022.6251 | red tilapia 115 g, RAS, 800 L tanks, 50 fish/tank, 50 days | 3 treatments (micro-bubble, blower, none) x 3 replicates | micro-bubble held DO at 4.28 mg/L, suppressed CO2 and ammonia; "fish biomass was higher ... with a lower FCR"; lower stress indices | peer-reviewed; VERIFIED (abstract); effect sizes not in abstract |
| Chen et al. 2025, Marine Biotechnology 27:92, https://doi.org/10.1007/s10126-025-10464-7 | kuruma shrimp P. japonicus juveniles, two RAS | DO 15.0 +/- 0.5 mg/L (O2 nano-bubbles) vs 7.5 +/- 0.5 mg/L | SGR, FCR, moult rate and survival "significantly improved"; antioxidant enzymes up; no stress-gene response | peer-reviewed; VERIFIED (abstract); hyperoxia study, not aeration-replacement |
| Sean et al. 2025, Fishes 10(11):550, https://doi.org/10.3390/fishes10110550 | Malabar red snapper, barramundi, hybrid tilapia in marine RAS | nano-bubble RAS vs control RAS | "no significant differences in fish growth, survival, or Feed Conversion Ratio"; "air nanobubbles did not significantly increase dissolved oxygen levels"; more nitrifiers, lower nitrite; densities < 20 kg/m3, exchange > 100 %/h | peer-reviewed; VERIFIED (abstract) — the negative result |
| Taukhid et al. 2025, J. Studies Sci. Eng. 5(2):72-97, https://doi.org/10.53898/josse2025534 | L. vannamei super-intensive, 500 ind/m3 | DIYM micro-bubble vs root blower vs combined | growth 0.20 +/- 0.005 g/day and 64 ind/kg in micro-bubble "significantly improved"; DO, survival, FCR not in accessible text | minor journal; VERIFIED (abstract) |
| Hanif et al. 2021, J. Akuakultur Indonesia | hybrid grouper fry in RAS with nano-bubbles, 500-700 fish/m3, 3 replicates | factorial | growth-performance study (values not extracted) | peer-reviewed; VERIFIED (exists) |
| Ferraro, De Guzman & Duran 2026, Springer chapter, https://doi.org/10.1007/978-3-032-11252-1_11 | Nile tilapia, Philippine RAS, Speece-cone nano-bubble | vs conventional aeration | "higher DO levels and larger fish" | book chapter; SNIPPET only (publisher blocked) |
| Senthilkumar, Aravindkrishnan & Jose Nivash 2026, Springer LNME chapter, https://doi.org/10.1007/978-981-96-9646-8_11 | shrimp culture, implementation review | — | not retrievable | SNIPPET only |
| Ozone nano-bubbles (Linh et al. 2022; Huang et al. 2023, Aquaculture 574:739866) | tilapia disease challenge; jade-perch pond water microbiology | — | pathogen/bacterial-load reduction (90-99 %), immune priming; not DO/yield | peer-reviewed; VERIFIED (abstracts); different mechanism |
| Vendor: Moleaer (The Fish Site, 13 Oct 2021; Sea Technology, 7 Oct 2024; moleaer.com case studies) | salmon RAS/hatchery/net pens, Norway and Chile | customer trials, no controls described | "22 % increase in fish biomass" (Canada RAS hatchery); DO +23 %, turbidity -30 %, nitrite -70 % (Lodingen Fisk RAS); 85 % oxygen-transfer efficiency; 50 % energy saving at a Chilean rearing tank | vendor claims; VERIFIED as claims only; no shrimp, tilapia or carp pond cases on the vendor's case-study page |

Reading of the evidence (2026-09-21): (1) where oxygen is genuinely limiting (dense raceways, RAS at 4 mg/L),
bubble aeration that raises DO improves feed intake, FCR and survival exactly as (c) predicts — the benefit is the
DO, not the bubble size; (2) where DO is not limiting the trials show nothing (Sean 2025) and conventional aeration
set-point trials show nothing above 2.5 mg/L (Araujo 2024); (3) no field trial with replicated earthen ponds in
Indian conditions was found (NOT_FOUND). The calculator should therefore model the benefit as the DO-response of
(c) applied to the pond's predicted pre-dawn minimum from (d), and treat any device-specific uplift as ASSUMED
until measured.

---

## `do_verify.py` (the Python used for the tables above; run `python do_verify.py`)

```python
import math
def do_sat_1atm(t_c, sal_ppt=0.0):
    T = t_c + 273.15
    ln_c = (-139.34411 + 1.575701e5 / T - 6.642308e7 / T**2 + 1.243800e10 / T**3 - 8.621949e11 / T**4
            - sal_ppt * (0.017674 - 10.754 / T + 2140.7 / T**2))
    return math.exp(ln_c)                       # mg/L, 1 atm moist air
def theta(t_c):  return 0.000975 - 1.426e-5 * t_c + 6.436e-8 * t_c**2
def vapour_pressure_atm(t_c):
    T = t_c + 273.15
    return math.exp(11.8571 - 3840.70 / T - 216961.0 / T**2)
def pressure_factor(t_c, p_atm):
    u = vapour_pressure_atm(t_c); th = theta(t_c)
    return ((p_atm - u) * (1 - th * p_atm)) / ((1 - u) * (1 - th))
def pressure_from_altitude_atm(alt_m):
    return math.exp(-9.80665 * 0.0289644 * alt_m / (8.31447 * 288.15))
def do_sat(t_c, sal_ppt=0.0, p_atm=1.0):
    return do_sat_1atm(t_c, sal_ppt) * pressure_factor(t_c, p_atm)
for t in [20, 25, 28, 30, 32, 35]:
    print(t, round(do_sat_1atm(t, 0), 3), round(do_sat_1atm(t, 15), 3), round(do_sat_1atm(t, 25), 3))
```
