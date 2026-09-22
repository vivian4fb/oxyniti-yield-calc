#!/usr/bin/env python3
"""Build the pond report for a vetted request (plan/LEAD_CAPTURE.md).

The page never shows profit, payback, unit sizing or the month-by-month oxygen budget; this
tool produces them for one farmer, from the same inputs the calculator held, using the
independent Python oracle (tests/oracle.py, MODEL_SPEC.md). The owner reads the HTML (or the
PDF), then sends it on WhatsApp. Nothing is sent by this tool.

It refuses to build unless vet_lead.py says APPROVE, or REVIEW with --force. REJECT is final.

Usage:
    python tools/leads/make_report.py --ref OXY1.eyJ...          # code from WhatsApp
    python tools/leads/make_report.py --text pasted_message.txt
    python tools/leads/make_report.py --file lead.json
    ... --pdf              also print to PDF with Edge or Chrome (headless)
    ... --force            build a REVIEW-verdict request after you have checked it
    ... --out DIR          default tools/leads/reports/ (git-ignored: personal data)

Exit code: 0 built, 2 refused by the verdict, 3 could not read or evaluate.

Python 3.13, standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(HERE))

import oracle  # noqa: E402  (tests/oracle.py)
import vet_lead  # noqa: E402

REPORTS_DIR = HERE / "reports"
CONTACT_PHONE_DISPLAY = "+91 96597 27477"   # published on oxyniti.com, VERIFIED 2026-09-21
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ROLE_LABEL = {"owner": "Farm owner", "manager": "Farm manager", "planning": "Planning a new pond",
              "consultant": "Consultant / trader", "supplier": "Equipment supplier", "other": "Other"}


class ReportError(Exception):
    pass


# --------------------------------------------------------------------------- formatting

def inr(v) -> str:
    if v is None:
        return "—"
    v = float(v)
    sign = "−" if v < 0 else ""
    a = abs(v)
    if a >= 1e7:
        return f"{sign}₹{a/1e7:.2f} Cr"
    if a >= 1e5:
        return f"{sign}₹{a/1e5:.2f} L"
    return f"{sign}₹{a:,.0f}"


def kg(v) -> str:
    if v is None:
        return "—"
    v = float(v)
    return f"{v:,.0f} kg" if abs(v) >= 100 else f"{v:,.1f} kg"


def num(v, dp=1) -> str:
    if v is None:
        return "—"
    return f"{float(v):,.{dp}f}"


def band(lo, hi, fmt) -> str:
    return f"{fmt(lo)} – {fmt(hi)}"


def esc(s) -> str:
    return html.escape("" if s is None else str(s))


# --------------------------------------------------------------------------- inputs -> oracle

def oracle_inputs(payload: dict, data: dict) -> dict:
    """The page's inputs are already in the model's vocabulary. Two fixes: n_units null means
    auto, and a missing tariff rate is resolved from its preset or refused, never defaulted."""
    i = dict(payload["inputs"])
    if i.get("n_units") in (None, ""):
        i["n_units"] = "auto"
    if i.get("tariff_inr_kwh") in (None, ""):
        preset = next((p for p in data["economics"]["tariff_presets"] if p.get("id") == i.get("tariff_id")), None)
        if preset is None or preset.get("inr_per_kwh") is None:
            raise ReportError(f"tariff_inr_kwh missing and tariff_id {i.get('tariff_id')!r} is not a known preset")
        i["tariff_inr_kwh"] = oracle.V(preset["inr_per_kwh"])
    required = ["district", "species", "area_acre", "depth_m", "density_per_acre", "stock_month", "price_inr_kg",
                "feed_price_inr_kg", "bloom", "existing_aeration_kw", "existing_run_h", "unit_model", "run_h"]
    missing = [k for k in required if i.get(k) in (None, "")]
    if missing:
        raise ReportError("request is missing required inputs: " + ", ".join(missing))
    return i


def species_label(data: dict, species_id: str) -> str:
    for sp in data.get("species", []):
        if sp.get("id") == species_id:
            return sp.get("common_name_en") or species_id
    return species_id


# --------------------------------------------------------------------------- HTML

CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font-family: Segoe UI, Arial, sans-serif; color: #06333d; margin: 0; padding: 24px; line-height: 1.45; font-size: 13px; }
h1 { font-size: 22px; margin: 0 0 4px; } h2 { font-size: 16px; margin: 26px 0 8px; border-bottom: 2px solid #14d8c4; padding-bottom: 4px; }
.head { display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; border-bottom: 3px solid #06333d; padding-bottom: 12px; }
.brand { font-size: 26px; font-weight: 800; letter-spacing: 0.02em; } .muted { color: #5a7a80; font-size: 12px; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 12px; }
th, td { border: 1px solid #c9dfe2; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #eaf7f5; } td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
.bands { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 12px 0; }
.band { border: 1px solid #c9dfe2; border-radius: 8px; padding: 10px 12px; }
.band .lbl { font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: #5a7a80; }
.band .val { font-size: 18px; font-weight: 800; margin-top: 2px; } .band .sub { font-size: 11px; color: #5a7a80; }
.warn { background: #fff4ee; border: 1px solid #ffb59a; border-radius: 8px; padding: 8px 12px; margin: 6px 0; }
.status { font-size: 10px; padding: 1px 6px; border-radius: 10px; background: #eaf7f5; } .ASSUMED { background: #fff1c2; } .UNTESTED, .NOT_FOUND { background: #ffd9cc; }
.foot { margin-top: 28px; border-top: 1px solid #c9dfe2; padding-top: 10px; font-size: 11px; color: #5a7a80; }
.crop { background: #eaf7f5; }
"""


