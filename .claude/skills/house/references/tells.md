# Tells of an AI edit (2026 edition)

HyperFrames' `spec.md` bans the first generation (dark void + glow, cream-paper-serif-mono-labels, fade-and-slide-up, three cards, docked logo). Read that list too. This list is the **second generation**: what models land on once the first list is banned. Each line names the tell, then what to do instead. Anything here is allowed only when the chosen look file explicitly asks for it.

## Picture

- **Text-only films.** Kinetic type of the whole script with no object, place, person or product on screen. → Every shot shows a *thing* from the subject's world; text labels the thing, it does not replace it.
- **The "bold" fallback.** Giant condensed caps (Anton, Bebas, League Gothic, Oswald, Archivo Black) on a flat saturated ground (orange, yellow, red, electric blue), maybe with a 4 px black border and a hard shadow. → Type and ground come from the look's medium.
- **The frame as a slide.** Every shot is a centred composition with even margins. → Use the frame: bleed off the edge, crop the hero at 120% of the frame, put the weight on a third, let something enter from outside.
- **Perfect vectors.** Everything razor-clean, flat, unaged. → The medium has a surface: toner noise, paper fibre, ink spread, misregistration, scan dust. Quantified in the look file, never more than it says.
- **Fake UI.** Browser chrome with three dots, an invented dashboard, a "terminal" with a blinking cursor. → Capture the real product (`npx hyperframes capture <url>`), or don't show UI.
- **Icon soup.** Emoji or line icons in rounded squares standing in for things. → Show the thing, or a pictogram drawn in the medium's own language.
- **Ticking counters, filling progress bars, checkmarks popping in.** → A number lands once, in its final state, with a physical cause (stamped, printed, flipped).
- **Gradient text, glitch/RGB-split, typewriter-with-cursor, spinning newspaper, lens dirt.** Banned outright.

## Motion (including HyperFrames' own house signature)

- **The HyperFrames entrance.** Per-word `blur(6px)` → 0 at 0.13 s, 0.067 s apart, on every title. It is good once; it is everyone's now. → The entrance is how the medium makes marks (printed, stamped, flipped, drafted, cut and placed).
- **One curve.** `expo.out` / `power4.out` on everything because the doctrine says "arrive slow". → Eases by role AND by medium; mechanical things are linear or stepped, hand-placed things settle with overshoot, light is eased both ways.
- **Smooth 30 fps on everything.** → Handmade media move on twos (12 fps, `steps()` or quantised time). Mechanical media snap. Only the camera and light are continuous.
- **The whip/zoom-through as glue.** Whips and zoom-throughs between every scene. → Transitions come from the medium (a page turns, a receipt tears, a flap falls, a sheet is exposed). Max one whip per film.
- **Everything animates.** Every element of a frame gets an entrance. → In each shot, decide what is *already there* (the world) and animate only what *arrives*.
- **Constant motion blur.** `data-motion-blur="on"` because it looks filmic. → Only where something moves fast enough to blur in the medium (camera, thrown paper).

## Edit

- **Metronome.** Every shot 2.5–3.5 s; scene lengths have a coefficient of variation under 0.25. → Vary on purpose: long establishing hold, a run of short shots, a hold before the payoff (`edit-doctrine.md`).
- **Music wall.** One track from 0 s to the end, ducked flat, fading out on the logo. → Start with sound or silence before music; drop the music out before the payoff; hit the payoff on a downbeat or on a cut to silence.
- **Sound effects as garnish.** A whoosh on every transition. → Sounds are the medium's own (copier hum, flap clatter, thermal printer chatter, paper tear). Every sound has a visible cause, not every visible cause gets a sound.
- **The ending card.** Logo + tagline + URL centred on a plain ground. → End on the last image of the story, with the brand living *inside* the medium (the receipt's header, the board's destination, the masthead).

## Captions (talking heads)

- **Hormozi-yellow.** Word-by-word pop, uppercase, one yellow word, emoji. → `/footage-edit` caption rules: phrase groups in the look's face, emphasis by weight or position, no emoji.
- **Captions dead centre on the face, on every clip.** → Captions follow the speaker's free space; they leave when a graphic says the same thing.

## Copy

See `copy.md`. The short version: no "Introducing", "Meet", "What if…", "Here's the thing", tricolon slogans ("Fast. Simple. Powerful."), "Ready to…?", "Let's dive in", "Stop X. Start Y.", or "game-changer".
