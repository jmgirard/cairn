# RB07: Jointly unsatisfiable binding criteria and defects outside a frozen scope (M114)

- **Date:** 2026-07-26
- **Output required:** write findings to `cairn/reviews/RR07-unsatisfiable-criteria-and-frozen-scope.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

**cairn** is a Claude Code plugin that governs project tracking. A repo adopts
it and a set of skills drive work through a milestone lifecycle backed by
markdown under `cairn/`. This repo IS the plugin and dogfoods its own format.
`/milestone-review` verifies a finished milestone: fresh evidence per
acceptance criterion, a consistency gate, then three fresh-context review
lenses plus an independent confidence scorer. A criterion or gate failure
returns the milestone to `in-progress` — a **return**.

Milestone M114 rewrote cairn's **thrash rule** (what happens as returns
accumulate) and added two rules to `skills/shared/guard-doctrine.md`. It has
now been returned **six times**.

Two prior Fable briefs are archived and their answers are in force:

- **RR05** settled the thrash rule's *design* at the fourth return. That design
  is not in question here: all three lenses have cleared its substance at every
  pass since, and its numeric tolerances were met exactly.
- **RR06** diagnosed the *author* at the fifth return. Its finding: the author
  verifies descriptions against its generative model of an artifact rather than
  against the artifact. It rejected park and drop, chose to **finish via a
  constrained sixth pass** — "transcription, not authorship" — and issued eight
  binding criteria (BC1–BC8) that were ingested verbatim as M114's acceptance
  criteria AC1–AC8. BC6 froze the pass's scope. RR06 also produced three
  recommendations (4, 5, 6) that BC8 required be **banked outside M114**.

**Pass 6 has now failed, and it failed partly on RR06's own criteria.** Six of
the eight criteria verified with fresh evidence and every numeric projection
was met exactly (19 asserts against a projected 19; 0 blanking survivors
against 0; 3/3 red and 3/3 green on the prescribed probes; exactly 2 files
under `skills/`; 0 diff lines implementing the banked recommendations). Two
criteria failed, and they failed in different ways:

- **AC8 (BC8) failed on a real artifact defect (finding F3, scored 90).** One of
  the three banked ROADMAP candidate rows states its falsifier as *"drop if two
  such milestones pass review with zero coverage findings, RR06's own stated
  falsifier"*. That is a **count** — the exact shape of the never-a-count rule
  M114 itself ships — and RR06 states no such falsifier. RR06's actual falsifier
  is post-adoption and opposite in polarity. The author's own criterion-evidence
  line for AC8 had read the row and called it clean without checking it against
  RR06: RR06's diagnosed root cause, recurring inside the pass RR06 constrained
  to prevent it.
- **AC6 (BC6) failed as a *criterion*, not as work.** Its tracking-side sentence
  confines `cairn/ROADMAP.md` changes to *"status mirroring"*. BC8 mandates
  banking three recommendations *as ROADMAP candidate rows*. The pass's ROADMAP
  delta is 4 insertions / 1 deletion: the deletion is the status mirror, the
  three insertions are the rows BC8 requires. **The two criteria are jointly
  unsatisfiable as written**, and both are RR06's verbatim binding text.

Separately, two confirmed high-confidence defects **cannot be fixed on this
branch at all**:

- **F1 (92)** — guard-doctrine §7's operative remedy sentence is pinned by no
  assert and deletes green.
- **F2 (90)** — guard-doctrine §3's remedy assert is truncated at the shipped
  line wrap, so the remedy's continuation deletes green.

Both live in `skills/tests/test_lesson_graduation.py`, a **third** file under
`skills/`, while BC6's tolerance names **exactly two**. Fixing them fails AC6;
leaving them merges doctrine M114 ships with guards that do not guard it.

At six returns M114's own **exhaustion branch** fires: trigger (a) holds as a
threshold and a re-plan/split is recorded spent, so the rule forbids
recommending a bare retry and offers escalation, parking, or dropping. The
maintainer chose escalation. That is why this brief exists — and it is the
**third** brief on one milestone.

## Materials

**The primary record.** `cairn/milestones/M114-review-loop-escape-hatches.md`,
in full. Its six review sections (`## Review`, `## Review pass 2` … `## Review
pass 6`) carry every finding with its confidence score and triage; the
`## Work log` records every return and every gated amendment. The `##
Acceptance criteria` block holds AC1–AC8 (= RR06's BC1–BC8) verbatim; note
AC6's tracking-side sentence and AC8's "never a count" clause specifically.

**The prior reviews**, both archived:
- `cairn/reviews/archive/RR06-author-verification-failure-pattern.md` — its
  binding criteria at lines 354–401, its stated falsifier for recommendation 5
  at lines 173–176, and its rejection of park/drop.
- `cairn/reviews/archive/RR05-thrash-trigger-precedence.md` — the settled
  design of the rule.

**The shipped doctrine** (unchanged since pass 1 and cleared by every lens):
- `skills/milestone-review/SKILL.md`, step 4's thrash rule — the two triggers,
  their composition, and the exhaustion branch.
- `skills/shared/tracking-rules.md` — "Falsifying promotion conditions", AC
  fencing, the git/approval model.
- `skills/shared/guard-doctrine.md` §3 (matcher renderings, around line 95) and
  §7 (silent cells, around line 221).

**The guards and the two defects:**
- `skills/tests/test_thrash_rule.py` (19 doctrine-pinning asserts),
  `skills/tests/test_mutation_harness.py` (19 matching `Mutation(...)` entries),
  `skills/tests/test_lesson_graduation.py` (F1 at lines 118–127, F2 at line 92).
- **Reproducing F1 and F2.** Extract a scratch copy from the repo root —
  `git archive HEAD | tar -x -C <scratchdir>` — and verify its baseline is
  GREEN first (`python3 -m unittest discover -s skills/tests` from inside the
  copy: 627 tests, exit 0; a partial copy gives a red baseline and makes every
  mutation look caught). Then, in the copy's `skills/shared/guard-doctrine.md`:
  delete §7's sentence beginning "Assert per cell that it checked a positive
  number of things" — the suite stays green. Restore, then delete §3's remedy
  continuation after "Carry the renderings INTO the test as positive" while
  leaving that lead-in intact — the suite stays green.

**The banked rows.** `cairn/ROADMAP.md`, the three candidate rows tagged
"RR06 rec 4 / rec 5 / rec 6". Rec 5's row carries F3's misquotation.

**Do not modify any file in the repository.** Use `git diff`/`log`/`show`
against refs only; never `git checkout`, `git switch`, `git worktree add`, or
`git reset`.

## Questions

1. **BC6 and BC8 are jointly unsatisfiable.** Which yields, and what is the
   exact replacement text? Give the amended criterion verbatim, in a form that
   can be ingested through the gated-amendment route. State whether the fault
   is BC6's characterization ("status mirroring") being too narrow, BC8's
   mandate reaching into a file BC6 froze, or the practice of freezing a scope
   by enumerating files at all.

2. **F1 and F2 are confirmed ≥90 defects in guards over doctrine M114 ships,
   in a file BC6's frozen scope excludes.** Should the scope be widened so
   pass 7 fixes them, or should they be banked as a follow-up and the branch
   merged with the gap? Give the principled test that decides this — not just
   the verdict for these two — since a frozen scope will exclude some real
   defect every time it is used.

3. **Every route to `done` currently ends with the author certifying its own
   correction**, which is the mechanism RR06 measured as failing. RR06's
   recommendation 5 (independent certification of the description layer by a
   fresh-context reader) was banked *outside* M114 by BC8 — yet it is precisely
   the mechanism that would have caught F1, F2 and F3. Should it be applied to
   M114 itself before it can reach `done`, notwithstanding BC8? If yes, state
   the minimum form. If no, state what else breaks the self-certification loop.

4. **RR06 chose FINISH over park and drop**, on the premise that a constrained
   sixth pass was transcription rather than authorship. That premise is now
   falsified in two ways: the constraints were internally contradictory, and
   two real defects lay outside them. With six returns on the record, what is
   the disposition now — finish (under what constraints), park, split, or drop?
   Answer against the evidence, not against RR06's prior answer, and say
   explicitly if you are superseding it.

5. **This is the third Fable brief on one milestone (RB05 → RB06 → RB07).** The
   exhaustion branch that produced it is doctrine M114 itself ships. Is
   escalation-at-exhaustion working here, or has it substituted a brief loop for
   a review loop? If the branch needs a bound on its own escalations — or any
   other change — say so with the exact text; if it does not, say why three
   briefs on one milestone is a healthy outcome rather than a smell.

## Constraints

Fixed; flag disagreement explicitly rather than working around it silently.

- **The shipped doctrine text is settled** — the thrash rule, the
  falsifying-promotion-condition rule, and guard-doctrine §3/§7. RR05 settled
  its design; every lens has cleared it at every pass; it is byte-identical
  since pass 1 except for RR05's own prescribed rework. Do not relitigate it
  unless a question above forces it.
- **IP4 / D-045: history is append-only.** `cairn/DECISIONS.md`, work logs,
  `milestones/archive/` and `reviews/archive/` are never edited — a false record
  is superseded by a new appended entry. D-065 already applies this to D-064.
  Current-knowledge files (`ROADMAP.md`, `LESSONS.md`, `DESIGN.md`,
  `references/`) are corrected in place and marked.
- **No `cairn_validate` mechanization of judgment over prose** — D-064 choice 6
  declined it and D-059 retired a built-and-measured instance of it. Clause
  coverage and claim accuracy are judgment, not structure.
- **Rulebook growth is governed at the door (D-057).** A recommendation adding
  lines to `skills/shared/tracking-rules.md` must justify them against that.
- **Criteria are never reinterpreted at review.** If work seems right but a
  criterion as written fails, the criterion is wrong and is amended through the
  gate — a charitable reading is prohibited. This is why AC6 failed rather than
  being read as containing an implicit carve-out.
- **IP3: findings are surfaced, never silently dropped.** Sub-threshold findings
  are logged, not discarded.
- **Fable escalation is gated per instance (D-004, D-062)** and only ever
  through this RB/RR protocol.

## Output format

In `RR07-unsatisfiable-criteria-and-frozen-scope.md`: answer each question by
number with your reasoning and evidence; list any additional findings
separately under "Beyond the brief"; end with concrete recommendations, each
marked apply / consider / reject-with-reason. Where findings bind
implementation, also emit a `## Binding criteria` section: numbered `BC1…`,
each a measurable assertion checkable against evidence, with any numeric
projection stating its tolerance. These are ingested VERBATIM into M114's
acceptance criteria and mechanically diffed against this file; departures are
legal only through the milestone's shown "Deviations from RR07" table.
