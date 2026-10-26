"""Generate the keyboard diagrams for Lesson 07 (Basic) and Lesson 08 (Advanced) Arpeggios.

Each step of the pattern gets a number; every note played in that step gets a badge with that
number overlapping the bottom of its key, and a key played again stacks its
badges upward. Notes grouped in ( ) share one step number.

  Lesson 07: 12 white keys from the root. LH on the lower root..5th, RH on
             the octave above.
  Lesson 08: 13 white keys from the root (from the white key below a black
             root). LH only; the lower octave is the normal octave, the upper
             one is the source's red "play an octave higher" notes (written C′).
             The C-chord patterns are moved to all 12 roots, in major and minor
             wherever the pattern uses the 3rd.

Usage: python Scripts/gen_arpeggio_svgs.py          (writes every diagram)
"""
import os
import re

LETTERS = "CDEFGAB"
HAS_SHARP = set("CDFGA")  # black key after these whites, never after E/B

WK_W, WK_H, BK_W, BK_H = 40, 180, 24, 110
N_WHITE = 12
PAD = 10
KB_Y = 96
R = 10
W = N_WHITE * WK_W + 2 * PAD
H = KB_Y + WK_H + 86  # room for note names, the finger row and 3 caption lines
GREEN, BLUE = "#3a8f5c", "#2c6fbb"
LH_COL, RH_COL, HIGH_COL = "#c9622a", "#3a8f5c", "#d64545"
ASSETS = os.path.join("Assets", "PIX Series YouTube Course")


def letter(root, deg):
    return LETTERS[(LETTERS.index(root) + deg) % 7]


def cx(pos):
    """Centre x of a key: white tile i, or i + 0.5 for the black key after it."""
    return PAD + pos * WK_W + WK_W / 2


