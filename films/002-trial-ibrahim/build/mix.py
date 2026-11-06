#!/usr/bin/env python3
"""v4 soundtrack.
- Voice: Ibrahim's lines, cleaned (HPF, light denoise, compression) and levelled per line.
- Music: Mixkit #31 "Dreaming Big" (uplifting film score), entered so its drum entry (30.22 s, measured) lands on the drop;
  soft piano under the story, sidechain-ducked under the voice, true silence for half a beat before the drop.
- Sound design, the way a pro mix is built: the footage's own sound first (jetski, desert, water, wind) low under the
  music; a long swell + riser that stop dead at the silence; a layered sub-boom + punch on the drop; one air sweep.
  Every SFX is placed by its MEASURED transient peak (see PEAKS), not by its file start.
-14 LUFS / -1.5 dBTP. Writes assets/audio/soundtrack.m4a.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cutlist import VO, SHOTS, MUSIC_FILE, MUSIC_IN, DROP, END, h  # noqa: E402

A = os.path.join(FILM, "assets/audio")
VOD = os.path.join(FILM, "assets/vo-candidates")
ZIP = os.path.join(FILM, "assets/footage/raw.zip")
ENTRIES = os.environ.get("ZIP_ENTRIES")
GAP = (h(-1), DROP)

# measured peak time inside each SFX file (s): the moment that must land on the target
PEAKS = {"563": 0.10, "1143": 0.50, "786": 3.80, "790": 2.40, "1180": 0.30, "175": 0.40}

# (target time, file, gain dB, length s, mode) — mode "peak": align the file's peak to target; "end": the file is cut at target
SFX = [
    (1.25, "1180", -12, 1.6, "peak"),        # the jump hits the water (subtle; the image already says it)
    (11.40, "175", -18, 0.6, "peak"),        # one air sweep into the montage, under the light leak
    (GAP[0], "786", -10, 3.8, "end"),        # long swell under the montage, cut dead at the silence
    (GAP[0], "790", -14, 2.4, "end"),        # riser layered on top of the swell's last 2.4 s
    (DROP, "1143", -6, 2.2, "peak"),         # sub-boom on the drop
    (DROP, "563", -9, 1.6, "peak"),          # punch layered on the boom
]

# the footage's own sound under the B-roll (shot index, gain dB); 1x-speed shots only
NATIVE = [(14, -14), (15, -20), (17, -18), (18, -18), (19, -24)]


def native_inputs():
    if not (ENTRIES and os.path.exists(ENTRIES) and os.path.exists(ZIP)):
        return []
    entries = {e["name"]: e for e in json.load(open(ENTRIES))}
    manifest = json.load(open(os.path.join(FILM, "assets/proxies/manifest.json")))
    out = []
    for i, db in NATIVE:
        st, en, proxy, src_in, speed = SHOTS[i][:5]
        rec = next((m for m in reversed(manifest) if (m.get("proxy") or "").rsplit(".", 1)[0] == proxy), None)
        e = entries.get(rec["name"]) if rec else None
        if not e or not rec.get("has_audio"):
            continue
        path = os.path.join(A, f"native-{i:02d}.wav")
        src = f"subfile,,start,{e['start']},end,{e['end']},,:{ZIP}"
        r = subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(src_in), "-t", str((en - st) * speed), "-i", src,
                            "-vn", "-ac", "2", "-ar", "48000", path])
        if r.returncode == 0 and os.path.exists(path):
            out.append((path, st, en - st, db))
    return out


def main():
    inputs, parts, vo_labels = [], [], []
    k = 0
    for key, f, a, z, place in VO:
        inputs += ["-i", os.path.join(VOD, f + ".m4a")]
        ms = int(round(place * 1000))
        parts.append(
            f"[{k}:a]atrim={a}:{z},asetpts=PTS-STARTPTS,aformat=channel_layouts=stereo,highpass=f=90,afftdn=nf=-30,"
            f"equalizer=f=3000:t=q:w=1:g=2,acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=4,"
            f"loudnorm=I=-15:TP=-2:LRA=7,afade=t=in:d=0.015,afade=t=out:st={z - a - 0.03:.3f}:d=0.03,aresample=48000,"
            f"adelay={ms}|{ms},apad[vo{k}]")
        vo_labels.append(f"[vo{k}]")
        k += 1
    parts.append(f"{''.join(vo_labels)}amix=inputs={len(vo_labels)}:normalize=0:duration=longest,atrim=0:{END},asplit=2[vox][vside]")

    mi = k
    inputs += ["-ss", f"{-MUSIC_IN:.3f}", "-i", os.path.join(A, MUSIC_FILE)]
    parts.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{END},"
                 f"volume=0:enable='between(t,{GAP[0]},{GAP[1]})',volume=0.85[mraw]")
    parts.append("[mraw][vside]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=400:makeup=1[mus]")
    labels = ["[vox]", "[mus]"]
    idx = mi + 1

    for j, (t, sid, db, ln, mode) in enumerate(SFX):
        inputs += ["-i", os.path.join(A, "sfx", sid + ".mp3")]
        if mode == "peak":
            lead = {"1143": 0.18, "563": 0.02}.get(sid)          # how much of the build-up before the peak to keep
            start_in_file = max(0.0, PEAKS[sid] - lead) if lead is not None else 0.0
            place = t - PEAKS[sid] + start_in_file
        else:  # "end": play the ln seconds of the file that END at its peak... cut dead at t
            start_in_file = max(0.0, PEAKS[sid] - ln)
            place = t - (PEAKS[sid] - start_in_file)
        ms = int(round(max(0, place) * 1000))
        fade_out = f"afade=t=out:st={max(0, ln - 0.15):.3f}:d=0.15," if mode == "peak" else "afade=t=out:st=%.3f:d=0.02," % max(0, ln - 0.02)
        parts.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={start_in_file:.3f}:{start_in_file + ln:.3f},"
                     f"asetpts=PTS-STARTPTS,afade=t=in:d={0.4 if mode == 'end' else 0.005},{fade_out}volume={db}dB,"
                     f"adelay={ms}|{ms},apad[s{j}]")
        labels.append(f"[s{j}]")
        idx += 1

    for n, (path, st, ln, db) in enumerate(native_inputs()):
        inputs += ["-i", path]
        ms = int(round(st * 1000))
        parts.append(f"[{idx}:a]highpass=f=60,afade=t=in:d=0.04,afade=t=out:st={max(0, ln - 0.06):.3f}:d=0.06,volume={db}dB,"
                     f"adelay={ms}|{ms},apad[n{n}]")
        labels.append(f"[n{n}]")
        idx += 1

    parts.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{END},"
                 f"afade=t=out:st={END - 0.25}:d=0.25,loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    out = os.path.join(A, "soundtrack.m4a")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(parts),
                    "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "256k", out], check=True)
    print("wrote", out, "with", len(labels) - 2, "sfx/native layers")


if __name__ == "__main__":
    main()
