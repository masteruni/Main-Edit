# 001 · Same Look

LOOK-ID: split-flap
TYPE:    general (no client preset)

GOAL:    a viewer who has scrolled past a hundred AI-edited videos recognises every cliché on the board, laughs when they all go to SAME LOOK, and remembers the one train that goes somewhere else.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps (a 4:5 cut is the next deliverable, see REVIEW.md)
TIME:    15.4 s x 30 = 462 frames. No music: the flap clatter is the score.

HOOKS (three written, one chosen):
  A. Specific claim, wide: "Every AI edit departs at 09:00" on the whole board. Rejected: a wide is unreadable on a phone (the first draft's P0).
  B. Pattern break, sound only: black frame + PA chime, board revealed after 1 s. Rejected: frame 1 must be a picture.
  C. Recognition, tight (CHOSEN): frame 1 is a close board listing clichés the viewer has *seen and heard* (WHOOSH ON CUT, ZOOM EVERY CUT, YELLOW CAPS, SLOW-MO DRONE, TIKTOK VOICE) via AI EDIT, with a PA chime on frame 1. The turn (row 1 → SAME LOOK) lands by 2.7 s.

LOOK:    split-flap (.claude/skills/house/looks/split-flap.md). Why: the subject is "everyone departs to the same destination"; a departure board is the one medium where that is literally what you read.
         housing #1E1F1D, tiles #2E2F2C (top) / #2A2B28 (bottom), split 2 px #121311; ink #EFE7D3; amber lamp #FFB21A on exactly one row;
         concrete wall #8C8A84 with 13% fractal grain across the whole wall; the board hangs from two steel rods #5D5C57; hard 7 px contact shadow.
         Barlow Condensed 700 for every flap (76 px glyph on a 64 x 92 tile, board space), 500 for painted column heads (26 px, +10% tracking).
         Columns TIME · DESTINATION · VIA · REMARKS, 60 px between fields, lamp column on the right.
OBJECTS: a mechanical departure board hung on a concrete station wall by two rods, a DEPARTURES plaque above it.
MOTION:  characters change only by flipping forward through the flap alphabet, 0.026–0.04 s per flap (±10% seeded per tile), tiles 0.03 s apart, finishing at different times.
         camera: linear dollies (≤ 30 px/s in frame); hard cuts between framings; no eased camera moves. Lamp: on in 1 frame with a 3-frame overshoot.

SHOTS:
  S1  0.0–3.1   HOOK. Tight on DESTINATION + VIA, rows 1–5 readable. Chime on frame 1. Row 1 holds WHOOSH ON CUT for 1.35 s, then flips to SAME LOOK (lands 2.7).
  S2  3.1–5.6   RE-HOOK / reveal. The whole board (bleeds left): every row flips to SAME LOOK and every TIME to 09:00, a clatter wave. Row 2's REMARKS start flipping at 5.0 (cut on action).
  S3  5.6–6.5   REMARKS of row 2, tile ≈ 220 px: AGAIN lands 6.24.
  S4  6.5–7.2   one row down, same size: AGAIN lands 6.97.
  S5  7.2–8.0   one row down: AGAIN lands 7.64. (S3–S5 are one phrase; all other AGAINs land off-screen before 8.0.)
  S6  8.0–8.7   HOLD (data-hold). Blank REMARKS tiles + dark lamp of the last row, dead still, no clicks. The chime returns.
  S7  8.7–10.3  PAYOFF 1. The last row: SOMEWHERE ELSE via MAIN EDIT flips in (lands 9.77), the SAME LOOK block above it.
  S8  10.3–11.7 PAYOFF 2. REMARKS + lamp: BOARDING lands 10.70, the lamp lights at 10.78 with a heavy settle clack.
  S9  11.7–15.4 LAND. The board: seven rows flip to CANCELLED (12.2 → 13.89), the lit row stays. 1.5 s still hold.
SHOT SHAPE: 3.1 · 2.5 · 0.9 · 0.7 · 0.8 · 0.7(hold) · 1.6 · 1.4 · 3.7  (CV 0.62)

BANNED:  taste/BANNED.md in full; HyperFrames "BANNED by default"; split-flap's own fails (tiles cycling in sync, a small board in a void, a full board unreadable on a phone).
         For this film also: no music, no whoosh, no fade anywhere, no logo end card, no maker's jargon on the board.
QA:      t=0.1 (hook frame: clichés readable), t=2.9 (row 1 SAME LOOK, others still clichés), t=4.2 (cascade mid-flip), t=6.3 (AGAIN close),
         t=8.3 (blank hold), t=9.9 (SOMEWHERE ELSE via MAIN EDIT), t=11.3 (BOARDING + amber lamp), t=15.2 (CANCELLED block + one lit row).
