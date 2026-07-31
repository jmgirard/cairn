# M125: Certification loops stop on a repeated defect shape

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** M124
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** m125-shape-repeat-stop

## Goal

End a certification loop by rule when consecutive rounds return the same shape
of defect, converting the obligation to a class-closing structural remedy, so
termination never again requires maintainer override.

## Scope

**In:** a stop rule in `guard-doctrine.md` §8 — two consecutive rounds
returning the same defect shape end the rounds — with the two obligation
sentences amended to acknowledge the new class, the falsifier framing updated,
and the stop rule's own falsifier clause stated; a recorded-counts rule in §6
at verbatim-reproducible grade; a D-entry narrowly superseding D-085's
clause-(i) gloss; pins, harness registration, and §8 ledger regeneration with
the diff read. Absorbs the §8-stop-condition candidate row (M124 §8 round 7,
maintainer override). M125's own §8 certification runs under the stop rule it
ships, as M124's ran under M123's rebuild.

**Out:** applying the stop rule to the plan-time criteria audit → not planned;
the audit is already incremental and closed itself at four passes in M124;
revisit only if an audit loop fails to close on its own. Retiring §8 or
folding it into the review fan-out → standing rejection (RR09 recs 8–9, RR10;
D-085 part 4), untouched — the falsifier clauses stay the retirement path.
New verification apparatus of any kind → D-090 closes that door at this plan
gate; the falsifier-state-disclosure and audit-over-falsifiers rows park
behind it. The disclosing-clause row's window condition is arguably met by
AC2's edit paying its re-anchoring cost; it stays parked behind D-090 rather
than absorbed (gate decision 2026-07-30).

## Acceptance criteria

- [ ] AC1 — `guard-doctrine.md` §8 contains a stop rule: when two consecutive
      rounds each return a reopening finding of the same defect shape — the
      judgment D-064's trigger (b) applies to review returns, applied here to
      certification rounds — the certification convenes no further round. The
      second same-shape finding forms its own finding class, whose one
      confirmation obligation is a structural remedy closing the shape's class
      rather than its instance, confirmed by operation (the suite, the harness,
      the sweeps); the stop, the shape, and the remedy are disclosed in
      work-log lines before `status -> review`. §8's two obligation sentences —
      "a finding that clears both lines is a reopening finding, carrying that
      class's obligation: a further fresh-context round" and "Each class
      carries exactly one confirmation obligation, and no class carries two" —
      are amended to acknowledge this class, so neither ships as a contradicted
      sentence.
- [ ] AC2 — The stop rule states its interaction with §8's falsifier: a
      shape-stopped certification counts toward the falsifier window exactly
      as run — the rounds it convened and their findings count where found,
      and no round it declined to convene is imputed or estimated — and §8's
      framing sentence attributing the falsifier's counted quantity to "the
      two rules above" is updated to count the stop rule among the rules that
      act on the round count. The stop rule carries its own falsifier in
      clause (ii)'s form: if a structural remedy authored under the stop rule
      is later found — by the three-lens review or a subsequent milestone —
      not to have closed its shape's class, the stop rule returns that shape
      to round-opening. Tolerance: one occurrence.
- [ ] AC3 — `guard-doctrine.md` §6 contains a rule that a count recorded in a
      milestone record — a work-log line, a docstring, a comment, or a
      D-entry — carries the procedure that produced it at verbatim-reproducible
      grade: the command as run, or the committed artifact it is read from,
      stated at the granularity that discriminates it from a disagreeing
      record. The rule names M124's measured case: three records disagreeing
      on one count, with the one discriminator — whether bullet paragraphs are
      re-wrapped — stated in none of them.
- [ ] AC4 — `cairn/DECISIONS.md` gains one appended entry recording the stop
      rule and the count rule: it narrowly supersedes D-085's clause-(i) gloss
      ("anything the two reopening rules have not already disposed of"), which
      the stop rule makes incomplete, with everything else in D-085 standing;
      it records the stop rule as a third way a certification ends — beside
      the gate opening at zero unresolved and the falsifier clauses retiring
      rounds across the window — reusing D-064 trigger (b)'s shape judgment
      beyond review returns; and it records the promotion of the ROADMAP's
      §8-stop-condition candidate row at the user's 2026-07-30 decision as a
      logged deviation from that row's second-override promotion condition.
      No existing entry is edited (IP4).
