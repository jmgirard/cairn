# M58: Rulebook doctrine placement — governance up, validation doctrine out, registry pointer

- **Status:** done (merged 2026-07-16, PR https://github.com/jmgirard/cairn/pull/56)
- **Priority:** normal · **Depends on:** — · **Principles touched:** GP1, GP3

**Goal.** Put each doctrine where it governs (RR01 recs 4/6/9): universal
change-governance up from two profile slots to the core rulebook; the
conditionally-relevant Validation doctrine out to a module; the shape-free
oracle registry gains a declared pointer.

**Outcome.** Dependency-change gate + deprecation-cycle policy now in
Universal tracking rules (generic adopters finally inherit both);
r-package/python keep only mechanical renderings. ~68 doctrine lines moved
verbatim to `skills/shared/validation-doctrine.md` (rulebook keeps a short
reference; M57's references/-page rules stayed in core as "References pages" —
they're universal, refining RR01's pre-M57 cut). Registry pointer: a
numeric-work repo declares where oracle records live in DESIGN.md Conventions;
absence is the audit finding. 3 new guard classes; 7 mutation-registry entries
added/retargeted.

**Decisions.** D-031 — new domain doctrine gets a module, not a rulebook
section; rulebook-reference-only wiring (annotates D-024/D-025/D-029).

**Review.** 5/5 ACs on fresh evidence; suites 165/83/32 OK; fan-out: 1 finding
(F1/85, stale location claims in two references pages) annotated + fixed; 0 others.
