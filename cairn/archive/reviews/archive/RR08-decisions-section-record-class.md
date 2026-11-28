# RR08: Is the milestone-local `## Decisions` section history or current knowledge? (M118)

- **Date:** 2026-07-27
- **Brief:** `cairn/reviews/RB08-decisions-section-record-class.md`
- **Materials read:** `cairn/DESIGN.md` (IP block); `skills/shared/tracking-rules.md`
  (ownership tables, weight caps, always-read governance, "Correcting a record
  proven false"); D-030, D-045, D-046, D-063, D-066, D-074 whole;
  `cairn/milestones/M118-decisions-section-cap-exempt.md`;
  `skills/shared/templates/milestone.md`; the `## Decisions` sections of M114
  (43 lines, `git show a25e6dd^`), M83, M84, M94, M98 at their final pre-archive
  revisions (ref-based git only); `hooks/session_context.py` (CAP_EXEMPT_SECTIONS),
  `scripts/cairn_scripts.py` (WORKLOG_HEADING, extractors),
  `scripts/cairn_validate.py` (check_worklog_format),
  `skills/tests/test_milestone_cap_exemption.py` (set-membership anchor).

## Answers

### 1. Is the classification correct?

**Yes — the section is history in D-045's sense.** The verdict is reached from
D-045's own criteria and the corpus, not from the cap.

D-045's operative distinction is the record's claim-type and its correction
discipline: history "records what was decided or done at a time, and is never
edited: supersede, never rewrite"; current knowledge "records what is true
*now*, is read to act on, and is corrected in place when proven false." Four
independent lines of evidence put the section on the history side:

- **What the entries are.** Every worked example at size is a set of dated
  dispositions. M114's 13 entries are round-by-round RR dispositions
  (`2026-07-26 (RR07 Q4): FINISH, superseding RR06 Q4's park-tripwire…`).
  M94's are dated RR-finding triages. M83's are dated mechanism decisions.
  M98's is a dated graduation ledger with its bar and its classification as
  decided that day. None of these asserts "what is true now" in LESSONS' sense
  — each records what was decided at a moment, exactly D-045's history
  criterion.
- **What the section is a shard of.** The file map's `DECISIONS.md` row
  explicitly delegates milestone-local decisions to the milestone file
  ("Milestone-local decisions (those live in the milestone file)"). The
  section is the declared local shard of the repo's canonical history file —
  same name, same dated-entry shape, same promote-when-cross-cutting valve.
  Classifying the shard differently from the file it shards would need a
  positive argument, and none exists.
- **Observed correction practice.** The decisive behavioral evidence is
  M83-D3: when two milestone-local decisions were proven wrong live (review
  findings F1/F2), the remedy actually used was supersession within the
  section — "M83-D3 (supersedes M83-D1 and M83-D2)… D1 and D2 stand as the
  record of what was tried; this is what ships." The section already operates
  under the history discipline, and it worked: the superseding entry sits
  lines below the superseded ones in a short section every reader reads whole.
- **Who consumes it, and for what.** The M114 post-mortems (D-066, D-067) were
  reconstructed from milestone files' unedited dated records — M114's
  Decisions section records the round-by-round RR dispositions those entries
  cite. An in-place-corrected section would have destroyed exactly the
  evidence those audits mined. The section's downstream value is *as* history.

One nuance, not a reversal: some content at size is measurement/evidence
rather than decision (M84-D1's survey table; M118's own T3 plans to commit a
per-file ledger into the section). Those are dated observations — snapshots
true of a date, which do not become false when the repo changes — so they do
not break the classification; but they do sit better in `## Review` (evidence)
or a committed file than in a decisions record. See rec 4 / BC4.

### 2. Is the supporting argument sound, or is it circular?

**The recorded argument is partly outcome-driven, but the conclusion is
independently derivable, and D-074's primary ground is already the forward
one.** Read D-074 part 1 closely: its first stated ground is forward-direction
— "the ownership table already makes it append-only, and its entries record
what was decided at a time." Only the auxiliary clause ("the alternative
classification is self-defeating: … a trimmable section has no claim to an
exemption grounded in un-editability") reasons from the exemption's
desirability. That clause is not strictly circular — it is a coherence check
showing one cannot hold both "current knowledge" and "un-editability
exemption" — but it cannot pick which horn to drop; only the forward argument
can, so it must not be read as load-bearing.

Run in the other direction, asking what the section *is* with the cap deleted
from the picture: the entries are dated dispositions (Q1), the section shards
DECISIONS.md by the file map's own delegation, and the one live correction the
corpus contains was handled by supersession (M83-D3). Same answer: history.

One weakness in the forward argument worth recording: **"the ownership table
says append-only" is corroborating, not sufficient.** D-045 itself is the
counterexample shape — the file map labeled `LESSONS.md` "append-only" and
D-045 found the label wrong, because it contradicted the file's cap-and-prune
governance and its actual practice. A write-mode label cannot settle record
class on its own. Here, unlike LESSONS, the label is *coherent* with
everything else that governs the section and with observed practice, which is
why the classification stands — but the classification rests on content and
practice, with the label as confirmation. If the D-074 rationale is ever
restated (rulebook wording, RR ingestion notes), lead with entries-and-practice,
not the table.

### 3. Is there a third option the plan missed?

**Yes, one exists — exemption on D-030's differently-owned ground — and it is
real, but inferior. M118's route should stand.**

The route is available and the repo's own records nearly state it: the cap
governs *plan discipline* (D-030: "the point is that plan discipline stays at
150"; D-074's rejection of raising the cap: "it governs plan discipline, which
is not what overran"), while the ownership table makes `## Decisions`
implement/review-owned — plan never writes it, and the template preamble says
so outright ("implement/review-owned, still counted (D-030/D-046) … so plan
spends none of it"). Charging a section plan cannot write or trim to a
plan-discipline budget was a category error from the start; `## Review` was
exempted on exactly that ground. The section is in fact the only one that
qualified under *both* recognized grounds (D-046's Consequences names the
taxonomy: "un-editable rather than differently-owned") and was still counted —
which is why the original refusals needed the brevity premise, now measured
false.

Comparison:

- **Robustness.** The ownership route makes a narrower commitment — no IP4
  extension — but it leaves the section's record class *undecided*. That is
  the exact gap D-045 was minted to close: an unclassified record surface
  eventually meets a proven-false entry, and the session at that moment either
  corrects in place with no rule sanctioning it (M75's incident, replayed) or
  supersedes with no rule requiring it. The question returns at the worst
  time, mid-milestone, instead of being settled now for one D-entry.
- **What each commits the repo to later.** M118's route commits the section to
  supersede-only forever (cost priced in Q4: low, and the section is now
  unbudgeted so supersession costs no cap). The ownership route commits to
  nothing — which is not neutrality but deferral, and it would also leave the
  cap-exempt set's justification prose weaker: "implement/review-owned" is
  true of `## Review` too, whose unboundedness is tolerated because it
  compresses at archive; the Decisions section's real claim to never being
  aimed at by the cap remedy is IP4, and only the history classification
  supplies that.
- **Mechanics are identical either way** (extraction beside the work log;
  D-063's read-bound is scoped to the cap-exempt set, so the section joins the
  read-bound under both routes).

Verdict: the ownership observation is worth keeping *as supporting context* —
it independently explains why the section never belonged in a plan-discipline
budget — but the exemption's operative reason should stay the one D-074 part 2
gives. Reject the third option as the route; see rec 6 for the salvage.

### 4. What does the classification cost if it is wrong?

**An acceptable outcome, not merely an acceptable cost — and for this section
the supersede discipline is affirmatively better, not a tolerated loss.**

If the section were really current knowledge, IP4 would force
supersede-by-later-entry for a milestone-local decision proven false. Price
that against D-045's stated failure mode ("a false record left readable gets
harvested into later plans"):

- **The harvest surface barely reaches this section.** Plan-time harvest reads
  LESSONS, the archive, and DECISIONS.md heading sweeps — not other
  milestones' live `## Decisions` sections; the section dies with the
  milestone into a ≤25-line archive summary. The misleading-record window is
  the milestone's own lifetime.
- **Within that window, supersession demonstrably works.** The section is
  short (median 4, max 43 lines) and read whole by anyone reading it at all;
  a superseding entry sits lines below the superseded one (M83-D3). D-063's
  newest-first injection even *privileges* the superseding entry — for a
  decisions section, newest-first is semantically the right order, because
  corrections are the newest content. Contrast DECISIONS.md, where entries sit
  2,400 lines apart and D-054's back-reference protocol exists to bridge the
  gap; the local section needs no such machinery.
- **The repo's own precedent.** `cairn/DECISIONS.md` operates supersede-only
  at repo scope and it works; the local shard operating the same way is
  consistency, not cost.
- **The genuine (small) loss, named:** a typo-grade factual slip in an entry
  (wrong line number, wrong date) cannot be repaired in place; superseding it
  burns an entry on trivia. Now unbudgeted, that burn costs no cap — accept it.
- **The affirmative case:** the D-066/D-067 post-mortems depended on the
  unedited round-by-round record. A section whose entries could be corrected
  in place would silently erase the "what was tried" trail (M83-D1/D2 "stand
  as the record of what was tried") that is this section's chief downstream
  value.

The work-log line of M118 records the right falsifier ("a milestone-local
decision that must be corrected in place rather than superseded by a later
entry in the same section"); nothing in the corpus instantiates it.

### 5. Does extending IP4's reach create second-order problems?

Three considered; one real gap found, one plan defect found, one non-problem.

- **D-063's read-bound gaining a third member is by design, but the wiring is
  enumerated, not derived.** D-063 choice (3) states the rule as derived
  ("sections the 150-line cap exempts are read-bounded"), yet the hook
  implements it as a hand-enumerated tuple
  (`CAP_EXEMPT_SECTIONS = ("work log", "review")`,
  `hooks/session_context.py`) with no test tying it to the cap counters'
  exempt set. M118's AC4 updates this instance explicitly — so nothing is
  *silent* in this plan — but nothing prevents a future member landing
  one-sided: cap-exempt in `cairn_scripts` but injected whole by the hook,
  which is precisely "the gap the read-bound exists to close" per the hook's
  own comment. Since M118 is the change that turns the pair into a trio and
  touches both sides anyway, it should leave the consistency mechanically
  asserted. BC2.
- **`cairn_validate` enforces IP4 on no section — unchanged, and by prior
  decision.** D-045 explicitly declined a validate check for correction
  discipline ("advisory doctrine has never been a validate gate"); the work
  log and DECISIONS.md already carry IP4 as conduct with no machine check.
  Adding a third section adds no new asymmetry. The two-writer point
  (implement and review both append) is likewise no weaker than the work log,
  which "any skill" appends to. Non-problem.
- **The real plan defect is AC5's transplanted grammar.** The `decisions
  format` advisory as specced WARNs on "an entry that is not a one-line `- `
  entry" — the work-log grammar. But the work log had a pre-existing one-line
  mandate the advisory merely enforces; the Decisions section has none, and
  its observed genre at size is the opposite: **every one** of M114's 13
  entries wraps to 2–3 physical lines, M83's are paragraphs, M84 and M98 use
  `### M<NN>-D<n>` sub-headings with paragraph bodies, M94's entries run 2–5
  lines each. A decision entry structurally carries rationale (alternatives,
  reasons) the way DECISIONS.md entries do; a one-line grammar either strips
  the rationale out of the record — destroying the value Q1/Q4 established —
  or WARNs permanently on every normal entry in exactly the M114-shaped files
  the exemption exists for, for the file's whole live window (the advisory
  reads live files only). A permanently-warning advisory trains the operator
  to ignore advisories. D-046's underlying concern is right and stays
  (something must watch an unbudgeted section for pasted output); the
  *grammar* must be the section's own. BC3, and note the D-074 collision it
  entails (below).

## Beyond the brief

- **D-074's "three distinct reasons" sentence miscounts.** Part 2 says the
  section joins "for D-046's reason and not D-030's," then says "the set
  becomes three members carrying three distinct reasons." Those cannot both be
  true: Review is exempt as differently-owned, Work log as history, and
  Decisions joins as history — three members, **two** grounds (or a
  work-log-shared ground, however sliced). D-074 is history and stays as
  written; but AC6 instructs every enumeration site to name "each member's own
  reason," and the shipped wording must not assert a false trichotomy. Say
  "three members, each with its stated reason" and let the Decisions reason
  cite D-045/D-074 the way the Work log's cites D-045/D-046 — honest, and it
  keeps the set-membership guard anchor re-derivable.
- **T3 self-collision.** T3 commits the AC3 per-file measurement table "into
  this file's `## Decisions` — the exemption's first use." That table is (a)
  AC3's *evidence*, which AC fencing places in `## Review`; (b) not a decision,
  so it dilutes the section's inflow the first time the section stops costing
  budget — the exact bloat D-046 feared; and (c) under AC5 as currently
  specced, a WARN generator inside the milestone's own file at its own review
  gate. Move the ledger (BC4); the exemption's "first use" is not a goal.
- **Reassurance worth recording:** D-063's newest-first order, designed for
  work logs ("a resume needs current state"), is independently correct for a
  decisions section — the newest entries are the superseding ones (M83-D3
  pattern), so the read-bound surfaces corrections first and elides the
  superseded tail. The composition is sound, not accidental.

## Recommendations

1. **Apply — uphold D-074 part 1.** The history classification is correct on
   forward-direction grounds (Q1); the RB's escalation resolves in favor of
   the recorded decision. No re-plan of M118's direction is needed.
2. **Apply — add the section to the rulebook's history-class enumeration.**
   The "Correcting a record proven false" bullet enumerates history's members
   (`tracking-rules.md:205-207`); it is the classification's authoritative
   rulebook surface and is absent from AC6's site list, so shipping M118
   without it leaves the rulebook's own member list contradicting D-074. BC1.
3. **Apply — redefine the `decisions format` advisory against the section's
   own genre**, not the work log's one-line grammar (Q5, third bullet). This
   departs from D-074 part 3's literal wording ("an entry that is not one
   line"), so it requires its own annotating D-entry narrowing part 3 —
   recorded at ingestion, before code, while reversal still costs one entry.
   BC3 states the measurable form; the detection mechanism (non-entry orphan
   lines, fenced blocks, or another shape) is the implementer's choice.
4. **Apply — move the T3 ledger out of `## Decisions`** into `## Review` (it
   is AC3 evidence) or a committed file. BC4. T3's text is amend-via-gate;
   the amendment is one line.
5. **Apply — assert hook/counter exempt-set consistency mechanically.** BC2.
6. **Consider — record the ownership observation as supporting context.** One
   clause in the rulebook's reason sentence or M118's work log noting the
   section was never plan-owned strengthens the exemption's story without
   becoming a second official ground; do not restructure the reasons around it.
7. **Reject — the third-option route (exempt without classifying, Q3).** It
   is available but leaves the record class undecided, re-creating the
   unclassified-surface gap D-045 exists to close; the classification is
   independently correct, so taking the weaker route buys nothing.
8. **Reject — any softening of the classification to hedge Q4.** The cost
   analysis shows supersede-only is the better discipline for this section,
   not a tolerated tax; no "current knowledge with restrictions" hybrid is
   warranted (and none exists in D-045's taxonomy to borrow).

## Binding criteria

Checked against itself for joint satisfiability: BC1 and M118's AC6 edit the
same rulebook file but no criterion freezes a file list, so no D-066-shaped
collision; BC3 collides with D-074 part 3's literal grammar and BC4 with T3's
current text — both collisions are named inside the criteria and resolved by
the ingestion-time instruments the repo already has (an annotating D-entry;
an amend-via-gate task edit), not discovered at review. Four criteria, sized
to sit beside M118's seven ACs; carry-by-reference (D-066 choice 4) is
available if the file cannot hold them verbatim.

- **BC1.** The history-member enumeration in `tracking-rules.md`'s
  "Correcting a record proven false" bullet names the milestone-local
  `## Decisions` section as a history member alongside `DECISIONS.md`,
  work-logs, milestone IDs, `milestones/archive/`, `reviews/archive/`, and
  entombed `legacy/` files; the guard suite pins the amended sentence under
  the file's existing mutation-registration rules. Evidence: the sentence in
  the shipped rulebook plus a green targeted guard run.
- **BC2.** A committed test fails whenever `hooks/session_context.py`'s
  `CAP_EXEMPT_SECTIONS` and the cap counters' exempt heading set
  (`scripts/cairn_scripts.py`) disagree in either direction, comparing
  normalized headings from both modules (a shared or mirrored constant the
  test reads from each side). Evidence: the test present and green, plus a
  demonstrated red under a one-sided member removal (the by-hand mutation
  check the guard rules already sanction is sufficient).
- **BC3.** The shipped `decisions format` advisory, run over the final
  pre-archive revisions of the measured ≥145-line files (at minimum M83, M84,
  M94, M98, M114, via ref-based `git show` into fixtures), emits **0 WARNs**
  (tolerance: exactly 0) on the corpus's standard entry forms — dated `- `
  entries that wrap, `### M<NN>-D<n>` sub-decision headings with paragraph
  bodies, and the template ownership comment — and **≥1 WARN** on a
  constructed fixture containing pasted command output or a fenced transcript
  block inside the section. This narrows D-074 part 3's "not a one-line `- `
  entry" grammar; the departure is recorded as an annotating D-entry at
  ingestion, before implementation.
- **BC4.** M118's own final `## Decisions` section contains only dated
  decision entries; the AC3 ledger lands in `## Review` as that criterion's
  evidence or as a committed file, never in `## Decisions`. The T3 text is
  amended via gate to match. Evidence: the file at review, and the advisory
  of BC3 reporting no WARN on M118 itself.
