# M170: Waiting on CI and background work follows a tested rule

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2, GP4
- **Resolves:** —
- **Branch/PR:** m170-wait-doctrine · https://github.com/jmgirard/cairn/pull/173

## Goal

Replace the rulebook's untested "one blocking wait" rule with a wait rule derived from an experiment over the harness's actual wait mechanisms, so sessions stop leaving stale or runaway watchers behind.

## Scope

Surface tier: user-facing — the rule is rulebook prose every adopting repo's sessions run under.

**In:** a controlled experiment in a scratch private GitHub repo with a synthetic CI matrix, exercising the four wait mechanisms (foreground Bash with a timeout, Bash `run_in_background`, Monitor, `gh pr checks --watch`) on green, red, timeout, and no-checks cases; a synthesis note recording the observations; the rewritten wait rule in tracking-rules covering CI checks, long-running local commands, and background subagents, with a stop-point clause; the three skill sites restating the rule; a superseding D-entry; one hand-run prose pin.

**Out:** a `/loop` or scheduled-task doctrine — named in the rule only as not a CI wait; a validator or hook enforcing the rule (prose plus the pin, per the meta-work proportionality stance; promote only if a runaway watcher is observed after the rule ships — candidate row if that happens); the scratch repo's deletion is a post-merge hygiene step taken on user confirmation, never autonomous.

## Acceptance criteria

- [x] AC1: `cairn/references/wait-mechanisms.md` exists as a synthesis note (Provenance block, using the first-hand-record re-verification exemption) recording, for each of the four mechanisms it names — foreground Bash with a timeout, Bash `run_in_background`, Monitor, and `gh pr checks --watch` — one dated observation each of: behaviour when CI finishes green, behaviour when CI finishes red, behaviour at the mechanism's own timeout, and whether the wait outlives the turn that started it; plus one dated observation of `gh pr checks` on a PR that reports no checks; each observation names the run or PR URL it was taken from, and a behaviour the harness documents but the experiment could not exercise (survival across `/clear`, which only the user can trigger) is recorded as documented-not-observed with the doc URL.
- [x] AC2: tracking-rules' "Waiting on CI" paragraph is replaced by a wait rule that states, for CI checks, for a long-running local command, and for a background subagent, which mechanism a session uses, the one-watcher-per-wait rule, what a session does when the wait times out, what it does on a PR that reports no checks, and the stop-point rule (no watcher left armed at a commit, turn-end, or `/clear` point — the session stops it with TaskStop first); no clause states harness behaviour the AC1 note does not record, and the paragraph cites the note by path.
- [x] AC3: every site the sweep `git grep -n -e '--watch' -e 'blocking wait' -e 'background poll' -- skills ':!skills/tests' README.md` returns states the AC2 rule's mechanism and stop-point clauses consistently with tracking-rules, and no site the sweep returns keeps the superseded "one blocking wait" wording — a spelling-level sweep by design; a site restating the rule in other words is outside this promise.

## Coverage

- AC1 → T1, T2, T3, T4, T5
- AC2 → T6
- AC3 → T6, T7

## Tasks

