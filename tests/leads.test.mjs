/*
 * tests/leads.test.mjs — contract tests for site/js/leads.js (plan/LEAD_CAPTURE.md).
 * Pure helpers only: phone normalisation, validation, reference-code round trip, payload
 * shape, WhatsApp text. Also writes tests/fixtures/lead.example.json and lead.example.ref so
 * tests/test_vet_lead.py can prove the Python decoder reads what the browser encodes.
 *
 * Node 22 built-in test runner, no npm packages:  node --test tests/
 */

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const require = createRequire(import.meta.url);
const Leads = require(path.join(ROOT, "site", "js", "leads.js"));

const CFG = { minTimeOnPageMs: 4000 };

function goodFields(over = {}) {
  return Object.assign({
    name: "Murugan S",
    phone: "+91 98400 12345",
    village: "Lalgudi",
    role: "owner",
    ponds: "2-5",
    area_total_acre: "3.5",
    email: "",
    best_time: "evening",
    consent: true
  }, over);
}
function goodSignals(over = {}) {
  return Object.assign({ t_ms: 42000, honeypot: "", challenge_ok: true }, over);
}
const INPUTS = {
  district: "Tiruchirappalli", station_name: null, species: "gift-tilapia", area_acre: 1, depth_m: 1.5,
  density_per_acre: 5965, stock_month: 6, price_inr_kg: 120, feed_price_inr_kg: 60, bloom: "medium",
  existing_aeration_kw: 0, existing_run_h: 0, tariff_id: "lt-iii-a1", tariff_inr_kwh: null,
  unit_model: "oxy-nano-1.5hp", n_units: null, o2_input_lpm_override: null, power_kw_override: null,
  unit_price_inr: 85000, concentrator_kw: 0.69, concentrator_price_inr: 45000, maintenance_pct: 3,
  subsidy_pct: 0, run_h: 8, include_fcr_gain: false
};
const RESULT = {
  delta: { low: { kg_crop: 10.2, kg_year: 20.4, profit_year: -57000 }, high: { kg_crop: 20.1, kg_year: 40.2, profit_year: -30000 } },
  payback: { status: "blocked", reason: "no payback", capex: 130000 },
  unit: { n_units: 1, n_best: 1 },
  warnings: [{ code: "NO_PAYBACK_AT_PUBLISHED_O2", message: "x" }]
};

/* ------------------------------------------------------------------ phone */

test("normalisePhone accepts +91, 91, 0 prefixes and spaces", () => {
  for (const raw of ["9840012345", "+91 98400 12345", "91-9840012345", "09840012345", "(98400) 12345"]) {
    const r = Leads.normalisePhone(raw);
    assert.equal(r.ok, true, raw);
    assert.equal(r.e164, "+919840012345");
  }
});

test("normalisePhone rejects short, landline-prefixed, repeated and sequential numbers", () => {
  assert.equal(Leads.normalisePhone("98400123").ok, false);
  assert.equal(Leads.normalisePhone("0431234567").reason, "prefix");
  assert.equal(Leads.normalisePhone("9999999999").reason, "repeated");
  assert.equal(Leads.normalisePhone("9876543210").reason, "sequence");
  assert.equal(Leads.normalisePhone("").reason, "empty");
});

/* ------------------------------------------------------------------ validate */

test("validate passes a complete, unhurried, consenting request", () => {
  const v = Leads.validate(goodFields(), goodSignals(), CFG);
  assert.deepEqual(v.errors, {});
  assert.equal(v.ok, true);
  assert.equal(v.honeypot, false);
});

test("validate flags each missing or wrong field by key", () => {
  const v = Leads.validate(goodFields({ name: "M", phone: "12345", village: "", role: "ceo", ponds: "9", email: "nope", consent: false }), goodSignals({ challenge_ok: false }), CFG);
  assert.equal(v.ok, false);
  for (const k of ["name", "phone", "village", "role", "ponds", "email", "consent", "challenge"]) assert.ok(v.errors[k], k);
});

test("validate blocks a submission faster than minTimeOnPageMs", () => {
  const v = Leads.validate(goodFields(), goodSignals({ t_ms: 900 }), CFG);
  assert.equal(v.errors.timing, "lead.err.timing");
});

test("validate reports a filled honeypot without adding a field error", () => {
  const v = Leads.validate(goodFields(), goodSignals({ honeypot: "http://spam.example" }), CFG);
  assert.equal(v.ok, true);
  assert.equal(v.honeypot, true);
});

test("validate accepts Tamil-script names", () => {
  const v = Leads.validate(goodFields({ name: "முருகன்" }), goodSignals(), CFG);
  assert.equal(v.errors.name, undefined);
});

