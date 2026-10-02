# M192: A claude-plugin toolchain profile for repos that build plugins and mods

- **Status:** in-progress
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

- [ ] AC1: `skills/shared/profiles/claude-plugin.md` defines the seven slots and fits the PROFILE.md line cap. Shown by adding `claude-plugin` to the per-profile loop in `scripts/tests/test_scripts.py`.
- [ ] AC2: The init-detection slot names `.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json` at the repo root as the marker. The verify slot names `claude plugin validate` on each plugin's `.claude-plugin/plugin.json` and on the marketplace file where one exists. Where the repo has `*.test.ts` or `*.test.tsx` files, the verify slot also names `claude plugin test`. The verify slot says where to find the `claude` binary when it is not on the PATH. The release-walk slot bumps `version` where present: in each plugin's `.claude-plugin/plugin.json`, including the one that each marketplace entry's `source` points at, and in each `.claude-plugin/marketplace.json` plugin entry.
- [ ] AC3: Tracking-rules "Toolchain profiles" and each of the three places `/cairn-init` states the inference order use one order. The three places are the selection steps, the no-marker list that decides the project-type chip, and the repair path. In that order, `DESCRIPTION` gives `r-package`, then `pyproject.toml` gives `python`, then a plugin marker gives `claude-plugin`, then a sole `Dockerfile` gives `docker-image`, else `generic`. A repo with a plugin marker and a `Dockerfile` infers `claude-plugin`, and the image-vs-package gate offers `docker-image`. The project-type chip lists the new profile.
- [ ] AC4: Take each file outside `cairn/`, `CHANGELOG.md`, and the three `tests/` trees that `git grep -il 'docker.image'` returns. Every list of the toolchain profiles in such a file also names `claude-plugin`. `git grep -inE '(four|4) (toolchain )?profiles'` outside `cairn/` and `CHANGELOG.md` returns no line.

## Coverage

- AC1 → T1, T2
- AC2 → T1
- AC3 → T3, T6
- AC4 → T4, T5

## Tasks

- [x] T1: Write `skills/shared/profiles/claude-plugin.md` from the `generic` profile's shape and M191's work-log facts (AC2).
- [x] T2: Add `claude-plugin` to the per-profile loop at `scripts/tests/test_scripts.py` (about line 2079), red first with a slot removed.
- [x] T3: Update the inference order in tracking-rules "Toolchain profiles" and at the three `/cairn-init` sites (about lines 109–126 and 321). Add the plugin markers to the no-marker list, and add the new profile to the project-type chip and the image-vs-package gate.
- [ ] T4: Sweep the profile lists that AC4's grep returns: README, `skills/cairn-init/SKILL.md` (about lines 159 and 200), tracking-rules, and the two plugin descriptions. Fix the "four profiles" lines in `skills/tests/test_toolchain_profiles.py` and `skills/tests/test_mutation_harness.py`, and hand-run `skills/tests`.
- [ ] T5: Add a CHANGELOG `Unreleased` entry.
- [ ] T6: In a scratch repo with only `.claude-plugin/plugin.json`, read through `/cairn-init`'s selection steps and record the profile they reach in the work log (AC3).

## Work log

- 2026-10-01: created by /milestone-plan, from the operator's request that cairn support Claude Code mod projects.
- 2026-10-01: criteria audit, full mode, two fresh Opus readers. The draft drew 6 findings and the revised text drew 6. Each had one clear fix and was fixed at the gate. None was posed as a question.
- 2026-10-01: plan gate chose M192 after M191 over two independent milestones, because the profile's verify and release steps are best written after cairn builds one real mod. Falsified by M191 stalling while an adopter needs the profile.
- 2026-10-01: plan chose to rank a language marker above the plugin markers, so a plugin repo with `pyproject.toml` stays `python`. This matches the existing hybrid rule that a repo keeps its language marker. Falsified by an adopter's plugin repo whose language profile misses the `claude plugin` checks it needs.
- 2026-10-01: implement started on branch m192-claude-plugin-profile. Question gate: `/cairn-init` asks the main-deliverable question for a plugin+language repo too, with the language profile recommended. Repair with no user keeps the language marker. The profile asks two greenfield openers, where the plugin is listed and whether it ships a mod.
- 2026-10-01: T1 done. `skills/shared/profiles/claude-plugin.md`, 112 lines, written from observed `claude` 2.1.287 output: marketplace validate warns on an entry `version` that differs from `plugin.json`, and `--strict` fails on the root CLAUDE.md warning.
- 2026-10-01: T2 done. `claude-plugin` added to the shipped-profile loop. With the consistency-gate slot cut it failed "claude-plugin missing consistency-gate", restored it passed. scripts 394 OK, hooks 174 OK, plugin validate passed with warnings, plugin test 47/47.
- 2026-10-01: T3 done. Tracking-rules and the three `/cairn-init` sites state one order with the plugin markers between `python` and `docker-image`. The disambiguation gate now covers any two of language, plugin, and image, recommending the profile the order picks, per the question gate. Verify green as at T2.

## Decisions
