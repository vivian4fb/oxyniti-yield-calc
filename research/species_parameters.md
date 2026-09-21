# Species parameters for the Oxyniti yield calculator - Tamil Nadu pond aquaculture

*Compiled 2026-09-21. Every figure carries a status (VERIFIED = read on the cited page/PDF; ASSUMED = secondary, converted or derived from a weaker source; NOT_FOUND = no sourced figure - never guessed) and a source key resolved in the Sources section. Ranges are as published; 'n/p' marks an unpublished bound. Conversions: 1 ha = 2.471 acre; 1 t/ha = 404.7 kg/acre. Machine-readable twin: `species_parameters.json`.*

## Coverage

| # | Species | Tamil name (status) | Water | Best TN-specific source |
|---|---|---|---|---|
| 1 | Catla (*Catla catla (syn. Labeo catla / Gibelion catla)*) | கட்லா மீன் (VERIFIED) | freshwater | FAO_TN |
| 2 | Rohu (*Labeo rohita*) | ரோகு மீன் (VERIFIED) | freshwater | FAO_TN |
| 3 | Mrigal (*Cirrhinus mrigala (Cirrhinus cirrhosus)*) | மிர்கல் மீன் (VERIFIED) | freshwater | THANJ |
| 4 | Common carp (*Cyprinus carpio*) | சாதாக்கெண்டை மீன் (VERIFIED) | freshwater | THANJ |
| 5 | Grass carp (*Ctenopharyngodon idella (C. idellus)*) | புல் கெண்டை மீன் (VERIFIED) | freshwater | THANJ |
| 6 | Silver carp (*Hypophthalmichthys molitrix*) | வெள்ளிக்கெண்டை மீன் (VERIFIED) | freshwater | THANJ |
| 7 | GIFT tilapia (all-male Nile tilapia) (*Oreochromis niloticus (GIFT strain)*) | திலாப்பியா / சிலேபி மீன் (ASSUMED) | freshwater | SLBC |
| 8 | Pangasius (striped catfish / sutchi) (*Pangasianodon hypophthalmus (Pangasius sutchi)*) | பங்காஸ் (ASSUMED) | freshwater | NABARD_PANG |
| 9 | Striped murrel / viral meen (*Channa striata*) | விரால் மீன் (VERIFIED) | freshwater | TNAU_MURREL |
| 10 | Giant freshwater prawn / scampi (*Macrobrachium rosenbergii*) | - (NOT_FOUND) | freshwater | TNPRAWN |
| 11 | Pearl spot / karimeen (*Etroplus suratensis*) | முத்துப்புள்ளி மீன் (VERIFIED) | brackish | TNAU_PEARL |
| 12 | Improved strains promoted in TN: Jayanti rohu and Amur carp (*Labeo rohita (CIFA 'Jayanti' selected line); Cyprinus carpio haematopterus / C. rubrofuscus (Amur carp)*) | - (NOT_FOUND) | freshwater | TNPN |
| 13 | Pacific white shrimp (vannamei) (*Litopenaeus (Penaeus) vannamei*) | வெள்ளை இறால் (ASSUMED) | brackish | BENISON |
| 14 | Black tiger shrimp (*Penaeus monodon*) | கருவண்டன் இறால் (ASSUMED) | brackish | MPEDA_CROP |
| 15 | Asian seabass / koduva (*Lates calcarifer*) | கொடுவா மீன் (VERIFIED) | brackish | ICSF_KARAIKAL |
| 16 | Milkfish (*Chanos chanos*) | பாலமீன் (VERIFIED) | brackish | TNAU_MILK |
| 17 | Grey mullet / madavai (*Mugil cephalus*) | சாம்பல் நிற மடவை (VERIFIED) | brackish | MPEDA_MULLET |
| 18 | Mud crab (fattening) (*Scylla serrata (also S. tranquebarica / S. oceanica in TN catches)*) | கழி நண்டு (ASSUMED) | brackish | SCYLLA_IN |


## Catla - *Catla catla (syn. Labeo catla / Gibelion catla)*

- Tamil name: **கட்லா மீன்** (VERIFIED; WIKI_TA)
- Water type: freshwater
- Culture system: earthen pond, semi-intensive carp polyculture (Indian major carps +/- Chinese carps) with manuring and supplementary feed; TN farmers mostly stock the three IMC only
- Notes: Surface zooplankton feeder. Thanjavur 1992-93 stocking share 29 per 100; Chinese carps least preferred in TN. Consumer-preferred size 1-2 kg (FAO).

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 25 to 32 | C | VERIFIED | FAO_CATLA |  |  |
| temp_tolerable_c | 14 to n/p | C | VERIFIED | FAO_CATLA |  | FAO: does not thrive below ~14 C; upper limit not published. |
| temp_growth_stops_below_c | 14 | C | VERIFIED | FAO_CATLA |  | Interpretation of FAO 'does not thrive at temperatures below 14 C'. |
| do_minimum_mg_l | 3.0 to 4.0 | mg/L | ASSUMED | BOYD |  | No carp-specific threshold found. Boyd (2010, channel catfish ponds): growth declined below ~50% saturation (~4 mg/L at 26 C); fish ate and grew better where daily minima stayed above 3-3.5 mg/L. Applied to Indian major carps by analogy. |
| do_preferred_mg_l | 5.0 | mg/L | VERIFIED | IMCREV |  | 'Dissolved oxygen ... should ideally be about 5 mg/L' (IMC review 2024). Kerala PoP 2021 hatchery/spawning: 5-6 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 1619 to 4047 | fingerlings/acre | VERIFIED | FAO_CATLA |  | FAO grow-out polyculture 4,000-10,000 fingerlings/ha (all carps combined). TN: TNAU/NABARD composite 5,000/ha (2,023/acre); TN Dept of Fisheries 2024-25 scale of finance assumes 10,000/ha (4,047/acre); Thanjavur survey 2010 mean 4,670 +/- 2,573/ha, floating-pellet farms 6,929/ha stocking 50-100 g seed; Thanjavur 1992-93 mean 4,172/ha. |
| culture_period_months | 6 to 12 | months | VERIFIED | FAO_TN |  | 6 months for stunted 50-100 g seed to >500 g (Thanjavur floating-pellet farms, FAO 2013); TNAU/NABARD composite culture 10-12 months; FAO 12-18 months to 1-1.5 kg. TN ponds are perennial July-March. |
| harvest_size_g | 500 to 1250 | g | VERIFIED | TNAU_COMP |  | TNAU composite: 750 g-1.25 kg at 1 year; FAO first-year gain 1-1.2 kg; Thanjavur pellet farms harvest >500 g (400-600 g) at ~6 months from stunted seed. |
| survival_pct | 80 | % | VERIFIED | NABARD_INT |  | NABARD 2015 model assumption for 200-250 g stunted fingerlings (6,250/ha). Farm-survey grow-out survival for TN NOT_FOUND. FAO gives nursery 30-50% and fingerling 60-70% only. |
| fcr | 1.11 to 1.96 | kg feed/kg gain | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: floating pellet 1.11:1, mash + sinking pellet 1.26:1, conventional rice-bran/oil-cake mash 1.96:1 (natural food included). Conventional mash elsewhere in India 3:1-4:1. |
| yield_kg_per_acre_per_crop | 1214 to 2024 | kg/acre/yr (whole polyculture) | VERIFIED | FAO_CATLA |  | FAO polyculture 3-5 t/ha/yr; TNAU composite 3-5 t/ha/yr (7-10 t/ha/yr possible); Thanjavur 2010 survey 3,010 (conventional) to 4,596 (floating pellet) kg/ha/yr = 1,218-1,860 kg/acre/yr; NABARD intensive catla+rohu 5 t/ha/crop, 2 crops; Thanjavur 1992-93 mean only 888 kg/ha/crop (359 kg/acre). Species share depends on stocking ratio. |
| crops_per_year_tn | 1 to 2 | crops/yr | VERIFIED | FAO_TN |  | One crop conventionally; floating-pellet farmers stocking stunted seed 'can raise two crops per year' (harvests 'generally twice'). |
| farmgate_price_inr_per_kg | 200 to 250 | INR/kg | VERIFIED | DTNEXT_PRICE | 2026-04-25; unspecified (farmer quote) | Nagapattinam aqua farmer, 25 Apr 2026: rohu/catla/mrigal normally Rs 200-250/kg, expected Rs 350-400/kg during the 2026 shortage; article does not state whether farm-gate or market. National wholesale (commoditymarketlive, Jun 2025): rohu monthly avg Rs 196.83, catla Rs 214.03/kg. Thanjavur 2010 farm price US$1.37-1.56/kg. |
| seed_cost_inr_per_unit | 3.0 | INR/fingerling | VERIFIED | SLBC | 2024-25 | Derived: TN scale of finance 2024-25 budgets seed Rs 30,000 for 10,000 fingerlings/ha = Rs 3.0 each. NABARD 2015: Rs 10-15 for 200-250 g stunted yearlings. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog (Oct 2025) 'floating feed Rs 40 to 70 per kg'; no institutional 2025-26 quote found. Thanjavur 2010: floating pellet US$0.44-0.50/kg, sinking US$0.33-0.39, farm mash US$0.27. |
| feed_share_of_variable_cost_pct | 50 to 75 | % of variable cost | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: feed = 75.0% of variable cost overall (US$2,864.6 of 3,819.1/ha/yr); floating pellet 63.1%, conventional 65.4%. TN scale of finance 2024-25: feed Rs 2.5 lakh of Rs 5.01 lakh working capital/ha = 49.9%. FAO: feed 'over 50 percent of total input cost'. |
| stocking_months_tn | July-August (stocking after pond preparation completed by July/August; ponds perennial July-March) | months | VERIFIED | FAO_TN |  | Thanjavur district survey 2010. Carp seed availability is tied to monsoon breeding; TN off-season breeding makes fingerlings available by March-April (search-level claim, not read). |
| aeration_common | no (unaerated semi-intensive ponds; pumping for water exchange budgeted, aerators not standard) | yes/no | ASSUMED | SLBC |  | No survey statement on aerator use in TN carp ponds was found; TN scale of finance includes an electricity line (Rs 30,000/ha) for pumping. IMC review notes paddlewheel aerators suit 1-1.5 m ponds when intensified. |

## Rohu - *Labeo rohita*

