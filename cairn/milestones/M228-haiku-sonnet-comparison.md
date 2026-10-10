<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M228: Compare Haiku 5.5 with Sonnet 5.5 on cairn's Sonnet roles

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — a measurement note under `cairn/references/` that no adopter reads   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m228-haiku-sonnet-comparison   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A committed note measures whether Haiku 5.5 does the work of each Sonnet role group for less money and with no loss of quality.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The three role groups come from the "Sonnet subagents" and reviewer
bullets of tracking-rules "Model and agent strategy". Search is the Explore
fan-outs. Edit work is a mechanical sweep and test writing against a spec.
History review is the blame-history and prior-PR-comments reviewers. Each
group gets three replayed tasks. Each task runs once on Sonnet and once on
Haiku from the same prompt. A scoring rule stated before the runs scores
each run, and the subagent transcripts' token counts price it. The note
ends with a verdict per group.

**Out:** A change to the model that any skill names → M229 (planned,
depends on M228). Opus and Fable roles stay as they are, because the
request named only the Sonnet roles. Repeated runs per task → the note's
re-measurement procedure, run only if a verdict is challenged. A
reasoning-effort setting per spawn → the existing `[low]` "Reasoning-effort
dial per spawned agent" candidate row.

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

- [x] AC1: `cairn/references/haiku-sonnet-roles.md` exists with its
      `INDEX.md` line and a `**Provenance.**` block. Its run table holds 18
      rows: nine tasks, three per role group, each run once with the Agent
      tool's model set to Sonnet and once set to Haiku, from the same
      prompt. The edit-work tasks include a mechanical sweep and a
      test-writing task. The history-review tasks include a blame-history
      task and a prior-PR-comments task.
- [x] AC2: Each row records the `model` id taken from every assistant
      record of its subagent transcript. Every id on a Sonnet row begins
      `claude-sonnet-5-5`, and every id on a Haiku row begins
      `claude-haiku-5-5`.
- [x] AC3: Each row's dollar cost is a sum over the distinct `message.id`
      values in its subagent transcript of each token class count times that
      model's price for the class at that call's prompt size, as the cited
      page gives it. The classes are input, 5-minute cache write, 1-hour
      cache write, cache read, and output. Each count comes from that id's
      last transcript record, except one: the run's final call, the last
      distinct `message.id` in the transcript's record order, takes its
      output count from the `usage` of the Agent tool result whose `agentId`
      matches the transcript's file name, and that `usage`'s input and cache
      counts equal the final id's last-record counts. The note states that
      the transcript records output counts at stream start, so each row's
      cost is a lower bound. The note cites the prices from Anthropic's
      published pricing by URL and access date.
- [x] AC4: Each row's quality score follows from its group's scoring rule
      as the note states it, and each rule yields a score of zero or more.
      An answer key, built by a command that the note gives, scores search.
      A target diff or a mutant set that the note gives scores edit work. A
      model-blind Opus judge rates each history-review finding valid or
      invalid.
- [x] AC5: The note gives each role group a verdict. The verdict is `move`
      exactly when Sonnet's summed score over the group's three tasks is
      above zero, Haiku's summed cost is below Sonnet's, and Haiku's summed
      score is at least 0.9 times Sonnet's. Otherwise it is `stay`. Each
      verdict follows from the run table by that rule.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3, T4, T5, T6
- AC2 → T3, T4, T5, T6
- AC3 → T1, T6
- AC4 → T1, T2, T3, T4, T5, T7
- AC5 → T1, T6, T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write the design into the note and commit it before any run.
      The design names the nine tasks and their sources, each prompt
      verbatim, each group's scoring rule, the 0.9 margin, and the price
      source. Search tasks are questions over this repo at a pinned commit.
      Edit work replays a past mechanical sweep commit and a small spec with
      a mutant set. History review replays past milestone diffs whose
      archived Review sections list findings. The prior-PR-comments task
      uses a repo with prior PR review comments. Load the `claude-api`
      skill for the price table, never prices from memory.
- [x] T2: Build each answer key, target diff, and mutant set by the
      procedure that T1 names. Record each one in the note with its command.
