---
id: wayfinding
medium: transit and airport wayfinding signage, panels mounted along a concourse
energy: mid
suits: [onboarding, howto, tutorial, steps, directions, navigation, setup, guide, process, explainer, help, saas, getting-started]
avoid: [music, fashion, romance, horror]
faces: ["Overpass"]
---

## Parts

- **Panels**: flat enamel sign panels, `#14213D` (dark signal blue) with `#FFFFFF` legend, rounded 14 px corners. Each panel is an object, mounted: a 2 px darker frame and two visible bolts (6 px circles, `#9AA0A6`).
- **Concourse**: the world the panels hang in: a light concrete wall `#C9C6BF`, a ceiling line, floor tiles `#A7A39A` in perspective in wide shots. The panel never floats on a flat colour.
- **Signal yellow** `#FFCC00` (black legend): **one** panel per shot, for the instruction that matters.
- **Pictograms**: ISO-7001-style figures, drawn as solid shapes with 10 px stroke-free geometry, never line icons.
- **Arrows**: the solid wayfinding arrow (stem width = 1/3 head width). An arrow always points to where the camera goes next.

## Numbers

- Legend: Overpass 800, cap height ≥ 7% of frame height on hero panels; secondary 600 at 3.2%. Tracking 0. Left-aligned on the panel with the arrow leading.
- Panel padding = 0.6 × cap height. Panels 3:1 to 5:1 wide.
- Step numbers: inside a white circle on the panel, as the system does it (`1` `2` `3` platform-style), never as "01 / 02" labels.

## Surface

- Enamel: 2% noise, a soft specular band (white 6% → 0, 120 px wide, diagonal) that moves **only** when the camera moves.
- Concrete: 5% noise, a seeded water stain or two. Ceiling light pools on the wall (radial, 12%).

## Motion

- The **camera walks**. The film is one continuous track along the concourse: linear lateral pans at walking pace (240–320 px/s at 1080p), with a 0.3 s ease into and out of each stop at a panel. Parallax: wall 1.0, panels 1.08, foreground pillar 1.6.
- Panels don't animate; the camera discovers them. A legend can **switch** (LED-style panel) with a 2-frame black blink.
- Arrows lead: before a pan, the arrow on screen is the only thing that changes (it brightens 100 → 115% for 3 frames).

## Transitions

- **Follow the arrow**: the camera pans in the direction the arrow points; the next panel is the next scene.
- **Through the gate**: push forward through a doorway / turnstile gap; the gate frame passes the lens (0.5 s `power2.in` then cut).
- **Escalator down**: the frame tilts down 0.6 s and comes up on a new level (a new colour wall = new chapter).

## Sound

Concourse ambience (distant footsteps, a big room), footstep rhythm locked to the pan speed, a soft two-tone chime on yellow panels. Music: optional, a calm pulse at walking tempo (100–112 BPM).

## Voice

Imperative and short: `Exit B → Settings`, `Change here for API keys`, `Mind the gap: save before you leave`. One instruction per panel.

## How this look fails

- Panels as flat UI cards on a coloured background. → They are mounted in a place.
- Every panel yellow. → Yellow is for the one thing.
- Icon soup. → Pictograms only where a real station would put one.
