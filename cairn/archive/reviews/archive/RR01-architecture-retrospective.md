# RR01: Whole-architecture retrospective

- **Date:** 2026-07-13
- **Brief:** `cairn/reviews/RB01-architecture-retrospective.md`
- **Reviewer:** independent Fable-tier review (RB/RR protocol, D-004)
- **Materials read:** all 9 SKILL.md files; `skills/shared/tracking-rules.md`;
  the three shipped profiles + `cairn/PROFILE.md`; DESIGN, DECISIONS (targeted
  D-001…D-029), LESSONS, ROADMAP; all 5 hooks + `cairn_common.py`; all 4
  scripts + `cairn_scripts.py`; templates; README head; `.claude-plugin/plugin.json`.
  Sanity: all three verify suites run green (134 + 65 + 32 = 231 tests).

---

## 1. DESIGN.md vs. reality

DESIGN.md is mostly honest but has four concrete drifts, one of them
public-facing.

- **The hooks bullet is stale.** DESIGN.md (Architecture, the `hooks/` bullet)
  lists "SessionStart context injection, Stop-guard …, PreToolUse merge-guard
  … technically backing IP1" — three hooks. The repo ships **five**:
  `commit_guard.py` (default-branch commit nudge) and `memory_guard.py` (GP4
  nudge, D-017) are absent from the architecture list. The rulebook's "Memory
  intake gate" names memory_guard, so the rulebook is ahead of DESIGN — the
  file that claims to document "architecture as it **is**" is the one behind.
- **"Known issues — Unpiloted (see M02/M03)" is no longer honest.** Fifty-two
  milestones are done; three real migration pilots ran (tidymedia M03,
  ackwards M20, intraclass M41 — each with recorded gotcha ledgers in
  `references/`); trigger descriptions and caps have been tuned repeatedly
  (D-018, D-023, M21, M32). The honest known-issues list today is different:
  *never run by anyone but the author; never run on a repo the author didn't
  shape; hooks unverified on Windows; conduct rules verified as prose
  (guard tests) but only spot-verified as runtime behavior.* Replace the
  section — a stale Known-issues section is worse than none, because it
  signals the honesty mechanism itself has rotted.
- **IP1's wording predates the default-branch generalization.** DESIGN.md:
  "Nothing reaches **main** without explicit user approval." M25 removed every
  hardcoded `main` from the operational surface (the rulebook says "the
  default branch" throughout, with a canonical detection recipe); the
  top-level inviolable principle still hardcodes the name. Wording only — but
  IP wording is exactly where wording is load-bearing.
- **The outward-facing description contradicts the architecture.**
  `.claude-plugin/plugin.json`: "Milestone-driven development workflow and
  tracking system **for R packages**…" and README ¶1: "A Claude Code plugin
  for milestone-driven **R package** development." M45–M48 made the core
  language-agnostic with three shipped profiles, and DESIGN.md says so — the
  two files an external adopter reads *first* still say R-only. This is the
  M48 "sweep all mentions" lesson (LESSONS 2026-07-13) recurring one layer
  further out: the sweep covered `cairn/` and the rulebook but not the
  manifest/README.

Smaller: the CLAUDE.md section template
(`skills/shared/templates/claude-md-section.md`) states the boundary rule
without `Lessons → LESSONS`, while tracking-rules' boundary rule and this
repo's own CLAUDE.md include it — a freshly scaffolded repo gets the stale
form. Otherwise DESIGN's claims spot-check true: scripts exist as described,
share `cairn_common`, exit 2 outside cairn repos; three profiles ship; the
"Two profiles" stale count M48's review caught is fixed.

## 2. Toolchain-profiles system — abstraction quality

The six slots are the right *axes* but one slot is a dumping ground and one
toolchain fact has no slot.

- **`test-doctrine` is carrying at least three concerns.** Compare
  `r-package.md`'s slot: test mechanics (testthat 3e, edge cases, snapshot
  policy) — genuinely test doctrine; but also **dependency-change governance**
  ("Imports/Suggests never unilateral — question-gate + D-entry"),
  **deprecation policy**, **docs-site indexing** (pkgdown reference-index
  row), **CI setup** (the M52 GitHub-Actions pair), and **fixture provenance**
  (D-028). `python.md` mirrors the same mix. The rulebook even admits it:
  "package-build rules, generated-file conventions, dependency-change and
  deprecation policy, error-condition idioms — now live in … `test-doctrine`
  and `consistency-gate`" — i.e. relocation was done by destination
  availability, not by concern. Consequence of the overload: see Q3 (universal
  doctrine got duplicated per-profile and then diverged).
