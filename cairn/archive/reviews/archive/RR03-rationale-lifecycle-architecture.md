# RR03: The lifecycle of rationale — an architectural audit of accumulation across cairn's always-read files

- **Date:** 2026-07-19
- **Brief:** `cairn/reviews/RB03-rationale-lifecycle-architecture.md`
- **Reviewer:** independent Fable-tier review (RB/RR protocol, D-004)
- **Materials read:** `cairn/milestones/M95-rulebook-editorial-slimming.md`
  whole (the LEDGER B1–B21 entries, `:126-146`, are the primary evidence);
  `skills/shared/tracking-rules.md` whole (765 lines);
  `cairn/LESSONS.md` whole (48 lines); `cairn/DECISIONS.md` — all 52 `### D-`
  headings, then D-015, D-030, D-031, D-032, D-045, D-046, D-049, D-050,
  D-051, D-052 whole; `reviews/archive/RR01-architecture-retrospective.md`
  and `RR02-weight-management-architecture.md` whole; `cairn/DESIGN.md`
  (IP/GP block, `:78-104`); `cairn/ROADMAP.md` (Candidates, `:24-43`);
  `cairn/milestones/M96-rulebook-growth-ratchet.md` and
  `M97-bounded-decisions-read.md` whole.
- **Measurements reproduced** (char_count = Python `len()`, characters not
  bytes): `tracking-rules.md` 765 lines / 52,316 chars; `DECISIONS.md`
  1,425 / 95,374 (52 entries; heading lines 5,326 chars, 5,378 with
  newlines — RR02's figure confirmed); `LESSONS.md` 48 / 20,484 (31 items,
  mean **631** chars, max 1,037, 18 items over 500 chars, 13 of 31 carrying
  extension/consolidation markers); `ROADMAP.md` 43 / 14,875.
  `cairn_validate` all green on the current tree.
- **Spot-verified guard-pinning claims:** B9 (`test_lessons_loop.py:163-218`
  pins each clause of the retirement rule, one assert per clause) and B17
  (`test_source_note_template.py:75-119` pins the standing-fact and
  dated-observation definitions per physical line; zero hits for
  "standing fact"/"dated observation" in `DECISIONS.md`). Both ledger
  entries check out as written.

---

## 1. Where should rationale live?

**Neither verdict as posed. The 9 no-home blocks are not one class, and the
question "defect or correct?" dissolves once the rulebook's own file-class is
named.** M95's ledger is the evidence: the material RR02 called "rationale"
is at least four distinct kinds of text, and they have different owners.

1. **Rules** — operative directives ("the stamp is replaced each pass,
   never appended to", `tracking-rules.md:154`). Rulebook, obviously.
2. **Application doctrine** — text that changes how a compliant agent
   *applies* a rule: the discriminating-word clause of retirement
   (`tracking-rules.md:189-191`), "measure that mean, never assume one"
   (`:99`), the entire standing-facts-vs-dated-observations block
   (`:686-697`, ledger B17). This is operative. An agent stripped of B17
   goes back to writing undated absence claims — the exact failure the
   block names. It is rule-like in every way that matters, and the guards
   pinning it are not accidents.
3. **Decision records** — legislative history: what was considered, what
   was rejected, measured values at decision time, the incident that forced
   the choice. `DECISIONS.md` (or a milestone file's local `## Decisions`)
   owns this; the rulebook gets a parenthetical cite. This is the class
   RR02 correctly diagnosed — and M95 measured it at ~35-40 lines (~5%),
   not 22-28%.
4. **Free-floating justification** — "and this is right because…"
   argumentation that neither changes application nor records a choice:
   D-050's "extends the same authority upstream" tail (`:220-221`, ledger
   B10), the provenance-block justification (`:704-712`, B18), the
   "density warns because…" sentence (`:107-109`, B3).

The 9 no-home blocks split across classes 2 and 4. B17, B3's severity
reasoning, B12's "ahead N, behind 1" failure-mode description (`:340-344` —
it teaches an agent to *recognize* the divergence it prevents) are class 2:
**correct** — the rulebook is their proper sole home, and authoring D-entries
for them would be a defect, not a repair. B1, B18, B19's "weaker consent"
argument are class 3/4 orphans: motivating facts and defenses that were never
decisions. For those the honest question is not "where is their home?" but
"do they need one?" — and the answer is no, because of the point the whole
system has been circling:

