# RR07: Jointly unsatisfiable binding criteria and defects outside a frozen scope (M114)

- **Date:** 2026-07-26
- **Brief:** `cairn/reviews/RB07-unsatisfiable-criteria-and-frozen-scope.md`
- **Reviewer baseline:** branch `m114-review-loop-escape-hatches` at `d8049c4`;
  all three suites green in a `git archive HEAD` scratch export with exit codes
  checked separately (skills 627 / scripts 280 / hooks 91, exit 0 each). No
  tracked file was modified during this review; ref-based git only; all
  mutation probes ran in the scratch export, whose baseline was verified
  `exit=0, Ran 627` before probing and whose target file was verified
  byte-identical to its original after each restore.
- **Findings independently reproduced this review:**
  - **F1** — deleting `guard-doctrine.md` §7's operative remedy sentence
    ("Assert per cell that it checked a positive number of things, and assert
    across the sweep that the positive case fired somewhere, so universal
    silence cannot satisfy it.") left the skills suite green at 627, exit 0.
    Restore green, byte-identical.
  - **F2** — gutting §3's remedy continuation while keeping the asserted
    lead-in "Carry the renderings INTO the test as positive" intact left the
    suite green at 627, exit 0. Restore green, byte-identical.
  - **F3** — `grep -rn "zero coverage\|two such"` over the archived RB06 and
    RR06 returns 0 hits; RR06's actual falsifier at its lines 173–176 is
    post-adoption and opposite in polarity, exactly as pass 6 recorded.
  - **AC6/AC8 joint unsatisfiability** — `git diff --numstat 295f7d3..HEAD --
    cairn/ROADMAP.md` is 4 insertions / 1 deletion: one status-cell mirror
    (1 del + 1 ins) plus the three candidate rows BC8 mandates. There is no
    delta that satisfies both criteria as written; BC8's alternative route
    (a `/milestone-plan`-cut milestone) also writes a ROADMAP row, so the
    conflict is not route-escapable.

## Answers

### 1. BC6 yields to BC8; the fault is BC6's characterization, and the fix is a one-clause amendment plus a rule about how such clauses are authored

**Which yields.** BC6's tracking-side sentence yields. BC8 is a substantive
obligation — the banked recommendations are review findings, and IP3 makes
their disposition non-optional — while BC6's tracking-side sentence is scope
hygiene: an enumeration whose purpose is to prevent delta wander, not to
declare any particular write illegitimate. When a hygiene enumeration and a
substantive mandate collide, the enumeration is corrected to admit the
mandate; the reverse (softening BC8 so the rows land somewhere ROADMAP-free)
has no landing zone at all, since BC8's own alternative route also writes a
ROADMAP row.

**The amended criterion, verbatim, for the gated-amendment route.** The delta
from RR06's text is a single inserted clause after "status mirroring":

> AC6 (BC6, amended): The pass-6 delta's runtime surface is confined to
> `skills/tests/test_thrash_rule.py` and `skills/tests/test_mutation_harness.py`:
> every other file under `skills/` — explicitly including
> `skills/milestone-review/SKILL.md` — is byte-identical across the pass
> (tolerance: `git diff --name-only` over `skills/` names exactly those two
> files), and the guard's module docstring is not edited. Tracking-side changes
> are confined to `cairn/milestones/M114-review-loop-escape-hatches.md`,
> `cairn/DECISIONS.md` per BC1, `cairn/ROADMAP.md` status mirroring and the
> three candidate rows BC8 mandates, and `cairn/reviews/` ingestion and
> archival of RB06/RR06.

The amendment is retrospective and its verification is already on the record:
pass 6 measured the `skills/` half clean (exactly the two files, docstring
byte-identical) and measured the ROADMAP delta as exactly the status mirror
plus the three BC8 rows. AC6-as-amended is therefore VERIFIED on pass-6
evidence with no new pass needed for it. Mechanically: show this amendment at
the RR07 ingestion preview, record AC6-as-amended verified, then replace the
AC block with this review's Binding criteria — RR06's set leaves the live
block and stays in the Review record, as RR05's did at the RR06 ingestion.

**Where the fault lies.** BC6's characterization, specifically — and the
evidence is internal to RR06. Its tracking-side sentence already performs
cross-criterion derivation once: it names "`cairn/DECISIONS.md` per BC1". The
method — enumerate each criterion's write obligations and admit them — was in
the author's hand, applied to BC1, and not applied to BC8, whose ROADMAP
writes were instead summarized from a mental model of the pass as "status
mirroring". That is the same defect RR06 diagnosed in M114's author:
describing an artifact (here, the future pass) from the generative model
rather than deriving it from the governing text. BC8's mandate is not at
fault (banking outside M114 was correct), and freezing a scope by enumerating
files is not at fault either — enumeration is the only thing
`git diff --name-only` can check, and the runtime half of BC6 worked
perfectly, catching nothing it shouldn't and fencing everything it should.
The practice that failed is authoring the enumeration as free prose. The
rule that survives this: **a frozen scope's file list is derived, not
authored — it is the union of the write obligations of the other criteria in
the same set, plus explicitly named mirroring, and it is re-derived whenever
the criteria set changes.** BC1 of this review shows its own derivation
inline, so the check is mechanical at ingest (see Q5).

### 2. Widen the scope for F1 and F2 — and here is the test that decides it in general

**Verdict for these two: fix them in pass 7.** The scope is re-derived to
admit `skills/tests/test_lesson_graduation.py` (and the harness file, already
in scope), with the fixes specified in closed form in BC2 and BC3 below.

**The principled test.** A frozen scope will exclude a real defect every time
it is used, so the decision rule cannot be "was it found in scope". A defect
outside the frozen scope is fixed inside the pass — the scope re-derived to
admit it — exactly when all three hold:

1. **Subject and severity:** it is a confirmed at-or-above-threshold defect
   whose subject is the milestone's own deliverable — merging with the gap
   would leave doctrine the milestone ships unguarded, or leave false a claim
   the milestone's own record makes. The gap falsifies the milestone's
   acceptance story, not merely something adjacent to it.
2. **Closed form:** the gate that owns the scope (the RR, or a gated
   amendment) can specify the fix in closed form — exact anchors, sentences,
   end states — so admitting it adds no authorship to the pass. If specifying
   it requires design judgment, it is new work, not a pass fix.
3. **Replay verification:** the fix is verifiable by replayed probes and
   measured counts, like the rest of the pass.

Fail any leg and the defect is banked with an IP3 disposition instead — a
candidate row, a follow-up milestone, or (for trivia) a trivial-tier fix
after merge — and the branch merges with the gap recorded in the Review
section. The scope's enumeration is an instrument derived from the fix set;
the fix set is never trimmed to preserve the enumeration. What the frozen
scope actually protects is the *authorship* boundary (no judgment re-enters
the pass) and the *wander* boundary (no file changes without a criterion
obliging it) — both survive a re-derivation; neither survives being used to
merge known-unguarded doctrine.

**Applying the test to F1 and F2.** Leg 1 holds: both are 90+ and both are
guards over §3 and §7 of `guard-doctrine.md` — doctrine M114 itself ships.
Merging with the gap merges the exact diagnosis-with-no-remedy shape this
branch actioned L2 (92) for one pass earlier, and leaves false the T4
work-log claim that diagnosis and remedy were "pinned separately" and the
D-064 Consequences passage describing the per-cell count half as guarded.
(Fixing F1 makes the D-064 claim true again — no supersession entry needed;
the T4 claim was false when written, so it takes a superseding work-log line
per the pass-4 precedent, folded into BC2.) Leg 2 holds: BC2 and BC3 name the
exact regexes, the exact `Mutation(...)` blocks copied from the shipped
bytes, and the end states — the same closed form BC2–BC4 of RR06 had, which
pass 6 executed flawlessly. Leg 3 holds: the two probes were run red-side-up
in this review and are replayed in BC6. Contrast F5 (66, the stale
`test_search_first_candidates.py` docstring claim): leg 1 fails — zero
coverage impact, no shipped doctrine unguarded — so it is banked, not
admitted (disposition in Beyond the brief, B4).

### 3. Yes — apply recommendation 5's mechanism to pass 7 as a one-off gate step; this is not a BC8 departure

**BC8 banked the standing rule, not the act.** What BC8 (correctly) kept out
of M114 is rec 5's *implementation*: a section in `guard-doctrine.md`, a line
in `/milestone-implement` — durable doctrine surfaces, new work, D-057
territory. It did not and could not ban non-author verification as such: the
review fan-out is already three non-author readers, and spawning a
fresh-context subagent is ordinary conduct. Running the certification once,
as a step of pass 7, adds zero diff lines anywhere — BC8's own tolerance is
"zero lines of the diff implement any of the three", and a process step
leaves no diff line. No row in the Deviations table is owed, because nothing
departs; the banking of recs 4–6 stands untouched.

**Why it must run before M114 reaches `done`.** Every route to `done`
currently ends with the author certifying its own correction, and pass 6 is
the measured refutation of that mechanism *even under transcription*: the
author's AC8 evidence line read the rec 5 row and called it clean without
checking it against RR06 — while the row claimed, in words, to be quoting
RR06. F1 and F2 are the same mechanism one layer down: T4 certified
"diagnosis and remedy pinned separately", and no non-author ever checked the
claimed coverage against the file until pass 6's lens did, at the most
expensive surface. The one defect class that has survived six passes is
precisely the class rec 5 targets. Withholding the only mechanism measured to
catch it — from the one milestone measured to need it — because its
*rulebook form* is banked would be process fetishism; IP3's spirit runs the
other way.

**Minimum form (this is BC5).** One fresh-context reader that authored no
part of the pass, spawned before `status -> review`, given exactly: the AC
block, the pass-7 diff, and the archived RR06 and RR07. It certifies four
things: (i) each AC clause maps to a pinning assert or evidence command;
(ii) every claim in a changed record, docstring, or comment matches the file
it describes; (iii) every anchor and every `Mutation(...)` block matches the
shipped bytes under re-wrap; (iv) **every quotation or attribution — any
claim of the form "X's stated Y" — is located in X verbatim, or the claim is
struck.** Clause (iv) is F3's specific lesson and is the addition this review
makes to rec 5's checklist; the rec 5 row's own text shows why it is needed —
it wrote "RR06's own stated falsifier" beside words RR06 nowhere contains,
and closed with "Never on a count of further defects" one clause after
stating a count. The verdict and any discrepancies are recorded verbatim in
the work log; the gate is entered only at zero unresolved discrepancies. The
author still runs suites, harness, and probes — operation self-corrects
(RR06 B2); certification of descriptions is what moves.

### 4. Finish, via a pass 7 that is fully closed-form plus certified — explicitly superseding RR06's tripwire prescription

**What the pass-6 evidence actually falsified.** Less than the brief's
framing suggests, and the distinction decides the disposition. Pass 6 was not
a uniform transcription pass: BC1–BC4 supplied exact anchors, sentences, and
end states, and every one of them verified with every numeric projection met
exactly. BC8 did not — it mandated *that* three rows exist with
falsifier-class conditions, but supplied no row text, leaving the rows the
one authored residue in a pass sold as authorship-free. The sole artifact
defect of the pass (F3) arose exactly and only there. So the premise
"transcription, not authorship" was not falsified; it was **under-applied** —
where the fix was closed-form, six passes of failure history produced zero
defects; where authorship remained, the diagnosed failure recurred on
schedule. The constraints being internally contradictory (AC6/AC8) is
likewise not a failure of constraint-as-method but a defect in one
constraint's text, fixed by a one-clause amendment (Q1). And F1/F2 lay
outside the scope because RR06 enumerated the scope around its own fix set —
the Q2 test re-derives it.

**Disposition: FINISH, under these constraints.** Pass 7 executes BC1–BC7:
the two guard fixes and the two row corrections specified in closed form by a
non-author (this review), the scope derived and shown, verification by
replayed probes and measured counts, and — new — the description layer
certified by a fresh-context non-author before the gate (Q3). Nothing is
left to author: this review supplies the row clauses verbatim, which is the
one thing RR06 left open. Park is wrong now for the same reason RR06 gave,
strengthened: the deliverable is sound, thrice-vetted, and the distance to
`done` is four closed-form edits plus one spawn — parking that empties
`blocked` of meaning. Drop discards RR-bound, twice-escalated work and every
lesson banked along the way, against IP3's spirit. Split has nothing to
split: the remaining work is one sitting, one file pair, two rows.

**Superseding RR06 — stated explicitly.** RR06's Q4 tripwire prescribed:
if pass 6 returns on a new author-verification defect inside the frozen
scope, park as `blocked` pending the Q3 process changes, no seventh pass. F3
is such a defect, so by RR06's letter M114 parks now. This review supersedes
that clause, on two grounds the tripwire's author did not have. First, the
tripwire conflated "inside the frozen scope" with "inside the transcription":
F3 arose in the residue BC8 left unspecified, so it falsifies the *coverage*
of RR06's closed-form spec, not the transcription premise — and the remedy
for under-specification is to finish specifying (done here), not to park.
Second, "pending the Q3 process changes" has a same-branch equivalent
available immediately: BC5 applies rec 5's mechanism to this pass without
implementing its rule, so waiting for the adoption milestone buys this branch
nothing it doesn't get now. RR06's rec 10 (reject park/drop) is *reaffirmed*,
not superseded. And the tripwire's core insight survives in stricter form as
BC7: pass 7 gets a terminus, defined below, after which parking is not an
option to weigh but the recorded outcome.

### 5. The exhaustion branch is working; the brief loop is a real smell one level up, and the repair belongs at RR ingestion, not in the branch

**What the record shows the branch doing.** Three firings (passes 3, 5, 6 —
the first as trigger (a)'s original remedy, then the exhaustion branch
twice), and each time it did exactly its job: no bare retry was ever the
recommended option, the re-plan/split was spent once and never recommended
again, and every escalation was an offer taken at the maintainer's call,
per-instance, D-004/D-062 intact. Each brief also converged: RB05 settled
design, RB06 settled diagnosis, RB07 settles criteria mechanics —
monotonically narrowing, with no relitigation (RR05's design untouched by
RR06 and this review; RR06's diagnosis confirmed and sharpened by pass 6's
own F3). Nothing false has reached main across six returns. That is the
branch functioning, not looping.

**The smell, named honestly.** RB07 is qualitatively different from its two
predecessors: RB05 and RB06 asked hard questions about the *work*; RB07
exists substantially to repair the *previous brief's output* — RR06 shipped a
binding-criteria set that was jointly unsatisfiable, and nothing between RR06
and the pass-6 gate checked it. That is the description-layer failure mode
moved one level up: the reviewer is also an author of criteria, and its
criteria got none of the scrutiny it prescribed for the milestone's (RR06's
rec 4 mandates a satisfiability audit for plan-time criteria while its own BC
block went unaudited into the AC slot). A brief loop would be three briefs
asking the same question; this is each layer of authorship failing once, in
sequence, as scrutiny moved up the stack. Once is signal, twice would be a
loop — which is what BC7 forecloses for M114.

