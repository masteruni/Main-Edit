---
id: xerox-zine
medium: a photocopied cut-and-paste zine, A5 pages on a light table
energy: high
suits: [manifesto, music, culture, punk, community, launch, opinion, art, fashion, protest, diy, creator, anti]
avoid: [finance, medical, enterprise, legal, luxury, calm]
faces: ["Anybody", "Courier Prime"]
---

## Parts

- **Ground**: photocopy paper, `#ECEBE6`, never pure white. The whole frame is paper; there is no "background" behind it.
- **Toner**: `#141414`. Every word, every photo, every rule. Photos are always toner: thresholded or coarse halftone, never full-tone.
- **Spot sticker**: fluorescent pink `#FF3D8B`, used **only** as a physical object stuck on the page (a dot sticker, a strip of tape, a highlighter stroke). One per shot, maximum.
- **Cut paper**: headlines and photos are separate pieces of paper with a 2 px toner edge where the scissors cut, laid at −4° to +4°.

## Numbers

- Headlines: Anybody, weight 900, width varies **per word** between 60 and 150 (`font-stretch: 60%`–`150%`) like letters cut from different magazines. Size 130–260 px at 1080p. Tracking −2%.
- Body / captions: Courier Prime 400/700, 34–44 px, typewritten, set ragged-left, never centred.
- Grid: none. Pieces overlap. One piece per shot is the hero and fills ≥ 55% of frame height.
- Photos: threshold 0.55 or halftone dots 9–14 px at 45°.

## Surface

- Toner noise: monochrome noise 6% on the paper, 0 on the black.
- Copier edge: a dark gradient 0→40 px at one random-but-seeded page edge (the lid wasn't shut), 35% opacity.
- Dust: 4–9 seeded toner specks per frame, 2–5 px, they **stay put** within a shot (it's the glass that's dirty) and change only on a new "copy".
- Misregistration of a re-copy: when a page is "copied again" the whole frame shifts 3–6 px and gets 4% darker.
- Never: blur, glow, soft shadows. The only shadow is a hard 3 px offset under a lifted cut piece at 30%.

## Motion

- Everything handmade moves **on twos**: quantise time to 12 fps (`gsap` ease `steps(n)` per tween or a `Math.floor(t*12)/12` sampler). Only the copier light bar is continuous.
- Pieces are **placed by hand**: enter from outside the frame along a short arc, overshoot by 2–4° of rotation, settle in 2 frames-on-twos. No fades. Ever.
- Text is **typed**: Courier lines appear one character per 1/24 s with no cursor.
- Tape goes on last, pressed: scale 1.04 → 1.0 in 2 steps.

## Transitions

- **The copy**: a white light bar (40 px, `#FFFFFF` at 90%) sweeps top→bottom in 0.33 s linear; behind it the frame is replaced by its next state. The cut happens under the bar.
- **The page flip**: the whole page (frame) lifts at one corner and slides off in 0.4 s on twos, revealing the next page already lying beneath.
- **Hard cut on a staple**: a staple sound + a 1-frame full-toner black frame.

## Sound

Copier start-up whirr + light-bar hum on "the copy"; scissors snip on cut pieces landing; tape tear; stapler. Music, if any: lo-fi drums or a single overdriven bass line, entering after the first copy.

## Voice

Short, blunt, first person. Lowercase body copy, CAPS only for the headline word that is cut out. Hand-lettered corrections allowed: a toner strike-through on a wrong word with the right one typed after it.

## How this look fails

- Becomes "grunge filter on a slide": textures applied on top of a normal centred layout. → The layout itself must be cut-and-paste.
- Too many rotated pieces at once: the frame turns to noise. → Max 3 pieces per shot, one hero.
- Pink everywhere. → One sticker per shot.
- Smooth 30 fps tweens. → On twos or it isn't paper.
