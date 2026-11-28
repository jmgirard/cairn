# RR02: Weight-management architecture

- **Date:** 2026-07-19
- **Brief:** `cairn/reviews/RB02-weight-management-architecture.md`
- **Reviewer:** independent Fable-tier review (RB/RR protocol, D-004)
- **Materials read:** `skills/shared/tracking-rules.md` whole (765 lines);
  RR01 §5/§7/recs 9+15 (`reviews/archive/RR01-architecture-retrospective.md`);
  `scripts/cairn_scripts.py:39–117`; `scripts/cairn_validate.py:60–173`;
  DECISIONS entries D-018, D-030, D-031, D-034, D-035, D-045, D-046, D-049,
  D-050, D-051, D-052; `DESIGN.md:78–104`; archives M84, M87;
  `milestones/M94-always-read-weight-signal.md`; `skills/milestone-plan/SKILL.md:10–60`.
- **Measurements reproduced:** rulebook 545 lines at RB01 (`0274bf4`),
  532 after M58 (`8d0f373`), 536 lines / 33,746 chars at plan M63 (`06e23ef`),
  765 lines / 52,797 chars today. `DECISIONS.md` 47,389 chars at plan M63,
  95,976 today (95,374 Unicode chars, 52 entries, 1,425 lines).
  `cairn_validate` all-green on the current tree, `record density` included.
  All of the brief's headline numbers check out.

One measurement the brief did not include, computed for this review — rulebook
growth **by section**, RB01 state (`0274bf4`) vs. today:

| Section | RB01 | now | Δ lines |
|---|---|---|---|
| Weight caps | 22 | 81 | **+59** |
| References pages | 0 | 67 | +67 (new, M57/D-031 kept it core) |
| Universal tracking rules | 29 | 72 | +43 |
| Output & interaction discipline | 59 | 98 | +39 |
| Git and approval model | 54 | 77 | +23 |
| Sizing and the work tiers | 34 | 51 | +17 |
| What gets a test | 25 | 40 | +15 |
| Validation doctrine | 64 | 11 | −53 (the rec 9 extraction) |
| everything else | 258 | 268 | +10 |

This table carries most of the argument below.

---

## 1. Why RR01 rec 9 failed to hold

**Structurally incapable, not incompletely executed** — though the execution
was also incomplete, the incompleteness is worth tens of lines against +233.

Three findings:

**(a) A one-time extraction is a stock remedy applied to a flow problem.**
The file has measured inflow of ~7.6 lines per milestone (536→765 over
M63–M93) and no outflow of any kind — no cap, no retirement path, no
editorial cadence. cairn itself already articulated this exact failure mode
for `LESSONS.md`: D-051 is titled "LESSONS.md gets **an outflow, not just a
ceiling**" (`DECISIONS.md:1306`). The rulebook got neither an outflow *nor* a
ceiling; it got a one-time cut plus a norm. Arithmetic did the rest.

**(b) The norm governs the wrong margin.** "New domain doctrine gets a module,
not a rulebook section" (D-031, `DECISIONS.md:624`) was *followed* — no new
domain doctrine entered the rulebook after M58. The file still grew 44%,
because the actual growth mode is not new domains but the **thickening of
existing cross-skill sections**, which D-031 explicitly reserves as monolithic.
The norm and the growth never meet.

**(c) The dominant inflow is rationale, not rules.** Reading the grown
sections against their D-entries shows the rulebook absorbing decision
*context* — dates, measured values, incident anecdotes, rejected alternatives
— that `DECISIONS.md` already owns. Examples, all always-read:

- `tracking-rules.md:91–94`: the "LESSONS.md sat at 49 lines… while its
  character mass grew 13%" anecdote — D-049's Context block
  (`DECISIONS.md:1213–1226`) restated.
- `tracking-rules.md:113–117`: the "one line reached 3,152 characters in an
  adopting repo… rewrote that stamp and still left it at 2,568" incident —
  D-052's Context (`DECISIONS.md:1360–1377`) restated. This one incident is
  now told in **four places**: D-052, the rulebook, the
  `cairn_scripts.py:86–104` comment, and the `cairn_validate.py:119–138`
  docstring.
- `tracking-rules.md:154–160`: the hygiene-stamp rule spends 7 lines, of which
  ~2 are the rule ("replaced each pass, never appended; one line, <400 chars")
  and ~5 are the IP4 defense D-052 already records.
- `tracking-rules.md:187–199`: D-051's retirement criteria restated with the
  discriminating-word argument, the trimmed-remainder rule's justification,
  and the retirement-vs-correction distinction — 13 lines where the rule
  itself is ~5.
