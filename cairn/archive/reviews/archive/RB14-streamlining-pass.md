# RB14: Streamlining pass over shipped code (M164)

- **Date:** 2026-08-29
- **Output required:** write findings to `cairn/reviews/RR14-streamlining-pass.md`
- **Binding criteria:** not requested

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

This repo is **cairn**, a Claude Code plugin for project tracking. Its
shipped runtime code is Python in two directories: `scripts/` (CLI tools an
adopting repo runs — a tracking-file validator, an impact scanner, a cost
reporter, a status snapshot, a next-action helper, plus a shared-helpers
module) and `hooks/` (PreToolUse/Stop/SessionStart hooks registered in
`hooks/hooks.json` that guard git operations and inject tracking context).
Both run inside adopting repos, so their length and clarity are user-facing.
Each directory carries a gating `unittest` suite under its `tests/`
subdirectory.

This review is a one-shot **streamlining audit**: the repo's own per-branch
review tooling only ever examines diffs, so code no recent branch touches
has never had a whole-corpus pass for length, directness, and
simplification. M164 exists to run exactly this audit and apply the accepted
recommendations. Your report is advisory; a maintainer triages every
recommendation individually (apply / consider / reject-with-reason).

## Materials

The corpus is these 22 files (current line counts shown), and nothing else:

```
      50 scripts/tests/test_shipped_templates.py
      62 scripts/cairn_status.py
      65 hooks/stop_guard.py
      70 hooks/idea_guard.py
      70 hooks/memory_guard.py
      78 hooks/merge_guard_post.py
     102 scripts/cairn_next.py
     103 hooks/commit_guard.py
     139 scripts/tests/test_bc_ac_ingest_form.py
     161 hooks/force_push_guard.py
     179 scripts/cairn_impact.py
     194 hooks/merge_guard.py
     277 scripts/tests/test_scaffold_check.py
     339 hooks/cairn_common.py
     341 scripts/tests/test_binding_criteria.py
     368 hooks/session_context.py
     455 scripts/cairn_cost.py
     465 scripts/cairn_scripts.py
     518 scripts/tests/test_cairn_cost.py
    1876 scripts/cairn_validate.py
    1927 hooks/tests/test_hooks.py
    3945 scripts/tests/test_scripts.py
```

You may also read `hooks/hooks.json` (hook registration) to understand how
hooks are invoked, but it is context, not corpus.

To run the gating suites (both must exit 0; run from the repo root):

```
python3 -m unittest discover -s scripts/tests
python3 -m unittest discover -s hooks/tests
```

Do not modify any file. Your only output is the RR file.

## Questions

1. **Length.** Which files or functions carry code that does not earn its
   length — duplicated logic, dead or unreachable branches, helpers used
   once that inline cleanly, over-general machinery serving one caller?
   Cite each site as `file:line` (or a line range) and say what the shorter
   form is.
2. **Directness.** Where does control or data flow take an indirect route a
   reader must unwind — needless layering, flag parameters selecting
   between two callers' behaviors, state threaded where a return value
   would do, string re-parsing of something already structured? Cite sites
   and the direct form.
3. **Simplification.** Which concrete rewrites would make a unit
   substantially simpler while preserving its observable behavior
   (including CLI output, exit codes, and hook JSON emitted)? Prefer
   rewrites whose behavior preservation the existing gating suites can
   attest; where the suites would not catch a regression the rewrite
   risks, say so explicitly.
4. **Test-suite streamlining.** The four test files are in scope as code:
   where do tests duplicate one another's coverage, re-assert the same
   contract at multiple sites, or carry scaffolding a shared helper or
   fixture would shrink? A recommendation to *remove* a test must name the
   surviving test that still covers the removed one's contract.
5. **Not worth it.** Which superficially attractive streamlinings should
   NOT be made — because the length is load-bearing (deliberate
   duplication between independently-registered hooks, defensive parsing
   of untrusted input, clarity that beats brevity)? Naming these prevents
   a later pass from making them by mistake.

## Constraints

Fixed; flag disagreement explicitly rather than silently working around it:

- **Observable behavior is preserved.** This pass changes no contract:
  CLI flags, output text consumed by other tooling, exit codes, and the
  JSON hooks emit to Claude Code all stay as they are. A recommendation
  that would change behavior is out of scope here; mark it as
  milestone-sized instead (it becomes a ROADMAP candidate, not an applied
  change).
- **The two gating suites stay gating** and must pass after every applied
  change; test count may drop only where a test's removal is itself one of
  your recommendations (question 4's bar).
- **Corpus boundary.** Skills prose, templates, and `cairn/` tracking
  files are out of scope (a separate program governs prose size — D-114);
  so is `skills/tests/` (hand-run prose guards, D-109). Do not recommend
  changes outside the 22 files.
- **Hooks are independently registered entry points** invoked by Claude
  Code per `hooks/hooks.json`; each must remain runnable as its own
  script. Shared logic belongs in `hooks/cairn_common.py`, which already
  exists — recommending consolidation into it is fine; recommending a new
  package structure or import-path change is milestone-sized.
- **Dependency policy.** No new dependencies; everything runs on the
  standard library (D-entries record that dependency changes are never
  unilateral).

## Output format

In `RR14-streamlining-pass.md`: answer each question by number with your
reasoning and evidence; list any additional findings separately under
"Beyond the brief"; end with concrete recommendations, each **numbered**
(`R1`, `R2`, …), each citing `file:line`, each marked
apply / consider / reject-with-reason, and each small enough to verify by
running the two gating suites — anything larger marked "milestone-sized"
instead. Your report is advisory: emit a `## Binding criteria` section ONLY
if this brief's header slot says `requested`.
