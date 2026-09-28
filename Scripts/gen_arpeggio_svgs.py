"""Generate the keyboard diagrams for Lesson 07 (Basic) and Lesson 08 (Advanced) Arpeggios.

Every diagram is a 12-white-key window starting at the root. Each step of the
pattern gets a number; every note played in that step gets a badge with that
number overlapping the bottom of its key, and a key played again stacks its
badges upward. Notes grouped in ( ) share one step number.

  Lesson 07: LH on the lower root..5th, RH on the octave above.
  Lesson 08: LH only; the lower octave is the normal octave, the upper one is
             the source's red "play an octave higher" notes (written C' etc.).

Usage: python Scripts/gen_arpeggio_svgs.py          (writes every diagram)
"""
import os

LETTERS = "CDEFGAB"
HAS_SHARP = set("CDFGA")  # black key after these whites, never after E/B

WK_W, WK_H, BK_W, BK_H = 40, 180, 24, 110
N_WHITE = 12
PAD = 10
KB_Y = 96
R = 10
W = N_WHITE * WK_W + 2 * PAD
H = KB_Y + WK_H + 62
GREEN, BLUE = "#3a8f5c", "#2c6fbb"
LH_COL, RH_COL, HIGH_COL = "#c9622a", "#3a8f5c", "#d64545"
ASSETS = os.path.join("Assets", "PIX Series YouTube Course")


def letter(root, deg):
    return LETTERS[(LETTERS.index(root) + deg) % 7]


def cx(tile):
    return PAD + tile * WK_W + WK_W / 2


def render(root, title, lines, brackets, events, captions):
    """events: list of steps, each a list of tiles (0 = root) played in that step."""
    whites = [letter(root, i) for i in range(N_WHITE)]
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
                                for i in range(N_WHITE)))
    o.append('    </g>')
    o.append('    <g stroke="#000" stroke-width="1" fill="#222222">')
    o.append("      " + "".join(f'<rect x="{PAD + (i+1)*WK_W - BK_W//2}" y="0" width="{BK_W}" height="{BK_H}"/>'
                                for i, n in enumerate(whites) if n in HAS_SHARP and i < N_WHITE - 1))
    o.append('    </g>')
    circles, labels = [], []
    for tile, steps in sorted(badges.items()):
        fill = GREEN if whites[tile] == root else BLUE
        for k, s in enumerate(steps):
            cy = WK_H - 14 - k * (2 * R + 2)
            circles.append(f'<circle cx="{cx(tile):g}" cy="{cy}" r="{R}" fill="{fill}" stroke="#ffffff" stroke-width="1"/>')
            labels.append(f'<text x="{cx(tile):g}" y="{cy + 4}">{s}</text>')
    o.append('    <g>')
    o.append("      " + "".join(circles))
    o.append('    </g>')
    o.append('    <g fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">')
    o.append("      " + "".join(labels))
    o.append('    </g>')
    o.append('    <g fill="#888" font-size="12" text-anchor="middle">')
    o.append("      " + "".join(f'<text x="{cx(i):g}" y="{WK_H + 16}">{n}</text>' for i, n in enumerate(whites)))
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


def l07_arp1(ex, root):
    rh = L07_ARP1[ex][0]
    lh_notes = [letter(root, d) for d in L07_LH]
    rh_notes = [letter(root, d) for d in rh]
    if (ex, root) in L07_TABLE:
        assert L07_TABLE[(ex, root)] == ("-".join(lh_notes), "-".join(rh_notes)), (ex, root)
    return render(
        root, f"Arpeggio 1 · Exercise {ex} — {root}",
        [("LH", LH_COL, " ".join(lh_notes), cx(2)), ("RH", RH_COL, " ".join(rh_notes), cx(9))],
        L07_BRACKETS,
        [[l, RH_OFF + r] for l, r in zip(L07_LH, rh)],
        ["Numbers = playing order; stacked badges = same key played again.",
         "Same number in LH &amp; RH = play together. Green = root."])


def l07_arp2(root):
    n = lambda d: letter(root, d)
    return render(
        root, f"Arpeggio 2 — {root}",
        [("LH", LH_COL, f"{n(0)} ({n(2)} {n(4)}) ({n(2)} {n(4)})", cx(2)),
         ("RH", RH_COL, f"{n(0)} {n(1)} {n(2)}", cx(9))],
        L07_BRACKETS,
        [[0, RH_OFF + 0], [2, 4, RH_OFF + 1], [2, 4, RH_OFF + 2]],
        ["Numbers = playing order. Notes in ( ) are grouped and share one number.",
         "Same number in LH &amp; RH = play together. Green = root."])


# ---------------------------------------------------------------- Lesson 08
# Straight from the Lesson 8 PDF; ' = a red note (one octave higher).
L08 = {
    1: ("4/4", "C G C' G E' G C' G"),
    2: ("4/4", "C (G C') C (G C') C (G C') (G C') C (G C')"),
    3: ("4/4", "C (G C') (G C') (C' E' G') (G C')"),
    4: ("3/4", "C (G C') (G C') (C' E' G') (G C')"),
}


def parse_l08(pattern):
    """'C (G C') E' ...' -> list of steps, each a list of tiles (C = 0, ' = +7)."""
    steps, group = [], None
    for tok in pattern.replace("(", " ( ").replace(")", " ) ").split():
        if tok == "(":
            group = []
        elif tok == ")":
            steps.append(group)
            group = None
        else:
            tile = LETTERS.index(tok[0]) + (7 if tok.endswith("'") else 0)
            if group is None:
                steps.append([tile])
            else:
                group.append(tile)
    return steps


def l08(n):
    time_sig, pattern = L08[n]
    return render(
        "C", f"Advanced Arpeggio {n} — C chord · {time_sig}",
        [("LH", LH_COL, pattern.replace("'", "′"), W / 2)],
        (("Normal octave", LH_COL, 0, 4), ("Octave higher (′ = red in PDF)", HIGH_COL, 7, 11)),
        parse_l08(pattern),
        ["Numbers = playing order; stacked badges = same key played again.",
         "Notes in ( ) are grouped and share one number. LH only. Green = root."])


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
    for n in L08:
        write(os.path.join(ASSETS, "Lesson 08", f"lesson08-arp{n}.svg"), l08(n))


if __name__ == "__main__":
    main()
