# M184: Guest collaboration mode — local-only tracking

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP2, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate -->
- **Surface tier:** user-facing — adopters declare the mode and run the skills under it   <!-- owner: plan -->
- **Branch/PR:** m184-guest-mode · https://github.com/jmgirard/cairn/pull/191   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create -->

A repo the operator does not own can run cairn's plan/implement/review loop with `cairn/` kept local — listed in `.git/info/exclude`, never committed — and nothing written outside `cairn/`.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a collaboration-mode declaration — `owner` (today's rules, the default when absent) or `guest` — as a second header line in `cairn/PROFILE.md`, `# Collaboration mode: guest` (D-137). `cairn_validate` reads it: value check; guest-mode `scaffold present` requires `cairn/` in `.git/info/exclude` and drops the `.gitignore`/`.Rbuildignore` requirements. `/cairn-init` gains a guest path: a mode chip whose recommendation reads `gh repo view --json viewerPermission`; writes `cairn/` to `.git/info/exclude`; skips the CLAUDE.md append, the `.gitignore` entries, the `.Rbuildignore` entry, the CI `paths-ignore` chip, and the scaffold commit + push. The session hook injects the CLAUDE.md routing section itself in guest mode. The commit guard denies a commit carrying any `cairn/` path in guest mode. A rulebook `## Collaboration mode` section states the guest rules; the plan and implement skills gain guest arms (tracking written to disk in the same turn, no commit); `/milestone` §2's CLAUDE.md-section check gains a guest arm; `/cairn-release` and `/cairn-triage` stop in guest mode; README subsection.

