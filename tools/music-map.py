#!/usr/bin/env python3
"""Map a music track for editing without hearing it: tempo, beat grid, and the energy contour
(intro / builds / drops / breakdowns) in 1-second bars.

  python3 -I tools/music-map.py track.mp3 [--json out.json]
"""
import json, subprocess, sys
import numpy as np

path = sys.argv[1]
SR = 22050
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
dur = len(x) / SR
hop = 512
frames = len(x) // hop
win = np.hanning(1024)
spec = np.abs(np.array([np.fft.rfft(x[i * hop:i * hop + 1024] * win) for i in range(frames - 2)]))
flux = np.maximum(0, np.diff(np.log1p(spec), axis=0)).sum(axis=1)
flux = (flux - flux.mean()) / (flux.std() + 1e-9)
fps = SR / hop
# tempo: autocorrelation of onset strength, 70-180 BPM
ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
lags = np.arange(len(ac))
bpm_l = 60 * fps / np.maximum(lags, 1)
mask = (bpm_l >= 70) & (bpm_l <= 180)
lag = lags[mask][np.argmax(ac[mask])]
bpm = 60 * fps / lag
# beat phase: offset that maximises onset energy on the grid
period = lag
best = max(range(int(period)), key=lambda o: flux[o::int(round(period))].sum() if True else 0)
beats = [round((best + k * period) / fps, 3) for k in range(int((len(flux) - best) / period))]
# energy contour: RMS dB and low-band (kick/bass) per second
rms = [20 * np.log10(np.sqrt(np.mean(x[i * SR:(i + 1) * SR] ** 2)) + 1e-9) for i in range(int(dur))]
lowband = []
for i in range(int(dur)):
    seg = x[i * SR:(i + 1) * SR]
    f = np.abs(np.fft.rfft(seg))
    fr = np.fft.rfftfreq(len(seg), 1 / SR)
    lowband.append(float(20 * np.log10(f[(fr > 30) & (fr < 150)].mean() + 1e-9)))
r = np.array(rms)
events = []
for i in range(2, len(r)):
    d = r[i] - r[max(0, i - 2):i].mean()
    if d > 4: events.append((i, "DROP/ENTRY", round(float(d), 1)))
    if d < -5: events.append((i, "BREAK/STOP", round(float(d), 1)))
out = {"file": path, "duration": round(dur, 2), "bpm": round(float(bpm), 1), "beat_period": round(float(period / fps), 4), "first_beat": beats[0] if beats else 0,
       "rms_db_per_s": [round(float(v), 1) for v in rms], "low_db_per_s": [round(v, 1) for v in lowband], "events": events}
if "--json" in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"))
print(f"{path}: {out['duration']}s  ~{out['bpm']} BPM  first beat {out['first_beat']}s")
lo, hi = min(rms), max(rms)
print("energy/s: " + "".join(" ▁▂▃▄▅▆▇█"[int((v - lo) / (hi - lo + 1e-9) * 8)] for v in rms))
print("events:   " + ", ".join(f"{t}s {k}({d})" for t, k, d in events[:14]))
