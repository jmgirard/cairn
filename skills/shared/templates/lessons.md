<!-- Instantiated by /cairn-init as cairn/LESSONS.md (file header; the
     scaffold ships it empty of lessons). One line per lesson; corrected in
     place when proven false; retirement per tracking-rules "Retiring a
     lesson". -->
# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Limits: at most 25
lessons, each at most 450 bytes. A lesson over 450 bytes is shortened or
split. Over 25 lessons, lessons retire first, and then the lowest-ranked
lesson leaves. Rank is the newest
milestone in a lesson's provenance, not counting `trimmed` or `corrected`
marks, and reviews mark `used M<NNN>` on the
lessons a milestone used. A `- waiting` line at the end is not a lesson.
When no lesson can leave a full file, review writes it. It takes no `used`
mark and waits for `/cairn-triage lessons` to admit or drop it. If the file
already holds 49 lines, review quotes the lesson in its close block instead.
Corrected in place when proven false (never append a correction).
