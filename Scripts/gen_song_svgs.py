"""Generate the keyboard diagrams for single-song tutorials under Songs/.

Same look as gen_arpeggio_svgs.py (40x180 white keys, 24x110 black keys,
numbered badges overlapping the bottom of each key, opaque background), but
the window is given as a real note range with octave numbers (middle C = C4),
since song parts land on black keys and span specific octaves.

Notes are written sharp-only, e.g. "C#5". Middle C gets a small marker under
its key so the octave is easy to find on a real keyboard.

Usage: python Scripts/gen_song_svgs.py          (writes every diagram)
"""
import os

LETTERS = "CDEFGAB"
HAS_SHARP = set("CDFGA")  # black key after these whites, never after E/B

WK_W, WK_H, BK_W, BK_H = 40, 180, 24, 110
PAD = 10
KB_Y = 96
R = 10
GREEN, BLUE = "#3a8f5c", "#2c6fbb"
LH_COL, RH_COL = "#c9622a", "#3a8f5c"
ASSETS = os.path.join("Assets", "Songs")


def parse(note):
    """'C#5' -> ('C', True, 5)."""
    return note[0], note[1] == "#", int(note[-1])


def whites_between(lo, hi):
    """White keys from lo to hi inclusive, both white-key names like 'C5'."""
    l, _, o = parse(lo)
    i, out = LETTERS.index(l), []
    while True:
        out.append(f"{LETTERS[i]}{o}")
        if out[-1] == hi:
            return out
        i += 1
        if i == 7:
            i, o = 0, o + 1