- [x] T3: Run the search group with the Explore agent type, `model` set to
      `sonnet` and then `haiku`, same prompt. After the first Haiku run,
      read its transcript's `model` id. If the id is not Haiku 5.5 (a
      2026-09-11 spawn ran as `claude-haiku-4-5-20251001`), stop and set
      M228 `blocked` with the id as the blocker. Record each run's
      transcript path (`~/.claude/projects/<slug>/<session>/subagents/`),
      its `model` ids, its token classes per `message.id`, and its score.
- [x] T4: Run the edit-work group the same way. Give each spawn
      `isolation: "worktree"`, so that no run edits the shared checkout.
      Score each run's diff against its target or mutant set.
- [x] T5: Run the history-review group the same way. Then spawn one Opus
      judge per task. The judge sees both runs' findings under shuffled A/B
      labels and rates each finding valid or invalid against the diff.
      Record the label mapping only after the judge returns.
- [x] T6: Compute each row's cost from its token classes and the cited
      prices, sum the costs per group, and apply AC5's rule. Write the
      verdicts, the single-run limit, and a re-measurement procedure into
      the note. Add the `INDEX.md` line and run `scripts/cairn_validate.py`.
- [x] T7: Review return 1. Re-judge H1–H3 with fresh Opus judges whose
      prompt states the note's validity rule verbatim, and record that
      prompt in the note. Give each mutant's exact old and new strings in
      the note. Apply pass 1's other fix-now findings, and add the
      follow-up candidate row for `cairn_cost.py`.

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

