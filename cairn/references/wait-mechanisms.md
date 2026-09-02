# How the harness's wait mechanisms behave on CI (M170)

**Provenance.** Ingested 2026-09-02 by M170 from a controlled experiment in
the scratch private repo `jmgirard/cairn-wait-lab` (one workflow: a
`sleep-60` / `sleep-360` / `sleep-720` matrix plus a `gate` job that fails
when a `FAIL` file exists; draft PR #1 for the matrix, draft PR #2 with the
workflow removed), driven from a Claude Code session in this repo, plus a
same-day read of the Claude Code documentation pages cited below.
Pagination: —.
Extraction: first-hand record, nothing to re-verify against — observed 2026-09-02.

**Scope.** What each of four wait mechanisms did when a GitHub Actions run
finished green, finished red, hit the mechanism's own timeout, and whether
the wait outlived the turn that started it; plus what `gh pr checks` reports
on a PR with no checks. Not a source summary and not a rule — the rule this
feeds lives in tracking-rules ("Waiting on CI and background work"); this
page records what was seen so the rule can be checked against it. It builds
no validator or hook. This is a reference, not an authority — status lives
in `ROADMAP.md`, decisions in `DECISIONS.md`, architecture in `DESIGN.md`.

**Evidence snapshot.** All timestamps UTC, 2026-09-02.

- Green run 1 — https://github.com/jmgirard/cairn-wait-lab/actions/runs/33635906501 (PR #1, 13:28–13:40) — observed 2026-09-02.
- Green run 2 — https://github.com/jmgirard/cairn-wait-lab/actions/runs/33637201059 (PR #1, 13:41–13:53) — observed 2026-09-02.
- Green run 3 — https://github.com/jmgirard/cairn-wait-lab/actions/runs/33638502957 (PR #1, 13:53–14:05) — observed 2026-09-02.
- Red run 4 (`FAIL` committed) — https://github.com/jmgirard/cairn-wait-lab/actions/runs/33639869206 (PR #1, 14:06–14:18) — observed 2026-09-02.
- Green run 5 (`FAIL` removed) — https://github.com/jmgirard/cairn-wait-lab/actions/runs/33640124122 (PR #1, 14:08–14:20) — observed 2026-09-02.
- No-checks PR — https://github.com/jmgirard/cairn-wait-lab/pull/2 (branch `nochecks`, workflow file removed) — observed 2026-09-02.
- Harness: Claude Code desktop session, Bash timeout ceiling 600 000 ms, Monitor default 300 000 ms — observed 2026-09-02.

## What the four mechanisms are

Neutral description, before any observation:

- **Foreground Bash with a timeout** — a Bash tool call with `timeout` up to
  the 600 000 ms ceiling; the call returns when the command exits or the
  timeout elapses.
- **Bash `run_in_background`** — the same tool with `run_in_background:
  true`; the call returns a task id at once, output goes to a file, and a
  `<task-notification>` arrives when the command exits.
- **Monitor** — a tool that runs a script whose stdout lines become
  notifications; it has its own `timeout_ms` (default 300 000, max
  3 600 000) or `persistent: true`.
- **`gh pr checks <pr> --watch`** — the GitHub CLI's own poll loop, refreshing
  every 10 s until every check leaves `pending`; `--fail-fast` exits at the
  first failure. It is a command, so it runs *under* one of the three above.

`TaskStop <id>` ends a background Bash task or a Monitor.

## Observation ledger

Tags: `observed` (seen in this experiment, run or PR URL in the row) ·
`documented` (stated by a cited doc or issue, not exercised here).

