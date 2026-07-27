# RB06: Why five review passes each found defects in the author's own verification (M114)

- **Date:** 2026-07-26
- **Output required:** write findings to `cairn/reviews/RR06-author-verification-failure-pattern.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

**cairn** is a Claude Code plugin that governs project tracking. A repo adopts
it and a set of skills drive work through a milestone lifecycle backed by
markdown under `cairn/`. This repo IS the plugin and dogfoods its own format.
`/milestone-review` verifies a finished milestone: it gathers fresh evidence
per acceptance criterion, runs a consistency gate, then spawns three
fresh-context review lenses plus an independent confidence scorer. A criterion
or gate failure returns the milestone to `in-progress` — a **return**.

Milestone M114 rewrote cairn's "thrash rule" (what happens as returns
accumulate) and added two rules to `skills/shared/guard-doctrine.md`. It has
been returned **five times**. A first Fable brief (RB05, archived) settled the
rule's *design* at the fourth return; that design is **not** in question here —
all three lenses cleared its substance at pass 5 and both of its numeric
tolerances were met exactly.

**What this brief asks about is the author, not the doctrine.** Across five
passes, every return was caused by defects in the author's *verification and
record-keeping around* a body of doctrine that has itself been sound since
pass 1. The author is a Claude Code session running these skills. You are being
asked to diagnose a repeating failure mode in that session's work and to say
what, if anything, cairn should do about it.

## Materials

**The primary record.** `cairn/milestones/M114-review-loop-escape-hatches.md`,
in full. Its five review sections — `## Review`, `## Review pass 2`,
`## Review pass 3`, `## Review pass 4`, `## Review pass 5` — carry every
finding with its confidence score and triage. Its `## Work log` records every
gate decision, each re-cut, and two superseded false claims.

**The three defect classes, with their evidence.** All ids below index into
those sections.

- *Class 1 — coverage the author under-pinned; found every single pass.*
  F1 (85) a rigid literal missing a wrapped fork; G1 (85) a detector with zero
  in-test positive controls, violating `guard-doctrine.md` §3 which **this
  milestone added**; G2 (83) and G3 (80) renderings the matcher could not see;
  H1 (95) controls with no non-vacuity assert, so the whole mechanism deleted
  green, violating `guard-doctrine.md` §7 which **this milestone also added**;
  L1 (90) an anchor narrowed to its pre-wrap half against the file's own
  documented rule; L2 (92) and L3 (88) two clauses an acceptance criterion
  explicitly required be pinned, both deletable green.
- *Class 2 — records drifting from the artifacts they describe.* G6 (68) and
  G7 (87) at pass 2; J3 (85) and J4 (85) at pass 4 — the same docstring, stale
  on two axes, after pass 2 had already corrected it; K1 at pass 4, a decision
  entry claiming a guard that had been deleted; K1 again at pass 5 (92), where
  the correction itself was made by editing an append-only record.
- *Class 3 — acceptance criteria the author wrote that encoded the wrong
  thing.* AC2's "repo-wide" was unsatisfiable and needed a gated amendment at
  pass 1; AC2 needed a **second** amendment at pass 2; AC11 as authored
  mandates an IP4 violation (pass 5, K1 at 92).

**Prior escalation.** `cairn/reviews/archive/RB05-thrash-trigger-precedence.md`
and `RR05-thrash-trigger-precedence.md`. RR05's eight Binding criteria are
AC1–AC8 of the milestone.

**Doctrine the author kept violating.** `skills/shared/guard-doctrine.md`,
especially §3 (a detector's matcher must be exercised at every rendering its
target can take) and §7 (a sweep whose cells may legitimately be silent passes
for free on silence). Both were added *by this milestone* and then violated
*by this milestone*.

**Lessons the author kept re-learning.** `cairn/LESSONS.md` — the
guard-authoring family: M95 (author anchors from the target's actual bytes,
never from the draft), M100 (the mutation engine sees only `Path.read_text`),
M103 (bind the record to its disposition, never the tally alone), M104 (editing
guarded prose can redden a *different* guard by reflowing its anchor), M105 (use
`\s+` to span a wrap), M113 (added prose can give an existing guard *false
coverage*).

**Decisions.** `cairn/DECISIONS.md` — D-045, D-054, D-057, D-059, D-062, D-064.
`cairn/DESIGN.md` — the IP/GP block, especially IP2, IP3, IP4.

