# M127: Guard-doctrine §8 is retired whole

**Status:** done (2026-07-31, PR #127 https://github.com/jmgirard/cairn/pull/127)

**Goal:** The certification step is retired whole — no fresh-context reading
of guard descriptions, no rounds, no §8 — ending the loop measured as the
repo's dominant session-cost burn.

**Outcome:** §8 removed; §9 keeps its number, its instrument prose recast
retrospective, the machinery's git home named (main `ba1e6bd`). Implement
clause and rulebook fresh-reader-loop sentence removed; D-067 carve-out kept.
121 registry entries retired with their guard classes; the numbering guard
and §9's re-homed pins live in `test_guard_doctrine_sections.py`. AC1 per-hit
ledger: `references/m127-ac1-ledger.md` (zero operative). Four ROADMAP rows
dropped, RR11 re-cut to BC5, ledger-rollout row restated to git.

**Decisions:** D-095 (the retirement: nine supersessions, D-067 narrowed to
the criteria audit, IP2-logged deviation from D-090's Untouched clause);
D-096 (five record corrections, one batched entry; batching row stays parked).

**Review:** 30 findings, 10 ≥80 actioned: F1 92 (§9 guards swept out by the
whole-file deletion — re-homed; three lenses converged), H2 90/F11 87 (record
corrections), F23 90 (rejected: §6 is the rule's guarded home), F2 85 +
F5/F16/F3/F15 → D-096, H3 80. 19 sub-80 logged. Whole-file-deletion lesson
captured; M60 hook-lifecycle lesson retired by move to `claude-code-hooks.md`.