| # | Mechanism | Case | What happened | Tag |
|---|---|---|---|---|
| W1 | Foreground Bash, timeout 600 000 ms | green | Run 1: the 720 s job outlasts the ceiling. At 600 s the harness replied "Command did not complete within its 600s timeout and was moved to the background (ID: b6igjkr8f)"; the `--watch` kept running, printed the all-pass table and exited 0 at 13:40:25, and a completion notification arrived — the green result reached the session through the auto-backgrounded continuation, not the foreground call. Run 5 (7 min left when the wait began, so it fits the ceiling): a foreground `gh pr checks 1 --watch --fail-fast` started 14:13:25, printed the all-pass table and exited 0 at 14:20:41 — a green result seen inside the foreground call, nothing backgrounded. | observed |
| W2 | Foreground Bash | red | Run 4: `gh pr checks 1 --watch --fail-fast` started 14:06:21, exited 1 at 14:06:22 — 17 s after the push (`gate` failed in 6 s) while three sleep jobs were still pending, versus ≈12 min for the full matrix. | observed |
| W3 | Foreground Bash | own timeout | Run 1: at the 600 000 ms ceiling the command was **moved to the background, not killed** (W1's quoted reply); the docs state the three exceptions that are stopped instead — a command starting with `sleep`, one containing `git` anywhere, or a compound command the harness cannot parse (tools-reference, cited below). | observed; exceptions documented |
| W4 | Foreground Bash | outlives the turn | Yes, once auto-backgrounded: the process ran on after the tool call returned and delivered its result later (run 1). A call that finishes inside its timeout leaves nothing behind. | observed |
| W5 | Bash `run_in_background`, timeout 600 000 ms | green | Run 2: the call returned "Command running in background with ID: b6o6e1wkp" immediately; the `--watch` printed the pass table, the task exited 0 at 13:52:58, a `<task-notification>` (completed, exit 0) arrived, and `TaskOutput(block=true)` returned the same output. | observed |
| W6 | Bash `run_in_background` | red | Run 4: `--watch --fail-fast` on the red run exited 1 within 1 s; the task's notification arrived. | observed |
| W7 | Bash `run_in_background` | own timeout | Run 2: the wait ran 13:41:07 → 13:52:58, 11 min 51 s, past the 600 000 ms `timeout` passed on the call — **the timeout did not end a background task**; only completion or `TaskStop` does. | observed |
| W8 | Bash `run_in_background` | outlives the turn | Yes: the process ran across every later tool call until it exited (runs 2, 4) or was stopped (W16). Docs: commands started by the main conversation "keep running" past the turn; a foreground subagent's commands end with that subagent. | observed |
| W9 | Monitor, 900 000 ms | green | Run 3: a poll loop over `gh pr checks 1 --json name,bucket` emitting each non-pending check once — events "gate: pass", "sleep-60: pass", "sleep-360: pass", "sleep-720: pass", "run complete 14:05:33" arrived as `<task-notification>` blocks (lines within 200 ms batched); the script exited 0 and a final "stream ended" notification followed. | observed |
| W10 | Monitor, 300 000 ms | red | Run 4: the loop, written to `exit 1` on any `fail` bucket, emitted "gate: fail" / "run red 14:06:48" ~15 s after arming; notification "script failed (exit 1)". | observed |
| W11 | Monitor, 300 000 ms (default) | own timeout | Run 3: at 300 s the harness killed the monitor — `TaskOutput` status `killed`, output ending "[killed]" — and delivered one event "[Monitor timed out — re-arm if needed.]"; the run had ≈7 min left. The default timeout is shorter than this matrix, so a default Monitor cannot see it finish. | observed |
| W12 | Monitor | outlives the turn | Yes: armed at 13:59:06, it ran across later tool calls and ended only at its own exit (W9), its timeout (W11), or `TaskStop` (W17). Docs: "Stop a monitor by asking Claude to cancel it or by ending the session." | observed |
| W13 | `gh pr checks --watch` | green | Runs 1–3: exits 0 once every check passes; refreshes every 10 s and reprints the whole table each time, so a 12-minute wait's output is ≈60 KB — read it with `tail`, never whole. | observed |
| W14 | `gh pr checks --watch` | red | Run 4: with `--fail-fast`, exit 1 at the first failed check (17 s); without it, keeps watching the pending jobs (W16 was stopped, not observed to completion). Plain `gh pr checks` (no `--watch`): exit 8 while any check is pending (run 1), exit 1 once one has failed (run 4). | observed |
| W15 | `gh pr checks --watch` | own timeout / outlives | `gh` has no timeout of its own — it polls until the checks settle (12 min on runs 1–3). Whether it outlives the turn is decided by the wrapper it runs under (W4, W8). | observed |
| W16 | `TaskStop` on a live background Bash | stop | Run 4: a full-matrix `gh pr checks 1 --watch` started as bgh51qznw at 14:07:00; `TaskStop` at 14:07:09 replied "Successfully stopped task"; afterwards `pgrep -fl 'gh pr checks'` found no process, the output file ends "[killed]", and no completion notification followed. | observed |
| W17 | `TaskStop` on a live Monitor | stop | An unbounded `while true` tick loop (b3ih5fjlf) emitted one tick; `TaskStop` replied "Successfully stopped task"; no later tick arrived and no process survived. | observed |
| W18 | `TaskStop` on a finished or timed-out task | stop | Both replied "No task found with ID" — a task that has exited or been killed is already gone. | observed |
| W19 | `gh pr checks` on a PR with no checks | no checks | PR #2 (workflow removed): `gh pr checks 2` and `gh pr checks 2 --watch` both print "no checks reported on the 'nochecks' branch" to stderr and **exit 1** at once — the watch form does not wait for checks that will not arrive. Re-checked 26 min after the PR opened: unchanged, no run ever registered for the branch. | observed |
| W20 | any background task | `/clear` | Only the user can `/clear`, so not exercised. Docs (interactive-mode) say `/clear` "starts a new session" and that background tasks "are automatically cleaned up when Claude Code exits" — nothing states that `/clear` stops them; issue #44357 (2026-04-06, v2.1.92, closed stale) reports two background tasks still active after `/clear`, ended only by `/exit`. Treat a watcher as surviving `/clear` until a doc says otherwise. | documented |
| W21 | any background task | `-p` (print) mode | Docs (headless): a background Bash shell "is terminated about five seconds after Claude has returned its final result and stdin has closed"; background subagents are waited for, capped at ten minutes idle from v2.1.182. | documented |
| W22 | any background task | `--resume` / session exit | Docs (interactive-mode): cleaned up when Claude Code exits; handed to a background session if the session is backgrounded rather than exited. Issue #25188 (2026-02-12, closed duplicate) reports tracked background tasks SIGTERM'd on exit and on context compaction; compaction teardown is not on the doc pages. Nothing documents a watcher being restored on `--resume`. | documented |
| W23 | background subagent | completion | Docs (sub-agents): "A background subagent's results reach Claude as a completion notification in a later turn"; it can leave a background Bash command running past its own end and is notified when that command ends; a finished subagent stays in `/tasks` marked done for ~30 s. | documented |

Documentation read 2026-09-02:
https://code.claude.com/docs/en/tools-reference ·
https://code.claude.com/docs/en/interactive-mode#background-bash-commands ·
https://code.claude.com/docs/en/headless#background-tasks-at-exit ·
https://code.claude.com/docs/en/sub-agents#run-subagents-in-foreground-or-background ·
https://github.com/anthropics/claude-code/issues/44357 ·
https://github.com/anthropics/claude-code/issues/25188.

## What the ledger implies for a wait rule

Stated here as findings, not as the rule (the rule is tracking-rules' and
cites this page):

- A foreground Bash wait is only "one blocking wait, resolved within the
  turn" when the command finishes inside its timeout; at the ceiling it
  silently becomes a background task (W3) — the very stale watcher the old
  rule tried to avoid. A foreground wait therefore needs a bound the caller
  chooses (`--fail-fast`, a `timeout` below the ceiling) and a plan for the
  cap.
- `run_in_background` ignores its `timeout` (W7); a Monitor honours its
  `timeout_ms` and reports the kill as an event (W11). Both deliver a
  completion notification (W5, W9) and both die cleanly under `TaskStop`
  (W16, W17). Neither is bounded by a stop point unless the session stops it.
- On a red run, `--fail-fast` turns a 12-minute wait into a 17-second one
  (W2, W6, W14) — the right default for a merge gate.
- A no-checks PR exits 1 at once (W19); the status "no checks reported" is
  readable on stderr, and a rule cannot key on exit 0 for that case.
- Beyond the session's control: a watcher is documented to survive `/clear`
  (W20) and to be torn down at `-p` exit (W21); nothing restores it on
  `--resume` (W22).

## Disposition

- W1–W19 → the wait rule in tracking-rules ("Waiting on CI and background
  work"), the three skill sites restating it, and D-128 (M170).
- W19 → `cairn/PROFILE.md` consistency-gate slot corrected in M170 (it said
  exit 0).
- W20 → the rule's stop-point clause (`/clear` not documented to stop a
  watcher); W23 → its background-subagent clause; W21–W22 (`-p` teardown,
  `--resume`) → recorded here only, cited by no clause. Re-open if a doc
  page states `/clear` teardown.
- Pin: `skills/tests/test_wait_rule.py` (hand-run) holds the rule's trigger
  and stop-point clauses.

## Open questions

- Whether a background wait survives context compaction is asserted only by
  issue #25188; not documented, not exercised — observed 2026-09-02.
- Whether a real-repo matrix (bsync's 7–9 min) behaves like the synthetic one
  is the plan gate's stated falsifier; unexercised — observed 2026-09-02.
