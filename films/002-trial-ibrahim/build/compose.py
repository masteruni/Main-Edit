#!/usr/bin/env python3
"""Write index.html from cutlist.SHOTS + CAPTIONS: one muted <video> per shot (graded clips from
render_shots.py), kinetic captions as timed groups whose words pop on the beat, the drop flash,
punches and pushes, and the pre-mixed soundtrack. Re-run after any timing change.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cutlist import SHOTS, END, b, h  # noqa: E402

S, B = "script", "sans"
# Caption groups: (start, end, top px, align, [(word, style, size px, appear time)])
CAPTIONS = [
    (0.10, b(2), 1180, "left", [("Everyone", B, 92, 0.10), ("wants", B, 92, b(0)), ("this.", S, 230, b(1))]),
    (b(2) + 0.1, b(4), 330, "left", [("Nobody", B, 92, b(2) + 0.10), ("wants", B, 92, h(2)), ("this.", S, 230, b(3))]),
    (b(4), b(5), 330, "left", [("5 AM.", B, 150, b(4))]),
    (b(5), b(7), 300, "right", [("No one", B, 96, b(5)), ("watching.", S, 190, b(6))]),
    (b(7), b(9), 300, "left", [("Every", B, 96, b(7)), ("single", S, 190, h(7)), ("day.", B, 96, b(8))]),
    (b(9), b(11), 300, "left", [("Until", B, 110, b(9)), ("…", B, 110, b(10))]),
    (b(11), b(13), 360, "center", [("it pays.", S, 250, b(11))]),
    (b(26) + 0.1, b(30), 330, "left", [("Same", S, 220, b(26) + 0.1), ("24 hours.", B, 104, b(27))]),
    (b(33), END, 1180, "left", [("Now everyone", B, 92, b(33)), ("wants", B, 92, b(34)), ("this.", S, 230, b(35))]),
]
PUNCH = [(b(11), 1.16), (b(17), 1.10), (b(30), 1.08)]       # instant scale on the cut, settles in 0.3 s
PUSH = {10: 1.06, 12: 1.07, 25: 1.06, 27: 1.05}               # hero shots: slow push across the shot
FLASH = [b(11)]


def html():
    v, cams, tl = [], [], []
    for i, (st, en, *_rest) in enumerate(SHOTS):
        cams.append(
            f'      <div class="cam" id="cam{i:02d}" style="z-index:{i + 1}">'
            f'<video id="v{i:02d}" class="clip" src="assets/shots/{i:02d}.mp4" muted playsinline '
            f'data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="0"></video></div>')
        if i in PUSH:
            tl.append(f'tl.fromTo("#cam{i:02d}", {{scale: 1}}, {{scale: {PUSH[i]}, duration: {en - st:.3f}, ease: "sine.inOut"}}, {st:.3f});')
    for t, sc in PUNCH:
        i = next(k for k, s in enumerate(SHOTS) if abs(s[0] - t) < 1e-3)
        tl.append(f'tl.fromTo("#cam{i:02d}", {{scale: {sc}}}, {{scale: 1, duration: 0.32, ease: "power3.out", immediateRender: false}}, {t:.3f});')
        if i in PUSH:  # resume the push after the punch
            st, en = SHOTS[i][0], SHOTS[i][1]
            tl.append(f'tl.to("#cam{i:02d}", {{scale: {PUSH[i]}, duration: {en - st - 0.32:.3f}, ease: "sine.inOut"}}, {t + 0.32:.3f});')
    caps = []
    for g, (st, en, top, align, words) in enumerate(CAPTIONS):
        spans = []
        for w, (word, style, size, at) in enumerate(words):
            wid = f"w{g}_{w}"
            spans.append(f'<span id="{wid}" class="{style}" style="font-size:{size}px">{word}</span>')
            tl.append(f'tl.fromTo("#{wid}", {{opacity: 0, scale: 1.22}}, {{opacity: 1, scale: 1, duration: 0.14, ease: "power3.out", immediateRender: false}}, {at:.3f});')
            tl.append(f'tl.set("#{wid}", {{opacity: 0}}, {st:.3f});' if at > st + 1e-3 else "")
        caps.append(
            f'      <div id="cap{g}" class="clip cap {align}" style="top:{top}px" data-start="{st:.3f}" '
            f'data-duration="{en - st:.3f}" data-track-index="1" data-layout-allow-overlap>{"".join(spans)}</div>')
    for k, t in enumerate(FLASH):
        caps.append(f'      <div id="flash{k}" class="clip flash" data-start="{t:.3f}" data-duration="0.2" data-track-index="2"><i></i></div>')
        tl.append(f'tl.fromTo("#flash{k} i", {{opacity: 0.9}}, {{opacity: 0, duration: 0.18, ease: "power2.out"}}, {t:.3f});')
    tl = [x for x in tl if x]
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Pinyon Script"; font-style: normal; font-weight: 400; font-display: block; src: url("assets/fonts/pinyon-script-400.woff2") format("woff2"); }}
      @font-face {{ font-family: "Hanken Grotesk"; font-style: normal; font-weight: 800; font-display: block; src: url("assets/fonts/hanken-grotesk-800.woff2") format("woff2"); }}
      :root {{ --ink: #f6f2ea; --script: "Pinyon Script", cursive; --sans: "Hanken Grotesk", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0c; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .cam {{ position: absolute; inset: 0; overflow: hidden; }}
      .cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .cap {{ position: absolute; left: 96px; right: 96px; z-index: 100; display: flex; flex-direction: column; color: var(--ink);
              text-shadow: 0 4px 22px rgba(0,0,0,.5), 0 1px 3px rgba(0,0,0,.35); }}
      .cap.left {{ align-items: flex-start; }} .cap.right {{ align-items: flex-end; }} .cap.center {{ align-items: center; }}
      .cap span {{ display: block; transform-origin: 30% 60%; }}
      .sans {{ font-family: var(--sans); font-weight: 800; letter-spacing: -0.015em; line-height: 0.98; }}
      .script {{ font-family: var(--script); font-weight: 400; line-height: 0.8; margin: -0.05em 0 0.08em -0.04em; }}
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
print("wrote index.html", len(SHOTS), "shots", len(CAPTIONS), "caption groups", f"{END:.3f}s")
