/*
 * tests/smoke_leads.mjs — browser smoke test of the report gate and the lead form.
 * Drives headless Chrome/Edge over the DevTools Protocol with Node 22's built-in WebSocket;
 * no npm packages. Needs the site served over HTTP:
 *
 *     cd site && python -m http.server 8765
 *     node tests/smoke_leads.mjs [http://127.0.0.1:8765/index.html]
 *
 * Checks (plan/LEAD_CAPTURE.md gate contract):
 *   1. the harvest band shows kilograms; profit, payback and units show the locked label
 *      and contain no rupee figure; the three chart containers are empty with the lock note.
 *   2. no uncaught exception or console.error while loading and interacting.
 *   3. "Get my pond report" opens the dialog; a valid form submitted after the minimum time
 *      reaches the received state with a WhatsApp link that carries an OXY1. code and no
 *      profit figure.
 *   4. the owner preview flag unlocks the page (so the charts still work).
 * Writes tests/screenshots/lead_gate_1280x1000.png and lead_form_390x844.png.
 */

import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const URL_ = process.argv[2] || "http://127.0.0.1:8765/index.html";
const PORT = 9333;
const BROWSERS = [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
];

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

const browser = BROWSERS.find((b) => fs.existsSync(b));
if (!browser) { console.error("no Chrome/Edge found"); process.exit(3); }
const profile = fs.mkdtempSync(path.join(os.tmpdir(), "oxy-smoke-"));
const proc = spawn(browser, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--window-size=1280,1000", "about:blank",
], { stdio: "ignore" });

let ws, nextId = 1;
const pending = new Map();
const events = [];
function send(method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}
async function evaluate(expression) {
  const r = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) throw new Error("evaluate failed: " + JSON.stringify(r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
}
async function screenshot(file, width, height, mobile) {
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile });
  await sleep(400);
  const shot = await send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync(file, Buffer.from(shot.data, "base64"));
}

const failures = [];
function check(cond, msg) { if (cond) console.log("  ok   " + msg); else { console.log("  FAIL " + msg); failures.push(msg); } }

