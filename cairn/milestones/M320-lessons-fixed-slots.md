<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M320: Keep lessons in fixed ranked slots

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, IP2
- **Resolves:** —
- **Surface tier:** user-facing — every adopting repo's review hygiene and `/cairn-triage lessons` follow the changed rules
- **Branch/PR:** —

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

- [ ] T1: `skills/shared/tracking-rules.md`: in Weight caps (lines 63-67),
      state the 25-lesson and 450-byte limits in place of the `LESSONS.md`
      20,000-byte budget, keep `LESSONS.md < 50 lines` as the validator
      backstop, and define the rank (AC2). In "Retiring a lesson" (lines
      126-141), drop "prune-the-stalest is the last resort" and name rank
      eviction at capture and in the triage pass. Re-seed the rulebook-mass
      baseline in its three places (LESSONS M149).
- [ ] T2: `skills/milestone-plan/SKILL.md` harvest step: the
      `lessons used:` work-log line. `skills/milestone-review/SKILL.md`
      post-merge hygiene (lines 903-953): `used` marks, extension past 450
      bytes becomes its own lesson, one-in-one-out at 25 with the
      none-removable stop, and remove the "pruning the stalest lines"
      sentence.
- [ ] T3: `skills/cairn-triage/SKILL.md` lessons pass (lines 108-253):
      `split` disposition and its gate display; compress-or-split for every
      lesson over 450 bytes, pins kept by surviving string; the `rank` drop
      exit down to 20; replace the 45-line and 18,000-byte near-cap figures
      with the lesson count; remove the keep-with-reasons option for length
      and "never proposes pruning the oldest lesson". Update the README row
      at `README.md:779` if its claim changes.
- [ ] T4: Headers and docs: `skills/shared/templates/lessons.md`, the
      `cairn/LESSONS.md` header (keep or move the string
      `test_lesson_graduation.py` pins), the `skills/cairn-init/SKILL.md:171`
      tree comment, and one `CHANGELOG.md` Unreleased entry under "Changes
      that affect existing repos".
- [ ] T5: D-entry: supersede D-051's rejection (3) and its prune-when-full
      last-resort clause, D-115's kept reasoning that item lines are never
      length-policed (for `LESSONS.md` only), D-119's `LESSONS.md` byte
      budget, D-169's rejection of pruning the oldest in the pass, and
      D-177/D-178's near-cap keep-with-reasons and last-resort clauses.
      State how it passes D-108's door (retained trigger: the shipped pass
      leaves the file at its budget, so capture has no room).
- [ ] T6: Prose guards: update the guards whose pinned text changes
      (`skills/tests/test_triage_lessons.py`, `test_mutation_harness.py`,
      `test_lessons_loop.py`, `test_lesson_graduation.py`, and any other
      `git grep` finds), add guards for the rank, `split`, `rank` exit,
      `used` mark, and one-in-one-out rules, and run `verify` plus the
      hand-run `skills/tests`.
- [ ] T7: Apply the new rules to `cairn/LESSONS.md`: split the three
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

## Decisions

## Review