**No bound on escalations — and the reason is the milestone's own rule.** A
numeric cap on briefs-per-milestone is a count: it pre-commits to paying for
every brief below it, then fires exactly at the cap rather than early — the
precise shape the falsifying-promotion-conditions rule M114 ships forbids,
and this brief's Background shows why the count would have been wrong here
(brief 3 was cheaper than one more blind pass). The bound that already
exists is the correct one: every escalation is a per-instance offer a human
declines or takes (D-004, D-062), and the human is the judgment the count
would badly proxy. For M114 specifically, BC7 adds a *disposition-shaped*
terminus — park on a defined class of evidence — which is how a bound should
be written in this repo.

**The change that is warranted, with its exact text — routed through the
banked rec 4, not the rulebook.** The defect entered at RR ingestion, so
that is where the check belongs. Ingestion already string-diffs the AC block
against the RR (`binding criteria` check) — fidelity is mechanized, but
nothing reads the set for joint satisfiability. The rec 4 candidate row is
extended to cover it (exact row text in BC4), and when that milestone
implements, `skills/milestone-brief/SKILL.md`'s ingestion step 3 gains this
sentence, after the "Binding criteria travel verbatim" passage:

> **Satisfiability read at ingest.** Before the AC block is replaced, read
> the RR's binding criteria as a set: list every file each criterion obliges
> the pass to change, and confirm that any criterion confining scope admits
> every obliged change and that no two criteria demand contradictory states.
> A conflict is resolved here — a shown gated amendment and a row in the
> Deviations table — never discovered at the review gate.

