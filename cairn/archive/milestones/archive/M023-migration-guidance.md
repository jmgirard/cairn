# M23: Migration-protocol §2 guidance hardening — done (2026-07-12)

**Goal:** Fold the M20 ackwards pilot's remaining migration gaps into
`/cairn-init` §2 so the next real migration of a mature repo doesn't re-hit them.

**Outcome:** Hardened the `skills/cairn-init/SKILL.md` migration protocol:
- Step 5 — rich living `DESIGN.md`: keep verbatim as `cairn/DESIGN.md` +
  re-record only still-governing decisions (Compromise A, default) / full
  extraction on request (B); embedded hard-constraint invariants routed to
  `/design-interview` rather than IP/GP-formalized at migration time. (G3/G5)
- Step 6 — "Reference sweep — repoint or note": in-code refs to relocated
  tracking files + redistributed CLAUDE prose naming entombed skills, two
  dispositions (repoint / note-and-leave). (G6/G10)
- Post-move hygiene: prune stale per-file `.Rbuildignore` entries (§1 + step 6);
  §0 Lineage B detection widened to a forward-only ROADMAP + explicit status /
  `Current focus` slot. (G7/G2)
- New guard test `test_migration_guidance.py` (5 cases) locks the phrase
  invariants; full suite green (56 skill + 33 script).

**Decisions:** none new (D-005 governs milestone history, not a living DESIGN;
D-013/D-014 reinforced). **Review:** 4/4 criteria verified with fresh evidence;
independent two-lens review (Opus diff-bug + Sonnet blame-history) = 0 findings.

**PR:** https://github.com/jmgirard/cairn/pull/20