- **The changelog is a toolchain fact with no slot.** `/hotfix` step 5
  hardcodes "NEWS.md entry under the development version" — an R convention —
  while the python profile's world is CHANGELOG.md (named only inside its
  `consistency-gate` prose) and a generic repo may have neither. A fourth
  toolchain (Rust: CHANGELOG.md/keep-a-changelog; Go: often none) hits this
  immediately. The fix is small: a one-line changelog declaration (file name,
  or "none") that `/hotfix`, `/cairn-release`, and the consistency-gate all
  read — either a seventh micro-slot or a mandated first line of
  `release-walk`.
- **MECE otherwise:** `verify` vs `consistency-gate` overlap in *content*
  (ruff appears in both python slots) but are cleanly distinguished by *when*
  (per-task vs review), which is the distinction the skills actually consume.
  `init-detection` and `greenfield-openers` are clean. A Rust/JS/Go profile
  maps onto the six slots without a missing axis beyond the changelog point.
- **Language still leaking into the core:** (a) tracking-rules, Git model:
  "The default branch … is a distribution channel (**`pak::pak()`** installs
  it; **pkgdown** may deploy from it)" — R-specific justification in the core
  rulebook; (b) tracking-rules, Milestone IDs: "User-facing materials
  (**NEWS.md**, README, **vignettes**, **pkgdown**) never reference milestone
  numbers"; (c) tracking-rules, work tiers: "Hotfix … **NEWS entry**";
  (d) `/hotfix` step 5 as above; (e) `cairn-init` §0 still opens its
  detection with "No DESCRIPTION file → **not an R package**: say so and ask —
  adapt … or abort" — framing non-R as the anomaly one bullet before the
  profile-selection bullet treats it as a normal case. All five are two-line
  fixes ("the profile's changelog/docs conventions"), and (e) should simply be
  deleted in favor of the profile-selection bullet below it.

## 3. The core/profile boundary (D-024/D-025)

The boundary is drawn correctly in the direction it was designed for, and
incorrectly in the direction nobody was watching.