def render(whites, title, lines, brackets, events, captions, fingers, roots, black_names=None):
    """events: list of steps, each a list of key positions played in that step
    (white tile i, or i + 0.5 for the black key after it).
    fingers: {pos: (finger label, colour)}, drawn in a row under the note names.
    roots: positions whose badges are green. black_names: {pos: name} printed in
    the note-name row for the black keys that are used."""
    n_white = len(whites)
    W = n_white * WK_W + 2 * PAD
    badges = {}
    for step, tiles in enumerate(events, 1):
        for t in tiles:
            badges.setdefault(t, []).append(step)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif">',
         f'  <rect width="{W}" height="{H}" fill="#fafafa"/>',
         f'  <text x="{W/2:g}" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#243447">{title}</text>']
    for label, col, text, x in lines:
        o.append(f'  <text x="{x:g}" y="44" text-anchor="middle" font-size="12" fill="#243447">'
                 f'<tspan fill="{col}" font-weight="bold">{label}:</tspan> {text}</text>')
    for label, col, t0, t1 in brackets:
        xa, xb = PAD + t0 * WK_W + 4, PAD + (t1 + 1) * WK_W - 4
        y = KB_Y - 10
        o.append(f'  <path d="M{xa} {y+6} V{y} H{xb} V{y+6}" fill="none" stroke="{col}" stroke-width="2"/>')
        o.append(f'  <text x="{(xa+xb)/2:g}" y="{y-6}" text-anchor="middle" font-size="12" font-weight="bold" fill="{col}">{label}</text>')

    o.append(f'  <g transform="translate(0,{KB_Y})">')
    o.append('    <g stroke="#333" stroke-width="1.5">')
    o.append("      " + "".join(f'<rect x="{PAD + i*WK_W}" y="0" width="{WK_W}" height="{WK_H}" fill="#ffffff"/>'
                                for i in range(n_white)))
    o.append('    </g>')
    o.append('    <g stroke="#000" stroke-width="1" fill="#222222">')
    o.append("      " + "".join(f'<rect x="{PAD + (i+1)*WK_W - BK_W//2}" y="0" width="{BK_W}" height="{BK_H}"/>'
                                for i, n in enumerate(whites) if n in HAS_SHARP and i < n_white - 1))
    o.append('    </g>')
    circles, labels = [], []
    for pos, steps in sorted(badges.items()):
        fill = GREEN if pos in roots else BLUE
        bottom = BK_H if pos % 1 else WK_H
        for k, s in enumerate(steps):
            cy = bottom - 14 - k * (2 * R + 2)
            circles.append(f'<circle cx="{cx(pos):g}" cy="{cy}" r="{R}" fill="{fill}" stroke="#ffffff" stroke-width="1"/>')
            labels.append(f'<text x="{cx(pos):g}" y="{cy + 4}">{s}</text>')
    o.append('    <g>')
    o.append("      " + "".join(circles))
    o.append('    </g>')
    o.append('    <g fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">')
    o.append("      " + "".join(labels))
    o.append('    </g>')
    o.append('    <g fill="#888" font-size="12" text-anchor="middle">')
    o.append("      " + "".join(f'<text x="{cx(i):g}" y="{WK_H + 16}">{n}</text>' for i, n in enumerate(whites)))
    o.append('    </g>')
    if black_names:
        o.append('    <g fill="#243447" font-size="10" font-weight="bold" text-anchor="middle">')
        o.append("      " + "".join(f'<text x="{cx(p):g}" y="{WK_H + 16}">{n}</text>' for p, n in sorted(black_names.items())))
        o.append('    </g>')
    o.append('    <g font-size="12" font-weight="bold" text-anchor="middle">')
    o.append("      " + "".join(f'<text x="{cx(t):g}" y="{WK_H + 33}" fill="{col}">{f}</text>'
                                for t, (f, col) in sorted(fingers.items())))
    o.append('    </g>')
    o.append('  </g>')
    for k, cap in enumerate(captions):
        y = H - 10 - 14 * (len(captions) - 1 - k)
        o.append(f'  <text x="{W/2:g}" y="{y}" text-anchor="middle" font-size="10" fill="#52616b">{cap}</text>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- Lesson 07
# Scale-degree offsets (0 = root), checked below against the lesson's tables.
L07_LH = [0, 2, 4, 2, 0, 2, 4, 2]
L07_ARP1 = {
    1: ([0, 1, 2, 3, 4, 3, 2, 1], "CDEFGAB"),
    2: ([0, 2, 1, 3, 2, 1, 0, 1], "CDEFG"),
    3: ([0, 4, 3, 2, 1, 0, 1, 2], "CDEF"),
}
L07_ARP2_ROOTS = "CDEFGAB"
L07_TABLE = {
    (1, "C"): ("C-E-G-E-C-E-G-E", "C-D-E-F-G-F-E-D"),
    (1, "B"): ("B-D-F-D-B-D-F-D", "B-C-D-E-F-E-D-C"),
    (2, "C"): ("C-E-G-E-C-E-G-E", "C-E-D-F-E-D-C-D"),
    (2, "G"): ("G-B-D-B-G-B-D-B", "G-B-A-C-B-A-G-A"),
    (3, "C"): ("C-E-G-E-C-E-G-E", "C-G-F-E-D-C-D-E"),
    (3, "F"): ("F-A-C-A-F-A-C-A", "F-C-B-A-G-F-G-A"),
}
L07_BRACKETS = (("LH", LH_COL, 0, 4), ("RH", RH_COL, 7, 11))
RH_OFF = 7  # RH plays one octave above the LH
# Not in the PDF: both hands stay in a five-finger position, so each key keeps
# one finger. LH 5-3-1 on root/3rd/5th; RH thumb on the root up to pinky on the 5th.
L07_LH_FINGER = {0: 5, 2: 3, 4: 1}
FINGER_CAPTION = "Coloured numbers under the keys = finger (1 = thumb … 5 = pinky), orange LH / green RH."


def l07_fingers(rh_degrees):
    f = {t: (str(n), LH_COL) for t, n in L07_LH_FINGER.items()}
    f.update({RH_OFF + d: (str(d + 1), RH_COL) for d in rh_degrees})
    return f


def l07_render(root, *args):
    """Lesson 07 window: 12 white keys from the root (all seven roots are white)."""
    return render([letter(root, i) for i in range(N_WHITE)], *args, {0, 7})


def l07_arp1(ex, root):
    rh = L07_ARP1[ex][0]
    lh_notes = [letter(root, d) for d in L07_LH]
    rh_notes = [letter(root, d) for d in rh]
    if (ex, root) in L07_TABLE:
        assert L07_TABLE[(ex, root)] == ("-".join(lh_notes), "-".join(rh_notes)), (ex, root)
    return l07_render(
        root, f"Arpeggio 1 · Exercise {ex} — {root}",
        [("LH", LH_COL, " ".join(lh_notes), cx(2)), ("RH", RH_COL, " ".join(rh_notes), cx(9))],
        L07_BRACKETS,
        [[l, RH_OFF + r] for l, r in zip(L07_LH, rh)],
        ["Numbers = playing order; stacked badges = same key played again.",
         "Same number in LH &amp; RH = play together. Green = root.", FINGER_CAPTION],
        l07_fingers(set(rh)))


def l07_arp2(root):
    n = lambda d: letter(root, d)
    return l07_render(
        root, f"Arpeggio 2 — {root}",
        [("LH", LH_COL, f"{n(0)} ({n(2)} {n(4)}) ({n(2)} {n(4)})", cx(2)),
         ("RH", RH_COL, f"{n(0)} {n(1)} {n(2)}", cx(9))],
        L07_BRACKETS,
        [[0, RH_OFF + 0], [2, 4, RH_OFF + 1], [2, 4, RH_OFF + 2]],
        ["Numbers = playing order. Notes in ( ) are grouped and share one number.",
         "Same number in LH &amp; RH = play together. Green = root.", FINGER_CAPTION],
        l07_fingers({0, 1, 2}))


# ---------------------------------------------------------------- Lesson 08
# Straight from the Lesson 8 PDF and video, written on the C chord:
# C = root, E = 3rd, G = 5th; ' = a red note (one octave higher).
# Patterns 3 and 4 are the same notes in 4/4 and 3/4, so they share one diagram.
L08 = {
    "1": ("Advanced Arpeggio 1", "4/4", "C G C' G E' G C' G"),
    "2": ("Advanced Arpeggio 2", "4/4", "C (G C') C (G C') C (G C') (G C') C (G C')"),
    "34": ("Advanced Arpeggio 3 (4/4) &amp; 4 (3/4)", None, "C (G C') (G C') (C' E' G') (G C')"),
}
# The video's "extended chord" (root, 5th, octave) has no 3rd, so it is the same
# for major and minor. Only the patterns that use the 3rd (E) need both versions.
L08_HAS_THIRD = {n for n, (_, _, p) in L08.items() if "E" in p}
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]  # sharp-only
THIRD = {"major": 4, "minor": 3}
L08_WHITES = 13  # enough for the 5th an octave up from any root
L08_W = L08_WHITES * WK_W + 2 * PAD
# Suggested LH fingering (not in the source), by pattern note: root 5, 5th 2,
# octave 1. Pattern 1 stretches the thumb up to the 3rd′; patterns 3/4 jump the
# hand up for the (C' E' G') triad (5-3-1), so C' is 1 in the (G C') groups but 5 there.
L08_FINGERS = {
    "1": {"C": "5", "G": "2", "C'": "1", "E'": "1"},
    "2": {"C": "5", "G": "2", "C'": "1"},
    "34": {"C": "5", "G": "2", "C'": "1/5", "E'": "3", "G'": "1"},
}


