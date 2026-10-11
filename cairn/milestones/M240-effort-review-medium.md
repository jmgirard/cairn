<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M240: Measure medium effort on the history reviewers, and state each spawned role's effort level

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the rulebook and review skill prose that every adopting repo's session follows when it spawns subagents
- **Branch/PR:** m240-effort-review-medium

## Goal

The rulebook states the reasoning-effort level each spawned role uses, backed by a committed measurement of `medium` effort on the history reviewers.

## Scope

**In:** Each history-review task of `cairn/references/haiku-sonnet-roles.md`
(H1 to H3, Sonnet, `general-purpose`) gets one `medium` run and one new
default run, with the Agent tool's `effort` unset in the default run. The runs
are in the foreground, so each Agent tool result carries its `usage`. One
blind Opus judge per task rates three reports: M239's default report, the new
default report, and the `medium` report. A new reference note records the
runs, the ratings, and a verdict by a rule fixed before any run. The
rulebook's model section then states the effort rule. If the verdict is
`medium`, the two history-review bullets of the review skill name it. A
D-entry records the rule.

**Out:** The user chose at this plan's question set not to adopt `low` for
search and edit work. M239 measured a 1.6% and a 10% saving on a few cents,
within the output undercount. The D-entry records it as a rejected
alternative. Effort for the Opus roles has no scored tasks. It stays in the
"Reasoning-effort dial per spawned agent" candidate row, which this
milestone's post-merge hygiene rewrites to that remainder. More than one new
run per arm goes to the note's re-measurement procedure.

## Acceptance criteria

- [ ] AC1: `cairn/references/effort-review-medium.md` exists with a
      `**Provenance.**` block and an `INDEX.md` line. For each of H1, H2,
      and H3, it records one `medium` run and one new default run. Each run
      shows its agent id, every `effort` and `message.model` value on its
      transcript's assistant records, and its token counts and USD by the
      cost method of `haiku-sonnet-roles.md` (Design, Cost). The note also
      records the judge's rating of every numbered finding in the three
      reports. Its run table also carries M239's H1 to H3 default rows, with
      the USD that `effort-roles.md` records. `cairn_validate` passes its
      references check.
- [ ] AC2: The note states one history-review verdict: `medium`, `default`,
      or `untested`. The commit that adds its Design section, with the rule
      below, is older than the first record of the first run transcript.
      There are three arms: M239 default, new default, and `medium`. An
      arm's score is the sum over H1 to H3 of the findings that this
      milestone's judges rate valid, and its cost is the sum of its three
      USD figures. The verdict is `untested` when a `medium` run's assistant
      records carry no `effort` value or any value other than `medium`, or
      when a new default run's records carry any value other than `high`.
      It is `medium` exactly when three conditions hold. The mean score of
      the two default arms is above zero. The `medium` arm's cost is below
      the two default arms' mean cost. Its score is at least 0.9 times their
      mean score. Otherwise it is `default`. A recomputation of the rule from
      the note's run and rating tables gives the stated verdict.
- [ ] AC3: The "Model and agent strategy" section of
      `skills/shared/tracking-rules.md` states one effort rule that covers
      every subagent role its bullets name. If AC2's verdict is `medium`, the
      blame-history and prior-PR-comments reviewers set the Agent tool's
      `effort` to `medium`. Otherwise they leave it unset. Every other role
      leaves it unset. The rule cites `effort-roles.md` and the new note.
      If the verdict is `medium`, the two reviewer bullets of
      `skills/milestone-review/SKILL.md` name `medium`. Otherwise
      `git diff <default-branch>..HEAD -- skills/milestone-review/SKILL.md`
      adds no line that contains `` `effort` `` or `effort:`.
- [ ] AC4: The `verify` slot of `cairn/PROFILE.md` passes. The hand-run
      `python3 -m unittest discover -s skills/tests` also passes.

## Coverage

- AC1 → T1, T2, T3, T4
- AC2 → T1, T3, T4
- AC3 → T5
- AC4 → T6

## Tasks

- [x] T1: Write the note's Design section and commit it before any run. It
      names the two arms and the pinned inputs. History-review runs read refs
      that predate `c023018`, as in M239. The cost method takes the final
      call's output from the foreground Agent tool result's `usage`. The M228
      judge prompt widens to three labeled reports. The section states AC2's
      verdict rule.
- [x] T2: Extract M239's H1 to H3 default reports into report files (agent
      ids `aa3398a8cbe013dcd`, `a19090c5879113da4`, `a358c3f0ff2386c3e`,
      under the M239 Provenance directory). Run H1 to H3 at
      `effort: "medium"` and with `effort` unset, with `model: "sonnet"` and
      the prompts of `haiku-sonnet-roles.md`. Read each run's `effort` and
      model values and its counts. The live tree holds `effort-roles.md`,
      which lists M239's findings, so check that no run or judge transcript
      names that file, as M239 did for `haiku-sonnet-roles.md`.
