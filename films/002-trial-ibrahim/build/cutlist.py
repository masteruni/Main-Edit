#!/usr/bin/env python3
"""v3: the story is Ibrahim's own voice (assets/vo-video, from the client's Dropbox), cut into one
arc, with the music's drop (first 808, measured at 14.769 s in Mixkit #364) on "10 million dollars".

Grid: beat n = DROP + 0.6857 n (87.5 BPM); B-roll cuts sit on it, talking-head cuts sit on the words.
Shot tuple: (start, end, source, src_in, speed, zoom, cx, cy, grade, fx)
  source = proxy slug (read from the 4K original in the Dropbox zip) or "vo:<file>" (assets/vo-video)
  fx     = "" | "bw-open" (first 0.25 s black & white, the reference's opening pop) | "ramp" (100→30→100 % speed)
"""
BEAT = 0.6857
DROP = 18.5
MUSIC_IN = DROP - 14.769          # the track starts (from 0) at this video time: 3.731 s


def b(n):
    return round(DROP + BEAT * n, 3)


def h(n):
    return round(DROP + BEAT * n + BEAT / 2, 3)


END = b(17)  # 30.157

# Voiceover: (key, file in assets/vo-candidates/*.wav + vo-video, src_in, src_out, place at video t)
VO = [
    ("V1", "ibrahim-filming-and-talking", 0.00, 1.92, 0.00),    # Feeling like your dreams are impossible?
    ("V2", "ibrahim-filming-and-talking", 2.57, 4.56, 2.05),    # This is the video for you.
    ("V3a", "ibrahim-recording-in-miami-crib", 2.24, 5.52, 4.20),  # If you're earning under $1,000 monthly, you're fighting
    ("V3b", "ibrahim-recording-in-miami-crib", 12.97, 14.55, 7.48),  # an uphill battle.
    ("V4", "ibrahim-filming-and-talking", 9.24, 14.04, 9.25),   # This is the most honest conversation ... changed my life.
    ("V5", "ibrahim-and-ramin-podcast-in-dubai", 0.00, 2.33, DROP),  # 10 million dollars in valuations going up.
    ("V6", "ibrahim-and-ramin-podcast-in-dubai", 7.63, 10.50, 23.985),  # And now we're launching another software company
    ("V7", "ibrahim-selfie-on-yacht", 0.00, 3.11, 26.95),         # Lock in boys, lock in. Let's go.
]

FILM = "vo:ibrahim-filming-and-talking.mov"
MIAMI = "vo:ibrahim-recording-in-miami-crib.mov"
POD = "vo:ibrahim-and-ramin-podcast-in-dubai.mov"
SELFIE = "vo:ibrahim-selfie-on-yacht.mov"

SHOTS = [
    # HOOK: the dream (the jump) under "Feeling like your dreams are impossible?"
    (0.00, 2.05, "ibrahim-yacht-jump", 3.35, 0.6, 1.25, 0.55, 0.32, "day", "bw-open"),
    # the man saying it, in sync
    (2.05, 4.20, FILM, 2.57, 1.0, 1.75, 0.57, 0.42, "neon", ""),
    # the problem, in sync; the jump cut is hidden by a 1.4x change of framing
    (4.20, 7.48, MIAMI, 2.24, 1.0, 1.55, 0.56, 0.56, "warm", ""),
    (7.48, 9.25, MIAMI, 12.97, 1.0, 2.15, 0.55, 0.58, "warm", ""),
    # "This is the most honest conversation..." in sync, then L-cut into the discipline
    (9.25, 11.40, FILM, 9.24, 1.0, 1.75, 0.60, 0.42, "neon", ""),
    (11.40, b(-9), "ibrahim-waking-up", 1.35, 1.0, 1.25, 0.48, 0.58, "dawn", ""),
    (b(-9), b(-7), "ibrahim-praying", 22.6, 1.0, 1.15, 0.50, 0.62, "night", ""),
    (b(-7), b(-6), "ibrahim-running-2", 8.4, 1.0, 1.0, 0.50, 0.50, "day", ""),
    (b(-6), b(-5), "ibrahim-pulldown", 11.2, 1.0, 1.05, 0.50, 0.45, "warm", ""),
    (b(-5), h(-5), "ibrahim-clap-pushups", 14.0, 1.0, 1.0, 0.50, 0.50, "warm", ""),
    (h(-5), b(-4), "cold-plunge-ibrahim", 2.2, 1.0, 1.1, 0.50, 0.45, "day", ""),
    (b(-4), b(-3), "ibrahim-night-work", 6.0, 1.0, 1.1, 0.55, 0.45, "neon", ""),
    # proof, punched until the number reads on a phone
    (b(-3), b(-2), "stripe-payment-2", 0.6, 1.0, 2.6, 0.27, 0.86, "night", ""),
    (b(-2), h(-1), "stripe-payment", 0.05, 1.0, 2.3, 0.54, 0.53, "night", ""),
    # (h(-1) → DROP: half a beat of black and silence)
    # DROP: "10 million dollars in valuations going up."
    (b(0), b(2), "jetski-takeoff", 5.3, 1.0, 1.1, 0.48, 0.55, "day", "ramp"),
    (b(2), b(3), "ibrahim-atv-desert", 4.0, 1.0, 1.0, 0.50, 0.50, "golden", ""),
    (b(3), b(6), "ibrahim-desert-eagle", 6.9, 0.5, 1.12, 0.50, 0.45, "golden", ""),
    (b(6), h(6), "ibrahim-wakesurfing", 6.0, 1.0, 1.15, 0.50, 0.40, "day", ""),
    (h(6), b(7), "jetski-spin", 3.9, 1.0, 1.15, 0.50, 0.50, "day", ""),
    (b(7), 23.985, "rolls-royce-inside", 1.0, 1.0, 1.0, 0.50, 0.50, "night", ""),
    # "And now we're launching another software company", in sync, then his night
    (23.985, b(10), POD, 7.63, 1.0, 1.7, 0.27, 0.52, "day", ""),
    (b(10), 27.55, "ibrahim-cigar", 2.0, 1.0, 1.05, 0.50, 0.45, "night", ""),
    # "Lock in boys, lock in. Let's go." (the selfie; its first 0.6 s of audio plays under the last cigar frames)
    (27.55, END, SELFIE, 0.60, 1.0, 1.25, 0.45, 0.45, "day", ""),  # in sync with V7 (placed 26.95)
]

LEAKS = [4.20, 9.25, 11.40]   # light-leak / prism-streak transitions (3 frames), as in ref1