def render(lo, hi, title, lines, brackets, badges, captions):
    """badges: list of (note, label, is_green); a key with several badges stacks them upward."""
    whites = whites_between(lo, hi)
    n_white = len(whites)
    W = n_white * WK_W + 2 * PAD
    H = KB_Y + WK_H + 62 + (14 if "C4" in whites else 0)  # room for the middle C marker

    def x_of(note):
        """Centre x of a key, relative to the keyboard group."""
        l, sharp, o = parse(note)
        i = whites.index(f"{l}{o}")
        return PAD + (i + 1) * WK_W if sharp else PAD + i * WK_W + WK_W / 2

    def bottom_of(note):
        return BK_H if parse(note)[1] else WK_H

    stacks = {}
    for note, label, green in badges:
        assert note in whites or (parse(note)[1] and parse(note)[0] in HAS_SHARP
                                  and f"{note[0]}{note[-1]}" in whites[:-1]), note
        stacks.setdefault(note, []).append((label, green))

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif">',
         f'  <rect width="{W}" height="{H}" fill="#fafafa"/>',
         f'  <text x="{W/2:g}" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#243447">{title}</text>']
    parts = "   ".join(f'<tspan fill="{col}" font-weight="bold">{label}:</tspan> {text}' for label, col, text in lines)
    o.append(f'  <text x="{W/2:g}" y="44" text-anchor="middle" font-size="12" fill="#243447">{parts}</text>')
    for label, col, a, b in brackets:
        xa, xb = x_of(a) - WK_W / 2 + 4, x_of(b) + WK_W / 2 - 4
        y = KB_Y - 10
        o.append(f'  <path d="M{xa:g} {y+6} V{y} H{xb:g} V{y+6}" fill="none" stroke="{col}" stroke-width="2"/>')
        o.append(f'  <text x="{(xa+xb)/2:g}" y="{y-6}" text-anchor="middle" font-size="12" font-weight="bold" fill="{col}">{label}</text>')

    o.append(f'  <g transform="translate(0,{KB_Y})">')
    o.append('    <g stroke="#333" stroke-width="1.5">')
    o.append("      " + "".join(f'<rect x="{PAD + i*WK_W}" y="0" width="{WK_W}" height="{WK_H}" fill="#ffffff"/>'
                                for i in range(n_white)))
    o.append('    </g>')
    o.append('    <g stroke="#000" stroke-width="1" fill="#222222">')
    o.append("      " + "".join(f'<rect x="{PAD + (i+1)*WK_W - BK_W//2}" y="0" width="{BK_W}" height="{BK_H}"/>'
                                for i, n in enumerate(whites) if n[0] in HAS_SHARP and i < n_white - 1))
    o.append('    </g>')
    circles, labels = [], []
    for note, items in stacks.items():
        x = x_of(note)
        for k, (label, green) in enumerate(items):
            cy = bottom_of(note) - 14 - k * (2 * R + 2)
            circles.append(f'<circle cx="{x:g}" cy="{cy}" r="{R}" fill="{GREEN if green else BLUE}" stroke="#ffffff" stroke-width="1"/>')
            labels.append(f'<text x="{x:g}" y="{cy + 4}">{label}</text>')
    o.append('    <g>')
    o.append("      " + "".join(circles))
    o.append('    </g>')
    o.append('    <g fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">')
    o.append("      " + "".join(labels))
    o.append('    </g>')
    o.append('    <g fill="#888" font-size="12" text-anchor="middle">')
    o.append("      " + "".join(f'<text x="{PAD + i*WK_W + WK_W/2:g}" y="{WK_H + 16}">{n[0]}</text>'
                                for i, n in enumerate(whites)))
    o.append('    </g>')
    if "C4" in whites:
        x = x_of("C4")
        o.append(f'    <text x="{x:g}" y="{WK_H + 30}" text-anchor="middle" font-size="9" font-weight="bold" fill="#c9622a">middle C</text>')
    o.append('  </g>')
    for k, cap in enumerate(captions):
        y = H - 10 - 14 * (len(captions) - 1 - k)
        o.append(f'  <text x="{W/2:g}" y="{y}" text-anchor="middle" font-size="10" fill="#52616b">{cap}</text>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


# ------------------------------------------------- Clash Royale Intro (Amosdoll Music)
# Notes read off the video's lit keys (frame-by-frame) and cross-checked with the narration.
CR_RIFF_LH = ["C#5", "F#5", "G#5"]
CR_RIFF_RH = ["C#6", "F6"]
CR_MELODY = ["A#4", "A4", "F4", "G4", "D5", "C5"]
CR_DS_MAJOR = ["D#3", "G3", "A#3"]
CR_C_MAJOR = ["C3", "E3", "G3"]


def cr_riff():
    notes = CR_RIFF_LH + CR_RIFF_RH
    return render(
        "C5", "G6", "Part 1 — The Iconic Riff (rolled, then held)",
        [("LH", LH_COL, "C# F# G#"), ("then RH", RH_COL, "C# F")],
        (("LH", LH_COL, "C5", "G#5"), ("RH", RH_COL, "C#6", "F6")),
        [(n, str(i), i == 1) for i, n in enumerate(notes, 1)],
        ["Starts on the C# one octave above middle C. Play 1→5 one after another, evenly,",
         "keep every key held down so the notes ring together. Green = start note."])


def cr_melody():
    return render(
        "C4", "E5", "Part 2 — RH Melody",
        [("RH", RH_COL, " → ".join(n[:-1] for n in CR_MELODY))],
        (),
        [(n, str(i), i == 1) for i, n in enumerate(CR_MELODY, 1)],
        ["Starts on the A# just above middle C. Numbers = playing order",
         "(the tune jumps around, so it doesn't read left-to-right). Green = start note."])


def cr_chord(notes, name):
    return render(
        "C3", "C4", f"Part 2 — LH {name} Chord",
        [("LH", LH_COL, " + ".join(n[:-1] for n in notes) + "  (press together)")],
        (),
        [(n, lab, lab == "1") for n, lab in zip(notes, ("1", "3", "5"))],
        ["The octave just below middle C. Badges = chord tones: 1 = root (green), 3 = 3rd, 5 = 5th.",
         "All three keys go down at the same time."])


def write(path, svg):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(path)


def main():
    d = os.path.join(ASSETS, "Clash Royale Intro")
    write(os.path.join(d, "clash-royale-riff.svg"), cr_riff())
    write(os.path.join(d, "clash-royale-melody.svg"), cr_melody())
    write(os.path.join(d, "clash-royale-ds-major.svg"), cr_chord(CR_DS_MAJOR, "D# Major"))
    write(os.path.join(d, "clash-royale-c-major.svg"), cr_chord(CR_C_MAJOR, "C Major"))


if __name__ == "__main__":
    main()
