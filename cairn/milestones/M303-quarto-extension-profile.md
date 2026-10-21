# M303: Add a quarto-extension toolchain profile

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — repos that adopt cairn read the profile and its release walk
- **Branch/PR:** m303-quarto-extension-profile

## Goal

cairn ships a quarto-extension toolchain profile whose release walk tags a version that a merge already raised, or raises the version at release time.

## Scope

**In:** a new `skills/shared/profiles/quarto-extension.md` with the seven slots. Its release walk names `version:` in `_extensions/<name>/_extension.yml` as the version marker, and a repo can name more markers that hold the same version. The walk has a tag-only arm for a version that the default branch's tip already carries with no tag, and a release-time arm that raises the version as the generic walk does. With changelog "none", the notes come from git history. A new `scripts/cairn_versions.py` finds where each version starts and which commit set it. Detection by `_extensions/*/_extension.yml` or `_extension.yaml` in the rulebook and `/cairn-init`, with the hybrid gate and the greenfield chip. `/cairn-release` learns the tag-only arm. README, DESIGN, CHANGELOG.

**Out:** the handoff of the tag commands at merge in `/milestone-review` and `/hotfix` → M304 (depends on this milestone). Switching embedpdf and quarto-index to the new profile → the candidate row "Switch Quarto repos to the new profile" (the user's choice at the question set). A second marker such as `embedpdf.lua`'s `add_html_dependency` version is named by each repo in its own slot, so the profile gives it as an example only.

## Acceptance criteria

- [ ] AC1: `skills/shared/profiles/quarto-extension.md` holds exactly the seven slots that `scripts/cairn_validate.py` requires, each non-empty, under the PROFILE.md line cap. The profile tuple in `test_shipped_reference_profiles_are_valid` (`scripts/tests/test_scripts.py`) includes `quarto-extension`, and that test passes.
- [ ] AC2: The profile's `release-walk` slot names `version:` in `_extensions/<name>/_extension.yml` as the version marker and lets a repo name more markers that must hold the same version. When the marker's version at the default branch's tip has no `v<version>` tag, the walk tags the first commit of the unbroken run of tip-ward first-parent commits that carry that version, and `/cairn-release` skips its version decision and changelog consolidation in that arm. Otherwise the walk raises every marker at release time and tags its prep commit. When the `changelog` slot is "none", the release notes are the commit subjects on the default branch since the previous `v*` tag.
- [ ] AC3: `scripts/cairn_versions.py` reads a marker file's `version:` value, quoted or not, along the default branch's first-parent history. It prints the tip's version, the first commit of that version's unbroken run at the tip, and whether a `v<version>` tag exists, annotated or lightweight. With `--changed-by <sha>` it compares the commit with its first parent and prints the version the commit set, or nothing when the version did not change. Commits where the file or its `version:` line is absent are skipped, and only a tip file without the line is an error that names the file. Tests in `scripts/tests/` on a fixture git repo cover: three versions with one tagged, a commit that leaves the version unchanged, a version raised, reverted, and raised again (the last run's start is printed), a quoted value, an annotated and a lightweight tag, early commits without the file, and the tip error.
- [ ] AC4: Run read-only in `/Users/jmgirard/github/embedpdf` on `_extensions/embedpdf/_extension.yml`, the script's run start for each version equals `git rev-parse v<version>^{commit}` for every tag that `git tag -l 'v1.*'` lists there. The run uses the script's history mode with each tag's version, or an equivalent `--at <rev>` option that `cairn_versions.py` documents.
- [ ] AC5: The rulebook's "Toolchain profiles" section and `skills/cairn-init/SKILL.md` select quarto-extension for a repo with `_extensions/*/_extension.yml` or `_extension.yaml` and no `DESCRIPTION`, Python, or plugin marker, ahead of docker-image and generic. The hybrid gate offers it as a deliverable. The greenfield no-marker list names the file, and the greenfield chip's follow-up question offers quarto-extension beside claude-plugin and docker-image. The rulebook says six profiles ship, and the guards in `skills/tests` that pin the profile count and list are updated to six.
- [ ] AC6: README.md, cairn/DESIGN.md, and a CHANGELOG.md Unreleased entry name the profile and its two release arms. `skills/cairn-release/SKILL.md` names the tag-only arm in its steps 1, 2, and 3.
- [ ] AC7: The five `verify` commands in `cairn/PROFILE.md` each exit 0.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T5
- AC7 → T1, T2, T4, T5

## Tasks

- [x] T1: Write `skills/shared/profiles/quarto-extension.md` from `generic.md` and `docker-image.md`: verify (the repo's render of its example document, declared by the repo), consistency-gate (each named marker holds the same version), test-doctrine, release-walk (both arms, notes from git history), init-detection, greenfield-openers, changelog. Add it to the tuple in `test_shipped_reference_profiles_are_valid`.
- [ ] T2: Write `scripts/cairn_versions.py` (stdlib, `git` subprocess, first-parent history) and its tests in `scripts/tests/` per AC3, tests first.
- [ ] T3: Run the script read-only on embedpdf and compare with each `v1.*` tag (AC4). Record the result in the work log.
- [ ] T4: Detection: the rulebook's "Toolchain profiles" order and count, `/cairn-init` selection order, hybrid gate, greenfield marker list and chip follow-up, instantiation list, and repair backfill. Update the `skills/tests` guards that pin five profiles (`test_toolchain_profiles.py`, `test_mutation_harness.py`, and the test in `test_scripts.py`), and hand-run `skills/tests`.
- [ ] T5: `/cairn-release` steps 1 to 3 name the tag-only arm. README, DESIGN (profile count and list, layout list), and a CHANGELOG Unreleased entry.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: milestone — a new toolchain profile, a script, and skill changes.
- 2026-10-20: source: embedpdf (generic profile) raised its version at each merge and shipped 13 untagged versions until its M026 tagged them by hand. quarto-index raises at release time and its tags match. Both are cairn-tracked Quarto extensions.
- 2026-10-20: collision check: extends M047 (release-walk slot), M068 (changelog slot), M070 (docker-image profile, the precedent), and M111 (the `gh release create` handoff). D-050 (release timing) holds for this milestone, whose walk runs only when the user runs `/cairn-release`. D-041 is about r-package versions only. No candidate row overlaps.
- 2026-10-20: inbox sweep: no open issues and no open PRs.
- 2026-10-20: profile plumbing sweep (Haiku Explore): the profile list appears in the rulebook, `/cairn-init` (order, hybrid gate, greenfield chip, instantiation list, repair), README, DESIGN, and the guards; no script or hook infers a profile.
- 2026-10-20: split: this milestone ships the profile, the script, and `/cairn-release`; M304 ships the merge-time handoff and depends on this one. The repo switch is a candidate row.
- 2026-10-20: criteria audit (full mode, Opus reader): 12 findings across M303 and M304, all taken toward the narrower promise. For M303: init-detection is already a required slot, and the tuple test checks slots and the cap only; the tag-only arm fires only for the tip's version, at the start of its unbroken run, and skips `/cairn-release`'s version decision and consolidation; the script skips early commits without the line and handles quoted values and both tag kinds; AC4 covers only `v1.*` tags, since three lightweight `v0.*` tags in embedpdf sit on later commits; detection also accepts `_extension.yaml`, and the five-profile guards are updated; the new prose owes no new guard (D-109).
- 2026-10-20: question set: what happens when a merge raises a Quarto extension's version — the close hands over the commands (M304).
- 2026-10-20: question set: switch embedpdf and quarto-index here — later, per repo, as a candidate row.
- 2026-10-20: plan chose a script for the version history over prose `git log` commands in the walk, because the run start and the tip check are easy to get wrong by hand and a script can be tested; falsified by the script disagreeing with a hand-placed tag in a real repo.
- 2026-10-20: plan chose the start of the tip's unbroken run over the first commit ever carrying the version, because a reverted and re-raised version is released from its last raise; falsified by a repo whose maintainers tag the first raise.
- 2026-10-20: changelog: T5 adds one Unreleased entry for the profile; M304 adds its own entry for the handoff.
- 2026-10-20: implement started on branch m303-quarto-extension-profile. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-20: T1 done. `skills/shared/profiles/quarto-extension.md` (94 lines) has the seven slots. The release walk calls `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_versions.py" <marker file>`, which prints the tip's version, its run `start`, and the tag state (the interface T2 builds). `quarto-extension` joined the tuple in `test_shipped_reference_profiles_are_valid`, which failed with FileNotFoundError before the file and passes after. Verify green (mod tests 2417). The simple-english lint flags the shared header comment and bold-label "When" lines in the new file; the body sentences were rewritten to its limits.
- 2026-10-20: implement chose `quarto render <example document>` as the verify example and left the command to each repo, since extensions keep their fixtures in different places.

## Decisions

## Review