**Out:** fork-aware remotes, the review handoff, and `/milestone` reconciliation of a maintainer-merged PR → M185. Adopting a third party's PR into a guest repo via `/hotfix` → unsupported, stated in the rulebook section. Two cairn operators in one repo → the standing candidate row. Branch-protected owner repos → the standing candidate row (guest mode pushes nothing to the default branch, so it sidesteps rather than solves it). A guest-mode substitute row in D-060's always-read frame → D-137 states the governance instead (the frame table is history).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: `cairn_common.collaboration_mode(root)` returns `guest` on a `cairn/PROFILE.md` carrying `# Collaboration mode: guest`, `owner` on one with no mode line, and `owner` when `cairn/PROFILE.md` is absent (unit tests in `hooks/tests/test_hooks.py`). On a fixture repo carrying a `DESCRIPTION` file, that guest line, `cairn/` in `.git/info/exclude`, no cairn entries in `.gitignore`, and no `.Rbuildignore`, `python3 scripts/cairn_validate.py` passes `scaffold present` and `profile valid`; the same fixture with the exclude line removed fails `scaffold present` with a message naming `.git/info/exclude`; a fixture whose mode line reads `# Collaboration mode: other` fails `profile valid` with a message naming the line; an owner fixture whose `.git/info/exclude` lists `cairn/` but whose `.gitignore` lacks the required entries still fails `scaffold present`.
- [x] AC2: On the guest fixture, `hooks/session_context.py` output contains a `## Collaboration mode` part whose body is the body of the section whose heading starts `## Project tracking` in `skills/shared/templates/claude-md-section.md`, read from disk at injection, followed by one line naming the mode; on an owner fixture the output contains no such part.
- [x] AC3: On the guest fixture, `hooks/commit_guard.py` returns `permissionDecision: deny` for a `git commit` whose `committed_paths()` set includes a `cairn/` path — probed as a staged path and via `git commit -am` over a modified, unstaged `cairn/` file, on a feature branch and on the default branch alike — the reason naming the path; a commit carrying only non-`cairn/` paths on a feature branch gets no deny and no nudge, and the same commit on the default branch gets the nudge and no deny; in guest mode the nudge text names `<slug>` rather than `m<nnn>-<slug>`; the four guest deny probes replayed against an owner fixture produce no `permissionDecision`, and the existing `TestCommitGuard` cases pass unmodified.
- [x] AC4: `skills/cairn-init/SKILL.md` carries one guest-path passage under a heading naming guest mode that names all eight items: the mode chip, the `viewerPermission` read behind its recommendation, the `.git/info/exclude` write, and the five skipped writes (CLAUDE.md append, `.gitignore` entries, `.Rbuildignore` entry, CI `paths-ignore` chip, scaffold commit + push); verified by reading the passage.
- [x] AC5: `skills/shared/tracking-rules.md` gains a `## Collaboration mode` section stating, for guest mode: `cairn/` is never committed; no docs-only commit or push to the default branch; tracking is written to disk in the turn that changes the code; the branch name is `<slug>` alone and PR bodies and commit messages carry no `M<NNN>` and no cairn vocabulary; `/cairn-release` and `/cairn-triage` stop with a stated reason; adopting a third party's PR is unsupported. The git model's `m<nnn>-<slug>` bullet is qualified as owner mode; the PROFILE file-map row and the "Toolchain profiles" section name the mode line as the only line outside the seven `##` slots that `scripts/cairn_validate.py` reads. `/milestone-plan` step 6, `/milestone-implement` step 4, and `/milestone` §2's CLAUDE.md-section check and its `uncommitted changes under cairn/` orphan check each state their guest arm; `/cairn-release` and `/cairn-triage` each carry a session-start stop clause; `cairn/DESIGN.md`'s GP2 carries a clause qualifying "tracking travels with code" as owner mode and naming guest mode's local-only tracking with its justification (D-137). Verified by reading each passage.
- [x] AC6: `grep -rniE "one (person|operator|cairn operator)|single-writer" README.md cairn/DESIGN.md skills/shared/tracking-rules.md skills/cairn-init/SKILL.md` is re-run at review and each of its hits either names guest mode in the same sentence or is listed in the work log as exempt with a stated reason; README's "Working with collaborators" section carries a guest-mode subsection naming the exclude file and what guest mode changes: no merge by cairn (the PR is handed to the maintainers), hygiene written to disk rather than committed, no release walk.
- [x] AC7: `CHANGELOG.md` carries an entry under the dev heading naming the guest mode, and the `verify` slot's two suites exit 0 from the repo root, each exit code checked, with no new test skipped.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T6, T7
- AC6 → T8
- AC7 → T9

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: `hooks/cairn_common.py`: `collaboration_mode(root)` reading `cairn/PROFILE.md` for a `# Collaboration mode: <value>` line (regex beside the shape of `session_context._PROFILE_HEADER`, hooks/session_context.py:33), `owner` when absent; tests in `hooks/tests/test_hooks.py`.
- [x] T2: `scripts/cairn_validate.py`: parse the same line by hand (hooks and scripts share no code — M113 lesson; a comment names the hook twin); `check_profile` FAILs a value outside `owner|guest` (`:787-813`); `check_scaffold` guest arm requires `cairn/` or `cairn` in `.git/info/exclude` and skips `REQUIRED_GITIGNORE`/`REQUIRED_RBUILDIGNORE` (`:487-514`); tests in `scripts/tests/test_scaffold_check.py` and `test_scripts.py::TestValidateProfile`.
- [x] T3: `hooks/session_context.py`: guest part after the profile part (`:244-251`), body read from the template relative to the hook file, charged against `MAX_CHARS`; tests beside `TestSessionContext`.
- [x] T4: `hooks/commit_guard.py`: guest deny arm ahead of the default-branch early return (`:86-90`), envelope as `merge_guard.py:180-190`; tests in `TestCommitGuard`.
- [x] T5: `skills/cairn-init/SKILL.md`: §0 mode detection + chip; §1 guest branch (exclude write; the five skips); §3 repair recognizes the guest scaffold; profile templates untouched (init writes the line).
- [x] T6: `skills/shared/tracking-rules.md`: `## Collaboration mode` section, owner qualifier on the branch bullet (`:225`), file-map PROFILE row and "Toolchain profiles" mention; `cairn/DESIGN.md` GP2 clause.
- [x] T7: guest arms in `milestone-plan` step 6, `milestone-implement` step 4 (`:70-72`), `milestone` §2 (`:127`, `:130-131`); session-start stop clauses in `cairn-release` and `cairn-triage`.
- [x] T8: README guest subsection; run AC6's grep and disposition each hit (amend or work-log exemption).
- [x] T9: CHANGELOG entry; run both suites from the repo root, exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-09-10: created by /milestone-plan; criteria audit ran in full mode via a fresh [O] reader: 24 findings across M184/M185, 20 fixed in the drafts, 4 posed at the gate (all took the recommended option); a second fresh [O] read of the post-gate wording returned 14 findings, all fixed before the commit.
- 2026-09-10: plan gate chose a `# Collaboration mode:` header line in PROFILE.md over a separate `cairn/MODE.md` because both existing readers already parse that header and no scaffold list changes; falsified by an adopter whose PROFILE.md hits the 120-line cap on that one line, or a third reader that cannot share the header regex.
- 2026-09-10: plan chose `.git/info/exclude` over an out-of-tree state directory because every `cairn/` path in the rulebook, skills, scripts, and hook root discovery stays valid; falsified by a workflow that routinely runs `git clean -fdx` in guest repos (the exclude file does not protect against it).
- 2026-09-10: /milestone-implement started; branch m184-guest-mode; question gate skipped — the plan gate settled the mode line, exclude file, and deny-arm shape, and the changelog dev heading follows the `## Unreleased` convention from git history.
- 2026-09-10: T1 done — `cairn_common.collaboration_mode(root)` with five tests in `TestCollaborationMode` (guest, no line, absent file, explicit owner, unknown value returned lowercased for the validator to judge).
- 2026-09-10: T2 done — minor amendment: the validator reuses `cairn_common.collaboration_mode` through cairn_scripts' existing shim instead of a hand-parsed twin (T2's "share no code" premise was off: `cairn_scripts` already imports `cairn_common`; one regex, no drift); `check_scaffold` guest arm requires `cairn/` (or `cairn`, `/cairn/`, `/cairn`) in `.git/info/exclude` and skips the .gitignore/.Rbuildignore entries; `check_profile` FAILs a mode outside owner|guest quoting the line; 6 tests in `TestScaffoldGuestMode`, 2 in `TestValidateProfile`.
- 2026-09-10: T3 done — `session_context.routing_section()` reads the template's `## Project tracking` body relative to the hook file; the `## Collaboration mode` part (body + one mode line) is appended after the profile part in guest mode only, inside the MAX_CHARS accounting; 2 tests in `TestSessionContext`.
- 2026-09-10: T4 done — guest deny arm in `commit_guard.main` ahead of the default-branch return (deny envelope as merge_guard, reason lists the cairn/ paths); the nudge's branch shape comes from `BRANCH_SHAPE[mode]` (`<slug>` in guest); 5 tests in `TestCommitGuardGuestMode`, the four deny probes (staged/-am × main/feature) replayed against an owner profile; existing `TestCommitGuard` unmodified and green.
- 2026-09-10: T5 done — cairn-init §0 gains a "Collaboration mode" bullet (the `viewerPermission` read and the mode chip), §1 a `### Guest mode` passage naming the mode line, the exclude write, and the five skipped writes, §3 a guest arm reading the line from the existing file.
- 2026-09-10: T6 done — rulebook `## Collaboration mode` section (six bullets: never-committed cairn/, no default-branch commit or push with tracking written to disk same turn, no cairn vocabulary and the `<slug>` branch, release/triage stop, third-party PR unsupported, merge/remotes deferred to M185); owner qualifier on the branch bullet; PROFILE file-map row and "Toolchain profiles" name the mode line; enforcement-boundary sentence names guest mode; DESIGN GP2 clause and the Known-issues collaboration-model sentence name guest mode with D-137.
- 2026-09-10: T7 done — guest arms in `/milestone-plan` step 6 (no plan commit or push; files written same turn), `/milestone-implement` step 4 (code-only checkpoint; tracking on disk; `<slug>` branch, no cairn vocabulary in messages), `/milestone` §2 (orphan check skipped and reported; CLAUDE.md check reads the exclude line instead); session-start stop clauses in `/cairn-release` and `/cairn-triage` with fixed status-line text.
- 2026-09-10: T8 done — README "Contributing to a repo you don't own (guest mode)" subsection under "Working with collaborators" (exclude file, no merge by cairn, hygiene on disk, no release walk or triage); AC6 grep re-run: 3 hits (DESIGN.md:162, README.md:268, tracking-rules.md:256), each names guest mode in the same sentence; no exemptions.
- 2026-09-10: T9 done — CHANGELOG `## Unreleased` → New entry for guest mode; both suites from the repo root: scripts 387 tests OK exit 0, hooks 138 tests OK exit 0, no skips; `cairn_validate` all checks passed.
- 2026-09-10: claim audit: 41 claims read, 5 corrected — README.md, CHANGELOG.md, skills/shared/tracking-rules.md, hooks/cairn_common.py, hooks/commit_guard.py, hooks/session_context.py ("any commit" narrowed to the commit the guard sees with its documented misses; the "parses by hand / share no code" comment replaced by the one-parser fact; stale commit_guard docstring gained the guest deny paragraph; abspath comment made exact). The same-reader re-read went to a second fresh [O] reader (this harness has no SendMessage; M182 precedent, the standing candidate row) and returned no corrections. Audit also raised a fence edge: a mode look-alike inside a slot body tripped `profile valid`; both readers now stop at the first `## ` heading, one test each side.
- 2026-09-10: open concern from the claim audit, not acted on (plan scope names the `.Rbuildignore` skip): in a guest-mode R-package repo `R CMD build` includes untracked files, so a local build would carry `cairn/` into the tarball without `^cairn$`; left for the review gate — a candidate row or an M185 note.
- 2026-09-10: all tasks done; both suites green; status → review.
- 2026-09-10: step-7 approval: PR #191 approved for merge.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

