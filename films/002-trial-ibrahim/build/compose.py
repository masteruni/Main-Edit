#!/usr/bin/env python3
"""v3 composition. Captions follow REFERENCE.md exactly:
- Montserrat Bold (running words, CAPS for hero claims) + Parisienne (title-case emphasis words);
- every word appears on its own spoken onset (word timings from the VO transcripts);
- script words wipe in left→right over 3 frames, sans words fade in over 2 frames with a hint of blur;
- words accumulate into a staircase block for the phrase; the block never moves; it clears at the phrase end;
- warm-white fill with a soft shadow, scene-tinted on B-roll (gold over the jetski sky), navy over the bright window.
Plus: light-leak streak transitions (ref1), the drop flash + punch, slow pushes on held shots.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cutlist import SHOTS, VO, END, DROP, LEAKS, b  # noqa: E402

SMALL = {"is", "the", "a", "in", "an", "for", "my", "to", "and", "of", "i've", "if", "you're", "we're", "about", "what", "this", "are", "like", "your", "had", "ever", "now"}

# Per VO line: chunk sizes (words per block), emphasis words (script), CAPS words, block position, tint
STYLE = {
    "V1": dict(chunks=[3, 3], script={"dreams"}, caps=set(), top=1120, align="left", tint="ink"),
    "V2": dict(chunks=[3, 3], script={"you"}, caps=set(), top=250, align="left", tint="ink"),
    "V3a": dict(chunks=[3, 3, 2], script=set(), caps={"monthly"}, top=250, align="left", tint="ink"),
    "V3b": dict(chunks=[3], script={"uphill"}, caps=set(), top=250, align="left", tint="ink"),
    "V4": dict(chunks=[5, 2, 3, 3, 3], script={"honest", "changed"}, caps=set(), top=250, align="left", tint="ink"),
    "V5": dict(chunks=[3, 2, 2], script={"valuations"}, caps={"million"}, top=260, align="left", tint="gold"),
    "V6": dict(chunks=[3, 2, 2], script={"another"}, caps=set(), top=250, align="left", tint="navy"),
    "V7": dict(chunks=[3, 2, 2], script={"lock", "in."}, caps=set(), top=250, align="left", tint="ink"),
}
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
        st = STYLE[key]
        words = vo_words(key, f, a, z, place)[: sum(st["chunks"])]  # only the words this line's blocks carry
        later = [v[4] for v in VO if v[4] > place]
        end_line = min(place + (z - a) + 0.2, (min(later) - 0.02) if later else END)
        idx = 0
        for n in st["chunks"]:
            chunk = words[idx: idx + n]
            idx += n
            if not chunk:
                continue
            c_start = max(0.0, chunk[0][1] - 0.02)
            nxt = words[idx][1] - 0.02 if idx < len(words) else end_line
            spans = []
            for wi, (text, at) in enumerate(chunk):
                bare = re.sub(r"[^a-z.']", "", text.lower())
                core = re.sub(r"[^a-z']", "", text.lower())
                wid = f"w{g}_{wi}"
                if core in st["script"] or bare in st["script"]:
                    t = text[:1].upper() + text[1:]
                    spans.append(word_html(t, "script", 200, wid))
                    tl.append(f'tl.fromTo("#{wid}", {{clipPath: "inset(-20% 100% -30% -5%)"}}, {{clipPath: "inset(-20% -5% -30% -5%)", duration: 0.125, ease: "power1.out", immediateRender: false}}, {at:.3f});')
                    tl.append(f'tl.set("#{wid}", {{clipPath: "inset(-20% 100% -30% -5%)"}}, {c_start:.3f});')
                else:
                    small = core in SMALL and core not in st["caps"]
                    t = text.upper() if core in st["caps"] else text
                    spans.append(word_html(t, "sans small" if small else "sans", 72 if small else 118, wid))
                    tl.append(f'tl.fromTo("#{wid}", {{opacity: 0, filter: "blur(4px)"}}, {{opacity: 1, filter: "blur(0px)", duration: 0.083, ease: "none", immediateRender: false}}, {at:.3f});')
                    tl.append(f'tl.set("#{wid}", {{opacity: 0}}, {c_start:.3f});')
            c_end = min(nxt, END)
            unders = [sh for sh in SHOTS if sh[0] < c_end - 0.02 and sh[1] > c_start + 0.02]  # every shot the block sits over
            tint = st["tint"] if (st["tint"] != "navy" or all(str(sh[2]).startswith("vo:ibrahim-and-ramin") for sh in unders)) else "ink"
            caps.append(f'      <div id="cap{g}" class="clip cap {st["align"]} tint-{tint}" style="top:{st["top"]}px" '
                        f'data-start="{c_start:.3f}" data-duration="{max(0.2, min(nxt, END) - c_start):.3f}" data-track-index="1">{"".join(spans)}</div>')
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
      @font-face {{ font-family: "Parisienne"; font-style: normal; font-weight: 400; font-display: block; src: url("assets/fonts/parisienne-400.woff2") format("woff2"); }}
      @font-face {{ font-family: "Montserrat"; font-style: normal; font-weight: 700; font-display: block; src: url("assets/fonts/montserrat-700.woff2") format("woff2"); }}
      :root {{ --ink: #f5f1ea; --gold: #f3c76b; --navy: #1b2440; --script: "Parisienne", cursive; --sans: "Montserrat", sans-serif; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #070708; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .cam {{ position: absolute; inset: 0; overflow: hidden; }}
      .cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .cap {{ position: absolute; left: 80px; width: 900px; z-index: 100; display: flex; flex-wrap: wrap; align-items: baseline;
              column-gap: 0; row-gap: 0; color: var(--ink); text-shadow: 0 2px 14px rgba(0,0,0,.45), 0 1px 3px rgba(0,0,0,.35); }}
      .cap.tint-gold {{ color: #fff6e6; }} .cap.tint-gold .script {{ color: var(--gold); text-shadow: 0 0 12px rgba(243,199,107,.55), 0 2px 10px rgba(0,0,0,.35); }}
      .cap.tint-navy {{ color: var(--navy); text-shadow: 0 1px 10px rgba(255,255,255,.35); }}
      .cap span {{ display: inline-block; position: relative; z-index: 1; margin-right: 0.24em; }}
      .cap.tint-ink::before, .cap.tint-gold::before {{ content: ''; position: absolute; inset: -50px -70px; z-index: 0;
              background: radial-gradient(closest-side, rgba(0,0,0,.32), rgba(0,0,0,0)); }}
      .sans {{ font-family: var(--sans); font-weight: 700; letter-spacing: -0.005em; line-height: 1.02; }}
      .sans.small {{ opacity: 0.9; }}
      .script {{ font-family: var(--script); font-weight: 400; line-height: 0.95; padding: 0 0.12em 0.05em 0.02em; margin: -0.12em 0 -0.06em; }}
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
