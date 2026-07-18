# M73: External-PR intake — /hotfix adopts a PR it did not author

**Status:** done (2026-07-18) · **PR:** https://github.com/jmgirard/cairn/pull/71

**Goal:** give the intake doctrine's "external PRs → review to the hotfix bar"
an entry point: teach `/hotfix` to adopt an existing PR rather than always
create one. Delivers D-043's third part; depends on M72.

**Outcome:** `/hotfix` is bidirectional. Given a PR reference it tier-checks the
contributor's diff, runs `gh pr checkout` rather than cutting `hotfix-<slug>` (that
branch name is exempt from the naming contract, mirrored in the rulebook's git model),
adds the missing regression test — proved by failing on the default branch and passing
on the PR head, fail-before-fix being unreachable once the fix exists — reconciles the
changelog, and reaches M72's approval chip unchanged. `--delete-branch` is dropped for
fork PRs; `description:` now fires on an incoming PR; Intake names `/hotfix` the door.

**Decisions:** no D-entry — M73 executes D-043 as recorded. Implement gate, all
user-selected: inline both forms in the existing steps; fork fallback is
ask-then-re-land-locally; the `commit_guard.py` nudge mirror dropped as unreachable.

**Review:** AC1–AC7 verified fresh; `cairn_validate` exit 0; verify 267/96/72.
Blame-history and prior-PR lenses clean; 5 diff-bug findings all scored sub-80,
of which the user elected to fix three — notably that re-landing an unpushable
fork PR closed a contributor's PR with no approval gate, now chip-gated. F5
(stale DESIGN/README trigger prose) → candidate row.
