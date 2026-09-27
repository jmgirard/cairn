# M189: Ingest the Opus 5.5 prompting guide — an early-stop clause for the between-gate stretches, and the effort notes re-scaled

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — a rulebook conduct bullet changes how every downstream repo's sessions end their turns
- **Branch/PR:** m189-opus-5-5-guide

## Goal

Ingest Anthropic's "Prompting Claude Opus 5.5" guide as a cited source note and adopt the one conduct rule it supplies that cairn lacks: a between-gate early-stop clause naming the turn endings that stop work while it is still owed.

## Scope

**In:** the source note (`cairn/references/prompting-opus-5-5.md`) with a per-section disposition of the guide; one rulebook bullet in "Question gates and phase closes" scoped to the stretches between gates; dated observations in `prompting-opus-5.md` and `effort-experiment-notes.md` recording the guide's statement that Opus 5 patterns remain a reasonable starting point and its effort-scale shift; a dated re-check note on the ROADMAP's effort-dial candidate row. The bullet is a rule about turn-ending conduct, outside D-108's door (rules about verification or records); D-039's central-rule-only placement applies.

**Out:** the guide's time-signal sentence for subagent prompts (not adopted at the plan gate — cairn's fan-outs are small and its reviewers exist to verify, which the sentence trades away; recorded in the source note's disposition list); a low-effort trial of cairn sessions (a user session setting, not a plugin change — the gate chose the dated observation alone); a prose guard for the new bullet (declined at the gate — `skills/tests` gates nothing since D-109); the guide's "status notes in the same message as the next tool call" clause (conflicts with the Mandated-substance rule; never imported); the "treat earlier answers as settled" chat instruction (the guide itself excludes agentic tasks); sections the Claude Code harness already applies (pasted-text marking, the progress reminder) or that have no cairn surface (thinking disabled, safeguard refusals, visual inputs, frontend defaults) — each recorded in the disposition list.

## Acceptance criteria

