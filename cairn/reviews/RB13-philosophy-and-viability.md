# RB13: cairn's philosophy, thrash cycles, and long-term viability (repo-level)

- **Date:** 2026-08-16
- **Output required:** write findings to `cairn/reviews/RR13-philosophy-and-viability.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read what this brief
directs you to read, answer the numbered questions, and write your findings to
the output path above using the same numbering.

This brief is unusual in two ways, and both are deliberate. It is **repo-level,
not milestone-scoped** — no milestone is in flight and none is blocked on it.
And it invites you to **question the project's premises**, including premises
recorded as decisions. Every other RB in this repo asked you to solve a problem
inside cairn's frame; this one asks whether the frame is right.

## Background

### What cairn is

cairn is a Claude Code plugin providing one milestone-driven development
workflow plus a markdown project-tracking system. It ships nine skills
(`/cairn-init`, `/milestone-plan`, `/milestone-implement`, `/milestone-review`,
`/milestone`, `/hotfix`, `/cairn-release`, `/milestone-brief`,
`/design-interview`), one shared rulebook (`skills/shared/tracking-rules.md`)
with three conditionally-read doctrine modules, eight enforcement hooks, six
read-only reporter scripts, and a suite of "prose guards" — unit tests that
assert substrings of the shipped skill/rulebook markdown so a rule cannot be
silently deleted or reworded.

An adopting repo gets a `cairn/` directory: `DESIGN.md` (architecture,
principles), `ROADMAP.md` (the sole status authority), `milestones/` (+
`archive/`), `DECISIONS.md` (append-only), `LESSONS.md` (capped), `PROFILE.md`
(toolchain slots), `references/`, `reviews/`.

**This repo dogfoods its own system by hand.** cairn's own development is
tracked in `cairn/` using cairn's rules. So the artifacts you will read are
simultaneously the product and the process record.

### The maintainer's question

The maintainer asks, in their own words:

> Assess the current and recent status of cairn, and consider what you would
> build if starting this project over from scratch now. I'm primarily
> wondering whether our recent thrash cycles indicate a deep problem with our
> philosophy here. Self-documentation is a good goal, but are we trying to do
> or store too much? Is a cairn project really viable long-term?

"Thrash" is a term of art here: `cairn/DECISIONS.md` D-064 defines a thrash
threshold over review returns within one milestone, and D-105 (2026-08-15) just
changed its remedy from "re-cut the milestone" to "descope or park". The
maintainer's question is whether the thrash is a tuning problem inside the
system or a symptom of the system's design.

### The shape of the evidence, stated up front

You should know these before you read, because they frame what to look for.
Each figure below is **pinned**: measured at commit `0e0850d` on 2026-08-16 by
the command given.

- **143 milestones archived.** `ls cairn/milestones/archive/ | wc -l` → 143.
- **107 decision entries, ~4,000 lines.** `grep -c '^### D-' cairn/DECISIONS.md`
  → 107; `wc -l cairn/DECISIONS.md` → 4002.
- **The rulebook is 990 lines** (`wc -l skills/shared/tracking-rules.md`),
  against 1,748 lines of skill files total (`wc -l skills/*/SKILL.md`).
- **Guard tests outweigh shipped tooling ~4:1.** `wc -l skills/tests/*.py` →
  14,983 across 56 files (55 `test_*.py` plus the mutation engine);
  `wc -l scripts/*.py` → 3,437; `wc -l hooks/*.py` → 1,299. The tests are overwhelmingly prose-guards over markdown, not
  tests of executable behavior.
- **Twelve prior Fable escalations** (`ls cairn/reviews/archive/`), of which
  RB09, RB10, RB11 and RB12 all concern one mechanism (guard-doctrine §8 and
  its successors).
- **Recent milestone subject matter.** Run
  `for f in cairn/milestones/archive/M1[0-4]*.md; do head -1 "$f"; done` and
  read the titles of M100–M143. The maintainer's impression, which you should
  test rather than accept, is that nearly all of them change how cairn records,
  verifies, or governs *its own* records — not what an adopting repo can do.
- **Zero external adopters.** `cairn/DESIGN.md` "Known issues" records
  single-author, single-environment, no external adopter, no external-repo
  migration.

### The paradigm thrash arc, as recorded

The clearest recorded instance is guard-doctrine §8 (a self-certification loop
for guard authoring). Its arc, from the candidate row in `cairn/ROADMAP.md`
that summarizes it (search the Candidates section for "Standing-instrument
adoption discipline"):

> D-067 adopted a gating instrument on n=1 evidence straight into a gating
> position; its exit fired at M119 (4.5-round average) and was re-armed five
> times (D-079→D-080→D-083→D-085→D-091) before M127 retired the step at user
> mandate, while the yield-by-kind classification that settled it was derivable
> from on-disk records by ~M117.

That is roughly ten milestones and four Fable briefs spent on an instrument
that was ultimately deleted.

A second recorded pattern is **corrections of corrections**: D-099 corrected by
D-100; D-101 corrected by D-102, then annotated by D-103, whose asserted
annotation was itself drawn by D-104; D-105 corrected by D-106. A ROADMAP
candidate row ("Batch history-record corrections into one superseding entry per
milestone") exists for exactly this and records that the generator was thought
removed at M127 but the pattern recurred at M139.

## Materials

Read in this order. Where a file is long, the pointer says what to read for.

**Tier 1 — the system's own statement of itself (read fully):**

1. `cairn/DESIGN.md` (131 lines) — purpose, architecture, IP1–IP4, GP1–GP4,
   and the "Known issues" section, which is unusually candid and is itself
   evidence.
2. `skills/shared/tracking-rules.md` (990 lines) — the rulebook. This is the
   central artifact. Read it as a *reader arriving fresh* would, and note where
   you lose the thread.
3. `cairn/ROADMAP.md` (52 lines) — note the ratio of the Milestones table (5
   rows) to the Candidates section (~28 rows), and the length and internal
   structure of individual candidate rows.
4. `cairn/LESSONS.md` (49 lines) — note the length of individual "one-line"
   lessons and the `**Extended M<NN>:**` accretion pattern inside them.

**Tier 2 — the thrash record (sample, do not read exhaustively):**

5. `cairn/milestones/archive/M127-retire-certification.md` — the retirement of
   guard-doctrine §8, with a post-mortem.
6. `cairn/milestones/archive/M114-review-loop-escape-hatches.md` — a
   nine-round review loop and the escape hatches it produced.
7. `cairn/reviews/archive/RR05-thrash-trigger-precedence.md` and
   `cairn/reviews/archive/RR10-section8-survival.md` — two prior escalations on
   this exact class of problem. Note what they recommended and whether it
   worked.
8. `cairn/milestones/archive/M139-narrowing-at-the-return.md`,
   `M140-equality-guards.md`, `M142-stakes-tier.md`,
   `M143-descope-first-thrash.md` — the four most recent substantive
   milestones, all governance-of-governance.

**Tier 3 — what an adopter actually gets:**

9. `README.md` — the user-facing pitch.
10. `skills/milestone-plan/SKILL.md` and `skills/milestone-review/SKILL.md`
    (270 and 378 lines) — the two heaviest operational skills. Ask what a first
    session with these costs and delivers.
11. `skills/shared/guard-doctrine.md` (350 lines) and
    `skills/shared/records-hygiene.md` (97 lines) — the doctrine modules that
    grew out of `LESSONS.md`.

**Tier 4 — reference points, if useful:**

12. `cairn/references/competitive-landscape.md` — the positioning claim.
13. `cairn/references/effort-experiment-notes.md` — prior cost measurement.
14. `git log --oneline -80` — the recent cadence.

You may run the test suites (`python3 -m unittest discover skills/tests`,
`hooks/tests`, `scripts/tests`) and the reporters (`python3
scripts/cairn_status.py .`, `cairn_validate.py .`, `cairn_cost.py`), but you are
not required to. You are a **read-only** reviewer: do not edit any file other
than writing your RR.

## Questions

1. **Is the thrash a tuning problem or a structural one?** Characterize the
   recurring failure mode behind the §8 arc, the M114 nine-round loop, and the
   D-099→D-100 / D-101→D-104 correction chains. Name the *generator* — the
   structural property of cairn that produces these loops — or state with
   evidence that no single generator exists and the cases are unrelated. If a
   generator exists, say whether it is removable without abandoning the
   project's core premise.

2. **Self-reference: how much of cairn's work is cairn?** Classify M100–M143
   into (a) capability an adopting repo can use, (b) governance of cairn's own
   records, (c) verification of cairn's own verification, (d) other. Give the
   counts and your classification rule. Then say whether the ratio you find is
   pathological, healthy for a tooling project at this stage, or
   uninterpretable — and what evidence would distinguish those.

3. **Is the prose-guard architecture earning its cost?** cairn tests markdown
   prose with ~15,000 lines of substring assertions, plus a mutation harness to
   test the tests, plus `guard-doctrine.md` to teach authoring them, plus
   repeated milestones (M117, M121–M126, M131–M132, M140) fixing the guards
   themselves. Assess: does this mechanism prevent enough real regressions to
   justify its mass, and is there a fundamentally cheaper instrument for the
   thing it protects (agent-read rules not silently drifting)? Consider —
   without assuming — that the answer may be "accept prose drift and detect it
   differently", or "stop guarding prose entirely".

4. **Storage: what is cairn keeping that it should not?** Go file class by file
   class — `DECISIONS.md` (append-only, ~4,000 lines, never shrinks),
   milestone archives (143 files), `LESSONS.md`, `ROADMAP.md` candidate rows,
   `references/`. For each, say what a reader or agent actually retrieves from
   it in practice versus what it costs to maintain and read. Name anything
   whose retrieval value has fallen below its maintenance cost, and say what
   the honest disposal path is given IP4 (history is never edited or deleted —
   see constraint C2).

5. **Doing: what is cairn doing that it should not?** Same treatment for the
   process, not the storage: the review fan-out (three reviewers plus a
   confidence scorer per milestone), the plan-gate criteria audit, the RB/RR
   protocol, the weight caps and their remedies, the AC/Coverage fencing, the
   hygiene passes. For each, is it load-bearing, is it insurance the maintainer
   is paying a premium on, or is it ceremony? Be concrete about which you would
   cut first.

6. **Clean slate.** Suppose you are designing, today, a project-memory and
   change-control system for a single maintainer working with coding agents,
   with cairn's 143 milestones of experience available but none of its code.
   What would you build? Specify it at the level of: what state files exist,
   what is enforced mechanically versus by prose, what the workflow's gates
   are, and — critically — **what you would deliberately not build**. Say how
   large it would be. If your answer is materially smaller than cairn, name the
   specific things cairn has that you dropped and why they were not worth it.

7. **Which of cairn's ideas survive the clean slate?** From your answer to Q6,
   identify the parts of cairn that are genuinely good and would be reinvented:
   the ones a from-scratch designer would arrive at independently. Distinguish
   these from parts that are locally reasonable but exist only because an
   earlier cairn decision made them necessary.

8. **The self-documentation premise itself.** cairn's bet is that durable,
   governed, human-readable project state makes agent-driven development
   reliable across sessions and across context loss. State the strongest
   version of the case *against* that bet — including the possibility that
   agent context handling has improved (or will) enough to make heavy external
   state redundant, and the possibility that the state itself becomes a context
   burden that degrades the sessions it was meant to help. Then give your
   verdict on the bet as cairn has implemented it, separating the premise from
   the implementation.

9. **Long-term viability, plainly.** Is a cairn project viable long-term —
   maintainable by one person, adoptable by someone else, and net-positive over
   a multi-year horizon? Answer in one of four forms, and say which: **viable
   as-is**, **viable after a specific reduction** (name it), **viable only if
   re-founded** (point at Q6), or **not viable** (say what should happen to the
   work instead). Support the verdict with the evidence you gathered, not with
   general principle.

10. **The next three milestones.** Whatever your verdict, the maintainer needs
    a next action. Give three concrete, sequenced pieces of work that move
    cairn toward your recommended end state, sized as cairn milestones (one
    reviewable PR, 1–3 sessions each). If your recommendation is a large
    reduction, the first of these should be the smallest reversible step that
    tests it rather than a big-bang rewrite.

## Constraints

Flag disagreement with a constraint explicitly rather than silently working
around it — that is a legitimate finding, and for this brief especially, since
several constraints below are exactly the kind of thing the maintainer is
asking you to question.

- **C1 — You may recommend deleting anything, including principles.** No
  D-entry, GP, or shipped mechanism is off-limits as a *recommendation target*.
  What you may not do is treat one as already void: name it by ID, quote the
  prior rationale, and state why it should be superseded.
- **C2 — IP4 is a fact about the remedy, not a shield.** History files
  (`DECISIONS.md`, work logs, milestone archives, `reviews/archive/`) are never
  edited or deleted; a wrong or obsolete entry is superseded by a new one.
  Recommendations about the history corpus must therefore work by *reading
  less*, by bounding, or by ceasing to add — not by rewriting. If you conclude
  IP4 itself is the problem, say so directly; that is question 4's territory
  and C1 permits it.
- **C3 — Two standing closures exist and must be named, not stepped around.**
  D-057 closed the "size governance" program (measuring and capping file mass)
  as measured not to bind. D-090 closed the door on new verification or audit
  apparatus absent a shipped-behavior defect as trigger. A recommendation that
  re-opens either must say so and give the superseding rationale.
- **C4 — Do not propose new machinery as the answer to too much machinery**
  without arguing why this instance escapes the pattern the §8 arc records.
  This is the single most likely way for this review to fail usefully.
- **C5 — The audience is one maintainer.** cairn assumes a single operator;
  multi-operator support is a known unsupported case. Do not build
  recommendations on a team-scale premise.
- **C6 — Evidence over principle.** Every substantive claim about cairn should
  cite a file, a milestone ID, a D-entry, or a command you ran. Where you are
  reasoning from general software-design experience rather than from this
  repo's record, say so explicitly.

## Output format

In `cairn/reviews/RR13-philosophy-and-viability.md`: answer each question by
number with your reasoning and evidence. List any additional findings
separately under "Beyond the brief" — for this review those are especially
welcome, since the brief's framing is itself the maintainer's hypothesis and
may be wrong. End with concrete recommendations, each marked
**apply** / **consider** / **reject-with-reason**.

Lead the file with a short **Verdict** section — five sentences or fewer,
plain language, no cairn-internal identifiers — that answers questions 1, 8 and
9 in summary. The maintainer will read that first and it will be shown verbatim
at the ingestion gate.

**Binding criteria:** omit the `## Binding criteria` section. No milestone is
constrained by this review, and a binding-criteria block would pre-commit the
maintainer to work whose shape is exactly what is in question. If a specific
recommendation genuinely needs measurable acceptance criteria, state them
inside that recommendation as proposed criteria for a future milestone, clearly
marked as proposals rather than binding.
