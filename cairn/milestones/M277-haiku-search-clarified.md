<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M277: Search subagents run on the model a clarified re-test supports

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — a `move` verdict changes the model of every adopter's Explore search subagents   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m277-haiku-search-clarified   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Explore searches run on the model that a search re-test with a clarified S2 prompt supports, Haiku 5.5 or Sonnet 5.5.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a new note, `cairn/references/haiku-search-clarified.md`. It runs M228's three search tasks (S1, S2, S3) three times on each model. S1 and S3 keep their prompts. S2's prompt says that the base name includes the `.py` extension. The note applies M264's verdict rule, fixed before the runs. On `move`, every skill that routes Explore searches to Sonnet routes them to Haiku. A D-entry supersedes the clauses of D-151 and D-174 that keep search on Sonnet, and a CHANGELOG entry says so. On `stay`, no skill or CHANGELOG line changes.

M228 and M264 (`haiku-sonnet-roles.md`, `haiku-sonnet-rerun.md`) gave search `stay`. In M264 Haiku scored 1.9962 and Sonnet 2.8865. Every Haiku S2 run there listed all nine registrations but wrote each script without `.py`. S2's prompt asks for "the Python file's base name" and does not say whether the extension is part of it.

**Out:** S3's prompt stays as written. It states its counting rule in full, and Sonnet's 45-pair runs read past it. Edit work (D-151) and the history reviewers (D-174) are not re-tested. Effort settings stay unset (D-157), and no effort run is made on Haiku search. A search task with an open answer, like a plan-time investigation, is not measured. The D-entry's falsifier names that case.

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

