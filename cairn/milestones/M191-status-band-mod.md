# M191: Milestone status band, a Claude Code mod inside the cairn plugin

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, GP2, GP3
- **Resolves:** —
- **Surface tier:** user-facing — every session that loads the cairn plugin loads the mod
- **Branch/PR:** m191-status-band-mod

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

- [ ] AC1: Take a session whose working directory, or its nearest parent, holds `cairn/ROADMAP.md` (the walk that `find_cairn_root` in `hooks/cairn_common.py` does), with one or more `in-progress` or `review` rows. The mod draws a band above the prompt with one line per such row, in ROADMAP order. Each line gives the id and title from the row, the phase (`implement` for `in-progress`, `review` for `review`), and the checked and total task counts. The counts are what `_AC_ITEM` over `_section_body(text, "Tasks")` in `scripts/cairn_validate.py` counts: any indent, `x` or `X` as checked, and no checkboxes outside `## Tasks`. If the row's milestone file is missing, the line says `no milestone file` in place of the counts. Shown by `claude plugin test` cases that mount the band on both `terminal` and `desktop`. The fixtures vary status, rows per status, zero tasks, nested tasks, a capital `X`, checked criteria boxes above a later H2, a missing milestone file, and a session started in a subdirectory. Also shown by one live desktop session in this repo that loads the plugin from its working tree, where the band shows this milestone's line with the task counts its milestone file has at that moment.
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

- [x] T1: Run a spike before any shipped code. Load a minimal module beside the classic hooks, with `--plugin-dir` or the dev-mods hot reload. Record these facts in the work log:
  - That the band draws on desktop.
  - The base that `$.fs` resolves paths against.
  - The event that marks the end of a turn, in a session and in `claude plugin test`.
  - That `claude plugin test` runs here.
  - The location of the `claude` binary in a desktop shell, which does not have it on the PATH. One observed location is `~/Library/Application Support/Claude/claude-code/<ver>/<hash>/claude.app/Contents/MacOS/claude`.
  - The version floor, from the release note or https://claude.dev/blog/getting-started-with-claude-code-mods/. The post states 2.1.287, and this session ran mods on 2.1.286.

  Load the mixed `hooks/hooks.json` with the older binary at `~/Library/Application Support/Claude/claude-code-vm/2.1.284/claude`, and record whether the classic guards still run. If an older binary refuses the file or drops the guards, stop and take the amendment gate. The proposed fallback is a separate opt-in plugin.
- [x] T2: Write fixtures under `hooks/status/fixtures/<case>/`, each with a `cairn/ROADMAP.md`, milestone files, and an `expected.json`. Cover every axis that AC1 and AC2 name, plus a checkbox under the H2 after `## Tasks`, and start the subdirectory case two levels below the root. Add a copy of this repo's `cairn/ROADMAP.md` at branch cut. A `*.test.ts` cannot read files. So generate `hooks/status/fixtures.gen.ts` from the directories, and add a `scripts/tests` case that fails when the module differs from a fresh generation. Write the `scripts/tests` agreement case over every fixture directory (AC4). Show it red first against one wrong `expected.json`.
- [x] T3: Write the TypeScript reader: the ROADMAP row parse, the `## Tasks` section bounds, the checkbox count, and the upward root walk. Add `*.test.ts` cases over every fixture (AC4).
- [x] T4: Build the band: `ui.render` on `AbovePrompt`, its `$.state` contract in `types/index.d.ts` (named by `plugin.json`), and the refresh at the end of each turn. The tests answer the shipped mod's `$.session.cwd`, `$.fs.stat` and `$.fs.read` calls from a copy of each fixture, each answer wrapped as `{ value }`. Add the surface cases for AC1–AC3, looped over `['terminal', 'desktop']`, with one AC3 case per named edit.
- [ ] T5: Wire it in. Add the `modules` key to `hooks/hooks.json` and the `types` field to `.claude-plugin/plugin.json`. Run the AC5 parsed-JSON comparison of the `hooks` key and `claude plugin validate .claude-plugin/plugin.json --json`. Add `claude plugin validate .claude-plugin/plugin.json` and `claude plugin test .` to the `cairn/PROFILE.md` verify slot as gating checks, with the note on where the binary lives (D-143). Run the AC5 live desktop session.
- [x] T6: Write the README section from T1's observations (AC6) and a CHANGELOG `Unreleased` entry. Take one live desktop look at the band in this repo during this milestone's own implement phase. Then check a task, end the turn, and see the count change.

