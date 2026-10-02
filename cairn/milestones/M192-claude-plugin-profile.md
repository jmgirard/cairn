# M192: A claude-plugin toolchain profile for repos that build plugins and mods

- **Status:** review
- **Priority:** normal
- **Depends on:** M191
- **Driving RR:** —
- **Principles touched:** GP3
- **Resolves:** —
- **Surface tier:** user-facing — adopters' `/cairn-init` and operational skills read the profile
- **Branch/PR:** m192-claude-plugin-profile

## Goal

Add a fifth toolchain profile, `claude-plugin`, so that cairn can track a repo that builds a Claude Code plugin or mod.

## Scope

**In:**
- `skills/shared/profiles/claude-plugin.md` with the seven slots, written from what M191 learned about `claude plugin validate`, `claude plugin test`, and the location of the binary.
- The inference order in tracking-rules "Toolchain profiles" and at each of the three places `/cairn-init` states it.
- The project-type chip and the image-vs-package gate in `/cairn-init`.
- Every file that lists the shipped profiles: README, the descriptions in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, and the hand-run prose guards that count the profiles.
- The per-profile loop in `scripts/tests/test_scripts.py` and a CHANGELOG entry.

**Out:**
- A change of this repo's declared profile from `generic` → candidate row "cairn's own profile".
- A release of the new profile → user-declared, never planned here.

## Acceptance criteria

- [x] AC1: `skills/shared/profiles/claude-plugin.md` defines the seven slots and fits the PROFILE.md line cap. Shown by adding `claude-plugin` to the per-profile loop in `scripts/tests/test_scripts.py`.
- [x] AC2: The init-detection slot names `.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json` at the repo root as the marker. The verify slot names `claude plugin validate` on each plugin's `.claude-plugin/plugin.json` and on the marketplace file where one exists. Where the repo has `*.test.ts` or `*.test.tsx` files, the verify slot also names `claude plugin test`. The verify slot says where to find the `claude` binary when it is not on the PATH. The release-walk slot bumps `version` where present: in each plugin's `.claude-plugin/plugin.json`, including the one that each marketplace entry's `source` points at, and in each `.claude-plugin/marketplace.json` plugin entry.
- [x] AC3: Tracking-rules "Toolchain profiles" and each of the three places `/cairn-init` states the inference order use one order. The three places are the selection steps, the no-marker list that decides the project-type chip, and the repair path. In that order, `DESCRIPTION` gives `r-package`, then `pyproject.toml` gives `python`, then a plugin marker gives `claude-plugin`, then a sole `Dockerfile` gives `docker-image`, else `generic`. A repo with a plugin marker and a `Dockerfile` infers `claude-plugin`, and the image-vs-package gate offers `docker-image`. The project-type chip lists the new profile.
- [x] AC4: Take each file outside `cairn/`, `CHANGELOG.md`, and the three `tests/` trees that `git grep -il 'docker.image'` returns. Every list of the toolchain profiles in such a file also names `claude-plugin`. `git grep -inE '(four|4) (toolchain )?profiles'` outside `cairn/` and `CHANGELOG.md` returns no line.

## Coverage

- AC1 → T1, T2
- AC2 → T1
- AC3 → T3, T6
- AC4 → T4, T5

## Tasks

- [x] T1: Write `skills/shared/profiles/claude-plugin.md` from the `generic` profile's shape and M191's work-log facts (AC2).
- [x] T2: Add `claude-plugin` to the per-profile loop at `scripts/tests/test_scripts.py` (about line 2079), red first with a slot removed.
- [x] T3: Update the inference order in tracking-rules "Toolchain profiles" and at the three `/cairn-init` sites (about lines 109–126 and 321). Add the plugin markers to the no-marker list, and add the new profile to the project-type chip and the image-vs-package gate.
- [x] T4: Sweep the profile lists that AC4's grep returns: README, `skills/cairn-init/SKILL.md` (about lines 159 and 200), tracking-rules, and the two plugin descriptions. Fix the "four profiles" lines in `skills/tests/test_toolchain_profiles.py` and `skills/tests/test_mutation_harness.py`, and hand-run `skills/tests`.
- [x] T5: Add a CHANGELOG `Unreleased` entry.
- [x] T6: In a scratch repo with only `.claude-plugin/plugin.json`, read through `/cairn-init`'s selection steps and record the profile they reach in the work log (AC3).

## Work log

