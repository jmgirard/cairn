<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M320: Keep lessons in fixed ranked slots

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, IP2
- **Resolves:** —
- **Surface tier:** user-facing — every adopting repo's review hygiene and `/cairn-triage lessons` follow the changed rules
- **Branch/PR:** m320-lessons-fixed-slots

## Goal

`cairn/LESSONS.md` keeps a fixed number of short lessons, and a new lesson replaces the one whose last use is oldest.

## Scope

**In:** Replace the `LESSONS.md` byte budget with two limits: at most 25
lessons, each one line of at most 450 bytes. Define a lesson's rank by the
newest milestone in its provenance. Plans record the lessons they used, and
review hygiene marks those lessons `used`. Review capture becomes
one-in-one-out at the limit, and an extension that would pass 450 bytes
becomes its own lesson. `/cairn-triage lessons` gains a `split` disposition,
shortens or splits every lesson over 450 bytes, and drops by rank down to 20
lessons. Remove "prune the stalest" as a last resort. Write a D-entry that
supersedes the clauses these changes contradict. Bring this repo's
`cairn/LESSONS.md` under the new limits.

**Out:** A validator check on the lesson count or the per-lesson length:
the limits stay judgment-checked at hygiene passes, like the byte budgets
(D-119), and the validator's 50-line cap stays as a backstop. Showing lessons
in the cairn pane stays the parked row "Show decisions and lessons in the
pane". An archive file for evicted lessons is not built: git history holds
them (D-051's rejection of a graduated-lessons file stands). Other adopting
repos' files are brought under the limits by their own next hygiene pass or
triage run.

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md`'s Weight caps, `skills/shared/templates/lessons.md`,
      the `cairn/LESSONS.md` header, and the `/cairn-init` tree comment in
      `skills/cairn-init/SKILL.md` each state that `LESSONS.md` holds at most
      25 lessons, each one line of at most 450 bytes; and
      `git grep -nE '20,000|18,000|50-line|45 lines' -- skills cairn/LESSONS.md`
      returns no hit that sets a cap on `LESSONS.md`.
- [ ] AC2: `skills/shared/tracking-rules.md` defines a lesson's rank as the
      highest milestone number among the ids in its parenthesized provenance,
      ids marked `trimmed` or `corrected` excepted, a tie going to the later
      date and then to the line later in the file; and
      `git grep -n "stalest" -- skills cairn/LESSONS.md` returns no hit.
- [ ] AC3: `/milestone-plan`'s lesson harvest writes one work-log line
      `lessons used: <lessons>` naming by date and provenance each lesson
      that shaped the plan, or `lessons used: none`; and `/milestone-review`
      post-merge hygiene adds `used M<NNN>` to the provenance of each lesson
      that line names and of each lesson whose trap the milestone met,
      replacing that lesson's earlier `used` mark and adding no other text
      for the use.
- [ ] AC4: `/milestone-review` post-merge hygiene, when a captured lesson
      would leave more than 25 lessons, removes in the same commit the
      lowest-ranked lessons that no pin file holds and no live milestone
      quotes until 25 remain and names each in the archive summary, or, when
      none can be removed, captures nothing and names the skipped lesson in
      its close block with `/cairn-triage lessons` fenced; and an extension
      that would take a lesson past 450 bytes is not written into it, its
      content becoming a lesson of its own.
- [ ] AC5: `/cairn-triage lessons` (a) has a `split` disposition that breaks
      a lesson into lessons of at most 450 bytes each, each keeping the
      original date and the provenance ids its text came from; (b) proposes
      `compress` or `split` for every lesson over 450 bytes, pinned lessons
      included, where a pin requires only that its asserted string survive in
      one resulting lesson; (c) when more than 20 lessons would remain after
      its other proposals, proposes `drop` with a `rank` exit for the
      lowest-ranked lessons not kept for a pin, a live milestone, or a merge
      survivor, until 20 remain or every remaining lesson is so kept; and (d)
      `git grep -n "oldest lesson" -- skills` returns no hit.
- [ ] AC6: At the branch head, `cairn/LESSONS.md` holds at most 20 lessons
      (the lines `grep -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2}'` lists), each at
      most 450 bytes, and one of them contains
      `"green" is only as wide as what you ran`.
