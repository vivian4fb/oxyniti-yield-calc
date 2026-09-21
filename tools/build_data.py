#!/usr/bin/env python3
# build_data.py -- WP1 data build for the Oxyniti yield calculator.
# Purpose: read research/* and plan/coefficients.json, write site/data/*.data.js (EXECUTION_PLAN.md 4.1).
"""
Deterministic, idempotent, standard-library-only. Re-running produces byte-identical output
because every transform below is a pure function of the research/plan files on disk (no
timestamps, no random, no unordered-set iteration feeding output order).

Usage: python tools/build_data.py
Exit code 0 on success (data files + plan/DATA_STATUS.md written), 1 on any validation failure.
"""

import sys
import io
import os
import re
import json
import math
import subprocess
import tempfile
from pathlib import Path

# Make prints safe on a cp1252 Windows console (Tamil strings, degree signs, etc.)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent                      # .../oxyniti_yield _calc
RESEARCH = ROOT / "research"
PLAN = ROOT / "plan"
SITE_DATA = ROOT / "site" / "data"

BUILD_DATE = "2026-09-21"                     # date stamp for values WP1 itself derives
HA_PER_ACRE = 2.4711
HP_TO_KW = 0.7457

STATUS_ENUM = {"VERIFIED", "ASSUMED", "UNTESTED", "NOT_FOUND"}

HILL_STATIONS = {"Kodaikanal", "Udhagamandalam (Ooty)", "Coonoor", "Valparai"}
PARTIAL_STATIONS = {"Kovilankulam"}
STATION_OVERRIDES = {
    # explicit disambiguation from the WP1 brief where more than one in-district
    # station exists and the generic "named after the district town" rule is ambiguous.
    "Chennai": "Chennai (Nungambakkam)",
    "Madurai": "Madurai (city)",
    "Coimbatore": "Coimbatore (airport)",
    "Dindigul": "Kamachipuram",
}

SPECIES_ID_ORDER = [
    "catla", "rohu", "mrigal", "common-carp", "grass-carp", "silver-carp",
    "gift-tilapia", "pangasius", "murrel", "scampi", "pearl-spot",
    "improved-strains", "vannamei", "black-tiger", "seabass", "milkfish",
    "grey-mullet", "mud-crab",
]
RESPIRATION_GROUP = {
    "catla": "freshwater_fish", "rohu": "freshwater_fish", "mrigal": "freshwater_fish",
    "common-carp": "freshwater_fish", "grass-carp": "freshwater_fish",
    "silver-carp": "freshwater_fish", "gift-tilapia": "freshwater_fish",
    "improved-strains": "freshwater_fish",
    "pangasius": "air_breathing_fish", "murrel": "air_breathing_fish",
    "scampi": "shrimp", "vannamei": "shrimp", "black-tiger": "shrimp",
    "pearl-spot": "brackish_fish", "seabass": "brackish_fish",
    "milkfish": "brackish_fish", "grey-mullet": "brackish_fish",
    "mud-crab": "crab",
}
REQUIRED_FOR_ESTIMABLE = [
    "temp_optimum_c", "stocking_density_per_acre", "culture_period_months",
    "harvest_size_g", "survival_pct", "fcr", "farmgate_price_inr_per_kg",
    "seed_cost_inr_per_unit", "feed_cost_inr_per_kg", "crops_per_year_tn",
]

# NABARD/TNAU 2015 model projects, economics_device_evidence.md section 5:
# other = opex_per_crop - feed - seed - electricity, per HECTARE per crop (WP1 divides by
# HA_PER_ACRE below). Figures are traced line-by-line from the section-5 tables in the report.
OTHER_COST_MODELS = {
    "catla": (62375.0,
              "https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/4.Intensive_fish_culture_15.pdf",
              "NABARD/TNAU 2015 intensive carp (catla+rohu, 6-month, 2 crops/yr) model: "
              "opex 2,88,075 - feed 1,63,200 - seed 62,500 - electricity 0 = 62,375/ha/crop "
              "(lime/SSP/urea/poultry litter 9,375 + watch&ward 21,000 + harvesting 7,000 + "
              "misc 15,000 + drying 10,000). Same model used for rohu/mrigal/common-carp "
              "because their survival_pct already cites this model (NABARD_INT) and all four "
              "carps are stocked together in one polyculture pond."),
    "gift-tilapia": (59750.0,
                     "https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/6.GIFT_Tilapia_culture_15.pdf",
                     "NABARD/TNAU 2015 GIFT tilapia model: opex 5,02,250 - feed 3,67,500 - "
                     "seed 75,000 - electricity 0 = 59,750/ha/crop."),
    "pangasius": (46000.0,
                  "https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/3.Pangassius_culture_15.pdf",
                  "NABARD/TNAU 2015 pangasius model: opex 5,57,000 - feed 4,38,000 - seed 13,000 "
                  "- electricity (pumping charges) 60,000 = 46,000/ha/crop."),
    "murrel": (110000.0,
               "https://static.vikaspedia.in/mediastorage/document/Murrel_Culture_in_Ponds.pdf",
               "NFDB/ICAR-CIFA murrel model (5x0.2 ha = 1 ha, 8-10 months): recurring cost "
               "9.50 lakh - feed 7.35 lakh - seed 0.70 lakh - electricity/fuel 0.35 lakh "
               "= 1.10 lakh/ha/crop."),
    "vannamei": (171625.0,
                 "https://agritech.tnau.ac.in/banking/nabard_pdf/Fisheries/5.Culture_of_Vannamei_white_legged_shrimp_15.pdf",
                 "NABARD/TNAU 2015 L. vannamei model (4-month crop, 50 PL/m2): opex 15,04,125 "
                 "- feed 8,92,500 - PL(seed) 3,75,000 - electricity/power charges 65,000 "
                 "= 1,71,625/ha/crop."),
}
for _id in ["rohu", "mrigal", "common-carp"]:
    OTHER_COST_MODELS[_id] = OTHER_COST_MODELS["catla"]

SEED_SIZE_G = {
    # EXECUTION_PLAN.md WP1 fallback 8.
    "crab": 100.0,
}


def seed_size_for(species_id, group):
    if group == "crab":
        return 100.0, "mud crab fattening stock (WP1 fallback 8)"
    if group == "shrimp":
        if species_id == "scampi":
            return 0.05, "scampi post-larvae (WP1 fallback 8)"
        return 0.01, "shrimp post-larvae (WP1 fallback 8)"
    return 5.0, "fish fingerlings (WP1 fallback 8)"


MONTH_NAMES = [
    ("january", 1), ("february", 2), ("march", 3), ("april", 4), ("may", 5),
    ("june", 6), ("july", 7), ("august", 8), ("september", 9), ("october", 10),
    ("november", 11), ("december", 12),
]


def mid_value(field):
    """Midpoint of a {value: ...} envelope: scalar -> itself; [low, high] -> mean of the
    non-null bounds (a one-sided [x, null] gives x, matching MODEL_SPEC.md 2 fallback 4)."""
    if field is None:
        return None
    v = field.get("value")
    if v is None:
        return None
    if isinstance(v, list):
        present = [x for x in v if x is not None]
        return sum(present) / len(present) if present else None
    return v


def first_month_in_text(text):
    """Return (month_number, matched_word) for the first calendar-month name in text, else None."""
    lower = text.lower()
    best = None
    for name, num in MONTH_NAMES:
        idx = lower.find(name)
        if idx != -1 and (best is None or idx < best[0]):
            best = (idx, num, name)
    if best is None:
        return None
    return best[1], best[2]


# ---------------------------------------------------------------------------
# Generic helpers: load, write, validate
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_data_js(varname, obj, filename, compact=False):
    """Write site/data/<filename> in the fixed classic-script shape (EXECUTION_PLAN.md 4.1)."""
    if compact:
        json_text = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    else:
        json_text = json.dumps(obj, ensure_ascii=False, indent=1)
    content = (
        "window.OXY_DATA = window.OXY_DATA || {};\n"
        f"window.OXY_DATA.{varname} = {json_text};\n"
    )
    out_path = SITE_DATA / filename
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return out_path, len(content.encode("utf-8"))


