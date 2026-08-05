<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below.

     DRAFTING BUDGETS (M99) — guidance, not a gate; the only size check that
     can fail is cairn_validate's <150 over the plan-owned body.
     Goal 7 · Scope 26 · AC 28 · Coverage 11 · Tasks 25 — each the measured p75
     over 99 milestone files, so three drafts in four already fit, and the
     fourth is the one that thrashed.
     ## Decisions reserves nothing: D-074 made it cap-exempt, so it costs the
     budget nothing and plan still spends none of it.
     (Redistributing the ≥21 lines it used to reserve is a ROADMAP candidate,
     deliberately not done at M118.) Together with this preamble they fit
     under the cap with room to spare — the counter prints the running total,
     so no figure here describes this block's own length (it would change each
     time the block was edited, and drifted twice when it did). Every figure is
     measured, never assumed (D-049). /milestone-plan step 4 names the counter. -->
# M134: Branch-added behavior claims are derived from the artifact, not the author's model

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP1, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m134-derived-claims · https://github.com/jmgirard/cairn/pull/134   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Branch-added prose claims about an artifact's behavior are derived from the
artifact at write time — never composed from the author's model — with the
rule stated where every implement session reads it.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A three-clause derived-claims rule in the always-read rulebook
(derive-don't-compose, restatement-is-not-written, pointer-over-enumeration),
covering all branch-added prose that states what an artifact does or contains
— tracking records, code comments, docstrings, changelog entries, docs. A
one-line pointer in `/milestone-implement` step 4 at the checkpoint-commit
bullet. A changelog-claims sentence in the "What gets a test" floor. Trimming
guard-doctrine §6's narrow evidence-counts copy to a cross-reference, and
dispositioning the other pre-existing overlapping sites the criteria audit
named. Guards, mutation-harness registrations, and two-probe inversion for
every new rule sentence. D-090 door: the deliverable is conduct prose, not an
instrument; the shipped-behavior defect in D-098's form is that
`/milestone-implement` instructs write-time conduct while the strong
derive-don't-compose rule sits only in guard-doctrine §6, a module loaded
solely for guard authoring — so a session writing NEWS, comments, or evidence
prose never meets it; measured downstream cost: intraclass M103, two review
returns, four actioned defects, all prose-about-code (D-098's M102 shape).

**Out:** Any review-time enumeration or audit of the diff's prose claims —
the documented failure family (M127's retired certification, RR06's
author-verification diagnosis, M114's detector returns); rejected, see the
work-log alternative record. Any new checker, instrument, or certification
step (D-090). Fixing intraclass M103's four defects → the intraclass session.
Per-repo checker retrofits (e.g. intraclass's doc-claims checkers) → those
repos' own tracking.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: `skills/shared/tracking-rules.md`'s "Universal tracking rules"
      section states the derived-claims rule in three operative clauses, each
      a sentence of its own: (a) a prose claim the branch adds about what an
      artifact does or contains — in tracking records, code comments,
      docstrings, changelog entries, or docs — is written against an
      execution's observed output or a same-session read of the artifact,
      never composed from recollection or expectation; (b) branch-added prose
      that restates what its cited artifact already shows is not written — a
      cross-reference replaces it; (c) a claim that would enumerate an
      artifact's members is written as a pointer to the artifact, except
      where the enumeration is itself the deliverable. Each clause is pinned
      by a guard registered in the mutation harness and verified by the M131
      lesson's two probes — subject-and-predicate transposition with a
      whole-bullet blank as control, and deletion of each sentence's tail
      beyond its registered block — with the runs recorded in the Review
      section.
- [x] AC2: The four pre-existing overlapping sites the criteria audit named —
      `tracking-rules.md`'s cap-remedy cross-reference line, its
      verify-edit-landed rule, `records-hygiene.md`'s restatement bullet, and
      guard-doctrine §6's evidence-counts-from-command-output line — are each
      dispositioned in the Review section: trimmed to a cross-reference to
      the central rule, or recorded as a distinct rule with the distinction
      stated; guard-doctrine §6's evidence-counts line is in the
      trimmed-to-cross-reference class.
- [x] AC3: `/milestone-implement` step 4's checkpoint-commit bullet carries a
      one-line cross-reference to the derived-claims rule, pinned by a
      registered guard and verified by the same two probes.
- [x] AC4: The "What gets a test" floor gains one sentence: a changelog entry
      asserting a behavior requires a test that fails without that behavior,
      or the entry narrows to what a named test enforces — pinned by a
      registered guard and verified by the same two probes.
- [x] AC5: The `LESSONS.md` lines for M114 (work-log entries state
      decision-relevant facts, never characterizations) and M116 (re-read the
      guard as you write the claim, or write a pointer instead of an
      enumeration that can drift) are each tested for coverage against the
      shipped rule and dispositioned per D-051's ownership criterion —
      retired by moving content, trimmed to the uncovered remainder, or kept
      with the reason stated — one work-log line per disposition.
- [x] AC6: The generic profile's verify slot is clean: all three suites green
      from the repo root with exit codes checked separately, and
      `python3 scripts/cairn_validate.py` exits 0.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T6
- AC6 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Author the three-clause rule in `tracking-rules.md` "Universal
      tracking rules", anchors copied from the target's shipped bytes (M95);
      after editing, grep that every nearby guard's asserted substring is
      still contiguous on one line (M104).
- [x] T2: Guards for the three clauses in `skills/tests/`, mutation-harness
      registrations, and the two-probe inversion runs (M131 lesson); read via
      `Path.read_text` (M100).
- [x] T3: Disposition the four overlapping sites (trim guard-doctrine §6's
      evidence-counts line to a cross-reference; trim or distinguish the
      other three), re-anchoring any guard the trims reflow.
- [x] T4: One-line pointer in `/milestone-implement` step 4's
      checkpoint-commit bullet + guard + registration + probes.
- [x] T5: Changelog-claims sentence in "What gets a test" + guard +
      registration + probes.
- [x] T6: Coverage-test and disposition the M114 and M116 LESSONS lines per
      D-051 ownership; work-log line each.
- [x] T7: Full three-suite run with per-suite exit codes, `cairn_validate`,
      `cairn_budget` on this file.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-04: created by /milestone-plan, prompted by intraclass M103's second prose-only review return (four actioned defects, all narration drifting from surviving code; sixth recorded recurrence of the class in that repo).
- 2026-08-04: criteria audit ([O] fresh reader) returned 12 findings over the 4-AC draft — §6 delete-first mis-cite, unbounded one-home universal, under-specified inversion probes, undefined surface width, D-039 mis-cite, unfalsifiable anchor, missing behavior delta, ambiguous changelog reading, unreachable enforcement-retirement, weak M114 coverage premise, misleading definite description, door argument not in D-098's form — all disposed: 8 fixed by rewording into the AC set above, 4 became the gate's questions.
- 2026-08-04: plan gate chose the generator-side write-time rule over review-time enumeration/audit of the diff's prose claims because the audit family is a documented failure (M127 retired certification for generating correction cascades; RR06 diagnosed author-enumeration as verifying against the generative model; M114 burned three returns on detector enumeration); falsified by the write-time rule shipping and a later milestone's review still finding composed-from-model prose defects at the same rate.
- 2026-08-04: plan gate chose central-rule-plus-step-4-pointer over central-only because an authoring step exists to anchor to (D-048's per-skill precedent; D-039 chose central-only for want of such a step); falsified by the pointer measurably not changing where drift defects arise.
- 2026-08-04: plan gate chose all-branch-prose surface over tracking-records-only because the motivating defects sat in NEWS, comments, and @details; falsified by the wide wording proving unenforceable or over-triggering on legitimate doc prose.
- 2026-08-04: plan gate chose trimming guard-doctrine §6's narrow evidence-counts copy over leaving both because two statements of one rule is the drift pattern in scope (step-0 one-home); falsified by the trim reddening guards in a way that costs more than the duplication.
- 2026-08-04: D-090 door surfaced and answered without supersession, per D-098's route: shipped-behavior defect stated in the Scope block; the deliverable adds no instrument.
- 2026-08-04: T1 done — three-clause rule inserted after the verify-edit-landed bullet in Universal tracking rules (pure insertion, no adjacent reflow); all four anchor phrases grep-unique across skills/; suite green.
- 2026-08-04: T2 done — test_derived_claims.py (4 tests, section-sliced with both bounds asserted) + 4 harness registrations; six probe mutations each RED (subject transposed, predicate negated, whole-bullet blank control, tail-beyond-block deleted for each clause), target restored byte-identical.
- 2026-08-04: T3 done — guard-doctrine §6's evidence-counts clause (unpinned, verified by grep over skills/tests/) trimmed to a cross-reference to the central rule; the other three sites are guard-pinned distinct rules (cap remedy, edit-landing verification, cap-time compression) left in place, distinctions to be recorded in Review per AC2; suite green after the trim.
- 2026-08-04: T4+T5 done — step-4 pointer sentence in /milestone-implement and changelog-claims sentence in the What-gets-a-test floor, each on one physical line, guarded, registered; eight probe mutations each RED (subject transposed, predicate negated, whole-line blank control, tail deleted, per sentence), targets restored byte-identical.
- 2026-08-04: T6 disposition (M116 line): RETIRED by ownership — its remedy is clause (a) same-session read plus clause (c) pointer-over-enumeration, now owned by the derived-claims rule; line deleted, no covered remainder.
- 2026-08-04: T6 disposition (M114 line): KEPT — it forbids characterizations even when derived from true measurements, a judgment the derived-claims rule does not make; no trimmable half leaves the teaching intact.
- 2026-08-04: T7 done — skills/scripts/hooks suites green with per-suite exit 0, cairn_validate exit 0, budget 138/149; status to review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

Review pass 1, 2026-08-04 (same-session; evidence by command, never recall).

- AC1: `test_derived_claims` 6/6 ok (section-sliced, both bounds asserted; heading uniqueness checked). Six probe mutations over the three clauses each RED — subject transposed, predicate negated, whole-bullet blank control, tail-beyond-registered-block deleted per clause — targets restored byte-identical (probe runner re-run at review). Four harness registrations blank-verified by the suite's `TestRegisteredGuardsFailWhenBlanked`.
- AC2 dispositions (the four audit-named sites): (1) guard-doctrine §6 evidence-counts line — TRIMMED to a cross-reference naming the central rule (was unpinned; verified by grep over `skills/tests/` before the trim). (2) tracking-rules cap-remedy line ("cross-reference a durable record rather than restate") — DISTINCT: a weight-cap remedy prescribing what to do when over cap, not a write-time authoring bar; guard-pinned, left verbatim. (3) tracking-rules verify-edit-landed rule — DISTINCT: verifies an edit landed before its record, not that a claim's content was derived; the new bullet sits directly after it as its authoring-side sibling. (4) records-hygiene compress bullet — DISTINCT: cap-time compression conduct (which section to cut, replacing already-restated content); guard-pinned, left verbatim.
- AC3: `test_implement_step4_carries_the_pointer` ok; four probe mutations RED (subject, predicate, whole-line blank, tail), restore verified.
- AC4: `test_changelog_claims_are_documented_claims` ok (What-gets-a-test section slice); four probe mutations RED, restore verified.
- AC5: work log carries one disposition line per lesson (2 lines, grep-verified); `grep -c M116 cairn/LESSONS.md` = 0 (retired by ownership), M114 line present unchanged (kept, reason logged).
- AC6: skills OK exit 0 · scripts exit 0 · hooks exit 0 · `cairn_validate` exit 0.
- Consistency gate: `cairn_validate` all checks passed (16 PASS, 8 advisories OK); generic profile names no toolchain checks (clean no-op); no DESIGN.md principle changed (`Principles touched: GP1, GP4` are worked-under, not edited) — `cairn_impact` skip.
