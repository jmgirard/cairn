# RB04: Redteam the tiering + mechanization + inviolable-budget proposal (M96)

- **Date:** 2026-07-20
- **Output required:** write findings to `cairn/reviews/RR04-rulebook-governance-redteam.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

**This is a REDTEAM brief, and that framing is deliberate.** RB01–RB03 asked
for open analysis and produced findings that the implementing session then
softened (evidence in Background). This brief asks you to *attack a specific
proposal* before it is built. Your default posture is adversarial: try to
break the proposal, find where it fails, and say so. A finding that the
proposal is unsound is the most valuable output you can produce. Do not
improve it into something you like and then endorse that — critique what is
actually written here.

## Background

### What cairn is

cairn is a Claude Code plugin providing a project-tracking system: milestone
files, a ROADMAP, a DECISIONS log, and phase skills (`/milestone-plan`,
`/milestone-implement`, `/milestone-review`, `/hotfix`, others). Its rules
live in `skills/shared/tracking-rules.md`, which **every skill reads whole at
every invocation — 3–4× per milestone.** This is the "always-read core". The
repo dogfoods its own system under `cairn/`.

### The problem

`tracking-rules.md` grows monotonically. Measured sizes at recent milestone
merges:

| Milestone | Lines | Δ |
|---|---|---|
| M92 — lesson retirement (gave LESSONS an outflow) | 748 | +13 |
| M93 — hygiene-stamp accretion fix | 765 | +17 |
| M97 — bounded DECISIONS read | 779 | +14 |
| M98 — lesson graduation to a doctrine module | 788 | +9 |
| M95 — **rulebook editorial slimming** | 779 | **−9** |

Sustained inflow ≈ **+13 lines / milestone**. Note that M92, M97 and M98 were
themselves *anti-growth* milestones and each still added lines. The file grew
33,746 → 52,797 chars across M63–M93 (+56%).

### The governance failure (the maintainer's actual complaint)

Three Fable reviews have been commissioned. The maintainer's stated
frustration is that **findings keep getting contradicted or softened by the
session implementing them**, and that each cycle ends by deferring the real
fix to "limit future growth" while itself adding more rules. The concrete
chain:

1. **RR02** diagnosed the growth as restated rationale and prescribed an
   editorial pass: "state the rule, cite the D-entry, delete the defense",
   projecting ~165–215 lines.
2. **M95's first implement run** built a 21-block ledger, found 9 of 21 blocks
   had no D-entry home and 14 were guard-pinned, and **stopped**, declaring
   RR02's premise refuted.
3. **RR03** (`cairn/reviews/archive/RR03-rationale-lifecycle-architecture.md`)
   found M95's acceptance criterion was itself the defect, established that
   the rulebook is *current knowledge* so justification is deletable against
   git, and projected an honest yield of **~60–100 lines**.
4. **M95's second run** (re-cut against RR03) removed 25 lines, **added 16**,
   net **−9** — and then recorded in `cairn/DECISIONS.md` as **D-056** that
   "The test predicts no yield" and that the shortfall should be read "as
   evidence the rulebook's mass is mostly class 1/2, not as a quota a later
   pass owes."
5. **An independent full-file classification sweep** (2026-07-20, results in
   "The measurement" below) then found **65 line-equivalents (8.4%) of
   removable-or-citable mass** — roughly what RR03 predicted, and 2.6× M95's
   gross removal. D-056's inference is therefore wrong and is now permanent
   history under IP4, requiring a superseding entry.

The pattern to keep in view: **the agent that adds rules is the agent that
judges whether they are necessary, and it is also the agent that interprets
the review findings constraining it.** Every existing rule came from a real
failure, so the marginal judgment is always "add, and keep everything."

### The measurement (independent full-file sweep, 2026-07-20)

First sweep of the whole file ever performed; earlier passes worked a
21-block candidate list inherited from RR02's falsified hypothesis.

| Class | Line-equivalents | % of 779 |
|---|---|---|
| Structural (blank, heading, separator) | 86 | 11.0% |
| **1 + 2 — operative (rules + application doctrine)** | **~628** | **80.6%** (90.6% of content lines) |
| 3 — decision-owned (compress to rule + cite) | ~27 | 3.5% |
| 4 — free-floating justification (delete) | ~38 | 4.9% |
| **3 + 4 combined** | **~65** | **8.4%** |

Concentration — three sections hold 55% of removable mass in 25% of the file:
**Weight caps 22.5%**, **What gets a test 15.7%**, **References pages 14.9%**.
Leanest large section: Output & interaction discipline, 1.4%.

Two further sweep findings:
- **A fifth class the current test does not name: intra-file restatement**
  (~10 lines) — rules stated in full in one section and restated in another.
  The three-step placement test in D-056 misroutes these to "rule" (they *are*
  rules), which may be part of why prior passes stalled.
- Only **~4.3 line-equivalents have no D-entry home at all**, against the
  9-of-21 that stopped M95's first run — that figure was an artifact of which
  blocks were nominated.
- Sweep verdict: yield is **one-time**. After a thorough pass the file sits
  ~97% operative; controlling inflow remains the durable lever.

### Existing mechanical enforcement surface

- `scripts/cairn_validate.py`: **23 checks** (15 hard CHECKs, 8 advisories)
- **40 guard files** under `skills/tests/`
- **278 mutation-registered blocks** in `skills/tests/test_mutation_harness.py`

Some rules are stated in always-read prose *and* enforced by a check
(e.g. "Absolute dates only", terminal-row retention's "5 most recent",
`ROADMAP.md` "< 60 lines").

## The proposal under review

Three parts, proposed by the orchestrating session and **not yet
implemented, planned, or recorded** anywhere in `cairn/`.

**A. Tier the always-read core by read-trigger, not by importance.**
A rule belongs in `tracking-rules.md` only if a session that does not already
know it would violate it. Rules binding at one phase move into that phase's
`SKILL.md` or a conditionally-read module. Rationale by analogy: M97's largest
single win in this programme came from bounding the *read* of `DECISIONS.md`
rather than its size.

**B. Make mechanization the primary outflow.**
A rule already enforced by a `cairn_validate` check or a guard test does not
need always-read prose; it shrinks to a pointer or is dropped. Claimed to be
strictly better than compression: enforcement strengthens, read cost goes to
zero. Claimed advantage over prior approaches: "is this already enforced by a
check?" has a mechanical answer, whereas "is this important?" — the question
every prior pass asked — is answered "yes" by every author.

**C. A hard inflow budget, as an inviolable principle (IP) rather than a
guiding one (GP).**
The always-read core gets a fixed line budget set by the maintainer, not
derived by an agent. Adding to the core requires displacing something or
demonstrating no conditional trigger exists, and **`/milestone-review` rules
on that, not the implementing author**. Rationale: GP means "tradeable with
stated justification"; GP1's bounded-read-cost goal has been traded away
repeatedly (D-049 recorded one such trade explicitly, D-053 amended GP1 after
its stated mechanism was found false, and M95 effectively made another).

## Materials

Read these. Sizes given so you can budget.

- `skills/shared/tracking-rules.md` — **779 lines**, the file under governance.
  Read whole; it is the subject.
- `cairn/DECISIONS.md` — **~1,650 lines, 57 entries.** Read the `### D-`
  headings, then read whole these entries: **D-056** (the placement test and
  the wrong inference, near end of file), **D-045** (history vs current
  knowledge), **D-049** (density thresholds; records a trade against GP1),
  **D-052** (per-line axis; ROADMAP as current knowledge), **D-053** (GP1
  amended), **D-030/D-046** (cap exemptions), **D-031** (domain doctrine gets
  a module — the precedent part A would extend), **D-055/D-051** (lesson
  outflows), **D-004** (Fable gated per instance).
