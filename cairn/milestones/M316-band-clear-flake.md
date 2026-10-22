<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M316: Fix the flaky refused-clear band tests

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cause can sit in the shipped status mod (`hooks/status/register.tsx`), not only in the test file
- **Branch/PR:** —

## Goal

The refused-clear tests of M221 AC4 in `hooks/status/band.test.tsx` stop failing at random with a doubled `/clear` fill, because the cause of the second fill is found and removed.

## Scope

**In:** Find the order of events that adds a second `/clear` fill in a refused-clear case. Remove that cause in the status mod (`hooks/status/register.tsx`) or in the test file, whichever holds it. Add a test that forces that order when the cause is in the mod. Add a CHANGELOG entry when the fix changes what the mod does for users.

**Out:** Other mod tests. None is recorded as flaky, and a new flaky test found here gets its own candidate row. A cause inside the `claude plugin test` runner: no in-repo fix reaches it, so the plan returns for amendment with the reproduction and a candidate row.

## Acceptance criteria

- [ ] AC1: The cause of the second `/clear` fill is removed, shown by its location. If the cause is in `hooks/status/register.tsx`, a test in `hooks/status/band.test.tsx` forces the order of events that adds the second fill. It passes with the fix, and it fails with two `/clear` fills when the fix's changes outside that test are reverted, one run of each recorded in the Review section. If the cause is in the test file, the Review section records one run with that order forced by a temporary edit, which fails with two `/clear` fills before the fix and passes after, and no permanent test is added.
- [ ] AC2: Each of the 9 test cases that the `describe` at `hooks/status/band.test.tsx:3648` runs on the default branch (2 fixtures × 2 surfaces × 2 templates, and the control) runs and passes on the branch under the same title. No `expect(` line in that `describe`, and none of the constants its cases read (`CLEAR_RUN`, `CLEAR_END`, `NO_RUN`, `SURFACES`), changes in `git diff <default-branch> -- hooks/status/band.test.tsx`.
- [ ] AC3: With the fix, the cases of the `describe` at `hooks/status/band.test.tsx:3648` fail 0 times across 20 consecutive runs of `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` from the repo root.
- [ ] AC4: The `verify` slot of `cairn/PROFILE.md` is green: each of its five commands exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T2
- AC3 → T3
- AC4 → T3

## Tasks

- [ ] T1: Find the cause. Read the held-command and fallback paths in `hooks/status/register.tsx` (`pressChecked` near :1474, the `session.end` hook near :736 with its unawaited `void run` and `void fallBack`, the module-level `heldRun`) and the test helpers (`seat`, `untilRuns` near :2961, which waits about 55 ms at `tries` 10). Force the suspected order, see two `/clear` fills on the default branch's code, and log the cause: the line that adds the second fill and the order that reaches it. If the cause depends on the fixture or surface, the forcing test loops over them as the original template does.
- [ ] T2: Fix the cause and keep the 9 cases as AC2 states. For a cause in the mod, keep the AC1 test. Add a CHANGELOG Unreleased entry when the mod's behavior for users changes.
- [ ] T3: Run the 20 consecutive runs in the background (about 37 minutes), checking each exit code, and record any fail outside the `describe` as a candidate row. Run the verify slot.

## Work log

- 2026-10-22: created by /milestone-plan.
- 2026-10-22: tier check: not run — work named at the question set.
- 2026-10-22: idea vet: no concern. A flaky test fix is correct by the repo's test doctrine, the operator lost review runs to it (M312, M313), and the row's name says what it does.
- 2026-10-22: collision check: source is the candidate row "Fix the flaky refused-clear band tests", absorbed in full. No archive or D-entry match for a band test flake. M221, M243, M255, and M260 shaped the held-command code.
- 2026-10-22: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn, so no overlap.
- 2026-10-22: lessons harvest: LESSONS M56+M65 (check each exit code, never pipe), M278 (cleanup moved behind awaits), and M193 (mod test harness facts) bear on T1 and T3.
- 2026-10-22: criteria audit (full mode, fresh Opus reader): 5 findings on this milestone, all fixed. AC1 made conditional on where the cause lies (mod, test file, or runner, the runner case moved to Out). AC3 narrowed from the whole suite to the `describe`'s cases, other fails going to candidate rows. AC2 now names the 9 cases and the constants, since unchanged `expect(` lines alone let a loop shrink. The fixture and surface probe went to T1.
- 2026-10-22: plan gate chose 20 repeat runs (about 37 minutes) over 50 because AC1's forced order carries the proof and the runs only back it; falsified by a fail of the `describe`'s cases after merge.
- 2026-10-22: plan split: M316 holds this fix, M317 holds the PR-cap report, both picked at the question set; the two are independent.

## Decisions

## Review
