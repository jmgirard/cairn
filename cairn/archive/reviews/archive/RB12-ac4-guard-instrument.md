# RB12: Can a prose guard deliver AC4's probe coverage, or is a different instrument needed (M139)

- **Date:** 2026-08-14
- **Output required:** write findings to `cairn/reviews/RR12-ac4-guard-instrument.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

This repo is **cairn**, a Claude Code plugin: a set of skills (markdown
instruction files under `skills/`), hooks, and scripts that implement a
project-tracking discipline. Its doctrine — the rules the skills state — is
prose, and the repo locks that prose with **prose guards**: Python `unittest`
asserts (substring and regex matches over the markdown files) in
`skills/tests/`. A **mutation harness**
(`skills/tests/test_mutation_harness.py`) verifies each guard is falsifiable
by blanking a registered exemplar block and requiring the guard to fail.

Milestone **M139** (branch `m139-narrowing-at-the-return`, PR #139) ships two
doctrine rules: a *widening test* in `/milestone-review` step 5 (a review
return whose only available repair widens an author-recalled enumeration is
classified as an amendment return, not a defect return) and a matching repair
direction in `/milestone-implement` step 6. Those rules are written and
verified (acceptance criteria AC1–AC3, AC5, AC6 all met at review pass 3).

The blocked question is **AC4**, which promises that *every sentence the
milestone adds to the two skill files reds the `skills/tests` suite under a
probe matrix*: relabel, negation, subject transposition, and relocation (run
twice — once into a different section of the host file, once into the other
file), with the file restored and `git diff` clean after each run.

AC4 has now failed **three review passes**, each time by a new mechanism of
one shape — *a guard's anchor reach differs from the extent of the rule it
claims to pin*:

- **Pass 1:** the guards pinned only the clause M139 added to an amended
  sentence; the sentence's *subject* and *tail* were pinned by nothing, so
  negation and subject transposition of the whole sentence ran green
  (the pre-existing "M131 class": predicate-without-subject,
  prefix-without-tail).
- **Pass 2:** the repair added per-sentence pins, but the marker-bounded
  *slice* the guards read spanned all three rules of the step — so any
  pinned sentence could be *relocated into a different rule's paragraph
  inside the slice* with the whole suite green, leaving the section
  self-contradicting (finding FA, scored 95, independently reproduced).
- **Pass 3:** the repair narrowed to four per-rule slices with unique
  boundary markers, but (R1, 96) two separately-pinned fragments of one rule
  had *nothing binding them to each other*, so text inserted **between**
  them fully inverted the rule with all 784 tests green; and (R3, 93) one
  slice's tail was still unbound, so hoisting a block mid-paragraph stranded
  two sentences under another rule's heading, again green. Both reproduced
  by two agents independently.

The third defect return fired the repo's thrash rule: no further repair
attempt is permitted under the current plan. The review's closing analysis
(end of the milestone file) reads: *"What the evidence indicts is the
instrument: a prose guard pins a phrase, and a phrase can be relocated,
detached from what binds it, or negated by insertion between two pinned
fragments. Three narrowings each closed a demonstrated hole and opened an
adjacent one."* The maintainer parked the milestone `blocked` on exactly
this question and approved this escalation.

Prior art inside the repo, recorded before M139:

- A standing ROADMAP candidate row ("One-surface pin for a doctrine rule")
  records that phrase-search requires its author to enumerate every
  rendering a phrase can take, that a similar detector burned three review
  returns at M114 on exactly that enumeration, and that its promotion
  condition is "a rendering-independent approach — a markdown/AST parse, or
  a content hash over normalized doctrine blocks — never after N further
  attempts at a wider matcher."
- `skills/shared/guard-doctrine.md` is the repo's craft module on making
  guards falsifiable (anchors, the harness's blind spots, absence asserts,
  fixtures, matchers over authored markdown).
- The repo has a history of guard-instrument over-reach: a certification
  instrument adopted on thin evidence consumed ~10 decision entries and was
  retired whole at user mandate (D-095); a program-closure decision (D-090)
  now requires a shipped-behavior defect as the trigger for any new
  verification apparatus.

## Materials

All paths relative to the repo root. The working tree is checked out on
branch `m139-narrowing-at-the-return`; read files from the working tree, and
use only ref-based git (`git diff`/`show`/`log` against `main...HEAD`) —
never `checkout`, `switch`, `reset`, or `worktree` commands.

- `cairn/milestones/M139-narrowing-at-the-return.md` — the whole file:
  Goal/Scope/AC (AC4 especially), the work log, and the `## Review` section
  recording all three passes, the probe matrices, and the findings quoted
  above (F1, FA, FD, R1–R4).
- `skills/milestone-review/SKILL.md` lines ~210–260 — the three rules of
  step 5 the guards protect: return floor, amendment return, widening test.
- `skills/milestone-implement/SKILL.md` step 6 — the Substantive-amendment
  bullet carrying the repair-direction sentence.
- `skills/tests/test_thrash_rule.py` lines 1–120 (the slice helpers:
  marker-bounded extraction) and lines 488–648 (`TestWideningTest`, the
  M139 guards — read every method and its comment; the comments record
  which review finding each guard answers).
- `skills/tests/test_mutation_harness.py` lines ~3148–3260 — the M139
  registrations, including the six slice markers.
