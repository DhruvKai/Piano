"""Generate the keyboard diagrams for Glossary/Extended Chords.md.

Reuses gen_song_svgs.render (real octave-numbered note ranges, middle C = C4).
Every chord is built on C so the shapes are easy to compare. Badges show the
chord degree (R, 3, ♭7, 9 ...) instead of a playing order; a grey badge marks a
note that is usually left out when the chord is actually played.

Usage: python Scripts/gen_extended_chord_svgs.py          (writes every diagram)
"""
import os

from gen_song_svgs import render, write, GREEN, BLUE, LH_COL, RH_COL

GREY = "#9aa5ad"
CORE_COL, EXT_COL = "#2c6fbb", "#c9622a"
ASSETS = os.path.join("Assets", "Glossary", "Extended Chords")
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Semitones above the root. Extensions (9/11/13 and their alterations) sit in
# the second octave, which is exactly why they get numbers above 8.
SEMIS = {
    "R": 0, "2": 2, "♭3": 3, "3": 4, "4": 5, "♭5": 6, "5": 7, "#5": 8,
    "6": 9, "♭♭7": 9, "♭7": 10, "7": 11,
    "♭9": 13, "9": 14, "#9": 15, "11": 17, "#11": 18, "♭13": 20, "13": 21,
}


def note(deg, root=0, octave=4):
    s = root + SEMIS[deg]
    return f"{NAMES[s % 12]}{octave + s // 12}"


def badge(deg, root=0, octave=4, omit=()):
    fill = GREY if deg in omit else GREEN if deg == "R" else BLUE
    return (note(deg, root, octave), deg, fill)


def spelled(degs):
    return " ".join(note(d)[:-1] for d in degs)


# ------------------------------------------------------------- 7th / 6th / sus
# (file stem, symbol, degrees, label for the note(s) on top of the triad)
SMALL = [
    ("maj7", "Cmaj7", ["R", "3", "5", "7"], "7th"),
    ("7", "C7", ["R", "3", "5", "♭7"], "7th"),
    ("m7", "Cm7", ["R", "♭3", "5", "♭7"], "7th"),
    ("m7b5", "Cm7♭5 (Cø)", ["R", "♭3", "♭5", "♭7"], "7th"),
    ("dim7", "Cdim7 (C°7)", ["R", "♭3", "♭5", "♭♭7"], "7th"),
    ("m-maj7", "Cm(maj7)", ["R", "♭3", "5", "7"], "7th"),
    ("6", "C6", ["R", "3", "5", "6"], "6th"),
    ("m6", "Cm6", ["R", "♭3", "5", "6"], "6th"),
    ("sus2", "Csus2", ["R", "2", "5"], None),
    ("sus4", "Csus4", ["R", "4", "5"], None),
    ("7sus4", "C7sus4", ["R", "4", "5", "♭7"], "7th"),
]


def small(symbol, degs, top):
    brackets = (("triad", CORE_COL, "C4", "G4"), (top, EXT_COL, "A4", "B4")) if top else ()
    return render(
        "C4", "C5", f"{symbol} — {spelled(degs)}",
        [("Formula", CORE_COL, " ".join(degs))],
        brackets,
        [badge(d) for d in degs],
        ["Badges = chord degree, not playing order. Green = root."],
        r=13)


# ------------------------------------------------------------ 9th / 11th / 13th
# (file stem, symbol, degrees, degrees usually left out, core bracket label)
BIG = [
    ("add9", "Cadd9", ["R", "3", "5", "9"], (), "triad"),
    ("m-add9", "Cm(add9)", ["R", "♭3", "5", "9"], (), "triad"),
    ("6-9", "C6/9", ["R", "3", "5", "6", "9"], (), "6 chord"),
    ("maj9", "Cmaj9", ["R", "3", "5", "7", "9"], ("5",), "maj7 chord"),
    ("9", "C9", ["R", "3", "5", "♭7", "9"], ("5",), "dominant 7 chord"),
    ("m9", "Cm9", ["R", "♭3", "5", "♭7", "9"], ("5",), "m7 chord"),
    ("11", "C11", ["R", "3", "5", "♭7", "9", "11"], ("3", "5"), "dominant 7 chord"),
    ("m11", "Cm11", ["R", "♭3", "5", "♭7", "9", "11"], ("5",), "m7 chord"),
    ("maj7-sharp11", "Cmaj7#11", ["R", "3", "5", "7", "9", "#11"], ("5",), "maj7 chord"),
    ("7-sharp11", "C7#11", ["R", "3", "5", "♭7", "9", "#11"], ("5",), "dominant 7 chord"),
    ("13", "C13", ["R", "3", "5", "♭7", "9", "11", "13"], ("5", "11"), "dominant 7 chord"),
    ("maj13", "Cmaj13", ["R", "3", "5", "7", "9", "11", "13"], ("5", "11"), "maj7 chord"),
    ("m13", "Cm13", ["R", "♭3", "5", "♭7", "9", "11", "13"], ("5",), "m7 chord"),
    ("7b9", "C7♭9", ["R", "3", "5", "♭7", "♭9"], ("5",), "dominant 7 chord"),
    ("7-sharp9", "C7#9", ["R", "3", "5", "♭7", "#9"], ("5",), "dominant 7 chord"),
    ("7b13", "C7♭13", ["R", "3", "5", "♭7", "♭13"], ("5",), "dominant 7 chord"),
]