- [ ] AC7: `CHANGELOG.md`'s Unreleased section carries one entry stating the
      25-lesson and 450-byte limits, the rank, one-in-one-out capture, and
      the triage `split` and `rank` proposals; and the repo's `verify` (both
      gating suites, `claude plugin validate` on the plugin and marketplace
      manifests, `claude plugin test`) and the hand-run `skills/tests` pass
      at the branch head.

## Coverage

- AC1 → T1, T4
- AC2 → T1, T4
- AC3 → T2
- AC4 → T2
- AC5 → T3
- AC6 → T7
- AC7 → T4, T6

## Tasks

- [x] T1: `skills/shared/tracking-rules.md`: in Weight caps (lines 63-67),
      state the 25-lesson and 450-byte limits in place of the `LESSONS.md`
      20,000-byte budget, keep `LESSONS.md < 50 lines` as the validator
      backstop, and define the rank (AC2). In "Retiring a lesson" (lines
      126-141), drop "prune-the-stalest is the last resort" and name rank
      eviction at capture and in the triage pass. Re-seed the rulebook-mass
      baseline in its three places (LESSONS M149).
- [x] T2: `skills/milestone-plan/SKILL.md` harvest step: the
      `lessons used:` work-log line. `skills/milestone-review/SKILL.md`
      post-merge hygiene (lines 903-953): `used` marks, extension past 450
      bytes becomes its own lesson, one-in-one-out at 25 with the
      none-removable stop, and remove the "pruning the stalest lines"
      sentence. Also the `/milestone` audit's by-hand budget check.
- [x] T3: `skills/cairn-triage/SKILL.md` lessons pass (lines 108-253):
      `split` disposition and its gate display; compress-or-split for every
      lesson over 450 bytes, pins kept by surviving string; the `rank` drop
      exit down to 20; replace the 45-line and 18,000-byte near-cap figures
      with the lesson count; remove the keep-with-reasons option for length
      and "never proposes pruning the oldest lesson". Update the README row
      at `README.md:779` if its claim changes.
- [x] T4: Headers and docs: `skills/shared/templates/lessons.md`, the
      `cairn/LESSONS.md` header (keep or move the string
      `test_lesson_graduation.py` pins), the `skills/cairn-init/SKILL.md:171`
      tree comment, and one `CHANGELOG.md` Unreleased entry under "Changes
      that affect existing repos".
- [x] T5: D-entry: supersede D-051's rejection (3) and its prune-when-full
      last-resort clause, D-115's kept reasoning that item lines are never
      length-policed (for `LESSONS.md` only), D-119's `LESSONS.md` byte
      budget, D-169's rejection of pruning the oldest in the pass, and
      D-177/D-178's near-cap keep-with-reasons and last-resort clauses.
      State how it passes D-108's door (retained trigger: the shipped pass
      leaves the file at its budget, so capture has no room).
- [x] T6: Prose guards: update the guards whose pinned text changes
      (`skills/tests/test_triage_lessons.py`, `test_mutation_harness.py`,
      `test_lessons_loop.py`, `test_lesson_graduation.py`, and any other
      `git grep` finds), add guards for the rank, `split`, `rank` exit,
      `used` mark, and one-in-one-out rules, and run `verify` plus the
      hand-run `skills/tests`.
- [x] T7: Apply the new rules to `cairn/LESSONS.md`: split the three
      lessons over 1,700 bytes, compress or split each other lesson over 450
      bytes, then drop by rank to at most 20 lessons, keeping the pinned
      string. Log the per-lesson dispositions in the work log so the merge
      question can list them.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: tier check: milestone — a design change to three skills and the rulebook's caps, more than one sitting.
