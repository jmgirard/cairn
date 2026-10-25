<!-- Instantiated by /cairn-init as cairn/LESSONS.md (file header; the
     scaffold ships it empty of lessons). One line per lesson; corrected in
     place when proven false; retirement per tracking-rules "Retiring a
     lesson". -->
# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`, at most 25 lessons of
at most 450 bytes each. A lesson over 450 bytes is shortened or split. Over 25
lessons, lessons retire first, and then the lowest-ranked lesson leaves. Rank
is the newest milestone in its provenance, not counting `trimmed` or `corrected`
marks, and reviews mark `used M<NNN>` on the lessons a milestone used. A
`- waiting` line is not a lesson: it takes no `used` mark and waits for
`/cairn-triage lessons`. Corrected in place when proven false (never append a
correction).
