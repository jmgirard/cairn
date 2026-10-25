<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M322: Stop citing lessons from code and docs

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — two edited files are shipped skill prose (`skills/milestone-plan/SKILL.md`, `skills/milestone-review/SKILL.md`), and the rest are tests, code comments, and tracking
- **Branch/PR:** m322-lesson-cites

## Goal

Code, tests, skill prose, and `cairn/DESIGN.md` stop pointing readers at `cairn/LESSONS.md` lines, which rank eviction and in-place correction can remove or change.

## Scope

**In:** absorbs the candidate row "Cut code cites to evicted lessons". A
D-entry decides that code, tests, skill prose, and `cairn/DESIGN.md` do not
cite a lesson. One sentence in the header of this repo's `cairn/LESSONS.md`
states the rule where lesson readers look. Every lesson cite that sweep S
(below) lists is rewritten. The comment states the point in its own words,
or it cites a milestone or D-entry whose file records that point. The
`cairn/DESIGN.md` Known issues sentence that says test comments cite
lessons by line number goes, since the gap is closed.

Sweep S, run from the repo root:

```
{ git grep -niE 'lesson' -- . ':!cairn' ':!CHANGELOG.md'; git grep -niE 'lesson' -- cairn/DESIGN.md; } | grep -E 'M[0-9]{2,3}|LESSONS ?:|LESSONS [0-9]'
```

On main at plan time it lists 73 lines in 35 files. Most are cites. The
rest name the lessons mechanism, a milestone's work on lessons, or fixture
data. S reads one line at a time, so it cannot see a cite that wraps
across a line break, such as `scripts/cairn_validate.py:1344-1345`.

**Out:**
- The shipped lessons template (`skills/shared/templates/lessons.md`) and
  adopters' own code stay unchanged. The new D-entry's Rejected says why.
- A test that fails when a new cite appears is not built. The D-entry's
  Rejected says why.
- Milestone files and archives that quote a lesson, and their protection
  after a use mark changes the provenance: the parked row "Match lesson
  citations after use marks".
- Pin files that assert strings present in `cairn/LESSONS.md`
  (`skills/tests/test_lesson_graduation.py`, `test_lessons_loop.py`)
  read lesson text and cite nothing, so they stay unchanged.
- `CHANGELOG.md` and the history files under `cairn/` (DECISIONS, archive,
  milestone work logs) are history, never edited (IP4).

## Acceptance criteria

- [ ] AC1: On the branch head, sweep S lists no line that cites a lesson.
      A cite sends the reader to a `cairn/LESSONS.md` line for a point.
      It names the lesson by milestone id, line number, date, or quoted
      text, as in "the M171 lesson", "LESSONS M194", "LESSONS :49", or
      "LESSONS: widening a capture class". Every line S still lists names
      the lessons mechanism, a milestone's work on lessons, or fixture
      data. The wrapped M81 cite at `scripts/cairn_validate.py:1344-1345`
      on main is rewritten as AC2 says.
- [ ] AC2: Take each line that S lists on main, that cites a lesson as
      AC1 defines it, and that the branch rewrites rather than deletes.
      Its new text states in words the point that the cite stood for. Or
      it cites a milestone or D-entry, and that milestone's file, its
      archive summary, or that entry records the point.
- [ ] AC3: `cairn/DECISIONS.md` gains a new D-entry, appended after D-221.
      The entry decides that code, tests, skill prose, and
      `cairn/DESIGN.md` do not cite a lesson. The header of
      `cairn/LESSONS.md`, which is the text before its first lesson line,
      states that rule in one sentence.
- [ ] AC4: `cairn/DESIGN.md`'s Known issues no longer says that test
      comments cite lessons by line number. The entry's other sentences
      are kept word for word, and its provenance tail gains a
      `narrowed 2026-10-25 — M322` mark (the date of the edit).
- [ ] AC5: The verify slot of `cairn/PROFILE.md` is green on the branch
      head (both gating suites, both `claude plugin validate` runs, and
      `claude plugin test`), and `python3 -m unittest discover -s
      skills/tests` passes.

## Coverage

- AC1 → T2, T3, T4, T5
- AC2 → T2, T3, T4
- AC3 → T1
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: Append the D-entry to `cairn/DECISIONS.md` and add the header
      sentence to `cairn/LESSONS.md`. Keep whole each string that
      `skills/tests/test_lesson_graduation.py` and `test_lessons_loop.py`
      assert in that file, and keep the header within the 23 lines that
      `test_lessons_header_leaves_room_for_25_lessons` allows.
- [x] T2: Rewrite the cites under `scripts/` and `hooks/`
      (`scripts/tests/test_scripts.py`, `scripts/tests/test_status_fixtures.py`,
      `scripts/cairn_validate.py:1097` and `:1109` and the wrapped cite at
      `:1344-1345`, `hooks/status/pane.test.tsx`,
      `hooks/status/reader.test.ts`, `hooks/status/register.tsx:404`).
