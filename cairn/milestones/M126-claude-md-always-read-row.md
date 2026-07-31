# M126: CLAUDE.md joins the always-read governance frame

- **Status:** blocked
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** `m126-claude-md-always-read-row` · https://github.com/jmgirard/cairn/pull/126

## Goal

The always-read governance frame's worked table covers every surface this repo
actually loads at session start, `CLAUDE.md` included, and states why cairn's
governance of it stops at the cairn section.

## Scope

**In:** a recorded sweep of what a session actually loads at start, classifying
each surface against the frame's table; a table row for each uncovered surface;
the statement of what makes the `CLAUDE.md` row unlike the five above it; guards
pinning both, mutation-registered and inversion-verified; a `DECISIONS.md` entry
recording the addition and its boundaries.

**Out:**
- Any change to what cairn governs in `CLAUDE.md` — D-018's section-only cap and
  D-009's routing-only rule both stand unchanged; nothing moves.
- Amending the frame's opening definition of an always-read file — settled at the
  plan gate as unnecessary; the reasoning lands in the D-entry (AC6), not in the
  rulebook.
- Reconciling the frame's membership rule with its contents — `tracking-rules.md`
  sits in the table though it is read when a skill fires, not at session start,
  while `PROFILE.md`'s slots are read that same conditional way and are absent →
  candidate row, added by this plan.
- Mechanizing the frame check → standing rejection (D-060, RR03 rec 10); the
  frame stays prose applied by audit judgment.

## Acceptance criteria

- [x] AC1: A sweep enumerates every surface a session loads at start, derived by
      reading `hooks/hooks.json`'s SessionStart entry and `session_context.py`'s
      `build_context`, plus the harness-loaded project instructions — never a
      list carried from this plan. Each surface is classified covered by the
      frame's table, uncovered, or out of scope with its reason. Evidence: the
      classification, one row per surface, in the Review section.
- [x] AC2: Each surface AC1 classifies uncovered gains a row in the
      "Always-read governance" worked table, appended after the existing fifth
      row so the guarded sentence "The fifth surface differs from the four above
      it" stays true. The `CLAUDE.md` row's three cells name: inflow — the
      routing-only rule (D-009); outflow — the weight-caps remedy trimming the
      section back to the template; signal — the <30-line cairn-section cap
      enforced by `cairn_validate`'s `weight caps` CHECK. Evidence: the shipped
      row plus the file:line of each of the three sources.
- [x] AC3: The rulebook states beneath the table what makes the `CLAUDE.md` row
      unlike the five above it — cairn governs its `## Project tracking` section
      and the remainder of the file is governed by nothing cairn owns (D-018),
      as against the milestone file, whose cap-exempt sections are still
      governed, by read-bounding (D-063). The statement claims no uniqueness
      about differing always-read and governed units.
- [ ] AC4: `test_always_read_frame.py` pins each new row whole — every cell, so
      an appended cell reds — and pins the AC3 statement. Every anchor is copied
      from the shipped bytes and sits on one physical line of the target, with a
      single exception: `BOUNDARY_STATEMENT`, which pins the AC3 statement
      entire under a whitespace normalization applied to both sides, because
      per-line anchoring is the defect shape guard-doctrine §8's stop rule
      convicted here. Evidence for the exception is that pin alone — green when
      the target's statement is re-wrapped, red when it is reworded. Each new
      pinned block gets its own `test_mutation_harness.py` REGISTRY entry, and
      the harness runs green with them present. The new prose is grepped for
      every phrase an existing `test_always_read_frame.py` assert anchors on;
      any assert whose phrase the new prose duplicates is re-anchored into its
      own sentence (M113).
- [x] AC5: Each rule this milestone ships in `tracking-rules.md` is inverted in
      place per `guard-doctrine.md` §1 — relabel, negate, or transpose **the
      rule**, never the assert; run; require red; restore and diff — with the
      per-rule result recorded. After restore, `python3 -m unittest discover`
      over `hooks/tests`, `scripts/tests` and `skills/tests` each exit 0, and
      `cairn_validate` exits 0.
- [x] AC6: A `DECISIONS.md` entry records: that this applies D-060's own audit
      bullet as D-063 did, superseding nothing; the D-018/D-009 boundary making
      the section the governed unit; why the frame's opening definition is left
      unamended; and why `PROFILE.md` and the hook's preamble are out of scope.
      Evidence: the appended entry, `dangling id tokens` clean.

## Coverage

- AC1 → T1
- AC2 → T3
- AC3 → T3
- AC4 → T4
- AC5 → T5, T6
- AC6 → T2

## Tasks

- [x] T1: Run the AC1 sweep against `hooks/hooks.json` and
      `hooks/session_context.py:240-270` (`build_context`); classify each
      surface and record the table.
