# M143: The thrash threshold recommends descoping before re-planning

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** `m143-descope-first-thrash` / https://github.com/jmgirard/cairn/pull/142

## Goal

At the thrash threshold `/milestone-review` recommends shrinking or parking
the milestone rather than re-cutting the same objective, because both
downstream lineages show a re-cut buying further returns, not a fix.

## Scope

**In:** recomposing `/milestone-review` step 4's thrash block whole — the
trigger-(a) threshold remedy, the both-triggers composition paragraph, and the
already-spent paragraph — plus re-anchoring the existing pins, a whole-slice
fixture for the block, the derivation of the downstream return counts, and one
D-entry narrowly superseding D-064's trigger-(a) remedy clause.

**Out:** trigger (b), the amendment-return track, and the widening test
(D-097/D-101) — untouched. Out: plan-side governors → M142. Out: the
step-6 *Substantive*-bullet pin coverage → the existing M140-review candidate
row, unpromoted (its trigger is an implement step-6 edit, not this).

## Acceptance criteria

- [x] AC1 `/milestone-review` step 4's thrash block is recomposed whole: at
      trigger (a)'s threshold the routing chip's recommended option is
      descoping — narrowing the milestone to its already-verified criteria via
      the gated amendment protocol, the unverified remainder exiting to
      candidate rows or a split milestone, followed by re-review of the
      narrowed set — or parking as `blocked` with the blocker named; a
      same-objective re-cut and dropping stay present options, the re-cut
      never recommended; the both-triggers composition paragraph carries (b)'s
      diagnosis and its `/milestone-brief` escalation offer into the
      recomposed menu rather than routing through `/milestone-plan`
      unconditionally. Registered prose-guards red when the recomposed remedy
      is deleted.
- [x] AC2 The already-spent paragraph is recomposed consistently with AC1:
      when (a) holds and a re-plan or split was already spent, the
      same-objective re-cut leaves the menu entirely; descope-or-park stays
      recommended, escalation and drop stay present. Existing pins in
      `skills/tests/test_thrash_rule.py` and the mutation registry are
      re-anchored to the recomposed bytes.
