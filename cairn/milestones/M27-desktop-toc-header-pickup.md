<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M27: Desktop TOC pickup of the `##` phase headers

- **Status:** review
- **Priority:** low
- **Depends on:** —
- **Branch/PR:** m27-desktop-toc-header-pickup

## Goal

Determine whether Claude Desktop's table of contents reliably indexes the
`##` phase headers, then either apply a header change that fixes it or record
it as a client-side limitation — with the finding written to disk either way.

## Scope

**In:**
- Characterize, with Jeff's Claude Desktop (the only place the behavior is
  observable), whether/when the `##` phase headers appear in the TOC, varying
  at least header level, exact format (`## Plan` vs `## Milestone <NN>`), and
  placement.
- Reach a recorded conclusion: a concrete header-convention change applied to
  `tracking-rules.md` + the affected skills (and `test_phase_header_levels.py`
  if the locked format changes), OR a D-entry concluding it is a client
  limitation outside cairn's control.

**Out:**
- The routing-chip mandate → M26.
- Any client-side / Anthropic-side fix to Claude Desktop itself (not ours to
  make); this milestone only decides cairn's response.

## Acceptance criteria

- [ ] Documented characterization of Desktop TOC behavior on the `##` phase
      headers across at least the three variants above, recorded in this
      milestone's Review section (or a `cairn/references/` note it links).
- [ ] A recorded decision in `cairn/DECISIONS.md`: either (a) a header-format
      change that improves indexing, applied to `tracking-rules.md` + the
      affected skills (+ the header guard test), or (b) a conclusion that it
      is a client limitation, annotating D-012's "both levels index" claim.

## Coverage

- AC1 → T1, T2
- AC2 → T3

## Tasks

- [x] T1 — With Jeff on Claude Desktop, observe how the TOC treats the `##`
      phase headers: reproduce the missing/unreliable indexing and note the
      conditions. (Evidence is manual — this milestone's data-gathering
      depends on the user's Desktop client; if Jeff is unavailable, status →
      `blocked` with a work-log line.)
- [x] T2 — Vary header level / exact format / placement to isolate what, if
      anything, changes TOC pickup; record the variant results.
- [x] T3 — Conclude and record: apply the winning header change to
      `tracking-rules.md` + affected skills (+ `test_phase_header_levels.py`)
      if one exists, else append a D-entry that it is a client limitation and
      annotate D-012. Update tracking accordingly.

## Work log

- 2026-07-12: created by /milestone-plan (absorbs candidate "Phase-header TOC
  pickup in Claude Desktop", 2026-07-12 Jeff feedback). Tension to resolve:
  D-012 claims both H1/H2 index in Desktop's TOC; this milestone tests that.
- 2026-07-12: /milestone-implement started; status → in-progress, branch
  m27-desktop-toc-header-pickup cut from main. T1/T2 are manual Desktop
  observations gathered live with Jeff.
- 2026-07-12: T1/T2 — live probing in Jeff's Claude Desktop (viewing a Claude
  Code session): H1/H2/H3 markdown headers across two messages produced zero
  TOC; one chapter marker produced a two-entry outline. Characterization →
  references/desktop-toc-mechanism.md.
- 2026-07-12: T3 — finding: in Claude Code (cairn's runtime) the TOC is driven
  by chapter markers, not markdown headers. Recorded D-020 (annotates D-012);
  corrected the false "headers land in the TOC" line in tracking-rules; banked
  a candidate to consider a hard chapter-marker mandate. AC2 option (b) taken;
  no header-format change. Decision gate: Jeff chose "Record + fix false line".

## Decisions

## Review