- `tracking-rules.md:216–222`: D-050's release-timing rationale ("deps going
  green says only that the *bundle* is complete…") — argumentation, not rule.

The rulebook's own first paragraph states the boundary this violates:
"Substance lives in the owner; any other file gets at most a one-line
cross-reference" (`tracking-rules.md:11–13`). That rule was written about
tracking files and has simply never been applied to the rulebook itself
relative to `DECISIONS.md`. RR01's frame — "every milestone has a legitimate
reason to add a rule" — was accurate but incomplete: milestones add a rule
*plus its legislative history*, and the history is 2–4× the rule.

On the execution question: rec 7's prune (default-branch recipe stated once,
de-enumeration) was indeed only partly done — the canonical recipe still runs
14 lines in the rulebook (`tracking-rules.md:322–337`) — but finishing it
recovers perhaps 15–20 lines. Not the story.

## 2. Is per-file, hand-derived thresholding the right mechanism class?

The nine milestones are not one mechanism, and the verdict splits cleanly
along the seam:

- **M32 (terminal-row retention), M92 (lesson retirement)** — *outflow*
  mechanisms. Both settled on first shipping; neither has needed a patch.
  Verdict (a→settled): right class, keep.
- **M55, M77 (cap-boundary exemptions, D-030/D-046), M69 (diagnostic)** —
  convergence on *what the item cap measures*. Each was a one-way narrowing
  driven by a live collision with IP4 or review-ownership; the series
  terminated (nothing since M77 has touched the boundary). Verdict (a): normal
  convergence of a young mechanism, now converged.
- **M84 → M87 → M93 → M94 — the character-mass family.** This is where the
  churn lives, and here the verdict is **(c): the mechanism class is wrong for
  prose files.** Three structural reasons:
  1. **The thresholds are nonstationary by design.** D-049's own derivation
     doctrine notes that the prescribed remedy (compression) *raises the
     measured mean item length*, so "a mean carried over from last time is
     stale by construction" (`cairn_scripts.py:68–70`, `DECISIONS.md:1228–1235`).
     A mechanism whose correct value moves every time its remedy is applied has
     re-derivation as a permanent operating cost, not a convergence cost.
  2. **Each proxy refinement discovers the next blind spot.** Whole-file lines
     missed intra-line mass (M84); whole-file mass used assumed means (M87);
     both whole-file axes missed single-line accretion (M93); and the two
     largest files have no axis at all (M94). The family grows O(files × axes)
     hand-maintained numbers, each with a derivation comment, a
     stated↔enforced coupling test, and a mutation registration — M94's AC3
     alone demands pinning "**every** site the number appears"
     (`M94-always-read-weight-signal.md:53–59`).
  3. **The governance now outweighs the governed.** The Weight-caps section
     grew +59 lines since RB01 — more than the rec 9 extraction saved (−53).
     See Beyond the brief.

**What replaces it, for prose/n=1 files** (the item-list caps stay as they
are):

- **Growth-rate / recency signals — adopt.** See Q3; this is the instrument
  that fits a file with no item structure and no population.
- **Budget-based allocation across files — reject.** A budget is one more
  hand-derived number with even less basis (the allocation *between* files has
  no oracle either), and it aggregates the n=1 problem rather than solving it.
