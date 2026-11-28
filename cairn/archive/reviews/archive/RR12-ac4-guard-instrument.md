# RR12: The AC4 guard instrument — diagnosis, in-principle limit, and the equality instrument (M139)

- **Date:** 2026-08-14
- **Brief:** `cairn/reviews/RB12-ac4-guard-instrument.md`
- **Evidence base:** read in full or at the brief's cited ranges:
  `cairn/milestones/M139-narrowing-at-the-return.md`,
  `skills/milestone-review/SKILL.md` step 5, `skills/milestone-implement/SKILL.md`
  step 6, `skills/tests/test_thrash_rule.py` (slice helpers and all of
  `TestWideningTest`), `skills/tests/test_mutation_harness.py` (the M139
  registry block), `skills/shared/guard-doctrine.md` whole,
  `skills/shared/tracking-rules.md` "What gets a test", the ROADMAP
  one-surface-pin row, and D-090, D-095, D-097, D-098, D-099 (in passing),
  D-101, D-102. Ran on the branch as checked out: full suite
  (`Ran 784 tests … OK`) and harness (`Ran 9 tests … OK`). **Independently
  re-reproduced R1**: inserted "counts as an ordinary defect return on the
  thrash count, and no part of it" between the pinned subject and pinned tail
  of the amendment-return sentence; the rule read as its own inversion, the
  full suite exited OK, the file was restored with `git checkout --` and
  `git diff` clean.

## 1. Diagnosis

**The failure set is not a finite collection of closable holes. The
anchor-based approach structurally under-determines the property, and the
three passes are the two halves of one invariant being violated
alternately.**

First, a precision the record supports but does not state: AC4's *literal*
matrix was satisfied at pass 3 — 30/30 probe runs red over the six added
sentences. What returned the milestone was the review's (correct) reading
that AC4's four forms name mutation *classes of the rule*, not edit
operations on the sentence's own bytes: R1 realizes the negation form by
insertion at a site between two pinned fragments, touching no pinned byte;
R3 realizes the relocation form by hoisting a block so that unpinned
sentences change which heading governs them. Under that reading — the only
reading under which AC4 is worth promising, since a rule inverted without
editing its pinned bytes is exactly as inverted — the property AC4 requires
of an instrument is:

> For each rule R this milestone adds or amends, let B(R) be the maximal
> contiguous span of the host file that R's meaning depends on — its label,
> subject, discriminator, force, and routing, in order. The instrument must
> red on **every file state in which B(R) does not read as R**: any token of
> B(R) relabeled or negated, any reordering of B(R), any text inserted
> *inside* B(R) that alters what it asserts, and B(R) or any sentence of it
> re-homed under a different rule's scope in the same file or the other
> file.

That is an invariant of the **block relative to its section**, and it
decomposes into exactly two conditions:

- **Totality.** The pinned extent equals the slice: no unpinned complement
  exists between the slice's boundaries. Any gap admits arbitrary text, and
  arbitrary text includes rule-inverting text.
- **Granularity.** The slice equals one rule: no second rule lives inside
  the boundaries, so there is no position within the slice a sentence can
  move to and thereby change which rule owns it.

The three passes are these two conditions failing in alternation, not three
independent holes: pass 1 violated totality (S2's subject and tail sat
outside the pinned clause); pass 2 violated granularity (one slice spanned
three rules, so intra-slice relocation crossed rule boundaries); pass 3
violated totality again, twice (an unpinned gap *between* two pinned
fragments — R1, which I reproduced; an unpinned slice tail — R3). Each
repair enlarged the pinned subset of the block; every proper subset leaves a
complement; the complement carried the next inversion. The sequence
converges only at the point where the pinned extent *is* the block — and
that point is no longer anchor-matching, it is whole-block comparison.

## 2. In-principle answer

**Yes, a substring/regex guard family over these files can deliver the
property — but only in the degenerate limit where the family collapses to
one whole-slice equality check per rule, at which point it has stopped being
an anchor family. Every anchor design short of that limit structurally
under-determines AC4, and each repair toward the limit multiplies the
enumeration burden guard-doctrine §3 warns about.**