- Tamil name: **ரோகு மீன்** (VERIFIED; WIKI_TA)
- Water type: freshwater
- Culture system: earthen pond, semi-intensive carp polyculture (Indian major carps +/- Chinese carps) with manuring and supplementary feed; TN farmers mostly stock the three IMC only
- Notes: Column omnivore; highest market demand; ~60% of stock in Thanjavur pellet-fed ponds (FAO 2013), 25 per 100 in 1992-93. Jayanti rohu (CIFA selected line) is promoted by TN Fisheries (see improved-strains row). FAO producer price <US$1/kg (2010).

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 22 to 31 | C | VERIFIED | FAO_ROHU |  | FAO gives 22-31 C as the optimal (spawning) range; a separate grow-out optimum is not published. |
| temp_tolerable_c | 14 to n/p | C | VERIFIED | FAO_ROHU |  | FAO: 'does not thrive at temperatures below 14 C'; upper limit not published. |
| temp_growth_stops_below_c | 14 | C | VERIFIED | FAO_ROHU |  | Interpretation of FAO 'does not thrive below 14 C'. |
| do_minimum_mg_l | 3.0 to 4.0 | mg/L | ASSUMED | BOYD |  | No carp-specific threshold found. Boyd (2010, channel catfish ponds): growth declined below ~50% saturation (~4 mg/L at 26 C); fish ate and grew better where daily minima stayed above 3-3.5 mg/L. Applied to Indian major carps by analogy. |
| do_preferred_mg_l | 5.0 | mg/L | VERIFIED | IMCREV |  | 'Dissolved oxygen ... should ideally be about 5 mg/L' (IMC review 2024). Kerala PoP 2021 hatchery/spawning: 5-6 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 1619 to 4047 | fingerlings/acre | VERIFIED | FAO_CATLA |  | FAO grow-out polyculture 4,000-10,000 fingerlings/ha (all carps combined). TN: TNAU/NABARD composite 5,000/ha (2,023/acre); TN Dept of Fisheries 2024-25 scale of finance assumes 10,000/ha (4,047/acre); Thanjavur survey 2010 mean 4,670 +/- 2,573/ha, floating-pellet farms 6,929/ha stocking 50-100 g seed; Thanjavur 1992-93 mean 4,172/ha. |
| culture_period_months | 6 to 12 | months | VERIFIED | FAO_TN |  | 6 months for stunted 50-100 g seed to >500 g (Thanjavur floating-pellet farms, FAO 2013); TNAU/NABARD composite culture 10-12 months; FAO 12-18 months to 1-1.5 kg. TN ponds are perennial July-March. |
| harvest_size_g | 500 to 1500 | g | VERIFIED | FAO_ROHU |  | FAO 700-800 g in one year, 1-1.5 kg in 12-18 months; Thanjavur pellet farms >500 g at ~6 months from 50-100 g stunted seed. |
| survival_pct | 80 | % | VERIFIED | NABARD_INT |  | NABARD 2015 model assumption for 200-250 g stunted fingerlings (6,250/ha). Farm-survey grow-out survival for TN NOT_FOUND. FAO gives nursery 30-50% and fingerling 60-70% only. |
| fcr | 1.11 to 1.96 | kg feed/kg gain | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: floating pellet 1.11:1, mash + sinking pellet 1.26:1, conventional rice-bran/oil-cake mash 1.96:1 (natural food included). Conventional mash elsewhere in India 3:1-4:1. |
| yield_kg_per_acre_per_crop | 1214 to 2024 | kg/acre/yr (whole polyculture) | VERIFIED | FAO_ROHU |  | FAO: 1-2 t/ha/yr extensive, 3-5 t/ha/yr scientific polyculture, 6-8 t/ha two-species (Kolleru); TN survey 3,010-4,596 kg/ha/yr (1,218-1,860 kg/acre/yr). |
| crops_per_year_tn | 1 to 2 | crops/yr | VERIFIED | FAO_TN |  | One crop conventionally; floating-pellet farmers stocking stunted seed 'can raise two crops per year' (harvests 'generally twice'). |
| farmgate_price_inr_per_kg | 200 to 250 | INR/kg | VERIFIED | DTNEXT_PRICE | 2026-04-25; unspecified (farmer quote) | Nagapattinam aqua farmer, 25 Apr 2026: rohu/catla/mrigal normally Rs 200-250/kg, expected Rs 350-400/kg during the 2026 shortage; article does not state whether farm-gate or market. National wholesale (commoditymarketlive, Jun 2025): rohu monthly avg Rs 196.83, catla Rs 214.03/kg. Thanjavur 2010 farm price US$1.37-1.56/kg. |
| seed_cost_inr_per_unit | 3.0 | INR/fingerling | VERIFIED | SLBC | 2024-25 | Derived: TN scale of finance 2024-25 budgets seed Rs 30,000 for 10,000 fingerlings/ha = Rs 3.0 each. NABARD 2015: Rs 10-15 for 200-250 g stunted yearlings. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog (Oct 2025) 'floating feed Rs 40 to 70 per kg'; no institutional 2025-26 quote found. Thanjavur 2010: floating pellet US$0.44-0.50/kg, sinking US$0.33-0.39, farm mash US$0.27. |
| feed_share_of_variable_cost_pct | 50 to 75 | % of variable cost | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: feed = 75.0% of variable cost overall (US$2,864.6 of 3,819.1/ha/yr); floating pellet 63.1%, conventional 65.4%. TN scale of finance 2024-25: feed Rs 2.5 lakh of Rs 5.01 lakh working capital/ha = 49.9%. FAO: feed 'over 50 percent of total input cost'. |
| stocking_months_tn | July-August (stocking after pond preparation completed by July/August; ponds perennial July-March) | months | VERIFIED | FAO_TN |  | Thanjavur district survey 2010. Carp seed availability is tied to monsoon breeding; TN off-season breeding makes fingerlings available by March-April (search-level claim, not read). |
| aeration_common | no (unaerated semi-intensive ponds; pumping for water exchange budgeted, aerators not standard) | yes/no | ASSUMED | SLBC |  | No survey statement on aerator use in TN carp ponds was found; TN scale of finance includes an electricity line (Rs 30,000/ha) for pumping. IMC review notes paddlewheel aerators suit 1-1.5 m ponds when intensified. |

## Mrigal - *Cirrhinus mrigala (Cirrhinus cirrhosus)*

- Tamil name: **மிர்கல் மீன்** (VERIFIED; WIKI_TA)
- Water type: freshwater
- Culture system: earthen pond, semi-intensive carp polyculture (Indian major carps +/- Chinese carps) with manuring and supplementary feed; TN farmers mostly stock the three IMC only
- Notes: Bottom detritivore; 20-25% of polyculture output (FAO); 21 per 100 stocked in Thanjavur 1992-93. Fetches 10-20% less than rohu/catla (FAO).

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 24 to 31 | C | VERIFIED | FAO_MRIGAL |  | FAO breeding range 24-31 C; grow-out optimum not published. |
| temp_tolerable_c | 14 to n/p | C | VERIFIED | FAO_MRIGAL |  | Minimum tolerance ~14 C; upper limit not published. |
| temp_growth_stops_below_c | 14 | C | VERIFIED | FAO_MRIGAL |  | Interpretation of FAO minimum tolerance 14 C. |
| do_minimum_mg_l | 3.0 to 4.0 | mg/L | ASSUMED | BOYD |  | No carp-specific threshold found. Boyd (2010, channel catfish ponds): growth declined below ~50% saturation (~4 mg/L at 26 C); fish ate and grew better where daily minima stayed above 3-3.5 mg/L. Applied to Indian major carps by analogy. |
| do_preferred_mg_l | 5.0 | mg/L | VERIFIED | IMCREV |  | 'Dissolved oxygen ... should ideally be about 5 mg/L' (IMC review 2024). Kerala PoP 2021 hatchery/spawning: 5-6 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 1619 to 4047 | fingerlings/acre | VERIFIED | FAO_CATLA |  | FAO grow-out polyculture 4,000-10,000 fingerlings/ha (all carps combined). TN: TNAU/NABARD composite 5,000/ha (2,023/acre); TN Dept of Fisheries 2024-25 scale of finance assumes 10,000/ha (4,047/acre); Thanjavur survey 2010 mean 4,670 +/- 2,573/ha, floating-pellet farms 6,929/ha stocking 50-100 g seed; Thanjavur 1992-93 mean 4,172/ha. |
| culture_period_months | 6 to 12 | months | VERIFIED | FAO_TN |  | 6 months for stunted 50-100 g seed to >500 g (Thanjavur floating-pellet farms, FAO 2013); TNAU/NABARD composite culture 10-12 months; FAO 12-18 months to 1-1.5 kg. TN ponds are perennial July-March. |
| harvest_size_g | 600 to 700 | g | VERIFIED | FAO_MRIGAL |  | First-year weight gain 600-700 g (FAO). |
| survival_pct | 80 | % | VERIFIED | NABARD_INT |  | NABARD 2015 model assumption for 200-250 g stunted fingerlings (6,250/ha). Farm-survey grow-out survival for TN NOT_FOUND. FAO gives nursery 30-50% and fingerling 60-70% only. |
| fcr | 1.11 to 1.96 | kg feed/kg gain | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: floating pellet 1.11:1, mash + sinking pellet 1.26:1, conventional rice-bran/oil-cake mash 1.96:1 (natural food included). Conventional mash elsewhere in India 3:1-4:1. |
| yield_kg_per_acre_per_crop | 1214 to 2024 | kg/acre/yr (whole polyculture) | VERIFIED | FAO_CATLA |  | FAO polyculture 3-5 t/ha/yr; TNAU composite 3-5 t/ha/yr (7-10 t/ha/yr possible); Thanjavur 2010 survey 3,010 (conventional) to 4,596 (floating pellet) kg/ha/yr = 1,218-1,860 kg/acre/yr; NABARD intensive catla+rohu 5 t/ha/crop, 2 crops; Thanjavur 1992-93 mean only 888 kg/ha/crop (359 kg/acre). Species share depends on stocking ratio. |
| crops_per_year_tn | 1 to 2 | crops/yr | VERIFIED | FAO_TN |  | One crop conventionally; floating-pellet farmers stocking stunted seed 'can raise two crops per year' (harvests 'generally twice'). |
| farmgate_price_inr_per_kg | 200 to 250 | INR/kg | VERIFIED | DTNEXT_PRICE | 2026-04-25; unspecified (farmer quote) | Quoted jointly with rohu and catla (Nagapattinam, Apr 2026: normal Rs 200-250, shortage Rs 350-400). FAO: mrigal sells 10-20% below rohu/catla. |
| seed_cost_inr_per_unit | 3.0 | INR/fingerling | VERIFIED | SLBC | 2024-25 | Derived: TN scale of finance 2024-25 budgets seed Rs 30,000 for 10,000 fingerlings/ha = Rs 3.0 each. NABARD 2015: Rs 10-15 for 200-250 g stunted yearlings. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog (Oct 2025) 'floating feed Rs 40 to 70 per kg'; no institutional 2025-26 quote found. Thanjavur 2010: floating pellet US$0.44-0.50/kg, sinking US$0.33-0.39, farm mash US$0.27. |
| feed_share_of_variable_cost_pct | 50 to 75 | % of variable cost | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: feed = 75.0% of variable cost overall (US$2,864.6 of 3,819.1/ha/yr); floating pellet 63.1%, conventional 65.4%. TN scale of finance 2024-25: feed Rs 2.5 lakh of Rs 5.01 lakh working capital/ha = 49.9%. FAO: feed 'over 50 percent of total input cost'. |
| stocking_months_tn | July-August (stocking after pond preparation completed by July/August; ponds perennial July-March) | months | VERIFIED | FAO_TN |  | Thanjavur district survey 2010. Carp seed availability is tied to monsoon breeding; TN off-season breeding makes fingerlings available by March-April (search-level claim, not read). |
| aeration_common | no (unaerated semi-intensive ponds; pumping for water exchange budgeted, aerators not standard) | yes/no | ASSUMED | SLBC |  | No survey statement on aerator use in TN carp ponds was found; TN scale of finance includes an electricity line (Rs 30,000/ha) for pumping. IMC review notes paddlewheel aerators suit 1-1.5 m ponds when intensified. |

## Common carp - *Cyprinus carpio*

- Tamil name: **சாதாக்கெண்டை மீன்** (VERIFIED; WIKI_TA)
- Water type: freshwater
- Culture system: earthen pond, semi-intensive carp polyculture (Indian major carps +/- Chinese carps) with manuring and supplementary feed; TN farmers mostly stock the three IMC only
- Notes: Bottom omnivore; 14 per 100 stocked in Thanjavur 1992-93; listed among species cultured in the Cauvery delta (DT Next 2025). TN-specific price NOT_FOUND.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 23 to 30 | C | VERIFIED | FAO_CC |  |  |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  | FAO sheet gives no tolerable range; tolerates salinity to ~5 ppt and pH 6.5-9. |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 3.0 to 4.0 | mg/L | ASSUMED | BOYD |  | Warmwater-fish analogy (Boyd 2010); species-specific growth threshold not found. |
| do_preferred_mg_l | 5.0 | mg/L | VERIFIED | IMCREV |  | 'Dissolved oxygen ... should ideally be about 5 mg/L' (IMC review 2024). Kerala PoP 2021 hatchery/spawning: 5-6 ppm. |
| do_lethal_mg_l | 0.3 to 0.5 | mg/L | VERIFIED | FAO_CC |  | FAO: 'can survive in 0.3-0.5 mg/litre' - survival floor, i.e. lethal only below this. |
| stocking_density_per_acre | 1619 to 2428 | fish/acre | VERIFIED | FAO_CC |  | FAO 4,000-6,000/ha for two-summer-old production (up to 20,000/ha with pellets). In TN it is a minor component of the IMC polyculture (see catla row for total densities). |
| culture_period_months | 6 to 12 | months | VERIFIED | FAO_TN |  | 6 months for stunted 50-100 g seed to >500 g (Thanjavur floating-pellet farms, FAO 2013); TNAU/NABARD composite culture 10-12 months; FAO 12-18 months to 1-1.5 kg. TN ponds are perennial July-March. |
| harvest_size_g | 600 to 1000 | g | VERIFIED | FAO_CC |  | '0.6 to 1.0 kg body weight' in a single season in sub-tropical/tropical conditions. |
| survival_pct | 80 | % | VERIFIED | NABARD_INT |  | NABARD 2015 model assumption for 200-250 g stunted fingerlings (6,250/ha). Farm-survey grow-out survival for TN NOT_FOUND. FAO gives nursery 30-50% and fingerling 60-70% only. |
| fcr | NOT_FOUND | kg feed/kg gain | NOT_FOUND | - |  | FAO sheet gives feeding rate (3-5% BW/day) but no FCR. |
| yield_kg_per_acre_per_crop | 1214 to 2024 | kg/acre/yr (whole polyculture) | VERIFIED | FAO_CATLA |  | FAO polyculture 3-5 t/ha/yr; TNAU composite 3-5 t/ha/yr (7-10 t/ha/yr possible); Thanjavur 2010 survey 3,010 (conventional) to 4,596 (floating pellet) kg/ha/yr = 1,218-1,860 kg/acre/yr; NABARD intensive catla+rohu 5 t/ha/crop, 2 crops; Thanjavur 1992-93 mean only 888 kg/ha/crop (359 kg/acre). Species share depends on stocking ratio. |
| crops_per_year_tn | 1 to 2 | crops/yr | VERIFIED | FAO_TN |  | One crop conventionally; floating-pellet farmers stocking stunted seed 'can raise two crops per year' (harvests 'generally twice'). |
| farmgate_price_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | No Tamil Nadu or South India quote for common carp found; FAO global average producer price US$0.92/kg (2002). |
| seed_cost_inr_per_unit | 3.0 | INR/fingerling | VERIFIED | SLBC | 2024-25 | Derived: TN scale of finance 2024-25 budgets seed Rs 30,000 for 10,000 fingerlings/ha = Rs 3.0 each. NABARD 2015: Rs 10-15 for 200-250 g stunted yearlings. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog (Oct 2025) 'floating feed Rs 40 to 70 per kg'; no institutional 2025-26 quote found. Thanjavur 2010: floating pellet US$0.44-0.50/kg, sinking US$0.33-0.39, farm mash US$0.27. |
| feed_share_of_variable_cost_pct | 50 to 75 | % of variable cost | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: feed = 75.0% of variable cost overall (US$2,864.6 of 3,819.1/ha/yr); floating pellet 63.1%, conventional 65.4%. TN scale of finance 2024-25: feed Rs 2.5 lakh of Rs 5.01 lakh working capital/ha = 49.9%. FAO: feed 'over 50 percent of total input cost'. |
| stocking_months_tn | July-August (stocking after pond preparation completed by July/August; ponds perennial July-March) | months | VERIFIED | FAO_TN |  | Thanjavur district survey 2010. Carp seed availability is tied to monsoon breeding; TN off-season breeding makes fingerlings available by March-April (search-level claim, not read). |
| aeration_common | no (unaerated semi-intensive ponds; pumping for water exchange budgeted, aerators not standard) | yes/no | ASSUMED | SLBC |  | No survey statement on aerator use in TN carp ponds was found; TN scale of finance includes an electricity line (Rs 30,000/ha) for pumping. IMC review notes paddlewheel aerators suit 1-1.5 m ponds when intensified. |

