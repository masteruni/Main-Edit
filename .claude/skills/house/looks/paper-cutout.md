---
id: paper-cutout
medium: construction-paper cutouts animated stop-motion under a rostrum camera
energy: mid
suits: [kids, education, food, recipe, story, friendly, explainer, nonprofit, health, community, character, family, learning]
avoid: [enterprise, legal, finance, luxury, breaking]
faces: ["Lilita One", "Atkinson Hyperlegible"]
---

## Parts

- **Base sheet**: one flat construction-paper colour per scene, chosen from the set: tomato `#E2532D`, grass `#2E8A4E`, sunflower `#F2B632`, sky `#3D8BC9`, plum `#7B3F72`, oat `#E7D9BD`. Never a gradient, never two bases at once.
- **Pieces**: every object is cut paper in 2–5 layers of the same set, with visible scissor-cut edges (slightly irregular polygons, not perfect curves).
- **Ink**: words are cut letters (Lilita One) in one paper colour, or written with a thick black marker `#1B1B1B` (Atkinson Hyperlegible 700 stands in for print where reading matters).
- **Real hand**: optional. A real photographed hand placing a piece (from footage) once per film is the strongest move this look has.

## Numbers

- Display: Lilita One 400, 120–220 px. Body / labels: Atkinson Hyperlegible 700, 40–52 px.
- Paper layers: each layer casts a hard-ish shadow: offset 0/5 px, blur 3 px, 30% black. Lifted pieces (in motion) cast 0/14 px, blur 10 px, 22%.
- Objects are big and simple: the hero object ≥ 50% of the frame height, made of ≤ 7 pieces.

## Surface

- Paper fibre noise 5% per piece, with a seeded offset per piece so pieces don't share a texture. A slight white fuzz on cut edges (1 px at 30%).
- The rostrum light: a very soft vignette 8%, and frame-to-frame exposure flicker ±1.5% (seeded, on twos).

## Motion

- **On twos** (12 fps), always: quantise every tween. Movement is a sequence of placed poses.
- Pieces **slide on the table** (they never fly in from nowhere): enter from the frame edge, ease-out with a 1-pose overshoot.
- Squash/stretch is replaced by **replacement**: a mouth opening is a different paper cutout swapped in, not a scaled one.
- Characters: limbs pivot on paper-fastener joints (a 6 px brass dot visible at the joint).

## Transitions

- **Paper pull**: the base sheet is pulled off the table to one side (0.5 s on twos), revealing the next colour sheet underneath with its pieces already placed.
- **Cover with a piece**: a large foreground piece (a leaf, a cloud, a hand) passes across the camera and the scene changes behind it.
- **Iris of paper**: a cut circle grows from a piece on screen (a plate, a sun) to fill the frame.

## Sound

Paper slides and rustles, a pencil scratch for marker writing, small foley for every placed piece (a soft "tak"). Music: ukulele, marimba, or simple hand percussion. Sound is crucial; this look is dead silent without foley.

## Voice

Warm, direct, second person, short sentences. Numbers written as words when small. Never cute baby-talk.

## How this look fails

- Vector flat illustration with a paper texture overlay. → Pieces with cut edges, layered, with shadows.
- Smooth 30 fps tweening. → On twos, always.
- Too many colours in one frame. → Base + up to 3 piece colours.
