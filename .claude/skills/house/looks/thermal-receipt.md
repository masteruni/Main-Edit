---
id: thermal-receipt
medium: a thermal-printed shop receipt, curling, on a laminate counter
energy: mid
suits: [pricing, price, money, refund, order, checkout, subscription, cost, savings, list, changelog, invoice, fintech, ecommerce, shopping, budget]
avoid: [luxury, music, cinematic, nature]
faces: ["Fragment Mono"]
---

## Parts

- **Counter**: laminate `#B9B3A8` with a fine 1 px speckle pattern at 8%. It is always visible at the frame edges; the receipt is an object on it.
- **Paper**: thermal paper `#F7F6F2`, 80 mm wide, i.e. a strip ~620 px wide in a 1920 frame, ~880 px in a 1080-wide vertical. Edges slightly irregular (±1 px seeded). It curls: a 6% darker gradient on the last 30 px of each side.
- **Thermal ink**: `#2A2A2C`, never pure black; prints 3–6% lighter on the right edge (the head is worn).
- **Accent**: none in the ink. The only colour is a **highlighter stroke** `#FFE45C` at 70% multiply, or a red ballpoint circle `#C8202A`, added by a hand after printing. One per shot.

## Numbers

- Fragment Mono 400 throughout. Line items 30 px, totals 44 px with letter-spacing 0.06em, header (store name) 52 px caps, double-height = `transform: scaleY(2)` like a real printer.
- 32 characters per line at item size. Left item, right price, dotted leader. Dashed separators `- - - -`.
- Camera: the receipt is never fully visible in hero shots. Crop to 5–8 lines.

## Surface

- Paper fibre noise 3%. Faint fold line across the strip at one seeded position, 1 px at 12%.
- Shadow of the curled paper on the counter: 10 px blur, 18% black, offset 0/6 px. The only soft shadow allowed.

## Motion

- **Printing**: the strip feeds upward out of the frame bottom at a constant **linear** speed (28 lines/s for a fast printer, 9 lines/s for drama). Each line appears printed at the head position (a fixed line near the frame bottom), never anywhere else.
- Things on the paper never animate after they are printed.
- The hand: highlighter strokes draw left→right in 0.25 s `power1.inOut` with a 1-frame jitter; the pen circle draws in 0.4 s and over-shoots its start by 15°.

## Transitions

- **Tear**: the strip is torn off against the cutter: a 0.15 s jerk upward of 40 px with a zigzag edge, then the next receipt starts printing.
- **Slide across the counter**: the receipt is pushed out of frame (0.45 s `power3.in`), revealing the next object already on the counter.
- **Feed-through**: keep printing; the next "scene" is just the next section of the same receipt (a new dashed header).

## Sound

Thermal printer chatter (a tight buzzy rattle) while lines print; the cutter tear; a cash-drawer clunk for the payoff; shop room tone. Music: none; this look is funnier dry.

## Voice

Receipt language: `QTY`, `SUBTOTAL`, `DISCOUNT`, `TOTAL`, `CHANGE DUE`, `THANK YOU FOR SHOPPING`. Put the real message in the line items (`1 x  SLEEP  ......  $0.00`). The payoff is a total.

## How this look fails

- A receipt floating in a void, centred, fully visible. → On a counter, cropped, at an angle of −2° to 3°.
- Lines fading in. → They print at the head, in order, linear.
- Unreadable 20 px type at phone size. → Fewer items, bigger type, crop tighter.
