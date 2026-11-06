#!/usr/bin/env node
// Fingerprint a HyperFrames project and lint it for convergence on the generic look.
//
//   node tools/fingerprint.mjs films/001-x            # report + fail on house rules
//   node tools/fingerprint.mjs films/001-x --json
//   node tools/fingerprint.mjs films/001-x --record   # append to taste/ledger.json (after delivery)
//
// It reads index.html and compositions/*.html as text (static analysis; nothing is executed).
// A project can allow a rule on purpose with house.json:
//   { "look": "split-flap", "allow": { "banned_face": "brand font is Inter", "one_curve": "..." } }
import { readFileSync, readdirSync, existsSync, writeFileSync } from "node:fs";
import { join, dirname, basename, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const LEDGER = join(ROOT, "taste/ledger.json");

// Faces generated design lands on (HyperFrames look.md + what models reach for once those are banned).
export const BANNED_FACES = [
  "inter", "space grotesk", "instrument serif", "geist", "jetbrains mono", "anton", "bebas neue",
  "league gothic", "oswald", "archivo black", "poppins", "montserrat", "playfair display", "dm sans",
  "manrope", "outfit", "sora", "syne", "clash display", "satoshi", "general sans", "plus jakarta sans",
];
const GENERIC = new Set(["sans-serif", "serif", "monospace", "system-ui", "inherit", "initial", "cursive", "fantasy"]);

const { values: a, positionals } = parseArgs({
  allowPositionals: true,
  options: { json: { type: "boolean", default: false }, record: { type: "boolean", default: false } },
});
const dir = positionals[0];
if (!dir || !existsSync(join(dir, "index.html"))) {
  console.error("usage: fingerprint.mjs <project-dir> [--json] [--record]");
  process.exit(2);
}

const files = [join(dir, "index.html")];
if (existsSync(join(dir, "compositions")))
  for (const f of readdirSync(join(dir, "compositions"))) if (f.endsWith(".html")) files.push(join(dir, "compositions", f));
const src = files.map((f) => readFileSync(f, "utf8")).join("\n");
const house = existsSync(join(dir, "house.json")) ? JSON.parse(readFileSync(join(dir, "house.json"), "utf8")) : {};
const allow = house.allow || {};

// ---------- extract ----------
const fontDecls = [...src.matchAll(/font-family\s*:\s*([^;}{"]+(?:"[^"]*"[^;}{]*)*)[;}]/g)].map((m) => m[1]);
const fontFaces = [...src.matchAll(/@font-face\s*\{[^}]*font-family\s*:\s*["']?([^"';]+)/g)].map((m) => m[1].trim().toLowerCase());
const varDefs = Object.fromEntries([...src.matchAll(/(--[\w-]+)\s*:\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
const resolveVar = (v) => v.replace(/var\((--[\w-]+)[^)]*\)/g, (_, n) => varDefs[n] ?? "");
const faces = new Set(fontFaces);
for (const d of fontDecls)
  for (const part of resolveVar(d).split(","))
    {
      const f = part.trim().replace(/^["']|["']$/g, "").toLowerCase();
      if (f && !GENERIC.has(f) && !f.startsWith("var(")) faces.add(f);
    }
// JS-set fonts (canvas ctx.font = "700 40px Name")
for (const m of src.matchAll(/font\s*=\s*["'`][^"'`]*?\d+px\s+["']?([A-Za-z][\w ]+)/g)) faces.add(m[1].trim().toLowerCase());

const hexes = [...src.matchAll(/#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b/g)].map((m) => {
  let h = m[1].toLowerCase();
  if (h.length === 3) h = [...h].map((c) => c + c).join("");
  return h;
});
const counts = {};
for (const h of hexes) counts[h] = (counts[h] || 0) + 1;
const palette = Object.entries(counts).sort((x, y) => y[1] - x[1]).slice(0, 8).map(([h]) => "#" + h);

const eases = [...src.matchAll(/ease\s*:\s*["'`]([^"'`]+)["'`]/g)].map((m) => m[1].replace(/\s/g, ""));
const easeCounts = {};
for (const e of eases) easeCounts[e] = (easeCounts[e] || 0) + 1;
const tweenCount = (src.match(/\.(?:to|from|fromTo)\s*\(/g) || []).length;
// Linear and stepped motion are deliberate (mechanisms, constant speed, on twos): not counted as "one curve".
const isCurve = (e) => !/^(none|linear|steps\()/.test(e);
const curveEases = eases.filter(isCurve);
const [domEase, domN] = Object.entries(easeCounts).filter(([e]) => isCurve(e)).sort((x, y) => y[1] - x[1])[0] || ["none", 0];
const steps = /steps\(\s*\d+\s*\)|Math\.floor\([^)]*\*\s*12\s*\)\s*\/\s*12|onTwos|ON_TWOS/.test(src);

const blurIns = (src.match(/\{[^{}]*filter\s*:\s*["'`]blur\(\s*[\d.]+px\s*\)["'`][^{}]*\}\s*,\s*\{[^{}]*blur\(\s*0(?:px)?\s*\)/g) || []).length;
const staggerBlur = /stagger/.test(src) && blurIns > 0;
const glow = (src.match(/(?:text|box)-shadow\s*:[^;]*\b0\s+0\s+(?:[2-9]\d|\d{3,})px/g) || []).length + (src.match(/drop-shadow\(\s*0(?:px)?\s+0(?:px)?\s+(?:[2-9]\d|\d{3,})px/g) || []).length;
const gradientText = /background-clip\s*:\s*text/.test(src);
const motionBlurOn = /data-motion-blur\s*=\s*["']on["']/.test(src);
const centred = (src.match(/text-align\s*:\s*center|justify-content\s*:\s*center|align-items\s*:\s*center|translate\(-50%,\s*-50%\)/g) || []).length;

// shots: scene hosts in index.html, or elements marked data-shot
const index = readFileSync(join(dir, "index.html"), "utf8");
const durOf = (tag) => parseFloat((/data-duration\s*=\s*["']([\d.]+)/.exec(tag) || [])[1]);
let shots = [...index.matchAll(/<[^>]*data-composition-src[^>]*>/g)].map((m) => durOf(m[0])).filter((n) => n > 0);
const marked = [...src.matchAll(/<[^>]*\bdata-shot\b[^>]*>/g)].map((m) => durOf(m[0])).filter((n) => n > 0);
if (marked.length > shots.length) shots = marked;
const mean = shots.reduce((s, x) => s + x, 0) / (shots.length || 1);
const cv = shots.length ? Math.sqrt(shots.reduce((s, x) => s + (x - mean) ** 2, 0) / shots.length) / mean : null;
const rootDur = parseFloat((/data-composition-id\s*=\s*["']main["'][^>]*data-duration\s*=\s*["']([\d.]+)/.exec(index) || /id="root"[^>]*data-duration\s*=\s*["']([\d.]+)/.exec(index) || [])[1]);

const fp = {
  project: basename(resolve(dir)),
  look: house.look || (/LOOK-ID:\s*([\w-]+)/.exec(existsSync(join(dir, "SPEC.md")) ? readFileSync(join(dir, "SPEC.md"), "utf8") : "") || [])[1] || null,
  date: new Date().toISOString().slice(0, 10),
  duration: rootDur || null,
  faces: [...faces].sort(),
  palette,
  eases: easeCounts,
  dominantEase: domEase,
  dominantEaseShare: curveEases.length ? +(domN / curveEases.length).toFixed(2) : 0,
  tweens: tweenCount,
  onTwos: steps,
  blurIns,
  glow,
  gradientText,
  motionBlurOn,
  centred,
  shots,
  shotCV: cv === null ? null : +cv.toFixed(2),
};

// ---------- rules ----------
const findings = [];
const add = (level, code, msg) => findings.push({ level: allow[code] ? "allowed" : level, code, msg: allow[code] ? `${msg} (allowed: ${allow[code]})` : msg });

for (const f of fp.faces) if (BANNED_FACES.includes(f)) add("fail", "banned_face", `"${f}" is where generated design lands. Take the face from the look file or the brand.`);
if (fp.faces.length === 0) add("fail", "no_face", "No font family set: the browser default is the most generic face there is.");
if (curveEases.length >= 6 && fp.dominantEaseShare > 0.6) add("fail", "one_curve", `${Math.round(fp.dominantEaseShare * 100)}% of tweens use ${domEase}. Ease by role and by medium.`);
if (shots.length >= 4 && cv < 0.25) add("fail", "metronome", `Shot lengths ${shots.join(" · ")} have CV ${fp.shotCV} (< 0.25). Plan a long–short–short–long shape.`);
else if (shots.length >= 4 && cv < 0.35) add("warn", "metronome", `Shot-length CV ${fp.shotCV} (< 0.35 target).`);
if (shots.length < 3 && (rootDur || 0) > 12) add("warn", "no_shots", "Over 12 s with fewer than 3 scene hosts or data-shot markers: mark shots so rhythm can be measured.");
if (blurIns >= 3) add("warn", "hf_signature", `${blurIns} blur-to-sharp entrances${staggerBlur ? " with stagger" : ""}: HyperFrames' house entrance. Use the medium's way of making marks.`);
if (glow > 0) add("warn", "glow", `${glow} glow-style shadows (0 0 ≥20px).`);
if (gradientText) add("fail", "gradient_text", "background-clip: text gradient type.");
if (motionBlurOn) add("warn", "motion_blur", "data-motion-blur on: only when the medium moves fast enough to blur.");
if (centred >= 6) add("warn", "centred", `${centred} centring rules: is every frame a centred slide?`);

// similarity with recent films
const ledger = existsSync(LEDGER) ? JSON.parse(readFileSync(LEDGER, "utf8")) : { films: [] };
const hexToRgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const near = (p, q) => {
  const [x, y] = [hexToRgb(p), hexToRgb(q)];
  return Math.hypot(x[0] - y[0], x[1] - y[1], x[2] - y[2]) < 36;
};
function similarity(f, g) {
  const jac = (A, B) => { const s = new Set([...A, ...B]); return s.size ? [...A].filter((x) => B.includes(x)).length / s.size : 0; };
  const pal = f.palette.length ? f.palette.slice(0, 5).filter((p) => g.palette.slice(0, 5).some((q) => near(p, q))).length / Math.min(5, f.palette.length) : 0;
  return +(0.35 * jac(f.faces, g.faces) + 0.35 * pal + 0.15 * (f.dominantEase === g.dominantEase ? 1 : 0) + 0.15 * (f.look && f.look === g.look ? 1 : 0)).toFixed(2);
}
const others = ledger.films.filter((g) => g.project !== fp.project).slice(-5);
fp.similar = others.map((g) => ({ project: g.project, look: g.look, score: similarity(fp, g) })).sort((x, y) => y.score - x.score);
if (fp.similar[0]?.score >= 0.6) add("fail", "too_close", `${Math.round(fp.similar[0].score * 100)}% like ${fp.similar[0].project}: change the face, the palette or the motion language.`);
else if (fp.similar[0]?.score >= 0.45) add("warn", "too_close", `${Math.round(fp.similar[0].score * 100)}% like ${fp.similar[0].project}.`);

// ---------- output ----------
const fails = findings.filter((f) => f.level === "fail");
if (a.record) {
  if (fails.length) {
    console.error(`Not recording: ${fails.length} failing rule(s). Fix or allow them in house.json first.`);
    process.exitCode = 1;
  } else {
    ledger.films = ledger.films.filter((g) => g.project !== fp.project);
    const { similar, ...entry } = fp;
    ledger.films.push(entry);
    writeFileSync(LEDGER, JSON.stringify(ledger, null, 2) + "\n");
  }
}
if (a.json) console.log(JSON.stringify({ fingerprint: fp, findings }, null, 2));
else {
  console.log(`${fp.project}  look=${fp.look ?? "?"}  ${fp.duration ?? "?"}s`);
  console.log(`faces     ${fp.faces.join(", ") || "—"}`);
  console.log(`palette   ${fp.palette.join(" ")}`);
  console.log(`eases     ${Object.entries(easeCounts).map(([e, n]) => `${e}×${n}`).join("  ") || "—"}${steps ? "   (on twos/stepped)" : ""}`);
  console.log(`shots     ${shots.join(" · ") || "—"}${shots.length > 1 ? `   CV ${fp.shotCV}` : ""}`);
  if (fp.similar.length) console.log(`closest   ${fp.similar[0].project} ${Math.round(fp.similar[0].score * 100)}%`);
  console.log("");
  for (const f of findings) console.log(`${f.level.toUpperCase().padEnd(7)} ${f.code.padEnd(14)} ${f.msg}`);
  if (!findings.length) console.log("clean");
  if (a.record && !fails.length) console.log(`\nrecorded in taste/ledger.json`);
}
if (fails.length) process.exitCode = 1;
