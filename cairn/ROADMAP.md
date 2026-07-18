# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-18 (M71 done + archived; M66 pruned under terminal-row retention; two M25 lessons pruned at the LESSONS cap)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

_Released 1.0.0 2026-07-16 (tag v1.0.0)._

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M71 | Idea-capture intake gate — out-of-band ideas also land as candidates (D-042) | done | — | high | milestones/archive/M71-idea-capture-intake-gate.md |
| M70 | Docker-image toolchain profile — fourth profile for pure-image repos | done | — | normal | milestones/archive/M70-docker-image-profile.md |
| M69 | Cap-overrun diagnostic — per-section breakdown + single-pass compression discipline | done | — | normal | milestones/archive/M69-cap-overrun-diagnostic.md |
| M68 | Changelog profile slot — required seventh slot, "none" legal (D-040) | done | — | normal | milestones/archive/M68-changelog-profile-slot.md |
| M67 | Narration discipline — outcomes, not deliberation (D-039) | done | — | high | milestones/archive/M67-narration-discipline.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- MCP-matcher semantics in `references/claude-code-hooks.md`: the reference's Matchers section never mentions MCP tool names, so the M71 T1 finding (a word-chars-only matcher is an EXACT-string compare, hence the regex form) survives only in a work log that compresses at archive — swept: no existing row or D-entry covers it; the M19/D-017 precedent put its T1 finding in this same file — added 2026-07-18 — M71 review F3 (63)
- Budget-first drafting (cap prevention): up-front per-section line budgets in the milestone template/rulebook so first drafts land under the 150-line cap by construction, rather than compressing after — reassess once M69's diagnostic + single-pass discipline is in use and we can see whether the cure suffices — added 2026-07-17 — M69 Out
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
