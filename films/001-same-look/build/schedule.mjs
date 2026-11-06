#!/usr/bin/env node
// Builds the flap schedule for every tile (pure data, seeded) and injects it into index.html.
// The same schedule drives the picture (index.html) and the sound (build/sound.py), so every
// click you hear belongs to a flap you see.
import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const DIR = join(dirname(fileURLToPath(import.meta.url)), "..");
export const ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.-+&";
export const FIELDS = { time: [0, 5], dest: [5, 14], via: [19, 9], rem: [28, 9] }; // [first tile, width]
const ORDER = ["time", "dest", "via", "rem"];
const COLS = 37;

function mulberry32(a) {
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rnd = mulberry32(1994);

// Viewer-facing tells (things people have seen or heard), all routed via AI EDIT. Row 7 is the payoff.
const TELLS = ["WHOOSH ON CUT", "ZOOM EVERY CUT", "YELLOW CAPS", "SLOW-MO DRONE", "TIKTOK VOICE", "STOCK B-ROLL", "NEON GLOW"];
const start = TELLS.map((d, r) => [`09:${String(r * 4).padStart(2, "0")}`, d, "AI EDIT", "ON TIME"]);
start.push(["", "", "", ""]);
export const PAYOFF_ROW = 7;
// [t, row, field, text, flapSeconds]
const changes = [];
changes.push([1.35, 0, "dest", "SAME LOOK", 0.026]); // the hook's turn, in close-up
for (let r = 1; r < 7; r++) {
  changes.push([3.15 + (r - 1) * 0.09, r, "dest", "SAME LOOK", 0.026]); // the reveal: the whole board goes the same way
  changes.push([3.3 + (r - 1) * 0.09, r, "time", "09:00", 0.03]); //  and every train leaves at once
}
// Each AGAIN starts before its close-up (cut on action) and lands >= 0.4 s before the next cut.
changes.push([5.0, 1, "rem", "AGAIN", 0.028], [5.75, 2, "rem", "AGAIN", 0.028], [6.45, 3, "rem", "AGAIN", 0.028]);
for (const [r, t] of [[0, 6.5], [4, 6.56], [5, 6.62], [6, 6.68]]) changes.push([t, r, "rem", "AGAIN", 0.028]);
changes.push([8.7, 7, "time", "10:00", 0.04], [8.72, 7, "dest", "SOMEWHERE ELSE", 0.034], [8.85, 7, "via", "MAIN EDIT", 0.034]);
changes.push([10.05, 7, "rem", "BOARDING", 0.03]);
for (let r = 0; r < 7; r++) changes.push([12.2 + r * 0.08, r, "rem", "CANCELLED", 0.03]);

const pad = (s, n) => (s.toUpperCase() + " ".repeat(n)).slice(0, n);
const rows = start.map((row) => {
  const chars = [];
  for (const [i, f] of ORDER.entries()) chars.push(...pad(row[i], FIELDS[f][1]));
  return chars;
});

// Per tile: { c0: initial char, ev: [{t, from, to, n (flaps), dt}] }
const tiles = rows.map((chars) => chars.map((c) => ({ c0: c, ev: [] })));
const clicks = []; // [time, col, row, kind] kind 0 = flap, 1 = final settle
let lampOn = 0;
for (const [t, r, field, text] of changes.sort((a, b) => a[0] - b[0])) {
  const [first, width] = FIELDS[field];
  const flap = changes.find((c) => c[0] === t && c[1] === r && c[2] === field)[4];
  const target = pad(text, width);
  for (let k = 0; k < width; k++) {
    const tile = tiles[r][first + k];
    const cur = tile.ev.length ? tile.ev[tile.ev.length - 1].to : tile.c0;
    const to = target[k];
    if (cur === to) continue;
    const n = (ALPHABET.indexOf(to) - ALPHABET.indexOf(cur) + ALPHABET.length) % ALPHABET.length;
    const dt = +(flap * (0.9 + rnd() * 0.2)).toFixed(4);
    const t0 = +(t + k * 0.03 + rnd() * 0.02).toFixed(4);
    tile.ev.push({ t: t0, from: cur, to, n, dt });
    for (let j = 0; j < n; j++) clicks.push([+(t0 + j * dt + dt * 0.55).toFixed(4), first + k, r, 0]);
    clicks.push([+(t0 + n * dt).toFixed(4), first + k, r, 1]);
    if (r === PAYOFF_ROW && field === "rem") lampOn = Math.max(lampOn, t0 + n * dt);
  }
}
lampOn = +(lampOn + 0.08).toFixed(3);
clicks.push([lampOn - 0.08, 36, PAYOFF_ROW, 2]);
const lastCancel = Math.max(...clicks.filter((c) => c[3] === 1 && c[0] > 12).map((c) => c[0]));
clicks.push([lastCancel, 30, 6, 2]);

const schedule = { alphabet: ALPHABET, cols: COLS, rows: tiles, lampRow: PAYOFF_ROW, lampOn };
writeFileSync(join(DIR, "assets/schedule.json"), JSON.stringify({ lampOn, clicks }));
const html = readFileSync(join(DIR, "index.html"), "utf8");
const out = html.replace(/\/\*SCHEDULE\*\/[\s\S]*?\/\*END\*\//, `/*SCHEDULE*/ ${JSON.stringify(schedule)} /*END*/`);
writeFileSync(join(DIR, "index.html"), out);
const last = Math.max(...clicks.map((c) => c[0]));
console.log(`tiles with events: ${tiles.flat().filter((t) => t.ev.length).length}, clicks: ${clicks.length}, last flap lands ${last.toFixed(2)} s, lamp on ${lampOn} s`);
for (const [r, row] of tiles.entries()) {
  const lands = row.flatMap((t) => t.ev.map((e) => +(e.t + e.n * e.dt).toFixed(2)));
  console.log(`row ${r}: ${lands.length ? `${Math.min(...lands)}–${Math.max(...lands)}` : "static"}`);
}