- [x] T2: Append the `DECISIONS.md` entry (AC6's four points).
- [x] T3: Add the row(s) after `tracking-rules.md:182` and the boundary
      statement beneath the table, near the existing fifth-surface paragraph at
      `tracking-rules.md:184-193`.
- [x] T4: Add the asserts to `skills/tests/test_always_read_frame.py` (row shape
      at `:72-97`, standalone claims at `:99-117`) and the REGISTRY entries near
      `skills/tests/test_mutation_harness.py:2156-2173`; run the adjacent-phrase
      grep; run the harness.
- [x] T5: Invert each shipped rule per guard-doctrine §1; record per-rule.
- [x] T6: Full verify (three suites + `cairn_validate`); ROADMAP row; hygiene.

## Work log

- 2026-07-31: created by /milestone-plan.
- 2026-07-31: criteria audit ([O], fresh context) returned nine findings on the step-2 draft; eight fixed here, one taken to the gate. Wrong-unit inflow cell (the file-map row owns the whole file, which D-018 excludes) → repointed to D-009; AC1 unconstrained on row position, admitting an insert that falsifies the guarded "fifth surface" sentence → append-after-fifth required; AC2's uniqueness claim false against the milestone file's own unit split → narrowed to what cairn governs at all; AC5 inverted the assert rather than the rule (vacuously red) → repointed to guard-doctrine §1; AC4's per-entry reddening report does not exist (subTest aggregates) → green-harness evidence; AC1's "adds no new rule" judgment-as-measurement and its ~400-char work-log quote evidence → file:line pointers; adjacent-guard grep added to AC4; T1's D-entry mapped by no criterion → AC6 added.
- 2026-07-31: plan gate chose leaving the frame's opening definition unamended over amending it, because the shipped sentence excludes nothing and an amendment would ship unguarded against D-060's prose-guarded mandate, its target line wrapping besides; falsified by a reader taking the definition to exclude a section-scoped surface.
- 2026-07-31: plan gate chose sweeping every session-start surface over closing the named `CLAUDE.md` gap alone, because a criterion that lists its sites becomes the sweep and omits the rest (M118, M112); falsified by the sweep returning surfaces whose rows the frame cannot state.
- 2026-07-31: plan gate chose a candidate row over settling the frame's membership rule here, because the table already holds a conditionally-read file and fixing that is doctrine revision, not a table row; falsified by the AC1 sweep being unable to classify a surface without the rule settled.
- 2026-07-31: implement gate chose scoping the new row's first cell to `CLAUDE.md`'s `## Project tracking` section over naming the file bare, because all three of the row's cells state section-scoped governance (D-009 inflow, the trim-to-template outflow, the 30-line section cap) and a file-named cell makes all three overclaim against D-018; and chose a new paragraph for the AC3 boundary statement over reworking the guarded fifth-surface paragraph, avoiding the re-anchoring the M104 trap runs on.
- 2026-07-31: minor amendment — T3 worked before T2 (task reorder only; no criterion, scope or task text changed), so the D-entry records what shipped rather than what was intended.
- 2026-07-31: T1 — AC1 sweep run against `hooks/hooks.json:3-13` and `build_context` (`hooks/session_context.py:241-344`) plus the harness-loaded project instructions; six surfaces, `CLAUDE.md` the sole uncovered one, `PROFILE.md`'s name header / the hook `PREAMBLE` / per-user memory out of scope. Classification table in `## Decisions`.
- 2026-07-31: T3 — sixth frame row shipped at `tracking-rules.md:183`, scoped to `CLAUDE.md`'s `## Project tracking` section; the AC3 boundary statement added as its own paragraph at `:196-206`, leaving the guarded fifth-surface paragraph untouched. Cell sources: D-009 `cairn/DECISIONS.md:90`, the trim-to-template remedy `tracking-rules.md:141-143`, the 30-line cap `tracking-rules.md:86` with `scripts/cairn_scripts.py:89` and `scripts/cairn_validate.py:75-77`.
- 2026-07-31: T4 — four asserts added to `test_always_read_frame.py` (the sixth row whole; the three AC3 claims, each anchored on one physical line of the target), four matching `test_mutation_harness.py` REGISTRY entries; harness green. Adjacent-phrase grep over all 13 existing anchors: each still occurs exactly once, so no re-anchoring is owed.
- 2026-07-31: T2 — D-094 appended, recording AC6's four points plus per-user memory's out-of-scope reason; `dangling id tokens` clean.
- 2026-07-31: T5 — four shipped rules inverted in place per guard-doctrine §1, each RED with exactly one failing test, each restored byte-identical (`git diff` empty): row cells transposed (inflow↔outflow); "never the whole file" → "the whole file too"; "stay governed, by a read-bound" → "stop being governed, with no read-bound"; "No uniqueness is claimed" → "Uniqueness is claimed".
- 2026-07-31: §8 certification round 1 ([O], fresh context) returned seven findings — three AC-clause coverage gaps, four claim-vs-file. All fixed here; none is a fix-authored record (round 1 has no prior fix), so all seven cleared both lines and a round 2 follows.
- 2026-07-31: round-1 fix — AC3's remainder clause and its no-uniqueness clause were each pinned only in a sentence head, both negatable green (the reader's probes: "governed by cairn too, and every cell in that row reaches it"; "a shape only this sixth surface carries"). The boundary paragraph was re-wrapped so each clause completes on one physical line, and two asserts added: `test_names_the_ungoverned_remainder_of_the_file`, plus the whole-claim anchor in `test_claims_no_uniqueness_for_the_split_unit`.
- 2026-07-31: round-1 fix — AC2's and D-094's "the guarded sentence 'The fifth surface differs from the four above it'" was false: nothing pinned that sentence, and nothing pinned the row's position, so a row inserted above the sixth passed all 827 tests. `test_the_sixth_row_is_appended_below_the_fifth` now pins both the sentence and the fifth-before-sixth order, which makes the claim true rather than superseding it.
- 2026-07-31: round-1 fix — a stray copy of the T5 work-log line had landed inside `## Acceptance criteria` (a botched string replace, not an amendment); removed, restoring the plan-owned section to what /milestone-plan authored.
- 2026-07-31: correction — the T5 line above records "exactly one failing test" per inversion, measured under `python3 -m unittest discover -s skills/tests -p test_always_read_frame.py`, which AC5 does not name. Under AC5's own command (`python3 -m unittest discover -s skills/tests`) each inversion reds two: the frame guard and the mutation harness, whose registered block no longer occurs.
- 2026-07-31: correction — the T3 line above puts the boundary paragraph at `tracking-rules.md:196-206`; it was `:196-205` as shipped then, and is `:196-203` after the round-1 re-wrap.
- 2026-07-31: T5 re-run over all six shipped rules plus two probes, under `python3 -m unittest discover -s skills/tests` from the repo root, each mutation applied to `skills/shared/tracking-rules.md` alone and the file restored between runs: row cells transposed; "never the whole file" negated; the D-018 remainder clause negated; the read-bound/cap contrast negated; the no-uniqueness PREDICATE negated (round 1's green probe); the sixth row moved above the fifth; the fifth-surface sentence deleted. All seven RED — six as `FAILED (failures=1, errors=1)`, the row transposition as `FAILED (failures=1)` — and the file restored byte-identical after each.
- 2026-07-31: §8 certification round 2 ([O], fresh context) returned six findings — one coverage gap on executable surface, five on records round 1's own fixes wrote. The coverage gap repeats round 1's defect shape (an anchor pins one side of the target's hard wrap while the criterion clause completes on the other, so negating the unpinned line stays green): round 1 on a sentence head, round 2 on the statement's subjects at `tracking-rules.md:196` and `:198`.
- 2026-07-31: §8 STOP disclosed (guard-doctrine §8 stop rule). Stop: two consecutive rounds returned the same defect shape, so the certification convenes no round 3. Shape: a per-line anchor over hard-wrapped prose pins one line and leaves the clause's other line negatable green. Remedy (structural, closing the class rather than the instance): `test_pins_the_whole_boundary_statement` pins the sixth surface's entire boundary statement whitespace-normalized, so every byte of it reds — no per-line anchor selection remains to get wrong — and `test_the_worked_table_holds_exactly_the_six_surfaces_in_order` pins the table's whole membership and order in place of the relative fifth-before-sixth check. Confirmed by operation: all twelve mutations below red, including all five probes the two rounds found green.
- 2026-07-31: inversion re-run over every rule this milestone ships plus the rounds' five green probes, under `python3 -m unittest discover -s skills/tests` from the repo root, each mutation applied to `skills/shared/tracking-rules.md` alone and the file restored between runs. Twelve of twelve RED, file restored byte-identical after each: row cells transposed `FAILED (failures=1, errors=1)`; "never the whole file" negated (2,1); the D-018 remainder clause negated (2,1); the read-bound/cap contrast negated (2,1); what-separates-them transposed (1,1); the no-uniqueness predicate negated (2,1); the remainder SUBJECT swapped (1); that subject double-negated (1); the section-scoping subject negated (1); the sixth row moved above the fifth (1); a row inserted ABOVE the fifth (1); the fifth-surface sentence deleted (1,1).
- 2026-07-31: correction — the round-1 fix line above says the boundary paragraph "was re-wrapped so each clause completes on one physical line". True of the D-063 contrast and the no-uniqueness claim only; the section-scoping clause spans `tracking-rules.md:196-197` and the remainder clause `:198-199`. That split is what round 2 found, and the whole-statement assert is what closes it rather than a further re-wrap.
- 2026-07-31: correction — the T5 re-run line above attributes `FAILED (failures=1)` to the row transposition and `FAILED (failures=1, errors=1)` to the other six. Reversed for that pair: the row transposition reds the frame guard AND errors the harness (its registered block no longer occurs), while the single-failure case was the sixth row moved above the fifth, whose registered blocks both survive the move. The same line says "six shipped rules plus two probes" and then counts seven: seven ran, and the rule at `tracking-rules.md:201-202` was not among them. It is inverted in the twelve-mutation run above (R5).
- 2026-07-31: correction — the round-1 fix line and a test comment both report "all 827 tests" green under an unnamed command. The figure is `python3 -m unittest discover -s skills/tests` at 667d919; the three suites AC5 names totalled 1262 there, and `skills/tests` is 830 now. The comment is corrected in place; this line supersedes the work-log figure.
- 2026-07-31: T6 — three suites green (`hooks/tests` 103, `scripts/tests` 332, `skills/tests` 830) and `cairn_validate` all checks passed, all advisories OK. Plan-owned body 102/149 lines. Anchor sweep over all 23 string constants in `test_always_read_frame.py`: 22 occur exactly once and wholly on one physical line of their target; the 23rd is `BOUNDARY_STATEMENT`, normalized by design and asserted against the normalized file. The file docstring gained the sixth-row paragraph its own M113 precedent set.
- 2026-07-31: status -> review at zero unresolved: every §8 finding from both rounds is fixed, and the shape-repeat stop's remedy is confirmed by operation rather than by a third round.
- 2026-07-31: review opened — draft PR #126; three-lens fan-out spawned and still running; criterion evidence gathered for AC1-AC3, AC5, AC6. AC4 fails as written: its "every anchor ... sitting on one physical line of the target" is universal over anchors, and `BOUNDARY_STATEMENT` — the whole-statement pin §8's stop rule obliged as its structural remedy — spans eight physical lines by construction. Disposition pending the fan-out.
- 2026-07-31: review round 1 returned the milestone to `in-progress`. AC4 FAILS as written — `BOUNDARY_STATEMENT` is an anchor spanning eight physical lines, and AC4 quantifies "sitting on one physical line of the target" over every anchor; the whole-statement pin is guard-doctrine §8's obliged structural remedy, so the criterion is what needs the gated amendment, never a charitable reading. Also actioned: F9 (92), two holes in the new table parser — a substring header match lets an appended column pass, and a deleted separator row passes, both against the guard's own comment. AC1-AC3, AC5, AC6 passed with fresh evidence recorded in the Review section; 18 sub-threshold findings logged there. Return 1 of this milestone.
- 2026-07-31: AMENDMENT (substantive, gated) — AC4's "every anchor ... sitting on one physical line of the target" was universal over anchors and so unsatisfiable by the whole-statement pin §8's stop rule obliged. Amended at the implement gate to split the bar: a per-line anchor still sits on one physical line, while a whole-object pin applies its declared normalization to both sides and is evidenced by the suite green under a reflow and red under a reword. A harder criterion, not a loosened one. Plan-owned body 102 -> 107 of 149.
- 2026-07-31: F9 (92) fixed — the table guard matched `TABLE_HEADER` as a substring and never required the separator row, so an appended `| Notes |` column and a deleted separator both passed against the guard's own comment. The header is now matched as a whole line via `splitlines().index`, and the separator is required by `assertRegex`. Both probes red.
- 2026-07-31: F4 (75) promoted from the logged list at the user's call and fixed — nothing pinned the boundary statement's position, so moving it to EOF stayed green. `test_the_boundary_statement_sits_beneath_the_table` bounds it on BOTH sides, between the table's last row and the section-closing audit paragraph; a one-sided "after the table" first cut passed the EOF relocation and was corrected before commit. Registered in the harness.
- 2026-07-31: amended-AC4 evidence, `python3 -m unittest discover -s skills/tests` from the repo root, mutating `skills/shared/tracking-rules.md` alone and restoring between runs. Whole-object arm measured on `test_pins_the_whole_boundary_statement` alone, since per-line anchors are meant to break on reflow: statement re-wrapped onto one line GREEN, at 55 cols GREEN, at 120 cols GREEN, reworded under a reflow RED. Whole-suite probes, all four previously green, now all RED: appended header column; deleted separator row; statement moved to EOF; statement moved above the table.
- 2026-07-31: three suites green (103 / 332 / 831) and `cairn_validate` exit 0. Status -> review.
- 2026-07-31: §8 delta round ([O], fresh context) over the return's own guard surface — run because the return authored new guards, and the earlier stop rule bars further rounds on the hard-wrap shape it closed, not on newly written surface. Five findings. Recorded honestly: the status flip to `review` preceded this round in the return, where §8 puts the reader first.
- 2026-07-31: AMENDMENT (substantive, gated) — the amended AC4 failed the SAME SHAPE as the original: a clause quantified over a scope the artifact cannot meet. "Evidence is the suite green against a reflowed target" is false, because per-line anchors are meant to break on reflow and a real re-wrap reds four of them; the evidence recorded under it was measured at single-test scope. Second failure of one criterion by a new mechanism of one shape, so the thrash rule's remedy applied: take the alternative the previous gate recorded against. AC4 is now the narrow form — one physical line for every anchor, `BOUNDARY_STATEMENT` named as the single exception, its evidence stated at that pin's own scope. Every clause measured against the files before the gate, not reasoned about.
- 2026-07-31: delta-round finding 3 fixed (executable surface) — `test_the_worked_table_holds_exactly_the_six_surfaces_in_order` compared first cells only, so a fifth cell appended to a four-column row passed green: F9's malformed-table class surviving on the row side after the header side was closed. Every row's cell count is now checked against the header's, and the separator's too. Probes: a fifth cell on the sixth row RED, on the fifth row RED, a 3-column separator RED, and a legitimately respaced `| --- | --- | --- | --- |` separator GREEN.
- 2026-07-31: delta-round finding 4 fixed in place — the new test's comment quoted "the five above it" as position-dependent prose in the statement; that phrase is in no rulebook line (the target says "the four above it", in the fifth-surface paragraph). Quote removed; the two true fragments stand.
- 2026-07-31: correction — the T6 line's "all 23 string constants ... 22 occur exactly once and wholly on one physical line" is staled by this return, and carried no procedure. Re-measured: AST-parse `skills/tests/test_always_read_frame.py`, take every `str` Constant over 25 characters containing no newline, resolve each against `tracking-rules.md` when that file contains it and `skills/milestone/SKILL.md` otherwise. 24 constants; 23 sit wholly on one physical line of their target; the exception is `BOUNDARY_STATEMENT`, normalized by design.
- 2026-07-31: delta-round findings 1 and 2 are the amended criterion's own wording and are closed by the amendment above rather than by a code change; finding 5 is the count corrected above. Out-of-mandate observations recorded and not chased: the position test's upper bound moves if the audit paragraph moves with the statement; the pinned region between table and audit paragraph is wide; the guard docstring's "each a single physical line" universal is the review's logged F3 (70), still open.
- 2026-07-31: §8 delta round 2 ([O], fresh context) returned four findings. Finding 1: AC4's "a whitespace normalization applied to both sides" was false — `assertIn` normalized the target only, the anchor being a pre-normalized fixed point. Fixed on the executable side rather than by rewording, so the clause is now true and a later re-wrap of the CONSTANT cannot red the guard spuriously.
- 2026-07-31: §8 STOP #2 disclosed. Shape: a universal claim about these anchors that the anchors do not satisfy — twice in AC4 ("every anchor ... on one physical line", then "evidence is the suite green against a reflowed target"), and now a third time in the guard file's own docstring, which delta round 1 wrongly filed out-of-mandate when guard-doctrine §8's check 2 names docstrings explicitly. Fixing each instance in place bought the next, which is the stop rule's own diagnosis. Remedy (structural, closing the class): `TestAnchorDescriptionMatchesTheAnchors` DERIVES the whole-object-pin set from the anchors themselves and reds when the docstring and the file disagree, with a non-vacuity assert so an empty derivation cannot pass green. Confirmed by operation: dropping the exception from the docstring RED; adding a second whole-object pin the docstring does not name RED; rewording inside a pin's target RED. The docstring is corrected to name `BOUNDARY_STATEMENT` and to point at the test that keeps it honest.
- 2026-07-31: correction — an earlier line calls the narrowing "the alternative the previous gate recorded against". The thrash rule points at the PLAN gate's recorded alternative, and no plan-gate line here records one bearing on anchor scope; the alternative taken was the one this milestone's own first implement gate offered and declined. The remedy applied is right, the citation was not.
- 2026-07-31: ROADMAP candidate added (search-first swept, nothing covers it) — verify a scripted multi-edit landed where it was aimed before writing the record that claims it did. Raised from a hitop session and corroborated by this milestone's own stray work-log line inside `## Acceptance criteria`. Added on this branch rather than main because the branch is open; it merges with the milestone.
- 2026-07-31: numeric records settled LAST, after every fix, because each earlier settling was re-staled by the next (guard-doctrine §6). Procedure for the anchor count: AST-parse `skills/tests/test_always_read_frame.py`; the anchor set is every module-level string constant over 25 characters plus every inline string literal over 25 characters with no newline that resolves into `skills/shared/tracking-rules.md` or `skills/milestone/SKILL.md`. 24 anchors, of which 23 sit wholly on one physical line of their target and one — `BOUNDARY_STATEMENT` — does not, by design. A blanket "every string constant" sweep instead returns 25 and two off-line, the second being an assert message rather than an anchor; that is the earlier count's defect, not a second exception.
- 2026-07-31: correction — every count recorded earlier in this milestone is superseded by these, measured at this commit with the commands named: `python3 -m unittest discover -s hooks/tests` 103, `-s scripts/tests` 332, `-s skills/tests` 833, each exit 0; `python3 scripts/cairn_validate.py .` exit 0, all checks passed; `python3 scripts/cairn_budget.py` on this file, plan-owned body 108 of 149; 22 `guard="test_always_read_frame"` REGISTRY entries. The earlier "830" and "102 -> 107 of 149" were true when written and are not now.
- 2026-07-31: review round 2 returned the milestone. Six findings at 80+: the STOP #2 structural remedy does not close its class (inline anchors invisible to its derivation, and its docstring check pins a token rather than agreement — both reproduced at the gate), three relocations still pass the position guard, round 2's own AC4 evidence line misattributes its figure to the guard, `BOUNDARY_STATEMENT`'s normalization is asymmetric across its two users, and the new ROADMAP candidate row ships truncated mid-sentence. guard-doctrine §8's stop-rule falsifier has FIRED on its one-occurrence tolerance: the universal-claim shape returns to round-opening. Return 2 — one more reaches the thrash rule's third-return threshold.
- 2026-07-31: blocked on RB11 — a guard's description of itself keeps drifting from what it checks. Three instances of one shape in this milestone, the third being the class-closing structural remedy itself, so guard-doctrine §8's stop-rule falsifier has spent its one-occurrence tolerance. Escalated rather than attempted a fourth time: the thrash rule owed this offer when trigger (b) fired and no plan-gate alternative existed, and each prior attempt was authored by a session that had just read the previous failure and checked its own work before shipping.
- 2026-07-31: RR11 received. Verdict is subtractive — delete the self-describing checker rather than write a fourth, collapse the double-pinned paragraph to one comparison rule, add a quantified-claim rule to guard-doctrine §6, and amend §8's shape-repeat remedy clause to prefer subtraction. It found three further defeats of the shipped remedy beyond review's two, including a pin named `BOUNDARY` passing the docstring check by substring — §1's opening defect inside the fix for a guard-doctrine violation.
- 2026-07-31: RR11 binding-criteria audit ([O], fresh context, pre-ingest) returned BC2 and BC6 UNSATISFIABLE as written, BC1 and BC4 PROBLEMATIC, three joint collisions, and a budget landing at ~166 of 149 with a forced compression pass aimed at the section the ingest would make verbatim-immutable. BC2 is this milestone's third instance of its own convicted shape: "pinned by exactly two tests" is falsified by the harness registration BC2 itself mandates, which reds third. BC6 adds a second confirmation obligation to a class whose single-obligation invariant §8 states in bold and two guards count. Not ingested verbatim; raised at the gate.

## Decisions

### 2026-07-31 — AC1 sweep: what a session actually loads at start

Derived by reading `hooks/hooks.json:3-13` (the sole `SessionStart` entry) and
`hooks/session_context.py:241-344` (`build_context`), plus the project
instructions the harness loads. Six surfaces; one uncovered.

| Surface | Loaded by | Classification |
|---|---|---|
| `CLAUDE.md` | the harness's project-instructions injection | **uncovered** — gains a frame row (AC2) |
| `cairn/ROADMAP.md` | `hooks/session_context.py:258` | covered — the frame's first row |
| each active `cairn/milestones/M<NN>-<slug>.md` | `hooks/session_context.py:294-296`, active statuses from `hooks/cairn_common.py:16` | covered — the frame's fifth row |
| `cairn/PROFILE.md`'s `# Toolchain profile:` header | `hooks/session_context.py:244-251` via `profile_name` (`:94-109`) | out of scope — only the profile NAME reaches the session; the seven slots the rulebook governs are read when a skill fires, so whether a conditionally-read file belongs in the frame is the membership question this milestone's Scope puts Out |
| the hook's `PREAMBLE` | `hooks/session_context.py:85-91`, emitted at `:243` | out of scope — plugin source rather than a repo record: a fixed string no repo writes to, so it has no inflow to test and cannot grow with use |
| per-user memory `MEMORY.md` | the harness's memory injection | out of scope — not a repo file, and it never holds project state ("Tracking files outrank memory", the GP4 intake gate); no repo's frame can bound a per-user surface |

Recorded, not resolved: the sweep runs one direction only. Three of the frame's
existing rows — `LESSONS.md`, `tracking-rules.md`, `DECISIONS.md` — are read
when a skill or a gate fires and not at session start, so the table's membership
already runs wider than its opening definition. That is the parked candidate
row, and nothing here settles it.

## Review

### Round 1 — 2026-07-31 · returned to `/milestone-implement`

Every criterion was executed by command in this round. **A return re-opens all
six: the next round re-executes them and records its own evidence.**

- **AC1 — PASS.** Sweep re-derived from source, not carried: `hooks/hooks.json`
  has exactly one `SessionStart` entry, `session_context.py`; `build_context`
  (`hooks/session_context.py:241-344`) emits at `:243` (PREAMBLE), `:246`
  (profile name), `:258` (ROADMAP), `:294` (one part per active milestone,
  statuses from `hooks/cairn_common.py:16`). With the harness-loaded project
  instructions that is six surfaces, classified in the `## Decisions` sweep
  table above: `CLAUDE.md` uncovered; `ROADMAP.md` and the active milestone
  files covered by rows 1 and 5; `PROFILE.md`'s name header, the hook
  `PREAMBLE` and per-user memory out of scope, each with its reason.
- **AC2 — PASS.** Row shipped at `skills/shared/tracking-rules.md:183`, appended
  below the fifth. Its three sources verified in place: inflow D-009 at
  `cairn/DECISIONS.md:90`; outflow the trim-to-template remedy at
  `tracking-rules.md:141-143`; signal the <30-line cap at `tracking-rules.md:86`,
  `scripts/cairn_scripts.py:89` (`CLAUDE_SECTION_CAP = 30`) and
  `scripts/cairn_validate.py:75-77` under the `weight caps` CHECK.
- **AC3 — PASS.** Statement shipped at `tracking-rules.md:196-203`: the section
  is the governed unit, the dev doctrine outside it is not reached by any cell
  (D-018), the milestone file's cap-exempt sections stay governed by a
  read-bound rather than a cap (D-063), and no uniqueness is claimed for either.
- **AC4 — FAIL.** Its clause "every anchor copied from the shipped bytes and
  sitting on one physical line of the target" is universally quantified over
  anchors. An AST sweep of `test_always_read_frame.py` finds every anchor on one
  physical line of its target except `BOUNDARY_STATEMENT`, which spans the eight
  lines of the boundary paragraph by construction — it is the whole-statement
  pin guard-doctrine §8's shape-repeat stop rule obliged as the structural
  remedy, after per-line anchoring was twice convicted as the defect shape. The
  work is right and the criterion is wrong: reinterpreting it charitably is
  exactly what AC fencing forbids, so the milestone returns for a gated
  amendment (`/milestone-implement` step 6). Every other AC4 clause holds:
  20 REGISTRY entries for the frame guard, harness green (9 tests), and the
  adjacent-phrase grep finds all 13 pre-M126 anchors still occurring exactly once.
- **AC5 — PASS.** Twelve inversions over every rule this milestone ships plus the
  §8 rounds' five green probes: twelve red, file restored byte-identical after
  each (work log, 2026-07-31). After restore `hooks/tests`, `scripts/tests` and
  `skills/tests` each exit 0 (103 / 332 / 830) and `cairn_validate` exits 0.
- **AC6 — PASS.** D-094 appended at `cairn/DECISIONS.md:3408`, carrying all four
  points; `dangling id tokens` OK.

**Consistency gate.** `cairn_validate` exit 0 — every CHECK PASS, every advisory
OK. The `generic` profile's `consistency-gate` slot names no toolchain checks, a
clean no-op. No `DESIGN.md` principle changed, so `cairn_impact` was skipped. No
CI is configured in this repo (`.github/workflows` absent), so the green-CI
requirement has nothing to wait on.

**Fan-out.** Three fresh-context lenses, then a Sonnet scorer that generated
none of the findings. The blame-history lens found no violation and confirmed
independently that replacing the relative row-order assert was a strengthening.
The prior-review lens found one: AC4 unamended, citing M113's own review as the
precedent for returning a milestone whose criterion fails as written. Its
GitHub-thread probe was run here instead and came back empty, so there is no
secondary surface. The diff-bug lens returned 19 candidates.

**Actioned (score ≥80), both fixed in the return:**

- **F9 (92) — two holes in the new table parser, both contradicting its own
  comment.** `self.rules.split(TABLE_HEADER, 1)` matches the header as a
  substring, so appending a `| Notes |` column plus a widened separator stays
  green while the comment claims a changed header reds; and deleting the
  `|---|---|---|---|` separator stays green, so the table can stop rendering as
  markdown with the guard silent.
- **F2 (90) — AC4 unsatisfiable as written**, as recorded above. Reported
  independently by the prior-review lens.

**Logged, below threshold (18), surfaced not dropped:** F7 (78) the T6 anchor
count of 23 reproduces under no stated procedure; F4 (75) the boundary paragraph
is not pinned to its position — moved to EOF the suite stays green; F8 (75) a
test comment attributes the above-the-fifth probe to §8 round 2, where it came
from the author's own re-run; F18 (72) D-094 quotes the frame definition with a
dropped leading word inside quotation marks; F3 (70) the guard docstring's
universal "each a single physical line" is now false of `BOUNDARY_STATEMENT`;
F11, F12, F13, F15 (55) D-094 silent on D-045's split and on D-053's
supersession trigger, the table's column header still reads `File` over a
section cell, and two prose lines stretched to 100 and 120 characters for
anchors the whole-statement pin now subsumes; F6 (50) D-094's "already existed
elsewhere in the rulebook" holds for two of the three elements; F17 (45) an
unused local in the table guard; F10, F14, F19 (35); B1 (30); F5 (25) the
section-consistency ledger is not rolled out to this section, already a parked
candidate; F1 (20) and F16 (12).

**Disposition: returned to `in-progress`.** AC4 fails as written and F9 is a
real hole in shipped guard surface. Return 1 of this milestone — no thrash
trigger reached.

### Round 2 — 2026-07-31

All six criteria re-executed by command; round 1's ticks were not carried.

- **AC1 — PASS.** Re-derived: `hooks/hooks.json` has exactly one `SessionStart`
  entry (`session_context.py`); `build_context` has four emit sites (PREAMBLE,
  profile name, ROADMAP, one part per active milestone). Six surfaces with the
  harness-loaded project instructions, classified in the `## Decisions` table —
  one uncovered, two covered, three out of scope with reasons.
- **AC2 — PASS.** Row at `skills/shared/tracking-rules.md:183`, below the fifth
  at `:182`. Sources re-verified: D-009 `cairn/DECISIONS.md:90`; the
  trim-to-template remedy `tracking-rules.md:141-143`; the <30-line cap
  `tracking-rules.md:86` with `scripts/cairn_scripts.py:89` and
  `scripts/cairn_validate.py:75-77`.
- **AC3 — PASS.** Statement at `tracking-rules.md:196-203`, carrying all four
  required claims; each is inversion-red under AC5 below.
- **AC4 — PASS**, every clause probed rather than read. *Rows whole:* a cell
  appended to the first, fifth and sixth rows each RED. *One physical line, one
  exception:* the guard's own derivation returns 24 anchors, 23 on one physical
  line, the single exception `BOUNDARY_STATEMENT`. *Exception evidence at that
  pin's own scope:* the target's statement re-wrapped at 40, 55, 72, 80 and 120
  cols and onto one line — all six GREEN; three independent rewords under a
  reflow — all RED. *REGISTRY:* 22 frame-guard entries, harness green (9 tests).
  *Adjacent-phrase:* all 23 anchors resolving into a target occur exactly once.
- **AC5 — PASS.** Eleven inversions re-run fresh over every rule the milestone
  ships — row cells transposed, the section-not-file clause, the D-018 remainder
  clause and its subject, the D-063 contrast, what-separates-them, the
  no-uniqueness predicate, the section-scoping subject, the fifth-surface
  sentence, the sixth row moved above the fifth, a row inserted above the fifth
  — all RED, `tracking-rules.md` restored byte-identical after each. After
  restore `hooks/tests`, `scripts/tests` and `skills/tests` each exit 0 and
  `cairn_validate` exits 0.
- **AC6 — PASS.** D-094 present with its four points; `dangling id tokens` OK.

**Consistency gate.** `cairn_validate` exit 0, every CHECK PASS (`weight caps`
and `coverage complete` included), every advisory OK. The `generic` profile
names no toolchain checks — a clean no-op. No `DESIGN.md` principle changed, so
`cairn_impact` was skipped. No CI configured, so nothing to wait on at merge.

**Fan-out.** Three fresh-context lenses, then a Sonnet scorer that generated
none of the findings. The prior-review lens verified round 1's two actioned
findings genuinely closed and found no past finding reintroduced. The
blame-history lens found no coverage dropped across the branch's many self-
rewrites — every guard from `main` still present, the replaced assert strictly
stronger, the harness diff pure addition. The diff-bug lens returned 20
candidates. The GitHub thread probe was empty, as in round 1.

**Actioned (score ≥80):**

- **A1 (88) — the §8 STOP #2 structural remedy does not close its class.**
  `whole_object_pins` walks only module-level `ast.Assign` nodes, so inline
  anchors inside `assertIn` are invisible to it. An inline anchor spanning two
  physical lines of the target, with no docstring mention, passes GREEN — the
  exact shape the remedy was declared to close. Reproduced independently at
  the gate before scoring.
- **A2 (87) — the docstring check pins a token, not agreement.**
  `assertIn(name, doc)` requires only that the string `BOUNDARY_STATEMENT`
  occur somewhere in the docstring. Replacing the exception clause with its
  exact opposite passes GREEN, so the remedy's headline claim — "reds when
  this paragraph and the file disagree" — is false as shipped. Also
  reproduced at the gate.
- **A5 (85) — three relocations still pass the position guard.** Statement and
  audit paragraph moved together to EOF; statement moved above the
  fifth-surface paragraph, making shipped prose "The sixth surface differs
  again" precede "The fifth surface differs…"; statement spliced into the
  middle of that paragraph. All GREEN.
- **A3 (83) — round 2's own evidence line states something false about the
  guard.** "the guard's own derivation returns 24 anchors, 23 on one physical
  line": the guard's derivation returns one entry, from four module-level
  assigns. The 24/23 figure came from an ad-hoc script, not the guard.
- **A8 (82) — `BOUNDARY_STATEMENT`'s normalization is asymmetric across its
  two users.** The position test compares the raw constant against a
  normalized target, so re-wrapping the constant raises `ValueError` there —
  the spurious red that delta round 2's fix was authored to remove.
- **A16 (80) — the new ROADMAP candidate row ends mid-sentence**, at "…
  corroborated by M126's own stray", with no noun. Shipped truncated tracking
  state, inside the candidate about verifying that a scripted edit landed
  where it was aimed.

**Logged, below threshold (16):** C1 (75) the round-1 comment misattribution
still ships; A14 (70) D-094's misquoted definition, now raised three times;
A6 (66) a bare appended `|` still passes the row-width check; B2 (65) the
STOP #2 disclosure narrates its shape across three sources rather than
establishing D-091's precondition; A7 (63) the separator regex rejects legal
GFM alignment syntax; A4 (62) thrash trigger (b)'s escalation offer was owed
and not made; A17 (58); A12, A13, A19 (55); A11, A18 (52); A9 (45); A10 (42);
A15 (38); A20 (35) pre-existing; B1 (25).

**Disposition: returned to `in-progress`. Return 2 of this milestone.**
AC4 is unticked — A1, A2 and A8 defeat its clauses and A3 falsifies its own
evidence line. Every other criterion's round-2 evidence stands.

**guard-doctrine §8 stop-rule falsifier: FIRED, one occurrence.** Its text —
"if a structural remedy authored under it is later found — by the three-lens
review, or by a subsequent milestone — not to have closed its shape's class,
the stop rule returns that shape to round-opening. Tolerance: one occurrence."
A1 is that finding. The hard-wrap / universal-claim shape returns to
round-opening, and the tolerance is now spent.
