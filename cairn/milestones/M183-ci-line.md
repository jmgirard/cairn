# M183: Close blocks say whether the next command waits on CI

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — skill prose every plugin user reads at each phase end
- **Branch/PR:** m183-ci-line · https://github.com/jmgirard/cairn/pull/190

## Goal

Every phase close on a live branch or open PR tells the user, in one plain
sentence, whether the fenced next command waits on CI itself and what they
do meanwhile, so "wait for green or go straight to review?" never needs
guessing.

## Scope

**In:** a mandated **CI line** in the tracking-rules close-block shape for
closes whose unit of work has a branch or an open PR; its implement-end
wording in `/milestone-implement` step 9 (nothing to wait for — no PR yet;
review pushes, opens the PR, and waits on CI itself at the merge step); its
timeout-stop wording at the three sites D-130 names (`/milestone-review`
step 8, `/hotfix` step 6, `/cairn-release` step 3): the current state as read
from the wait's own source, rerunning the named command re-checks and waits
again, waiting for green first is optional.

**Out:** a CI line on merged closes (`/milestone-review` step 10, `/hotfix`
step 7) — the PR is merged, nothing is in flight; declined at the plan gate.
A prose pin for the line in `skills/tests` — declined at the plan gate
(D-128's precedent: the timeout stop's next-command clause is unpinned).
Any change to the wait mechanism itself — D-128 stands.

## Acceptance criteria