## Work log

- 2026-10-01: created by /milestone-plan, from the operator's request to build Claude Code mods for cairn (https://claude.dev/blog/getting-started-with-claude-code-mods/).
- 2026-10-01: criteria audit, full mode, two fresh Opus readers. The draft drew 14 findings and the gate-revised text drew 17. Each had one clear fix and was fixed at the gate. None was posed as a question.
- 2026-10-01: plan gate chose shipping the mod inside the cairn plugin over a separate opt-in plugin in cairn's marketplace, because the operator is cairn's primary user and wants the band in every session. Falsified by a Claude Code version (older, or with mods off) that refuses the mixed hooks file or drops the classic guards.
- 2026-10-01: plan gate chose a band above the prompt over a status-line entry or a band plus a roadmap pane, because it shows one line per active milestone with no new command. Falsified by the band crowding the prompt or going unread in use.
- 2026-10-01: plan gate chose gating `claude plugin` checks over hand-run checks, because a broken mod otherwise ships unseen in every session. Falsified by the `claude` binary being unavailable where the gating suites run.
- 2026-10-01: plan chose a TypeScript reader held to `cairn_scripts` on shared fixtures over running `scripts/cairn_status.py` through `$.process.run`. The module API exposes no plugin root to find the script, and the run needs python3 at draw time. Falsified by the mod API exposing its plugin root.
- 2026-10-01: implement started on branch `m191-status-band-mod`, cut from main at 5b5ec19.
- 2026-10-01: T1 spike on 2.1.286. `claude plugin validate` and `claude plugin test` run here, from `~/Library/Application Support/Claude/claude-code/2.1.286/f2326db61802/claude.app/Contents/MacOS/claude`. `$.fs` resolves a relative path against the session working directory, which is the plugin folder in a test. `turn.complete` marks a turn end, and a test raises it with `$.turn.complete`.
- 2026-10-01: T1 spike: a test or an inline plugin can answer `$.fs`, `$.session.cwd`, `$.session.root` and `$.process.run` calls. The plugin under `claude plugin test` still gets "no implementation" from each. The `$.store`, `$.clock` and `$.env` mocks answer.
- 2026-10-01: T1 version floor: the post states "Claude Code 2.1.287 or later". The plan's `claude-code-vm/2.1.284/claude` is a Linux binary. The macOS 2.1.284 binary under `claude-code/2.1.284/4819fdb9b264/` validates the mixed `hooks.json` and lists the module's hooks. The auto-mode classifier refused its headless guard run because the run starts a nested agent, so the operator runs it.
- 2026-10-01: the TypeScript-reader falsifier fired, because `$.plugin.root` exists on 2.1.286. The gate kept the TypeScript reader: a test cannot answer `$.process.run` either, and the Python route needs python3 at every turn end.
- re-audit: AC1 (full) — four findings. A "because" clause bound the test instrument, and AC2 and AC3 lacked the same wording. Both were fixed. The live look reaches only the repo root, and the gate kept it so. Two loaded copies of the plugin cannot occur here, because `~/.claude/skills/cairn` links to this working tree.
- 2026-10-01: amendment (gate): the "Shown by" clauses of AC1, AC2 and AC3 now name hooks built by the shipped factory over a fixture file source. AC1 adds one live desktop look. The live look does not reach the subdirectory walk, the missing-file read, or a re-read after an edit through the real `$.fs` source. T6 checks the re-read by hand.
- re-audit: AC1 (full) — root-walk wording, which file a row names, no fixture checkbox below `## Tasks`, and a one-level subdirectory. Second line for AC1, so no further rewording. The fixes went to T2: a checkbox under the next H2 and a two-level subdirectory. The parenthetical `find_cairn_root` and AC4's `cairn_scripts.rows` already pin the walk and the `File/Archive` path.
- re-audit: AC2 (full) — nothing.
- re-audit: AC3 (full) — two findings. One case per named edit went to T4. No case re-reads through the real `$.fs` source, which is logged as a gap above, and T6 checks it by hand.
- 2026-10-01: T2 done. Seven fixtures, the generator `hooks/status/gen_fixtures.py`, and `scripts/tests/test_status_fixtures.py`. A planted wrong count in `mixed/expected.json` (M010 checked 4) turned the agreement case red on that fixture, then the file was restored. Scripts 394 OK, hooks 174 OK.
- 2026-10-01: minor amendment: the `modules` key moved from T5 to T3, because `claude plugin test` refuses to run with no module named. T3 ships a no-op `register` until T4.
- 2026-10-01: T3 done. `hooks/status/reader.ts` and `reader.test.ts`, 13 cases pass under `claude plugin test`. A planted `[x]`-only checked pattern failed `mixed`, `subdirectory` and the detail case, then the file was restored. The Write tool turned ` ` escapes into literal characters, so the line-break pattern builds them from character codes. Scripts 394 OK, hooks 174 OK, `claude plugin validate` passed with one warning about the root CLAUDE.md.
- 2026-10-01: correction of the second T1 spike line. A test can answer a plugin's `$.fs` and `$.session` calls. A plain answer must go back as a result object, `{ value }`, and the spike returned bare values, which the engine skipped. Observed on 2.1.286 when the engine reported "returned something that is not a result object", then confirmed for `fs.exists` and `session.cwd`.
- 2026-10-01: T4 found that the engine refuses the factory design. `register` must be exported as a literal const function, and `$` goes only to top-level functions in the module's own file.
- 2026-10-01: amendment (gate): on the corrected fact, AC1, AC2 and AC3 return to the plan's "Shown by" wording, and AC1 keeps the one live desktop look. The operator chose this at the mini gate. AC1 had two `re-audit` lines, so no reader ran for it.
- re-audit: AC2 (full) — "both surfaces" points at AC1 only, and no case puts a ROADMAP below the working directory. Second line for AC2, so no rewording. A below-the-directory case was added to the tests.
- re-audit: AC3 (full) — "out of both statuses" can start from `review`, and no surface is named. Second line for AC3, so no rewording. A `review` to `done` case was added, and every AC3 case runs on both surfaces.
- 2026-10-01: T4 done. `hooks/status/register.tsx`, `band.ts`, `types/index.d.ts`, the `types` field in `plugin.json`, and `band.test.tsx`. In the AC2 cases, a probe plugin above the mod draws the mod's `next.trace` outcome. Mod tests 32 pass. Plants turned red where expected: a render throw (AC2 shows `skipped`), no refresh at a turn end (14 cases), and a band that ignores a survey (1 case). Scripts 394 OK, hooks 174 OK, `claude plugin validate` passed with the CLAUDE.md warning.
- 2026-10-01: T5 in part. The `hooks` key of `hooks/hooks.json` equals 5b5ec19's, compared as parsed JSON. `claude plugin validate .claude-plugin/plugin.json --json` reports `"success": true` and no errors. The verify slot in `cairn/PROFILE.md` gates on the two `claude plugin` checks and says where the binary lives. Validate exits 1 on a planted contract error and 0 with warnings only. The live desktop check waits for the session to reload the plugin, which happens at a turn end.
- 2026-10-01: T6 in part. README "The milestone band" and a CHANGELOG `Unreleased` entry. Still owed: the README sentence on older Claude Code, after the operator's 2.1.284 run on a copy of this branch, and the live look.
- 2026-10-01: the operator's 2.1.284 control run stopped at "Not logged in · Please run /login", before any hook ran.
- 2026-10-01: AC5 live, in this desktop session after the turn end that reloaded the plugin from the working tree: `gh pr merge 99999 --squash` was denied with the merge guard's own reason ("Merging to main requires explicit user approval at the review gate …").
- 2026-10-01: AC1 live: the operator saw the band above the prompt in this desktop session, with the line "M191 Milestone status band, a Claude Code mod inside the cairn plugin · implement · 3/6 tasks". The milestone file then had T2, T3 and T4 checked. The operator will log the 2.1.284 binary in and rerun the guard check.
- 2026-10-01: T1 old binary, run by the operator after logging the 2.1.284 binary in. The control run had cairn disabled and no `--plugin-dir`: `gh pr merge 99999 --squash` ran and failed "no git remotes found", no hook denied it, and no cairn context arrived. The run with `--plugin-dir` on a copy of this branch printed "cairn-mixed: hooks module not loaded: hooks modules are not turned on for installed plugins in this process (early access: set CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 …)". The merge guard denied the merge with its own reason, and the session start carried "# cairn tracking context (auto-injected by the cairn plugin)". T1 done. README states this result.
- 2026-10-01: T6 done. After the turn end that followed checking T1, the operator's screenshot of the band read "M191 Milestone status band, a Claude Code mod inside the cairn plugin · implement · 4/6 tasks", up from 3/6. So the shipped `$.fs` source re-reads the milestone file at a turn end.

## Decisions
