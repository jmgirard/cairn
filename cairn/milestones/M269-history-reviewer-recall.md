# M269: Test whether Haiku misses history conflicts that Sonnet catches, then pick the history reviewers' model

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Resolves:** —
- **Surface tier:** user-facing — a `move` verdict changes the model of two reviewers in every adopter's `/milestone-review`
- **Branch/PR:** m269-history-reviewer-recall

## Goal

The blame-history and prior-PR-comments reviewers run on the model that a planted-conflict recall test supports, Haiku 5.5 or Sonnet 5.5.

## Scope

**In:** a new note, `cairn/references/history-review-recall.md`, that plants known history conflicts in three local commits. Both models review each commit three times, and an Opus judge marks which planted conflicts each run caught. The note applies a verdict rule fixed before the runs. On `move`, the two reviewers move to Haiku in the skills, with a D-entry that supersedes D-151's history clause and a CHANGELOG entry. On `stay`, no skill or CHANGELOG line changes.

M228 and M264 (`haiku-sonnet-roles.md`, `haiku-sonnet-rerun.md`) counted reported findings that a judge rated valid: Haiku 12, Sonnet 13 over nine runs each, verdict `move`. Neither measured conflicts that a reviewer missed, which is D-016's reason ("can silently drop a real bug") and the reason D-151 kept both reviewers on Sonnet.

**Out:** cost and precision (invalid findings) are not re-measured. They rest on M264's figures, which the note and any D-entry cite. Search stays on Sonnet and stays in the candidate row "Haiku for the remaining Sonnet roles". Effort settings for the history reviewers stay unset (D-157), and no new effort measurement runs.

## Acceptance criteria

- [ ] AC1: The new note `cairn/references/history-review-recall.md` has a Design section with six parts. (1) Three planted-conflict tasks: two under the blame-history lens and one under the prior-PR-comments lens. Each task is a local commit, and the note names its SHA and its parent. At least one task edits skill prose and at least one edits code. (2) The patch of each task's two planted conflicts. Across the four blame-history plants, each of the lens's three forms occurs at least once: undoing a deliberate past addition, bringing back a fixed bug, and contradicting a D-entry. Of the two prior-PR-comments plants, one brings back a defect that an archived review recorded as fixed, and one contradicts a point that an archived review raised. (3) An answer key that names, for each plant, the commit, D-entry, or archived review finding that it conflicts with. (4) The reviewer prompt and the judge prompt. (5) The catch rule. A run catches a plant when one finding cites the plant's file and either a line inside the plant's changed hunk or the changed text, and also names the history that the key names or the milestone, commit, D-entry, or review that carries it. (6) The verdict rule. For each model, take each task's mean recall (plants caught divided by 2) over its three runs, and sum the means over the three tasks. The verdict is `move` when Sonnet's sum is above zero and Haiku's sum is at least 0.9 times Sonnet's sum. Otherwise the verdict is `stay`.
- [ ] AC2: The note's Runs section has one row for each of the 18 reviewer runs (three tasks, two models, three runs each) and one row for each of the nine judge runs. Each reviewer row gives the agent id, the model id from the run's transcript, the run's count of numbered findings, and the judge's mark (caught or missed) for each of the task's two plants. Each judge row gives the judge's agent id and its model id from its transcript. The note states that the label mappings were read only after all nine judges returned. It also states the result of a search over the tool calls and tool results of all 27 transcripts for the note's path, this milestone file's path, and the key and mapping file names. The Verdict section applies the AC1 rule to the marks and states `move` or `stay`. If both models catch all 18 plant-runs, the Verdict section says that the test cannot show a gap on harder plants.
- [ ] AC3: The files under `skills/`, `CHANGELOG.md`, and `cairn/DECISIONS.md` follow the AC2 verdict. If the verdict is `move`, three things are true. (1) In `skills/milestone-review/SKILL.md`, the blame-history and prior-PR-comments lens bullets name Haiku and do not name Sonnet. In the "Model and agent strategy" section of `skills/shared/tracking-rules.md`, the Haiku, Sonnet, and `/milestone-review` review bullets, each read whole with whitespace collapsed, name the two reviewers under Haiku and not under Sonnet. (2) A new `cairn/DECISIONS.md` entry supersedes the D-151 clause that keeps history review on Sonnet, and cites the AC2 verdict and M264 for cost and precision. (3) The Unreleased section of `CHANGELOG.md` says that the two reviewers now run on Haiku. If the verdict is `stay`, `git diff <default-branch>...HEAD -- skills/ CHANGELOG.md` is empty and `cairn/DECISIONS.md` gains no entry.
- [ ] AC4: The profile's `verify` slot passes: the `scripts/tests` and `hooks/tests` unittest suites, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test`. The hand-run `skills/tests` suite also passes.

## Coverage

- AC1 → T1, T4
- AC2 → T2, T3, T4
- AC3 → T5
- AC4 → T5, T6

## Tasks

