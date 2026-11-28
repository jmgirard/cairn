# M111: GitHub-release handoff command — /cairn-release provides a conditional `gh release create`

**Status:** done (2026-07-23, PR #111 https://github.com/jmgirard/cairn/pull/111)

**Goal:** `/cairn-release`'s handoff hands the user a ready-to-run `gh release
create` command — provided, never run by cairn.

**Outcome:** step 4 (the universal handoff spine — every profile, no four-slot
duplication) gained a fenced `gh release create v<version> … --notes-file …
--verify-tag` block, gated on a GitHub `origin` + `gh` and omitted cleanly
otherwise; the body is the just-consolidated changelog section. cairn provides
but never runs it (never-self-submits). The generic profile's release-walk
gained a one-line parity mention. New guard `test_github_release_handoff.py`
(6 asserts) + 6 mutation-registry entries.

**Decisions:** none — provided-not-run and the GitHub+`gh` condition were
settled at the plan gate (conduct, no D-entry); no IP/GP changed.

**Review:** 6/6 ACs fresh + PASS; suites green (skills 604, scripts 280, hooks
72), cairn_validate clean. Inline 3-lens review (session spawn-control
guidance) — no findings ≥80; one sub-threshold cosmetic note logged. No lessons
captured or retired.
