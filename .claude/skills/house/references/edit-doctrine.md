# Edit doctrine

What separates an edited film from an assembled one is rhythm and sound. These numbers are defaults for this repo. A reference the person gives wins.

## Shot lengths

- Plan shot lengths as a **shape**, not a list. Write them in `SPEC.md` as a row of numbers before building, e.g. `4.2 · 1.1 · 0.9 · 1.4 · 3.0 · 0.6 · 0.6 · 0.6 · 2.4(hold) · 3.5`.
- Coefficient of variation (std/mean) of shot lengths **≥ 0.35**. `fingerprint.mjs` measures scene hosts; under 0.25 fails as metronomic.
- **Long–short–short–long.** Establish (3–5 s) → accelerate (0.5–1.5 s runs of 3–6 shots) → hold before the payoff (0.4–0.9 s of nothing new) → payoff at normal speed → land (≥ 2 s).
- A run of fast shots shares one thing (a direction of motion, a colour, a shape, a sound) so it reads as one phrase, not noise.
- First frame is a real image (it is the thumbnail). Something has already happened by 0.5 s.

## Cuts

- Cut **on action**: at the fastest frame of a move, matching direction across the cut.
- Cut **on sound**: a cut lands on a transient (a consonant, a beat, a hit) ± 1 frame. Off-beat cuts are a choice, used once as a jolt.
- **Match cuts** are the cheapest way to look expensive: a shape, a position or a motion that continues across the cut (the circle of a stamp becomes the circle of a clock). Plan at least one per film over 15 s.
- No crossfades between worlds. A dissolve means time passed; use it only for that.

## Sound

- Sound is designed, not added. In `SPEC.md`, each shot's line names its sound.
- Order of layers: **room / medium tone** (the hum of the copier, the hall of a station) under everything at −30 to −36 LUFS-ish, then **sync sounds** for visible actions, then **voice**, then **music** last.
- Music is allowed to be absent. When present: it enters after the first sound, it **drops out 0.4–1.0 s before the payoff**, and returns (or doesn't) on the payoff's downbeat.
- Loudness targets: social −14 LUFS integrated, YouTube −14, broadcast −23. `npx hyperframes normalize-audio`. True peak ≤ −1 dBTP.
- You cannot hear. Measure (`npx hyperframes audio <file> --json`) and say in `REVIEW.md` that the mix was measured, not heard.

## Pacing per platform

| Where | Length | First 1 s | Shot mean | Captions |
| --- | --- | --- | --- | --- |
| Reels / TikTok / Shorts (9:16) | 12–45 s | the most interesting frame of the film, not a title | 1.2–2.2 s | yes, burned |
| Feed (4:5 or 1:1) | 15–60 s | a question the image asks | 1.8–3 s | yes |
| YouTube / web (16:9) | any | the world, then the problem | 2.5–5 s | sidecar `.srt` |
| Launch / landing loop | 8–20 s, loops | identical to last frame | 2–4 s | none |

## Holds

- A line the viewer reads: 0.5 s + 0.3 s per word, minimum. The final line ≥ 2 s.
- A deliberate hold of nothing new (dread, anticipation, a joke landing) carries `data-hold` so `check` stops warning, and is written in `SPEC.md` with its reason.
