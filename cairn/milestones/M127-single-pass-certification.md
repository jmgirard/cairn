# M127: Guard-doctrine §8 becomes a single-pass instrument

- **Status:** planned
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP4, GP1
- **Branch/PR:** —

## Goal

One fresh-context certification round per guard-authoring milestone, with
no rule under which a second is convened — verification that cannot loop.

## Scope

**In:** Rebuild `skills/shared/guard-doctrine.md` §8 (lines 265–443 at
plan time) to single-pass form: the fresh-context [O] reader and its three
checks stay, run once before `status -> review`; every finding is fixed
once and confirmed by operation (suite, harness, sweeps) or by
`/milestone-review`'s three-lens fan-out at the merge gate. Delete the
machinery that governed reconvening: the reopening-finding obligation, the
fix-authored-record provenance axis, the shape-repeat stop (M125), and
falsifier clauses (i) and (ii). Rewrite the certified-scope paragraph
(D-069) to its single-pass form — the subject-matter axis stays, the
round-to-round convergence rationale goes. Carry clause (iii) over as the
sole falsifier (retire-whole). Update or retire every test surface pinning
the retired machinery; regenerate the §8 section ledger. Append the
superseding D-entry; dispose the mooted ROADMAP rows.

**Out:** the review fan-out and the plan-time criteria audit — unchanged
by explicit gate choice (2026-07-31, Q3). Adopting RR11 BC5 → stays a
parked candidate row, re-cut by this milestone to BC5 only. A
correction-batching rule → candidate row banked at this plan commit,
promoted only if the cascade survives the rebuild. New apparatus or new
doctrine of any kind → nowhere; D-090's door stands and this milestone
only subtracts.

## Acceptance criteria

- [ ] AC1: Shipped `guard-doctrine.md` §8 obliges exactly one
      fresh-context certification round before `status -> review` and,
      read whole, provides no rule under which a second round is
      convened: the reopening-finding obligation, the fix-authored-record
      provenance axis, the shape-repeat stop, and falsifier clauses (i)
      and (ii) are absent; the certified-scope paragraph is rewritten to
      its single-pass form (subject-matter axis retained, round-to-round
      rationale gone); and every finding class the rebuilt section names
      carries a confirmation obligation that is not a further round.
- [ ] AC2: The rebuilt §8's sole falsifier is clause (iii) carried over
      verbatim in substance — retire-whole on its four counted
      quantities, its three-milestone window, and exact-zero tolerance —
      pinned by a mutation-harness-registered guard that reds when the
      falsifier is deleted.
- [ ] AC3: Every test file whose asserts, controls, or comments pin the
      retired machinery — found by the AC6 search over `skills/`, never
      by a fixed list — is updated or retired with its registry entries;
      `skills/tests/ledgers/guard-doctrine-8.txt` is regenerated from the
      rebuilt section; and all three suites pass from the repo root with
      each exit code checked.
- [ ] AC4: A registry-derived polarity sweep over the rebuilt §8,
      excluding the section-ledger guard from red-detection, reds on
      every subject it derives, with the denominator disclosed as every
      derived subject (none reported untested), recorded in a work-log
      line carrying the command at verbatim-reproducible grade.
- [ ] AC5: A superseding D-entry records: the 2026-07-31 user mandate;
      that the remedy is falsifier clause (i)'s own, fired ahead of its
      measured window as a deliberate deviation (IP2); the override of
      RR10's recorded rejection of "decreeing a single pass" (D-085);
      the D-090 door ground — its Untouched clause, a falsifier's firing
      removes apparatus; the affected clauses of D-069, D-070, D-083,
      and D-091; and the candidate-row disposals, so D-090's by-name
      parking reference resolves. `cairn_validate` green.
- [ ] AC6: The mixed-round-precedence and falsifier-state-disclosure
      candidate rows leave the ROADMAP with dispositions recorded; the
      RR11 row is re-cut to BC5 only with BC6's mooting recorded; the
      audit-over-falsifiers row's condition is re-stated against the
      rebuilt section; and a search for "reopening finding",
      "shape-repeat", and "fix-authored record" returns zero hits under
      `skills/` and in `README.md` — run as review evidence, never
      shipped as an `assertNotIn`.

## Coverage

- AC1 → T1, T6
- AC2 → T1, T2
- AC3 → T2, T3
- AC4 → T3
- AC5 → T4
- AC6 → T5

## Tasks

- [ ] T1: Rebuild §8 (`skills/shared/guard-doctrine.md:265-443`) to
      single-pass form, carrying clause (iii) over as sole falsifier;
      author anchors from shipped bytes, never from the draft (LESSONS
      M95).
- [ ] T2: Sweep `skills/` for the retired terms; update or retire every
      pinning test and registry entry found (known at plan time:
      `test_fresh_context_readers.py`, the §8 registrations in
      `test_mutation_harness.py`, `test_section_ledger.py`,
      `test_delegation_warrant.py:165`); regenerate
      `skills/tests/ledgers/guard-doctrine-8.txt`.
- [ ] T3: Run all three suites from the repo root (each exit code
      checked) and the polarity sweep with the ledger-guard exclusion;
      record the sweep's work-log line (AC4).
- [ ] T4: Author the superseding D-entry; preview verbatim in chat
      before the commit that lands it.
- [ ] T5: ROADMAP row disposals and re-cuts (AC6); run and record the
      AC6 search as review evidence.
- [ ] T6: Single-pass certification of the rebuilt section under its own
      rebuilt rule — one round, findings fixed once — before
      `status -> review`.

## Work log

- 2026-07-31: created by /milestone-plan.
- 2026-07-31: plan-gate criteria audit ([O] fresh reader, fresh context) returned 13 findings; 11 fixed into the criteria wording as the audit prescribed (D-069 disposition added to AC1; clause-(iii) carry-over replaces an undefined "zero findings" in AC2; AC3 search-scoped rather than file-listed; ledger-guard exclusion added to AC4; RR10-override and D-090-Untouched grounds named in AC5; third mooted row and the §7 grep collision folded into AC6), 2 became gate questions (cut depth; correction batching).
- 2026-07-31: plan gate chose single-pass §8 over retiring the step whole because round 1 demonstrably still yields (M126's certification found a real shipped defect; this plan's own audit found 13 findings); falsified by clause (iii)'s window returning zero findings across three §8-running milestones.
- 2026-07-31: plan gate chose single-pass over keep-multi-round-and-wait because the post-M125 evidence (M126: 460 turns, 19 agents, multi-round certification the day after the stop rule shipped) shows the loop still burns; falsified by a shipped-behavior defect traced to a finding a reconvened round would have surfaced.
- 2026-07-31: plan gate chose no-new-batching-rule over adding the sentence now because the rebuild removes the cascade's generator and D-090 counsels against preemptive doctrine; falsified by two or more correcting D-entries landing in a single milestone after M127 ships (the banked row's condition).
- 2026-07-31: plan gate chose keeping the review fan-out and criteria audit over trimming them because both are single-shot instruments and the measured burn is loop turns, not spawns; falsified by cairn_cost showing a regression attributable to spawn volume (the existing spawn-cap row's trigger).
- 2026-07-31: plan gate chose keeping RR11 BC5 parked over folding it in because a subtractive milestone should not add doctrine; falsified by a quantified-claim defect shipping in a guard-authoring milestone before BC5 lands.

## Decisions

## Review