- `cairn/DESIGN.md` — the IP/GP block (IP1–IP4, GP1–GP4). Short.
- `cairn/reviews/archive/RR01-architecture-retrospective.md` — **rec 15** is
  the standing rejection part A must supersede: "the cross-skill contract
  (file map, caps, status, git model, gates, output discipline, profiles
  mechanism) stays monolithic".
- `cairn/reviews/archive/RR02-weight-management-architecture.md` — Q3 rejects
  a level threshold on this file for an n=1 population with no oracle; Q5
  upholds rec 15.
- `cairn/reviews/archive/RR03-rationale-lifecycle-architecture.md` — Q5
  ("three fitted mechanisms, one shared frame"; every always-read file needs
  an inflow test, an outflow or read-bound, and an attention signal), Q6 (GP1
  amendment), rec 10 (rejects a unified lifecycle across files).
- `cairn/milestones/M96-rulebook-growth-ratchet.md` — the currently-planned
  milestone this proposal would displace or reshape: a growth-since-last-pass
  ratchet modelled on the `references staleness` advisory.
- `scripts/cairn_validate.py` — the 23 checks. Skim for what is mechanically
  enforced today.
- `skills/shared/guard-doctrine.md` and `skills/shared/validation-doctrine.md`
  — the two existing conditionally-read modules; the precedent for part A's
  destination.
- Run `python3 scripts/cairn_validate.py` and
  `python3 -m unittest discover -s skills/tests -q` from the repo root if you
  want to see the enforcement surface live.

## Questions

Answer by number. Be adversarial: for each, the most useful answer is a
concrete failure mode with evidence, not an endorsement.

1. **Does part A (read-trigger tiering) actually reduce cost, or relocate
   it?** If a rule moves from `tracking-rules.md` into three phase skills that
   each need it, total bytes rise and the duplication must be kept
   consistent — cairn already has a guard-locked deliberate duplication of
   this kind (`test_default_branch_parameterized.py`). Model the realistic
   outcome: how many of the 628 operative lines are genuinely single-phase,
   and what does tiering cost in duplication, drift risk, and guard count?
   Give a number or a defensible range, and if the answer is "less than the
   overhead", say so.