## Grass carp - *Ctenopharyngodon idella (C. idellus)*

- Tamil name: **புல் கெண்டை மீன்** (VERIFIED; WIKI_TA)
- Water type: freshwater
- Culture system: earthen pond, semi-intensive carp polyculture (Indian major carps +/- Chinese carps) with manuring and supplementary feed; TN farmers mostly stock the three IMC only
- Notes: Macrophyte feeder; 4 per 100 stocked in Thanjavur 1992-93; DT Next (Aug 2025) reports Chinese carp reaching 2 kg/yr in delta ponds. Temperature, DO and TN price not found.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 3.0 to 4.0 | mg/L | ASSUMED | BOYD |  | Warmwater-fish analogy (Boyd 2010). |
| do_preferred_mg_l | 5.0 | mg/L | VERIFIED | IMCREV |  | 'Dissolved oxygen ... should ideally be about 5 mg/L' (IMC review 2024). Kerala PoP 2021 hatchery/spawning: 5-6 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 304 to 1214 | fish/acre | VERIFIED | FAO_GC |  | FAO grow-out polyculture 750-3,000/ha. |
| culture_period_months | 6 to 12 | months | VERIFIED | FAO_TN |  | 6 months for stunted 50-100 g seed to >500 g (Thanjavur floating-pellet farms, FAO 2013); TNAU/NABARD composite culture 10-12 months; FAO 12-18 months to 1-1.5 kg. TN ponds are perennial July-March. |
| harvest_size_g | 1000 to 1500 | g | VERIFIED | FAO_GC |  | Marketed at 1-1.5 kg from ponds (Vietnam); grow-out target >1.5 kg. |
| survival_pct | NOT_FOUND | % | NOT_FOUND | - |  | FAO gives nursery (70-90%) and fingerling (>95%) survival only. |
| fcr | 2.0 to n/p | kg feed/kg gain | VERIFIED | FAO_GC |  | 'FCR is high (usually >2:1)' on formulated feed; grass-fed FCR far higher. |
| yield_kg_per_acre_per_crop | 405 to 1214 | kg/acre/yr | VERIFIED | FAO_GC |  | Pond yield 1,000-3,000 kg/ha where grass carp is the main species. |
| crops_per_year_tn | 1 to 2 | crops/yr | VERIFIED | FAO_TN |  | One crop conventionally; floating-pellet farmers stocking stunted seed 'can raise two crops per year' (harvests 'generally twice'). |
| farmgate_price_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | No TN or South India quote found; FAO retail US$0.7-1.0/kg, production cost US$0.50/kg (2010). |
| seed_cost_inr_per_unit | 3.0 | INR/fingerling | VERIFIED | SLBC | 2024-25 | Derived: TN scale of finance 2024-25 budgets seed Rs 30,000 for 10,000 fingerlings/ha = Rs 3.0 each. NABARD 2015: Rs 10-15 for 200-250 g stunted yearlings. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog (Oct 2025) 'floating feed Rs 40 to 70 per kg'; no institutional 2025-26 quote found. Thanjavur 2010: floating pellet US$0.44-0.50/kg, sinking US$0.33-0.39, farm mash US$0.27. |
| feed_share_of_variable_cost_pct | 50 to 75 | % of variable cost | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: feed = 75.0% of variable cost overall (US$2,864.6 of 3,819.1/ha/yr); floating pellet 63.1%, conventional 65.4%. TN scale of finance 2024-25: feed Rs 2.5 lakh of Rs 5.01 lakh working capital/ha = 49.9%. FAO: feed 'over 50 percent of total input cost'. |
| stocking_months_tn | July-August (stocking after pond preparation completed by July/August; ponds perennial July-March) | months | VERIFIED | FAO_TN |  | Thanjavur district survey 2010. Carp seed availability is tied to monsoon breeding; TN off-season breeding makes fingerlings available by March-April (search-level claim, not read). |
| aeration_common | no (unaerated semi-intensive ponds; pumping for water exchange budgeted, aerators not standard) | yes/no | ASSUMED | SLBC |  | No survey statement on aerator use in TN carp ponds was found; TN scale of finance includes an electricity line (Rs 30,000/ha) for pumping. IMC review notes paddlewheel aerators suit 1-1.5 m ponds when intensified. |

## Silver carp - *Hypophthalmichthys molitrix*

- Tamil name: **வெள்ளிக்கெண்டை மீன்** (VERIFIED; WIKI_TA)
- Water type: freshwater
- Culture system: earthen pond, semi-intensive carp polyculture (Indian major carps +/- Chinese carps) with manuring and supplementary feed; TN farmers mostly stock the three IMC only
- Notes: Phytoplankton filter feeder. Least preferred in TN: only 7 per 100 stocked (vs 20-30% recommended) because of low consumer price and handling mortality (Thanjavur 1992-93; FAO 2013).

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 22 to 28 | C | VERIFIED | FAO_SC |  | FAO optimal 22-28 C (spawning/hatching context); embryonic abnormalities below 17 C or above 31 C. |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 3.0 to 4.0 | mg/L | ASSUMED | BOYD |  | Warmwater-fish analogy (Boyd 2010). |
| do_preferred_mg_l | 5.0 | mg/L | VERIFIED | IMCREV |  | 'Dissolved oxygen ... should ideally be about 5 mg/L' (IMC review 2024). Kerala PoP 2021 hatchery/spawning: 5-6 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | NOT_FOUND | fish/acre | NOT_FOUND | - |  | FAO gives nursery/broodstock densities only; TN share of polyculture 7 per 100. |
| culture_period_months | 6 to 12 | months | VERIFIED | FAO_TN |  | 6 months for stunted 50-100 g seed to >500 g (Thanjavur floating-pellet farms, FAO 2013); TNAU/NABARD composite culture 10-12 months; FAO 12-18 months to 1-1.5 kg. TN ponds are perennial July-March. |
| harvest_size_g | NOT_FOUND | g | NOT_FOUND | - |  |  |
| survival_pct | NOT_FOUND | % | NOT_FOUND | - |  |  |
| fcr | NOT_FOUND | kg feed/kg gain | NOT_FOUND | - |  | Filter feeder; no FCR published. |
| yield_kg_per_acre_per_crop | NOT_FOUND | kg/acre/crop | NOT_FOUND | - |  | Not published separately; part of polyculture yield (see catla row). |
| crops_per_year_tn | 1 to 2 | crops/yr | VERIFIED | FAO_TN |  | One crop conventionally; floating-pellet farmers stocking stunted seed 'can raise two crops per year' (harvests 'generally twice'). |
| farmgate_price_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | No TN quote found; TN farmers report it 'fetched a low price' (Thanjavur 1992-93). China farm price US$0.5/kg (2010). |
| seed_cost_inr_per_unit | 3.0 | INR/fingerling | VERIFIED | SLBC | 2024-25 | Derived: TN scale of finance 2024-25 budgets seed Rs 30,000 for 10,000 fingerlings/ha = Rs 3.0 each. NABARD 2015: Rs 10-15 for 200-250 g stunted yearlings. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog (Oct 2025) 'floating feed Rs 40 to 70 per kg'; no institutional 2025-26 quote found. Thanjavur 2010: floating pellet US$0.44-0.50/kg, sinking US$0.33-0.39, farm mash US$0.27. |
| feed_share_of_variable_cost_pct | 50 to 75 | % of variable cost | VERIFIED | FAO_TN |  | Thanjavur 2010 survey: feed = 75.0% of variable cost overall (US$2,864.6 of 3,819.1/ha/yr); floating pellet 63.1%, conventional 65.4%. TN scale of finance 2024-25: feed Rs 2.5 lakh of Rs 5.01 lakh working capital/ha = 49.9%. FAO: feed 'over 50 percent of total input cost'. |
| stocking_months_tn | July-August (stocking after pond preparation completed by July/August; ponds perennial July-March) | months | VERIFIED | FAO_TN |  | Thanjavur district survey 2010. Carp seed availability is tied to monsoon breeding; TN off-season breeding makes fingerlings available by March-April (search-level claim, not read). |
| aeration_common | no (unaerated semi-intensive ponds; pumping for water exchange budgeted, aerators not standard) | yes/no | ASSUMED | SLBC |  | No survey statement on aerator use in TN carp ponds was found; TN scale of finance includes an electricity line (Rs 30,000/ha) for pumping. IMC review notes paddlewheel aerators suit 1-1.5 m ponds when intensified. |

## GIFT tilapia (all-male Nile tilapia) - *Oreochromis niloticus (GIFT strain)*

- Tamil name: **திலாப்பியா / சிலேபி மீன்** (ASSUMED; TAWIKI_LIST) - No Tamil Wikipedia langlink for Nile tilapia; name taken from the Tamil Wikipedia species list via summariser. Retail lists use 'Jalebi meen'.
- Water type: freshwater
- Culture system: earthen pond monosex culture on floating pellets, semi-intensive to intensive; only all-male/hybrid tilapia permitted in India under the 2011 responsible-farming guidelines (licence via State Fisheries Dept)
- Notes: TN Fisheries promotes GIFT (Policy Note 2020-21) and runs GIFT hatchery expansion (Manjalar). Tolerates 12-15 ppt salinity (NABARD). Live-fish sales fetch premiums.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 24 to 30 | C | VERIFIED | KERALA |  | Kerala PoP 2021 grow-out table 24-30 C. Conflict: FAO 'preferred temperature ranges from 31 to 36 C'; juvenile trial best growth at 30 C of 26/28/30 (PMC 2024). |
| temp_tolerable_c | 11 to 42 | C | VERIFIED | FAO_TIL |  | FAO: lower and upper lethal temperatures 11-12 C and 42 C; spawning begins at 24 C. |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  | Secondary summaries cite no feeding/growth below ~15-16 C; not confirmed on a page read for this table. |
| do_minimum_mg_l | 0.8 to 3.0 | mg/L | VERIFIED | TRANDUY |  | Incipient DO below which feed intake and growth decline is reported at <0.8 to 3 mg/L; Tran-Duy 2008 measured lower intake at ~3.0 vs ~5.5 mg/L. Use 3 mg/L as the practical feeding threshold. |
| do_preferred_mg_l | 5.0 to n/p | mg/L | VERIFIED | KERALA |  | Kerala PoP grow-out: DO >5 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  | Tolerates ~0.8 mg/L (10% saturation) briefly (Tran-Duy 2008 citing literature); lethal level not published. |
| stocking_density_per_acre | 12141 to 20235 | fingerlings/acre | VERIFIED | NABARD_GIFT |  | NABARD 2015: 3-5 nos/m2 after one-month hapa nursery (economics use 25,000 seed/ha). FAO ponds: 1-3 fish/m2 (4,047-12,141/acre). Odisha farms: 6,000/acre (Fish Site 2022). |
| culture_period_months | 5 to 8 | months | VERIFIED | NABARD_GIFT |  | NABARD 5-6 months to 500 g; Kerala PoP 5-6 months; FAO 5-8 months; TN scale of finance assumes a 5-month cycle. |
| harvest_size_g | 400 to 900 | g | VERIFIED | FAO_TIL |  | FAO 400-500 g; NABARD 500 g; MPEDA 600-900 g in 6 months; Odisha farms 700-800 g. |
| survival_pct | 75 to 92 | % | VERIFIED | NABARD_GIFT |  | NABARD model 75%; Odisha farms 90-92% (Fish Site 2022); Kerala PoP 90%. |
| fcr | 1.17 to 1.5 | kg feed/kg gain | VERIFIED | NABARD_GIFT |  | NABARD 'FCR 1.25 to 1.5'; Odisha farm 1.17. |
| yield_kg_per_acre_per_crop | 2428 to 4047 | kg/acre/crop | VERIFIED | NABARD_GIFT |  | NABARD 8-10 t/ha per 6-month crop (economics 9,375 kg/ha); FAO 6-8 t/ha/crop, up to 10. Odisha farms ~2-3 t/acre/yr. |
| crops_per_year_tn | 2 to 3 | crops/yr | VERIFIED | NABARD_GIFT |  | NABARD economics use 2 crops/yr; 'three crops are possible in perennial ponds'. TN scale of finance period 5 months. |
| farmgate_price_inr_per_kg | 110 to 200 | INR/kg | ASSUMED | GOLDEN | 2026-09-21; mixed (see note) | Low: Odisha farm-gate Rs 110/kg (Fish Site, Jun 2022; retail Rs 160-170). High: 'Tamil Nadu fish price today' tilapia Rs 200/kg (21 Sep 2026, market level not stated). National wholesale monthly avg Rs 158.5/kg (Jun 2025). NABARD 2015 model Rs 75/kg. No TN farm-gate quote found. |
| seed_cost_inr_per_unit | 2.5 to 6.0 | INR/fingerling | VERIFIED | RGCA | 2025-04-15 | MPEDA-RGCA list Apr 2025: GIFT all-male 1.5-2.5 cm Rs 2.50; 2.0-3.0 cm Rs 4-6. TN scale of finance budgets Rs 2 lakh/ha for GIFT seed (density not stated). NABARD 2015: Rs 3. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog Oct 2025; NABARD 2015 used Rs 28/kg. |
| feed_share_of_variable_cost_pct | 43 to 73 | % of variable cost | VERIFIED | SLBC |  | Derived: TN scale of finance 2024-25 GIFT per ha feed Rs 3,22,300 of Rs 7,43,300 = 43.4%; NABARD 2015 model Rs 3,67,500 of Rs 5,02,250 = 73.2%. |
| stocking_months_tn | NOT_FOUND | months | NOT_FOUND | - |  | No TN season found; hatchery seed (RGCA) available year-round; Krishnagiri farm-pond scheme stocks GIFT because ponds hold water only ~4 months. |
| aeration_common | yes in intensive ponds (>3/m2) - paddlewheel; not standard in extensive farm ponds | yes/no | ASSUMED | NABARD_GIFT |  | NABARD model lists a 5 HP pump but no aerator; MPEDA/vendors report paddlewheels on tilapia farms. |