This is conditionally-read skill prose, not tracking-rules; D-057's door
stays shut. It is not implemented in pass 7 (it is new work, and my own Q2
test's leg 1 fails for it — its absence unguards no doctrine M114 ships);
it rides the rec 4 row per BC8's own logic. This review holds itself to the
rule it proposes: BC1 below shows its file list derived from BC2–BC6's write
obligations, so the ingesting session can run the satisfiability read on
RR07 itself, mechanically.

## Beyond the brief

- **B1. RR06's BC8 embedded authorship inside a pass premised on there being
  none.** BC2–BC4 specified anchors and end states; BC8 specified only
  properties the rows must have, leaving row text — including the claim
  "RR06's own stated falsifier" — to the author whose paraphrase-instead-of-
  quote failure RR06 had just diagnosed. F3 is the predictable product. The
  general rule for future RRs: a binding criterion that obliges new prose
  either supplies the prose or names the source it must be transcribed from,
  with quote-fidelity checkable by grep. This review's BC4 supplies the
  prose.
- **B2. RR06's BC6 tracking-side list was derivable from its own criteria
  set and was not derived.** It names BC1's DECISIONS writes ("per BC1") —
  proof the derivation method was in hand — and omits BC8's ROADMAP writes
  from the same set. The reviewer exhibited the failure it diagnosed, one
  level up. Symmetrically, BC1 below carries its derivation inline so it can
  be checked rather than trusted.
- **B3. F2's truncation propagated into the mutation harness.** The
  registered block at `skills/tests/test_mutation_harness.py:2458` is the
  same truncated lead-in ("Carry the renderings INTO the test as positive"),
  so the harness's blanking sweep also proves only lead-in coverage — a
  defect in a guard replicates into its verification machinery when both are
  authored from the same model. BC3 amends the block together with the
  assert; a fix to either alone would leave the other certifying the old
  gap.
- **B4. F5 (66) disposition, per IP3.** The
  `skills/tests/test_search_first_candidates.py` module docstring's claim
  "every asserted phrase lives on a single source line (M23)" is false since
  this branch's own line 61 (`\s+` regex across the shipped wrap). Declined
  for pass 7: it fails Q2 leg 1 (zero coverage impact, no shipped doctrine
  unguarded), and docstring edits are this branch's measured staleness
  hazard. Fix after merge as a trivial-tier commit (CLAUDE.md routing:
  no runtime surface), replacing that clause with: "so every asserted phrase
  lives on a single source line (M23), except the falsifying-class phrase,
  matched with `\s+` across its shipped wrap (M105)". Recorded here so it is
  surfaced, never silently dropped.

## Recommendations

1. **Apply.** Finish M114 via pass 7 under BC1–BC7: fully closed-form fix
   set, derived scope, replayed verification, independent certification,
   defined terminus. This supersedes RR06 Q4's tripwire clause (park pending
   process changes) on the grounds in Q4, and reaffirms RR06 rec 10's
   rejection of park and drop.