try {
  let targets = null;
  for (let i = 0; i < 50 && !targets; i++) {
    try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); } catch { await sleep(200); }
  }
  const page = targets.find((t) => t.type === "page");
  ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r));
  ws.addEventListener("message", (m) => {
    const msg = JSON.parse(m.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id).resolve(msg.result || msg); pending.delete(msg.id); }
    else if (msg.method) events.push(msg);
  });
  await send("Runtime.enable");
  await send("Page.enable");
  await send("Log.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 1000, deviceScaleFactor: 1, mobile: false });
  await send("Page.navigate", { url: URL_ });
  await sleep(2500);

  console.log("1. gate");
  const gate = await evaluate(`(() => {
    const t = (id) => (document.getElementById(id) || {}).textContent || "";
    return {
      harvest: t("res-harvest"), profit: t("res-profit"), payback: t("res-payback"), units: t("res-units"),
      season: document.getElementById("season-strip").children.length,
      waterfall: document.getElementById("waterfall").children.length,
      seasonNote: !document.getElementById("season-locked").classList.contains("hidden"),
      compare: t("station-compare-tbody"),
      cta: t("cta-report"),
      resultsCardHasRupeeOutsideBaseline: (() => {
        const card = document.getElementById("result-content").cloneNode(true);
        card.querySelector("#res-baseline")?.remove();
        return card.textContent.includes("₹");
      })()
    };
  })()`);
  check(/kg/.test(gate.harvest), "harvest band shows kilograms: " + gate.harvest.slice(0, 60));
  check(gate.profit === "In your pond report", "profit band locked: " + gate.profit);
  check(gate.payback === "In your pond report", "payback band locked");
  check(gate.units === "In your pond report", "units band locked");
  check(gate.season === 0 && gate.waterfall === 0 && gate.seasonNote, "charts empty with lock note");
  check(gate.compare.includes("Included in your pond report"), "station comparison locked");
  check(!gate.resultsCardHasRupeeOutsideBaseline, "no rupee figure in the results card outside the baseline line");
  check(gate.cta === "Get my pond report", "CTA reads 'Get my pond report'");

  // interact with a slider so the interaction counter and re-render are exercised
  await evaluate(`(() => { const s = document.getElementById("in-area_acre"); s.value = "2"; s.dispatchEvent(new Event("input", { bubbles: true })); return true; })()`);
  await sleep(600);
  const after = await evaluate(`document.getElementById("res-profit").textContent`);
  check(after === "In your pond report", "profit stays locked after re-evaluation");
  const warnText = await evaluate(`document.getElementById("res-warnings").textContent`);
  check(!/cover the electricity|oxygen-limited|capped/i.test(warnText), "economic/sizing warnings withheld while locked: " + JSON.stringify(warnText.slice(0, 80)));
  await evaluate(`document.getElementById("results-card").scrollIntoView({ block: "start" }); true`);
  await screenshot(path.join(HERE, "screenshots", "lead_gate_1280x1000.png"), 1280, 1000, false);

  console.log("2. form");
  await evaluate(`document.getElementById("cta-report").click(); true`);
  await sleep(300);
  const opened = await evaluate(`document.getElementById("lead-dialog").open === true && document.getElementById("lead-district").value`);
  check(!!opened, "dialog opens with the district prefilled: " + opened);
  await screenshot(path.join(HERE, "screenshots", "lead_form_390x844.png"), 390, 844, true);
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 1000, deviceScaleFactor: 1, mobile: false });

  // submit too early: must be refused on timing (page loaded < 4 s ago? we have waited ~4 s, so force via empty consent first)
  const earlyErr = await evaluate(`(() => {
    const v = (id, val) => { document.getElementById(id).value = val; };
    v("lead-name", "Farmer One"); v("lead-phone", "98400 12345"); v("lead-village", "Lalgudi");
    v("lead-role", "owner"); v("lead-ponds", "2-5"); v("lead-area-total", "3");
    const q = document.getElementById("lead-challenge-q").textContent.match(/(\\d+) \\+ (\\d+)/);
    v("lead-challenge", String(Number(q[1]) + Number(q[2])));
    document.getElementById("lead-consent").checked = false;
    document.getElementById("lead-form").requestSubmit();
    return document.getElementById("lead-form-error").textContent;
  })()`);
  check(/tick the box/.test(earlyErr), "missing consent is refused: " + earlyErr);

  await sleep(4500);
  await evaluate(`(() => { document.getElementById("lead-consent").checked = true; document.getElementById("lead-form").requestSubmit(); return true; })()`);
  await sleep(800);
  const received = await evaluate(`(() => ({
    shown: !document.getElementById("lead-received").classList.contains("hidden"),
    ref: document.getElementById("lead-received-ref").textContent,
    href: document.getElementById("lead-cta-whatsapp").href,
    stored: localStorage.getItem("oxy_lead_request") ? JSON.parse(localStorage.getItem("oxy_lead_request")).lead_id : null,
    cta: document.getElementById("cta-report").textContent,
    profit: document.getElementById("res-profit").textContent
  }))()`);
  check(received.shown, "received state shown");
  check(/^OXY-\d{8}-[A-Z2-9]{5}$/.test(received.ref), "lead id format: " + received.ref);
  check(received.href.startsWith("https://wa.me/919659727477?text=") && decodeURIComponent(received.href).includes("Ref: OXY1."), "WhatsApp link carries the reference code");
  check(!/₹|profit/i.test(decodeURIComponent(received.href)), "WhatsApp text carries no profit figure");
  check(received.stored === received.ref, "received state persisted in localStorage");
  check(received.cta.startsWith("Request received"), "results CTA now reads 'Request received…'");
  check(received.profit === "In your pond report", "profit stays locked after the request (report comes after vetting)");

  console.log("3. owner preview");
  await evaluate(`localStorage.setItem("oxy_owner", "1"); true`);
  await send("Page.reload");
  await sleep(2500);
  const unlocked = await evaluate(`(() => ({
    profit: document.getElementById("res-profit").textContent,
    season: document.getElementById("season-strip").children.length,
    compareRows: document.querySelectorAll("#station-compare-tbody tr").length
  }))()`);
  check(/₹/.test(unlocked.profit), "owner preview shows profit: " + unlocked.profit.slice(0, 50));
  check(unlocked.season > 0 && unlocked.compareRows > 5, "owner preview renders charts and the station table");
  await evaluate(`localStorage.removeItem("oxy_owner"); localStorage.removeItem("oxy_lead_request"); true`);

  console.log("4. console");
  const errors = events.filter((e) =>
    e.method === "Runtime.exceptionThrown" ||
    (e.method === "Runtime.consoleAPICalled" && e.params.type === "error") ||
    (e.method === "Log.entryAdded" && e.params.entry.level === "error" && !/tile|openstreetmap|arcgis|favicon/i.test(e.params.entry.text || e.params.entry.url || ""))
  );
  check(errors.length === 0, "no uncaught exceptions or console errors (" + errors.length + ")");
  for (const e of errors) console.log("     ", JSON.stringify(e.params).slice(0, 300));
} catch (err) {
  console.error("smoke test crashed:", err);
  failures.push(String(err));
} finally {
  try { ws && ws.close(); } catch {}
  proc.kill();
  await sleep(300);
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
}
console.log(failures.length ? `\nFAILED ${failures.length}` : "\nPASS");
process.exit(failures.length ? 1 : 0);
