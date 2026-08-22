# CLAUDE.md

Guidance for Claude Code (and future me) working in this repo.

## What this is
An [Obsidian](https://obsidian.md) vault used as a personal learning journal for piano. It is **not** a software project — there's no build/test/lint step. "Correct" here means: notes are accurate, well-linked, and render properly in Obsidian.

## Repo / remote
- GitHub: https://github.com/DhruvKai/Piano.git (branch: `main`)
- Just `git add` / `git commit` / `git push` — no CI, no PR requirement, this is a personal notebook.

## Structure
- `Home.md` — vault dashboard / map of content (MOC), links out to every course and glossary note.
- `<Course Name>/` — one folder per course/source, e.g. `PIX Series YouTube Course/`. Each has a `<Course Name> - Course Overview.md` that links to all of its lesson notes.
- `Glossary/` — atomic, single-concept reference notes (e.g. `Alankar.md`, `Sargam.md`) that lesson notes link to via `[[wikilink]]` instead of re-explaining the concept every time.
- `Templates/Lesson Note Template.md` — starting point for a new lesson note.
- `Assets/` — images referenced by notes (e.g. keyboard diagrams), embedded via `![[filename.svg]]`. Prefer self-drawn SVG diagrams over fetched/downloaded images to avoid licensing issues. Organized into subfolders mirroring the note structure — `Assets/<Course Name>/Lesson NN/` for lesson-specific diagrams, `Assets/Glossary/` for concept diagrams shared across notes — rather than one flat folder; Obsidian's `![[filename.svg]]` embed resolves by filename across the whole vault, so it doesn't need a path, just a unique filename.
- `Paid Course/` — not created yet. Add it (see below) once a paid course actually starts.

## Note conventions (must stay Obsidian-compatible)
- Internal links use `[[Wikilink]]` syntax, not markdown relative links, so Obsidian's graph view and backlinks work.
- Every note has YAML frontmatter:
  ```yaml
  ---
  title: <Lesson Title>
  course: <Course/Series Name>       # omit on glossary/MOC notes
  type: lesson-note | course-overview | concept | moc
  source: <video URL>                 # lesson notes only
  channel: <channel/instructor name>
  date: <YYYY-MM-DD>
  status: in-progress | done
  tags: [piano, ...]
  ---
  ```
- Tags live in frontmatter as a YAML array, not inline `#hashtags`, so Obsidian's tag pane stays clean.
- Use Obsidian callouts (`> [!info]`, `> [!tip]`) for source links / asides — they render as boxes in Obsidian and degrade gracefully to blockquotes elsewhere.
- A new concept, technique, or notation the courses introduce gets its own note under `Glossary/` and gets linked wherever it's used, rather than re-defined inline every time.
- Before writing a concept note, check `Glossary/` for one that already covers it (or overlaps closely). If it exists, don't re-explain or duplicate it — just `[[link]]` to the existing note from wherever the concept comes up. Only write a new note when the concept genuinely isn't covered yet.
- File naming: `Lesson NN - <Title>.md` with zero-padded two-digit lesson numbers, so files sort correctly in the file explorer.
- Use **sharp-only keyboard notation** throughout the vault: `C#`, `D#`, `F#`, `G#`, and `A#`. Do not use flat labels (`Db`, `Eb`, `Gb`, `Ab`, `Bb`) in lesson tables, diagrams, practice lists, or note explanations. Use sharp-key aliases for scale names where needed (for example, `A# Major` rather than `Bb Major`). For beginner keyboard clarity, show `B#` as `C` and `E#` as `F`; briefly explain the formal theoretical spelling only when it directly helps the lesson.
- Keyboard SVGs: keys stay plain white/black — **never recolor a key** to mark it "in scale." Playing order is shown only by small numbered circle badges (colored, `1`/`8`=green root, others blue) placed **overlapping the bottom of each relevant key**, not in a separate row below the keyboard. Every SVG must have an explicit opaque background rect behind the *entire* canvas (title/caption text included, not just the keys) — Obsidian's dark theme otherwise swallows dark text that has no background of its own. When a scale's root isn't C, lay the keyboard window out starting at that root (not always a fixed C-to-C window), so the numbers read left-to-right in true playing order.

## Workflow: taking notes from a YouTube video
When given a video URL to take notes on:
1. `WebFetch` the URL for basic metadata. YouTube serves a JS-rendered page, so this usually only yields the title — not a transcript.
2. `WebSearch` the exact title + channel name to find companion material. Course channels often publish a matching blog post or downloadable PDF/notation sheet with the real lesson content (this is how the PIX Series lesson notes were built) — check before giving up.
3. If a PDF turns up, `WebFetch` it — it comes back as a saved binary file — then `Read` that saved path directly to extract the real text/diagrams.
4. If none of the above surfaces real content, **ask the user** to paste a transcript, timestamps, or a summary of what was covered. Never fabricate lesson content from a title alone.
5. Write the note from `Templates/Lesson Note Template.md`, link any new terms into `Glossary/`, and add the lesson to its course's `Course Overview.md`.

## Paid course (not started yet)
When it starts, create `Paid Course/<Actual Course Name>/` mirroring the same structure: a course overview note, lesson notes, and glossary links.
