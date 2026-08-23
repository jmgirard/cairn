# M57: references/ + linking hardening (done 2026-07-16)

**Goal:** Execute M56's three adopted dispositions — name the synthesis-note
page type, mechanize an INDEX↔disk references check, add an FP-tolerant
dangling M/D-token advisory.

**Outcome:** File map + Source-ingestion name both committed `references/`
page types (source + synthesis notes; mutation-registered guard).
`check_references` (hard CHECK): every committed note has an INDEX line and
vice versa; no-ops sans INDEX.md (M45 pattern). `check_dangling_ids` (WARN
ADVISORY): M/D tokens resolving to no ROADMAP row, milestone file, or
D-entry warn; tolerance per D-023 — above-max skip (M99 example-prose
class) + same-line owner/repo-slug skip (cross-repo-cite class), each
fixture-pinned on a gapped known-ID set; legacy/ excluded (D-005).

**Decisions (milestone-local):** tolerance shape gate-chosen (above-max +
slug, deliberately loose on path-bearing lines — preferred miss); tolerance
rules folded into T3 (M46 fold-don't-defer). Quirk: the milestone's own ID
made the live "ackwards M57" hazard self-resolve — fixtures carry both
hazard classes independently of the live tree.

**Review:** all 6 ACs fresh-evidenced; live tree 15/15 + zero WARNs; suites
156/83/32. Three lenses + scorer — 1 finding (F1/85, fixed: INDEX-line
capture tolerated decorated filenames + regression test); blame/prior-PR
lenses clean. **PR:** https://github.com/jmgirard/cairn/pull/55
