---
id: cyanotype
medium: a sun-printed cyanotype blueprint sheet, pinned to a drafting board
energy: low
suits: [engineering, architecture, process, how-it-works, infrastructure, hardware, build, craft, science, design, technical, explainer, history]
avoid: [party, kids, sale, food]
faces: ["Chivo Mono", "Chivo"]
---

## Parts

- **Sheet**: Prussian blue `#1F3F7A`, uneven: a large, soft radial variance of ±6% across the sheet (the coating was brushed on) and brush-stroke edges where the coating stops, revealing raw paper `#E8E6DE` at the sheet border.
- **Lines**: exposed white `#F1F4F8` at 92%, never pure, with a slight bloom of 0.8 px (sun-print edges are soft, not glowing).
- **Annotation**: graphite pencil `#4A4A48` on the raw-paper border only (title block, scale, date), never on the blue.
- **Objects**: drawn as orthographic projections and sections (front / side / plan), with dimension lines and leaders. Photos, when used, are exposed as cyanotype (photo inverted to blue/white via media-treatment, no full colour).

## Numbers

- Labels: Chivo Mono 400, 30 px caps, tracking +6%. Titles: Chivo 300 (light), 96–140 px, tracking −1%, sitting in the drawing like a draughtsman's title, left-aligned.
- Line weights: object 4 px, hidden lines 2 px dashed 10/6, dimension 1.5 px with 12 px arrowheads.
- The drawing is big: the object fills 60–80% of the frame; the camera visits details at 300%.

## Surface

- Paper fibre 4% across everything. Seeded pin holes at the corners. A coffee ring is allowed once in a film, at 10%.
- Exposure falloff: lines at the sheet edges are 10% weaker.

## Motion

- Lines are **drafted**: `stroke-dashoffset` at a constant pen speed (900–1400 px/s), linear, in the order a draughtsman would draw (outline, then details, then dimensions, then labels).
- Dimension numbers appear when their line completes (no fade: they're exposed, 2-frame 0 → 100%).
- Camera: slow pans along the drawing (linear 60 px/s) and decisive moves between details (0.7 s `power2.inOut`). Never rotates.

## Transitions

- **Exposure**: the next sheet is exposed: white floods from a sunlit side, 0.6 s, then washes to blue as the new drawing appears (a light-leak gradient, not a fade).
- **Section cut**: a dashed section line crosses the object; the view swings to the section along that line.
- **Pull back to the board**: the camera pulls back to show the sheet pinned on a drafting board, then a new sheet is pinned over it.

## Sound

Pencil scratch while drafting, a ruler set down, paper pinned. Room tone of a quiet studio. Music: a sparse piano or a slow cello line, or nothing.

## Voice

Annotated, precise: `SECTION A–A`, `SCALE 1:20`, `NOT TO SCALE`, measurements with units. The narrative lives in the title block and in callouts with leaders.

## How this look fails

- "Blue tech grid with glowing lines" = the generated HUD look. → No glow, no grid, no HUD; it's a sun print with brush edges.
- Drawing everything simultaneously. → One pen, drawing in order.
- Tiny drawing in the middle. → Fill the sheet, crop into details.
