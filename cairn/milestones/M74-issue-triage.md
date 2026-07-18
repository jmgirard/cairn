<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M74: Issue triage — /milestone enumerates untriaged inboxes into candidate rows

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M73   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Replace `/milestone`'s unenumerable "untriaged inboxes" audit bullet with a
concrete sweep that lists open issues and external PRs and proposes a
disposition for each.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a concrete enumeration step in `/milestone` §2 (`gh issue list` /
`gh pr list`, cross-checked against existing candidate rows, the archive, and
DECISIONS per the search-first rule); a triage acceptance chip in §3 showing
each proposed disposition verbatim per D-037/D-038; clean degradation when
`gh` is absent, unauthenticated, or the repo has no remote — report and skip,
never fail the audit.

**Out:** any writing to GitHub (labels, comments, closing issues) — cairn
reads the inbox, it never manages it. Auto-creating candidate rows without the
chip. A scheduled or hook-driven sweep. Making `cairn_validate` aware of
issues — the scripts stay offline and stdlib-only
(`cairn/DESIGN.md:55-62`); this step lives in skill prose, like every other
`gh` invocation in the repo.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `skills/milestone/SKILL.md` §2's untriaged-inboxes bullet
      (`:78-79`) is replaced by a step naming the actual commands and the
      search-first cross-check against candidates + `milestones/archive/` +
      `DECISIONS.md`. Evidence: the step quoted.
- [ ] AC2 — the step states the degradation path for no `gh` / no auth / no
      remote: report the reason, skip the sweep, do not FAIL the audit.
- [ ] AC3 — §3's triage chip shows each proposed disposition verbatim above
      the chip (issue → candidate row / hotfix via `/hotfix` / milestone via
      `/milestone-plan` / leave), satisfying the Acceptance-chips bar.
- [ ] AC4 — external PRs in the same sweep route to M73's `/hotfix` door for
      the hotfix-bar disposition; no second intake mechanism is introduced.
- [ ] AC5 — a guard test locks AC1's commands and AC2's degradation clause,
      registered in `skills/tests/test_mutation_harness.py` with the
      completeness meta-test green; `test_gate_conclusion_preview.py` still
      passes with the new chip wording.
- [ ] AC6 — the `verify` slot is clean: all three `unittest discover` suites
      pass from the repo root.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [ ] T1 — Rewrite the §2 bullet (`skills/milestone/SKILL.md:78-79`) as a
      concrete step: `gh issue list --state open --json number,title,url` (and
      the PR equivalent), the search-first cross-check, and the degradation
      clause. Keep it inside the "script deliberately does not judge these"
      block (`:64`) — this stays model judgment over a mechanical listing.
- [ ] T2 — Add the triage disposition chip to §3 (`:83-101`), with the
      verbatim-above-the-chip requirement stated at the step; route the PR
      dispositions to `/hotfix` per M73.
- [ ] T3 — Write the guard test; register it in the mutation harness; re-run
      `test_gate_wording.py` and `test_gate_conclusion_preview.py`, which
      assert on `/milestone`'s chip wording.
- [ ] T4 — Run all three suites from the repo root.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan.

## Decisions
<!-- owner: implement / review · append-only -->