- [ ] AC5 — Every rule this milestone adds to or amends in `guard-doctrine.md`
      is pinned by an assert that fails when that rule is inverted in place;
      each such assert is registered in `skills/tests/test_mutation_harness.py`,
      and every block this milestone registers fails when blanked. An assert
      pins the AC4 entry's existence, so deleting that entry reds the suite.
      The §8 ledger `skills/tests/ledgers/guard-doctrine-8.txt` is regenerated
      from the edited section, its diff read sentence by sentence, and the
      reading recorded in the work log.
- [ ] AC6 — `python3 -m unittest discover` over `skills/tests`,
      `scripts/tests`, and `hooks/tests` each exit 0, and `cairn_validate`
      exits 0.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T1, T4
- AC6 → T5

## Tasks

- [x] T1 — Author §8's stop rule: the new finding class and its one
      obligation; amend the two obligation sentences (`guard-doctrine.md:342-345`,
      `:347-348`) and re-read the licence rationale clause (`:344-345`) for
      coherence under the exception (audit pass 2, finding 1a); update the
      falsifier framing sentence (`:373-375`) and add the stop rule's own
      falsifier clause. Expect breakage in the falsifier-neighborhood pins
      M124 just re-anchored (`test_the_falsifier_counts_where_a_finding_was_found`,
      `..._non_vacuity_floor`, `..._both_tolerances`); 69 of §8's ~85 registry
      blocks carry literal newlines, so re-anchor from shipped bytes (M95).
      Regenerate `skills/tests/ledgers/guard-doctrine-8.txt`, read the diff
      sentence by sentence, record the reading (AC1, AC2, AC5).
- [x] T2 — Author §6's recorded-counts rule; phrase the M124 case so the
      third record (which stated no procedure at all) is not claimed to have
      stated one (audit pass 2, finding 3) (AC3).