def semis(tok, third):
    """'E'' -> semitones above the root (3rd = 4 major / 3 minor, ' = +12)."""
    return {"C": 0, "E": third, "G": 7}[tok[0]] + (12 if tok.endswith("'") else 0)


def spell(root, s, prime=True):
    return NAMES[(NAMES.index(root) + s) % 12] + ("′" if prime and s >= 12 else "")


def l08_line(pattern, root, third):
    """Rewrite the C-chord pattern for root, keeping ( ) and the primes."""
    return re.sub(r"[CEG]'?", lambda m: spell(root, semis(m.group(), third)), pattern)


def l08_steps(pattern, third):
    """'C (G C') E' ...' -> list of steps, each a list of semitone offsets."""
    steps, group = [], None
    for tok in pattern.replace("(", " ( ").replace(")", " ) ").split():
        if tok == "(":
            group = []
        elif tok == ")":
            steps.append(group)
            group = None
        elif group is None:
            steps.append([semis(tok, third)])
        else:
            group.append(semis(tok, third))
    return steps


def l08_keys(root):
    """White keys from the root (from the white key just below a black root), and
    the position of every key in chromatic order counting from the root."""
    whites = [letter(root[0], i) for i in range(L08_WHITES)]
    chroma = []
    for i, n in enumerate(whites):
        chroma.append(i)
        if n in HAS_SHARP and i < L08_WHITES - 1:
            chroma.append(i + 0.5)
    return whites, chroma[len(root) - 1:]


