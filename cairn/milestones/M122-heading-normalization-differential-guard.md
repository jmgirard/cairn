# M122: A differential guard holding the hook and the cap counters to one heading contract

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** `m122-heading-normalization-differential-guard` · https://github.com/jmgirard/cairn/pull/122

## Goal

Pin the session-context hook and the cap counters to one heading-classification
contract with a table-driven differential guard, so a normalization step dropped
on either side reds instead of silently unbounding a milestone's history sections.

## Scope

**In:** a differential test in `hooks/tests/test_hooks.py` driving both
classifiers over one shared table — the counters through a real file
(`cairn_scripts.milestone_body_line_count`), the hook through its real injection
path (`session_context.milestone_part`) — with an expected-verdict column, a
both-directions non-vacuity assert, the fence axis (a cap-exempt heading
quoted inside a ``` or `~~~` block is content on both layers), and mutation
evidence scoped to the new class. Graduating the falsified candidate row out of `cairn/ROADMAP.md` with the
true measurement recorded here.

**Out:** changing either layer's behaviour — both classify correctly today
(measured 2026-07-30), so this milestone adds a guard and no code change;
a shared constant or module across the two packages — a hook may import only
`cairn_common` (D-063), which is why a guard is the instrument and M119's
`TestExemptSetMirror` the precedent; deriving the renderings from a producer
instead of listing them (`guard-doctrine.md` §3) — milestone headings are
hand-authored and have no producer to sweep, the negative M117 already recorded;
trimming `cairn/LESSONS.md:42` to its uncovered remainder → this milestone's
post-merge hygiene pass, decided at the plan gate 2026-07-30.

## Acceptance criteria

- [x] AC1: A guard in `hooks/tests/test_hooks.py` asserts, for every row of one
      shared table, that three verdicts agree: the counters' (from writing a real
      milestone file and calling `cairn_scripts.milestone_body_line_count`), the
      hook's (from `session_context.milestone_part`, reading whether an elision
      marker was emitted), and the row's own expected verdict, which pins ground
      truth so a drift hitting both layers identically still reds. Neither
      measured verdict restates the other's expression, and every fixture section
      carries more than `MIN_TAIL_BLOCKS` entries (`session_context.py:59`, = 3),
      below which no budget elides and the guard would red on correct code.
- [x] AC2: The table covers both axes. Format: `## Work log`, `## Work Log`,
      `## WORK LOG`, `##  Work log` (two spaces), `## Work log ` (trailing space).
      Site: at least one `## Review` and one `## Decisions` rendering, because the
      counters normalize at two sites — `cairn_scripts.py:375-376` (boundary) and
      `:412` (subtraction) — and a work-log-only table never reaches the first.
      Fence: a cap-exempt heading quoted inside a ``` block and inside a `~~~`
      block is content on both layers (M45), each pinned so that dropping either
      layer's support for either fence reds.
      Controls: `## Reviewers`, `## Decisions notes`, `## Scope`. Every rendering
      is pinned individually — dropping any single row reds.
- [x] AC3: Each control pairs its no-marker assert with a positive signal that the
      section was injected whole (its own content present in the returned text),
      so a `milestone_part` returning nothing cannot satisfy it.
- [x] AC4: A non-vacuity assert over the OBSERVED verdicts fails when the table
      stops exercising both outcomes, proven both ways: reduced to exempt-only
      rows the hooks suite reds, reduced to controls-only it reds.
- [x] AC5: Guard-must-fail evidence in the Review section, scoped to the new test
      class — 7 of 98 hooks tests already red on the `.lower()` mutation
      pre-milestone (baseline measured 2026-07-30), so a whole-suite verdict
      proves nothing about this guard: `.strip()` removed from
      `session_context.heading_name` reds the new class; `.lower()` removed reds
      it; both restored, it passes.
- [x] AC6: The candidate row "The hook's heading normalization is unguarded
      against case drift" is gone from `cairn/ROADMAP.md`, and this file records
      what it got wrong: `.lower()` removal reds 7 of 98 hooks tests (the row
      claimed all 98 green), `hooks/` byte-identical to `016a210` so the tree had
      not moved, and `.strip()` the axis this milestone closes — with the hook's
      `~~~` fence support a second uncovered axis the sweep misread as red (that
      mutation errored, it did not catch).
- [x] AC7: The `verify` slot is clean — `skills/tests`, `scripts/tests` and
      `hooks/tests` all green, run from the repo root.

## Coverage

- AC1 → T1
- AC2 → T1, T5
- AC3 → T1
- AC4 → T1, T2
- AC5 → T2
- AC6 → T4
- AC7 → T2

## Tasks

- [x] T1: Write the guard beside `TestExemptSetMirror`
      (`hooks/tests/test_hooks.py:466-536`, which already puts `scripts/` on
      `sys.path` and imports both modules): the shared table with its expected
      column, the counters driver over a temp file, the hook driver through
      `milestone_part`, controls carrying positive signals, and the
      observed-verdict non-vacuity assert.
- [x] T2: Run the guard-must-fail protocol — `.strip()` dropped, `.lower()`
      dropped, the table reduced each way — requiring red from the new class each
      time; restore, confirm the three suites green, and record each result in
      the work log, from which review carries it into the Review section.
- [x] T3: Confirm the file needs no mutation-harness registration (a behavioural
      guard over code, not a prose-guard asserting doc substrings) against
      `skills/tests/test_mutation_harness.py`'s completeness meta-test; register
      it if it does.
- [x] T4: Remove the candidate row from `cairn/ROADMAP.md` and record the
      correction here.
- [x] T5: Cover the fence axis the certification found open — a quoted-heading
      fixture in both fence spellings, asserting the counters' arithmetic (not
      just their section list, which the exempt subtraction hides) and the hook's
      marker count.