- [x] AC1: The tracking-rules close-block paragraph ("Question gates and
      phase closes") lists a **CI line** as a required element of a close
      block whose unit of work has a branch or an open PR: one plain-language
      sentence stating whether the fenced next command waits on CI itself and
      what the user does meanwhile — a bare check state ("CI: running") never
      satisfies it. The sites restating their own line are AC2–AC3's four;
      every other such close inherits the rule by citation.
- [x] AC2: `/milestone-implement` step 9's close-block spec states the
      implement-end CI line: nothing to wait for now — no PR exists yet;
      `/milestone-review` pushes the branch, opens the PR, and waits on CI
      itself at the merge step.
- [x] AC3: Each of the three timeout-stop sites — `/milestone-review` step 8,
      `/hotfix` step 6, `/cairn-release` step 3 — states the timeout CI line:
      the current check state as read from the wait's own source (`gh pr
      checks` for a PR wait; the moved task's fresh output for a local check),
      then that rerunning the named command re-derives that state and waits
      again, so waiting for green first is optional and never required.
- [x] AC4: The `verify` slot is clean (`python3 -m unittest` over
      `scripts/tests` and `hooks/tests`), and the hand-run `skills/tests`
      suite shows no red beyond the pre-existing `test_lesson_graduation`
      failure (`'trimmed M98'`).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4

## Tasks

- [x] T1: tracking-rules "Question gates and phase closes", close-block
      paragraph (`skills/shared/tracking-rules.md:299-303`): add the CI line
      element with its domain clause and the bare-state exclusion; keep the
      status line's "check results, where they exist" — the CI line is what
      disposes of them.
- [x] T2: `/milestone-implement` step 9 (`SKILL.md:187-199`): add the
      implement-end CI line wording to the close-block spec.
- [x] T3: the three timeout stops — `/milestone-review` step 8
      (`SKILL.md:405-416`), `/hotfix` step 6 (`SKILL.md:184-191`),
      `/cairn-release` step 3 (`SKILL.md:74-81`): add the timeout CI line
      wording, each naming its own resume command and its wait's own state
      source.
- [x] T4: run both gating suites from the repo root with explicit exit codes;
      hand-run `skills/tests`; confirm the only red is the pre-existing
      lesson-graduation failure (D-109).

## Work log

- 2026-09-10: created by /milestone-plan.
- 2026-09-10: criteria audit (full mode, fresh [O] reader): AC1 bounded-promise finding repaired (domain scoped to the rulebook paragraph plus four restating sites); AC3 source finding repaired (`/cairn-release` waits on local checks, not `gh pr checks`); AC4 pre-existing red named concretely; no existing pin quotes the changed sentences.
- 2026-09-10: plan gate chose a fact-stating timeout line ("rerun whenever; it re-checks and waits again; green-first optional") over "wait for green, then rerun" because the latter costs a manual GitHub check even when CI lands a minute later; falsified by repeated timeout stops on the same PR in the record after the line ships.
- 2026-09-10: plan gate chose branch-or-open-PR closes only over every close block (merged ones too) because a merged close has nothing in flight; falsified by a user report of wait-uncertainty at a merged close.
- 2026-09-10: question gate skipped — the plan fixes each site's wording, nothing open. T1: CI line element added to the rulebook close-block paragraph (domain clause, bare-state exclusion, four restating sites named); verify green 379/126.
- 2026-09-10: T2: implement-end CI line added to step 9's close-block spec (nothing to wait for; review pushes, opens the PR, waits at merge); verify green.
- 2026-09-10: T3: timeout CI line added at `/milestone-review` step 8, `/hotfix` step 6, `/cairn-release` step 3 — each names its own resume command and its wait's own state source (`gh pr checks` twice, the moved task's output for the release check); verify green.
- 2026-09-10: T4: scripts 379 / hooks 126 green (exit 0 each); skills/tests 661 hand-run — the T1 rewrap first split two pinned close-block sentences across lines (`test_gate_wording.TestPhaseCloseBlock`), rewrapped so each pin sits on one line; only remaining red is the pre-existing `test_lesson_graduation` failure (D-109).
- 2026-09-10: minor amendment (T2): step 9's CI line gains a parenthetical for the return-from-review case, where the header already names a draft PR — the line then says review re-waits on that PR's checks at merge; AC2 text unchanged and still met.
- 2026-09-10: claim audit: 12 claims read, 1 corrected — skills/shared/tracking-rules.md, skills/milestone-implement/SKILL.md, skills/milestone-review/SKILL.md, skills/hotfix/SKILL.md, skills/cairn-release/SKILL.md (the correction's re-read ran in a second fresh [O] reader: SendMessage is disabled in this session, so the same reader could not be continued).
- 2026-09-10: all tasks checked; status → review.
- 2026-09-10: plan gate chose no prose pin over a `skills/tests` guard because D-128 leaves the sibling next-command clause unpinned and the checker is internal; falsified by the CI line drifting out of a site in a later milestone's diff.

## Decisions

## Review

- 2026-09-10: main unmoved since the cut (main = origin/main = merge-base); branch pushed; draft PR #190 opened (`Resolves: —`, no closing lines).
- AC1 ✓ — `skills/shared/tracking-rules.md:299-306` read at HEAD: the close-block paragraph lists the **CI line** for a unit of work with a branch or open PR, as one plain-language sentence on whether the fenced next command waits on CI and what the user does meanwhile; the bare-state exclusion (`"CI: running"`) is present; the four restating sites are named and every other close inherits by citation.
- AC2 ✓ — `skills/milestone-implement/SKILL.md:195-201` read at HEAD: step 9's close-block spec states the implement-end line (nothing to wait for now, no PR yet; `/milestone-review` pushes, opens the PR, waits on CI at the merge step), plus the return-from-review parenthetical logged as a minor amendment.
- AC3 ✓ — grep at HEAD: `/milestone-review` step 8 (`SKILL.md:412-415`) and `/hotfix` step 6 (`SKILL.md:191-195`) each state the current check state as read from fresh `gh pr checks`, then that rerunning their own named command re-derives it and waits again, green-first optional and never required; `/cairn-release` step 3 (`SKILL.md:81-85`) states the same from the moved task's fresh output, naming `/cairn-release`.
- AC4 ✓ — from the repo root: `scripts/tests` 379 tests OK (exit 0); `hooks/tests` 126 tests OK (exit 0); `skills/tests` hand-run 661 tests, the sole red `test_lesson_graduation.TestFamilyActuallyLeft.test_partial_coverage_was_trimmed_not_deleted` (the pre-existing D-109 failure).
- Driving RR: — (projection-vs-outcome no-ops).
- Consistency gate: `cairn_validate.py` all checks passed (exit 0); no principle change (`Principles touched: —`), impact report skipped; profile `generic` names no toolchain checks.
- Independent review (user-facing tier → three lenses): [S] blame-history — no conflicts (D-128/D-130/D-133 read, `test_gate_wording` pins intact); [S] prior-review — no prior-review evidence (archives M170/M172 read; PR-comment probe empty); [O] diff-bug — 10 findings, triaged:
  1. `/hotfix` step 6 line promises the rerun "re-derives that state and waits again", but step 1 routes an *open* PR reference into the adopt-a-PR walk (only `MERGED` has a re-entry) — **follow-up**: pre-existing M172 gap in hotfix's resume route, not introduced here (the wording is AC3's); candidate row at hygiene.
  2. `/cairn-release` line applies the element outside the rulebook's branch-or-open-PR domain and to a local check — **reject**: the rulebook names `/cairn-release` step 3 as a restating site and AC3 names the local source; plan-intentional.
  3. `/cairn-release` has no resume route, so the rerun redoes the walk — **reject**: the line states what happens to the wait; the walk's re-entry cost is the skill's own concern and the prep steps are docs-only.
  4. step 9 parenthetical contradicts its own "no PR exists yet" premise — **fixed now**: parenthetical reworded to replace the whole line ("instead says there is still nothing to wait for now…").
  5. return-from-review status table may show pre-fix check state undisposed — **fixed now**, folded into 4 (the line now names the pre-return head).
  6. rulebook inventories its restating sites — **reject**: AC1 requires naming them; drift falsifier logged at the plan gate.
  7. "disposes of the status line's check results" reads as rationale — **reject**: T1 kept it deliberately; it binds the CI line to the status line's check results.
  8. `/milestone-review` line omits that route (c) re-poses the merge chip before the wait — **reject**: the rerun does wait again; the chip is the route's detail, not the line's.
  9. insertion position pushes "never left armed" from its subject — **reject**: style; the pins read fine.
  10. `/cairn-release` "report results when they arrive" tension — **reject**: pre-existing, not introduced.
- conversation: PR #190 — reviews 0, comments 0, unresolved threads 0 (empty read).

- 2026-09-10: step-7 approval: PR #190 approved for merge.
