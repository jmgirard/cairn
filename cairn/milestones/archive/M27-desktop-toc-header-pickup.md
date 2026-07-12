# M27: Desktop TOC pickup of the `##` phase headers (done 2026-07-12)

**Status:** done · **PR:** #25 (squash `7d9ae86`) · **Priority:** low

## Goal
Determine whether Claude Desktop's TOC indexes cairn's `##` phase headers; fix via a header change or record as a client limitation.

## Outcome
Live probing in Jeff's Claude Desktop (viewing a **Claude Code** session —
cairn's runtime) showed markdown `#`/`##`/`###` headers produce **zero** TOC
entries across every level/format/placement variant; a single chapter marker
produces the outline. So the navigable TOC in cairn's runtime is driven by
**chapter markers, not markdown headers**. Took AC2 option (b): no
header-format change (H1/H2 levels stay, as visual hierarchy). Characterization:
`references/desktop-toc-mechanism.md`.

## Key decisions
- **D-020** — records the mechanism; annotates D-012's "both levels index"
  claim as *unverified for cairn's runtime* (other surfaces untested).
- Corrected the false "headers land in the TOC" line in `tracking-rules.md`
  and the `test_phase_header_levels.py` docstring (review F2); levels unchanged.

Review: AC1/AC2 fenced; gate green (validate 10/10, skills 68/68, scripts
43/43). F2 (88) fixed; F1 (75) actioned to harden D-020. Candidate banked:
promote the chapter-marker rule to a hard per-phase mandate.