**The rulebook is current knowledge under D-045's split, and nobody ever said
so.** D-045 (`DECISIONS.md:1066-1071`) enumerates history (DECISIONS,
work-logs, IDs, archives, legacy) and current knowledge (LESSONS,
references/, DESIGN, and per D-052 ROADMAP) — but the class list covers
tracking files only. `tracking-rules.md` is plugin logic, edited in place at
every milestone that touches it, guarded by tests rather than by IP4, with
git holding every prior state. It meets every term of the current-knowledge
definition and none of history's. D-052 already ran this exact argument for
the hygiene stamp: "not an IP4 history edit — `git log` holds every earlier
stamp verbatim" (`DECISIONS.md:1409-1410`). The same reasoning licenses
deleting class-4 justification from the rulebook **against git, with no
backfill** — deleting a defense is not deleting history, because a defense
that never recorded a choice was never history.

This is where M95's AC1 went wrong, and its ledger says so itself: B15
(`M95:140`) — "AC1 as written forbids the milestone's cleanest win." AC1
conflated *preserved somewhere* with *recorded as a decision*. The stop was
correct given the AC; the AC was the defect.

**The decision procedure** (authoring time and editing time, same test):

1. **Inversion test:** if this text were deleted or inverted, would a
   compliant agent's behavior change — misapply a rule, miss a failure
   mode, make a judgment the text forecloses? **Yes → rulebook** (class
   1/2). A D-entry may also exist if a choice was made, but the rulebook
   text is not a restatement of it and is never "slimmed back" to it.
2. **Decision test:** does it record a choice among alternatives made at a
   point in time — rejected options, decision-time measurements, the
   forcing incident? **Yes → the D-entry (or milestone-local decision)
   owns it**; the rulebook keeps the rule plus a cite. If no record exists
   and the choice is cross-cutting, *that* is the defect — author the
   D-entry when the choice is next touched, not as a backfill sweep.