- [ ] AC1: The new note `cairn/references/haiku-search-clarified.md` has a Design section with four parts. (1) The runs. Tasks S1, S2, and S3 of `haiku-sonnet-roles.md` each run six times. The Agent tool's `model` is `sonnet` in three runs and `haiku` in three. Every run uses the `Explore` agent type with `effort` unset. Each run reads its own `git archive c023018` copy in the session scratchpad. (2) The prompts. S1's and S3's are the `haiku-sonnet-roles.md` text with the repository path replaced by the copy's path. S2's differs from that text only in its FORM value, where "the Python file's base name" becomes "the Python file's base name including its `.py` extension, for example `cairn_next.py`". (3) The scoring rule and answer keys of `haiku-sonnet-roles.md`, and the cost method of `haiku-sonnet-rerun.md`. (4) The verdict rule of `haiku-sonnet-rerun.md`. For each model, take each task's mean score and mean cost over its three runs, and sum each over the three tasks. The verdict is `move` when three things hold: Sonnet's summed score is above zero, Haiku's summed cost is below Sonnet's, and Haiku's summed score is at least 0.9 times Sonnet's. Otherwise it is `stay`. The Design section names the SHA of the commit that adds it. Its text at HEAD is byte-identical to its text at that commit, and that commit's committer date is earlier than the first record of each run transcript the Runs section lists.
- [ ] AC2: The note's Runs section has one row for each of 18 counted runs, three per task and model. Each row gives the agent id, the model ids on the run transcript's assistant records, the token counts, the cost by the AC1 cost method, and the score. Each `sonnet` row's model ids are `claude-sonnet-5-5` alone, and each `haiku` row's are `claude-haiku-5-5` alone. A run whose transcript shows other model ids is not counted, and the note lists it with its ids. No counted run's tool calls name a path under the live checkout `/Users/jmgirard/github/cairn/`. Each row's score is the F1 of that run's `ANSWER:` items against its task's key, under the AC1 scoring rule. The Verdict section applies the AC1 rule to the rows and states `move` or `stay`.
- [ ] AC3: The files under `skills/`, `CHANGELOG.md`, and `cairn/DECISIONS.md` follow the AC2 verdict. If the verdict is `move`, four things are true. (1) The "Model and agent strategy" section of `skills/shared/tracking-rules.md` names fan-out searches (Explore) in its Haiku subagents bullet, read whole with whitespace collapsed. No bullet of that section names Sonnet as a model that a role's spawn sets. (2) `skills/milestone-plan/SKILL.md` step 2, `skills/milestone-implement/SKILL.md` step 5, `skills/design-interview/SKILL.md`, and `skills/cairn-triage/SKILL.md` each name Haiku for their Explore spawns. Each line that `git grep -n -i sonnet -- skills ':!skills/tests'` prints sits in a sentence that names Sonnet as the model of a past measurement, never as the model that a role's spawn sets. (3) A new `cairn/DECISIONS.md` entry supersedes D-151's clause that keeps search on Sonnet and D-174's clause "Explore searches stay on Sonnet (D-151)". It cites the AC2 verdict. (4) The Unreleased section of `CHANGELOG.md` says that Explore searches now run on Haiku. Its entry "Edit-work subagents run on Haiku 5.5" no longer says that Explore searches stay on Sonnet. If the verdict is `stay`, `git diff <default-branch>...HEAD -- skills/ CHANGELOG.md` is empty and `cairn/DECISIONS.md` gains no entry.
- [ ] AC4: The profile's `verify` slot passes. That slot is the `scripts/tests` and `hooks/tests` unittest suites, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test`. The hand-run `skills/tests` suite also passes.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2, T3
- AC3 → T4
- AC4 → T3, T4, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: Write the note's Provenance, Scope, and Design sections (AC1). Quote the old and the new S2 FORM value and state the verdict rule. Checkpoint-commit them before the first run, and name that commit's SHA in the Design section in a later commit outside the section's text.
- [ ] T2: Make one `git archive c023018` copy per run in the session scratchpad. Run the 18 runs as foreground Agent calls (`Explore`, `model` set to `sonnet` or `haiku`, `effort` unset). A foreground call's Agent tool result carries `usage`. Read each transcript's model ids, and rerun any run whose ids are not the expected model.
- [ ] T3: Score each run's `ANSWER:` items against the keys of `haiku-sonnet-roles.md`. Cost each run from its transcript and its Agent tool result. Search the 18 transcripts' tool calls for the live checkout path. Write the Runs and Verdict sections, with per-run notes on missed and extra items. Add the note's `INDEX.md` line. Add its row in the shipped-page ledger test in `scripts/tests/test_scripts.py`, beside `haiku-sonnet-rerun.md`. Add a pointer from the search reading of `haiku-sonnet-rerun.md`.
- [ ] T4: Apply the verdict (AC3). On `move`, make these edits. In tracking-rules "Model and agent strategy", move fan-out searches (Explore) and its reading-list clause into the Haiku subagents bullet. Remove the Sonnet subagents bullet, and drop Sonnet from the "Set the model on every spawn" list. Change the four Explore sites AC3 (2) names to Haiku. Add a pin to `skills/tests/test_review_fanout.py`: the Haiku bullet names fan-out searches, no Sonnet subagents bullet remains, and the four sites name Haiku for Explore. See the pin red on a planted revert at the rulebook and at one skill site. Re-measure the rulebook-size seed at its three sites (`skills/milestone/SKILL.md`, `test_cost_audit_line.py`, `test_mutation_harness.py`). Append the superseding D-entry. Its falsifier is a real Haiku Explore fan-out that misses a site that a Sonnet rerun of the same prompt finds. Its Consequences say that the effort-unset evidence for search (`effort-roles.md`) was measured on Sonnet. Add the CHANGELOG entry and revise the M229 entry's Sonnet sentence. Grep the repo outside history records for "Sonnet Explore" and "Sonnet for Explore", whitespace collapsed, and fix each hit. On `stay`, change no file under `skills/` and no CHANGELOG line.
- [ ] T5: Run the verify slot from the repo root and check each exit code. Hand-run `skills/tests` (AC4).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: not run — work named at the question set.
- 2026-10-18: question set: what to work on — the Haiku search re-test with a clarified S2 prompt, which changes the search model if Haiku passes. After the plan — go on to implement.
- 2026-10-18: collision sweep: absorbs the candidate row "Haiku for the remaining Sonnet roles" in full (its promotion is the maintainer's wish for this re-test). Builds on M228, M264 (search `stay`), D-151, D-174, D-157. No open issues or PRs (inbox sweep: 0 and 0).
- 2026-10-18: lessons applied: run each gating suite from the repo root with exit codes checked (M56); re-seed the rulebook size at all three sites (M149); keep the "reading list" phrase that `test_rulebook_polish.py` pins (M148).
- 2026-10-18: plan gate chose 18 fresh runs over reusing M264's S1 and S3 runs because one session and harness state keeps the six cells comparable; falsified by fresh S1 or S3 means that differ from M264's by more than run-to-run range.
- 2026-10-18: plan gate chose to clarify S2 alone over clarifying S3 too because S2's "base name" is ambiguous and S3 states its rule in full; falsified by a reading of S3's prompt that admits Sonnet's 45-pair answer.
- 2026-10-18: plan gate chose a new note over a section in `haiku-sonnet-rerun.md` because that page is M264's fixed run record with its own provenance; falsified by a reader who needs both runs on one page to apply either verdict.
- 2026-10-18: criteria audit (full, fresh Opus reader): 8 findings, 7 fixed. AC1 now pins the Design text at HEAD byte-identical to its commit; S2's change is the FORM value with "base name" kept and a non-key example; AC2 sets aside runs on other model ids and bars tool calls into the live checkout; AC3 (3) also supersedes D-174's search clause; AC3 (2) names the four Explore sites and judges grep lines in their sentences; the effort gap joins T4's D-entry. Rejected: adding the test pin as a criterion (an instrument, so it stays in T4, widened to the four sites). The candidate row needs no criterion: post-merge hygiene graduates it by its started token.
- 2026-10-18: implement started on branch `m277-haiku-search-clarified`. Untracked `cairn-probe.log` and `tsconfig.json` predate the milestone and stay unstaged.
- 2026-10-18: T1: Design section written and committed before any run. Its SHA goes in the Design heading in a later commit, so the section body under the heading stays byte-identical (AC1's "text" read as the body). The INDEX line and the shipped-page ledger row moved up from T3 so the validator and `scripts/tests` stay green at this checkpoint (418 and 179 tests OK).

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
