# RB02: Weight-management architecture — are per-file hand-derived caps the right mechanism? (M94)

- **Date:** 2026-07-19
- **Output required:** write findings to `cairn/reviews/RR02-weight-management-architecture.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

**What cairn is.** cairn is a Claude Code plugin that gives a repo a
milestone-based tracking system: markdown state files under `cairn/`
(ROADMAP, DECISIONS, LESSONS, DESIGN, per-milestone files) plus nine skills
(`/milestone-plan`, `/milestone-implement`, `/milestone-review`, `/hotfix`,
…) that read a single shared rulebook, `skills/shared/tracking-rules.md`.
This repo *is* the plugin and dogfoods its own format by hand. Validation is
three Python `unittest` suites plus `scripts/cairn_validate.py`, which runs
hard CHECKs (gate failures) and soft advisories (WARNs) over the `cairn/`
files.

**What triggered this review.** The maintainer observed that milestones were
getting slower and asked whether the test suite or cairn itself was
responsible. Measurement (2026-07-19):

- Wall clock, `plan M<NN>` commit → `review M<NN>: done` commit: median ~23
  min across M63–M68, ~39 min across M88–M93. Confounded by scope and human
  latency; directional only.
- Test suites: 722 tests, ~37s total. Not test count — `skills/tests` runs
  441 tests in 0.50s while `hooks/tests` runs 72 in 16.5s and
  `scripts/tests` 209 in 21.6s (subprocess-spawn bound). At ~6 verify runs
  per milestone, ~10% of a milestone.
- Re-read volume, the larger share. Growth M63 (2026-07-16) → M93
  (2026-07-19), 30 milestones:

  | File | M63 | M93 | Δ | Governed by a cap? |
  |---|---|---|---|---|
  | `skills/shared/tracking-rules.md` | 33,746 ch | 52,797 ch | +56% | **no** |
  | `cairn/DECISIONS.md` | 47,389 ch | 95,976 ch | +103% | **no** |
  | `cairn/ROADMAP.md` | 2,861 ch | 9,777 ch | +242% | yes (<21,000 ch, <60 lines) |
  | `cairn/LESSONS.md` | 16,165 ch | 20,618 ch | +28% | yes (<20,500 ch, <50 lines) — at cap |

  The two capped files are the two that did not become a problem; the two
  largest always-read files have no weight governance at all. `cairn_validate`
  reports all-green on this state.

**Why this needs independent review, and not just a threshold.** Milestone
M94 set out to give both ungoverned files a threshold. Two rounds of
maintainer gating failed to produce a defensible basis:

- `tracking-rules.md` is a *plugin* file — exactly one instance exists in the
  world — so there is no population to derive a threshold from. cairn's
  established derivation method (see M87 below) derives a character threshold
  from a file's own *line cap* at measured mean item length; neither
  ungoverned file has a line cap, which is precisely why they are ungoverned.
- A threshold set above today's mass blesses the state the investigation
  flagged as the defect. A threshold set below it, enforced as a hard CHECK,
  makes the repo's own `verify` gate unreachable until a large deferred
  refactor lands. An advisory anchored on the pre-slowdown baseline is
  available but frankly correlational.

**The pattern that motivates the architectural framing.** Milestones whose
*goal* is weight management, by date of creation:

```
2026-07-12  M32  terminal-row retention
2026-07-13  M55  milestone-file cap — exempt the review-owned section
2026-07-17  M69  cap-overrun diagnostic (per-section breakdown)
2026-07-18  M77  work-log cap exemption
2026-07-18  M84  record-density advisory — item caps gain a character-mass axis
2026-07-19  M87  re-derive both density thresholds — M84's were wrong on BOTH files
2026-07-19  M92  lesson retirement — LESSONS.md gains an outflow
2026-07-19  M93  hygiene-line accretion — the stamp is replaced, not appended
2026-07-19  M94  this milestone
```

Nine milestones, five of them in two days, and M87 exists solely to fix
thresholds M84 shipped three days earlier. The maintainer's read is that the
strategy is generating follow-up work faster than it settles anything.

**The precedent that makes this urgent.** RB01/RR01 (2026-07-13, archived at
`cairn/reviews/archive/`) was a whole-architecture retrospective. Its §5
addressed rulebook size directly, at 545 lines. It **rejected** splitting the
rulebook into per-skill fragments (rec 15), prescribed **one** extraction —
the Validation doctrine to its own module (rec 9) — and adopted the norm "new
domain doctrine gets a module, not a rulebook section." M58 executed it; D-031
recorded it. Outcome:

```
2026-07-13   545 lines   the state that triggered RR01's concern
2026-07-16   532 lines   after M58 executed RR01 rec 9
2026-07-19   765 lines   today
```

The prescribed remedy netted 13 lines and was erased within three days. RR01
projected "~460 lines core + a 60-line conditional module"; the core is now
765 and the module 93. The extraction was a one-time cut with a norm attached
and no governing mechanism, and growth resumed immediately at roughly
+6.7 lines per milestone — every milestone has a legitimate reason to add a
rule, and nothing bounds the sum.

## Materials

Read these. Line references are current as of 2026-07-19.

1. `skills/shared/tracking-rules.md` — the rulebook itself (765 lines). Read
   whole; it is read whole by every skill at every phase, which is the cost
   under review. Note especially the "Weight caps" section (lines 81–160).
2. `cairn/reviews/archive/RR01-architecture-retrospective.md` — §5 "The
   rulebook's size and cohesion (GP1)" (lines 158–199), §7 on the principles
   (line 263 ff.), recommendation 9 and recommendation 15 (in the
   "Recommendations" section, line 448 ff.). This is the prior ruling; you
   are reviewing why it failed to hold, not re-deriving it from scratch.
3. `scripts/cairn_scripts.py` lines 40–110 — `LINE_CAPS`, `MILESTONE_CAP`,
   `ARCHIVE_CAP`, `CHAR_CAPS`, `NON_ITEM_LINE_CAP`, `CLAUDE_SECTION_CAP`, and
   the long derivation comments recording how each threshold was obtained.
   The comment at lines 48–82 is the current derivation doctrine.
4. `scripts/cairn_validate.py` lines 60–175 — `check_caps` and
   `check_record_density`, the hard-CHECK and advisory implementations.
5. `cairn/DECISIONS.md` — entries D-018, D-030, D-031, D-034, D-035, D-045,
   D-046, D-051, D-052. These record every prior weight decision and its
   rationale. The file is 95,976 characters; read these entries, not the whole
   file.
6. `cairn/DESIGN.md` lines 80–105 — the IP/GP principle block. GP1 ("Efficient
   — store decisions and outcomes, not minutiae; caps + archiving keep
   always-read files small") is the principle at stake; IP4 (history is never
   rewritten) is the binding constraint on `DECISIONS.md`.
7. `cairn/milestones/archive/M84-record-density-advisory.md` and
   `M87-density-threshold-recalibration.md` — the clearest instance of the
   pattern: a mechanism shipped, then re-derived three days later.
8. `cairn/milestones/M94-always-read-weight-signal.md` — the milestone this
   brief blocks, including its acceptance criteria and the held AC3
   amendment.

To reproduce the measurements: `wc -c` / `wc -l` on the files above;
`git show <rev>:<path> | wc -c` for historical points; `python3
scripts/cairn_validate.py` for current check/advisory state; `for s in skills
scripts hooks; do python3 -m unittest discover -s $s/tests; done` from the
repo root for the suites.

## Questions

1. **Why did RR01 rec 9 fail to hold?** The extraction was executed as
   prescribed and the file is now 44% larger than the state that prompted it.
   Is a one-time extraction plus a stated norm structurally incapable of
   governing an always-read file that every milestone has a reason to add to,
   or was the execution incomplete in a way that could be fixed by finishing
   it (RR01 also prescribed pruning restated detail — the default-branch
   recipe and the phase-header mapping — which was only partly done)?

2. **Is per-file, hand-derived thresholding the right mechanism class?**
   Nine milestones in eight days have added, exempted, re-derived, or patched
   caps, and M87 existed only to correct M84's numbers. Assess whether this
   is (a) normal convergence of a young mechanism, (b) a mechanism whose
   maintenance cost is inherent and acceptable, or (c) a sign the mechanism
   class is wrong. If (c), what replaces it? Consider explicitly: budget-based
   allocation across files rather than per-file caps; growth-rate/derivative
   signals rather than absolute levels; structural limits (a rule may only be
   added by replacing one); or no mechanism at all beyond periodic human
   review.

3. **How should a threshold be derived for a file with n=1 and no oracle?**
   cairn's derivation doctrine (M87, `cairn_scripts.py` 48–82) requires
   deriving from measurement and never from an assumed number, and derives
   character mass from an item cap. `tracking-rules.md` has no item structure,
   no line cap, and one instance. Either give a defensible derivation method,
   or state that "threshold" is the wrong instrument for this file and say
   what the right one is.

4. **What governs an always-read file that can never shrink?**
   `cairn/DECISIONS.md` doubled to 95,976 characters and is swept whole at
   every `/milestone-plan` collision check. IP4 forbids editing or deleting
   entries, so compression and eviction — the two remedies cairn's existing
   weight axes prescribe — are both illegal. Options seem to be: bound the
   *read* (a generated index, sectioning, or search-first retrieval instead of
   a whole-file sweep); archive superseded entries with pointers; or accept
   unbounded growth. Note the tension: the sweep exists to serve IP2 ("prior
   state is surfaced, never silently obeyed or silently overridden"), so a
   lossy index trades an IP2 guarantee for read cost. Which option, and what
   does it cost?

5. **Is the file size the problem, or the read pattern?** Every skill reads
   the rulebook whole, at every phase, by design — RR01 §5 defends this
   ("skills read it whole, so an extraction that skills must *remember* to
   read separately recreates the drift D-003 solved"). If the read pattern is
   the real cost driver, a conditional or sectioned read would beat any cap —
   but that is close to what rec 15 rejected. Does the whole-read guarantee
   still earn its cost at 765 lines, and if not, what preserves D-003's
   anti-drift property without it? If you disagree with rec 15, say so
   explicitly rather than working around it (see Constraints).

6. **Is character mass even the right proxy?** Every cairn weight mechanism
   measures characters or lines. The cost actually being paid is agent
   attention and latency over re-read context. Name any measurement cairn
   should be taking and is not — and say whether the observed slowdown is
   plausibly attributable to re-read volume at all, given that the evidence is
   correlational (two files grew; milestones got slower; no causal isolation
   was performed). A finding that the diagnosis is unsupported is a valid and
   useful answer.

## Constraints

Fixed unless you explicitly argue otherwise — flag disagreement with a
constraint openly rather than silently working around it.

- **RR01 rec 15** rejects splitting the rulebook into per-skill fragments, on
  the grounds that a single rules-home is what makes "nothing is said twice"
  and the whole-read guarantee work, and that fragmenting recreates the
  pre-D-003 drift the plugin exists to prevent. Standing rejection: to
  recommend against it, say so directly and give the superseding rationale.
- **D-031** fixes the extraction boundary: domain doctrine that is
  self-contained and conditionally relevant may become a module; the
  cross-skill contract (file map + ownership table, weight caps, universal
  tracking rules, status vocabulary, sizing tiers, git/approval model,
  question gates/chips, output discipline, model strategy, profiles
  mechanism) stays monolithic.
- **IP4** — history is never fabricated, rewritten, or renumbered.
  `DECISIONS.md`, work logs, `milestones/archive/`, and entombed `legacy/`
  files are append-only and are never edited. Any recommendation touching
  `DECISIONS.md` must respect this.
- **D-045/D-052** — the current-knowledge vs. history split: `LESSONS.md`,
  `references/` pages, `DESIGN.md`, `ROADMAP.md` are corrected in place;
  history is superseded, never edited.
- **The CHECK/advisory severity split** — structural facts are hard CHECKs
  that fail the gate; judgments about prose quality are advisories that only
  WARN. Argue for a reclassification if warranted, but do not ignore the
  distinction.
- Not under review: the milestone/status vocabulary, the git and approval
  model, the review fan-out, the skill surface. RR01 covered these; this
  brief is scoped to weight management.
- cairn assumes a single operator running these skills, on macOS with Claude
  Code. Do not recommend multi-operator machinery.

## Output format

In `RR02-weight-management-architecture.md`: answer each question by number
with your reasoning and evidence; cite file:line for every claim about the
implementation. List any additional findings separately under "Beyond the
brief"; end with concrete recommendations, each marked apply / consider /
reject-with-reason, and each naming which question it follows from.

Where a recommendation would supersede a standing D-entry or an RR01
recommendation, name the entry by ID and give the superseding rationale
explicitly.