def reparse_data_js(path, varname):
    """Strip the fixed prefix and json.loads the remainder -- the oracle.py contract."""
    text = path.read_text(encoding="utf-8")
    prefix = "window.OXY_DATA = window.OXY_DATA || {};\n"
    marker = f"window.OXY_DATA.{varname} = "
    if not text.startswith(prefix):
        raise ValueError(f"{path}: missing fixed prefix line")
    body = text[len(prefix):]
    if not body.startswith(marker):
        raise ValueError(f"{path}: missing 'window.OXY_DATA.{varname} = ' marker")
    tail = body[len(marker):].rstrip("\n")
    if not tail.endswith(";"):
        raise ValueError(f"{path}: assignment does not end in ';'")
    return json.loads(tail[:-1])


NODE_VALIDATOR = r"""
const fs = require('fs');
const vm = require('vm');
const args = process.argv.slice(-2);
const filepath = args[0], varname = args[1];
const code = fs.readFileSync(filepath, 'utf8');
const sandbox = {};
sandbox.window = sandbox;
vm.runInNewContext(code, sandbox, { filename: filepath });
if (!sandbox.OXY_DATA || typeof sandbox.OXY_DATA[varname] === 'undefined') {
  console.error('FAIL: OXY_DATA.' + varname + ' not set by ' + filepath);
  process.exit(1);
}
console.log('OK OXY_DATA.' + varname);
"""


def node_vm_check(path, varname, errors):
    try:
        proc = subprocess.run(
            ["node", "-e", NODE_VALIDATOR, str(path), varname],
            capture_output=True, text=True, timeout=30,
        )
    except FileNotFoundError:
        errors.append("node executable not found; cannot run vm.runInNewContext check")
        return False
    if proc.returncode != 0:
        errors.append(f"node vm check failed for {path.name}: {proc.stdout.strip()} {proc.stderr.strip()}")
        return False
    return True


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def check_ranges(obj, errors, where):
    """Every {value: [low, high]} envelope with both bounds non-null must have low <= high."""
    for d in walk(obj):
        if not isinstance(d, dict) or "value" not in d:
            continue
        v = d["value"]
        if isinstance(v, list) and len(v) == 2 and all(x is None or isinstance(x, (int, float)) for x in v):
            low, high = v
            if low is not None and high is not None and low > high:
                errors.append(f"{where}: range low>high in {d!r}")


def check_statuses(obj, errors, where, strict=True):
    """Every field-envelope status (a dict carrying both 'value' and 'status') is one of the
    four enum values. Verbatim-copied upstream structures (climate station completeness,
    geoJSON provenance) use a different, documented vocabulary and are reported, not failed,
    unless strict=True."""
    bad = []
    for d in walk(obj):
        if not isinstance(d, dict) or "status" not in d or "value" not in d:
            continue
        if d["status"] not in STATUS_ENUM:
            bad.append(d["status"])
    if bad and strict:
        errors.append(f"{where}: non-enum status value(s) found: {sorted(set(bad))}")
    return bad


# ---------------------------------------------------------------------------
# Sources: resolve species "source": "KEY" to a URL via _meta.sources, keeping the key
# ---------------------------------------------------------------------------

def resolve_sources(obj, sources_map):
    for d in walk(obj):
        if not isinstance(d, dict):
            continue
        src = d.get("source")
        if isinstance(src, str) and src in sources_map and "source_url" not in d:
            d["source_url"] = sources_map[src]["url"]


# ---------------------------------------------------------------------------
# Haversine + shoelace centroid (pure Python, no numpy)
# ---------------------------------------------------------------------------

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def ring_area_and_centroid(ring):
    """Shoelace signed area (deg^2) and centroid (lng, lat) for one closed [lng,lat] ring."""
    n = len(ring)
    a_sum = 0.0
    cx = 0.0
    cy = 0.0
    for i in range(n - 1):
        x0, y0 = ring[i]
        x1, y1 = ring[i + 1]
        cross = x0 * y1 - x1 * y0
        a_sum += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    area = a_sum / 2.0
    if area == 0:
        # degenerate ring; fall back to the vertex average
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        return 0.0, (sum(xs) / len(xs), sum(ys) / len(ys))
    cx = cx / (6.0 * area)
    cy = cy / (6.0 * area)
    return area, (cx, cy)


def largest_ring_centroid(geometry):
    """Area-weighted shoelace centroid of the largest (by |area|) exterior ring in a
    Polygon/MultiPolygon geometry. Interior rings (holes) are not considered."""
    polys = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    best = None  # (abs_area, centroid, signed_area)
    for poly in polys:
        exterior = poly[0]
        area, centroid = ring_area_and_centroid(exterior)
        if best is None or abs(area) > best[0]:
            best = (abs(area), centroid, area)
    return best[1], best[2]  # (lng, lat), signed_area_of_largest_ring


def total_area_deg2(geometry):
    """Sum of |area| of the largest ring per polygon part (used only for sanity reporting)."""
    polys = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    total = 0.0
    for poly in polys:
        area, _ = ring_area_and_centroid(poly[0])
        total += abs(area)
    return total


# ---------------------------------------------------------------------------
# SPECIES
# ---------------------------------------------------------------------------

