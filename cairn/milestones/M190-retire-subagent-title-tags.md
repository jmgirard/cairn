<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M190: Retire the subagent model-tier title tags

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the skill prose is what an adopting repo's session follows   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m190-retire-subagent-tier-tags   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Drop the rule that every subagent title opens with a one-letter model tag, because the Claude desktop app now shows each subagent's model.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** delete the tracking-rules bullet "Subagent titles carry the model
tier". At each skill site where a bracket tag named a role's model (for
example "a fresh-context Opus reader" in place of the tagged form), write
the model name in words. Add one line to the rulebook's "Model and agent
strategy" section: set the model on each spawn with the Agent tool's
`model` setting, so the model the app shows is the one the role calls for.
Re-pin the hand-run `skills/tests` guards that pin a tag. Reword the one
live ROADMAP candidate row that uses a tag. D-141 records the retirement
(plan commit).

**Out:** history files (`cairn/DECISIONS.md`, `cairn/milestones/archive/`,
`cairn/reviews/`) stay as written (IP4). Reference pages keep their tags:
the provenance lines and the two ledgers are snapshots at a named commit.
The `scripts/tests` provenance fixture strings are test data, not the
rule. The rulebook-mass baseline in `/milestone` stays at the M166
figures (gate choice). A per-spawn reasoning-effort setting stays the
existing `[low]` candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: `git grep -nE '\[(S|O|F)\\?\]|tier[- ]tag' -- . ':!cairn/DECISIONS.md' ':!cairn/milestones' ':!cairn/reviews' ':!cairn/references' ':!scripts/tests'` returns no match.
- [ ] AC2: For each line that `git grep -nE '\[(S|O|F)\]' 23e13ec -- skills ':!skills/tests'` lists, other than the retired "Subagent titles carry the model tier" bullet, the sentence that carried the tag names the model the tag stood for (Sonnet, Opus, or Fable) in words after the change.
- [ ] AC3: The "Model and agent strategy" section of `skills/shared/tracking-rules.md` tells the session to set the model on each spawn through the Agent tool's `model` setting.
- [ ] AC4: The profile's verify slot is clean: `python3 -m unittest discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests`, run from the repo root, each exit 0.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2, T3
- AC2 → T1, T2
- AC3 → T1
- AC4 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: `skills/shared/tracking-rules.md`: delete the "Subagent titles
      carry the model tier" bullet (line 475). In "Model and agent
      strategy", add the set-the-model line, worded so it covers Explore
      fan-outs too, and write the model names in the review bullet (lines
      501-504).
- [x] T2: Write the model name in words at each tagged skill site:
      milestone-plan steps 2 and 3, milestone-brief step 3 and the RR
      ingestion audit, milestone-implement step 5 (drop "tier-tag the Agent
      description"), the amendment audit, and the claim audit,
      milestone-review step 5's routing text and lens list, the
      cairn-triage delegation note, and the design-interview
      investigation. Reword the ROADMAP candidate row that says "[O] lens".
      M190's own ROADMAP row, hygiene stamp, and any changelog entry name
      the change in words, never by the bracket tokens, since AC1's grep
      reads those files.
- [x] T3: Re-pin the `skills/tests` guards that pin a tag
      (`test_fresh_context_readers.py`, the three blocks in
      `test_mutation_harness.py`, the docstring and comment in
      `test_review_fanout.py`). Hand-run those three modules: no failure
      beyond the ones each shows at 23e13ec. Run the two gating suites
      from the repo root, each exit code checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-09-29: created by /milestone-plan.
- 2026-09-29: criteria audit (full mode, fresh Opus reader) returned 4 findings, all fixed at the gate: AC1 missed the escaped `\[O\]` pin form and the live ROADMAP row; AC2 was unsatisfiable for the deleted rule bullet and loose at step level (now per sentence); AC3 bound a hand-run module that already errors at base (moved to T3). Re-audit of the revised wording: PENDING.
- 2026-09-29: plan gate chose model names in words plus a set-the-model line over names alone because the app now shows the model a spawn actually runs, which is the inherited default unless the spawn sets one; falsified by a harness where the Agent tool has no model setting.
- 2026-09-29: plan gate chose to leave the rulebook-mass baseline at M166 over re-seeding its three sites because it stood through the later rulebook edits; falsified by a `/milestone` audit reader misreading the growth figure.
- 2026-09-29: re-audit of the revised criteria (same Opus reader, full mode) returned 1 finding and 1 suggestion, both handled in the tasks with no criterion change: AC1 could fail on M190's own ROADMAP row, hygiene stamp, or changelog entry if they quote the tokens (T2 now says they name the change in words), and the set-the-model line should read naturally over Explore fan-outs (T1). AC2 to AC4: no finding.
- 2026-09-29: implement started on m190-retire-subagent-tier-tags. Implement question gate skipped because nothing was open. Guard baselines at 23e13ec: test_fresh_context_readers OK, test_review_fanout OK, test_mutation_harness 1 error.
- 2026-09-29: T1 done. Deleted the title-tag bullet, added the "Set the model on every spawn" bullet under "Model and agent strategy", and wrote the review bullet's models in words. Gating suites: scripts exit 0, hooks exit 0.
- 2026-09-29: T2 done. Model names in words at the 14 skill sites across plan, brief, implement, review, triage, and design-interview, and in the ROADMAP candidate row. Minor amendment: renamed the file from M190-retire-subagent-tier-tags.md to M190-retire-subagent-title-tags.md because AC1's `tier[- ]tag` pattern matched the old path in M190's own ROADMAP row (T2's own-records clause).
- 2026-09-29: T3 done. Re-pinned the three guard modules to the Opus wording. test_review_fanout also needed its three lens pins and its split string capitalized, because T2 opens each lens bullet with the role name. Restored T1's original line break in the review bullet because the rewrap split the pinned "three distinct-evidence reviewers". Results: test_fresh_context_readers OK, test_review_fanout OK, test_mutation_harness 1 error (the base error, the unrelated test_default_branch_parameterized locator). Full skills/tests: 4 failures and 1 error, the same pre-existing set. Gating suites: scripts exit 0, hooks exit 0. AC1 grep: no match. validate green.
- 2026-09-29: claim audit: 12 claims read, 3 corrected — skills/shared/tracking-rules.md, skills/tests/test_review_fanout.py
- 2026-09-29: claim-audit corrections. An unset spawn takes the agent type's or harness default, not always the session model. The unsourced app-display clause was dropped from the rulebook. The test comment's stale "Sonnet scorer" became gate triage. The same reader re-read all three: they hold. D-141 carried the unset-spawn error and an unattributed app claim, so D-142 supersedes those two clauses (one correction entry for the milestone). Suites after the fixes: scripts 0, hooks 0, both guard modules OK.
- 2026-09-29: implement complete; status review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->
