# M183: Close blocks say whether the next command waits on CI

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — skill prose every plugin user reads at each phase end
- **Branch/PR:** m183-ci-line

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

- [ ] AC1: The tracking-rules close-block paragraph ("Question gates and
      phase closes") lists a **CI line** as a required element of a close
      block whose unit of work has a branch or an open PR: one plain-language
      sentence stating whether the fenced next command waits on CI itself and
      what the user does meanwhile — a bare check state ("CI: running") never
      satisfies it. The sites restating their own line are AC2–AC3's four;
      every other such close inherits the rule by citation.
- [ ] AC2: `/milestone-implement` step 9's close-block spec states the
      implement-end CI line: nothing to wait for now — no PR exists yet;
      `/milestone-review` pushes the branch, opens the PR, and waits on CI
      itself at the merge step.
- [ ] AC3: Each of the three timeout-stop sites — `/milestone-review` step 8,
      `/hotfix` step 6, `/cairn-release` step 3 — states the timeout CI line:
      the current check state as read from the wait's own source (`gh pr
      checks` for a PR wait; the moved task's fresh output for a local check),
      then that rerunning the named command re-derives that state and waits
      again, so waiting for green first is optional and never required.
- [ ] AC4: The `verify` slot is clean (`python3 -m unittest` over
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