def l08_file(n, root, quality):
    slug = root[0].lower() + ("-sharp" if root.endswith("#") else "")
    return f"lesson08-arp{n}-{slug}" + (f"-{quality}" if quality else "") + ".svg"


def l08(n, root, quality):
    name, time_sig, pattern = L08[n]
    third = THIRD.get(quality, 0)
    whites, pos = l08_keys(root)
    steps = l08_steps(pattern, third)
    used = {s for step in steps for s in step}
    octave = int(pos[12])  # white tile of (or just below) the octave
    chord = f"{root} {quality}" if quality else f"{root} (major = minor)"
    return render(
        whites, f"{name} — {chord}" + (f" · {time_sig}" if time_sig else ""),
        [("LH", LH_COL, l08_line(pattern, root, third), L08_W / 2)],
        (("Normal octave", LH_COL, 0, octave - 1), ("Octave higher (′ = red in the video)", HIGH_COL, octave, L08_WHITES - 1)),
        [[pos[s] for s in step] for step in steps],
        ["Numbers = playing order; stacked badges = same key played again.",
         "Notes in ( ) are grouped and share one number. LH only. Green = root.",
         "Orange numbers under the keys = LH finger (1 = thumb … 5 = pinky)."],
        {pos[semis(t, third)]: (f, LH_COL) for t, f in L08_FINGERS[n].items()},
        {pos[0], pos[12]},
        {pos[s]: spell(root, s, prime=False) for s in used if pos[s] % 1})


# The C pattern from the PDF, and the C# major slide from the video.
assert l08_line(L08["1"][2], "C", 4) == "C G C′ G E′ G C′ G"
assert l08_line(L08["1"][2], "C#", 4) == "C# G# C#′ G# F′ G# C#′ G#"


def write(path, svg):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(path)


def main():
    d07 = os.path.join(ASSETS, "Lesson 07")
    for ex, (_, roots) in L07_ARP1.items():
        for root in roots:
            write(os.path.join(d07, f"lesson07-arp1-ex{ex}-{root.lower()}.svg"), l07_arp1(ex, root))
    for root in L07_ARP2_ROOTS:
        write(os.path.join(d07, f"lesson07-arp2-{root.lower()}.svg"), l07_arp2(root))
    d08 = os.path.join(ASSETS, "Lesson 08")
    for root in NAMES:
        for n in L08:
            for quality in (("major", "minor") if n in L08_HAS_THIRD else (None,)):
                write(os.path.join(d08, l08_file(n, root, quality)), l08(n, root, quality))


if __name__ == "__main__":
    main()