2. **RR01 rec 15 says the cross-skill contract stays monolithic, upheld by
   RR02 Q5 and RR03 Q5. Is part A's distinction — "must never be violated" is
   not the same claim as "must be read every time" — a genuine narrowing of
   rec 15, or a rationalization that rec 15 already anticipated and
   rejected?** Quote rec 15's actual reasoning. If it does not survive, say
   what it should be superseded *with*.

3. **Attack part B specifically. What fraction of the 23 checks and 40 guard
   files have an always-read prose twin that could be retired, and what is the
   realistic line yield?** Then the harder half: **what breaks when prose is
   removed in favour of a check?** Consider at minimum — a check reports a
   violation after the fact while prose prevents it; a check cannot convey
   *why* or how to apply a rule (the sweep's "class 2 application doctrine",
   which is 90.6% of the file's operative mass); an agent that never reads the
   rule cannot follow it proactively, only be corrected by a failing gate.
   Is part B strictly better as claimed, or is that claim false?

4. **Is part C's IP framing sound, or does it fail the way GP1 failed?**
   `DESIGN.md` says changing an IP requires an explicit user decision plus a
   D-entry. A budget that can be raised by the same gate that raises anything
   else may be no more binding than a GP in practice. Specifically: what stops
   an implementing session from proposing a budget increase at its own
   question gate and the maintainer approving it under time pressure — the
   exact softening dynamic in Background? Propose a stronger mechanism if the
   IP framing is inadequate.

5. **Who is the counterparty, really?** Part C assigns the add-to-core ruling
   to `/milestone-review`. But `/milestone-review` is an agent running in the
   same session lineage, reading the same rulebook, and its fresh-context
   reviewers are spawned by the implementing orchestrator. Is "review rules on
   it" a real check, or theatre? If it is theatre, what would a real
   counterparty be — a mechanical gate, a diff-level constraint, the
   maintainer, something else?

6. **Is the fifth class (intra-file restatement) evidence of a deeper defect
   in D-056's three-step test?** The test routes by "does deleting change
   behavior", which answers *yes* for a restated rule even though the file
   loses nothing by cutting the copy. Should the test be restructured, and if
   so, what replaces it — noting D-056 is already permanent history requiring
   a superseding entry.

7. **Given the sweep says the yield is one-time (~97% operative after a
   pass), is any stock-side mechanism worth building at all?** M96's ratchet
   fires when mass grows past a stamp, and its escape is "perform a pass" —
   which after the one-time harvest has no remedy left. Should M96 be built,
   re-cut, or dropped? If dropped, say what replaces it.

8. **The failure this whole programme keeps reproducing is that a correct
   finding gets softened by the session implementing it** (Background, step
   4 — the finding was even converted into a durable decision record arguing
   against the finding). No mechanism in cairn prevents this; the acceptance
   criteria are prose interpreted by the implementer. **What would actually
   stop it?** This is the maintainer's central question and the one they most
   need answered. Concrete mechanisms only — "be more careful" is not an
   answer.

9. **Steelman the null option.** Argue the strongest case that a 779-line
   always-read rulebook read 3–4× per milestone is simply *not a problem worth
   more milestones*, that the ~10 sunk on weight governance exceed any read
   cost saved, and that the correct move is to stop governing size entirely
   and accept monotone growth. If this is right, say so plainly — it would be
   the most valuable finding in this brief.

## Constraints

Fixed. Flag disagreement explicitly rather than working around it silently.

- **IP4 (history integrity)** — `DECISIONS.md` is append-only; supersede,
  never edit or renumber. D-056's wrong inference must be *superseded*, not
  corrected in place. RR03 Q4 examined IP4 and found no case against it.
- **D-004** — Fable is gated per instance; this review is that gate exercised.
- **D-045 / D-052** — the history vs current-knowledge split, and the rulebook
  being current knowledge (D-056 part 1, which the sweep *supports* — only its
  yield inference is disputed).
- The maintainer sets any budget number. **Do not derive a target and present
  it as the answer** — three prior agent-derived targets (RR02's 550–600,
  RR03's 60–100, M95's outcome) were each renegotiated by the next agent. If
  you recommend a budget, present it as an input for the maintainer to set,
  with the tradeoff at each level.
- You may recommend rejecting any or all of parts A, B, and C. The proposal
  has no standing; nothing has been built. Rejecting it costs nothing but this
  review.

## Output format

In `cairn/reviews/RR04-rulebook-governance-redteam.md`: answer each question
by number with your reasoning and evidence; list any additional findings
separately under "Beyond the brief"; end with concrete recommendations, each
marked **apply / consider / reject-with-reason**. Where you disagree with a
predecessor review (RR01, RR02, RR03) or with a standing D-entry, say so
explicitly and name it.