2. **Apply.** Amend AC6 by the shown gated amendment to Q1's verbatim text;
   record AC6-as-amended VERIFIED on the pass-6 evidence already in the
   Review record, then ingest this review's Binding criteria as the live AC
   block, RR06's set leaving to the Review record as RR05's did.
3. **Apply.** Fix F1 and F2 in pass 7 per BC2 and BC3 — the Q2 test admits
   them (own-doctrine subject at 90+, closed-form spec, replayable) — and
   supersede T4's "pinned separately" work-log claim by appended entry, never
   edit (IP4).
4. **Apply.** Correct the rec 5 and rec 4 candidate rows per BC4's exact
   clauses: RR06's real falsifier transcribed with its polarity intact, no
   count anywhere in a promote or drop clause, and rec 4 extended to RR
   binding-criteria sets at ingestion.
5. **Apply.** Run the independent description-layer certification (Q3
   minimum form) as pass 7's pre-gate step, BC5. Not a BC8 departure: zero
   diff lines implement any banked recommendation; no Deviations row owed.
6. **Apply.** When the rec 4 milestone implements, add the satisfiability-
   read sentence to `skills/milestone-brief/SKILL.md` ingestion step 3,
   exactly as given in Q5. Nothing lands in `skills/shared/tracking-rules.md`
   (D-057).
