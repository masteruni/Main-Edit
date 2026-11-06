# The look library

Each file is a **medium**: a real-world thing that carries words and pictures, written as rules with numbers. A look is not a palette. It says what each part may carry, how marks get made (which is how things enter), and how the medium changes state (which is how scenes transition).

Pick with `node tools/pick-look.mjs --brief "<one line>"`. It scores looks on the brief's words against each file's `suits` / `avoid` tags and pushes down any look used in the last 3 films in `taste/ledger.json`. It proposes; you decide, and say why in `SPEC.md`.

None of these looks use the HyperFrames bundled faces or the faces generated design lands on (Inter, Space Grotesk, Instrument Serif, Geist, JetBrains Mono, Anton, Bebas). Fetch faces with `tools/fetch-font.mjs`.

| id | Medium | Energy | Good for |
| --- | --- | --- | --- |
| `xerox-zine` | Photocopied cut-and-paste zine | high | manifestos, culture, music, launches with attitude |
| `split-flap` | Mechanical departure board | mid | dates, launches, schedules, status, "now boarding" moments |
| `thermal-receipt` | Thermal printer receipt | mid | pricing, money, refunds, lists, product changes, orders |
| `wayfinding` | Transit / airport signage | mid | onboarding, how-to, directions, steps, navigation |
| `broadcast-94` | 1990s TV sports/news graphics | high | results, rankings, live, versus, overlays on footage |
| `tabloid` | Tabloid front page on newsprint | high | announcements, reveals, drama, news, testimonials |
| `cyanotype` | Sun-printed blueprint | low | engineering, architecture, process, how it's made |
| `paper-cutout` | Construction-paper stop motion | mid | kids, education, food, friendly explainers, stories |

## Writing a new look

When nothing fits the subject, write one before building. Copy this shape exactly:

```markdown
---
id: kebab-id
medium: one line, a physical thing
energy: low | mid | high
suits: [tags]
avoid: [tags]
faces: ["Display Face", "Body Face"]
---
## Parts         what each part of the medium may carry (ground, ink, accent, image, texture)
## Numbers       hex, face + weight + px at 1080p + tracking, grid, margins
## Surface       texture with amounts (%, px), and where it is NOT applied
## Motion        how marks are made = how things enter; frame rate (24/30 or on twos); eases
## Transitions   how the medium changes state; 2–4 kinds; one sentence of build each
## Sound         the medium's own sounds; what music (if any) fits
## Voice         how this medium phrases words
## How this look fails   its own slop risks, which go into the BANNED line
```

Good mediums are ones a viewer has touched: a vending machine, a bus ticket, a hymn board, a cake box, a ferry timetable, a lottery scratch card, a VHS spine, an exam paper, a seed packet. Avoid mediums that are already "design styles" (glassmorphism, bento grid, Y2K, vaporwave, brutalism): they arrive with their own clichés.
