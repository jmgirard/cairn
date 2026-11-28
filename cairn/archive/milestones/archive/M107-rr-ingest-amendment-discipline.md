# M107: RR-ingest / amendment discipline — the ingest surface carries the plan path's form, budget, and file hygiene

**Status:** done (2026-07-21, PR #105 https://github.com/jmgirard/cairn/pull/105)

**Goal:** The brief-ingest and implement-amendment paths carry the form,
budget, and file-hygiene discipline the plan path already has.

**Outcome:** milestone-brief step 3 + the milestone template prescribe the
binding-criterion ingest form `- [ ] AC-N (BCn): <verbatim>` — each BC lands as
a numbered, Coverage-mapped acceptance criterion, so the positional
`check_coverage_complete` stays quiet while `check_binding_criteria` still
matches the verbatim body. `cairn_budget` + the tracking-rules one-pass-trim
rule are now referenced from the implement step-6 amendment gate and the brief
ingest step. Brief step 4's archive move uses `mv` + `git add`, never `git mv`
(untracked RR). test_bc_ac_ingest_form.py pins the interaction; four new
mutation-registered guards; `_owners_from_lines` extracted with a bounded scan.

**Decisions:** none (dispositions Q1–Q3 recorded in the plan/scope; the deferred
BC-aware coverage message is a ROADMAP candidate).

**Review:** three lenses + scorer. F1 (92, fixed) — the widened owner-comment
scan could borrow a later section's tag when a section lacked its own comment;
bounded to the section + two regression tests. No sub-80 findings.
