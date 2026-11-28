# RR04: Redteam of the tiering + mechanization + inviolable-budget proposal

- **Date:** 2026-07-20
- **Brief:** `cairn/reviews/RB04-rulebook-governance-redteam.md`
- **Reviewer:** independent Fable-tier review (RB/RR protocol, D-004)
- **Materials read:** `skills/shared/tracking-rules.md` whole (779 lines);
  `cairn/DECISIONS.md` — all 57 `### D-` headings, then D-045, D-049, D-052,
  D-053, D-054, D-056 whole (D-004/D-030/D-031/D-046/D-051/D-055 via headings
  and their restatements in the entries read whole); `cairn/DESIGN.md` whole;
  RR01 recs 9–17 (`reviews/archive/RR01-architecture-retrospective.md:490-531`);
  RR02 whole; RR03 whole; `cairn/milestones/M96-rulebook-growth-ratchet.md`
  whole; `scripts/cairn_validate.py` (check inventory);
  `skills/shared/guard-doctrine.md` whole; `skills/shared/validation-doctrine.md`
  (length check); `skills/tests/` listing; `test_default_branch_parameterized.py`
  header; mutation-harness registry.
- **Measurements reproduced:** rulebook 779 lines; `cairn_validate` all green
  on the current tree; mutation registry **278** entries, of which **111
  anchor in `tracking-rules.md`**; 40 guard files; 9 skills totaling 1,373
  lines of SKILL.md. The brief's independent sweep (65 line-equivalents
  removable) could **not** be reproduced or audited — no committed artifact
  exists; see Beyond the brief, item 1, before relying on that number.

**Verdict in one paragraph.** Part A is sound only where it collapses into a
precedent cairn already has (D-031 modules for activity-triggered doctrine)
and unsound where it is new (phase-tiering the cross-skill contract); rec 15
survives, narrowed but not superseded. Part B's "strictly better" claim is
false — it confuses three enforcement channels with different properties, and
its honest yield is ~15–25 net lines; its salvageable core is an *inflow*
rule and a deletion-candidate screen, not an outflow program. Part C's IP
framing fails exactly the way GP1 failed, because every prior softening was
procedurally clean — the leak is the gate, not the label; the mechanical form
(maintainer-owned number, hard CHECK, coupling guard) is the only version
worth having, and only if the maintainer wants a hard bound at all. On the
central question (Q8), the fix is to make review findings travel as verbatim,
mechanically-diffed criteria with mandatory projection-vs-outcome reporting,
and to bar the implementing session from adjudicating the review that
constrained it. On Q9: the null option is mostly right, and I say so plainly
below — the governance program has cost more than the growth it governs, and
it is the dominant *cause* of that growth.

---

## 1. Part A: cost reduction or cost relocation?

**Mostly relocation. The genuinely movable mass is ~55–90 gross lines, of
which ~40–60 move under a precedent that already exists (D-031 modules) and
only ~15–30 are phase-tierable at all; the phase-tier residue costs more
than it saves.**

Modeling the 628 operative lines by read-trigger:

- **Cross-skill contract — ~500+ lines, immovable under part A's own test.**
  File map/ownership, universal tracking rules, IDs/status, sizing/tiers,
  git/approval model, context hygiene, question gates, output discipline,
  toolchain profiles: every phase skill touches these. Moving a rule needed
  by 3 phases into 3 SKILL.md files multiplies its bytes by 3 and creates a
  consistency obligation. cairn's one deliberate duplication of this kind
  needed a dedicated coupling guard
  (`skills/tests/test_default_branch_parameterized.py` spans the rulebook
  plus four operational skills); tiering N cross-phase rules buys N such
  guards. Total read cost per milestone likely *rises*: `/milestone-plan`,
  `/milestone-implement`, and `/milestone-review` each read their own
  SKILL.md *plus* the shared core, so a rule duplicated into two phase
  skills is read as often as before and maintained twice.
