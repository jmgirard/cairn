# RB11: A guard's description of itself keeps drifting from what it checks (M126)

- **Date:** 2026-07-31
- **Output required:** write findings to `cairn/reviews/RR11-self-describing-guard-drift.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

**The repo.** `cairn` is a Claude Code plugin that supplies a project-tracking
system: a rulebook (`skills/shared/tracking-rules.md`), phase skills, and a
suite of **prose-guards** — Python tests that lock doctrine wording by
asserting substrings of markdown documents. The repo dogfoods its own system
by hand under `cairn/`. Its toolchain is language-agnostic; `verify` is
`python3 -m unittest` over `hooks/tests`, `scripts/tests` and `skills/tests`.

**Prose-guards and why they are hard.** A prose-guard gives *false coverage*
when a phrase it asserts also occurs elsewhere, or when the asserted phrase is
only part of the rule: deleting or negating the rule leaves the assertion
satisfied, so the guard passes over a rule that is gone. The repo's accumulated
craft for avoiding this is `skills/shared/guard-doctrine.md`, and its
mechanical backstop is a mutation harness
(`skills/tests/test_mutation_harness.py`) that blanks each registered block and
asserts the guard fails.

**The milestone.** M126 adds a sixth row to a governance table in
`tracking-rules.md` ("Always-read governance") plus a paragraph beneath it, and
guards both. The governance content itself is settled and is **not** what this
brief is about.

**The failure this brief is about.** M126 has now produced **three successive
instances of one defect shape**, each introduced by the fix for the previous
one. The shape: *a claim, stated as a universal, about what this guard file's
anchors satisfy — where the anchors do not in fact satisfy it, and nothing
reds.*

1. Acceptance criterion AC4 required "every anchor copied from the shipped
   bytes and sitting on one physical line of the target". A whole-statement pin
   (`BOUNDARY_STATEMENT`) was then authored as the obliged remedy for an
   unrelated per-line-anchoring defect; it spans eight physical lines by
   construction. The criterion was unsatisfiable by the artifact.
2. AC4 was amended to split the rule into a per-line arm and a whole-object
   arm, with the whole-object arm evidenced by "the suite green against a
   reflowed target and red against a reworded one". Also false: a real re-wrap
   reds four per-line anchors, because per-line anchors are *supposed* to break
   on reflow. The evidence had been measured at single-test scope and written
   at suite scope.
3. AC4 was narrowed to name `BOUNDARY_STATEMENT` as a single exception, and a
   **structural remedy** was authored to close the class rather than the
   instance: a test class (`TestAnchorDescriptionMatchesTheAnchors`) that
   *derives* the set of "whole-object pins" from the file's own anchors and
   asserts the module docstring names each one. Independent review then found
   this remedy does not close its class either — see Materials for the two
   reproductions.

Instance 3 is the important one, because it is the *class-closing* attempt.
Under `skills/shared/guard-doctrine.md` §8, a structural remedy later found by
review not to have closed its shape's class returns that shape to
round-opening, with a tolerance of one occurrence. That tolerance is now spent.

**Why this needs independent review rather than a fourth attempt.** Each of the
three instances was authored by a session that had just read the previous
failure and was explicitly trying not to repeat it, and each was checked before
shipping. The author's checking passed every time. What the author cannot seem
to do is see the gap between "what I wrote the guard to do" and "what the guard
does". A fourth attempt by the same author is the thing this brief exists to
avoid.

## Materials

Read these, in this order:

1. `skills/shared/guard-doctrine.md` — the whole module, but especially §1
   (what an assert must pin), §2 (what the mutation harness does and does not
   catch), §3 (absence assertions and the enumeration trap), §7 (scoping a
   sweep), §8 (the author never certifies its own guard's coverage, including
   its stop rule and that rule's falsifier), and §9 (presence is not
   consistency).
2. `skills/tests/test_always_read_frame.py` — the guard file at issue, whole.
   Note the module docstring, the module-level constants (`TABLE_HEADER`,
   `FRAME_ROWS`, `BOUNDARY_STATEMENT`), and the class
   `TestAnchorDescriptionMatchesTheAnchors` with its two tests
   (`test_the_docstring_names_each_whole_object_pin`,
   `test_each_whole_object_pin_still_matches_under_its_normalization`) and its
   helper `whole_object_pins`.
3. `skills/shared/tracking-rules.md` lines 155–206 — the guarded section (the
   "Always-read governance" frame, its table, and the boundary paragraph M126
   adds).
4. `skills/tests/test_mutation_harness.py` — the `REGISTRY` entries whose
   `guard` field is `test_always_read_frame` (22 of them), and the harness's
   own tests near the end of the file.
5. `cairn/milestones/M126-claude-md-always-read-row.md` — the `## Work log`
   (the three instances are recorded there in order, with the probes run for
   each) and the `## Review` section (rounds 1 and 2, with scored findings).

**Running things.** From the repo root:

```
python3 -m unittest discover -s skills/tests
python3 -m unittest discover -s hooks/tests
python3 -m unittest discover -s scripts/tests
python3 scripts/cairn_validate.py .
```

All four are green at `HEAD` of branch `m126-claude-md-always-read-row`. To
probe a mutation without touching the working tree, copy the repo first
(`git archive HEAD | tar -x -C <somewhere>`) and mutate the copy.

**The two reproductions that defeat instance 3.** Both were run on a copy and
both returned GREEN where the file's own description says they must be RED:

- *Inline anchors are invisible to the derivation.* `whole_object_pins` walks
  `ast.parse(source).body` and keeps only `ast.Assign` nodes — module-level
  constants. Every other anchor in the file is an inline literal inside an
  `assertIn`. Adding an inline anchor that spans two physical lines of the
  target, with no docstring mention, passes green. The class docstring claims
  "A whole-object pin added later without a word of description reds here."
