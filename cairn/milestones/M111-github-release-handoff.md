# M111: GitHub-release handoff command — /cairn-release provides a conditional `gh release create`

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** —

## Goal

`/cairn-release`'s handoff hands the user a ready-to-run `gh release create`
command — provided, never run by cairn — so cutting the GitHub release is one
copy-run step instead of a bare "cut the GitHub release" instruction.

## Scope

**In:** In `/cairn-release`'s step 4 (the universal handoff spine, so every
profile is covered without duplicating into four profile slots), add a provided
`gh release create v<version>` command to the handoff checklist, in a fenced
block per the copy-run rule. It is **conditional**: emitted only when the
`origin` remote is a GitHub remote and `gh` is available; otherwise the step
skips it with no failure. The release-notes body is the just-consolidated
changelog section for the new version, extracted to a notes file passed via
`--notes-file`, so the GitHub release body matches the changelog entry. cairn
**provides but never runs** the command (never-self-submits, unchanged). The
generic profile's `release-walk` slot gains a one-line mention so a reader of
the slot alone knows the GitHub release is part of its walk (parity with the
python/docker slots, which already name it).

**Out:** Executing `gh release create` — cairn hands it off (→ never-self-submits,
unchanged). Rewriting the three non-generic profile slots' existing "cut the
GitHub release" prose — they already name it and are now backed by the step-4
command; left as-is. A provided command for non-GitHub hosts (GitLab, etc.) →
candidate row if ever wanted; this milestone's condition simply skips them.

## Acceptance criteria

- [ ] `skills/cairn-release/SKILL.md` step 4 provides a `gh release create
      v<version>` command in the handoff checklist, in a fenced block, gated on
      the `origin` remote being GitHub and `gh` being available.
- [ ] The provided command's release body is the consolidated changelog section
      for the new version, extracted to a notes file and passed via
      `--notes-file` — the GitHub release body matches the changelog entry.
- [ ] The step states cairn **provides but does not run** the command; the
      command is the user's to run (never-self-submits preserved).
- [ ] The condition is explicit: where the remote is not GitHub or `gh` is
      absent, the step skips the GitHub-release command without failing.
- [ ] `skills/shared/profiles/generic.md`'s `release-walk` slot names the
      GitHub-release handoff in one line, consistent with the python/docker slots.
- [ ] A guard test pins the step-4 prose (conditional · provided-not-run ·
      notes-from-changelog), mutation-registered per repo conventions, reading
      its target via `Path.read_text`; all three verify suites and
      `cairn_validate` are green.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T1
- AC5 → T2
- AC6 → T3, T4

## Tasks

- [ ] T1: Edit `skills/cairn-release/SKILL.md` step 4 — add the conditional
      GitHub-release handoff: a fenced `gh release create v<version> --title
      "<name> <version>" --notes-file <notes> --verify-tag` block, gated on a
      GitHub `origin` + `gh`, body = extracted changelog section, framed as
      provided-not-run.
- [ ] T2: Add a one-line GitHub-release mention to
      `skills/shared/profiles/generic.md`'s `release-walk` slot.
- [ ] T3: Add guard asserts over the step-4 prose (extend
      `skills/tests/test_release_timing.py` or a sibling), mutation-registered,
      `Path.read_text`; after the edit, grep that every adjacent guard's asserted
      substring stays contiguous on one physical line (M104).
- [ ] T4: Run all three verify suites from the repo root + `cairn_validate`;
      confirm green (generic `verify` slot).

## Work log

- 2026-07-23: created by /milestone-plan.

## Decisions

## Review
