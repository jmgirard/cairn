# RR06: Why five review passes each found defects in the author's own verification (M114)

- **Date:** 2026-07-26
- **Brief:** `cairn/reviews/RB06-author-verification-failure-pattern.md`
- **Reviewer baseline:** branch `m114-review-loop-escape-hatches` at `eee0678`;
  all three suites green from the repo root with exit codes checked separately
  (skills 625 / scripts 280 / hooks 91, exit 0 each); `python3
  scripts/cairn_validate.py` exit 0, all checks passed, 1 advisory. No tracked
  file was modified during this review; all mutation probes ran in a
  `git archive HEAD` scratch export whose baseline was verified `exit=0,
  Ran 625` before use, byte-restored between probes.
- **Findings independently reproduced this review:** L1, L2 and L3 were each
  re-verified by mutation in the scratch copy — rerouting trigger (a)'s remedy
  to `/hotfix` leaves the suite green (L1); replacing the exhaustion branch's
  remedy-composition sentence with vague prose leaves it green (L2); deleting
  "and the milestone routes through `/milestone-plan`" leaves it green (L3).
  K1's mechanics were confirmed from git: D-064 was appended at `6546db0` and
  edited in place at `96625ba`, both on this unmerged branch.

## Answers

### 1. There is one root cause, and it is broader than the author's hypothesis

