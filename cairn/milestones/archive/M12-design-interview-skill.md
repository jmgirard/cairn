# M12: Design-interview skill (facts → principles) — done 2026-07-11

**Goal:** Ship a standalone `/design-interview` skill running the two-phase
(facts → principles) DESIGN-elicitation interview from the openac pilot notes.

**Outcome:** New `skills/design-interview/SKILL.md` encoding notes items
1–11: Phase 1 elicits facts and banks proto-principles (never classifies);
a checkpoint seam; Phase 2 mines git/domain/banked sources for candidates,
each pre-classified (IP/GP/skip) with a recommendation, stress-tested against
Phase-1 answers, written IP-block-first. `/cairn-init` hands off to it.
Guard test `test_design_interview.py` (12 cases) locks the invariants; suite
17/17. Documented in README + CHANGELOG. PR #10.

**Key decisions:**
- D-013: standalone skill (not folded into cairn-init) — reusable to deepen
  an existing DESIGN; cairn-init seeds then hands off.
- D-014: recommends running the session on Fable (soft steer). The openac
  pilot found Opus's questions too technical; Fable was markedly better.
  User's per-instance model choice — no cairn-spawned Fable subagent, so
  D-004 stands; "orchestrator: Opus" default holds for every other skill.

**Review:** all 6 criteria met (criterion 6 pilot passed on Fable);
independent Opus review returned 3 minor findings, all fixed. "Phase-2-to-
Fable elevation" candidate absorbed by D-014 and dropped.
