# M142: The plan gate scales criteria rigor to the deliverable's stakes

**Status:** done (2026-08-15, PR #143 https://github.com/jmgirard/cairn/pull/143)

**Goal:** `/milestone-plan` classifies every deliverable's surface tier and holds internal-tier criteria to a domain-bounded standard.

**Outcome:** Four rules in `/milestone-plan`: the step-2 surface-tier rule
(user-facing vs internal; unclear or spanning → user-facing; tier + reason
in Goal/Scope); the internal-tier criteria standard (a promise quantifies
over a domain its named procedure enumerates directly; repair narrows or
descopes, never widens; governs promises, never guard construction); the
step-3 proportionality audit question; the collision check's checker-regress
clause (deletion recommended, hardening present non-recommended;
promise-widening is the shape however framed). Guarded by
`test_stakes_tier.py`: step-scoped slices, pins plus four whole-slice
equality fixtures (D-103), 27 registered harness blocks.

**Decisions:** D-107 (adoption + regress question beside D-090's door;
annotates D-090, Untouched clause intact; hosted per D-098).

**Review:** Three passes. Pass 1 (3-lens fan-out, 22 scored): defect return
#1 on six guard gaps (D4-D8, P1; 85-90) plus a record fix (D17 88). Pass 2:
defect return #2 — three same-class survivors (R1-R3, 90-93) fired thrash
trigger (b); pins replaced by whole-slice fixtures. Pass 3: 29 probes red,
suites green. Lesson captured; follow-through candidate row added (D2/D19).
