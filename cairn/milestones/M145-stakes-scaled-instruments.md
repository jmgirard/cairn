# M145: Standing instruments scale to stakes

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, GP1
- **Branch/PR:** m145-stakes-scaled-instruments

## Goal

`/milestone-review`, `/milestone-brief`, and `/milestone-plan` scale their
standing verification instruments to the stakes of what they check — or stand
them down (RR13 recs 5–7 and B1; RR13 carries no Binding criteria, so it is
advisory lineage, not a Driving RR). User-facing tier: the skills ship to
every adopting repo.

## Scope

**In:**
- `/milestone-review` step 5 routes by stakes: internal-tier milestone whose
  diff touches only markdown/tracking files → one fresh-context [O] diff
  reviewer; any other diff → the three-lens fan-out. The confidence scorer is
  removed from both paths: reviewers rank their own findings, the maintainer
  triages the ranked list at the gate, every reported finding logged in
  `## Review` (IP3).
- The defect-return and amendment-return counting re-based on
  maintainer-actioned findings (the ≥80/≥90 score tiers go with the scorer).
- `/milestone-brief` + `templates/brief.md`: an RR is advisory by default —
  a `## Binding criteria` section only on the maintainer's explicit choice at
  RB authoring; a brief on a mechanism's second-or-later escalation (counted
  by sweeping `cairn/reviews/` + `archive/` for briefs naming it) lists
  removal among its options.
- `/milestone-plan` step 3: the criteria audit scales by stakes — full for
  user-facing or RB-tripwire-tagged work; a reduced two-question form
  (bounded-promise + proportionality) for internal tier.
- `records-hygiene.md` §5 (reading a review scorer) removed with its subject;
  `tracking-rules.md` fan-out/scorer text and the archive-summary template's
  "with scores" wording updated.

**Out:** the rulebook reduction → M146; the LESSONS/candidate diet → M147;
AC fencing, the merge-approval gate, and the RB/RR approval protocol —
untouched.

## Acceptance criteria

- [ ] AC1: `skills/milestone-review/SKILL.md` step 5 routes review rigor by
      stakes: for a milestone whose declared surface tier is internal and
      whose `git diff <default-branch>...HEAD --name-only` shows only
      markdown/tracking files, it prescribes exactly one fresh-context [O]
      diff reviewer; for every other diff it prescribes the three-lens
      fan-out — verified by reading the shipped step.
- [ ] AC2: The `Score before triage` step and its 0–100 rubric are absent
      from step 5, which instead states that reviewers rank their own
      findings and the maintainer triages the ranked list at the gate, every
      reported finding logged in `## Review` (IP3) — verified by reading the
      shipped step; residue sweep: every hit of `grep -rn "scorer" skills/
      README.md cairn/DESIGN.md` (skills/tests/ excepted) dispositioned in
      the Review section.
- [ ] AC3: Step 5's return counting operates on maintainer-actioned
      findings, and step 5 contains no numeric confidence score, threshold,
      or band — verified by reading the shipped step, every digit-bearing
      line of the step dispositioned in the Review section.
- [ ] AC4: `skills/milestone-brief/SKILL.md` and
      `skills/shared/templates/brief.md` make an RR advisory by default: a
      `## Binding criteria` section is requested only on an explicit
      maintainer choice recorded at RB-authoring time, and a brief whose
      subject mechanism is on its second-or-later escalation — counted by
      sweeping `cairn/reviews/` and `cairn/reviews/archive/` for briefs
      naming the same mechanism — lists removal among its options.
- [ ] AC5: `skills/milestone-plan/SKILL.md` step 3 scales the criteria audit
      by stakes: user-facing tier, or any drafted criterion or task carrying
      an RB-tripwire tag, gets the full audit; internal tier gets a reduced
      audit — the same fresh-context [O] reader asking only the
      bounded-promise and proportionality questions of each criterion. The
      shipped step states that the reduced mode keeps the disposal rule and
      omits the probe question; both modes record one work-log line naming
      the mode, and an absent line still means no audit ran.