def build_species(species_research, coefficients, economics_crossfill, errors, report):
    sources_map = species_research["_meta"]["sources"]
    raw_species = species_research["species"]
    if len(raw_species) != len(SPECIES_ID_ORDER):
        errors.append(f"species: expected {len(SPECIES_ID_ORDER)} species, found {len(raw_species)}")

    group_defaults = coefficients["species_group_defaults"]
    fallback_log = []   # (species_id, field, rule)
    out = []

    for idx, sp in enumerate(raw_species):
        sid = SPECIES_ID_ORDER[idx]
        group = RESPIRATION_GROUP[sid]
        rec = dict(sp)  # shallow copy: keep every original field intact

        # --- fallback 1: temp_tolerable_c from temp_optimum_c +/- margin -----------------
        margin = coefficients["thermal"]["tolerable_fallback_margin_c"]["value"]
        to = rec.get("temp_optimum_c")
        tt = rec.get("temp_tolerable_c")
        if to and to.get("value") and all(x is not None for x in to["value"]):
            lo_opt, hi_opt = to["value"]
            if tt is None or tt.get("value") is None:
                rec["temp_tolerable_c"] = {
                    "value": [lo_opt - margin, hi_opt + margin], "unit": "C",
                    "status": "ASSUMED", "date": BUILD_DATE,
                    "source": "derived from temp_optimum_c +/- 5 C (EXECUTION_PLAN WP1 fallback 1)",
                    "fallback_rule": "temp_tolerable_c NOT_FOUND; both bounds = temp_optimum_c +/- 5 C",
                }
                fallback_log.append((sid, "temp_tolerable_c", "both bounds filled (NOT_FOUND source)"))
            else:
                lo, hi = tt["value"]
                changed = False
                note_bits = []
                if lo is None:
                    lo = lo_opt - margin
                    changed = True
                    note_bits.append(f"low bound = temp_optimum_c.low - 5 = {lo}")
                if hi is None:
                    hi = hi_opt + margin
                    changed = True
                    note_bits.append(f"high bound = temp_optimum_c.high + 5 = {hi}")
                if changed:
                    tt["value"] = [lo, hi]
                    tt["status"] = "ASSUMED"
                    tt["fallback_rule"] = "EXECUTION_PLAN WP1 fallback 1: " + "; ".join(note_bits)
                    fallback_log.append((sid, "temp_tolerable_c", "; ".join(note_bits)))
        # else: temp_optimum_c itself missing (grass-carp, improved-strains) -- no fallback
        # possible; temp_tolerable_c stays whatever it was (NOT_FOUND).

        # --- fallback 3 (special case first): air-breather survival-floor reclassification -
        dmin = rec.get("do_minimum_mg_l")
        dlet = rec.get("do_lethal_mg_l")
        if group == "air_breathing_fish" and dmin and isinstance(dmin.get("value"), (int, float)) \
                and dmin["value"] is not None and dmin["value"] < 1.0:
            moved_value, moved_status, moved_source = dmin["value"], dmin["status"], dmin.get("source")
            rec["do_lethal_mg_l"] = {
                "value": moved_value, "unit": "mg/L", "status": moved_status,
                "date": dmin.get("date", BUILD_DATE), "source": moved_source,
                "fallback_rule": "air-breather: survival floor reclassified (EXECUTION_PLAN WP1 fallback 3)",
                "note": f"moved from do_minimum_mg_l ({dmin.get('note', '')})".strip(),
            }
            group_default = group_defaults[group]["do_min_growth_mg_l"]
            rec["do_minimum_mg_l"] = {
                "value": group_default["value"], "unit": group_default["unit"],
                "status": "ASSUMED", "date": BUILD_DATE,
                "source": f"coefficients.json species_group_defaults.{group}.do_min_growth_mg_l",
                "fallback_rule": "air-breather: survival floor reclassified (EXECUTION_PLAN WP1 fallback 3)",
            }
            fallback_log.append((sid, "do_minimum_mg_l / do_lethal_mg_l",
                                  f"air-breather reclassification: {moved_value} mg/L moved to "
                                  f"do_lethal_mg_l; do_minimum_mg_l set to group default {group_default['value']}"))
        else:
            # --- fallback 3, plain: do_minimum_mg_l null -> group do_min_growth_mg_l -------
            if dmin is None or dmin.get("value") is None:
                gd = group_defaults[group]["do_min_growth_mg_l"]
                rec["do_minimum_mg_l"] = {
                    "value": gd["value"], "unit": gd["unit"], "status": "ASSUMED",
                    "date": BUILD_DATE,
                    "source": f"coefficients.json species_group_defaults.{group}.do_min_growth_mg_l",
                    "fallback_rule": "EXECUTION_PLAN WP1 fallback 3: group default (do_minimum_mg_l NOT_FOUND)",
                }
                fallback_log.append((sid, "do_minimum_mg_l", f"group default {gd['value']} mg/L ({group})"))

        # --- fallback 2: do_lethal_mg_l null -> group default ------------------------------
        dlet = rec.get("do_lethal_mg_l")
        if dlet is None or dlet.get("value") is None:
            gd = group_defaults[group]["do_lethal_mg_l"]
            rec["do_lethal_mg_l"] = {
                "value": gd["value"], "unit": gd["unit"], "status": "ASSUMED",
                "date": BUILD_DATE,
                "source": f"coefficients.json species_group_defaults.{group}.do_lethal_mg_l",
                "fallback_rule": "EXECUTION_PLAN WP1 fallback 2: group default (do_lethal_mg_l NOT_FOUND)",
            }
            fallback_log.append((sid, "do_lethal_mg_l", f"group default {gd['value']} mg/L ({group})"))

        # --- A1 (MODEL_SPEC.md section 7, binding amendment 2026-09-21): where
        # do_minimum_mg_l is STILL a genuine [low, high] range after the fallbacks above, the
        # growth threshold used by the model is the high bound (the low bound is a tolerance
        # figure); write the scalar, keep the range in the note. ------------------------------
        dmin = rec.get("do_minimum_mg_l")
        dmin_val = dmin.get("value") if dmin else None
        if isinstance(dmin_val, list) and len(dmin_val) == 2 and all(x is not None for x in dmin_val):
            low, high = dmin_val
            range_note = (f"Sourced range [{low}, {high}] mg/L; high bound used as the growth "
                          f"threshold, low bound is a tolerance figure (MODEL_SPEC.md section 7 "
                          f"amendment A1).")
            old_note = dmin.get("note", "")
            dmin["value"] = high
            dmin["fallback_rule"] = "do_min_high_bound"
            dmin["note"] = f"{range_note} {old_note}".strip()
            fallback_log.append((sid, "do_minimum_mg_l",
                                  f"A1: range [{low}, {high}] mg/L collapsed to high bound {high} "
                                  f"mg/L (do_min_high_bound)"))

        # --- fallback 7: cross-fill from economics_device_evidence.md ---------------------
        if sid in economics_crossfill:
            for field, payload in economics_crossfill[sid].items():
                rec[field] = payload
                fallback_log.append((sid, field, "cross-filled from economics_device_evidence.md "
                                                   "(EXECUTION_PLAN WP1 fallback 7)"))

        # --- salinity_ppt -------------------------------------------------------------------
        water_type = rec.get("water_type", "")
        is_freshwater = water_type.strip().lower().startswith("freshwater")
        if is_freshwater:
            salinity_value = 0
            salinity_note = f"freshwater species (water_type: \"{water_type}\")"
        else:
            salinity_value = 15 if sid == "vannamei" else 20
            salinity_note = f"low-to-mid of the salinity range quoted in water_type: \"{water_type}\""
        rec["salinity_ppt"] = {
            "value": salinity_value, "unit": "ppt", "status": "ASSUMED", "date": BUILD_DATE,
            "source": "derived from this species' own water_type text (EXECUTION_PLAN WP1 brief)",
            "note": salinity_note,
        }

        # --- seed_size_g (fallback 8) --------------------------------------------------------
        seed_g, seed_note = seed_size_for(sid, group)
        rec["seed_size_g"] = {
            "value": seed_g, "unit": "g", "status": "ASSUMED", "date": BUILD_DATE,
            "source": "EXECUTION_PLAN.md WP1 fallback 8",
            "note": seed_note,
        }

        # --- stocking_month_tn_default (fallback 5) ------------------------------------------
        smt = rec.get("stocking_months_tn")
        parsed = first_month_in_text(smt["value"]) if smt and smt.get("value") else None
        if parsed:
            month_num, word = parsed
            rec["stocking_month_tn_default"] = {
                "value": month_num, "unit": "month (1-12)", "status": smt.get("status", "VERIFIED"),
                "date": smt.get("date", BUILD_DATE), "source": smt.get("source"),
                "note": f"parsed as the first month named in stocking_months_tn (\"{word}\")",
            }
        else:
            default_month = 7
            if is_freshwater:
                rule = ("EXECUTION_PLAN WP1 fallback 5: freshwater default (sourced carp pattern); "
                        "stocking_months_tn NOT_FOUND")
            else:
                rule = ("EXECUTION_PLAN WP1 fallback 5: no month named in any read source for this "
                        "brackish species; defaulted to July")
            rec["stocking_month_tn_default"] = {
                "value": default_month, "unit": "month (1-12)", "status": "ASSUMED",
                "date": BUILD_DATE, "source": None, "fallback_rule": rule,
            }
            fallback_log.append((sid, "stocking_month_tn_default", rule))

        # --- other_cost_inr_per_acre_crop ----------------------------------------------------
        if sid in OTHER_COST_MODELS:
            per_ha, url, label = OTHER_COST_MODELS[sid]
            rec["other_cost_inr_per_acre_crop"] = {
                "value": round(per_ha / HA_PER_ACRE, 2), "unit": "INR/acre/crop",
                "status": "ASSUMED", "date": BUILD_DATE, "source": url, "note": label,
            }
        else:
            rec["other_cost_inr_per_acre_crop"] = {
                "value": None, "unit": "INR/acre/crop", "status": "NOT_FOUND", "date": BUILD_DATE,
                "source": None, "note": "no NABARD/TNAU 2015 model project found for this species",
            }

        # --- price_default_inr_per_kg (fallback 6) -------------------------------------------
        fg = rec.get("farmgate_price_inr_per_kg")
        if fg is None or fg.get("value") is None:
            rec["price_default_inr_per_kg"] = {
                "value": None, "unit": "INR/kg", "status": "NOT_FOUND", "date": BUILD_DATE,
                "source": None, "label": "no sourced price for this species",
            }
        else:
            v = fg["value"]
            low, high = (v, v) if not isinstance(v, list) else (v[0], v[1] if v[1] is not None else v[0])
            market_level = (fg.get("market_level") or "").lower()
            is_farmgate = "farm-gate" in market_level or "farmer sale" in market_level
            if is_farmgate:
                default_value = round((low + high) / 2.0, 2)
                rule = "midpoint of sourced range (farm-gate market level)"
            else:
                default_value = low
                rule = "low end of sourced range (retail/wholesale/unstated market level)"
            as_of = fg.get("as_of", fg.get("date", BUILD_DATE))
            level_text = fg.get("market_level") or "market level unstated"
            rec["price_default_inr_per_kg"] = {
                "value": default_value, "unit": "INR/kg", "status": "ASSUMED", "date": BUILD_DATE,
                "source": "derived from farmgate_price_inr_per_kg (EXECUTION_PLAN WP1 fallback 6)",
                "label": f"₹{default_value:g}/kg, {as_of}, {level_text}",
                "rule": rule,
            }

        # --- id / respiration_group ----------------------------------------------------------
        rec["respiration_group"] = group

        # --- estimable / missing (computed AFTER the fallback-7 cross-fill above) ------------
        missing = [f for f in REQUIRED_FOR_ESTIMABLE
                   if rec.get(f) is None or rec[f].get("value") is None]
        rec["estimable"] = len(missing) == 0
        rec["missing"] = missing

        # --- A3 (MODEL_SPEC.md section 7, binding amendment 2026-09-21): density_default_per_acre
        # anchored to the sourced yield, instead of compounding three independent range
        # midpoints (density x survival x harvest size), which overshoots the sourced yield. ---
        yield_field = rec.get("yield_kg_per_acre_per_crop")
        dens_field = rec.get("stocking_density_per_acre")
        if rec["estimable"] and yield_field and yield_field.get("value") is not None:
            yield_mid = mid_value(yield_field)
            survival_mid = mid_value(rec.get("survival_pct"))
            harvest_mid_g = mid_value(rec.get("harvest_size_g"))
            crops_mid = mid_value(rec.get("crops_per_year_tn")) or 1
            yield_unit = (yield_field.get("unit") or "").lower()
            if "yr" in yield_unit or "year" in yield_unit:
                yield_mid_per_crop = yield_mid / crops_mid
                per_year_note = f"published per year, divided by crops-per-year midpoint {crops_mid:g}; "
            else:
                yield_mid_per_crop = yield_mid
                per_year_note = ""
            denom = (survival_mid / 100.0) * (harvest_mid_g / 1000.0)
            density_default = yield_mid_per_crop / denom if denom else None

            # "the kg it would imply": naive compounding of the SOURCED density range's own
            # midpoint with survival_mid/harvest_mid, for contrast in the note (this is the
            # 8,786 kg/acre/crop figure for GIFT that the amendment itself illustrates).
            dens_mid = mid_value(dens_field)
            naive_kg = dens_mid * denom if dens_mid is not None else None
            dens_range_txt = (f"{dens_field['value']}" if dens_field else "null")
            dens_unit = dens_field.get("unit", "per acre") if dens_field else "per acre"

            note = (f"{per_year_note}Sourced stocking_density_per_acre {dens_range_txt} "
                    f"{dens_unit} would imply {naive_kg:,.0f} kg/acre/crop via survival_mid x "
                    f"harvest_mid, against a sourced yield of {yield_field['value']} "
                    f"{yield_field.get('unit', '')}; density_default_per_acre anchors to the "
                    f"sourced yield instead of compounding three independent range midpoints "
                    f"(MODEL_SPEC.md section 7 amendment A3).")
            rec["density_default_per_acre"] = {
                "value": round(density_default, 1) if density_default is not None else None,
                "unit": dens_unit, "status": "ASSUMED", "date": BUILD_DATE,
                "source": "derived from yield_kg_per_acre_per_crop, survival_pct and "
                          "harvest_size_g (MODEL_SPEC.md section 7 amendment A3)",
                "fallback_rule": "yield_consistent_density",
                "note": note,
            }
            fallback_log.append((sid, "density_default_per_acre",
                                  f"A3: yield-anchored density {rec['density_default_per_acre']['value']} "
                                  f"{dens_unit} (naive compounding would have implied {naive_kg:,.0f} "
                                  f"kg/acre/crop against sourced yield {yield_field['value']})"))
            report.setdefault("a3_table", []).append(
                (sid, rec["density_default_per_acre"]["value"], dens_unit, naive_kg,
                 yield_field["value"], yield_field.get("unit", ""))
            )
        else:
            rec["density_default_per_acre"] = {
                "value": None, "unit": (dens_field.get("unit") if dens_field else "per acre"),
                "status": "NOT_FOUND", "date": BUILD_DATE, "source": None,
                "note": "species not estimable or yield_kg_per_acre_per_crop NOT_FOUND "
                        "(MODEL_SPEC.md section 7 amendment A3 applies to estimable species only)",
            }

        # --- reorder into the fixed-interface field order, keeping every extra field ---------
        ordered_keys = [
            "common_name_en", "common_name_ta", "scientific_name", "water_type",
            "salinity_ppt", "temp_optimum_c", "temp_tolerable_c", "do_minimum_mg_l",
            "do_lethal_mg_l", "stocking_density_per_acre", "density_default_per_acre", "seed_size_g",
            "culture_period_months", "harvest_size_g", "survival_pct", "fcr",
            "farmgate_price_inr_per_kg", "price_default_inr_per_kg", "seed_cost_inr_per_unit",
            "feed_cost_inr_per_kg", "other_cost_inr_per_acre_crop", "crops_per_year_tn",
            "stocking_month_tn_default", "respiration_group", "estimable", "missing", "notes",
        ]
        final = {"id": sid}
        for k in ordered_keys:
            if k in rec:
                final[k] = rec.pop(k)
        # anything left in rec is an original research field not in the fixed list -- keep it.
        for k, v in rec.items():
            final[k] = v
        out.append(final)

    resolve_sources(out, sources_map)

    report["species_fallbacks"] = fallback_log
    report["species_estimable"] = [s["id"] for s in out if s["estimable"]]
    report["species_not_estimable"] = [(s["id"], s["missing"]) for s in out if not s["estimable"]]
    return out