- [x] AC1: `cairn/references/prompting-opus-5-5.md` exists, authored from `skills/shared/templates/source-note.md`; its Provenance block names the retrieval (`curl` of the page's `.md` sibling, saved on the gitignored shelf as `cairn/references/sources/prompting-opus-5-5.md`, with its byte count) and a dated, verified Extraction status; every quotation in its Extracted values section is found in the shelf copy by a whitespace-collapsed fixed-string match (every quotation a hit); `cairn/references/INDEX.md` carries the page's line and `cairn_validate`'s references check is green.
- [x] AC2: The "Question gates and phase closes" section of `skills/shared/tracking-rules.md` gains one bullet, the early-stop clause, scoped to the stretches between gates, that (a) names in cairn's words the four turn endings the guide's § Unattended agentic runs sample paragraph numbers One to Four as unwanted while work is still owed — the fourth worded so it excludes the phase close block and a task-boundary checkpoint stop — and carries the guide's push to do the next thing instead of offering to wait; and (b) states the wanted-stop test as "nothing can move without the user", with cairn's stops as examples (a gate or decision chip a skill step mandates, an escalation offer, confirmation before an irreversible or destructive action, a checkpoint stop at a task boundary when context hygiene demands one, the phase close block, a timeout stop). The bullet does not import the guide's same-message status-note clause. Evidence: the section's diff, and the source note's Traces-to line pointing at the bullet.
- [x] AC3: `cairn/references/prompting-opus-5.md` Open questions carries a dated observation naming the Opus 5.5 guide and quoting its statement that the Opus 5 patterns "remain a reasonable starting point"; `cairn/references/effort-experiment-notes.md` carries a dated observation attributing to the guide's § Calibrate effort that Opus 5.5 defaults to `medium` and quoting its claim that Opus 5.5 at `medium` "matches or exceeds Claude Opus 5 at `high`", so the notes' recommendation is read against the new effort scale.
- [x] AC4: The source note's Role or Open questions section lists every `##` section of the shelf copy (the domain enumerated by `grep '^## '` over it; twelve at plan time) with a one-clause disposition: adopted (naming the repo site), already covered by an existing cairn rule or by the Claude Code harness (naming which), or not adopted with the reason.
- [x] AC5: The two gating suites are green from the repo root with exit codes checked (`python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`), `python3 scripts/cairn_validate.py` is green, and the hand-run `skills/tests` suite's failing and erroring test ids after the change equal the ids recorded before it in the work log (T4).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T1
- AC5 → T4

## Tasks

- [x] T1: Retrieve the guide (`curl` of the `.md` sibling) to `cairn/references/sources/prompting-opus-5-5.md`; author `cairn/references/prompting-opus-5-5.md` from the template with provenance, citation, role, verbatim extracted values (the four numbered turn endings, the wanted-stop sentence, the human-in-the-loop caution, the "remain a reasonable starting point" and effort-scale statements, the time-signal claim and its verification caveat), the per-section disposition list, and its INDEX line; run the whitespace-collapsed match over every quotation.
- [x] T2: Add the early-stop bullet to `skills/shared/tracking-rules.md` "Question gates and phase closes", after the paragraph carrying "between gates, work autonomously, never dripping questions"; add the source note's Traces-to line for it.
- [x] T3: Append the dated observations to `prompting-opus-5.md` and `effort-experiment-notes.md`; re-check the ROADMAP's "Reasoning-effort dial per spawned agent" row against the Agent tool's current schema and append a dated re-check note to the row.
- [x] T4: Before T2, run the hand-run `skills/tests` suite and record its failing and erroring test ids in the work log; after T1–T3, run both gating suites, `cairn_validate`, and `skills/tests` again, and record the results.

## Work log

- 2026-09-27: created by /milestone-plan.
- 2026-09-27: criteria audit ran in full mode ([O] fresh reader, 11 findings): 8 fixed before the gate (wanted stops phrased as the guide's test with examples; shape four excludes the phase close and checkpoints; the same-message status-note clause not imported; retrieval saved to the sources shelf; whitespace-collapsed quotation match; skills/tests compared by test id; effort default attributed to the guide; "repo site" in AC4), 3 posed as gate questions (between-gate scope vs softer form, the prose guard, T3's row re-check kept as a task with no criterion).
- 2026-09-27: plan gate chose the between-gate early-stop bullet with the guide's push over the softer name-only form and over a candidate row because cairn's between-gate stretches are unattended and the guide says the push is what the model responds to; falsified by a cairn session skipping a stop the rulebook wanted (a gate, a confirmation, a checkpoint) after the bullet ships.
- 2026-09-27: plan gate chose not adopting the time-signal sentence over a candidate row or Explore-only adoption because the guide's own caveat is less verification and cairn's fan-outs are small; falsified by a fan-out measured as a session's wall-clock bottleneck.
- 2026-09-27: plan gate chose a dated observation in the effort notes over a planned low-effort trial because effort is a user session setting, not a plugin surface; falsified by a downstream repo asking cairn to recommend an effort level.
- 2026-09-27: plan gate chose no prose guard for the new bullet over an M152-pattern hand-run guard because `skills/tests` gates nothing (D-109) and a guard adds upkeep without protection; falsified by the bullet drifting or being deleted unnoticed in a later rulebook edit.
- 2026-09-27: implement started on `m189-opus-5-5-guide`; the question gate was skipped — the plan gate settled every open choice and the criteria name the citekey and sites.
- 2026-09-27: T4 baseline, `skills/tests` before T2 at 3af2b45 (661 tests, 4 failures, 1 error): FAIL test_default_branch_parameterized.TestDefaultBranchParameterized.test_cairn_init_fallback_matches_canonical_recipe; FAIL test_default_branch_parameterized.TestDetectionRecipeInGitModel.test_recipe_command_present; FAIL test_lesson_graduation.TestFamilyActuallyLeft.test_partial_coverage_was_trimmed_not_deleted; FAIL test_resume_routing.TestHotfixMergedPrReentry.test_two_way_check_runs_against_the_baseline; ERROR test_mutation_harness.TestRegisteredGuardsFailWhenBlanked.test_each_registered_guard_fails_when_its_block_is_blanked (guard test_default_branch_parameterized).
- 2026-09-27: T1 done — guide fetched (`curl -L` of the `.md` sibling, HTTP 200, 28,306 bytes) to the shelf; `prompting-opus-5-5.md` authored with 14 quotations, all found in the shelf copy by the whitespace-collapsed match (the intro quotation split around a link label); twelve-section disposition in Role; INDEX line added; `cairn_validate` green. The simple-english lint hook reports em-dashes and long sentences in the page; they sit in verbatim quotations and the repo's record convention, left as written.
- 2026-09-27: T2 done — the early-stop bullet added to "Question gates and phase closes" after the "between gates, work autonomously" paragraph: the four unwanted endings in cairn's words (the fourth excluding the phase close block and a task-boundary checkpoint), the push, and the wanted-stop test with cairn's six stops as examples; the same-message status-note clause not imported. The source note's Traces-to line names the bullet by its title.
- 2026-09-27: T3 done — dated observations appended to `prompting-opus-5.md` (the "remain a reasonable starting point" statement) and `effort-experiment-notes.md` (the `medium` default and the `medium`-matches-`high` claim, attributed to § Calibrate effort); the ROADMAP effort-dial row re-checked against the Agent tool's schema (`model` parameter, no effort parameter) and its re-check note appended on the same line.
- 2026-09-27: T4 done — the first scripts run failed one test, the pinned shipped-page ledger in `scripts/tests/test_scripts.py` (`TestShippedPageStateLedger`), which requires every committed references page registered with its state; `prompting-opus-5-5.md` registered as `ok` (a minor discovered sub-task). After that: `scripts/tests` 391 OK exit 0, `hooks/tests` 174 OK exit 0, `cairn_validate` exit 0, `skills/tests` 661 with the same 4 failures and 1 error by id as the pre-T2 baseline line above.
- 2026-09-27: claim audit: 20 claims read, 1 corrected — skills/shared/tracking-rules.md, scripts/tests/test_scripts.py. The correction: the wanted-stop list omitted the external-blocker stop `/milestone-implement` step 8 mandates; added as "a stop at an external blocker a skill step names". Ending Two also re-worded to the guide's own "the user was not going to give". Both re-read once by the same [O] reader: hold. Verify slot re-run clean after the change.
- 2026-09-27: all tasks checked; status → review.
- 2026-09-27: review — five criteria verified with fresh evidence; three-lens review: 21 findings, 15 fixed on the branch, 6 rejected with reasons (Review section); no defect return.
- 2026-09-27: step-7 approval: m189-opus-5-5-guide approved for merge.

## Decisions

## Review

Reviewed 2026-09-27 on `m189-opus-5-5-guide` at 1cf30e6; `origin/main` fetched, 0 commits ahead of the branch point, so no merge was needed.

- AC1 — pass. `cairn/references/prompting-opus-5-5.md` exists with the template's seven anchors in order (`#` title, Provenance, Citation, Role, Extracted values, Traces to, Open questions). Its Provenance block names the `curl -L` retrieval of the `.md` sibling, the shelf path `cairn/references/sources/prompting-opus-5-5.md` (git-ignored, confirmed by `git check-ignore`), and 28,306 bytes, which `wc -c` on the shelf copy reproduces; Extraction reads "verified 2026-09-27 … observed 2026-09-27". A whitespace-collapsed fixed-string match run at review over every quotation in Extracted values: 14/14 hits. `INDEX.md` line 23 carries the page; `cairn_validate` `references index<->disk` PASS.
- AC2 — pass. `git diff origin/main...HEAD -- skills/shared/tracking-rules.md` shows one added bullet in "Question gates and phase closes", after the "between gates, work autonomously" paragraph and before the close-block paragraph, opening "Between gates, the turn does not end while work is still owed". (a) The four unwanted endings appear in order — the recap naming the next step, the offer to carry on, the non-blocking decision list, and stopping to report because the turn has been long or a task landed — the fourth carrying "the phase close block and a task-boundary checkpoint stop are stops the steps name, never this ending"; the push reads "deletes that and does the next thing". (b) The wanted-stop test reads "the ones where nothing can move without the user", with the six named stops plus the external-blocker stop as examples. No sentence places status notes in the same message as the next tool call; the bullet keeps only the carry-on-with-independent-work half of that clause. The source note's Traces to section names the bullet by its title.
- AC3 — pass. `prompting-opus-5.md` Open questions gains a bullet naming *Prompting Claude Opus 5.5* and quoting "remain a reasonable starting point", ending "— observed 2026-09-27". `effort-experiment-notes.md` Open questions gains a bullet attributed to "§ Calibrate effort" stating Opus 5.5 defaults to `medium` and quoting "Claude Opus 5.5 at `medium` matches or exceeds Claude Opus 5 at `high`", ending "— observed 2026-09-27".
- AC4 — pass. `grep '^## '` over the shelf copy lists 12 sections; the Role section's numbered disposition lists 12 items whose `§` names match them one to one (mechanical comparison at review). Each carries adopted-with-site (2: effort notes; 4: the rulebook bullet), already-covered-naming-which (6: `prompting-opus-5.md`'s M152 trace and the harness progress reminder; 10: the harness's pasted-text note), or not-adopted-with-reason (1, 3, 5, 7, 8, 9, 11, 12).
- AC5 — pass. From the repo root at review: `scripts/tests` 391 tests OK exit 0; `hooks/tests` 174 tests OK exit 0; `cairn_validate` all checks passed exit 0; `skills/tests` 661 tests, failures=4 errors=1, the five ids identical to the T4 baseline line in the work log (test_default_branch_parameterized ×2, test_lesson_graduation, test_resume_routing, test_mutation_harness error on the default-branch guard).
- Driving RR: none, so no projection-vs-outcome pairs.
- Consistency gate: `cairn_validate` all checks passed (exit 0) after the Review edits; no principle changed, so `cairn_impact` skipped; the generic profile names no toolchain checks.

Independent review (three lenses, fresh context; surface tier user-facing, so the full fan-out). Every finding and its disposition:

- [O] diff-bug lens, 19 findings, ranked by the reviewer:
  1. The bullet kept two parts of the same-message status-note clause ("a recommendation on an open decision is stated, and the work that does not depend on the answer carries on") without saying where the recommendation goes — fix now: the clause now places it (a gate chip where the decision is the user's and a skill step mandates one, otherwise a Mandated-substance position). AC2 as written names the same-message placement, which the bullet never carried, so no criterion failed.
  2. The guide's second wanted stop ("deliberately protected from you") was dropped, so a guard-hook denial read as a stop to push past — fix now: the wanted-stop test gains that clause and the list gains "a guard hook's denial".
  3. The phase-close/checkpoint carve-out hung off ending four only, and the wanted-stop list read as exhaustive — fix now: the carve-out now follows all four endings; the list is introduced "among them".
  4. Two versions of the checkpoint exemption (one conditioned on context hygiene, one not) — fix now: both conditioned.
  5. The guide's human-in-the-loop caution was quoted but not engaged in disposition 4 — fix now: disposition 4 names the caution and the plan gate's reading; the adoption itself is the plan gate's recorded choice, unchanged.
  6. Disposition 6 said `prompting-opus-5.md` traces the narration-cadence instruction to "Deltas, not dumps" and "Plain style" — verified wrong (no such trace; "Plain style" takes § Response length) — fix now: disposition 6 now names the harness system prompt (read this session) and the "Outcome-first recaps" bullet, and says the Opus 5 page traces the instruction to no cairn bullet. The AC4 evidence line above repeated the wrong name; the criterion's form (a disposition naming what covers the section) held, the harness half of the name was right, and the cairn-rule half is corrected at the gate.
  7. Dispositions 6 and 10 asserted harness behavior with no record of how it was checked — fix now: both now say the note and the reminder were read in the ingesting session, dated; this session's own system prompt carries the `<pasted_content>` note and the harness sent the progress reminder during this review.
  8. The Opus 5 page's new bullet said "the values above stand for the successor model", past the source — fix now: "patterns" are the starting point, and the effort values are said not to carry over, quoting the guide.
  9. The effort-notes bullet said the cohorts ran on Opus 5 / Fable 5; the header dates the high cohort's first days to Opus 4.8 — verified — fix now: the bullet names the boundary.
  10. Seven undated absence claims in the disposition list — fix now: each carries `— observed 2026-09-27` inline.
  11. Disposition 9 (and the plan-owned Scope) said the guide excludes the settled-answers instruction from agentic tasks; the guide excludes it from agentic tasks "where a later step can reveal a mistake in an earlier one" — fix now in disposition 9 (with the quoted qualifier); the Scope wording is plan-owned and stands as written.
  12. Disposition 1 called the Capabilities comparison the § Calibrate effort claim — fix now: the narrower claim is named.
  13. The Open questions preamble dropped the template's "re-checked before the milestone merges" clause — fix now.
  14. No D-entry for a rulebook conduct rule — rejected: the plan gate's four choices are work-log lines, and M152's comparable rulebook bullets took no D-entry; open to the maintainer at the gate.
  15. No CHANGELOG entry for a user-facing rule change — fix now: an Unreleased entry under "Changes that affect existing repos".
  16. The push ("offering to wait deletes that") is not scoped away from a chip's pause option — rejected: a gate chip is a named wanted stop, and its pause option is a chip invariant, not an offer to wait.
  17. "cairn's fan-outs are small" characterizes without a number — fix now in disposition 8 ("at most three reviewers"); the work-log line is history.
  18. "irreversible or destructive" versus "risky or destructive" — fix now: the list item reads "risky, irreversible, or destructive".
  19. Ledger dict placement breaks byte order — rejected: a style nit in an unsorted dict.
- [S] blame-history lens: no findings; the ledger registration, the bullet's carve-outs against the close block, checkpoint, timeout, and chip rules, and the additive observations checked clean.
- [S] prior-review-record lens: no regression; GitHub probe empty. Two judgment calls: (1) the bullet's placement outside the verification-apparatus door is asserted without a D-entry — rejected: the reviewer, the diff-bug lens, and the blame lens each read the bullet as turn-ending conduct, outside that door; (2) a lighter guard standard than M152/M124 for the same section — rejected: the plan gate's recorded choice, with `skills/tests` gating nothing since D-109.
- Return floor: no finding demonstrated a criterion failing; fix-now 15, follow-up 0, rejected 6. Fix-now edits committed on the branch before the push.

Post-triage re-verification (after the fix-now edits):
- AC2 — pass, re-read: the bullet still carries the four endings in order, the fourth still worded "at a point where the skill's steps name no stop" with the phase close block and a hygiene-demanded checkpoint stop excluded in the sentence that follows; the push stands; the wanted-stop test still reads "nothing can move without the user", now with the guide's protected-blocker clause and eight example stops; no sentence places status notes in the same message as the next tool call; the Traces-to line unchanged and still accurate.
- AC1 — pass, re-run: 14/14 quotations found; the three quotations the fixes added (dispositions 1 and 9, the Opus 5 page) also found in the shelf copy by the same match.
- AC4 — pass, re-read: still 12 dispositions matching the 12 shelf sections; disposition 6 now names the harness prompt and the "Outcome-first recaps" bullet.
- AC5 — pass, re-run from the repo root: `scripts/tests` 391 OK exit 0; `hooks/tests` 174 OK exit 0; `cairn_validate` exit 0; `skills/tests` 661, the same 4 failures and 1 error by id as the baseline.