- 2026-10-09: created by /milestone-plan.
- 2026-10-09: question set: which work to plan — the Haiku 5.5 row (ROADMAP candidate "Haiku for Sonnet subagent work", promoted here and in M229; the row graduates at M229's post-merge hygiene). Which roles move — "all, but only if some testing finds it is cheaper and noninferior"; M228 is that testing, M229 the move.
- 2026-10-09: collision: D-016 keeps the "Never Haiku" blanket, saying a weaker model in a gating review step "can silently drop a real bug"; D-110 retired the scorer and left the blanket standing. M228 changes no rule, so nothing is superseded here; M229 supersedes D-016 only on a `move` verdict. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-09: plan gate chose replaying past cairn tasks with stated scoring over citing published benchmarks, because benchmarks do not run cairn's prompts; falsified by Haiku-run roles in later live milestones costing more or missing findings that the replay said they would catch.
- 2026-10-09: plan gate chose one run per model per task over three runs, because 54 spawns cost three times as much for a go/no-go call; falsified by a rerun that flips a group's verdict.
- 2026-10-09: plan gate set the noninferiority margin at 0.9 of Sonnet's summed score; a tighter margin (0.95) was weighed and rejected because three tasks per group cannot resolve a 5% gap; falsified by a later re-measurement that finds the gap larger than 10%.
- 2026-10-09: plan gate chose a model-blind Opus judge for history review over counting overlap with the archived original findings, because the originals ran on older models and are not a complete answer key; falsified by the judge rating as valid a finding that the milestone's own reviewers had shown false.
- 2026-10-09: criteria audit (reduced mode, fresh Opus reader) returned four findings, all fixed: AC2 bound the transcript file and a singular `model` field, so it now binds what each row records, per row type; AC3 summed records, which overcounts because one `message.id` spans several records, so it now sums each id's last record; AC4/AC5 allowed a negative score or a zero Sonnet sum, so AC4 requires scores of zero or more and AC5 gives `stay` on a zero Sonnet sum. The reader also found a 2026-09-11 `haiku` spawn that ran as Haiku 4.5, so T3 now stops and sets `blocked` if the first Haiku run is not 5.5. AC1 drew no finding.
- 2026-10-09: implement started on branch `m228-haiku-sonnet-comparison`. Untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-09: a one-word probe spawn per model before any run resolved `haiku` to `claude-haiku-5-5` and `sonnet` to `claude-sonnet-5-5`, so T3's blocked stop does not fire. The 2026-09-11 Haiku 4.5 spawn the audit found was a `claude-code-guide` agent type, whose own definition sets its model.
- 2026-10-09: the Haiku spawns here are the measurement the question set granted ("only if some testing finds it is cheaper and noninferior"), not delegation, so implement step 5's "never Haiku" does not apply to them.
- 2026-10-09: T1 design chosen: search keys from git grep, a JSON parse, and a heading parse; edit work is one rename sweep (`find_cairn_root`, 20 sites in 11 files) and two test-writing tasks scored on six hand-made mutants each; history review replays M226 and M227 (blame-history) and M225 (prior-PR-comments). Prices read from the live pricing page, which gives Sonnet 5.5 cache reads at $0.10 per million tokens where the `claude-api` skill's cached table says $0.20, so the live page is cited.
- 2026-10-09: T2 built the S1 to S3 keys (10, 9, 89 items), the E1 target (32 lines, 11 files), and 12 mutants, all recorded in the note. A reference test file killed 12 of 12 mutants and an always-true test killed 0 of 6, so the mutant scoring can tell the two apart. Measurement helpers live in the session scratchpad (`m228.py`), not in the repo.
- 2026-10-09: substantive amendment: AC3 rewritten. The search runs showed that subagent transcripts record each call's `output_tokens` at stream start (the Haiku S3 final call shows 6 in its transcript and 4,227 in the Agent tool result's `usage`), so the old formula undercounted output. The new AC3 takes the final call's output from the tool result and states that each row's cost is a lower bound. What the user gets is unchanged: a cost per row and a verdict per group.
- 2026-10-09: re-audit: AC3 (reduced) — first reader returned five findings: the final call was not tied to an id, earlier calls named no record, "undercounts" was unverifiable, Haiku's prompt-size tiers were missing, and the lower bounds could bias AC5; the first four were fixed in the wording, the fifth is answered by the note's robustness statement on the cost comparison.
- 2026-10-09: re-audit: AC3 (reduced) — second reader returned four findings, answered without rewording (a further rewording would be the second-re-audit stop): the price at a call's prompt size is read from the note's table, which records the cited page at its access date and defines prompt size as input plus both cache writes plus cache read; the input-and-cache equality is recorded per row in the note as a cross-check; each row names the main session transcript that holds its one Agent tool result; costs are recorded to four decimal places and recomputed at that precision.
- 2026-10-09: correction to the T2 line: the S3 key holds 88 pairs, not 89, by `len()` of the built key; the note is corrected in place.
- 2026-10-09: T3 ran the six search spawns. Scores Sonnet 1.0, 1.0, 0.6767 and Haiku 1.0, 0.0, 1.0; costs Sonnet $0.3650 and Haiku $0.0218 in sum. Haiku's S2 zero is a format miss (script names without `.py`), scored as the fixed rule says; the note records it. Every row's final match is yes.
- 2026-10-09: T4 ran the six edit spawns in worktrees. Every run scored 1.0 (both sweeps exact, all four test files killed 6 of 6). Costs Sonnet $0.4884 and Haiku $0.0407 in sum. The sweep diffs and test files are saved in the scratchpad; the worktrees are removed at T6.
- 2026-10-09: T5 ran the six review spawns and three Opus judges under labels drawn with `random.SystemRandom`, read after the judges returned. Valid findings Sonnet 5, 3, 2 and Haiku 3, 2, 4. Haiku used 1.9 to 4.0 times as many calls and crossed the 100,000-token tier, so its H3 row cost more than Sonnet's.
- 2026-10-09: T6 verdicts: search `stay` (score ratio 0.7472, from S2's missing `.py`), edit work `move` (ratio 1.0, both at the ceiling), history review `move` (ratio 0.9, exactly at the margin). The output undercount can reverse only the history-review cost comparison (break-even about 870 unrecorded Haiku output tokens per non-final call); the note says so. The six edit worktrees and their branches are removed.
- 2026-10-09: the verdicts are mixed, so M229's T1 will stop for the user, as M229's plan says.
- 2026-10-09: verify first ran red on one test: `TestShippedPageStateLedger` pins every references page's staleness state, and the new note had no pin. Added `haiku-sonnet-roles.md: exempt` (its status says nothing to re-verify against) in `scripts/tests/test_scripts.py`; all five verify checks then passed and `cairn_validate` reports no FAIL.
- 2026-10-09: claim audit: not owed — internal tier
- 2026-10-09: implement complete; status set to `review`.
- 2026-10-09: review return 1: AC4 fails as written for the history-review rows (the judges applied a broader validity rule than the note states, diff-bug #1) and for the edit-work mutants (the note's table does not give the exact strings, diff-bug #7). The other fix-now findings of pass 1 ride the same return; dispositions are in the Review section.
- 2026-10-09: implement resumed for return 1; added T7 for it (minor amendment) and mapped AC4 and AC5 to T7.
- 2026-10-09: correction to the T1 design line: the `find_cairn_root` sweep has 21 sites (21 lines removed and 21 added over 11 files), not 20.
- 2026-10-09: T7 re-judged H1–H3 with three fresh Opus judges whose prompt states the note's rule verbatim, under new shuffled labels read after they returned. Valid findings Sonnet 1, 1, 2 and Haiku 1, 0, 3, so 4 against 4: history review stays `move`, now at a ratio of 1.0 instead of 0.9. The two judgings rate 11 of 22 findings differently; the note records both and the judge prompt.
- 2026-10-09: T7 also gave the note each mutant's exact old and new strings (a parse of the table matches the applied mutants, 12 of 12, each occurring once), corrected the target-diff count, re-dated the page's status as a dated read of the prices (pin moved `exempt` → `ok`, since the prices age), reworded the Scope, the edit-work and verdict readings, added observed dates and the cross-references to `cairn_cost.py` and the price discrepancy, added a "what could flip it" column, and filed the candidate row "Session-store reading in `cairn_cost.py`".
- 2026-10-09: verify passed on all five checks after T7, and `cairn_validate` reports no FAIL or WARN; status set to `review`.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

- 2026-10-09: The 18 Haiku and Sonnet measurement runs, and the one-word probe of each, are an exception to tracking-rules' "Never Haiku. For anything." bullet and D-016's blanket, scoped to this milestone's measurement. The rule stays in force for delegated work; the user granted the test at the plan gate ("only if some testing finds it is cheaper and noninferior"), and a measurement of Haiku cannot run without spawning it. Whether the rule changes is M229's decision, through a D-entry that supersedes D-016. Recorded here after review pass 1 (blame-history #3) found the exception only in the work log.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->

Pass 1, 2026-10-09, on `2620860` (branch current with `origin/main`, no PR yet).

- AC1 evidence: `cairn/references/haiku-sonnet-roles.md` exists, `INDEX.md` carries its line (grep count 1), and it has one `**Provenance.**` block. A parse of the note's run table (`verify_note.py`, scratchpad) finds 18 rows over tasks S1–S3, E1–E3, H1–H3, each task with one `sonnet` and one `haiku` row. E1 is the rename sweep and E2, E3 are test writing; H1, H2 use the blame-history lens and H3 the prior-PR-comments lens; the note's prompts section gives each prompt once for both models.
- AC2 evidence: for each of the 18 rows, the recorded "Model ids" equal the set of `model` values on the assistant records of `subagents/agent-<id>.jsonl`, re-read by `cost_v2`; 0 rows fail. Every Sonnet row's ids are `claude-sonnet-5-5` and every Haiku row's `claude-haiku-5-5`.
- AC3 evidence: recomputing each row from its transcript (distinct `message.id`s in record order, last-record counts, the final id's output from the one Agent tool result with matching `agentId` in the session transcript, Haiku's tier by each call's input-plus-cache sum) reproduces every row's call count, five token columns, final-match flag, and USD to four places; 0 of 18 rows fail, every row finds exactly one tool result, and all 18 final matches are yes. The note states the stream-start recording and the lower bound (Cost paragraph) and cites the prices by URL with "read 2026-10-09".
- AC4 evidence: the note states each group's rule, every rule yields a score of zero or more (F1, Jaccard, killed fraction, valid count). Re-scoring from the tool results' reports and the keys gives S1–S3 scores equal to the table (1.0, 1.0 / 1.0, 0.0 / 0.6767, 1.0). The saved sweep diffs score Jaccard 1.0 each against a rebuilt target, and the four saved test files re-score 1.0 each on fresh `git archive c023018` copies. The three Opus judges' reports read `A valid: 3, B valid: 5` (H1), `3, 2` (H2), `4, 2` (H3), and the sealed mapping turns these into the table's Sonnet 5, 3, 2 and Haiku 3, 2, 4.
- AC5 evidence: applying the rule to the parsed table gives search 0.3650 / 0.0218 USD, 2.6767 / 2.0 score → `stay`; edit 0.4884 / 0.0407, 3.0 / 3.0 → `move`; review 0.6066 / 0.4318, 10 / 9 → `move` (9 ≥ 0.9 × 10). These equal the note's Verdicts table.
- Gate: `cairn_validate` exit 0, no FAIL or WARN lines. Verify on the review head: scripts suite 401 tests OK (21 skipped), hooks suite 174 OK, plugin validate 0, marketplace validate 0 with no `version` warning, mod test 0. No principle changed, so `cairn_impact` is skipped. No changelog entry is owed: the diff has no user-visible change (internal tier; files are tracking, a references page, and one test pin).
- spawned: diff-bug, blame-history, prior-review (the diff touches `scripts/tests/test_scripts.py`, so the full fan-out).
- diff-bug #1: the note states the history-review validity rule as "the history or prior review it cites exists and the diff does conflict with it", but the judge prompts also counted a finding valid when "the diff really does leave something stale or inconsistent", and the judge prompt is recorded nowhere; AC4 requires scores to follow the rule as the note states it — fix now, floor return (AC4 fails as written for H1–H3): re-judge with the design's rule verbatim and record the judge prompt.
- diff-bug #2: "the target diff changes 32 lines in 11 files" is the count of distinct triples; the diff has 21 removals and 21 additions over 21 sites, and the T1 work-log line's "20 sites" is wrong — fix now (note reworded; a superseding work-log line).
- diff-bug #3: the page's status says nothing to re-verify, but its price table comes from a page that can change, and the `exempt` pin turns off the staleness warning for it — fix now (status claims a dated direct read of the prices; pin follows the new class).
- diff-bug #4: Scope says "with no loss of quality", but the rule allows a 10% lower score — fix now.
- diff-bug #5: the edit-work note's "lowest of the three groups relative to the work done" is unmeasured and E3 Haiku has the highest output of all rows; "cannot show a quality gap smaller than these tasks' difficulty" does not parse — fix now.
- diff-bug #6: "one finding either way would flip it" holds only in one direction — fix now.
- diff-bug #7: the mutant table gives descriptions, and `return "owner"` and `re.IGNORECASE` each occur twice in the file, so the mutants cannot be rebuilt from the note — fix now, part of the AC4 floor return ("a mutant set that the note gives"): the note gives each exact old and new string.
- diff-bug #8: "no source gives the true output of earlier calls" is too strong, since prompt growth bounds it from above — fix now (reworded).
- diff-bug #9: "1.9 to 4.0 times as many calls per task" holds only for review tasks — fix now.
- diff-bug #10: the INDEX line omits that final-call output comes from the session transcript — fix now.
- blame-history #1: `scripts/cairn_cost.py` (docstring and report text) and `references/session-cost-notes.md` (row A4, open question) say subagent turns are absent from the store, but `<session>/subagents/agent-*.jsonl` records them, as M228 used — fix now for the note's cross-reference to those claims; follow-up for correcting the script and the older note (new candidate row, door `/hotfix`, since the script prints the false claim to users).
- blame-history #2: `cairn_cost.py` sums every assistant record and never groups by `message.id`, which the reviewer counted as 35,199 records against 14,049 ids, so its turn and cache-read figures run about 2.5 times high, and top-level transcripts also record output at stream start — follow-up (same new candidate row, door `/hotfix`), a pre-existing defect the diff did not introduce; the note gains a cross-reference.
- blame-history #3: the Haiku spawns' exception to the "never Haiku" rule is recorded only in the work log — fix now (milestone-local Decisions entry).
- blame-history #4: the Verdicts table prints history review `move` with no marker of its margin and its uncertain cost comparison — fix now (a column for how robust each verdict is).
- blame-history #5: the note does not mention that the `claude-api` skill's cached price table differs from the live page — fix now.
- prior-review #1: the Scope paragraph's claim about what the rulebook assigns to Sonnet is a repo-state claim without an inline observed date — fix now.
- prior-review #2: the absence claims about uncommitted helpers and unrecorded output lack inline observed dates — fix now.
- prior-review #3: "lowest of the three groups" and "because of one format miss" are characterizations — fix now (the first with diff-bug #5; the second restated as the measured sensitivity).
- prior-review #4: the Review section must carry the per-finding list before archiving — reject, false as a defect: this pass logs every finding here.
- prior-review #5: the test pin comment says "in this session" with no date — fix now.
