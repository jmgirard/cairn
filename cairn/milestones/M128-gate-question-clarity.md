<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M128: Gate questions lead in plain words

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m128-gate-question-clarity · https://github.com/jmgirard/cairn/pull/128

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

- [x] AC1: The "Accessible language on the decision surface" bullet in
      `skills/shared/tracking-rules.md` states the two-sentence test: an
      AskUserQuestion's question text opens with a first sentence saying
      what is being decided in plain words and a second sentence saying
      what happens on each choice, both before any term of art; a term of
      art used after them is glossed at first use. The test is a stated
      shape the author applies — the bullet's judgment-never-a-gate clause
      survives, reconciled with it.
- [x] AC2: The same bullet bans cairn-internal record identifiers —
      D-/RR-/BC-ids, IP/GP numbers, and doctrine section numbers, with
      `M<NN>` explicitly exempt — from question text and option labels;
      the identifier and its technical justification appear only in the
      chat above the chip.
- [x] AC3: A worked bad/good pair sits beside the rule: the Candidate A
      reconstruction chosen at the plan gate (labeled a reconstruction,
      not a capture) and its plain rewrite, each at most 4 lines, labeled
      bad and good.
- [x] AC4: One conduct sentence beside the rule: a gate prompt the user
      flags as unclear is captured verbatim in the same session — as a
      work-log line when a milestone is active, otherwise absorbed into an
      existing candidate ROADMAP row or added as one (search-first).
- [x] AC5: Every guard assert this milestone adds or edits anchors on the
      shipped file's actual bytes and is registered per the shipped
      per-file bar (or the by-hand check recorded); any absence-shaped
      assert is paired with a positive anchor; the new rule sentences are
      inverted in place per guard-doctrine §1 (invert → suite red →
      restore) and the sweep recorded in the work log; after the worked
      pair lands, every existing guard phrase over `tracking-rules.md` is
      re-grepped for new second occurrences (guard-doctrine §1).
- [x] AC6: All three suites (`skills/tests`, `scripts/tests`,
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
- [x] T3: Update `TestAccessibleLanguageRule` and the mutation-harness
      registry: re-anchor the four existing asserts, add asserts for the
      new sentences, pair any absence assert with a positive anchor, run
      the §1 inversion sweep and the second-occurrence re-grep; log both.
- [x] T4: Run the three suites and `cairn_validate` from the repo root;
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
- 2026-07-31: T3 — four new guard tests (10 asserts, all positive presence, no absence asserts), five registry entries; §1 inversion sweep: 6/6 negations red, restore hash-verified; second-occurrence re-grep over every guard literal vs tracking-rules.md: 0 multiplicity changes.
- 2026-07-31: T4 — skills 704 OK, scripts OK, hooks 103 OK (exit codes checked individually), cairn_validate all checks passed (2 standing advisories); status → review.
- 2026-07-31: correction (review O9): the T3 line's "five registry entries" is wrong — the T3 commit added four; three more landed at review triage, seven total for this milestone.
- 2026-07-31: correction (review O12): T4's "2 standing advisories" mischaracterized them — both are `work-log format` WARNs on this file's own wrapped plan-session entries, M128's own, not pre-existing.
- 2026-07-31: review triage — by-hand check (O10) recorded: all 12 asserted phrases in the four new guard methods occur 0× in origin/main and exactly 1× in HEAD's tracking-rules.md (script in review session), so each fails against pre-milestone content.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review

Evidence (fresh, 2026-07-31, review session):

- AC1: `sed -n '596,625p'` fresh read — two-sentence test stated (first
  sentence decides in plain words, second states consequences, both before
  any term of art), gloss clause intact, never-a-gate clause present
  reconciled as author judgment. ✓
- AC2: same read — D-/RR-/BC-ids, IP/GP numbers, section numbers "stay out
  of question text and option labels", `M<NN>` explicitly exempt,
  identifier + justification located above the chip. ✓
- AC3: worked pair present beside the rule, labeled "reconstructs the
  observed failure shape (M128), it is not a capture"; Bad 3 lines,
  Good 3 lines (≤4 each). ✓
- AC4: capture sentence present: flagged prompt captured verbatim same
  session — work-log line when active, else absorbed into an existing
  candidate row or added as one (search-first). ✓
- AC5: five registry entries live (mutation harness in skills suite,
  green = blanking reds); review-side inversion sweep 6/6 negations red,
  restore hash-verified; 1,943 guard literals re-grepped, 0 multiplicity
  changes vs origin/main; all 10 new asserts positive presence. ✓
- AC6: skills OK (exit 0) · scripts 332 OK (exit 0) · hooks 103 OK
  (exit 0) · cairn_validate all checks passed, 2 standing advisories. ✓

Consistency gate: cairn_validate exit 0; no IP/GP change → cairn_impact
skipped; generic profile → no toolchain checks. The 2 WARNs are this
file's own wrapped plan-session work-log lines (work-log format), left
as history per IP4.

Fan-out (3 lenses + scorer): [O] diff-bug 28 findings, [S] blame-history
6, [S] prior-review 0 (probe: no PR threads; archive clean — its own
sweep reproduced AC5's 0-multiplicity result). Scorer actioned 6 (≥80):

- O9 (90): record said "five registry entries", diff added four → fixed,
  correcting work-log line appended.
- O12 (88): "standing advisories" are M128's own two wrapped work-log
  lines → characterization corrected (lines left unedited, IP4).
- O25 (85): worked-pair guard pinned only each quote's first line — the
  Good's payload sentence was deletable green → payload line now asserted
  + registered.
- O10 (83): 10 asserts, 4 registry entries, no recorded by-hand check for
  the rest → by-hand check run and recorded (12 phrases, 0× main /
  1× HEAD); 3 registry entries added.
- O8 (82): capture sentence's operative middle clause ("a work-log line
  when a milestone is active") unpinned → asserted + registered.
- O6 (80): id-ban assert pinned the verb but not its object ("question
  text and option labels" rewritable green) → assert widened to span
  object + exemption; registered.

Fixed opportunistically while editing the pinned line: O2/O15 (74/62) —
the Good example's second sentence now states a consequence of each
option and says "ten records" (D-095 touches ten, not eight).

Logged sub-80 (excluded from actioned list, IP3): 24 findings — O1/B1/B3
(78, two-sentence predicate undefined for labels; the plain-words scope
sentence still governs them), O7 (78, "any term of art" unpinned), O5
(76, never-a-gate sentence unpinned), O2 (74, fixed above), O15 (62,
fixed above), O20 (52), O23 (48), B4 (48), O4 (45, archives retain via
git), O11 (45), O14 (42), B6 (40), O18 (35), O16 (30), O17 (30), O19
(32), O24 (28), O13 (25), O22 (25), O3 (20), O21 (20), O26 (20), O28
(12), O27 (10). Post-fix: suites re-run green; by-hand check PASS.
