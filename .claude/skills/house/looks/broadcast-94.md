---
id: broadcast-94
medium: 1990s TV sports and news graphics package over live footage
energy: high
suits: [results, ranking, leaderboard, live, versus, sports, score, stats, competition, news, breaking, overlay, footage, highlights, podcast, interview]
avoid: [calm, luxury, wellness, minimal]
faces: ["Chakra Petch"]
---

Built to sit **over footage**. Without footage it becomes a parody; use it only when there's real video (or a real broadcast-style story).

## Parts

- **Footage**: full-frame, graded with `npx hyperframes media-treatment` toward broadcast tape: saturation 108%, a slight warm lift in the blacks, 1.5% grain, never crushed. Never under a dim overlay.
- **Bars**: graphics are **bars with bevels**: a main bar in network red `#C8102E`, a secondary in deep field green `#0B3D2E`, legend white `#FFFFFF`; a 3 px top highlight at 35% white and a 3 px bottom shade at 30% black (the 90s bevel). Bars are skewed −12°.
- **Bug**: the score/clock bug lives top-left, compact, always on during "live" sections, and is the only persistent element.
- **Accent**: gold `#F2B705` for a single number (the score, the rank, the record).

## Numbers

- Chakra Petch 700 italic for names and numbers, 700 roman for small legends. Lower-third name 58 px caps, title 34 px, tracking +2%.
- Lower third sits at 74% of frame height, left edge at the 10% action-safe line, width 40–55% of frame.
- Numbers in the bug: 46 px, tabular.

## Surface

- Bars carry a fine horizontal scanline texture (1 px lines every 3 px at 6%), not the footage.
- Footage: optional interlace shimmer only on freeze-frames (the classic "replay freeze": 2-frame stutter then hold, with a white 1-frame flash).

## Motion

- **Wipes with a leading edge**: bars extend from their anchor with a 10 px gold leading edge, 0.25 s `power3.out`; the legend wipes in behind the edge (clip-path), never fades.
- Exits: retract into the anchor 0.18 s `power3.in`.
- Numbers **roll** (odometer: digits scroll vertically, linear, last digit lands with a 2-frame overshoot).
- A **stinger** (a shape that crosses the full frame in 0.5 s) covers every change of segment.

## Transitions

- **Stinger**: a skewed red/green/gold bar stack sweeps across the frame left→right in 0.5 s; the cut to the next footage happens at its midpoint when the frame is fully covered.
- **Replay freeze**: the footage freezes with a 1-frame white flash, the word REPLAY in the corner bar, then the slow-motion clip plays (`playbackRate` via a pre-rendered slow clip, never by seeking).
- **Split screen versus**: the frame divides along the −12° skew; two feeds slide in from opposite sides.

## Sound

Stadium / studio ambience under the footage. Stinger = a short brass-and-drum sting (one per segment, max 3 per film). Odometer = a quick tick roll. A crowd swell on the payoff. Commentary-style voice works; keep it energetic and short.

## Voice

Broadcast shorthand: `FINAL`, `LIVE`, `NEW RECORD`, `+12 THIS WEEK`, `ROUND 2`, names in caps, stats with units.

## How this look fails

- Graphics over a flat colour, with no footage. → Footage or don't use this look.
- Glossy "web 2.0" bars. → The bevel is 3 px and hard-edged, not a gradient blob.
- A stinger on every cut. → Only between segments.