- [x] T1: Build the plants on parent `c56be32` (main at plan time), picking six conflicts from history at or before it that meet the AC1 form and surface mix. Add one unrelated neutral edit per task. Build each task's commit with a temporary index (`GIT_INDEX_FILE`) and `git commit-tree`, never moving HEAD or the working tree, and store it under a neutral ref name (`refs/probe/<letter>`) with a neutral one-line message. Write the plant patches and the answer key to one key file in the session scratchpad, never in the repo. Write the note's Provenance, Scope, and Design sections with the prompts, the catch rule, the verdict rule, and the key file's sha256 in place of parts (2) and (3). Checkpoint-commit them before any run.
- [ ] T2: Run the 18 reviewer runs as foreground Agent calls (`general-purpose`, `model` set to `sonnet` or `haiku`, `effort` unset). Use the M228 history prompt, changed for a proposed commit with no milestone file, with the lens paragraph from `skills/milestone-review/SKILL.md` at `c56be32`. Save each report in the session scratchpad.
- [ ] T3: For each task and run index, draw labels A and B with `random.SystemRandom` and write the mapping to the scratchpad. Run one Opus judge that reads both reports and that task's key entries, and marks each plant caught or missed for each report by the AC1 catch rule. Read the mappings only after all nine judges return.
- [ ] T4: Copy the key file's patches and key into Design parts (2) and (3), and check that the file still matches the committed sha256. Run the transcript search (AC2). Write the Runs and Verdict sections. Add the note's `INDEX.md` line, its row in the shipped-page ledger test in `scripts/tests/test_scripts.py` (beside `haiku-sonnet-rerun.md`), and a pointer from the last reading of `haiku-sonnet-rerun.md`. After the note records the SHAs, delete the probe refs.
- [ ] T5: Apply the verdict (AC3). On `move`, edit the two lens bullets in `skills/milestone-review/SKILL.md` and the three bullets of the tracking-rules "Model and agent strategy" section. Update the pins and docstring in `skills/tests/test_review_fanout.py`. Append the superseding D-entry, whose Consequences note that the effort-unset evidence for history review (`effort-roles.md`) was measured on Sonnet. Add the CHANGELOG entry. Grep the repo for "Sonnet blame-history", "reviewer (Sonnet)", and "Sonnet prior-PR", whitespace collapsed, and fix each hit outside history records. On `stay`, change no file under `skills/` and no CHANGELOG line.
- [ ] T6: Run the verify slot from the repo root and check each exit code. Hand-run `skills/tests` (AC4).

## Work log

- 2026-10-17: created by /milestone-plan.
- 2026-10-17: tier check: not run — work named at the question set.
- 2026-10-17: question set: which work to plan — history reviewers to Haiku, testing missed findings first and moving only if Haiku holds up; go on to build after the plan — yes.
- 2026-10-17: collision check: absorbs the history-review part of the candidate row "Haiku for the remaining Sonnet roles" (search part stays in the row; the row narrows at post-merge hygiene under either verdict). D-151 keeps history review on Sonnet by the user's choice and is superseded only on `move`. D-016's missed-bug reason is what this test measures. M228 and M264 (done) measured valid findings, not misses. No dropped milestone or standing rejection applies.
- 2026-10-17: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-17: lessons surfaced: run both gating suites after a SKILL.md edit and check each exit code; a wording change sweeps the whole repo for the old phrasing and owes a CHANGELOG task; prose guards in `skills/tests` pin the reviewer names, so hand-run them; quote `====` separators in zsh.
- 2026-10-17: criteria audit (full mode, fresh Opus reader): 7 items, 6 findings, all fixed. (1) Key could leak to reviewers through the committed note: the key stays in the scratchpad with a committed sha256, and AC2 adds a transcript search. (2) Plants varied location only: AC1 now requires each lens form and both surfaces; AC2 adds a ceiling reading. (3) Recall-only rule: Out now says cost and precision rest on M264; AC2 rows record finding counts. (4) Catch rule lived only in a task: now AC1 part (5) with a hunk-or-text rule. (5) Line-based grep misses wrapped prose: AC3 reads named bullets whole; T5 covers the test docstring and the effort note. (6) Judge rows lacked model id and mapping-read timing: added to AC2. AC4: no finding.
- 2026-10-17: plan gate chose planted conflicts with an answer key over scoring each run against the pool of valid findings from M264's runs, because a pool drawn from the same reports is blind to conflicts that both models miss; falsified by a ceiling result where both models catch every plant while a later real review shows a Haiku-only miss.
- 2026-10-17: plan gate chose to take cost and precision from M264 over re-measuring them, because M264 measured both on three runs per task and this milestone's gap is misses only; falsified by a planted-run finding count far from M264's per-run counts.
- 2026-10-17: implement started on branch `m269-history-reviewer-recall`; untracked `cairn-probe.log` and `tsconfig.json` (2026-10-03/04 leftovers, not this milestone's) left unstaged.
- 2026-10-17: T1: plants built by a scratchpad script with `git commit-tree` on `c56be32` under `refs/probe/a`, `/b`, `/c`. A (code): force-push guard back to a local command-position pattern (hotfix #180), merge guard checks only the first chained `gh pr merge` (M72). B (hotfix skill): draft PR opened before approval (D-138, M186), re-land fallback without the user's chip (M73). C (implement and review skills): remote-only-commits check moved after the rebase (M267 defect return), review runs its own rebase and push instead of implement's sync (M267 pass 2). Key file sha256 committed in the note; INDEX line and ledger pin (`exempt`, no prices or external source) added now so validate and the scripts suite stay green.

## Decisions

## Review
