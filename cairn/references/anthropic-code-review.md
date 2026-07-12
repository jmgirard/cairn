# code-review (Anthropic official plugin)

Source: https://github.com/anthropics/claude-plugins-official
`plugins/code-review/` @ dc72937 (studied 2026-07-11, full source read).
Note: distinct from the built-in `/code-review` skill in current Claude
Code environments; cited here as `anthropic-code-review`.

## What it is

A single 92-line `/code-review <PR>` command: a multi-agent pipeline that
reviews a GitHub PR and posts one formatted comment via `gh`.

## Pipeline (the interesting part)

1. **Haiku eligibility gate** — skip closed/draft/trivial/already-reviewed
   PRs; re-checked again at the end before commenting.
2. Haiku agents gather context: relevant CLAUDE.md paths, PR summary.
3. **5 parallel Sonnet reviewers, each with a distinct evidence base**:
   (a) CLAUDE.md compliance; (b) shallow bug scan of the diff only;
   (c) git blame/history of modified code; (d) comments on *previous PRs*
   touching these files; (e) code comments in modified files.
4. **Generate-then-verify**: every flagged issue goes to a fresh Haiku
   scorer with a verbatim 0–100 confidence rubric; <80 filtered out.
5. Explicit false-positive taxonomy (pre-existing issues, linter-catchable,
   nitpicks, unmodified lines, intentional changes).

## What cairn should steal

- **Distinct-evidence-base fan-out** for `/milestone-review`'s independent
  review: cairn runs one fresh Opus reviewer; blame-history and
  prior-PR-comment lenses are cheap and orthogonal to a diff read.
  *(Shipped: blame-history → M17; prior-PR-comments → M40.)*
- **Separate scorer verifying reviewer output** — two-stage
  generate-then-verify with the rubric given verbatim.
- The false-positive taxonomy, nearly verbatim, for review subagent
  prompts.

## What cairn does that it doesn't

Review here is stateless drive-by commentary: no acceptance criteria to
verify, no merge authority (comments only), no tracking of what was
found. Cairn's review gate verifies criteria with fresh evidence and
holds the merge until user approval.

## Doctrine challenge for cairn

The pipeline leans on **Haiku** for eligibility gates, context gathering,
and confidence scoring — cheap mechanical triage. Cairn's rulebook says
"Never Haiku. For anything." Anthropic's own flagship review plugin is
counter-evidence for the narrow case of low-judgment gating/scoring
steps; worth revisiting the rule's blanket form (synthesis note).
