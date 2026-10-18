<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M273: The plan target is the first high-priority row the Candidates list shows

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters read `cairn_next.py`'s output, the pane's Next pill, and press the Plan Button   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m273-plan-target-matches-list, https://github.com/jmgirard/cairn/pull/285   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When the next step is planning, the cairn pane's Next pill and Plan press name the first `[high]` candidate row that the pane's Candidates list draws, and `cairn_next.py` names the row that list would draw with no pull request read.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the M272 review edges where the plan target and the Candidates
list disagree: a dead started token (its milestone `done`, `dropped`, or
gone from the table) no longer hides a row from planning; a live token on a
same-titled sibling hides the row from planning as it hides it from the
list; a `#` token of 16 or more digits is no token, as in the list; the
pane picks its target from the rows it draws, so an open PR body or an open
hotfix PR that hides the first `[high]` row moves planning to the next
drawn `[high]` row. Docs: README, the `## Unreleased` CHANGELOG entry M272
added (rewritten in place), `cairn/DESIGN.md`, the `cairn_next.py`
docstrings, `skills/milestone-review/SKILL.md` step 10's `→ /<skill>
[M<NNN>]` tail, and `skills/milestone/SKILL.md`'s "`cairn_next` reads
status and priority alone".

**Out:** three edges that change what the Candidates list itself reads, in
every reader (`candidate_count`, the pane list, the plan target): a row
under `## Candidates (dropped)`, a row after an unclosed `<!--`, and an
untokened row that a `planned` or `blocked` milestone file quotes → stay in
the candidate row "Plan target edges (M272 review)", narrowed. Reading pull
requests from `cairn_next.py` (it stays read-only with no network) → its
two differences from the pane (every `#` token counts, and an open PR body
hides nothing) are stated in `cairn/DESIGN.md`'s Known issues.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [x] AC1: When `cairn_next.recommend` recommends planning, its `title` is
      the short title of the first candidate row, in ROADMAP order, that
      opens with `[high] `, has a non-empty short title, and whose short
      title no counted token names, else None. A counted token is a
      ` — started M<n>` token whose milestone id, compared by `canon_id`,
      some ROADMAP table row holds as `planned` or `blocked`, leaving out a
      `blocked` row that `blocked()` marks `archived`, or a ` — started #<n>`
      token with 1 to 15 digits; either is followed by the row's end or a
      character that is not an ASCII letter or digit, and it names the short
      title of the candidate row that carries it. `TestNext` in
      `scripts/tests/test_scripts.py` passes a case for each of: an `M`
      token whose id is `done`, `dropped`, or absent from the table (row
      named); an `M` token whose id is `planned`, one whose id is `blocked`,
      and an `M5` token beside a `planned` `M005` row (row passed over); a
      `blocked` row `blocked()` marks `archived` (row named); a row whose
      same-titled sibling carries a counted token (passed over, the next
      `[high]` row named); a `#` token of 15 digits (passed over) and of 16
      digits (row named).
- [x] AC2: `highTitle` and `recommend` in `hooks/status/reader.ts` give the
      `title` AC1 gives: `reader.test.ts` passes the AC1 cases against
      `highTitle`, and `python3 -m unittest scripts.tests.test_status_fixtures`
      and `claude plugin test .` pass with every fixture's expected
      `next.title` regenerated under the AC1 rule.
- [x] AC3: The pane's Next line, and the Plan press on the pane and on the
      band, name the first `[high]` candidate row with a non-empty short
      title that `paneLines`' drawn filter keeps over the pane state and
      root-matched PR read current at that draw or press, and no title when
      the filter keeps no such row. The pick is one function used by all
      three. `claude plugin test .` passes cases of that function where: an
      open PR body names the first `[high]` row (the second is named); a
      `#` token's PR is in the open hotfix list (row passed over); the same
      token's PR is not in the list (row named); a same-titled sibling
      carries a counted `M` token (row passed over); every `[high]` row is
      hidden (no title); plus one Next-line case and one press case each on
      the pane and the band.
