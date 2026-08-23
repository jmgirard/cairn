# M156: Phase ends close with a standard block; gate chips stand alone

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Branch/PR:** m156-phase-close-block

## Goal

Every skill ends with one recognizable close — recap, status table, copyable next command — and every decision chip is posed in the same turn as its presentation and readable on its own, so the user always knows at a glance what to do next.

## Scope

**In:** The routing-chip mandate is replaced by a phase-close rule (the close block: outcome recap, status table or line, fenced next command(s) with plain one-line labels, a note that adjusting or `/clear` is safe); all ten skills' phase-end chips convert to it. The three chip-placement bullets shipped by M155 are rewritten to same-turn, self-sufficient decision chips (compact decision-relevant substance in question text and option descriptions; fuller evidence best-effort above and cited by file path where it exists on disk); the merge-approval gate follows the same form. The Accessible-language rule's identifier ban extends to option descriptions, chip text gains a no-record-identifier-filler standard, and its identifier-overflow clause reroutes to best-effort chat plus path citation. Guards retire/narrow/re-pin accordingly; rulebook-mass baseline re-seeds; one D-entry supersedes the founding routing-chip clause and one-click mechanism (D-003/D-022), absorbs the review-end exception (D-019) as the new norm, and narrows D-123's turn-break prong.

