# M112: Soften the Fable warning — neutral token-cost framing, lower recommend bar, gate retained

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP4
- **Branch/PR:** m112-soften-fable-warning · https://github.com/jmgirard/cairn/pull/112

## Goal

Rewrite cairn's anti-Fable framing from a billing-hazard warning into neutral
token-cost guidance — Fable is no longer pay-on-demand — while keeping the
per-instance RB/RR approval gate and lowering the bar for recommending it.

## Scope

**In:** neutralize the cost-hazard wording in `skills/shared/tracking-rules.md`,
`skills/milestone-brief/SKILL.md`, and `skills/milestone-implement/SKILL.md`;
lower the recommend bar so escalation may be offered on a tripwire hit *or* for
a genuinely hard question the session cannot confidently settle (the three
tripwires stay the canonical must-offer cases); append D-062 superseding D-004's
pay-per-use premise; a prose-guard pinning the retained per-instance approval
gate and RB/RR-only escalation path; and README.md's Fable framing (L201, L259).

**Out:** removing or weakening the per-instance approval gate or the RB/RR-only
escalation path (both retained — that is the point of the guard); adding a
fourth tripwire category (considered at the plan gate, not chosen); any change
to `/design-interview`'s Fable recommendation (D-014, already positive,
untouched); editing D-004 itself (IP4 — superseded, never edited).

## Acceptance criteria

- [x] AC1: Across the three skill files and README.md, the billing-hazard
      phrases — "token-billed pay-per-use", "no standing authorization exists",
      "never a silent cost", "costs real money", "paid escalation" — are gone,
      replaced by neutral framing (Fable uses more tokens than Opus; no longer
      pay-on-demand), while each file's per-instance explicit-approval
      requirement (and README's per-instance-yes point) remains present in text.
- [x] AC2: `tracking-rules.md`'s RB-tripwire rule states escalation may be
      offered on a tripwire hit OR for a genuinely hard question the session
      cannot confidently settle, naming the three tripwires as the canonical
      must-offer cases; `milestone-implement/SKILL.md` no longer forbids
      offering escalation absent a tripwire hit.
- [x] AC3: `cairn/DECISIONS.md` gains D-062 recording the policy change,
      retaining D-004's per-instance RB/RR gate on token-cost grounds and the
      lowered recommend bar; its heading back-references D-004; `git diff`
      shows D-004's own text unedited.
- [x] AC4: A prose-guard asserts milestone-brief's per-instance explicit-approval
      gate and the RB/RR-only escalation path survive, registered in the
      mutation harness (`test_mutation_harness.py`); it reds when either
      invariant is blanked.
- [x] AC5: `python3 -m unittest` over the skills suites passes clean and
      `cairn_validate` reports no failures.

## Coverage

- AC1 → T1, T6
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: Neutralize the cost-hazard framing in `tracking-rules.md:641-646`,
      `milestone-brief/SKILL.md:13-16,32`, and any incidental spot; preserve
      each file's per-instance approval wording verbatim in intent.
- [x] T2: Relax the recommend bar — `tracking-rules.md:657-658` (tripwire-hit
      OR genuinely-hard-question) and `milestone-implement/SKILL.md:47-51`
      (drop the "never offer without a tripwire hit" prohibition, keep the
      three tripwires canonical).
- [x] T3: Append D-062 to `cairn/DECISIONS.md` (heading back-references D-004);
      repoint skill citations to cite D-062 alongside D-004 where the premise
      is stated. Leave D-004 unedited.
- [x] T4: Add/extend a prose-guard for the retained approval gate + RB/RR-only
      path; register its exemplar block in `test_mutation_harness.py` and
      confirm the completeness meta-test passes.
- [x] T5: Run `python3 -m unittest` (skills suites) and `cairn_validate`; fix
      to green.
- [x] T6: Rewrite README.md's Fable framing — L201 "costs real money" → neutral
      token-cost, L259 "paid escalation" → "escalation" — keeping the
      per-instance-yes point. (Added at review as a gated scope amendment.)

## Work log

- 2026-07-24: created by /milestone-plan.
- 2026-07-24: amendment (review) — folded README.md into scope (blame-history reviewer flagged L201/L259 still 'token-billed'/'paid escalation'); AC1 + Scope + Coverage amended, T6 added, both lines rewritten to neutral framing; suite 608 OK, cairn_validate clean.
- 2026-07-24: T5 — verify slot clean: python3 -m unittest 608 OK; cairn_validate all checks pass; budget 82/149. Status → review.
- 2026-07-24: T4 — added test_fable_gate_retained.py (per-instance gate + RB/RR-only path invariants) and registered its 6 blocks in the mutation harness; suite green (608), harness confirms each block reds its guard.
- 2026-07-24: T3 — verified D-062 present (heading back-references D-004), D-004 unedited, D-062 cited in all three skills; no new file change beyond milestone (D-062 landed in the plan commit, citations in T1/T2).
- 2026-07-24: T2 — lowered the recommend bar in tracking-rules RB-tripwire block + milestone-implement step 3 (tripwire-hit OR genuinely-hard-question; three tripwires stay must-offer); gate retained; suite green (604).
- 2026-07-24: T1 — neutralized cost-hazard framing in tracking-rules, milestone-brief (framing + gate reminder); hazard phrases gone, per-instance approval wording retained; suite green (604).

## Decisions

## Review

_2026-07-24 · PR #112 · no Driving RR (projection-vs-outcome no-ops)._

**Evidence per criterion (fresh):**

- AC1 ✓ — grep of the three skill files AND README.md for "token-billed",
  "pay-per-use", "no standing authorization", "never a silent cost",
  "costs real money", "paid escalation" returns nothing; neutral framing
  present ("no longer pay-on-demand", "typically uses more tokens than Opus").
  Approval wording retained: `per-instance approval gate` (rulebook),
  `explicit user approval, every time` (milestone-brief), and README's
  per-instance-yes point (L259). README amended at review (T6, scope
  amendment).
- AC2 ✓ — `tracking-rules.md:660` "may be offered on a tripwire hit OR for a
  genuinely hard question", `:662` "three tripwires remain the cases where it
  must be offered"; `milestone-implement/SKILL.md:50-51` reworded, the
  "never offer escalation without a tripwire hit" prohibition removed.
- AC3 ✓ — D-062 at `DECISIONS.md:1859`, heading back-references D-004
  ("supersedes D-004's premise"); `git diff origin/main..HEAD -- DECISIONS.md`
  shows no `±` line touching D-004's body; D-062 cited in all three skills.
- AC4 ✓ — `test_fable_gate_retained.py` present; 6 blocks registered under
  `guard="test_fable_gate_retained"`; `TestRegisteredGuardsFailWhenBlanked`
  and `TestRegistryCompleteness` pass — each block reds its guard when blanked
  (no false coverage), the file is registered.
- AC5 ✓ — `python3 -m unittest discover -s skills/tests` → 608 OK;
  `cairn_validate` → all checks pass (23 PASS/OK, 0 FAIL).

**Consistency gate:** `cairn_validate` exit 0, all checks pass. Profile
`generic` → no toolchain `consistency-gate` checks (clean no-op). No DESIGN
principle changed (IP2/IP4 worked-under, not modified) → `cairn_impact` skipped.