- **Structural add-by-replacing-one — reject as a hard rule, adopt as a soft
  norm.** As a gate it is wrong (some milestones legitimately add without an
  offset — M92's retirement rule had nothing to replace). As a stated norm —
  *a rulebook-touching milestone names the lines it removes, or states in the
  work log why none* — it is the missing outflow pressure at near-zero cost.
- **No mechanism beyond periodic human review — reject alone, adopt with
  instrumentation.** Periodic human review is in fact what caught this (the
  maintainer noticed slowness) — but it took 30 milestones, because no routine
  surface reports always-read mass. A dashboard line in the `/milestone` audit
  (mass + growth since last editorial pass for the always-read set) makes
  periodic review informed instead of accidental. Signals for humans, gates
  for structure.

## 3. Deriving a threshold for a file with n=1 and no oracle

**"Threshold" is the wrong instrument; the M94 deadlock is the proof, not a
failed derivation.** A level threshold encodes a claim about what size is
*right*. The derivation doctrine (`cairn_scripts.py:58–70`) satisfies that
demand for ROADMAP/LESSONS by borrowing an independent fact — the item cap —
and measuring what it permits. `tracking-rules.md` has no item cap, no item
structure, and no population, so every candidate level is circular: derived
from the file's own current or past mass. That is exactly the brief's
trilemma (above-current blesses the defect; below-current deadlocks `verify`;
baseline-anchored is correlational), and no amount of further gating will
produce a fourth option, because the doctrine's "measure, never assume" has
nothing non-self-referential to measure.

**The right instrument already exists in cairn's own toolbox: the
recency/staleness class.** The `references staleness` advisory
(`tracking-rules.md:714–724`) does not judge whether a page is *correct* — it
reports that too much time has passed since anyone *looked*, and the remedy is
to look and stamp the look. Port that to the rulebook:

- The rulebook (or a sidecar the guard reads) carries a one-line **editorial-pass
  stamp**: date + the file's mass at that pass.
- The guard in `skills/tests` fires when current mass exceeds the stamped mass
  by a stated ratio (e.g., ≥15%, a round tripwire — legitimate here because it
  asserts nothing about the right size, only that accumulated growth warrants
  a deliberate look; both of its inputs are measured).
- The escape is **performing the pass and re-stamping** — an editorial review
  that either cuts (rationale → its D-entry owner, per Q1) or records "reviewed
  YYYY-MM-DD, nothing to cut because …" in the work log of the milestone that
  ran it. Re-stamping without a recorded pass is the same offense as ticking an
  AC without evidence, and the same discipline governs it.

Properties: it cannot deadlock `verify` (the escape is always available and is
itself the desired behavior); it blesses nothing (the stamp records *reviewed
mass*, not *permitted mass*); it is a ratchet on **attention**, not size; and
its basis is defensible under the doctrine because both operands are
measurements and the ratio is a tripwire for human judgment, not a verdict.
This supersedes M94's AC2/AC3 level-threshold framing (a plan-gate amendment,
not a D-entry) and replaces the held AC3 amendment — anchoring on the M63
baseline anchors on the correlational point itself; anchor on the last
deliberate look instead. The first stamp is the post-slimming pass of
recommendation 1.

## 4. What governs an always-read file that can never shrink?

**Bound the read.** The other two options fail cleanly: unbounded whole-file
reads double every ~30 milestones (47k→95k chars M63→M93) with no ceiling,
and archival touches IP4's enumerated set for little gain (below). The mass
itself is not the defect — history legitimately grows, and IP4 is right to
protect it; the defect is that two routine surfaces read all of it:
session start at `/milestone-plan` (`skills/milestone-plan/SKILL.md:17–18`)
and every collision/search-first sweep (`SKILL.md:35–36`;
`tracking-rules.md:308–315`).

