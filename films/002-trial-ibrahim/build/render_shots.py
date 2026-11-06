#!/usr/bin/env python3
"""Render every shot in cutlist.SHOTS to assets/shots/NN.mp4: trimmed, re-timed, cropped and
graded, 1080x1920 @ 30 fps, silent. Source = the 4K original read in place from the Dropbox zip
(sharper crops), falling back to the 1080 proxy. HLG phone footage is tone-mapped to SDR first.

  python3 -I build/render_shots.py [--only 3,5] [--proxy]
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cutlist import SHOTS  # noqa: E402

ZIP = os.path.join(FILM, "assets/footage/raw.zip")
ENTRIES = os.environ.get("ZIP_ENTRIES")  # entries.json from the thumbnail scan: name -> byte range
OUT = os.path.join(FILM, "assets/shots")
os.makedirs(OUT, exist_ok=True)
manifest = json.load(open(os.path.join(FILM, "assets/proxies/manifest.json")))
entries = {e["name"]: e for e in json.load(open(ENTRIES))} if ENTRIES and os.path.exists(ENTRIES) else {}
only = set(int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
use_proxy = "--proxy" in sys.argv

# Grades: warm highlights / teal shadows (the references), tuned per light situation.
GRADES = {
    "day": "eq=contrast=1.08:saturation=1.10:gamma=0.98,colorbalance=rs=-0.03:bs=0.04:rh=0.04:bh=-0.03",
    "golden": "eq=contrast=1.10:saturation=1.12:gamma=0.97,colorbalance=rs=0.02:bs=0.02:rm=0.04:bm=-0.03:rh=0.06:bh=-0.05",
    "warm": "eq=contrast=1.08:saturation=1.05:gamma=0.97,colorbalance=rs=-0.02:bs=0.03:rh=0.05:bh=-0.04",
    "night": "eq=contrast=1.12:saturation=1.08:gamma=0.95,colorbalance=rs=-0.03:bs=0.05:rh=0.04:bh=-0.02",
    "neon": "eq=contrast=1.06:saturation=1.0:gamma=0.97",
    "dawn": "eq=contrast=1.10:saturation=0.85:brightness=-0.06:gamma=0.92,colorbalance=rs=-0.04:gs=-0.01:bs=0.06:rm=-0.02:bm=0.04",
}
FINISH = "vignette=angle=PI/5:mode=forward,noise=alls=5:allf=t,format=yuv420p"


def source(proxy):
    """(input spec, is_hlg) for a proxy slug: the original in the zip when we know its byte range."""
    # last match wins: when two sources once shared a name, the later one wrote the proxy file
    rec = next((m for m in reversed(manifest) if (m.get("proxy") or "").rsplit(".", 1)[0] == proxy), None)
    if rec is None:
        raise SystemExit(f"no proxy for {proxy}")
    hlg = rec.get("color") in ("arib-std-b67", "smpte2084")
    e = entries.get(rec["name"])
    if e and not use_proxy and os.path.exists(ZIP):
        return f"subfile,,start,{e['start']},end,{e['end']},,:{ZIP}", hlg, True
    return os.path.join(FILM, "assets/proxies", rec["proxy"]), False, False  # proxies are already SDR


def render(i, shot):
    start, end, proxy, src_in, speed, zoom, cx, cy, grade = shot
    dur = end - start
    frames = round(dur * 30)
    src, hlg, original = source(proxy)
    pre = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p," if hlg else ""
    # crop a 9:16 window of 1/zoom of the frame around (cx, cy), clamped inside the frame
    crop = (f"crop=w='trunc(min(iw,ih*9/16)/{zoom}/2)*2':h='trunc(min(iw,ih*9/16)/{zoom}*16/9/2)*2':"
            f"x='max(0,min(iw-ow,iw*{cx}-ow/2))':y='max(0,min(ih-oh,ih*{cy}-oh/2))'")
    vf = f"{pre}setpts=(PTS-STARTPTS)/{speed},fps=30,{crop},scale=1080:1920:flags=lanczos,{GRADES[grade]},{FINISH}"
    out = os.path.join(OUT, f"{i:02d}.mp4")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", str(src_in), "-t", str(dur * speed + 0.5), "-i", src,
           "-vf", vf, "-frames:v", str(frames), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-g", "15", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return f"{i:02d} {proxy} FAILED: {r.stderr[-300:]}"
    got = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    return f"{i:02d} {proxy:28s} {dur:5.2f}s {frames}f (got {got}) {'4K' if original else 'proxy'}{' HLG→SDR' if hlg else ''}"


jobs = [(i, s) for i, s in enumerate(SHOTS) if only is None or i in only]
with ThreadPoolExecutor(max_workers=2) as ex:
    for line in ex.map(lambda a: render(*a), jobs):
        print(line, flush=True)
