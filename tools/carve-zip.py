#!/usr/bin/env python3
"""Pull media out of a (possibly partial) STORED zip, e.g. a Dropbox folder download, and make
editing proxies, without needing the zip's central directory and without unzipping everything.

  python3 -I tools/carve-zip.py raw.zip out_dir [--short 1080] [--keep-originals] [--only "a.mov,b.MP4"]

Each entry is read in place (ffmpeg subfile protocol), probed, and transcoded to an H.264 proxy whose short side is
--short px (original fps and audio kept). A manifest.json lists
name, duration, fps, resolution, rotation and audio for every proxy. An entry cut off by the end of
a partial download is reported and skipped.
"""
import json, os, re, struct, subprocess, sys, tempfile

args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] not in ("--short", "--only")]
short = int(next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--short"), 1080))
keep = "--keep-originals" in sys.argv
only = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--only"), None)  # comma-separated names
only = set(x.strip() for x in only.split(",")) if only else None
zpath, out = args[0], args[1]
os.makedirs(out, exist_ok=True)
size = os.path.getsize(zpath)
MEDIA = re.compile(r"\.(mp4|mov|m4v|mxf|mts|avi|wav|mp3|m4a|aac)$", re.I)

# 1) find local file headers by scanning for the signature and validating the header
offs = []
with open(zpath, "rb") as f:
    buf_off = 0
    tail = b""
    while True:
        chunk = f.read(64 << 20)
        if not chunk:
            break
        data = tail + chunk
        base = buf_off - len(tail)
        for m in re.finditer(b"PK\x03\x04", data):
            o = base + m.start()
            h = data[m.start(): m.start() + 30]
            if len(h) < 30:
                continue
            ver, flag, comp, mt, md, crc, cs, us, nlen, elen = struct.unpack("<HHHHHIIIHH", h[4:30])
            name = data[m.start() + 30: m.start() + 30 + nlen]
            if comp == 0 and 0 < nlen < 512 and ver < 100 and name and all(32 <= c < 127 or c >= 128 for c in name):
                offs.append((o, nlen, elen, flag, name.decode("utf-8", "replace")))
        tail = data[-64:]
        buf_off += len(chunk)

entries = [e for e in offs if not e[4].endswith("/")]
manifest_path = os.path.join(out, "manifest.json")
manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else []
done = {m["name"] for m in manifest}

for k, (o, nlen, elen, flag, name) in enumerate(entries):
    if not MEDIA.search(name) or name in done or (only and name not in only):
        continue
    start = o + 30 + nlen + elen
    nxt = next((e[0] for e in offs if e[0] > o), None)
    if nxt is None:
        print(f"skip (cut off by partial download): {name}")
        continue
    end = nxt - (24 if flag & 8 else 0)  # zip64 data descriptor; ffmpeg ignores a few stray bytes anyway
    stem = os.path.splitext(os.path.basename(name))[0]
    safe = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
    used = {(m.get("proxy") or "").rsplit(".", 1)[0] for m in manifest}
    base, n = safe, 2
    while safe in used:  # "Ibrahim praying.mov" vs "Ibrahim Praying.MP4": never overwrite
        safe, n = f"{base}-{n}", n + 1
    # Read the entry in place through ffmpeg's subfile protocol: no temp copy, so a nearly full disk is fine.
    src = f"subfile,,start,{start},end,{end},,:{os.path.abspath(zpath)}"
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", src], capture_output=True, text=True).stdout or "{}")
    vs = next((s for s in pr.get("streams", []) if s.get("codec_type") == "video"), None)
    has_audio = any(s.get("codec_type") == "audio" for s in pr.get("streams", []))
    info = {"name": name, "bytes": end - start, "has_audio": has_audio}
    if vs:
        num, den = map(int, (vs.get("avg_frame_rate") or "0/1").split("/"))
        fps = round(num / den, 3) if den else None
        rot = 0
        for sd in vs.get("side_data_list", []) or []:
            if "rotation" in sd:
                rot = int(sd["rotation"])
        w, h = vs["width"], vs["height"]
        if abs(rot) == 90:
            w, h = h, w
        info.update(fps=fps, width=w, height=h, rotation=rot, duration=float(pr["format"].get("duration", 0)), codec=vs.get("codec_name"),
                    color=vs.get("color_transfer"), pix=vs.get("pix_fmt"))
        proxy = os.path.join(out, f"{safe}.mp4")
        scale = f"scale='if(lt(iw,ih),{short},-2)':'if(lt(iw,ih),-2,{short})'"
        # HDR (HLG/PQ) phone footage: tone-map to SDR so it doesn't render washed out
        vf = scale if vs.get("color_transfer") not in ("arib-std-b67", "smpte2084") else \
            f"zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,{scale}"
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", "-movflags", "+faststart"] + (["-c:a", "aac", "-b:a", "192k"] if has_audio else ["-an"]) + [proxy]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and "zscale" in vf:  # no zscale in this ffmpeg: plain scale
            cmd[cmd.index(vf)] = scale
            r = subprocess.run(cmd, capture_output=True, text=True)
        info["proxy"] = os.path.basename(proxy) if r.returncode == 0 else None
        if r.returncode != 0:
            info["error"] = r.stderr[-400:]
    elif has_audio:
        proxy = os.path.join(out, f"{safe}.m4a")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-c:a", "aac", "-b:a", "256k", proxy])
        info.update(proxy=os.path.basename(proxy), duration=float(pr["format"].get("duration", 0)))
    if keep:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-c", "copy", os.path.join(out, "orig-" + os.path.basename(name))])
    manifest.append(info)
    json.dump(manifest, open(manifest_path, "w"), indent=1)
    print(f"[{k + 1}/{len(entries)}] {name} → {info.get('proxy')}  {info.get('width')}x{info.get('height')} {info.get('fps')}fps {info.get('duration', 0):.1f}s audio={has_audio}", flush=True)
