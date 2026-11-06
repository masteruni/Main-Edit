#!/usr/bin/env node
// Builds the flap schedule for every tile (pure data, seeded) and injects it into index.html.
// The same schedule drives the picture (index.html) and the sound (build/sound.py), so every
// click you hear belongs to a flap you see.
import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const DIR = join(dirname(fileURLToPath(import.meta.url)), "..");
export const ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.-+&";
export const FIELDS = { time: [0, 5], dest: [5, 14], plat: [19, 2], rem: [21, 9] }; // [first tile, width]
const COLS = 30;

function mulberry32(a) {
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rnd = mulberry32(1994);

const start = [
  ["09:00", "DARK VOID", "2", "ON TIME"],
  ["09:04", "BLUR-IN TITLES", "4", "ON TIME"],
  ["09:08", "CREAM + SERIF", "1", "ON TIME"],
  ["09:12", "WORD-POP CAPS", "3", "ON TIME"],
  ["09:16", "NEON GLOW", "2", "ON TIME"],
  ["", "", "", ""],
];
// [t, row, field, text, flapSeconds]
const changes = [];
for (let r = 0; r < 5; r++) changes.push([0.75 + r * 0.09, r, "dest", "SAME LOOK", 0.026]);
// Each AGAIN starts before its close-up (cut on action) and lands >= 0.4 s before the next cut, so it is read.
changes.push([2.7, 1, "rem", "AGAIN", 0.028], [3.45, 2, "rem", "AGAIN", 0.028], [4.35, 3, "rem", "AGAIN", 0.028]);
changes.push([4.5, 0, "rem", "AGAIN", 0.028], [4.62, 4, "rem", "AGAIN", 0.028]); // land before the silent hold at 5.9
changes.push([6.75, 5, "time", "10:00", 0.04], [6.8, 5, "dest", "SOMEWHERE ELSE", 0.04], [6.86, 5, "plat", "1", 0.04], [6.9, 5, "rem", "BOARDING", 0.04]);
for (let r = 0; r < 5; r++) changes.push([9.85 + r * 0.12, r, "rem", "CANCELLED", 0.03]);

const pad = (s, n) => (s.toUpperCase() + " ".repeat(n)).slice(0, n);
const rows = start.map((row) => {
  const chars = [];
  for (const [i, f] of ["time", "dest", "plat", "rem"].entries()) chars.push(...pad(row[i], FIELDS[f][1]));
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
    if (r === 5) lampOn = Math.max(lampOn, t0 + n * dt);
  }
}
lampOn = +(lampOn + 0.12).toFixed(3);

const schedule = { alphabet: ALPHABET, cols: COLS, rows: tiles, lampRow: 5, lampOn };
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
