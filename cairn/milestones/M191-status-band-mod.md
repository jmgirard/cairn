# M191: Milestone status band, a Claude Code mod inside the cairn plugin

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, GP2, GP3
- **Resolves:** —
- **Surface tier:** user-facing — every session that loads the cairn plugin loads the mod
- **Branch/PR:** —

## Goal

Ship a Claude Code mod inside the cairn plugin that draws the active milestone, its phase, and its task progress above the prompt.

## Scope

**In:**
- A hooks module at `hooks/status/register.tsx`, with its state contract and `*.test.ts` files beside it. A new `modules` key in `hooks/hooks.json` names it, beside the classic command hooks.
- A TypeScript reader for `cairn/ROADMAP.md` rows and for the `## Tasks` checkboxes of a milestone file.
- A band above the prompt that refreshes at the end of each turn.
- Shared fixtures under `hooks/status/fixtures/`. A `scripts/tests` case holds the Python helpers to the same fixtures.
- This repo's `cairn/PROFILE.md` verify slot gains the two `claude plugin` checks as gating checks (D-143).
- README and CHANGELOG entries.

**Out:**
- A roadmap pane, clickable next-command actions, and tests on the `vscode` and `mobile` surfaces → candidate row "Status mod follow-ons".
- A toolchain profile for repos that build plugins or mods → M192.
- A change of this repo's declared profile from `generic` → candidate row "cairn's own profile".
- A separate opt-in plugin → the fallback that T1 stops for, if an older Claude Code refuses the mixed hooks file.

## Acceptance criteria

- [ ] AC1: Take a session whose working directory, or its nearest parent, holds `cairn/ROADMAP.md` (the walk that `find_cairn_root` in `hooks/cairn_common.py` does), with one or more `in-progress` or `review` rows. The mod draws a band above the prompt with one line per such row, in ROADMAP order. Each line gives the id and title from the row, the phase (`implement` for `in-progress`, `review` for `review`), and the checked and total task counts. The counts are what `_AC_ITEM` over `_section_body(text, "Tasks")` in `scripts/cairn_validate.py` counts: any indent, `x` or `X` as checked, and no checkboxes outside `## Tasks`. If the row's milestone file is missing, the line says `no milestone file` in place of the counts. Shown by `claude plugin test` cases that mount the band on both `terminal` and `desktop`. The fixtures vary status, rows per status, zero tasks, nested tasks, a capital `X`, checked criteria boxes above a later H2, a missing milestone file, and a session started in a subdirectory.
- [ ] AC2: The band draws nothing, and the render hook completes without throwing, in two cases. The first is a session with no `cairn/ROADMAP.md` at or above its working directory. The second is a cairn repo with no `in-progress` or `review` row. Shown by `claude plugin test` cases on both surfaces for both fixtures.
- [ ] AC3: The band follows the session's edits. A task in an active milestone file gets checked, or a ROADMAP row moves from `planned` to `in-progress`, from `in-progress` to `review`, or out of both statuses. After the next turn ends, the band shows the new state. Shown by `claude plugin test` cases that assert the band at a first turn end, edit a copy of a fixture, and assert the band again at a second turn end.
- [ ] AC4: For every fixture directory under `hooks/status/fixtures/`, the mod's reader returns the milestone ids, statuses, and task counts that the fixture's `expected.json` states. The no-ROADMAP fixture expects an empty result, and the missing-file fixture expects no counts. A `scripts/tests` case asserts that `cairn_scripts.rows`, with `_AC_ITEM` over `_section_body(text, "Tasks")`, matches the `expected.json` of each fixture in the same way.
- [ ] AC5: Adding the mod keeps cairn's guards working. The `hooks` key of `hooks/hooks.json` is unchanged from the default branch at branch cut, compared as parsed JSON. `claude plugin validate .claude-plugin/plugin.json --json` reports success with zero errors. In one live desktop session in this repo that loads the plugin with the module, the merge guard denies `gh pr merge 99999 --squash` with its own reason text, and the session start carries the tracking context that `session_context` injects.
- [ ] AC6: README states the minimum Claude Code version that the mod needs and cites the release note or post that sets it. README also states what an older Claude Code does with the cairn plugin, as T1 observed it, and what the band shows in the AC1 and AC2 states.

