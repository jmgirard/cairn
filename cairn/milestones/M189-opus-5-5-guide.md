# M189: Ingest the Opus 5.5 prompting guide — an early-stop clause for the between-gate stretches, and the effort notes re-scaled

- **Status:** in-progress
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

- [ ] AC1: `cairn/references/prompting-opus-5-5.md` exists, authored from `skills/shared/templates/source-note.md`; its Provenance block names the retrieval (`curl` of the page's `.md` sibling, saved on the gitignored shelf as `cairn/references/sources/prompting-opus-5-5.md`, with its byte count) and a dated, verified Extraction status; every quotation in its Extracted values section is found in the shelf copy by a whitespace-collapsed fixed-string match (every quotation a hit); `cairn/references/INDEX.md` carries the page's line and `cairn_validate`'s references check is green.
- [ ] AC2: The "Question gates and phase closes" section of `skills/shared/tracking-rules.md` gains one bullet, the early-stop clause, scoped to the stretches between gates, that (a) names in cairn's words the four turn endings the guide's § Unattended agentic runs sample paragraph numbers One to Four as unwanted while work is still owed — the fourth worded so it excludes the phase close block and a task-boundary checkpoint stop — and carries the guide's push to do the next thing instead of offering to wait; and (b) states the wanted-stop test as "nothing can move without the user", with cairn's stops as examples (a gate or decision chip a skill step mandates, an escalation offer, confirmation before an irreversible or destructive action, a checkpoint stop at a task boundary when context hygiene demands one, the phase close block, a timeout stop). The bullet does not import the guide's same-message status-note clause. Evidence: the section's diff, and the source note's Traces-to line pointing at the bullet.
- [ ] AC3: `cairn/references/prompting-opus-5.md` Open questions carries a dated observation naming the Opus 5.5 guide and quoting its statement that the Opus 5 patterns "remain a reasonable starting point"; `cairn/references/effort-experiment-notes.md` carries a dated observation attributing to the guide's § Calibrate effort that Opus 5.5 defaults to `medium` and quoting its claim that Opus 5.5 at `medium` "matches or exceeds Claude Opus 5 at `high`", so the notes' recommendation is read against the new effort scale.
- [ ] AC4: The source note's Role or Open questions section lists every `##` section of the shelf copy (the domain enumerated by `grep '^## '` over it; twelve at plan time) with a one-clause disposition: adopted (naming the repo site), already covered by an existing cairn rule or by the Claude Code harness (naming which), or not adopted with the reason.
- [ ] AC5: The two gating suites are green from the repo root with exit codes checked (`python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`), `python3 scripts/cairn_validate.py` is green, and the hand-run `skills/tests` suite's failing and erroring test ids after the change equal the ids recorded before it in the work log (T4).

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

## Decisions

## Review