- [ ] AC6: Two superseding D-entries are appended, each naming what it
      supersedes in its heading: one narrowly superseding D-016's scorer
      clause — the Never-Haiku blanket stands — and superseding D-078; one
      narrowing D-067's criteria-audit clause to the stakes-scaled form,
      D-079 clause 2's record rule surviving in both modes.
- [ ] AC7: `python3 -m unittest discover -s scripts/tests` and
      `python3 -m unittest discover -s hooks/tests` both pass (the
      PROFILE.md verify slot).

## Coverage

- AC1 → T1
- AC2 → T1, T5
- AC3 → T1
- AC4 → T2
- AC5 → T3
- AC6 → T4
- AC7 → T5

## Tasks

- [x] T1: Rewrite `/milestone-review` step 5
      (skills/milestone-review/SKILL.md:149–269): stakes routing, scorer
      removal, return counting on maintainer-actioned findings; update the
      fan-out bullet at skills/shared/tracking-rules.md:751–766 (and the
      :719–727 carve-out if its wording no longer holds) and
      skills/shared/templates/archive-summary.md:14.
- [x] T2: `/milestone-brief` BC opt-in and second-escalation removal option
      (skills/milestone-brief/SKILL.md:72–115);
      skills/shared/templates/brief.md:38–44.
- [x] T3: `/milestone-plan` step 3 audit scaling
      (skills/milestone-plan/SKILL.md:114–149).
- [x] T4: Remove `records-hygiene.md` §5 and fix the tracking-rules.md:280
      mapping clause; draft, preview, and append the two superseding
      D-entries.
- [ ] T5: Run both gating suites; hand-run `skills/tests` and disposition
      every red in the Review section (scorer-guard reds expected as
      intentional); run the AC2 residue sweep.

## Work log

- 2026-08-16: created by /milestone-plan (RR13 step 2, gate round 1).
- 2026-08-16: criteria audit ran ([O] fresh reader): A-AC2/A-AC3 proxy greps replaced with read-the-step promises + dispositioned sweeps; A-AC6 narrowed to D-016's scorer clause; A-AC4 gained its escalation-counting procedure; A-AC5's stakes form was a gate judgment call; re-audit of the gate-amended A-AC5 returned OK with two notes, both folded into AC5's shipped-text clause.
- 2026-08-16: plan gate chose stakes-routed single-reviewer over deleting the fan-out outright because the diff-bug and blame lenses have real code catches on the record (RR13 §5); falsified by an internal doc-only regression a retired lens would demonstrably have caught.
- 2026-08-16: plan gate chose the reduced two-question internal-tier audit over RR13 rec 7's full skip because D-107's internal-tier standard would otherwise have no execution path; falsified by reduced audits returning zero findings across successive internal-tier milestones.
- 2026-08-16: plan gate chose defaults-first ordering over the candidate row's reduction-first because M146/M147 then review under the lighter regime; falsified by the new routing misclassifying M146's mixed diff.
- 2026-08-16: T1 done — step 5 rewritten (stakes routing, ranked findings, gate triage, re-based return floor); tracking-rules fan-out bullet + archive-summary template updated; both gating suites exit 0.
- 2026-08-16: T2 done — RRs advisory by default (BC section on explicit recorded request only), second-escalation briefs list removal; brief skill step 1 + template Output format edited.
- 2026-08-16: T3 done — audit scaled to stakes (full vs reduced mode, mode named in the record line); the probe question's guard-doctrine citation dropped in passing, shrinking an M146 T2 site; both gating suites exit 0 (covers T2's template edit too).
- 2026-08-16: T4 done — records-hygiene §5 deleted whole (retired-section comment left, numbering stable), mapping clause trimmed; D-110/D-111 previewed and appended; validate exit 0, no dangler batch unmasked.

## Decisions

## Review