- [x] T3: Rewrite the cites in `skills/tests/*.py`. Before each edit near a
      pinned slice, read the mutation harness's `block=` strings so no pin
      loses its unique start marker.
- [x] T4: Rewrite the skill-prose cites (`skills/milestone-plan/SKILL.md:548`,
      `skills/milestone-review/SKILL.md:435`) and `cairn/DESIGN.md:649`.
      Delete the Known issues sentence at `cairn/DESIGN.md:1025-1026` and
      add the entry's `narrowed` mark.
- [x] T5: Run sweep S and record in one work-log line why each line it
      still lists is not a cite. Run the verify slot and the hand-run
      `skills/tests`, and check each exit code.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: not run — work named at the question set.
- 2026-10-25: question set: which candidate to plan — "Cut code cites to evicted lessons"; run through to implement and review — yes.
- 2026-10-25: idea vet: none — the row's title names evicted lessons, but its detail asks whether code cites a lesson at all, and any lesson can leave later, so the plan covers every cite S lists.
- 2026-10-25: collision check: candidate row "Cut code cites to evicted lessons" absorbed; the DESIGN.md Known issues sentence on line-number cites absorbed (AC4); parked row "Match lesson citations after use marks" is distinct (milestone files quoting lessons) and named in Out; no D-entry rules on where lessons are cited (D-015, D-045, D-051, D-218 to D-221 read).
- 2026-10-25: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-25: lessons used: 2026-07-16 (M56+M65), 2026-07-24 (M112), 2026-08-04 (M133), 2026-08-17 (M148), 2026-08-30 (M165), 2026-09-02 (M169), 2026-10-25 (M321).
- 2026-10-25: criteria audit (full, fresh Opus reader): 5 findings, all taken — AC1 names the wrapped M81 cite S cannot see; AC1's cite definition adds quoted text; AC2's domain narrows to rewritten cites; AC4 allows the entry's `narrowed` mark; AC3 says "gains … appended after D-221" in place of "ends with". AC5 had none.
- 2026-10-25: plan gate chose to cut each cite and state its point in place over replacing it with the lesson's milestone id, because a milestone's record often lacks the point (M105's archive says nothing about squash); falsified by a rewritten comment that a reader cannot follow without the lesson.
- 2026-10-25: plan gate chose a LESSONS.md header sentence over a test that fails on a new cite, because a pattern finds only the spellings it lists and S already needed three; falsified by a new lesson cite in code after the header sentence lands.
- 2026-10-25: plan gate chose to leave the shipped lessons template alone over adding the rule there, because cairn sets no rule for an adopter's code comments; falsified by an adopter asking for it.
- 2026-10-25: changelog: no entry, because no behavior or rule an adopter sees changes; the two skill-prose edits drop a parenthetical cite.
- 2026-10-25: implement started on m322-lesson-cites from main at 67187333; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-25: T1 done: D-222 appended after D-221; LESSONS.md header gains a two-line rule sentence (header 22 lines, test limit 23); lessons_loop and lesson_graduation tests and validate green.
- 2026-10-25: T2 done: 15 cites in 6 files under scripts/ and hooks/ rewritten to state their point, the wrapped M81 cite at cairn_validate.py:1344 included; no milestone cite added; both gating suites green.
- 2026-10-25: T3 done: 38 cites in 21 skills/tests files rewritten (cites only in comments and docstrings, no `block=` string touched); test_source_note_template.py:7 kept, since it recounts M63-M65 history and cites no lesson; skills/tests green (977 tests).
- 2026-10-25: T4 done: the two skill-prose parentheticals dropped (no pin holds either line); DESIGN.md:649 cite dropped; the Known issues sentence on line-number cites deleted and the entry's tail marked `narrowed 2026-10-25 — M322`; skills/tests and validate green.
- 2026-10-25: T5 sweep S on the branch lists 16 lines, none a cite: fixture data (hooks/status/fixtures.gen.ts:441, fixtures/repo-at-cut ROADMAP:4, test_scripts.py:2476 milestone filename, :3439 fixture LESSONS text); the lessons mechanism or a milestone's lesson work (test_lesson_graduation.py:1, test_lessons_loop.py:1/75/256, test_triage_lessons.py:1/11/18, test_mutation_harness.py:2400/2941/4677, DESIGN.md:38); history narrative (test_source_note_template.py:7).
- 2026-10-25: T5 verify slot green: scripts/tests and hooks/tests OK, both plugin validates exit 0 (no version warning), plugin test 2466 pass 0 fail; skills/tests 977 OK.

## Decisions

## Review
