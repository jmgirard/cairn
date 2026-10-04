# M207: Candidate rows in the idle cairn pane

**Status:** done (2026-10-04, PR #214 https://github.com/jmgirard/cairn/pull/214)

**Goal:** When no milestone is active, show the ROADMAP's candidate rows in the cairn pane.

**Outcome:** With no `in-progress` or `review` row, the pane draws a `Candidates N` heading below the queue and one line per candidate row: `↑` (orange, bold) for an exact `[high] ` opening, `·` for normal, `↓` (gray, gray title) for `[low] `, then the text before the first `: `, or all of it. `candidateRows` in `reader.ts` reads flush-left `- ` lines in each `## Candidates` section after removing that section's HTML comments, so the `/cairn-init` skeleton's placeholders are not read. The pane state and `CairnPaneState` gained `candidates`, and the atom's tag moved to `pane-2`. `python_candidates` in `test_status_fixtures.py` holds the reader to each fixture's new `candidates` key, and to `candidate_count` where no comment sits in the section. New fixtures are `candidates` and `candidates-skeleton`. Mod tests went from 904 to 956. README, CHANGELOG, and DESIGN describe the section. The candidate-row part of "Pane content follow-ons" was absorbed and trimmed from that row.

**Decisions:** Flush-left rows only, over `candidate_count`'s indented match, since ROADMAP rows are one top-level line each. AC1's long-title clause was amended at the operator's choice after two re-audits: the test checks the `truncate-end` wrap prop, because the test API cannot see drawn text.

**Review:** Three lenses gave 24 findings. 7 were fixed: comments removed per section rather than over the whole file, which a `<!--` in another section could break; token rows that test the full text; `CairnPaneState` missing `candidates`; mark styles tested; a CRLF case; and narrower DESIGN and header wording. 12 went to follow-up, most to the new row "Candidate pane follow-ons (M207 review)". 5 were rejected as planned or style. A claim audit read 41 claims and corrected 2.
