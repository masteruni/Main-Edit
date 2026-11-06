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

# ref3 caption units per VO line: lists of (word index, role). role: "" single word (replaces the previous),
# "c" small connector stacked over the key, "k" key word (+ "." / "?" adds end punctuation, "C" caps, "b" overlay-blend).
UNITS = {
    "V1": [[(0, "")], [(1, "")], [(2, "c"), (3, "k")], [(4, "")], [(5, "k?")]],
    "V2": [[(0, "")], [(1, "")], [(2, "c"), (3, "k")], [(4, "c"), (5, "k.")]],
    "V3a": [[(0, "")], [(1, "")], [(2, "")], [(3, "c"), (4, "k")], [(5, "kC")], [(6, "")], [(7, "k")]],
    "V3b": [[(0, "c"), (1, "k")], [(2, "k.b")]],
    "V4": [[(0, "c"), (1, "k")], [(2, "")], [(3, "c"), (4, "k")], [(5, "k")], [(6, "k")], [(7, "c"), (8, "k")], [(9, "")],
           [(10, "")], [(11, "c"), (12, "k")], [(13, "k")], [(14, "c"), (15, "k.")]],
    "V5": [[(0, "c"), (1, "kC")], [(2, "")], [(3, "c"), (4, "kb")], [(5, "")], [(6, "k.")]],
    "V6": [[(0, "c"), (1, "k")], [(2, "c"), (3, "k")], [(4, "")], [(5, "c"), (6, "k.")]],
    "V7": [[(0, "c"), (1, "k")], [(2, "")], [(3, "c"), (4, "k.")], [(5, "c"), (6, "k.")]],
}
TOP = {"V2": 1290, "V3a": 1400, "V3b": 1400, "V4": 1290, "V7": 700}  # block centre y; default 1075 (56%); faces kept clear
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
                    f'src="assets/shots/{i:02d}.mp4" muted playsinline data-start="{st:.3f}" data-duration="{en - st:.3f}" '
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
        units = UNITS[key]
        for ui, unit in enumerate(units):
            idxs = [i for i, _ in unit]
            if max(idxs) >= len(words):
                continue
            u_start = max(0.0, words[idxs[0]][1] - 0.02)
            nxt_i = units[ui + 1][0][0] if ui + 1 < len(units) else None
            u_end = min((words[nxt_i][1] - 0.02) if nxt_i is not None and nxt_i < len(words) else end_line, END)
            spans = []
            for (wi, role) in unit:
                raw, at = words[wi]
                text = re.sub(r",$", "", raw)
                if "k" in role:
                    text = text.lower().rstrip(".?!")
                    if "C" in role:
                        text = text.upper()
                    if "." in role:
                        text += "."
                    if "?" in role:
                        text += "?"
                    size = min(200, int(1600 / max(4, len(text))))
                    cls = "key blend" if "b" in role else "key"
                elif "c" in role:
                    size, cls = 88, "conn"
                    text = text if text.startswith("I") else text.lower()
                else:
                    size, cls = min(140, int(1500 / max(4, len(text)))), "single"
                wid = f"w{g}_{wi}"
                spans.append(f'<span id="{wid}" class="{cls}" style="font-size:{size}px">{text}</span>')
                tl.append(f'tl.fromTo("#{wid}", {{opacity: 0, filter: "blur(12px)", scale: 1.08}}, {{opacity: 1, filter: "blur(0px)", scale: 1, duration: 0.17, ease: "power2.out", immediateRender: false}}, {at:.3f});')
                if at > u_start + 0.03:
                    tl.append(f'tl.set("#{wid}", {{opacity: 0}}, {u_start:.3f});')
            top = TOP.get(key, 1075)
            caps.append(f'      <div id="cap{g}" class="clip cap" style="top:{top}px" data-start="{u_start:.3f}" '
                        f'data-duration="{max(0.12, u_end - u_start):.3f}" data-track-index="1">{"".join(spans)}</div>')
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
      .cap {{ position: absolute; left: 60px; right: 60px; z-index: 100; display: flex; flex-direction: column; align-items: center;
              transform: translateY(-50%); color: #fff; font-family: var(--sans); font-weight: 900; letter-spacing: -0.04em; text-align: center; }}
      .cap span {{ display: block; line-height: 0.92; text-shadow: 0 3px 10px rgba(0,0,0,.5), 0 1px 2px rgba(0,0,0,.35); white-space: nowrap; }}
      .cap .conn {{ margin-bottom: -0.02em; }}
      .cap .key.blend {{ mix-blend-mode: overlay; text-shadow: none; color: #fff; }}
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