3. **Neither → it is justification. Default delete** (or compress to a
   clause). Justification that serves a future *editor* ("don't
   re-litigate") belongs in the D-entry when one exists; justification
   that serves the acting *agent* is class 2 by definition and stays.

Applied to the 9: B17, B3 (its operative half), B12, B19's pinned label —
stay, no D-entry owed. B1, B18, B10's tail, B19's unpinned argumentation,
B14's parenthetical — deletable under step 3 with no backfill. B15's
enumeration — removable on redundancy grounds (RR01 rec 7), which the new
AC1 must permit. The "author the missing D-entries, then slim" remedy the
M95 work log names (`M95:148`) is the maximalist reading and I recommend
against it — see rec 9.

## 2. Is "guard-pinned ⇒ rule" a sound test?

**Sound in the direction M95 used it; unsound as a biconditional; and it
subtly inverts the ownership relation if promoted as-is.**

As a *deletion screen* it is conservative and correct: a block whose removal
reddens the suite is prima facie load-bearing, and M95 was right to stop on
it. The two failure directions the brief worries about are both real:

- **Unpinned ⇏ not-a-rule.** Registration is per file, not per assertion —
  `LESSONS.md:20` and the rulebook (`tracking-rules.md:746-749`) both say
  so — and B18 is live proof of operative-looking prose with no pin. M95
  handled this correctly by requiring D-entry evidence *in addition*, never
  treating unpinned as deletable.
- **Pinned ⇏ rule.** Guards were authored ad hoc across ~40 milestones;
  mutation-harness anchors are chosen as *exemplar blocks per file*, i.e.,
  partly for matchability, not because each anchored sentence is doctrine.
  A guard can pin scaffolding.

But the deeper unsoundness is this: **the test treats the guard as owning
the text, when the text owns the guard.** Guards are editable — M95's own
AC3 machinery exists precisely to re-anchor them — so "pinned" can never
mean "immovable," only "moving it costs a re-anchor." A pinned block that
fails the Q1 inversion test at the *behavioral* level (the guard reddens on
deletion, but no agent behavior depends on the prose) is shortenable with a
re-anchor. M95 read pinned as frozen, which is over-conservative; frozen
anchors are how a rulebook's editability dies one guard at a time.

**Replacement, and promotion:** promote the *behavioral inversion test* —
"a rule is what changes compliant behavior when deleted or inverted" — as
doctrine, with guard-reddening as its mechanical proof procedure where a
guard exists (M74's relabel/negate/transpose protocol,
`tracking-rules.md` AC2 form) and a recorded by-hand inversion where none
does. Two sentences in "What gets a test" or the ownership preamble. Do
**not** promote "guard-pinned ⇒ keep verbatim." The asymmetry to preserve:
guard-reddening is *sufficient* to block a careless deletion, *never
necessary* to justify one, and *never sufficient* to keep prose that fails
the behavioral test.

## 3. Is compression a remedy or a deferral?

**Against redundancy, a remedy. Against distinct content, a deferral by
construction — consolidation conserves mass while relaxing the item axis,
which is exactly the trajectory `LESSONS.md` exhibits.** Merging two
lessons deletes a date stamp and a conjunction; the content survives, so
the mean rises and the weight stays. The file's own markers narrate it:
`(M53, extended M54, trimmed M92)` (`LESSONS.md:20`), `(M56+M65,
consolidated M78/M83)` (`:21`), `(M58+M59+M64+M65, consolidated
M78/M82/M90, trimmed M92)` (`:24`) — 13 of 31 items carry such markers, 18
of 31 exceed 500 chars, and the file has grown net (20,466 → 20,484) since
M92 gave it retirement. The item axis is green because items merge; the
mass grows because merging preserves content. D-049 states the mechanism
(`DECISIONS.md:1232-1234`) and this review confirms it is not merely a
calibration nuisance but a **treadmill**: re-deriving the threshold today
at the measured mean gives 876 + 32 × 631 ≈ 21,067 → 21,500 — the
prescribed remedy raises the mean, the mean raises the re-derived
threshold, and the weight axis can never bind long-term. It can only tax
each hygiene pass on the way up. (This also means: do not re-measure D-049's
mean after a consolidation pass and call the raised threshold a fix.)

**What is the correct outflow?** Read what the file actually holds. By my
classification, 18 of 31 items — 12,232 of 19,560 item-chars, **63% of the
item mass** — are one coherent subject: how to author prose-guards,
fixtures, matchers, and validators that actually falsify what they claim to
(`LESSONS.md:20,22,24,26,27,28,33,35,36,38,40,41,42,43,45,46,47,48`).
These are no longer "build quirks and gotchas" (D-015's charter,
`DECISIONS.md:190-191`). They are **matured doctrine**: consolidated three
and four times, stable in content, extended only with new instances of the
same principles. They fail both D-051 criteria *forever by construction* —
no test fails on the mistake (they teach the judgment guards cannot make:
"The harness catches neither", `LESSONS.md:33`) and no tracking-file slot
owns guard-authoring craft, because none exists. D-051's two criteria cover
*enforcement* and *duplication*; they have no exit for *maturation*, and a
file whose only moves are merge-in-place will saturate its weight axis with
its most valuable content. That is what 16 chars of headroom is.

**So: D-051 is necessary but insufficient. Add a third outflow —
graduation to doctrine.** When a lesson family has stabilized (consolidated
repeatedly, teaching principles rather than incidents), the retiring
milestone distills it into a doctrine home and the lessons leave whole.
RR01 already said this in Q8: "When the same lesson class hits three
entries, that's the tripwire for converting it into mechanism" — it was
stated for *mechanism* (harness, check) and never extended to *doctrine*,
which is what these lessons are, mechanism having already been built
(the harness exists; the lessons teach how to use it honestly). Two
precedented homes, no new tracking file:

- **A module: `skills/shared/guard-doctrine.md`** — D-031's exact shape
  ("new domain doctrine gets a module, not a rulebook section",
  `DECISIONS.md:635-638`). The domain condition is "authoring or editing a
  prose-guard/validator," referenced from "What gets a test" in one line;
  conditionally read, so it adds nothing to the always-read core. This is
  my recommendation: the lessons bind at guard-authoring time, which is
  when a module's trigger fires, whereas LESSONS is surfaced at plan time
  — the wrong moment for craft this specific.
- **A synthesis note** under `cairn/references/` — "an analysis that will
  outlive its milestone" (`tracking-rules.md:674-675`) — if the maintainer
  prefers repo-local to plugin-shipped. Weaker: nothing triggers its read.

Against D-029/D-015 as the brief requires: this is doctrine prose, not a
record registry, so D-029's shape-free-content preference is inapposite
(and D-031 post-dates and licenses the module form); the D-015
four-wiring-points cost applies to new *tracking* files — a module wires
once (a pointer beside the existing validation-doctrine pointer).
D-051's ownership criterion already permits the *move* ("the retiring
milestone may move the content there", `DECISIONS.md:1329-1330`); an
annotating D-entry should still name maturation as a distinct third
criterion, because "another tracking file's slot" reads too narrow to
cover a module without it.

Discharge: retiring the graduated family frees ~12k of 20,484 chars — the
file returns to being what D-015 chartered, with real headroom on both
axes, and the same play is available to the adopting repos where the
maintainer reports the identical pattern.

## 4. Can rationale have an IP4-compatible lifecycle?

**Yes, and most of it already exists unassembled.** Stated as a lifecycle:

- **Born:** in the milestone — work-log lines and milestone-local
  `## Decisions` (history, cheap, cap-exempt under D-046).
- **Promoted:** to a D-entry only when cross-cutting — a *choice among
  alternatives* (the file map's own boundary, `tracking-rules.md:22`).
- **Cited:** from the rulebook in one line; the rulebook carries only
  class-1/2 text (Q1).
- **Read:** DECISIONS boundedly (headings → matched entries whole — M97),
  never whole-file.
- **Superseded:** by new entries, never edited — IP4 untouched.
- **Observed:** provisional lessons live in LESSONS until they die
  (enforcement), move (ownership), or mature into doctrine (Q3).

Each option the brief names, against IP4's letter and intent:

- **Bounded/tiered read (M97): compatible with both, fully.** Nothing on
  disk changes. This is the correct primary governor for a file whose
  growth is structural: the mass is legitimate; the whole-read was the
  defect (RR02 Q4/Q5, upheld — one of the parts of RR02 that M95's
  evidence does not touch).
- **Supersession-aware read: compatible; a refinement of M97, not a rival.**
  15 of 52 headings already name what they supersede/annotate/narrow; the
  heading-quality rule M97 AC3 adds makes this reliable. A scan that
  deprioritizes (never skips) entries another heading names as superseded
  is a read-protocol detail — worth two sentences inside M97, not a
  mechanism.
- **Archival-with-tombstone: against the letter as written, arguably
  within the intent, correctly parked.** IP4 says "append-only … DECISIONS"
  (`DESIGN.md:91-93`); replacing an entry body with a tombstone edits the
  file even though nothing is fabricated or renumbered. RR02's
  "IP4-adjacent, needs its own D-entry" is right, and post-M97 it buys
  almost nothing (the heading scan grows ~100 chars/decision — decades of
  headroom). Keep the candidate row (`ROADMAP.md:31`) parked on its stated
  trigger.
- **Is IP4 the wrong constraint? No — and I say so having looked for the
  case.** Accumulation in DECISIONS is structural, not a hygiene failure,
  exactly as the brief frames it; but the cost of that accumulation is
  entirely a read cost, and the read is boundable without touching the
  principle. Meanwhile IP4 is what made RR01, RR02, M95's ledger, and this
  review possible — the supersession chains are the audit trail. No
  superseding D-entry is warranted. The one boundary clarification needed
  is on the *other* side: the rulebook is not in IP4's set and is current
  knowledge (Q1) — stating that is a D-045 annotation, not an IP4 change.

## 5. One lifecycle or three?

**Three fitted mechanisms, one shared frame — and the frame already exists:
D-045.** Arguing the trade honestly:

*For unification:* the three files exhibit the same failure shape (inflow
without outflow; the governing mechanism feeding the growth), and three
independently-derived mechanisms invite three independent blind spots —
M84→M87→M93→M94 is what per-file derivation costs.

*Against:* the files have genuinely different type signatures.
`DECISIONS.md` is **history**: immutable, monotonic, correctly governed by
bounding the read. `LESSONS.md` is **provisional current knowledge**:
item-structured, correctly capped, needing outflows (die / move / mature).
`tracking-rules.md` is **operative current knowledge**: prose, whole-read
mandatory (rec 15, upheld), where the governed quantity can only be
*editorial attention* because no level is derivable (RR02 Q3, upheld). A
lifecycle model general enough to cover all three — "content enters, is
governed, leaves per-file" — constrains nothing; a specific one fits at
most one file. A unified model that fits none would be worse than three
fitted ones, and that is the model any unification would produce.

The real common substrate is smaller and worth stating as one paragraph of
doctrine, not mechanism: **every always-read file names its three elements
— an inflow test (what belongs here), an outflow or read-bound (how content
leaves, or how the read stops growing), and an attention signal (what
reports growth)** — with the history/current-knowledge split (D-045)
deciding which outflows are legal. Under that audit frame the actual defect
is visible in one row: DECISIONS has inflow-test + outflow (supersession) +
signal-not-needed-once-read-bounded; LESSONS has all three (after Q3's
third outflow); **the rulebook had none of the three** — no inflow test
(anything a milestone writes), no outflow (nothing until M95/M96), no
signal (nothing until M94/M96). The rulebook having no governance was the
defect; per-file governance was not.

## 6. GP1 is false as stated

**Amend — do not retire, and "correct the practice to meet it" is
impossible for one of the three files.** GP1's intent (bounded always-read
cost) is real and load-bearing: it drives the caps that demonstrably work
(ROADMAP, milestone bodies, archives). But its stated *mechanism* — "caps +
archiving keep always-read files small" (`DESIGN.md:94-95`) — cannot be
made true of `DECISIONS.md` under IP4 (no cap or archive is legal), was
never applied to the rulebook (no cap on either axis), and D-049 already
recorded a formal trade against GP1 (`DECISIONS.md:1246-1248`). A
principle whose mechanism is impossible for the largest file in its scope
will keep generating milestones that chase the wrong quantity — nine of
them so far.

Retiring it would be worse: the item caps and archive discipline it
licenses are the parts of weight governance that settled on first shipping
(RR02 Q2's own finding). Amend the wording so the goal is the read cost and
the mechanism is per file-class. Proposed text (a user decision recorded as
a D-entry; the number GP1 is kept, per the never-renumber rule):

> GP1: Efficient — store decisions and outcomes, not minutiae; every
> always-read surface keeps a bounded read cost: caps with outflows bound
> the item-listed files, recorded editorial passes bound the rulebook, and
> history is bounded by reading less of it, never by shrinking it.

## 7. What should M95, M96, and M97 become?

**Keep all three; re-cut one; add one. Order: M97 → M98 (new) → M95′ → M96.**

- **M97 — keep as-is, run first.** Its premise (DECISIONS is large,
  append-only, and swept whole) is untouched by M95's findings; it is the
  single largest read reduction available (~90% of a 95k sweep); it has no
  dependencies; and it changes the economics of everything else — once
  DECISIONS is read-bounded, the marginal cost of a new D-entry stops
  being an always-read cost, which is what makes Q1's "author a D-entry
  only when a real choice surfaces" sustainable. Fold in the
  supersession-aware scan (Q4) as a two-sentence refinement of AC2 if the
  maintainer agrees at the gate; otherwise ship as written.
- **M98 (new) — lesson graduation.** Author the guard-doctrine module (or
  synthesis note), move the matured family, retire the covered lessons
  whole under D-051's ownership criterion, and land the annotating D-entry
  naming maturation as the third outflow (Q3). High priority: LESSONS has
  16 chars of weight headroom and 1 line of item headroom, and the only
  currently-legal remedy is the treadmill (Q3). Independent of the other
  three; can run before or after M97.
- **M95′ — re-cut, keeping the T1/T2 ledger as input.** Same goal shape
  (an editorial pass, first stamp for M96), with the premise corrected:
  the rulebook is current knowledge (D-045 annotation authored in this
  milestone, with the Q1 decision procedure and Q2 inversion doctrine in
  the same entry — one entry, it is one boundary). AC1 is replaced: a
  block is removable when **(a)** it restates an existing decision record
  (cite-and-delete — the ~35-40 lines already proven), or **(b)** it fails
  the behavioral inversion test and records no decision (delete against
  git, no backfill), or **(c)** it is redundant with the skills' own
  directives (B15 / RR01 rec 7's prune, now legal). AC2's
  inversion-and-re-anchor machinery is unchanged and is what "zero rules
  lost" rests on; guard-pinned blocks that fail the behavioral test are
  shortened *with re-anchoring*, not skipped. Honest yield expectation:
  ~60-100 lines, not RR02's 165-215; the count stays evidence, never a
  gate (the old AC5 was right). New D-entries: only where the pass
  surfaces a genuine unrecorded cross-cutting choice — expected few,
  possibly zero.
- **M96 — keep, one amendment.** The ratchet is the right instrument class
  and nothing in M95's ledger touches RR02 Q3's reasoning (the trilemma
  argument is about derivability, not about where rationale lives). Amend
  the editorial-pass rule the stamp references: the pass applies Q1's
  decision procedure, not RR02 rec 1's "delete the defense back to its
  D-entry" (which M95 proved has nothing to delete back to for much of the
  text). Dependencies unchanged (M94 done; M95′ provides the first stamp).
  While in the file, add the Q5 inflow-test sentence to the rulebook
  preamble — it is the ratchet's editorial criterion stated at the door.

Dropping M96 was considered and rejected: without a standing signal, M95′
repeats RR01 rec 9's failure mode — a one-time cut with no outflow
pressure, undone by arithmetic in ~30 milestones. This is the smallest set
that addresses the root cause on all three files: the rulebook gets an
inflow test + outflow + signal (M95′+M96), DECISIONS gets its read bound
(M97), LESSONS gets its missing outflow (M98).

---

## Beyond the brief

- **RR02's flagship error has a diagnosable mechanism, and cairn's own
  lesson corpus predicted it.** RR02 §1(c) matched the rulebook's "49
  lines … 13%" to D-049 on numeric similarity without reading the entry
  out — precisely the failure `LESSONS.md:35` (M75) teaches: "a
  restatement is unverified until read out of the source." (Nuance for the
  record: D-049's "never approaching 50" counts *lessons* while the
  rulebook's "49 lines" counts *physical lines* — both true, different
  measurands, neither recording the rulebook's fact. M95's NO-HOME verdict
  stands.) The system knew the trap; the reviewer had not read LESSONS.
  Worth remembering when weighing what "Fable-tier review" buys: this
  review's authority is exactly as good as its citations, which is why the
  brief's read-it-out-of-the-source discipline should stay in every future
  RB.
- **D-049's weight threshold is a treadmill, stated numerically.**
  Re-derived at today's measured mean (631), LESSONS' threshold becomes
  876 + 32 × 631 ≈ 21,067 → 21,500, i.e. above the current 20,500. Each
  consolidation raises the mean; each re-measurement would ratify the
  accretion. The threshold can tax but never bind. This does not fault
  D-049's derivation for its purpose (backstopping the item cap at
  ordinary density) — it faults treating the weight axis as an outflow
  driver, which only Q3's graduation actually is.
