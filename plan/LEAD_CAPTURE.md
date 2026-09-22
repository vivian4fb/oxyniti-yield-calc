# Lead capture and the report gate

*Written 2026-09-22. Status: VERIFIED 2026-09-22 (tests below). Owner: Vivian.*

## Decision

The calculator is a client attractor. Its job is to produce a sales lead that already carries
the farmer's pond capacity and economics, and to hand out the full estimate **only** to a
person who has given a working contact and passed vetting.

| Rule | Implementation | Status |
|---|---|---|
| The farmer sees enough to want more | The extra-harvest band updates live with every slider (`res-harvest`) | VERIFIED 2026-09-22 |
| Nothing else leaves the model into the page | Profit, payback, investment, unit sizing, seasonal strip, station comparison and waterfall are replaced by "In your pond report"; `ui.js` never writes them to the DOM while `OxyLeads.isLocked()`. The four economic/sizing warning codes (no payback, not oxygen-limited, ceiling clamped, sizing capped) are withheld too; input-side warnings stay so the farmer can fix inputs before asking | VERIFIED 2026-09-22 (`tests/smoke_leads.mjs`: no rupee figure in the results card outside the baseline line; economic warnings absent) |
| No contact, no report | The only call to action is "Get my pond report", which opens the request form; the form needs name, valid Indian mobile, village, role, pond count and consent | VERIFIED 2026-09-22 |
| Report only after vetting | The page never unlocks for the farmer, even after a request. The owner runs `tools/leads/vet_lead.py`, then `make_report.py`, then sends the PDF on WhatsApp | VERIFIED 2026-09-22 (`tests/test_vet_lead.py`) |
| Bots are filtered | Honeypot field; minimum 4 s on page; arithmetic check; interaction count, timezone, referrer and user agent recorded; optional Turnstile | VERIFIED 2026-09-22 (client checks); vet rules in `vet_lead.py` |
| Competitors are flagged | Self-declared role, vendor words, corporate e-mail domain, datasheet overrides, manual unit counts, non-Indian timezone, duplicate phone → REVIEW; a person decides | VERIFIED 2026-09-22 (`test_vet_lead.py`, 12 verdict tests) |
| Personal data stays out of the public repo | `tools/leads/inbox/`, `reports/`, `ledger.jsonl` git-ignored | VERIFIED 2026-09-22 |

## What the lead carries

Contact: name, WhatsApp number (normalised to +91), village, district (from the map), role,
number of ponds, total water area (optional), e-mail (optional), best time to call (optional).

Pond: every calculator input (25 fields) exactly as the model received them, so the report
reproduces what the farmer was looking at.

Signals: page language, milliseconds on page, calculator interactions, timezone offset,
referrer host; on the endpoint route also user agent, viewport and pointer type.

Model output: **none** in the WhatsApp message or the reference code (the farmer could read
it in the compose box). The endpoint POST carries a headline summary for triage by e-mail.

## Routes out of a static page

The site is GitHub Pages: no server. Two routes, both wired (`site/js/leads.config.js`):

1. **WhatsApp deep link** to +91 96597 27477 with a human-readable summary and a
   `OXY1.<base64url>` reference code (`REF_FIELDS`, 41 positions, identical in
   `site/js/leads.js` and `tools/leads/vet_lead.py`). Works today, needs nothing. Because the
   farmer sends it from their own phone, the number is proved by the act of sending.
2. **JSON POST** to `endpoint` when set (Web3Forms, Formspree, a Worker). Empty at launch:
   creating a key needs the owner's inbox (`tools/leads/README.md`, 5 minutes). Until then
   the received screen tells the farmer the WhatsApp step is required, so no lead is dropped
   silently.

## What this cannot do

The model is public (`site/js/model.js`, `MODEL_SPEC.md`) and runs in the browser. A
competitor who reads source gets the model; the gate stops them getting a personalised
report or a lead-shaped contact with Oxyniti, and the vetting stops the report being sent to
them. Keeping the model itself private means moving it server-side and making the repository
private, an owner decision for EXECUTION_PLAN.md section 7.

Tamil: the form ships in English only. The i18n header rule stands: no machine-translated
copy in production without native review. The `ta` mode falls back to English for `lead.*`.

## Tests and evidence (2026-09-22)

- `node --test tests/*.test.mjs` 57/57 (43 model + 14 lead helpers).
- `python -m unittest tests/test_vet_lead.py` 21/21, including a report built end to end by
  the independent oracle for a clean request, and refusal of REJECT/REVIEW requests.
- `node tests/smoke_leads.mjs` PASS: 22 checks in headless Chrome over CDP; console clean.
  Screenshots `tests/screenshots/lead_gate_1280x1000.png`, `lead_form_390x844.png`.
- `python tests/compare.py` unchanged (the model was not touched).
