#!/usr/bin/env python3
"""Synthesise the film's sound from assets/schedule.json: hall tone, every flap click
(louder on the row the camera is looking at), a two-note PA chime before the payoff, and
the lamp relay. Writes build/sound.wav; encode with loudnorm to assets/sound.m4a."""
import json, sys, wave
from pathlib import Path
import numpy as np

DIR = Path(__file__).resolve().parent.parent
SR, DUR = 48000, 13.6
N = int(SR * DUR)
rng = np.random.default_rng(1994)
sched = json.loads((DIR / "assets/schedule.json").read_text())
out = np.zeros((N, 2))

def place(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
    out[i:i + len(sig), 0] += sig * gain * l
    out[i:i + len(sig), 1] += sig * gain * r

def flap(kind):
    n = int(SR * (0.012 if kind == 0 else 0.035))
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    noise = np.diff(noise, prepend=0)                     # brighten: plastic flap, not a thud
    env = np.exp(-tt / (0.0011 if kind == 0 else 0.0035))
    body_f = rng.uniform(1700, 2600) if kind == 0 else rng.uniform(780, 980)
    body = np.sin(2 * np.pi * body_f * tt) * np.exp(-tt / (0.003 if kind == 0 else 0.012))
    return (0.55 * noise * env + 0.45 * body) * rng.uniform(0.6, 1.0)

# which row the camera is on, per shot (None = wide)
SHOTS = [(0, 3.6, None), (3.6, 4.4, 1), (4.4, 5.1, 2), (5.1, 5.9, 3), (5.9, 6.7, 5), (6.7, 9.7, 5), (9.7, 13.6, None)]
def focus(t):
    for a, b, r in SHOTS:
        if a <= t < b: return r
    return None

clicks = np.zeros((N, 2))
for t, col, row, kind in sched["clicks"]:
    f = focus(t)
    g = 1.0 if f is None else (1.7 if row == f else 0.45)
    g *= 0.9 if kind == 0 else 1.6
    pan = (col / 29 - 0.5) * (1.1 if f is None else 0.5)
    i = int(t * SR)
    s = flap(kind)[: max(0, N - i)]
    if len(s) == 0: continue
    clicks[i:i + len(s), 0] += s * g * np.sqrt((1 - pan) / 2)
    clicks[i:i + len(s), 1] += s * g * np.sqrt((1 + pan) / 2)

# station hall: an exponentially decaying noise IR, a different seed per side
def ir(seed):
    r = np.random.default_rng(seed)
    n = int(SR * 1.1)
    tt = np.arange(n) / SR
    h = r.standard_normal(n) * np.exp(-tt / 0.28)
    h[: int(SR * 0.012)] = 0                             # pre-delay
    return h / np.sqrt(np.sum(h ** 2))
def convolve(x, h):
    m = len(x) + len(h) - 1
    k = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, k) * np.fft.rfft(h, k), k)[: len(x)]
wet = np.stack([convolve(clicks[:, 0], ir(1)), convolve(clicks[:, 1], ir(2))], axis=1)
out += clicks + 0.32 * wet

# hall tone: brown noise, high-passed, plus a faint fluorescent hum
b = np.cumsum(rng.standard_normal((N, 2)), axis=0)
b -= np.stack([np.convolve(b[:, c], np.ones(4800) / 4800, mode="same") for c in range(2)], axis=1)
b /= np.max(np.abs(b))
tt = np.arange(N) / SR
hum = 0.02 * np.sin(2 * np.pi * 100 * tt) + 0.008 * np.sin(2 * np.pi * 200 * tt)
room = 0.11 * b + hum[:, None]
room[: int(SR * 0.15)] *= np.linspace(0, 1, int(SR * 0.15))[:, None]
out += room

# PA chime: two soft notes, E5 then C5, with the hall on them
def note(f, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    env = np.minimum(1, t / 0.012) * np.exp(-t / 0.42)
    return env * (np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t) + 0.08*np.sin(2*np.pi*3*f*t))
chime = np.zeros(N)
for f, t0 in ((659.25, 5.98), (523.25, 6.36)):
    s = note(f, 1.4); i = int(t0 * SR); chime[i:i + len(s)] += s[: N - i]
out += 0.16 * np.stack([chime, chime], axis=1) + 0.12 * np.stack([convolve(chime, ir(3)), convolve(chime, ir(4))], axis=1)

# lamp relay: a click and a small thump
n = int(SR * 0.06); t = np.arange(n) / SR
relay = 0.6 * np.sin(2*np.pi*110*t) * np.exp(-t / 0.018) + 0.4 * rng.standard_normal(n) * np.exp(-t / 0.002)
place(relay, sched["lampOn"], 0.5, -0.6)

# safety: gentle limiter, then write 24-bit
peak = np.max(np.abs(out))
out = np.tanh(out / peak * 1.6) / np.tanh(1.6) * 0.89
pcm = (out * (2**23 - 1)).astype("<i4")
raw = b"".join(int(v).to_bytes(4, "little", signed=True)[:3] for v in pcm.reshape(-1))
with wave.open(str(DIR / "build/sound.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(3); w.setframerate(SR); w.writeframes(raw)
print("wrote build/sound.wav", N / SR, "s")