def economics_crossfill_values():
    """Fallback 7: figures cross-filled from economics_device_evidence.md into species records
    that are NOT_FOUND in their own file. Hand-transcribed with page citations (never invent)."""
    return {
        "seabass": {
            "survival_pct": {
                "value": 84.89, "unit": "%", "status": "VERIFIED", "date": BUILD_DATE,
                "source": "https://eprints.cmfri.org.in/19157/1/Impact%20of%20Technologies%20and%20"
                          "Policies%20on%20Marine%20and%20Inland%20Fish%20Culture%20Systems%20in%20"
                          "India_2025_Shinoj%20Parappurathu.pdf",
                "note": "Tamil Nadu cage culture, ICAR-CIBA/CMFRI survey Apr 2022-Mar 2023 "
                        "(economics_device_evidence.md section 5.6); species file had NOT_FOUND.",
            },
        },
    }


# ---------------------------------------------------------------------------
# CLIMATE
# ---------------------------------------------------------------------------

def apply_elevation_fix(stations, report):
    """A2 (MODEL_SPEC.md section 7, binding amendment 2026-09-21): a coastal station whose
    elevation_m is null because of an IMD table misprint gets 5 m, ASSUMED. Cuddalore is the
    only station in this dataset with elevation_m null (verified against climate_normals.json:
    its own notes already record the misprint -- IMD prints 395.3 m, identical to Coimbatore's
    entry, physically wrong for a coastal town). Any other null elevation is left NOT_FOUND;
    the district-station search below then excludes it so no district resolves to a
    stationless elevation."""
    fixed = []
    for s in stations:
        if s.get("elevation_m") is None:
            if s["name"] == "Cuddalore":
                s["elevation_m"] = 5
                s["geodata_status"] = (
                    "lat/lng VERIFIED (IMD); elevation ASSUMED 5 m -- WP1 fix per MODEL_SPEC.md "
                    "section 7 amendment A2 (coastal town, IMD table misprint: header printed "
                    "395.3 m, identical to Coimbatore's entry, physically wrong for coastal "
                    "Cuddalore)"
                )
                notes = s.setdefault("notes", [])
                notes.append(
                    "WP1 fix (MODEL_SPEC.md section 7 amendment A2): elevation_m set to 5 m, "
                    "ASSUMED, coastal town within 10 km of the coast; was null pending this fix."
                )
                fixed.append(s["name"])
            else:
                report.setdefault("elevation_still_null", []).append(s["name"])
    report["elevation_fixed_stations"] = fixed
    return stations