- [x] T1: Create the scratch private repo (`gh repo create <login>/cairn-wait-lab --private`) with one workflow: a matrix of jobs sleeping 60, 360, and 720 s (the last crosses the harness's 10-minute foreground cap) plus a job that fails when a `FAIL` file exists at the repo root; push, open a draft PR, record the repo and PR URLs in the work log.
- [x] T2: Green grid — on a green run, take one wait per mechanism (foreground Bash `timeout` at the 600 000 ms cap; `run_in_background`; Monitor at its default 300 000 ms timeout and once at 900 000 ms; `gh pr checks <pr> --watch --fail-fast` under each); record completion signal, exit code, whether the foreground call was auto-backgrounded at the cap, whether the wait outlived the turn, and what `/tasks`-style listing and TaskStop showed afterwards. One watcher at a time; stop each before starting the next.
- [x] T3: Red grid — commit the `FAIL` file, rerun T2's mechanisms on the red run; record `--fail-fast` exit codes and timing versus the full matrix.
- [x] T4: No-checks case — a PR in this repo (which has no workflows) or a scratch branch with the workflow removed; record `gh pr checks` output and exit code. Record documented-not-observed behaviours (`/clear` survival, `--resume` non-restoration, `-p` mode teardown) with doc URLs.
- [x] T5: Write `cairn/references/wait-mechanisms.md` from `skills/shared/templates/synthesis-note.md`; add its `INDEX.md` line; `cairn_validate` green.
- [x] T6: Rewrite tracking-rules lines 242–245 as the AC2 rule; align `skills/cairn-release/SKILL.md:61`, `skills/hotfix/SKILL.md:107`, `skills/milestone-review/SKILL.md:322`; append D-128 superseding the one-blocking-wait rule (old rule, mechanism chosen, the observation class that would overturn it — a watcher outliving a stop point under the new rule).
- [x] T7: Add `skills/tests/test_wait_rule.py` pinning the rule's trigger clause (what it applies to) and its stop-point clause with one mutation entry each, retired tokens spelled by concatenation (M169 lesson); hand-run `skills/tests`, run both gating suites.

## Work log

- 2026-09-02: created by /milestone-plan. Criteria audit ran in full mode ([O] fresh reader): six findings — five FIX applied (checker/INDEX clauses moved to T5; first-hand provenance exemption named; no-checks observation added to AC1; AC2 traceability narrowed to "no clause states harness behaviour the note does not record"; AC3 sweep scoped past `skills/tests`); one DECIDE (grep as spelling-level proxy) disposed by bounding AC3's promise to the sweep's returns.
- 2026-09-02: plan gate chose a scratch private repo with a synthetic matrix over a bsync live draft PR because only the synthetic matrix can force a red run and a job crossing the 10-minute foreground cap; falsified by a real-repo wait behaving differently from the synthetic one (bsync's 7–9 min matrix is the first place to look).
- 2026-09-02: plan gate chose one rule spanning CI, local commands, and subagents over a CI-only rewrite because the stale-watcher failure is the same across the three; falsified by a subagent or local-command wait that the CI-derived clauses misdescribe.
- 2026-09-02: plan gate chose a superseding D-entry over a prose-only repair because the replaced rule is operative and its reason is no longer in the rulebook; falsified by nothing — a record choice.
- 2026-09-02: plan gate kept the hand-run prose pin (repo convention) over no pin; falsified by the pin costing a return without catching a clause deletion.
- 2026-09-02: T1 done — scratch repo https://github.com/jmgirard/cairn-wait-lab (private), workflow `lab` (sleep-60/360/720 matrix + FAIL-file gate), draft PR https://github.com/jmgirard/cairn-wait-lab/pull/1; run 1 https://github.com/jmgirard/cairn-wait-lab/actions/runs/33635906501 started 13:28Z.
- 2026-09-02: T2 done — green grid over runs 33635906501/33637201059/33638502957: foreground Bash at the 600 s cap was moved to the background (not killed) and finished later with a notification; run_in_background ran 11m51s past its 600 000 ms timeout and finished; Monitor at 300 000 ms was killed at 5 min with a timeout event, at 900 000 ms saw the run finish; TaskStop on a finished task returns "No task found". No-checks PR #2 (workflow removed): `gh pr checks` and `--watch` both print "no checks reported" and exit 1 (PROFILE.md said 0). Ledger in scratch, note in T5.
- 2026-09-02: T3 done — red run 33639869206 (FAIL file): `--watch --fail-fast` exited 1 in 17 s from the push (gate fails in 6 s) under foreground and run_in_background alike, versus ≈12 min for the full matrix; a Monitor loop exiting on any fail bucket ended in ~15 s with a failed-script notification; TaskStop on a live background `--watch` and on a live Monitor both reported success and left no process. Plain `gh pr checks` exits 8 while pending, 1 with a failure.
- 2026-09-02: T4 done — no-checks PR https://github.com/jmgirard/cairn-wait-lab/pull/2 (branch with the workflow removed): `gh pr checks` and `--watch` both print "no checks reported on the 'nochecks' branch" and exit 1 without waiting. Documented-not-observed items gathered with URLs (tools-reference, interactive-mode, headless, sub-agents pages; issues #44357 and #25188): `/clear` survival, `-p` teardown at five seconds after the final result, subagent completion as a later-turn notification.
- 2026-09-02: T5 done — `cairn/references/wait-mechanisms.md` (W1–W23, Provenance first-hand exemption, doc URLs for the documented-not-observed rows), INDEX line, page pinned `exempt` in `scripts/tests/test_scripts.py`'s shipped-page ledger; green run 5 (33640124122) added a foreground wait that finished inside its timeout (7m16s, exit 0). `cairn_validate` green.
- 2026-09-02: T6 done — tracking-rules "Waiting on CI and background work" replaces the one-blocking-wait paragraph (cites the note by path); `skills/cairn-release/SKILL.md`, `skills/hotfix/SKILL.md`, `skills/milestone-review/SKILL.md` restate mechanism + stop-point; D-128 appended; minor: `cairn/PROFILE.md` consistency-gate corrected from "exits 0" to "exits 1" on the no-checks observation (W19).
- 2026-09-02: T7 done — `skills/tests/test_wait_rule.py` pins the trigger and stop-point clauses (two harness registrations) and checks the retired spelling by concatenation; hand-run skills/tests 583 OK; scripts and hooks suites exit 0.

## Decisions

## Review

- 2026-09-02: draft PR https://github.com/jmgirard/cairn/pull/173; main at 9f7f2e2 unchanged since the branch was cut (no merge needed). Suites re-run at review: `scripts/tests` 329 OK, `hooks/tests` 121 OK (both exit 0); hand-run `skills/tests` 583 OK.
- AC1 evidence: `cairn/references/wait-mechanisms.md` present with a Provenance block naming the first-hand-record exemption; ledger rows W1–W4 (foreground Bash), W5–W8 (`run_in_background`), W9–W12 (Monitor), W13–W15 (`--watch`; W15 carries own-timeout and outlives-turn together) cover green / red / own timeout / outlives the turn for each mechanism; W19 is the no-checks observation (PR #2, exit 1); W20 records `/clear` survival as `documented` with the interactive-mode doc URL and issue #44357; every observed row names its run number, resolved to a run or PR URL in the Evidence snapshot; all dated 2026-09-02. Verified.
- AC2 evidence: tracking-rules "Waiting on CI and background work" (lines 242–255) replaces the old paragraph; `git grep -i 'one blocking wait'` over skills (tests excluded) and README returns nothing. The paragraph states the mechanism for CI checks, a long-running local command, and a background subagent; one watcher per wait; the on-timeout action; the no-checks case; and the stop-point clause with `TaskStop`. Each behaviour claim traces to the note: ceiling→background W3, background `timeout` not ending the task W7, Monitor killed and reported W11, subagent notification W23, no-checks exit 1 W19, `/clear` survival W20, `TaskStop` W16–W17; the note is cited by path in the paragraph's first line. Verified.
- AC3 evidence: the sweep returns four sites — `skills/hotfix/SKILL.md:107`, `skills/milestone-review/SKILL.md:322`, `skills/shared/tracking-rules.md:244` and `:252`; each names the foreground `--watch --fail-fast` call with a timeout below the ceiling and the `TaskStop`-before-stop-point clause; none carries the superseded wording. (`skills/cairn-release/SKILL.md:61` restates the rule without the sweep tokens and is outside the promise; read anyway, consistent.) Verified.
- Consistency gate: `cairn_validate` all checks passed (exit 0; coverage complete PASS, release window advisory not fired); `DESIGN.md` untouched, so `cairn_impact --changed` skipped; generic profile's consistency-gate slot names no toolchain checks — no-op.
- Driving RR: — (no projection-vs-outcome pairs).
- Fresh-context review: three-lens fan-out (user-facing tier; diff touches `scripts/tests` and `skills/tests`).
- Reviewer findings and triage (three lenses; [S] blame-history: none, [S] prior-review: none — PR-comments probe found no threads; [O] diff-bug: 14, ranked as reported):
  - F1 (tracking-rules stop-point premise "ends only at completion or `TaskStop`" contradicts W11 and the paragraph's own Monitor clause): confirmed; **demonstrates AC2 failing** (a clause stating behaviour the note contradicts) — floor-qualifying; fixed at the gate (clause now names the Monitor's own `timeout_ms`), disposition put to the user at the merge chip.
  - F2 ("documented to survive `/clear`" overstates W20): confirmed; fix-now — now "no doc states that `/clear` stops either (a closed issue reports survival)".
  - F3 (hotfix and milestone-review sites omit that the session stops after a timed-out wait): partly refuted — both sites already require green CI before the merge; fix-now anyway, both now say "the session stops there … never merged past".
  - F4 (`TaskStop` prescribed for a timed-out Monitor, W18 says it is already gone): confirmed; fix-now — Monitor clause says "is then gone (`TaskStop` finds nothing)", on-timeout says "`TaskStop` a moved task".
  - F5 (Disposition mis-lands W21–W23): confirmed; fix-now — Disposition split per row.
  - F6 (four asserts, two registrations): rejected — T7 planned one entry per clause and PROFILE's test-doctrine owes no registration.
  - F7 (PROFILE correction keeps the wrong figure readable, contra the correcting-a-record convention): confirmed; fix-now — marker is now `(corrected M170)`, rewrapped.
  - F8 (run URLs indirect; W17/W18 name no run): rejected — AC1's enumerated observations all resolve to a URL via the Evidence snapshot; W17/W18 are outside its enumeration.
  - F9 (W3 mixes observed and documented under one tag): confirmed; fix-now — tag reads "observed; exceptions documented".
  - F10 (auto-background stated unconditionally; W3 records killed exceptions): confirmed; fix-now — exceptions named in the CI-checks clause.
  - F11 (cairn-release applies `TaskStop` to a foreground call): confirmed; fix-now — "a task still running at a … point is stopped with `TaskStop` first".
  - F12 (sweep no longer reaches cairn-release): rejected — the plan's DECIDE bounded AC3 to the sweep's returns; site read and consistent.
  - F13 (header lacked the PR URL at HEAD): no change needed — recorded in 76b4683.
  - F14 (PROFILE's no-checks claim generalized from the scratch repo): refuted by fresh evidence — `gh pr checks 173` on this repo printed "no checks reported on the 'm170-wait-doctrine' branch" and exited 1.
  - Fix-now batch re-verified: skills/tests 583 OK (trigger pin made wrap-tolerant, harness blocks re-anchored to the reflowed bytes), scripts 329 OK, hooks 121 OK, `cairn_validate` all checks passed, AC3 sweep unchanged (four sites, no retired wording).
- 2026-09-02: merge approved at the gate; user accepted the gate-side F1 fix as a logged deviation from the return floor (no defect return counted; the fix is on the branch at f552ff6 and re-verified).