Surface tier: **user-facing** — the rulebook and every skill ending ship to adopting repos. Rules door (D-108/D-090): passed via the shipped-behavior trigger — the maintainer reports the M155 two-exchange flow as an interaction defect in what the skills do (this plan's driving conversation, 2026-08-22).

**Out:** any harness rendering fix (unchanged from M155's Out); reworking gate *content* beyond placement/readability (question batching, recommendation rules stand); `/milestone-review`'s merge-guard marker flow (unchanged).

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md` replaces the routing-chip mandate with a phase-close rule stating: a phase or skill end that previously posed a routing chip instead ends the turn with a close block in its final rendered text — an outcome recap, a status table or line (unit of work, status, branch/PR and check results where they exist), the next command or commands in fenced blocks (primary first, each with a one-line plain-language label), and one line noting that adjustments or `/clear` are both safe at this point; no chip is posed to route to the next skill, decision-gate chips (the merge-approval gate among them) are explicitly unaffected, and the review-end exception text is rewritten since chip-less closes become the norm. Evidence: the shipped lines quoted at review.
- [ ] AC2: The three chip-placement bullets — "Mandated substance renders", "Chips carry choices, not evidence", "Acceptance chips show what's accepted" — each state same-turn placement: the decision chip is posed in the same turn as its presentation, its question text and option descriptions alone carrying what the choice needs in plain language, fuller evidence best-effort above and cited by file path in the question text where it exists on disk; none retains an end-the-preceding-turn deferral; `grep -rn "posed after the user responds" --include='*.md' skills/` returning no hits corroborates. Evidence: the three bullets quoted and the empty grep output.
- [ ] AC3: The Accessible-language rule's identifier ban covers option descriptions as well as question text and option labels, states that chip text is written in plain language with no record-identifier filler (a single file-path citation in question text permitted), and its identifier-overflow clause routes the justification best-effort to chat above with the path citation — no clause directs it to a position the doctrine no longer provides. Evidence: the shipped lines quoted at review.
- [ ] AC4: Every line returned by `grep -rn -i "routing chip" --include='*.md' skills/` and every line returned by `grep -rn "AskUserQuestion" --include='*.md' skills/` on the milestone branch is dispositioned: it defines or cross-references the phase-close rule, states a decision gate, or was edited to one of those; no returned line instructs posing a chip to route at a phase end. Evidence: both sweeps' output with a per-hit disposition.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T2

## Tasks

- [x] T1: Rewrite `skills/shared/tracking-rules.md`: the "Question gates and routing chips" section becomes the phase-close rule (AC1); the three chip-placement bullets become same-turn self-sufficient form (AC2); the Accessible-language rule gains the description-ban, no-filler standard, and rerouted overflow clause (AC3); re-seed the rulebook-mass baseline in its three sites (M149 lesson).
- [x] T2: Run both AC4 sweeps; convert every phase-end chip in the ten skill files and `migration-protocol.md` to a close-block directive referencing the central rule, and update the decision-gate directives (plan gate, implement mini-gates, brief RB gate, review merge gate, milestone route triage, hotfix chips, init gates) to the same-turn self-sufficient form; per-hit dispositions in the work log.
- [x] T3: Guards: retire `TestRoutingChipMandate`, narrow `TestChipInvocationImperative` to gate-chip options naming a skill, re-pin every phrase the rewrites change, add guards + mutation entries pinning the phase-close rule and same-turn chip prong (M152 convention); hand-run `skills/tests` to zero reds.
- [ ] T4: Draft the batched D-entry (supersedes D-003's routing-chip clause and D-022's one-click mechanism; absorbs D-019; narrows D-123's turn-break prong). It states the why — explanation text before a chip going randomly missing is too costly for one-click routing to be worth it — and the re-open condition: a harness guarantee that pre-tool-call text always renders makes re-enabling one-click routing worth reconsidering. Preview verbatim per the durable-record rule.
- [ ] T5: Run both gating suites and `cairn_validate`; all green.

## Work log

- 2026-08-22: created by /milestone-plan from the maintainer's chip-flow feedback after M155 shipped.
- 2026-08-22: criteria audit ran in full mode ([O] fresh reader, one round): 4 findings, all repaired — AC1 scoped to the routing position with decision gates spared (the merge chip is IP1's) and the review-end exception rewrite added; AC2's domain moved from a grep proxy to the three named bullets, grep demoted to corroboration; AC3 gained the identifier-overflow-clause rewrite; AC4's dead archive carve-out dropped and a second AskUserQuestion sweep added.
- 2026-08-22: plan gate chose retiring all routing chips over milestone-loop-only because a mixed regime is drift bait (the repo's chip-mandate drift history); falsified by an adopting repo needing one-click routing back.
- 2026-08-22: plan gate chose the table+command close shape over lean prose and a heading banner because the fixed table is the at-a-glance boundary signal requested; falsified by the table proving noise in skills with empty cells.
- 2026-08-22: plan gate chose a uniform same-turn merge gate over a merge-only two-step because the on-disk Review section is the guaranteed evidence position and the extra exchange was the reported defect; falsified by a merge decided on a chip summary that the full findings would have changed.
- 2026-08-22: plan gate chose superseding the one-click decision over keeping a single implement-to-review chip because the typed command replaces the click uniformly at every hop; falsified by measured friction complaints after adoption.
- 2026-08-22: maintainer directive at the routing chip — the D-entry must record the supersession's why (randomly missing pre-chip text is too costly) and the re-open condition (a rendering guarantee reopens one-click routing); T4 refined (minor amendment).
- 2026-08-22: T1 done — section retitled 'Question gates and phase closes' with the close-block rule; the three chip-placement bullets rewritten to same-turn self-sufficient form; Accessible-language ban extended to descriptions with the no-filler standard and rerouted overflow; copy-run bullet re-anchored; invocation imperative retained for gate-chip skill options; rulebook 433/39,744 -> 441/40,716 (`wc -l -m`), baseline re-seeded in its three sites; one guard re-pointed to the same-turn sentence; all suites exit 0 (525 skills tests).
- 2026-08-22: T2 done — routing-chip sweep: 17 hits, 14 converted to close-block directives (hotfix 26; milestone 146; init 154,156,164,169,255; migration 184; design-interview 156; release 100 + its step-4 reference; brief 134; plan 280; implement 134,144; review 371-383 reworded to the generalized close), 2 reclassified as decision chips with relabels (migration 38 dry-run acceptance; design-interview 81 continue/stop), post-sweep `grep -rn -i 'routing chip' --include='*.md' skills/` returns nothing; AskUserQuestion sweep: 22 pre-edit hits, 12 decision-gate lines kept (hotfix 84,96; init 52,63,138,235; tracking-rules 253,256; design-interview 50; brief 44; plan 104; review 296,383), rest were the converted lines.
- 2026-08-22: T3 done — 8 guard reds fired on the edited lines (fired-guard proof); TestRoutingChipMandate retired with its subject, its merge-gate assert moved into new TestPhaseCloseBlock (6 asserts incl. a no-reintroduction sweep over skills/*/SKILL.md); 4 RULES-target mutation entries added; pins re-pointed in test_copy_run_handoffs, test_issue_triage, test_gate_conclusion_preview (+3 mutation blocks); implement's safe-`/clear`-point phrase restored inline per the D-048 guard's intent; skills/tests 528 exit 0; scripts/hooks/validate exit 0.

## Decisions

## Review