7. **Consider.** F5's one-clause docstring correction as a trivial-tier
   commit after merge, exact text in B4.
8. **Reject a numeric bound on exhaustion-branch escalations** — reason: a
   count pre-commits to paying for every brief below it and then fires
   exactly at the cap, the shape M114's own falsifying-promotion-conditions
   rule forbids; the per-instance human gate (D-004/D-062) is the working
   bound, and BC7 gives M114 a disposition-shaped terminus instead.
9. **Reject park and drop as the disposition now** — reason: Q4; parking a
   thrice-vetted deliverable four closed-form edits from `done` empties
   `blocked` of meaning, dropping discards RR-bound work against IP3's
   spirit. Park becomes the *recorded outcome* — not an option to weigh —
   exactly on BC7's condition.
10. **Reject sweeping the remaining logged findings into pass 7** — reason:
    the scope is derived from the fix set and nothing else; F6 (76) is
    discharged by the Q1 amendment, F5 (66) by recommendation 7. A pass that
    grows by accretion recreates the delta wander the frozen scope exists to
    prevent.

## Binding criteria

- BC1: The pass-7 delta, measured from the RR07 ingest commit to the gate:
  `git diff --name-only <ingest>..HEAD -- skills/` names exactly
  `skills/tests/test_lesson_graduation.py` and
  `skills/tests/test_mutation_harness.py`, and every other file under
  `skills/` — explicitly including `skills/shared/guard-doctrine.md`,
  `skills/milestone-review/SKILL.md` and `skills/tests/test_thrash_rule.py` —
  is byte-identical across the pass. Tracking-side changes are confined to
  `cairn/milestones/M114-review-loop-escape-hatches.md` and
  `cairn/ROADMAP.md`, whose delta touches only M114's status cell and the
  rec 4 and rec 5 candidate rows per BC4 (tolerance: no other ROADMAP line
  changes). Derivation, shown: this list is the union of BC2–BC6's write
  obligations — BC2/BC3 write the two test files, BC4 writes the two ROADMAP
  rows, BC5 and the pass write the milestone file's work log, status
  mirroring writes the ROADMAP cell; the RR07 ingestion's own writes (the AC
  block, Decisions pointers, `cairn/reviews/` archival of RB07/RR07, any
  appended DECISIONS entry) land at the ingest commit and are outside the
  measured delta.
