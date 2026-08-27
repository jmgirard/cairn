<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M161: Finding-absorbing candidate rows get a disposition trigger at hygiene

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** m161-finding-row-disposition · https://github.com/jmgirard/cairn/pull/162

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

- [x] AC1: `skills/shared/records-hygiene.md` carries a new `## 7.` section,
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
- [x] AC2: both hygiene surfaces pose the chip at the moment of extension:
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

- [x] T1: Author the records-hygiene `## 7.` section (≤12 lines), counting
      lines and bytes while writing against the 55/4,000 header budget.
- [x] T2: Extend the `/milestone` health-audit triage clause
      (`skills/milestone/SKILL.md:110`) to fire on finding-absorbing rows and
      pose the disposition chip, deferring options to the module.
- [x] T3: Add the disposition-chip clause to `/milestone-review` step 9
      (`skills/milestone-review/SKILL.md:320-379`), at the point the hygiene
      pass extends candidate rows.
- [x] T4: Run both gating suites (`python3 -m unittest` over `scripts/tests`
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
- 2026-08-26: T1 — records-hygiene §7 authored (12 lines incl. heading); trailing remainder-ledger comment compressed 8→5 lines to hold the module at 54 lines / 3,187 bytes (`wc -l -c`), under its 55/4,000 header budget; both gating suites green.
- 2026-08-26: T2 — health-audit triage clause extended (`skills/milestone/SKILL.md:111`, inside the staleness/candidate-triage bullet): finding-absorbing rows triaged even though not untouched, chip options deferred to records-hygiene §7; suites green.
- 2026-08-26: T3 — step-9 disposition clause added (`skills/milestone-review/SKILL.md:355`, between accepted-limitations routing and lesson retirement; step 9 spans 320–387), firing before the pass writes the extension, options deferred to records-hygiene §7; suites green.
- 2026-08-26: T4 — final sweep: scripts/tests and hooks/tests exit 0, skills/tests hand-run 528 tests OK (no locator breakage to repair), cairn_validate all checks passed; status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->

- 2026-08-26 AC1: read the shipped `## 7.` section in place — states the two-or-more-distinct-milestones trigger (keyed to provenance/weighed notes), names both hygiene surfaces, covers all four chip dispositions (promote bounded milestone / route to Known issues via the accepted-limitations block / prune / extend once as explicit choice), defines "extended", and states compression never substitutes. Section is 12 lines by `sed | wc -l` (heading through last body line); module `wc -l -c` = 54 lines / 3,187 bytes, under the 55 / 4,000 header budget.
- 2026-08-26 AC2: read both clauses in place. Audit clause at `skills/milestone/SKILL.md:111-115` (`grep -n finding-absorbing` → 111), inside the staleness/candidate-triage bullet spanning 101-116 (next bullet 117): finding-absorbing row triaged even though not untouched, options deferred to records-hygiene §7. Review clause at `skills/milestone-review/SKILL.md:355-362` (`grep -n` → 355), inside step 9 (320-387; step 10 at 388): chip posed before the pass writes the extension, options deferred to §7. Neither clause restates the option list.
- 2026-08-26 consistency gate: `cairn_validate` all checks passed; generic profile — no toolchain checks. Fresh suite runs: scripts/tests exit 0, hooks/tests exit 0, skills/tests hand-run 528 tests OK. No Driving RR — projection-vs-outcome no-op.
- 2026-08-26 review fan-out (user-facing tier → three lenses): [O] diff-bug 13 findings, [S] blame-history 2 (both duplicating O5/O6), [S] prior-PR-comments 1. Triage:
  - O2 (step-9 clause ordered after the accepted-limitations block it routes into) — fixed at gate: block moved above Route accepted limitations, now `skills/milestone-review/SKILL.md:351-358`, with a pointer to the block below; still inside step 9.
  - O8 (untouched-row chip and disposition chip share the audit bullet with no precedence) — fixed at gate: one clause added, a row meeting both triggers takes the disposition chip (`skills/milestone/SKILL.md:115-116`).
  - O13 (door-walk rationale lives only in the work log once the file archives) — actioned at step 9: the archive summary will name the D-108 door walk and its trigger.
  - O1 (D-108 door trigger argued weak — absence, not malfunction) — rejected: the door walk was decided at the plan gate with a recorded falsifier; re-litigating a user decision is not a diff defect. Surfaced to the maintainer at the gate.
  - O3 (§7 frames /milestone as "about to extend" though the audit only triages) — rejected: intentional; AC1 fixes §7's surface list and the audit clause self-labels its distinct trigger.
  - O4 (step 9 never names the action that extends a row; a step-7 write precedes the chip) — rejected: placement is plan-specified; §7 binds any pass about to extend, so a step-7 absorption is still covered by the module rule.
  - O5/B1 (ledger compression dropped per-section topic glosses) — rejected: deliberate, logged at T1; the ledger cites git for the full text and destinations survive.
  - O6/B2 (module headroom spent; 1 line slack) — rejected: informational; the budget header's own remedy governs the next addition.
  - O7 (trigger phrase verbatim in three files) — rejected: within contract (AC2 defers only the option list); each surface must state when it fires.
  - O9 (§7 promote vs §1 graduate-at-completion) — rejected: no conflict; promotion creates the milestone, §1 still holds the row until completion.
  - O10/P1 (§7 options carry no recommended marker or stop option; not in → /skill notation) — rejected: tracking-rules Contextual chip construction binds the chip at composition time; skill menus are examples, not scripts.
  - O11 (bare module path, not `${CLAUDE_PLUGIN_ROOT}`) — rejected: matches tracking-rules' own citation of this module; prose cross-reference, not an executed read.
  - O12 (post-merge chip is a new interruption) — rejected: informational; reviewer notes the mid-skill-decision clause permits it.
- 2026-08-26 post-fix re-verification: scripts/tests and hooks/tests exit 0, skills/tests 528 OK, `cairn_validate` exit 0. Return floor: no finding demonstrates an AC failing or a load-bearing deliverable defect — no status return; no amendment return.
