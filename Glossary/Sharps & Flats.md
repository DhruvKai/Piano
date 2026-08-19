---
title: Sharps & Flats
type: concept
tags: [glossary, theory, keyboard-layout]
---

# Sharps & Flats (Accidentals)

![[keyboard-one-octave.svg]]

Recap: the white keys are the 7 [[Western Note Names|C D E F G A B]] notes, sitting inside an [[Octave]] of 12 keys total. The other **5 keys are black**, and they're named using **sharps (#)** and **flats (b)**.

## What sharp and flat actually mean
- **Sharp (#)** = raise a note by one **half step** — the smallest possible distance between two neighboring keys (black or white).
- **Flat (b)** = lower a note by one half step.
- Two half steps = one **whole step**.

So `C#` means "one half step above C", and `Db` means "one half step below D". On a piano these land on **the exact same physical key** — just two different names for it. That's called an **enharmonic equivalent**.

### Semitone and Tone, highlighted
![[semitone-vs-tone.svg]]

**Semitone** (half step) — the smallest possible distance on the keyboard: one key straight to the very next key, black or white, with nothing in between. `C → C#` is a semitone.

**Tone** (whole step) — two semitones stacked together, i.e. one key skipped. `C → D` is a tone: it passes right over `C#` to get there.

> [!info] Other names for the same thing
> **Semitone = half step**, **Tone = whole step** — same distances, different words for them. [[Lesson 03 - Major Scales|Later lessons]] abbreviate these as **ST** and **T** — see [[Major Scale]], where this exact distance is what the whole major-scale formula is built from.

## Why only 5 black keys, not 7?
Every white key is a whole step from its neighbor — **except E→F and B→C**, which are already just a half step apart, so there's no room for a black key to sit between them. This gap is exactly why the black keys come in [[Octave|groups of 2 and 3]] instead of being evenly spaced.

> [!tip] Memory trick
> E and B are the two white keys with "no black key next door." Everywhere else, every white key has a black key immediately after it.

## The chromatic scale (all 12 half steps)
Walking through every key, white and black, one half step at a time, is called the **chromatic scale**:

```mermaid
graph LR
  C["C"] -->|half step| Cs["C# / Db"]
  Cs -->|half step| D["D"]
  D -->|half step| Ds["D# / Eb"]
  Ds -->|half step| E["E"]
  E -->|"half step (no black key!)"| F["F"]
  F -->|half step| Fs["F# / Gb"]
  Fs -->|half step| G["G"]
  G -->|half step| Gs["G# / Ab"]
  Gs -->|half step| A["A"]
  A -->|half step| As["A# / Bb"]
  As -->|half step| B["B"]
  B -->|"half step (no black key!)"| C2["C"]

  classDef white fill:#f5f5f5,stroke:#333,color:#111;
  classDef black fill:#2b2b2b,stroke:#000,color:#fff;
  class C,D,E,F,G,A,B,C2 white;
  class Cs,Ds,Fs,Gs,As black;
```

Light nodes = white keys, dark nodes = black keys. Notice the two spots (E→F, B→C) where a white key connects straight to the next white key with nothing in between.

## All 12 notes, both spellings

| White key | Black key right after it | Enharmonic pair |
|-----------|--------------------------|------------------|
| C | Yes | C# / Db |
| D | Yes | D# / Eb |
| E | **No** | — |
| F | Yes | F# / Gb |
| G | Yes | G# / Ab |
| A | Yes | A# / Bb |
| B | **No** | — |

## Sharp vs. flat — which name to use?
Both names point to the same key, so which spelling you use depends on context (the key/scale you're in) rather than the sound. As a beginner, it's fine to think of them as interchangeable — you'll pick up the "correct" spelling per scale later, once [[Western Note Names|major/minor scales]] come up.

## Relation to Sargam (Komal / Teevra)
The [[Sargam]] system already names this same idea from the Indian classical side: **Komal swar = flat**, **Teevra swar = sharp**. See [[Octave]] for the full Shuddh/Komal/Teevra breakdown — it's the same 12 physical keys, just two different naming systems layered on top.

## Used in
- [[Western Note Names]]
- [[Octave]]
- [[Major Scale]]
