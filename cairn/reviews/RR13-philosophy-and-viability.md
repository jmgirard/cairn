# RR13: cairn's philosophy, thrash cycles, and long-term viability (repo-level)

- **Date:** 2026-08-16
- **Brief:** `cairn/reviews/RB13-philosophy-and-viability.md`
- **Reviewer baseline:** working tree at `daeca15` (clean); the brief's pinned
  figures at `0e0850d` adopted as given and spot-checked (143 archive files,
  107 `### D-` entries / 4,002 lines, rulebook 990 lines, skills 2,738 lines
  total, RB01–RB12 archived). Materials read: all of Tier 1 whole
  (`cairn/DESIGN.md`, `skills/shared/tracking-rules.md`, `cairn/ROADMAP.md`,
  `cairn/LESSONS.md`); Tier 2 as sampled (M127, M114, M139, M140, M142, M143
  archives; RR05 and RR10 whole); Tier 3 whole (`README.md`,
  `skills/milestone-plan/SKILL.md`, `skills/milestone-review/SKILL.md`,
  `skills/shared/guard-doctrine.md`, `skills/shared/records-hygiene.md`);
  Tier 4 (`references/competitive-landscape.md`,
  `references/effort-experiment-notes.md`, `git log --oneline -80`); plus
  D-057 and D-090 whole and the D-078–D-107 headings. No file edited other
  than this report.

## Verdict

The thrash is structural, not a tuning problem: cairn decided that its own
rulebook prose is a product to be tested and that its records are measurements
to be audited, and on that substrate every fix creates new prose that itself
demands testing and auditing, so the loops are built in. The underlying bet —
durable, human-readable project state that any session can resume from, with a
human gate on every merge — is sound, and this repo's own history is the proof
that it works. What failed is the enforcement tower built on top of that
state, which now costs far more to maintain than the state it protects: about
three quarters of the last 44 milestones changed how the system governs or
verifies itself rather than anything an adopting repo can use, and roughly
half of what review finds are defects in records the process itself mandates.
The project is viable after a specific reduction, not as-is and not by
rewrite: keep the files, the gates, the hooks, and the scripts; retire the
prose-testing layer and the measurement-grade record discipline; shrink the
rulebook to the rules that change behavior. That is three ordinary milestones
of work, and it leaves a system one person can maintain and a second person
could plausibly adopt.

## Answers

### 1. The thrash is structural. The generator is code-grade verification applied to artifacts that have no oracle.

The three named cases look different on the surface — a certification loop
(§8), a nine-round review (M114), correction chains in `DECISIONS.md` — but
they share one mechanism, and it has two coupled halves.

**G1 — prose as a tested artifact.** cairn's deliverable is markdown conduct
rules, and it decided to verify them the way code is verified: substring
guards, a mutation harness to test the guards, inversion protocols to test the
pins, doctrine (`guard-doctrine.md`, 350 lines) to teach the authoring. But
prose has no oracle. A test of code is checked against behavior; a test of a
sentence can only be checked against another rendering of the sentence, so
every verification instrument over prose has an enumeration at its heart —
anchors, renderings, sites, slices — and the author of the enumeration is
exactly who cannot complete it (guard-doctrine §3 says this about detectors,
in cairn's own words). Each discovered blind spot became a new rule plus a new
guard plus new doctrine — M117 (site axis), M121–M126 (inversion sweeps, decoy
tables), M131–M132 (predicate/subject, promise/procedure), M139–M140
(insertion, whole-slice equality) — and the new prose was itself subject to
the same verification demand. That is a regress by construction, and the §8
arc is its purest run: the instrument that certified guard descriptions was
itself guard-authored, so it received maximal certification of itself, which
RR10 §3 measured directly — 11 of round 2's 13 findings existed only because
the rebuild existed. Cost tracked prose mass, not risk.

**G2 — records as measurements under append-only history.** The rules require
record claims to be derivation-backed (the derived-claims, derived-figures,
and failure-identity rules, M134/M136/M137), while IP4 makes the record
corpus append-only. A measurement written into a D-entry about the corpus is
falsified by the next change to the corpus — the M99 fixed-point lesson, hit
three times — and the only legal repair is another entry, which carries its
own measurements. That is the correction cascade: D-084, D-086, D-089, D-092,
D-093, D-096, D-100, D-102, D-104, D-106 — ten of the last thirty entries
exist solely to correct measurement claims in other entries. The ROADMAP's own
batching row records that the generator was thought dead at M127 and recurred
at M139.

The two halves are one property: **cairn extends code-grade correctness
discipline to non-code artifacts** — doctrine prose (G1) and tracking records
(G2). Every recorded loop is an instance. M114's nine rounds were G1 (the
doctrine was byte-stable from pass 1; "every return was description-layer" —
its own archive). The §8 arc was G1 with the instrument pointed at itself.
The correction chains are G2. The recent run M130→M143 is the generator in
its narrowed, post-D-090 form: no new *apparatus*, but a new *rule about
verification or records* roughly weekly, each shipping with guard surface and
each reviewed by the machinery it modifies (M142 took three passes and two
defect returns — on guards over the rule that scales rigor down).

