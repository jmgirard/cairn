<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M152: Chat and record prose gain a plain-style rule

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** m152-plain-style-rule

## Goal

Give the rulebook a sentence-level plain-style rule for chat output and for durable records, so cairn sessions stop reading as verbose, jargon-laden, trope-filled prose.

## Scope

**In:** User-facing tier — the rulebook ships to every plugin adopter. Trigger (D-108/D-090, recorded per the door's retained clause): a maintainer-reported defect in shipped behavior — cairn sessions' chat output and records remain verbose and trope-filled despite D-039 and the M147 record diet (reported 2026-08-22). Two rulebook rules (chat style in Output & interaction discipline; record prose in Universal tracking rules, with the derived-claims exemption sentence naming the new governor and the lesson-ownership exit widened to the rulebook); `prompting-opus-5` references-page extension and re-verification; a sweep of the skills' own prose for padding-inviting instructions; one hand-run prose-guard pin.

**Out:** user-level `~/.claude/CLAUDE.md` style snippet → delivered conversationally after this plan, not repo work; length governance of shipped artifacts beyond records (README, skills, code) → already governed by GP1, the weight caps, and D-119, no cited defect; M114-lesson trim and other hygiene acts → `/milestone-review` post-merge hygiene, never criteria (D-120).

## Acceptance criteria

- [ ] AC1: The "Output & interaction discipline" section of `skills/shared/tracking-rules.md` carries a prose-style rule for chat output, placed in that section (whose binding sentence it inherits), whose operative content states at least: response length matched to what the turn needs; plain words over jargon, with terms of art glossed or dropped; and no stock filler phrasing, hype adjectives, or padding.
- [ ] AC2: The "Universal tracking rules" section of `skills/shared/tracking-rules.md` carries a record-prose rule whose operative content states at least: durable records under `cairn/` (work-log lines, D-entries, milestone-file sections, LESSONS lines, ROADMAP rows, archive summaries) state decision-relevant facts in plain words; characterizations the facts do not need (adjectives, superlatives, hype) are omitted; and record length is matched to the record's job (the length standard AC1's rule states, applied by cross-reference, not restated). The derived-claims exemption sentence names the new rule among the governors of tracking records.

## Coverage

- AC1 → T2
- AC2 → T3

## Tasks

- [x] T1: Re-read the `prompting-opus-5` source page (curl the `.md` sibling per the page's provenance); extract verbatim any response-verbosity/prose-style guidance with section anchors, or record a dated found-none observation; mark the re-read inline on the extraction status; replace the two stale Traces-to anchors (`tracking-rules.md:553`/`:650`) with stable bullet-title anchors.
- [x] T2: Author the chat prose-style rule (AC1) in "Output & interaction discipline", beside the narration-discipline bullet; add its Traces-to entry.
- [x] T3: Author the record-prose rule (AC2) in "Universal tracking rules"; amend the derived-claims exemption sentence to name it; widen the lesson-retirement ownership exit to "another tracking file's slot, or the shared rulebook" (doctrine-prose repair within the surfacing milestone, D-090); add its Traces-to entry.
- [x] T4: Sweep the skills' own prose (`grep -rniE 'recap|summar|restat|verbatim|report' skills/*/SKILL.md skills/shared/*.md`) for instructions inviting output longer than its purpose needs; trim hits on the branch, keeping D-039's named carve-outs (durable-record preview, acceptance chips); one work-log line records the dispositions.
- [x] T5: Add one hand-run prose-guard pin in `skills/tests` covering both new rules' spans (M148 lesson: reword new sentences near pinned slices, never the pinned ones); record the guard beside each Traces-to entry.
- [x] T6: Re-seed the three rulebook-mass baselines (M149 lesson: `skills/milestone/SKILL.md` cost line, `test_cost_audit_line.py:67`, `test_mutation_harness.py:117`); run both gating suites and hand-run `skills/tests` from the repo root, exit codes checked (M56 lesson).

## Work log

- 2026-08-22: created by /milestone-plan.
- 2026-08-22: plan criteria audit ran in full mode (fresh [O] reader, two rounds): round 1 — 13 findings on the draft pair (record-act criterion demoted to tasks, unverifiable citation clause dropped, stale Traces-to anchors surfaced); round 2 on the gate-added AC2 — 10 findings (domain enumerated, "or deliverable" cut as exceeding the claimed trigger, exemption-sentence amendment added, M114 lesson trims rather than retires).
- 2026-08-22: plan gate chose plugin rule + user-level snippet over user-level-only because the plugin ships the fix to every cairn adopter; falsified by the rule proving inert in adopting repos while the personal snippet alone suffices.
- 2026-08-22: plan gate chose chat+record scope (D-108 trigger claimed) over chat-only because the reported defect names records too; falsified by record verbosity recurring only through genre rules a style rule cannot reach.
- 2026-08-22: plan gate chose one hand-run pin over no guard because guide-sourced rules are pinned by convention; falsified by the pin costing locator churn (M148 shape) without ever catching a drift.
- 2026-08-22: step 2 chose central-rule placement over per-skill wiring per D-039's precedent for continuous conduct; falsified by style drift recurring despite the central rule (D-039 names per-skill wiring as the superseding entry).

- 2026-08-22: T1 done — source page re-fetched (12,483 bytes), no drift in prior values; § Response length and verbosity + § User-facing progress updates extracted (4 new values, incl. the positive-examples-beat-prohibitions finding that shapes T2/T3 wording); stale Traces-to line anchors replaced with bullet-title anchors.
- 2026-08-22: T2 done — "Plain style" bullet added to Output & interaction discipline; Traces-to entry added; skills/tests hand-run: 513 OK. (T1 line above re-seated at log end, restoring append order after a mis-placed insert.)
- 2026-08-22: T3 done — record-prose rule added to Universal tracking rules; exemption sentence names it; ownership exit widened to the shared rulebook (doctrine-prose repair, D-090); Traces-to entry added; all three suites green (exit 0).
- 2026-08-22: T4 done — sweep run (named grep + a detail/thorough/explain pass over the same files): 119 hits, zero trims — every hit is mandated substance under D-039's carve-outs or a functional report-the-result step; no padding-inviting instruction found.
- 2026-08-22: T5 done — test_plain_style.py added (2 classes, 6 asserts) pinning both rules; Traces-to entries name the guard; 519 skills/tests green.
- 2026-08-22: registry-completeness red caught post-commit (checkpoint chained past the exit code — the M56 shape); fixed by registering 6 Mutation entries for test_plain_style, harness green.
- 2026-08-22: T6 done — three mass baselines re-seeded to 412 lines / 37,468 chars (M152); skills 525 / scripts / hooks suites all exit 0; cairn_validate green. All tasks complete; status → review.

## Decisions

## Review
