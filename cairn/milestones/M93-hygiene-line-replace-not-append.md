<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M93: Hygiene-line accretion — the ROADMAP stamp is replaced, not appended

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP4, GP1, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m93-hygiene-line-replace   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make `Last hygiene check` a replaced one-line stamp rather than a growing
`Prior:`/`Earlier:` chain, and give the density advisory a per-line axis that
catches the accretion wherever it recurs.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the doctrine (the stamp is current knowledge under D-045, so it is
corrected in place, never appended to); a D-entry narrowing the standing
per-line rejection at `tracking-rules.md:109-111` to item lines; the
instruction at all three write sites plus the `/cairn-init` skeleton; a
`record density` per-line axis over non-item lines; guards; and pruning this
repo's own stamp.

**Out:**
- Editing intraclass's and circumplex's ROADMAP files → their own next
  `/milestone` audit, which the new advisory will flag (user decision,
  this session). This milestone reads them as live-fire evidence only.
- Preserving the existing `Prior:`/`Earlier:` chains anywhere → dropped;
  `git log` and `milestones/archive/` already own that detail (user
  decision, this session).
- A per-line axis over *item* lines (rows, candidate bullets, lessons) →
  stays rejected; D-052 narrows the rejection, it does not remove it.
- Raising or lowering the whole-file `CHAR_CAPS` thresholds → D-049 owns
  those; this milestone adds an axis beside them, it does not retune them.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 `tracking-rules.md` states that the hygiene stamp records the
      *current* check only — replaced each pass, never appended to — and
      grounds that in D-045's current-knowledge class, so the rule is
      visibly not an IP4 history edit. A guard pins the label to its rule on
      one physical line (M74/M92).
- [ ] AC2 The per-line rejection at `tracking-rules.md:109-111` is narrowed
      in place to item lines only, and `D-052` records the narrowing with
      the original rationale quoted. No standing rejection is left
      contradicted-but-unsuperseded.
- [ ] AC3 All four authoring surfaces carry the replace instruction:
      `skills/milestone/SKILL.md:104`, `skills/milestone-review/SKILL.md:185`,
      `skills/cairn-init/SKILL.md:109` (skeleton), and the tracking-rules
      rule from AC1. Evidence is a grep naming each file:line, scoped to
      the prose surface and exempting this milestone's own tracking lines
      (M58/M59/M62).
- [ ] AC4 `record density` gains a non-item-line axis at
      `NON_ITEM_LINE_CAP = 400` (derived below), reported as a WARN under
      the existing advisory label — never a FAIL, per the severity split at
      `tracking-rules.md:106`. It fires at 400 and is silent at 399, both
      directions proven.
- [ ] AC5 The new guard is non-vacuous on both known failure shapes: every
      absence-assert is paired with a positive signal that the path actually
      ran (`OK record density` in stdout), so a crash cannot read as a pass
      (M84's own F2/90 defect); and the advisory is run against the
      `/cairn-init` ROADMAP skeleton *instantiated* from
      `skills/cairn-init/SKILL.md:109`, not a fixture copy, which the
      skeleton passes (M77/M80). Registered in the mutation harness per
      file (M53).
- [ ] AC6 Live-fire, read-only: the new axis WARNs on circumplex's 3,152-char
      and intraclass's 1,870-char stamps and stays silent on ackwards' and
      openac's, and this repo's own stamp is under the threshold after its
      hygiene pass — the rule run over the artifact the milestone itself
      authors (M78). Evidence is command output with the counts written from
      it, never from memory (M28).
- [ ] AC7 `verify` clean: all three suites green, each exit code checked
      explicitly from the repo root, no piping (M56/M65).

## Coverage
<!-- owner: plan · create/amend-via-gate; review reads to fence evidence -->

- AC1 → T1, T5
- AC2 → T1, T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T1, T2, T3, T4, T5, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 In `skills/shared/tracking-rules.md`: add the replace rule to the
      hygiene-stamp doctrine and narrow the per-line rejection at lines
      109-111 to item lines. Author the label→rule clause on ONE physical
      line — a wrapped sentence is how these anchors go unpinned (M74).
- [ ] T2 Append `D-052` to `cairn/DECISIONS.md`: quote the original
      rejection verbatim, narrow it to item lines, and classify the stamp as
      D-045 current knowledge (which is what makes replacement lawful under
      IP4). Append-only; never edit a prior entry.
- [ ] T3 Wire the three write sites + the `/cairn-init` skeleton
      (`skills/milestone/SKILL.md:104`,
      `skills/milestone-review/SKILL.md:185`,
      `skills/cairn-init/SKILL.md:109`). Each currently says only "update",
      which is what reads as "append".
- [ ] T4 `scripts/cairn_scripts.py`: add `NON_ITEM_LINE_CAP = 400` beside
      `CHAR_CAPS` with the derivation in a comment. `scripts/cairn_validate.py`:
      extend `check_record_density` with the non-item-line axis. Item lines
      (table rows `|…`, bullets `- `) are exempt by construction, not by
      threshold. Warn at `n >= cap` — read the operator, do not assume the
      cap value is attainable (M87).
- [ ] T5 Guards in `scripts/tests` + `skills/tests`: the 400/399 boundary
      both directions, the positive `OK` signal, the instantiated-skeleton
      pairing, and the tracking-rules label→rule anchor. Register the new
      guard file in the mutation harness; verify by inversion — negate the
      rule in place, require red, restore and diff (M74).
- [ ] T6 Live-fire the advisory across the six surveyed repos (read-only —
      no commits outside cairn), record the counts from output, then prune
      this repo's own stamp and re-run `verify`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-19: created by /milestone-plan. Cap 400 derived from a six-repo non-item-line survey — healthy max 245, then 230/194/141/105/101/100, against defects at 1,870 and 3,152; warns at `>=` so it permits 399, leaving 154 chars (63%) of headroom over the observed healthy max and sitting 4.7×/7.9× under both live defects.
- 2026-07-19: implement gate — two open choices settled by the user. (1) `ROADMAP.md` was in NEITHER the history nor the current-knowledge list at `tracking-rules.md:159-162`, so AC1's D-045 grounding did not yet reach it; D-052 adds it to current knowledge rather than classifying the stamp alone. Found by reading the rule out of its source (M75/M85/M91), not assumed from the plan. (2) The `_Released …_` line (105 chars, +~33/release) gets NO exemption from the new cap — it crosses 400 in ~9 releases and the remedy is the milestone's own thesis.
- 2026-07-19: T1 — tracking-rules gained the replace rule, the current-knowledge enumeration gained `ROADMAP.md`, and M84's blanket per-line rejection is narrowed to item lines in place. The mutation harness reddened two registered anchors I had disturbed (`test_current_knowledge_set_is_enumerated_under_its_own_label`, `test_rule_records_why_a_per_line_warn_was_rejected`); M84's original rationale was restored VERBATIM on one physical line so its assert passes unchanged, while the enumeration assert + its `Mutation(...)` block were re-authored deliberately because that rule genuinely changed. 432/196/72 green, exit codes checked unpiped (M56).

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive; EXEMPT from the 150-line cap (M55) -->
