# Main-Edit

An AI video editing studio built on [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4), with a house layer whose only job is to make our videos **not look like everyone else's Claude edit**.

## Who this is for

The person is a freelance video editor with several clients. Most jobs are **general edits**. Think like their senior editor: every cut must not look like generic AI video, and must keep a scrolling stranger watching (hook in the first second, re-hooks every few seconds, payoff, end fast).

## Before any video work

0. **Ask: general edit or client?** (AskUserQuestion; "General edit (no preset)" first, then each client in `clients/`, then "New client".) Skip only if the request already says. General = no preset, nothing saved; a reference they send applies to that one video only and never becomes a default anywhere. Client = load `clients/<slug>/PROFILE.md`. See `clients/README.md`.
1. Invoke `/hyperframes`: the render contract and work loop. Non-negotiable.
2. Invoke `/house`: our looks, anti-convergence rules, edit doctrine, critic loop.
3. Real footage involved → also `/footage-edit`.
4. Read `taste/BANNED.md`. Every film's `SPEC.md` BANNED line includes it.

## Layout

| Path | What |
| --- | --- |
| `films/NNN-slug/` | One HyperFrames project per film. `SPEC.md`, `REVIEW.md`, `house.json` (look id + any deliberate rule allowances) live in it. |
| `.claude/skills/hyperframes*`, `media-use` | Official HyperFrames skills, vendored and pinned to CLI **0.9.19** (`HYPERFRAMES-LICENSE`, Apache-2.0). Don't edit; update all together with the CLI version. |
| `.claude/skills/house/` | House layer: `SKILL.md`, `looks/` (one medium per file), `references/` (tells, edit doctrine, copy). |
| `.claude/skills/footage-edit/` | Editor's judgment for real footage. |
| `.claude/agents/slop-critic.md` | Fresh-eyes reviewer. Give it the project + brief only. |
| `tools/` | `pick-look.mjs`, `fingerprint.mjs`, `fetch-font.mjs`, `edit-plan.mjs`. |
| `taste/` | `BANNED.md` (grows every film) and `ledger.json` (fingerprints of delivered films). |
| `clients/<slug>/` | Per-client preset: `PROFILE.md`, `refs/`, `assets/`. Updated only with the person's confirmation. |

## Commands

```bash
npx hyperframes@0.9.19 init films/NNN-slug --skip-skills   # new film (skills are already vendored)
node tools/pick-look.mjs --brief "<one line>"               # propose a medium
node tools/fetch-font.mjs --project films/NNN-slug --family "Face" --weights 400,700
npx hyperframes check --json                                # in the film dir
node tools/fingerprint.mjs films/NNN-slug                   # house lint + similarity to recent films
npx hyperframes snapshot --review                           # in the film dir; then run the slop-critic agent
npx hyperframes render -o renders/<name>.mp4                # in the film dir
node tools/fingerprint.mjs films/NNN-slug --record          # after delivery
```

Pin the CLI as `npx hyperframes@0.9.19` in scripts so it matches the vendored skills.

## Rules of the house

- A film is not done until `check` is clean, `fingerprint.mjs` passes, the critic's P0s are fixed, new tells are appended to `taste/BANNED.md`, and the film is recorded in the ledger.
- Commit `films/*/` source and `REVIEW.md`; commit renders only when small (< 8 MB). Large source footage stays out of git (see `.gitignore`).
- Never claim to have heard audio. Say it was measured.