## Pangasius (striped catfish / sutchi) - *Pangasianodon hypophthalmus (Pangasius sutchi)*

- Tamil name: **பங்காஸ்** (ASSUMED; TAWIKI_LIST) - No Tamil Wikipedia langlink; name from Tamil Wikipedia species list via summariser.
- Water type: freshwater (tolerates <2 ppt; used in abandoned shrimp ponds)
- Culture system: earthen pond monoculture (semi-intensive, high density) or polyculture with carps; pelleted floating feed; 1.5-2 m depth
- Notes: Promoted by TN Fisheries as a fast-growing species (Policy Note 2020-21). AP farm-gate price is volatile and has discouraged farmers (Global Seafood Advocate 2017; WAS 2019).

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 25 to 30 | C | VERIFIED | NABARD_PANG |  | NABARD 2015 water-quality target 25-30 C. Conflict: FAO sheet gives 22-26 C (Mekong context). |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 0.1 | mg/L | VERIFIED | NABARD_PANG |  | Facultative air-breather: NABARD target DO 0.1 mg/l; FAO 'as low as 0.05 to 0.10 mg/litre'. Growth-suppression threshold not published. |
| do_preferred_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  | 'Air breathing fish thus they don't need to have a much higher dissolved oxygen' (NABARD). |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 4047 to 10117 | fingerlings/acre | VERIFIED | NABARD_PANG |  | NABARD: 12,500/ha typical; monoculture <20,000/ha (15-20 g fingerlings); polyculture <10,000/ha. Andhra practice (WAS 2019): 8,750/ha at 0.76 m depth, 25,000/ha (max 45,000) at 1.5-2.7 m. FAO Vietnam 20-60/m2 is not comparable. |
| culture_period_months | 8 to 12 | months | VERIFIED | NABARD_PANG |  | NABARD 8-12 months to 1-1.5 kg; AP farms 150-350 days (WAS 2019); FAO 1-1.5 kg in 6 months or less. |
| harvest_size_g | 1000 to 1500 | g | VERIFIED | NABARD_PANG |  |  |
| survival_pct | 76 to 96 | % | VERIFIED | WAS_PANG |  | AP farms 76-96% (60-70% in prolonged culture); NABARD 80-90%. |
| fcr | 1.3 to 2.35 | kg feed/kg gain | VERIFIED | WAS_PANG |  | AP farms 1.3-1.46 on 28% protein pellets; NABARD 2.35 average on mash/pellets; FAO commercial pellets 1.7-1.9. |
| yield_kg_per_acre_per_crop | 4856 to 10118 | kg/acre/crop | VERIFIED | NABARD_PANG |  | NABARD: monoculture 20-25 t/ha/crop, polyculture 12-14 t/ha; India typical 10-15 t/ha/yr (Global Seafood Advocate 2017). |
| crops_per_year_tn | 1 | crops/yr | VERIFIED | NABARD_PANG |  | Derived from 8-12 month grow-out. |
| farmgate_price_inr_per_kg | 71.5 to 80 | INR/kg | VERIFIED | WAS_PANG | 2018; farm-gate (Andhra Pradesh) | Andhra Pradesh farm-gate 2018: Rs 71.5-80/kg (2017: Rs 55.6-78). No 2025-26 farm-gate quote found for TN or AP; trade listings Rs 100-130/kg are wholesale/retail. |
| seed_cost_inr_per_unit | 0.3 to 7.0 | INR/fingerling | VERIFIED | WAS_PANG | 2018 | Seasonal: Rs 5-7 (Jan-May), Rs 0.3-1 (Jun-Dec) in 2018; NABARD 2015 Rs 1; 2025 trade listings Rs 0.6-2. |
| feed_cost_inr_per_kg | 40 to 70 | INR/kg (floating pellet) | ASSUMED | PERFECT | 2025-10-09 | Vendor blog Oct 2025 (Rs 36/kg pangasius pellet listings exist); NABARD 2015 mash Rs 14.6/kg. |
| feed_share_of_variable_cost_pct | 78.6 | % of variable cost | VERIFIED | NABARD_PANG |  | Derived: feed Rs 4,38,000 of Rs 5,57,000 operational cost/ha/crop (NABARD 2015). |
| stocking_months_tn | NOT_FOUND | months | NOT_FOUND | - |  | Seed is cheapest Jun-Dec in India (WAS 2019); no TN stocking season published. |
| aeration_common | optional - air-breather; aerators used in intensive monoculture | yes/no | ASSUMED | NABARD_PANG |  | NABARD text says no high DO needed; its farm photo shows a paddlewheel aerator. |

## Striped murrel / viral meen - *Channa striata*

- Tamil name: **விரால் மீன்** (VERIFIED; WIKI_TA) - Tamil Wikipedia article title; alternative names முறால், நெடுமுரல்.
- Water type: freshwater
- Culture system: earthen pond monoculture of weaned (pellet-trained) fingerlings on 40% CP floating feed; also concrete tanks/biofloc
- Notes: Cultured in the Cauvery delta districts (DT Next 2025). Feed-trained (weaned) fingerlings are essential; cannibalism if ungraded.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 28 to 30 | C | VERIFIED | TNAU_MURREL |  | TNAU pond culture at 29 +/- 1 C. Secondary summaries cite 28-35 C thriving range. |
| temp_tolerable_c | 15 to 35 | C | VERIFIED | KERALA |  | Kerala PoP 2021: tolerates annual temperature variation 15-35 C, salinity to 12 ppt, pH 4-9. |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  | Obligate air-breather; TNAU ponds recorded 0.06-6.52 mg O2/l without loss. Feeding-suppression threshold not published. |
| do_preferred_mg_l | 6.0 | mg/L | ASSUMED | IJISEM |  | Nizamabad commercial pond ran at 6 mg/L with weekly exchange; not a published optimum. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 4047 to 6070 | fingerlings/acre | VERIFIED | NFDB_MURREL |  | NFDB 10,000/ha (5-8 cm); TNAU 12,000-15,000/ha (8-10 cm); Kerala PoP 1-2/m2. Nizamabad commercial case 3,500 in 1,115 m2 = 31,400/ha (12,700/acre). |
| culture_period_months | 8 to 10 | months | VERIFIED | NFDB_MURREL |  |  |
| harvest_size_g | 600 to 900 | g | VERIFIED | NFDB_MURREL |  | NFDB 600-700 g; TNAU 800-900 g; Nizamabad 2,500 kg from ~3,000 fish (~830 g). |
| survival_pct | 70 to 95 | % | VERIFIED | NFDB_MURREL |  | NFDB model 70%; TNAU 90-95%; Nizamabad 85.7%. |
| fcr | 1.28 to 1.5 | kg feed/kg gain | VERIFIED | NFDB_MURREL |  | NFDB 1:1.5; Nizamabad 1.28-1.3. |
| yield_kg_per_acre_per_crop | 1983 to 9073 | kg/acre/crop | VERIFIED | NFDB_MURREL |  | NFDB model 4.90 t/ha/crop (1,983 kg/acre); Nizamabad high-density pond 2,500 kg/0.1115 ha = 22.4 t/ha (9,073 kg/acre). |
| crops_per_year_tn | 1 | crops/yr | VERIFIED | NFDB_MURREL |  | Derived from 8-10 month cycle. |
| farmgate_price_inr_per_kg | 270 | INR/kg | VERIFIED | IJISEM | 2025; farm-gate (Telangana) | Farm-gate Rs 270/kg, Nizamabad (Telangana) 2025 case study. NFDB: open-market Rs 400-500/kg; national wholesale avg Rs 196.9/kg (Jun 2025); Madurai trade listing Rs 450/kg (ASSUMED). No TN farm-gate quote found. |
| seed_cost_inr_per_unit | 7 to 8 | INR/fingerling | VERIFIED | NFDB_MURREL |  | NFDB Rs 7/pc (5-8 cm weaned); trade listings Rs 5-8 (2025). TNAU page's Rs 1 is historic. |
| feed_cost_inr_per_kg | 100 to 136 | INR/kg (40% CP pellet) | VERIFIED | NFDB_MURREL |  | NFDB Rs 100/kg; Nizamabad derived ~Rs 136/kg (79.65% of Rs 5,46,645 over 3,200 kg feed). |
| feed_share_of_variable_cost_pct | 78 to 80 | % of variable cost | VERIFIED | IJISEM |  | Nizamabad 79.65% of operating cost; NFDB model ~78% (Rs 7.35 lakh feed of ~Rs 9.4 lakh). |
| stocking_months_tn | NOT_FOUND | months | NOT_FOUND | - |  | Murrel breeds in the monsoon; weaned seed availability season for TN not published. |
| aeration_common | no - air-breather; water exchange used instead | yes/no | ASSUMED | IJISEM |  |  |

## Giant freshwater prawn / scampi - *Macrobrachium rosenbergii*

- Tamil name: **NOT_FOUND** (NOT_FOUND; -) - Tamil Wikipedia title is only a transliteration (மேக்ரோபிராக்கியம் ரோசென்பெர்கி); the Tamil species list gave a generic prawn word. Common TN name not sourced.
- Water type: freshwater (<10 ppt)
- Culture system: earthen pond monoculture (or polyculture with carps) of nursed juveniles, semi-intensive, partial harvesting
- Notes: TN had only 192 ha under scampi (0.75 t/ha) in the mid-2000s (TNAU table); the species is a minor TN crop. CIFA-GI scampi strain grows ~30% larger (Assam trial).

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 28 to 31 | C | VERIFIED | TNAU_PRAWN |  | TNAU: optimum 28-31 C (25-31 C for year-round production); TN Parangipettai ponds 27-31 C. |
| temp_tolerable_c | 20 to n/p | C | VERIFIED | TNAU_PRAWN |  | TNAU: needs water >=20 C for at least 7 months; upper limit not published (disease risk at 33-34 C). |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 3.0 | mg/L | VERIFIED | TNAU_PRAWN |  | Lower bound of TNAU grow-out requirement 3-7 ppm. |
| do_preferred_mg_l | 4.0 to 6.0 | mg/L | VERIFIED | TNPRAWN |  | Tamil Nadu (Parangipettai) ponds 4.0-6.0 ppm; TNAU range 3-7 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 1619 to 20235 | PL or juveniles/acre | VERIFIED | TNAU_PRAWN |  | TNAU monoculture 4,000-50,000 PL/ha, recommended 4 juveniles/m2 (40,000/ha = 16,188/acre); FAO semi-intensive 4-20/m2; TN Parangipettai trial 33,000/ha; Assam 30,000/ha mono, 10,000/ha poly. |
| culture_period_months | 6 to 8 | months | VERIFIED | TNAU_PRAWN |  | Monoculture 6-8 months (polyculture 8-12); TN trial 193 days with partial harvests from month 3. |
| harvest_size_g | 50 to 200 | g | VERIFIED | TNAU_PRAWN |  |  |
| survival_pct | 50 to 70 | % | VERIFIED | TNAU_PRAWN |  | Grow-out survival 50-70%; Assam farmer ~80%. |
| fcr | 2.0 to 3.0 | kg feed/kg gain | VERIFIED | FAO_GRP |  |  |
| yield_kg_per_acre_per_crop | 227 to 607 | kg/acre/crop | VERIFIED | TNAU_PRAWN |  | TNAU target 1,500 kg/ha (607 kg/acre); TN Parangipettai monoculture 561 kg/ha (227 kg/acre) in 193 days; India average productivity 1.05 t/ha (425 kg/acre); FAO semi-intensive 500-5,000 kg/ha/yr. |
| crops_per_year_tn | 1 | crops/yr | ASSUMED | TNAU_PRAWN |  | Derived from a 6-8 month cycle plus pond drying. |
| farmgate_price_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | No TN/South India 2025-26 quote found. Assam farmer sold at Rs 1,200/kg (Fish Site, Sep 2024); TNAU page Rs 175/kg large, Rs 70/kg small (undated, ~2010). |
| seed_cost_inr_per_unit | 0.6 to 1.0 | INR/PL | ASSUMED | TNAU_PRAWN |  | TNAU Rs 600 per 1,000 PL (undated); 2025 trade listing Rs 1/PL-25. |
| feed_cost_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | No 2025-26 prawn-pellet price found; TNAU model implies Rs 20/kg (Rs 60,000 for 3 t, undated). |
| feed_share_of_variable_cost_pct | NOT_FOUND | % of variable cost | NOT_FOUND | - |  |  |
| stocking_months_tn | NOT_FOUND | months | NOT_FOUND | - |  |  |
| aeration_common | no (semi-intensive ponds unaerated) | yes/no | ASSUMED | FAO_GRP |  |  |

