# M173: A whole-list triage pass over candidates and Known issues

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP4
- **Resolves:** —
- **Branch/PR:** m173-candidate-triage

## Goal

Give cairn an on-demand `/cairn-triage` skill that reads every candidate row and every Known issues entry, proposes one disposition per item at one gate, applies the accepted ones in one docs-only commit, and records principled drops in a D-entry, so the lists are pruned when the operator asks instead of growing until a per-row hygiene chip nags.

## Scope

Surface tier: user-facing — a plugin skill that adopting repos run.

**In:** a new `skills/cairn-triage/SKILL.md` (frontmatter, session start, an
enumerate → assess → propose → gate → apply → record → close workflow); the
disposition vocabulary (keep, compress, merge, split, drop, promote, route)
with the staleness heuristics the assess step applies; a soft row shape and
~300-byte aim for `compress`, advisory and stated only in the skill; the
D-027-shaped per-pass D-entry for principled drops and trigger-losing merges;
one-line pointers from `/milestone` §2, `/milestone-review` step 9, README,
and the DESIGN.md architecture skill count; a CHANGELOG entry.

**Out:** LESSONS.md (its retirement rules stay with `/milestone-review`
hygiene); any validator, hook, threshold, or auto-trigger for the pass
(D-057/D-114: no size machinery without a measured regression; the pass is
on demand); changes to records-hygiene §7 or the `/milestone` staleness chip
(both stay per-row, M161); a fuzzy duplicate detector (rejected at M039;
merging stays judgment); grouping or sub-statuses for candidates (D-035
stands); planning a promoted row (that is `/milestone-plan`'s job, and the
row is pruned only at its milestone's post-merge hygiene, records-hygiene
§1); new prose-guard tests (hand-run since D-109; proportionality).

## Acceptance criteria

- [ ] AC1: `skills/cairn-triage/SKILL.md` exists with frontmatter (`name`, `description` naming the triggers "triage the candidates", "prune the backlog", "clean up the roadmap"), and its workflow reads every `- ` line under `## Candidates` in `cairn/ROADMAP.md` and every `- ` entry under `## Known issues` in `cairn/DESIGN.md`, assigning each exactly one proposed disposition from the vocabulary the skill states: keep, compress, merge (into a named surviving row), split (into named rows), drop, promote (handed to `/milestone-plan`, never planned in the pass), route (a candidate row to Known issues, or a Known issues entry to a candidate row). Verified by reading the skill text.
- [ ] AC2: The skill presents its proposals as one table in the chat above a single AskUserQuestion gate (item → disposition → one-line reason, with the evidence class behind each drop or merge) whose options are accept-as-proposed, amend (the user names the items to change), and apply-nothing; the skill text places every file write after that gate, and an amended or apply-nothing answer leaves every item not accepted untouched. Verified by reading the skill text.
- [ ] AC3: The skill records, in one `DECISIONS.md` entry per pass shaped like D-027's context / decision / consequences structure minus its counts (decision naming each removed item and its reason; consequences naming any prior entry superseded), every `drop` whose reason is a rejection on principle and every `merge` whose absorbed row's promotion trigger does not survive in the surviving row; a drop whose reason is a refuted premise or work already shipped is named in the commit message and the hygiene stamp instead, and `keep`, `compress`, `split`, `route`, and trigger-preserving `merge` write no D-entry. Verified by reading the skill text.
- [ ] AC4: Accepted dispositions land in one docs-only commit to the default branch, prefixed `triage:`, that also replaces the ROADMAP `Last hygiene check` stamp with one line naming what the pass changed; the skill's close block hands the user `/milestone-plan` for every `promote` item. Verified by reading the skill text.
- [ ] AC5: At review, running `/cairn-triage` in a fresh session against this repo's live `cairn/ROADMAP.md` and `cairn/DESIGN.md` reaches the gate with one proposed disposition for every `- ` line under `## Candidates` and every `- ` entry under `## Known issues` (counts read from the files at that commit), and selecting apply-nothing adds no entry to `git status --porcelain cairn/` beyond the pre-run state; a second run against a scratch copy of the repo whose `## Candidates` section is empty and whose `## Known issues` section is removed reaches the gate with an empty table and no failure.
- [ ] AC6: `skills/milestone/SKILL.md` (the §2 candidate-staleness bullet), `skills/milestone-review/SKILL.md` (the step-9 finding-absorbing-row clause), `README.md` (the "You want to…" table), and `cairn/DESIGN.md` (the architecture line counting skills) each name `/cairn-triage` in one line without restating its disposition vocabulary, and `CHANGELOG.md` carries an Unreleased entry for it — verified by reading each cited line, with `grep -l cairn-triage` over the five files confirming presence; `skills/shared/records-hygiene.md` is unchanged (`git diff --stat` shows no hunk in it).

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T4
- AC5 → T6
- AC6 → T5

