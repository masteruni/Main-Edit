# Review · 002 trial edit (v5)

## v5 changes (person's notes: captions don't look like the reference and stutter; didn't like the music or SFX)
- **Captions, re-measured side by side against ref3:**
  - Key words now ~50% of frame width (v4 ran 65–85%).
  - Small words sit on one line, left-aligned on top of the key word, tight.
  - Single filler words are small; firmer offset drop shadow; blur-in without scale.
- **Stutter fixed:** units are grouped so every caption holds ≥ 0.36 s (v4 flashed words for 0.12–0.2 s, each re-triggering the blur and scale).
- **Music (the person's pick):** Mixkit #32 "Driving Ambition" (uplifting brass + drums, 99.4 BPM).
  - Entered so its full-band hit (37.66 s, measured) lands on the drop; B-roll re-cut to the new grid.
  - "10 million" now starts 0.3 s after the hit, so the ducking doesn't swallow it. The drop is the loudest moment (−11.4 dB vs −14).
- **SFX (the person's pick: minimal & clean):** one soft impact on the drop and a soft whoosh on three big cuts. Nothing else.
- Loudness −14.0 LUFS, true peak −1.4 dBTP, no clipping. Measured, not heard.
- `hyperframes check` hung at its final analysis step this round, so it is unverified for v5.
  - Earlier it was blocked by a stuck background check process and browser, which I killed.
  - Lint: 0 errors. The render completed normally.

---


## v4 changes (person's notes: "this kind of typography", motivational music, more professional SFX)
- **Typography:** ref3 studied (REFERENCE.md "ref3").
  - Inter Black at -4% (a Helvetica Neue Heavy match), centred on the chest, word-by-word replacing.
  - A small connector stacks over a big key word. Key words are lowercase with end punctuation; "$1,000" and "MILLION" in caps.
  - Every word blurs in from 12 px with a 108→100% scale settle over 4 frames.
  - Two key words are overlay-blended into the plate. Lines moved off faces.
- **Music:** Mixkit #31 "Dreaming Big" (uplifting film score, piano + strings → drums), 89.1 BPM.
  - Soft piano under the story; the measured drum entry (30.22 s) lands on "10 million dollars".
  - B-roll re-cut to the new beat grid.
- **SFX, rebuilt:**
  - Removed coins, notification pops and the alarm.
  - Added the footage's own sound (jetski, desert, wake, water, car) under the music.
  - A long swell plus riser that stop dead at the silence, then a layered sub-boom and punch on the drop; one air sweep into the montage.
  - Every effect is now placed by its measured peak. v3's "big cinematic impact" peaked 2.1 s after its start, so its hit had landed late.
- Loudness −14.0 LUFS, true peak −1.4 dBTP, no clipping. Measured, not heard.

---


Delivered: `renders/ibrahim-trial-edit.mp4`, 1080×1920, 30 fps, 30.6 s, H.264 CRF 17 + AAC 256k (not in git).
Preview: `renders/v5-preview.mp4`.

## Scroll test (v3)
| Time | What a stranger sees and hears | Stay? |
| --- | --- | --- |
| 0.0–2.0 | Three guys frozen mid-air off a yacht, black & white snapping to colour, a voice: "Feeling like your dreams are impossible?" | Yes. Striking image and a direct question to me. |
| 2.0–4.2 | The man himself in a purple-lit studio: "This is the video for you." | Yes. Now there's a person and a promise. |
| 4.2–9.2 | At his desk: "If you're earning under $1,000 MONTHLY, you're fighting an *Uphill* battle." | Yes. It names my situation; the framing changes 1.4× on the jump cut. |
| 9.2–14.2 | "…the most *Honest* conversation… what really *Changed* my life" over 5 AM life: waking, prayer, treadmill, gym | Yes. Open loop: what changed it? |
| 14.2–18.5 | Shots get shorter, his real Stripe numbers, a riser, then silence and black | Tension; I want the payoff. |
| 18.5–23.9 | Flash + drop: "10 MILLION dollars in *Valuations* going up." Jetski ramp, desert, falcon | Paid off at 61%, in his own words. |
| 24.0–27.0 | "And now we're launching *Another* software company" | Second loop: there's more. |
| 27.0–30.2 | His selfie on a yacht: "*Lock* in boys, *Lock* in. Let's go." | Ends on energy and a person; loops into the jump. |

## What changed after review
- v2 critic (fresh-eyes agent): payoff at 31%, montage of other people, stock-motivational copy, echo ending, unreadable proof, script colliding with the line above. All addressed in v3:
  - The story is now his own voiceover, found by listing the full Dropbox (893 files) and transcribing 13 voice candidates.
  - Copy is his words only.
  - Proof is punched until the number reads.
  - The payoff comes at 61%, with a second loop after it.
  - It ends on him, not an echo.
- Reference studied frame by frame (REFERENCE.md). The fonts were identified by side-by-side rendering: Montserrat Bold + Parisienne, replacing my earlier Hanken + Pinyon.

## Measured, not heard
- Loudness −14.0 LUFS integrated, true peak −1.0 dBTP, no clipping.
- Voice lines are levelled within 1 dB of each other. The pre-drop gap is digital silence.
- I cannot hear: voice clarity was judged by SNR (19–23 dB on the hook and the closing line, 11–15 dB on the podcast and Miami lines). The noisy "4 AM webinar" line (6 dB) was left out.
- Whisper wrote his name as "every". The line containing it isn't used.

## Kept on purpose
- `line_unread` warnings: the reference captions each word on its spoken onset, so words are heard while read.
- Blur-in sans words and Montserrat (house bans) are allowed for this film only, because the client's reference uses them.

## Weakest moment / with more time
- 14.2–16.4 s: the montage plays under quieter music before the riser. A second voice line here would carry it.
- A 16:9 cut for YouTube; a version with burned-in captions sized for TikTok's UI.
