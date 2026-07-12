<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M27: Desktop TOC pickup of the `##` phase headers

- **Status:** review
- **Priority:** low
- **Depends on:** —
- **Branch/PR:** m27-desktop-toc-header-pickup · PR #25

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

- [x] Documented characterization of Desktop TOC behavior on the `##` phase
      headers across at least the three variants above, recorded in this
      milestone's Review section (or a `cairn/references/` note it links).
- [x] A recorded decision in `cairn/DECISIONS.md`: either (a) a header-format
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

- 2026-07-12: TOC mechanism finding recorded cross-cutting as D-020 (annotates
  D-012). Milestone-local: took AC2 option (b) — no header-format change — on
  the evidence that no markdown header of any level/format/placement indexes
  in cairn's Claude Code runtime.

## Review

**Reviewed 2026-07-12 · branch `m27-desktop-toc-header-pickup` · PR #25.**

Fresh evidence per acceptance criterion (AC fencing — box ticked only against
a recorded evidence line):

- **AC1 — characterization across ≥3 variants.** PASS. `references/desktop-toc-mechanism.md`
  documents live probing in Claude Desktop viewing a Claude Code session,
  varying header **level** (H1/H2/H3), **format** (`## Plan` vs
  `## Milestone 27`), and **placement** (mid-message, end-of-message, across
  two messages). Result invariant across all three: markdown headers → zero
  TOC entries; one chapter marker → a two-entry outline. Note is linked from
  `references/INDEX.md`.
- **AC2 — recorded decision annotating D-012.** PASS. `DECISIONS.md` D-020
  records the conclusion (option b: no header-format change; the header→TOC
  mechanism does not apply to cairn's Claude Code runtime) and explicitly
  annotates D-012's "both levels index" claim as surface-specific. The
  now-false line in `tracking-rules.md` was corrected to credit the
  chapter-marker rule.

**Consistency gate (by command, 2026-07-12):** `cairn_validate` exit 0 (all 10
checks). Coverage completeness: AC1→T1,T2 · AC2→T3, all tasks present and
checked. skills guard tests 68/68, scripts tests 43/43. R-specific gates
waived (plugin repo, CLAUDE.md); no DESIGN principle changed (impact report
skipped); no user-facing behavior change (no NEWS entry). `test_phase_header_levels.py`
still green — header levels unchanged, only the rationale text was corrected.

**Fresh-context review (2 lenses + scorer, 2026-07-12):**
- **F2 (scored 88) — fixed.** `test_phase_header_levels.py`'s docstring still
  carried the exact false "both land in Claude Desktop's TOC" claim that D-020
  refutes and that `tracking-rules.md` was corrected for — a second live copy
  left contradictory. Corrected the docstring to credit chapter markers
  (M27/D-020); test assertions untouched, still 68/68.
- **F1 (scored 75, below the 80 gate) — logged and actioned anyway.** D-020
  and the reference note asserted D-012's claim "described a different surface
  (regular claude.ai chat)" where headers *do* index — a positive claim M27
  never tested. Reworded both to annotate D-012's claim as *unverified for
  cairn's runtime*, not confirmed elsewhere. Below-threshold so not mandated,
  but actioned because it hardens the honesty of a permanent append-only
  record at one-clause cost; surfaced at the approval gate.
- Both reviewers independently noted the archived `M11-phase-header-levels.md`
  repeats the old phrasing; left as-is (historical milestone record, not live
  rulebook text). No other findings.
