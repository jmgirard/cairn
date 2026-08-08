# M137: Derived figures are pinned or procedural, never free-standing

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** —

## Goal

A derived count or figure written into branch-added prose ships pinned —
beside the procedure that produced it and the commit or dated artifact it
was measured at — or replaced by its derivation; the free-standing
hand-written figure, the record-defect class the 2026-08-08 effort audit
(`references/effort-experiment-notes.md`) found dominant across M113–M136's
actioned review findings, stops being a legal write.

## Scope

**In:** the derived-figures rule in `skills/shared/tracking-rules.md`
"Universal tracking rules" beside the derived-claims rule, under a distinct
name, over that rule's domain; guard-doctrine §6's recorded-counts
paragraph trimmed to defer to it — the M124 story and its citation
retained, the universal-claim corollary's identification and fallback kept,
the §6 counts pointer (`guard-doctrine.md:231`) re-pointed; a D-entry
narrowly superseding D-091 part 3's placement clause; guards, harness
registrations and inversion probes for the added clauses; a full-diff
compliance sweep of the branch's own added figures.

**Out:** any checker or validator over figures — declined at the candidate
row (delete-over-govern; a validator reaches machine-derivable figures
only), revisit only via D-090's trigger. A retroactive sweep of
pre-existing free-standing figures in live tracking files — the
correcting-a-record rule owns each as it is next touched; no milestone.
False or unverified claims, as opposed to stale figures — owned by the
shipped derived-claims rule (M134) and failure-identity rule (M136).

## Acceptance criteria

- [ ] AC1: The "Universal tracking rules" section of
      `skills/shared/tracking-rules.md` states the derived-figures rule,
      under a name distinct from the derived-claims rule's and governing
      that rule's domain (tracking records, code comments, docstrings,
      changelog entries, docs): a derived count or figure written there
      takes one of two forms — pinned, stating beside the figure the
      procedure that produced it and the commit or dated artifact it was
      measured at, or procedural, the figure replaced by its derivation
      with no figure stated — and the free-standing form is not written.
      Evidence: the shipped bytes, read out at review.
- [ ] AC2: Guard-doctrine §6's recorded-counts paragraph defers to the
      tracking-rules derived-figures rule by cross-reference rather than
      stating a parallel weaker form, the M124 evidence story retained with
      its citation
      (`git show a5a7007:cairn/milestones/M124-section-consistency-ledger.md`)
      traveling beside it, and the §6 counts pointer
      (`guard-doctrine.md:231`) re-pointed to the derived-figures rule; the
      universal-claim corollary keeps its identification sentence and its
      unenumerable-domain fallback, deferring only its procedure-grade
      clause. A D-entry narrowly supersedes D-091 part 3's placement
      clause — the operative rule now lives in tracking-rules, widened to
      derived figures across the derived-claims domain and strengthened by
      the pin requirement — with D-091's decision otherwise standing.
      Evidence: the shipped bytes of both files and the appended D-entry.
- [ ] AC3: Every rule clause this milestone adds to
      `skills/shared/tracking-rules.md` or
      `skills/shared/guard-doctrine.md` — candidate sites enumerated by
      `git diff main...HEAD -- skills/shared/tracking-rules.md skills/shared/guard-doctrine.md`,
      read added-line by added-line with each line's rule-clause-or-not
      classification recorded — is pinned by a guard registered in the
      mutation harness, and each such guard reddens under blanking and
      under three inversion-probe kinds (negation, relocation, dispersal),
      the probe commands and results recorded with the procedure that
      produced them.
- [ ] AC4: Every derived figure the branch adds — candidate sites
      enumerated by `git diff main...HEAD`, read added-line by
      added-line — either complies with the rule AC1 states (pinned or
      procedural) or is classified as a site the rule does not govern, the
      per-hit classification recorded; a non-compliant figure in an
      append-only record is remedied by a superseding pinned restatement
      noted in the sweep, never by an edit. The sweep is recorded with its
      command.
- [ ] AC5: The generic profile's verify clean — the three unittest suites
      (`skills/tests`, `scripts/tests`, `hooks/tests`) pass from the repo
      root, each exit code checked singly.

