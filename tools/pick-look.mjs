#!/usr/bin/env node
// Propose looks for a brief, pushing down looks used in recent films.
//   node tools/pick-look.mjs --brief "pricing change for a coffee subscription" [--json]
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const LOOKS = join(ROOT, ".claude/skills/house/looks");
const LEDGER = join(ROOT, "taste/ledger.json");

const { values: a } = parseArgs({ options: { brief: { type: "string" }, json: { type: "boolean", default: false } } });
if (!a.brief) {
  console.error('usage: pick-look.mjs --brief "<one line>"');
  process.exit(2);
}

export function parseFrontmatter(text) {
  const m = /^---\n([\s\S]*?)\n---/.exec(text);
  if (!m) return null;
  const out = {};
  for (const line of m[1].split("\n")) {
    const kv = /^(\w+):\s*(.*)$/.exec(line);
    if (!kv) continue;
    let v = kv[2].trim();
    if (v.startsWith("[")) v = JSON.parse(v.replace(/([\w-]+)(?=\s*[,\]])/g, (w) => (/^".*"$/.test(w) ? w : `"${w}"`)).replace(/""/g, '"'));
    out[kv[1]] = v;
  }
  return out;
}

const stem = (w) => w.toLowerCase().replace(/[^a-z0-9-]/g, "").replace(/(ing|es|s)$/, "");
const words = new Set(a.brief.split(/\s+/).map(stem).filter(Boolean));
const ENERGY = { high: ["loud", "hype", "bold", "energetic", "fast", "punchy", "fun", "viral"], low: ["calm", "quiet", "slow", "thoughtful", "premium", "serious", "gentle"] };

// Client films follow their preset's look, so only general films push a look down.
const recent = existsSync(LEDGER) ? JSON.parse(readFileSync(LEDGER, "utf8")).films.filter((f) => !f.client).slice(-3).map((f) => f.look) : [];

const looks = readdirSync(LOOKS)
  .filter((f) => f.endsWith(".md") && f !== "README.md")
  .map((f) => parseFrontmatter(readFileSync(join(LOOKS, f), "utf8")))
  .filter(Boolean);

const scored = looks.map((l) => {
  const why = [];
  let score = 0;
  for (const t of l.suits) if (words.has(stem(t))) (score += 2), why.push(`+2 ${t}`);
  for (const t of l.avoid) if (words.has(stem(t))) (score -= 3), why.push(`-3 avoid:${t}`);
  for (const [lvl, hints] of Object.entries(ENERGY))
    for (const h of hints) if (words.has(stem(h))) (score += l.energy === lvl ? 1 : l.energy === "mid" ? 0 : -1), why.push(`energy:${h}`);
  const idx = recent.lastIndexOf(l.id);
  if (idx !== -1) {
    const pen = 4 - (recent.length - 1 - idx);
    score -= pen;
    why.push(`-${pen} used recently`);
  }
  return { id: l.id, medium: l.medium, energy: l.energy, faces: l.faces, score, why };
});
scored.sort((x, y) => y.score - x.score);

if (a.json) console.log(JSON.stringify(scored, null, 2));
else {
  console.log(`brief: ${a.brief}\nrecent looks: ${recent.join(", ") || "none"}\n`);
  for (const s of scored.slice(0, 3)) console.log(`${String(s.score).padStart(3)}  ${s.id.padEnd(16)} ${s.medium}\n     ${s.why.join(", ") || "no tag match"}`);
  if (scored[0].score <= 0)
    console.log("\nNo look fits this brief well. Write a new medium in .claude/skills/house/looks/ (see README.md) from the subject's own world.");
  else console.log("\nThe top score is a proposal. Choose from the subject, then say why in SPEC.md.");
}
