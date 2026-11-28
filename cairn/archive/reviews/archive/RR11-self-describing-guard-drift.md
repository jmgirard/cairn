# RR11: A guard's description of itself keeps drifting from what it checks (M126)

- **Date:** 2026-07-31
- **Brief:** `cairn/reviews/RB11-self-describing-guard-drift.md`
- **Reviewed at:** `HEAD` of `m126-claude-md-always-read-row` (987f49b), all four
  verify commands green before probing; every probe below run on a
  `git archive` copy and confirmed by command, never by reading alone.

## 1. Is a self-describing guard the right instrument at all?

**No.** It relocates the author-enumeration problem twice over, and its second
half is not mechanically checkable at all. Answering question 3.

**The derivation is the enumeration.** `whole_object_pins` does not observe
"the anchors"; it observes the author's *definition* of an anchor — module-level
`ast.Assign`, `literal_eval`-able, `len > 25`, resolved against a hard-coded
target list. Every hole found is a hole in that authored definition, and I
found three beyond the brief's two, each reproduced GREEN on a copy where the
class docstring says RED:

- **Substring pin-name (new).** Add a second whole-object pin named `BOUNDARY`
  (a two-line-spanning copy of real target text), with no docstring mention.
  The derivation *does* find it (`derived pins: ['BOUNDARY_STATEMENT',
  'BOUNDARY']`) and the check still passes, because
  `assertIn("BOUNDARY", doc)` is satisfied by the substring inside
  `BOUNDARY_STATEMENT`. This is guard-doctrine §1's opening defect
  (`merge_guard` → `merge_guard_post`) reproduced *inside the remedy that was
  supposed to close a doctrine-violation class*.
- **Length threshold (new).** A 24-character constant spanning the wrap at
  `tracking-rules.md:196-197` (`"Its three cells describe"`) is a whole-object
  pin invisible to the `len(text) > 25` filter. Suite green, no docstring
  mention.
- **Expression-built constant (new).** A pin assembled as
  `" ".join([...])` makes `ast.literal_eval` raise `ValueError`, which the
  `except ValueError: continue` swallows silently. Derived set unchanged,
  suite green.

