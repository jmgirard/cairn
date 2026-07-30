# M123: Rebuild guard-doctrine §8 so its certification loop converges

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP4
- **Branch/PR:** —

## Goal

Rebuild `guard-doctrine.md` §8 so its certification loop terminates on its own
stated rules rather than by maintainer override.

## Scope

**In:** `skills/shared/guard-doctrine.md` §8 — the reopening rule stated on the
reopening object, the mandate boundary, the confirmation-obligation
reconciliation, the evidence paragraph, and the replaced falsifier; the asserts
in `skills/tests/test_fresh_context_readers.py` that pin them and their
`skills/tests/test_mutation_harness.py` registry entries; the `cairn/DECISIONS.md`
entry recording every supersession the rebuild requires.

**Out:** RR09 rec 7's one-shot robustness read beside round 1 → stays the
ROADMAP candidate row it is banked on. `/milestone-implement` step 8's routing →
unchanged; §8 owns the rules and step 8 only fires it. Any repair of D-079,
D-080 or D-081's standing text → IP4 forbids it; this milestone supersedes and
never edits. Any `cairn_validate` mechanization of §8 → rejected at D-067 and
not reopened here.

## Acceptance criteria

- [ ] AC1 — §8 defines the class of finding that does **not** reopen a round as
      description-layer records that a previous round's own fix authored,
      naming at minimum docstrings, comments, work-log lines and record claims;
      the paragraph uses one term for that class, defined at first use, never
      alternating it with an unmarked synonym; and the same paragraph states
      that a fix's code, asserts and fixtures remain ordinary round-opening
      surface. A false claim in an original record still reopens.
- [ ] AC2 — §8 states the two-axis discriminator: subject matter draws what the
      reader checks and the author fixes, citing D-069 and D-070 by id;
      provenance draws what reopens a round. Every occurrence of "certified
      scope" in §8 refers to the subject-matter axis, and the provenance rule is
      nowhere called a certified-scope exclusion. Evidence:
      `grep -n "certified scope"` over §8, each hit's axis named.
- [ ] AC3 — §8 states a mandate boundary: a round reopens only on a finding
      within §8's three named checks, and robustness observations that no
      acceptance-criterion clause pins — mutation survivors, one-directional
      pins, near-miss coverage, fixture weakness — are fixed as ordinary
      milestone work under §§1–7 and the mutation harness without reopening
      certification. §8 states that a finding reopens only if it clears both
      this boundary and AC1's rule.
- [ ] AC4 — §8 assigns each finding class exactly one confirmation obligation: a
      reopening finding obliges a further fresh-context round; a non-reopening
      finding is fixed in place and confirmed by the author re-reading the
      corrected record against the file it describes, recorded in the work log,
      never by a further round. No two sentences in §8 assign both obligations
      to one class, and the shipped sentence "The gate is entered at zero
      unresolved: a discrepancy is fixed and re-certified, never argued down as
      imprecision" is restated accordingly. Evidence: every §8 sentence stating
      a confirmation obligation enumerated with the single class it governs.
- [ ] AC5 — §8's falsifier is replaced by a yield-based pair naming its window,
      both counted quantities and both consequences: (i) over the next three
      guard-authoring milestones that run §8, window closing when the third
      completes, zero shipped-behaviour defects and zero pre-round-1-surface
      findings **returned by** the rounds after each milestone's first — counted
      where a finding was found, never where it was fixed, so AC3's routing
      cannot zero it — retires those later rounds and runs §8 as a single
      certification pass (tolerance: exact zero on both counts, totalled across
      the window); (ii) one record fixed in place under AC1's rule and later
      found false by the three-lens review or a subsequent milestone returns
      that class to round-opening (tolerance: one occurrence).
- [ ] AC6 — one appended `cairn/DECISIONS.md` entry supersedes every D-067,
      D-069 or D-070 claim this rebuild changes — at minimum the falsifier as
      D-082 restored it and D-067's zero-unresolved bar as AC3 narrows it —
      naming each by id. Its ground against D-059 is the checkable fact that the
      replacement's counted quantity is not the round count, never an assertion
      that the change is principled. No existing D-entry is edited.
- [ ] AC7 — §8's evidence paragraph grounds the rule on the record-churn class
      and states separately (a) that under AC1's rule alone M119's round count is
      unchanged, each of rounds 5–9 having returned at least one reopening
      finding, and (b) what AC3's boundary projects for that same record. Every
      count carries the revision it was derived from, and a derived figure
      contradicting a standing D-entry claim gets its own superseding entry.
