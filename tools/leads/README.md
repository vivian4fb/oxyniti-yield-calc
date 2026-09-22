# Lead vetting and report building — owner's runbook

*Written 2026-09-22. Status: VERIFIED 2026-09-22 against `tests/test_vet_lead.py` (21 tests).*

The calculator page shows a farmer the extra-harvest band only. Extra profit, payback, unit
sizing, the month-by-month oxygen budget and the charts are **never written to the page**. The
farmer asks for them as a report, and the report goes out only after a person has vetted the
request with the tools here. Design and rationale: `plan/LEAD_CAPTURE.md`.

## How a request reaches you

| Route | When | What you receive |
|---|---|---|
| WhatsApp to +91 96597 27477 | Always (the only route until an endpoint is configured) | A message: name, village, district, role, ponds, pond facts, and a `Ref: OXY1.…` code |
| JSON POST to `OXY_LEADS_CONFIG.endpoint` | After you set `endpoint` in `site/js/leads.config.js` | The same fields flat, plus `inputs_json`, `headline_json`, `signals_json`, `ref` |

The `OXY1.` code is base64url JSON of the request's contact fields, calculator inputs and bot
signals, in the order `REF_FIELDS` in `site/js/leads.js` and `vet_lead.py`. It carries **no
model output**, so nothing in the WhatsApp message tells the farmer more than the page did.

## Step 1 — vet

```sh
# paste the code straight from WhatsApp
python tools/leads/vet_lead.py --ref OXY1.eyJ...  --record
# or save the whole message to a file
python tools/leads/vet_lead.py --text message.txt --record
# or the JSON an endpoint relayed
python tools/leads/vet_lead.py --file lead.json --record
```

Output is the decoded request, every signal found, and a verdict. Exit code 0 APPROVE,
1 REVIEW, 2 REJECT, 3 unreadable.

| Verdict | Fires on | What to do |
|---|---|---|
| REJECT | honeypot filled; form sent under 4 s after page load; invalid Indian mobile; name without letters; automated user agent; same `lead_id` already in the ledger | Nothing. Do not reply. |
| REVIEW | role supplier/consultant; vendor words in name, village, e-mail or referrer (`competitor_signals.txt`); corporate e-mail domain; datasheet overrides or a manual unit count (probing the model); no slider touched and under 20 s on page; browser timezone not India; >100 acres with a non-farm role; 20+ ponds while "planning a new pond"; same phone within 30 days | Read the reasons. Call the number if unsure. Then `make_report.py --force` or drop it. |
| APPROVE | none of the above | Build and send. |

`--record` appends one line to `ledger.jsonl` and saves the full request to `inbox/<lead_id>.json`.
Both are **git-ignored** (`.gitignore`): they hold personal data and the repository is public.

Add real competitor names or domains to `competitor_signals.txt` as you meet them, one per
line. The shipped list is generic patterns only, deliberately: an invented company name would
be a fabrication.

## Step 2 — build the report

```sh
python tools/leads/make_report.py --ref OXY1.eyJ... --pdf
```

Runs the independent oracle (`tests/oracle.py`, the same model as the page, proved equal by
`tests/compare.py`) on the farmer's inputs and writes `reports/<lead_id>.html` (+ `.pdf` with
Edge or Chrome headless, + `.result.json`). The report holds: the pond as described, the four
headline bands, the profit build-up, the twelve-month oxygen budget, warnings, and every
assumption with its status and date. The footer's last line is an internal vetting note.
Remove it if you print the HTML yourself; the PDF route keeps it, so re-print without it or
crop it before sending.

The tool refuses REJECT outright and REVIEW unless `--force`.

## Step 3 — send

Send the PDF on WhatsApp to the number in the request, from the Oxyniti number. Then arrange
the free DO-meter demo. Nothing here sends automatically, by design.

## Setting up the endpoint (5 minutes, optional)

WhatsApp works today with nothing configured. To also receive requests by e-mail (needed for
the Instagram-ad and website-embed funnels, where a farmer may not finish the WhatsApp step):

1. Create a free Web3Forms access key at web3forms.com with the Oxyniti inbox address. The
   key arrives by e-mail. It is a public key: it only lets a page send mail *to you*.
2. In `site/js/leads.config.js` set `endpoint: "https://api.web3forms.com/submit"` and
   `extraFields: { access_key: "<the key>" }`.
3. `powershell -File deploy.ps1 -Message "leads: enable e-mail endpoint"`.

Each request then arrives as an e-mail with the `ref` field; vet it exactly as above. Any
other JSON-accepting endpoint (Formspree, a Cloudflare Worker) works the same way.

Optional bot wall: set `turnstileSiteKey` to a Cloudflare Turnstile site key and the widget
loads in the form. Without a server to verify the token it is only a hurdle, so the page
still runs the honeypot, timing and arithmetic checks with or without it.

## Previewing the unlocked page

In the browser console on the calculator page:

```js
localStorage.setItem("oxy_owner", "1"); location.reload();
```

`localStorage.removeItem("oxy_owner")` restores the gate. This is a preview convenience for
the owner, not a secret: the model itself is public in `site/js/model.js`.

## What this does and does not protect

- **Protects:** the personalised report and the profit/payback numbers from anyone who does
  not give a working Indian mobile number and pass vetting. Bots and casual competitors get
  the harvest band and nothing else.
- **Does not protect:** the model. The repository is public and the model runs in the
  browser, so a determined competitor can read `site/js/model.js` and `plan/MODEL_SPEC.md`.
  Preventing that means moving the model behind a server and making the repository private.
  That is an owner decision (EXECUTION_PLAN.md section 7), not something the gate can do.