## Pearl spot / karimeen - *Etroplus suratensis*

- Tamil name: **முத்துப்புள்ளி மீன்** (VERIFIED; WIKI_TA) - Tamil Wikipedia article title for Etroplus suratensis; Tamil species list gives கிளி மீன் (ASSUMED).
- Water type: brackish (also freshwater); 15-30 ppt
- Culture system: brackishwater pond monoculture or polyculture with grey mullet; slow-growing, high-value
- Notes: Feeding 3-5% biomass/day; breeds in ponds. Slow growth makes it a niche crop in TN.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 24 to 32 | C | VERIFIED | TNAU_PEARL |  |  |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 3.5 | mg/L | VERIFIED | TNAU_PEARL |  | TNAU: DO >3.5 ppm. |
| do_preferred_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 8094 to 12141 | fingerlings/acre | VERIFIED | TNAU_PEARL |  | TNAU monoculture 20,000-30,000/ha; Kerala PoP polyculture 15,000/ha pearl spot + 5,000/ha mullet. |
| culture_period_months | 8 to 12 | months | VERIFIED | TNAU_PEARL |  | 8-10 months to marketable size; 9-12 months at high density. |
| harvest_size_g | 120 to 150 | g | VERIFIED | TNAU_PEARL |  | Kerala market grades: B >100 g, A >150 g, A+ >250 g. |
| survival_pct | NOT_FOUND | % | NOT_FOUND | - |  |  |
| fcr | NOT_FOUND | kg feed/kg gain | NOT_FOUND | - |  |  |
| yield_kg_per_acre_per_crop | 405 | kg/acre/yr | VERIFIED | TNAU_PEARL |  | Monoculture 1,000 kg/ha/yr. |
| crops_per_year_tn | 1 | crops/yr | ASSUMED | TNAU_PEARL |  |  |
| farmgate_price_inr_per_kg | 240 to 600 | INR/kg | VERIFIED | ONM_KARI | 2025-12-30; retail (Kerala) | Fisher-society retail, Kumarakom (Kerala), 30 Dec 2025: A+ Rs 600, A Rs 500, B Rs 320, C Rs 240/kg. TNAU page 'up to Rs 150/kg' is historic; Chennai trade listing Rs 300/kg (ASSUMED). No TN farm-gate quote found. |
| seed_cost_inr_per_unit | 7 to 9 | INR/fingerling | VERIFIED | RGCA | 2025-04-15 | MPEDA-RGCA Etroplus seed 2.5-3.5 cm Rs 7-9 (Apr 2025). |
| feed_cost_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  |  |
| feed_share_of_variable_cost_pct | NOT_FOUND | % of variable cost | NOT_FOUND | - |  |  |
| stocking_months_tn | NOT_FOUND | months | NOT_FOUND | - |  |  |
| aeration_common | no | yes/no | ASSUMED | TNAU_PEARL |  |  |

## Improved strains promoted in TN: Jayanti rohu and Amur carp - *Labeo rohita (CIFA 'Jayanti' selected line); Cyprinus carpio haematopterus / C. rubrofuscus (Amur carp)*

- Tamil name: **NOT_FOUND** (NOT_FOUND; -) - No Tamil name sourced; use rohu / சாதாக்கெண்டை names.
- Water type: freshwater
- Culture system: as for rohu and common carp; promoted for short-season farm ponds and multipurpose ponds
- Notes: VERIFIED 2026-09-21: TN Fisheries Policy Note 2020-21 (p.109) lists 'Promotion of culture technology for fast growing fishes viz., Amur Carp, Jayanthi Rohu, Genetically Improved Farmed Tilapia (GIFT) and Pangasius'. ASSUMED (search-level only): Jayanti rohu ~17% faster growth per generation (CIFA); Karnataka pond trial reached Amur 423 g and Jayanti rohu 256 g in a 5:5 mix. Treat as rohu/common carp with a growth premium until TN farm data are found.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | NOT_FOUND | C | NOT_FOUND | - |  | Use rohu / common carp rows. |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| do_preferred_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | NOT_FOUND | fish/acre | NOT_FOUND | - |  |  |
| culture_period_months | NOT_FOUND | months | NOT_FOUND | - |  |  |
| harvest_size_g | NOT_FOUND | g | NOT_FOUND | - |  |  |
| survival_pct | NOT_FOUND | % | NOT_FOUND | - |  |  |
| fcr | NOT_FOUND | kg feed/kg gain | NOT_FOUND | - |  |  |
| yield_kg_per_acre_per_crop | NOT_FOUND | kg/acre/crop | NOT_FOUND | - |  |  |
| crops_per_year_tn | NOT_FOUND | crops/yr | NOT_FOUND | - |  |  |
| farmgate_price_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | Sold as rohu / common carp. |
| seed_cost_inr_per_unit | NOT_FOUND | INR/fingerling | NOT_FOUND | - |  | Only trade listings found (banglakrishi etc.); not used. |
| feed_cost_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  |  |
| feed_share_of_variable_cost_pct | NOT_FOUND | % of variable cost | NOT_FOUND | - |  |  |
| stocking_months_tn | NOT_FOUND | months | NOT_FOUND | - |  |  |
| aeration_common | NOT_FOUND | yes/no | NOT_FOUND | - |  |  |

## Pacific white shrimp (vannamei) - *Litopenaeus (Penaeus) vannamei*

- Tamil name: **வெள்ளை இறால்** (ASSUMED; TAWIKI_LIST) - No Tamil Wikipedia langlink; name from the Tamil species list via summariser. Trade usage 'வண்ணாமி இறால்' unsourced.
- Water type: brackish (0.5-45 ppt; grows best 10-15 ppt)
- Culture system: lined or earthen pond, semi-intensive to intensive with SPF PL, paddlewheel/long-arm aeration, zero/low water exchange; CAA-registered farms
- Notes: TN: 3,001 CAA-registered shrimp farms on 5,745 ha across 13 coastal districts (TN Fisheries page, search-level; site unreachable). Nagapattinam is the leading TN producer. NABARD 2015 cost of production Rs 150-160/kg at 8-10 t/ha; 2023 TN break-even Rs 250-330/kg. Wholesale/export prices differ from farm-gate.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 28 to 32 | C | VERIFIED | MPEDA_SHRIMP |  | MPEDA ideal 28-32 C; NABARD 'optimal 30-34 C'; CAA optimal 28-33 C (pond) / 28-32 C; Kerala PoP 30-34 C. |
| temp_tolerable_c | 18 to 36 | C | VERIFIED | CAA |  | CAA table 'tolerable limit 18-36 C'; NABARD: 'very tolerant to low temperatures of up to 15 C'. |
| temp_growth_stops_below_c | 20 | C | VERIFIED | NABARD_VAN |  | 'At 20 C growth virtually stops.' |
| do_minimum_mg_l | 4.0 | mg/L | VERIFIED | NABARD_VAN |  | 'DO levels should be maintained above 4 ppm'. Boyd (2010) penaeid data: survival 42% and FCR 2.64 at 2.32 mg/L vs 61% and 1.96 at 3.89 mg/L. |
| do_preferred_mg_l | 4.5 to 7.0 | mg/L | VERIFIED | CAA |  | CAA optimal 5-7 ppm (>50% air saturation); NABARD >4.5 ppm optimal; MPEDA 4-6 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  | Secondary summaries cite 0-1.5 mg/L lethal and 1.7-3.0 mg/L slow growth (PANAMJAS); page could not be fetched (certificate error). |
| stocking_density_per_acre | 161878 to 242817 | PL/acre | VERIFIED | NABARD_VAN |  | NABARD/CAA: 40-60 PL/m2 preferred, 'above 60 no./sq m is not permitted'; India 2025 practice 40-60 PL/m2 (AAP). FAO semi-intensive 10-30 PL/m2, extensive 4-10. MPEDA: aerators required above 30,000/ha. |
| culture_period_months | 3.3 to 4.0 | months | VERIFIED | NABARD_VAN |  | 20 g in 100-120 days at 60/m2; NABARD economics 4-month crop; FAO 4-5 months; TN fisheries dept page (not readable) cites 110-125 days. |
| harvest_size_g | 20 to 25 | g | VERIFIED | NABARD_VAN |  | NABARD 20-25 g average; TN farms harvest partial counts from 100/kg (10 g) down to 30/kg. |
| survival_pct | 85 | % | VERIFIED | NABARD_VAN |  | NABARD model assumption; FAO super-intensive 55-91%. |
| fcr | 1.1 to 1.4 | kg feed/kg gain | VERIFIED | NABARD_VAN |  | NABARD 1.1-1.4 (model 1.40); FAO 1.2-1.8; TNAU 1.2. |
| yield_kg_per_acre_per_crop | 3238 to 4300 | kg/acre/crop | VERIFIED | NABARD_VAN |  | NABARD 8-10 t/ha/crop at 50/m2 (model 10,625 kg/ha); FAO semi-intensive 0.5-2 t/ha/crop, intensive 7-20 t/ha/crop. |
| crops_per_year_tn | 2 to 3 | crops/yr | VERIFIED | MPEDA_CROP |  | MPEDA: TN vannamei stocking and harvest Jan-Dec (year-round); NABARD 2 crops; AAP 2025: up to five crops in two years on 30-40% of farms. |
| farmgate_price_inr_per_kg | 200 to 400 | INR/kg | VERIFIED | BENISON | 2023-07-07 (TN); 2026-05-22 (AP); farm-gate | Tamil Nadu farm-gate by count, 7 Jul 2023: 30-count Rs 400, 40 Rs 300, 60 Rs 240, 80 Rs 220, 100 Rs 200; break-even then Rs 330/290/250 for 40/60/100 count. Latest: Andhra Pradesh 100-count Rs 270 -> 235 -> 220/kg (22 May 2026, Undercurrent); size 30 US$4.71/kg (Oct 2025), size 60 US$3.87/kg (end-2025). No 2025-26 TN quote found. |
| seed_cost_inr_per_unit | 0.25 to 0.35 | INR/PL | ASSUMED | SP_SEARCH | 2025-03 | S&P Global (Mar 2025) via search summary: 'Rs 0.25-0.30 per seed, up to Rs 0.35 in January'; page returned 403. NABARD 2015 model Rs 0.75/PL; FAO US$0.4-3.0 per 1,000 PL. |
| feed_cost_inr_per_kg | 108 to 112 | INR/kg | VERIFIED | DC_FEED | 2026-06-19 | Andhra Pradesh, 19 Jun 2026: feed cut from Rs 112 to Rs 108/kg. Apr 2025 (BS, search only): 25 kg vannamei bag Rs 2,667-2,702 = Rs 107-108/kg. Jul 2023: ~Rs 90/kg (Benison). |
| feed_share_of_variable_cost_pct | 59 to 70 | % of variable cost | VERIFIED | PLOS |  | Gujarat survey (PLOS 2021): ~70% of variable cost; NABARD model feed Rs 8.93 lakh of Rs 15.04 lakh = 59.3%. Trade sources cite 55-60% intensive, ~40% semi-intensive (ASSUMED). |
| stocking_months_tn | January-December (year-round); typical two crops Apr-Jun and Aug-Sep | months | VERIFIED | MPEDA_CROP |  | MPEDA cropping pattern (TN); crop timing from Benison 2023. |
| aeration_common | yes - paddlewheel / long-arm aerators, 1 HP per 300 kg (NABARD) to 1 HP per 400 kg biomass (MPEDA); 4 x 2 HP per ha in NABARD model | yes/no | VERIFIED | NABARD_VAN |  |  |

## Black tiger shrimp - *Penaeus monodon*