def render_html(payload: dict, result: dict, data: dict, verdict: dict, built_at: dt.datetime) -> str:
    c = payload["contact"]
    i = payload["inputs"]
    d = result["delta"]
    lo, hi = d["low"], d["high"]
    pb = result["payback"]
    u = result["unit"]
    b = result["baseline"]
    sp = species_label(data, i["species"])
    station = result.get("station") or {}
    crop_months = {m["m"] for m in result["crop"]["months"]} if isinstance(result["crop"].get("months"), list) and result["crop"]["months"] and isinstance(result["crop"]["months"][0], dict) else set(result["crop"].get("months") or [])

    def month_rows():
        out = []
        for m in result["months"]:
            cls = ' class="crop"' if (m.get("in_crop") or m["m"] in crop_months) else ""
            out.append(
                f"<tr{cls}><td>{MONTHS[m['m']][:3]}</td><td class=n>{num(m['t_air_c'])}</td><td class=n>{num(m['t_w_c'])}</td>"
                f"<td class=n>{num(m['c_s_mg_l'], 2)}</td><td class=n>{num(m['g_t'], 2)}</td><td class=n>{num(m.get('biomass_kg'), 0)}</td>"
                f"<td class=n>{num(m['do_dawn_base'], 2)}</td><td class=n>{num(m['do_dawn_oxy'], 2)}</td>"
                f"<td class=n>{num(m['s_base'], 2)}</td><td class=n>{num(m['s_oxy'], 2)}</td></tr>")
        return "\n".join(out)

    if pb.get("status") == "ok":
        payback_val = f"{num(pb['months_low'])} – {num(pb['months_high'])} months"
        payback_sub = f"Investment {inr(pb.get('capex'))} after subsidy"
    else:
        payback_val = "No payback at these inputs" if (pb.get("reason") or "").lower().startswith("no payback") else (pb.get("reason") or "Blocked").capitalize()
        payback_sub = f"Investment {inr(pb.get('capex'))}" if pb.get("capex") is not None else "Enter a real unit price to compute payback"

    warnings_html = "".join(f"<div class=warn><b>{esc(w.get('code'))}</b> — {esc(w.get('message'))}</div>" for w in result.get("warnings", [])) or "<p class=muted>No warnings for this pond.</p>"

    assumptions_rows = "\n".join(
        f"<tr><td>{esc(a.get('label'))}</td><td class=n>{esc(a.get('value'))} {esc(a.get('unit') or '')}</td>"
        f"<td><span class='status {esc(a.get('status'))}'>{esc(a.get('status'))}</span></td><td>{esc(a.get('date') or '')}</td><td>{esc(a.get('source') or '')}</td></tr>"
        for a in result.get("assumptions", []))

    aeration = f"{i['existing_aeration_kw']} kW × {i['existing_run_h']} h/night" if i.get("existing_aeration_kw") else "none"
    fcr_line = "applied (UNTESTED single-pond trial)" if i.get("include_fcr_gain") else "not applied"

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Oxyniti pond report {esc(payload['lead_id'])}</title><style>{CSS}</style></head>
<body>
<div class=head>
  <div><div class=brand>Oxyniti</div><div class=muted>OXY-Nano nano-bubble aeration · pond report</div></div>
  <div style="text-align:right"><div><b>Ref {esc(payload['lead_id'])}</b></div><div class=muted>Prepared {built_at:%d %B %Y}</div><div class=muted>Request received {esc(str(payload.get('ts', ''))[:10])}</div></div>