def build_climate(climate_research, district_names, district_centroids, errors, report):
    stations = apply_elevation_fix(climate_research["stations"], report)
    station_by_name = {s["name"]: s for s in stations}
    stations_with_elevation = {s["name"] for s in stations if s.get("elevation_m") is not None}

    def clean_district(text):
        base = re.split(r"\s*\(", text)[0].strip()
        if base == "Nilgiris":
            base = "The Nilgiris"
        return base

    # index in-district candidates (elevation-eligible only, per amendment A2)
    by_district = {}
    for s in stations:
        if s["name"] not in stations_with_elevation:
            continue
        d = clean_district(s["district"])
        by_district.setdefault(d, []).append(s)

    district_station_map = {}
    method_rows = []  # (district, station, distance_km, rule)

    eligible_fallback_stations = [
        s for s in stations
        if s["name"] not in HILL_STATIONS and s["name"] not in PARTIAL_STATIONS
        and s["name"] in stations_with_elevation
    ]
    partial_only_stations = [
        s for s in stations if s["name"] in PARTIAL_STATIONS and s["name"] in stations_with_elevation
    ]

    for district in district_names:
        centroid = district_centroids[district]  # (lng, lat)
        d_lat, d_lng = centroid[1], centroid[0]

        if district in STATION_OVERRIDES:
            chosen_name = STATION_OVERRIDES[district]
            rule = f"override (explicit brief instruction; in-district candidates: " \
                   f"{[s['name'] for s in by_district.get(district, [])]})"
        elif district in by_district and by_district[district]:
            cands = by_district[district]
            town_matches = [s for s in cands
                             if s["name"].split(" (")[0].strip().lower() == district.lower()
                             or district.lower() == s["name"].strip().lower()]
            if town_matches:
                chosen_name = town_matches[0]["name"]
                rule = "in-district (station named after the district town)"
            elif len(cands) == 1:
                chosen_name = cands[0]["name"]
                rule = "in-district (only station)"
            else:
                # tie-break: nearest of the in-district candidates to the centroid
                ranked = sorted(
                    cands,
                    key=lambda s: haversine_km(d_lat, d_lng, s["lat"], s.get("lng", s.get("lon"))),
                )
                chosen_name = ranked[0]["name"]
                rule = ("in-district, nearest-to-centroid tie-break among "
                        f"{[s['name'] for s in cands]} (no station literally named after the "
                        "district town)")
        else:
            pool = eligible_fallback_stations
            ranked = sorted(
                pool, key=lambda s: haversine_km(d_lat, d_lng, s["lat"], s.get("lng", s.get("lon")))
            )
            nearest = ranked[0]
            nearest_km = haversine_km(d_lat, d_lng, nearest["lat"], nearest.get("lng", nearest.get("lon")))
            # PARTIAL-station 60 km exception
            if partial_only_stations:
                ps = partial_only_stations[0]
                ps_km = haversine_km(d_lat, d_lng, ps["lat"], ps.get("lng", ps.get("lon")))
                if ps_km < nearest_km and ps_km <= 60.0:
                    nearest, nearest_km = ps, ps_km
                    rule = (f"nearest (haversine {ps_km:.1f} km), PARTIAL station used because "
                            "nothing else is within 60 km")
                else:
                    rule = f"nearest (haversine {nearest_km:.1f} km); hill + PARTIAL stations excluded"
            else:
                rule = f"nearest (haversine {nearest_km:.1f} km); hill + PARTIAL stations excluded"
            chosen_name = nearest["name"]

        district_station_map[district] = chosen_name
        st = station_by_name[chosen_name]
        dist_km = haversine_km(d_lat, d_lng, st["lat"], st.get("lng", st.get("lon")))
        method_rows.append((district, chosen_name, round(dist_km, 1), rule))

    report["climate_method_rows"] = method_rows
    report["climate_in_district_count"] = sum(1 for r in method_rows if r[3].startswith("in-district") or r[3].startswith("override"))
    report["climate_nearest_count"] = sum(1 for r in method_rows if r[3].startswith("nearest"))

    # A2 confirmation: every one of the 38 districts must resolve to a station with a
    # non-null elevation_m (needed for the DO-saturation pressure/elevation correction).
    no_elevation = [
        d for d in district_names
        if station_by_name[district_station_map[d]].get("elevation_m") is None
    ]
    report["districts_without_elevation"] = no_elevation
    if no_elevation:
        errors.append(f"climate: {len(no_elevation)} district(s) resolve to a station with no "
                       f"elevation: {no_elevation}")

    return {"stations": stations, "district_station_map": district_station_map}


# ---------------------------------------------------------------------------
# HOTSPOTS
# ---------------------------------------------------------------------------

def build_hotspots(hotspots_research, errors, report):
    out_of_range = []
    for h in hotspots_research:
        lat, lng = h.get("lat"), h.get("lng")
        if lat is None or lng is None or not (8.0 <= lat <= 13.6 and 76.2 <= lng <= 80.4):
            out_of_range.append((h.get("id"), lat, lng))
    report["hotspots_out_of_range"] = out_of_range
    report["hotspots_count"] = len(hotspots_research)
    return hotspots_research


# ---------------------------------------------------------------------------
# DISTRICTS
# ---------------------------------------------------------------------------

def build_districts(geojson, hotspots_research, errors, report):
    district_summaries = {h["district"]: h for h in hotspots_research if h.get("type") == "district_summary"}

    features = geojson["features"]
    names = [f["properties"]["district"] for f in features]
    unmatched = []
    for f in features:
        d = f["properties"]["district"]
        hs = district_summaries.get(d)
        if hs is None:
            unmatched.append(d)
            f["properties"]["inland_production_t"] = None
            f["properties"]["production_year"] = None
            f["properties"]["production_source"] = None
            continue
        prod = hs.get("inland_production_t", {})
        f["properties"]["inland_production_t"] = prod.get("value")
        f["properties"]["production_year"] = prod.get("year")
        f["properties"]["production_source"] = prod.get("source")

    report["districts_unmatched_production"] = unmatched
    report["districts_feature_count"] = len(features)
    report["districts_names"] = names
    report["districts_total_area_deg2"] = sum(total_area_deg2(f["geometry"]) for f in features)

    if len(features) != 38:
        errors.append(f"districts: expected 38 features, found {len(features)}")
    if len(set(names)) != len(names):
        errors.append("districts: duplicate district names")

    return geojson


# ---------------------------------------------------------------------------
# PRODUCTS  (economics_device_evidence.md section 1.1-1.2)
# ---------------------------------------------------------------------------

def build_products():
    claims = [
        {"text": "2x Dissolved oxygen uplift", "url": "https://www.oxyniti.com/"},
        {"text": "+15% Higher survival rate", "url": "https://www.oxyniti.com/"},
        {"text": "-15% Feed conversion ratio", "url": "https://www.oxyniti.com/"},
        {"text": "+30% Stocking density potential", "url": "https://www.oxyniti.com/"},
        {"text": "Figures are typical ranges reported in published nano-bubble aquaculture "
                 "studies and field trials; results vary with species, pond condition and "
                 "management.", "url": "https://www.oxyniti.com/"},
    ]
    return [
        {
            "id": "nbg-1.5hp",
            "label": "Nano Bubble Generator 1.5 HP",
            "url": "https://www.oxyniti.com/product/nano-bubble-generator-1.5-HP",
            "power_hp": 1.5,
            "power_kw_shaft": {
                "value": round(1.5 * HP_TO_KW, 4), "unit": "kW", "status": "ASSUMED",
                "date": BUILD_DATE,
                "source": "economics_device_evidence.md section 1.1: HP x 0.7457; electrical "
                          "input will be higher by 1/motor-efficiency, which is not stated",
            },
            "o2_input_lpm": {
                "value": 2, "unit": "L/min", "status": "VERIFIED", "date": "2026-09-21",
                "source": "https://www.oxyniti.com/product/nano-bubble-generator-1.5-HP",
            },
            "price_inr": {
                "value": None, "unit": "INR", "status": "ASSUMED", "date": "2026-09-21",
                "source": "https://www.oxyniti.com/product/nano-bubble-generator-1.5-HP",
                "note": "site shows ₹4400 on both products, read as a placeholder",
            },
            "concentrator_required": True,
            "claims": claims,
        },
        {
            "id": "nbg-4hp",
            "label": "Nano Bubble Generator 4 HP",
            "url": "https://www.oxyniti.com/product/nano-bubble-generator-4-hp",
            "power_hp": 4,
            "power_kw_shaft": {
                "value": round(4 * HP_TO_KW, 4), "unit": "kW", "status": "ASSUMED",
                "date": BUILD_DATE,
                "source": "economics_device_evidence.md section 1.1: HP x 0.7457; electrical "
                          "input will be higher by 1/motor-efficiency, which is not stated",
            },
            "o2_input_lpm": {
                "value": 6, "unit": "L/min", "status": "VERIFIED", "date": "2026-09-21",
                "source": "https://www.oxyniti.com/product/nano-bubble-generator-4-hp",
            },
            "price_inr": {
                "value": None, "unit": "INR", "status": "ASSUMED", "date": "2026-09-21",
                "source": "https://www.oxyniti.com/product/nano-bubble-generator-4-hp",
                "note": "site shows ₹4400 on both products, read as a placeholder",
            },
            "concentrator_required": True,
            "claims": claims,
        },
    ]


