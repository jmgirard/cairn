<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M273: The plan target is the first high-priority row the Candidates list shows

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters read `cairn_next.py`'s output, the pane's Next pill, and press the Plan Button   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m273-plan-target-matches-list   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: When `cairn_next.recommend` recommends planning, its `title` is
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
- [ ] AC2: `highTitle` and `recommend` in `hooks/status/reader.ts` give the
      `title` AC1 gives: `reader.test.ts` passes the AC1 cases against
      `highTitle`, and `python3 -m unittest scripts.tests.test_status_fixtures`
      and `claude plugin test .` pass with every fixture's expected
      `next.title` regenerated under the AC1 rule.
- [ ] AC3: The pane's Next line, and the Plan press on the pane and on the
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
- [ ] AC4: Every line that `git grep -n -e "started token" -e "unstarted"
      -e "\[high\]"` prints over `README.md`, `CHANGELOG.md`,
      `cairn/DESIGN.md`, `scripts/cairn_next.py`, `hooks/status/*.ts*`,
      `skills/milestone/SKILL.md`, and `skills/milestone-review/SKILL.md`
      at the branch head, and that describes the plan target, states it as
      AC1 gives it for `cairn_next.py` or as AC3 gives it for the pane;
      `git grep -n -e "status and priority alone" -e "The pill and \`Plan\`
      then name no title"` over the same paths prints nothing; and
      `cairn/DESIGN.md`'s Known issues states that `cairn_next.py` counts
      every `#` token and that an open PR body hides nothing from it.
- [ ] AC5: The profile's `verify` slot passes on the branch head after T4: both gating
      `python3 -m unittest` suites, `claude plugin validate` on the plugin
      and marketplace manifests, and `claude plugin test .`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

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
- 2026-10-17: T5 done: verify on the T4 tree: scripts 418 OK (21 skipped), hooks 179 OK, plugin and marketplace validate exit 0, plugin test 2074 pass 0 fail.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->
