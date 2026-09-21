# Independent Python oracle for the Oxyniti yield calculator.
# Implements plan/MODEL_SPEC.md sections 2-7, including the 2026-09-21 amendments A1-A5, verbatim
# from the spec alone (WP3; site/js/model.js and tests/model.test.mjs were never opened while
# writing this file - see plan/EXECUTION_PLAN.md WP3).
"""
Usage:
    python tests/oracle.py tests/scenarios.json

Loads site/data/*.data.js (stripping the window.OXY_DATA assignment wrapper and json.loads-ing the
remainder), evaluates every scenario in the given scenarios file against MODEL_SPEC.md, and prints a
JSON array of results (one per scenario, in the same order). A scenario whose evaluation throws is
reported as {"error": "<exception class>: <field>"} instead of a result object.

Python 3.13, standard library only.
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

MONTHS_IN_YEAR = 12
ACRE_TO_M2 = 4046.86


# --------------------------------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------------------------------

class MissingDataError(Exception):
    """Mirrors the fixed interface OxyModel.MissingDataError (EXECUTION_PLAN.md 4.2):
    a required field was null/absent after every documented fallback. Fail loudly, never default."""

    def __init__(self, field, species=None):
        self.field = field
        self.species = species
        msg = f"missing required field '{field}'"
        if species is not None:
            msg += f" for species '{species}'"
        super().__init__(msg)


# --------------------------------------------------------------------------------------------------
# Data loading (site/data/*.data.js -> OXY_DATA dict). Independent of site/js/model.js.
# --------------------------------------------------------------------------------------------------

_GUARD_RE_TEXT = "window.OXY_DATA = window.OXY_DATA || {};"


def _strip_line_comments(text: str) -> str:
    out_lines = []
    for line in text.split("\n"):
        if line.strip().startswith("//"):
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


def load_data_file(path: pathlib.Path):
    """Strip the window.OXY_DATA = window.OXY_DATA || {}; guard line, the
    window.OXY_DATA.<name> = prefix and the trailing ';', then json.loads the remainder."""
    text = path.read_text(encoding="utf-8")
    text = _strip_line_comments(text)
    text = text.replace(_GUARD_RE_TEXT, "")

    marker = "window.OXY_DATA."
    idx = text.find(marker)
    if idx == -1:
        raise ValueError(f"no 'window.OXY_DATA.<name> =' assignment found in {path}")
    rest = text[idx + len(marker):]
    eq = rest.find("=")
    if eq == -1:
        raise ValueError(f"malformed OXY_DATA assignment in {path}")
    name = rest[:eq].strip()
    body = rest[eq + 1:].strip()
    if body.endswith(";"):
        body = body[:-1]
    body = body.strip()
    try:
        value = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"failed to parse JSON for OXY_DATA.{name} in {path}: {exc}") from exc
    return name, value


def load_oxy_data(data_dir: pathlib.Path) -> dict:
    data = {}
    files = sorted(data_dir.glob("*.data.js"))
    if not files:
        raise FileNotFoundError(f"no *.data.js files found in {data_dir}")
    for f in files:
        name, value = load_data_file(f)
        data[name] = value
    return data


# --------------------------------------------------------------------------------------------------
# Envelope / range helpers. Every numeric field in the data files is either a plain value or the
# {value, unit, status, date, source} envelope (EXECUTION_PLAN.md 4.1); these helpers accept both.
# --------------------------------------------------------------------------------------------------

def V(x):
    """Unwrap the {value, unit, status, ...} envelope if present; otherwise return x unchanged."""
    if isinstance(x, dict) and "value" in x and "status" in x:
        return x["value"]
    return x


def mid(x):
    """Unwrap, then collapse a [low, high] range to its midpoint (WP1 fallback rule 4: a one-sided
    range [x, null] uses x; never widen). Scalars pass through as float. None stays None."""
    v = V(x)
    if v is None:
        return None
    if isinstance(v, list):
        lo, hi = v[0], v[1]
        if lo is None and hi is None:
            return None
        if hi is None:
            return float(lo)
        if lo is None:
            return float(hi)
        return (float(lo) + float(hi)) / 2.0
    return float(v)


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def js_round(x):
    """Round-half-up, matching JavaScript's Math.round (Python's round() is round-half-to-even and
    disagrees with JS on exact .5 ties, e.g. gift-tilapia's culture_period_months mid = 6.5)."""
    return math.floor(x + 0.5)


# --------------------------------------------------------------------------------------------------
# Assumptions accumulator, for the result's `assumptions` list (every parameter with value, unit,
# status, date, source - EXECUTION_PLAN.md 3, Assumptions panel).
# --------------------------------------------------------------------------------------------------

def new_bucket():
    return {"_seen": set(), "list": []}


def record(bucket, id_, label, envelope, unit=None):
    if envelope is None:
        return
    if isinstance(envelope, dict) and "status" in envelope:
        value = envelope.get("value")
        e_unit = envelope.get("unit", unit)
        status = envelope.get("status")
        date = envelope.get("date")
        source = envelope.get("source")
    else:
        value, e_unit, status, date, source = envelope, unit, "VERIFIED", None, None
    if id_ in bucket["_seen"]:
        return
    bucket["_seen"].add(id_)
    bucket["list"].append({
        "id": id_, "label": label, "value": value, "unit": e_unit,
        "status": status, "date": date, "source": source,
    })


def pull(bucket, envelope, id_, label, unit=None):
    """Unwrap a coefficients.json-style envelope and record it as an assumption in one step."""
    val = V(envelope)
    record(bucket, id_, label, envelope, unit)
    return val