- **Oracle doctrine universal: right.** Nothing in the Validation doctrine is
  language-mechanical. Its one candidate ("a committed generator that
  reproduces it from scratch") is stated shape-free in core and concretized
  R-mechanically in the r-package slot (`data-raw/` scripts, D-028) — exactly
  the right layering. The five-type taxonomy, the ≥2-types bar, the
  reproducibility and primary-sources hard stops are all domain doctrine that
  would read identically in a Rust numerical crate. Keep it.
- **The reverse leak is real: universal governance sits in profile slots.**
  "Dependency changes are never unilateral — question-gate + D-entry" and
  "Breaking changes … follow a deprecation cycle unless pre-1.0 and explicitly
  waived" appear near-verbatim in *both* `r-package.md` and `python.md`
  `test-doctrine` slots — and **not at all in `generic.md`**. Neither rule is
  language-mechanical: "don't add a dependency unilaterally" and "don't break
  users without a cycle" are exactly the kind of cross-cutting conduct the
  core rulebook exists to state once. The generic-profile gap is the proof of
  cost: a generic adopter (this very repo!) currently has no stated
  dependency-change gate. Move both rules up to tracking-rules (the "What gets
  a test" neighborhood or the question-gates section); profiles keep only the
  mechanical rendering ("Imports/Suggests" vs "`pyproject.toml`
  dependencies", `DeprecationWarning` vs `lifecycle`).

## 4. Shape-free oracle registry (M51)

Shape-free is a principled call on the evidence (two working exemplars with
different shapes; D-028 symmetry), but as shipped it is **half of an
auditable rule**. The content fields are fixed (ID, type, asserting
`test:line`, source, provenance) — so a record, once *found*, is checkable.
What is not fixed is **where to look**. An auditor (human or mechanical)
verifying the ≥2-types bar must first discover whether the repo's records
live in a central file, generator headers, or fixture fields — and a repo
that recorded nothing is indistinguishable from a repo whose shape you
haven't found yet. That makes the audit's *completeness* unfalsifiable, which
is the false-coverage trap (Q8) in doctrine form: the check can pass because
the checker looked in the wrong place.

The minimal structure that fixes this without forcing a shape is a
**declared registry pointer**: one line in the adopting repo's DESIGN.md
Conventions (the universal home — not PROFILE, since oracles are orthogonal
to toolchain), e.g. "Oracle records: provenance headers in
`data-raw/oracle-*.R`" or "central `cairn/ORACLES.md`". Then: absence of the
line in a repo with numeric work is itself the audit finding; presence gives
every future audit a deterministic entry point. This does not reopen D-029's
rejected validate CHECK — the doctrine stays advisory prose enforced by
review judgment; it just gains an address. A second, cheaper hardening worth
considering: fix the record's *micro-syntax* (a greppable key, e.g.
`oracle O-<id> type=<one-of-five>`) while leaving its location free — that
would make even a mechanical ≥2-types tally possible later without any new
tracking file.

## 5. The rulebook's size and cohesion (GP1)

Strictly, GP1 governs tracking files, and tracking-rules.md is plugin logic —
no letter-violation. In spirit, yes: it is a 545-line always-read file with
no cap and a demonstrated one-way growth trend (M42, M45–M46, M51 all grew
it). But the monolith is also load-bearing in three ways that argue against a
big split: (1) "skills state workflows; the rulebook states rules; nothing is
said twice" only works with one rules-home; (2) ~14 guard-test files anchor
on its exact phrasing; (3) skills read it whole, so an extraction that skills
must *remember* to read separately recreates the drift D-003 solved.

The right cuts respect that:

- **Move (one file, still core, still universal): the Validation doctrine +
  oracle registry + sources/ingestion block** (~60 lines, "Validation
  doctrine" through "Source ingestion") to
  `skills/shared/validation-doctrine.md`, referenced from the rulebook in
  three lines. It is the only rulebook section that is *conditionally*
  relevant (repos with numeric results), it is self-contained, its guard
  tests (`test_oracle_doctrine.py`) re-anchor trivially, and D-024/D-025's
  "universal, not a profile slot" is about core-vs-profile, not about
  single-file packaging. Every non-statistical repo currently pays ~11% of
  the rulebook read for doctrine that never applies to it.
- **Prune (restated detail):** the default-branch detection recipe is stated
  in full in the rulebook *and* re-stated with commands in
  `/milestone-implement` step 2, `/milestone-review` step 1, and `cairn-init`
  §0 (where the restatement has drifted — see Q6). Keep the canonical recipe
  in the rulebook; skills should say "detect per the tracking-rules git
  model" and nothing more. Similarly, the Output-discipline "Phase header"
  rule enumerates every skill's H1/H2 mapping centrally (~15 lines) while
  each skill already carries its own `Phase header:` directive — state the
  two-level convention centrally and let the per-skill directives own the
  mapping.
- **Must stay monolithic:** file map + ownership table, weight caps,
  universal tracking rules, status vocabulary, sizing tiers, git/approval
  model, question gates/chips, output discipline, model strategy, the
  toolchain-profiles mechanism. These are the cross-skill contract; every
  skill genuinely consumes them.

Net effect: ~460 lines core + a 60-line conditional module, and a rule for
the future: **new domain doctrine gets a module, not a rulebook section.**

## 6. Enforcement vs. honor-system

The split is mostly in the right place — the three highest-stakes rules have
mechanical backing — but the map has soft spots and one missing cheap hook.

Enforced (mechanically): IP1's merge path (`merge_guard`, with honestly
documented bypasses — compound `git checkout main && git merge`, backticks,
`git -C`; the enforced path is the `gh pr merge` convention, which is the
path the skills actually use); tracking-dirty-at-turn-end (`stop_guard`,
cairn/ files only — deliberate and right); 14 deterministic consistency
checks (`cairn_validate`, including mirror, caps, coverage-complete,
principles-slot, profile schema); plus two advisory nudges (commit_guard,
memory_guard) that are correctly *not* blocking, per their honest "can't be
decided mechanically" rationales.

Honor-system but load-bearing, in descending order of concern:

1. **"Never force-push" has no guard.** Unlike merges, a force-push to the
   default branch is destructive, mechanically detectable at PreToolUse
   (`git push --force`/`-f` + on-default-branch, the exact machinery
   commit_guard already has), and has essentially no legitimate-in-cairn
   false-positive case. This is the one honor-system rule that clears the bar
   for a blocking hook. Recommend adding it (deny, not nudge).
2. **"Never merge red or pending CI"** — prose only; the skills' `--watch`
   discipline is the mitigation. Acceptable: a hook can't cheaply know CI
   state.
3. **Question-gate/chip conduct** is enforced only as *prose* (guard tests
   lock the skill text, not the runtime behavior). That's the architecture's
   deliberate bet; note it plainly in DESIGN's Known issues rather than
   pretending otherwise (Q1).
4. **AC fencing / never-reinterpret** — pure review-time honor. `cairn_validate`'s
   coverage-complete check covers the mappable half; the "no evidence line, no
   tick" half could be mechanized later (a validate check that a ticked AC in
   a status-`review` file has a Review-section line citing it), but it's
   judgment-adjacent; leave honor-system for now.

Brittleness found:

- **`merge_guard` consumes the marker even when the merge then fails** —
  already bitten (M33 lesson, "rewrite the marker before each retry"). The
  guard runs at PreToolUse so it cannot see the outcome; a small PostToolUse
  companion that *restores* the marker on a failed `gh pr merge` (nonzero
  exit) would remove a recurring manual step. Consider.
- **`cairn-init` §0's default-branch recipe contradicts the rulebook's.**
  cairn-init: "falling back to the current branch (`git branch
  --show-current`) whenever that fails." tracking-rules: try `origin/HEAD`,
  then `git ls-remote --symref` when a remote exists, and "Only with no
  remote at all ask the user — **never guess the local current branch**."
  cairn-init skips the ls-remote rung and guesses. Its context is more
  forgiving (init usually runs on the default branch), but a shallow-clone
  init on a feature branch would scaffold with the wrong name; and the
  rulebook rule exists precisely so no skill carries its own variant. Align
  cairn-init to the canonical recipe.
- **Stale check-enumerations in two skills.** `/milestone-review` step 4
  parenthetically lists 10 of `cairn_validate`'s 14 checks;
  `/milestone` §2 lists a different stale subset (no ISO dates, no
  coverage-complete, no principles-slot, no profile). Worse, review step 4
  then lists "Coverage completeness" as a *separate manual* bullet although
  `check_coverage_complete` has been mechanical since M34 — a reader can't
  tell what's script vs. judgment. Skills should stop enumerating the
  script's internals ("run it; it prints one line per check") — the
  enumeration is a stale-count trap (M28 lesson) built into two skills.

## 7. The principles (IP1–IP3, GP1–GP4)

All seven are load-bearing; none is filler. IP1: mechanically backed
(merge_guard), cited everywhere. IP2: directly shapes the plan collision
check's "surfaced, never silently obeyed/overridden" protocol and the RR
ingestion rule. IP3: generates real machinery (remainder ledger, migration
ledger, the sub-80-score logging rule, greenfield "bank one candidate row").
GP1: drives caps/archiving (and is the axis of the Q5 tension — a healthy
sign that it's real). GP2: one status authority + stateless resume are the
system's spine. GP3: the profiles work is GP3 executed. GP4: has its own
hook and two D-entries. The two-strength system earns its keep concretely:
the M17 IP2→IP3 miscitation was caught *because* citations are checkable
ids, and IP-change friction (D-entry required) has been exercised.

**One de-facto inviolable is unnamed: history integrity.** The architecture
treats "never fabricate, never rewrite, never renumber" as inviolable in at
least five places — append-only work-logs/DECISIONS ("supersede, never edit
history"; "Never fabricate history"), IDs never reused, the migration
no-invention rule, entomb-verbatim (D-005), catch-up-line reconciliation —
and violating it is never offered as a tradeable option anywhere. That is an
IP in fact but not in name, which matters because the IP list is what
`/design-interview`, `cairn_impact`, and the RB `ip-touching` tripwire key
on: today, work that would weaken the no-invention rule would not trip the
`ip-touching` tripwire. Name it IP4.

(Minor, from Q1: IP1's "main" should read "the default branch.")

## 8. Self-hosting friction as an architecture signal

Both recurring traps are structural, and both have structural dissolutions.

**False-coverage guard tests (M23, M26, M39, M40, M47, M48-F3, M50 — six-plus
occurrences).** The root cause: the architecture's chosen enforcement medium
for conduct rules is *substring assertions over prose*, and `assertIn` over a
545-line file is satisfied by any prior occurrence of the token — so every
new guard is one lazy anchor away from asserting nothing. The lessons pile up
because each lesson refines *authoring discipline* while the *verification of
guards* stays manual ("sanity-check by mentally deleting the feature" —
M40's own words, and M40 itself then shipped the trap). The structural fix is
to make M40's mental deletion mechanical: a **mutation harness for
prose-guards** — a meta-suite that, for each registered (rule-block, guard)
pair, deletes/blanks the block in an in-memory copy and asserts the guard
*fails*. A guard that survives its rule's deletion is false coverage by
definition, caught at authoring time instead of by the diff-bug lens four
milestones later. The registration cost is one table; the class of defect
disappears rather than being re-learned. (This is the plugin applying its own
oracle doctrine to itself: a guard test's oracle is "fails when the rule is
absent," and today that oracle is run by hand, sometimes.)

**150-line cap vs. review evidence (M19, M22, M33, M50).** Root cause: one
file serves two masters on opposite schedules — the plan document must stay
small for the whole milestone, and the Review section *grows precisely at the
end*, when the file is at its fullest; the same cap covers both. The current
remedies (strip scaffolding comments, compress task lines) are one-time
reserves that M50 already exhausted ("no `<!-- owner -->` comments left to
trim"). Dissolve it by making the cap match the ownership model it already
has: **cap the plan-owned body and exempt (or separately budget) the
review-exclusive section** — mechanically, `check_caps` counts a live file's
lines *excluding* the `## Review` section, or equivalently caps plan+log at
120 and Review at 40. The file's smallness goal survives (the archive
compresses to ≤25 lines days later anyway); the recurring end-of-milestone
scramble — which twice damaged content (M33's collapsed header) — ends. The
alternative (raise the cap to 180) is worse: it spends the headroom on plan
bloat, which the cap exists to prevent.

The meta-signal: both traps recur because LESSONS.md is the system's only
home for "known failure mode," and lessons don't execute. LESSONS is also now
at 49/50 lines — the cap will soon force pruning exactly the M39/M40-class
lessons the traps depend on remembering. When the same lesson class hits
three entries, that's the tripwire for converting it into mechanism (a
harness, a validate check, a cap change) — worth stating as a rule in the
rulebook's LESSONS ownership row.

