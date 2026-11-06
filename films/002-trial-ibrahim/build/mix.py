#!/usr/bin/env python3
"""Pre-mix the soundtrack: Mixkit music (entered at MUSIC_OFFSET), every SFX on its visible cause,
the breather low-passed, a silent gap before the drop, normalised to -14 LUFS / -1 dBTP.
Writes assets/audio/soundtrack.m4a.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cutlist import MUSIC_OFFSET, END, b, h  # noqa: E402

A = os.path.join(FILM, "assets/audio")
MUSIC = os.path.join(A, "music-mixkit-364.mp3")
GAP = (b(11) - 0.34, b(11))          # the half-beat of silence before the drop
BREATHER = (b(26), b(30))            # "Same 24 hours": music low-passed under the waves

# (time, file, gain dB, max length s)
SFX = [
    (1.31, "sfx/1180.mp3", -5, 1.5),          # yacht jump: hitting the water (source 4.1 s)
    (b(2), "sfx/988.mp3", -11, 1.35),        # alarm on the cut to waking up
    (b(4), "sfx/498.mp3", -9, 1.5),          # low heartbeat hit under "5 AM."
    (GAP[0] - 2.0, "sfx/790.mp3", -7, 2.0),  # riser into the gap
    (b(9) + 0.05, "sfx/2354.mp3", -9, 0.8),  # Stripe dashboard
    (b(10) + 0.05, "sfx/2354.mp3", -8, 0.8), # Stripe notification
    (b(10) + 0.12, "sfx/1993.mp3", -12, 0.8),
    (b(11), "sfx/788.mp3", -2, 3.0),         # THE DROP
    (b(11) + 0.05, "sfx/1311.mp3", -8, 1.0), # jetski spray on the drop
    (b(26), "sfx/1185.mp3", -15, BREATHER[1] - BREATHER[0]),  # sea under the horse
    (b(30) + 0.25, "sfx/2836.mp3", -11, 1.0),                 # friends: glasses clink
]


def main():
    dur = END
    inputs = ["-ss", str(MUSIC_OFFSET), "-t", str(dur + 0.5), "-i", MUSIC]
    m_off = MUSIC_OFFSET
    music = (f"[0:a]volume=0.0:enable='between(t,{GAP[0]},{GAP[1]})',"
             f"lowpass=f=520:enable='between(t,{BREATHER[0]},{BREATHER[1]})',"
             f"volume=0.55:enable='between(t,{BREATHER[0]},{BREATHER[1]})',"
             f"atrim=0:{dur},afade=t=out:st={dur - 0.04}:d=0.04[m]")
    parts, labels = [music], ["[m]"]
    for k, (t, f, db, ln) in enumerate(SFX, start=1):
        inputs += ["-i", os.path.join(A, f)]
        ms = int(round(t * 1000))
        parts.append(f"[{k}:a]atrim=0:{ln},afade=t=out:st={max(0, ln - 0.15)}:d=0.15,volume={db}dB,"
                     f"adelay={ms}|{ms},apad[s{k}]")
        labels.append(f"[s{k}]")
    # the fireworks' own sound from the original clip, under the last shot
    fw = os.path.join(A, "fireworks-native.m4a")
    if os.path.exists(fw):
        k = len(SFX) + 1
        inputs += ["-i", fw]
        ms = int(round(b(32) * 1000))
        parts.append(f"[{k}:a]volume=-13dB,afade=t=in:d=0.3,adelay={ms}|{ms},apad[s{k}]")
        labels.append(f"[s{k}]")
    parts.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{dur},"
                 f"loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    out = os.path.join(A, "soundtrack.m4a")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(parts), "-map", "[out]",
           "-ar", "48000", "-c:a", "aac", "-b:a", "256k", out]
    subprocess.run(cmd, check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
