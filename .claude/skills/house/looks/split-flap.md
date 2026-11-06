---
id: split-flap
medium: a mechanical split-flap departure board in a station hall
energy: mid
suits: [launch, date, schedule, status, travel, release, countdown, update, announcement, roadmap, delay, event, time]
avoid: [kids, food, soft, wellness]
faces: ["Barlow Condensed"]
---

## Parts

- **Board**: the frame IS the board. Housing `#1E1F1D`, flap tiles `#2B2C29` with a 2 px horizontal split line `#121311` across the middle of every tile. There is no empty void: tiles fill the frame edge to edge, blank tiles included.
- **Ink**: flap lettering `#EFE7D3` (aged white).
- **Status lamp**: amber `#FFB21A` for exactly one status cell or one lamp per shot (BOARDING, NOW, DELAYED). Green `#38C172` only for a single "ON TIME" if the story needs good news.
- **Hall**: optional wide shots show the board mounted in a hall: concrete `#8C8A84`, people as motion-blurred silhouettes from real footage only.

## Numbers

- Tile: 64×92 px at 1080p with 6 px gutters; a row is a line of text. Characters Barlow Condensed 700, 74 px, centred in the tile, caps only.
- Columns like a real board: TIME · DESTINATION · VIA · PLATFORM · REMARKS. Use the columns to carry the message (DESTINATION = the product, TIME = the launch date, REMARKS = the status).
- Hero shots: crop the board so 3–5 tiles fill the frame width (tile ≈ 380 px wide), the split line big and visible.

## Surface

- Each tile: top half 4% lighter than bottom half (the flap catches the hall light). 1 px highlight on the top edge of each flap at 25%.
- Wear: seeded scuffs on 10% of tiles, 3–8% lighter blotches.
- Subtle hall flicker: board brightness ±2% at 0.5 Hz **only** in wide shots.

## Motion

- Letters change by **flipping through the alphabet**: each tile flips top flap down in 0.06 s per character (linear rotateX 0 → −90° on the top half, then the next bottom half from 90° → 0), cycling through 4–14 intermediate characters before landing. Tiles in a row start 0.02–0.05 s apart, left to right, and **finish at different times** (different cycle counts, seeded).
- Nothing on the board ever fades or slides. Only the camera moves: slow lateral dolly (40–80 px/s, linear) or a push to a single row (0.9 s `power2.inOut`).
- Lamps switch on in 1 frame with a 3-frame 120% overshoot in brightness.

## Transitions

- **Row cascade**: the whole board refreshes, rows flipping top to bottom 0.08 s apart; the new board is the new scene.
- **Rack to the next row**: camera pushes from one row to another; focus pulls (blur 0 → 6 px → 0 on the board layer) in 0.5 s.
- **Cut on the clack**: a hard cut exactly on the frame where the last tile lands.

## Sound

The flap clatter is the soundtrack: one short click per flip, layered so a cascade becomes a rattling wave; a final settle clack. Station hall tone underneath. A single PA chime (two notes) before the key line. Music: none, or a slow synth pad entering only after the payoff.

## Voice

Board language. Caps, terse, no punctuation except the colon in times. `NOW BOARDING`, `PLATFORM 4`, `DELAYED → ON TIME`, `ALL DESTINATIONS`. The joke or emotion lives in the gap between board language and what it says.

## How this look fails

- Cycling every tile at once, all finishing together: reads as a digital effect. → Staggered starts, seeded cycle counts.
- A tiny board in the middle of a dark frame. → The board fills the frame; that's the rule.
- Too much text: a full board is unreadable at phone size. → Hero shots show one row.
