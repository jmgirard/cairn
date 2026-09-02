# M170: Waiting on CI and background work follows a tested rule

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2, GP4
- **Resolves:** —
- **Branch/PR:** m170-wait-doctrine

## Goal

Replace the rulebook's untested "one blocking wait" rule with a wait rule derived from an experiment over the harness's actual wait mechanisms, so sessions stop leaving stale or runaway watchers behind.

## Scope

Surface tier: user-facing — the rule is rulebook prose every adopting repo's sessions run under.

**In:** a controlled experiment in a scratch private GitHub repo with a synthetic CI matrix, exercising the four wait mechanisms (foreground Bash with a timeout, Bash `run_in_background`, Monitor, `gh pr checks --watch`) on green, red, timeout, and no-checks cases; a synthesis note recording the observations; the rewritten wait rule in tracking-rules covering CI checks, long-running local commands, and background subagents, with a stop-point clause; the three skill sites restating the rule; a superseding D-entry; one hand-run prose pin.

**Out:** a `/loop` or scheduled-task doctrine — named in the rule only as not a CI wait; a validator or hook enforcing the rule (prose plus the pin, per the meta-work proportionality stance; promote only if a runaway watcher is observed after the rule ships — candidate row if that happens); the scratch repo's deletion is a post-merge hygiene step taken on user confirmation, never autonomous.

## Acceptance criteria

- [ ] AC1: `cairn/references/wait-mechanisms.md` exists as a synthesis note (Provenance block, using the first-hand-record re-verification exemption) recording, for each of the four mechanisms it names — foreground Bash with a timeout, Bash `run_in_background`, Monitor, and `gh pr checks --watch` — one dated observation each of: behaviour when CI finishes green, behaviour when CI finishes red, behaviour at the mechanism's own timeout, and whether the wait outlives the turn that started it; plus one dated observation of `gh pr checks` on a PR that reports no checks; each observation names the run or PR URL it was taken from, and a behaviour the harness documents but the experiment could not exercise (survival across `/clear`, which only the user can trigger) is recorded as documented-not-observed with the doc URL.
- [ ] AC2: tracking-rules' "Waiting on CI" paragraph is replaced by a wait rule that states, for CI checks, for a long-running local command, and for a background subagent, which mechanism a session uses, the one-watcher-per-wait rule, what a session does when the wait times out, what it does on a PR that reports no checks, and the stop-point rule (no watcher left armed at a commit, turn-end, or `/clear` point — the session stops it with TaskStop first); no clause states harness behaviour the AC1 note does not record, and the paragraph cites the note by path.
- [ ] AC3: every site the sweep `git grep -n -e '--watch' -e 'blocking wait' -e 'background poll' -- skills ':!skills/tests' README.md` returns states the AC2 rule's mechanism and stop-point clauses consistently with tracking-rules, and no site the sweep returns keeps the superseded "one blocking wait" wording — a spelling-level sweep by design; a site restating the rule in other words is outside this promise.

## Coverage

- AC1 → T1, T2, T3, T4, T5
- AC2 → T6
- AC3 → T6, T7

## Tasks

