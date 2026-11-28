# M169: Criteria and tasks carry positional labels

**Status:** done (2026-09-02, PR #172 https://github.com/jmgirard/cairn/pull/172)

**Goal:** Every milestone file's acceptance criteria and tasks open with the positional label Coverage cites (`AC1:`, `T1:`), because the shipped template shows them and the plan and implement skills state the rule.

**Outcome:** `skills/shared/templates/milestone.md` example items read `- [ ] AC1:`, `- [ ] AC2:`, `- [ ] T1:` and the Acceptance criteria and Tasks comments state the position rule (label = position counted top-to-bottom, the number Coverage cites; insertion, removal, or reorder renumbers labels and Coverage lines together). Binding-criterion ingest form unified to `- [ ] ACn (BCm): <verbatim>` at its five sites (template comment, `milestone-brief/SKILL.md`, `test_bc_ac_ingest_form.py` docstring, two `test_finding_enforcement.py` assertions); `git grep "AC-N" -- skills scripts` is empty. `/milestone-plan` step 4 gains a **Positional labels** bullet; `/milestone-implement` step 6 states the renumbering obligation on both the minor and the substantive branch. Hand-run prose guard `skills/tests/test_positional_labels.py` (12 tests, 13 mutation entries). Validator advisory on labels declined (D-107 shape); no archived or live file relabeled.

**Decisions:** none cross-cutting. Plan gate: template-and-prose fix over a validator advisory; renumbering on both step-6 branches; the colon form `ACn:`/`Tn:`.

**Review:** two passes. Pass 1: defect return 1 — AC1's grep matched the new guard's own docstring and `assertNotIn` literal; repaired by concatenating the token. Pass 2: AC1–AC3 verified; three-lens fan-out — blame-history and prior-review clean; diff-bug 11 findings: F3 (ROADMAP row spelling), F4 (`(BCn)` comments in two script tests), F6 (docstring overclaimed every block pinned) fixed on-branch; F1/F2 (minor-branch Coverage renumbering vs plan ownership) rejected as the plan gate's chosen both-branch rule with the mapping unchanged; F5, F7–F11 rejected as declined hardening or pre-existing. Hygiene: one LESSONS line (a grep-clause criterion's domain includes its own guard file); nothing graduated or retired.