- `skills/shared/guard-doctrine.md` — whole file, especially §1 (inversion
  protocol, anchor choice), §3 (enumeration by the detector's author), §4
  (fixture design).
- `skills/shared/tracking-rules.md` — the "What gets a test" section: the
  guard-must-fail rule, the mutation-harness paragraph, and the
  "guard-reddening is a deletion screen" paragraph.
- `cairn/ROADMAP.md` — the candidate row beginning "One-surface pin for a
  doctrine rule" (its two negative evaluations and its promotion condition).
- `cairn/DECISIONS.md` — read these entries by heading: D-090, D-095, D-097,
  D-098, D-101, D-102. The file is large; scan `### D-` headings and read
  only those entries whole.
- To run the suites: `python3 -m unittest discover -s skills/tests` (full),
  `python3 -m unittest discover -s skills/tests -k mutation_harness`
  (harness only). Both must pass on the branch as checked out; you may
  reproduce any probe by editing a skill file, running the suite, and
  restoring with `git checkout -- <file>` (file-scoped restore is fine; it
  moves no branch).

## Questions

1. **Diagnosis.** Across the three passes, is the failure set a finite
   collection of closable holes (subject/tail, slice width, inter-fragment
   binding, slice tail), or does the anchor-based approach structurally
   under-determine the property AC4 asserts? State the property AC4 actually
   requires of an instrument, precisely — what must be invariant about a
   rule-sentence relative to its section for relabel, negation,
   transposition, and both relocation forms all to red.

2. **In-principle answer.** Can a substring/regex guard family over these
   markdown files deliver that property at all? If yes, state the joint
   invariant the guards must enforce (for example: per-rule slices with
   unique boundary markers, plus total ordering and adjacency of every
   pinned fragment within its slice, plus a no-insertion bound between
   fragments) and whether `TestWideningTest`'s current slice design extends
   to it with bounded effort — or whether each new guard multiplies the
   enumeration burden guard-doctrine §3 warns about. If no, state the
   impossibility argument concretely against the four probe forms.

3. **Instrument recommendation.** If a different mechanism is warranted,
   evaluate at least: (a) a markdown/AST structural parse asserting rule
   blocks as semantic units (the ROADMAP row's rendering-independent
   approach); (b) a content hash over normalized doctrine blocks; (c)
   promoting the probe matrix itself to the instrument — extending the
   existing mutation harness to *generate* the relocation/negation/
   transposition probes mechanically, so coverage is by construction rather
   than by hand-enumerated anchors; (d) any better alternative. For the
   recommended one: implementation sketch against this repo's actual files,
   expected cost, and its own failure modes.

4. **Disposition for M139.** Given your answers, which route should the
   milestone take, and why: (i) keep AC4 as written and re-plan with the
   recommended instrument; (ii) amend AC4 (through the gated amendment
   protocol) to the coverage prose guards demonstrably deliver, shipping the
   already-verified doctrine now; (iii) split — ship the two doctrine rules
   and their current guards now, re-cutting the AC4-strength coverage
   promise as its own milestone on the recommended instrument? Note the
   thrash rule forbids a fourth in-place repair under the current plan, so
   (i)–(iii) are the admissible shapes.

5. **Generalization.** The anchor-reach-vs-rule-extent shape predates M139
   (M131's subject/tail class; M123's whole-file-anchor relocation class)
   and presumably holds latently across the existing guard corpus. Does the
   evidence warrant a corpus-wide remedy now, or does D-090's
   trigger discipline confine any remedy to the surface M139 touched, with
   the corpus left to fail forward case by case? If you recommend
   corpus-wide work, state what shipped-behavior defect (D-090's required
   trigger) licenses it, or flag the constraint as the blocker.

## Constraints

Fixed; flag disagreement explicitly rather than silently working around it.

- **D-090:** the verification-apparatus program is closed at the door — a
  new apparatus milestone needs a shipped-behavior defect as its trigger.
  D-101 records M139's own trigger as satisfied (under D-098's cross-repo
  host reading), so an instrument *for M139's surface* is in-scope; a
  standing corpus-wide instrument is a separate door (question 5).
- **D-095:** the certification-step instrument class is retired at user
  mandate — no per-sentence/per-probe committed ledgers, no certification
  rounds, no replacement standing step. M139's plan gate reaffirmed this:
  probes are run and their outcome recorded, never ledgered.
- **D-097 / D-101 / D-102:** the counting tracks (defect returns vs
  amendment returns, the second-occurrence stop) and the widening test's
  classification are decided; not relitigated here. AC4's instrument is the
  open question, not the doctrine the guards protect.
- **IP4** (`cairn/DESIGN.md`): history records — `DECISIONS.md`, work logs,
  the milestone `## Decisions` section — are never edited, only superseded.
  D-102 exists because this was violated once on this branch; do not
  recommend edits to history records.
- **Thrash rule:** no fourth repair attempt under the current plan; every
  recommendation must route through re-plan/split (`/milestone-plan`) or a
  gated criterion amendment.

## Output format

In `cairn/reviews/RR12-ac4-guard-instrument.md`: answer each question by
number with your reasoning and evidence; list any additional findings
separately under "Beyond the brief"; end with concrete recommendations, each
marked apply / consider / reject-with-reason. Where findings bind
implementation, also emit a `## Binding criteria` section: numbered `BC1…`,
each a measurable assertion checkable against evidence, with any numeric
projection stating its tolerance. These are ingested VERBATIM into the
constrained milestone's acceptance criteria and mechanically diffed against
this file; departures are legal only through that milestone's shown
"Deviations from RR12" table.