## Coverage

- AC1 → T1
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5
- AC5 → T5

## Tasks

- [ ] T1: Author the derived-figures rule in
      `skills/shared/tracking-rules.md` "Universal tracking rules",
      directly after the derived-claims bullet (`tracking-rules.md:228`):
      distinct name, the derived-claims domain phrase, the two legal forms
      and the free-standing defect named. Grep the repo for surfaces
      restating the recorded-counts rule (M112 lesson) and confirm no
      nearby guard's anchored phrase reflows (M104/M113 lessons).
- [ ] T2: Trim guard-doctrine §6: the recorded-counts paragraph
      (`guard-doctrine.md:234`) defers by cross-reference with the M124
      story and citation retained; the universal-claim corollary
      (`guard-doctrine.md:243`) keeps its identification sentence and
      unenumerable-domain fallback, deferring only its procedure-grade
      clause; the `:231` counts pointer re-points to the derived-figures
      rule. Re-anchor the two existing pins
      (`skills/tests/test_lesson_graduation.py:249`,
      `skills/tests/test_mutation_harness.py:2541`).
- [ ] T3: Append the D-entry narrowly superseding D-091 part 3's placement
      clause: rule relocated to tracking-rules, widened to derived figures
      over the derived-claims domain, strengthened by the pin requirement;
      D-091's decision otherwise stands.
- [ ] T4: Guards + mutation-harness registrations for every added rule
      clause; run blanking and the three inversion-probe kinds (negation,
      relocation, dispersal — the M136 lesson's vocabulary,
      marker-locator scoping) and record AC3's sweep with its per-line
      clause classification.
- [ ] T5: Run AC4's full-diff compliance sweep, classify each added-figure
      hit, fix or supersede per the rule; settle numeric records last
      (guard-doctrine §6); run the three suites singly and record AC5.

## Work log

- 2026-08-08: created by /milestone-plan from the 2026-08-08 candidate row (lineage: effort-audit classification, `references/effort-experiment-notes.md`); promoted under the condition-met reading — the row's condition ("next review whose defect return or ≥80 actioned finding is a stale free-standing figure") read as already satisfied by M134's D14/88 stale work-log count and M135's two record defects, both on the record in the row's own motivation (gate Q1; the logged-deviation reading was the rejected alternative); falsified by showing M134 D14/88 was not a stale free-standing figure.
- 2026-08-08: criteria audit ([O] fresh-context reader, two rounds). Round 1 returned 2 clear-fixes (the §6 corollary's identification and fallback sentences would be lost by a pure cross-reference — kept in §6; AC4 unsatisfiable under IP4 for append-only sites — supersede pathway added), 4 judgments (D-091 relation → gate Q2; rule domain → gate Q3; AC3's clause-hood classification recorded per line — applied; the M124 story's citation travels with it — applied) and a naming observation (distinct rule name — adopted into AC1). Round 2, on the gate-revised wording, returned 1 clear-fix (the `guard-doctrine.md:231` counts pointer becomes determinately wrong under the distinct name — re-point folded into AC2) and 1 judgment (the widened domain exceeded AC4's two-tree pathspec — sweep widened to the full diff; the recorded-exclusion alternative rejected as a gap with no offsetting saving).
- 2026-08-08: plan gate chose narrow supersession of D-091 part 3's placement clause over annotation-with-overlap because a relocation-plus-widening leaving two live statements is the drift class this milestone exists to kill, and D-091 part 2 is the precedent shape (gate Q2); falsified by a case §6's original scope governed that the widened rule does not.
- 2026-08-08: plan gate chose the derived-claims domain phrase over tracking-plus-milestone-records-only because one shared domain keeps the sibling rules coherent and leaves no orphaned D-091 scope (gate Q3); falsified by sweep-judgment cost on docs/comments hits exceeding the pin's value there.
- 2026-08-08: plan chose always-read placement (tracking-rules) over a records-hygiene module home because the rule binds every record write and a conditional read misses most of them (the M134 precedent); falsified by a measured cairn_cost regression attributable to the addition. The no-checker choice is the candidate row's own and was not re-weighed here.

## Decisions

## Review
