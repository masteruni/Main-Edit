#!/usr/bin/env python3
"""v3 soundtrack: Ibrahim's voiceover (cleaned, levelled per line) + Mixkit #364 entering at MUSIC_IN,
ducked under the voice by a sidechain, true silence for half a beat before the drop, SFX on visible
causes only. -14 LUFS / -1.5 dBTP. Writes assets/audio/soundtrack.m4a.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cutlist import VO, MUSIC_IN, DROP, END, b, h  # noqa: E402

A = os.path.join(FILM, "assets/audio")
VOD = os.path.join(FILM, "assets/vo-candidates")
MUSIC = os.path.join(A, "music-mixkit-364.mp3")
GAP = (h(-1), DROP)

SFX = [
    (1.25, "sfx/1180.mp3", -7, 1.4),           # the jump lands
    (11.40, "sfx/988.mp3", -20, 0.9),          # alarm under the cut to waking up (quiet: he is still talking)
    (b(-3) + 0.05, "sfx/2354.mp3", -11, 0.7),  # Stripe dashboard
    (b(-2) + 0.05, "sfx/2354.mp3", -10, 0.7),  # Stripe notification
    (b(-2) + 0.12, "sfx/1993.mp3", -14, 0.6),
    (GAP[0] - 2.0, "sfx/790.mp3", -9, 2.0),    # riser into the silence
    (DROP, "sfx/788.mp3", -4, 3.0),            # the drop
    (DROP + 0.04, "sfx/1311.mp3", -10, 1.0),   # jetski spray
]


def main():
    inputs, parts, vo_labels = [], [], []
    k = 0
    for key, f, a, z, place in VO:
        inputs += ["-i", os.path.join(VOD, f + ".m4a")]
        ms = int(round(place * 1000))
        parts.append(
            f"[{k}:a]atrim={a}:{z},asetpts=PTS-STARTPTS,aformat=channel_layouts=stereo,highpass=f=90,afftdn=nf=-30,"
            f"acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-15:TP=-2:LRA=7,"
            f"afade=t=in:d=0.015,afade=t=out:st={z - a - 0.03:.3f}:d=0.03,aresample=48000,adelay={ms}|{ms},apad[vo{k}]")
        vo_labels.append(f"[vo{k}]")
        k += 1
    parts.append(f"{''.join(vo_labels)}amix=inputs={len(vo_labels)}:normalize=0:duration=longest,atrim=0:{END},asplit=2[vox][vside]")
    mi = k
    inputs += ["-i", MUSIC]
    ms = int(round(MUSIC_IN * 1000))
    parts.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},apad,atrim=0:{END},"
                 f"volume=0:enable='between(t,{GAP[0]},{GAP[1]})',volume=0.9[mraw]")
    parts.append("[mraw][vside]sidechaincompress=threshold=0.02:ratio=7:attack=25:release=350:makeup=1[mus]")
    labels = ["[vox]", "[mus]"]
    for j, (t, f, db, ln) in enumerate(SFX):
        idx = mi + 1 + j
        inputs += ["-i", os.path.join(A, f)]
        ms = int(round(t * 1000))
        parts.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{ln},afade=t=out:st={max(0, ln - 0.12)}:d=0.12,"
                     f"volume={db}dB,adelay={ms}|{ms},apad[s{j}]")
        labels.append(f"[s{j}]")
    parts.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{END},"
                 f"afade=t=out:st={END - 0.05}:d=0.05,loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    out = os.path.join(A, "soundtrack.m4a")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(parts),
                    "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "256k", out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
