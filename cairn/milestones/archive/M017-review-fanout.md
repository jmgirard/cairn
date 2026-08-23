# M17: Review fan-out + confidence scoring — done 2026-07-11

**Goal:** Strengthen `/milestone-review`'s independent review with a second
orthogonal evidence lens and a confidence scorer that filters — but never
silently drops — low-confidence findings.

**Outcome:** Step 5 of `/milestone-review` reworked from one fresh Opus
reviewer into a two-lens fan-out — `[O]` diff-bug reviewer (Opus) + `[S]`
blame-history reviewer (Sonnet), each with a distinct evidence base — followed
by a `[S]` generate-then-verify confidence scorer (verbatim 0–100 rubric,
threshold 80; sub-threshold findings excluded from the actioned list but logged
in the Review section, never dropped). False-positive taxonomy embedded in the
reviewer prompts. `tracking-rules.md` model-strategy section describes the
fan-out; "Never Haiku" kept intact. Locked by `skills/tests/test_review_fanout.py`
(8 checks; full suite 35/35).

**Key decisions:** D-016 — keep the blanket "Never Haiku" rule; the scorer runs
on Sonnet (review fires once per milestone so the saving is marginal, and the
scorer gates which findings reach the user). Fan-out width = 2 lenses; the
prior-PR-comments lens and a coverage-lint script were split to candidates.

**Review note:** M17's own fan-out (live-symlinked plugin) caught an IP2→IP3
miscitation in the scorer's "never silently dropped" line — fixed pre-merge.

**PR:** https://github.com/jmgirard/cairn/pull/15
