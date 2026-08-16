# M145: Standing instruments scale to stakes

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, GP1
- **Branch/PR:** m145-stakes-scaled-instruments · PR #146 https://github.com/jmgirard/cairn/pull/146

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

- [x] AC1: `skills/milestone-review/SKILL.md` step 5 routes review rigor by
      stakes: for a milestone whose declared surface tier is internal and
      whose `git diff <default-branch>...HEAD --name-only` shows only
      markdown/tracking files, it prescribes exactly one fresh-context [O]
      diff reviewer; for every other diff it prescribes the three-lens
      fan-out — verified by reading the shipped step.
- [x] AC2: The `Score before triage` step and its 0–100 rubric are absent
      from step 5, which instead states that reviewers rank their own
      findings and the maintainer triages the ranked list at the gate, every
      reported finding logged in `## Review` (IP3) — verified by reading the
      shipped step; residue sweep: every hit of `grep -rn "scorer" skills/
      README.md cairn/DESIGN.md` (skills/tests/ excepted) dispositioned in
      the Review section.
- [x] AC3: Step 5's return counting operates on maintainer-actioned
      findings, and step 5 contains no numeric confidence score, threshold,
      or band — verified by reading the shipped step, every digit-bearing
      line of the step dispositioned in the Review section.
- [x] AC4: `skills/milestone-brief/SKILL.md` and
      `skills/shared/templates/brief.md` make an RR advisory by default: a
      `## Binding criteria` section is requested only on an explicit
      maintainer choice recorded at RB-authoring time, and a brief whose
      subject mechanism is on its second-or-later escalation — counted by
      sweeping `cairn/reviews/` and `cairn/reviews/archive/` for briefs
      naming the same mechanism — lists removal among its options.
- [x] AC5: `skills/milestone-plan/SKILL.md` step 3 scales the criteria audit
      by stakes: user-facing tier, or any drafted criterion or task carrying
      an RB-tripwire tag, gets the full audit; internal tier gets a reduced
      audit — the same fresh-context [O] reader asking only the
      bounded-promise and proportionality questions of each criterion. The
      shipped step states that the reduced mode keeps the disposal rule and
      omits the probe question; both modes record one work-log line naming
      the mode, and an absent line still means no audit ran.
- [x] AC6: Two superseding D-entries are appended, each naming what it
      supersedes in its heading: one narrowly superseding D-016's scorer
      clause — the Never-Haiku blanket stands — and superseding D-078; one
      narrowing D-067's criteria-audit clause to the stakes-scaled form,
      D-079 clause 2's record rule surviving in both modes.
- [x] AC7: `python3 -m unittest discover -s scripts/tests` and
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
- [x] T5: Run both gating suites; hand-run `skills/tests` and disposition
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
- 2026-08-16: T5 done — scripts/tests + hooks/tests exit 0; skills/tests hand-run: 813 tests, 22 failures + 12 errors, every red mapped to an M145 intentional edit (scorer/fan-out guards, return-floor slice fixtures, audit-block pins, brief template, §5, harness registrations on changed bytes; full log scratchpad kt.log); AC2 residue sweep: 2 hits, both the retirement's own record. Status → review.
- 2026-08-16: triage record moved from Decisions to Review — a same-session anchoring slip, corrected before the gate (the line is review content, not a milestone-local decision).

## Decisions

## Review

- 2026-08-16 AC1: shipped step 5 read — both routing bullets present verbatim (internal-tier docs-only → "spawn **one** fresh-context reviewer"; "Any other diff" → "spawn the full three-lens fan-out"), predicate names the tier and `git diff <default-branch>...HEAD --name-only`. PASS.
- 2026-08-16 AC2: "Score before triage" and "0–100" absent from step 5; "rank its own findings", "maintainer triages the ranked" list, and "surfaced, never silently dropped (IP3)" present. Residue sweep: 2 hits — tracking-rules.md:766 (the retirement's own record) and records-hygiene.md:68 (§5 tombstone comment) — both legitimate records of the change, not live scoring steps. PASS.
- 2026-08-16 AC3: return floor and actioned-list definition operate on maintainer triage ("Over the actioned list"; "the findings triaged fix-now or follow-up"); ≥80/≥90/below-80/80–89 all absent. All 17 digit-bearing lines of the step enumerated and dispositioned: step numbers (3,4,6), milestone ids (M36/M91/M130/M139), decision ids (D-078/D-097/D-064), the `per_page=1` API parameter, "AC<N>" — none a confidence score, threshold, or band. PASS.
- 2026-08-16 AC4: brief SKILL.md:29-36 states advisory-by-default, BC on the maintainer's explicit recorded choice, and the second-or-later-escalation removal option with its reviews-sweep counting procedure; template :39 emits BC "ONLY if this brief explicitly requests one", :47 lists removal on second-or-later escalation. PASS.
- 2026-08-16 AC5: plan SKILL.md:114-155 — modes selected by tier/tripwire (:121-122), reduced audit = bounded-promise + proportionality only, "omits the satisfiability, reachability, and probe questions", "keeps the disposal rule below in full" (:143-145), record line "naming the mode" with the absent-line rule intact (:153-155). PASS.
- 2026-08-16 AC6: D-110 heading narrowly supersedes D-016's scorer clause (Never-Haiku stands) and supersedes D-078; D-111 heading narrows D-067's criteria-audit clause with D-079 clause 2 surviving — both at DECISIONS.md:4081/:4110. PASS.
- 2026-08-16 AC7: fresh runs — scripts/tests 345 tests exit 0; hooks/tests 103 tests exit 0. PASS.
- 2026-08-16 skills/tests hand-run (D-109 cadence, non-gating): 813 tests, 22 failures + 12 errors; each red dispositioned as an intentional M145 re-wording — scorer/fan-out guards (test_review_fanout), return-floor and widening slice fixtures (test_thrash_rule; fixture reds prove slice coverage, M143 F10), audit-block pins (test_fresh_context_readers, test_stakes_tier), brief template (test_finding_enforcement), §5 pins (test_records_hygiene_graduation), and mutation-harness registrations over changed bytes. Zero defect-classified reds.
- 2026-08-16 fan-out triage (maintainer, at the gate): 24 findings across three lenses (prior-review lens clean; blame-history 3; diff-bug 21). Actioned fix-now (14): step 5/6/7 triage-ordering coherence (F1/F2), amendment-audit mode at two sites (F3), the two §5 triage heuristics folded into step 5 (F4), D-112 appended for the routing decision (F5), carve-out + single-reviewer + probe-clause + ingest-mode wording (F8-F11), brief template comment placement and a named Binding-criteria header slot (F12/F13), twin re-sync on the dropped citation (F19), D-113 batching the two D-111 corrections (F16/F17) with D-110's spawn count corrected inside D-112 (F18). Follow-ups: the sub-threshold-findings row dropped as fulfilled at hygiene (user-approved); the stakes-tier row's changed shape → M147 ledger (F15). Rejected with reasons, logged: F6 (step-1 sync makes ..// ... coincide at routing time; three-dot is branch-own-content semantics), F7 (the tier conjunct carries prose-as-product repos under D-107's spanning rule), F20 (the ledger pins its snapshot commit; a re-run diffing the changed corpus is the instrument working), F21 (tombstone transitional, deleted by M146's trim; guard-doctrine's retired §8 is the numbering precedent), blame-1 (D-109's falsifier instrument is the hygiene run, unchanged; D-110/D-112 are the append-only record), blame-2 (transitional, module deleted at M146), blame-3 (D-061 records a graduation event, not a no-retirement guarantee). Post-fix: validate exit 0, scripts/tests + hooks/tests exit 0.