- [x] T1: Create the scratch private repo (`gh repo create <login>/cairn-wait-lab --private`) with one workflow: a matrix of jobs sleeping 60, 360, and 720 s (the last crosses the harness's 10-minute foreground cap) plus a job that fails when a `FAIL` file exists at the repo root; push, open a draft PR, record the repo and PR URLs in the work log.
- [x] T2: Green grid — on a green run, take one wait per mechanism (foreground Bash `timeout` at the 600 000 ms cap; `run_in_background`; Monitor at its default 300 000 ms timeout and once at 900 000 ms; `gh pr checks <pr> --watch --fail-fast` under each); record completion signal, exit code, whether the foreground call was auto-backgrounded at the cap, whether the wait outlived the turn, and what `/tasks`-style listing and TaskStop showed afterwards. One watcher at a time; stop each before starting the next.
- [x] T3: Red grid — commit the `FAIL` file, rerun T2's mechanisms on the red run; record `--fail-fast` exit codes and timing versus the full matrix.
- [ ] T4: No-checks case — a PR in this repo (which has no workflows) or a scratch branch with the workflow removed; record `gh pr checks` output and exit code. Record documented-not-observed behaviours (`/clear` survival, `--resume` non-restoration, `-p` mode teardown) with doc URLs.
- [ ] T5: Write `cairn/references/wait-mechanisms.md` from `skills/shared/templates/synthesis-note.md`; add its `INDEX.md` line; `cairn_validate` green.
- [ ] T6: Rewrite tracking-rules lines 242–245 as the AC2 rule; align `skills/cairn-release/SKILL.md:61`, `skills/hotfix/SKILL.md:107`, `skills/milestone-review/SKILL.md:322`; append D-128 superseding the one-blocking-wait rule (old rule, mechanism chosen, the observation class that would overturn it — a watcher outliving a stop point under the new rule).
- [ ] T7: Add `skills/tests/test_wait_rule.py` pinning the rule's trigger clause (what it applies to) and its stop-point clause with one mutation entry each, retired tokens spelled by concatenation (M169 lesson); hand-run `skills/tests`, run both gating suites.

## Work log

- 2026-09-02: created by /milestone-plan. Criteria audit ran in full mode ([O] fresh reader): six findings — five FIX applied (checker/INDEX clauses moved to T5; first-hand provenance exemption named; no-checks observation added to AC1; AC2 traceability narrowed to "no clause states harness behaviour the note does not record"; AC3 sweep scoped past `skills/tests`); one DECIDE (grep as spelling-level proxy) disposed by bounding AC3's promise to the sweep's returns.
- 2026-09-02: plan gate chose a scratch private repo with a synthetic matrix over a bsync live draft PR because only the synthetic matrix can force a red run and a job crossing the 10-minute foreground cap; falsified by a real-repo wait behaving differently from the synthetic one (bsync's 7–9 min matrix is the first place to look).
- 2026-09-02: plan gate chose one rule spanning CI, local commands, and subagents over a CI-only rewrite because the stale-watcher failure is the same across the three; falsified by a subagent or local-command wait that the CI-derived clauses misdescribe.
- 2026-09-02: plan gate chose a superseding D-entry over a prose-only repair because the replaced rule is operative and its reason is no longer in the rulebook; falsified by nothing — a record choice.
- 2026-09-02: plan gate kept the hand-run prose pin (repo convention) over no pin; falsified by the pin costing a return without catching a clause deletion.
- 2026-09-02: T1 done — scratch repo https://github.com/jmgirard/cairn-wait-lab (private), workflow `lab` (sleep-60/360/720 matrix + FAIL-file gate), draft PR https://github.com/jmgirard/cairn-wait-lab/pull/1; run 1 https://github.com/jmgirard/cairn-wait-lab/actions/runs/33635906501 started 13:28Z.
- 2026-09-02: T2 done — green grid over runs 33635906501/33637201059/33638502957: foreground Bash at the 600 s cap was moved to the background (not killed) and finished later with a notification; run_in_background ran 11m51s past its 600 000 ms timeout and finished; Monitor at 300 000 ms was killed at 5 min with a timeout event, at 900 000 ms saw the run finish; TaskStop on a finished task returns "No task found". No-checks PR #2 (workflow removed): `gh pr checks` and `--watch` both print "no checks reported" and exit 1 (PROFILE.md said 0). Ledger in scratch, note in T5.
- 2026-09-02: T3 done — red run 33639869206 (FAIL file): `--watch --fail-fast` exited 1 in 17 s from the push (gate fails in 6 s) under foreground and run_in_background alike, versus ≈12 min for the full matrix; a Monitor loop exiting on any fail bucket ended in ~15 s with a failed-script notification; TaskStop on a live background `--watch` and on a live Monitor both reported success and left no process. Plain `gh pr checks` exits 8 while pending, 1 with a failure.

## Decisions

## Review
