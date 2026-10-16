<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M263: /cairn-triage lessons triages LESSONS.md

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — a `/cairn-triage` mode that plugin users run   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m263-triage-lessons, https://github.com/jmgirard/cairn/pull/275   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

`/cairn-triage lessons` proposes one disposition per `cairn/LESSONS.md` lesson at one gate, so lessons can leave the file when the user asks, not only at a milestone's review hygiene.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a `lessons` argument to `/cairn-triage` (`skills/cairn-triage/SKILL.md`)
that runs the pass over LESSONS.md lines only, with the same preconditions,
table, chip, apply, stamp, and commit. Lesson meanings for `keep`,
`compress`, `merge`, `drop` (enforcement or ownership exit), and `promote`
(a family that meets the maturation bar, handed to `/milestone-plan`). A
check that keeps lessons that tests pin. A D-entry annotating D-051 and
D-055; the tracking-rules retirement paragraph, README, DESIGN.md, and
CHANGELOG name the pass. A prose guard with mutation entries.

**Out:** plain `/cairn-triage` stays candidates and Known issues only (the
user's choice at the question set). Pruning the stalest lesson stays the
last resort at `/milestone-review` hygiene, and correcting a false lesson
stays with whoever proves it false (D-045); the pass only flags it. The
graduation a `promote` hands on is its own milestone, planned when the
user runs the fenced `/milestone-plan`. Running the pass for real on this
repo is the user's, after the merge.

## Acceptance criteria

- [x] AC1: With the argument `lessons`, `/cairn-triage`
      (`skills/cairn-triage/SKILL.md`) enumerates each line of
      `cairn/LESSONS.md` that opens with `- ` and a `YYYY-MM-DD` date as one
      `lesson` item, listing its source `lesson`, its subject (the text
      after the first `): `, or after the date when the line has none,
      trimmed to about 80 characters), its provenance (the parenthesized
      milestone list after the date), its byte length, and its date, with
      `—` as its priority. A missing `cairn/LESSONS.md`, or one with no
      such line, yields zero items with no failure.
- [x] AC2: The skill states that with no argument the pass enumerates
      candidates and Known issues and no lesson, that an argument other than
      `lessons` stops before enumeration with a close block naming `lessons`
      as the one accepted value, and that the `lessons` pass runs the same
      preconditions, gate, apply, stamp, and commit as the default pass.
- [x] AC3: The skill states a lesson meaning for each of five dispositions
      and proposes no `split`, `route`, or `retitle` for a lesson: `keep`;
      `compress`, shortened or trimmed to the part no other record covers;
      `merge`, folded into a named surviving lesson; `drop`, naming its exit,
      either enforcement (a test by file and test name, quoting the
      assertion that fails on the mistake the lesson warns about) or
      ownership (a `cairn/` tracking file and the section that owns the
      content); `promote`, naming the lesson family and stating each of the
      three maturation conditions (it teaches transferable craft, it was
      extended or consolidated at least twice, and no other exit applies).
      A compressed or merged lesson keeps its `- YYYY-MM-DD (M…)` prefix and
      any `corrected` or `trimmed` mark. A lesson the pass finds false is
      `keep`, its reason naming the record that refutes it. The close block
      fences one `/milestone-plan` per promoted family.
- [x] AC4: The skill states that before it proposes a disposition for a
      lesson, the pass reads each file that `git grep -l "LESSONS.md"` lists
      whose path contains `test` (none listed means no pins and no failure).
      A lesson that holds a string such a file asserts is present in
      `cairn/LESSONS.md` is `keep`, its reason naming the file, and no
      accepted edit writes a string such a file asserts is absent.
- [x] AC5: The skill states that a dropped or merged-away lesson leaves no
      line in `cairn/LESSONS.md`; that after the edits
      `wc -l -c cairn/LESSONS.md cairn/ROADMAP.md` stays under both files'
      line caps and byte budgets, or the pass returns to the chip; that the
      stamp and the commit message name each dropped lesson by its date and
      provenance with its exit, and each merged-away lesson with its
      survivor; that in guest mode the stamp alone names them, with their
      evidence; and that a lesson drop or merge writes no decision entry.
- [x] AC6: The skill's frontmatter `description` and `argument-hint`, its
      H1, README.md's "Prune the backlog" table row, `cairn/DESIGN.md`'s
      `cairn-triage` line, and the tracking-rules paragraph "Retiring a
      lesson that no longer earns its line" each name `lessons` or
      `cairn/LESSONS.md`. That paragraph's sentence "Checked at
      `/milestone-review` post-merge hygiene, scoped to what the milestone
      shipped" is amended to name the on-demand pass. `cairn/DECISIONS.md`
      gains an entry annotating D-051 and D-055 that states the pass and
      why D-051's rejected per-hygiene re-sweep does not reach it.
      CHANGELOG.md's Unreleased section has one entry for the pass.
- [x] AC7: The active profile's `verify` slot is green and the hand-run
      `skills/tests` suite is green.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. Review reads to fence
     evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6
- AC2 → T1
- AC3 → T2
- AC4 → T2, T6
- AC5 → T3
- AC6 → T1, T4
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label. -->

- [x] T1: In `skills/cairn-triage/SKILL.md`, add the `lessons` argument:
      frontmatter `description` and `argument-hint`, the H1, a session-start
      paragraph (the stop on any other argument; the pass reads
      `cairn/LESSONS.md` and its pin files in place of the two lists), and
      step 1's lesson item shape (AC1, AC2).
- [x] T2: Step 2: lesson meanings in the disposition table, the two drop
      exits with their evidence, the maturation bar for `promote`, the
      false-lesson `keep`, and the pin check before any proposal (AC3, AC4).
- [x] T3: Steps 3 to 7 for lessons: the chip and table wording, apply (no
      line left behind; prefix and marks kept), the cap and budget check over
      both files, the stamp and commit naming drops and merges, the guest arm,
      no decision entry, one `/milestone-plan` per promoted family (AC3, AC5).
- [x] T4: Write the D-entry annotating D-051 and D-055; amend the
      tracking-rules retirement paragraph; update README's "Prune the
      backlog" row, DESIGN.md's `cairn-triage` line, and the CHANGELOG
      Unreleased entry. Sweep with `git grep -n "candidates and Known
      issues"` outside `cairn/` for other surfaces that now read short (AC6).
- [x] T5: Add `skills/tests/test_triage_lessons.py`, pinning the argument
      and stop, the lesson item shape, each disposition meaning and exit,
      the pin check, and the cap check, with mutation entries in
      `skills/tests/test_mutation_harness.py`, each seen red; hand-run
      `skills/tests` and run the `verify` slot (AC7).
- [x] T6: Dry run: a fresh subagent follows steps 1 to 3 of `/cairn-triage
      lessons` on this repo up to the table, poses no chip, and writes no
      file; check the table has one row per lesson line
      (`grep -c "^- 20" cairn/LESSONS.md`) and that the two pinned lessons
      read `keep` (AC1, AC4).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: milestone — adds a disposition pass to `/cairn-triage`, skill behavior with design decisions.
- 2026-10-16: question set: when the pass runs — opt-in `/cairn-triage lessons` (over every triage pass, and over not adding it); exits — retire by a named failing test or an owning tracking file, trim, merge, and hand a ready family to `/milestone-plan` (over also pruning the oldest, and over trim and merge only).
- 2026-10-16: collision check: no candidate row, planned milestone, or archive covers a lessons triage; M173 shipped `/cairn-triage` for candidates and Known issues. D-051 read whole: its rejection (4) refuses re-evaluating every lesson each hygiene pass because it taxes every milestone, and its Decision says "never as a full re-sweep"; an opt-in pass the user runs carries no per-milestone cost, so the plan annotates D-051 rather than superseding it (AC6). D-015, D-045, D-055, D-061, D-119, D-027 read whole; none rejects the pass.
- 2026-10-16: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-16: lessons harvested: M165 (LESSONS prunes check the graduation guards first, so AC4's pin check), M112 (sweep every surface that restates the old wording, so T4's grep), M148 and M182 (new prose near a pinned slice; hand-run `skills/tests`), M171 (pin whole lists), M133 (a zsh glob with no match is a hard error, so AC4 uses `git grep -l`).
- 2026-10-16: criteria audit (full mode, fresh Opus reader) returned 12 findings, all taken: D-051's operative text needs a D-entry (AC6) and opt-in posed at the set; subject fallback, provenance, and `—` priority (AC1); ownership exit narrowed to a `cairn/` tracking file (AC3); `promote` states the maturation bar and fences one plan per family (AC3); a false lesson is `keep` (AC3); prefix and marks kept (AC3); "test name" not "method" (AC3); the pin check reads the repo's test files with `git grep` and covers absence asserts (AC4); guest arm and the ROADMAP byte budget (AC5); the stray-argument stop (AC2); the surface list adds the H1 and `argument-hint` and amends the "Checked at" sentence (AC6). AC7 clean.
- 2026-10-16: plan gate chose annotating D-051 over superseding it, because its rejection's reason (a cost on every milestone) does not reach an opt-in pass and its retirement criteria stand unchanged; falsified by a lessons pass found running unasked, or retiring a lesson whose trap then recurs.
- 2026-10-16: plan gate chose a subagent dry run to the table (T6) over posing the triage chip at review, because the chip would add a stop for the user and the table is what the criteria bind; falsified by a defect that shows only in steps 4 to 7 of a real pass.
- 2026-10-16: branch m263-triage-lessons cut from main at 9af1b99d; untracked `cairn-probe.log` and `tsconfig.json` left unstaged.
- 2026-10-16: T1-T3 done in one section: `skills/cairn-triage/SKILL.md` gains "The lessons pass (`/cairn-triage lessons`)" before the workflow, stating each step's change for lessons (argument and stop, pin-file read, item shape, five lesson dispositions with exits and the maturation bar, false-lesson `keep`, apply with the two-file cap check, record, close), plus the frontmatter `description`, `argument-hint: "[lessons]"`, the H1, and one session-start sentence. Chose one section over threading lesson clauses through steps 1-7, because the existing step text is pinned by guards (priority token, guest arm) and a separate section leaves it untouched. It cites D-169, the entry T4 writes. Suites green.
- 2026-10-16: T4 done: D-169 annotates D-051 and D-055; the tracking-rules retirement sentence now reads "…scoped to what the milestone shipped, and over the whole file only when the user runs `/cairn-triage lessons`; prune-the-stalest is the last resort."; README's "Prune the backlog" row and DESIGN.md's `cairn-triage` line name the lessons pass; CHANGELOG Unreleased entry added. `git grep -n -i "candidates and Known issues"` outside `cairn/milestones` and DECISIONS.md found only README:624, DESIGN.md:31, and the skill itself, all now naming lessons. The rulebook grew to 679 lines / 65,305 bytes, so its baseline is re-seeded at all three sites (`skills/milestone/SKILL.md`, `test_cost_audit_line.py`, the mutation block), per the M149 lesson. Suites and `cairn_validate` green.
- 2026-10-16: T5 done: `skills/tests/test_triage_lessons.py` (20 tests, six classes: argument, items, pin check, dispositions, apply and record, surfaces) with 25 mutation entries, each red when blanked (`guard_fails_when_blanked` per entry). Verify slot green: scripts/tests 408, hooks/tests 175, both `claude plugin validate` exit 0 with no version warning, `claude plugin test .` 1777 pass 0 fail; `skills/tests` 786 OK.
- 2026-10-16: T6 done (fresh Opus subagent, read-only, stopped before the chip): 32 lesson items enumerated, equal to `grep -c "^- 20" cairn/LESSONS.md`; 3 of the 10 `git grep` pin files assert on the live file; both lessons pinned by '"green" is only as wide as what you ran' read `keep`. Table: 1 `compress` (the M170 lesson's `cd`-spelling clause, restated by the M163 lesson, about 190 bytes), 31 `keep`, no `drop`, no `promote`. Outcome: under D-051's strict exits this repo's pass frees about 190 bytes and no line. It reported 14 places where the section was unclear; fixed in the skill: only assertions on the live file are pins, a line-format pattern and a size assertion are not lesson pins, which session-start reads still run, byte length is the whole line, a stale lesson is `keep` with evidence, length alone never fires `compress`, the merge survivor's edit, "twice" counts over the family, a family whose module was retired is not proposed, the chip names a lesson by date and provenance, and the stamp names exits. Left as the criteria state them: a pinned lesson is `keep` even for a compress that keeps the pin (AC4), ownership needs a `cairn/` tracking file (AC3), compress keeps marks (AC3). It also noted that a real run on this checkout stops at the dirty-tree precondition because of the untracked `cairn-probe.log` and `tsconfig.json`, a precondition that predates M263. One mutation block re-wrapped; 25 entries red, suites and `cairn_validate` green.
- 2026-10-16: claim audit: 46 claims read, 8 corrected — skills/cairn-triage/SKILL.md, skills/shared/tracking-rules.md, skills/tests/test_mutation_harness.py, skills/tests/test_cost_audit_line.py, CHANGELOG.md. (1) A retired module is found by `git grep -n "<module>.md" cairn/DECISIONS.md` over the bodies, since no heading names `guard-doctrine.md` (D-114 retired it). (2) The description scopes "principled drops as a decision" to the default pass. (3) A lesson merge names no trigger class. (4) A false lesson "is corrected in place at a milestone, not in this pass (D-045, D-169)". (5) The mutation comment says blocks are exact substrings. (6) The cost-audit pin comment names M263. (7) CHANGELOG adds the guest-mode caveat. (8) The rulebook's "archive summary names what it graduated" adds "(the stamp and commit message, for `/cairn-triage lessons`)", rewrapped to the 120-column margin. The rulebook is re-measured at 679 lines / 65,365 bytes and re-seeded at its three sites; two mutation blocks follow the rewraps. 34 entries red, verify slot and `skills/tests` (786) green.
- 2026-10-16: implement done; status `review`.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, gate results, findings + triage. -->

Review head 5fffc716, PR #275 (opened at review start, Copilot arm). Evidence is a whitespace-collapsed substring read of the "The lessons pass" section of `skills/cairn-triage/SKILL.md` and the named surfaces, run 2026-10-16.

- AC1: found "`/cairn-triage lessons` runs the pass over `cairn/LESSONS.md`", the item rule ("opens with `- ` and a `YYYY-MM-DD` date"), source `lesson`, the subject rule with its no-`): ` fallback and ~80-character trim, provenance, byte length, date, "Its priority is `—`.", and "A missing `cairn/LESSONS.md`, or one with no such line, yields zero items with no failure." T6's dry run enumerated 32 items against `grep -c "^- 20" cairn/LESSONS.md` = 32. PASS.
- AC2: found "With no argument the pass enumerates the candidates and Known issues and no lesson.", the stop for any other argument naming `lessons`, and "The lessons pass runs the same preconditions, gate, apply, stamp, and commit as the default pass". PASS.
- AC3: found "A lesson takes one of five dispositions, and never `split`, `route`, or `retitle`"; the table's `keep`, `compress` ("Shortened, or trimmed to the part no other record covers."), `merge` (named survivor), `drop` with both exits word for word, `promote` with the family and the three maturation conditions; the prefix-and-marks sentence; the false-lesson `keep` naming the refuting record; one `/milestone-plan <family>` per promoted family. PASS.
- AC4: found the pin-file rule (`git grep -l "LESSONS.md"`, paths containing `test`, "None listed means no pins and no failure"), read at session start before step 2's "Before it proposes a disposition for a lesson, the pass checks the pins."; the pinned-lesson `keep` naming the file; "No accepted edit writes a string that a pin file asserts is absent." T6's dry run kept both lessons pinned by '"green" is only as wide as what you ran'. PASS.
- AC5: found the no-line, no-breadcrumb rule; the `wc -l -c cairn/LESSONS.md cairn/ROADMAP.md` check with the return to the step-3 chip; the stamp and commit naming drops by date and provenance with exit and merges with survivor, the guest stamp; "A lesson drop or merge writes no decision entry." PASS.
- AC6: frontmatter `description` ("or with the argument `lessons` every cairn/LESSONS.md lesson") and `argument-hint: "[lessons]"`, the H1 ("…, or of lessons"), README.md:624, DESIGN.md:31-32, and the tracking-rules sentence ("…scoped to what the milestone shipped, and over the whole file only when the user runs `/cairn-triage lessons`; prune-the-stalest is the last resort.", old wording gone) all found; D-169 heading and its "rejection (4)'s reason, a cost on every milestone, does not reach it"; one CHANGELOG Unreleased entry. PASS.
- AC7: scripts/tests 408 OK, hooks/tests 175 OK, both `claude plugin validate` exit 0 with no `plugins[N].version` warning, `claude plugin test .` 1777 pass 0 fail, `skills/tests` 786 OK. PASS.
- Consistency gate: `cairn_validate.py` exit 0; no principle changed, `cairn_impact` skipped; profile gate green, CHANGELOG entry present with no milestone number.
- spawned: diff-bug, blame-history, prior-review.
- diff-bug #1: an ownership drop could delete content the owning section did not already hold, since the pass edits only LESSONS.md — fix now: the exit needs "the section that already holds the lesson's content. The pass moves nothing into it."; D-169 says so, fixed 5020b1cf.
- diff-bug #2: a false lesson's flag lived only in the chat table, and an all-keep pass writes no stamp — fix now: a lesson flagged false or stale makes steps 4 to 6 run for a stamp naming it and its evidence; the D-045 citation now covers only "corrected in place", fixed 5020b1cf.
- diff-bug #3: skipping the live-milestone notes let a pass re-promote or drop lessons a planned milestone is moving — fix now: the notes run, and a lesson a live milestone's file quotes or names is `keep`, fixed 5020b1cf.
- diff-bug #4: D-169's Context said M262's hygiene "could not add a lesson", which M262's archive does not say — fix now: the Context states the cap condition without the M262 claim, fixed 5020b1cf.
- diff-bug #5: `promote` names `skills/shared/`, which an adopting repo does not have — fix now: "A repo with no `skills/shared/` directory gets no `promote`.", fixed 5020b1cf.
- diff-bug #6: the default pass's drop reasons and readiness class were not switched off for lessons — fix now: "A lesson leaves only by the two exits above", the default reasons and readiness named as not applying, fixed 5020b1cf.
- diff-bug #7: a pinned lesson could be edited as a merge survivor — fix now: "A pinned lesson is neither a merge survivor nor merged away.", fixed 5020b1cf.
- diff-bug #8: in guest mode the pin files and enforcement tests were read from the working tree — fix now: read at `<base>/<default-branch>`, as step 2's guest rule states for code, fixed 5020b1cf.
- diff-bug #9: the close block's safety line names `/cairn-triage`, which never re-examines a lesson — fix now: the lessons close names `/cairn-triage lessons`, fixed 5020b1cf.
- diff-bug #10: the two-file cap check sends back a pass that trims but does not get under a cap already exceeded — follow-up, "Lessons triage edges (M263 review)".
- diff-bug #11: tracking-rules' guest-triage sentence names the default pass's drop classes, and review's "nothing else records it" — reject, false: the tracking-rules sentence describes the default pass, whose guest stamp still names those classes, and the lessons section states its own guest stamp; the review sentence governs review hygiene's own retirements.
- diff-bug #12: the maturation bar dropped D-055's "about authoring or verifying, not a fact about this repo's tools or runtime" — fix now: the full condition, pin and mutation block updated, fixed 5020b1cf.
- diff-bug #13: a bad argument was refused only after the owner-mode fetch and pull — fix now: "That check runs first, before the owner-mode preconditions.", fixed 5020b1cf.
- diff-bug #14: the claim-audit work-log line says "34 entries red" where the M263 entries number 25 — noted: 34 counted the 25 `test_triage_lessons` entries plus the 9 `test_cost_audit_line` entries checked in the same run; 25 are new.
- diff-bug #15: the H1, DESIGN.md line, CHANGELOG entry, and D-169 have no guard pin — reject, proportionality: AC6 is verified by reading them, and D-109 owes no guard for each surface.
- diff-bug #16: test comments cite lessons by line number ("LESSONS :49"), which go stale after any drop — follow-up, "Lessons triage edges (M263 review)" (pre-existing pattern).
- blame-history #1: in guest mode a dropped lesson has no git copy, and the stamp alone outlives it until the next pass — follow-up, "Lessons triage edges (M263 review)" (the same gap as "Guest triage drop evidence outlives one stamp").
- blame-history #2: same as diff-bug #8 — fix now, fixed 5020b1cf.
- blame-history #3: review hygiene's cap-bite path did not name the new pass — fix now: `skills/milestone-review/SKILL.md` step 9 fences `/cairn-triage lessons` when the cap bites; the pinned "never re-sweep every lesson" sentence stays, fixed 5020b1cf.
- blame-history #4: the pass frees almost nothing on this repo (T6: one compress, no drop) — noted, stated at the merge question.
- blame-history #5: D-169 is framed as an annotation, not a narrowing — reject, planned change: AC6 asks for an entry annotating D-051 and D-055, and D-051's exits stand unchanged.
- blame-history #6: D-169 did not say how it passes D-108's door on new record rules — fix now: D-169 walks the door on its retained trigger (the review skill's lesson capture had no room at the caps), fixed 5020b1cf; surfaced at the merge question.
- blame-history #7: the retired-module grep cannot tell a creation from a retirement — fix now: "read each hit, since an entry that created the module did not retire it", fixed 5020b1cf.
- blame-history #8: same as diff-bug #3 — fix now, fixed 5020b1cf.
- blame-history #9: the ownership exit cannot move content — fix now, with diff-bug #1, fixed 5020b1cf.
- blame-history #10: `git grep -l "LESSONS.md"` misses a test that builds the path — follow-up, "Lessons triage edges (M263 review)".
- prior-review #1: same as diff-bug #8 (M235's guest base-ref fix) — fix now, fixed 5020b1cf.
- prior-review #2: same as blame-history #1 — follow-up.
- After the fixes: 25 mutation entries red, verify slot green (scripts 408, hooks 175, both validates, plugin test 1777 pass 0 fail), `skills/tests` 786 OK, `cairn_validate` green, rulebook unchanged at 679 lines / 65,365 bytes.
- copilot: cairn/milestones/M263-triage-lessons.md:14 (PR URL in the header) — fix now, fixed 5fffc716.
- copilot: skills/tests/test_triage_lessons.py:211 (pin DESIGN.md and CHANGELOG too) — reject, proportionality (D-109); same as diff-bug #15.
- copilot: cairn/milestones/M263-triage-lessons.md:157 (work log's 65,305 vs 65,365) — reject: the work log is append-only history, and the later claim-audit line records the re-measure.
- copilot: review body (3 findings, each anchored to a thread above) and 3 empty-body reviews from the replies — noted.
- Copilot level: Lite (set by GitHub's settings); reviewed an earlier head. PR conversation: no issue comments, no other reviews.
