<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M340: Fix mod tests that fail on main

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — the status mod's tests in this repo; no external consumer relies on them   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The status mod's test suite passes on the installed `claude` binaries again, with its band tests written for the engine's per-plugin `AbovePrompt` rows.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `hooks/status/band.test.tsx`. The engine now asks each plugin for its own `AbovePrompt` row (plugin-authoring reference, 2.1.331). The PROBE plugin's `next.trace` read of a `cairn` link now reads "absent", and the cases with the BENEATH plugin, which never calls `next`, now also get the engine's slot row. Rewrite the PROBE cases' no-throw check (for example with the kit's `ui.keepsBeneath()`), and update the BENEATH cases' expected rows to the per-plugin model, keeping each case's stated property. The 19 failing names are the sorted `(fail)` lines of main's run at f16ca210 (M339 review evidence).

**Out:** changes to the mod's code (`hooks/status/*.ts`, `register.tsx`); if a fix needs one, that is an amendment stop. The parked flaky refused-clear band tests → their own row "Fix the flaky refused-clear band tests".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: On the branch, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exits 0 under the Homebrew `claude` 2.1.323 and under the desktop-app binary 2.1.331 (the newest under the path that `cairn/PROFILE.md`'s verify slot names), and each run reports at least 2466 tests.
- [ ] AC2: In `hooks/status/band.test.tsx` on the branch, the two `no-roadmap … does not throw` cases and every `with nothing workable, <skill> draws the empty row with no action Buttons (M213)` case fail when a `throw` is the first statement of the `AbovePrompt` hook in `hooks/status/register.tsx`.
- [ ] AC3: On the branch, both `python3 -m unittest discover` suites (`scripts/tests`, `hooks/tests`), both `claude plugin validate` commands of the verify slot, and the hand-run `python3 -m unittest discover -s skills/tests -p "test_*.py"` pass.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2, T4
- AC2 → T1, T3
- AC3 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [ ] T1: Rewrite the PROBE cases (`band.test.tsx` ~lines 1522-1536 and ~2100-2110): assert the mod draws nothing and keeps what is beneath (`ui.keepsBeneath()`), and find a kit signal that tells a thrown hook from a returned one (the kit's report of skipped hooks, or a check in the case itself); drop PROBE if nothing uses it.
- [ ] T2: Update the BENEATH cases ("the close button (M194 AC2) > mixed over a plugin beneath", "cairn's rows sit above the band beneath (M193 AC6)") to the per-plugin row model, keeping their stated property: cairn's rows first, the other plugin's row kept, and a press leaving that row.
- [ ] T3: Plant a `throw` as the first statement of the `AbovePrompt` hook (`hooks/status/register.tsx:811`), run the suite once, record which AC2 cases fail, and revert; the plant is never committed.
- [ ] T4: Run the verify slot under both binaries and the hand-run `skills/tests`; record each binary's version and test count.

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

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
