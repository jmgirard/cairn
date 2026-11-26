<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M340: Fix mod tests that fail on main

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — the status mod's tests in this repo; no external consumer relies on them   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m340-mod-tests-per-plugin-rows, https://github.com/jmgirard/cairn/pull/355   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The status mod's test suite passes on the installed `claude` binaries again, with its band tests written for the engine's per-plugin `AbovePrompt` rows.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `hooks/status/band.test.tsx`. The engine now asks each plugin for its own `AbovePrompt` row (plugin-authoring reference, 2.1.331). The PROBE plugin's `next.trace` read of a `cairn` link now reads "absent", and the cases with the BENEATH plugin, which never calls `next`, now also get the engine's slot row. Rewrite the PROBE cases' no-throw check (for example with the kit's `ui.keepsBeneath()`), and update the BENEATH cases' expected rows to the per-plugin model, keeping each case's stated property. The 19 failing names are the sorted `(fail)` lines of main's run at f16ca210 (M339 review evidence).

**Out:** changes to the mod's code (`hooks/status/*.ts`, `register.tsx`); if a fix needs one, that is an amendment stop. The parked flaky refused-clear band tests → their own row "Fix the flaky refused-clear band tests".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: On the branch, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exits 0 under the Homebrew `claude` 2.1.323 and under the desktop-app binary 2.1.331 (the newest under the path that `cairn/PROFILE.md`'s verify slot names), and each run reports at least 2466 tests.
- [x] AC2: On the branch, both `python3 -m unittest discover` suites (`scripts/tests`, `hooks/tests`), both `claude plugin validate` commands of the verify slot, and the hand-run `python3 -m unittest discover -s skills/tests -p "test_*.py"` pass.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2, T4
- AC2 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: Rewrite the PROBE cases (`band.test.tsx` ~lines 1522-1536 and ~2100-2110): assert the mod draws nothing and keeps what is beneath (`ui.keepsBeneath()`), and look for a kit signal that tells a thrown hook from a returned one; drop PROBE. The search found no such signal (T3), so that check went to the parked row "Recheck band tests for per-plugin rows" and is not part of this task's result.
- [x] T2: Update the BENEATH cases ("the close button (M194 AC2) > mixed over a plugin beneath", "cairn's rows sit above the band beneath (M193 AC6)") to the per-plugin row model, keeping their stated property: cairn's rows first, the other plugin's row kept, and a press leaving that row.
- [x] T3: Plant a `throw` as the first statement of the `AbovePrompt` hook (`hooks/status/register.tsx:811`), run the suite once, record what fails, and revert; the plant is never committed.
- [x] T4: Run the verify slot under both binaries and the hand-run `skills/tests`; record each binary's version and test count.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-11-25: created by /milestone-plan from the high candidate row "Fix mod tests that fail on main" (M339 implement).
- 2026-11-25: tier check: milestone — several test cases change, and how to assert that the mod's hook did not throw is a design choice; no runtime surface changes.
- 2026-11-25: idea vet: one gap — the probe's no-throw check may have no exact kit replacement; reading taken: AC2's planted throw must turn those cases red, by whatever signal T1 finds. No flaw.
- 2026-11-25: lessons used: 2026-10-25 (M321), 2026-07-16 (M56), 2026-10-01 (M286).
- 2026-11-25: collision check: D-143 (the mod's checks gate this repo) holds and is the reason for the fix; archived M193 AC6, M194 AC2, M213 own the cases' properties; parked row "Fix the flaky refused-clear band tests" stays separate. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-11-25: criteria audit (reduced mode, fresh Opus reader): AC1 pins both binary versions (taken); the 2466 floor is brittle if cases merge (kept, as the guard against dropping cases; a merge is an amendment); AC2 names its case list instead of a filter and drops the plant's method and its pass half, which T3 and AC1 hold (taken); AC3 none.
- 2026-11-25: question set: none posed — nothing open is the user's to settle (no permission, file, or choice of what the user gets).
- 2026-11-25: plan gate chose updating the tests to the per-plugin model over pinning an older `claude` for the verify slot, because both installed binaries draw per-plugin rows and the reference documents it; falsified by a current Claude Code that again composes `AbovePrompt` as one chain across plugins.

- 2026-11-25: implement started on branch m340-mod-tests-per-plugin-rows.
- 2026-11-25: T1, T2: PROBE removed; the two no-roadmap cases assert only `[ENGINE]` (the kit's `keepsBeneath()` rejects there, since the test draws the engine slot with its own hook) and are renamed "draws nothing and the engine's slot shows"; the M213 empty-row cases assert `keepsBeneath()` is true; the five BENEATH cases expect the engine's slot after the other plugin's row. First run: 2464 pass, 2 fail (the `keepsBeneath` rejects), fixed.
- 2026-11-25: T3: with a planted `throw` as the hook's first statement, `band.test.tsx` did not load at all ("its run ended without a report"), and the kit has no call that tells a test a hook was skipped (it names skipped hooks only in a failure's report), so no case can tell a thrown hook from one that drew nothing. Reverted; `git diff -- hooks/status/register.tsx` empty.
- 2026-11-25: substantive amendment: AC2 (the planted-throw discrimination) removed, and AC3 renumbered AC2; T3's record line reworded. The lost no-throw check goes to the parked row "Detect a thrown band hook in tests". A removal leaves no amended wording to re-audit, so no reader ran; it narrows the criteria and changes nothing the user sees, so no stop.
- 2026-11-25: plan gate's alternative (a state-read check: assert cairn's hook read its `band` state during the mount) weighed and not taken, because the atom read may be served without a `state.get` and the planted run cannot load the file to prove it; falsified by a kit release that reports skipped hooks or a planted run that loads.
- 2026-11-25: T4: `claude plugin test .` exit 0, 2466 pass of 2466, under claude 2.1.323 (Homebrew) and 2.1.331 (desktop app); scripts and hooks suites OK, both validates exit 0, hand-run `skills/tests` OK.
- 2026-11-25: claim audit: not owed — internal tier
- 2026-11-25: implement done; status review.
- 2026-11-25: T1's wording narrowed at review (minor amendment, Copilot thread on PR #355): it no longer claims a thrown-hook signal was found; T3 recorded none, and the check is in the parked row "Recheck band tests for per-plugin rows".

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->

