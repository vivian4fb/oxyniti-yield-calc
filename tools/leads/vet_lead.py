#!/usr/bin/env python3
"""Vet a pond-report request before any report is built or sent (plan/LEAD_CAPTURE.md).

A request reaches the owner either as a WhatsApp message carrying a reference code
("OXY1.<base64url>") produced by site/js/leads.js, or as a JSON POST relayed by the endpoint
in site/js/leads.config.js. This tool decodes it, scores the bot and competitor signals,
prints every reason, and gives one of three verdicts:

    APPROVE  build and send the report (tools/leads/make_report.py)
    REVIEW   a person decides; make_report.py needs --force
    REJECT   do not build; make_report.py refuses

It never sends anything and never fabricates a field. Verdict rules are listed in vet();
the keyword list lives in competitor_signals.txt (owner-maintained, patterns only).

Usage:
    python tools/leads/vet_lead.py --ref OXY1.eyJ...            # code copied from WhatsApp
    python tools/leads/vet_lead.py --text pasted_message.txt    # whole WhatsApp message
    python tools/leads/vet_lead.py --file lead.json             # endpoint payload
    ... --record          also append to tools/leads/ledger.jsonl and save inbox/<lead_id>.json
    ... --json            machine-readable output

Exit code: 0 APPROVE, 1 REVIEW, 2 REJECT, 3 could not read the request.

Python 3.13, standard library only.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
LEDGER_PATH = HERE / "ledger.jsonl"
INBOX_DIR = HERE / "inbox"
SIGNALS_PATH = HERE / "competitor_signals.txt"

REF_VERSION = 1
REF_PREFIX = "OXY1."
REF_RE = re.compile(r"OXY1\.[A-Za-z0-9_-]{20,}")

# Wire order shared with site/js/leads.js (REF_FIELDS). Change both or neither.
REF_FIELDS = [
    "v", "lead_id", "ts",
    "name", "phone", "village", "role", "ponds", "area_total_acre", "email", "best_time",
    "district", "station_name", "species", "area_acre", "depth_m", "density_per_acre", "stock_month",
    "price_inr_kg", "feed_price_inr_kg", "bloom", "existing_aeration_kw", "existing_run_h",
    "tariff_id", "tariff_inr_kwh", "unit_model", "n_units", "o2_input_lpm_override",
    "power_kw_override", "unit_price_inr", "concentrator_kw", "concentrator_price_inr",
    "maintenance_pct", "subsidy_pct", "run_h", "include_fcr_gain",
    "lang", "t_ms", "interactions", "tz_min", "ref_host",
]
CONTACT_FIELDS = ["name", "phone", "village", "role", "ponds", "area_total_acre", "email", "best_time"]
INPUT_FIELDS = REF_FIELDS[11:36]
SIGNAL_FIELDS = ["lang", "t_ms", "interactions", "tz_min", "ref_host"]

MIN_TIME_ON_PAGE_MS = 4000          # mirrors OXY_LEADS_CONFIG.minTimeOnPageMs
QUICK_AND_UNTOUCHED_MS = 20000      # form done in under 20 s with no slider touched
IST_OFFSET_MIN = -330               # JavaScript getTimezoneOffset() for Asia/Kolkata
DUPLICATE_WINDOW_DAYS = 30
FREE_MAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "yahoo.in", "yahoo.co.in", "outlook.com", "hotmail.com", "live.com",
    "rediffmail.com", "protonmail.com", "proton.me", "icloud.com", "ymail.com",
}


class LeadReadError(Exception):
    """The request could not be decoded. Fail loudly; never guess a field."""


# --------------------------------------------------------------------------- decoding

def decode_ref(code: str) -> dict:
    s = (code or "").strip()
    if not s.startswith(REF_PREFIX):
        raise LeadReadError("not a reference code (expected prefix OXY1.)")
    b64 = s[len(REF_PREFIX):]
    b64 += "=" * (-len(b64) % 4)
    try:
        raw = base64.urlsafe_b64decode(b64.encode("ascii")).decode("utf-8")
        arr = json.loads(raw)
    except Exception as exc:  # noqa: BLE001 - any decoding failure is the same failure to the caller
        raise LeadReadError(f"reference code is not valid base64url JSON: {exc}") from exc
    if not isinstance(arr, list) or len(arr) != len(REF_FIELDS):
        raise LeadReadError(f"reference code has {len(arr) if isinstance(arr, list) else 'no'} fields, expected {len(REF_FIELDS)}")
    if arr[0] != REF_VERSION:
        raise LeadReadError(f"reference code version {arr[0]!r} is not {REF_VERSION}")
    flat = dict(zip(REF_FIELDS, arr))
    return {
        "v": flat["v"],
        "lead_id": flat["lead_id"],
        "ts": flat["ts"],
        "contact": {k: flat[k] for k in CONTACT_FIELDS},
        "inputs": {k: flat[k] for k in INPUT_FIELDS},
        "signals": {k: flat[k] for k in SIGNAL_FIELDS},
        "source": "ref",
    }


def extract_ref(text: str) -> str:
    m = REF_RE.search(text or "")
    if not m:
        raise LeadReadError("no OXY1. reference code found in the text")
    return m.group(0)


def load_payload_file(path: pathlib.Path) -> dict:
    """Accepts the full payload leads.js POSTs (nested) or the flat form an e-mail relay
    (Web3Forms and the like) hands back, where inputs/headline/signals are JSON strings."""
    obj = json.loads(path.read_text(encoding="utf-8"))
    if "contact" in obj and "inputs" in obj:
        obj.setdefault("source", "file")
        return obj
    if "ref" in obj and isinstance(obj["ref"], str) and obj["ref"].startswith(REF_PREFIX):
        p = decode_ref(obj["ref"])
        for k in ("inputs_json", "headline_json", "signals_json"):
            if isinstance(obj.get(k), str):
                try:
                    p[k[:-5]] = json.loads(obj[k])
                except json.JSONDecodeError as exc:
                    raise LeadReadError(f"{k} is not valid JSON: {exc}") from exc
        p["source"] = "endpoint"
        return p
    raise LeadReadError("file is neither a lead payload nor an endpoint relay with a ref")


# --------------------------------------------------------------------------- signals

def load_signal_patterns(path: pathlib.Path = SIGNALS_PATH) -> list[str]:
    if not path.exists():
        raise LeadReadError(f"competitor signal list missing: {path}")
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line.lower())
    return out


def read_ledger(path: pathlib.Path = LEDGER_PATH) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _phone_ok(phone) -> bool:
    digits = re.sub(r"\D", "", str(phone or ""))
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    if len(digits) != 10 or digits[0] not in "6789":
        return False
    if len(set(digits)) == 1 or digits in {"1234567890", "9876543210", "6789012345"}:
        return False
    return True


def _parse_ts(ts) -> dt.datetime | None:
    try:
        return dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def vet(payload: dict, ledger: list[dict] | None = None, patterns: list[str] | None = None) -> dict:
    """Returns {"verdict", "score", "reasons": [(severity, text)]}.
    severity: "reject" (certain), "review" (needs a person), "note" (informational)."""
    ledger = ledger or []
    patterns = patterns if patterns is not None else load_signal_patterns()
    c = payload.get("contact") or {}
    i = payload.get("inputs") or {}
    s = payload.get("signals") or {}
    reasons: list[tuple[str, str]] = []

    def reject(t): reasons.append(("reject", t))
    def review(t): reasons.append(("review", t))
    def note(t): reasons.append(("note", t))

    # --- certain bot signals -------------------------------------------------------------
    if s.get("honeypot"):
        reject("honeypot field was filled")
    t_ms = s.get("t_ms")
    if isinstance(t_ms, (int, float)) and t_ms < MIN_TIME_ON_PAGE_MS:
        reject(f"form submitted {t_ms/1000:.1f} s after page load (minimum {MIN_TIME_ON_PAGE_MS/1000:.0f} s)")
    if not _phone_ok(c.get("phone")):
        reject(f"phone {c.get('phone')!r} is not a valid Indian mobile number")
    name = str(c.get("name") or "").strip()
    if len(name) < 2 or not re.search(r"[^\W\d_]", name):
        reject(f"name {name!r} has no letters")
    for row in ledger:
        if row.get("lead_id") == payload.get("lead_id"):
            reject(f"lead_id {payload.get('lead_id')} already in the ledger (verdict {row.get('verdict')})")
            break
    ua = str(s.get("ua") or "")
    if re.search(r"headless|python-requests|curl/|wget/|bot\b|spider|crawler", ua, re.I):
        reject(f"user agent looks automated: {ua[:60]}")

    # --- signals that need a person ------------------------------------------------------
    role = c.get("role")
    if role in ("supplier", "consultant"):
        review(f"self-declared role is {role!r}")
    haystack = " ".join(str(c.get(k) or "") for k in ("name", "village", "email", "best_time")).lower()
    hits = [p for p in patterns if p in haystack]
    if hits:
        review("competitor/vendor words in contact fields: " + ", ".join(hits))
    email = str(c.get("email") or "").strip().lower()
    if email and "@" in email:
        domain = email.rsplit("@", 1)[1]
        if domain not in FREE_MAIL_DOMAINS:
            review(f"corporate e-mail domain {domain}")
    ref_host = str(s.get("ref_host") or "").lower()
    if ref_host and any(p in ref_host for p in patterns):
        review(f"referrer {ref_host} matches the signal list")
    overrides = [k for k in ("o2_input_lpm_override", "power_kw_override") if i.get(k) not in (None, "")]
    if overrides:
        review("datasheet overrides set in Advanced: " + ", ".join(overrides) + " (probing the model)")
    if i.get("n_units") not in (None, "auto"):
        review(f"manual unit count {i.get('n_units')}")
    inter = s.get("interactions")
    if isinstance(t_ms, (int, float)) and t_ms < QUICK_AND_UNTOUCHED_MS and inter == 0:
        review(f"no calculator interaction and only {t_ms/1000:.0f} s on the page")
    tz = s.get("tz_min")
    if isinstance(tz, (int, float)) and int(tz) != IST_OFFSET_MIN:
        review(f"browser timezone offset {tz} min is not India ({IST_OFFSET_MIN})")
    area_total = c.get("area_total_acre")
    if isinstance(area_total, (int, float)) and area_total > 100 and role not in ("owner", "manager"):
        review(f"{area_total} acre total water area with role {role!r}")
    if c.get("ponds") == "20+" and role == "planning":
        review("planning a new pond yet reports more than 20 ponds")
    when = _parse_ts(payload.get("ts"))
    for row in ledger:
        if row.get("phone") == c.get("phone") and row.get("lead_id") != payload.get("lead_id"):
            prev = _parse_ts(row.get("ts"))
            if when and prev and abs((when - prev).days) <= DUPLICATE_WINDOW_DAYS:
                review(f"same phone requested {row.get('lead_id')} on {row.get('ts', '')[:10]} (verdict {row.get('verdict')})")
                break

    # --- notes ---------------------------------------------------------------------------
    if s.get("lang"):
        note(f"page language {s.get('lang')}")
    if ref_host:
        note(f"arrived from {ref_host}")
    if payload.get("headline"):
        h = payload["headline"]
        note(f"headline sent with the request: extra kg/crop {h.get('extra_kg_crop')}, payback {h.get('payback_status')}")
    if not any(sev == "review" for sev, _ in reasons) and not any(sev == "reject" for sev, _ in reasons):
        note("no bot or competitor signal found")

    n_reject = sum(1 for sev, _ in reasons if sev == "reject")
    n_review = sum(1 for sev, _ in reasons if sev == "review")
    if n_reject:
        verdict = "REJECT"
    elif n_review:
        verdict = "REVIEW"
    else:
        verdict = "APPROVE"
    return {"verdict": verdict, "score": n_reject * 10 + n_review, "reasons": reasons}


# --------------------------------------------------------------------------- recording

def record(payload: dict, verdict: dict, ledger_path: pathlib.Path = LEDGER_PATH, inbox_dir: pathlib.Path = INBOX_DIR) -> pathlib.Path:
    """Append one ledger line and save the full request. Both paths are git-ignored: they
    hold personal data and must never enter the public repository."""
    inbox_dir.mkdir(parents=True, exist_ok=True)
    c = payload.get("contact") or {}
    row = {
        "lead_id": payload.get("lead_id"),
        "ts": payload.get("ts"),
        "vetted_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "phone": c.get("phone"),
        "name": c.get("name"),
        "district": (payload.get("inputs") or {}).get("district"),
        "verdict": verdict["verdict"],
        "score": verdict["score"],
        "source": payload.get("source"),
    }
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    out = inbox_dir / f"{payload.get('lead_id')}.json"
    out.write_text(json.dumps({"payload": payload, "vet": verdict}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


# --------------------------------------------------------------------------- CLI

def load_from_args(args) -> dict:
    if args.ref:
        return decode_ref(args.ref)
    if args.text:
        return decode_ref(extract_ref(pathlib.Path(args.text).read_text(encoding="utf-8")))
    if args.file:
        return load_payload_file(pathlib.Path(args.file))
    raise LeadReadError("give --ref, --text or --file")


def print_report(payload: dict, verdict: dict) -> None:
    c = payload.get("contact") or {}
    i = payload.get("inputs") or {}
    s = payload.get("signals") or {}
    print(f"Lead {payload.get('lead_id')}  received {payload.get('ts')}  via {payload.get('source')}")
    print(f"  {c.get('name')}  {c.get('phone')}  {c.get('village')}, {i.get('district')}")
    print(f"  role {c.get('role')}  ponds {c.get('ponds')}  total area {c.get('area_total_acre')} acre  email {c.get('email') or '-'}  call {c.get('best_time') or '-'}")
    print(f"  pond: {i.get('species')}  {i.get('area_acre')} acre x {i.get('depth_m')} m  {i.get('density_per_acre')}/acre  month {i.get('stock_month')}  bloom {i.get('bloom')}  aeration {i.get('existing_aeration_kw')} kW x {i.get('existing_run_h')} h")
    print(f"  unit {i.get('unit_model')}  n_units {i.get('n_units')}  price {i.get('unit_price_inr')}  tariff {i.get('tariff_id')}/{i.get('tariff_inr_kwh')}  subsidy {i.get('subsidy_pct')} %")
    print(f"  signals: {s.get('t_ms')} ms on page, {s.get('interactions')} interactions, tz {s.get('tz_min')}, lang {s.get('lang')}, from {s.get('ref_host') or '-'}")
    print()
    for sev, text in verdict["reasons"]:
        print(f"  [{sev.upper():6}] {text}")
    print()
    print(f"VERDICT {verdict['verdict']}  (score {verdict['score']})")


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--ref", help="OXY1. reference code")
    ap.add_argument("--text", help="file holding a pasted WhatsApp message that contains the code")
    ap.add_argument("--file", help="JSON payload from the endpoint")
    ap.add_argument("--record", action="store_true", help="append to ledger.jsonl and save inbox/<lead_id>.json")
    ap.add_argument("--ledger", default=str(LEDGER_PATH))
    ap.add_argument("--json", action="store_true", help="print the payload and verdict as JSON")
    args = ap.parse_args(argv)

    try:
        payload = load_from_args(args)
    except LeadReadError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    ledger_path = pathlib.Path(args.ledger)
    verdict = vet(payload, read_ledger(ledger_path))
    if args.json:
        print(json.dumps({"payload": payload, "vet": verdict}, ensure_ascii=False, indent=2))
    else:
        print_report(payload, verdict)
    if args.record:
        out = record(payload, verdict, ledger_path=ledger_path, inbox_dir=ledger_path.parent / "inbox")
        print(f"recorded: {out}")
    return {"APPROVE": 0, "REVIEW": 1, "REJECT": 2}[verdict["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
