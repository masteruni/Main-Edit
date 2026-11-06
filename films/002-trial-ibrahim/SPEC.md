# 002 · Paid trial edit for Ibrahim Ansari: "Everyone wants this"

TYPE:    general edit (no client preset). References in refs/ apply to this film only.
GOAL:    a stranger scrolling Reels stops on a mid-air yacht jump, feels the contrast between the reward everyone wants and the
         5 AM discipline nobody films, and gets paid off on a drop that turns the discipline into the reward. Loops on replay.
OUTPUT:  1080 x 1920, 30 fps, ~26 s, IG Reel / TikTok / Short. Burned-in kinetic captions (no VO in the footage).
SOUND:   Mixkit "Waka Floka Type" (id 364, Arabic-flavoured trap, 87.5 BPM, beat 0.686 s), entered at 6.0 s so its drop
         (14.0 s) lands at video 8.0 s. Mixkit SFX with a visible cause only. Target −14 LUFS, true peak ≤ −1 dBTP.

## Reference grammar (refs/ref1.mp4, refs/ref2.mp4): measured, used for this film only
- Cuts on the beat / on the spoken word; B-roll shots 0.5–1.5 s; heroes held 2–3 s.
- Kinetic type: one italic script word + bold sans words, stacked in the negative space beside the subject,
  word by word on the beat, white with a soft shadow, sometimes tinted to the scene.
- Warm highlights / teal shadows grade, deep blacks, light film texture.

## Hooks (three written, one chosen)
A. CHOSEN · Contrast: frame 1 = Ibrahim mid-air jumping off a yacht (slow-mo, splash on the beat), "Everyone wants *this.*" →
   hard cut on the alarm to him waking up in the dark, "Nobody wants *this.*" The contrast is set in 3 s.
B. Result first: a Stripe notification ("$50k today") as frame 1. Rejected: the phone screen is small and soft at Reel size,
   and money-first reads as a course ad.
C. Mid-action: a cold-plunge face shot with "5 AM." Rejected: strong image, but no promise until the payoff.

## Story & shot list (cuts on beats; music beats at video t = 0.457 + 0.6857·n)
| # | time | shot (proxy) | text | sound |
|---|------|--------------|------|-------|
| 1 | 0.00–1.74 | yacht jump, 0.5× slow-mo | Everyone wants / *this.* | music intro, water splash on landing |
| 2 | 1.74–3.13 | waking up, dark bedroom | Nobody wants / *this.* | alarm clock on the cut |
| 3–10 | 3.13–8.01 | praying → treadmill → pulldown → clap push-ups → cold plunge → night work → Stripe ×2 (shots get shorter: 0.7 → 0.35) | 5 AM. · No one / watching. · Every / *single* day. · Until… | riser into the drop, notification pops on the Stripe shots, 0.3 s silence before the drop |
| 11–25 | 8.01–18.46 | DROP: jetski spin, Burj Khalifa, Rolls-Royce Dubai, falcon in the desert (held 2 beats), ATV desert, wakesurf, yacht, jetski drone, Rolls-Royce starlight, BMW driver, Dubai yachts… | *it pays.* (on the drop) | impact on the drop; music full |
| 26 | 18.46–21.25 | riding a horse into the sea, slow-mo | Same / *24 hours.* | music low-passed (breather), sea waves |
| 27–28 | 21.25–23.34 | friends on the yacht at sunset → on a yacht | | glasses clink |
| 29 | 23.34–26.4 | fireworks over the yacht | Now everyone wants / *this.* | music to the end; loops back to shot 1 |

## Look
- Grade baked into each clip (ffmpeg): warm highlights, teal shadows, contrast +8%, saturation 108%, black lift 2%, 3% grain, 12% vignette.
- Type: Pinyon Script 400 (the script word, 150–190 px) + Hanken Grotesk 800 (sans, 64–84 px, tracking −1%), white #F6F2EA,
  shadow 0 4px 18px rgba(0,0,0,.45). Placed in the shot's empty side, inside the 80% title-safe box, never over the face.
- Motion: words land on beats, each word 0.12 s pop (scale 1.18 → 1, opacity 0 → 1, power3.out); held dead still; hard exit on the cut.
  One push-in (100 → 108%) baked into hero shots; a 2-frame white flash + 115 → 100% punch on the drop.

## BANNED
taste/BANNED.md in full, HyperFrames' "BANNED by default", plus for this film:
- whoosh on every cut (max 1 whoosh in the whole film);
- per-word yellow highlight captions, emoji;
- logo/end card; "follow for more" outro;
- a slow creeping zoom on every clip (only hero shots get a push).

## QA
t=0.2 (hook frame readable on a phone), 2.4 (contrast landed), 7.5 (Until…), 8.1 (drop flash + it pays.), 10.5 (falcon hero),
19.5 (Same 24 hours.), 25.5 (callback line), last frame → first frame (loop).