- [x] AC3 A D-entry narrowly supersedes D-064's trigger-(a) remedy clause
      ("recommend re-plan or split"), records the downstream lineage with its
      return counts derived from the source repos' work logs under both
      counting tracks (D-097, D-101) and pinned per the derived-figures
      rule — never asserted from recollection — and names the falsifier that
      reopens it, hosted per D-098. Suites green from the repo root with
      per-suite exit codes checked; new and edited guards registered per
      protected block; relabel, negation, transposition, and relocation probes
      run red on the recomposed remedy sentences; and the recomposed thrash
      block gains a whole-slice equality fixture in
      `skills/tests/test_thrash_rule.py` (D-103's instrument).

## Coverage

- AC1 → T2
- AC2 → T2, T3
- AC3 → T1, T4

## Tasks

- [x] T1 Derive the intraclass M120 return classification from its work log
      under the D-097 and D-101 tracks; record the pinned derivation
      (procedure + commit) in this milestone's work log as input to T4.
- [x] T2 Recompose the step-4 thrash block in
      `skills/milestone-review/SKILL.md` — threshold remedy, composition
      paragraph, already-spent paragraph — as one coherent menu across both
      states.
- [x] T3 Re-anchor the existing pins (`skills/tests/test_thrash_rule.py`,
      mutation-registry blocks) to the recomposed bytes; add the whole-slice
      equality fixture and guards for the new remedy sentences; probes red
      (commit fixes before any probe that restores — M140 lesson).
- [x] T4 Append the D-entry (next free id) with the derived, pinned lineage;
      run `cairn_validate` and the three suites from the repo root.

## Work log

- 2026-08-15: created by /milestone-plan, beside M142, from the maintainer's churn/thrash report over intraclass and circumplex.
- 2026-08-15: criteria audit ran (fresh [O] reader, two rounds) — round 1 returned findings 2/3/4/6 against this milestone (joint unsatisfiability, composition-paragraph under-scope, unverified lineage count, retired author-re-read instrument), all disposed at the gate; round 2 returned two residuals ("ships on" arm unreachable, missing whole-slice fixture), fixed in place.
- 2026-08-15: plan gate chose descope-first at the first threshold over flipping only after a spent re-plan because both downstream lineages show a re-cut buying further returns; falsified by descoped remainders repeatedly re-entering as their own thrashing milestones.
- 2026-08-15: T2 — step-4 thrash block recomposed in skills/milestone-review/SKILL.md (threshold remedy now descope-or-park with the re-cut demoted to present-never-recommended; composition paragraph composes the chip from (a)'s menu with (b)'s escalation carried in; already-spent paragraph drops the re-cut from the menu); trigger (b), the counting preamble and every step outside the block are byte-identical.
- 2026-08-15: T1 — lineage derived from the return and thrash lines of intraclass `cairn/milestones/M120-checkpoint-staleness-guard.md`'s work log, read at intraclass commit `1e95baf` (branch `m120-checkpoint-staleness-guard`): four defect returns (returns 1–3 whole; return 4's F1 leg) and one amendment return (return 4's F4 leg, recorded there under the widening test), so trigger (a)'s threshold was genuinely reached at return 3 on the defect track alone, not inflated by amendment returns; the re-cut spent after return 3 was followed by a fourth defect return, and the milestone was parked `blocked` at the maintainer's decision on 2026-08-15 — the exit this milestone makes the recommended default.
- 2026-08-15: T3 — pins re-anchored (5 guard tests rewritten, 7 registry blocks re-anchored, 4 registry blocks added), whole-slice THRASH_FIXTURE added from shipped bytes; relabel/negation/transposition/relocation probes each RED with restore byte-verified and the suite green after (probe script committed nothing mid-run; work was committed first per the M140 lesson); skills suite 785 OK, scripts 345 OK, hooks 103 OK, per-suite exit codes checked.

- 2026-08-15: T4 — D-105 appended (both lineages derived and pinned: intraclass at `1e95baf`, circumplex at `b343054f`); cairn_validate all checks passed with zero warnings; suites skills 785 / scripts 345 / hooks 103 all OK with per-suite exit codes checked; status -> review.

- 2026-08-15 fan-out: three lenses spawned ([O] diff-bug, [S] blame-history, [S] prior-PR-record); prior-record lens reports no regressions across every recorded trap (J2/L1/L2/L3, O-F1, M95/M104/M113/M123/M126/M131/M132/M136 lessons) and an empty PR-thread probe; blame lens confirms the RR05 composition fix preserved, registry coverage grown by 4 entries, D-097/D-101 byte-untouched. 17 candidate findings scored by fresh [S] scorer: 0 at/above 80 — actioned list empty. Sub-threshold, logged one line each:
  - F5/78: AC3's "both counting tracks" read as covering the circumplex lineage too; its figure is a milestone count by directory grep, not a work-log return count — surfaced verbatim at the approval gate.
  - F1/60: D-105's Consequences "re-cut present on the menu at every firing" reads against its own Decision's already-spent removal — repair, if wanted, is a later superseding entry (IP4).
  - F2/60: the composition paragraph carries (b)'s diagnosis and escalation but not (b)'s reconsider-the-alternative remedy, which now lives only in the never-recommended re-cut option.
  - F4/55: the circumplex grep procedure pins the count but not the consecutiveness/hardening characterization beside it.
  - F7/55: two stale docstrings (module bullet still said "the routing"; class said step-5-only) — fixed on the branch this pass.
  - F6/45, F10/45: the whole-slice fixture spans trigger (b) and the counting preamble (a two-site edit obligation on out-of-scope rules; defended in the fixture comment) and makes the four probe reds non-localizing.
  - B3/30, F3/30, F8/35, F9/30, F12/30, F13/25, F14/30, B8/15, F11/15, F15/20: pin-granularity, handoff-underspecification, wording and hygiene notes — logged.

- 2026-08-15 merge gate: maintainer directed F1/F2 fixed rather than accepted — D-106 appended (narrows D-105's at-every-firing clause; IP4 forbade an in-place edit), composition paragraph gains the (b)-remedy sentence with fixture/pin/registry re-anchored in the same commit; suites 786/345/103 OK, validate exit 0.
## Decisions

## Review

- 2026-08-15 AC1: all eight recomposed clauses verified PRESENT in the shipped bytes by exact-string probe (recommended descope-or-park with M143 tag; gated-amendment routing; remainder exit; re-review; park; re-cut demoted; composition menu; (b) carried into the composed chip) — one probe string initially misrendered a wrap and was corrected against the file's bytes, lines 141-142. Fresh deletion probe: removing the whole recomposed (a) remedy run reds the skills suite; restore byte-verified. Ticked on this evidence.
- 2026-08-15 AC2: already-spent clauses verified in shipped bytes ("the same-objective re-cut leaves the menu entirely"; "Descope-or-park stays the recommended option"; escalation and drop present at lines 141-142); the five rewritten guard tests and eleven re-anchored/added registry blocks pass inside the skills suite (785 OK), whose mutation-harness completeness and blank-reddening tests exercise every registered block. Ticked on this evidence.
- 2026-08-15 AC3: D-105 present (grep count 1), superseding exactly D-064's trigger-(a) remedy clause, both lineage counts derived and pinned (intraclass work log at `1e95baf` under the D-097/D-101 tracks: 4 defect + 1 amendment; circumplex `grep norms` over archive at `b343054f`: 14 files + M86), falsifier named in Consequences. Fresh at review: skills=0 scripts=0 hooks=0 (785/345/103 Ran), cairn_validate exit 0 zero warnings; relabel, negation, transposition and relocation probes each RED with restore byte-verified; THRASH_FIXTURE whole-slice equality test present and passing with both slice markers asserted unique. Ticked on this evidence.