- *The docstring check pins a token, not agreement.*
  `self.assertIn(name, doc)` requires only that the string
  `BOUNDARY_STATEMENT` occur somewhere in the docstring. Replacing the
  docstring's exception clause with its exact opposite — asserting that
  `BOUNDARY_STATEMENT` is *no* exception and sits on one physical line pinned
  byte-for-byte — passes green. The module docstring claims the test "reds
  when this paragraph and the file disagree."

## Questions

1. **Is a self-describing guard the right instrument at all?** The instinct
   behind instance 3 was: prose about the guard keeps going stale, so derive
   the prose's subject from the artifact and check the prose against it. Is
   that a sound instrument, or does it merely relocate the same
   author-enumeration problem `guard-doctrine.md` §3 warns about — the author
   must still enumerate what counts as a "pin", and the derivation is
   the enumeration? If it is sound, what is the minimum it must do to be
   worth having? If it is not, say so plainly and answer question 3 instead.

2. **If it is sound: what is the correct derivation?** Specifically — should
   the set be derived from the guard's *source* (AST over constants and
   `assertIn` arguments, as attempted), from the *mutation registry* (which
   already enumerates the blocks the harness exercises), from the *target
   documents*, or from something else? Name the failure mode of each option
   you reject. The two known defeats are inline literals and the token-vs-
   agreement check; assume there are others and try to find them.

3. **What is the alternative if self-description is the wrong instrument?**
   Candidates the author has not properly evaluated: (a) delete the
   descriptive universal from the docstring entirely, on the reasoning that a
   claim nothing checks is worse than no claim — the repo has a precedent for
   this, `cairn/LESSONS.md` records a case where the fix for a self-referential
   figure was to delete the figure rather than guard it; (b) make the
   *criterion* rather than the docstring carry the claim, and check the
   criterion at review only; (c) accept the class as open, record it as a
   candidate, and stop. Which, and why?

4. **Is the underlying anchor design itself the problem?** The file now
   carries both per-line anchors and one whole-object normalized pin over the
   *same* paragraph, so every byte of that paragraph is pinned twice under two
   different comparison rules — which is what makes "what do the anchors
   satisfy" hard to state truthfully in the first place. Would collapsing to a
   single comparison rule for that paragraph dissolve the problem rather than
   solve it? What is lost if the four per-line anchors over the boundary
   statement are deleted and only the whole-object pin remains?

5. **Is there a general rule worth adding to `guard-doctrine.md`?** Three
   instances in one milestone suggests a missing piece of doctrine, not just
   three mistakes. If you can state it as one rule that would have caught all
   three, state it — and say where it belongs (§1, §8, §9, or a new section)
   and what would have to guard it. If the honest answer is that no single
   rule covers all three, say that instead; the repo would rather have no rule
   than a rule that reads as covering more than it does.

6. **Does the stop rule in `guard-doctrine.md` §8 need changing?** Its
   falsifier has now fired on its one-occurrence tolerance. Read the stop rule
   and its falsifier as shipped. Did the rule behave as designed here — the
   author stopping the rounds and authoring a structural remedy, which then
   failed — or did the rule *cause* this outcome by pushing toward a
   class-closing remedy the author was not equipped to write? If the latter,
   what should it say instead?

## Constraints

Fixed; flag disagreement explicitly rather than working around it.

- **The governance content is settled.** The sixth table row, its three cells,
  and the boundary paragraph's claims are approved and out of scope. Do not
  relitigate what the row says or whether `CLAUDE.md`'s cairn section belongs
  in the frame. See `cairn/DECISIONS.md` D-094.
- **D-018 and D-009** fix what cairn governs in `CLAUDE.md` — the
  `## Project tracking` section only, routing content only. Not open.
- **D-057** closed the stock-side size-governance program; **D-060**'s frame is
  completeness-only and never measures mass. A recommendation that reintroduces
  size or mass governance must supersede those entries explicitly.
- **D-090** closed the verification-apparatus program at the door: a new
  apparatus milestone needs a shipped-behavior defect as its trigger. This
  brief has one, so recommendations here are admissible — but say so explicitly
  if a recommendation would open new apparatus beyond that trigger.
- **D-067** rejected instructing an author to re-check its own work, on the
  grounds that it asks for the judgment authors fail at. A recommendation that
  amounts to "the author should check more carefully" contradicts it and needs
  to say so.
- **Prose-only remedies are preferred** where they work; new machinery needs to
  earn itself. `guard-doctrine.md` and `tracking-rules.md` are read at every
  guard-authoring session, so lines added there are paid for repeatedly.
- **IP4:** `cairn/DECISIONS.md` entries, work logs and archived files are
  history and are never edited — only superseded by new entries.

## Output format

In `cairn/reviews/RR11-self-describing-guard-drift.md`: answer each question by
number with your reasoning and evidence; list any additional findings
separately under "Beyond the brief"; end with concrete recommendations, each
marked apply / consider / reject-with-reason. Where findings bind
implementation, also emit a `## Binding criteria` section: numbered `BC1…`,
each a measurable assertion checkable against evidence, with any numeric
projection stating its tolerance. These are ingested VERBATIM into M126's
acceptance criteria and mechanically diffed against this file; departures are
legal only through that milestone's shown "Deviations from RR11" table.

Keep the binding-criteria set small and jointly satisfiable — criteria that are
individually reasonable can still be jointly unsatisfiable, and a frozen scope
in one can forbid work another mandates. M126's plan-owned body currently sits
at 108 of a 149-line cap, so a large criteria set will force a compression pass.
