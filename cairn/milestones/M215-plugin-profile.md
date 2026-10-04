<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M215: Move this repo to the claude-plugin profile

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — it changes only this repo's own toolchain declaration and the dev docs that restate it   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m215-plugin-profile   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

This repo declares the `claude-plugin` toolchain profile in place of `generic`, with its own Python suites kept as gating checks.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `cairn/PROFILE.md`, rewritten from
`skills/shared/profiles/claude-plugin.md` with this repo's specifics kept:
the two `unittest` suites, the desktop binary path, the hand-run
`skills/tests` note, the no-CI note, and the no-`pytest` rule. The verify
slot gains `claude plugin validate .claude-plugin/marketplace.json`, which
passes today with no version warning. The statements that this repo runs
`generic`: `CLAUDE.md:4-9` and `cairn/DESIGN.md:14-15`.

**Out:** changes to the shipped profiles under `skills/shared/profiles/`
(their edge cases stay in the candidate row "claude-plugin profile edge
cases"). Re-gating `skills/tests` (D-109 stands). Adding CI. A
`CHANGELOG.md` entry, because no adopter sees this change. The two
untracked root files `cairn-probe.log` and `tsconfig.json`, which stay
unstaged at the user's choice.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: `cairn/PROFILE.md`'s first line is `# Toolchain profile: claude-plugin`, and from the repo root `python3 scripts/cairn_validate.py` exits 0 and prints `PASS  profile valid` and `PASS  weight caps`.
- [x] AC2: The `verify` slot of `cairn/PROFILE.md` names five gating commands, and each exits 0 when run from the repo root: `python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`, `claude plugin validate .claude-plugin/plugin.json`, `claude plugin validate .claude-plugin/marketplace.json`, and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`.
- [x] AC3: The `consistency-gate` slot names the claude-plugin profile's three checks (the verify checks pass on the review head, the marketplace validate prints no `plugins[N].version` warning, and `CHANGELOG.md` has an entry for the milestone's user-visible changes) and keeps the statement that this repo has no CI. The `release-walk` slot bumps `version` in `.claude-plugin/plugin.json` and in the `.claude-plugin/marketplace.json` plugin entry.
- [x] AC4: The `test-doctrine` slot still states three rules for this repo: no `pytest` in acceptance criteria, `skills/tests` hand-run and gating nothing, and the status mod tested by its `*.test.ts(x)` files under `claude plugin test`.
- [x] AC5: Among the lines that `git grep -n -w generic -- . ':!cairn/DECISIONS.md' ':!cairn/milestones' ':!cairn/legacy' ':!cairn/reviews' ':!*/tests/*' ':!hooks/status/fixtures*'` returns at review, none states that this repo's profile is `generic`, except the "cairn's own profile" candidate row in `cairn/ROADMAP.md` (the row this milestone promotes); and `CLAUDE.md` and `cairn/DESIGN.md` each name `claude-plugin` as this repo's profile.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1, T4
- AC2 → T1, T4
- AC3 → T1
- AC4 → T1, T5
- AC5 → T2, T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Rewrite `cairn/PROFILE.md` from `skills/shared/profiles/claude-plugin.md`:
      the header line, a comment naming the template and M215 (replacing
      the M46 `generic` note), and all seven slots. Keep this repo's notes
      from the current file (verify: the suites, `-k` and `discover` notes,
      the desktop binary path, `skills/tests` non-gating; consistency-gate:
      no CI; test-doctrine: no `pytest`, the status fixtures). Drop the
      template text that only serves other repos (the native-install path,
      the multi-plugin wording) to stay under the 120-line cap.
- [x] T2: Change `CLAUDE.md:4-9` and `cairn/DESIGN.md:14-15` to name
      `claude-plugin` as this repo's profile.
- [x] T3: Run the AC5 `git grep` and read each hit; fix any line that still
      states this repo runs `generic`.
- [x] T4: From the repo root, run `cairn_validate` and each of the five
      verify commands on its own, checking each exit code (no pipe, no `;`
      chain). The desktop shell has no `claude` on its PATH; use the newest
      app binary that the verify slot names.
- [x] T5: (review return 1) State in the `test-doctrine` slot that
      `skills/tests` gates nothing, then re-run the verify commands.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to plan (no work named) — switch this repo to the claude-plugin profile.
- 2026-10-04: question set: untracked `cairn-probe.log` and `tsconfig.json` in the repo root — leave them alone; never staged.
- 2026-10-04: collision check: promotes the candidate row "cairn's own profile" (M192 Out); its condition holds, since M192 shipped and that profile's verify slot takes a repo's own test commands. D-143's four gating checks are kept. D-109 is unaffected. No other ROADMAP, archive, or D-entry overlap.
- 2026-10-04: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-04: lessons harvested: M112 and M157 (sweep every surface that restates the profile, DESIGN.md by hand) shape AC5 and T2. M154 (the promoted row is pruned at post-merge hygiene, not at plan). M56 (check each exit code) shapes T4.
- 2026-10-04: criteria audit (reduced mode, fresh Opus reader): AC1-AC4 no finding. AC5 finding: "which post-merge hygiene removes" bound an act after review; narrowed to a parenthetical naming the row this milestone promotes. Side note: the rewritten PROFILE.md can come close to its 120-line cap, which T1 handles.
- 2026-10-04: plan gate chose adopting the shipped claude-plugin slots over keeping `generic` with only the header renamed, because verify already runs the profile's plugin checks and the 1.12.0 release commit (c08d01d) already bumped both manifests; falsified by a claude-plugin check this repo cannot pass on its own manifests.
- 2026-10-04: no `CHANGELOG.md` entry: no adopter-visible change.
- 2026-10-04: ROADMAP: pruned the M212 terminal row so the file stays under its 60-line cap with the M215 row added.
- 2026-10-04: implement started on branch m215-plugin-profile. Untracked `cairn-probe.log` and `tsconfig.json` left unstaged (question set).
- 2026-10-04: T1 done: PROFILE.md rewritten from the claude-plugin template at 113 lines. Dropped the template's native-install path and multi-plugin wording. test-doctrine names Python 3 stdlib as the dependency surface. greenfield-openers summarizes the two openers and this repo's answers. verify green: scripts 397 OK, hooks 174 OK, both validates exit 0, plugin test 1105 pass.
- 2026-10-04: T2 done: `CLAUDE.md:4-8` and `cairn/DESIGN.md:14-15` name `claude-plugin` as this repo's profile, and CLAUDE.md names the marketplace validate.
- 2026-10-04: T3 done: the AC5 sweep returned 33 lines. 31 name `generic` as a profile in a list or as an ordinary word, `cairn/PROFILE.md:4` records the past profile, and `cairn/ROADMAP.md:41` is the promoted row. None states the current profile is `generic`, so nothing more to fix.
- 2026-10-04: T4 done on ba8ee3b: cairn_validate exit 0 (profile valid, weight caps PASS), scripts 397 OK, hooks 174 OK, plugin validate exit 0, marketplace validate exit 0 with no version warning, plugin test 1105 pass 0 fail.
- 2026-10-04: claim audit: not owed — internal tier
- 2026-10-04: implement complete, status set to review.
- 2026-10-04: review return 1: AC4 fails as written. The `test-doctrine` slot does not state that `skills/tests` gates nothing.
- 2026-10-04: minor amendment: added T5 for review return 1, Coverage AC4 → T1, T5.
- 2026-10-04: T5 done: test-doctrine now calls `skills/tests` "a hand-run tripwire that gates nothing". verify green: validate exit 0, scripts 397 OK, hooks 174 OK, both validates exit 0, plugin test 1105 pass. Status set to review.
- 2026-10-04: step-7 approval: m215-plugin-profile approved for merge

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Pass 1, 2026-10-04, on b417323 (main 14ec5a7 not moved, no PR).

- AC1: PROFILE.md line 1 is `# Toolchain profile: claude-plugin`. `cairn_validate` exit 0 with `PASS  weight caps` and `PASS  profile valid`.
- AC2: the verify slot's command block lists the five commands. Each exit 0 from the repo root: scripts 397 OK (21 skipped), hooks 174 OK, plugin validate, marketplace validate, plugin test 1105 pass 0 fail.
- AC3: consistency-gate lists the three checks and keeps the no-CI paragraph. release-walk bumps `version` in `.claude-plugin/plugin.json` and the marketplace plugin entry.
- AC4: FAIL. test-doctrine states no `pytest` and the status mod under `claude plugin test`, and calls `skills/tests` a hand-run tripwire, but does not state that it gates nothing (only the verify slot says so).
- AC5: the sweep returns 33 lines. None states the current profile is `generic` except the promoted row `cairn/ROADMAP.md:41`. `CLAUDE.md:5` and `cairn/DESIGN.md:15` name `claude-plugin`.

Pass 2, 2026-10-04, on 13d2ce1 (main 14ec5a7 not moved).

- AC1: line 1 `# Toolchain profile: claude-plugin`. `cairn_validate` exit 0, `PASS  weight caps`, `PASS  profile valid`.
- AC2: the five commands each exit 0: scripts 397 OK (21 skipped), hooks 174 OK, plugin validate, marketplace validate, plugin test 1105 pass 0 fail.
- AC3: unchanged since pass 1 (T5 touched only test-doctrine). Three consistency-gate checks, no-CI note, both version bump sites present.
- AC4: test-doctrine lines 4-5 (no `pytest`), line 7 (mod tests under `claude plugin test`), line 13 (`skills/tests` "a hand-run tripwire that gates nothing").
- AC5: sweep returns 33 lines, the same classification as pass 1.
- Gate: `cairn_validate` exit 0. No principle changed, so `cairn_impact` skipped. Profile consistency-gate: verify passes on the review head (AC2 run), marketplace validate shows 0 `plugins[N].version` warnings, and no `CHANGELOG.md` entry is owed (no user-visible change).
- spawned: diff-bug (internal tier, docs-only diff)
- diff-bug #1: the changelog check is not tied to the surface tier — reject (false): the slot asks for an entry only for user-visible changes, and an internal milestone has none.
- diff-bug #2: PROFILE.md and CLAUDE.md credit the marketplace validate to D-143, which adopted only the plugin validate and the mod test — fix now, fixed c0add10.
- diff-bug #3: the template's warning that `claude plugin test .` runs every `*.test.ts(x)` under the folder was dropped — fix now, fixed c0add10.
- diff-bug #4: no file states the lowest Claude Code version the test-doctrine names as a dependency — follow-up, added to the candidate row "claude-plugin profile edge cases".
- diff-bug #5: the gate re-runs verify on the same head as the AC step — reject (planned change): AC3 requires the profile's checks, and the cost is one more run.
- diff-bug #6: the release-walk repeats steps `/cairn-release` already takes — reject (planned change): it is the shipped template's text, which AC3 requires.
- diff-bug #7: "Skill and rulebook markdown … owes no test" is broader than D-109 — fix now, fixed c0add10.
