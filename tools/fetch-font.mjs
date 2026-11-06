#!/usr/bin/env node
// Download a Google Fonts family (latin subset, woff2) into a HyperFrames project
// and print the @font-face rules to paste into the composition.
//
//   node tools/fetch-font.mjs --project films/002-x --family "Courier Prime" --weights 400,700 [--italic]
//   node tools/fetch-font.mjs --check --family "Fragment Mono" --weights 400   (only verify it exists)
//
// HyperFrames only resolves its bundled fonts by name; anything else must ship as a file
// (contract rule 9). Every house look uses non-bundled faces on purpose, so this is step one.
import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { parseArgs } from "node:util";

const { values: a } = parseArgs({
  options: {
    project: { type: "string" },
    family: { type: "string" },
    weights: { type: "string", default: "400" },
    italic: { type: "boolean", default: false },
    check: { type: "boolean", default: false },
    axes: { type: "string" }, // raw css2 axis spec, e.g. "wdth,wght@50..150,100..900" for a variable face
  },
});
if (!a.family || (!a.project && !a.check)) {
  console.error('usage: fetch-font.mjs --project <dir> --family "Name" --weights 400,700 [--italic] | --check');
  process.exit(2);
}

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";
const weights = a.weights.split(",").map((w) => w.trim()).filter(Boolean);
const axes = a.axes ? a.axes : a.italic
  ? `ital,wght@${[...weights.map((w) => `0,${w}`), ...weights.map((w) => `1,${w}`)].join(";")}`
  : `wght@${weights.join(";")}`;
const url = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(a.family).replace(/%20/g, "+")}:${axes}&display=block`;

const res = await fetch(url, { headers: { "User-Agent": UA } });
if (!res.ok) {
  console.error(`Google Fonts has no "${a.family}" at weights ${a.weights}${a.italic ? " (+italic)" : ""} (HTTP ${res.status}).`);
  process.exit(1);
}
const css = await res.text();

// Keep only the /* latin */ blocks: one file per style+weight.
const faces = [];
for (const m of css.matchAll(/\/\*\s*latin\s*\*\/\s*@font-face\s*\{([^}]*)\}/g)) {
  const body = m[1];
  faces.push({
    style: /font-style:\s*(\w+)/.exec(body)[1],
    weight: /font-weight:\s*([\d ]+)/.exec(body)[1].trim(),
    src: /url\(([^)]+)\)/.exec(body)[1],
    stretch: /font-stretch:\s*([^;]+);/.exec(body)?.[1].trim(),
  });
}
if (!faces.length) {
  console.error("No latin subset found in the response.");
  process.exit(1);
}
if (a.check) {
  console.log(`ok ${a.family}: ${faces.map((f) => `${f.weight}${f.style === "italic" ? "i" : ""}`).join(", ")}`);
  process.exit(0);
}

const slug = a.family.toLowerCase().replace(/[^a-z0-9]+/g, "-");
const dir = join(a.project, "assets", "fonts");
mkdirSync(dir, { recursive: true });
const rules = [];
for (const f of faces) {
  const file = `${slug}-${f.weight.replace(/ /g, "-")}${f.style === "italic" ? "i" : ""}.woff2`;
  const path = join(dir, file);
  if (!existsSync(path)) {
    const r = await fetch(f.src, { headers: { "User-Agent": UA } });
    if (!r.ok) throw new Error(`download failed ${f.src}: ${r.status}`);
    writeFileSync(path, Buffer.from(await r.arrayBuffer()));
  }
  rules.push(
    `@font-face { font-family: "${a.family}"; font-style: ${f.style}; font-weight: ${f.weight};${f.stretch ? ` font-stretch: ${f.stretch};` : ""} font-display: block; src: url("assets/fonts/${file}") format("woff2"); }`,
  );
}
console.log(rules.join("\n"));
