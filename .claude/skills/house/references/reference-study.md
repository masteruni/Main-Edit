# Studying a reference (mandatory for every reference the person sends)

A reference is studied, not glanced at. Before any edit that has a reference, write `films/<film>/REFERENCE.md` with every section below filled from measurements. Mark each item **measured** or **guessed**. The person's standing instruction: study the font, the caption animation and the text effects "very clearly and specifically".

Scope: a reference sent for a general edit applies to that film only (never to house rules, looks or clients). A reference saved to a client goes in `clients/<slug>/refs/` with its REFERENCE.md.

## 1. Extract

```bash
ffprobe ref.mp4                                   # size, fps, duration, audio
npx hyperframes transcribe ref.mp4 --model small.en --json   # words + timings (non-English: see /footage-edit)
# every frame of a caption event, numbered, at the ref's own fps:
ffmpeg -ss <t> -t 1.6 -i ref.mp4 -vf "scale=480:-2,drawtext=text='%{n} %{pts\:hms}':x=4:y=4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.7,tile=6x7" -frames:v 1 anim.jpg
# full-res crops of the type for font ID:
ffmpeg -ss <t> -i ref.mp4 -frames:v 1 -vf "crop=W:H:X:Y,scale=2*W:-2" type.png
```

Do this for at least: the first caption, one caption over talking head, one over B-roll, one transition, the last caption.

## 2. Identify the fonts (measured, by side-by-side rendering)

- Render the reference's actual words in 6–10 candidate faces (Google Fonts and the common CapCut/Premiere defaults) on a Playwright page; screenshot; compare letterforms against the crops: capitals' loops, `g`/`y` tails, `t` and `M` shapes, stroke contrast, slant, x-height.
- Usual suspects for this genre: sans → Montserrat, Poppins, Inter, Gilroy-like (use Outfit/Plus Jakarta), Bebas/Anton for caps; script → Parisienne, Great Vibes, Pinyon Script, Allura, Alex Brush, Mrs Saint Delafield; serif italic → Playfair Display Italic, Cormorant Italic, Bodoni Moda Italic.
- Record: family, weight, case (lowercase / Title / CAPS), tracking, size as % of frame height for each role (hero word, small connector word, script word), line spacing / overlap between stacked lines.

## 3. Measure the caption animation (frame by frame)

For each word role, count frames:
- **Entrance**: cut-on / fade (n frames) / wipe direction (n frames) / scale from % / blur from px / slide px and direction / per-letter vs per-word.
- **Sync**: does each word land on its spoken onset (± frames), on the beat, or both?
- **Accumulation**: do words stack into a block? Alignment (left/right/staircase), which words go where, does the block move when a word is added?
- **Hold & exit**: held still? Exit on the cut, fade (n frames), or replaced in place?
- **Per-shot layout**: where blocks sit relative to the subject (beside the head, negative space, split across the frame), never over the face?

## 4. Text effects

Colour (white? warm white? tinted to the scene: sample the hex from the plate), adaptive dark text over bright plates, shadow (offset, blur, opacity), glow (colour, radius), outline, blend mode, gradient, opacity of secondary words, motion blur.

## 5. Picture & edit grammar

Shot lengths (list them), cut points (on word / on beat / on action), transitions (each kind + frame count: light leak, whip, zoom blur, flash, B&W→colour), speed ramps, grade (shadows/highlights tint, saturation, contrast), aspect ratio and framing, first frame / hook, sound (music genre, VO style, SFX, ducking).

## 6. Translate

End REFERENCE.md with a short "Apply to this film" list: what we copy exactly (fonts, animation timings, effects), what we adapt (and why), and what we deliberately don't take (anything in taste/BANNED.md unless the person's reference explicitly uses it, then it's allowed for this film only).