- 2026-09-10: default branch in sync with origin, unmoved since the cut; branch pushed; draft PR #191 opened (Resolves `—`, no closing lines).
- AC1: `collaboration_mode()` on a scratch fixture returned `guest` (mode line), `owner` (no line), `owner` (no PROFILE.md); `cairn_validate` on the guest fixture (DESCRIPTION, exclude line, no cairn .gitignore entries, no .Rbuildignore) passed `scaffold present` and `profile valid` (exit 0); exclude line removed → `scaffold present` FAIL naming `.git/info/exclude`; mode `other` → `profile valid` FAIL quoting the line; owner fixture with the exclude line and no .gitignore entries → `scaffold present` FAIL. `TestCollaborationMode` 5, `TestScaffoldGuestMode` 6, `TestValidateProfile` 2 green. PASS.
- AC2: `session_context.py` on the guest fixture emitted a `## Collaboration mode` part; the template's `## Project tracking` body (read from disk) is contained in it verbatim, followed by the line naming mode `guest`; the owner fixture's output has no such part. PASS.
- AC3: `commit_guard.py` on the guest fixture: staged and `-am` probes over a modified `cairn/ROADMAP.md`, on `main` and on `feature` → all four `permissionDecision: deny`, reason naming the path; non-cairn commit on `feature` → empty output; on `main` → nudge, no deny, nudge names `<slug>` and not `m<nnn>`; the four probes replayed on an owner fixture → no `permissionDecision`. The branch diff to `test_hooks.py` is additions only (existing `TestCommitGuard` untouched), and the class runs green. PASS.
- AC4: `skills/cairn-init/SKILL.md` §1 `### Guest mode` names the mode line, the `.git/info/exclude` write, and the five skipped writes (CLAUDE.md append, .gitignore entries, .Rbuildignore entry, CI paths-ignore chip, scaffold commit + push); the mode chip and the `viewerPermission` read sit in §0 and the passage names them as §0's. Read. PASS.
- AC5: rulebook `## Collaboration mode` section read: never-committed `cairn/`, no docs-only commit or default-branch push, tracking to disk same turn, `<slug>` branch and no cairn vocabulary in commits/PRs, release and triage stop with the reason, third-party PR unsupported. Git-model branch bullet reads "(owner mode; guest mode names the branch `<slug>` alone)"; PROFILE file-map row and "Toolchain profiles" both name the mode line as the only non-slot line the validator reads. Guest arms read in `/milestone-plan` step 6, `/milestone-implement` step 4, `/milestone` §2 (orphan check skipped and reported; CLAUDE.md check reads the exclude line); session-start stop clauses read in `/cairn-release` and `/cairn-triage`; DESIGN GP2 clause qualifies owner mode and names guest mode's local-only tracking with its justification and D-137. PASS.
- AC6: grep re-run at review: 3 hits (DESIGN.md:162, README.md:268, tracking-rules.md:256), each naming guest mode in the same sentence; no exemptions. README "Working with collaborators" carries "Contributing to a repo you don't own (guest mode)" naming `.git/info/exclude`, no merge by cairn (PR handed to the maintainers), hygiene written to disk, no release walk or triage. PASS.
- AC7: `CHANGELOG.md` `## Unreleased` → New entry names the guest mode. Suites from the repo root: scripts 388 tests exit 0, hooks 139 tests exit 0, no skips. PASS.
- Driving RR `—`: no projection-vs-outcome pairs.
- Consistency gate: `cairn_validate` all checks passed (exit 0); `cairn_impact --changed` on GP2 lists 10 references — DESIGN.md:120 (the principle), D-137, M184/M185 (this work), two archives (history) — nothing to reconcile; profile `generic` names no toolchain checks (no-op).
- Independent review (three lenses, fresh context): [S] blame-history — no regressions, no undone intent, no weakened owner-mode guard; [S] prior-review record — 29 archives read, no contradicted finding (M36's warn-only doctrine deliberately narrowed by D-137's one hard lever; M45's fence-aware slot parser not reached by the header-only scan). [O] diff-bug — 14 ranked findings, triaged:
  - F1 `/milestone-review` and `/hotfix` have no guest arm though prose describes guest review/hotfix behavior → follow-up: review handoff is M185 (planned, in scope); `/hotfix` guest arm → new candidate row. The README/rulebook sentences are the ones AC5/AC6 mandate.
  - F2 pathspec commit (`git commit -m x cairn/f`) passes the guest deny while the docs enumerate misses as exhaustive → fix now: docstring lists the pathspec miss (reachable only while cairn/ is tracked, which F5's check now FAILs); CHANGELOG and rulebook enumerate by pointer + the new miss.
  - F3 mode reader degrades to owner on a lowercase key, `#Collaboration`, or a BOM → fix now: key matched case-insensitively, file opened `utf-8-sig`; 3 subtests. Invalid UTF-8 still reads owner (rejected: no observed instance; the validator's `profile valid` reads the same file and would surface the file itself).
  - F4 worktree/submodule: `.git` is a file, exclude lives in the common dir → fix now: validator resolves `git rev-parse --git-path info/exclude` (literal path as no-git fallback); cairn-init §1/§3 name the resolution; worktree test (PASS with the common-dir line, FAIL without).
  - F5 exclude line does nothing for tracked files (owner→guest switch) → fix now: guest scaffold arm FAILs while `git ls-files -- cairn` lists anything, naming `git rm -r --cached cairn`; tracked and untracked tests.
  - F6 guest R-package tarball carries `cairn/` (implement-time open concern) → follow-up: candidate row.
  - F7 AC2 test mirrors the hook's loop → fix now: independent sentinel assertion ("Never implement code on the default branch").
  - F8 unreadable template → empty routing body claimed present → fix now: the part names the unreadable template path and points at the rulebook; test.
  - F9 deny remedy says "unstage" for the `-am` case → fix now: wording names dropping `-a` and `git rm --cached`.
  - F10 header-region fence asymmetry → reject: a PROFILE.md header region carries no fence in any shipped template or adopter; no observed instance.
  - F11 owner test asserts absence only → reject: `test_owner_nudge_keeps_the_owner_branch_shape` is the positive control on the same fixture.
  - F12 `abspath` vs `realpath` for the template path → reject: follows `cairn_scripts.py`'s precedent; per-file symlink installs are not a supported layout.
  - F13 two extra git subprocesses per guest commit → reject: the deny must read paths on every branch; sub-second.
  - F14 exclude spellings limited to four → reject: init writes the canonical form; the FAIL message names it.
  - Return floor: no finding demonstrates an acceptance criterion failing; no status change. After fixes: scripts 391 / hooks 141 tests, both exit 0; `cairn_validate` passes; AC1–AC3 fixture script re-run green.
- conversation: PR #191 — empty read (0 reviews, 0 comments, 0 unresolved threads).