Plus the brief's two, both re-confirmed: inline `assertIn` literals are
invisible (the derivation walks only `ast.Assign`), and the docstring check
pins a token, not agreement (the exception clause replaced by its exact
opposite — "`BOUNDARY_STATEMENT` is no exception: it too sits on one physical
line, pinned byte-for-byte" — passes green). Five defeats of one small
function. Extending the definition to close each is the enumeration treadmill
§9 records losing four consecutive times against the rename class.

**The agreement half is judgment, not a check.** "Reds when this paragraph and
the file disagree" asks a test to adjudicate whether English prose agrees with
an artifact. §9 is explicit that a mechanical instrument "detects a change and
never judges it," and that building it to judge "would rebuild the judgment
D-059 retired." The strongest thing an `assertIn` can do against a docstring is
token presence; anything stronger is a prose-guard over the guard's own
docstring, which regresses — who describes *that* guard's coverage, and who
checks the description?

**The deepest problem:** a docstring universal about what this file's anchors
satisfy is a *coverage certification*, and §8's first sentence is that the
author never certifies its own guard's coverage. Instance 3 was the author
building a machine to perform its own certification. The machine inherits the
author's blind spot because the author wrote both the claim and the checker of
the claim; the gap between them is exactly the gap the author cannot see
(D-067). No derivation choice fixes that — hence question 3.

## 2. If sound, the correct derivation

Answered for completeness since the brief asks for the failure modes of each
option even under a "not sound" verdict:

- **Guard source AST (as attempted):** the five defeats above; and the
  definition-is-enumeration point — the derivation can only ever be as complete
  as the author's model of "pin," which is the model that failed three times.
- **Mutation registry:** under-enumerates *by design* — registration is
  per-file exemplar, never per assertion (§2), so absence from the registry
  proves nothing; and the registry represents the whole-statement pin by a
  single interior line (`test_mutation_harness.py:2210-2215`, block `"so the
  two differ in whether..."`), so pin *shape* is unrecoverable from it. It is
  also author-maintained, so the same hand writes claim and checker.
- **Target documents:** the target has no knowledge of which guard pins it or
  how. Deriving "what is pinned" from the target yields what *should* be
  pinned — the criterion — not the fact about the guard; the comparison is then
  criterion-vs-criterion, vacuously green.
- **Runtime introspection** (trace which asserts read which bytes): new
  apparatus that D-090 would need to admit on its own trigger, and it still
  cannot check the prose-agreement half, which is where instance 3 actually
  died.

None of the four reaches the token-vs-agreement defect, because that is not a
derivation problem.

## 3. The alternative

**(a), by deletion — plus the checking machinery the repo already has.**

The repo's own precedent is exact: LESSONS 2026-07-20 (M99), "a figure stated
INSIDE the artifact it measures is a fixed point — writing it changes it...
the fix was not a better guard but DELETING the figure." A docstring universal
quantified over the file's own anchors is the same fixed point: every anchor
added or reshaped re-stales it, which is why fixing each instance in place
bought the next. A claim that exists nowhere cannot drift; a claim nothing
checks is worse than no claim. So:

- Delete `TestAnchorDescriptionMatchesTheAnchors` whole (both tests, the
  helper, its REGISTRY entry at `test_mutation_harness.py:2228-2233` and the
  comment block above it).
- Delete the docstring's quantified inventory claims — "Each sits on a single
  physical line... with one exception...", "That exception set is not prose to
  be trusted: ... reds when this paragraph and the file disagree." Replace with
  non-quantified pointer prose: where the anchors come from (shipped bytes,
  M95/M100) and that `BOUNDARY_STATEMENT` is pinned whole under normalization
  — *see its test's comment* — without any "each/every/only" over the set.

**Where the inventory claim lives instead: (b), narrowly.** AC4 keeps the
claim, stated with its enumeration procedure at D-091 part-3 grade (the work
log's 2026-07-31 numeric-settling line already has the right shape), and the
§8 fresh-context reader plus the review gate check it — the instruments that
in fact caught all three instances. This adds nothing: §8 check 2 already
assigns claim-vs-file accuracy to a fresh reader. Under D-067 this is not
"author checks harder": the author's obligation is only to *run* the stated
procedure and paste output (operation), and the checking sits with readers who
authored nothing.

**(c) rejected:** the class does not need to stay open. Its members are
universal claims sitting on unchecked surface; subtraction removes the
surface, and the doctrine rule in §5 below governs writing new ones.

## 4. Is the underlying anchor design the problem?

**Yes — the double-pinning is what made the description unstatable, and
collapsing it dissolves most of the problem.** The boundary paragraph is
currently pinned under two comparison rules at once: four per-line anchors
(`test_names_the_section_scoped_surface`,
`test_names_the_ungoverned_remainder_of_the_file`,
`test_contrasts_the_milestone_file_whose_exempt_sections_stay_governed`,
`test_claims_no_uniqueness_for_the_split_unit`) *and* the whole-object
normalized pin over the same bytes. Any truthful sentence about "what the
anchors satisfy" must quantify across both rules — which is the sentence that
kept coming out false.

Probed on a copy: with all four per-line tests deleted and the round-1 green
probe applied to the target ("governed by cairn too, and every cell in that
row reaches it"), the file reds — `FAILED (failures=2, errors=1)` — on the
whole pin, its normalization sibling, and the position test. The whole-object
pin strictly dominates the per-line anchors for *detection* within the
paragraph: any byte-level negation, transposition, or deletion reds it, and
the twelve-mutation work-log run already showed this. §1 itself licenses the
normalized form here: "a plain presence check over prose that legitimately
re-wraps may normalize whitespace instead."

**What is lost, honestly:**

- *Failure localization.* A reword reds one whole-pin assert with a large
  normalized-string diff instead of a named per-clause test. Real but cheap:
  AC5's inversions and the position test still name what moved, and the four
  clause names can survive as prose in the whole pin's comment.
- *Per-clause AC3→assert legibility.* All four AC3 clauses map to one assert.
  Legal under §8 check 1 — the assert genuinely pins each clause (negating any
  one reds) — but the Coverage mapping should say so explicitly.
- *Nothing else.* Reflow-sensitivity is a cost here, not a benefit; it is the
  precise mechanism of §8 rounds 1 and 2's findings.

Mechanics: the four REGISTRY entries for the deleted tests re-point to
`test_pins_the_whole_boundary_statement` with blocks unchanged (blanking any
line of the paragraph reds the whole pin), preserving per-block harness
coverage. After the collapse the file has one comparison rule per region —
table: structural whole-table check; boundary paragraph: whole-normalized pin
plus position; everything else: per-line anchors — and with §3's deletion
there is no universal left to state about it anyway.

## 5. A general rule for guard-doctrine.md

**Yes, one rule covers all three, in §6.** All three instances are §6's
restatement defect ("a rule inherited from a prior finding is unverified until
read out of the implementation") specialized to *quantified* claims, and a
universal is a count in disguise — "every anchor sits on one line" is "the
count of exceptions is zero." D-091 part 3 already obliges counts to carry a
verbatim-reproducible procedure; it just does not reach quantifiers. The rule:

> **A universal quantified over the milestone's own artifacts ("every anchor",
> "the suite", "all N", "reds whenever") is a count claiming zero exceptions,
> and carries the same obligation as any recorded count: state the procedure
> that enumerates its domain, run it against the artifact after the artifact's
> last edit, and write the claim from the output. Where no stated procedure
> can enumerate the domain — a guard's own coverage, "reds when X disagrees" —
> the universal is not written; point at the test instead.**

Checked against the three instances: (1) "every anchor ... one physical line"
— the AST enumeration, run, outputs `BOUNDARY_STATEMENT`; the claim as written
could not have survived its own procedure. (2) "the suite green against a
reflowed target" — the domain is the named suite command; running the claim at
its own stated scope reds four per-line anchors. (3) the docstring's "each ...
single physical line" falls to the first arm, and "reds when this paragraph
and the file disagree" has no enumerable domain (the space of disagreements),
so the second arm forbids writing it — the deletion §3 recommends is what the
rule mandates.

Placement: §6, beside D-091's recorded-counts rule, whose obligation it
extends — not §1 (about asserts, not records), not §8 (this binds all records,
not certification only), not a new section (two sentences do it, and
prose-only is preferred). Guard: the standard pair — a prose-guard assert on
the rule's load-bearing line plus one REGISTRY entry.

Stated limit, per the brief's honesty bar: the rule governs *writing*
universals; it does not make an author able to see coverage gaps. The seeing
stays with §8's fresh readers. It would have caught all three instances
because all three would have had to run their own enumeration before shipping,
and two red immediately while the third becomes unwritable.

## 6. Does the §8 stop rule need changing?

**Both of the brief's readings are partly true; the remedy clause needs
amending, the stop and the falsifier do not.**

What worked as designed: the rounds ended by rule, the stop was disclosed, and
the falsifier fired exactly per its text when review found the remedy short —
the outer loop caught in one review what a fourth round might not have. That
is the falsifier doing its job, not the rule failing silently.

What the rule caused: it *obliges* the same author who has just demonstrated,
twice consecutively, that it cannot see its own guards' coverage gaps to
author — immediately, in-branch — a remedy carrying the strongest possible
coverage claim there is ("closes the class"), confirmed by *operation alone*.
But §3 of the same doctrine already says operation-style mutation confirmation
"proves only that the guard catches the mutation its author thought of — and
the author of a detector is exactly who cannot enumerate the renderings it
misses." The stop rule's confirmation channel is the channel the doctrine
elsewhere distrusts, applied at the moment of maximum distrust. It mandated an
author-certified universal — in tension with §8's own first sentence.

**Amendment (two clauses, prose-only, narrowly superseding D-091 part 1 via a
new D-entry per IP4):**

1. **Prefer subtraction.** A structural remedy should first try to *remove the
   surface the shape occurs on* — delete the drifting description, collapse
   the redundant pin — rather than add checking machinery. A subtractive
   remedy is confirmable by absence; an additive checker is new author-written
   surface of exactly the kind the author is currently failing at. (M126's
   correct remedy under this clause was §§3–4 of this report: delete the
   docstring universal, collapse the double pin — no
   `TestAnchorDescriptionMatchesTheAnchors` would have existed.)
2. **An additive remedy's class-closure claim is confirmed by a fresh-context
   reader or the three-lens review, never by operation alone.** Operation
   confirms the remedy *runs red on the author's probes*; it cannot confirm
   the universal "the class is closed." Until that confirmation, the
   disclosure records the claim as pending. This routes confirmation to
   instruments that already exist (D-090-clean), keeps the author out of
   self-certification (D-067-clean), and costs at most one reader pass.

On the fired falsifier: per its own text the universal-claim shape has
returned to round-opening with the tolerance spent. This RB/RR is an
independent fresh-context reading of exactly that shape — stronger than a
certification round — and the milestone should record it as discharging the
reopened round rather than convening another author-checked one.

## Beyond the brief

- **Three new defeats of the shipped remedy** (Q1): substring pin-name,
  25-char threshold, expression-built constant — all reproduced GREEN. The
  substring one deserves note in the record: the remedy for a
  guard-doctrine-violation class itself violates §1's opening rule.
- **Misdirected second arm.** `whole_object_pins` lists
  `skills/milestone/SKILL.md` as a target, but
  `test_each_whole_object_pin_still_matches_under_its_normalization` checks
  every derived pin against `tracking-rules.md` only — a whole-object pin over
  SKILL.md would red spuriously. Moot once the class is deleted.
- **Review round 2's other actioned findings remain owed** independent of this
  RR: A5 (three relocations pass the position guard), A8 (asymmetric
  normalization across `BOUNDARY_STATEMENT`'s two users — BC3 below folds this
  in because the Q4 collapse touches the same code), A3 (the evidence line
  misattributing the 24/23 figure to the guard — a record; supersede, don't
  edit, per IP4 where it is work-log surface), A16 (the ROADMAP candidate row
  shipped truncated mid-sentence — broken live tracking state; fix the row).
- **Constraint compliance:** nothing here touches the governance content
  (D-094), D-018/D-009, or reintroduces size governance (D-057/D-060). The §6
  and §8 additions are prose plus standard guard registration — admissible
  under D-090's trigger, and no recommendation opens apparatus beyond it. No
  recommendation instructs the author to re-check its own work (D-067): every
  checking obligation lands on stated-procedure operation or on fresh readers.

## Recommendations

1. **Apply** — delete `TestAnchorDescriptionMatchesTheAnchors` (tests, helper,
   REGISTRY entry at `test_mutation_harness.py:2228-2233`) and the module
   docstring's quantified anchor-inventory claims; replace with non-quantified
   pointer prose. (Q1/Q3; LESSONS M99 precedent.)
2. **Apply** — collapse the boundary paragraph to one comparison rule: delete
   the four per-line tests over it, re-point their REGISTRY entries to
   `test_pins_the_whole_boundary_statement`, note the four-clauses-to-one-assert
   mapping in Coverage. (Q4; probe recorded above.)
3. **Apply** — symmetrize `BOUNDARY_STATEMENT`'s normalization across both its
   consumers while in that code (review A8).
4. **Apply** — AC4 keeps the inventory claim only with its enumeration
   procedure stated verbatim and its output recorded post-last-edit; no clause
   quantified over an unenumerable domain. (Q3b/Q5.)
5. **Apply** — add the quantified-claim rule to guard-doctrine §6, guarded and
   registered the standard way. (Q5.)
6. **Apply** — amend §8's shape-repeat remedy clause: prefer subtractive
   remedies; additive remedies' class-closure claims confirmed by fresh reader
   or review, pending until then; new D-entry narrowly superseding D-091
   part 1. (Q6.)
7. **Consider** — record in the M126 work log that the falsifier-reopened
   round is discharged by this RB/RR as the independent fresh-context reading.
8. **Consider** — fix review A5's three relocations with a section-bounded
   ordering check rather than more index comparisons; and fix A16's truncated
   ROADMAP row. Owed to review round 2 regardless of this RR.
9. **Reject** — any re-derivation of the pin set (from source, registry, or
   targets): each option's failure mode is named under Q2, and none reaches
   the token-vs-agreement defect.
10. **Reject** — a fourth author-written self-description checker, for the
    reason the brief itself states: the gap between intended and actual
    coverage is invisible to the author, and a checker the author writes sits
    inside that gap.

## Binding criteria

- BC1: `skills/tests/test_always_read_frame.py` contains no
  `TestAnchorDescriptionMatchesTheAnchors` class, no test deriving an anchor
  or pin set from the guard's own source, and a module docstring with no
  universally quantified claim over the file's anchors and no claim that any
  test reds on docstring–file disagreement. `test_mutation_harness.py`
  contains no REGISTRY entry naming the deleted class. All suites green.
- BC2: The boundary paragraph (`tracking-rules.md`, "The sixth surface differs
  again…") is pinned by exactly two tests: the whole-object normalized pin and
  the position test. The four per-line tests named in RR11 §4 are deleted;
  their four REGISTRY blocks remain registered, re-pointed to
  `test_pins_the_whole_boundary_statement`; harness green, and one recorded
  probe shows the D-018 remainder clause negated in the target reds the suite.
- BC3: Both consumers of `BOUNDARY_STATEMENT` apply the same
  normalize-both-sides comparison: one recorded probe re-wraps the constant in
  the guard source and the full skills suite stays green; one recorded probe
  rewords the target statement under a reflow and the suite reds.
- BC4: AC4 as shipped contains no universal whose domain lacks a stated
  enumeration procedure; its anchor-inventory clause names the procedure
  verbatim and the count recorded is the procedure's output measured after the
  guard file's final edit (tolerance: exact).
- BC5: `guard-doctrine.md` §6 contains the quantified-claim rule (universal =
  zero-exception count carrying the procedure obligation; unenumerable domain
  → universal not written), pinned by one new assert and one REGISTRY entry,
  mutation-red when blanked.
- BC6: `guard-doctrine.md` §8's shape-repeat remedy clause states subtraction
  preference and fresh-reader/review confirmation for additive remedies'
  class-closure claims, with a `DECISIONS.md` entry narrowly superseding
  D-091 part 1; `dangling id tokens` clean.