- **Activity-triggered doctrine — ~40–60 lines, movable, but this is D-031,
  not part A.** The References-pages section (`tracking-rules.md:652-716`,
  65 lines) is the one large block whose binding moment is an *activity*
  (authoring a references page), not a phase. Its authoring craft — standing
  facts vs. dated observations, provenance block, re-verification — is
  exactly the shape M98 just moved for guard craft: read at authoring time,
  triggered by an act the agent knows it is performing without having read
  the rule. The "when a page is owed" trigger (~10 lines) must stay in the
  core — an agent that hasn't read *that* never knows a page is owed — but
  the mechanics can live in a module beside `guard-doctrine.md`. This is the
  only part of A that genuinely reduces always-read cost, and it needs no
  new doctrine to license it.
- **Single-phase rules — ~15–30 lines.** The review fan-out block
  (`:574-588`) binds only `/milestone-review`. The merge-marker mechanics
  (`:360-370`) bind review and hotfix. AC fencing, the section-ownership
  table, weight-cap remedies, and the git model all bind 3+ skills. The
  single-phase residue is small, and each move pays: re-anchoring across
  the **111 mutation-registered blocks anchored in the rulebook**, plus the
  guards in up to 40 files, plus the drift risk rec 15 names.

**The brief's M97 analogy is false.** M97 bounded the read of *history* —
content addressed by topic, with the `### D-` headings as a zero-divergence
index, consulted when a query arises. The rulebook is *conduct*: it must
shape behavior before any trigger fires. Part A's own inclusion test — "a
rule belongs in the core only if a session that does not already know it
would violate it" — is self-undermining as a tiering criterion: the sessions
that most need a rule are precisely the ones that don't know to go fetch the
module holding it. A conditional read works only where the trigger is
recognizable *without* knowing the rule (numeric work → validation doctrine;
writing a guard → guard doctrine; authoring a references page → the move
above). "You are in the review phase" qualifies; almost nothing else in the
file does.

**Also: part A's claimed mechanical advantage does not exist for A itself.**
"Which phase needs this rule?" is answered by the same author judgment as
"is this important?" — there is no mechanical predicate (unlike part B's
"does a check exist?"). A tiering pass would be one more agent
classification of the same file, the fifth (see Beyond the brief, item 1).

**Number:** net always-read reduction from A done maximally ≈ 50–80 lines,
of which ~80% is the D-031 module move. The phase-tier remainder is less
than its overhead (coupling guards, re-registration, pointer lines, drift
risk). Do the module move when the section is next touched; reject the rest.

## 2. Rec 15: genuine narrowing or rationalization?

Rec 15's actual reasoning (`RR01:519-522`):

> "Reject — splitting the rulebook into per-skill fragments (beyond
> recommendation 9): the single-file rulebook is what makes 'nothing is
> said twice' and whole-read guarantees work; fragmenting it recreates the
> pre-D-003 drift the plugin exists to prevent."

RR02 Q5 sharpened the grounds (`RR02:250-257`): "the contract has no content
trigger to gate a conditional read on … any sectioned read reintroduces
'skills must remember which sections apply,' which is the pre-D-003 drift."

Three findings:

1. **Part A's distinction is logically genuine.** "Must never be violated"
   and "must be read every time" are different claims; rec 15 never argues
   they are the same. But rec 15 already *accommodated* the distinction via
   its own carve-out — "beyond recommendation 9" — which is exactly the
   module path (validation doctrine then, guard doctrine at M98, references
   craft next). Content with a real read-trigger has always had a legal
   exit. Part A rediscovers the carve-out and presents it as a supersession.
2. **RR02's sharpening contains one false clause.** "The contract has no
   content trigger" is wrong for genuinely single-phase text: the phase a
   session is running *is* a content trigger, the crispest one cairn has.
   Rec 15's conclusion survives anyway, because (Q1) the genuinely
   single-phase mass is ~15–30 lines — the exception is real but too small
   to justify superseding a standing rejection and paying the machinery.