- Tamil name: **கருவண்டன் இறால்** (ASSUMED; TAWIKI_LIST) - Tamil Wikipedia article title is only a transliteration (பின்னேயஸ் மோனோடான்); 'கருவண்டன்' from the Tamil species list via summariser.
- Water type: brackish (optimal 15-30 ppt; tolerates 0.2-70 ppt)
- Culture system: earthen pond, traditional / improved-traditional / scientific extensive to semi-intensive (CAA permits only these); SPF PL now available (RGCA)
- Notes: Indian production rose to 69,072 t in 2025-26 (MPEDA, search-level). CAA guidelines permit only traditional/improved-traditional/scientific extensive systems in coastal areas.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 28 to 32 | C | VERIFIED | MPEDA_SHRIMP |  | MPEDA ideal 28-32 C (shared LV/BT page); CAA optimal 28-33 C. |
| temp_tolerable_c | 12 to 37.5 | C | VERIFIED | TNAU_SHRIMP |  | 'Mortalities occur at temperatures below 12 C only'; 'can tolerate temperatures up to at least 37.5 C'. CAA tolerable 18-36 C. |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 4.0 | mg/L | VERIFIED | MPEDA_SHRIMP |  | Lower bound of MPEDA ideal 4-6 ppm; CAA hatchery/pond standards 'above 3' / 'above 4'. |
| do_preferred_mg_l | 5.0 to 7.0 | mg/L | VERIFIED | CAA |  | CAA optimal 5-7 ppm (>50% saturation); MPEDA 4-6 ppm. |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 28329 to 80939 | PL/acre | VERIFIED | AAP2025 |  | India 2025: 7-10 PL/m2 rising to 20 PL/m2; FAO semi-intensive 5-20 PL/m2, extensive <2; Gujarat survey 1.2-1.4/m2; CAA: keep below 15 PL/m2 for pond-bottom management. |
| culture_period_months | 3.5 to 5.3 | months | VERIFIED | MPEDA_CROP |  | TN crops Mar/Apr-Jun/Jul and Jul/Aug-Oct/Nov (MPEDA); FAO 4-5 months; Gujarat 146-158 days. |
| harvest_size_g | 30 to 35 | g | VERIFIED | FAO_MON |  | FAO semi-intensive/intensive 30-35 g; Indian revival farms target 45-50 g (16-20 count) - search-level. |
| survival_pct | NOT_FOUND | % | NOT_FOUND | - |  | Grow-out survival not published in sources read (FAO gives hatchery survival only). |
| fcr | 1.2 to 2.0 | kg feed/kg gain | VERIFIED | FAO_MON |  | FAO intensive 1.2-2.0; TNAU 1.8. |
| yield_kg_per_acre_per_crop | 202 to 1619 | kg/acre/yr | VERIFIED | FAO_MON |  | FAO semi-intensive 500-4,000 kg/ha/yr; extensive 50-500; intensive 4,000-15,000. |
| crops_per_year_tn | 2 | crops/yr | VERIFIED | MPEDA_CROP |  | Two seasonal crops in TN; Gujarat farms 1. |
| farmgate_price_inr_per_kg | 460 to 485 | INR/kg (converted) | ASSUMED | AAP2025 | 2025-10; farm-gate (Andhra Pradesh) | Published: size 30/kg black tiger US$5.50/kg farm-gate, Andhra Pradesh, Oct 2025 (VERIFIED). INR range is my conversion at Rs 84-88/US$. TNAU page: 'over Rs 450 per kg' at peak (undated). |
| seed_cost_inr_per_unit | 0.5 to 0.6 | INR/PL | VERIFIED | RGCA | 2025-04-15 | MPEDA-RGCA P. monodon PL13-PL20 Rs 0.50-0.60 (Apr 2025). |
| feed_cost_inr_per_kg | 108 to 120 | INR/kg | ASSUMED | BS_FEED | 2025-04 | Tiger feed 25 kg bag Rs 2,947-2,995 (Apr 2025, search summary only) = Rs 118-120/kg; general aqua feed Rs 108-112/kg (Deccan Chronicle Jun 2026, VERIFIED). |
| feed_share_of_variable_cost_pct | 80 | % of variable cost | VERIFIED | PLOS |  | Gujarat survey: ~80% of variable cost. |
| stocking_months_tn | March-April (1st crop) and July-August (2nd crop) | months | VERIFIED | MPEDA_CROP |  |  |
| aeration_common | yes where stocking exceeds 30,000/ha (3 PL/m2) - paddlewheel; unaerated in traditional systems | yes/no | VERIFIED | MPEDA_SHRIMP |  |  |

## Asian seabass / koduva - *Lates calcarifer*

- Tamil name: **கொடுவா மீன்** (VERIFIED; WIKI_TA) - Tamil Wikipedia article title.
- Water type: brackish (also freshwater); 10-30 ppt grow-out
- Culture system: earthen pond monoculture of graded hatchery fingerlings on pellets (or trash fish), semi-intensive; also cages
- Notes: Cannibalism requires size grading; hatchery at RGCA Thoduvai (Mayiladuthurai district) and CIBA. Trash-fish feeding is common in TN and worsens FCR.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 26 to 32 | C | VERIFIED | IJPAB |  | Grow-out optimum 26-32 C (nursery 25-32). |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | 4.0 | mg/L | VERIFIED | IJPAB |  | Lower bound of optimum 4-8 ppm. |
| do_preferred_mg_l | 4.0 to 8.0 | mg/L | VERIFIED | IJPAB |  |  |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 1214 to 4047 | fingerlings/acre | VERIFIED | TNAU_SEABASS |  | TNAU 3,000-5,000/ha (5-10 g seed); review monoculture 5,000-10,000/ha (5-10 cm seed); RGCA Karaikal 8,500/ha; FAO 0.25-2 fish/m2. |
| culture_period_months | 7 to 12 | months | VERIFIED | TNAU_SEABASS |  | TNAU 7-8 months; review 8-12 months to 800-1,200 g; Karaikal 11 months; cage farms 6 months to 0.9-1.25 kg (ICSF). |
| harvest_size_g | 800 to 1200 | g | VERIFIED | IJPAB |  | 400-600 g at 4-6 months; 800-1,200 g at 8-12 months; Karaikal ~1 kg. |
| survival_pct | NOT_FOUND | % | NOT_FOUND | - |  | Pond grow-out survival not published in sources read (nursery 60%, Kerala PoP). |
| fcr | 1.6 to 1.8 | kg feed/kg gain | VERIFIED | FAO_BAR |  | Commercial pellet FCR 1.6-1.8 (experimental 1.0-1.2); trash fish 4-8. |
| yield_kg_per_acre_per_crop | 809 to 2024 | kg/acre/crop | VERIFIED | TNAU_SEABASS |  | TNAU 2-3 t/ha in 7-8 months; review 3-5 t/ha in 8-12 months; RGCA Karaikal expected 15 t from two 1-ha ponds (7.5 t/ha = 3,035 kg/acre). |
| crops_per_year_tn | 1 | crops/yr | VERIFIED | TNAU_SEABASS |  | Derived from 7-12 month grow-out; cage farms take two harvests a year. |
| farmgate_price_inr_per_kg | 350 to 440 | INR/kg | VERIFIED | ICSF_KARAIKAL | c. 2021 (page undated); farm-gate (TN) | Karaikal: 'farm rate up to Rs 440 per kg', retail Rs 650+ (ICSF repost, undated - c. 2021); Vennangapattu cage farm market price Rs 350-400/kg, rearing cost Rs 190/kg (ICSF, undated). Karaikal production cost Rs 250 per 1-kg fish. |
| seed_cost_inr_per_unit | 14 to 48 | INR/fingerling | VERIFIED | RGCA | 2025-04-15 | MPEDA-RGCA Apr 2025: seabass 3.6-10.5 cm Rs 14-35; 4-5.5 cm Rs 26-30; 5-6 cm Rs 28-30; 8-10 cm Rs 38-48. |
| feed_cost_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | Imported/CIBA pellets used; no price found. |
| feed_share_of_variable_cost_pct | NOT_FOUND | % of variable cost | NOT_FOUND | - |  |  |
| stocking_months_tn | September-November (wild seed season in TN); hatchery seed (RGCA Thoduvai) year-round | months | VERIFIED | IJPAB |  | Review citing Arasu et al. 2008 for TN wild seed; RGCA availability list for hatchery seed. |
| aeration_common | yes in intensive monoculture ponds (site must have power for aerators) | yes/no | VERIFIED | IJPAB |  |  |

## Milkfish - *Chanos chanos*

- Tamil name: **பாலமீன்** (VERIFIED; WIKI_TA) - Tamil Wikipedia article title; CIBA uses 'Paal Kendai' / 'Paal Meen' (search-level).
- Water type: brackish (0-145 ppt tolerance)
- Culture system: brackishwater earthen pond, extensive to semi-intensive on natural food (lab-lab) plus supplementary feed; CIBA multiple-stocking-multiple-harvest model
- Notes: CIBA achieved captive breeding in 2015 (Muttukadu). Herbivore/detritivore - low feed cost; often polycultured with mullet, pearl spot and tiger shrimp.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | NOT_FOUND | C | NOT_FOUND | - |  | FAO/Bagarinao: 23 C decreases growth, temperatures up to 33 C increase it; no optimum range stated. |
| temp_tolerable_c | 15 to 40 | C | VERIFIED | KERALA |  | Kerala PoP 2021; lethal limits for juveniles 8.5 C and 42.7 C (FAO, Garcia 1986). |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  | Growth and feeding reduced at 23 C (FAO). |
| do_minimum_mg_l | 1.4 | mg/L | VERIFIED | FAO_MILKBIO |  | 'Symptoms of asphyxiation are discernible at 1.4 ppm oxygen among 200 to 300 g fish' (Gerochi et al. 1978). Secondary summaries put the growth optimum at >=3 mg/L (ASSUMED). |
| do_preferred_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| do_lethal_mg_l | 0.1 to 0.4 | mg/L | VERIFIED | FAO_MILKBIO |  | 50% mortality at 0.1-0.4 ppm at 31-34 C. |
| stocking_density_per_acre | 809 to 4047 | fingerlings/acre | VERIFIED | TNAU_MILK |  | TNAU production ponds 2,000-10,000/ha of 7-15 cm fingerlings. |
| culture_period_months | 6 to 8 | months | VERIFIED | CIBA_FIN |  | CIBA MSMH grow-out 6-8 months; CIBA 2015: 500 g in 6 months. |
| harvest_size_g | 300 to 800 | g | VERIFIED | TNAU_MILK |  | TNAU 300-800 g; FAO 250-500 g. |
| survival_pct | 80 to 95 | % | VERIFIED | TNAU_MILK |  |  |
| fcr | NOT_FOUND | kg feed/kg gain | NOT_FOUND | - |  |  |
| yield_kg_per_acre_per_crop | 202 to 1416 | kg/acre/crop | VERIFIED | TNAU_MILK |  | TNAU traditional earthen ponds 500-1,000 kg/ha; CIBA MSMH model 3.5 t/ha (1,416 kg/acre); FAO 800-2,000 kg/ha. |
| crops_per_year_tn | 1 | crops/yr | ASSUMED | CIBA_FIN |  | MSMH is continuous with partial harvests. |
| farmgate_price_inr_per_kg | 120 to 150 | INR/kg | VERIFIED | ICAR_MILK | 2015-07-10; local market | ICAR-CIBA, 10 Jul 2015: local market Rs 120-150/kg, production cost Rs 50-60/kg. No 2025-26 TN quote found. |
| seed_cost_inr_per_unit | NOT_FOUND | INR/fry | NOT_FOUND | - |  | Only trade listings (Rs 1-6/piece) found; wild fry collection is the norm. |
| feed_cost_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  |  |
| feed_share_of_variable_cost_pct | NOT_FOUND | % of variable cost | NOT_FOUND | - |  |  |
| stocking_months_tn | March-June (natural fry season; TNAU) | months | VERIFIED | TNAU_MILK |  | Pulicat larval ingress Feb/Mar-Oct with peaks in April and Aug/Sep (search-level). |
| aeration_common | no | yes/no | ASSUMED | TNAU_MILK |  |  |

## Grey mullet / madavai - *Mugil cephalus*

