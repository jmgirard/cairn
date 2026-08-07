# M136: An observed failure backs a claim only as the failure it is verified to be

**Status:** done (2026-08-06, PR #136 https://github.com/jmgirard/cairn/pull/136)

**Goal:** Close the confounded-measurement class where an observed failure is
read as the behavior under test when it is an artifact of malformed inputs.

**Outcome:** tracking-rules "Universal tracking rules" gains the
failure-identity rule — verify a failure's identity (condition class,
message, signaling site) before the claim; explicit distinguishing step;
a test asserts which failure; a control passes for the claim's reason —
with the "What gets a test" floor requiring the fired condition asserted,
the r-package rendering (`expect_error(class =)`/message matcher), and a
/milestone-implement step-4 pointer. 9 guards + 9 registrations (new
R_PROFILE target); 15 distinct inversion probes RED incl. relocation and
dispersal. Trigger: tidymedia M54 review 2, hosted per D-098.

**Decisions:** none promoted; plan-gate approach choices in the work log
with falsifiers.

**Review:** 23 scored + 3 delta findings. Defect return 1 (D12/82: AC4's
per-probe record absent); actioned: false evidence counts (P1/D11 88,
D10 88), EOF-slice guard defeated by relocation (D1/85), false docstring
scoping (D2/82), vacuous-control neutrality claims (D8/85, D9/82); round-2
delta caught premise dispersal green. All fixed; 14 sub-80 logged.