- [x] AC4: Every line that `git grep -n -e "started token" -e "unstarted"
      -e "\[high\]"` prints over `README.md`, `CHANGELOG.md`,
      `cairn/DESIGN.md`, `scripts/cairn_next.py`, `hooks/status/*.ts*`,
      `skills/milestone/SKILL.md`, and `skills/milestone-review/SKILL.md`
      at the branch head, and that describes the plan target, states it as
      AC1 gives it for `cairn_next.py` or as AC3 gives it for the pane;
      `git grep -n -e "status and priority alone" -e "The pill and \`Plan\`
      then name no title"` over the same paths prints nothing; and
      `cairn/DESIGN.md`'s Known issues states that `cairn_next.py` counts
      every `#` token and that an open PR body hides nothing from it.
- [x] AC5: The profile's `verify` slot passes on the branch head after T4: both gating
      `python3 -m unittest` suites, `claude plugin validate` on the plugin
      and marketplace manifests, and `claude plugin test .`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4, T6
- AC5 → T5, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: `scripts/cairn_next.py`: cap `STARTED`'s `#` digits at 15;
      `high_title(roadmap, rows, archived)` drops a row whose short title a
      counted token names (the `takenRows` rule, `hooks/status/reader.ts`
      ~666); `recommend` passes the table rows and the archived `blocked`
      ids from `blocked()`. Tests first in `TestNext` (flip the 16-digit
      subtest in `test_plan_passes_over_a_started_high_row`).
