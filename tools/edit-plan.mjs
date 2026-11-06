#!/usr/bin/env node
// Turn a word-timed transcript into an editor's first-pass plan for talking-head footage:
// what to cut (fillers, stutters, dead air), how much air to leave, and where the framing
// should change to hide a jump cut. It only PROPOSES; read the plan, then compile it with
// HyperFrames' transcript-cut:
//
//   npx hyperframes transcribe talk.mp4 --model small.en --json        # -> assets/transcript.json
//   node tools/edit-plan.mjs assets/transcript.json --style social > edit-plan.json
//   node .claude/skills/media-use/scripts/transcript-cut.mjs --input talk.mp4 \
//        --transcript assets/transcript.json --remove "$(node -e 'console.log(require("./edit-plan.json").remove)')" --out talk.cut.mp4
//
// Transcript: [{text,start,end}] or {words:[...]}.
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";

const { values: a, positionals } = parseArgs({
  allowPositionals: true,
  options: {
    style: { type: "string", default: "social" }, // social | conversational | calm
    "keep-fillers": { type: "boolean", default: false },
  },
});
if (!positionals[0]) {
  console.error("usage: edit-plan.mjs transcript.json [--style social|conversational|calm]");
  process.exit(2);
}
const raw = JSON.parse(readFileSync(positionals[0], "utf8"));
const words = (Array.isArray(raw) ? raw : raw.words || raw.segments?.flatMap((s) => s.words) || [])
  .map((w, i) => ({ i, text: String(w.text ?? w.word).trim(), start: +w.start, end: +w.end }))
  .filter((w) => w.text && !/^[♪�\[\(]/.test(w.text));

// Air left at a trimmed pause. Zero air is the jump-cut-everything tell: breath is rhythm.
const STYLE = {
  social: { maxPause: 0.35, keep: 0.14, keepSentence: 0.24, keepQuestion: 0.42 },
  conversational: { maxPause: 0.55, keep: 0.22, keepSentence: 0.34, keepQuestion: 0.55 },
  calm: { maxPause: 0.9, keep: 0.35, keepSentence: 0.55, keepQuestion: 0.8 },
}[a.style];
if (!STYLE) throw new Error(`unknown style ${a.style}`);

const norm = (t) => t.toLowerCase().replace(/[^a-z']/g, "");
const FILLERS = new Set(["um", "uh", "erm", "er", "ah", "uhm", "mm", "hmm", "umm", "uhh"]);
const SOFT = new Set(["like", "basically", "literally", "actually", "so", "right", "okay"]);

const remove = []; // [start, end, reason]
const cand = []; // suggestions only
const gapBefore = (k) => (k > 0 ? words[k].start - words[k - 1].end : 0);
const gapAfter = (k) => (k < words.length - 1 ? words[k + 1].start - words[k].end : 0);

for (let k = 0; k < words.length; k++) {
  const w = words[k];
  const n = norm(w.text);
  if (!a["keep-fillers"] && FILLERS.has(n)) remove.push([w.start, w.end, `filler "${w.text}"`]);
  else if (k > 0 && n && n === norm(words[k - 1].text) && gapBefore(k) < 0.4 && !["that", "had", "very", "no"].includes(n))
    remove.push([words[k - 1].start, w.start, `stutter "${words[k - 1].text} ${w.text}"`]);
  else if (n === "you" && norm(words[k + 1]?.text || "") === "know" && (gapBefore(k) > 0.12 || gapAfter(k + 1) > 0.12))
    cand.push({ at: +w.start.toFixed(2), words: "you know", why: "verbal tic between pauses: cut if it isn't doing work" });
  else if (SOFT.has(n) && gapBefore(k) > 0.15 && gapAfter(k) > 0.15)
    cand.push({ at: +w.start.toFixed(2), words: w.text, why: "isolated by pauses: probably a filler here" });
}

// Dead air: trim each long gap down to STYLE air, more after a sentence, most after a question.
for (let k = 1; k < words.length; k++) {
  const gap = gapBefore(k);
  if (gap <= STYLE.maxPause) continue;
  const prev = words[k - 1].text;
  const keep = /\?$/.test(prev) ? STYLE.keepQuestion : /[.!]$/.test(prev) ? STYLE.keepSentence : STYLE.keep;
  // Keep 45% of the air after the last word (its release tail) and 55% before the next (the breath in).
  const s = words[k - 1].end + keep * 0.45;
  const e = words[k].start - keep * 0.55;
  if (e - s > 0.05) remove.push([s, e, `pause ${gap.toFixed(2)}s → ${keep}s`]);
}
// Leading/trailing silence
if (words.length && words[0].start > 0.3) remove.push([0, words[0].start - 0.12, "head silence"]);

remove.sort((x, y) => x[0] - y[0]);
const merged = [];
for (const r of remove) {
  const last = merged[merged.length - 1];
  if (last && r[0] <= last[1] + 0.02) (last[1] = Math.max(last[1], r[1])), (last[2] += `; ${r[2]}`);
  else merged.push([...r]);
}

// Framing plan: each jump cut inside a sentence changes the framing so it reads as an edit, not a glitch.
// Two framings (wide 1.00 / tight 1.18) alternate; a new idea (cut after a sentence end) returns to wide;
// a run of 3+ cuts inside 4 s gets ONE extreme close (1.35) on the cut nearest the strongest word (longest word).
const total = words.length ? words[words.length - 1].end : 0;
const framing = [];
let tight = false;
for (const [s, e] of merged) {
  if (s === 0) continue;
  const prevWord = [...words].reverse().find((w) => w.end <= s + 0.01);
  const newIdea = prevWord && /[.!?]$/.test(prevWord.text);
  tight = newIdea ? false : !tight;
  framing.push({ cutAt: +s.toFixed(2), scale: tight ? 1.18 : 1.0, why: newIdea ? "new idea: back to wide" : "hide jump cut" });
}
for (let k = 0; k + 2 < framing.length; k++) {
  if (framing[k + 2].cutAt - framing[k].cutAt < 4 && !framing.slice(k, k + 3).some((f) => f.scale === 1.35)) {
    const pick = framing.slice(k, k + 3).filter((f) => !f.why.startsWith("new idea")).reduce((best, f) => {
      const next = words.find((w) => w.start >= f.cutAt);
      return (next?.text.length || 0) > (best.len || 0) ? { f, len: next.text.length } : best;
    }, {});
    if (pick.f) (pick.f.scale = 1.35), (pick.f.why = "emphasis close in a fast run");
    k += 2;
  }
}

const removed = merged.reduce((s, [x, y]) => s + (y - x), 0);
const spoken = words.filter((w) => !FILLERS.has(norm(w.text))).length;
const plan = {
  style: a.style,
  remove: merged.map(([s, e]) => `${s.toFixed(2)}-${e.toFixed(2)}`).join(","),
  cuts: merged.map(([s, e, why]) => ({ start: +s.toFixed(2), end: +e.toFixed(2), why })),
  candidates: cand,
  framing,
  stats: {
    before_s: +total.toFixed(2),
    after_s: +(total - removed).toFixed(2),
    removed_s: +removed.toFixed(2),
    wpm_before: total ? Math.round((words.length / total) * 60) : 0,
    wpm_after: total - removed > 0 ? Math.round((spoken / (total - removed)) * 60) : 0,
    note: "Social talking heads read well at 160–190 wpm after the cut; over 200 feels breathless: raise --style.",
  },
};
console.log(JSON.stringify(plan, null, 2));