def big(symbol, degs, omit, core):
    played = [d for d in degs if d not in omit]
    cap = "Badges = chord degree, not playing order. Green = root."
    if omit:
        cap += " Grey = usually left out."
    return render(
        "C4", "C6", f"{symbol} — {spelled(degs)}",
        [("Formula", CORE_COL, " ".join(degs)), ("Usually played", EXT_COL, spelled(played))],
        ((core, CORE_COL, "C4", "B4"), ("extensions (2nd octave)", EXT_COL, "C5", "B5")),
        [badge(d, omit=omit) for d in degs],
        [cap, "Every note stacked in thirds to show the theory — not a hand shape. See the note for voicings."],
        r=13)


# --------------------------------------------------------------- concept charts
def degree_numbers():
    whites = [f"{l}{o}" for o in (4, 5) for l in "CDEFGAB"] + ["C6"]
    return render(
        "C4", "C6", "Counting past the octave: 9 = 2, 11 = 4, 13 = 6",
        [("Same key, octave up", EXT_COL, "9 = D · 11 = F · 13 = A")],
        (("1st octave", CORE_COL, "C4", "B4"), ("2nd octave", EXT_COL, "C5", "C6")),
        [(n, str(i), GREEN if i in (1, 8, 15) else BLUE) for i, n in enumerate(whites, 1)],
        ["Keep counting the C major scale past 8 instead of starting again at 1.",
         "Extensions are just 2, 4 and 6 played an octave higher. Green = C."],
        r=13)


def stacking_thirds():
    degs = ["R", "3", "5", "7", "9", "11", "13"]
    return render(
        "C4", "C6", "Stacking thirds — skip every other white key",
        [("C major scale, every 2nd note", CORE_COL, spelled(degs))],
        (("triad + 7th", CORE_COL, "C4", "B4"), ("extensions", EXT_COL, "C5", "B5")),
        [badge(d) for d in degs],
        ["Triad = 3 notes, 7th chord = 4, 9th = 5, 11th = 6, 13th = 7 — then you're back on C.",
         "Badges = chord degree. Green = root."],
        r=13)


# ------------------------------------------------- ii–V–I with rootless voicings
# LH plays the root; RH plays 4 notes without the root (3rd/7th + colour tones).
II_V_I = [
    ("ii-v-i-1-dm9", "1. Dm9 (ii)", "D3", [("F4", "♭3"), ("A4", "5"), ("C5", "♭7"), ("E5", "9")],
     "Each RH key either stays put or moves one step into the next chord."),
    ("ii-v-i-2-g13", "2. G13 (V)", "G3", [("F4", "♭7"), ("A4", "9"), ("B4", "3"), ("E5", "13")],
     "From Dm9 only one RH key moves: C → B. Root G in LH."),
    ("ii-v-i-3-cmaj9", "3. Cmaj9 (I)", "C3", [("E4", "3"), ("G4", "5"), ("B4", "7"), ("D5", "9")],
     "From G13 every RH key slides down to its nearest chord tone."),
]


def ii_v_i(title, lh, rh, cap):
    for n, d in rh:  # the hand-picked voicing must really be these degrees
        assert note(d, NAMES.index(lh[:-1]))[:-1] == n[:-1], (title, n, d)
    return render(
        "C3", "E5", f"ii–V–I in C · {title}",
        [("LH", LH_COL, lh[:-1]), ("RH", RH_COL, " ".join(n[:-1] for n, _ in rh))],
        (("LH — root", LH_COL, "C3", "B3"), ("RH — rootless voicing", RH_COL, "C4", "E5")),
        [(lh, "R", GREEN)] + [(n, d, BLUE) for n, d in rh],
        [cap, "Badges = chord degree. Green = root (LH). RH fingers 1-2-3-5 or 1-2-4-5, low to high."],
        r=13)


def main():
    write(os.path.join(ASSETS, "extended-degree-numbers.svg"), degree_numbers())
    write(os.path.join(ASSETS, "extended-stacking-thirds.svg"), stacking_thirds())
    for stem, symbol, degs, top in SMALL:
        write(os.path.join(ASSETS, f"chord-c-{stem}.svg"), small(symbol, degs, top))
    for stem, symbol, degs, omit, core in BIG:
        write(os.path.join(ASSETS, f"chord-c-{stem}.svg"), big(symbol, degs, omit, core))
    for stem, title, lh, rh, cap in II_V_I:
        write(os.path.join(ASSETS, f"{stem}.svg"), ii_v_i(title, lh, rh, cap))


if __name__ == "__main__":
    main()