- [ ] AC8 — Every rule AC1–AC5 adds to §8 is pinned by an assert that fails when
      its block is blanked and fails when the rule is inverted in place. A
      positive block carries its own `test_mutation_harness.py` registry entry;
      a negative or heading-bounded assert registers its positive framing phrase
      instead and records the by-hand check, never the bound. The inversion
      sweep covers §8 whole rather than this milestone's diff, recorded in the
      work log naming the mutation applied and the test that reddened. The two
      asserts whose target text is rewritten —
      `test_section_requires_zero_unresolved_and_forbids_arguing_down` and
      `test_section_carries_its_own_falsifier` — are re-anchored to the shipped
      bytes with their registry entries updated.
- [ ] AC9 — The active profile's `verify` slot passes clean (all three suites)
      and `cairn_validate` reports no new FAIL.

## Coverage

- AC1 → T2, T7
- AC2 → T2, T7
- AC3 → T3, T7
- AC4 → T4, T7
- AC5 → T5, T7
- AC6 → T6
- AC7 → T1, T5
- AC8 → T7, T8
- AC9 → T8

## Tasks

- [ ] T1 — Re-derive each count AC7 cites from a revision named per source
      (M119's work log at `8dace78^` = `016a210`; M114 pass 8 and M121 round 2
      have no named revision yet and T1 identifies theirs). Record each
      derivation and any disagreement with RR09 §2 or D-081 in the work log.
- [ ] T2 — Write §8's two-axis discriminator and the provenance-qualified
      non-reopening class (AC1, AC2), engaging D-069 and D-070 by id.
- [ ] T3 — Write the mandate boundary and its "clears both" composition (AC3).
- [ ] T4 — Restate §8's confirmation-obligation sentences so each class carries
      exactly one, and enumerate them as evidence (AC4).
- [ ] T5 — Write the yield-based falsifier and the evidence paragraph from T1's
      figures (AC5, AC7).
- [ ] T6 — Append the superseding `cairn/DECISIONS.md` entry covering every
      D-067/D-069/D-070 claim T2–T5 changed (AC6).
- [ ] T7 — Author the asserts for AC1–AC5's rules, register positive blocks in
      the mutation harness, record the by-hand check for negative and bounded
      ones, and re-anchor the two rewritten asserts (AC8).
- [ ] T8 — Run the inversion sweep over §8 whole and record it; run the three
      suites and `cairn_validate` (AC8, AC9).

## Work log

- 2026-07-30: created by /milestone-plan.
- 2026-07-30: criteria audit ([O], fresh context, authored none of the criteria) returned 12 findings + 4 set-level conflicts; 8 fixed pre-gate, 3 posed at the gate, 1 (F12, Review-section ownership) fixed to work-log recording.
- 2026-07-30: plan gate chose counting a finding where it was FOUND over counting it where it was fixed, because AC3's routing would otherwise zero AC5(i) by construction; falsified by a window closing at zero counts while the rounds demonstrably returned findings.
- 2026-07-30: plan gate chose author-re-reads-the-record over "verified by the diff and the suite" for non-reopening fixes, because a false docstring passes every suite — §8's own founding diagnosis (D-067); falsified by an in-place fix later found false, which AC5(ii) counts.
- 2026-07-30: plan gate chose one milestone over splitting rules from falsifier, because a half-rebuilt §8 leaves a record chain a later reader must reconstruct — the cost D-082 names; falsified by the plan-owned body missing the 150-line cap or the AC set proving jointly unsatisfiable at implement.
- 2026-07-30: plan gate chose the pre-rebuild §8 to govern this milestone's own certification over the rebuilt rules, because RR09 faults D-079 as "authored by the session whose loop it excuses"; falsified by the loop exceeding M119's nine rounds, at which point the maintainer override is the recorded remedy.
- 2026-07-30: chose subordinating AC3's out-of-mandate list to check 1 over a separate tie-break clause, the gate having declined the tie-break option; falsified by a finding that is neither pinned by an AC clause nor classifiable under §§1–7.
- 2026-07-30: CHECKPOINT — committed with the second criteria-audit pass (over the gate-changed AC1/AC3/AC4/AC5/AC6/AC7/AC8) still running; its findings land as a plan-owned amendment before implement starts, and this line is the honest record that the audit had not reported at commit time.
- 2026-07-30: `cairn_validate` sizing advisory WARNs at 9 acceptance criteria (>7 split tripwire); the gate chose one milestone over a split with the tripwire stated, so the advisory stands unactioned by user decision.

## Decisions

## Review