**The index already exists and cannot diverge.** The 52 `### D-0NN (date):
title` headings total 5,378 chars — 5.6% of the file — and are uniformly
substantive; 15 of them already name the entries they supersede, annotate, or
narrow in the heading itself (e.g., D-049 "…supersedes M84-D1's assumed
means", D-052 "…narrows M84, annotates D-045"). A generated external index
would be a second record of what DECISIONS holds — the divergence vector M56
and D-051 both rejected (`DECISIONS.md:1337–1340`). The in-file headings *are*
the index, at zero divergence risk.

**Protocol:** session start reads the heading lines only; the collision check
scans headings for topical overlap and reads every matched entry **whole**
before surfacing it. IP2's protocol is otherwise unchanged — a found collision
is still quoted verbatim from the full entry ("D-014 rejected X because Y"),
never from the heading. Read cost: ~5.4k chars scanned + a handful of full
entries (~2k each), versus 95k swept — roughly a 90% reduction at plan time,
which is the single largest read in the system (larger than the rulebook).

**The IP2 trade, stated honestly.** Recall shifts from full-text to
heading-plus-targeted-read: a collision whose entry heading fails to name its
subject can be missed. This is a real loss and should be recorded as a
D-entry annotating IP2's collision-check reading, not slipped in as an
optimization. Two mitigations bound it: (1) make heading quality a stated
rule — *a D-entry heading names its subject and any entry it supersedes or
annotates* — which is already the uniform practice and is checkable at
authoring time because the durable-record preview (D-036) shows every new
entry in chat pre-commit; (2) the sweep is performed by a model, not a literal
grep — headings provide anchors and the reader follows them liberally. Against
that bounded risk, the alternative is a whole-file sweep whose cost doubles on
a ~3-day cadence at current velocity and never stops growing.

**Archival with pointers — defer.** Moving superseded entries verbatim to an
archive file with a tombstone line arguably fabricates, rewrites, and
renumbers nothing, but it is IP4-adjacent machinery requiring its own D-entry,
and once the read is heading-bounded it buys almost nothing: the whole file
stays greppable on disk, and the heading scan grows at ~100 chars per
decision — decades of headroom under any plausible ceiling. Reconsider only
if the heading scan itself becomes the cost.

## 5. Is the file size the problem, or the read pattern?

**Different answers for the two files.** For `DECISIONS.md`: pure read
pattern (Q4); the size is legitimate. For `tracking-rules.md`: the read
pattern is correct and the size is illegitimate.

**Rec 15 is upheld — explicitly, not worked around.** The whole-read
guarantee earns its cost *for the cross-skill contract*, at 765 lines or any
other count, because the alternative fails structurally: the contract has no
content trigger to gate a conditional read on (unlike the validation
doctrine, whose trigger is "milestone touches numeric work" —
`tracking-rules.md:650–657`), so any sectioned read reintroduces
"skills must remember which sections apply," which is the pre-D-003 drift.
I found no fragmentation scheme that survives that objection.

**But the guarantee protects the contract, not the contract's legislative
history.** The whole-read is priced per line, so what rides inside it must
earn per-line inclusion. Q1(c) shows a substantial share of the 765 lines is
rationale owned by D-entries. An editorial pass with the single rule *state
the rule; cite the D-entry; delete the defense* plausibly returns the core to
~550–600 lines with **zero rules removed** — indicative targets from reading
each section against its D-entries: Weight caps 81→~35, Universal tracking
rules 72→~55, References pages 67→~45, Output discipline 98→~80, Git model
77→~65. (Estimates, not commitments; the pass itself is the measurement.)
The re-anchoring cost across the ~14 guard-test files is real, one-time, and
made honest by the mutation harness — the same argument D-031 used to justify
M58's extraction.

For perspective on where the read cost actually sits: a `/milestone-plan`
session start reads ROADMAP (12.6k) + active milestone + DECISIONS (95k) +
LESSONS (20.5k) + the rulebook (52.8k) ≈ **185k chars, roughly 45k tokens,
before any work begins** — and DECISIONS is over half of it. The Q4 bounded
read beats any conceivable rulebook cap on read volume; the rulebook pass is
worth doing anyway for the conduct-quality reason in Q6.

## 6. Is character mass even the right proxy?

**The causal diagnosis is unsupported, and saying so is this review's most
useful finding on this question.** The evidence for "re-read volume slowed
milestones" is: two files grew; six-milestone median wall clock rose. The
confounds are disabling:

- **Composition.** The slow window M88–M93 is dominated by the
  weight-management/meta family (M92, M93 in-window; the brief's own list has
  five of nine weight milestones on 07-18/19). Meta-milestones demonstrably
  carry more gate rounds — M94 alone burned two failed gating rounds and an
  escalation (`M94-always-read-weight-signal.md:116–118`). Gate rounds are
  human latency, the largest and least-measured term.
- **Sample.** Median of six vs. median of six, wall clock including human
  think time, is directional at best — which the brief concedes.
- **The only causally isolated number in the record is the test suites' ~10%**
  — and it exonerates them.

**What cairn should measure and is not: tokens and phases, not characters and
files.** Character mass is a fine proxy for *read tokens* (~4 chars/token) but
nobody has connected read tokens to wall clock. Claude Code session
transcripts (JSONL) record per-message token usage; a per-milestone
"input tokens by phase + compaction events" line — extractable mechanically,
no new tracking file — would settle attribution in one or two milestones of
data. Run that before any further weight machinery ships; if re-read volume is
not the driver, the next M84-class milestone is spent on the wrong term.

**Independent of latency, the growth is still a real defect** — on two costs
character mass does track: context-window pressure (compaction risk mid-phase,
which stateless resume exists to avoid) and **instruction dilution** — a
765-line conduct spec competes with itself for the model's attention, and the
observable is drift incidents (the D-019 prose-options class), also currently
unmeasured. GP1's "caps + archiving keep always-read files small"
(`DESIGN.md:94–95`) is false today of the two largest always-read files
regardless of what caused the slowdown. Fix the growth on its merits; just
don't book the ~23→~39 min against it without the token data.

---

## Beyond the brief

- **Weight governance is the largest single contributor to the growth it
  exists to govern.** The Weight-caps section grew 22→81 lines since RB01
  (+59), exceeding the rec 9 extraction's savings (−53). Nine milestones of
  weight work made the always-read core *bigger*. Any future weight mechanism
  should be presumed guilty of this until its rulebook footprint is counted in
  its cost.
- **The same incident is told four times.** The 3,152-char stamp story
  appears in D-052, `tracking-rules.md:113–117`, `cairn_scripts.py:86–104`,
  and `cairn_validate.py:119–138`. The derivation-comment doctrine is right to
  demand the derivation be recorded — once. Source comments should cite the
  D-entry, not retell it.
- **`LESSONS.md` sits 6 chars under its density threshold** (20,494 vs
  <20,500). The next capture triggers a compression pass. Expected behavior,
  worth knowing before the next review's hygiene step.
- **M94's AC4 presumes the instrument this review rejects** — a level
  threshold for DECISIONS validated by a fire/quiet split across nine repos.
  Under recommendation 3, the DECISIONS remedy is a bounded read, not a mass
  advisory; AC4 should be amended alongside AC2/AC3 rather than implemented
  as written.
- **Growth rate confirmation:** 536→765 lines over M63–M93 ≈ +7.6
  lines/milestone, consistent with the brief's +6.7 from M58.

## Recommendations

Each marked **apply / consider / reject-with-reason**, with the question it
follows from. Where a standing ruling is touched, it is named.

1. **Apply (Q1, Q5) — a one-time editorial slimming milestone for
   `tracking-rules.md`:** move restated rationale, derivation narratives, and
   incident anecdotes to their D-entry owners, leaving the rule plus a
   parenthetical D-cite; finish RR01 rec 7's prune while in there. Target
   ~550–600 lines, zero rules removed; re-anchor guards via the mutation
   harness. This supersedes no standing entry — it *enforces*
   `tracking-rules.md:11–13`'s own ownership boundary against the rulebook
   itself, and repeats M58's playbook under D-031's existing authority.
2. **Apply (Q3) — replace M94's level threshold with a growth-since-last-
   editorial-pass ratchet** for `tracking-rules.md`: dated stamp recording
   reviewed mass; `skills/tests` guard fires at ≥15% growth over the stamp;
   the escape is performing and recording the pass, never silently
   re-stamping. First stamp = recommendation 1's pass. Supersedes M94 AC2/AC3
   as written and the held AC3 amendment (baseline anchoring is
   correlational); amend at the plan gate. D-049 is untouched — it governs the
   item-capped files, where its derivation remains sound.
3. **Apply (Q4) — bound the `DECISIONS.md` read:** session start and
   collision/search-first sweeps scan the `### D-` headings and read matched
   entries whole; add the heading-quality rule (a heading names its subject
   and any superseded/annotated IDs). Record as a new D-entry annotating
   IP2's collision-check reading, stating the recall trade openly. Amend M94
   AC4 accordingly (the mass advisory becomes moot, or is retargeted to
   heading-discipline). IP4 untouched — nothing is edited, moved, or deleted.
4. **Apply (Q6) — instrument before further mechanism:** extract per-phase
   input-token and compaction counts from session transcripts for the next
   2–3 milestones, and add an always-read mass + growth line to the
   `/milestone` audit output so the periodic human review that actually
   catches these things is informed rather than accidental. No new tracking
   file; no threshold.
5. **Consider (Q2) — the soft offset norm:** one rulebook sentence — *a
   milestone adding rulebook lines names the lines it removes, or logs why
   none* — as standing outflow pressure. Costs three lines against the
   pattern's demonstrated +7.6/milestone; drop it if recommendation 2's
   ratchet alone proves sufficient after a few cycles.
6. **Consider (Q4) — archival-with-tombstone for superseded D-entries**, only
   if the heading scan itself ever becomes the cost; needs its own
   IP4-adjacent D-entry. Decades of headroom at current velocity; not now.
7. **Reject (Q2) — cross-file budget allocation:** the allocation between
   files has no oracle either, so it aggregates the n=1 derivation problem
   into one bigger hand-derived number, and every reallocation is a fresh
   gating round of exactly the kind M94 just failed twice.
8. **Reject (Q5) — any conditional or sectioned read of the cross-skill
   contract:** RR01 rec 15 is upheld on its original grounds, sharpened here —
   the contract has no content trigger to gate a partial read on, so
   fragmentation necessarily recreates pre-D-003 drift. The size problem is
   solved by evicting non-contract content (rec 1), not by reading the
   contract partially.
9. **Reject (Q2) — "no mechanism, periodic review alone":** the unassisted
   form took 30 milestones and a felt slowdown to fire. Recommendation 4's
   dashboard is the minimum instrumentation that makes it a mechanism.