- 2026-10-24: idea vet: one concern, that ranking by repeats alone evicts the lessons that work best, since a lesson that prevents its trap never recurs; the set chose ranking by newest use, which counts a plan's use of a lesson.
- 2026-10-24: collision: D-051 rejection (3) and D-169's rejection of pruning the oldest in the pass (the user's choice at M263) — question set chose rank eviction by newest use, superseded at T5; D-115's kept reasoning that item lines are never length-policed — question set chose the 450-byte limit, superseded at T5; D-119 and D-177/D-178 clauses superseded at T5 by the agent as consequences of those answers.
- 2026-10-24: D-108's door: passed on its retained trigger — the shipped `/cairn-triage lessons` pass freed 1 or 2 lessons per run and left `cairn/LESSONS.md` at 19,993 of 20,000 bytes, so review capture has no room.
- 2026-10-24: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-24: question set: when to bring this repo's `LESSONS.md` under the limits — inside the milestone (T7), the merge question listing each dropped, split, or shortened lesson.
- 2026-10-24: plan gate chose rank by newest use over agent judgment alone because the judgment-only pass freed 1 or 2 lessons per run; falsified by a lesson evicted by rank whose trap then recurs within 20 milestones.
- 2026-10-24: plan gate chose a 450-byte per-lesson limit with `split` over a count limit plus byte budget because three extended lessons held 34% of the file; falsified by a split lesson whose pieces stop making sense apart.
- 2026-10-24: agent chose 25 slots, a triage target of 20, and 450 bytes: 25 × 450 bytes plus the header stays under the old 20,000-byte budget, and the 5-slot gap leaves room for several captures between triage runs.
- 2026-10-24: agent chose to keep the validator's 50-line cap unchanged as a backstop and add no count check, matching D-119's judgment-checked budgets and avoiding new machinery (D-057).
- 2026-10-24: criteria audit (full mode, Opus): 9 findings, all fixed — AC1 grep widened to every old cap figure in `skills` and `cairn/LESSONS.md`; AC2 rank stated over all provenance ids with `trimmed`/`corrected` excepted and a file-order last tie-break, count tie-break dropped; AC2 grep adds `cairn/LESSONS.md`; superseding D-entry added as T5 rather than a criterion; AC3 `used` mark replaces the earlier one so marks cannot grow a lesson past 450 bytes; AC4 handles a file over 25 and the none-removable case; AC5(b) includes pinned lessons with the pin kept by surviving string; AC6 restated as the file's state at branch head with the pinned string; AC7 names the full `verify`. Noted: a planned milestone's `lessons used:` line keeps those lessons in triage under the live-milestone rule.
- 2026-10-24: lessons used: 2026-07-16 (M56+M65, …) on running each gating suite and the hand-run `skills/tests` after skill edits; 2026-08-17 (M149) on re-seeding the rulebook-mass baseline in three places; 2026-07-24 (M112) on sweeping README, templates, and CHANGELOG for old wording; 2026-08-17 (M148) on prose-guard start markers; 2026-08-30 (M165) on checking pin tests before a LESSONS prune.
- 2026-10-24: implement started on branch m320-lessons-fixed-slots; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-24: T1 done — rulebook Weight caps state the 25-lesson and 450-byte limits and the rank, the remedy bullet and "Retiring a lesson" name rank eviction, use marks, and the `rank` exit (cites D-218, written at T5); rulebook-mass baseline re-seeded to 844 lines / 83,145 bytes in its three places; verify green (5/5).
- 2026-10-24: simple-english lint hook flags 535 pre-existing hits in tracking-rules.md and 199 in skills/milestone/SKILL.md; only this milestone's added lines were made free of semicolons and em-dashes, the rest left to the files' existing style.
- 2026-10-24: T2 done — plan harvest names the `lessons used:` line and step 4 writes it; review hygiene adds `used M<NNN>` marks (newest replaces older), sends an over-450-byte extension to its own lesson, and evicts by rank to 25 with the none-removable stop, replacing the stalest-prune sentence; minor amendment: T2 also updates the `/milestone` audit's by-hand LESSONS check (`skills/milestone/SKILL.md:83`), found by grep.
- 2026-10-24: T3 done — the lessons pass gains `split` (seven dispositions), the length rule (every lesson over 450 bytes is `compress` or `split`, a pinned string or quoted text kept whole in one line, no keep-as-is), the rank rule with the `rank` drop exit down to 20, a lesson-count chip sentence in place of the 45-line and 18,000-byte figures, and split/rank naming in apply and record; "never proposes pruning the oldest lesson" removed. Agent chose: a merge whose survivor would pass 450 bytes is not proposed, and a live milestone's quoted text is kept whole the way a pin's string is. README row and the skill description updated.
- 2026-10-24: T4 done — `cairn/LESSONS.md` header (pinned "or when a matured family / graduates whole" phrase kept), the lessons template, and the `/cairn-init` tree comment state the 25-lesson and 450-byte limits; one CHANGELOG Unreleased entry under "Changes that affect existing repos".
- 2026-10-24: T5 done — D-218 written: supersedes D-051 rejection (3) and its prune-when-full last resort, D-119's LESSONS byte budget, D-169's rejection of pruning in the pass, D-177's near-cap rule; narrows D-115's kept no-length-policing clause for LESSONS; passes D-108's door on its retained trigger.
- 2026-10-24: T6 done — `test_triage_lessons.py` re-pinned to the new pass text (seven dispositions, six exits with `rank`, `split`, length rule, rank rule, gate count, limit check, record naming) plus two rulebook tests (limits and rank; use marks and one-in-one-out); `test_lessons_loop.py` gains `TestUseMarksAndCapture` (plan line, review mark, long extension, one-in-one-out); mutation registry updated and extended, every new block red when blanked. Gating suites green; `skills/tests` green but for `test_lessons_file_is_back_under_its_cap` (LESSONS.md at 50 lines after T4's header line), which T7 clears.
- 2026-10-24: T7 split — 2026-07-16 (M56+M65, …) "green" (1,985 bytes) into five: the suites-and-exit-codes core (kept, pinned and named by this milestone's `lessons used:` line), sweep-probe (M111/M137/M140), copied-tree probe (M164), stale bytecode (M180), references Provenance (M279); 2026-10-01 (M193, M191 …) mod facts (3,072 bytes) into four: mod checks (M284), test-hook answers (M278), state and loading (M311), desktop drawing (M294/M311), dropping the U+2028 detail (held by the M272 lesson), the dismiss-label, `minWidth`, and fixture-roster details; 2026-10-03 (M201) live looks (1,730 bytes) into two (M213; M305), dropping the M302/M305 Candidates-heading and session-start details. Inline `(Mxxx)` marks moved into each line's provenance.
- 2026-10-24: T7 compressed to ≤450 bytes — 2026-08-04 (M133, now extended M173/M283), 2026-08-17 (M149), 2026-08-17 (M148), 2026-08-22 (M152), 2026-10-17 (M272, now extended M293/M294), 2026-10-18 (M274, now extended M303), 2026-10-18 (M277). Unchanged — 2026-07-24 (M112), 2026-08-30 (M165), 2026-09-02 (M169), 2026-10-18 (M275), 2026-10-18 (M278).
- 2026-10-24: T7 `rank` drops (lowest rank first, 40 lessons after splits, 5 kept for this milestone, 15 by rank down to the M202 cut) — 2026-07-20 (M100) rank M100; 2026-07-25 (M113) bounding pass and 2026-07-25 (M113, trimmed M122) hook normalization, M113; 2026-07-26 (M115, corrected M135) dangling ids and 2026-07-26 (M115) unmerged-branch citation, M115; 2026-07-20 (M99 …) fixed-point figure, M118; 2026-07-31 (M127) whole-file deletion; split piece sweep-probe, M140; 2026-08-22 (M153) Review findings; 2026-08-22 (M156) wrapped token; 2026-08-23 (M158) record-type preview; 2026-08-29 (M163 …) merge_guard quoted text; split piece copied-tree probe, M164; 2026-09-02 (M170) failed merge marker; 2026-09-02 (M171) list pins; 2026-09-02 (M172) re-entry routes; split piece stale bytecode, M180; 2026-09-05 (M178, extended M181) hand-rolled reader; 2026-09-10 (M185) second-mode sweep; 2026-08-23 (M157, extended M192) repo-wide count. Result: 20 lessons, longest 437 bytes, 8,151 bytes total; the pinned "green" string is in the first lesson; `skills/tests` and validate green.

## Decisions

## Review