## Tasks

- [x] T1: Draft `skills/cairn-triage/SKILL.md`: frontmatter, phase header (`# Triage` → `## Pass`), session start (ROADMAP, DESIGN Known issues, `### D-` heading scan, archive listing), and the enumerate step that lists every `- ` line of both sections with its byte length and added date.
- [x] T2: Write the assess step and vocabulary: for each item, evidence for staleness (premise refuted by an archived milestone — grep the archive for the row's subject; trigger already fired or unfireable; a cited path no longer exists), overlap (two rows on one subject → merge with lineage in the survivor), overgrowth (two triggers or an "and" goal → split; over the ~300-byte aim → compress to what-it-is / promote-when / provenance), misfiling (route), and readiness (promote → `/milestone-plan`); a row carrying findings from 2+ milestones takes records-hygiene §7's options inside this vocabulary. One optional `[S]` Explore fan-out only when rows cite code paths to check, per the delegation-warrant rule.
- [x] T3: Write the propose-and-gate step: the table above the chip, the three-option chip (accept / amend via named items / apply-nothing, stop option present), the no-write-before-answer ordering, and the amend loop (one re-presentation, then the chip again).
- [ ] T4: Write the apply, record, and close steps: edits to both files, the D-027-shaped D-entry for principled drops and trigger-losing merges only, the replaced hygiene stamp, one `triage:` docs-only commit and push, and the close block with fenced `/milestone-plan` lines per promoted item.
- [ ] T5: Pointer edits: `/milestone` §2 staleness bullet, `/milestone-review` step 9 §7 clause, README "You want to…" row, DESIGN.md skill count, CHANGELOG Unreleased entry; run both gating suites and the hand-run `skills/tests` suite.
- [ ] T6: Dry-run evidence for AC5: the fresh-session run over this repo (apply-nothing) and the empty-lists scratch-copy run; summarize both in one work-log line each.

## Work log

- 2026-09-03: created by /milestone-plan.
- 2026-09-03: criteria audit ran in full mode (user-facing tier, fresh [O] reader): 7 findings, all fixed before the gate — AC2 gate reshaped to accept/amend/apply-nothing and its no-write promise narrowed to the skill text's ordering; AC3 "D-027's structure minus its counts"; AC4 byte-reporting clause dropped (instrument property); AC5 gained the empty-lists scratch run; AC6 gained the DESIGN.md skill-count line and read-verification wording.
- 2026-09-03: plan gate chose a standalone `/cairn-triage` skill over a `/milestone` sub-mode and over doctrine-only in records-hygiene because the pass is on demand and `/milestone`'s audit already carries two per-row chips; falsified by operators reaching for `/milestone` to triage and never finding the skill.
- 2026-09-03: plan gate chose candidates + Known issues over candidates-only and over adding LESSONS because rows are misfiled in both directions while LESSONS has its own retirement rules; falsified by a LESSONS line that only a whole-list pass would have retired.
- 2026-09-03: plan gate chose a stated ~300-byte soft aim for `compress` over no target because rows average 529 bytes here; falsified by compressed rows losing the trigger or provenance a later sweep needs.
- 2026-09-03: plan gate chose D-entries for principled drops only over every-drop and over none because deferrals and refuted premises are ROADMAP facts, not decisions, while a rejection must be findable by search-first; falsified by a refuted-premise row being re-added because search-first reads no git log.
- 2026-09-03: implement started on `m173-candidate-triage`; question gate skipped — the plan settled every open choice (phase header, gate options, D-entry shape, commit prefix); no dependency changes.
- 2026-09-03: T1 done — frontmatter, session start, preconditions, and the enumerate step (per-item source/subject/bytes/date; empty or absent sections yield zero items). Discovered sub-task: `scripts/cairn_cost.py` PHASES gains `cairn:cairn-triage`, required by the gating test that maps every shipped skill to a phase. Both gating suites green (329 + 121).
- 2026-09-03: T2 done — seven-word disposition table, five evidence classes in check order (staleness, overlap, overgrowth, misfiling, readiness), the §7 and §1 mappings, and the delegation clause (one [S] Explore only for citation checks). Suites green.
- 2026-09-03: T3 done — proposal table shape (changes first, evidence class on every drop/merge), the three-option chip with its substance rule, the fixed no-write-before-answer ordering, one amend re-presentation then the chip again, and the untouched-unless-accepted clause. Suites green.

## Decisions

## Review
