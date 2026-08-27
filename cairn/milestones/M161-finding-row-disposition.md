<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M161: Finding-absorbing candidate rows get a disposition trigger at hygiene

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** —

## Goal

A candidate row that keeps absorbing deferred review findings is dispositioned
at a hygiene pass — promote, route to Known issues, or prune — rather than
extended indefinitely.

## Scope

**In:** One new prose section in `skills/shared/records-hygiene.md` stating
the disposition rule, plus one routing clause in each of the two hygiene
surfaces (`skills/milestone/SKILL.md` health audit,
`skills/milestone-review/SKILL.md` step 9). User-facing tier: the deliverable
is doctrine adopting repos' hygiene passes obey. Walks the records-conduct
door on its retained shipped-behavior trigger (D-108/D-090, hosted per
D-098): the shipped health audit's only candidate-triage trigger is a row
untouched ~6 months, structurally blind to a row extended every few days —
measured in quarto-index (a row holding ~55 filed findings, extended six of
ten days to 2026-08-26) and circumplex (rows compressed for byte budget with
no disposition, 2026-08-24 stamp).

**Out:** No validator or hook check — the rule is prose, judgment-applied at
hygiene passes (the checker-regress gate's simplify-first stance; D-057
untouched). No per-row byte allowance (rejected at the plan gate). No change
to tracking-rules — its existing records-hygiene pointer already covers the
module. The one-off triage of quarto-index's own row → that repo's next
planning session, not this milestone.

## Acceptance criteria

- [ ] AC1: `skills/shared/records-hygiene.md` carries a new `## 7.` section,
      at most 12 lines, stating the disposition rule: a candidate row already
      carrying deferred review findings filed from two or more distinct
      milestones (named in its provenance or weighed notes) is not silently
      extended again — the hygiene pass about to extend it (the `/milestone`
      health audit or `/milestone-review`'s post-merge pass) must pose a
      disposition chip covering: promote a bounded milestone for the items
      that guard shipped behavior; route items the user accepts to
      `cairn/DESIGN.md` Known issues (the review skill's accepted-limitations
      block); prune the rest; extend once more as an explicit choice, never
      the default. The section also states that compressing such a row to
      meet a byte budget never substitutes for the disposition, and defines
      "extended" as gaining a new provenance or weighed note without a
      disposition. Verified by reading the shipped section; the module stays
      under its header budget (`wc -l -c` reports under 55 lines and under
      4,000 bytes).
- [ ] AC2: both hygiene surfaces pose the chip at the moment of extension:
      `skills/milestone/SKILL.md`'s health-audit candidate-triage clause
      covers the finding-absorbing row (triaged even though not "untouched")
      and `skills/milestone-review/SKILL.md`'s step 9 poses the disposition
      chip when its hygiene pass is about to extend such a row; each clause
      defers the option list to the records-hygiene module section rather
      than restating it. Verified by reading each clause in place, with
      `grep -n` giving the line number confirming it falls inside the
      candidate-triage bullet and inside step 9 respectively.

## Coverage

- AC1 → T1
- AC2 → T2, T3

## Tasks

- [ ] T1: Author the records-hygiene `## 7.` section (≤12 lines), counting
      lines and bytes while writing against the 55/4,000 header budget.
- [ ] T2: Extend the `/milestone` health-audit triage clause
      (`skills/milestone/SKILL.md:110`) to fire on finding-absorbing rows and
      pose the disposition chip, deferring options to the module.
- [ ] T3: Add the disposition-chip clause to `/milestone-review` step 9
      (`skills/milestone-review/SKILL.md:320-379`), at the point the hygiene
      pass extends candidate rows.
- [ ] T4: Run both gating suites (`python3 -m unittest` over `scripts/tests`
      and `hooks/tests`, exit codes checked) and hand-run `skills/tests`;
      repair any prose-guard locator breakage by rewording new sentences,
      never pinned ones (M148 lesson).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-26: created by /milestone-plan.
- 2026-08-26: full criteria audit ([O] fresh reader, user-facing tier) ran over the two drafted ACs: 8 findings — 6 fixed in the wording as written (under-vs-at-most budget off-by-one; module-states/skills-pose voice; trigger keyed to provenance/weighed notes; section numbered §7 past the retired §3–§6; grep probe replaced by read-in-place location; audit chip defers options to the module), 2 routed to the plan gate (section size vs module budget; chip surface).
- 2026-08-26: plan gate chose the two-milestone recurrence trigger over a per-row byte allowance because size invites width-gaming and adds a number to maintain; falsified by a row absorbing findings from many milestones compactly enough to warrant disposition before any second-milestone note lands, or by recurrence firing so often the chip becomes noise.
- 2026-08-26: plan gate chose posing the chip at both hygiene surfaces over audit-only-with-review-flagging because the decision belongs at the moment of extension; falsified by step-9 disposition chips measurably delaying merges or being deferred routinely.
- 2026-08-26: plan gate chose proceeding through the records-conduct door (trigger argued met: the shipped audit's untouched-~6-months triage is blind to constantly-extended rows, measured in two adopter repos) over parking as a candidate row; falsified by evidence the accumulation self-corrects (rows drawn down without the rule) or that the rule fires only on healthy batching.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->