- **The mutation-registration set is becoming a second constituency for
  rulebook prose.** 14 of 21 ledger blocks are guard-pinned; several
  anchors exist for matchability rather than doctrine. As guards
  accumulate, every editorial pass pays a re-anchoring tax that grows with
  the guard count — the Q2 asymmetry (reddening blocks careless deletion
  but never justifies keeping) is what stops that tax from hardening into
  a freeze. Watch it: if a future pass finds re-anchoring dominating the
  cost, the anchor-choice discipline (anchor on rules, not on scaffolding)
  deserves a line in the harness's own doctrine.
- **The heading index figure reconciles exactly:** 52 headings, 5,326
  chars flat, 5,378 with newlines — RR02's number was newline-inclusive.
  Trivial, but it means both measurements are honest and M97's AC4
  baseline can cite either with a stated basis.
- **`LESSONS.md:19` (M51) and `:44` (M87)** — the archive-summary
  budgeting and compress-what-your-phase-owns lessons — are candidates for
  the graduated family's second tier (records-hygiene craft rather than
  guard craft). M98 should classify, not assume, the family boundary; the
  63% figure above is this review's classification and belongs in M98's T1
  evidence, re-derived.

## Recommendations

Each marked **apply / consider / reject-with-reason**, naming the standing
D-entry it touches.

