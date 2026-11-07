#!/usr/bin/env python3
"""v4 composition. Captions follow REFERENCE.md "ref3" (the person's chosen typography):
- Inter Black, -4% tracking, centred at 56% height; words appear on their spoken onsets (VO transcripts);
- single words replace each other; a small connector stacks over its big key word; key words lowercase with end punctuation;
- every word blurs in (12 px -> 0) with a 108 -> 100% settle over 4 frames; hard exits; soft drop shadow;
- 2 key words overlay-blended into the plate.
Plus: light-leak streak transitions (ref1), the drop flash + punch, slow pushes on held shots.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cutlist import SHOTS, VO, END, DROP, LEAKS, b  # noqa: E402

SMALL = {"is", "the", "a", "in", "an", "for", "my", "to", "and", "of", "i've", "if", "you're", "we're", "about", "what", "this", "are", "like", "your", "had", "ever", "now"}

# Shot clips are written with data-start 0.5 ms early at 4 decimals: a cut at 13.0667 s rounded to "13.067" would start
# after its frame (392/30 = 13.06667) and the outgoing shot would hold one extra frame.
# ref3 captions (v5), grouping measured against the reference:
# - a unit is 1-3 consecutive spoken words that stays on screen >= MIN_HOLD (the ref never flashes a word for < ~0.4 s);
# - in a multi-word unit the key word is big and the others are small, stacked LEFT-aligned on top of it, tight;
# - key words: the KEY set, else the longest word of the unit; end punctuation kept on keys; KEEP_CAPS words in caps.
MIN_HOLD = 0.36
GROUPS = {"V2": [4, 2]}
MAXW = {"V1": 6, "V2": 6, "V3a": 8, "V3b": 3, "V4": 16, "V5": 7, "V6": 7, "V7": 7}   # words each line's audio really carries
KEY = {"dreams", "impossible", "video", "most", "honest", "really", "you", "$1,000", "monthly", "fighting", "uphill", "battle", "honest", "conversation",
       "changed", "life", "million", "dollars", "valuations", "up", "launching", "company", "lock", "boys", "go"}
KEEP_CAPS = {"million", "monthly"}
BLEND = {"battle"}
SMALL_WORDS = {"a", "an", "the", "is", "in", "of", "to", "for", "my", "and", "if", "you're", "we're", "i've", "this", "that",
               "are", "like", "your", "had", "ever", "now", "about", "what", "really", "let's", "most", "under", "another", "software"}
TOP = {"V2": 1240, "V3a": 1330, "V3b": 1330, "V4": 1240, "V7": 720}  # block centre y; default 1000 (52%); faces kept clear
PUNCH = [(DROP, 1.14)]
PUSH = {16: 1.07, 21: 1.05, 2: 1.04}


def vo_words(key, f, a, z, place):
    w = json.load(open(os.path.join(FILM, "assets/vo-candidates", f + ".json")))
    w = w if isinstance(w, list) else w["words"]
    out = []
    for x in w:
        if x["start"] >= a - 0.05 and x["start"] < z - 0.05 and not re.match(r"^[♪\[\(]", x["text"]):
            out.append((x["text"], round(place + max(0, x["start"] - a), 3)))
    return out


def word_html(text, role, size, wid):
    return f'<span id="{wid}" class="{role}" style="font-size:{size}px">{text}</span>'


def html():
    cams, caps, tl = [], [], []
    for i, (st, en, *_r) in enumerate(SHOTS):
        cams.append(f'      <div class="cam" id="cam{i:02d}" style="z-index:{i + 1}"><video id="v{i:02d}" class="clip" '
                    f'src="assets/shots/{i:02d}.mp4" muted playsinline data-start="{st - 0.0005:.4f}" data-duration="{en - st:.4f}" '
                    f'data-track-index="0"></video></div>')
        punched = any(abs(st - t) < 1e-3 for t, _ in PUNCH)
        if i in PUSH and not punched:
            tl.append(f'tl.fromTo("#cam{i:02d}", {{scale: 1}}, {{scale: {PUSH[i]}, duration: {en - st:.3f}, ease: "sine.inOut"}}, {st:.3f});')
        if punched:
            sc = next(s for t, s in PUNCH if abs(st - t) < 1e-3)
            tl.append(f'tl.fromTo("#cam{i:02d}", {{scale: {sc}}}, {{scale: 1, duration: 0.3, ease: "power3.out", immediateRender: false}}, {st:.3f});')

    g = 0
    for key, f, a, z, place in VO:
        words = vo_words(key, f, a, z, place)
        later = [v[4] for v in VO if v[4] > place]
        end_line = min(place + (z - a) + 0.25, (min(later) - 0.02) if later else END)
        words = words[: MAXW.get(key, len(words))]
        core = lambda i: re.sub(r"[^a-z0-9$,']", "", words[i][0].lower()).strip(",")
        keyish = lambda i: core(i) in KEY or core(i) not in SMALL_WORDS
        # units close ON a key word (small words lead into it, like "Stay / humble."), hold >= MIN_HOLD, max 3 words
        units, cur = [], []
        for i in range(len(words)):
            cur.append(i)
            nxt_at = words[i + 1][1] if i + 1 < len(words) else end_line
            hold = nxt_at - words[cur[0]][1]
            if i + 1 == len(words) or (keyish(i) and hold >= MIN_HOLD) or (len(cur) >= 3 and any(keyish(j) for j in cur)) or len(cur) == 4:
                units.append(cur); cur = []
        if cur:
            units.append(cur)
        if key in GROUPS:  # hand-set phrasing for a line
            sizes, units, n = GROUPS[key], [], 0
            for k in sizes:
                units.append(list(range(n, n + k))); n += k
        # a unit that still holds < MIN_HOLD joins the previous one (never flash a word)
        merged = []
        for u in units:
            nxt = units[units.index(u) + 1][0] if units.index(u) + 1 < len(units) else None
            hold = (words[nxt][1] if nxt is not None else end_line) - words[u[0]][1]
            if merged and hold < MIN_HOLD and len(merged[-1]) + len(u) <= 4:
                merged[-1] = merged[-1] + u
            else:
                merged.append(u)
        units = merged
        for ui, unit in enumerate(units):
            u_start = max(0.0, words[unit[0]][1] - 0.02)
            u_end = min((words[units[ui + 1][0]][1] - 0.02) if ui + 1 < len(units) else end_line, END)
            cores = [re.sub(r"[^a-z0-9$,']", "", words[i][0].lower()).strip(",") for i in unit]
            keyed = [i for i, c in zip(unit, cores) if c in KEY] or [i for i, c in zip(unit, cores) if c not in SMALL_WORDS]
            k_i = keyed[-1] if keyed else max(unit, key=lambda i: (len(cores[unit.index(i)]), i))
            spans = []
            for i, core in zip(unit, cores):
                raw, at = words[i]
                text = re.sub(r",$", "", raw)
                if core in KEEP_CAPS:
                    text = text.upper()
                elif i == k_i:
                    text = text if text.startswith(("I", "$")) else text.lower()
                is_key = (i == k_i)
                if is_key:
                    size = int(max(104, min(168, 580 / (0.56 * max(3, len(text))))))
                    cls = "key blend" if core.strip(".?!") in BLEND else "key"
                else:
                    size, cls = (64 if len(unit) > 1 else 84), "conn"
                wid = f"w{g}_{i}"
                spans.append(f'<span id="{wid}" class="{cls}" style="font-size:{size}px">{text}</span>')
                tl.append(f'tl.fromTo("#{wid}", {{opacity: 0, filter: "blur(10px)"}}, {{opacity: 1, filter: "blur(0px)", duration: 0.125, ease: "power2.out", immediateRender: false}}, {at:.3f});')
                if at > u_start + 0.03:
                    tl.append(f'tl.set("#{wid}", {{opacity: 0}}, {u_start:.3f});')
            # small words that come before the key share one line above it; small words after it share one line below
            k_pos = unit.index(k_i)
            before, after = spans[:k_pos], spans[k_pos + 1:]
            spans = ([f'<div class="row">{"".join(before)}</div>'] if before else []) + [spans[k_pos]] + \
                    ([f'<div class="row after">{"".join(after)}</div>'] if after else [])
            top = TOP.get(key, 1000)
            caps.append(f'      <div id="cap{g}" class="clip cap" style="top:{top}px" data-start="{u_start:.3f}" '
                        f'data-duration="{max(0.12, u_end - u_start):.3f}" data-track-index="1"><div class="stack">{"".join(spans)}</div></div>')
            g += 1

    for k, t in enumerate(LEAKS):
        caps.append(f'      <div id="leak{k}" class="clip leak" data-start="{t - 0.05:.3f}" data-duration="0.17" data-track-index="2"><i></i></div>')
        tl.append(f'tl.fromTo("#leak{k} i", {{xPercent: -60, opacity: 0.95}}, {{xPercent: 40, opacity: 0, duration: 0.16, ease: "power1.in"}}, {t - 0.05:.3f});')
    caps.append(f'      <div id="flash0" class="clip flash" data-start="{DROP:.3f}" data-duration="0.2" data-track-index="2"><i></i></div>')
    tl.append(f'tl.fromTo("#flash0 i", {{opacity: 0.85}}, {{opacity: 0, duration: 0.18, ease: "power2.out"}}, {DROP:.3f});')

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; font-style: normal; font-weight: 900; font-display: block; src: url("assets/fonts/inter-900.woff2") format("woff2"); }}
      :root {{ --ink: #f5f1ea; --gold: #f3c76b; --navy: #1b2440; --sans: "Inter", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #070708; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .cam {{ position: absolute; inset: 0; overflow: hidden; }}
      .cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .cap {{ position: absolute; left: 0; right: 0; z-index: 100; display: flex; justify-content: center;
              transform: translateY(-50%); color: #fff; font-family: var(--sans); font-weight: 900; letter-spacing: -0.045em; }}
      .cap .stack {{ display: flex; flex-direction: column; align-items: flex-start; }}
      .cap span {{ display: block; line-height: 0.86; white-space: nowrap;
                   text-shadow: 0 3px 2px rgba(0,0,0,.30), 0 4px 12px rgba(0,0,0,.42); }}
      .cap .row {{ display: flex; gap: 0.22em; margin: 0 0 -0.02em 0.06em; font-size: 64px; }}
      .cap .row.after {{ margin: 0.02em 0 0 0.06em; }}
      .cap .key.blend {{ mix-blend-mode: overlay; text-shadow: none; }}
      .leak {{ position: absolute; inset: 0; z-index: 150; pointer-events: none; overflow: hidden; mix-blend-mode: screen; }}
      .leak i {{ position: absolute; left: -40%; top: -20%; width: 180%; height: 140%; opacity: 0;
                 background: repeating-linear-gradient(72deg, rgba(255,120,40,0) 0 40px, rgba(255,140,60,.85) 60px, rgba(80,220,255,.7) 90px, rgba(255,60,140,.6) 120px, rgba(255,255,255,0) 170px); filter: blur(6px); }}
      .flash {{ position: absolute; inset: 0; z-index: 200; pointer-events: none; }}
      .flash i {{ position: absolute; inset: 0; background: #fffaf0; opacity: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END:.3f}" data-width="1080" data-height="1920">
{chr(10).join(cams)}
{chr(10).join(caps)}
      <audio id="soundtrack" class="clip" src="assets/audio/soundtrack.m4a" data-start="0" data-duration="{END:.3f}" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + '      ').join(tl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


open(os.path.join(FILM, "index.html"), "w").write(html())
print("wrote index.html", len(SHOTS), "shots", f"{END:.3f}s")