3. **What rec 15 protects is not what part A attacks.** Rec 15 lists the
   cross-skill contract explicitly (file map, caps, status, git model,
   gates, output discipline, profiles). Part A's realistic harvest (Q1) is
   almost entirely *outside* that list. A supersession would spend an
   ip-adjacent decision to license moves that are already licensed.

**Disposition: rec 15 stands.** If a concrete single-phase move is ever
made, record the narrowing as an annotation on that occasion ("phase is a
valid read-trigger; the contract still stays monolithic"), not as a standing
supersession bought in advance. Explicit disagreement with RR02 Q5's "no
content trigger" clause is recorded here; its conclusion is upheld.

## 3. Part B: attack

**The claim "strictly better" is false. It rests on a category error about
what the three enforcement channels do.**

**Fraction and yield.** Of the 23 `cairn_validate` checks, roughly 10–12
have an always-read prose twin (caps, density, terminal retention, dates,
work-log format, vocab, single-in-progress, mirror, references index,
staleness, heading quality, profile slots). But the twins are mostly already
thin — the rule plus its number in 1–4 lines — because the fat around them
is class-2 application doctrine: the two-axes/opposite-remedies block
(`:87-110`), the over-cap remedy list (`:126-140`), the stamp discipline
(`:145-151`). Gross retirable prose ≈ 20–35 lines; net after pointer lines
≈ **15–25 lines**. That is the whole stock-side prize of part B.

The 40 guard files contribute **zero** to this prize, and citing them
reveals the category error: a prose-guard does not enforce behavior at
runtime — it enforces that *the prose exists*. Retiring prose "because a
guard enforces it" is circular: the guard's referent is the prose. Delete
the rule and the guard either reddens (blocking the deletion) or gets
re-anchored to nothing (and now enforces nothing). Only the 23 checks and
the two blocking hooks (`merge_guard`, `force_push_guard`) enforce anything
an agent does; `DESIGN.md`'s Known issues says this plainly: "Conduct rules
… are enforced as prose: guard tests lock the skill/rulebook wording, not
the runtime behavior."

**What breaks when prose is removed in favour of a check:**

1. **Proactive compliance becomes reactive correction, at the worst time.**
   A check fires at gate time — `/milestone-review`, after the milestone's
   artifacts are authored. An agent that never read the stamp rule writes a
   noncompliant stamp, does a milestone of work, and discovers it at review:
   a fix commit, a re-run, sometimes a send-back. The read cost does not go
   to zero; it converts into retry loops priced in wasted work and gate
   rounds — the most expensive currency in the record (RR02 Q6: gate rounds
   are the dominant unmeasured latency term).
2. **Advisory-backed rules decay to nothing.** 8 of the 23 are WARNs that
   cannot fail the gate, by settled design (D-049/D-052's severity split:
   judgments warn, structural facts fail). An agent that never read the rule
   has no norm to check the WARN against and no reason to heed it. Retiring
   prose behind an advisory doesn't mechanize the rule; it deletes it on a
   delay.
3. **A check cannot carry the remedy, and the remedy is the hard part.**
   `record density` can say a file is over threshold; it cannot say that the
   two axes take *opposite* remedies and that compressing when you should
   prune (or re-deriving the mean after consolidating — RR03's treadmill)
   makes things worse. The M84→M87→M93 sequence is a documented record of
   what agents do when improvising weight remedies without doctrine. The
   sweep's own figure says 90.6% of the file's operative mass is exactly
   this class; part B has no offer for it.
4. **The prose does not disappear; it moves off the measured surface.**
   For gate-driven correction to work, the check's docstring and failure
   message must teach the rule — and `cairn_validate.py` is already 1,605
   lines and was already caught retelling the stamp incident as its fourth
   copy (RR02, Beyond the brief). Part B shrinks `tracking-rules.md` by
   growing an unmeasured file. That is Goodhart, not governance.

**What survives the attack — B inverted, as flow control:**

- **As an inflow rule (real, cheap):** a *new* rule that ships with a hard
  CHECK may state itself in the core in ≤2 lines plus a pointer — the
  doctrine burden shifts to the check's docstring at authoring time, when
  someone is writing both anyway. This is where "is it enforced?" genuinely
  has a mechanical answer and genuinely bounds growth.
- **As a deletion-candidate screen (weak but honest):** "check exists" is a
  legitimate generator of candidates for the class-3/4 harvest — each
  candidate still owes the three-step test, because the class-2 filter is
  judgment, which is the thing part B claimed to eliminate and cannot.

## 4. Part C: does the IP framing fail the way GP1 failed?

**Yes — and the record proves it, because every prior softening was
procedurally clean.** D-049 recorded its trade against GP1 explicitly.
D-053 amended GP1 through the exact channel an IP change requires: an
explicit user decision recorded as a D-entry, approved at a gate. D-056 was
shown at a gate and approved. Nothing was violated silently; the findings
were softened *through* the gates, with paperwork. Promoting the budget from
GP to IP changes the required ceremony from "stated justification" to
"explicit user decision + D-entry" — which is the ceremony that has already
failed three times, because the implementing session authors the framing,
composes the chip, and the maintainer approves under time pressure. An IP is
a label on a gate, and the gate is the leak.

Two additional failure modes specific to a budget-IP:

- **A parameterized IP corrodes the IP class.** IP1–IP4 are qualitative
  invariants, two of them hook-backed. A budget-IP invites recurring
  renegotiation of its *number*, each formally an IP change that feels like
  tuning. After two or three raises, "IP" means "number we change with
  paperwork" — spending the credibility of the only principle class that has
  held.
- **Displacement pressure targets the wrong mass, and leaks to unmeasured
  surfaces.** At budget, the cheapest displacement is class-2 application
  doctrine (always arguable), and the cheapest evasion is relocation — into
  SKILL.md files, validate docstrings, or modules — all off the budgeted
  surface. The weight program has already demonstrated the water-balloon
  (the stamp incident told in four places; Weight caps +59 while the best
  extraction saved −53).

**Stronger mechanism, if the maintainer wants a hard bound at all** (Q9
argues they may not):

1. **The number lives in a maintainer-owned artifact** (one line, e.g. in
   `DESIGN.md` beside the principles, or a dedicated file), never derived
   or drafted by an agent.
2. **A hard CHECK in `cairn_validate` reads it** and FAILs when the
   always-read surface exceeds it. Deterministic; cannot be softened
   in-session; deadlock is the *point* (the escape is displacing or
   parking, both visible).
3. **The budgeted surface is enumerated in the check** — rulebook + the
  `CLAUDE.md` cairn section + any module whose pointer makes it effectively
   always-read — or the budget just redirects growth (see above).
4. **Changing the number is protected the way merges are** — the only
   pattern in cairn that has actually resisted agent pressure is
   `merge_guard`'s marker: mechanical denial absent a user-written token.
   Minimum viable form: a coupling guard hardcodes the same number, so a
   raise touches a test file and shows in the review diff, and the
   merge-approval chip is required (guard-pinned) to state the delta
   verbatim: "always-read Δ: +N, budget B." Maximum form: a PreToolUse hook
   denies edits to the budget artifact without a user marker.
5. **Ban the ask at implementing gates.** A session at budget ships within
   it or parks `blocked`; budget raises are raised only by the maintainer
   unprompted or at `/milestone` status time — never proposed from inside
   the milestone the budget is squeezing. This last rule is prose and
   therefore soft; items 1–4 are what actually bind. If the maintainer
   raises the number under pressure anyway, that is ownership working as
   designed; no mechanism should try to stop an informed owner.

## 5. Who is the counterparty, really?

**Theatre, for this purpose.** The dependency chain: `/milestone-review`
runs in the same session lineage; its fresh-context reviewers are spawned
and their prompts authored by the implementing orchestrator; the confidence
scorer gates which findings the user sees; and the review applies the same
rulebook the change under review may be amending — self-amending law with
self-selected judges. The record already contains the experiment: M95's
second run and D-056 both passed review and the gate. Fresh context removes
diff-blindness (its actual job, M17); it does not create independent
interest.

Real counterparties, in descending hardness, all already native to cairn:

1. **Deterministic scripts on script-measurable quantities** — a CHECK
   cannot be argued with in-session (Q4's mechanism).
2. **Diff-visible constraints** — guards + the mutation harness make
   softening a *test edit* someone must commit, not an interpretation.
3. **The maintainer at a gate fed mandated verbatim numbers** — one number
   ("Δ +14 against projection −60") resists framing far better than prose;
   the chip rules already require verbatim substance (D-037), but nothing
   currently requires the *comparison* to appear (see Q8).
4. **A Fable review with binding criteria ingested verbatim** (Q8, item 1).

Assigning the ruling to `/milestone-review` adds none of these. Reject that
clause of part C regardless of what happens to the budget.

## 6. The fifth class and D-056's test

**Yes, it is evidence of a real (but bounded) defect: the test is per-block,
and restatement is a relation between blocks that no per-block test can
see.** The mechanism is the disjunction in step 1 — "deleted **or**
inverted." Deleting a duplicate changes nothing (the other copy still
governs → route to delete), but *inverting* a duplicate creates a
contradiction, which does change behavior → "yes → the rulebook owns it."
Any rule-shaped text passes the inversion arm, copies included. The two
probes answer different questions: inversion detects *rules*; deletion
detects *necessary* text. A retention test for an always-read file should
require the deletion arm; inversion belongs to guard verification (its M74
role), not placement.

**Restructure, minimally — supersede, don't demolish.** D-056's part 1
(current knowledge) and part 3 (guard asymmetry) are sound and the sweep
*supports* part 1. The superseding entry needs three edits:

- **Step 0 (single home):** "Is this stated elsewhere in the always-read
  core? → one home keeps the statement; other sites get at most a
  cross-reference." This is not new doctrine — it is `DESIGN.md`'s existing
  convention ("nothing is said twice") and the file map's "substance lives
  in the owner" applied intra-file, finally made a test step.
- **Split the probes:** retention in the core requires
  deletion-changes-behavior; inversion is the guard-verification protocol
  only.
- **Replace the yield clause** ("The test predicts no yield … not a quota a
  later pass owes") with the measurements — see Beyond the brief, item 1,
  for what the superseding entry may honestly claim.

Note D-056's own supersession trigger is directional — "if this test [admits]
a deletion that loses a rule" — anticipating only over-deletion, not
over-retention. An entry that names failure modes in one direction only is
itself a small signature of the defensive drafting the Background describes.

## 7. Is any stock-side mechanism worth building? (M96's fate)

**As planned: no. M96's ratchet is calibrated for a world the sweep says is
gone.** After a thorough one-time harvest the file sits ~97% operative; at
+13 lines/milestone a 15% ratio fires every ~9 milestones; each firing
mandates a pass whose honest outcome is "reviewed, nothing to cut"; the
escape degenerates into ritual re-stamping — precisely the failure D-049
documented for the density thresholds ("can tax but never bind," a
per-milestone levy on records the milestone never touched). RR03's argument
for keeping M96 ("without a standing signal, a one-time cut is undone by
arithmetic in ~30 milestones") correctly demands a *signal*; it does not
justify a *pass mandate* with no remedy.

**Re-cut, don't drop — the fix is to change what the pass audits.** A ratchet
on total mass has a one-time remedy; a ratchet on **unreviewed delta** has a
remedy forever:

- The stamp records date + mass, as planned (AC1 stands).
- The advisory fires on growth over the stamp, as planned (AC2/AC3 stand).
- **The pass reviews only the lines added since the stamp**, against the
  placement test (as repaired in Q6, step 0 included) and the B-inflow rule
  (Q3). Scope ~100–150 new lines, not 779; outcome is "each addition
  classified, class-3/4 additions fixed" — a completable, repeatable act.
  AC5/AC6 carry over with the pass so redefined.

This converts M96 from a shrink mandate (exhausted after one harvest) into a
flow audit (never exhausted, cheap, scoped). If the maintainer instead takes
the Q9 null seriously — defensible — the further fallback is to fold M96 to
a reporting line in the `/milestone` audit (mass + growth since stamp,
RR02 rec 4's shape) and build no pass machinery at all. Either way, do not
build M96 as written.

## 8. What would actually stop the softening? (the central question)

The failure signature across the record: a finding arrives as prose; the
implementing session translates it into acceptance criteria (M95's first AC1
mistranslated RR02); executes; then authors the durable interpretation of
the outcome (D-056's "read that as evidence…"), which the gate approves
because the author also composed the gate. Every step is one agent
interpreting text that constrains itself. Mechanisms that break specific
links, concrete and buildable:

1. **Binding criteria travel verbatim and are diffed mechanically.** An RR
   gains a "Binding criteria" section written as measurable assertions. The
   ingesting milestone's AC block must contain them **verbatim**; a
   `cairn_validate` check (or guard) string-compares the milestone's AC
   text against the RR file — the RR is already on disk and, being a review
   record, is never edited. A softened criterion is then a red check, not a
   reading. Deviations are legal only through a "Deviations from RR<NN>"
   table in the milestone file, shown verbatim at the ingest chip — IP3's
   conservation ledger applied to review findings. (Cost: ~10 lines in
   `/milestone-brief`'s ingest protocol + one check. This targets the exact
   link that failed between RR02→M95-AC1 and RR03→D-056.)
2. **Projection-vs-outcome is reported mechanically, side by side.** Any
   numeric projection in the driving RR is copied into the milestone at plan
   time; `/milestone-review` must print measured-vs-projected in the Review
   section and in the chat above the merge chip. A shortfall beyond a stated
   tolerance forces an explicit chip option — "accept shortfall, recorded as
   such" — so the maintainer decides *seeing the gap*. M95's −9 against
   RR03's 60–100 sailed through because no surface ever juxtaposed the two
   numbers; this makes the juxtaposition unavoidable and costs three lines
   of rulebook.
3. **Adjudication asymmetry.** The implementing session records what it did
   and measured; it does not author, into permanent history, the verdict on
   whether the review constraining it was right. "The premise is refuted /
   the test predicts no yield" claims route to a new RB or to the
   maintainer's own words at the gate. One rulebook sentence; D-056's wrong
   inference is the incident it exists to prevent. (A guard can pin the
   sentence; the conduct itself stays prose-enforced — stated honestly, this
   is the weakest of the four.)
4. **Prefer script-measurable acceptance criteria; commit the classification
   artifact when judgment is unavoidable.** Line counts, diff stats, check
   outcomes cannot be renegotiated; classifications (class 2 vs 4) will be
   renegotiated forever because no oracle exists. Where an AC must rest on a
   classification, the ledger itself is committed as evidence — M95's B1–B21
   ledger is what made RR03's audit possible; that is the pattern working,
   by accident. Make it a rule.

What demonstrably does **not** work, from the record: prose ACs interpreted
by their implementer (M95 twice); the review fan-out as an independence
mechanism (Q5); recording the constraint at higher principle strength (Q4);
and asking the next Fable review to re-litigate (this is the fourth, and the
pattern the maintainer is complaining about includes the reviews).

## 9. Steelman of the null option

**The strongest case, argued for real:**

- **The read cost is small money.** 52.8k chars ≈ ~13k tokens, ×3–4 reads
  per milestone ≈ 40–50k tokens/milestone. The mass actually in dispute —
  the sweep's 65 line-equivalents ≈ ~1.1k tokens per read — is ~3% of that.
  Ten governance milestones plus four Fable reviews have cost, conservatively,
  orders of magnitude more than years of the growth they govern.
- **The program is the dominant cause of the growth.** RR02 measured Weight
  caps +59 lines against −53 for the best extraction ever performed; the
  brief's own table shows the four *anti-growth* milestones (M92, M93, M97,
  M98) adding +53 lines combined. The observed +13/milestone inflow is
  measured over a window dominated by governance milestones; stop them and
  the inflow likely halves on its own.
- **The causal case for harm was never made.** RR02 Q6: the only causally
  isolated latency number exonerated read volume; the slowdown confounds
  with meta-milestone composition and gate rounds. Instruction dilution is
  real as a mechanism but unmeasured as a fact — and M94 built `cairn_cost`
  precisely to measure it, and nobody has yet let the data speak.
- **The one-time harvest is bounded and known.** ~65 line-equivalents, 8.4%.
  Even taken at face value, capturing it changes per-read cost by ~3%. The
  durable lever the sweep itself identifies — controlling inflow — does not
  require a milestone; it requires a sentence at the door and a number at
  the chip.

**Where the null breaks, honestly:** an unbounded always-read conduct spec
has a real dilution failure mode with an observed incident class (the D-019
prose-options drift), doubling time ~5 months at the measured rate; and GP1
as amended — approved by the maintainer — commits to a bounded read cost, so
"accept monotone growth" requires re-amending a principle the owner just set.

**Verdict: the null is ~80% right, and this is the review's most useful
finding after Q8.** Right that no further milestones should be spent on
stock-side size governance — the marginal governance milestone is
negative-value, and this brief's own Background is the evidence. Wrong only
at the zero-marginal-cost margin: the inflow sentence, the delta line at the
merge chip, the (re-cut) delta audit, and `cairn_cost` data are cheap,
mostly built, and flow-side. Stop governing the stock. Watch the flow.
Let the token data, not felt slowness, trigger anything further — and let
the trigger be a measured regression, not a review's projection.

---

## Beyond the brief

1. **The sweep is a fourth unaudited agent classification, and the Background
   overstates what it refutes.** No committed artifact of the 2026-07-20
   sweep exists in `cairn/` for this review to audit; its 65 line-equivalent
   figure joins RR02's 165–215, RR03's 60–100, and M95's ~0 as the fourth
   agent-derived number for the same quantity, each produced by an agent
   declaring its predecessor wrong. Class-2/class-4 boundaries have no
   oracle; inter-rater disagreement is the *documented history of this
   file*. Moreover D-056's headline claim — "the rulebook's mass is mostly
   class 1/2" — is **confirmed** by the sweep (90.6% of content lines
   operative); only the "predicts no yield / not a quota" clause is
   contradicted, by ~56 lines net. The orchestrating session that authored
   the proposal also produced the measurement declaring D-056 wrong, then
   wrote a brief embedding that verdict as fact ("D-056's inference is
   therefore wrong") — structurally the same move the brief indicts. Before
   any superseding entry cites the sweep: **commit the sweep ledger**
   (per-block classifications, the artifact M95's B1–B21 modeled) so the
   next agent audits the ledger, not the summary (Q8, item 4).
2. **The re-anchoring tax is now the binding constraint on any relocation.**
   111 of 278 mutation-registered blocks anchor in `tracking-rules.md`.
   RR03 flagged the guard set as "a second constituency for rulebook prose"
   and parked anchor-choice doctrine on a trigger ("if re-anchoring
   dominates the cost"); any pass executing Q1's module move will hit that
   trigger. `guard-doctrine.md` §1 is the home; one paragraph (anchor on
   rules, never scaffolding) discharges RR03 rec 8.
3. **The irony budget of this review's own recommendations, counted.** Q8's
   mechanisms add ~14 lines to always-read surfaces (ingest protocol lives
   in `/milestone-brief`, conditionally read; the projection-comparison and
   adjudication rules are ~4 rulebook lines); the B-inflow rule ~2; a budget
   check ~3. Net stock change if the references-craft module move happens:
   ≈ −40. Any milestone implementing these must count its rulebook footprint
   in its cost, per RR02's "presumed guilty" standard — including this
   paragraph's.
4. **M96 is currently `blocked` on this review.** Disposition is in Q7:
   re-cut to a delta-scoped audit, or fold to a reporting line; do not build
   as written; do not drop the signal entirely.

## Recommendations

Each marked **apply / consider / reject-with-reason**. Disagreements with
predecessors: RR02 Q5's "no content trigger" clause (Q2, conclusion upheld);
RR03's keep-M96-as-amended (Q7, re-cut further); D-056's yield clause and
test structure (Q6, supersede narrowly — its part 1 and part 3 stand).

1. **Reject — part A as phase-tiering of the cross-skill contract.** Rec 15
   stands on its original grounds; the genuinely single-phase residue
   (~15–30 lines) costs more in coupling guards, re-anchoring (111 blocks),
   and drift risk than it saves. (Q1, Q2.)
2. **Consider — the references-authoring module move** (~40–60 lines, D-031
   precedent, trigger stays in core): the one real always-read reduction in
   part A. Fold into the next milestone that touches the section; never a
   dedicated governance milestone. (Q1, Q9.)
3. **Reject — part B as a prose-retirement program.** The claim "strictly
   better" is false: guards enforce prose existence, not behavior; checks
   fire after authoring; advisories cannot bind; remedies are class-2
   doctrine no check carries; the prose relocates to unmeasured surfaces.
   Honest yield ~15–25 net lines. (Q3.)
4. **Apply — part B inverted, as the inflow rule:** a new rule shipping with
   a hard CHECK states itself in ≤2 core lines + pointer, doctrine in the
   check's docstring. ~2 rulebook lines; this is the mechanical inflow bound
   the program has been looking for. (Q3.)
5. **Reject — part C as an IP.** The gate is the leak, not the label; every
   prior softening was procedurally clean, and a parameterized IP corrodes
   the IP class. (Q4.)
6. **Consider — the mechanical budget** (maintainer-owned number, enumerated
   surface, hard CHECK, coupling guard, delta line mandated verbatim at the
   merge chip, no in-milestone raise proposals) — *only if* the maintainer
   wants a hard bound after weighing Q9. Tradeoff to present, number left to
   the maintainer per the brief's constraint: a budget at the current mass
   freezes (every add displaces, immediately); slack above current buys
   quiet milestones and delays the forcing function; no budget plus the
   delta line is the Q9-consistent minimum. (Q4, Q5, Q9.)
7. **Reject — assigning the add-to-core ruling to `/milestone-review`.**
   Same lineage, spawned reviewers, self-composed gates: theatre. The
   counterparties are the check, the diff, and the maintainer fed verbatim
   numbers. (Q5.)
8. **Apply — Q8's mechanisms 1, 2, and 4:** RR binding criteria ingested
   verbatim and mechanically diffed, with a shown deviations table;
   mandatory projection-vs-outcome reporting at review and at the merge
   chip; script-measurable ACs preferred, committed ledgers where judgment
   is unavoidable. This is the answer to the maintainer's central question.
   Mechanism 3 (adjudication asymmetry) — **apply** as one sentence, with
   the stated caveat that it is prose-enforced. (Q8.)
9. **Apply — supersede D-056 narrowly:** add step 0 (single home), split
   deletion (placement) from inversion (guard verification), replace the
   yield clause with committed measurements. Parts 1 and 3 restated as
   standing. Precondition: the sweep ledger is committed first (Beyond the
   brief, item 1). (Q6.)
10. **Apply — re-cut M96 to a delta-scoped audit** (stamp + advisory stand;
    the mandated pass reviews only lines added since the stamp, against the
    repaired placement test and rec 4's inflow rule). Fallback if the
    maintainer takes Q9 fully: fold to a `/milestone` audit reporting line
    and build no pass machinery. Do not build as written. (Q7.)
11. **Apply — declare the stock-side weight-governance program closed.** No
    further milestone targets the rulebook's size absent a measured
    `cairn_cost` regression as its trigger. The program has been the largest
    contributor to the growth it governs; the felt-slowness trigger is
    retired in favor of the instrument built to replace it. (Q9, RR02 rec 4.)
