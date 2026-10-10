<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M228: Compare Haiku 5.5 with Sonnet 5.5 on cairn's Sonnet roles

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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

- [ ] AC1: `cairn/references/haiku-sonnet-roles.md` exists with its
      `INDEX.md` line and a `**Provenance.**` block. Its run table holds 18
      rows: nine tasks, three per role group, each run once with the Agent
      tool's model set to Sonnet and once set to Haiku, from the same
      prompt. The edit-work tasks include a mechanical sweep and a
      test-writing task. The history-review tasks include a blame-history
      task and a prior-PR-comments task.
- [ ] AC2: Each row records the `model` id taken from every assistant
      record of its subagent transcript. Every id on a Sonnet row begins
      `claude-sonnet-5-5`, and every id on a Haiku row begins
      `claude-haiku-5-5`.
- [ ] AC3: Each row's dollar cost equals a sum over the distinct
      `message.id` values in its transcript: each token class count from
      that id's last record, times that model's price for the class. The
      classes are input, 5-minute cache write, 1-hour cache write, cache
      read, and output. The note cites the prices from Anthropic's
      published pricing by URL and access date.
- [ ] AC4: Each row's quality score follows from its group's scoring rule
      as the note states it, and each rule yields a score of zero or more.
      An answer key, built by a command that the note gives, scores search.
      A target diff or a mutant set that the note gives scores edit work. A
      model-blind Opus judge rates each history-review finding valid or
      invalid.
- [ ] AC5: The note gives each role group a verdict. The verdict is `move`
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
- AC4 → T1, T2, T3, T4, T5
- AC5 → T1, T6

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
- [ ] T3: Run the search group with the Explore agent type, `model` set to
      `sonnet` and then `haiku`, same prompt. After the first Haiku run,
      read its transcript's `model` id. If the id is not Haiku 5.5 (a
      2026-09-11 spawn ran as `claude-haiku-4-5-20251001`), stop and set
      M228 `blocked` with the id as the blocker. Record each run's
      transcript path (`~/.claude/projects/<slug>/<session>/subagents/`),
      its `model` ids, its token classes per `message.id`, and its score.
- [ ] T4: Run the edit-work group the same way. Give each spawn
      `isolation: "worktree"`, so that no run edits the shared checkout.
      Score each run's diff against its target or mutant set.
- [ ] T5: Run the history-review group the same way. Then spawn one Opus
      judge per task. The judge sees both runs' findings under shuffled A/B
      labels and rates each finding valid or invalid against the diff.
      Record the label mapping only after the judge returns.
- [ ] T6: Compute each row's cost from its token classes and the cited
      prices, sum the costs per group, and apply AC5's rule. Write the
      verdicts, the single-run limit, and a re-measurement procedure into
      the note. Add the `INDEX.md` line and run `scripts/cairn_validate.py`.

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
