# M79: References content check — the lint stops being a filename census

**Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/77 · **Depends on:** M78

**Goal.** Make `check_references` verify that a committed references page carries provenance, and close the two gaps that let pages escape the check.

**Outcome.** Every committed `references/` page must carry M78's `**Provenance.**` block naming an ingested date and a source pointer; the walk is recursive, so a nested page is enforced like a top-level one; a directory holding pages but no `INDEX.md` is reported instead of passing (the M45 no-op survives only as a genuine not-adopted signal). All 16 of this repo's pages passed unmodified — no D-045 correction, nothing grandfathered. Also renamed the gitignored source shelf `references/pdf/` → `references/sources/`, user-raised at the implement gate.

**Decisions.** M79-D1 (milestone-local): the content conditions are a hard CHECK — D-029's oracle-registry precedent does not transfer, because a provenance block is a *structural* field of a shipped template, not a judgment about evidence quality; D-023 is honoured in the parser, not the severity. D-047: the rename follows a post-1.0 deprecation cycle — `check_scaffold` accepts the legacy entry and a new non-failing `scaffold deprecations` advisory names the successor.

**Amendments (both gated).** AC1 checks a provenance source pointer, not a citation line: M78's template scopes `**Citation.**` to published primary sources, and 16 of 17 pages here are synthesis or web-source notes, so a blanket check would contradict the template it enforces. The rename entered Scope as AC8/T7–T8.

**Review.** All 8 criteria verified; AC2/AC3 proven differentially against `main`'s checker, not by assertion alone. Blame-history and prior-PR lenses: no findings. Diff-bug lens: five findings, all ≥80, all fixed with regression fixtures — an orphaned rationale comment (F1/80) and four parser defects where a sound page hard-FAILed or a non-entry was admitted (F2/95 decoy heading swallowed the block; F3/92 label alone on its line lost its body; F4/90 the literal token "from" required, failing a template-sanctioned "retrieved via <url>"; F5/85 widened INDEX capture admitted prose bullets and `..` escapes that silently satisfied entries). F2–F4 were exactly the false-positive class M79-D1 promised to absorb in the parser, so the severity stood and the parser got more generous. After fixes: skills 324, scripts 128, hooks 72, each exit 0; `cairn_validate` exit 0.

**Noted, not resolved.** AC8's first clause ("no live `references/pdf` string … outside history") is in tension with the deprecation path the same criterion mandates, which necessarily keeps that string in code. Both independent lenses read it as satisfied; recorded at the merge gate rather than reinterpreted review-side.
