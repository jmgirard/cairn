# M45: Toolchain-profile spine — mechanism + r-package/generic profiles + init selection

**Status:** done · PR #43 · merged 2026-07-12 · milestone 1 of the toolchain-profiles arc (M46 rewire, M47 release).

## Goal
Establish the toolchain-profile mechanism (`cairn/PROFILE.md`, six slots) and ship the r-package + generic reference profiles selected at init, without rewiring the operational skills.

## Outcome
- Six-slot PROFILE.md schema (markdown `## <slot>`); `skills/shared/profiles/{r-package,generic}.md` shipped — r-package captures current devtools/CRAN commands verbatim.
- `cairn-init` selects on DESCRIPTION presence, instantiates PROFILE.md, repair-mode backfills by inference (back-compat: absent PROFILE.md → infer r-package/generic).
- `session_context` surfaces the active profile (no-op when absent); `cairn_validate.check_profile` validates slot completeness when present, no-ops when absent; PROFILE.md wired into file-map + weight-caps + `LINE_CAPS` (<90).
- Operational skills byte-for-byte intact (AC6). Oracle doctrine stays universal (D-024/D-025), not a slot.

## Key decisions
- PROFILE.md schema = markdown `## <slot>` sections (over YAML frontmatter / freeform) — milestone-local.
- Review fix (diff-bug, scored 91): `_profile_slots` made fence-aware — a `## ` line inside a fenced command block is slot body, not a new slot.

Evidence: skills 105 / scripts 65 / hooks 32 green; `cairn_validate` clean.
