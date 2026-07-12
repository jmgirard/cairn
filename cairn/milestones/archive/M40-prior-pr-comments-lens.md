# M40: Prior-PR-comments reviewer lens — done 2026-07-12

**Goal:** Add a third distinct-evidence lens to `/milestone-review`'s fan-out —
a prior-PR-comments reviewer flagging where the diff regresses a lesson a past
PR review already taught on the touched files.

**Outcome:** `milestone-review/SKILL.md` step 5 now fans out to THREE lenses
(`[O]` diff-bug, `[S]` blame-history, `[S]` prior-PR-comments) → `[S]` scorer.
The new lens reads prior merged PRs' review comments on the modified files
(recipe-in-prose: `git diff --name-only` → `gh pr list`/`git log` →
`gh api …/pulls/{n}/comments`), flags only regressions of a prior review
(narrow), always spawns, no-ops cleanly ("no prior-PR evidence", zero findings)
on thin/no-history repos or without a remote, and feeds the existing scorer
unchanged. `tracking-rules.md` model-strategy updated two → three;
`test_review_fanout.py` extended (`TestPriorPRLens` + three-reviewer lock).

**Key decisions (plan gate):** recipe-in-prose not a script; narrow
regression-only scope; always-spawn/no-op not conditional. No D-entry (skill
conduct; IP3 worked-under, not changed).

**Review:** all 6 ACs fresh; **AC3 no-op live-confirmed** — the lens reviewing
its own milestone returned "no prior-PR evidence". F1 (92, fixed) — a
false-coverage test (M39 trap) replaced with a lens-specific deferral test; F2
(45) logged below cutoff. **PR:** #38 (squash-merged).