</div>

<h1>Report for {esc(c['name'])}</h1>
<p class=muted>{esc(c['village'])}, {esc(i['district'])} district · {esc(ROLE_LABEL.get(c.get('role'), c.get('role')))} · {esc(c.get('ponds'))} pond(s){(' · ' + esc(c.get('area_total_acre')) + ' acre total water area') if c.get('area_total_acre') else ''} · WhatsApp {esc(c['phone'])}</p>

<h2>Your pond as you described it</h2>
<table>
<tr><th>Species</th><td>{esc(sp)}</td><th>Pond</th><td>{i['area_acre']} acre × {i['depth_m']} m average depth</td></tr>
<tr><th>Stocking</th><td>{i['density_per_acre']:,}/acre, stocked in {MONTHS[int(i['stock_month'])]}</td><th>Bloom</th><td>{esc(i['bloom'])}</td></tr>
<tr><th>Existing aeration</th><td>{aeration}</td><th>Climate used</th><td>{esc(station.get('name'))}{(' (' + esc(station.get('district')) + ')') if station.get('district') else ''}</td></tr>
<tr><th>Farm-gate price</th><td>₹{i['price_inr_kg']}/kg</td><th>Feed price</th><td>₹{i['feed_price_inr_kg']}/kg</td></tr>
<tr><th>Electricity</th><td>{esc(i.get('tariff_id') or '')} at ₹{num(result['inputs_resolved'].get('tariff_inr_kwh', {}).get('value') if isinstance(result.get('inputs_resolved', {}).get('tariff_inr_kwh'), dict) else i.get('tariff_inr_kwh'), 2)}/kWh</td><th>Run hours</th><td>{i['run_h']} h/night</td></tr>
<tr><th>Unit</th><td>{esc(u.get('label') or u.get('id'))}, {u.get('o2_input_lpm_used', u.get('o2_input_lpm'))} L/min O₂, {u.get('power_kw_used', u.get('power_kw_shaft'))} kW</td><th>Sizing</th><td>{u.get('n_units')} unit(s), {esc(u.get('sizing'))}</td></tr>
<tr><th>Unit price</th><td>{inr(u.get('price_inr'))} + concentrator {inr(u.get('concentrator_price_inr'))}</td><th>Subsidy</th><td>{i.get('subsidy_pct') or 0} %</td></tr>
<tr><th>FCR gain</th><td colspan=3>{fcr_line}</td></tr>
</table>

<h2>What more oxygen is worth on this pond</h2>
<div class=bands>
  <div class=band><div class=lbl>Extra harvest</div><div class=val>{band(lo['kg_crop'], hi['kg_crop'], kg)} per crop</div><div class=sub>{band(lo['kg_year'], hi['kg_year'], kg)} per year, low – high</div></div>
  <div class=band><div class=lbl>Extra profit</div><div class=val>{band(lo['profit_crop'], hi['profit_crop'], inr)} per crop</div><div class=sub>{band(lo['profit_year'], hi['profit_year'], inr)} per year after maintenance</div></div>
  <div class=band><div class=lbl>Payback on the unit(s)</div><div class=val>{payback_val}</div><div class=sub>{payback_sub}</div></div>
  <div class=band><div class=lbl>Units</div><div class=val>{u.get('n_units')} × {esc(u.get('label') or u.get('id'))}</div><div class=sub>best for profit {u.get('n_best')}; full pre-dawn relief needs {u.get('n_relief')}; worst-month deficit {num(u.get('deficit_max_mg_l'), 2)} mg/L</div></div>
</div>
<p class=muted>Baseline for context: {kg(b['kg'])} harvest and {inr(b['profit'])} profit per crop without OXY-Nano. Uplift capped at the internal model's +18 % saleable kg, applied in proportion to how oxygen-limited each crop month is. Not a guarantee: we verify on your pond with a DO meter during the free demo.</p>

<h2>How the extra profit is built (per crop)</h2>
<table>
<tr><th></th><th class=n>Low case</th><th class=n>High case</th></tr>
<tr><td>Extra revenue</td><td class=n>{inr(lo['revenue_crop'])}</td><td class=n>{inr(hi['revenue_crop'])}</td></tr>
<tr><td>Extra feed</td><td class=n>−{inr(lo['feed_crop'])}</td><td class=n>−{inr(hi['feed_crop'])}</td></tr>
<tr><td>Extra electricity</td><td class=n>−{inr(lo['elec_crop'])}</td><td class=n>−{inr(hi['elec_crop'])}</td></tr>
<tr><th>Extra profit per crop</th><th class=n>{inr(lo['profit_crop'])}</th><th class=n>{inr(hi['profit_crop'])}</th></tr>
<tr><td>Maintenance per year</td><td class=n>−{inr(lo['maintenance_year'])}</td><td class=n>−{inr(hi['maintenance_year'])}</td></tr>
<tr><th>Extra profit per year</th><th class=n>{inr(lo['profit_year'])}</th><th class=n>{inr(hi['profit_year'])}</th></tr>
</table>