- BC2: In `skills/tests/test_lesson_graduation.py`,
  `test_sweep_section_states_the_silent_cell_rule` gains an assert pinning
  §7's operative remedy — `assertRegex` with pattern
  `r"Assert per cell that it checked a positive number of things, and assert across\s+the sweep that the positive case fired somewhere, so universal silence cannot\s+satisfy it\."`
  — with its own `Mutation(...)` entry (`guard="test_lesson_graduation"`,
  target the guard-doctrine module) whose block is the sentence copied from
  the shipped bytes:
  `"Assert per cell that it checked a positive number of things, and assert across\nthe sweep that the positive case fired somewhere, so universal silence cannot\nsatisfy it."`
  — closing F1. The pass-7 work-log entry supersedes, by appended line and
  never by edit (IP4), T4's claim that §3 and §7's diagnosis and remedy were
  "pinned separately", recording that it held for §7's operative remedy and
  §3's continuation only from this fix. Probe: in a scratch copy with a
  verified-green baseline, deleting that sentence from
  `skills/shared/guard-doctrine.md` reds the skills suite; restoring returns
  it green (tolerance: red then green, target byte-identical after restore).
- BC3: The §3 remedy assert in
  `test_absence_section_states_the_matcher_rendering_rule` (currently the
  `assertIn` at `skills/tests/test_lesson_graduation.py:92`) is widened from
  its truncated lead-in to the full remedy — `assertRegex` with pattern
  ``r"Carry the renderings INTO the test as positive\s+controls: append the real value at full precision, rounded, and `signif`-ed,\s+and require the detector to see each one\."``
  — and its registered block in `skills/tests/test_mutation_harness.py`
  (currently line 2458) is replaced by the full sentence copied from the
  shipped bytes:
  ``"Carry the renderings INTO the test as positive\ncontrols: append the real value at full precision, rounded, and `signif`-ed,\nand require the detector to see each one."``
  — closing F2 in both the guard and the harness (B3). Probe: deleting the
  continuation after the lead-in, with the lead-in kept intact, reds the
  skills suite; restore green (tolerance: red then green, byte-identical
  after restore).