- Tamil name: **சாம்பல் நிற மடவை** (VERIFIED; WIKI_TA) - Tamil Wikipedia article title; common usage மடவை.
- Water type: brackish (euryhaline)
- Culture system: brackishwater pond monoculture of nursed >50 g fingerlings, or polyculture with milkfish, pearl spot and tiger shrimp; supplementary feed 2-5% BW
- Notes: Hatchery seed only recently achieved at CIBA Muttukadu; farmers depend on wild seed. TN (Madras) contributed 37% of Indian mullet production in the 1960s.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 26 to 30 | C | VERIFIED | KERALA |  | Kerala PoP grow-out 26-30 C. Conflict: FAO sheet 'nursery and grow-out optimum 20-26 C' (Egypt/temperate context). |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  | FAO: highest disease mortality below 24 C. |
| do_minimum_mg_l | 4.0 | mg/L | VERIFIED | KERALA |  | Kerala PoP grow-out DO >4 ppm. |
| do_preferred_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 2499 to 4047 | fingerlings/acre | VERIFIED | MPEDA_MULLET |  | CIBA monoculture 10,000/ha of >50 g fingerlings (Kerala PoP also 10,000/ha); FAO monoculture 6,175-7,410/ha; polyculture 8,000-15,000/ha with 15,000-30,000 tiger shrimp. |
| culture_period_months | 6 to 10 | months | VERIFIED | MPEDA_MULLET |  | 8-month culture to 500-800 g; 2-3 t/ha systems in 6-10 months. |
| harvest_size_g | 500 to 800 | g | VERIFIED | MPEDA_MULLET |  | FAO 750-1,000 g in one 7-8 month season. |
| survival_pct | NOT_FOUND | % | NOT_FOUND | - |  |  |
| fcr | NOT_FOUND | kg feed/kg gain | NOT_FOUND | - |  |  |
| yield_kg_per_acre_per_crop | 1214 to 2024 | kg/acre/crop | VERIFIED | MPEDA_MULLET |  | 3-5 t/ha at 10,000/ha in 8 months; 2-3 t/ha in 6-10 months with farm-made feed; polyculture trial 3.5 t/ha total. |
| crops_per_year_tn | 1 | crops/yr | ASSUMED | MPEDA_MULLET |  |  |
| farmgate_price_inr_per_kg | 300 to 500 | INR/kg | VERIFIED | MPEDA_MULLET | 2022-06; farmer sales (partial harvest) | 'Farmers adopting partial harvesting ... sell their produce at Rs 300-500/kg' (CIBA, June 2022). |
| seed_cost_inr_per_unit | 6 to 10 | INR/fingerling | VERIFIED | MPEDA_MULLET | 2022-06 | Wild seed Rs 6-10/unit, available Nov-Feb on the east coast. |
| feed_cost_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  |  |
| feed_share_of_variable_cost_pct | NOT_FOUND | % of variable cost | NOT_FOUND | - |  |  |
| stocking_months_tn | November-February (wild seed season, east coast) | months | VERIFIED | MPEDA_MULLET |  |  |
| aeration_common | no | yes/no | ASSUMED | MPEDA_MULLET |  |  |

## Mud crab (fattening) - *Scylla serrata (also S. tranquebarica / S. oceanica in TN catches)*

- Tamil name: **கழி நண்டு** (ASSUMED; TAWIKI_LIST) - No Tamil Wikipedia langlink for Scylla serrata; name from Tamil species list via summariser.
- Water type: brackish (15-25 ppt optimal)
- Culture system: fattening of moulted 'water crabs' for 15-40 days in small brackishwater ponds, pens or cages; grow-out of crablets 4-6 months
- Notes: TNAU annual net profit examples: Rs 24,000 per 100 m2 pen, Rs 22,000 per 100 m2 pond. RGCA Thoduvai runs the mud crab hatchery. Tuticorin/Pattukottai are TN trade hubs.

| Field | Value | Unit | Status | Source | As of / market | Note |
|---|---|---|---|---|---|---|
| temp_optimum_c | 26 to 30 | C | ASSUMED | AFS528 |  | From a search summary of an Asian Fisheries Society pond-culture paper (not read): salinity 15-25 ppt, 26-30 C, pH 7.8-8.5. Hatchery larval rearing 28-31 C (Marichamy 2001) and 28-30 C (Kerala PoP) are VERIFIED. |
| temp_tolerable_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| temp_growth_stops_below_c | NOT_FOUND | C | NOT_FOUND | - |  |  |
| do_minimum_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  | Secondary summaries cite >3 ppm desirable / >5 mg/L ideal; not confirmed on a page read. |
| do_preferred_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| do_lethal_mg_l | NOT_FOUND | mg/L | NOT_FOUND | - |  |  |
| stocking_density_per_acre | 4047 to 8094 | crabs/acre (fattening) | VERIFIED | SCYLLA_IN |  | Fattening 1-2 crabs/m2 (Marichamy 2001); FAO fattening up to 1/m2 communal. Grow-out 5,000-8,000/ha (2,023-3,238/acre); FAO polyculture 500-800/ha. |
| culture_period_months | 0.5 to 1.0 | months (fattening) | VERIFIED | SCYLLA_IN |  | Fattening 15-30 days (Marichamy 2001; FAO), 3-4 weeks (TNAU), 20-40 days (Kerala farmers 2026). Grow-out 4-5 months (Marichamy); CIBA 2 g to >500 g in 165 days (search-level). |
| harvest_size_g | 300 to 700 | g | VERIFIED | ONM_CRAB |  | Marketable 300-700 g; ideal fattening stock 500 g+ (Kerala, Jul 2026); TNAU stocks ~550 g water crabs. Grow-out: 644 g males in 142 days (Marichamy). |
| survival_pct | 50 | % | VERIFIED | SCYLLA_IN |  | Grow-out at 5,000/ha: survival 50%; fattening survival not published. |
| fcr | NOT_FOUND | kg feed/kg gain | NOT_FOUND | - |  | Fed trash fish/clam at 5-10% biomass/day. |
| yield_kg_per_acre_per_crop | 486 to 567 | kg/acre/crop (grow-out) | VERIFIED | SCYLLA_IN |  | Grow-out net production 1,200-1,400 kg/ha in 4-5 months (Marichamy 2001); polyculture up to 2,440 kg/ha. Fattening throughput not published. |
| crops_per_year_tn | 2 | crops/yr (grow-out); fattening 8-12 cycles/yr | VERIFIED | FAO_CRAB |  | FAO: two grow-out crops annually; fattening cycles derived from 20-40 day turns (ASSUMED). |
| farmgate_price_inr_per_kg | 1000 to 2300 | INR/kg | VERIFIED | ONM_CRAB | 2026-07-27; farmer sale price (Kerala) | Kerala farmers (Jul 2026): water crabs bought at Rs 300-600/kg, sold after hardening at Rs 1,000-2,300/kg (market level not stated). National wholesale green mud crab avg Rs 485/kg, high Rs 650 (May 2025). No TN quote found. |
| seed_cost_inr_per_unit | 20 to 32 | INR/crablet | VERIFIED | RGCA | 2025-04-15 | MPEDA-RGCA crablets 1.6-4.0 cm Rs 20-32; megalopa Rs 12 (Apr 2025). Fattening stock = water crabs at Rs 300-600/kg. |
| feed_cost_inr_per_kg | NOT_FOUND | INR/kg | NOT_FOUND | - |  | Trash fish / clam meat; no price found. |
| feed_share_of_variable_cost_pct | NOT_FOUND | % of variable cost | NOT_FOUND | - |  |  |
| stocking_months_tn | NOT_FOUND | months | NOT_FOUND | - |  | Fattening is run year-round on wild water crabs (ASSUMED). |
| aeration_common | no | yes/no | ASSUMED | TNAU_CRAB |  |  |

## Conflicts between sources (both values kept)

- **Carp yields, TN**: Thanjavur farm survey 1992-93 averaged only 888 kg/ha/crop (359 kg/acre; Jayaraman 1997) against 3,010-4,596 kg/ha/yr in the 2010 Thanjavur survey (FAO 2013) and 3-5 t/ha/yr in FAO/TNAU guidance; NABARD's intensive model assumes 5 t/ha per 6-month crop. Use the 2010 survey for TN semi-intensive ponds.
- **Tilapia optimum temperature**: Kerala PoP 24-30 C vs FAO 'preferred 31-36 C'.
- **Pangasius optimum temperature**: NABARD 25-30 C vs FAO 22-26 C (Mekong).
- **Pangasius stocking**: NABARD monoculture <20,000/ha vs Andhra practice up to 25,000-45,000/ha in deep ponds (WAS 2019); FAO Vietnam 40-60/m2 is a different system.
- **Grey mullet optimum temperature**: Kerala PoP 26-30 C vs FAO 20-26 C.
- **Vannamei stocking ceiling**: NABARD/CAA-derived 'above 60/m2 not permitted' vs CAA general guidelines recommending only extensive/improved-traditional systems (<15 PL/m2 for pond-bottom management).
- **Vannamei prices**: TN farm-gate Jul 2023 (100-count Rs 200) vs Andhra May 2026 (Rs 220-270) - different states and dates; TN 2025-26 NOT_FOUND.
- **Murrel yield**: NFDB model 4.9 t/ha/crop vs a Telangana commercial pond at 22.4 t/ha (31,400/ha stocking).
- **Milkfish stocking**: TNAU 2,000-10,000/ha; The Fish Site copy of the FAO sheet reports 50,000-100,000/ha for 'extensive/semi-intensive ponds', which looks like a nursery figure and was not used.
- **Carp price**: DT Next quote (Rs 200-250 normal; Rs 350-400 in the April 2026 shortage) does not state the market level; national wholesale averages (Jun 2025) were Rs 197 (rohu) and Rs 214 (catla).

## Fields most often NOT_FOUND

- do_lethal_mg_l: 16 of 18 species
- temp_growth_stops_below_c: 14 of 18 species
- temp_tolerable_c: 9 of 18 species
- fcr: 7 of 18 species
- survival_pct: 7 of 18 species
- stocking_months_tn: 7 of 18 species
- feed_cost_inr_per_kg: 7 of 18 species
- feed_share_of_variable_cost_pct: 7 of 18 species
- do_preferred_mg_l: 6 of 18 species
- farmgate_price_inr_per_kg: 5 of 18 species
- temp_optimum_c: 3 of 18 species
- do_minimum_mg_l: 3 of 18 species
- stocking_density_per_acre: 2 of 18 species
- harvest_size_g: 2 of 18 species
- yield_kg_per_acre_per_crop: 2 of 18 species
- seed_cost_inr_per_unit: 2 of 18 species
- culture_period_months: 1 of 18 species
- crops_per_year_tn: 1 of 18 species
- aeration_common: 1 of 18 species

## Sources