<h2>Night-time oxygen budget, month by month</h2>
<p class=muted>Crop months are shaded. Dawn DO is the dissolved oxygen the fish experience at first light; stress runs from 0 (above the growth threshold) to 1 (at the lethal limit).</p>
<table>
<tr><th>Month</th><th class=n>Air °C</th><th class=n>Water °C</th><th class=n>DO sat. mg/L</th><th class=n>Thermal factor</th><th class=n>Biomass kg</th><th class=n>Dawn DO before</th><th class=n>Dawn DO with OXY-Nano</th><th class=n>Stress before</th><th class=n>Stress after</th></tr>
{month_rows()}
</table>

<h2>Warnings</h2>
{warnings_html}

<h2>Every number behind this report</h2>
<table><tr><th>Parameter</th><th class=n>Value</th><th>Status</th><th>Date</th><th>Source</th></tr>
{assumptions_rows}
</table>

<div class=foot>
<p>Estimates only, from monthly climate normals and sourced species data (plan/MODEL_SPEC.md). Prices marked ASSUMED are rough estimates until replaced by a quotation. Next step: a free DO-meter demo on your pond. WhatsApp {CONTACT_PHONE_DISPLAY}.</p>
<p>Vetting: {esc(verdict['verdict'])} on {built_at:%Y-%m-%d} — {esc('; '.join(t for s, t in verdict['reasons'] if s != 'note'))or 'no signals'}. Internal line; remove before sending if you print this page.</p>
</div>
</body></html>
"""


# --------------------------------------------------------------------------- PDF

def find_browser() -> str | None:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if pathlib.Path(c).exists():
            return c
    for name in ("msedge", "chrome", "google-chrome", "chromium"):
        p = shutil.which(name)
        if p:
            return p
    return None


def print_pdf(html_path: pathlib.Path) -> pathlib.Path:
    browser = find_browser()
    if not browser:
        raise ReportError("no Edge or Chrome found for --pdf; open the HTML and print it instead")
    pdf_path = html_path.with_suffix(".pdf")
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not pdf_path.exists():
        raise ReportError(f"PDF was not produced (exit {proc.returncode}): {proc.stderr[-400:]}")
    return pdf_path


# --------------------------------------------------------------------------- build

def build(payload: dict, verdict: dict, out_dir: pathlib.Path, data: dict | None = None,
          built_at: dt.datetime | None = None) -> pathlib.Path:
    data = data or oracle.load_oxy_data(ROOT / "site" / "data")
    built_at = built_at or dt.datetime.now()
    inputs = oracle_inputs(payload, data)
    try:
        result = oracle.evaluate(inputs, data)
    except oracle.MissingDataError as exc:
        raise ReportError(f"model refused the request: {exc}") from exc
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{payload['lead_id']}.html"
    out.write_text(render_html(payload, result, data, verdict, built_at), encoding="utf-8")
    (out_dir / f"{payload['lead_id']}.result.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--ref")
    ap.add_argument("--text")
    ap.add_argument("--file")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--force", action="store_true", help="build a REVIEW request after checking it yourself")
    ap.add_argument("--out", default=str(REPORTS_DIR))
    ap.add_argument("--ledger", default=str(vet_lead.LEDGER_PATH))
    args = ap.parse_args(argv)

    try:
        payload = vet_lead.load_from_args(args)
    except vet_lead.LeadReadError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    verdict = vet_lead.vet(payload, vet_lead.read_ledger(pathlib.Path(args.ledger)))
    vet_lead.print_report(payload, verdict)
    if verdict["verdict"] == "REJECT":
        print("Refusing to build: verdict REJECT.", file=sys.stderr)
        return 2
    if verdict["verdict"] == "REVIEW" and not args.force:
        print("Refusing to build: verdict REVIEW. Check the reasons above, then re-run with --force.", file=sys.stderr)
        return 2

    try:
        out = build(payload, verdict, pathlib.Path(args.out))
        print(f"report: {out}")
        if args.pdf:
            print(f"pdf:    {print_pdf(out)}")
    except ReportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
