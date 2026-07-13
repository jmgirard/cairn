# M54: Release positioning + DESIGN refresh (done)

**Goal:** Align cairn's outward positioning + DESIGN.md with the
language-agnostic architecture (RR01 recs 1 + 5). PR #52 (squash, 2026-07-13).

**Outcome:**
- Positioning: plugin.json + marketplace.json descriptions and README ¶1
  reframed R-only → language-agnostic core + toolchain profiles (R/Python/
  generic); cairn-init §0 "not an R package" bullet removed; /hotfix step 5
  genericized (NEWS.md → the profile's changelog, no schema slot added).
- DESIGN: hooks bullet → all 5 (added commit_guard, memory_guard); IP1
  "main" → "the default branch"; Known-issues rewritten to the honest
  single-author / single-OS / Windows-unverified + honor-system list.
- Template: claude-md-section boundary rule gains `Lessons → LESSONS`.
- Guard: test_positioning_guard.py (7 methods) + 8 mutation-harness entries
  lock the framing, 5-hook list, IP1 wording, Known-issues, template rule.

**Key decisions:** IP1 reword is wording-alignment only — M25 owns the
semantics (it scoped itself to operational skills, leaving DESIGN's IP1 a
gap), so no D-entry. Carved from the "Public release prep" candidate;
remainder (LICENSE, worked example, de-risking, DRAFT removal, v1.0 tag)
stays in that row (RR01 rec 14/§10).

**Review:** verify green (150 skills + 65 scripts), cairn_validate 14/14,
cairn_impact reconciled; 3 fresh-context lenses → zero findings.