**Is it removable without abandoning the core premise?** Yes, cleanly. The
premise — durable, governed, human-readable state; human-gated merges — makes
no demand that the rules be substring-pinned or that records be
measurement-grade. The evidence for separability is already in the record:
D-057 removed one stratum of the tower (size governance) and the size thrash
stopped; M127 removed another (§8) at user mandate and the certification
thrash stopped; both removals cost one milestone each and nothing regressed
behind them (M127's AC1 per-hit ledger: zero operative losses). What each
removal missed is that the generator survives at the next level down —
after D-057 the apparatus grew, after D-090 the conduct rules grew. The
removal that has not yet been tried is the stratum itself.

### 2. Self-reference: roughly three quarters of M100–M143 is cairn governing cairn.

Classification rule: a milestone is **(a)** if its deliverable changes what an
operator of an adopting repo gets from the skills, hooks, or scripts in
ordinary work on their own code; **(b)** if it changes how cairn's tracking
records are authored or governed; **(c)** if it changes how cairn verifies its
own prose, guards, criteria, or review loops (verification of verification);
**(d)** other (ingestion of external references, decommissioning passes).
Each milestone classified by its archive title and summary; where a rule ships
in a skill all repos run but its subject and trigger are cairn's own records
or verification conduct, it is classed by subject, not by shipping vehicle.

- **(a) adopter capability — 9 of 44:** M103, M106, M111, M112, M113, M128,
  M129, M135, M141.
- **(b) governance of cairn's records — 13:** M100, M104, M105, M107, M108,
  M110, M118, M119, M126, M131, M134, M136, M137.
- **(c) verification of cairn's verification — 19:** M102, M109, M114, M115,
  M116, M117, M121, M122, M123, M124, M125, M127, M130, M132, M138, M139,
  M140, M142, M143.
- **(d) other — 3:** M101, M120, M133.

Ambiguity margin: M100 and M105 could be argued into (a) (they improve review
conduct any repo benefits from), which moves the split to at most 11/44
adopter-facing. Either way the ratio is **(b)+(c) ≈ 73–77%**, and the trend is
adverse: of the last six substantive milestones (M137–M140, M142, M143), six
of six are (b) or (c). Exactly one milestone in the whole window — M135 — was
triggered by a defect surfaced from an adopting repo (intraclass's audit).

Is that pathological? For a tooling project in a hardening phase, a high
governance share can be healthy. Three things make this one pathological
rather than healthy. First, duration: the share has been at this level for
~44 milestones spanning a month, not a sprint. Second, the demand signal is
internal: with zero external adopters (DESIGN Known issues), no (b)/(c)
milestone since M135 was triggered by anything a user hit — they were
triggered by defects in records and guards that earlier (b)/(c) milestones
created. Third, the repo's own measurement agrees: the 2026-08-08 effort
audit found roughly half of actioned review findings were record defects
(ROADMAP re-measurement row), i.e. the review machinery is mostly catching
defects in the records the machinery mandates. The evidence that would
overturn this reading is adopter-driven demand — external issues, shipped
behavior defects — pulling (b)/(c) work. It does not currently exist.

### 3. The prose-guard architecture is not earning its cost, and the cheaper instrument already exists: the diff.

What the ~15,000 lines protect: the wording of markdown rules against silent
deletion or drift. What threatens that wording: edits made in this repo, by
this repo's own milestones — every one of which already passes through a PR
with a three-lens fresh-context review and a maintainer merge gate. The
guards' marginal value over "a human and three reviewers read the diff" is
automation of the case where a prose edit silently mangles an *adjacent*
rule (the M104 reflow trap, the M23/M39/M40 anchors). That case is real; it
is also small, and git makes no prose deletion silent.

Measured yield versus measured cost, from the record:

- The yield the stratum can claim is the §8-era finds: real contradictions
  invisible to a green suite (RR10's D9), shipped-rule inversions (M121). But
  almost all of that yield was defects **in the stratum's own prose**. RR10
  §3: 11 of 13 findings were scaffolding the rebuild generated. M127's
  retirement ledger: zero operative losses from deleting 121 registry
  entries. The mutation-registry census (ROADMAP partial-pin row, measured
  at M116): of 412 registered blocks, 22 pinned whole sentences; 390 were
  fragments — most "fragments by design". A pin architecture whose census
  looks like that is pinning matchability, not meaning, which is exactly
  what "What gets a test" itself warns of ("a guard can pin scaffolding").
- The cost is on the record at every level: ten-plus milestones fixing the
  guards themselves (M117, M121–M126, M131–M132, M139–M140); the M104 trap
  reddening guards on rules a milestone never touched; LESSONS.md — the
  file meant for build quirks — now over half guard-authoring craft (lines
  18, 26, 27, 37, 38, 43, 44, 47 by subject); a 350-line doctrine module;
  four Fable escalations (RB09–RB12) on one mechanism family; and the
  opportunity cost counted in Q2.

The comparison that decides it: **hooks and scripts are tested the ordinary
way** — 1,299 + 3,437 lines of code carrying ~4,700 lines of behavioral
tests — and that layer has generated approximately zero thrash across the
whole record. The pathology is confined to tests over markdown. Same repo,
same author, same review process; the only variable is the substrate.

Of the brief's two alternatives: "accept prose drift and detect it
differently" is the right one, and the different detector is the one already
running — PR diff review by fresh-context readers, plus git history. "Stop
guarding prose entirely" is nearly right but overshoots slightly: a handful
of smoke checks that the load-bearing *mechanical contracts* still hold
(files exist, section headings parse, the templates instantiate — things
`cairn_validate` mostly already checks) are cheap and oracle-backed. What
should end is the substring-pinning of rule wording, the mutation harness
over it, and the doctrine that teaches it. Note this recommendation removes
apparatus, which D-090's Untouched clause expressly permits ("firing removes
apparatus rather than adds it"); no door is being reopened.

### 4. Storage, file class by file class.

**`DECISIONS.md` (append-only, 4,002 lines, 107 entries).** What is actually
retrieved: standing closures and rejections at collision time — D-050, D-057,
D-090, D-044, and perhaps fifteen others do real, recurring work stopping
re-litigation. That function is valuable and cheap under the bounded heading
read (D-054). What has fallen below maintenance value: the ten
correction-of-correction entries named in Q1, and the §8 archaeology
(D-079–D-093, fifteen entries about one retired mechanism) — no future
decision hinges on them, yet every heading scan walks their headings, which
have themselves grown to 40–66 words (D-095's heading is 66 words — the
heading discipline is exporting entry mass into the index the bounded read
depends on). Honest disposal path under IP4/C2: **cease to add**. Two
narrowings, both already half-practiced: (i) a D-entry records the decision
and its rationale and *no derived measurements* — figures live in the
milestone file the entry names (this narrows the derived-figures rule's
application to `DECISIONS.md` rather than violating it: procedural-by-pointer
is one of its two legal forms); (ii) corrections batch, one superseding entry
per milestone at most (D-096 and D-106 are the practiced precedent). Those
two cut the inflow to roughly one entry per substantive milestone and end the
cascade at its source. No new index file is needed; the heading scan suffices
once headings stop carrying measurement clauses.

**Milestone archives (143 files, ≤25 lines each).** Retrieved by the
prior-review lens and collision sweeps; bounded by the cap; near-zero
maintenance. The one storage class that is working exactly as designed. Keep.

**`LESSONS.md` (49 lines).** The 50-line cap is real but the one-line format
is a fiction: the per-line density axis deliberately exempts item lines
(D-052), and the lessons metastasized exactly there — line 18 runs ~2,900
characters with five `Extended M<NN>` grafts; lines 43 and 27 are similar.
Read at every plan session. Over half the content by mass is guard-authoring
craft that is moot if Q3's recommendation lands; the file's own retirement
rules (D-051/D-055 — enforcement, ownership, maturation) already license the
exit, and `LESSONS.md` is current knowledge, so shedding is legal today. What
remains should be what the file's header promises: build quirks and testing
tricks, one actual line each.

**`ROADMAP.md` candidate rows (~28 rows).** The worst cost-per-byte-read in
the repo: an always-read file whose rows run 300–500 words each, carrying
sweep provenance, audit annotations, promotion falsifiers, and negative
evaluation results (rows at lines 25, 30, 32, 38, 39, 48, 50 of the current
file). Each clause was individually mandated by a real rule (search-first,
falsifying promotion conditions, D-042 pairing) — this is the density-cap
hole again: the item axis charges a 500-word row one line, and the per-line
axis deliberately looks away. What a candidate row needs to do its job is:
the idea, why it is parked, and what would promote it — one to two lines. The
rest is protection against re-litigation whose annual cost now exceeds the
re-litigation it prevents. ROADMAP is current knowledge (D-052): prune in
place, with git holding every pruned clause.

**`references/`.** The healthiest corpus in the repo. Small, demand-pull,
honestly provenance-stamped, and it contains the single most decision-useful
artifact I read (`effort-experiment-notes.md` — see B3). Keep unchanged.

### 5. Process, item by item.

- **AC fencing and the Coverage map — load-bearing, keep.** Cheap (a rule and
  a mechanical check), aimed at a real, measured failure (optimistic
  check-off), and central to what makes the merge gate honest. This is the
  part of review an adopter is buying.
- **The three-lens review fan-out — load-bearing for code, a premium for
  prose.** The diff-bug lens earns its keep everywhere. The blame-history
  lens has real catches on the record (M104's scoped-sibling collision,
  M112's README contradiction). The prior-PR lens measured its own primary
  surface empty (M91) and mostly no-ops. The premium case is doctrine-only
  milestones — three reviewers plus a scorer over a markdown diff is how a
  wording milestone comes to take three passes. Scale the fan-out with M142's
  own stakes tier: internal/doc-only diffs get one fresh reviewer; code and
  user-facing diffs keep the fan-out.
- **The confidence scorer — insurance the maintainer is now paying to
  overrule.** Its measured behavior: down-scores exactly the finding classes
  that matter in this repo (RR10: 78/78/68/60, logged not fixed, merge held
  by hand), scored a real irreversibility defect at 48 (records-hygiene §5),
  and at M143 the maintainer directed two 60-scored findings fixed at the
  gate. The 80 threshold now functions as a formality the operator reads
  past — records-hygiene §5 explicitly instructs reading every sub-80
  finding anyway. Cut the scorer; let the (single or fanned) reviewers rank
  their own findings and let the maintainer triage. This supersedes the
  D-016/D-078 scorer design and should say so.
- **The plan-gate criteria audit — keep, gated by stakes.** Its founding
  catch was real (M114's unsatisfiable criteria). But its record clause is
  half-honored (three of five post-adoption milestones carry no line —
  `/milestone-plan` step 3 admits this in its own text), and its reach has
  kept growing (M138). Run it for user-facing or irreversible work; skip it
  for internal-tier milestones, which M142's tier now identifies.
- **The RB/RR protocol — keep the protocol, change two defaults.** The brief
  artifact is genuinely good (reproducible, auditable escalation). Two
  measured problems. First, Binding criteria: verbatim-ingested BC blocks
  string-compared at review (M107) turn an advisory review into a
  pre-commitment, and the §8 arc shows RRs compounding upstream RRs' BCs.
  This brief's own choice to omit them is right and should become the
  default: an RR is advisory unless the maintainer asks otherwise. Second,
  deference: RR09 and RR10 each recommended amended keeps of §8; the user's
  blunt retirement at M127 outperformed both. A mechanism reaching its second
  escalation should have removal as the brief's default option (see B1).
- **Weight caps — keep the item caps, retire the density ceremony.** The item
  caps with outflows are cheap and have held. The second axis (record
  density), the budget scripts at drafting time, and the stamp discipline
  are ceremony with a measured cost: the stamp's check-ordering needed a
  hotfix (`0e0850d`), and the axis design has a known hole exactly where the
  mass accumulated (Q4). One cap per file, one remedy per cap.
- **Hygiene passes — keep at milestone close; drop the standalone sweeps.**
  Post-merge hygiene is where archives, lessons, and graduations happen —
  load-bearing. The standalone candidate-audit passes that annotate rows in
  place (the 2026-08-15 sweep, which wrote "Audited … evidence both ways,
  kept" paragraphs *into* the always-read rows) are governance producing
  more governed mass.
- **The thrash machinery itself — collapse to a paragraph.** M143/D-105
  landed in the right place (descope-or-park, re-cut never recommended). But
  the surrounding taxonomy — defect vs amendment returns, the widening test,
  second-occurrence stops, per-track counting (D-097, D-101, M130, M139) —
  exists mostly to arbitrate collisions between the process's own parts (the
  return floor vs AC fencing vs criteria rigor). Under Q3's and Q5's
  reductions those collisions largely vanish, and the rule can be: count
  returns in the work log; at the third, descope, park, or escalate; never
  re-cut the same objective.

### 6. Clean slate.

Designing today, for one maintainer working with coding agents, with the 143
milestones of experience and none of the code:

**State files — cairn's layout, essentially unchanged.** `DESIGN.md`
(architecture + a short IP/GP block), `ROADMAP.md` (status table + one-line
candidates), `DECISIONS.md` (append-only; an entry only when a future session
could re-litigate; decision + rationale, no measurements), `LESSONS.md`
(capped, genuinely one line each), `milestones/` with active files and
≤25-line archive summaries, `references/` demand-pull. This part of cairn is
right and I would not change the file map at all.

**Mechanical enforcement — everything executable cairn has, nothing over
prose.** The eight hooks as they stand (merge marker bound to its PR,
force-push guard, session injection, stop guard, the advisory nudges); the
reporters (`status`, `next`, `validate`, `impact`, `cost`); `cairn_validate`
checking structure — status consistency, orphans, coverage completeness,
scaffold presence, caps. Tests over hooks and scripts, behavioral, roughly
the ~4,700 lines they have now. Zero tests over markdown.

**Prose — one rulebook ≤ ~250 lines, skills ≤ ~120 lines each.** The rulebook
states: file ownership and the boundary rule; status vocabulary and
gatekeeping; the git/approval model; sizing and the three tiers; AC fencing;
question gates; the DECISIONS bounded read; toolchain profiles; a one-
paragraph thrash rule; a one-paragraph escalation protocol. Rationale lives
in git and the decision log, not inline. No always-read governance frame —
the frame's job (notice growth) is done by the caps and by the maintainer.

**Gates — two, plus approval.** Plan questions (one batched round), merge
approval (chip + marker + evidence). Review: one fresh-context reviewer on
the diff by default, the full fan-out on request or for user-facing code. No
scorer, no certification, no criteria audit by default — rigor escalates by
stakes, at the maintainer's word.

**Deliberately not built:** prose-guard suites and the mutation harness
(~15,000 lines — the single largest artifact in the repo); guard doctrine;
description-layer certification in any form; the confidence scorer; the
criteria audit as a standing step; the density axis, budget scripts, and
stamp rules; binding-criteria string comparison; the always-read governance
frame; the records measurement-grade rules (derived claims/figures, failure
identity) as applied to tracking prose; the amendment/widening return
taxonomy. Each is dropped for the same reason: it defends prose correctness
at code-correctness prices, and Q1–Q3 measure that trade as negative.

**Size:** roughly 2,500–3,500 lines of prose + scripts + hooks, plus ~5,000
lines of behavioral tests — against today's ~22,000+ (990 rulebook + 2,738
skills + 447 doctrine modules + 14,983 guard tests + 4,736 hooks/scripts +
their tests). A ~70–80% reduction overall, ~97% of it from the guard mass,
while the hooks and scripts survive nearly whole.

### 7. What survives the clean slate.

Genuinely good — a from-scratch designer re-arrives at these, and the
competitive survey confirms several are differentiating:

- The file map and ownership boundary (Architecture → DESIGN · Status →
  ROADMAP · …), and one sole status authority.
- Status gatekeeping by skill (only `/milestone-review` sets `done`) —
  unique in kind per the M06 survey.
- The hook-backed human merge gate with a PR-bound approval marker —
  cairn's sharpest edge, and the survey found no analogue.
- AC fencing: evidence before the tick, criteria never reinterpreted at
  review, the Coverage map.
- Small milestones ≈ one PR; checkpoint commits; stateless resume; `/clear`
  at the milestone boundary.
- Append-only decisions with supersede-never-edit, in lightweight form.
- Archive compression to bounded summaries.
- Toolchain profiles (core stays language-agnostic).
- The deterministic reporter scripts.
- The RB/RR escalation artifact (self-contained brief, ingestible report).
- The interaction layer: routing chips, plain-language gates, the README's
  worked example — under-credited in cairn's own self-assessment (B3).

Locally reasonable but path-dependent — each exists only because an earlier
cairn decision created the problem it solves, and none is reinvented from
scratch: `guard-doctrine.md` (exists because prose guards exist), the
mutation harness (because the guards needed guarding), `records-hygiene.md`
(because record ceremony needed craft), the density second axis (because
caps met accretion), the derived-claims/figures/failure-identity family
(because records were promoted to measurements), the amendment-return and
widening-test taxonomy (because the return floor collided with criteria
rigor), the always-read governance frame (because the rulebook grew), D-098
cross-repo hosting (because governance work needed a home outside the repo
that surfaced it).

### 8. The self-documentation premise.

The strongest case against the bet: (i) **Redundancy.** Harness context
handling keeps improving — long contexts, session summarization, resumable
task state — so the marginal value of curated external state over "git
history + the code + the PR record" shrinks; much of what ROADMAP and the
archives hold is re-derivable from git at read time. (ii) **The state
becomes the burden.** The state must be maintained by the same fallible
agent it serves; cairn's own measurements show maintenance became the
dominant work (Q2's 73–77%; the ~half-of-findings-are-record-defects
figure), and the always-read mass means every session pays a conduct tax —
~17K tokens of rulebook at every skill fire (measured in the phase-gated-
loading row) and a rules-compliance review dynamic (M137's F19/F27
"pin-compliance ceremony" shape). (iii) **Selection.** The one repo that has
exercised the system hardest is the system itself — a worst case for
self-reference, and no external adopter exists to show the ordinary case.

Against that, the premise's measured wins, from this record: stateless
resume demonstrably works (143 milestones across `/clear` boundaries, seven
releases, and a reviewer today can reconstruct the §8 arc entirely from
disk — this brief and this report are only possible because the record
exists); the token cost of reading state is small and roughly constant
(~200–330K cache-read/turn in both effort eras — the cost driver is session
length, not state mass); and the closures that stopped thrash (D-057, D-090,
M127) were themselves only reachable because the record made the pattern
visible and citable.

Verdict, premise separated from implementation: **the premise holds in its
weak form and fails in its strong form.** Weak form — a small, bounded,
human-readable state layer (status, decisions, design, archives) plus
human-gated change control — is cheap, demonstrably useful, and not made
redundant by better context handling, because its value is durability and
auditability, not context supply. Strong form — that the state layer itself
must be verified, measured, and governed to the standard of shipped code —
is the part that degraded the sessions it was meant to help, and it is not
entailed by the weak form. cairn implemented the strong form. The
implementation should retreat to the weak form; the premise itself stands.

### 9. Long-term viability: viable after a specific reduction.

**Form: viable after a specific reduction.** The reduction, named: retire
the prose-verification stratum (guard suites over markdown, mutation
harness, guard doctrine, certification residue) and the measurement-grade
records discipline (derived-figures-class obligations on tracking prose, the
correction-cascade genre); shrink the rulebook and skills to operative
rules; scale review rigor by the stakes tier that M142 already ships; and
hold the governance door shut at conduct rules as well as apparatus.

Why not viable as-is: the trend line. The last six substantive milestones
are all governance-of-governance (Q2); the correction cascade recurred after
its generator was declared dead (ROADMAP batching row: "arguably fired at
M139"); every widening of the door's definition has been squeezed through
(D-090 closed apparatus, and M130–M143 shipped rules-about-rules weekly);
and the maintainer is one person carrying ~15,000 lines of tests whose
subject is 990 lines of prose. Adoptability compounds it: a new adopter's
first planning session reads a 990-line rulebook plus conditional modules —
the first-session cost is the strong form's, while the value they came for
is the weak form's.

Why not "viable only if re-founded": separability is demonstrated, not
hypothesized. The failure mass sits in nameable files (`skills/tests/` over
markdown; doctrine modules; record-rule sections) with clean boundaries from
the healthy mass (hooks, scripts, their tests, the file map, the gates), and
the repo has twice removed a stratum in one milestone with zero operative
loss (D-057; M127 with its per-hit ledger). A rewrite would discard the
operational core — which works, is measured to work, and is the part the
competitive survey says is unique.

Why not "not viable": the core loop has 143 milestones, seven releases, and
honest self-measurement on the record; nothing in the evidence says the weak
form fails. The disease is an addition, and additions can be removed.

### 10. The next three milestones.

**First — "The guard suites leave the merge gate" (1 session; the smallest
reversible probe).** `/milestone-review`'s consistency gate and the trivial-
tier suite-run rule stop running `skills/tests/` (the prose-guard suites);
`hooks/tests/` and `scripts/tests/` keep gating. The suite files stay in the
repo, runnable by hand — nothing is deleted, so the step is a switch, not a
demolition. The same milestone appends the superseding entries the change
owes (C1/C3): one widening D-090's door to cover new conduct rules about
verification or records (naming D-090, quoting its trigger, grounding the
widening in the M130–M143 recurrence), and one recording this probe's own
exit condition, stated as a falsifier per the repo's own rule: re-arm the
gate if a prose regression ships that diff review missed and a specific
retired guard would have caught. Proposed acceptance criteria (proposals,
not binding): the two skills' gate text names the two gating suites only;
the superseding entries exist; all three suites still pass when run by hand
at the merge ref.

**Second — "The rulebook states rules; git holds reasons" (2–3 sessions).**
With guards ungated, re-anchoring cost is gone, so the reduction pass
becomes cheap: cut `tracking-rules.md` toward ~250–400 lines by removing
justification prose, §8-era residue, the density/budget/stamp machinery, and
the records-measurement rules as applied to tracking prose; retire
`guard-doctrine.md` to the archive (its craft is moot for gating purposes;
git and the LESSONS graduation trail preserve it); trim `records-hygiene.md`
to its candidate-lifecycle and supersede-discipline sections; prune LESSONS
to true one-liners and the ROADMAP candidates to one–two lines each
(current-knowledge edits, legal under D-045/D-052). This partially reopens
ground D-057 closed and must supersede it honestly (C3): D-057's trigger was
tokens-at-read, correctly measured not to bind; the new ground is different —
rule count as thrash surface and guard surface, evidence post-dating D-057
(Q1–Q3) — and the pass only became cheap because milestone one removed the
re-anchoring cost that made M95-era passes the most expensive sessions in
the repo's history.

**Third — "An external adoption pass" (1–3 sessions, capability-class
only).** Run `/cairn-init` and one full milestone loop on a repo the author
did not shape — ideally with a second person driving — and fix what breaks:
init rough edges, README gaps, first-session cost, the reduced rulebook's
comprehensibility to someone who has never read the old one. If no external
repo or person is available yet, the fallback is the capability backlog
(README flow diagram row, contributor scaffold row). The point is
directional: it produces cairn's first adopter-triggered demand signal
(Q2's missing evidence) and re-centers the roadmap on class (a) work.

## Beyond the brief

- **B1 — The escalation genre has been part of the loop.** Every prior RB
  asked its reviewer to solve a problem inside cairn's frame, and the
  reviewers obliged: RR05's recommendations added thrash machinery that
  M143 later had to recompose; RR09 and RR10 each recommended keeping §8
  amended, with RR10 running 556 lines and twelve recommendations —
  outperformed three weeks later by the maintainer's one-sentence
  retirement mandate at M127. Advisory conclusions delivered at Fable
  fluency acquire unearned momentum; the BC mechanism then hardened them
  into criteria. The correction is structural and cheap: RRs advisory by
  default (this brief already models it), and any brief about a mechanism
  on its second escalation must carry removal as a listed option.
- **B2 — The density design has a measured hole where the mass actually
  accumulated.** D-052 deliberately exempts item lines from the per-line
  axis to protect the one-item-per-line format; candidate rows and lessons
  then metastasized inside single "lines" (Q4). The caps report green while
  the read cost concentrates exactly where the axes do not look. No third
  axis should be built (C4); the Q4/Q10 diet covers it — but the hole is
  worth recording so the next cap design remembers that exempting a surface
  redirects growth to it.
- **B3 — What is genuinely excellent, said plainly.** The hooks and scripts
  layer is small, tested properly, and has never thrashed. The README is an
  unusually honest and well-written piece of user documentation — the
  enforcement-boundary and "what this deliberately does NOT do" sections
  especially. The effort-experiment page is the repo's best genre:
  self-measurement pointed at cost and quality rather than at prose, with
  stated confounds and a re-measurement procedure. And the DESIGN Known-
  issues section's candor ("a deliberate architectural bet, noted plainly
  rather than papered over") is the reason this review could be evidence-
  based at all.
- **B4 — The dogfooding conflation explains how the mass felt justified.**
  Because this repo's product is prose, "testing the product" and "testing
  the process records" blurred into one activity. But an adopting repo
  receives none of the guard mass's protection — the guards run only in
  cairn's own CI over cairn's own markdown. The 4:1 test-to-tooling ratio
  is entirely internal QA of wording, which is why retiring it (Q3) touches
  nothing an adopter has.
- **B5 — Runtime honoring is the actual open verification question, and the
  guards never addressed it.** DESIGN's Known issues concedes that conduct
  rules are enforced as prose and live honoring is only spot-verified. The
  15,000 lines guarantee the *text* of the promises is stable while nothing
  measures whether sessions *keep* them. If verification investment ever
  resumes (behind the widened door, on a shipped-behavior trigger), the
  worthwhile instrument is transcript-level spot-audit of conduct — does the
  review actually fence evidence, does the chip actually stop — not another
  layer over the wording.

## Recommendations

1. **Apply** — Remove the prose-guard suites from every gate (Q3, Q10 first
   milestone): `skills/tests/` stops gating merges and trivial-tier commits;
   hooks/scripts tests keep gating; files retained, runnable by hand; exit
   falsifier recorded. Removes apparatus — permitted by D-090's Untouched
   clause, no door reopened.
2. **Apply** — Supersede D-090 with a widened door (named per C1/C3): its
   trigger — a defect in shipped behavior — extends to new *conduct rules*
   about verification or records, not only new apparatus. Ground: D-090's
   Context predicted the signature ("the anti-cost program maximizes the
   cost it exists to reduce"); M130–M143 reproduced it through the door's
   definitional gap, and the correction cascade recurred at M139.
3. **Apply** — Records de-escalation (Q1-G2, Q4): D-entries carry decisions
   and rationale, never derived measurements (figures live in the milestone
   file, satisfying the derived-figures rule's procedural form); corrections
   batch to one superseding entry per milestone (D-096/D-106 precedent,
   graduating the parked batching row). Narrows the application of D-099's
   family to tracking prose; the family stands for code-adjacent artifacts.
4. **Apply** — The rulebook reduction pass (Q10 second milestone), with an
   explicit superseding entry for D-057's trigger clause as argued there —
   this is a partial reopening of closed ground and is flagged as such
   rather than worked around (C3).
5. **Apply** — Review rigor scales with M142's stakes tier (Q5): doc-only /
   internal diffs take one fresh-context reviewer; code and user-facing
   diffs keep the fan-out. The confidence scorer is retired in both modes —
   reviewers rank their own findings; the maintainer triages. Supersedes the
   D-016/D-078 scorer design, named here per C1.
6. **Apply** — RRs are advisory by default: Binding criteria only at the
   maintainer's request, and a brief about a mechanism on its second
   escalation lists removal among its options (B1).
7. **Consider** — The plan-gate criteria audit becomes stakes-gated:
   user-facing or irreversible work only (Q5). Its founding catch was real;
   its standing cost on internal-tier work is not paying.
8. **Consider** — Candidate-row and LESSONS diet as a hygiene pass under the
   reduced format (Q4): rows to one–two lines, lessons to true one-liners,
   guard-craft families retired by maturation into the archived doctrine.
9. **Consider** — After the reduction, one re-measurement in the effort-
   experiment genre: governance share of milestones, record-defect share of
   findings, and per-milestone cost, against the Q2 and 2026-08-08
   baselines — the honest check on whether this review's surgery worked.
10. **Reject** — Abandoning IP4 / append-only history. Reason: the cascade's
    cost came from measurement-grade claims meeting append-only repair, not
    from append-onlyness itself; with recommendation 3, appending is cheap,
    and IP4's audit value (this review depended on it) is intact.
11. **Reject** — Abandoning the external-state premise (folding back to
    CLAUDE.md + git + memory). Reason: Q8 — the weak form's value is
    measured and real; the failure was the strong form layered on it.
12. **Reject** — Re-founding / clean-slate rewrite. Reason: Q9 —
    separability is demonstrated on this repo's own record (D-057, M127),
    the surviving core is the differentiating part (Q7), and a rewrite
    would spend months to arrive where three milestones of subtraction
    arrive from here.