## 9. The skill surface

The nine-skill decomposition is right, and the routing-chip glue is sound —
D-019/D-022 sanded off its two real frictions (review's dead-end chip;
hand-back-instead-of-invoke), and the phase seams coincide with the
`/clear` seams, which is the architecture's best idea (Q11). No skill should
merge; none is missing (release, brief, and interview each have distinct
gates that would blur inside a phase skill).

Two scoping notes:

- **`cairn-init` is two skills in one file.** Scaffold+repair (~§0–§1, ~155
  lines) is the common path; the migration protocol (§2, ~150 lines,
  three-pilot-deep with lineage-specific dispositions) loads on every
  greenfield scaffold that will never migrate anything. The decomposition
  *within* the file is clean, so the cheap fix is progressive disclosure, not
  a new skill: move §2 to `skills/shared/migration-protocol.md`, read only
  when §0 detects an existing footprint — same pattern as the rulebook
  itself. (A separate `/cairn-migrate` skill would also work but adds a
  routing surface for a once-per-repo event; not worth it.)
- **`milestone-review` at 201 lines is dense but correctly scoped.** The
  fan-out + scorer is one coherent gate; splitting it would scatter the
  evidence-fencing rules. The only trim: the verbatim false-positive taxonomy
  and scorer rubric could live in a shared reviewer-prompts file, but at ~12
  lines the extraction barely pays. Leave it.