## Coverage

- AC1 → T2, T3, T4
- AC2 → T4
- AC3 → T4
- AC4 → T2, T3
- AC5 → T1, T5
- AC6 → T1, T6

## Tasks

- [ ] T1: Run a spike before any shipped code. Load a minimal module beside the classic hooks, with `--plugin-dir` or the dev-mods hot reload. Record these facts in the work log:
  - That the band draws on desktop.
  - The base that `$.fs` resolves paths against.
  - The event that marks the end of a turn, in a session and in `claude plugin test`.
  - That `claude plugin test` runs here.
  - The location of the `claude` binary in a desktop shell, which does not have it on the PATH. One observed location is `~/Library/Application Support/Claude/claude-code/<ver>/<hash>/claude.app/Contents/MacOS/claude`.
  - The version floor, from the release note or https://claude.dev/blog/getting-started-with-claude-code-mods/. The post states 2.1.287, and this session ran mods on 2.1.286.

  Load the mixed `hooks/hooks.json` with the older binary at `~/Library/Application Support/Claude/claude-code-vm/2.1.284/claude`, and record whether the classic guards still run. If an older binary refuses the file or drops the guards, stop and take the amendment gate. The proposed fallback is a separate opt-in plugin.
- [ ] T2: Write fixtures under `hooks/status/fixtures/<case>/`, each with a `cairn/ROADMAP.md`, milestone files, and an `expected.json`. Cover every axis that AC1 and AC2 name, and add a copy of this repo's `cairn/ROADMAP.md` at branch cut. Write the `scripts/tests` agreement case over every fixture directory (AC4). Show it red first against one wrong `expected.json`.
- [ ] T3: Write the TypeScript reader: the ROADMAP row parse, the `## Tasks` section bounds, the checkbox count, and the upward root walk. Add `*.test.ts` cases over every fixture (AC4).
- [ ] T4: Build the band: `ui.render` on `AbovePrompt`, its `$.state` contract in `types/index.d.ts` (named by `plugin.json`), and the refresh at the end of each turn. Add the surface cases for AC1–AC3, looped over `['terminal', 'desktop']`.
- [ ] T5: Wire it in. Add the `modules` key to `hooks/hooks.json` and the `types` field to `.claude-plugin/plugin.json`. Run the AC5 parsed-JSON comparison of the `hooks` key and `claude plugin validate .claude-plugin/plugin.json --json`. Add `claude plugin validate .claude-plugin/plugin.json` and `claude plugin test .` to the `cairn/PROFILE.md` verify slot as gating checks, with the note on where the binary lives (D-143). Run the AC5 live desktop session.
- [ ] T6: Write the README section from T1's observations (AC6) and a CHANGELOG `Unreleased` entry. Take one live desktop look at the band in this repo during this milestone's own implement phase.

## Work log

- 2026-10-01: created by /milestone-plan, from the operator's request to build Claude Code mods for cairn (https://claude.dev/blog/getting-started-with-claude-code-mods/).
- 2026-10-01: criteria audit, full mode, two fresh Opus readers. The draft drew 14 findings and the gate-revised text drew 17. Each had one clear fix and was fixed at the gate. None was posed as a question.
- 2026-10-01: plan gate chose shipping the mod inside the cairn plugin over a separate opt-in plugin in cairn's marketplace, because the operator is cairn's primary user and wants the band in every session. Falsified by a Claude Code version (older, or with mods off) that refuses the mixed hooks file or drops the classic guards.
- 2026-10-01: plan gate chose a band above the prompt over a status-line entry or a band plus a roadmap pane, because it shows one line per active milestone with no new command. Falsified by the band crowding the prompt or going unread in use.
- 2026-10-01: plan gate chose gating `claude plugin` checks over hand-run checks, because a broken mod otherwise ships unseen in every session. Falsified by the `claude` binary being unavailable where the gating suites run.
- 2026-10-01: plan chose a TypeScript reader held to `cairn_scripts` on shared fixtures over running `scripts/cairn_status.py` through `$.process.run`. The module API exposes no plugin root to find the script, and the run needs python3 at draw time. Falsified by the mod API exposing its plugin root.

## Decisions