**The code.** `skills/tests/test_thrash_rule.py` and its entries in
`skills/tests/test_mutation_harness.py` (search `guard="test_thrash_rule"`).
The rule itself is in `skills/milestone-review/SKILL.md`, the block beginning
`**Thrash rule.**`.

**Running things.** From the repo root: `python3 -m unittest discover -s
skills/tests`, `... -s scripts/tests`, `... -s hooks/tests` — check each exit
code separately, never pipe. Also `python3 scripts/cairn_validate.py`. To
experiment, export a scratch copy: `git archive HEAD | tar -x -C /tmp/<dir>`.
A partial copy yields a red baseline and misleads; verify your scratch baseline
is `exit=0, Ran 625` first. **Do not modify any tracked file** — a pass-1
reviewer did and contaminated a commit.

## Questions

1. **Is there a common root cause across the three classes, or are they
   independent?** The author's hypothesis is that each is a case of not
   re-deriving the records and guards that *describe* an artifact after
   changing the artifact. Test it against the evidence. Note the hypothesis was
   formed by the same judgment that produced the defects, and that pass 5
   produced three fresh Class-1 findings *after* the author had explicitly
   named Class 1 as the pattern — so a diagnosis that predicts the author can
   fix this by trying harder is contradicted by the record.

2. **Is cairn's review machinery working as intended, or compensating for
   something that should be prevented upstream?** Every defect *was* caught
   before merge by the three-lens fan-out plus scorer; nothing bad reached the
   default branch. Is five passes the system working expensively but correctly,
   or evidence that the author-verifies-own-work loop is structurally wrong for
   a milestone whose deliverable is doctrine about verification?

3. **Should cairn gain a rule for this, and if so which?** Candidates the
   author can see, each with an obvious cost: a mandatory re-derivation step
   after any artifact change; a rule that an acceptance criterion authored by
   the implementer is reviewed before implementation begins; a rule that a
   guard's author may not be the one who verifies it. Recommend for or against
   each with reasons, and reject the ones that do not pay. Any new rule must
   earn its lines (D-057); the rulebook is an always-read file.

4. **For M114 specifically: finish, park, or drop?** Four findings remain —
   K1 (92), L2 (92), L1 (90), L3 (88) — all small and mechanical. The
   exhaustion branch has fired and forbids *recommending* a bare retry; the
   maintainer chose escalation over parking and dropping. Given the pattern,
   is finishing right, and if so what would make a sixth pass different from
   the previous five?

5. **Is the scoring rubric or its application systematically biased?** Two
   findings scored below the 80 action threshold later mattered: F4 (60,
   logged at pass 1) predicted a trigger collision that then occurred at
   pass 3; J5 (35, logged at pass 4) predicted a miscount that then occurred
   at pass 5. Both were under-scored. Is the rubric wrong, is its application
   biased against exactly the findings that later matter, or are two instances
   insufficient evidence?

## Constraints

Fixed; flag disagreement explicitly rather than working around it.

- **RR05's design decisions are settled** and are not to be relitigated.
- **IP4 and D-045 — history is superseded, never edited.** K1 at pass 5 is
  precisely a violation of this, so nothing you recommend may weaken it.
- **Fable escalation stays gated per instance through the RB/RR protocol**
  (D-004, D-062). Do not recommend making it automatic or a standing menu item.
- **Rulebook growth is governed at the door** (D-057). `tracking-rules.md` is
  always-read; additions must earn their lines. Prefer a conditionally-read
  module where one fits.
- **D-059 is the precedent for retiring rather than repairing** a mechanism
  measured not to work. It cuts both ways here; use it honestly.
- **IP3 — nothing the user asked for is silently dropped.** **IP2 — prior state
  is surfaced, never silently obeyed or silently overridden.**

## Output format

In `RR06-author-verification-failure-pattern.md`: answer each question by
number with your reasoning and evidence; list any additional findings
separately under "Beyond the brief"; end with concrete recommendations, each
marked apply / consider / reject-with-reason. Where findings bind
implementation, also emit a `## Binding criteria` section: numbered `BC1…`,
each a measurable assertion checkable against evidence, with any numeric
projection stating its tolerance. These are ingested VERBATIM into the
constrained milestone's acceptance criteria and mechanically diffed against
this file; departures are legal only through that milestone's shown
"Deviations from RR06" table.
