# Client presets

One folder per client: `clients/<slug>/PROFILE.md` (from `_template/PROFILE.md`), plus optional `refs/` (reference notes, links, small stills) and `assets/` (logos, fonts, LUTs, intro/outro files the client supplies).

## The rule: ask first, every time

Before any new edit, Claude asks one question (AskUserQuestion):

> **Is this a general edit or for a client?**
> - **General edit (no preset)**: the default. Nothing loaded, nothing saved. Any reference you send applies to this video only.
> - **<each existing client>**: loads that client's profile.
> - **New client**: creates a profile from your answers, then uses it.

Skip the question only when the request already names a client or says "general".

## What a preset is, and is not

- A preset is **this client's taste**: platforms, formats, caption style, pacing, hook style, music, brand, do's and don'ts, deliverables. It is used only for that client's films.
- A **reference you send for a general edit is never saved**: not into a client, not into the house rules, not into a look file. It applies to that one film and is recorded only in that film's `SPEC.md`.
- A reference sent for a client goes into that client's `refs/` **only if you say so** ("save this to the client"). Otherwise it is for that one film too.
- A client profile is updated only from things you confirm: Claude proposes the change ("Client said captions too big → caption size 64 → 54 px. Save to profile?") and writes it when you say yes. Feedback history lives at the bottom of the profile.
- Client films may look like each other (that's the point of a preset), so `fingerprint.mjs` only compares a client film against *other* clients' and general films, never against the same client's. General films are still compared against everything recent so they don't converge.
- The house layer (no AI-slop tells, retention, edit craft) applies to client work too, unless the client's profile explicitly asks for one of the banned things. Then it's allowed for that client only, written in their profile with the reason.
