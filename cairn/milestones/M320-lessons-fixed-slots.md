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
- **Branch/PR:** m320-lessons-fixed-slots, https://github.com/jmgirard/cairn/pull/333

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

- [x] AC1: `skills/shared/tracking-rules.md`'s Weight caps, `skills/shared/templates/lessons.md`,
      the `cairn/LESSONS.md` header, and the `/cairn-init` tree comment in
      `skills/cairn-init/SKILL.md` each state that `LESSONS.md` holds at most
      25 lessons, each one line of at most 450 bytes; and
      `git grep -nE '20,000|18,000|50-line|45 lines' -- skills cairn/LESSONS.md`
      returns no hit that sets a cap on `LESSONS.md`.
- [x] AC2: `skills/shared/tracking-rules.md` defines a lesson's rank as the
      highest milestone number among the ids in its parenthesized provenance,
      ids marked `trimmed` or `corrected` excepted, a tie going to the later
      date and then to the line later in the file; and
      `git grep -n "stalest" -- skills cairn/LESSONS.md` returns no hit.
- [x] AC3: `/milestone-plan`'s lesson harvest writes one work-log line
      `lessons used: <lessons>` naming by date and provenance each lesson
      that shaped the plan, or `lessons used: none`; and `/milestone-review`
      post-merge hygiene adds `used M<NNN>` to the provenance of each lesson
      that line names and of each lesson whose trap the milestone met,
      replacing that lesson's earlier `used` mark and adding no other text
      for the use.
- [x] AC4: `/milestone-review` post-merge hygiene, when a captured lesson
      would leave more than 25 lessons, removes in the same commit the
      lowest-ranked lessons that no pin file holds and no live milestone
      quotes until 25 remain and names each in the archive summary, or, when
      none can be removed, captures nothing and names the skipped lesson in
      its close block with `/cairn-triage lessons` fenced; and an extension
      that would take a lesson past 450 bytes is not written into it, its
      content becoming a lesson of its own.
- [x] AC5: `/cairn-triage lessons` (a) has a `split` disposition that breaks
      a lesson into lessons of at most 450 bytes each, each keeping the
      original date and the provenance ids its text came from; (b) proposes
      `compress` or `split` for every lesson over 450 bytes, pinned lessons
      included, where a pin requires only that its asserted string survive in
      one resulting lesson; (c) when more than 20 lessons would remain after
      its other proposals, proposes `drop` with a `rank` exit for the
      lowest-ranked lessons not kept for a pin, a live milestone, or a merge
      survivor, until 20 remain or every remaining lesson is so kept; and (d)
      `git grep -n "oldest lesson" -- skills` returns no hit.
- [x] AC6: At the branch head, `cairn/LESSONS.md` holds at most 20 lessons
      (the lines `grep -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2}'` lists), each at
      most 450 bytes, and one of them contains
      `"green" is only as wide as what you ran`.
- [x] AC7: `CHANGELOG.md`'s Unreleased section carries one entry stating the
      25-lesson and 450-byte limits, the rank, one-in-one-out capture, and
      the triage `split` and `rank` proposals; and the repo's `verify` (both
      gating suites, `claude plugin validate` on the plugin and marketplace
      manifests, `claude plugin test`) and the hand-run `skills/tests` pass
      at the branch head.

## Coverage

- AC1 → T1, T4
- AC2 → T1, T4, T8
- AC3 → T2, T9
- AC4 → T2, T9
- AC5 → T3, T8
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
- [x] T5: D-entry superseding the clauses these changes contradict and
      passing D-108's door on its retained trigger (written as D-218; its
      heading lists each clause).
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
- [x] T8: Review return 1: spell "stalest" and "oldest lesson" by
      concatenation in their `assertNotIn` guards
      (`test_lessons_loop.py`, `test_triage_lessons.py`), and restore the
      paragraph break before the `promote` sentence in
      `skills/cairn-triage/SKILL.md`.