1. **Apply — classify `tracking-rules.md` as current knowledge and record
   the placement procedure.** One D-entry annotating D-045 (and citing
   D-052's precedent): the rulebook is current knowledge; class-3 text is
   owned by decision records; class-4 justification is deletable against
   git; the Q1 three-step procedure and the Q2 behavioral-inversion
   doctrine stated as the authoring/editing test. Touches D-045 (annotate),
   D-052 (cite), IP4 (reading confirmed, wording untouched). Delivered by
   M95′, which needs it as its license.
2. **Apply — M97 as planned, first in order.** Optionally fold in the
   supersession-aware scan as an AC2 refinement. Touches IP2 (the
   annotation its AC1 already plans); IP4 untouched.
3. **Apply — re-cut M95 per Q7** (AC1 replaced with the three removal
   grounds; ledger reused as input; yield recorded as evidence, never a
   gate). Touches no standing entry beyond rec 1's; supersedes RR02 rec 1's
   framing, which M95's ledger falsified.
4. **Apply — M98, lesson graduation:** distill the guard-craft family into
   `skills/shared/guard-doctrine.md` (synthesis-note fallback), retire the
   covered lessons whole, annotate D-051 with maturation as the third
   outflow. Touches D-051 (annotate), D-015 (charter restored, not
   changed); argued against D-029/D-015 costs in Q3.
5. **Apply — keep M96 with the amended editorial rule** (the stamped pass
   applies rec 1's procedure) and the one-sentence rulebook inflow test.
   Touches GP1 (see rec 6), D-031 (unchanged, cited).
6. **Apply (recommend to the user — principle change): amend GP1** to the
   exact wording in Q6, recorded as a D-entry. Touches GP1; requires the
   explicit user decision DESIGN.md mandates.
7. **Consider — the always-read audit frame:** the `/milestone` audit (or
   M96's advisory output) names, per always-read file, its inflow test /
   outflow / signal, so the next unguarded file is visible before it costs
   30 milestones. One paragraph; no new mechanism. Touches nothing
   standing.
8. **Consider — anchor-choice doctrine for the mutation harness** (Beyond
   the brief, item 3), only if M95′'s re-anchoring cost proves material.
   Touches nothing standing.
9. **Reject — the "author the missing D-entries, then slim" remedy**
   (M95's work-log candidate re-cut, `M95:148`): it converts editable mass
   into permanent history mass at ~1,900 chars per entry to license
   ~3-line deletions, misclassifies operative doctrine (B17) as displaced
   rationale, and — pre-M97 — would grow the always-read burden it exists
   to shrink. Rec 1 makes it unnecessary.
10. **Reject — a unified lifecycle mechanism across the three files** (Q5):
    the type signatures differ; a model general enough to cover all three
    constrains none. The shared frame is D-045's two classes plus the
    three-element completeness demand (rec 7), which is doctrine, not
    mechanism.
11. **Reject — any IP4 change, and archival-with-tombstone now:** IP4 is
    doing its job and the read-bound removes the cost; the tombstone
    candidate stays parked on its stated trigger (`ROADMAP.md:31`).
    Touches IP4 (explicitly left untouched), RR02 rec 6 (upheld as
    parked).
12. **Reject — re-deriving D-049's LESSONS threshold from the
    post-consolidation mean:** it would ratify accretion (the treadmill,
    Beyond the brief). After M98 discharges the graduated family, a fresh
    measurement is legitimate — the mean will have *fallen*, and the
    derivation doctrine applies as written. Touches D-049 (unchanged;
    application guidance only).

**Where this review disagrees with its predecessors, explicitly:** RR02
§1(c)'s flagship example is wrong (verified by hand, mechanism diagnosed
above); RR02 rec 1's remedy and yield are falsified by M95's ledger and are
superseded by rec 3 here; RR02's "rationale" classification lumped
operative application doctrine with legislative history (Q1). RR02 Q3
(ratchet), Q4 (bounded read), Q5 (rec 15 upheld), and Q6 (instrument first
— since executed as M94) all survive M95's evidence and are upheld here.
RR01 rec 7's prune is completed by M95′ under the corrected AC1; RR01's
Q8 "three entries → mechanism" tripwire is extended, not contradicted, by
Q3's graduation-to-doctrine.