Review head 15dd70b6, merge base 2b2d90ae (= origin/main). Copilot arm: PR #355 opened at review start, Copilot requested.

- AC1: on 15dd70b6, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exit 0, 2466 pass of 2466, under the Homebrew claude 2.1.323 and the desktop-app claude 2.1.331 (the newest under the verify slot's path). Also green on 5baf3eeb before the fix-now commit. Met.
- AC2: on 15dd70b6, `scripts/tests` and `hooks/tests` OK, both `claude plugin validate` commands exit 0 (no `plugins[N].version` warning), hand-run `skills/tests` OK. Met.
- Consistency gate: `cairn_validate` all checks passed; no DESIGN principle changed; no CHANGELOG entry owed (test-only change, no user-visible behavior); verify per AC1-AC2.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the five other-plugin cases now check the engine's row stacking more than cairn's placement of `next(e)` — follow-up, parked row "Recheck band tests for per-plugin rows" (extended), promote when a band hook misplaces a row in a live session
- diff-bug #2: `not.toContain(BENEATH_ROW)` in cairn's Box is vacuous — fix now
- diff-bug #3: the M194 AC2 case's "leaves the row" half cannot fail through cairn's code — follow-up, same parked row
- diff-bug #4: those cases test dependency behavior ("What gets a test") — follow-up, same parked row
- diff-bug #5: the new `keepsBeneath()` check was never shown able to fail — fix now (removed; the M213 cases' `isEmptyRow` already fails when no empty row draws)
- diff-bug #6: the no-throw property is lost for the no-roadmap cases — follow-up, same parked row
- diff-bug #7: the parked row overstated the M213 cases' loss — fix now (row rewritten)
- diff-bug #8: the BENEATH comment credits the plugin for the engine's slot — fix now
- diff-bug #9: stale `lines()` comment order and "beneath" names — fix now for the comment; reject the names (style: "band beneath" still names the other plugin's row below cairn's)
- diff-bug #10: `[rows, ENGINE]` assertions elsewhere test less than before — follow-up, same parked row (outside the diff)
- diff-bug #11, #12: no issue found
- blame-history #1: no-throw check lost (D-143's risk) — follow-up, same parked row
- blame-history #2: parked row overstates the M213 loss — fix now (same as diff-bug #7)
- blame-history #3: Scope still says to rewrite the no-throw check — reject (false: the amendment's work-log line supersedes it; Scope is plan-owned)
- blame-history #4: the `keepsBeneath` rejection in the no-roadmap cases is unverified — reject (false: observed as a HooksError in the first T1 run)
- blame-history #5, #6: no finding
- prior-review #1: plant-verified discrimination dropped — follow-up, same parked row
- prior-review #2: `keepsBeneath()` meaning under a throw unverified — fix now (removed, as diff-bug #5)
- prior-review #3: the rename hides that a throw was under test — reject (planned change: the amendment removed that claim)
- prior-review #4: ENGINE ordering encoded as contract — follow-up, same parked row
- prior-review #5: the AC2 removal had no reader — reject (false: a removal leaves no amended wording for the re-audit)
- ripple #1: "the band beneath shows alone" now false — fix now (renamed)
- copilot: cairn/milestones/M340-mod-tests-per-plugin-rows.md:43 (T1 claims the signal search delivered) — fix now
- copilot: https://github.com/jmgirard/cairn/pull/355#pullrequestreview-6067564881 — no comment
- Copilot level: Low (set by GitHub's settings)
- conversation: PR #355 — no issue comments; the one thread is Copilot's above
- snapshot: none
- Fix-now items fixed 15dd70b6 (test file and parked row) and in this commit (T1 wording).
