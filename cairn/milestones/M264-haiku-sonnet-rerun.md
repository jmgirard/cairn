# M264: Re-test Haiku 5.5 against Sonnet 5.5 on search and history review, three runs each

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** internal — a measurement note under `cairn/references/` that changes no shipped behavior
- **Branch/PR:** m264-haiku-sonnet-rerun, https://github.com/jmgirard/cairn/pull/276

## Goal

A committed note gives the search and history-review role groups a Haiku-or-Sonnet verdict from three runs per task and model, in place of M228's single runs.

## Scope

**In:** a new note `cairn/references/haiku-sonnet-rerun.md` that replays tasks
S1 to S3 (search) and H1 to H3 (history review) of
`cairn/references/haiku-sonnet-roles.md` three times on Sonnet 5.5 and three
times on Haiku 5.5, judges the history runs, prices every run, and states a
verdict per group. The note's INDEX line, its shipped-page ledger pin, and a
pointer from the old note's re-measurement section.

**Out:**
- The edit-work group: D-151 moved it to Haiku, and its falsifier (a defect
  traced to a Haiku edit diff) stands. Not re-tested here.
- Changing which model a role uses: if a verdict is `move`, the rule change
  is a later milestone the user chooses after reading the note. The candidate
  row "Haiku for the remaining Sonnet roles" holds it until post-merge
  hygiene narrows or removes that row (records-hygiene §1).