- **FAO_CATLA** - FAO Cultured Aquatic Species fact sheet: Catla catla (2009), FAO CD-ROM mirror - <https://www.fao.org/fishery/docs/CDrom/aquaculture/I1129m/file/en/en_catla.htm>
- **FAO_ROHU** - FAO fact sheet: Labeo rohita (Mar 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-roho-labeo>
- **FAO_MRIGAL** - FAO fact sheet: Cirrhinus mrigala (Dec 2009), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-mrigal-carp>
- **FAO_CC** - FAO fact sheet: Cyprinus carpio (Jan 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-common-carp>
- **FAO_GC** - FAO fact sheet: Ctenopharyngodon idellus (Jan 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-grass-carp>
- **FAO_SC** - FAO fact sheet: Hypophthalmichthys molitrix (Mar 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-silver-carp>
- **FAO_TIL** - FAO fact sheet: Oreochromis niloticus (Jun 2010), FAO CD-ROM mirror - <https://www.fao.org/fishery/docs/CDrom/aquaculture/I1129m/file/en/en_niletilapia.htm>
- **FAO_PANG** - FAO fact sheet: Pangasius hypophthalmus (Jun 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquaculture-species-striped-catfish>
- **FAO_GRP** - FAO fact sheet: Macrobrachium rosenbergii (Apr 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquaculture-species-giant-river-prawn>
- **FAO_VAN** - FAO fact sheet: Penaeus vannamei (2009), FAO CD-ROM mirror - <https://www.fao.org/fishery/docs/CDrom/aquaculture/I1129m/file/en/en_whitelegshrimp.htm>
- **FAO_MON** - FAO fact sheet: Penaeus monodon (Jul 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-giant-tiger-prawn>
- **FAO_BAR** - FAO fact sheet: Lates calcarifer (Apr 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquaculture-species-barramundi>
- **FAO_MILK** - FAO fact sheet: Chanos chanos (Dec 2009), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-milkfish-chanos-chanos>
- **FAO_MILKBIO** - FAO/SPC milkfish biology chapter (Bagarinao), FAO document AC282E - <https://www.fao.org/4/ac282e/ac282e04.htm>
- **FAO_MUL** - FAO fact sheet: Mugil cephalus (Apr 2010), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquaculture-species-flathead-grey-mullet>
- **FAO_CRAB** - FAO fact sheet: Scylla serrata (Sep 2012), reproduced by The Fish Site - <https://thefishsite.com/articles/cultured-aquatic-species-indopacific-swamp-crab>
- **TNAU_COMP** - TNAU Agritech portal: Composite fish culture (farm enterprises page) - <https://agritech.tnau.ac.in/farm_enterprises/Farm%20enterprises_composite%20fish%20culture.html>
- **NABARD_INT** - NABARD model bankable project (2015): Intensive carp culture (catla + rohu), hosted by TNAU - <https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/4.Intensive_fish_culture_15.pdf>
- **NABARD_PANG** - NABARD model bankable project (2015): Pangasius culture, hosted by TNAU - <https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/3.Pangassius_culture_15.pdf>
- **NABARD_GIFT** - NABARD model bankable project (2015): GIFT tilapia culture, hosted by TNAU - <https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/6.GIFT_Tilapia_culture_15.pdf>
- **NABARD_VAN** - NABARD model bankable project (2015): Culture of L. vannamei, hosted by TNAU - <https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/5.Culture_of_Vannamei_white_legged_shrimp_15.pdf>
- **TNAU_PEARL** - TNAU Agritech portal: Pearl spot culture - <https://agritech.tnau.ac.in/fishery/fish_cul_brackish_pearlspot.html>
- **TNAU_SEABASS** - TNAU Agritech portal: Seabass culture - <https://agritech.tnau.ac.in/fishery/fish_cul_brackish_seabass.html>
- **TNAU_MILK** - TNAU Agritech portal: Milkfish culture - <https://agritech.tnau.ac.in/fishery/fish_cul_brackish_milkfish.html>
- **TNAU_CRAB** - TNAU Agritech portal: Mud crab fattening - <https://agritech.tnau.ac.in/fishery/fish_cul_brackish_mudcrab.html>
- **TNAU_MURREL** - TNAU Agritech portal: Murrel culture - <https://agritech.tnau.ac.in/fishery/fish_cul_freshwater_murrel.html>
- **TNAU_PRAWN** - TNAU Agritech portal: Freshwater prawn (scampi) farming - <https://agritech.tnau.ac.in/fishery/fish_freshwaterprawn.html>
- **TNAU_SHRIMP** - TNAU Agritech portal: Shrimp culture (species biology) - <https://agritech.tnau.ac.in/fishery/fish_cul_brackish_shrimps_area.html>
- **SLBC** - Govt of Tamil Nadu, Dept of Fisheries and Fishermen Welfare: Scale of Finance for working capital, inland fisheries 2024-25 (SLBC Tamil Nadu) - <https://www.slbctn.com/uploads/SoF/Inland%20Fisheries%202024-25.pdf>
- **TNPN** - Govt of Tamil Nadu: Fisheries Policy Note 2020-21 (Demand No. 7), p.109 - <https://www.fisheries.tn.gov.in/includes/assets/cms_uploads/pdf/glance/Fisheries_-_Policy_Note_2020-21_-_English_4605.pdf (mirror: https://fisheryprogress.org/sites/default/files/documents_actions/TN%20fisheries_Policy%20Note%202020_21%5B8276%5D.pdf)>
- **MPEDA_CROP** - MPEDA: Shrimp cropping pattern by state - <https://mpeda.gov.in/?page_id=645>
- **MPEDA_SHRIMP** - MPEDA farmers portal: Shrimp (L. vannamei and black tiger) BMP - <https://mpeda.gov.in/farmers/?page_id=1693>
- **MPEDA_GIFT** - MPEDA farmers portal: Tilapia (GIFT) - <https://mpeda.gov.in/farmers/?page_id=1720>
- **MPEDA_MULLET** - Sukumaran et al. (ICAR-CIBA), 'Grey mullet aquaculture in India', MPEDA Newsletter Vol X No 3, June 2022, pp.26-30 - <http://www.ciba.res.in/wp-content/uploads/2022/06/MNL-JUNE-2022-FOR-WEB-1-1.pdf>
- **CAA** - Coastal Aquaculture Authority: Guidelines for regulating coastal aquaculture (Annexure I) - <https://caa.gov.in/uploaded/doc/Guidelines-Englishnew.pdf>
- **RGCA** - MPEDA-RGCA seed and other products availability list as on 15.04.2025 - <https://rgca.co.in/assets/docs/sead_availability/2025/seed_availability_22_apr_2025.pdf>
- **FAO_TN** - Nandeesha, Sentilkumar & Antony Jesu Prabhu (2013) 'Feed management of major carps in India, with special reference to practices adopted in Tamil Nadu', FAO Fisheries and Aquaculture Technical Paper 583, pp.433-462 (Thanjavur field survey 2010) - <https://www.fao.org/fishery/docs/CDrom/T583/root/16.pdf>
- **THANJ** - Jayaraman (1997) 'Carp culture in Thanjavur district, Tamil Nadu: an economic analysis', Asian Fisheries Science 9:275-288 (survey 1992-93) - <https://www.asianfisheriessociety.org/publication/downloadfile.php?id=947&file=Y0dSbUx6QTJOVGsyT0RFd01ERXpOVFkxTVRBMU16a3VjR1Jt>
- **DTNEXT_PRICE** - DT Next, Chennai, 25 Apr 2026: 'Pricey freshwater fish fail to compensate for seafood demand' (Nagapattinam aqua farmer quoted) - <https://www.dtnext.in/news/chennai/pricey-freshwater-fish-fail-to-compensate-for-seafood-demand>
- **DTNEXT_INLAND** - DT Next, 11 Aug 2025: 'High potential for inland aquafarming visible in TN' - <https://www.dtnext.in/news/tamilnadu/high-potential-for-inland-aquafarming-visible-in-tn-842891>
- **CML** - commoditymarketlive.com wholesale fish price pages (national aggregate, May-Jun 2025) - <https://www.commoditymarketlive.com/fish-price/>
- **GOLDEN** - Golden Chennai 'Tamil Nadu fish price today' (21 Sep 2026; market level and city not stated) - <https://rates.goldenchennai.com/fish-price/tamil-nadu-fish-price-today/>
- **BENISON** - Benison Media, 7 Jul 2023: 'Flat vannamei prices leave Indian farmers eating costs' (Tamil Nadu farm-gate by count; Sea Gem Aqua) - <https://benisonmedia.com/flat-vannamei-prices-leave-indian-farmers-eating-costs-in-painful-year/>
- **UCN_MAY26** - Undercurrent News, 25 May 2026: 'India shrimp farmers protest falling prices, rising feed costs' (Andhra Pradesh) - <https://www.undercurrentnews.com/2026/05/25/india-shrimp-farmers-protest-falling-prices-rising-feed-costs/>
- **AAP2025** - Aqua Culture Asia Pacific, 9 Apr 2026: 'Asian shrimp in 2025: steady supply and price volatility' - <https://aquaasiapac.com/2026/04/09/asian-shrimp-in-2025-steady-supply-and-price-volatility/>
- **DC_FEED** - Deccan Chronicle, 19 Jun 2026: 'Aqua feed prices cut by Rs 4 per kilo after CM's call' (Andhra Pradesh) - <https://www.deccanchronicle.com/southern-states/andhra-pradesh/aqua-feed-prices-cut-by-rs-4-per-kilo-after-cms-call-1964619>
- **PLOS** - Comparative profitability of P. monodon and L. vannamei in India, PLOS ONE 2021 (Gujarat survey, 220 farms) - <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0250727>
- **ICSF_KARAIKAL** - ICSF news repost: 'It is profitable to culture Asian seabass fish in Tamil Nadu' (RGCA Karaikal demonstration farm; page carries no date - search metadata suggests Sept 2021) - <https://icsf.net/newss/it-is-profitable-to-culture-asian-seabass-fish-in-tamil-nadu/>
- **ICSF_CAGE** - ICSF news repost: 'Tamil Nadu: cashing in on sea bass in backwaters' (Vennangapattu cage farm; undated) - <https://icsf.net/newss/tamil-nadu-cashing-in-on-sea-bass-in-backwaters/>
- **IJPAB** - Chudasama et al. (2023) 'A short review of Asian seabass cultivation', Ind. J. Pure App. Biosci. 11(3):17-35 - <https://www.ijpab.com/form/2023%20Volume%2011,%20issue%203/IJPAB-2023-11-3-17-35.pdf>
- **ICAR_MILK** - ICAR, 10 Jul 2015: 'Breakthrough in artificial breeding of milkfish' (ICAR-CIBA Muttukadu) - <https://icar.org.in/node/8021>
- **CIBA_FIN** - ICAR-CIBA Finfish Culture Division page (MSMH milkfish model) - <https://ciba.res.in/?page_id=1365>
- **ONM_CRAB** - Onmanorama, 27 Jul 2026: 'Mud crab farming: how to turn low cost water crabs into a highly profitable business' (Kerala) - <https://www.onmanorama.com/news/kerala/2026/07/27/crab-farming-profitability1.html>
- **ONM_KARI** - Onmanorama, 30 Dec 2025: 'Karimeen prices fall in Kumarakom' (fisher-society retail prices by grade) - <https://www.onmanorama.com/news/kerala/2025/12/30/karimeen-prices-vembanad-lake.html>
- **SCYLLA_IN** - Marichamy & Rajapackiam (2001) 'The aquaculture of Scylla species in India', Asian Fisheries Science 14:231-238 - <https://www.asianfisheriessociety.org/publication/downloadfile.php?id=534&file=Y0dSbUx6QXpNelk0TmpBd01ERXpOVFU0T0RJeE5ETXVjR1Jt>
- **KERALA** - Dept of Fisheries, Govt of Kerala: Package of Aquaculture Practices (2021) - <https://fisheries.kerala.gov.in/sites/default/files/2021-02/Aquaculture%20Practices_compressed.pdf>
- **NFDB_MURREL** - NFDB 'Recent trends in aquaculture: Murrel culture in ponds' (undated; file metadata 2011-2015), hosted on Vikaspedia - <https://static.vikaspedia.in/mediastorage/document/Murrel_Culture_in_Ponds.pdf>
- **IJISEM** - Case study on Channa striata farming, Dharpally, Nizamabad, Telangana, IJISEM (article 662, 2025) - <https://ijisem.com/journal/index.php/ijisem/article/view/662>
- **TNPRAWN** - Preliminary observations on freshwater prawn farming in Tamil Nadu (Parangipettai), Int. J. Zool. Res. 2008 - <https://scialert.net/fulltext/?doi=ijzr.2008.72.76>
- **FS_ASSAM** - The Fish Site, 13 Sep 2024: 'Giant river prawns prove their worth in Assam' - <https://thefishsite.com/articles/giant-river-prawns-prove-their-worth-in-assam>
- **FS_GIFT** - The Fish Site, 24 Jun 2022: 'Can GIFT gain ground in eastern India?' (Odisha farms) - <https://thefishsite.com/articles/can-gift-gain-ground-in-eastern-india-odisha>
- **WAS_PANG** - World Aquaculture Society, Asian-Pacific Aquaculture 2019 Chennai abstract: 'Recent trends in pangasius farming, production and marketing in India' - <https://www.was.org/Meeting/Program/PaperDetail/154045>
- **BOYD** - Boyd, C.E. (2010) 'Dissolved oxygen concentrations in pond aquaculture', Global Seafood Alliance Advocate - <https://www.globalseafood.org/advocate/dissolved-oxygen-concentrations-pond-aquaculture/>
- **TRANDUY** - Tran-Duy et al. (2008) 'Effects of oxygen concentration and body weight on maximum feed intake, growth and hematological parameters of Nile tilapia', Aquaculture - <https://www.ecowin.org/pdf/documents/Tran-Duy%202008%20tilapia%20DO%20consumption.pdf>
- **IMCREV** - 'Comprehensive review on Indian major carps', Int. J. Fisheries and Aquatic Studies 2024; 12(1):1-12 - <https://www.fisheriesjournal.com/archives/2024/vol12issue1/PartA/11-6-20-676.pdf>
- **PMC_TIL** - Temperature and feeding frequency in juvenile Nile tilapia, BMC Vet Res 2024 (PMC11571909) - <https://pmc.ncbi.nlm.nih.gov/articles/PMC11571909/>
- **PERFECT** - Perfect Aqua Feeds blog, 9 Oct 2025: 'Fish feed prices in India 2025' (vendor content) - <https://www.perfectaquafeeds.com/post/fish-feed-prices-in-india-2025-a-comprehensive-comparison-and-buying-guide>
- **WIKI_TA** - Wikipedia interlanguage links (en -> ta) via API; Tamil article titles - <https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&lllang=ta&titles=Catla|Rohu|Mrigal%20carp|Common%20carp|Grass%20carp|Silver%20carp|Channa%20striata|Green%20chromide|Barramundi|Milkfish|Flathead%20grey%20mullet>
- **TAWIKI_LIST** - Tamil Wikipedia: மீன் வகைகள் பட்டியல் (list of fish types) - read via summariser, so names taken from it are labelled ASSUMED - <https://ta.wikipedia.org/wiki/%E0%AE%AE%E0%AF%80%E0%AE%A9%E0%AF%8D_%E0%AE%B5%E0%AE%95%E0%AF%88%E0%AE%95%E0%AE%B3%E0%AF%8D_%E0%AE%AA%E0%AE%9F%E0%AF%8D%E0%AE%9F%E0%AE%BF%E0%AE%AF%E0%AE%B2%E0%AF%8D>
- **SP_SEARCH** - S&P Global Commodity Insights, 3 Mar 2025 'Indian shrimp prices fall amid talks of recovering supply' - page returned HTTP 403; figure taken from search summary only - <https://spglobal.com/commodity-insights/en/news-research/latest-news/agriculture/030325-indian-shrimp-prices-fall-amid-talks-of-recovering-supply>
- **BS_FEED** - Business Standard, 13 Apr 2025 'Tariff impact: shrimp feed prices drop by Rs 4/kg' - page returned HTTP 403; figures from search summary only - <https://www.business-standard.com/industry/news/tariff-impact-shrimp-feed-prices-drop-by-4-kg-to-reimburse-farmers-125041300459_1.html>
- **AFS528** - 'Pond culture of mud crab Scylla serrata fed...' Asian Fisheries Society paper (id=528) - not read; water-quality optima from search summary only - <https://www.asianfisheriessociety.org/publication/downloadfile.php?id=528&file=Y0dSbUx6QTFORGc1TURjd01ERXpOVFU0T0RFeU16QXVjR1Jt>