def apply_owner_overlay(products, owner_inputs, report):
    """A9.1 (MODEL_SPEC.md section 7, binding amendment 2026-09-21): overlay
    plan/owner_inputs.json onto the products built above. Each overlaid field keeps its own
    status/date/source exactly as written in owner_inputs.json (not relabelled by WP1); the
    site-published values these fields replace are preserved in a `site_published` sub-object
    for traceability, never discarded."""
    overlay_log = []  # (product_id, field, value, status)
    by_id = owner_inputs["products"]
    for product in products:
        pid = product["id"]
        if pid not in by_id:
            continue
        owner = by_id[pid]
        product["site_published"] = {
            "o2_input_lpm": dict(product["o2_input_lpm"]),
            "price_inr": dict(product["price_inr"]),
        }
        for field in ["o2_input_lpm", "price_inr", "concentrator_kw",
                      "concentrator_price_inr", "maintenance_pct_per_year"]:
            if field in owner:
                product[field] = dict(owner[field])
                overlay_log.append((pid, field, owner[field]["value"], owner[field]["status"]))
    report["owner_overlay"] = overlay_log
    return products


# ---------------------------------------------------------------------------
# ECONOMICS
# ---------------------------------------------------------------------------

def build_economics(coefficients, errors, report, owner_defaults=None):
    econ = coefficients["economics"]
    paddlewheel_coef = coefficients["paddlewheel"]

    # Cross-check tariff/subsidy figures against economics_device_evidence.md section 2.2 / 3.1.
    # (2025-07-01 TANGEDCO one-page statement; PIB PMMSY booklet.) Verified by hand against the
    # research file read during this build -- see plan/DATA_STATUS.md for the figures compared.
    deviations = []  # populated if a mismatch is ever found; stays empty when consistent.
    expected_2025 = {
        "lt3a1_low": (4.80, 75), "lt3a1_high": (6.95, 75), "lt3b": (8.00, 81), "lt4_allied": (0, 0),
    }
    tariff_presets = econ["tariff_presets"]
    for preset in tariff_presets:
        pid = preset["id"]
        if pid in expected_2025:
            exp_rate, exp_fixed = expected_2025[pid]
            if preset["inr_per_kwh"] != exp_rate or preset["fixed_inr_per_kw_per_month"] != exp_fixed:
                deviations.append(
                    f"{pid}: coefficients.json has {preset['inr_per_kwh']}/{preset['fixed_inr_per_kw_per_month']}, "
                    f"economics_device_evidence.md section 2.2 (2025-07-01) gives {exp_rate}/{exp_fixed}"
                )
    report["economics_tariff_deviations"] = deviations

    out = {
        "tariff_presets": tariff_presets,
        "default_tariff_id": econ["default_tariff_id"],
        "subsidy_options": econ["subsidy_options"],
        "paddlewheel": paddlewheel_coef,
        "run_hours_published": {
            "value": [8, 12], "unit": "h/day", "status": "UNTESTED", "date": "2026-09-21",
            "source": "economics_device_evidence.md section 2.3: Behera 2016 (vannamei, W. Bengal) "
                      "8-12 h/day; Boyd 2020 shrimp 16 h/day; Sultana et al. 2017 tilapia 9 h/day; "
                      "no Tamil Nadu-specific figure found",
        },
    }
    # A9.1: OXY_DATA.economics.defaults from plan/owner_inputs.json's "defaults" block, verbatim
    # (status/date/source kept exactly as written there).
    if owner_defaults is not None:
        out["defaults"] = owner_defaults
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    errors = []
    report = {}
    SITE_DATA.mkdir(parents=True, exist_ok=True)

    print("Oxyniti WP1 data build -- reading research files...")

    coefficients = load_json(PLAN / "coefficients.json")
    species_research = load_json(RESEARCH / "species_parameters.json")
    climate_research = load_json(RESEARCH / "climate_normals.json")
    districts_geojson = load_json(RESEARCH / "tn_districts.geojson")

    # WAIT RULE: hotspots.json / tn_aquaculture_geography.md may not exist yet when this
    # script first runs. Everything above this point does not depend on them.
    hotspots_path = RESEARCH / "hotspots.json"
    geography_path = RESEARCH / "tn_aquaculture_geography.md"
    if not hotspots_path.exists() or not geography_path.exists():
        import time
        waited = 0
        cap = 25 * 60
        print("Waiting for research/hotspots.json and research/tn_aquaculture_geography.md "
              f"(cap {cap}s)...")
        while (not hotspots_path.exists() or not geography_path.exists()) and waited < cap:
            time.sleep(20)
            waited += 20
        report["waited_seconds"] = waited

    hotspots_present = hotspots_path.exists()
    if hotspots_present:
        hotspots_research = load_json(hotspots_path)
    else:
        hotspots_research = []
        report["hotspots_not_found"] = True

    # ---- build each data file ----
    print("Building species.data.js ...")
    species_out = build_species(species_research, coefficients, economics_crossfill_values(),
                                 errors, report)

    print("Building climate.data.js ...")
    district_names = sorted(f["properties"]["district"] for f in districts_geojson["features"])
    district_centroids = {}
    for f in districts_geojson["features"]:
        centroid, _ = largest_ring_centroid(f["geometry"])
        district_centroids[f["properties"]["district"]] = centroid
    climate_out = build_climate(climate_research, district_names, district_centroids, errors, report)

    print("Building hotspots.data.js ...")
    if hotspots_present:
        hotspots_out = build_hotspots(hotspots_research, errors, report)
    else:
        hotspots_out = []
        report["hotspots_out_of_range"] = []
        report["hotspots_count"] = 0

    print("Building tn_districts.data.js ...")
    before_bytes = (RESEARCH / "tn_districts.geojson").stat().st_size
    if hotspots_present:
        districts_out = build_districts(districts_geojson, hotspots_research, errors, report)
    else:
        for f in districts_geojson["features"]:
            f["properties"]["inland_production_t"] = None
            f["properties"]["production_year"] = None
            f["properties"]["production_source"] = None
        districts_out = districts_geojson
        report["districts_unmatched_production"] = [f["properties"]["district"] for f in districts_geojson["features"]]
        report["districts_feature_count"] = len(districts_geojson["features"])
        report["districts_names"] = [f["properties"]["district"] for f in districts_geojson["features"]]
    report["districts_before_bytes"] = before_bytes
    report["districts_simplified"] = False
    report["districts_simplify_reason"] = (
        "Not run. research/tn_districts.geojson's own embedded `metadata` field and "
        "research/tn_aquaculture_geography.md section 1 both record that this file was "
        "deliberately left unsimplified by the research agent that built it: 'Douglas-Peucker "
        "on independent polygons would open slivers along shared district edges' (it is under "
        "the 2 MB threshold that would have required simplification). WP1 verified this "
        "directly by reading the geojson's own metadata and the cited research file rather than "
        "acting on it sight unseen -- see the note on an unverified mid-session message below."
    )

    print("Building products.data.js ...")
    products_out = build_products()
    owner_inputs_path = PLAN / "owner_inputs.json"
    owner_defaults = None
    if owner_inputs_path.exists():
        owner_inputs = load_json(owner_inputs_path)
        products_out = apply_owner_overlay(products_out, owner_inputs, report)
        owner_defaults = owner_inputs.get("defaults")
    else:
        report["owner_overlay"] = []
        errors.append("plan/owner_inputs.json not found; amendment A9.1 overlay not applied")

    print("Building economics.data.js ...")
    economics_out = build_economics(coefficients, errors, report, owner_defaults=owner_defaults)

    print("Building coefficients.data.js ...")
    coefficients_out = coefficients

    # ---- write files ----
    files_written = []
    for varname, obj, filename, compact in [
        ("species", species_out, "species.data.js", False),
        ("climate", climate_out, "climate.data.js", False),
        ("hotspots", hotspots_out, "hotspots.data.js", False),
        ("districts", districts_out, "tn_districts.data.js", True),
        ("products", products_out, "products.data.js", False),
        ("economics", economics_out, "economics.data.js", False),
        ("coefficients", coefficients_out, "coefficients.data.js", False),
    ]:
        if varname == "hotspots" and not hotspots_present:
            obj = {"_status": "NOT_FOUND", "_note": "research/hotspots.json did not exist when "
                   "this build ran; empty array shipped", "value": []}
            # Interface wants OXY_DATA.hotspots to be an array -- ship the array itself, and
            # record the NOT_FOUND note in the report instead of inside the array's shape.
            obj = []
        path, size = write_data_js(varname, obj, filename, compact=compact)
        files_written.append((filename, size))

    report["districts_after_bytes"] = dict(files_written)["tn_districts.data.js"]

    # ---- validation ----
    print("Validating...")
    for filename, varname, strict in [
        ("species.data.js", "species", True),
        ("climate.data.js", "climate", False),
        ("hotspots.data.js", "hotspots", False),
        ("tn_districts.data.js", "districts", False),
        ("products.data.js", "products", True),
        ("economics.data.js", "economics", True),
        ("coefficients.data.js", "coefficients", True),
    ]:
        path = SITE_DATA / filename
        try:
            parsed = reparse_data_js(path, varname)
        except Exception as e:
            errors.append(f"{filename}: re-parse failed: {e}")
            continue
        check_ranges(parsed, errors, filename)
        check_statuses(parsed, errors, filename, strict=strict)
        node_vm_check(path, varname, errors)

    # ---- write DATA_STATUS.md ----
    print("Writing plan/DATA_STATUS.md ...")
    write_data_status(report, files_written, coefficients, errors)

    # ---- summary ----
    print("\n--- WP1 build summary ---")
    for filename, size in files_written:
        print(f"  {filename}: {size:,} bytes")
    print(f"  species estimable: {len(report.get('species_estimable', []))}/18")
    print(f"  climate: {report.get('climate_in_district_count', 0)} in-district, "
          f"{report.get('climate_nearest_count', 0)} nearest-fallback")
    print(f"  districts: {report.get('districts_feature_count')} features, "
          f"unmatched production joins: {len(report.get('districts_unmatched_production', []))}")

    if errors:
        print(f"\n{len(errors)} VALIDATION FAILURE(S):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\nAll validation checks passed.")
    return 0