**The hypothesis is directionally right and fails on half the evidence.**
"Not re-deriving the records and guards that describe an artifact after
changing the artifact" fits the staleness cases exactly — J3/J4 (T7 edited the
file after T6 had just corrected the docstring), K1's original false claim
(T6 deleted the guard D-064 describes), L1 (an anchor re-authored during the
T9/T10 delta and narrowed against the file's own rule). But a majority of the
evidence is defects that were **wrong at birth, before any change existed to
re-derive from**:

- G7's "Six entries" was written against a registry holding 7 — wrong on
  arrival, the record's own words.
- G4's commit hash `4f7e0dc` never existed at any point; it was written from
  memory, not written correctly and then staled.
- AC2's "repo-wide" was unsatisfiable the moment it was authored — D-064's
  legitimate quotation already existed and IP4 already made it permanent.
- F1, G1, H1: the one-surface guard was blind to the wrap, uncontrolled, and
  vacuity-prone from its first commit; no artifact change de-verified it.
- L2/L3: the two AC6 clauses were never pinned, not un-pinned by an edit.

**The cause that covers both halves: the author verifies descriptions against
its generative model of the artifact instead of against the artifact.** A
record written from the model is wrong at birth when the model is wrong (G7,
G4, AC2, AC11) and goes stale when the model isn't updated after a change
(J3/J4, K1, L1). A guard written from the model pins the renderings the model
imagines, not the ones the target can take (F1, G2, G3), and a coverage claim
checked against the model ("I wrote a guard for the exhaustion branch") passes
at test-exists granularity while the criterion demanded clause-pinned
granularity (L2, L3, H1). Re-derivation failure is the special case of this
where the model was once right; the record shows the general case.

**The three classes are this one cause expressed at three layers.** Class 1
is descriptions-of-doctrine (guards), Class 2 is descriptions-of-artifacts
(records), Class 3 is descriptions-of-intent (criteria). Each is a
second-order artifact authored by the same process that authored its subject
and verified by that process against itself. The discriminating evidence is
where the defects are NOT: the doctrine itself — the one deliverable derived
from external inputs (the intraclass post-mortem data, then RR05) rather than
from the author's own model — has been sound since pass 1, byte-identical
through three passes, and cleared by all three lenses at pass 5. The failure
concentrates exactly and only where the sole input was the author's own model
of its own work.

**The brief's closing observation is the clincher, and the diagnosis predicts
it.** Pass 5 produced three fresh Class-1 findings after the author had
explicitly named Class 1 as the pattern. Naming a pattern is an act of the
model; it adds no independent reader. Guard-doctrine §3 — written by this
milestone — states the mechanism in its own words: "the author of a detector
is exactly who cannot enumerate the renderings it misses." M114 then
demonstrated that sentence five consecutive times, twice while citing it.
The work log shows the author invoking M95 ("anchors copied from the shipped
bytes") in the same delta that shipped L1's narrowed anchor. Any diagnosis
whose remedy is the author applying its own doctrine more diligently is
contradicted by a record in which the author repeatedly cited the doctrine
while violating it. The fix must add an independent reader or a mechanical
check, not another instruction to the same reader.

### 2. The gate is working; the loop upstream of it is miscast, and the fan-out is compensating at the most expensive possible surface

**As a gate, the machinery worked correctly.** Nothing false reached main
(IP1 held); every one of the five returns was caught by the fan-out; the
failure shape narrowed monotonically (design-level at passes 1–3, records at
pass 4, small mechanical items at pass 5); and the thrash rule's own
escalation path fired on schedule and produced RB05, then this brief. The
review side has nothing to fix — the milestone's own Scope already records
that judgment ("changes to the `/milestone-review` fan-out ... it is
working"), and this review confirms it.

**But five passes is compensation, not cost of doing business.** Two
measurements say so:

- **Almost every finding was a non-application of doctrine already in the
  repo.** F1/L1 are M105; G1 is §3; H1 is §7; G7/J3/J4 are §6; L2/L3 are
  §1's own sentence ("the clause likeliest to go unpinned is one a
  mid-implementation gate amendment added ... re-read the guard against the
  acceptance criteria after any amendment" — AC6's clause list arrived by
  RR05 ingestion, exactly that case). The lenses were not supplying insight;
  they were supplying the read-the-artifact step that the implement loop
  claims to perform and demonstrably does not.
- **Each return re-runs full ceremony to find what a single focused reader
  finds in one spawn.** A return costs fresh per-criterion evidence, the
  consistency gate, three lenses, and a scorer. The defects it caught at
  passes 4 and 5 (stale docstring, unpinned clause, narrowed anchor) are
  findable by one fresh-context reader given the guard file, the AC block,
  and the shipped bytes — before the milestone ever leaves implement.

**The structural claim in the brief's question is too broad, though.** The
loop is not wrong "for a milestone whose deliverable is doctrine about
verification" — the irony is real but the mechanism is authorship, not
subject matter. The author-verifies-own-work loop performed fine on the
first-order deliverable; it failed on the description layer, and the
intraclass record (M92: seven passes, "1-6 each failed AC5 on prose authored
about the work, never on the code") shows the same signature on milestones
whose deliverables were not verification doctrine. The loop is structurally
wrong for **self-describing artifacts** — guards, records, and criteria about
the author's own work — wherever they occur. That is what should be fixed
upstream, and it is narrower and cheaper than reworking the loop in general.

### 3. Rules: one to reject, two to apply in scoped form — and none in the rulebook

**(a) A mandatory re-derivation step after any artifact change —
reject-with-reason.** This is "try harder" in rule form, addressed to the
same reader who already holds six lessons and two doctrine sections saying
re-derive, and who cited them while violating them (Q1). The record directly
falsifies the mechanism: guard-doctrine §1 predicted L2/L3's exact shape in
advance and did not prevent them; the T10 work-log entry invokes M95 in the
delta that shipped L1. It would also bind every milestone always (a process
tax D-057's evidence warns about — governance ceremony was the most expensive
thing this repo ever measured) to repair a mechanism measured not to work,
which is the direction D-059 exists to forbid. More prose to the same judgment
does not pay; do not add it.

**(b) Implementer-authored acceptance criteria reviewed before implementation
begins — apply, scoped to the plan gate.** Class 3 cost this milestone a full
return (AC2, pass 1), a second amendment (pass 2), and part of a fifth return
(AC11). All three defects were discoverable at plan time by a reader asking
two mechanical questions per criterion: *what state of the world satisfies
this exactly as written* (AC2 fails — the phrase already legitimately occurred
in `DECISIONS.md`, one grep away), and *does any IP or D-entry make that state
unreachable* (AC11 fails — IP4/D-045 forbid the edit it mandates, one read
away). Guard-doctrine §7 already knows plan time is where grep-shaped
criteria get scoped cheaply ("exempt the tracking lines in the criterion at
plan time — otherwise it needs a gated amendment at implement"); this
generalizes that insight from one criterion shape to the AC block. **Form:**
a fresh-context audit of the AC block at the `/milestone-plan` gate — fresh
context because the plan author's own check is precisely what failed. **Home:**
`/milestone-plan`'s SKILL, a conditionally-read surface; D-057's door
governance is not in play. **Cost:** one subagent per plan, against a measured
price of gated amendments and review returns.

**(c) A guard's author may not be the one who verifies it — apply, in the
scoped form; the ban as stated is the wrong cut.** The author must still run
suites, harness, and sweeps — that is operation, and the record shows the
author's *command-level* verification self-corrects fine (see Beyond the
brief, B2). What must move to an independent reader is **certification of the
description layer**: that each AC clause maps to a pinning assert, that every
docstring/comment/record claim about the guard matches the file it sits in,
and that every multi-word anchor matches the shipped bytes under re-wrap.
This is candidate (c) restated as: *the author may not certify its own
guard's coverage*. The mechanism is already proven in-repo — the review
lenses are the same model in fresh context reading artifacts without the
generative model, and they went five for five — this recommendation only
moves one focused instance of it earlier, from after `status -> review`
(price: a full return) to the end of implement (price: one spawn). It is
also the honest D-059 move: author self-certification of guard coverage is a
mechanism now measured not to work across five consecutive passes plus the
intraclass record; retire it and route the load to the mechanism measured to
work, rather than repairing it with more doctrine. **Home:** a short section
in `guard-doctrine.md` (conditionally read exactly at guard-authoring time)
plus one line in `/milestone-implement`'s pre-review step; not the rulebook.
**Falsifier, stated up front per this milestone's own promotion-condition
rule:** if guard-authoring milestones still average multiple
description-layer returns after adoption, the step didn't work — retire it
(D-059), don't tune it.

**Both applied rules are new work and neither rides into M114** (BC8). They
route through `/milestone-plan` as their own scoped milestone, with promotion
conditions naming falsifying evidence classes, never counts — the rule this
milestone ships, applied to its own aftermath.

**Rejected additionally: any `cairn_validate` mechanization of the above.**
Clause-coverage and claim-accuracy are judgment over prose meaning, exactly
the shape D-064 choice 6 declined to mechanize and D-059's retirement
precedent covers. The rulebook itself gains nothing under any of these
recommendations; D-057's door stays shut.

### 4. Finish — with the sixth pass constrained so the step that failed five times never runs

**Finish is right; park and drop are both worse.** The deliverable is sound,
externally vetted twice (RR05 on design, three lenses on substance at pass 5),
and both numeric tolerances were met exactly. The four remaining findings are
small, mechanical, and now independently reproduced and specified in closed
form by a non-author (this review — the Binding criteria below carry the
exact anchors, sentences, and end states). Parking a finished, vetted
deliverable over four enumerated mechanical defects makes `blocked` mean
"nobody wrote three asserts"; dropping discards user-directed, RR-bound work
against IP3's spirit. And the exhaustion branch's constraint is satisfied,
not circumvented: this is not a recommended bare retry — the maintainer chose
the branch's escalation option, the escalation ran, and its output is a
constrained fix set. That is the branch working as designed, on its own
milestone, end to end.

**What makes a sixth pass different from the previous five: the authorial
step that failed is removed, not re-attempted.** Every prior pass asked the
author to *decide* what to pin, write, or claim — the exact operation Q1
diagnoses — and pass 5 followed passes 1–4 for that reason. Pass 6 is
different only if it is transcription:

1. **The fix set is externally specified in closed form.** BC1–BC4 name the
   anchors, the sentences, and the end states. No judgment about what to
   cover remains with the author.
2. **The scope is frozen** (BC6). Class 2 arose from delta wander — T7
   re-staled the docstring T6 had just fixed. Pass 6 touches only the
   enumerated files; `skills/milestone-review/SKILL.md` is not edited at all
   (RR05's design is settled and every fix is guard- or record-side), and the
   guard's module docstring is not edited (it is count-free per AC7, its
   property list already names the compose and exhaustion properties the new
   asserts pin, and every docstring edit in this milestone's history
   introduced a staleness defect).
3. **Verification is replay, not judgment** (BC7). The probes are the three
   mutations this review already ran red-side-up, plus the standard blanking
   sweep and measured counts. The author re-executes them; it does not design
   them.
4. **A tripwire replaces open-ended iteration.** If pass 6 returns on any
   new author-verification defect *inside* the frozen scope, that falsifies
   this review's premise that transcription suffices — park as `blocked`
   pending the Q3 process changes rather than attempt a seventh pass. (A
   finding outside the frozen scope is a new fact, handled on its merits.)

### 5. The rubric is not wrong; its application systematically discounts exactly one class, and the record shows four instances, not two

**First, the count is four, not two.** Beyond F4 (60 → the pass-3 collision)
and J5 (35 → the pass-5 miscount): F3 (30, "the rewrite drops the old
count-the-work-log pointer") was adopted at T7 and the work log itself
records "F3, scored 30 and right"; and G6 (68, stale `\s+`-exception count)
recurred as J3 at 85 in the same file one pass later. Four under-scores that
later mattered, out of fourteen sub-threshold findings logged, is a signal,
not noise — though the selection bias cuts the other way too (an under-score
only becomes visible when the milestone survives long enough for it to fire,
and no ≥80 finding was ever reversed, so the threshold's positive side is
clean).

**The pattern in the four is one class.** All four are *predictive* findings
about the milestone's own doctrine or records, whose harm was contingent on a
future process event: a collision that had not yet co-fired, a count that had
not yet been miscounted, a pointer whose absence had not yet stranded a
reviewer, a stale count that had not yet propagated. None was demonstrable by
running a command at scoring time — and every ≥80 finding was. The rubric, as
applied, operationalizes confidence as *present demonstrability*. For code
that is a fine proxy: a latent code defect can be demonstrated now with the
right input. For process doctrine, the defect only manifests when the process
path is walked, so demonstrability-now systematically under-weights exactly
the findings that matter for a doctrine deliverable. The scorer's own words
show the mechanism: J5 was held at 35 because the token "tracks them reliably
in practice" — a claim about future counting behavior, taken from the
author's records, and falsified one pass later.

**Verdict: two instances would be insufficient; four with a shared mechanism
is enough to act on the disposition, not the rubric.** The 80 threshold and
the rubric survive — their job is ranking present defects and they did it
(every actioned finding was real). What fails is the *disposition* of one
narrow class, and RR05 B3 already named the fix: a sub-threshold finding
whose subject is doctrine or criteria the milestone itself ships gets a
cheaper disposition than "wait until it happens" — resolve it at the gate
that is already open, or decline it with a recorded reason; never merely log
it. That is two sentences in `/milestone-review`'s scoring step
(conditionally read; D-057 untouched). Rewriting the rubric or moving the
threshold on n=4 — reject; the general bar is doing its job.

## Beyond the brief

- **B1. Class-2 defects contaminate the scorer, so fixing Class 2 upstream
  also repairs scoring.** The scorer is fresh-context but scores findings
  against the author's records: J5's 35 rested on an author-context claim
  pass 5 falsified. A rubric applied honestly to false inputs under-scores
  honestly. This tightens Q1's diagnosis: record integrity is not just an
  output property, it is an input to every downstream judgment including the
  independent ones.
- **B2. The author's failure is layer-specific, and the record proves it with
  a clean contrast.** Where the artifact pushes back immediately, the author
  self-corrects: pass 3 caught its own case-sensitive evidence command, pass
  5 caught its own over-broad AC7 probe — both recorded unprompted ("the
  second time this session"). Where the artifact cannot push back — prose
  claims, coverage certifications, criteria — defects persist until an
  independent reader supplies the feedback. This is why Q3(c) targets
  certification and not operation, and it predicts where any future rule will
  and won't work: mechanical feedback loops self-heal, judgment-only loops
  don't.
- **B3. The thrash rule's counting clause proved itself at pass 5.** A naive
  `grep -c "FAILED the gate"` returns five (one hit is prose inside pass 4's
  Review section); the work-log-scoped count the rule mandates returns four,
  which is correct. The clause F3 (30) restored at T7 is the reason the
  count was right when it mattered — worth noting as evidence banked for the
  rule, and as F3's final vindication.
- **B4. The IP4 question K1 forces has a subtlety the fix must respect.**
  Once an illegal in-place edit exists on the branch, *both* leaving it and
  reverting it touch the entry. Reverting is the IP4-conforming terminus:
  the protected object is the record as appended (`6546db0`), the edit is a
  working-tree defect that has not reached main, and restoring makes the
  protected object whole while git preserves the incident. Leaving the edited
  bytes and appending a note would make the rewrite permanent on main — the
  strictly worse outcome under IP4. The repo's own precedent already decides
  this: pass 4 refused the identical edit on work-log claims *on this same
  unmerged branch*, fixing append-time, not merge-time, as when IP4 attaches.

## Recommendations

1. **Apply.** Finish M114 via a constrained sixth pass per the Binding
   criteria below; the fix set is transcription, the scope is frozen, and
   verification is replay (Q4).
2. **Apply.** Amend AC11 by gated amendment to the supersession route:
   restore D-064's appended bytes and append a superseding DECISIONS entry
   carrying the correction; never edit an appended entry again, merged or not
   (Q4, K1, B4 — strengthens IP4/D-045, weakens nothing).
3. **Apply.** Close L1, L2, L3 exactly as specified in BC2–BC4, with counts
   measured and the red-side probes replayed (Q4).
4. **Apply.** The plan-gate criteria audit: at the `/milestone-plan` gate a
   fresh-context reader checks each acceptance criterion for
   satisfiability-as-written and for conflict with any IP or D-entry; home in
   `/milestone-plan`'s SKILL (Q3 candidate b, scoped). New work — routed
   through `/milestone-plan`, not folded into M114.
5. **Apply.** Independent certification of the description layer for
   guard-authoring milestones: before `status -> review`, a fresh-context
   reader verifies AC-clause-to-assert coverage, claim-vs-file accuracy, and
   anchor-vs-shipped-bytes fidelity; the author never certifies its own
   guard's coverage. Home in `guard-doctrine.md` plus one line in
   `/milestone-implement`; carries its own stated falsifier and D-059 exit
   (Q3 candidate c, scoped). New work — routed through `/milestone-plan`.
6. **Consider.** RR05 B3's disposition rule for sub-threshold findings whose
   subject is doctrine the milestone itself ships: resolve at the open gate
   or decline with recorded reason, never merely log (Q5). Two sentences in
   `/milestone-review`'s scoring step.
7. **Reject a mandatory re-derivation step after any artifact change** —
   reason: it instructs the same judgment that failed while citing the same
   instructions; guard-doctrine §1 predicted L2/L3 in advance and prevented
   nothing; it taxes every milestone to repair a mechanism measured not to
   work, which D-059 says to retire, not repair (Q3 candidate a).
8. **Reject any rubric rewrite or threshold move** — reason: n=4 with
   selection bias, and every ≥80 finding was real; the defect is the
   disposition of one finding class, fixed by recommendation 6 (Q5).
9. **Reject any `cairn_validate` mechanization of criteria audits or
   coverage certification** — reason: judgment over prose meaning, the shape
   D-064 choice 6 declined and D-059 retired; the fresh-context reader is the
   right instrument (Q3).
10. **Reject park and drop for M114** — reason: parking a twice-vetted
    deliverable over four enumerated mechanical fixes empties `blocked` of
    meaning; dropping discards RR-bound work against IP3's spirit; the
    exhaustion branch's escalation option was taken and produced this
    constrained path, so finishing is the branch's own outcome, not a bare
    retry (Q4).

## Binding criteria

- BC1: AC11 is amended through a shown gated amendment to require the
  supersession route, and the end state on the branch is: D-064's entry in
  `cairn/DECISIONS.md` is byte-identical to its originally appended form
  (commit `6546db0`), and a new appended DECISIONS entry records that D-064's
  one-surface Consequences claim is superseded — the guard was re-cut out at
  M114's third return and the pin is a ROADMAP candidate. Tolerance:
  `git diff 6546db0..HEAD -- cairn/DECISIONS.md` contains additions only —
  zero deletion or modification lines inside the D-064 entry.
- BC2: In `skills/tests/test_thrash_rule.py`, the assert on trigger (a)'s
  remedy pins the full remedy including its routing target — the anchor spans
  the phrase "recommend re-plan or split via" together with its
  backtick-quoted `/milestone-plan` target, matched with `\s+` across the
  shipped wrap — closing L1. Probe: in a scratch copy, editing the shipped
  rule's routing target to `/hotfix` reds the skills suite; restoring returns
  it green (tolerance: red then green, 0 mismatches).
- BC3: The composition clause's routing half — the phrase "and the milestone
  routes through" together with its backtick-quoted `/milestone-plan` target,
  matched with `\s+` across the shipped wrap — is pinned by its own
  doctrine-pinning assert, closing L3. Probe: deleting that clause in a scratch copy reds the skills
  suite (tolerance: red, then green on restore).
- BC4: The exhaustion branch's positive remedy composition — the routing chip
  composed from an offered `/milestone-brief` escalation, parking as
  `blocked`, or dropping at the user's explicit decision — is pinned by its
  own doctrine-pinning assert, closing L2. Probe: replacing that sentence
  with prose naming no options in a scratch copy reds the skills suite
  (tolerance: red, then green on restore).
- BC5: Each added doctrine-pinning assert carries its own `Mutation(...)`
  entry with its block copied from the shipped bytes; the doctrine-pinning
  assert count equals the registered entry count, both read out of the files
  (tolerance: exact; projected 19 against 19 — two asserts added to the
  measured 17, with BC2 amending an existing assert and its registered block
  in place — any departure in the projected number routes through the
  Deviations table); blanking every registered block reds its named test
  (tolerance: 0 survivors).
- BC6: The pass-6 delta's runtime surface is confined to
  `skills/tests/test_thrash_rule.py` and
  `skills/tests/test_mutation_harness.py`: every other file under `skills/`
  — explicitly including `skills/milestone-review/SKILL.md` — is
  byte-identical across the pass (tolerance: `git diff --name-only` over
  `skills/` names exactly those two files), and the guard's module docstring
  is not edited. Tracking-side changes are confined to
  `cairn/milestones/M114-review-loop-escape-hatches.md`, `cairn/DECISIONS.md`
  per BC1, `cairn/ROADMAP.md` status mirroring, and `cairn/reviews/`
  ingestion and archival of RB06/RR06.
- BC7: On the final tree, the three suites pass from the repo root with exit
  codes checked separately (tolerance: exit 0 each, never piped),
  `python3 scripts/cairn_validate.py` exits 0, and the three probes of
  BC2–BC4 have been replayed red-side-up in a scratch copy whose baseline was
  verified green before probing (tolerance: 3/3 red on mutation, 3/3 green on
  restore).
- BC8: Recommendations 4, 5 and 6 are banked outside M114 — as ROADMAP
  candidate rows or a `/milestone-plan`-cut milestone — each with a promotion
  condition naming the class of evidence that would falsify it, never a count
  (tolerance: zero lines of M114's pass-6 diff implement any of the three;
  their disposition appears in the work log or ROADMAP, per IP3).
