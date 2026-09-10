# M184: Guest collaboration mode — local-only tracking

**Status:** done (2026-09-10, PR #191 https://github.com/jmgirard/cairn/pull/191)

**Goal:** A repo the operator does not own can run cairn's plan/implement/review loop with `cairn/` kept local — listed in `.git/info/exclude`, never committed — and nothing written outside `cairn/`.

**Outcome:** A second axis beside the toolchain profile (D-137): `# Collaboration mode: guest` as a header line of `cairn/PROFILE.md`, absent meaning owner. `cairn_common.collaboration_mode(root)` reads it (header region only, key case-insensitive, BOM-tolerant); `cairn_validate`'s `profile valid` FAILs a value outside owner|guest, and its guest `scaffold present` arm requires `cairn/` in git's exclude file (`git rev-parse --git-path info/exclude`, so a worktree reads the common dir), drops the `.gitignore`/`.Rbuildignore` entries, and FAILs while `git ls-files -- cairn` lists anything. The session hook injects the plugin's CLAUDE.md routing template as a `## Collaboration mode` part in guest mode (naming an unreadable template rather than emitting an empty body); the commit guard denies any commit it sees carrying a `cairn/` path on every branch, its nudge naming the `<slug>` branch shape. `/cairn-init` gains the mode chip (recommendation from `viewerPermission`), the exclude write, and five skipped writes; the rulebook gains `## Collaboration mode`; guest arms in `/milestone-plan` step 6, `/milestone-implement` step 4, `/milestone` §2; `/cairn-release` and `/cairn-triage` stop in guest mode; README subsection; changelog entry.

**Decisions:** none milestone-local; the axis and its rejected alternatives are D-137.

**Review:** three-lens fan-out. Blame-history and prior-review lenses clean. Diff-bug lens: 14 findings — 7 fixed at the gate (pathspec-commit miss documented; case/BOM-tolerant mode line; worktree exclude resolution; tracked-`cairn/` check; AC2 sentinel assertion; unreadable-template notice; deny remedy wording), 2 routed to candidate rows (`/hotfix` guest arm; guest-mode R tarball carrying `cairn/`), 5 rejected with reasons. No defect returns. Nothing graduated or retired at hygiene.
