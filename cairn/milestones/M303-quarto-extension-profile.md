# M303: Add a quarto-extension toolchain profile

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — repos that adopt cairn read the profile and its release walk
- **Branch/PR:** m303-quarto-extension-profile https://github.com/jmgirard/cairn/pull/317

## Goal

cairn ships a quarto-extension toolchain profile whose release walk tags a version that a merge already raised, or raises the version at release time.

## Scope

**In:** a new `skills/shared/profiles/quarto-extension.md` with the seven slots. Its release walk names `version:` in `_extensions/<name>/_extension.yml` as the version marker, and a repo can name more markers that hold the same version. The walk has a tag-only arm for a version that the default branch's tip already carries with no tag, and a release-time arm that raises the version as the generic walk does. With changelog "none", the notes come from git history. A new `scripts/cairn_versions.py` finds where each version starts and which commit set it. Detection by `_extensions/*/_extension.yml` or `_extension.yaml` in the rulebook and `/cairn-init`, with the hybrid gate and the greenfield chip. `/cairn-release` learns the tag-only arm. README, DESIGN, CHANGELOG.

**Out:** the handoff of the tag commands at merge in `/milestone-review` and `/hotfix` → M304 (depends on this milestone). Switching embedpdf and quarto-index to the new profile → the candidate row "Switch Quarto repos to the new profile" (the user's choice at the question set). A second marker such as `embedpdf.lua`'s `add_html_dependency` version is named by each repo in its own slot, so the profile gives it as an example only.

## Acceptance criteria

- [x] AC1: `skills/shared/profiles/quarto-extension.md` holds exactly the seven slots that `scripts/cairn_validate.py` requires, each non-empty, under the PROFILE.md line cap. The profile tuple in `test_shipped_reference_profiles_are_valid` (`scripts/tests/test_scripts.py`) includes `quarto-extension`, and that test passes.
- [x] AC2: The profile's `release-walk` slot names `version:` in `_extensions/<name>/_extension.yml` as the version marker and lets a repo name more markers that must hold the same version. When the marker's version at the default branch's tip has no `v<version>` tag, the walk tags the first commit of the unbroken run of tip-ward first-parent commits that carry that version, and `/cairn-release` skips its version decision and changelog consolidation in that arm. Otherwise the walk raises every marker at release time and tags its prep commit. When the `changelog` slot is "none", the release notes are the commit subjects on the default branch since the previous `v*` tag.
- [x] AC3: `scripts/cairn_versions.py` reads a marker file's `version:` value, quoted or not, along the default branch's first-parent history. It prints the tip's version, the first commit of that version's unbroken run at the tip, and whether a `v<version>` tag exists, annotated or lightweight. With `--changed-by <sha>` it compares the commit with its first parent and prints the version the commit set, or nothing when the version did not change. Commits where the file or its `version:` line is absent are skipped, and only a tip file without the line is an error that names the file. Tests in `scripts/tests/` on a fixture git repo cover: three versions with one tagged, a commit that leaves the version unchanged, a version raised, reverted, and raised again (the last run's start is printed), a quoted value, an annotated and a lightweight tag, early commits without the file, and the tip error.
- [x] AC4: Run read-only in `/Users/jmgirard/github/embedpdf` on `_extensions/embedpdf/_extension.yml`, the script's run start for each version equals `git rev-parse v<version>^{commit}` for every tag that `git tag -l 'v1.*'` lists there. The run uses the script's history mode with each tag's version, or an equivalent `--at <rev>` option that `cairn_versions.py` documents.
- [x] AC5: The rulebook's "Toolchain profiles" section and `skills/cairn-init/SKILL.md` select quarto-extension for a repo with `_extensions/*/_extension.yml` or `_extension.yaml` and no `DESCRIPTION`, Python, or plugin marker, ahead of docker-image and generic. The hybrid gate offers it as a deliverable. The greenfield no-marker list names the file, and the greenfield chip's follow-up question offers quarto-extension beside claude-plugin and docker-image. The rulebook says six profiles ship, and the guards in `skills/tests` that pin the profile count and list are updated to six.
- [x] AC6: README.md, cairn/DESIGN.md, and a CHANGELOG.md Unreleased entry name the profile and its two release arms. `skills/cairn-release/SKILL.md` names the tag-only arm in its steps 1, 2, and 3.
- [x] AC7: The five `verify` commands in `cairn/PROFILE.md` each exit 0.

## Coverage

- AC1 → T1
- AC2 → T1, T6
- AC3 → T2, T6
- AC4 → T3
- AC5 → T4, T6
- AC6 → T5, T6
- AC7 → T1, T2, T4, T5, T6

## Tasks

- [x] T1: Write `skills/shared/profiles/quarto-extension.md` from `generic.md` and `docker-image.md`: verify (the repo's render of its example document, declared by the repo), consistency-gate (each named marker holds the same version), test-doctrine, release-walk (both arms, notes from git history), init-detection, greenfield-openers, changelog. Add it to the tuple in `test_shipped_reference_profiles_are_valid`.
- [x] T2: Write `scripts/cairn_versions.py` (stdlib, `git` subprocess, first-parent history) and its tests in `scripts/tests/` per AC3, tests first.
- [x] T3: Run the script read-only on embedpdf and compare with each `v1.*` tag (AC4). Record the result in the work log.
- [x] T4: Detection: the rulebook's "Toolchain profiles" order and count, `/cairn-init` selection order, hybrid gate, greenfield marker list and chip follow-up, instantiation list, and repair backfill. Update the `skills/tests` guards that pin five profiles (`test_toolchain_profiles.py`, `test_mutation_harness.py`, and the test in `test_scripts.py`), and hand-run `skills/tests`.
- [x] T5: `/cairn-release` steps 1 to 3 name the tag-only arm. README, DESIGN (profile count and list, layout list), and a CHANGELOG Unreleased entry.
- [ ] T6: Review return 1: fix the Review section's fix-now list. Script: refuse a shallow clone, check the version's shape, strip a BOM, make the first-parent test discriminate. Walk: fetch tags and read the default branch, confirm the version and `start` with the user in step 1, check the other markers at `start`, take notes and the claim-read from the version's changelog section, name the previous-tag command and the unset `${CLAUDE_PLUGIN_ROOT}` rule, add the feature-series clause. Detection text, CHANGELOG, DESIGN, comments, and guards per the list.

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
- 2026-10-20: T2 done. `scripts/cairn_versions.py FILE [--root DIR] [--at REV | --changed-by SHA]` reads the first-parent chain with one `git cat-file --batch` call and prints `version`, `start`, and `tag present|absent`, or for `--changed-by` the version the commit set. 11 tests in `scripts/tests/test_versions.py` on a built git repo, all failing before the script. A planted defect (the run loop skipping over a break) failed only the revert test. `argparse` is outside the scripts' stdlib allowlist (`TestStdlibOnly`), so the arguments are parsed by hand. Scripts suite 439 OK; the other verify checks green.
- 2026-10-20: T3 done. Read-only in embedpdf (main level with origin): for each of the 16 tags `git tag -l 'v1.*'` lists (v1.0.0 to v1.2.9), `cairn_versions.py _extensions/embedpdf/_extension.yml --at <tag>` printed a `start` equal to `git rev-parse <tag>^{commit}` and a `version` equal to the tag's, 0 mismatches. The tip reads 1.2.9, start a68951d, tag present. (The plan's audit counted 18 such tags; the listing has 16.)
- 2026-10-20: T4 done. The rulebook says six profiles ship and infers quarto-extension after claude-plugin and before docker-image. `/cairn-init` selects it from `_extension.yml` or `_extension.yaml`, names it as a hybrid deliverable, lists both spellings as greenfield markers, offers it in the chip's follow-up, and names it in the tree comment, the instantiation list, the release-intent opener, and the repair backfill. Guards: the five-profile class became `TestRulebookNamesSixProfiles`, both profile tuples gained `quarto-extension`, a new `test_init_selects_quarto_extension` is registered in the mutation harness, and the positioning guard's `LABELS` gained "Quarto extension". That guard requires the label in README ¶1 and both manifest descriptions, so those three lists name it (one scripted replace, an exception to the Edit-tool rule). skills/tests 930 OK; verify green.
- 2026-10-20: T5 done. `/cairn-release` gains a "Tag-only arm (quarto-extension)" paragraph before step 1, and steps 1 and 2 say the arm skips them; step 3 gains a quarto-extension bullet. DESIGN names six profiles with the new one, lists it in the profiles directory, and adds `cairn_versions` to the scripts layer. CHANGELOG Unreleased "New" gains the profile entry. All five verify checks, skills/tests (930), and `cairn_validate` green.
- 2026-10-20: claim audit: 90 claims read, 7 corrected — skills/shared/profiles/quarto-extension.md, skills/cairn-release/SKILL.md, CHANGELOG.md, scripts/cairn_versions.py. Quarto 1.10 installs from the branch named `main`, not the default branch. An untagged tip version is "unreleased" (a first release is one too), and first-release notes drop `<previous tag>..`. The tag-only arm tags only the tip's version. A repo with no PROFILE.md now infers the profile. A `Dockerfile` sends the repo to the disambiguation gate. The script names a missing file and a bad `--root` (two new tests, 13 in all), and an unquoted value ends at a space or `#`. The same reader re-read all seven: each holds.
- 2026-10-20: implement done. All five tasks are checked, verify is green (scripts 441, mod tests 2417, skills/tests 930), and the status is review.
- 2026-10-20: after the handoff note, a README row (the "Prepare a release" row in the task table) gained the quarto-extension release arms, which AC6 asks for; it was added after the claim audit, so the review lenses read it first.
- 2026-10-20: review return 1: load-bearing defects in `/cairn-release`'s tag-only arm and the version reader. The arm tags with no confirmation (a first run tags a placeholder). A shallow or tag-less clone gives a wrong `start` and re-tags a released version. The walk reads `HEAD`, not the default branch. With a declared changelog it has no notes source and skips the claim-read. The fix-now list in the Review section (diff-bug #1-4, #7-13; blame-history #1-6; prior-review #1, #3, #4; ripple #2, #3, #5-8) goes with it.

## Decisions

## Review

Review head `c9880c1f`, synced with `origin/main` (0 behind). PR #317 opened at review start (Copilot round on).

- AC1: `_profile_slots` on `skills/shared/profiles/quarto-extension.md` returns exactly the seven `_REQUIRED_SLOTS` (changelog, consistency-gate, greenfield-openers, init-detection, release-walk, test-doctrine, verify), none empty, no extra slot, 99 lines (PROFILE.md cap <120). `test_shipped_reference_profiles_are_valid`, whose tuple holds `quarto-extension`, passes.
- AC2: the `release-walk` slot read on the head names `version:` in `_extensions/<name>/_extension.yml` as the marker and lets a repo name more markers that hold the same version. Its tag-only arm fires when the tip's version has no `v<version>` tag and tags `<start>`, the first commit of the version's unbroken first-parent run, with no bump and no prep commit. `/cairn-release` skips steps 1 and 2 in that arm (its "Tag-only arm (quarto-extension)" paragraph and the step 1 and 2 headers). The release-time arm raises every named marker and tags the prep commit. With changelog "none", the notes are `git log --first-parent --format='- %s' <previous tag>..<tagged commit>`. No guard asserts this prose (D-109), so the evidence is this read.
- AC3: `python3 -m unittest scripts.tests.test_versions -v` on the head ran 13 tests, all OK. They cover three versions with one tagged (and `--at`), an unchanged commit (`--changed-by` prints nothing), raise, revert, and raise again (the start is the last raise), quoted values (double, single with a `#` comment), an annotated and a lightweight tag, early commits without the file and without the line, a merged side branch on first-parent history, the tip errors for a missing line and a missing file (exit 2, naming the file), a bad root, an unknown revision, and `--at` with `--changed-by`. T2's planted defect failed the revert test.
- AC4: read-only in embedpdf (main at `4acfb5a`), for each of the 16 tags `git tag -l 'v1.*'` lists, `cairn_versions.py _extensions/embedpdf/_extension.yml --at <tag>` printed a `start` equal to `git rev-parse <tag>^{commit}`: 0 mismatches.
- AC5: `skills/shared/tracking-rules.md:692-697` says six profiles ship and infers quarto-extension from `_extensions/*/_extension.yml` (or `.yaml`) after the plugin marker and before docker-image and generic. `skills/cairn-init/SKILL.md` selects it at :111-114 in the same place, names "a Quarto extension (an extension marker)" as a hybrid deliverable, lists both spellings in the greenfield no-marker list (:134), offers it in the chip's follow-up (:139), and names it in the tree comment (:172), the instantiation list (:220), the release opener (:228), and the repair backfill (:347). The guards are updated: `TestRulebookNamesSixProfiles` asserts "Six profiles ship" (registered in the mutation harness), both profile tuples hold `quarto-extension`, `test_init_selects_quarto_extension` is new and registered, and the positioning `LABELS` holds "Quarto extension". `skills/tests` ran 930 OK on the head.
- AC6: README.md :14 names "Quarto extension" in the profile list and :757 (the "Prepare a release" row) names both arms. cairn/DESIGN.md :14 names the profile with both arms, :67 lists it, and :716 adds `cairn_versions`. CHANGELOG.md :147 (Unreleased, New) names the profile and both arms. `skills/cairn-release/SKILL.md` names the tag-only arm before step 1 (:53), in step 1 (:60), in step 2 (:83), and in step 3 (:102).
- AC7: on `c9880c1f`: `scripts/tests` OK (441 run, 21 skipped), `hooks/tests` OK (193), plugin validate exit 0, marketplace validate exit 0, mod test exit 0 (2417 pass).
- Consistency gate: `cairn_validate.py` all checks passed; no principle changed, so `cairn_impact` was skipped. Verify green (AC7). The marketplace validate output has no `plugins[N].version` warning. The CHANGELOG Unreleased entry covers the change and names no milestone.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: in the tag-only arm with a declared changelog, step 2 is skipped, so the release notes have no section and Unreleased entries roll into a later version — fix now (floor return)
- diff-bug #2: a shallow or `--no-tags` clone gives a wrong `start` and `tag absent`, so the arm re-tags a released version, in the shallow case on the wrong commit — fix now (floor return)
- diff-bug #3: the walk reads `HEAD`, and nothing requires the default branch to be checked out — fix now (floor return)
- diff-bug #4: the tag-only arm never checks the other named markers at `start` — fix now
- diff-bug #5: a `.yml` to `.yaml` rename ends the run, and `--changed-by` on the rename reports a version — follow-up, row "Handle version reader edge cases"
- diff-bug #6: a `v<version>` tag on a different commit counts as present with no warning — follow-up, row "Handle version reader edge cases"
- diff-bug #7: the first-parent test passes without `--first-parent`, and two asserts are always true — fix now
- diff-bug #8: on a first run with no tags, the arm tags a placeholder version without asking — fix now (floor return)
- diff-bug #9: the arm skips step 2's claim-read, and step 4 still explains "why the version was chosen" — fix now
- diff-bug #10: `docker-image.md` and `claude-plugin.md` init-detection omit the extension marker — fix now
- diff-bug #11: the notes range ends at `start` and no command finds the previous tag — fix now for the command; reject (false) for the range, since commits after `start` belong to the next version
- diff-bug #12: `${CLAUDE_PLUGIN_ROOT}` lands in an adopter's PROFILE.md with no unset-variable rule — fix now
- diff-bug #13: a UTF-8 BOM before a first-line `version:` gives the tip error — fix now
- diff-bug #14: a multi-line quoted scalar with `version:` at column 0 matches — follow-up, row "Handle version reader edge cases"
- diff-bug #15: the script reads every first-parent blob — reject (false as a defect): embedpdf's whole history reads in well under a second
- diff-bug #16: `--root=DIR` is a usage error — reject (false): the docstring promises only `--root DIR`
- diff-bug #17: the greenfield chip's third option is long but within the four-option limit — reject (false as a defect)
- blame-history #1: the tag-only arm skips the D-136 claim-read that M182 put before a tag — fix now, with diff-bug #9
- blame-history #2: tag-only releases have no notes source with a declared changelog — fix now, with diff-bug #1
- blame-history #3: a repo with a `Dockerfile` and an extension marker and no PROFILE.md now infers quarto-extension, and the CHANGELOG files this under New, not under changes that affect existing repos — fix now
- blame-history #4: the arm drops the one confirmation before a tag, and README :757 says you run the tag step yourself — fix now for the confirmation (with diff-bug #8); reject (false) for README, since the arm makes the tag locally and you push it, as in the generic walk
- blame-history #5: the arm is decided by a step-3 read but gates steps 1 and 2 — fix now
- blame-history #6: `docker-image.md` init-detection is stale — fix now, with diff-bug #10
- blame-history #7: the new selection guards are hand-run only — reject (planned change): D-109
- prior-review #1: the profile's consistency-gate lacks the feature-series clause the other four carry (PR #286), and `test_feature_series.py` leaves it out — fix now, with ROADMAP's parked row "Series entry after a release" saying "the four profiles"
- prior-review #2: three pins of the rulebook's size (761 lines) are stale — reject (false): they are a dated baseline that `/milestone` reports growth from
- prior-review #3: only one of `test_init_selects_quarto_extension`'s asserts is registered in the mutation harness (PRs #243, #260, #283) — fix now
- prior-review #4: the marker's `version:` value reaches `git tag` with no shape check (PRs #241, #243) — fix now
- ripple #1: `docker-image.md` init-detection — fix now, with diff-bug #10
- ripple #2: `cairn/DESIGN.md` Known issue says only the generic walk names the release-prep commit — fix now
- ripple #3: `cairn/DESIGN.md` says the scripts exit 2 outside a cairn repo — fix now for DESIGN; reject (false) for `scripts/cairn_scripts.py:11`, which describes the scripts that import it, and `cairn_versions` does not
- ripple #4: the feature-series "four profiles" text — fix now, with prior-review #1
- ripple #5: `claude-plugin.md` init-detection omits the extension marker — fix now, with diff-bug #10
- ripple #6: `/cairn-release` step 4's per-profile handoff list has no quarto entry — fix now
- ripple #7: `/cairn-release`'s description names no quarto arm — fix now
- ripple #8: `cairn_validate.py:823` and `hooks/session_context.py:114` say the skills infer the profile from DESCRIPTION — fix now
