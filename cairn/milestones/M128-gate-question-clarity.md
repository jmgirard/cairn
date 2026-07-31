<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M128: Gate questions lead in plain words

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m128-gate-question-clarity

## Goal

Rewrite the accessible-language rule from adjectives into a stated
two-sentence shape with a worked example, so gate questions are readable
without cairn's internal vocabulary.

## Scope

**In:** the "Accessible language on the decision surface" bullet in
`skills/shared/tracking-rules.md` (rewritten in place, extending — never
restating — the neighboring chip rules); a worked bad/good pair beside it;
one capture-on-flag conduct sentence; the guard updates in
`skills/tests/test_gate_conclusion_preview.py` (`TestAccessibleLanguageRule`)
and the mutation-harness registry that the prose edit forces.

**Out:** any machine check of question wording — "too technical" stays an
author judgment, never a gate (D-059's shape; promote only if the conduct
rule is measured to fail again, via the AC4 capture record). Banning
milestone ids from chips — rejected at the plan gate 2026-07-31; the four
`M<NN>` menu examples in `skills/milestone/SKILL.md` and
`skills/milestone-plan/SKILL.md` stand. Rewriting any skill's own gate
steps — conduct stays central-only (M04). Verbatim-captured exemplars —
none exist on disk; AC4's mechanism accumulates them for a future pass.

## Acceptance criteria

- [ ] AC1: The "Accessible language on the decision surface" bullet in
      `skills/shared/tracking-rules.md` states the two-sentence test: an
      AskUserQuestion's question text opens with a first sentence saying
      what is being decided in plain words and a second sentence saying
      what happens on each choice, both before any term of art; a term of
      art used after them is glossed at first use. The test is a stated
      shape the author applies — the bullet's judgment-never-a-gate clause
      survives, reconciled with it.
- [ ] AC2: The same bullet bans cairn-internal record identifiers —
      D-/RR-/BC-ids, IP/GP numbers, and doctrine section numbers, with
      `M<NN>` explicitly exempt — from question text and option labels;
      the identifier and its technical justification appear only in the
      chat above the chip.
- [ ] AC3: A worked bad/good pair sits beside the rule: the Candidate A
      reconstruction chosen at the plan gate (labeled a reconstruction,
      not a capture) and its plain rewrite, each at most 4 lines, labeled
      bad and good.
- [ ] AC4: One conduct sentence beside the rule: a gate prompt the user
      flags as unclear is captured verbatim in the same session — as a
      work-log line when a milestone is active, otherwise absorbed into an
      existing candidate ROADMAP row or added as one (search-first).
- [ ] AC5: Every guard assert this milestone adds or edits anchors on the
      shipped file's actual bytes and is registered per the shipped
      per-file bar (or the by-hand check recorded); any absence-shaped
      assert is paired with a positive anchor; the new rule sentences are
      inverted in place per guard-doctrine §1 (invert → suite red →
      restore) and the sweep recorded in the work log; after the worked
      pair lands, every existing guard phrase over `tracking-rules.md` is
      re-grepped for new second occurrences (guard-doctrine §1).
- [ ] AC6: All three suites (`skills/tests`, `scripts/tests`,
      `hooks/tests` via `python3 -m unittest discover` from the repo root,
      exit codes checked individually) and `cairn_validate` pass green.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T1
- AC5 → T3
- AC6 → T4

## Tasks

- [x] T1: Rewrite the accessible-language bullet in
      `skills/shared/tracking-rules.md` (~line 596): two-sentence test,
      id ban with the `M<NN>` exemption, capture-on-flag sentence,
      never-a-gate clause reconciled. Copy anchor phrases from the shipped
      bytes, not the draft (M95 lesson).
- [x] T2: Author the worked bad/good pair beside the bullet — Candidate A
      verbatim from the M128 plan session as the bad case, plain rewrite
      as the good case, ≤4 lines each.
- [ ] T3: Update `TestAccessibleLanguageRule` and the mutation-harness
      registry: re-anchor the four existing asserts, add asserts for the
      new sentences, pair any absence assert with a positive anchor, run
      the §1 inversion sweep and the second-occurrence re-grep; log both.
- [ ] T4: Run the three suites and `cairn_validate` from the repo root;
      fix what reds.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-31: created by /milestone-plan (promoted from the gate-question
  comprehensibility candidate row at the user's request, its stated
  promotion condition).
- 2026-07-31: criteria audit ([O] fresh-context) returned 6 findings — 3 problems: AC2's M-id ban collided with four shipped routing-chip labels (became gate Q1); AC3's "representative" bar unverifiable with no captured exemplar (became gate Q2); AC5's blanking parenthetical unsound for absence asserts (fixed in wording, with the per-file registration bar and the §1 re-grep obligation). AC1/AC4 wording fixes applied; AC6 clean.
- 2026-07-31: plan gate chose exempting `M<NN>` from the id ban over banning it because milestone numbers are the operator's own referent and the ban would red four shipped chip labels; falsified by the operator flagging an M-id-led prompt as unclear (via AC4's capture record).
- 2026-07-31: plan gate chose a reconstructed bad example (Candidate A, picked by the user from three) over a verbatim capture because no flagged prompt exists on disk and the Desktop gate transcripts are not searchable; falsified/replaceable by the first AC4-captured real exemplar.
- 2026-07-31: plan gate chose shipping the capture-on-flag sentence over shipping the rule change alone because the next fix should be evidence-based; falsified by the sentence producing no captures across milestones in which the operator reports further unclear prompts.
- 2026-07-31: T1+T2 — bullet rewritten in place preserving all five pinned anchor lines byte-identical; worked pair authored (Candidate A as bad, labeled reconstruction).

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->
