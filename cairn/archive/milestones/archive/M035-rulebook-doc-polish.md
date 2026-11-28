# M35: Rulebook & doc-wording polish batch

- **Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/33 · **Merged:** 2026-07-12

## Goal

Apply five deferred doc/wording tweaks to `tracking-rules.md`, each locked by
a prose-guard so it can't silently drift.

## Outcome

Five wording rules added to `skills/shared/tracking-rules.md`: (1) weight-caps
— cluster a large legacy/parking-lot backlog into grouped candidate rows
pointing at the entombed legacy ROADMAP (M21 G-C4); (2) cap at 3 prioritized
clarification markers per gate; (3) give Explore fan-out subagents a reading
list; (4) state *why* review uses a fresh model (author diff-blindness);
(5) copy-run commands go in their own fenced block, not inline backticks.
Plus a one-line `cairn-init` §2 pointer (M23-guarded wording untouched).

Locked by AC2 in `test_gate_wording.py`, AC4 in `test_review_fanout.py`, new
`test_rulebook_polish.py` (AC1/AC3/AC5). Prose + guards only; skills suite
83/83; two-lens fan-out zero findings. No D-entries. Graduated on merge: the
mature-backlog-remedy and M06-survey-tweaks candidate rows (both fulfilled).