/* ------------------------------------------------------------------ lead id */

test("makeLeadId is OXY-YYYYMMDD-XXXXX with a base-32 suffix", () => {
  const id = Leads.makeLeadId(new Date(Date.UTC(2026, 8, 22, 10, 0, 0)), [0, 1, 2, 3, 4]);
  assert.match(id, /^OXY-20260922-[A-Z2-9]{5}$/);
  assert.equal(id, "OXY-20260922-ABCDE");
});

/* ------------------------------------------------------------------ payload + ref */

function buildExample() {
  return Leads.buildPayload({
    lead_id: "OXY-20260922-K7Q4M", ts: "2026-09-22T10:00:00.000Z",
    contact: goodFields({ name: "முருகன் S" }), inputs: INPUTS, result: RESULT,
    signals: { lang: "en", t_ms: 42000, interactions: 7, tz_min: -330, ref_host: "www.instagram.com", ua: "Mozilla/5.0 test", viewport: "390x844", pointer: "coarse", turnstile_token: null },
    page: "https://vivian4fb.github.io/oxyniti-yield-calc/"
  });
}

test("buildPayload normalises the phone, keeps every input key and summarises the result", () => {
  const p = buildExample();
  assert.equal(p.contact.phone, "+919840012345");
  assert.equal(p.contact.area_total_acre, 3.5);
  assert.equal(Object.keys(p.inputs).length, 25);
  assert.equal(p.inputs.n_units, null);
  assert.deepEqual(p.headline.extra_kg_crop, [10.2, 20.1]);
  assert.equal(p.headline.payback_status, "blocked");
  assert.deepEqual(p.headline.warnings, ["NO_PAYBACK_AT_PUBLISHED_O2"]);
});

test("encodeRef/decodeRef round-trip contact, inputs and the vetting signals, and carry no result", () => {
  const p = buildExample();
  const ref = Leads.encodeRef(p);
  assert.match(ref, /^OXY1\.[A-Za-z0-9_-]+$/);
  assert.ok(ref.length < 700, "ref length " + ref.length);
  const back = Leads.decodeRef(ref);
  assert.equal(back.lead_id, p.lead_id);
  assert.deepEqual(back.contact, p.contact);
  assert.deepEqual(back.inputs, p.inputs);
  assert.deepEqual(back.signals, { lang: "en", t_ms: 42000, interactions: 7, tz_min: -330, ref_host: "www.instagram.com" });
  assert.equal(back.headline, undefined);
  assert.equal(ref.indexOf("57000"), -1);
});

test("decodeRef refuses foreign strings and wrong versions", () => {
  assert.throws(() => Leads.decodeRef("hello"), /not a reference code/);
  assert.throws(() => Leads.decodeRef("OXY1.W1t"), /JSON|Unexpected/);
  const bad = "OXY1." + Buffer.from(JSON.stringify([2, "x"])).toString("base64url");
  assert.throws(() => Leads.decodeRef(bad), /fields/);
});

test("buildWhatsAppText names the farmer, the pond and the reference", () => {
  const p = buildExample();
  const ref = Leads.encodeRef(p);
  const text = Leads.buildWhatsAppText(p, ref, { speciesLabel: "GIFT tilapia", monthLabel: "stocked June" });
  assert.match(text, /OXY-20260922-K7Q4M/);
  assert.match(text, /Lalgudi, Tiruchirappalli/);
  assert.match(text, /GIFT tilapia, 1 acre, 1.5 m, 5965\/acre, stocked June, medium bloom/);
  assert.ok(text.endsWith("Ref: " + ref));
  assert.equal(text.indexOf("57000"), -1, "no model output in the message");
});

/* ------------------------------------------------------------------ fixture for the Python side */

test("writes the lead fixture the Python decoder test reads", () => {
  const p = buildExample();
  const ref = Leads.encodeRef(p);
  const dir = path.join(HERE, "fixtures");
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "lead.example.json"), JSON.stringify(p, null, 2) + "\n");
  fs.writeFileSync(path.join(dir, "lead.example.ref"), ref + "\n");
  assert.ok(fs.existsSync(path.join(dir, "lead.example.ref")));
});

test("REF_FIELDS is the documented wire order (change tools/leads/vet_lead.py with it)", () => {
  assert.equal(Leads.REF_FIELDS.length, 41);
  assert.equal(Leads.REF_FIELDS[0], "v");
  assert.equal(Leads.REF_FIELDS[Leads.REF_FIELDS.length - 1], "ref_host");
});