The impossibility argument for proper-subset anchors, stated against the
probe forms: a set of independent substring/regex asserts accepts every file
state containing each asserted pattern within its slice. When the asserted
patterns cover a proper subset of the slice, the accepted set includes
states where the complement carries new text. The complement's text is
unconstrained, so it includes (i) a clause inverting the rule's force
inserted between two pinned fragments — the negation form, demonstrated at
R1 and re-reproduced for this report with the suite green at 784; (ii) a
re-homed block whose displaced neighbors change governing heading — the
relocation form, demonstrated at R3. No finite repair closes this while a
complement remains, because the mutation site quantifies over the
complement, not over the pinned set. Three narrowings measured this: each
closed the demonstrated instance and left the class.

The joint invariant a regex family *would* have to enforce is: per-rule
slices with unique boundary markers (granularity), **plus** the slice's
entire normalized content matching a single anchored pattern equivalent to
the rule's full text (totality) — i.e. `\A<entire rule>\Z` over the
normalized slice. Ordering constraints, pairwise adjacency asserts, and
no-insertion bounds between fragments are all strictly weaker restatements
of the same thing that re-introduce enumeration: N fragments need N−1
adjacency bounds, every legitimate edit re-derives them by hand, and a
missed bound is invisible until a review finds it — the M114/M117 shape, a
fourth time. `TestWideningTest`'s current slice design extends to the
equality limit with bounded effort (the slices and unique markers are
already built and fail safe — a missing marker collapses the slice to `""`,
which equality reds); it does not extend to it as an anchor family.

## 3. Instrument recommendation

**Recommended: (d), a variant of (b) — normalized whole-slice equality
against a verbatim in-test fixture. It is (b) with the hash left
uncompressed, which is precisely what fixes (b)'s worst failure mode.**

Evaluations:

- **(a) Markdown/AST structural parse — reject as machinery.** An AST gives
  rendering-independent *boundary extraction*, but the boundary problem is
  already solved here: the four slices are bounded by six markers asserted
  unique, and the markers are the rules' own bold labels — under the
  equality instrument they become pinned fixture content, not free anchors.
  The reference problem (what must the block say?) an AST does not touch.
  Python's stdlib has no markdown parser; `skills/tests` is stdlib-only, so
  (a) means a vendored parser or a hand-rolled block splitter — and a
  hand-rolled splitter is one more matcher over authored markdown with its
  own renderings to enumerate (§5).
