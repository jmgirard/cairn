<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M74: Issue triage — /milestone enumerates untriaged inboxes into candidate rows

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M73   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m74-issue-triage   <!-- owner: implement (branch) / review (PR URL) · create -->

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
never fail the audit; and the doc surfaces that still describe the pre-M73
`/hotfix` trigger (`cairn/DESIGN.md:69-70`, `README.md:118` and `:194`),
brought in line with the bidirectional description M73 shipped.

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
- [ ] AC6 — `cairn/DESIGN.md`'s Conventions bullet no longer says `/hotfix`
      triggers only on bug reports, and README's `/hotfix` row + contributions
      bullet name PR adoption; all three read consistently with the shipped
      `skills/hotfix/SKILL.md` `description:`. Evidence: the passages quoted
      beside that description, plus a repo-wide `git grep` for surviving
      pre-M73 trigger prose (history files excepted per M58, and this
      milestone's own file — which necessarily quotes the prose it
      removes, M62).
- [ ] AC7 — the `verify` slot is clean: all three `unittest discover` suites
      pass from the repo root.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3
- AC6 → T4
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Rewrite the §2 bullet (`skills/milestone/SKILL.md:78-79`) as a
      concrete step: `gh issue list --state open --json number,title,url` (and
      the PR equivalent), the search-first cross-check, and the degradation
      clause. Keep it inside the "script deliberately does not judge these"
      block (`:64`) — this stays model judgment over a mechanical listing.
- [x] T2 — Add the triage disposition chip to §3 (`:83-101`), with the
      verbatim-above-the-chip requirement stated at the step; route the PR
      dispositions to `/hotfix` per M73.
- [x] T3 — Write the guard test; register it in the mutation harness; re-run
      `test_gate_wording.py` and `test_gate_conclusion_preview.py`, which
      assert on `/milestone`'s chip wording.
- [x] T4 — Bring the doc surfaces in line with M73: rewrite
      `cairn/DESIGN.md:69-70`'s trigger clause and `README.md:118`/`:194` so
      the PR door is described where a reader looks for architecture. `git
      grep` the whole repo for other pre-M73 trigger prose (M48/M58: sweep
      live files, excluding only history — DECISIONS, CHANGELOG, legacy,
      reviews archive).
- [x] T5 — Run all three suites from the repo root.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: /milestone-plan gated amendment — absorbed the M73-review-F5 candidate (stale `/hotfix` trigger prose in DESIGN + README) as AC6/T4 at user request; prior AC6 verify renumbered AC7/T5.
- 2026-07-18: implement started on m74-issue-triage; gate settled three open choices (bullet not subsection, extend §3's existing triage option not a second chip, new guard file).
- 2026-07-18: T1 — §2 untriaged-inboxes bullet is now a concrete step (both `gh` commands, search-first cross-check, three-case degradation clause); kept inside the `:64` judgment block per plan. Skills suite green (267).
- 2026-07-18: T2 — §3 resolves the sweep: four named dispositions (candidate row / `/hotfix` / `/milestone-plan` / leave), PRs routed to M73's door, verbatim-above-the-chip stated; extended the existing triage option rather than adding a second chip. Both registered blocks verified still unique.
- 2026-07-18: T3 — new `test_issue_triage.py` (18 tests) + 4 mutation entries (commands, search-first ordering, degradation floor, PR routing), each block verified unique and proven to fail when blanked. Hit the M23/M64 reflow trap live: the degradation directive wrapped mid-phrase, so the prose was reflowed to keep it on one line rather than weakening the assert. Skills suite 285 green.
- 2026-07-18: T4 — DESIGN Conventions bullet now says `/hotfix` is bidirectional; README gained an outside-PR row and the contributions bullet names both doors. Repo-wide sweep found the stale claim in live prose only at `DESIGN.md:69` (README's two spots were incomplete, not wrong).
- 2026-07-18: T4 amendment (step-6 gate, user approved) — AC6's evidence grep hit this milestone's own AC text (M62 trap); criterion amended to except it alongside the M58 history files.
- 2026-07-18: T5 — all three suites green from the repo root (scripts 96, skills 285, hooks 72); `cairn_validate` all checks passed. Status → review.

## Decisions
<!-- owner: implement / review · append-only -->
