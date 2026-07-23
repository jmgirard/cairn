# M111: GitHub-release handoff command — /cairn-release provides a conditional `gh release create`

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m111-github-release-handoff · https://github.com/jmgirard/cairn/pull/111

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

- [x] `skills/cairn-release/SKILL.md` step 4 provides a `gh release create
      v<version>` command in the handoff checklist, in a fenced block, gated on
      the `origin` remote being GitHub and `gh` being available.
- [x] The provided command's release body is the consolidated changelog section
      for the new version, extracted to a notes file and passed via
      `--notes-file` — the GitHub release body matches the changelog entry.
- [x] The step states cairn **provides but does not run** the command; the
      command is the user's to run (never-self-submits preserved).
- [x] The condition is explicit: where the remote is not GitHub or `gh` is
      absent, the step skips the GitHub-release command without failing.
- [x] `skills/shared/profiles/generic.md`'s `release-walk` slot names the
      GitHub-release handoff in one line, consistent with the python/docker slots.
- [x] A guard test pins the step-4 prose (conditional · provided-not-run ·
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

- [x] T1: Edit `skills/cairn-release/SKILL.md` step 4 — add the conditional
      GitHub-release handoff: a fenced `gh release create v<version> --title
      "<name> <version>" --notes-file <notes> --verify-tag` block, gated on a
      GitHub `origin` + `gh`, body = extracted changelog section, framed as
      provided-not-run.
- [x] T2: Add a one-line GitHub-release mention to
      `skills/shared/profiles/generic.md`'s `release-walk` slot.
- [x] T3: Add guard asserts over the step-4 prose (new
      `skills/tests/test_github_release_handoff.py` — a distinct concern from
      D-050 timing), mutation-registered (6 anchors), `Path.read_text`; adjacent
      guards' asserted substrings unaffected (append-only, no reflow) (M104).
- [x] T4: Run all three verify suites from the repo root + `cairn_validate`;
      confirm green (generic `verify` slot).

## Work log

- 2026-07-23: created by /milestone-plan.
- 2026-07-23: implemented T1–T4 on branch m111-github-release-handoff — step-4 conditional gh-release handoff (provided-not-run), generic-profile mention, new mutation-registered guard (6 anchors); suites green (skills 604, scripts 280, hooks), cairn_validate clean; tasks landed as one checkpoint (skill+test+registry interdependent). Status → review.

## Decisions

## Review

**Evidence (fresh, 2026-07-23, branch `m111-github-release-handoff` @ base `8974e7c`):**

- AC1 — `skills/cairn-release/SKILL.md` step 4 carries the "GitHub release
  (conditional)" paragraph + a fenced `gh release create v<version> --title …
  --notes-file … --verify-tag` block, gated on "`origin` … names `github.com`)
  and `gh` is available". Guards `test_command_is_gated_on_github_origin_and_gh`
  PASS.
- AC2 — "whose body is the changelog section you just consolidated" +
  "Extract that section to a notes file and pass it with `--notes-file`".
  Guards `test_release_body_…` + `test_notes_are_passed_by_notes_file_…` PASS.
- AC3 — "cairn provides this command; it never runs it — publishing … is the
  user's action". Guard `test_cairn_provides_but_never_runs_the_command` PASS.
- AC4 — "Where the remote is not GitHub or `gh` is absent, omit this command
  with no failure — the tag alone is the release." Guard
  `test_command_is_skipped_cleanly_off_github` PASS.
- AC5 — `skills/shared/profiles/generic.md` release-walk: "provides a `gh
  release create` command whose body is the new changelog section". Guard
  `test_generic_profile_slot_names_the_handoff` PASS.
- AC6 — `test_github_release_handoff.py` (6 asserts) + 6 REGISTRY entries in
  `test_mutation_harness.py`; mutation harness green proves each anchor reddens
  when blanked. Suites: skills 604, scripts 280, hooks 72 — all OK.
  `cairn_validate` exit 0, no advisories.

**Consistency gate:** `cairn_validate` all checks passed (exit 0). No principle
change (Principles touched: —) → `cairn_impact` skipped. Generic profile names
no toolchain consistency checks → no-op.

**Independent review:** inline (not the mandated fresh-context fan-out — this
session's spawn-control guidance; small prose+test diff). Three lenses:
diff-bug (well-formed; `--verify-tag` a sound default; copy-run fenced block) —
0 findings; blame-history (reinforces never-self-submits; leaves D-050 and "no
registry step" intact) — 0 findings; prior-PR (no archived `## Review` findings
on the touched files reference the handoff; PR-thread probe 0 inline comments)
— no-op. No findings ≥80.

**Sub-threshold (logged, not actioned):** the three non-generic profiles' "cut/
tag the GitHub release" prose is now redundantly backed by the universal
provided command — cosmetic consolidation, scoped `Out`, not a defect.
