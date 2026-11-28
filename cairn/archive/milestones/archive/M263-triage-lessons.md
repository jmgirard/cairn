# M263: /cairn-triage lessons triages LESSONS.md

**Status:** done (2026-10-16, PR #275 https://github.com/jmgirard/cairn/pull/275)

**Goal:** `/cairn-triage lessons` proposes one disposition per `cairn/LESSONS.md` lesson at one gate, so lessons can leave the file when the user asks, not only at a milestone's review hygiene.

**Outcome:** `skills/cairn-triage/SKILL.md` gains "The lessons pass (`/cairn-triage lessons`)": the `lessons` argument (any other argument stops first, before the owner-mode preconditions; no argument means no lesson); lesson items (date, subject, provenance, byte length, priority `—`); pin files from `git grep -l "LESSONS.md"` on test paths, read at `<base>/<default-branch>` in guest mode, with only assertions on the live file counting; five dispositions (`keep`, `compress`, `merge`, `drop` by an enforcement exit or an ownership exit whose section already holds the content, `promote` with D-055's full bar and none in a repo without `skills/shared/`); a pinned, live-milestone, false, or stale lesson is `keep`, and a false or stale flag forces a stamp; a two-file cap check; drops and merges named in the stamp and commit, no D-entry. Frontmatter, H1, the tracking-rules retirement sentence, README, DESIGN.md, CHANGELOG, and review hygiene's cap path (fences the pass) name it. Rulebook baseline re-seeded to 679 lines / 65,365 bytes. `test_triage_lessons.py` (20 tests), 25 mutation entries.

**Decisions:** D-169 (annotates D-051 and D-055; walks D-108's door on its retained trigger). The question set chose opt-in over every triage pass, and four exits over also pruning the oldest.

**Review:** No returns. Criteria audit (full): 12 findings taken. T6 dry run (32 lessons): 1 compress, 31 keep, no drop, so the pass frees about 190 bytes and no line on this repo. Claim audit 46 claims, 8 corrected. Three lenses: 14 fixed (ownership must already hold the content, false-lesson stamp, live-milestone and pin guards, guest base ref, D-169's door and Context), 4 to "Lessons triage edges (M263 review)", 3 rejected. Copilot (Lite) 1 fixed, 2 rejected. No lesson captured (LESSONS.md at its caps); nothing retired.