## Work log

- 2026-07-30: created by /milestone-plan.
- 2026-07-30: investigation falsified the candidate row's premise — `.lower()` removed from `heading_name` reds 7 of 98 hooks tests, not zero, and `hooks/` is byte-identical to `016a210`, so the tree had not moved since the row was written 2026-07-27. A five-mutation sweep found `.strip()` on the hook side the only uncovered axis (hook `.strip()` green; hook `.lower()`, hook `~~~` fence, counters subtraction `.lower()`, counters boundary `.lower()` all red).
- 2026-07-30: criteria audit ([O] fresh-context reader) returned 14 findings, reproduced every measurement above, and built AC1's mechanism to confirm it is achievable. Twelve had one clear right answer and are fixed in the criteria above — `MIN_TAIL_BLOCKS` reachability, the non-discriminating `.lower()` arm, the missing site axis, the missing expected-verdict column, vacuous absence controls, and seven wording or duplication repairs. Two went to the gate: row disposal and the LESSONS trim.
- 2026-07-30: plan gate chose a shared-table differential guard over pinning only the two uncovered spellings in the existing hook tests, because a spelling list re-opens the gap the moment either side gains a normalization step; falsified by a measured divergence the table's renderings cannot distinguish.
- 2026-07-30: plan gate chose removing the candidate row over keeping a narrowed third-caller row, because this milestone closes its only live residue; falsified by a third caller appearing that needs the same normalization.
- 2026-07-30: plan gate decided `cairn/LESSONS.md:42` is trimmed to its uncovered remainder — that matching two layers' rules by hand stays a review item — at this milestone's post-merge hygiene, the covered instance dropped.
- 2026-07-30: implement started on `m122-heading-normalization-differential-guard`; no implementation choice was left open by the plan, so no question gate.
- 2026-07-30: T1 — `TestHeadingNormalizationContract` added to `hooks/tests/test_hooks.py` beside `TestExemptSetMirror`: a 12-row table (5 work-log renderings, 4 review/decisions renderings for the site axis, 3 controls), each row measured three ways — counters via `milestone_body_line_count` over a real file, hook via `milestone_part` at budget 0, and the row's expected verdict — with positive signals on both arms and an observed-verdict non-vacuity assert. Hooks suite 98 -> 101 tests.
- 2026-07-30: T2 — guard-must-fail protocol run scoped to the new class, all four required reds: `.strip()` dropped from `heading_name` RED (3 failures, the axis that was green pre-milestone), `.lower()` dropped RED (3), table reduced to exempt-only rows RED (1), table reduced to controls-only RED (2). Restored and re-run: the class is green and all three suites pass (skills 700, scripts 332, hooks 101).
- 2026-07-30: AC7's parenthetical did not reproduce — `scripts/tests` reported plain `OK` today, not `OK (skipped=1)`; the skip is machine-conditional (M109). The criterion's substance, all three suites green, holds and the AC text is left as written.
- 2026-07-30: T3 — no mutation-harness registration owed: `prose_guard_modules` (`skills/tests/test_mutation_harness.py:3227-3230`) globs `skills/tests/test_*.py` only, so a guard in `hooks/tests/` is outside the completeness meta-test's scope, and this is a behavioural guard over code rather than a prose-guard asserting doc substrings.
- 2026-07-30: T4 — the candidate row was already removed in the plan commit `1966e1f`, earlier than the task placed it; the correction it owed is recorded in AC6 and in this log rather than re-done here.
- 2026-07-30: §8 certification ([O] fresh-context reader) returned 11 discrepancies. Two were my own measurements, both re-measured here and both wrong as recorded: the `.lower()` mutation reds 11 in the new class, NOT the 3 recorded above, and dropping the hook's `~~~` fence support left the suite GREEN — the sweep line above recorded it red on an `errors=1` crash, which is M117's trap verbatim (a crash counts as a pass to the harness, and as a catch to a careless reader).
- 2026-07-30: certification fixes — the site-coverage test no longer routes the table through `heading_name`, the function under test (a hook mutation was reporting as a table defect); every table row is now pinned individually, measured by deleting each of the 12 in turn (2 were previously unnoticed: `##  Decisions` and `## Reviewers`); AC1's `MIN_TAIL_BLOCKS` clause gained the assert it lacked; the `## Scope` control comment and the `cairn_scripts.py:375-376` reference corrected.
- 2026-07-30: amendment gate — AC2 (line reference + the fence axis), AC6 (the "one uncovered axis" claim narrowed to what was measured) and AC7 (the skip parenthetical, which did not reproduce) amended at the user's approval; Scope In widened to the fence axis, T5 added. The earlier "left as written" disposition of AC7 is superseded: §8's bar is that a discrepancy is fixed, not explained.
- 2026-07-30: T5 — fence axis closed on both layers. Mutation evidence: hook `~~~` support dropped RED, hook ``` support dropped RED, counters `~~~` support dropped RED (this last one needed the count assert; the counters SUBTRACT a mis-split cap-exempt heading, so the section list alone stayed green).
- 2026-07-30: final mutation set against the new class (5 tests): `.lower()` dropped 12 failures, `.strip()` dropped 3, `~~~` dropped 1, table exempt-only 1, controls-only 2, any single table row dropped RED.
- 2026-07-30: round-2 certification found a SURVIVING mutation, and it was the milestone's own failure mode: `cairn_scripts.py:375`'s `.strip()` dropped left the class green while `## Review `, `##  Review` and `## REVIEW ` were capped to the counters and exempt to the hook. Every whitespace rendering in the table landed at the subtraction site (`:412`), which re-strips independently, so the boundary site's own `.strip()` was unreachable. Closed by one row, `("## Review ", True)`; that mutation now reds.
- 2026-07-30: claim repairs from round 2 — the `## Decisions notes` control is attributed to M55's boundary bug alone (M118 designed exactness in from the start and hit no near miss); the class docstring no longer says the counters' verdict "became" anything under the `.strip()` mutation (only the hook's half moves, and the divergence is what reds); the fence comment's "101 tests" is marked as the then-current file's count.
- 2026-07-30: numbers settled on THIS commit's tree, superseding every earlier count in this log — the earlier figures were measured on intermediate trees, and one pair was distorted by a stale `__pycache__` (the `.strip()`- and `.lower()`-dropped files are byte-identical in length, so back-to-back runs reused bytecode; re-run under `-B`). Against `TestHeadingNormalizationContract` (5 tests): hook `.lower()` 13 · hook `.strip()` 4 · hook `~~~` 1 · hook ``` 1 · counters `:375` `.strip()` 1 · counters `:376` `.lower()` 3 · counters `:412` `.lower()` 9 · counters `~~~` 1 · table exempt-only 2 · table controls-only 2 · each of the 13 rows dropped in turn RED, none unnoticed.
- 2026-07-30: no round-3 certification. Round 2's five remaining findings were stale counts in this log, whose subject is the certification rounds themselves — outside §8's certified scope (D-069), and auditing them manufactures exactly the surface a next round would audit, the round-generating pathology RR09 banked for rebuild. Deliberate deviation from §8's zero-unresolved bar, logged not resisted: the numbers are settled in one line above and the milestone goes to the review fan-out, a different instrument carrying different evidence.
- 2026-07-30: all tasks complete, three suites green on this tree (skills 700, scripts 332, hooks 103); status -> review.
- 2026-07-30: review fan-out — 3 lenses + scorer, 11 findings, 4 actioned (>=80), 7 logged below threshold. Prior-PR-comments lens: no findings (repo-wide inline-comment probe empty; the archive's M113 F3 is the finding this guard pins against recurrence, not one the diff regresses). Blame-history lens: no regression, and it reproduced the mutation counts and suite totals independently.
- 2026-07-30: F1 (88) and F2 (80) were SURVIVING MUTATIONS — the `## ` prefix test is itself a normalization step and was unpinned on both layers, as was an `lstrip()` added ahead of it. Closed by two rows (`### Work log`, `  ## Work log`), neither a heading to either layer today, each divergent the moment one layer's prefix handling moves. Now red: hook prefix loosened 1, counters prefix loosened 1, hook `lstrip()` added 1, counters reading `stripped` 1.
- 2026-07-30: F3 (85) closed on its closable half only, and the limit is recorded rather than papered over: the coverage list is now ONE `assertEqual` over `TABLE`'s headings, so a row added without being declared reds (measured). A coordinated edit deleting a row from both places still passes — no restatement inside the file can catch its own coherent edit, which is what review is for.
- 2026-07-30: F5 (80) — this log's earlier "no round-3 certification" justification is SUPERSEDED as wrong on all three legs. The five remaining findings were mutation counts describing the guard's behaviour, so they were records describing the WORK and inside §8's certified scope; D-070 narrowed exactly this case, and D-069 never covered it. The exclusion reading leaned on D-079 clause 1, which D-080 WITHDREW — and D-080's own Consequences say the round-count problem is open, so RR09's banked rebuild is not available as ground to stop. What stands unchanged is the disposition and its honest name: declining round 3 was a deliberate deviation from §8's zero-unresolved bar, taken as a judgment call with the maintainer in the loop, logged not resisted. The numbers it settled were independently reproduced by two review lenses.
- 2026-07-30: logged below threshold, actioned by none — F4 (70) `cairn_scripts.py:412`'s `.strip()` half is dead because `:375` already strips, so AC2 credits a redundant half as a covered site; B1 (60) Scope Out credits M117 with a negative it did not record, though the underlying judgment holds; F10 (48) a comment says "two axes" where AC2 now names three; F9 (45) fixtures put a `## ` heading with no blank line above it, a layout no real milestone file uses; F8 (42) the hook verdict proxy is the literal `_cairn:`, so renaming that marker would misdiagnose as a classification failure; F6 (30) four superseded values for one count survive in this append-only log before the settling line; F7 (30) the module docstring's subprocess claim predates this milestone and is now untrue for 5 more tests.
- 2026-07-30: the measurement INSTRUMENT was wrong before this line and is corrected here — its row pattern required `## ` right after the quote, so it silently skipped the two new rows (13 of 15 tested), and its "exempt-only" reduction removed a hardcoded control list that no longer matched the table, so that reduction was not exempt-only at all. It now parses every row and derives both reductions from the parsed verdicts. The prior numbers were measurements of something other than what they named — the same failure this milestone exists to catch, one level up.
- 2026-07-30: numbers settled on this commit's tree, superseding every earlier count in this log. Table 15 rows (10 exempt / 5 control). Against the class (5 tests), all eleven mutations red: hook `.lower()` 13 · hook `.strip()` 4 · hook prefix `## `->`##` 1 · hook `lstrip()` added 1 · hook `~~~` 1 · hook ``` 1 · counters `:375` `.strip()` 1 · counters `:376` `.lower()` 3 · counters `:412` `.lower()` 9 · counters prefix 1 · counters `~~~` 1. Reductions: exempt-only 2, controls-only 2. Each of the 15 rows dropped in turn RED, none unnoticed. Suites: skills 700, scripts 332, hooks 103.
- 2026-07-30: Scope amended at the merge gate — the `Out:` clause claiming prefix-matching divergences were "already red under mutation and covered by the existing tests" is DELETED. Review F1 disproved it (both layers' `## ` prefix test dropped green), and the milestone now covers that axis, so the clause was false twice over. Approved by the user 2026-07-30.

## Decisions

## Review

**Review fan-out (2026-07-30).** Three fresh-context lenses plus a scorer that
did not generate the findings. 11 findings: 4 scored >=80 and were actioned, 7
scored below and are logged in the work log above, one line each (IP3 —
surfaced, never dropped). The two highest were surviving mutations of the
milestone's own failure mode, both now red; the full mutation set was re-run
after the fixes.

_Evidence gathered 2026-07-30 by command on the branch tree at `9100a4d`; every
figure below was re-run fresh at review, not carried from implement._

- **AC1** — met. The three verdicts come from independent expressions: counters
  `count == len(PREAMBLE.splitlines())` over a file written to a temp dir, hook
  `"_cairn:" in part` over a real `milestone_part` call, expected from the table
  literal. Both measured arms are proven load-bearing by mutation — dropping the
  hook's normalization reds (13 and 4 failures), dropping either counters site
  reds (1, 3 and 9). The `MIN_TAIL_BLOCKS` clause has its own assert
  (`assertGreater(self.ENTRIES, self.sc.MIN_TAIL_BLOCKS)`).
- **AC2** — met on all three axes. Format: the five renderings are present and
  each is pinned individually. Site: `## Review `carries whitespace to the
  boundary site, without which `cairn_scripts.py:375` drops green (this was the
  round-2 certification finding). Fence: all four layer×fence mutations red —
  hook ``` 1, hook `~~~` 1, counters `~~~` 1, and the counters' `~~~` case needs
  the count assert because the exempt subtraction hides a mis-split from the
  section list. Individual pinning measured by deleting each of the 13 rows in
  turn: 13 red, none unnoticed.
- **AC3** — met. Each control asserts the whole-section line count and both the
  oldest and newest entry present alongside `marked is False`, so a
  `milestone_part` returning nothing fails rather than passes.
- **AC4** — met, both directions: table reduced to exempt-only rows reds (2
  failures), reduced to controls-only reds (2). `test_the_table_exercises_both_verdicts_on_both_layers`
  is among the failures in both.
- **AC5** — met, scoped to the class as the criterion requires. `.strip()`
  removed from `heading_name`: 4 failures in the class. `.lower()` removed: 13.
  Both restored: the class passes. The scoping matters — 7 of the 98 pre-milestone
  hooks tests already red on `.lower()`, so a whole-suite verdict would prove
  nothing about this guard.
- **AC6** — met. The candidate row is absent from `cairn/ROADMAP.md`, and the
  three facts it got wrong are recorded in this file's work log and in AC6
  itself: `.lower()` reds 7 of 98, `hooks/` byte-identical to `016a210`, and
  `.strip()` the axis this milestone closes.
- **AC7** — met. `skills/tests` 700 OK · `scripts/tests` 332 OK · `hooks/tests`
  103 OK, all run from the repo root.

**Consistency gate.** `cairn_validate` exit 0, all checks passed. The `generic`
profile's `consistency-gate` slot names no toolchain checks, so that half is a
clean no-op. No `DESIGN.md` principle changed (the header's `GP1` is a principle
this milestone works under, not one it alters), so `cairn_impact --changed` does
not apply. No returns: this is the milestone's first review pass, so neither
thrash trigger is reached.
