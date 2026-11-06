# Main-Edit

AI video editing with Claude Code, built so the results **don't look like everyone else's AI edit**.

The engine is [HyperFrames](https://github.com/heygen-com/hyperframes) (open source, from HeyGen): a video is an HTML page, rendered frame by frame into an MP4 by a headless browser + FFmpeg. Claude writes and edits that HTML. You describe the video; Claude builds, checks, reviews and renders it.

## Why another layer

HyperFrames already bans the first wave of AI-video clichés (dark void + glow, cream paper + serif, everything fading and sliding up). But everyone using Claude + HyperFrames reads the same bans and lands on the **same replacements**: per-word blur-in titles, whip transitions, big condensed caps on a flat bright colour, zoom-through-a-button. That's the next wave of slop. This repo adds:

| Piece | What it does |
| --- | --- |
| **Look library** (`.claude/skills/house/looks/`) | Looks built from real **mediums** (departure board, thermal receipt, photocopied zine, tabloid, blueprint, transit signage, 90s broadcast, paper cut-outs), each with exact numbers for colour, type, texture, *and how things move and transition*. The medium is chosen from the subject, so every film looks like its subject, not like "AI video". |
| **Anti-convergence ledger** (`tools/fingerprint.mjs`, `taste/ledger.json`) | Fingerprints every film (faces, palette, easing, shot rhythm) and fails a new film that is too close to a recent one, uses a default face, runs on one easing curve, or cuts like a metronome. |
| **Growing ban list** (`taste/BANNED.md`) | Every film's review adds the new clichés it caught. The list only gets longer. |
| **Edit doctrine** (`.claude/skills/house/references/`) | Shot-length shapes, cut-on-action/sound, sound design before music, copy rules that ban "Introducing…" & friends. |
| **Footage editing** (`.claude/skills/footage-edit/`, `tools/edit-plan.mjs`) | For real video: paper edit first, cut fillers but **keep breath**, framing changes that hide jump cuts (never zoom-on-every-cut), captions without the yellow-word-pop look, non-literal B-roll. |
| **Retention** (`.claude/skills/house/references/retention.md`) | Three hook options per video, sound and picture hook on frame 1, re-hooks every 3–6 s, payoff then end. A second-by-second "would I scroll?" test is written into every REVIEW.md. |
| **Client presets** (`clients/`) | Every edit starts with one question: general edit (no preset, nothing saved) or which client. Client taste lives in `clients/<slug>/PROFILE.md`, updated only when you confirm. References never leak into other videos. |
| **Fresh-eyes critic** (`.claude/agents/slop-critic.md`) | A separate agent that reviews the frames without seeing the author's reasoning, and names every generated-video tell. |

## Using it

Open this repo in Claude Code and ask for a video. Examples:

- "Make a 20 s vertical clip announcing our price change from $12 to $9."
- "Here's my talking-head recording (link). Cut it to 45 s for Reels with captions."
- "Make a launch film for <url>."

Claude follows `CLAUDE.md`: `/hyperframes` → `/house` → (footage → `/footage-edit`) → SPEC → build → check → fingerprint → critic → render.

**Sharing footage:** big video files don't belong in git. Share a link (Google Drive works in this session) or drop small files into `films/<film>/assets/`.

## Films

| # | Film | Look | Notes |
| --- | --- | --- | --- |
| 001 | [Same Look](films/001-same-look/) ([mp4](films/001-same-look/renders/final.mp4)) | split-flap | Every cliché departs to SAME LOOK via AI EDIT; one train goes SOMEWHERE ELSE. Picture and sound come from one flap schedule. |

## Requirements

Node 22+, FFmpeg, Chrome/Chromium. Python 3 + numpy for films that synthesise their own sound. Check with `npx hyperframes@0.9.19 doctor`.

HyperFrames skills in `.claude/skills/hyperframes*` and `media-use` are © HeyGen, Apache-2.0 (`.claude/skills/HYPERFRAMES-LICENSE`), vendored unmodified at v0.9.19.