- 2026-10-01: created by /milestone-plan, from the operator's request that cairn support Claude Code mod projects.
- 2026-10-01: criteria audit, full mode, two fresh Opus readers. The draft drew 6 findings and the revised text drew 6. Each had one clear fix and was fixed at the gate. None was posed as a question.
- 2026-10-01: plan gate chose M192 after M191 over two independent milestones, because the profile's verify and release steps are best written after cairn builds one real mod. Falsified by M191 stalling while an adopter needs the profile.
- 2026-10-01: plan chose to rank a language marker above the plugin markers, so a plugin repo with `pyproject.toml` stays `python`. This matches the existing hybrid rule that a repo keeps its language marker. Falsified by an adopter's plugin repo whose language profile misses the `claude plugin` checks it needs.
- 2026-10-01: implement started on branch m192-claude-plugin-profile. Question gate: `/cairn-init` asks the main-deliverable question for a plugin+language repo too, with the language profile recommended. Repair with no user keeps the language marker. The profile asks two greenfield openers, where the plugin is listed and whether it ships a mod.
- 2026-10-01: T1 done. `skills/shared/profiles/claude-plugin.md`, 112 lines, written from observed `claude` 2.1.287 output: marketplace validate warns on an entry `version` that differs from `plugin.json`, and `--strict` fails on the root CLAUDE.md warning.
- 2026-10-01: T2 done. `claude-plugin` added to the shipped-profile loop. With the consistency-gate slot cut it failed "claude-plugin missing consistency-gate", restored it passed. scripts 394 OK, hooks 174 OK, plugin validate passed with warnings, plugin test 47/47.
- 2026-10-01: T3 done. Tracking-rules and the three `/cairn-init` sites state one order with the plugin markers between `python` and `docker-image`. The disambiguation gate now covers any two of language, plugin, and image, recommending the profile the order picks, per the question gate. Verify green as at T2.
- 2026-10-01: T4 done. README, the two plugin descriptions, and `/cairn-init`'s tree and file list name `claude-plugin`. Also fixed: the docker-image detection slot now names the plugin markers. `skills/tests` (hand-run) went from 6 reds and 2 errors to main's 4 reds and 1 error after the label map, the profile loop, and the five-profiles guard and its mutation entry were updated. AC4's second grep returns no line. Verify green.
- 2026-10-01: T5 done. CHANGELOG `Unreleased` → New gains the profile entry, including that a plugin repo with no PROFILE.md now infers `claude-plugin`.
- 2026-10-01: T6 done. Scratch git repo holding only `.claude-plugin/plugin.json`: the seven markers read absent except that one. `/cairn-init`'s selection step passes `DESCRIPTION` and the Python markers and reaches **claude-plugin**. One deliverable's markers, so no disambiguation gate. A marker is present, so not greenfield and no project-type chip. The repair path and tracking-rules reach the same profile. `claude plugin validate` passed there.
- 2026-10-01: delegated the claim audit to one fresh-context Opus reader, read-only. It reported 22 claims, 1 wrong (CHANGELOG said a plugin repo used to infer `generic`, but with a `Dockerfile` it inferred `docker-image`) and 1 holding with a limit (validate's markdown check is shallow). Both were reworded and the same reader re-read them: 2 hold. DESIGN.md's "Four profiles ship" line, outside AC4's grep, was updated to five.
- 2026-10-01: claim audit: 22 claims read, 2 corrected — CHANGELOG.md, skills/shared/profiles/claude-plugin.md
- 2026-10-01: implement complete. scripts 394 OK, hooks 174 OK, plugin validate passed with warnings, plugin test 47/47, cairn_validate all checks passed. `skills/tests` (hand-run, non-gating) 661 with main's 4 reds and 1 error. Status → review.

## Decisions

## Review

- AC1: 2026-10-01, `python3 -m unittest scripts.tests.test_scripts -k test_shipped_reference_profiles_are_valid` OK, with `claude-plugin` in the loop at `scripts/tests/test_scripts.py:2079`. The file has the seven slot headings in order and 113 lines against the PROFILE.md cap of <120. At implement, cutting the consistency-gate slot failed this test with "claude-plugin missing consistency-gate". PASS.
- AC2: 2026-10-01, a slot-scoped read of `claude-plugin.md` found all ten required items. init-detection names both marker files at the repo root. verify names `claude plugin validate` on each plugin's `.claude-plugin/plugin.json` and on `.claude-plugin/marketplace.json`, `claude plugin test` where `*.test.ts` or `*.test.tsx` files exist, and two places to find `claude` off the PATH. release-walk bumps `version` in each plugin manifest, including the one each entry's `source` points at, and in each marketplace entry. Both named paths exist on this machine (`~/.local/bin/claude` → `versions/2.1.287`, the desktop 2.1.286 binary). Both validate commands exit 0 here. PASS.
- AC3: 2026-10-01, a read of tracking-rules "Toolchain profiles" and of `/cairn-init`'s selection step, greenfield marker list, and repair backfill. The three ordered statements give `DESCRIPTION` → r-package, the Python markers → python, a plugin marker → claude-plugin, a sole `Dockerfile` → docker-image, else generic. The greenfield no-marker list includes both plugin markers, and its project-type chip lists "Claude Code plugin". The selection step says a plugin marker beside a `Dockerfile` recommends claude-plugin and offers docker-image. T6's scratch repo with only `plugin.json` reached claude-plugin (work log). PASS.
- AC4: 2026-10-01, `git grep -il 'docker.image'` outside the excluded paths returns six files. The two plugin descriptions and README:14 list "R, Python, Claude Code plugin, Docker image, or generic". `/cairn-init` lists the profile at 109–113 (order), 133 (chip), 166 (tree), 207 (file list), and 328–331 (repair). tracking-rules:531 lists five profiles. `docker-image.md` names only itself and holds no list of profiles. The second grep exits 1 with no line. PASS.
- Consistency gate, 2026-10-01: `cairn_validate` all checks passed (exit 0). No DESIGN principle changed, so `cairn_impact` was skipped. This repo's `generic` profile names no toolchain checks. Verify slot: scripts 394 OK (21 skipped), hooks 174 OK, `claude plugin validate` passed with warnings, `claude plugin test` 47 pass and 0 fail.

Findings (three lenses: diff-bug 13, blame-history 7, prior-review 1):

- R1 (diff-bug 1): the greenfield project-type chip now has five options, but the question tool takes at most four, and the rulebook says the same. A greenfield `/cairn-init` call fails or drops an option. Proposed: fix now. Four options: R package / Python package / Claude Code plugin or Docker image (a second question picks one) / generic.
- R2 (diff-bug 2): `claude plugin test <mod-dir>` names the module's folder, but the command needs the plugin folder whose `hooks/hooks.json` has a `modules` key. The reviewer saw `claude plugin test hooks/status` exit 1 with "no hooks module to load". Proposed: fix now, rename the placeholder `<plugin-dir>` and gloss it.
- R3 (diff-bug 3): `claude plugin test` runs every `*.test.ts(x)` under the folder. A vitest file fails with "cannot import "vitest"", and with no mod the run fails with "no hooks module to load". Proposed: fix now within AC2's wording. Keep the trigger and state both facts, so other TypeScript tests live outside the folder or use another suffix.
- R4 (diff-bug 5, blame-history 4): the CHANGELOG lists the new inference for a plugin repo with no PROFILE.md under New, but it changes existing repos. Proposed: fix now, move it to "Changes that affect existing repos".
- R5 (prior-review 1, blame-history 1): `cairn/DESIGN.md:48` still lists four profiles. AC4's grep leaves out `cairn/`. Proposed: fix now.
- R6 (diff-bug 6): the test-doctrine bullet implies that `claude plugin validate` checks skill markdown. The reviewer saw it pass broken front matter. Proposed: fix now, say only that this markdown owes no test.
- R7 (diff-bug 9): "always draws one" is false in guest mode, which writes no CLAUDE.md. Proposed: fix now, "draws one whenever a CLAUDE.md sits at the plugin root".
- R8 (diff-bug 8): `/cairn-init`'s list of how each profile renders distribution ambition leaves out claude-plugin, and docker-image too. Proposed: fix now, name both openers.
- R9 (diff-bug 13): README:14 breaks the paragraph's wrap. Proposed: fix now, rewrap.
- R10 (diff-bug 4, 7, 10): profile edge cases. The release walk bumps every plugin to one version and one tag, and cannot edit an entry whose `source` is another repo. A plugin with no manifest, or only in a subfolder, is not validated or detected. The commands and paths are POSIX and macOS only. Proposed: follow-up, one candidate row "claude-plugin profile edge cases".
- R11 (diff-bug 11, blame-history 5): the profile leaves 6 lines under the 120-line PROFILE.md cap, and an adopter adding commands can cross it. Proposed: reject. `cairn_validate` names the overrun, and the remedy is the adopter's own compression.
- R12 (diff-bug 12, blame-history 2, 3): no prose guard covers claude-plugin in `/cairn-init` or its verify tokens, and a docstring still says "Dockerfile+language-marker". Proposed: reject. `skills/tests` is hand-run, and this repo owes no new prose guards (PROFILE test-doctrine, D-109).
- R13 (blame-history 4, second half): the repair text "without changing behavior" now looks false. Proposed: reject. The backfill writes exactly what the absent-file inference gives, which is the behavior the sentence means.
- R14 (blame-history 6): `generic.md` and `python.md` do not mention the plugin marker. Proposed: reject. Both remain correct.
- R15 (blame-history 7): the profile does not say that validate skips `types/index.d.ts`. Proposed: reject. The M193 lesson in LESSONS.md holds it.

Triage, 2026-10-01: the user chose the proposed dispositions at the gate. R1–R9 were fixed on the branch. I reproduced R2's "no hooks module to load" on `hooks/status` and on a scratch plugin with no mod before writing the new verify text. R10 became the candidate row "claude-plugin profile edge cases". R11–R15 were rejected for the reasons above. After the fixes: scripts 394 OK, hooks 174 OK, plugin validate passed with warnings, plugin test 47/47, `cairn_validate` all passed, and `skills/tests` showed main's 4 reds and 1 error. The profile is 115 lines.