# --------------------------------------------------------------------------------------------------
# Species field accessors - fail loudly (MissingDataError) on any null load-bearing field.
# --------------------------------------------------------------------------------------------------

def species_raw(species, field, species_id, allow_none=False):
    env = species.get(field)
    v = V(env)
    if v is None and not allow_none:
        raise MissingDataError(field, species_id)
    return v


def species_mid(bucket, species, field, label, species_id, unit=None, allow_none=False):
    env = species.get(field)
    resolved = mid(env)
    if resolved is None and not allow_none:
        raise MissingDataError(field, species_id)
    if env is not None:
        record(bucket, f"species.{species_id}.{field}", label, env, unit)
    return resolved


def species_range(bucket, species, field, label, species_id, unit=None):
    """Returns (low, high). Most range fields are sourced as [low, high]; a few (e.g. murrel's
    farmgate_price_inr_per_kg) are sourced as a single scalar - treated as a degenerate range
    (low == high == that scalar), consistent with WP1 fallback rule 4's 'never widen a range'."""
    env = species.get(field)
    v = V(env)
    if isinstance(v, list):
        if v[0] is None or v[1] is None:
            raise MissingDataError(field, species_id)
        lo, hi = float(v[0]), float(v[1])
    elif v is not None:
        lo = hi = float(v)
    else:
        raise MissingDataError(field, species_id)
    record(bucket, f"species.{species_id}.{field}", label, env, unit)
    return lo, hi


def find_species(data, species_id):
    for s in data.get("species", []):
        if s.get("id") == species_id:
            return s
    raise MissingDataError("species", species_id)


def check_estimable(species, species_id):
    if species.get("estimable") is False:
        missing = species.get("missing") or ["estimable"]
        raise MissingDataError(missing[0], species_id)


def find_product(data, product_id):
    for p in data.get("products", []):
        if p.get("id") == product_id:
            return p
    raise MissingDataError("unit_model", product_id)


def find_station(data, station_name):
    for st in data.get("climate", {}).get("stations", []):
        for key in ("name", "id", "station", "station_name"):
            if st.get(key) == station_name:
                return st
    raise MissingDataError("station", station_name)


def station_air_temps(station):
    """{month(1..12): (tmax_c, tmin_c)} from the station's `months` list (research/climate_normals.json
    shape: a list of 12 dicts keyed by m, tmax_c, tmin_c - carried through by WP1 'as research')."""
    months = station.get("months")
    out = {}
    if isinstance(months, list):
        for rec in months:
            m = V(rec.get("m"))
            tmax = V(rec.get("tmax_c"))
            tmin = V(rec.get("tmin_c"))
            out[int(m)] = (float(tmax), float(tmin))
    elif isinstance(months, dict):
        for k, rec in months.items():
            out[int(k)] = (float(V(rec.get("tmax_c"))), float(V(rec.get("tmin_c"))))
    if len(out) != 12:
        raise MissingDataError("months", station.get("name"))
    return out


# --------------------------------------------------------------------------------------------------
# MODEL_SPEC.md section 4.1 - DO saturation (Benson & Krause 1984), from research/do_physics.md (a).
# --------------------------------------------------------------------------------------------------

def do_saturation(t_c, salinity_ppt, p_atm, do_coeffs):
    a0, a1, a2, a3, a4 = V(do_coeffs["ln_cstar_coefficients"])
    b0, b1, b2 = V(do_coeffs["salinity_term"])
    c0, c1, c2 = V(do_coeffs["theta_coefficients"])
    d0, d1, d2 = V(do_coeffs["vapour_pressure_coefficients"])

    T = t_c + 273.15
    ln_c = (a0 + a1 / T + a2 / T ** 2 + a3 / T ** 3 + a4 / T ** 4
            - salinity_ppt * (b0 + b1 / T + b2 / T ** 2))
    c_star = math.exp(ln_c)

    theta = c0 + c1 * t_c + c2 * t_c ** 2
    u = math.exp(d0 + d1 / T + d2 / T ** 2)
    fp = ((p_atm - u) * (1 - theta * p_atm)) / ((1 - u) * (1 - theta))
    return c_star * fp


def pressure_from_elevation(z_m):
    return math.exp(-9.80665 * 0.0289644 * z_m / (8.31447 * 288.15))


# --------------------------------------------------------------------------------------------------
# MODEL_SPEC.md section 2 - pond water temperature.
# --------------------------------------------------------------------------------------------------

def pond_temperature(t_air_c, a, b):
    return a + b * t_air_c


# --------------------------------------------------------------------------------------------------
# MODEL_SPEC.md section 3 - thermal suitability trapezoid.
# --------------------------------------------------------------------------------------------------

def thermal_factor(t_w, tt_lo, to_lo, to_hi, tt_hi):
    if t_w < tt_lo or t_w > tt_hi:
        return 0.0
    if t_w < to_lo:
        return (t_w - tt_lo) / (to_lo - tt_lo)
    if t_w <= to_hi:
        return 1.0
    return (tt_hi - t_w) / (tt_hi - to_hi)


# --------------------------------------------------------------------------------------------------
# MODEL_SPEC.md section 4.3 - fish respiration q(T_w).
# --------------------------------------------------------------------------------------------------

def fish_respiration_rate(t_w, q_ref, q10, t_ref, t_cap):
    """mg O2 / kg / h. The Q10 exponent line below is the compare.py --self-test injection target."""
    exponent = (min(t_w, t_cap) - t_ref) / 10.0
    return q_ref * (q10 ** exponent)


