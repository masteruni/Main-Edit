# Review · 001 Same Look

Delivered: `renders/final.mp4`, 1920×1080, 30 fps, 15.4 s, 4.2 MB.

## Scroll test (final cut)

| Time | What I see | Would I stay? |
| --- | --- | --- |
| 0.0–0.5 | A station chime, and a departure board listing WHOOSH ON CUT, ZOOM EVERY CUT, YELLOW CAPS… all via AI EDIT | **Yes.** I recognise these, and it's an odd, physical medium in a feed of talking heads. |
| 0.5–2.7 | Reading the list; the top row starts rattling and flips to SAME LOOK | Yes. The first laugh lands before 3 s. |
| 3.1–5.6 | Pull out: the whole board clatters, every row becomes SAME LOOK, every train 09:00 | Yes. It's a re-hook: bigger scale, a sound wave. |
| 5.6–8.0 | Three fast close-ups, AGAIN, AGAIN, AGAIN, each one row lower | Yes. The rhythm is the joke; something new every 0.7–0.9 s. |
| 8.0–8.7 | Silence, a blank row, a dark lamp, the chime | Yes. Anticipation: something is about to be announced. |
| 8.7–11.7 | SOMEWHERE ELSE via MAIN EDIT; BOARDING; the only light on the board comes on | Paid off at 70% of the runtime. |
| 11.7–15.4 | Everything else CANCELLED, one lit row | The end frame is a poster. It ends ~1.5 s after the last change; no outro. |

Weakest moment for a stranger: 3.1–3.4 s. Most of the board is still mid-flip, so it reads as noise for a quarter-second before the block forms. I'm keeping it: the noise is the cascade, and the sound carries it.

## What changed after review

The first draft failed the scroll test and the critic's review:
- **No real hook.** It opened on a wide, small board, unreadable on a phone. Now it opens tight on the readable list of clichés.
- **Unreadable setup.** The setup was on screen for 0.95 s. The premise now holds 1.35 s before it turns, and lands by 2.7 s.
- **Maker's jargon.** Destinations like BLUR-IN TITLES and CREAM + SERIF only mean something to toolmakers. They're now things a viewer has seen or heard, routed via AI EDIT, against MAIN EDIT.
- **Fake coverage.** Three "close-ups" were the same plate reframed. They're now real close-ups (tile ≈ 220 px) that move one row down per cut.
- **Payoff cropped.** BOARDING was never in the payoff shot. It's now split into a destination shot and a BOARDING + lamp shot.
- **Board in a void.** It's now hung by rods on a fully grained concrete wall, with a hard contact shadow, bleeding off the frame. The phantom wall slab and the soft blob "wear" are gone.
- **Inaudible sound.** The hall tone was inaudible on a phone and is now raised. Settle clacks are added, and there's a chime on frame 1.
- **New tells.** Seven new tells went into `taste/BANNED.md`.

## Measured, not heard

- Audio: −17.6 LUFS integrated, true peak −1.0 dBTP, no clipping, no digital silence. Target was −16; loudnorm's single pass stopped at the true-peak ceiling, so I kept −17.6 rather than clip. I can't hear: the clatter, chime and clacks were checked as waveforms and timings, not by ear.
- `hyperframes check`: 0 errors. Warnings kept on purpose:
  - `line_unread` on mid-flip glyphs (they are meant to blur past).
  - `nested_structure_needs_subcomposition`: one continuous board world across shots keeps every flap continuous through cuts.
  - `timeline_track_too_dense`: the shot markers.
- `fingerprint.mjs`: clean, shot CV 0.62.

## With more time

- **A 4:5 (1080×1350) cut for feeds.** In 16:9 on a phone the wide shots' glyphs are small. In 4:5 the wides would frame DESTINATION + REMARKS only.
- **A second critic pass** on the final; only my own frames and the scroll test checked it.
- **Real station room tone** from a recording instead of synthesised brown noise.
