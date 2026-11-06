# Retention: hook, hold, payoff

Every edit is judged by one person: someone scrolling with their thumb already moving. They give the first frame about half a second and the first line about two seconds. After that, every couple of seconds they decide again. Edit for that person.

## The scroll test (run it on every cut, out loud, in `REVIEW.md`)

Watch the frames second by second as that person, not as the editor. For each second write one line:

```
0.0–0.5  what I see: … | would I stop? yes/no, because …
0.5–2.0  what I now want to know: … | still here? …
2.0–…    is something new arriving before I get bored? …
end      do I get what I was promised? would I rewatch / share / comment?
```

Any "no" in the first 3 seconds is a P0. A stretch over ~3 s where nothing new arrives (new information, new image, new sound, a change in framing) is a P1. The critic runs this same test independently.

## The hook (0–3 s)

The hook is three layers at once; the strongest edits use all three in the first second:

1. **Visual hook (frame 1):** the first frame is the thumbnail and the stop. It must be the most interesting picture in the video, already in motion or mid-action, never a logo, a title card, a blank or a fade from black. Faces looking at the lens, a strange object, the result before the process, a big readable claim on screen.
2. **Spoken/written hook (0–2 s):** one line that opens a loop the viewer needs closed. Patterns that work (pick the one the content can actually pay off):
   - **Result first:** show the end state, then "here's how" (before/after, the finished dish, the final number).
   - **Specific claim:** a number or a fact that sounds wrong ("This board has 3,364 flaps and they all say the same thing").
   - **Pattern break:** something visually or sonically out of place in the feed (silence, a mechanical sound, an unexpected medium).
   - **Direct callout:** name the viewer's exact situation ("If your edits look like everyone's…").
   - **Mid-action start:** cut into the middle of the story, the context comes later.
   - **Stakes / conflict:** two things in tension; someone is wrong.
3. **Audio hook (0–1 s):** sound starts on frame 1. No silent first second, no slow music fade-in. A voice, a hit, a distinctive sound.

Never open with: a greeting, the person's name, "In this video…", an intro sting, a logo, context the viewer hasn't asked for yet. Those go later or nowhere.

**Write three hooks, keep one.** In `SPEC.md`, before building, write three different hook options (different patterns from the list above) and say which one you chose and why. For footage, the hook is usually a line from the middle of the recording, moved to the front.

## Holding them (3 s → end)

- **Open loops:** the hook opens a question; close it near the end, not right away. Open a smaller second loop before closing the first ("but that's not the weird part").
- **Re-hooks every 3–6 s:** something new arrives: new information, a new shot, a change of framing, a sound, a graphic that adds (not repeats) what is said. On a talking head this is the framing change, a B-roll insert, an on-screen word, a pattern interrupt.
- **Cut the run-up:** start every sentence as late as possible and leave as early as possible. If a line can go, it goes.
- **Shot shape, not a metronome:** fast runs then a hold (see `edit-doctrine.md`). A hold is a choice with a reason (a joke landing, a reveal), never dead air.
- **Payoff at 70–90% of the runtime,** then end fast. Don't keep going after the payoff; no outro, no "thanks for watching".
- **Loops (short-form):** the last frame/line can lead back into the first, so a replay feels continuous. Rewatches count.

## Length and density by platform

| Platform | Hook window | Re-hook every | Sweet spot |
| --- | --- | --- | --- |
| TikTok / Reels / Shorts | 0.5–1.5 s | 2–4 s | 15–45 s |
| YouTube long-form | 0–15 s (then the intro promise) | 20–40 s (a new chapter/loop) | as long as it stays dense |
| Ads | 0–1 s | 2–3 s | 6–30 s |
| Feed (LinkedIn/X/FB) | 0–2 s, works muted | 3–5 s | 20–60 s |

Assume sound off on feeds: the hook must work with captions and picture alone.

## Retention checklist before render

- [ ] Frame 1 is a stop-the-thumb image (not a title, logo, black, or fade).
- [ ] Sound on frame 1.
- [ ] The promise is clear by 2 s, muted.
- [ ] Nothing static for more than ~3 s without a reason written in SPEC.
- [ ] The payoff is delivered and the video ends within ~2 s after it.
- [ ] Scroll test written in REVIEW.md with no "no" in the first 3 s.