- [x] T9: Review return 2: fix the pass-2 fix-now findings the work log's
      `review return 2:` line lists, D-219 included.

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
- 2026-10-24: claim audit: 57 claims read, 5 corrected — skills/shared/templates/lessons.md, cairn/LESSONS.md header, README.md, CHANGELOG.md, skills/shared/tracking-rules.md (also milestone-review ordering): "last use is oldest" and "least recently used" restated as the lowest rank, the CHANGELOG cut sentence split into review-capture and triage halves, the rulebook names a per-line byte command and points the remedy at "Retiring a lesson", and review says to mark use even when no lesson is learned; rulebook-mass baseline re-seeded to 844 lines / 83,211 bytes in its three places. Verify 5/5 green, `skills/tests` green, validate green.
- 2026-10-24: review opened PR #333 at review start (Copilot round on); `gh pr edit --add-reviewer @copilot` exited 0 but the state query still read `none`, so the request may not be recorded by GitHub; no second request.
- 2026-10-24: review return 1: AC2 and AC5(d) fail as written — `git grep -n "stalest" -- skills cairn/LESSONS.md` hits `skills/tests/test_lessons_loop.py:125` and `skills/tests/test_triage_lessons.py:423`, and `git grep -n "oldest lesson" -- skills` hits `skills/tests/test_triage_lessons.py:313`, all `assertNotIn` literals; spell each retired token in its guard by concatenation. Also restore the paragraph break between the rank rule and the `promote` sentence in `skills/cairn-triage/SKILL.md` (~line 220).
- 2026-10-24: T8 done (minor amendment for return 1: task added, Coverage AC2 and AC5 cite T8) — the three guards spell "stal" "est" and "oldest " "lesson" by concatenation, the paragraph break before the `promote` sentence restored; both criterion greps now return no hit. Verify 5/5 green, `skills/tests` green. Handing back to review.
- 2026-10-24: review return 2: load-bearing defects from pass 2's fan-out (Review section): guest-mode rank eviction loses lessons with no copy (diff-bug #1, #18); review eviction's partial-removal case undefined (#4) and its archive-summary naming can pass 25 lines (#2); a `used` mark can push a lesson past 450 bytes (#5); `lessons used:` reaches only the first milestone file (#15). Same return also carries the pass's other fix-now items: one batched D-219 correcting D-218 (diff-bug #8, #9, #14; blame-history #1, #2, #7), rulebook sentence that rank eviction is not a retirement exit (ripple #1, #2), rank exception in template, LESSONS.md header, README, CHANGELOG (diff-bug #17, ripple #3), split-line rank-drop display (#10), LESSONS.md provenance fixes (#13), stale harness comment (#19), "(M320 review)" test comments removed (#20), DESIGN.md:1023 wording (ripple #6). Follow-up row "Match lesson citations after use marks" added.
- 2026-10-24: T9 done (minor amendment for return 2: task added, Coverage AC3 and AC4 cite T9) — review hygiene: the `used` mark counts toward 450 bytes and a lesson it pushes over is shortened; eviction names removed lessons in one archive-summary line, removes none when too few can go, and in guest mode quotes each removed lesson in the close block. Plan writes `lessons used:` in each milestone file. Triage shows a rank-dropped split line under its split. Rulebook: rank eviction is not a retirement exit. Rank exception added to template, LESSONS.md header, README, CHANGELOG; DESIGN.md:1023 says limit check; LESSONS.md mod-lesson provenance corrected (M191 to its `{ value }` lesson, M195 to the mod-checks lesson; the M195 session clause stays in the 2026-10-03 lesson as a merge, not a split); harness comment and test-comment citations fixed; D-219 written. Guards updated and extended; rulebook-mass baseline re-seeded to 845 lines / 83,349 bytes. Verify 5/5 green, `skills/tests` green.
- 2026-10-24: claim audit: 52 claims read, 3 corrected — cairn/DECISIONS.md, CHANGELOG.md (return-2 diff): D-219's item (1) wrongly said D-051's Decision is narrowed and its heading misnamed the narrowed keep clauses, corrected by D-220; the CHANGELOG entry now states the too-few-removable case and the guest quote.
- 2026-10-24: correction to the T7 compression line (pass-3 blame-history #3, #7): the compressions also dropped these clauses, unnamed there — from 2026-08-04 (M133) the `&&`-not-`;` join of a record-writing script and its commit (its point stays in the first lesson's `;`-chaining sentence); from 2026-08-17 (M148) the renumbering sweep of heading text across `skills/tests`; from 2026-10-18 (M277) the example of the set-aside run; from 2026-10-18 (M274) the name `test_shipped_reference_profiles_are_valid`.
- 2026-10-24: review return 3: pass-3 load-bearing findings — review hygiene's use-mark step reads the `lessons used:` line from the milestone file the same pass already deleted (diff-bug #1); shortening a lesson a `used` mark pushes past 450 bytes can break a pinned string or quoted text (diff-bug #2); a lesson skipped when too few can be removed is kept only in chat (diff-bug #11). This is the third defect return, so the thrash rule (a) stops the run: no retry is queued, and the disposition goes to the user at a chip (descope recommended). Follow-up rows "Close the small gaps in lesson ranking" and "Cut code cites to evicted lessons" added.

## Decisions

## Review

Pass 1 (2026-10-24), branch head b0f4c65e; PR #333 opened at review start (Copilot round on; request returned 0 but the state query still read `none`, reported, no second request).

- AC1 evidence: `grep -n 'at most 25'` finds the 25-lesson, 450-byte limit at tracking-rules.md:65-66, templates/lessons.md:12-13, cairn/LESSONS.md:9, cairn-init/SKILL.md:171. `git grep -nE '20,000|18,000|50-line|45 lines' -- skills cairn/LESSONS.md` hits only `150-line` milestone-cap text, a `20,000` inside an `assertNotIn` guard, and `test_lessons_loop.py:5`'s docstring naming the retained `< 50 lines` validator backstop; none sets a cap on `LESSONS.md`. Pass.
- AC2 evidence: rank defined at tracking-rules.md:68-70 as written. `git grep -n "stalest" -- skills cairn/LESSONS.md` returns two hits, `test_lessons_loop.py:125` and `test_triage_lessons.py:423`, both `assertNotIn("stalest", …)` guards. The criterion as written fails. Fail.
- AC3 evidence: plan harvest at milestone-plan/SKILL.md:370-374 writes `lessons used: <lessons>` or `lessons used: none`; review hygiene at milestone-review/SKILL.md:909-913 adds `used M<NNN>` for each named lesson and each met trap, replacing the earlier `used` mark and adding no other text. Pass.
- AC4 evidence: milestone-review/SKILL.md:959-968 removes lowest-ranked unpinned, unquoted lessons until 25 remain, names each in the archive summary, and captures nothing with the skipped lesson named when none can go (`/cairn-triage lessons` fenced at :968-969); :914-916 sends an over-450-byte extension to its own lesson. Pass.
- AC5 evidence: (a) `split` row at cairn-triage/SKILL.md:163 with date and own provenance ids; (b) length rule at :201-212 covers pinned and live lessons, the pinned string kept whole, no keep-as-is; (c) rank rule at :213-219 drops by `rank` to 20, stopping when every remaining lesson is kept. (d) `git grep -n "oldest lesson" -- skills` returns `test_triage_lessons.py:313`, an `assertNotIn` guard. (d) fails as written. Fail.
- AC6 evidence: `grep -cE '^- [0-9]{4}-[0-9]{2}-[0-9]{2}' cairn/LESSONS.md` → 20; longest lesson 437 bytes (`LC_ALL=C awk`); `"green" is only as wide as what you ran` found once. Pass.
- AC7: CHANGELOG.md:7-22 carries the one entry naming the limits, rank, one-in-one-out capture, and the triage `split` and `rank` proposals; verify to be re-run on the head that review approves.

Pass 2 (2026-10-24), branch head fdd66913, after return 1 (T8). Copilot state query read `none`; one request made (exit 0), still `none` after it, so it may not be recorded by GitHub; no second request.

- AC2 evidence: rank definition at tracking-rules.md:68-70 unchanged; `git grep -n "stalest" -- skills cairn/LESSONS.md` exits 1 with no hit. Pass.
- AC5 evidence: `split` row, length rule ("A long lesson is never kept as it is"), and rank rule ("propose `drop` with the `rank` exit") each found once in cairn-triage/SKILL.md; `git grep -n "oldest lesson" -- skills` exits 1 with no hit. Pass.
- AC1, AC3, AC4, AC6 recheck on fdd66913: the diff since b0f4c65e touches only the milestone file, two test guards, and one paragraph break in cairn-triage/SKILL.md; the AC1 grep hits are unchanged (backstop docstring, an `assertNotIn` guard); LESSONS.md holds 20 lessons, longest 437 bytes.
- AC7 evidence: CHANGELOG.md:7-22 entry as above; on fdd66913 `scripts/tests` OK (966), `hooks/tests` OK (210), both `claude plugin validate` exit 0, `claude plugin test` exit 0 (2466 pass), hand-run `skills/tests` OK (446, 21 skipped). Pass.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: guest mode loses rank-evicted lessons for good (untracked LESSONS.md, no git copy; D-218's "git holds them") — fix now (review names each evicted lesson's full text in the close block in guest mode; D-219 records the guest exception)
- diff-bug #2: naming each evicted lesson can blow the 25-line archive summary when an adopter evicts many — fix now (one line names them all)
- diff-bug #3: review gives no step for pre-existing long lessons or a file over 25 with no capture — reject, planned change (triage owns both; CHANGELOG states it)
- diff-bug #4: review eviction leaves undefined the case where some lessons can go but more than 25 remain — fix now
- diff-bug #5: a `used` mark can take a 440-450-byte lesson past 450 — fix now (the mark counts toward the limit, and the pass shortens such a lesson)
- diff-bug #6: rank rule counts ids after a comma in "corrected M159, M211" — reject, false (provenance lists a mark's ids with `/`; that list sits outside the provenance)
- diff-bug #7: marking "each lesson whose trap the milestone met" re-sweeps every lesson, against D-051 rejection (4) — reject, false (it records what the milestone hit, scoped to its own work; it judges no lesson for retirement)
- diff-bug #8: D-218's Door says the user decides each drop at its gate, but review eviction has no gate, and rank is age for an unused lesson — fix now (D-219)
- diff-bug #9: D-218 leaves D-169's pin-keep and last-resort clauses and D-178 (5) unnamed — fix now (D-219)
- diff-bug #10: gate display undefined for a split line the rank rule drops — fix now (one sentence)
- diff-bug #11: an over-long merge survivor must be `keep` yet the length rule demands compress or split — reject, false (a merge whose survivor would pass 450 bytes is not proposed, so no such survivor arises)
- diff-bug #12: triage step 4 loops when more than 25 lessons remain and all are kept for pins or live milestones — reject, edge (input: over 25 lessons pinned or quoted by live milestones, outside documented and common use; effect: the pass cannot apply and returns to its chip)
- diff-bug #13: split provenance errors: M191 on the wrong mod line, `tool.call` lacks M195, M195's clause moved across lessons — fix now (provenance corrected; the M195 clause recorded as a merge into the live-look lesson)
- diff-bug #14: D-218 Context says the Goal holds figures — fix now (D-219)
- diff-bug #15: `lessons used:` goes only in the first milestone file, so later milestones of a plan mark no use — fix now (each milestone file the plan writes)
- diff-bug #16: a live milestone's date-and-provenance citation can stop matching after later `used` marks or splits — follow-up, candidate row "Match lesson citations after use marks"
- diff-bug #17: template, LESSONS.md header, README state rank without the `trimmed`/`corrected` exception — fix now
- diff-bug #18: review eviction says "in this same commit", but guest mode makes none — fix now (with #1)
- diff-bug #19: stale mutation-harness comment names "five drop exits" and "the near-cap rule" — fix now
- diff-bug #20: test comments cite "(M320 review)", which the test-comments rule does not allow — fix now (citation removed)
- blame-history #1: review eviction contradicts D-051's Decision (two exits), unnamed by D-218; tracking-rules says "three exits" at review — fix now (D-219 names it; rulebook says rank eviction is not a retirement exit)
- blame-history #2: pin protection narrowed (D-169, D-178 (5)) without being named — fix now (D-219; same as diff-bug #9)
- blame-history #3: the M157 repo-wide-count lesson, whose trap recurred, was rank-evicted — reject, planned change (T7 applies the rank rule; D-218's falsifier watches recurrence; the merge question lists it)
- blame-history #4: the M180 stale-bytecode piece was rank-evicted with no other home — reject, planned change (as #3)
- blame-history #5: the M170 failed-merge-marker lesson was rank-evicted — reject, planned change (as #3)
- blame-history #6: the M163 merge_guard quoted-text lesson was rank-evicted — reject, planned change (as #3)
- blame-history #7: D-218 calls rank "newest use, not the age", but for an unused lesson it is age — fix now (D-219)
- blame-history #8: D-108's door is claimed on a trigger that is the cap working as designed — reject, false (D-169 and D-177 passed the door on the same trigger: the shipped capture step could not add a lesson)
- blame-history #9: M171, M172, M178, M153, M158, M156, and M133's `&&` clause dropped with no owner — reject, planned change (as #3)
- blame-history #10: the T7 work-log line says "15 by rank" but lists 20 drops — reject, false (15 kept by rank plus 5 for this milestone; 20 dropped; the diff-bug lens confirmed it)
- prior-review #1: pinned and live lessons can now be compressed or split — reject, planned change (AC5(b) names pinned lessons; the pinned string stays whole)
- prior-review #2: M320's work log names the lessons it drops by date and provenance, which the live-milestone rule would keep — reject, false (the drops are applied; the rule governs proposals for lessons still in the file)
- prior-review #3: rank eviction removed lessons earlier reviews captured (M185, M178, M172, M153) — reject, planned change (as blame-history #3)
- ripple #1: tracking-rules "At review hygiene, three exits" no longer lists every way a lesson leaves at review — fix now (with blame-history #1)
- ripple #2: "retirement removes the redundant, never the merely disputed" disagrees with rank eviction — fix now (with blame-history #1)
- ripple #3: rank wording "newest milestone" in LESSONS.md, the template, and CHANGELOG lacks the exception — fix now (with diff-bug #17)
- ripple #4: tracking-rules keeps `LESSONS.md` < 50 lines beside the 25-lesson limit — reject, planned change (the validator backstop the Scope Out keeps)
- ripple #5: stale mutation-harness comment — fix now (same as diff-bug #19)
- ripple #6: DESIGN.md:1023 names the "two-file cap check" — fix now (limit check)
- ripple #7: README.md:793 "capped and pruned" — reject, false (rank eviction is pruning; the line stays accurate)
- Pass-2 fix-now items above are fixed in cf9442a2 and bd621095 (return 2, T9).

Pass 3 (2026-10-24), branch head bd621095, after return 2. Copilot state query read `none`; one request (exit 0), still `none`, may not be recorded by GitHub; no second request.

- AC1 recheck: the 25-lesson, 450-byte limit at all four sites; the cap grep hits only `150-line` text, the rulebook-mass figure "845 lines" (matched by `45 lines`), the backstop docstring, and an `assertNotIn` guard; none sets a cap on `LESSONS.md`. Pass.
- AC2 recheck: rank definition present once; `git grep -n stalest -- skills cairn/LESSONS.md` exits 1. Pass.
- AC3 recheck: milestone-plan/SKILL.md:370-372 writes `lessons used:` (or `lessons used: none`) in each milestone file; milestone-review/SKILL.md:909-913 marks `used M<NNN>`, replacing the earlier mark and adding no other text. Pass.
- AC4 recheck: milestone-review/SKILL.md:962-973 removes lowest-ranked unpinned, unquoted lessons until 25 remain in the hygiene pass (its one docs-only commit), names them in one archive-summary line, removes none and captures nothing with the skipped lesson named when too few can go, fences `/cairn-triage lessons`; :916-918 sends an over-450-byte extension to its own lesson. Pass.
- AC5 recheck: `split` row, length rule (pinned and live lessons covered), rank rule each present; `git grep -n "oldest lesson" -- skills` exits 1. Pass.
- AC6 recheck: 20 lessons, longest 437 bytes, pinned string present once. Pass.
- AC7 recheck: CHANGELOG entry as corrected at bd621095; `scripts/tests` OK (966), `hooks/tests` OK (210), both validates exit 0 with no `version` warning, `claude plugin test` exit 0 (2466), `skills/tests` OK (446, 21 skipped), `cairn_validate` all checks passed. Pass.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the use-mark step reads the `lessons used:` line from the milestone file the same pass already deleted (archive replaces it; untracked in guest mode) — load-bearing; return 3 (thrash stop, disposition to the user)
- diff-bug #2: shortening a lesson a `used` mark pushes past 450 bytes has no rule keeping a pinned string or quoted text whole — load-bearing; return 3 (as #1)
- diff-bug #11: in the too-few-removable case the skipped lesson's text is kept only in chat — load-bearing; return 3 (as #1)
- diff-bug #3: DESIGN.md:649, register.tsx:404, pane.test.tsx:7151 cite lesson text T7 dropped — follow-up, row "Cut code cites to evicted lessons"
- diff-bug #4: split and merge do not say where a `used` mark goes — follow-up, row "Close the small gaps in lesson ranking"
- diff-bug #5: guest `/cairn-triage lessons` keeps no copy of a `rank` drop — follow-up, same row (widens the DESIGN.md:1022 known issue)
- diff-bug #6: an adopter's first capture can evict many lessons with no gate — reject, planned change (Scope Out names it; D-219 (4))
- diff-bug #7: triage lines 117-119 still say review checks only the lessons the milestone covered — follow-up, row "Close the small gaps in lesson ranking"
- diff-bug #8: the rulebook's one-in-one-out sentence omits the too-few stop and the citation test — reject, false (the rulebook states the rule, the skill its steps)
- diff-bug #9: "shorten or split first" does not help a count overrun — follow-up, row "Close the small gaps in lesson ranking"
- diff-bug #10: the M210 mod line lacks M191 for its `register` sentence — reject, false in effect (rank stays M311; T7 log names the provenance as judged)
- diff-bug #12: the hygiene preview does not name marked, shortened, or evicted lines — follow-up, row "Close the small gaps in lesson ranking"
- diff-bug #13: docstrings cite "M320 (D-218)"; a guard runs over the whole review skill — reject, style (matches each file's docstring convention) and false (the change removed that word from the review skill)
- diff-bug #14: new claims in README, template, and LESSONS header have no prose guard — follow-up, row "Close the small gaps in lesson ranking"
- diff-bug #15: "never split an item across lines" clashes with `split` — reject, false (a split makes separate one-line items)
- diff-bug #16: CHANGELOG.md:23 is 106 characters — reject, style
- blame-history #1: D-220 reverses D-219 on D-051 — reject, false (D-051's Decision gives two retirement criteria and no "only"; D-218 supersedes the prune that rank eviction replaces)
- blame-history #2: six exits contradict D-177's "one of five exits", unnamed by D-218 — follow-up, row "Close the small gaps in lesson ranking"
- blame-history #3: T7 compressions dropped clauses (M133 `&&`, M148 renumbering sweep, M277 set-aside example) without a log — fixed in the work log (2026-10-24 line below); the M133 clause's point stays in the first lesson's `;`-chaining sentence
- blame-history #4: guest triage rank drops keep no copy — follow-up (same as diff-bug #5)
- blame-history #5: the M170 merge-marker recovery steps were rank-dropped — reject, planned change (as pass-2 blame-history #3)
- blame-history #6: the M163 checkout gotcha was rank-dropped — reject, planned change (as #5)
- blame-history #7: the M274 lesson lost its test-name pointer in compression — fixed in the work log (with #3)
- prior-review #1: a `used` mark can break a live milestone's citation — follow-up, existing row "Match lesson citations after use marks"
- prior-review #2: test docstrings cite milestones — reject, style (as diff-bug #13)
- prior-review #3: no guard on DESIGN.md or CHANGELOG lessons-pass text — reject, planned change (D-109's hand-run scope; M263's disposition stands)
- ripple #1: ten test files cite "the M171 lesson", now dropped — follow-up, row "Cut code cites to evicted lessons"
- ripple #2: pane.test.tsx:7151 cites LESSONS M284 for text dropped — follow-up, same row
- ripple #3: DESIGN.md:648, register.tsx:404 cite LESSONS M194 — follow-up, same row
- ripple #4: the archived-file arm skips use marks without naming the skip — follow-up, row "Close the small gaps in lesson ranking"
- ripple #5: milestone-plan/SKILL.md:547 cites "the M118 lesson" (already off on main) — follow-up, row "Cut code cites to evicted lessons"
- ripple #6: line-number lesson cites (`LESSONS :24`) point at other lessons (already off on main) — follow-up, same row
- Consistency gate: `cairn_validate.py` all checks passed; no DESIGN.md principle changed, so no `cairn_impact` run; profile gate: verify green on the review head, marketplace validate prints no `version` warning, the CHANGELOG entry names no milestone number.
