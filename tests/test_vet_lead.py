"""tests/test_vet_lead.py — the owner-side lead tools (plan/LEAD_CAPTURE.md).

    node --test tests/leads.test.mjs      # first: writes tests/fixtures/lead.example.{json,ref}
    python -m unittest tests/test_vet_lead.py

Proves: the Python decoder reads what the browser encodes; the verdict rules fire on the
signals they claim to; make_report refuses REJECT/REVIEW and builds a full report for a clean
request using the independent oracle. Python 3.13, standard library only.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools" / "leads"))
sys.path.insert(0, str(HERE))

import make_report  # noqa: E402
import oracle  # noqa: E402
import vet_lead  # noqa: E402

FIXTURE_JSON = HERE / "fixtures" / "lead.example.json"
FIXTURE_REF = HERE / "fixtures" / "lead.example.ref"
PATTERNS = vet_lead.load_signal_patterns()


def clean_payload() -> dict:
    """A plausible farmer request built on the first scenario in tests/scenarios.json, so the
    oracle can evaluate it. Contact details are invented test values, not a real person."""
    scenario = json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))[0]
    inputs = dict(scenario["inputs"])
    inputs["n_units"] = None
    return {
        "v": 1, "lead_id": "OXY-20260922-TEST1", "ts": "2026-09-22T09:30:00.000Z",
        "contact": {"name": "Farmer One", "phone": "+919840012345", "village": "Sirkazhi", "role": "owner",
                    "ponds": "2-5", "area_total_acre": 3.0, "email": None, "best_time": None},
        "inputs": inputs,
        "signals": {"lang": "en", "t_ms": 65000, "interactions": 9, "tz_min": -330, "ref_host": None},
        "source": "test",
    }


class DecodeTests(unittest.TestCase):
    def test_wire_order_matches_the_browser(self):
        self.assertEqual(len(vet_lead.REF_FIELDS), 41)
        self.assertEqual(vet_lead.INPUT_FIELDS[0], "district")
        self.assertEqual(vet_lead.INPUT_FIELDS[-1], "include_fcr_gain")
        self.assertEqual(len(vet_lead.INPUT_FIELDS), 25)

    def test_decodes_the_fixture_the_browser_module_wrote(self):
        self.assertTrue(FIXTURE_REF.exists(), "run node --test tests/leads.test.mjs first")
        expected = json.loads(FIXTURE_JSON.read_text(encoding="utf-8"))
        got = vet_lead.decode_ref(FIXTURE_REF.read_text(encoding="utf-8"))
        self.assertEqual(got["lead_id"], expected["lead_id"])
        self.assertEqual(got["contact"], expected["contact"])
        self.assertEqual(got["inputs"], expected["inputs"])
        self.assertEqual(got["signals"]["t_ms"], expected["signals"]["t_ms"])
        self.assertEqual(got["contact"]["name"], "முருகன் S")
        self.assertNotIn("headline", got)

    def test_extracts_the_code_from_a_whatsapp_message(self):
        ref = FIXTURE_REF.read_text(encoding="utf-8").strip()
        text = "Oxyniti pond report request OXY-20260922-K7Q4M\nName: x\nRef: " + ref + "\n"
        self.assertEqual(vet_lead.extract_ref(text), ref)
        with self.assertRaises(vet_lead.LeadReadError):
            vet_lead.extract_ref("no code here")

    def test_refuses_foreign_and_short_codes(self):
        with self.assertRaises(vet_lead.LeadReadError):
            vet_lead.decode_ref("hello")
        with self.assertRaises(vet_lead.LeadReadError):
            vet_lead.decode_ref("OXY1.W1td")


class VetTests(unittest.TestCase):
    def verdict(self, mutate=None, ledger=None):
        p = clean_payload()
        if mutate:
            mutate(p)
        return vet_lead.vet(p, ledger or [], PATTERNS)

    def reasons(self, v, severity):
        return [t for s, t in v["reasons"] if s == severity]

    def test_clean_request_is_approved(self):
        v = self.verdict()
        self.assertEqual(v["verdict"], "APPROVE", v)
        self.assertEqual(self.reasons(v, "review"), [])

    def test_honeypot_rejects(self):
        v = self.verdict(lambda p: p["signals"].__setitem__("honeypot", "http://x"))
        self.assertEqual(v["verdict"], "REJECT")

    def test_too_fast_rejects(self):
        v = self.verdict(lambda p: p["signals"].__setitem__("t_ms", 1200))
        self.assertEqual(v["verdict"], "REJECT")
        self.assertTrue(any("after page load" in t for t in self.reasons(v, "reject")))

    def test_bad_phone_rejects(self):
        for bad in ("+919999999999", "0431234567", "12345"):
            v = self.verdict(lambda p, b=bad: p["contact"].__setitem__("phone", b))
            self.assertEqual(v["verdict"], "REJECT", bad)

    def test_automated_user_agent_rejects(self):
        v = self.verdict(lambda p: p["signals"].__setitem__("ua", "python-requests/2.32"))
        self.assertEqual(v["verdict"], "REJECT")

    def test_duplicate_lead_id_rejects(self):
        ledger = [{"lead_id": "OXY-20260922-TEST1", "verdict": "APPROVE", "phone": "+919840012345", "ts": "2026-09-22T09:30:00Z"}]
        self.assertEqual(self.verdict(ledger=ledger)["verdict"], "REJECT")

    def test_supplier_role_needs_review(self):
        v = self.verdict(lambda p: p["contact"].__setitem__("role", "supplier"))
        self.assertEqual(v["verdict"], "REVIEW")

    def test_vendor_words_need_review(self):
        v = self.verdict(lambda p: p["contact"].__setitem__("name", "Aqua Nano Enterprises"))
        self.assertEqual(v["verdict"], "REVIEW")
        self.assertTrue(any("nano" in t for t in self.reasons(v, "review")))

    def test_corporate_email_needs_review_but_free_mail_does_not(self):
        v = self.verdict(lambda p: p["contact"].__setitem__("email", "ops@somefirm.co.in"))
        self.assertEqual(v["verdict"], "REVIEW")
        v2 = self.verdict(lambda p: p["contact"].__setitem__("email", "farmer@gmail.com"))
        self.assertEqual(v2["verdict"], "APPROVE")

    def test_datasheet_overrides_need_review(self):
        v = self.verdict(lambda p: p["inputs"].__setitem__("o2_input_lpm_override", 20))
        self.assertEqual(v["verdict"], "REVIEW")

    def test_foreign_timezone_needs_review(self):
        v = self.verdict(lambda p: p["signals"].__setitem__("tz_min", 0))
        self.assertEqual(v["verdict"], "REVIEW")

    def test_same_phone_within_30_days_needs_review(self):
        ledger = [{"lead_id": "OXY-20260901-OLDER", "verdict": "APPROVE", "phone": "+919840012345", "ts": "2026-09-01T09:30:00Z"}]
        v = self.verdict(ledger=ledger)
        self.assertEqual(v["verdict"], "REVIEW")

    def test_record_writes_ledger_and_inbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            p = clean_payload()
            v = vet_lead.vet(p, [], PATTERNS)
            out = vet_lead.record(p, v, ledger_path=tmp / "ledger.jsonl", inbox_dir=tmp / "inbox")
            self.assertTrue(out.exists())
            rows = vet_lead.read_ledger(tmp / "ledger.jsonl")
            self.assertEqual(rows[0]["lead_id"], "OXY-20260922-TEST1")
            self.assertEqual(rows[0]["verdict"], "APPROVE")


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = oracle.load_oxy_data(ROOT / "site" / "data")

    def test_builds_a_full_report_for_a_clean_request(self):
        p = clean_payload()
        v = vet_lead.vet(p, [], PATTERNS)
        with tempfile.TemporaryDirectory() as tmp:
            out = make_report.build(p, v, pathlib.Path(tmp), data=self.data, built_at=dt.datetime(2026, 9, 22, 10, 0))
            html = out.read_text(encoding="utf-8")
            self.assertIn("Report for Farmer One", html)
            self.assertIn("Sirkazhi, Nagapattinam district", html)
            self.assertIn("Night-time oxygen budget", html)
            self.assertIn("Extra profit", html)
            self.assertGreaterEqual(html.count("<tr class=\"crop\">"), 1)
            self.assertTrue((pathlib.Path(tmp) / "OXY-20260922-TEST1.result.json").exists())

    def test_null_unit_count_means_auto_and_missing_tariff_is_resolved_from_its_preset(self):
        p = clean_payload()
        p["inputs"]["tariff_inr_kwh"] = None
        inputs = make_report.oracle_inputs(p, self.data)
        self.assertEqual(inputs["n_units"], "auto")
        self.assertIsInstance(inputs["tariff_inr_kwh"], float)

    def test_unknown_tariff_without_rate_fails_loudly(self):
        p = clean_payload()
        p["inputs"]["tariff_inr_kwh"] = None
        p["inputs"]["tariff_id"] = "no-such-preset"
        with self.assertRaises(make_report.ReportError):
            make_report.oracle_inputs(p, self.data)

    def test_cli_refuses_review_and_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            p = clean_payload()
            p["contact"]["role"] = "supplier"
            f = tmp / "lead.json"
            f.write_text(json.dumps(p), encoding="utf-8")
            self.assertEqual(make_report.main(["--file", str(f), "--out", str(tmp / "r"), "--ledger", str(tmp / "l.jsonl")]), 2)
            self.assertEqual(make_report.main(["--file", str(f), "--out", str(tmp / "r"), "--ledger", str(tmp / "l.jsonl"), "--force"]), 0)
            p2 = copy.deepcopy(clean_payload())
            p2["signals"]["t_ms"] = 500
            f.write_text(json.dumps(p2), encoding="utf-8")
            self.assertEqual(make_report.main(["--file", str(f), "--out", str(tmp / "r"), "--ledger", str(tmp / "l.jsonl"), "--force"]), 2)


if __name__ == "__main__":
    unittest.main()
