#!/usr/bin/env python3
"""The edit, as data. Every cut is on the music grid: beat n = 0.457 + 0.6857 n (video seconds; 87.5 BPM),
music entered at 6.769 s so its drop (the first 808 at 14.769 s, measured) lands on beat 11 = 8.000 s.

Each shot: proxy file, source in-point, speed (0.5 = half speed from 60 fps), crop zoom + centre
(fractions of the frame), and a grade preset. build/render_shots.py turns these into
assets/shots/NN.mp4 (1080x1920, 30 fps, graded, silent); index.html places them.
"""
BEAT0, BEAT = 0.457, 0.6857


def b(n):  # time of beat n
    return round(BEAT0 + BEAT * n, 3)


def h(n):  # half a beat after beat n
    return round(BEAT0 + BEAT * n + BEAT / 2, 3)


MUSIC_OFFSET = 6.769
END = b(37)  # 25.828: last downbeat; the replay loops back into the hook

# (start, end, proxy, src_in, speed, zoom, cx, cy, grade)
SHOTS = [
    # HOOK: the reward everyone wants, then the part nobody wants
    (0.0, b(2), "ibrahim-yacht-jump", 3.35, 0.6, 1.25, 0.55, 0.32, "day"),  # all three mid-air on frame 1
    (b(2), b(4), "ibrahim-waking-up", 1.35, 1.0, 1.08, 0.50, 0.55, "dawn"),
    # BUILD: discipline, shots getting shorter into the drop
    (b(4), b(5), "ibrahim-praying", 22.85, 1.0, 1.15, 0.50, 0.62, "night"),
    (b(5), b(6), "ibrahim-running-2", 8.4, 1.0, 1.0, 0.50, 0.50, "day"),
    (b(6), b(7), "ibrahim-pulldown", 11.2, 1.0, 1.05, 0.50, 0.45, "warm"),
    (b(7), h(7), "ibrahim-clap-pushups", 14.0, 1.0, 1.0, 0.50, 0.50, "warm"),
    (h(7), b(8), "cold-plunge-ibrahim", 2.2, 1.0, 1.1, 0.50, 0.45, "day"),
    (b(8), b(9), "ibrahim-night-work", 6.0, 1.0, 1.1, 0.55, 0.45, "neon"),
    (b(9), b(10), "stripe-payment-2", 0.6, 1.0, 1.55, 0.36, 0.83, "night"),
    (b(10), b(11), "stripe-payment", 0.05, 1.0, 1.35, 0.28, 0.55, "night"),
    # DROP: it pays
    (b(11), b(13), "jetski-takeoff", 5.3, 0.75, 1.1, 0.48, 0.55, "day"),
    (b(13), b(14), "burj-khalifa-clip", 2.0, 1.0, 1.0, 0.50, 0.40, "night"),
    (b(14), b(16), "ibrahim-desert-eagle", 7.1, 0.5, 1.12, 0.50, 0.45, "golden"),
    (b(16), b(17), "ibrahim-atv-desert", 4.0, 1.0, 1.0, 0.50, 0.50, "golden"),
    (b(17), h(17), "ibrahim-wakesurfing", 6.0, 1.0, 1.15, 0.50, 0.40, "day"),
    (h(17), b(18), "jetski-spin", 3.9, 1.0, 1.15, 0.50, 0.50, "day"),
    (b(18), b(19), "ibrahim-yacht-king", 1.5, 1.0, 1.12, 0.45, 0.62, "day"),
    (b(19), b(20), "rolls-royce-inside", 1.0, 1.0, 1.0, 0.50, 0.50, "night"),
    (b(20), b(21), "jetski-drone-ibrahim", 14.8, 1.0, 1.1, 0.50, 0.50, "day"),
    (b(21), b(22), "ibrahim-rolls-royce", 1.0, 1.0, 1.0, 0.50, 0.55, "night"),
    (b(22), b(23), "ibrahim-driving-boat", 5.0, 1.0, 1.0, 0.50, 0.50, "day"),
    (b(23), h(23), "dubai-yachts", 1.0, 1.0, 1.25, 0.50, 0.45, "golden"),
    (h(23), b(24), "ibrahim-on-a-yacht", 2.3, 1.0, 1.0, 0.50, 0.50, "day"),
    (b(24), b(25), "ibrahim-cigar", 2.0, 1.0, 1.05, 0.50, 0.45, "night"),
    (b(25), b(26), "ibrahim-dinner", 0.5, 1.0, 1.0, 0.50, 0.50, "night"),
    # BREATHER: same 24 hours
    (b(26), b(30), "ibrahim-riding-horse", 29.0, 0.5, 1.05, 0.50, 0.50, "day"),
    # RETURN + LOOP
    (b(30), b(32), "ibrahim-with-friends", 1.8, 0.75, 1.0, 0.50, 0.50, "golden"),
    (b(32), END, "fireworks-broll-yacht", 9.5, 1.0, 1.0, 0.50, 0.50, "night"),
]