- BC4: The two ROADMAP candidate-row corrections, exact replacement clauses.
  In the rec 5 row, the clause "Promote when a milestone whose deliverable is
  a guard next reaches implement — or drop if two such milestones pass review
  with zero coverage findings, RR06's own stated falsifier. Never on a count
  of further defects." is replaced by: "Promote when a milestone whose
  deliverable is a guard next reaches implement. Drop if the defect class
  motivating it stops appearing — guard-authoring milestones passing review
  without description-layer findings while the step is not in place — never
  on a count of milestones or findings. Post-adoption falsifier, transcribed
  from RR06: 'if guard-authoring milestones still average multiple
  description-layer returns after adoption, the step didn't work — retire it
  (D-059), don't tune it.'" In the rec 4 row, the clause "Promote when a
  milestone next carries more than a handful of criteria, or fold into any
  milestone that touches `/milestone-plan`'s gate — drop if criteria authored
  over several milestones prove satisfiable without it." is replaced by:
  "Promote when a milestone next authors acceptance criteria not ingested
  verbatim from an RR — and extend the audit to RR binding-criteria sets at
  `/milestone-brief` ingestion, where RB07's trigger arose: RR06's BC6 and
  BC8 were jointly unsatisfiable and the conflict surfaced at the review gate
  instead of at ingest — or fold into any milestone that touches
  `/milestone-plan`'s gate. Drop if authored criteria stop failing review as
  criteria — no gated amendment forced by an unsatisfiable or conflicting
  criterion — while the audit is not in place; never on a count of milestones
  or criteria." Tolerance: after the pass, `grep -n "zero coverage\|two
  such\|more than a handful"` over `cairn/ROADMAP.md` returns 0 hits, every
  quoted attribution in the three rec rows is locatable verbatim in its named
  source, and the rec 6 row is byte-identical across the pass.
- BC5: Before `status -> review`, a fresh-context reader that authored no
  part of pass 7 certifies the description layer of the pass-7 delta against
  the artifacts: (i) each acceptance criterion maps to its pinning assert or
  evidence command; (ii) every claim in a changed record, docstring, or
  comment matches the file it describes; (iii) every anchor and every
  `Mutation(...)` block matches the shipped bytes under re-wrap; (iv) every
  quotation or attribution in changed content is located verbatim in its
  named source, or struck. The certifier's verdict and every discrepancy are
  recorded verbatim in the work log, and the gate is entered only at zero
  unresolved discrepancies (tolerance: the work-log entry exists and names
  zero unresolved; zero lines of the pass-7 diff implement the standing rules
  of RR06 recs 4, 5 or 6 — their banking stands).
- BC6: On the final tree, the three suites pass from the repo root with exit
  codes checked separately (tolerance: exit 0 each, never piped; projected
  skills 627 / scripts 280 / hooks 91 — BC2/BC3 add asserts to existing test
  methods, no new test method — any departure routes through the Deviations
  table); `python3 scripts/cairn_validate.py` exits 0; `Mutation(...)`
  entries naming `guard="test_lesson_graduation"` number exactly **14**
  against the measured 13 (tolerance: exact; one entry added by BC2, BC3
  amending an existing block in place); blanking every registered block reds
  its named test (tolerance: 0 survivors); and the BC2 and BC3 probes have
  been replayed red-side-up in a `git archive` scratch copy whose baseline
  was verified green before probing (tolerance: 2/2 red on mutation, 2/2
  green on restore, target byte-identical after).
- BC7: Terminus. If pass 7 fails the gate on (i) any finding whose subject is
  work BC2–BC4 specify in closed form, or (ii) any discrepancy in material
  BC5's certifier recorded as clean, then M114 is parked as `blocked` by that
  fact: the work-log line names this criterion, no eighth implement pass is
  queued, and no further review brief is opened for M114 — the recorded
  unblock condition is adoption of RR06 recs 4–5 through their own milestone.
  A gate failure outside (i) and (ii) is a new fact, handled on its merits.
