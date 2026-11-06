---
name: house
description: Main-Edit's house layer on top of HyperFrames. Read it right after /hyperframes for ANY video made or edited in this repo (films, edits of real footage, captions, social cuts). Holds the anti-convergence rules, the look library, the taste ledger, the edit doctrine and the critic loop that keep our videos from looking like everyone else's Claude edit.
---

# House layer

`/hyperframes` gives the render contract and bans the obvious generated look. That is not enough, because **everyone running Claude with HyperFrames reads the same bans and lands on the same replacements**: per-word blur-ins at 0.13 s, whip transitions, `expo.out` on every arrival, a big condensed caps title on a flat bold colour, zoom-through-a-button. Those are the next generation of slop. This layer exists to make each film here specific to its subject and different from the last one.

Read `/hyperframes` first, always. This skill adds to it; where they conflict on craft, this skill wins; on the render contract, `/hyperframes` always wins.

## The four rules

1. **A look comes from a medium, and the medium comes from the subject.** Before anything visual, answer: *where in the real world would this message physically live?* A refund policy lives on a receipt. A launch date lives on a departure board. A recipe lives on a stained card. Pick the medium from `looks/` (`node tools/pick-look.mjs --brief "<one line>"`) or write a new one in the same format. The medium dictates palette, type, texture, **and how things move and transition**. No motion idea may come from outside the medium.
2. **No two films in a row share a fingerprint.** Every finished film is recorded in `taste/ledger.json` (`node tools/fingerprint.mjs <project> --record`). Before building, run `node tools/fingerprint.mjs <project>` on the draft: it fails on banned faces, a single-ease timeline, metronomic shot lengths, HyperFrames house signatures, and anything too close to a recent film.
3. **Edit like an editor, not a template.** Shot lengths vary on purpose, silence is used, the payoff is earned with a hold, sound does half the work. `references/edit-doctrine.md` has the numbers. Real footage: `/footage-edit`.
4. **Nobody grades their own homework.** After `check` and `snapshot --review`, hand the sheets to the `slop-critic` agent (`.claude/agents/slop-critic.md`) with only the brief, never your reasoning. Fix every P0 it returns. Then add every new tell it named to `taste/BANNED.md`, so the list grows with every film.

## Work order

1. Brief → one sentence: who watches, where (phone feed, TV, a landing page), what they do after.
2. `references/tells.md`: read it every time. It is short on purpose.
3. Medium → `node tools/pick-look.mjs --brief "..."`; read the chosen `looks/<id>.md` in full. If none fits the subject, write a new look file in the same shape before building, and say why.
4. `SPEC.md` per `/hyperframes` `references/spec.md`, with the look's numbers copied in, and the BANNED line = HyperFrames' list + `taste/BANNED.md` + the look's own "How this look fails".
5. Fonts: `node tools/fetch-font.mjs --project <dir> --family "<face>" --weights ...` and paste the printed `@font-face` rules.
6. Build. Scenes per `/hyperframes`. Motion per the look file. Rhythm per `references/edit-doctrine.md`.
7. `npx hyperframes check --json` → `node tools/fingerprint.mjs <dir>` → `npx hyperframes snapshot --review`.
8. `slop-critic` agent pass. Fix P0s, then P1s worth their time. Re-snapshot what changed.
9. Render. `node tools/fingerprint.mjs <dir> --record`. Write `REVIEW.md` per `/hyperframes`.

Projects live in `films/NNN-slug/`. Scaffold with `npx hyperframes init films/NNN-slug --skip-skills` (skills are vendored in `.claude/skills/`, pinned to the CLI version in `CLAUDE.md`).

## What to read

| Need | Read |
| --- | --- |
| Every film | `references/tells.md`, `references/edit-doctrine.md` |
| Choosing / writing a look | `looks/README.md`, then one `looks/<id>.md` |
| Real footage: talking head, vlog, podcast, interview, B-roll | `/footage-edit` |
| Copy on screen or in voiceover | `references/copy.md` |
| Review | `.claude/agents/slop-critic.md`, `taste/BANNED.md` |