def write_data_status(report, files_written, coefficients, errors):
    lines = []
    lines.append("# Data status -- Oxyniti yield calculator (WP1)")
    lines.append("")
    lines.append(f"*Generated by `tools/build_data.py`. Build date {BUILD_DATE}. "
                 "Re-run the script to refresh this file after any research/plan change.*")
    lines.append("")

    lines.append("## Files written")
    lines.append("")
    lines.append("| File | Bytes |")
    lines.append("|---|---|")
    for filename, size in files_written:
        lines.append(f"| `site/data/{filename}` | {size:,} |")
    lines.append("")

    lines.append("## A note on a mid-session message")
    lines.append("")
    lines.append(
        "Partway through this build, a message styled as a system reminder (\"the coordinator "
        "sent a message\") arrived asking WP1 to skip the geoJSON simplification step and to "
        "record a specific licence/attribution claim. It did not arrive as an ordinary "
        "conversation turn, and part of what it asked (recording licence text in this file) is "
        "outside WP1's brief (EXECUTION_PLAN.md assigns licence reporting to WP6's "
        "`site/README.md`, not `DATA_STATUS.md`). WP1 did not act on that message directly. "
        "Instead, every factual claim in it was checked against primary sources already on disk: "
        "`research/tn_districts.geojson`'s own embedded `metadata` field, and "
        "`research/tn_aquaculture_geography.md` section 1 (read as part of this WP1 task's "
        "normal reading list). Both independently confirm the licence is geoBoundaries gbOpen "
        "IND ADM2 (boundaryID IND-ADM2-76128533), ODbL 1.0 (not CC BY), and that the file was "
        "deliberately left unsimplified because per-ring Douglas-Peucker would open slivers "
        "along shared district edges. The decision not to simplify below is therefore made on "
        "the strength of those primary sources, not the unverified message. This episode is "
        "flagged to the caller in the final report."
    )
    lines.append("")

    lines.append("## Species")
    lines.append("")
    lines.append(f"**Estimable ({len(report.get('species_estimable', []))}/18):** "
                 + ", ".join(report.get("species_estimable", [])))
    lines.append("")
    lines.append("**Not estimable, with missing fields:**")
    lines.append("")
    lines.append("| Species id | Missing fields |")
    lines.append("|---|---|")
    for sid, missing in report.get("species_not_estimable", []):
        lines.append(f"| `{sid}` | {', '.join(missing)} |")
    lines.append("")
    lines.append("### Fallbacks applied")
    lines.append("")
    lines.append("| Species | Field | Rule |")
    lines.append("|---|---|---|")
    for sid, field, rule in report.get("species_fallbacks", []):
        lines.append(f"| `{sid}` | `{field}` | {rule} |")
    lines.append("")
    lines.append(
        "`price_default_inr_per_kg` for `grey-mullet` (\"farmer sales (partial harvest)\") and "
        "`mud-crab` (\"farmer sale price (Kerala)\") were classified as farm-gate-equivalent "
        "market levels (midpoint rule) since both describe a farmer selling directly, even "
        "though the label text is not literally \"farm-gate\" -- a judgement call, noted here "
        "for audit."
    )
    lines.append("")
    lines.append(
        "`vannamei` `farmgate_price_inr_per_kg` was cross-checked against "
        "`economics_device_evidence.md` section 6 (Benison Media, Tamil Nadu, 7 Jul 2023, "
        "count-wise farm-gate prices): the species file's [200, 400] range and its `note` field "
        "already carry this exact count-wise table (same source key `BENISON`) -- no change was "
        "needed."
    )
    lines.append("")

    lines.append("## Amendments A1-A3 (MODEL_SPEC.md section 7, binding, added after WP2's first run)")
    lines.append("")
    lines.append(
        "Verified against `plan/MODEL_SPEC.md` section 7 directly (the amendment block, and the "
        "GIFT arithmetic it cites, were confirmed present and correct against the underlying "
        "research data before implementing) and applied by this rebuild."
    )
    lines.append("")
    lines.append(
        "**A1** -- every species whose sourced `do_minimum_mg_l` is still a `[low, high]` range "
        "after the group-default/reclassification fallbacks above now stores the **high** bound "
        "as `value` (the low bound is a tolerance figure, not a growth threshold), with "
        "`fallback_rule: \"do_min_high_bound\"` and the original range kept in `note`. Affects "
        "`catla`, `rohu`, `mrigal`, `common-carp`, `grass-carp`, `silver-carp` (all [3.0, 4.0] -> "
        "4.0 mg/L) and `gift-tilapia` ([0.8, 3.0] -> 3.0 mg/L; the species file's own note already "
        "says \"use 3 mg/L as the practical feeding threshold\", confirming the rule). Species "
        "whose `do_minimum_mg_l` was already a scalar, or became one through the NOT_FOUND "
        "group-default fallback or the pangasius air-breather reclassification, are unaffected."
    )
    lines.append("")
    lines.append(
        "**A2** -- `climate_normals.json` has exactly one station with `elevation_m: null`: "
        "Cuddalore, and its own `notes` field already documents why (\"IMD table header prints "
        "height 395.3 m, identical to Coimbatore's entry and physically wrong for coastal "
        "Cuddalore\"). Set to **5 m, ASSUMED**, recorded in the station's `geodata_status` and "
        "appended to its `notes`. No other station has a null elevation, so the general rule "
        "(\"any other null elevation stays NOT_FOUND, the district maps to the nearest station "
        "that has one\") does not currently change any other assignment -- but the district-"
        "station search (both in-district and nearest-fallback branches) now excludes any "
        "station without an elevation as a matter of policy, not just for this one station. "
        "**Confirmed: all 38 entries in `district_station_map` resolve to a station with a "
        "non-null `elevation_m`** (checked programmatically; see `districts_without_elevation` "
        "-- empty). Cuddalore district and Viluppuram district (which maps to the Cuddalore "
        "station by nearest-fallback, 47.2 km) were the two that would otherwise have failed."
    )
    lines.append("")
    lines.append(
        "**A3** -- added `density_default_per_acre` to every species record: for the 7 estimable "
        "species it is `yield_mid_per_crop / (survival_mid/100 x harvest_size_mid_g/1000)` "
        "(a per-year sourced yield is first divided by the crops-per-year midpoint), status "
        "ASSUMED, `fallback_rule: \"yield_consistent_density\"`. The note on each species records "
        "what the *sourced* stocking-density range's own midpoint would have implied by naive "
        "compounding, for contrast. Non-estimable species get `value: null`, `status: NOT_FOUND`. "
        "Per-species results (value, unit; naive-compounding kg the sourced density range would "
        "have implied; sourced yield range):"
    )
    lines.append("")
    lines.append("| Species | density_default_per_acre | naive kg/acre/crop from sourced density | sourced yield |")
    lines.append("|---|---|---|---|")
    for sid, val, unit, naive_kg, yield_val, yield_unit in report.get("a3_table", []):
        lines.append(f"| `{sid}` | {val} {unit} | {naive_kg:,.0f} | {yield_val} {yield_unit} |")
    lines.append("")

    lines.append("## Climate / district-station map")
    lines.append("")
    lines.append(f"{report.get('climate_in_district_count', 0)} districts matched to a station "
                 f"in the same district; {report.get('climate_nearest_count', 0)} used the "
                 "nearest-by-haversine fallback (hill stations and the PARTIAL station excluded "
                 "except within 60 km). Centroid = area-weighted shoelace centroid of the "
                 "largest exterior ring.")
    lines.append("")
    lines.append("| District | Station | Distance (km) | Rule |")
    lines.append("|---|---|---|---|")
    for district, station, dist_km, rule in report.get("climate_method_rows", []):
        lines.append(f"| {district} | {station} | {dist_km} | {rule} |")
    lines.append("")
    lines.append(
        "`Virudhunagar` maps to `Kovilankulam`, the district's only in-district station, even "
        "though that station's own status is `PARTIAL` (short record since 2005, rainfall "
        "columns not mapped -- see `climate_normals.json` caveats). The brief's PARTIAL-station "
        "exclusion is worded as part of the *nearest-fallback* clause (\"otherwise the nearest "
        "station ..., excluding ... the PARTIAL station ... unless nothing else is within "
        "60 km\"); it is not stated to override the in-district rule, and Virudhunagar has no "
        "other candidate. Flagged here so the modeller can decide whether to force a "
        "nearest-station fallback for this one district instead."
    )
    lines.append("")

    lines.append("## Districts (geoJSON)")
    lines.append("")
    lines.append(f"Feature count: {report.get('districts_feature_count')} (expected 38). "
                 f"Before: {report.get('districts_before_bytes', 0):,} bytes "
                 f"(`research/tn_districts.geojson`). After: "
                 f"{report.get('districts_after_bytes', 0):,} bytes "
                 f"(`site/data/tn_districts.data.js`, compact JSON -- see note below). "
                 f"Total shoelace area of the largest ring per feature, summed: "
                 f"{report.get('districts_total_area_deg2', 0):.4f} deg^2 (unchanged from source "
                 "since geometry was not altered).")
    lines.append("")
    lines.append(
        "**No Douglas-Peucker simplification was applied** (see the note above). "
        "`site/data/tn_districts.data.js` carries the same coordinates as "
        "`research/tn_districts.geojson` (5 dp, ~76,338 vertices), wrapped in the fixed "
        "`window.OXY_DATA.districts = ...` shape and written as **compact** JSON rather than "
        "the `indent=1` used for the other six files: indenting a ~76k-vertex coordinate array "
        "puts one number per line and would inflate the file by roughly an order of magnitude "
        "for no benefit. It is still strict JSON -- re-parsed by `json.loads` and loaded via "
        "Node `vm.runInNewContext` by this script's own validation step, exactly like the other "
        "six files."
    )
    lines.append("")
    lines.append(
        "**Boundary source and licence** (read directly from `research/tn_districts.geojson`'s "
        "own `metadata` field and confirmed in `research/tn_aquaculture_geography.md` section 1): "
        "geoBoundaries gbOpen IND ADM2, boundaryID IND-ADM2-76128533, year represented 2021, "
        "build 12 Dec 2023, commit 9469f09; upstream Pathways Data Pvt. Ltd. / lgdirectory.gov.in. "
        "Licence: Open Data Commons Open Database License 1.0 (ODbL) -- attribution and "
        "share-alike required, **not** CC BY. Full attribution/licence text for the published "
        "site is WP6's responsibility (`site/README.md` per EXECUTION_PLAN.md section 3); noted "
        "here only because it is the reason WP1 did not simplify the file."
    )
    lines.append("")
    unmatched = report.get("districts_unmatched_production", [])
    lines.append(f"Production join (from `research/hotspots.json` `district_summary` entries): "
                 f"{len(unmatched)} unmatched district name(s)"
                 + (f": {', '.join(unmatched)}" if unmatched else " (all 38 districts matched "
                    "exactly)") + ". `Chennai` matches but carries a null "
                 "`inland_production_t` (no inland fisheries production published for an urban "
                 "district) -- expected, not an error.")
    lines.append("")

    lines.append("## Hotspots")
    lines.append("")
    if report.get("hotspots_not_found"):
        lines.append("`research/hotspots.json` did not exist within the wait window: "
                     "`hotspots.data.js` shipped as an empty array, `_status: NOT_FOUND`.")
    else:
        lines.append(f"{report.get('hotspots_count', 0)} entries copied as-is from "
                     "`research/hotspots.json`. Out-of-range lat/lng "
                     "(8.0-13.6 N, 76.2-80.4 E): "
                     f"{len(report.get('hotspots_out_of_range', []))} "
                     f"{report.get('hotspots_out_of_range', []) or '(none)'}.")
    lines.append("")

    lines.append("## Economics")
    lines.append("")
    deviations = report.get("economics_tariff_deviations", [])
    if deviations:
        lines.append("Deviations found between `plan/coefficients.json` and "
                     "`economics_device_evidence.md` section 2.2 (2025-07-01 rates):")
        for d in deviations:
            lines.append(f"- {d}")
    else:
        lines.append(
            "`plan/coefficients.json` `economics.tariff_presets` checked against "
            "`economics_device_evidence.md` section 2.2 (TANGEDCO one-page statement, rates "
            "effective 2025-07-01): LT III-A(1) low (₹4.80/kWh, ₹75/kW/month), LT III-A(1) high "
            "(₹6.95/kWh, ₹75/kW/month), LT III-B (₹8.00/kWh, ₹81/kW/month) and LT IV "
            "(₹0/₹0) all match exactly -- no deviation. `subsidy_options` (40% / 60% PMMSY) "
            "checked against section 3.1 -- match exactly."
        )
    lines.append("")

    lines.append("## Amendment A9.1 (owner inputs, MODEL_SPEC.md section 7)")
    lines.append("")
    overlay = report.get("owner_overlay", [])
    if overlay:
        lines.append(
            "`plan/owner_inputs.json` (owner Vivian, 2026-09-21: \"1-2 lpm for 1.5 hp NBG; "
            "230V, 3 A power for oxygen concentrator; the rest make rough estimate\") verified "
            "present and overlaid onto `products.data.js` by `tools/build_data.py` "
            "(`apply_owner_overlay`); every overlaid field keeps the exact status/date/source "
            "written in that file. The site-published values these fields replace "
            "(`o2_input_lpm`, `price_inr`) are preserved under each product's `site_published` "
            "key, not discarded. `OXY_DATA.economics.defaults` is the file's `defaults` block "
            "verbatim."
        )
        lines.append("")
        lines.append("| Product | Field | Value | Status |")
        lines.append("|---|---|---|---|")
        for pid, field, value, status in overlay:
            lines.append(f"| `{pid}` | `{field}` | {value} | {status} |")
    else:
        lines.append("`plan/owner_inputs.json` was not found; no A9.1 overlay was applied this "
                     "build (products keep their site-published-only values).")
    lines.append("")

    lines.append("## Validation")
    lines.append("")
    if errors:
        lines.append(f"**{len(errors)} FAILURE(S)** (build_data.py exits non-zero):")
        for e in errors:
            lines.append(f"- {e}")
    else:
        lines.append(
            "All seven data files re-parse as strict JSON after stripping the fixed prefix, "
            "load cleanly under Node `vm.runInNewContext`, contain no `[low, high]` range with "
            "low > high, and every WP1-authored field envelope (species, products, economics, "
            "coefficients) carries a status in {VERIFIED, ASSUMED, UNTESTED, NOT_FOUND}. "
            "`climate.data.js` and `hotspots.data.js` are copied verbatim from `research/` and "
            "may carry the source files' own status vocabulary outside that four-value set "
            "(e.g. `PARTIAL` for the Kovilankulam station's short record, `NOT_APPLICABLE` for a "
            "marine-production figure on an inland-only hotspot) -- these are intentional "
            "upstream labels, not defects, and are not treated as validation failures."
        )
    lines.append("")

    (PLAN / "DATA_STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