# --------------------------------------------------------------------------------------------------
# Top-level pipeline - MODEL_SPEC.md sections 2-7 (including amendments A1-A5, end of section 7).
# --------------------------------------------------------------------------------------------------

def evaluate(inputs: dict, data: dict) -> dict:
    coeffs = data["coefficients"]
    bucket = new_bucket()
    warnings = []

    species_id = inputs["species"]
    species = find_species(data, species_id)
    check_estimable(species, species_id)

    water_type = species_raw(species, "water_type", species_id)
    respiration_group_name = species_raw(species, "respiration_group", species_id)
    if respiration_group_name not in coeffs["respiration_groups"]:
        raise MissingDataError("respiration_group", species_id)

    salinity_ppt = 0.0 if water_type == "freshwater" else species_mid(
        bucket, species, "salinity_ppt", "Salinity", species_id, unit="ppt")

    to_lo, to_hi = species_range(bucket, species, "temp_optimum_c", "Optimum temperature", species_id, "degC")
    tt_lo, tt_hi = species_range(bucket, species, "temp_tolerable_c", "Tolerable temperature", species_id, "degC")

    culture_months_n = js_round(species_mid(
        bucket, species, "culture_period_months", "Culture period", species_id, "months"))
    if culture_months_n < 1:
        culture_months_n = 1
    T_months = float(culture_months_n)

    harvest_size_mid = species_mid(bucket, species, "harvest_size_g", "Harvest size", species_id, "g")
    S0 = species_mid(bucket, species, "survival_pct", "Survival", species_id, "%") / 100.0
    w0 = species_mid(bucket, species, "seed_size_g", "Seed size", species_id, "g")
    FCR0 = species_mid(bucket, species, "fcr", "FCR", species_id, "kg feed/kg gain")
    # A1: do_minimum_mg_l, when sourced as a range, is WP1-resolved to its HIGH bound (not the
    # midpoint) before it reaches this file; mid() here is a no-op passthrough for that scalar and
    # only falls back to an in-oracle midpoint if a range somehow still arrives.
    do_min = species_mid(bucket, species, "do_minimum_mg_l", "DO growth threshold", species_id, "mg/L")
    do_lethal = species_mid(bucket, species, "do_lethal_mg_l", "DO lethal threshold", species_id, "mg/L")
    seed_cost = species_mid(bucket, species, "seed_cost_inr_per_unit", "Seed cost", species_id, "INR/unit")
    other_cost_pa = species_mid(bucket, species, "other_cost_inr_per_acre_crop", "Other cost", species_id,
                                 "INR/acre/crop")
    crops_per_year = species_mid(bucket, species, "crops_per_year_tn", "Crops per year", species_id, "crops/yr")
    stocking_month_default = int(round(species_mid(
        bucket, species, "stocking_month_tn_default", "TN default stocking month", species_id, "month")))
    farmgate_lo, farmgate_hi = species_range(bucket, species, "farmgate_price_inr_per_kg",
                                              "Farm-gate price (sourced)", species_id, "INR/kg")

    # --- climate: MODEL_SPEC.md section 2, station_name override per A9.2 -----------------------
    district = inputs["district"]
    station_map = data["climate"]["district_station_map"]
    station_name_override = inputs.get("station_name")
    if station_name_override:
        station_name = station_name_override
    else:
        station_name = station_map.get(district)
        if not station_name:
            raise MissingDataError("district_station_map", district)
    station = find_station(data, station_name)
    air = station_air_temps(station)
    # A2: WP1 guarantees every mapped station has a non-null elevation (coastal null -> 5 m ASSUMED,
    # any other null station is not mapped to); default to sea level only as a last resort.
    elevation_m = V(station.get("elevation_m"))
    if elevation_m is None:
        elevation_m = 0.0
    p_atm = pressure_from_elevation(elevation_m)

    ref_station_name = station_map.get("Tiruchirappalli")
    if not ref_station_name:
        raise MissingDataError("district_station_map", "Tiruchirappalli")
    ref_station = find_station(data, ref_station_name)
    ref_air = station_air_temps(ref_station)

    a_pt = pull(bucket, coeffs["pond_temperature"]["a_intercept_c"], "pond_temperature.a", "Pond temperature intercept (a)")
    b_pt = pull(bucket, coeffs["pond_temperature"]["b_slope"], "pond_temperature.b", "Pond temperature slope (b)")

    stock_month = int(inputs["stock_month"])
    crop_months = [((stock_month - 1 + i) % MONTHS_IN_YEAR) + 1 for i in range(culture_months_n)]
    ref_crop_months = [((stocking_month_default - 1 + i) % MONTHS_IN_YEAR) + 1 for i in range(culture_months_n)]

    def t_w_of(air_map, m):
        tmax, tmin = air_map[m]
        t_air = (tmax + tmin) / 2.0
        return t_air, pond_temperature(t_air, a_pt, b_pt)

    g_t_actual = {}
    for m in range(1, 13):
        _, t_w = t_w_of(air, m)
        g_t_actual[m] = thermal_factor(t_w, tt_lo, to_lo, to_hi, tt_hi)
    g_t_ref_list = []
    for m in ref_crop_months:
        _, t_w = t_w_of(ref_air, m)
        g_t_ref_list.append(thermal_factor(t_w, tt_lo, to_lo, to_hi, tt_hi))

    G_T = sum(g_t_actual[m] for m in crop_months) / len(crop_months)
    G_T_ref = sum(g_t_ref_list) / len(g_t_ref_list) if g_t_ref_list else 0.0

    size_clamp_lo, size_clamp_hi = V(coeffs["thermal"]["size_factor_clamp"])
    if G_T_ref > 0:
        size_factor = clamp(G_T / G_T_ref, size_clamp_lo, size_clamp_hi)
    else:
        size_factor = size_clamp_lo
    record(bucket, "thermal.size_factor_clamp", "Size-factor clamp", coeffs["thermal"]["size_factor_clamp"])

    w_h0 = harvest_size_mid * size_factor

    # --- section 4.2/4.3/4.4: night-time DO budget, per month (n_units-independent) -------------
    n = inputs["density_per_acre"] * inputs["area_acre"]
    area_m2 = inputs["area_acre"] * ACRE_TO_M2
    depth_m = inputs["depth_m"]
    V_l = area_m2 * depth_m * 1000.0

    rgroup = coeffs["respiration_groups"][respiration_group_name]
    q_ref = pull(bucket, rgroup["q_ref_mg_o2_kg_h"], f"respiration_groups.{respiration_group_name}.q_ref",
                 "Fish respiration reference rate")
    q10_fish = pull(bucket, rgroup["q10"], f"respiration_groups.{respiration_group_name}.q10",
                     "Fish respiration Q10")
    t_ref_fish = pull(bucket, rgroup["t_ref_c"], f"respiration_groups.{respiration_group_name}.t_ref",
                       "Fish respiration reference temperature")
    t_cap_fish = pull(bucket, rgroup["t_cap_c"], f"respiration_groups.{respiration_group_name}.t_cap",
                       "Fish respiration temperature cap")

    nb = coeffs["night_budget"]
    h_night = pull(bucket, nb["h_night"], "night_budget.h_night", "Night length")
    f_dusk = pull(bucket, nb["f_dusk"], "night_budget.f_dusk", "Dusk saturation fraction")
    d_diff = pull(bucket, nb["d_diff_mg_l_per_night"], "night_budget.d_diff", "Diffusion from air")
    bloom = inputs["bloom"]
    r_plankton_table = V(nb["r_plankton_ref_mg_l_h_at_25c"])
    if bloom not in r_plankton_table:
        raise MissingDataError("bloom", species_id)
    k_p = r_plankton_table[bloom]
    record(bucket, "night_budget.r_plankton_ref", f"Plankton respiration ({bloom} bloom)",
           nb["r_plankton_ref_mg_l_h_at_25c"])
    q10_p = pull(bucket, nb["q10_plankton"], "night_budget.q10_plankton", "Plankton respiration Q10")
    k_sed = pull(bucket, nb["k_sed_g_o2_m2_h"], "night_budget.k_sed", "Sediment respiration rate")
    q10_s = pull(bucket, nb["q10_sed"], "night_budget.q10_sed", "Sediment respiration Q10")
    t_ref_night = pull(bucket, nb["t_ref_c"], "night_budget.t_ref", "Night-budget reference temperature")

    # --- unit: product lookup + A4 datasheet overrides + A9.1 (o2_input_lpm is now a range) -------
    product_id = inputs["unit_model"]
    product = find_product(data, product_id)
    o2_lpm_published = mid(product.get("o2_input_lpm"))  # A9.1: range [low, high] -> midpoint
    o2_override = inputs.get("o2_input_lpm_override")
    o2_lpm_used = o2_override if o2_override is not None else o2_lpm_published
    if o2_lpm_used is None:
        raise MissingDataError("o2_input_lpm", product_id)

    power_kw_published = V(product.get("power_kw_shaft"))
    if power_kw_published is None:
        power_hp = V(product.get("power_hp"))
        hp_to_kw = pull(bucket, coeffs["oxygen_supply"]["hp_to_kw"], "oxygen_supply.hp_to_kw", "HP to kW")
        if power_hp is None:
            raise MissingDataError("power_kw_shaft", product_id)
        power_kw_published = power_hp * hp_to_kw
    power_override = inputs.get("power_kw_override")
    power_kw_used = power_override if power_override is not None else power_kw_published

    if o2_override is not None:
        record(bucket, "inputs.o2_input_lpm_override", "Oxygen delivery override (datasheet)",
               {"value": o2_override, "unit": "L/min", "status": "user-entered", "date": None,
                "source": "user input"})
    if power_override is not None:
        record(bucket, "inputs.power_kw_override", "Electrical input override (datasheet)",
               {"value": power_override, "unit": "kW", "status": "user-entered", "date": None,
                "source": "user input"})

    os_coeffs = coeffs["oxygen_supply"]
    rho_o2 = pull(bucket, os_coeffs["rho_o2_g_per_l"], "oxygen_supply.rho_o2", "Oxygen gas density")
    purity = pull(bucket, os_coeffs["purity"], "oxygen_supply.purity", "Concentrator purity")
    eta_nb = pull(bucket, os_coeffs["eta_dissolved"], "oxygen_supply.eta_dissolved", "Dissolution efficiency")
    run_h = inputs["run_h"]
    m_o2_per_unit_g = o2_lpm_used * 60.0 * run_h * rho_o2 * purity * eta_nb

    concentrator_kw = inputs.get("concentrator_kw")
    if concentrator_kw is None:
        warnings.append({"code": "CONCENTRATOR_POWER_UNKNOWN",
                          "message": "Concentrator power draw is not known and is excluded from electricity."})
        concentrator_kw_for_power = 0.0
    else:
        concentrator_kw_for_power = concentrator_kw
    P_unit = power_kw_used + concentrator_kw_for_power

    existing_kw = inputs["existing_aeration_kw"]
    existing_h = inputs["existing_run_h"]
    sae = pull(bucket, coeffs["paddlewheel"]["sae_field_kg_o2_per_kwh"], "paddlewheel.sae",
               "Paddlewheel field SAE")

    # Pass 1: in-crop biomass trajectory. Amendment A6 (MODEL_SPEC.md 4.4, pinned 2026-09-21) also
    # needs the crop-mean biomass here, for out-of-crop months' do_dawn_*/s_* below.
    biomass_by_m = {}
    for i, m in enumerate(crop_months):
        frac = (i + 0.5) / T_months
        S_t = 1.0 - (1.0 - S0) * frac
        w_t = w0 + (w_h0 - w0) * frac
        biomass_by_m[m] = n * S_t * w_t / 1000.0
    crop_mean_biomass = sum(biomass_by_m.values()) / len(biomass_by_m) if biomass_by_m else 0.0

    # Pass 2: every month's temperature/DO/stress. A6: an out-of-crop month's biomass_kg is the
    # crop-mean biomass (not zero), so do_dawn_*/s_* there reflect a representative stocking.
    months = []
    do_base_by_m = {}
    for m in range(1, 13):
        t_air, t_w = t_w_of(air, m)
        c_s = do_saturation(t_w, salinity_ppt, p_atm, coeffs["do_saturation"])
        g_t = g_t_actual[m]
        in_crop = m in crop_months
        biomass_kg = biomass_by_m[m] if in_crop else crop_mean_biomass

        do_dusk = f_dusk * c_s
        r_fish = biomass_kg * fish_respiration_rate(t_w, q_ref, q10_fish, t_ref_fish, t_cap_fish) / V_l
        r_plankton = k_p * (q10_p ** ((t_w - t_ref_night) / 10.0))
        r_sed = (k_sed / depth_m) * (q10_s ** ((t_w - t_ref_night) / 10.0))
        supply_exist = existing_kw * sae * existing_h * 1e6 / V_l

        pre_diff = do_dusk - h_night * (r_fish + r_plankton + r_sed) + supply_exist
        if pre_diff < c_s:
            pre_diff += d_diff
        do_dawn_base = clamp(pre_diff, 0.0, c_s)
        do_base_by_m[m] = do_dawn_base

        s_base = clamp((do_min - do_dawn_base) / (do_min - do_lethal), 0.0, 1.0)

        months.append({
            "m": m, "t_air_c": float(t_air), "t_w_c": float(t_w), "c_s_mg_l": float(c_s),
            "g_t": float(g_t), "in_crop": in_crop, "biomass_kg": float(biomass_kg),
            "do_dawn_base": float(do_dawn_base), "s_base": float(s_base),
            "do_dawn_oxy": None, "s_oxy": None,
        })

    crop_month_recs = [r for r in months if r["in_crop"]]

    zero_months = [r["m"] for r in crop_month_recs if r["g_t"] <= 0.0]
    if zero_months:
        warnings.append({
            "code": "THERMAL_OUT_OF_RANGE",
            "message": "outside the species' tolerable temperature - oxygen will not fix this",
            "months": zero_months,
        })

    price = inputs["price_inr_kg"]
    if price < farmgate_lo or price > farmgate_hi:
        warnings.append({"code": "PRICE_OUT_OF_SOURCED_RANGE",
                          "message": f"Price INR {price}/kg is outside the sourced range [{farmgate_lo}, {farmgate_hi}]."})

    # --- section 6: economics, baseline (n_units-independent) -------------------------------------
    feed_price = inputs["feed_price_inr_kg"]
    days = culture_months_n * pull(bucket, coeffs["economics"]["days_per_month"], "economics.days_per_month",
                                    "Days per month")

    kg0 = n * S0 * w_h0 / 1000.0
    gain0 = kg0 - n * S0 * w0 / 1000.0
    Revenue0 = kg0 * price
    Feed0 = gain0 * FCR0 * feed_price
    Seed = n * seed_cost
    Other = other_cost_pa * inputs["area_acre"]

    tariff_rate = inputs["tariff_inr_kwh"]
    tariff_id = inputs.get("tariff_id")
    preset = None
    for p in data["economics"]["tariff_presets"]:
        if p.get("id") == tariff_id:
            preset = p
            break
    fixed_per_kw_month = V(preset["fixed_inr_per_kw_per_month"]) if preset else 0.0
    if preset is not None:
        record(bucket, f"economics.tariff_presets.{tariff_id}", f"Tariff preset ({tariff_id})",
               {"value": preset.get("inr_per_kwh"), "unit": "INR/kWh", "status": preset.get("status"),
                "date": preset.get("date"), "source": preset.get("source")})

    Elec0 = existing_kw * existing_h * days * tariff_rate
    Profit0 = Revenue0 - Feed0 - Seed - Other - Elec0

    # A9.2/A9.3: unit price, concentrator price and maintenance, resolved early because n_best's
    # objective (below) must maximise dProfit_year net of maintenance, not just raw profit.
    unit_price = inputs.get("unit_price_inr")
    concentrator_price_input = inputs.get("concentrator_price_inr")
    concentrator_price = concentrator_price_input if concentrator_price_input is not None else 0.0
    maintenance_pct = inputs.get("maintenance_pct")
    if maintenance_pct is None:
        maintenance_pct = 0.0
    subsidy_pct = inputs.get("subsidy_pct", 0)
    # capex = n_units x (unit_price_inr + concentrator_price_inr) x (1 - subsidy_pct/100); a null
    # concentrator_price_inr is treated as 0, by analogy with concentrator_kw = null excluding the
    # concentrator from electricity (CONCENTRATOR_POWER_UNKNOWN) rather than blocking the model.
    total_unit_cost = (unit_price + concentrator_price) if unit_price is not None else 0.0

    def maint_year_for_n(n_candidate):
        return n_candidate * total_unit_cost * maintenance_pct / 100.0

    def elec1_for_n(n_candidate):
        fixed = 0.0 if tariff_id == "lt4_allied" else (
            n_candidate * power_kw_used * fixed_per_kw_month * culture_months_n)
        return Elec0 + n_candidate * P_unit * run_h * days * tariff_rate + fixed

    uc = coeffs["uplift"]
    growth_max = pull(bucket, uc["growth_max_fraction"], "uplift.growth_max_fraction", "Growth uplift at full relief")
    surv_max = pull(bucket, uc["survival_points_max"], "uplift.survival_points_max", "Survival uplift at full relief")
    fcr_gain_max = pull(bucket, uc["fcr_gain_max_fraction"], "uplift.fcr_gain_max_fraction", "FCR gain at full relief")
    ceiling = pull(bucket, uc["ceiling_extra_kg_fraction"], "uplift.ceiling_extra_kg_fraction", "Claims ceiling")
    # A5: the low case multiplies each of the three coefficients (growth, survival, FCR) by
    # low_case_factor - so FCR-low's max fraction is fcr_gain_max * low_case_factor = 0.035.
    low_case_factor = pull(bucket, uc["low_case_factor"], "uplift.low_case_factor", "Low-case multiplier")
    survival_cap = pull(bucket, uc["survival_cap"], "uplift.survival_cap", "Survival cap")
    include_fcr_gain = bool(inputs.get("include_fcr_gain", False))

    def ds_for_n(n_candidate):
        supply = n_candidate * m_o2_per_unit_g * 1000.0 / V_l
        total = 0.0
        for r in crop_month_recs:
            do_oxy = min(r["do_dawn_base"] + supply, r["c_s_mg_l"])
            s_oxy = clamp((do_min - do_oxy) / (do_min - do_lethal), 0.0, 1.0)
            total += (r["s_base"] - s_oxy)
        return clamp(total / len(crop_month_recs), 0.0, 1.0)

    def high_case_profit_year_for_n(n_candidate):
        ds_n = ds_for_n(n_candidate)
        G = growth_max * ds_n
        dS = surv_max * ds_n
        S1 = min(S0 + dS, survival_cap)
        w_h1_natural = w_h0 * (1.0 + G)
        kg1_natural = n * S1 * w_h1_natural / 1000.0
        extra_natural = (kg1_natural / kg0 - 1.0) if kg0 > 0 else 0.0
        extra_reported = min(extra_natural, ceiling)
        kg1 = kg0 * (1.0 + extra_reported)
        fcr_factor = (1.0 - fcr_gain_max * ds_n) if include_fcr_gain else 1.0
        FCR1 = FCR0 * fcr_factor
        gain1 = kg1 - n * S1 * w0 / 1000.0
        Revenue1 = kg1 * price
        Feed1 = gain1 * FCR1 * feed_price
        Elec1_n = elec1_for_n(n_candidate)
        Profit1 = Revenue1 - Feed1 - Seed - Other - Elec1_n
        return (Profit1 - Profit0) * crops_per_year - maint_year_for_n(n_candidate)

    # --- section 7 (amended): n_relief (full relief) and n_best (profit-maximising) sizing --------
    deficits = [max(do_min - do_base_by_m[m], 0.0) for m in crop_months]
    deficit_max = max(deficits) if deficits else 0.0
    n_units_cap = int(pull(bucket, coeffs["sizing"]["n_units_cap"], "sizing.n_units_cap", "Unit count cap"))

    raw_relief_n = math.ceil(deficit_max * V_l / (m_o2_per_unit_g * 1000.0)) if deficit_max > 0 else 0
    n_relief = max(1, min(raw_relief_n, n_units_cap))
    sizing_capped = raw_relief_n > n_units_cap
    if sizing_capped:
        warnings.append({"code": "SIZING_CAPPED",
                          "message": f"{raw_relief_n} units would be needed for full relief; capped at {n_units_cap}."})

    n_best = 1
    best_profit_year = high_case_profit_year_for_n(1)
    for candidate in range(2, n_units_cap + 1):
        candidate_profit = high_case_profit_year_for_n(candidate)
        if candidate_profit > best_profit_year + 1e-9:
            best_profit_year = candidate_profit
            n_best = candidate

    if best_profit_year <= 0:
        warnings.append({
            "code": "NO_PAYBACK_AT_PUBLISHED_O2",
            "message": "At the published oxygen input of this product the extra fish do not cover "
                       "the electricity for any number of units; enter the datasheet oxygen delivery "
                       "under Advanced.",
        })

    n_units_input = inputs.get("n_units", "auto")
    if n_units_input in (None, "auto"):
        n_units_final = n_best
        sizing_mode = "auto"
    else:
        n_units_final = int(n_units_input)
        sizing_mode = "manual"

    supply_oxy = n_units_final * m_o2_per_unit_g * 1000.0 / V_l
    for rec in months:
        c_s = rec["c_s_mg_l"]
        do_dawn_oxy = min(rec["do_dawn_base"] + supply_oxy, c_s)
        s_oxy = clamp((do_min - do_dawn_oxy) / (do_min - do_lethal), 0.0, 1.0)
        rec["do_dawn_oxy"] = float(do_dawn_oxy)
        rec["s_oxy"] = float(s_oxy)

    ds = clamp(sum(r["s_base"] - r["s_oxy"] for r in crop_month_recs) / len(crop_month_recs), 0.0, 1.0)

    # A8 (pinned, MODEL_SPEC.md section 7): fires iff the crop-mean of s_base (baseline stress,
    # independent of n_units) is below 0.05 - not "every month is exactly zero".
    crop_mean_s_base = sum(r["s_base"] for r in crop_month_recs) / len(crop_month_recs) if crop_month_recs else 0.0
    if crop_mean_s_base < 0.05:
        warnings.append({"code": "NOT_OXYGEN_LIMITED",
                          "message": "This pond is not oxygen-limited in any crop month; the unit adds no yield benefit here."})

    Elec1 = elec1_for_n(n_units_final)
    Maint_year = maint_year_for_n(n_units_final)

    def compute_case(mult):
        G = growth_max * mult * ds
        dS = surv_max * mult * ds
        S1 = min(S0 + dS, survival_cap)
        w_h1_natural = w_h0 * (1.0 + G)
        kg1_natural = n * S1 * w_h1_natural / 1000.0
        extra_natural = (kg1_natural / kg0 - 1.0) if kg0 > 0 else 0.0
        ceiling_clamped = extra_natural > ceiling + 1e-12
        extra_reported = min(extra_natural, ceiling)
        kg1 = kg0 * (1.0 + extra_reported)
        w_h1 = (kg1 * 1000.0 / (n * S1)) if (n > 0 and S1 > 0) else w_h1_natural
        fcr_factor = (1.0 - fcr_gain_max * mult * ds) if include_fcr_gain else 1.0
        FCR1 = FCR0 * fcr_factor
        gain1 = kg1 - n * S1 * w0 / 1000.0
        Revenue1 = kg1 * price
        Feed1 = gain1 * FCR1 * feed_price
        Profit1 = Revenue1 - Feed1 - Seed - Other - Elec1
        return {
            "G": G, "dS": dS, "fcr_factor": fcr_factor, "extra_kg_fraction": extra_reported,
            "ceiling_clamped": ceiling_clamped,
            "S1": S1, "w_h1_g": w_h1, "kg": kg1, "revenue": Revenue1, "feed": Feed1,
            "seed": Seed, "other": Other, "elec": Elec1, "profit": Profit1,
        }

    low = compute_case(low_case_factor)
    high = compute_case(1.0)

    if low["ceiling_clamped"] or high["ceiling_clamped"]:
        warnings.append({"code": "CEILING_CLAMPED",
                          "message": "Extra harvest capped at the internal +18% model."})

    def delta_for(case):
        kg_crop = case["kg"] - kg0
        revenue_crop = case["revenue"] - Revenue0
        feed_crop = case["feed"] - Feed0
        elec_crop = Elec1 - Elec0
        profit_crop = case["profit"] - Profit0
        # A9.3: dProfit_year = dProfit_crop x crops_per_year_tn - Maint_year (both cases). Maint_year
        # is well-defined as 0 internally when unit_price_inr is null (nothing to maintain a cost
        # on), but is reported as null there rather than a misleadingly precise "0" - confirmed
        # against site/js/model.js's own choice via the parity comparator.
        profit_year = profit_crop * crops_per_year - Maint_year
        return {
            "kg_crop": kg_crop, "kg_year": kg_crop * crops_per_year,
            "revenue_crop": revenue_crop, "feed_crop": feed_crop, "elec_crop": elec_crop,
            "profit_crop": profit_crop, "profit_year": profit_year,
            "maintenance_year": Maint_year if unit_price is not None else None,
        }

    delta_low = delta_for(low)
    delta_high = delta_for(high)

    # A9.3: capex includes the concentrator price; blocked only for "enter unit price" (null
    # unit_price_inr) or "No extra profit at these inputs" (dProfit_year_high <= 0).
    if unit_price is None:
        capex = None
        payback_status = "blocked"
        payback_reason = "enter unit price"
        months_low = None
        months_high = None
    else:
        capex = n_units_final * total_unit_cost * (1.0 - subsidy_pct / 100.0)
        if delta_high["profit_year"] <= 0:
            payback_status = "blocked"
            payback_reason = "No extra profit at these inputs"
            months_low = None
            months_high = None
        else:
            payback_status = "ok"
            payback_reason = None
            months_high = capex / (delta_high["profit_year"] / 12.0)
            months_low = capex / (delta_low["profit_year"] / 12.0) if delta_low["profit_year"] > 0 else None

    unit_status = "VERIFIED"
    o2_env = product.get("o2_input_lpm")
    if isinstance(o2_env, dict):
        unit_status = o2_env.get("status", unit_status)

    input_units = {
        "district": "-", "species": "-", "area_acre": "acre", "depth_m": "m",
        "density_per_acre": "animals/acre", "o2_input_lpm_override": "L/min",
        "power_kw_override": "kW", "stock_month": "1-12", "price_inr_kg": "INR/kg",
        "feed_price_inr_kg": "INR/kg", "bloom": "-", "existing_aeration_kw": "kW",
        "existing_run_h": "h/night", "tariff_inr_kwh": "INR/kWh", "unit_model": "-",
        "n_units": "count", "unit_price_inr": "INR", "concentrator_kw": "kW", "subsidy_pct": "%",
        "run_h": "h/night", "include_fcr_gain": "-", "tariff_id": "-",
        "concentrator_price_inr": "INR", "maintenance_pct": "% of capex", "station_name": "-",
    }
    inputs_resolved = {}
    for key, unit_str in input_units.items():
        if key in inputs:
            inputs_resolved[key] = {"value": inputs[key], "unit": unit_str, "status": "user", "source": "user input"}

    result = {
        "inputs_resolved": inputs_resolved,
        "station": {"name": station_name, "district": district, "source": V(station.get("source"))},
        "months": months,
        "crop": {"months": crop_months, "size_factor": float(size_factor), "G_T": float(G_T),
                 "G_T_ref": float(G_T_ref), "ds": float(ds)},
        "uplift": {
            "low": {k: low[k] for k in ("G", "dS", "fcr_factor", "extra_kg_fraction", "ceiling_clamped")},
            "high": {k: high[k] for k in ("G", "dS", "fcr_factor", "extra_kg_fraction", "ceiling_clamped")},
        },
        "baseline": {
            "n": float(n), "S0": float(S0), "w0_g": float(w0), "w_h0_g": float(w_h0), "kg": float(kg0),
            "revenue": float(Revenue0), "feed": float(Feed0), "seed": float(Seed), "other": float(Other),
            "elec": float(Elec0), "profit": float(Profit0),
        },
        "with_oxy": {
            "low": {k: low[k] for k in ("S1", "w_h1_g", "kg", "revenue", "feed", "seed", "other", "elec", "profit")},
            "high": {k: high[k] for k in ("S1", "w_h1_g", "kg", "revenue", "feed", "seed", "other", "elec", "profit")},
        },
        "delta": {"low": delta_low, "high": delta_high},
        "payback": {"status": payback_status, "reason": payback_reason, "capex": capex,
                    "months_low": months_low, "months_high": months_high},
        "unit": {
            "id": product.get("id"), "label": V(product.get("label")),
            "power_kw_shaft": float(power_kw_published), "power_kw_used": float(power_kw_used),
            "o2_input_lpm": float(o2_lpm_published) if o2_lpm_published is not None else None,
            "o2_input_lpm_used": float(o2_lpm_used),
            "price_inr": unit_price, "n_units": n_units_final, "n_best": n_best, "n_relief": n_relief,
            "sizing": sizing_mode, "o2_g_per_unit_night": float(m_o2_per_unit_g),
            "supply_mg_l_per_unit_night": float(m_o2_per_unit_g * 1000.0 / V_l),
            "deficit_max_mg_l": float(deficit_max), "status": unit_status,
            "concentrator_kw": concentrator_kw,
            "concentrator_price_inr": concentrator_price_input, "maintenance_pct": float(maintenance_pct),
        },
        "warnings": warnings,
        "assumptions": bucket["list"],
    }
    return result


