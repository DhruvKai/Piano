---
title: Remembering Chord Notes
type: concept
tags: [glossary, chords, practice, mnemonic]
---
# Remembering Chord Notes — the 1-5-8 / 1-4-8 Trick

A counting shortcut for figuring out any [[Chord|triad]]'s three notes without recalling "4 semitones then 3" from memory: **count keys instead of semitones.**

> [!info] Verified
> Checked below against [[Chord]]'s interval table and against every already-verified note list in [[Lesson 05 - Chords]] — all match exactly. See the [Verification](#verification) section for the arithmetic and four worked examples.

## The trick

Starting on the root, **count every key going up — white and black, no skipping** — and call the root "1":

- **Major triad = positions 1, 5, 8.**
- **Minor triad = positions 1, 4, 8.**

Only the middle number changes. The root (1) and the fifth (8) are in the exact same place for both — the *only* thing that moves between a chord's major and minor version is that middle count, 5 vs. 4. That's the same "only the 3rd moves" fact from [[Remembering Chord Fingering]], just counted a different way.

### Worked example — C

![[Assets/Glossary/chord-trick-major-c.svg]]

C(1) · C#(2) · D(3) · D#(4) · E(**5**) · F(6) · F#(7) · G(**8**) → **C major = C, E, G** ✓

![[Assets/Glossary/chord-trick-minor-c.svg]]

C(1) · C#(2) · D(3) · D#(**4**) · E(5) · F(6) · F#(7) · G(**8**) → **C minor = C, D#, G** ✓

## Why this works — the verification

[[Chord]] already establishes the real intervals:

| Triad | Root → 3rd | 3rd → 5th | Root → 5th |
|---|---|---|---|
| Major | 4 semitones | 3 semitones | 7 semitones |
| Minor | 3 semitones | 4 semitones | 7 semitones |

Counting **keys** starting the root at "1" is the same thing as counting **semitones** starting the root at "0" — position *N* is always `N − 1` semitones above the root, because the root itself takes up slot 1 without being a step away from itself.

So:
- Major 3rd = 4 semitones above root = position `4 + 1 = 5` ✓ matches "1-5-8"
- Minor 3rd = 3 semitones above root = position `3 + 1 = 4` ✓ matches "1-4-8"
- Perfect 5th (same for both) = 7 semitones above root = position `7 + 1 = 8` ✓ matches the "8" in both

The trick is exactly the interval table above, just reframed as "which key do I land on" instead of "how many steps do I take" — arguably easier to do by eye on the keyboard, since you're pointing at physical keys instead of holding a running semitone count in your head.

### Two more worked examples, including a black-key root

To confirm the trick isn't a C-major coincidence, here it is starting from F# (a black key) and from G minor — both cross-checked against [[Lesson 05 - Chords]]'s already-verified note lists:

![[Assets/Glossary/chord-trick-major-f-sharp.svg]]

F#(1) · G(2) · G#(3) · A(4) · A#(**5**) · B(6) · C(7) · C#(**8**) → **F# major = F#, A#, C#** ✓ matches [[Lesson 05 - Chords#F# Major]]

![[Assets/Glossary/chord-trick-minor-g.svg]]

G(1) · G#(2) · A(3) · A#(**4**) · B(5) · C(6) · C#(7) · D(**8**) → **G minor = G, A#, D** ✓ matches [[Lesson 05 - Chords#G Minor]]

All four examples land exactly on the note lists already documented in [[Lesson 05 - Chords]] and [[Gold Silver Bronze Chords]] — the trick checks out for both a white-key and a black-key root, and for both chord qualities.

## Using it at the keyboard

1. Put your thumb on the root and silently count it as **"1."**
2. Walk one key at a time — **every** key, white or black — counting **2, 3, 4...** as you go. Don't skip black keys; that's the single most common way this trick goes wrong (see below).
3. Land on **5** (major) or **4** (minor) for the middle finger — that's the 3rd.
4. Keep counting to **8** for the pinky — that's the 5th, same spot either way.

This pairs naturally with [[Remembering Chord Fingering]]'s `1-3-5` finger numbering: finger `1` plays keyboard-position `1`, finger `3` plays keyboard-position `5` (major) or `4` (minor), finger `5` plays keyboard-position `8`. Two different counting systems landing on the same three keys is a good sign neither is a coincidence.

> [!warning] Common mistake: skipping black keys
> It's tempting to count only the white keys you'd normally name (C, D, E...) and lose track once a black key is involved. The trick only works if you count **every physical key** in the run, including ones you're not going to play — an unplayed black key still occupies a counted slot. Miscounting here is the #1 reason this trick gives a wrong note.

## Used in
- [[Chord]]
- [[Remembering Chord Fingering]]
- [[Lesson 05 - Chords]]
- [[Gold Silver Bronze Chords]]