- Reasoning-effort levels: D-157 leaves `effort` unset, and so do these runs.
- Real conflicts a reviewer missed (D-016's "silently drop a real bug"): the
  judged score counts reported findings only. The note states this limit, as
  M228's did.

## Acceptance criteria

- [x] AC1: `cairn/references/haiku-sonnet-rerun.md` holds one run table in which each of the 12 task-model pairs (tasks S1, S2, S3, H1, H2, H3 of `cairn/references/haiku-sonnet-roles.md`, models Sonnet 5.5 and Haiku 5.5) has exactly three rows, and every row gives the run's agent id, the model ids on its subagent transcript, its cost in USD, and its score.
- [x] AC2: The note states one verdict, `move` or `stay`, for the search group and one for the history-review group, and each verdict equals what the verdict rule stated in the note's design section gives when applied to the note's own run table.
- [x] AC3: The `verify` slot of `cairn/PROFILE.md` passes and `python3 scripts/cairn_validate.py` reports no FAIL on the merge head.

## Coverage

- AC1 → T2, T3
- AC2 → T1, T4
- AC3 → T4

## Tasks

- [x] T1: Write the note's Provenance block and design section, and checkpoint-commit it before any run. Design: the six task prompts, keys, judge prompt, and cost method of `haiku-sonnet-roles.md`, reused verbatim; search runs on the `Explore` type in a `git archive c023018` copy, the prompt's repo path replaced by the copy's path; history runs on `general-purpose`, ref-based git on this repo; Agent `model` `sonnet` or `haiku`, `effort` unset; one Opus judge per history task and run index r, given Sonnet run r and Haiku run r under labels drawn at random and recorded before the judge runs. Verdict rule: per group and model, take each task's mean score and mean cost over its three runs and sum over the group's three tasks; `move` exactly when Sonnet's sum of scores is above zero, Haiku's cost is below Sonnet's, and Haiku's score is at least 0.9 times Sonnet's; otherwise `stay`.
- [x] T2: Run the 18 search spawns, score each against the S1 to S3 keys, read its counts from its subagent transcript and its final-call output from its tool result or completion notification, and add its rows to the run table.
- [x] T3: Run the 18 history-review spawns and the 9 judges; add each run's row and a per-finding rating table, and read the label mappings only after all judges return.
- [x] T4: Compute the verdicts by the T1 rule. Add readings: each task's score range over its runs, an S2 reading that ignores a missing `.py` (stated as outside the verdict), and the cost break-even the undercount allows. Add the INDEX line, the `EXPECTED` entry and comment in `scripts/tests/test_scripts.py`'s shipped-page ledger, and one pointer line in `haiku-sonnet-roles.md`'s "Limits and re-measurement". Run `verify` and `cairn_validate.py`.

## Work log

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: not run — work named at the question set.
- 2026-10-16: question set: what to work on — the Haiku re-test (candidate "Haiku for the remaining Sonnet roles"); runs per task and model — three.
- 2026-10-16: collision check: absorbs the candidate "Haiku for the remaining Sonnet roles"; M228 (done) measured one run each and M229 (done, D-151) moved edit work only; D-016, D-151, D-157, D-158 read whole, none blocks a re-measurement; no open issues or PRs on jmgirard/cairn.
- 2026-10-16: criteria audit (reduced mode, internal tier, fresh Opus reader): 0 findings on AC1 to AC3.
- 2026-10-16: no CHANGELOG entry: the milestone changes no user-visible behavior (profile consistency-gate).
- 2026-10-16: plan gate chose fresh Sonnet runs over reusing the three Sonnet history runs already on record (M228, M239 default, M240 new default) because those were judged in three sessions under different pairings; falsified by a judging that rates the reused runs' findings as their original judges did.
- 2026-10-16: plan gate chose M228's prompts and scoring verbatim over a clarified S2 prompt because the old note's re-measurement procedure keeps them, so the rerun stays comparable; falsified by Haiku dropping `.py` on S2 in all three runs while matching Sonnet elsewhere, which would show the prompt and not the model decides the group.
- 2026-10-16: plan gate chose a new note over appending to `haiku-sonnet-roles.md` (462 lines) because a rerun with its own runs and verdicts is a separate measurement; falsified by a reader needing both notes open to apply either verdict.
- 2026-10-16: implement started on `m264-haiku-sonnet-rerun`; untracked `cairn-probe.log` and `tsconfig.json` at the root are not this milestone's and stay unstaged.
- 2026-10-16: T1 done: design section committed before any task run; spawns run in the foreground because this session's Agent tool result carries `usage` (checked on the audit reader), so M228's "Final match" applies; the INDEX line and ledger pin moved forward from T4 (minor amendment) so `verify` passes at this checkpoint; verify green, validate green.
- 2026-10-16: the simple-english hook flags the note's Pagination and Extraction lines (em dash, semicolon, long sentence); they keep the references template's shape, which `cairn_validate` reads, so they stay.
- 2026-10-16: T2 done: 18 search runs (Explore, foreground), all final-match `yes`, rows added to the note; scored by a session-local helper that rebuilds M228's S1 to S3 keys at `c023018` (10, 9, 88 items, as M228 recorded). All three Haiku S2 runs listed every registration but dropped `.py` and score 0, which fires the plan's falsifier on the verbatim-prompt choice; the note reports this as a reading, outside the verdict.
- 2026-10-16: T3 done: 18 history runs and 9 Opus judges (foreground), all final-match `yes`; labels drawn with `random.SystemRandom` into a mapping file outside the judges' directories, read after all nine returned; a first contamination grep hit every transcript on the branch name `m264-haiku-sonnet-rerun` in injected context, so the check was narrowed to tool calls and tool results, which show no read of the mapping or the earlier notes.
- 2026-10-16: T4 done: verdicts search `stay` (Haiku 1.9962 against Sonnet 2.8865, ratio 0.6916) and history review `move` (4.0000 against 4.3333, ratio 0.9231, one-finding margin; Haiku 0.3092 USD against 0.9762); a script reading the note's own run table recomputes both; INDEX line and the pointer in `haiku-sonnet-roles.md` added; the simple-english hook's hits on INDEX.md and `haiku-sonnet-roles.md` are their existing text, left as is.
- 2026-10-16: claim audit: not owed — internal tier.

## Decisions

## Review

Pass 1, 2026-10-16. PR #276 opened at review start (Copilot round on); Copilot requested on state `none`.

- AC1: a script reading the note's `## Runs` table finds 36 rows, 12 task-model pairs with exactly 3 rows each, 36 distinct agent ids, and 0 rows missing an agent id, a `claude-` model id, a four-place USD figure, or a score; two sampled ids resolve to transcript files in the Provenance directory. Pass.
- AC2: the same script applies the design section's verdict rule (per-task means over three runs, summed per group; `move` when Sonnet's score is above zero, Haiku's cost below Sonnet's, and Haiku's score at least 0.9 times Sonnet's) to the run table: search `stay` (1.9962 against 2.8865), history review `move` (4.0000 against 4.3333, cost 0.3092 against 0.9762); both equal the verdicts the note's Verdicts table states. Pass.
- AC3: from the repo root, each exit code read: `scripts/tests` and `hooks/tests` unittest suites 0, `claude plugin validate` on `plugin.json` and `marketplace.json` 0, `claude plugin test .` 0, `cairn_validate.py` 0 ("all checks passed"), on head after `M264: record PR #276`. Pass.
- Consistency gate: `cairn_validate.py` green; no principle changed, so `cairn_impact --changed` skipped; verify green (AC3); marketplace validate prints no `version` warning; no CHANGELOG entry owed, as the diff changes no user-visible behavior (diffstat: 6 files, +241 −7, all under `cairn/` except the four-line ledger pin in `scripts/tests/test_scripts.py`).
- spawned: diff-bug, blame-history, prior-review (full fan-out: the diff touches `scripts/tests/test_scripts.py`).
- diff-bug #1: S3 search note says the other S3 runs miss pairs only from D-085, but Sonnet run 1 misses `D-116 D-108` — fix now.
- diff-bug #2: T4's per-task score ranges are not stated — fix now (range columns in the per-task table).
- diff-bug #3: the Extraction line's "that day's session store" follows 2026-10-09 and so misdates the runs — fix now.
- diff-bug #4: T3's per-finding table is only V/I strings with no finding text — fix now (64-row per-finding table; descriptions by a Haiku subagent from the reviewer reports, rows diffed equal to the checked file, ratings from the judges).
- diff-bug #5: AC1 to AC3 unticked on the branch at status `review` — reject, false: each box is ticked in this pass against its evidence line above.
- diff-bug #6: "All six runs use the same prompt" reads as one prompt for six tasks — fix now.
- blame-history #1: the note does not say the S2 gap can come from the prompt, and the pointer in `haiku-sonnet-roles.md` carries no S2 caveat — fix now.
- blame-history #2: T3 per-finding table and T4 ranges missing — fix now (same fixes as diff-bug #2 and #4).
- blame-history #3: the candidate row "Haiku for the remaining Sonnet roles" still reads as before the rerun — reject, planned change: Scope Out leaves the row to post-merge hygiene.
- blame-history #4: the note states the contamination check without its narrowing to tool calls and results — fix now.
- prior-review #1: Limits drops M228's judge-disagreement caveat (11 of 22), which exceeds the one-finding margin — fix now.
- prior-review #2: the verdict table lacks the "What could flip it" column the sibling notes carry — fix now ("What flips it").
- prior-review #3: "S2 is the whole gap" is loose, as Haiku leads on S3 — fix now (note and INDEX line).
- prior-review #4: per-finding table missing — fix now (same fix as diff-bug #4).
- prior-review #5: the break-even is not compared with recorded output; Haiku history final calls record 2,078 to 5,780 tokens — fix now.
- prior-review #6: the INDEX line's "32% of the cost" lacks the undercount caveat — fix now.
- prior-review #7: contamination narrowing absent from the note — fix now (same fix as blame-history #4).
- prior-review #8: two repo-state claims in Scope carry no observed date — fix now.
- After the fixes: AC1 and AC2 checks re-run on the edited note (36 rows, 12 pairs of 3; both verdicts recompute and match); verify green. No finding demonstrates a criterion failing, so no return.