- [x] T2: `hooks/status/reader.ts`: `highTitle` over `takenRows`; drop the
      uncapped `STARTED`; `recommend` takes the archived ids; `reader.test.ts`
      cases; regenerate every fixture's expected `next.title` via
      `fixtures.gen.ts` (`high-candidate`'s `— started M900`, absent from its
      table, is now dead: give it a live token so the fixture still passes a
      taken row, and let one fixture's named `[high]` row carry a dead token).
- [x] T3: `hooks/status/pane.ts`: replace `nextTitle` with one pick over
      `state.candidates` under the drawn filter's `startedRefs` test; use it
      in the Next line and in `pressNext` (`register.tsx` ~1117); update the
      M272 AC4 block's "a body names the title" case; add the AC3 cases.
- [x] T4: Docs per Scope In and AC4, each claim read against T1–T3's
      output (derived-claims rule); hand-run `skills/tests` after the two
      skill edits.
- [x] T5: Run the `verify` slot on the code head and record each exit code.
- [x] T6: Review return 1: restate `hooks/status/band.test.tsx:3002`'s plan-title comment by the AC3 pick, re-run the AC4 sweep over the test files too, and re-run `verify`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-17: created by /milestone-plan.
- 2026-10-17: tier check: not run — work named at the question set.
- 2026-10-17: question set: what to work on — "Plan target edges (M272 review)"; run on after planning — yes; runs per model — not a measurement.
- 2026-10-17: surface tier user-facing — `cairn_next.py` output and the pane pill and Plan press are what adopters read and press.
- 2026-10-17: collision check: absorbs the candidate row "Plan target edges (M272 review)" in part (started token appended, three edges stay); extends M272 (done); works under D-165, D-166, D-167 (the tokens and the pane's hide rule), unchanged; D-179/D-180 untouched; D-108's door not engaged (a behavior change, not a conduct rule about verification or records); not the checker-regress shape (a recommender, not a checker of repo-internal artifacts). Inbox: 0 open issues, 0 open PRs.
- 2026-10-17: lessons surfaced: build invisible-character strings from code points (M272); grep old phrasing and own a CHANGELOG task (M112); hand-run `skills/tests` near edited SKILL.md slices (M148); run both gating suites after `scripts/`, `hooks/`, or SKILL.md edits (M56).
- 2026-10-17: plan gate chose the rows the pane's Candidates list draws as the plan target over M272's first `[high]` row with no started token of any kind, because the pill then can neither name a hidden row nor pass over a shown one; falsified by a session where the pill names a row the list hides, or where an operator wants a dead-token row kept out of planning.
- 2026-10-17: plan gate chose for `cairn_next.py` to count every `#` token over reading hotfix PR state with `gh`, because the script is read-only with no network and the fixture parity needs one rule both readers apply without PR reads; falsified by a session where `cairn_next.py` passes over a row whose hotfix PR closed and the operator plans the wrong row.
- 2026-10-17: split: the `## Candidates (dropped)` heading, unclosed `<!--`, and untokened-quoted-row edges change every candidate reader, so they stay in the narrowed row "Plan target edges (M272 review)"; the M272 `## Unreleased` CHANGELOG entry is rewritten in place, since it has not shipped.
- 2026-10-17: criteria audit (full mode, fresh Opus reader) returned 7 findings, all fixed: AC1 names the token's milestone id by `canon_id` and the archived row by `blocked()`'s flag, with a padded-id case; AC2 binds title parity with every fixture regenerated, not a new fixture (`high-candidate`'s M900 token goes dead, T2); AC3 names `paneLines`' drawn filter at draw or press time, one shared pick, an all-hidden case, and one case per surface; AC4 sweeps "started token", "unstarted", and `[high]` over named paths in place of a two-phrase proxy; AC5 runs on the head after T4. No reachability or proportionality finding.
- 2026-10-17: implement started on branch m273-plan-target-matches-list; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-17: T1 done: `taken_titles` and `high_title(roadmap, rows, archived)` in `cairn_next.py`, `STARTED` capped at 15 digits; TestNext gains the dead/live/padded/archived and sibling cases (red before the change, 6 failures); plants (no archived exclusion; raw-id compare) each turned TestNext red, restored.
- 2026-10-17: T2 done: `highTitle` in `reader.ts` reads `takenRows`, the uncapped `STARTED` is gone, `recommend` takes the archived ids; `high-candidate` now has a planned M002 whose `— started M2` hides "Taken row", and "Chosen row" carries a dead `— started M001`; pane tests that assumed every fixture row draws now read a hand-written HIDDEN list.
- 2026-10-17: T3 done: `nextTitle(next, candidates, taken, hotfixes, started)` picks the first drawn `[high]` row with the list's `startedRefs` test, used by the Next line and `pressNext`; the M272 AC4 block's body case now plans "Later high". Implementation choice: kept the name `nextTitle`, since every caller already used it; the pane atom's shape is unchanged, so the `pane-7` tag stays.
- 2026-10-17: verify on the T3 head: scripts 418 OK (21 skipped), hooks 179 OK, both validates exit 0, plugin test 2074 pass 0 fail.
- 2026-10-17: T4 done: README (three paragraphs), the M272 `## Unreleased` CHANGELOG entry rewritten in place, DESIGN.md (two plan-target lines and a Known issues sentence on the PR-read difference), `cairn_next.py` and `reader.ts` doc comments, `skills/milestone/SKILL.md` ("does not read the release window"), and `skills/milestone-review/SKILL.md` step 10's tail; AC4's old-phrase grep prints nothing and each sweep line on the plan target states the new rule; `skills/tests` hand-run 842 OK. The simple-english lint hook reports whole-file counts on README, CHANGELOG, and both skills (all older text); new sentences over its limit were split, older text left as it is.
- 2026-10-17: claim audit: 38 claims read, 4 corrected — hooks/status/reader.ts (`planTitle` → `nextTitle`), scripts/cairn_next.py (`high_title` docstring: the pane's two differences), hooks/status/pane.test.tsx (sibling comment and unused row), README.md and CHANGELOG.md (an archived blocked row's token does not count); the same reader re-read the four and found each true.
- 2026-10-17: after the claim fixes: scripts 418 OK (21 skipped), hooks 179 OK, plugin test 2074 pass 0 fail; manifests unchanged since the T4 validates.
- 2026-10-17: review return 1: AC4 — `hooks/status/band.test.tsx:3002` still describes the plan target as "the fixture's first unstarted `[high]` candidate row" (the M272 rule); the sweep's 97 lines include the test files.
- 2026-10-17: T6 added (minor amendment, review return 1; Coverage AC4 and AC5 gain T6) and done: `band.test.tsx` comment now names the first `[high]` row the fixture's Candidates list shows; "unstarted" grep over the AC4 paths prints nothing; verify: scripts 418 OK (21 skipped), hooks 179 OK, both validates exit 0, plugin test 2074 pass 0 fail.
- 2026-10-17: T5 done: verify on the T4 tree: scripts 418 OK (21 skipped), hooks 179 OK, plugin and marketplace validate exit 0, plugin test 2074 pass 0 fail.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive. -->

Review pass 1, 2026-10-17, branch head 4dd0a5a9 (main 69c8f751 unmoved). PR #285 opened at review start (Copilot round on), Copilot requested on state `none`.

- AC1: `python3 -m unittest -v scripts.tests.test_scripts -k TestNext` — 16 OK; `test_plan_counts_only_a_token_whose_milestone_is_open` holds `done`, `dropped`, absent (M900) named, `planned` and `blocked` with an `M5` token beside an `M005` row passed over, and a `blocked` M006 whose file is archived named; `test_plan_passes_over_a_row_whose_sibling_is_taken` passes over "Shared" and names "Next high"; `test_plan_passes_over_a_started_high_row` passes over the 15-digit `#` token and names the 16-digit one; code: `taken_titles`/`high_title(roadmap, rows, archived)` in `scripts/cairn_next.py`, `STARTED` `#[0-9]{1,15}`. PASS.
- AC2: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` at 4dd0a5a9 — 2074 pass, 0 fail, among them the eight `highTitle names the first [high] row no counted token names (M272, M273)` cases (the AC1 set: dead and live `M` tokens with `M5`/`M005`, the archived id, the sibling, 15 and 16 digits) and "the pane's milestones and next step match expected.json" for all 31 fixtures; `python3 -m unittest scripts.tests.test_status_fixtures` OK, holding `cairn_next.recommend` to every `expected.json`; `high-candidate`'s expected `next.title` "Chosen row" carries a dead `— started M001` and follows a row hidden by `— started M2` (planned M002). PASS.
- AC3: same plugin test run; "the pick passes over each row the list hides and names the first it draws" holds `nextTitle` (the one pick, `hooks/status/pane.ts`, called by the Next line and `pressNext` in `register.tsx`, which the pane and band Plan Buttons share) on: a PR body naming "First high" (names "Second high"), a `#41` token with PR 41 in the hotfix list (passed over) and not in it (named), a counted `M005` token (passed over), every `[high]` row hidden (null), and a non-planning step (null); the Next-line case names the pick and the command alone with no drawn row; "a body naming the row moves planning to the next drawn row on the line and the press" runs the pane press and then the band press, each with `Later high`. PASS.
- AC4: at 4dd0a5a9, the AC4 sweep over the named paths (`hooks/status/*.ts*` takes in the test files and `fixtures.gen.ts`) prints 97 lines. `hooks/status/band.test.tsx:3002` describes the plan target as "the fixture's first unstarted `[high]` candidate row", the M272 rule: `high-candidate`'s "Chosen row" now carries a dead token. The other plan-target lines (README.md:189-193, :233, :303-308; CHANGELOG.md:9-22; cairn/DESIGN.md:181, :299-302; scripts/cairn_next.py:9-11, :148-177; hooks/status/reader.ts:510, :690-697; pane.ts:245-253; register.tsx:1097-1099; the reader and pane test names) state the new rule; the old-phrase grep prints nothing (exit 1); `cairn/DESIGN.md:721-723` states the Known issues sentence. FAIL (one line).
- AC5: verify at 4dd0a5a9 (after T4 and the claim-audit fixes): `scripts/tests` 418 OK (21 skipped), `hooks/tests` 179 OK, `claude plugin validate` plugin.json exit 0 and marketplace.json exit 0, `claude plugin test .` 2074 pass 0 fail. PASS.
- Gate: `cairn_validate.py` exit 0, all checks passed; no principle touched, so no `cairn_impact`; profile gate: verify green (AC5), marketplace validate output has no `version` warning, and `CHANGELOG.md` `## Unreleased` carries the rewritten entry with no milestone number. PASS.

Review pass 2, 2026-10-17, branch head 45440813 (main 69c8f751 unmoved), after review return 1 (T6), pushed to PR #285.

- AC4: at 45440813 the sweep prints 97 lines; `hooks/status/band.test.tsx:3001-3003` now names "the first `[high]` candidate row that the fixture's Candidates list shows"; a grep for "unstarted" and the two old phrases over the AC4 paths prints nothing (exit 1); the other plan-target lines are as pass 1 lists them, unchanged since 4dd0a5a9 but for that comment; `cairn/DESIGN.md:721-723` holds the Known issues sentence. PASS.
- AC1–AC3, AC5: the T6 diff is one comment in `band.test.tsx`; verify at 45440813: scripts 418 OK (21 skipped, TestNext among them), hooks 179 OK, both validates exit 0, `claude plugin test .` 2074 pass 0 fail (the `highTitle`, `nextTitle`, Next-line, press, and 31 fixture next-step cases among them). Pass-1 evidence stands. PASS.
- Gate: `cairn_validate.py` exit 0 at 45440813; profile gate as pass 1. PASS.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: no test sends the open hotfix list through the Next line or `pressNext`, so a caller passing `[]` stays green — fix now (a `#41` token on "Chosen row" with hotfix PR 41 open plans "Later high" on the line, the pane press, and the band press, and with PR 42 open plans "Chosen row"; a planted `[]` in `pressNext` turned the PR-41 case red)
- diff-bug #2: README and CHANGELOG say an `M` token counts only while "its file is not archived", but the readers leave out only a `blocked` row whose file was archived — fix now (both say so)
- diff-bug #3: `types/index.d.ts:58` still calls `next.title` the first unstarted `[high]` row — fix now (names `highTitle` and the pane's own pick)
- diff-bug #4: `high_title`/`highTitle`/`recommend` default to no rows and no archived ids, so a caller that omits them counts no `M` token — reject (no defect: every call site passes both; the defaults serve the token-free unit cases)
- diff-bug #5: the pane's sibling case passes a taken entry by title, with no second same-titled row — reject (false as a gap: `TakenRow` carries only a title, and title keying is the readers' `takenRows`/`taken_titles`, held by their sibling cases)
- diff-bug #6: `cairn_next.py` counting every `#` token has no D-entry, while D-165 counts a `#` token while the hotfix list holds it — reject (planned change: D-165 speaks of the pane, M272 already counted every token in the script, AC1 and the plan-gate line record the choice, DESIGN.md Known issues states it)
- diff-bug #7: a press reads state at press time, so a PR read landing after the draw can plan a row the pill did not show — reject (planned design: M212/M213 press-time reads, M272 review diff-bug #10; AC3 names "at that draw or press")
- diff-bug #8: `_planning_tree` left earlier subtests' files on disk — fix now (each call builds in its own folder; the archived subtest reuses M005 and passes)
- blame-history #1: the script counts every `#` token, where the Goal says it names "the row that list would draw with no pull request read" — reject (planned change: AC1 states the rule and the plan-gate line records it; the Goal's phrase is looser than AC1, said at the merge question)
- blame-history #2: the reader's `next.title` and the pane's `nextTitle` are two picks, the first read only by tests and the fixture parity — reject (planned design: the reader mirrors `cairn_next.py` for parity, DESIGN.md:299-302 says the pane does not use it)
- blame-history #3: a started token written before a row's first `: ` becomes part of the short title and names no row — follow-up (new row "Started token before the colon (M273 review)"; pre-existing since M258)
- blame-history #4: `recommend` now reads blocked milestone files for the archived ids — reject (no defect: `render` already reads them through `blocked()`, a few file reads in a read-only script)
- blame-history #5: the fenced `/milestone-plan <title>` carries a raw title that can hold backticks — reject (false: a fenced block shows backticks as written; the ✎ press passes titles the same way, M242)
- prior-review #1: CHANGELOG.md:14 (102 columns) and README.md:193 (95) run past the wrap, as M272's review fixed — fix now (rewrapped with diff-bug #2's fix)
