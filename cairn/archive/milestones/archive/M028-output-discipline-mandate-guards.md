# M28: Harden the output-discipline mandate guards

- **Status:** done · **PR:** #26 (merged 2026-07-12)

**Goal:** Promote the chapter-marker rule to a hard per-phase mandate guarded
across all nine skills, and bring `milestone-brief`'s routing chip under the
routing-chip guard M26 missed.

**Outcome:** The tracking-rules "Chapter markers" rule is now a per-phase
mandate (mark a chapter at each phase transition) with a no-mechanism fallback
(H1/H2 headers cover it; nothing breaks). All nine phase skills carry a
one-line `Chapter markers:` directive; new `test_chapter_marker_mandate.py`
locks the rule wording + every directive. `milestone-brief` step 5 now names
`AskUserQuestion`, is in `NON_REVIEW_CHIP_SKILLS` (now seven), and its stale
"no terminal chip" comment is corrected.

**Key decisions:** D-021 — chapter-marker mandate; enforcement = per-skill
directive + guard; fallback = attempt-always, headers fallback; scope = all
nine incl. review (orthogonal to the D-019 routing-chip exception); annotates
D-020.

**Evidence:** guard 71/71, scripts 43/43, `cairn_validate` 10/10. Fan-out F1
(D-021 "(six)"→"seven", scored 92) caught by both lenses, fixed pre-merge.