- [ ] T3 — Append the D-entry as **D-091** — D-090 is reserved on main by the
      door entry and invisible from this branch, so the naive next id would
      duplicate it (D-067's reserved-not-skipped precedent); supersede
      D-085's clause-(i) gloss narrowly; record the candidate-row promotion
      deviation; run `cairn_validate` and expect the M115 dangling-id
      unmasking batch (AC4).
- [ ] T4 — Pin every added or amended rule by in-place inversion restored
      byte-identical; pin the D-entry's existence; register each block;
      blanking sweep green (AC5).
- [ ] T5 — Full verify: three suites exit 0, `cairn_validate` exit 0;
      `/milestone-implement` step 8 fires §8 certification, which runs under
      the shipped stop rule (AC6).

## Work log

- 2026-07-30: created by /milestone-plan, from the maintainer's request to diagnose and durably fix certification/review thrash.
- 2026-07-30: absorbs the §8-stop-condition candidate row (added 2026-07-30 from M124 §8 round 7's maintainer override); promoted at the user's decision as a logged deviation from the row's second-override promotion condition (IP2: surfaced, not silently overridden).
- 2026-07-30: the absorbed row lives on M124's unmerged branch, not on main — it will land with M124's squash-merge and M124's post-merge hygiene pass removes it then, this line making the removal owed rather than discovered.
- 2026-07-30: criteria audit (fresh-context [O], authored none of the criteria) pass 1 returned 9 findings: 4 clear, all fixed — the obligation-sentence contradiction, the stale "two rules above" framing, "adds" widened to "adds to or amends", the unpinned D-entry; 2 judgment, both to the gate — D-085 supersede-vs-annotate, count-rule inclusion; 3 satisfiable-as-written confirmations.
- 2026-07-30: plan gate (4 questions): plan ahead of M124's review with `Depends on: M124`; close the verification-apparatus program at the door (D-090, appended with this commit); supersede D-085's clause-(i) gloss narrowly rather than annotate; include the count rule at verbatim-reproducible grade.
- 2026-07-30: criteria audit pass 2 over the revised AC1–AC5 (AC6 unchanged, deliberately not re-read): all five satisfiable as written; residual notes carried into task text (licence-rationale re-read, §6 third-record phrasing, re-anchoring expectation). Pass 2 also confirmed the D-090/D-091 reserved-id handling against D-067's precedent.
- 2026-07-30: AC2's stop-rule falsifier clause was authored AFTER pass 2, on pass 2's own finding 1(b) prescription (§8 states the cost of a narrowing and points it at a falsifier clause; clause (ii) is the form) — the audit loop closes at 2 passes rather than re-opening for it, M124's pass-4 precedent.
- 2026-07-30: plan gate chose a shape-repeat stop over a round-count cap, because D-083 measured the round count as the wrong quantity (satisfiable by construction by the rules it polices); falsified by a certification loop that repeats no shape yet still fails to converge on yield alone.
- 2026-07-30: plan gate chose closing the apparatus program at the door (D-090) over stop-rule-only, because the stop rule alone makes each apparatus milestone cheaper while the queue keeps growing — D-057's measured signature; falsified by a shipped-behavior defect class that a parked apparatus candidate would have prevented.
- 2026-07-30: plan gate chose narrowly superseding D-085's clause-(i) gloss over annotating beside it, following the precedent M124's branch set when it superseded D-083 part 3(a) for the same shape — a description made incomplete by a later addition (that entry is unmerged, so it is named here by description, per the M115 lesson); falsified by the rounds-vs-findings defense proving right — a later reader showing the gloss was never incomplete because the stop rule declines rounds, not findings.
- 2026-07-30: plan gate chose verbatim-grade count procedures over cutting the rule, because M123/M124's correction-of-correction churn fed rounds and the discriminator was procedure granularity; falsified by procedure text bloating records at a cost exceeding the adjudication rounds it prevents.
- 2026-07-30: implement gate (1 question): §8's growth recorded as deliberate rather than offset within the section (user decision, M123's precedent); measured 150 -> 177 lines, both by `awk '/^## 8\. /{f=1} /^## 9\. /{f=0} f' skills/shared/guard-doctrine.md | wc -l` (at main and at the T1 commit; no existing paragraph re-wrapped).
- 2026-07-30: T1 — stop rule, window-counting and own falsifier authored as two paragraphs between the reopening rule and the obligations paragraph; both obligation sentences amended, the licence clause gains the no-such-silence sentence, the framing sentence counts the stop rule among the rules acting on the round count; suites 812/332/103 OK, cairn_validate exit 0.
- 2026-07-30: T1 breakage differed from the plan's expectation: the three falsifier-neighborhood pins held; what broke was the framing pin, the sentence-A pin, the obligations proxy (renamed exactly-three -> exactly-four, M124's rename precedent), and clause (ii)'s bare tolerance anchor — false coverage against the stop rule's identical "Tolerance: one occurrence." phrase, so both tolerance asserts are now anchored on their own clause's words ("that class" vs "that shape").
- 2026-07-30: T1 ledger regenerated and its diff read sentence by sentence: 12 added/amended units, every one deliberately authored; 2 removals, both the pre-amendment forms of the two amended sentences; nothing unintended.
- 2026-07-30: T2 — §6 recorded-counts rule appended at section end; the M124 case phrased per audit pass 2 finding 3 — the two records that named a procedure omitted the discriminator, the third named no procedure at all; skills suite 812 OK.

## Decisions

## Review
- 2026-07-30: M124's post-merge hygiene removed the absorbed §8-stop-condition candidate row from the ROADMAP — the removal this log recorded as owed.
- 2026-07-30: M124's review B5 measured shipped §8 at exactly 150 lines — zero headroom under the size M123 chose deliberately — so T1's additions must offset lines within §8 or record the growth as a deliberate choice the way M123's implement gate did; noted here so implement prices it, procedure: `awk` over the §8 span at M124's merge commit.