One glue-model residual: each chip-hop re-reads the 545-line rulebook
("read … first" in every skill). In-session that's cached context; the real
cost is Q5's, not the chips'.

## 10. Readiness for external adopters (v1.0)

Ranked. The theme: the *system* is more general than its *packaging*, and
everything has been verified in exactly one environment (the author's macOS +
Claude Code + full model roster).

1. **Positioning says R-only (fix first, it's an hour).** `plugin.json`
   description and README ¶1 both say R packages (Q1). The first Python
   adopter reads "for R packages," and either leaves or distrusts every
   generic claim after it. Also in this bucket: `cairn-init` §0's "not an R
   package — adapt or abort" framing, and `/hotfix`'s hardcoded NEWS.md.
2. **Environment assumptions are unverified outside the author's machine.**
   `hooks.json` invokes `python3` — on stock Windows there is no `python3`
   on PATH (it's `py`/`python`), so every hook silently dies or errors each
   session; skills assume an authenticated `gh` CLI (`/milestone-review`
   cannot reach its merge gate without it); the model strategy assumes
   Sonnet/Opus/Fable are all available (a Pro-plan adopter has no Fable, and
   the review fan-out's tiering degrades undefined). De-risk: an environment
   check in `/cairn-init` (python3, git, gh, remote) with documented
   degradation paths, and a stated fallback for each model tier.
3. **Migration is three-pilot-deep on the author's own precursor lineages.**
   §2's footprint recognition keys on the author's precursor systems
   (Lineage A/B); the "unrecognized footprints get an interview" fallback is
   the right design but has never fired. The first external migration will
   also collide with `cairn_validate`'s caps mid-flight (a 300-row legacy
   backlog vs. the 60-line ROADMAP; clustering remedy exists as prose only).
   De-risk: one external-repo migration pilot before 1.0, or a read-only
   migration **dry-run mode** ("here is the inventory and proposed ledger;
   nothing written") that makes the first contact safe by construction.
4. **The merge model assumes the `gh pr merge`-from-CLI workflow.** Adopters
   with branch protection + merge queues, or who merge in the GitHub UI,
   bypass merge_guard entirely (guard sees only agent Bash) and then hit the
   post-merge hygiene pass out of order. Nothing breaks catastrophically,
   but the docs should say which parts of the approval model survive a
   UI-merge workflow and which quietly become honor-system.
5. **First-session comprehension.** A new adopter's agent conduct depends on
   a 545-line rulebook read the human never sees, and the human-facing
   surface (README) doesn't yet state the ~10 things the *human* must know
   (chips are stops; merges need your explicit approval; `cairn/` files
   outrank chat; how to bail out). A one-page "what cairn will and won't do
   without asking" is cheap 1.0 insurance against the trust-destroying first
   surprise.

## 11. Overall verdict

What's genuinely good and should be protected: the **logic/state split with
one shared rulebook** (D-001/D-003) — rules stated once, skills thin, drift
structurally impossible across repos; the **stateless-resume discipline**
(stop points = commit points = clear points) which makes every seam in the
workflow a safe interruption point and is the single design choice that most
distinguishes cairn from prompt-pile "workflow" systems; the **supersede-
never-edit decision ledger**, whose quality (D-023, D-028, D-029 carry their
own reversal instructions) is what made this retrospective possible at all;
and the **evidence culture** — AC fencing, fresh-evidence-only review,
the oracle doctrine — which is the same idea applied at three scales. None of
these should be "simplified." The single highest-leverage change: **build
the prose-guard mutation harness (Q8)** — the guard-test layer is the
foundation everything else's non-regression rests on, it is the layer with
the worst recurring defect record (6+ incidents), and mechanizing its oracle
converts the plugin's most-relearned lesson into a solved problem while
directly practicing the validation doctrine cairn preaches to its adopters.

---

## Beyond the brief

- **D-007 residue:** README advertises manual install "while piloting" and
  DESIGN/README both promise DRAFT_2.md's removal at 1.0 — both fine, but the
  Public-release-prep candidate row should absorb the Q1/Q10-1 positioning
  fixes so they can't be forgotten at the same moment DRAFT_2 is deleted.
- **LESSONS.md is one line from its cap** (49/50). Before pruning, mine it:
  at least two lesson *classes* (Q8) should graduate to mechanism, and the
  M23/M26/M39/M40 chain becomes obsolete the day the mutation harness lands —
  prune those *after* the harness, not before.
- **LESSONS append-only ordering has drifted:** 2026-07-13 entries (M47,
  M48) sit interleaved among 2026-07-12 lines rather than appended at the
  tail — cosmetic, but the file's own header says append-only, and ordering
  is the only structure it has.
- **No constraint found actively wrong.** D-001, D-004, D-008, D-002/D-003,
  IP1–IP3, and stdlib-only all held up under this review; nothing to
  relitigate.

## Recommendations

Ranked; each **apply** / **consider** / **reject-with-reason**.

1. **Apply — fix outward positioning before anything else ships:** update
   `.claude-plugin/plugin.json` description and README ¶1 from "R packages"
   to the profile-based framing; delete `cairn-init` §0's "not an R package —
   adapt or abort" bullet (the profile-selection bullet already owns the
   case); change `/hotfix` step 5's "NEWS.md" to the profile's changelog.
   *(Q1, Q2, Q10-1 — the architecture already generalized; the packaging
   didn't.)*
2. **Apply — build the prose-guard mutation harness:** a meta-test that
   deletes each registered rule block and asserts its guard fails; require
   new guards to register. *(Q8, Q11 — dissolves the 6-incident
   false-coverage class instead of appending lesson #7.)*
3. **Apply — exempt the review-exclusive section from the 150-line cap**
   (count live-file lines excluding `## Review` in `check_caps`, or split the
   budget 120/40) and state it in the weight-caps rule. *(Q8 — ends the
   M19/M22/M33/M50 end-of-milestone scramble without loosening plan
   discipline.)*
4. **Apply — move dependency-change gating and deprecation-cycle policy from
   the r-package/python `test-doctrine` slots up to tracking-rules**, leaving
   only the mechanical renderings in profiles. *(Q3 — universal governance is
   currently duplicated in two profiles and absent from generic.)*
5. **Apply — refresh DESIGN.md to match reality:** five hooks listed; rewrite
   "Known issues" to the current honest list (single-author, single-OS,
   prose-verified conduct); IP1 "main" → "the default branch". *(Q1, Q7 —
   DESIGN is the audit baseline; it should audit clean.)*
6. **Apply — add a registry-pointer line to the oracle doctrine:** a repo
   with numeric work declares *where* its oracle records live (DESIGN.md
   Conventions), shape still free. *(Q4 — makes the ≥2-types audit's
   completeness falsifiable without reopening D-029's rejected validate
   CHECK.)*
7. **Apply — align `cairn-init` §0's default-branch fallback to the
   canonical recipe** (ls-remote rung, then ask; never guess the current
   branch), and de-enumerate `cairn_validate`'s check list from
   `/milestone-review` step 4 and `/milestone` §2 (run-and-read, don't
   restate; drop review's now-mechanical "Coverage completeness" manual
   bullet). *(Q6 — two skills contradict or trail the single source of
   truth.)*
8. **Apply — add a force-push guard hook** (PreToolUse deny of
   `git push --force*` targeting the default branch in a cairn repo; reuse
   commit_guard's branch machinery). *(Q6 — the one high-stakes honor-system
   rule that is cheaply, false-positive-free enforceable.)*
9. **Consider — extract the Validation doctrine (+ registry, sources,
   ingestion) to `skills/shared/validation-doctrine.md`**, referenced from
   the rulebook; adopt the norm "new domain doctrine gets a module, not a
   rulebook section." *(Q5 — cuts ~11% of every session's always-read core;
   costs a guard-test re-anchor and one more file every skill must know
   exists — do it with recommendation 2 in place.)*
10. **Consider — name history integrity as IP4** ("History is never
    fabricated, rewritten, or renumbered: append-only logs, no-invention
    migration, IDs never reused"), with the D-entry it requires. *(Q7 — it is
    already inviolable in practice; naming it arms the `ip-touching`
    tripwire and `cairn_impact` for it.)*
11. **Consider — a changelog declaration in the profile schema** (file name
    or "none", read by hotfix/release/consistency-gate) when the next
    non-R/non-Python profile is authored; until then recommendation 1's
    hotfix wording change suffices. *(Q2.)*
12. **Consider — progressive disclosure for `cairn-init` §2:** move the
    migration protocol to a shared file read only when a precursor footprint
    is detected. *(Q9 — halves the common-path skill read; zero behavior
    change.)*
13. **Consider — a PostToolUse companion for merge_guard** that restores the
    consumed marker when the guarded merge command exits nonzero. *(Q6 —
    removes the M33 rewrite-the-marker manual step; small, but touch the
    approval path carefully and test the retry flow live.)*
14. **Consider — pre-1.0 external de-risking:** an environment check in
    `/cairn-init` (python3/git/gh, with a Windows launcher fallback in
    hooks.json), a migration dry-run mode, and a one-page human-facing "what
    cairn does without asking" README section. *(Q10-2/3/5.)*
15. **Reject — splitting the rulebook into per-skill fragments** (beyond
    recommendation 9): the single-file rulebook is what makes "nothing is
    said twice" and whole-read guarantees work; fragmenting it recreates the
    pre-D-003 drift the plugin exists to prevent. *(Q5.)*
16. **Reject — merging or hard-splitting any of the nine skills** (beyond
    12's content move): the phase seams match the gate/clear seams, and
    each skill's trigger surface is distinct; restructuring buys nothing the
    chip glue doesn't already provide. *(Q9.)*
17. **Reject — mandating a central `ORACLES.md` or a validate CHECK for the
    oracle doctrine:** D-029's reasoning held up under review — two working
    exemplar shapes exist, and the doctrine is review-judgment territory;
    recommendation 6's pointer line is the auditability fix that preserves
    both. *(Q4.)*