def compare_stations(inputs: dict, data: dict) -> list:
    """MODEL_SPEC.md section 7, amendment A9.4: evaluate the same inputs with station_name set to
    each station in data['climate']['stations'] in file order, auto sizing. A station whose
    evaluate() throws yields {station, error} instead of a full row."""
    rows = []
    for station in data["climate"]["stations"]:
        station_name = V(station.get("name"))
        candidate_inputs = dict(inputs)
        candidate_inputs["station_name"] = station_name
        candidate_inputs["n_units"] = "auto"
        try:
            result = evaluate(candidate_inputs, data)
        except Exception as exc:  # noqa: BLE001 - a per-station failure must not abort the sweep
            field = getattr(exc, "field", None)
            rows.append({
                "station": station_name,
                "error": f"{type(exc).__name__}: {field if field is not None else str(exc)}",
            })
            continue
        elevation_m = V(station.get("elevation_m"))
        rows.append({
            "station": station_name,
            "district": V(station.get("district")),
            "elevation_m": float(elevation_m) if elevation_m is not None else 0.0,
            "G_T": result["crop"]["G_T"],
            "size_factor": result["crop"]["size_factor"],
            "harvest_size_g": result["baseline"]["w_h0_g"],
            "baseline_kg_crop": result["baseline"]["kg"],
            "ds": result["crop"]["ds"],
            "extra_kg_crop_high": result["delta"]["high"]["kg_crop"],
            "profit_year_high": result["delta"]["high"]["profit_year"],
            "n_best": result["unit"]["n_best"],
            "warnings": [w["code"] for w in result["warnings"]],
        })
    return rows


# --------------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------------

def _default_data_dir() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent / "site" / "data"


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if len(argv) < 2:
        print("usage: oracle.py <scenarios.json> [data_dir]", file=sys.stderr)
        return 2

    scenarios_path = pathlib.Path(argv[1])
    data_dir = pathlib.Path(argv[2]) if len(argv) > 2 else _default_data_dir()

    data = load_oxy_data(data_dir)
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))

    results = []
    for scenario in scenarios:
        try:
            if scenario.get("mode") == "compare_stations":
                rows = compare_stations(scenario["inputs"], data)
                results.append({"rows": rows})
            else:
                result = evaluate(scenario["inputs"], data)
                results.append(result)
        except Exception as exc:  # noqa: BLE001 - deliberately broad: fail-loud scenarios must be caught and reported
            field = getattr(exc, "field", None)
            results.append({"error": f"{type(exc).__name__}: {field if field is not None else str(exc)}"})

    print(json.dumps(results))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