- **(b) Content hash over normalized blocks — reject in favor of the
  plaintext form.** Coverage-identical to equality, but the discharge of a
  red hash is regenerating an opaque constant, and the one measured failure
  mode of this instrument class (M124's ledger, guard-doctrine §9) was "a
  ledger updated without its diff being read, which no guard can detect." A
  hash makes that failure mode *the default*: the update diff shows one
  constant replacing another. A verbatim fixture makes the update
  self-evidencing — the PR diff shows old and new rule text beside the skill
  file's own diff, and `assertEqual` prints the divergence on failure.
  A bare hash constant is also the more ledger-shaped artifact — opaque,
  answering only "changed?" — sitting closer to the class D-095 retired.
- **(c) Promote the probe matrix to the instrument — reject as the
  instrument; keep one thin slice of it as verification.** Three grounds.
  The negation form is semantic and cannot be mechanically generated —
  generating relabel/transpose/relocate but hand-writing negation reproduces
  the enumeration split that failed. Generated probes *test* a guard; they
  are not one — with today's anchors the generator would simply report the
  incompleteness at every gap, mechanically rediscovering R1 without
  supplying a passing design. And a standing probe-generation stage inside
  the harness is a new standing verification apparatus with certification
  flavor, the shape D-095 retired and D-090 doors. The thin slice worth
  keeping: a **one-time insertion-gap probe** at the child milestone's
  review — insert a fixed sentinel sentence at every inter-sentence gap
  inside each guarded slice, require red each time, record the outcome as a
  Review line, never ledgered. Under equality guards it reds by
  construction; running it once proves that, which is the falsifiability
  demonstration AC4 exists to demand.

**Implementation sketch against the actual files.** In
`test_thrash_rule.py`: add a `normalize()` helper (collapse `\s+` to single
spaces over the already-lowercased read). For each of the four slices —
`review_floor()`, `review_amendment()`, `review_widening()`, and the
implement-side M139 span — one method, one assertion:
`self.assertEqual(normalize(slice_fn()), FIXTURE)`, with `FIXTURE` a
module-level verbatim copy of the rule's full text. The 11 per-fragment
regexes of `TestWideningTest` are **replaced**, not accumulated beside (the
equality assert strictly subsumes each of them; keeping both doubles the
sync cost of every legitimate edit). The six marker-uniqueness asserts stay
(granularity + the decoy defense, M126). In `test_mutation_harness.py`: one
registration per slice, blanking any registered exemplar inside the slice
reds its equality method one-to-one, preserving the amended-AC5 shape.
Implement-side, R4 is closed by granularity, not by pinning the whole
Substantive bullet: the bullet holds six rules and freezing all of them
under an M139 fixture would make this guard own text other milestones edit.
Bound a sub-slice around the amendment-return-protocol region so the M139
sentences' slice contains no rule they could re-home under, with its
boundary markers asserted unique like the others.

**Expected cost.** One short task: on the order of four fixtures (~40 lines
of quoted doctrine), one helper, four methods replacing eleven, two new
implement-side markers, four registrations replacing eleven. Recurring cost,
stated rather than hidden: every legitimate edit to a guarded rule now reds
the suite and requires the fixture updated in the same commit — a
deliberate two-site act, which for return-classification doctrine (the text
the thrash counter itself reads) is the correct default; "the text owns the
guard" is preserved because the discharge is mechanical and the diff
readable.

**The instrument's own failure modes**, stated:

1. A fixture updated without its diff being read — the residual no guard
   can detect (M124's cost, carried honestly). Mitigation is structural:
   the update is a readable PR diff beside the rule's own diff, the
   cheapest possible review surface.
2. Normalization is a declared blind spot: mutations expressible purely in
   collapsed whitespace pass. In prose, benign; declare it.
3. Marker dependence remains, but fails safe: a lost or duplicated marker
   collapses the slice to `""` or binds a decoy, and equality reds either
   way — unlike an anchor family, where a truncated slice can keep every
   fragment matching (R3's geometry).
4. The fixture is a copy of doctrine inside a test. It is not a second
   *home* (no reader consults it for the rule; step-0 unviolated), and its
   staleness reds the suite — which is the stated↔enforced coupling §6
   demands rather than the silent fork it warns about. Flagged rather than
   worked around: if the maintainer reads D-095's retired class as covering
   an in-test verbatim fixture, the instrument fails at that door — but the
   repo's own harness already commits verbatim doctrine fragments as
   `Mutation(block=...)` entries, so the fixture introduces no new artifact
   class, only longer members of an existing one.

## 4. Disposition for M139

**Route (iii): split.** Ship the two doctrine rules and their current
guards now; re-cut the AC4-strength coverage promise as its own milestone
on the equality instrument, with this report's Binding criteria as its
acceptance floor.

- Against (i) re-plan whole: it holds doctrine already verified five ways
  (AC1–AC3, AC5, AC6) hostage to instrument work, forces fresh re-review of
  criteria that have passed three times unchanged, and keeps a three-return
  branch open longer. Nothing about the doctrine depends on the instrument.
- Against (ii) amend AC4 down: an amendment is admissible only as a
  narrowing, and narrowing AC4 to "what fragment anchors deliver" abandons
  coverage the record shows is real — the rule's full inversion ran green
  and was reproduced three times, once for this report. With a bounded-cost
  instrument identified that meets the promise as reviewers read it,
  lowering the promise is the one move the evidence argues against.
- For (iii): it is the thrash rule's own sanctioned remedy (re-plan or
  split via `/milestone-plan`); it delivers user-approved doctrine now; and
  it scopes the child tightly to one task on one surface. On D-090: the
  child is not a new apparatus program at the door — it is the completion
  of M139's own coverage promise on M139's own surface, hosted by the same
  surfacing whose trigger D-101 records as satisfied under D-098's host
  reading. The door stays closed to anything beyond that surface
  (question 5).

Two consequences the split must carry, so they are not lost at the plan
gate: **(1)** shipping now carries a recorded exposure — until the child
lands, an edit inserting between pinned fragments or stranding a slice tail
in the two shipped rules would run green; bounded because the doctrine text
is stable and user-approved and any such edit still faces PR review of the
skill diff, and precedented as an accepted, recorded exposure by D-095's
own §8-re-add clause. **(2)** the re-cut prunes AC4 from M139 and must
touch AC5's wording, whose "re-run against the AC4 mutation" clause
cross-references the pruned criterion (evidence already gathered at pass 3
stands; the wording routes through the gated amendment protocol like any
Substantive change). The re-cut can also repair R6/FE (Scope and AC1 still
say "two clauses" where three limbs ship) in the same gated pass.

## 5. Generalization

**Confine the remedy to M139's surface. D-090's trigger for corpus-wide
work is not satisfied, and that constraint is the blocker — flagged, not
worked around.**

The anchor-reach-vs-rule-extent shape is real corpus-wide: every
fragment-anchored guard has an unpinned complement, M131 and M123 predate
M139 on the same geometry, and nothing in this report's diagnosis is
specific to `TestWideningTest`. But every instance on record was produced
by a probe or a review lens — an instrument examining the apparatus's own
coverage. D-090 is explicit that a defect in the apparatus's own coverage
is fixed as ordinary work where it surfaces and never promoted into its own
apparatus milestone; the licensing trigger would be a **shipped-behavior
defect**: a guard-complement inversion in shipped doctrine that misrouted
what a skill actually did for a user (measured in a user repo, hosted under
D-098). No such defect is on record. So: the corpus fails forward case by
case, and each milestone that touches a guarded rule may bring its own
guards to the equality form as ordinary work within itself.

What *is* in-discipline now: the child milestone banks the transferable
lesson in `guard-doctrine.md` as ordinary work within itself — §2's
blind-spot list gains the insertion axis ("blanking is not swapping" is not
inserting either), and §1 or §9 gains the two-invariant statement
(totality: pinned extent = slice; granularity: slice = one rule; anchors
short of totality leave a free complement). That is a module edit inside a
triggered milestone, not a standing apparatus. If a shipped-behavior defect
of this class ever appears, D-090 names itself as the entry to supersede,
and this report's diagnosis is the evidence file for that day.

## Beyond the brief

- **B1.** The carried findings R2 (85) and R4 (80) are closed by
  construction under the recommended instrument: R2 because the widening
  rule's entire text, including the force of "only", is inside the
  equality fixture; R4 by the implement-side sub-slice (granularity),
  provided the child's probes exercise that file's relocation axis —
  BC4 requires it.
- **B2.** The ROADMAP one-surface-pin row: the equality instrument is
  in-home-file evidence that the row's named "content over normalized
  doctrine blocks" approach is workable, but it does not satisfy the row's
  promotion condition — the row's target is *fork detection across files*,
  a different application, and its promotion additionally sits behind
  D-090's trigger. Worth a dated note on the row; no promotion.
- **B3.** Guard-doctrine §2's list of what the harness cannot see is one
  axis short, as B1's geometry shows: blanking (covered), swapping
  (covered), *inserting* (uncovered — R1's class). Child-milestone edit,
  see question 5.
- **B4.** The M139 registry comment at
  `test_mutation_harness.py:3219-3222` ("The six slice markers…") sits
  above a block whose first entry is the routing-sentence pin, not a
  marker; cosmetic, worth fixing in passing when the registry block is
  rewritten for the equality registrations.
- **B5.** Work-log ordering in the milestone file is non-monotone at the
  tail (the 2026-08-14 escalation line sits above 2026-08-13 lines) —
  the FM/58 class already logged; noted only so the re-cut's hygiene pass
  sees it.

## Recommendations

1. **Apply** — route M139 as a split (question 4): prune AC4 via the gated
   re-cut, review and ship the doctrine on AC1–AC3/AC5/AC6, open a child
   milestone carrying the Binding criteria below verbatim.
2. **Apply** — implement the equality instrument (question 3): normalized
   whole-slice `assertEqual` against verbatim in-test fixtures for the four
   M139 rule slices, replacing the eleven fragment regexes, keeping the
   marker-uniqueness asserts, re-registering per slice in the harness.
3. **Apply** — implement-side sub-slice so granularity holds in
   `/milestone-implement` step 6 (closes R4's geometry rather than
   freezing six rules under one fixture).
4. **Apply** — one-time insertion-gap probe at the child's review, outcome
   recorded as Review lines, never ledgered (D-095-conformant).
5. **Consider** — bank the two-invariant statement and the insertion axis
   in `guard-doctrine.md` within the child milestone (question 5, B3).
6. **Consider** — dated note on the ROADMAP one-surface-pin row (B2), and
   the B4 comment fix in passing.
7. **Reject** — content hash as the committed form: coverage-identical to
   the verbatim fixture but opaque at discharge, defaulting into the one
   failure mode the M124 record proves (updated without its diff read).
8. **Reject** — markdown/AST parsing: solves the already-solved boundary
   half, not the reference half, at the cost of a non-stdlib dependency or
   a hand-rolled splitter that is itself a matcher with renderings to
   enumerate.
9. **Reject** — a standing mechanical probe generator as the instrument:
   negation is not mechanically generatable, generated probes test a guard
   rather than constitute one, and a standing generation stage is the
   certification shape D-095 retired at D-090's door.
10. **Reject** — corpus-wide remediation now: D-090's shipped-behavior
    trigger is unsatisfied; confined to M139's surface, failing forward
    elsewhere (question 5).

## Binding criteria

- BC1. Each of the four M139 rule slices (`review_floor`,
  `review_amendment`, `review_widening`, and the implement-side M139
  sub-slice) is guarded by exactly one test method holding exactly one
  assertion of the form `assertEqual(normalize(<slice>), <fixture>)`, where
  the fixture is a verbatim copy of the slice's entire rule text held in
  `skills/tests/`, and no per-fragment substring or regex assert remains as
  any of those slices' pin — checked by AST walk over `TestWideningTest`'s
  successor at the review commit.
- BC2. AC4's original probe matrix, re-run at the review commit over the
  domain enumerated by `git diff -w main...HEAD -- skills/milestone-review/SKILL.md
  skills/milestone-implement/SKILL.md` split at sentence boundaries, reds on
  every probe run with zero green (tolerance: zero), each run restored with
  `git diff` shown clean.
- BC3. An insertion probe placing one fixed sentinel sentence at every
  inter-sentence gap inside each guarded slice reds the suite at every gap,
  zero green (tolerance: zero); the gap count is derived at the review
  commit from the slice text by a stated procedure, not free-standing; each
  run restored with `git diff` shown clean.
- BC4. A relocation probe moving each M139-added sentence (a) into each
  other rule block of `/milestone-review` step 5, (b) into the other skill
  file, and (c) for the implement-side sentences, to at least two other
  positions inside the Substantive bullet but outside their sub-slice, reds
  on every move, zero green (tolerance: zero), the move counts derived at
  the review commit by a stated procedure; each run restored clean.
- BC5. Every slice fixture has a mutation-harness registration whose
  blanked block reds that slice's own equality method one-to-one, and
  `python3 -m unittest discover -s skills/tests -k mutation_harness`
  reports `OK` at the review commit.
- BC6. The child branch's `git diff main...HEAD` adds no committed
  artifact outside `skills/tests/` and the tracking files: no ledger file,
  no hash constant, no per-probe record; probe outcomes appear only as
  Review-section evidence lines (D-095).
- BC7. All six existing boundary markers, plus any new implement-side
  sub-slice markers, are each asserted unique in their host file, and a
  slice helper returning `""` on a missing marker fails the equality assert
  rather than passing vacuously — demonstrated once at the review commit by
  the marker-blanking entries of BC5's harness run.