- [x] T3: Run one Opus judge per task over its three reports, with `effort`
      unset. Draw the labels with `random.SystemRandom` and write the mapping
      before the judge runs. Record every rating and compute the verdict.
- [x] T4: Finish the note: run table, rating table, verdict, limits, and
      re-measurement procedure. Add its `INDEX.md` line. Pin it in the
      shipped-page ledger of `scripts/tests/test_scripts.py` (`EXPECTED`,
      near the `effort-roles.md` entry).
- [x] T5: Write the effort rule into tracking-rules "Model and agent
      strategy". If the verdict is `medium`, also write it into the two
      reviewer bullets of `skills/milestone-review/SKILL.md` (near line
      275). Re-seed the rulebook mass baseline at its three sites:
      `skills/milestone/SKILL.md` near line 118,
      `skills/tests/test_cost_audit_line.py` near line 68, and the
      `skills/tests/test_mutation_harness.py` entry near line 118. Append a
      D-entry that records the rule. Its rejected alternatives are `low`
      for search and edit work and unmeasured levels for the Opus roles.
- [x] T6: Run the `verify` slot and the hand-run `skills/tests` suite from
      the repo root, and check each exit code.

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: question set: what to plan — the effort dial; the user asked whether `low` saves meaningful tokens on search and edit work, answered no (edit $0.003 over three tasks, search 1.6% within the undercount), and the re-asked choice was a `medium` test on history review only.
- 2026-10-10: question set: how far the dial goes — add a `medium` test first.
- 2026-10-10: collision check: absorbs the candidate row "Reasoning-effort dial per spawned agent" (M120 Out, measured M239), which stays until post-merge hygiene (records-hygiene §1). No D-entry sets effort levels (the DECISIONS hits for "effort" are D-099 and D-100's verification-effort audit). D-141, D-142, and D-151 are compatible. Inbox: 0 open issues, 0 open PRs. No checker-regress shape.
- 2026-10-10: lessons harvested: M149 (rulebook mass baseline at three sites) into T5, M56 and M148 (each suite from the root, `skills/tests` hand-run after skill edits) into T6.
- 2026-10-10: criteria audit (full mode, fresh Opus reader): 8 findings, AC4 clean. Fixed in place: AC2 arms and judging defined, `untested` widened to a missing effort value and to a new default run not at `high`, M239 default rows required in AC1, Design-before-runs made a commit-time check, AC3 narrowed to subagent roles, AC3's grep tightened to `` `effort` `` and `effort:`. Decided toward the narrower promise: the D-entry stays a task with no criterion. Moved to T2: the check that no transcript names `effort-roles.md`.
- 2026-10-10: plan gate chose comparing `medium` with the mean of two default arms (M239's and one new) over one `medium` run against M239's default alone, because M239 measured a run-to-run spread equal to its whole low-against-default gap; falsified by a rerun that flips this milestone's verdict.
- 2026-10-10: plan gate chose leaving search and edit work at default over `low` (user's choice), because the measured saving sits inside the output undercount; falsified by a measurement where `low` saves more than the undercount can reverse.
- 2026-10-10: implement started on branch `m240-effort-review-medium`. Untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-10: T1 done: the note's Design section committed before any run. New runs reuse the M239 default runs' first user records as prompts (extracted, verbatim). Each report is the run's `SubagentHandback` message, else its last assistant text.
- 2026-10-10: T2 done: six Sonnet runs (three `medium`, three effort unset), all foreground in one message. Every `medium` record says `medium` and every new default record says `high`. The only note-name hit is `effort-roles.md` as a path in a `gh api` comment listing in the H3 default run, which read no such file.
- 2026-10-10: T3 done: three Opus judges over shuffled labels, with the mapping read after they returned. Scores M239 default 3, new default 3, `medium` 2. Costs $0.8794, $0.9830, $0.6700. Verdict `default`: 2 is below 0.9 times the mean default score of 3.
- 2026-10-10: T4 done: note finished, page pinned `ok` in `TestShippedPageStateLedger`. The note's later sections were appended with a shell heredoc, not the Edit tool, so the app's edited-files card leaves that append out.
- 2026-10-10: T5 done: verdict `default`, so tracking-rules gains one "Leave effort unset on every spawn" bullet citing both notes, and `skills/milestone-review/SKILL.md` is unchanged. Rulebook mass re-seeded to 642 lines / 61,338 bytes (`wc -l -c`, this branch) at its three sites. D-157 appended.
- 2026-10-10: T6 done: verify green (scripts 406 tests OK, hooks 174 OK, plugin and marketplace validate exit 0, `claude plugin test` 0 fail), hand-run `skills/tests` 726 OK.
