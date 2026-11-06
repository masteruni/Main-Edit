# 001 · Same Look

LOOK-ID: split-flap

GOAL:    a viewer who has scrolled past a hundred AI-edited videos laughs at the board, then remembers that one train goes somewhere else.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps
TIME:    13.2 s x 30 = 396 frames. No music: the flap clatter is the score.
LOOK:    split-flap (.claude/skills/house/looks/split-flap.md). Why: the subject is "everyone departs to the same destination"; a departure board is the one medium where that is literally what you read.
         ground = the board itself, housing #1E1F1D, tiles #2E2F2C (top) / #2A2B28 (bottom), split 2 px #121311; ink #EFE7D3;
         amber lamp #FFB21A on exactly one row; hall wall #8C8A84 with 5% noise only at the frame edges in wide shots.
         Barlow Condensed 700 for every flap character (62 px glyph on a 52 x 76 tile, board space), 500 for the painted column heads (22 px, +8% tracking).
OBJECTS: a mechanical departure board mounted on a station wall, with a painted operator plaque above it ("MAIN EDIT · DEPARTURES").
         Tiles read as flaps because the top half is lighter than the bottom and the split line crosses every glyph.
MOTION:  board characters only change by flipping forward through the flap alphabet, 0.036–0.044 s per flap (seeded per tile), tiles in a field start 0.03 s apart and finish at different times.
         camera: linear dollies 40–60 px/s; hard cuts between framings, no eased camera moves. Lamp: 1-frame on with a 3-frame overshoot.
SHOTS:
  S1  0.0–3.6   wide board. Rows read the tells as destinations (DARK VOID, BLUR-IN TITLES, CREAM + SERIF, WORD-POP CAPS, NEON GLOW), all ON TIME.
                at 0.9 s the destinations cascade to SAME LOOK, row by row. Row 6 is blank. Sound: hall tone, then the clatter wave.
  S2  3.6–4.4   close on row 2 (dest + remarks). Its REMARKS are mid-flip (started 3.2 s, cut on action) and land on AGAIN.
  S3  4.4–5.1   close on row 3: AGAIN lands.
  S4  5.1–5.9   close on row 4: AGAIN lands. (S2–S4 are one phrase: same move, same sound, different row.)
  S5  5.9–6.7   extreme close on the blank row's tiles; nothing moves. PA chime (two notes). data-hold: anticipation.
  S6  6.7–9.7   the blank row, readable whole: flips to 10:00 · SOMEWHERE ELSE · 1 · BOARDING. Amber lamp on when the last tile lands.
  S7  9.7–13.2  wide again. The five SAME LOOK rows flip their remarks to CANCELLED, top to bottom. The amber row stays. Final hold ≥ 1.5 s after the last tile lands.
SHOT SHAPE: 3.6 · 0.8 · 0.7 · 0.8 · 0.8(hold) · 3.0 · 3.5  (CV ≈ 0.68)
BANNED:  taste/BANNED.md in full; HyperFrames "BANNED by default"; split-flap's own fails: every tile cycling in sync, a small board in a dark void, a full board unreadable on a phone.
         For this film also: no music, no whoosh, no fade anywhere, no logo end card.
QA:      t=0.2 (thumbnail reads as a board listing AI tells), t=2.6 (all SAME LOOK), t=4.3 (AGAIN landed), t=6.3 (blank hold), t=8.6 (SOMEWHERE ELSE + lamp), t=12.8 (CANCELLED + one amber row). Phone sheet: S2–S6 legible at 360 px.
