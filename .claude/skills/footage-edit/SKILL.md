---
name: footage-edit
description: Editing real footage in this repo - talking heads, vlogs, podcasts, interviews, tutorials, reels from phone video, B-roll montages. The editor's judgment layer (what to cut, how much air to leave, how framing hides jump cuts, how captions and B-roll behave) on top of HyperFrames' transcribe / transcript-cut / media-treatment tools. Read after /hyperframes and /house whenever the person gives you video files.
---

# Footage edit

Most "AI edits" are a transcript run through a silence remover, a zoom on every cut, and yellow word-pop captions. All three are tells. The footage is the film; the tools serve the read.

## Pipeline

1. **Ingest & look.** `ffprobe` every file (resolution, fps, rotation, audio channels, VFR). Make a 1 fps contact sheet (`ffmpeg -i in.mp4 -vf "fps=1,scale=320:-1,tile=8x8" sheet.png`) and **look at it** before deciding anything: where is the face, the light, burned-in text, the best moments.
2. **Transcribe.** `npx hyperframes transcribe <file> --model small.en --json` (or `--model small --language <code>`). Read the transcript. Fix names and terms by hand.
3. **Paper edit first.** Write `PAPER-EDIT.md`: the story in the speaker's own sentences, reordered if that tells it better, with timestamps. Cut whole ideas before you cut breaths. A 3-minute ramble usually holds a 40-second film; find the sentence it ends on, then the one it opens on (usually the most surprising claim, not the greeting). Write **three hook candidates** pulled from anywhere in the recording (a result, a specific claim, a moment of conflict, a reaction) per `/house` `references/retention.md`, and move the chosen one to 0 s even if it was said at 2:40. Then plan a re-hook every 3–6 s (framing change, B-roll, on-screen word, sound) and cut everything after the payoff.
4. **First pass, mechanically.** `node tools/edit-plan.mjs assets/transcript.json --audio <source> --style social|conversational|calm` (always pass `--audio`: whisper stretches words over pauses, so only measured silence finds the dead air) proposes fillers, stutters, dead air and a framing plan. Read every candidate; keep a "like" or a pause when it's doing work (comic timing, thinking on camera, a real emotional beat).
5. **Compile** with `node .claude/skills/media-use/scripts/transcript-cut.mjs --input … --transcript … --remove "<ranges>" --plan` first, then without `--plan` to write the cut. Or build the cut as clips in a HyperFrames composition when graphics interleave with it.
6. **Picture.** Grade with `npx hyperframes media-treatment` (measure with `--analyze` first). Reframe for the platform (see below). Captions, B-roll, graphics from the look.
7. **Sound.** `npx hyperframes normalize-audio --lufs=-14` for social. Room tone under every cut (never digital silence between words: a hard silence gap is audible). Music, if any, ducks under voice (`/media-use` mixing) and drops out before the line that matters.
8. **Review** with the `slop-critic` agent, then render.

## Cutting voice

- **Air is rhythm.** Never remove every pause. Leave 0.12–0.2 s between phrases, 0.25–0.35 s at a sentence end, up to 0.6 s after a question or before a punchline. `edit-plan.mjs` does this by style.
- Cut in the silence just before a plosive or the start of a breath, never mid-word. Check each join by ear-proxy: the waveform at the cut is near zero, and there's no half-breath left.
- **J and L cuts** when B-roll or a second angle exists: let the next sentence's audio start 4–10 frames under the current picture (J), or keep the picture on the speaker 4–10 frames into the B-roll's sound (L). Hard A/V cuts on every edit read as a machine.
- Keep one imperfection per minute that makes the person human (a laugh, a self-correction that lands). Over-cleaned speech sounds generated.

## Framing

- Jump cuts inside a sentence change framing (wide 1.00 ↔ tight 1.18) so they read as edits; a new idea goes back to wide. One extreme close (1.30–1.40) only on the strongest word of a fast run. `edit-plan.mjs` proposes this; **it is never "zoom on every cut"**.
- Punch-ins are instant (a cut), not animated zooms. A slow creeping zoom over a whole clip is a tell; use it only for a single sentence that is the emotional peak, at ≤ 4% total.
- Keep eyes on the upper third line. When scaling, re-centre on the face, not the frame.
- Vertical from horizontal: crop around the face with a fixed crop per shot; move the crop only on cuts. A crop that drifts to follow the head looks like auto-reframe software.

## Captions

- Phrase groups of 2–5 words broken at breath and syntax, from `/hyperframes` `references/captions.md` timing rules.
- Style comes from the look file's type and medium (a receipt look prints captions as receipt lines; a broadcast look uses its lower-third language). Default when no look: one face (never a banned one), sentence case, ink on a tight per-line scrim, no per-word pop, **no emoji, no all-caps, no coloured keyword** unless the look calls for it.
- Captions leave when a graphic is on screen saying the same thing. Captions never cover the mouth.
- Deliver `.srt` as well for platforms that support native captions.

## B-roll

- Not literal. If the speaker says "money", do not cut to a stack of cash. Cut to what the money *did* (the product, the place, the person's reaction).
- B-roll comes from the speaker's world first: their screen recordings, their product, their room, photos they own. Stock is the last resort and never generic (no handshake, no typing hands, no city timelapse).
- Every B-roll shot is motivated by a word, and its cut lands on that word's start ± 2 frames.
- B-roll shot length follows `house/references/edit-doctrine.md`: vary it.

## Footage problems

| Problem | Do |
| --- | --- |
| Dark / flat / colour cast | `media-treatment --analyze`, then a grade; see `/media-use` `references/grading.md` |
| Shaky handheld | `ffmpeg` vidstabdetect/vidstabtransform two-pass, then crop ~6% |
| VFR phone video | Re-encode CFR before anything: `ffmpeg -i in.mov -vf fps=30 -c:v libx264 -crf 16 -c:a aac cfr.mp4` |
| Echoey room / noise | `ffmpeg` `afftdn=nf=-25` + a gentle high-pass at 80 Hz; say in REVIEW.md that it was measured, not heard |
| Burned-in captions already present | Scan the contact sheet; place ours elsewhere or crop |

## Delivery

- Render per platform from one project: 9:16 1080×1920 for Reels/TikTok/Shorts, 4:5 1080×1350 feed, 16:9 1920×1080 YouTube. Separate compositions sharing the cut.
- In `REVIEW.md`: the paper edit decisions, what was cut and why, the loudness measured, and that audio was measured, not heard.
