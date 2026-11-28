# RB01: Whole-architecture retrospective (standing — no milestone)

- **Date:** 2026-07-13
- **Output required:** write findings to `cairn/reviews/RR01-architecture-retrospective.md`

You are performing an independent expert architectural review of a mature-but-
pre-1.0 codebase. This brief is fully self-contained — do not assume any
conversation context. Read the files this brief directs you to, answer the
numbered questions **by number**, and write your findings to the output path
above.

This is a retrospective, not a gate on a specific change: the question is
**what went well, and what should change** across the architecture as it
stands today. Be candid and specific. A finding that names a file, a line, a
principle, or a D-entry is worth ten that gesture at "the design." Prefer
concrete "change X to Y because Z" over praise.

## Background

**What cairn is.** A Claude Code *plugin* (not an application) that gives an
AI coding agent one canonical, milestone-driven development workflow plus a
markdown project-tracking system. It ships:

- **Skills** (`skills/<name>/SKILL.md`, 9 workflow skills) — the operational
  logic an agent runs: `/milestone-plan → /milestone-implement →
  /milestone-review`, plus `/hotfix`, `/milestone` (status), `/cairn-init`
  (adoption/migration), `/cairn-release`, `/milestone-brief` (Fable
  escalation — the skill that produced *this* brief), and `/design-interview`.
- **The rulebook** (`skills/shared/tracking-rules.md`, ~545 lines) — a single
  shared file every skill reads first and never restates. It owns the file
  map, weight caps, git/approval model, sizing tiers, question-gate
  discipline, model/agent strategy, toolchain-profile mechanism, and the
  numeric-validation ("oracle") doctrine.
- **Templates + profiles** (`skills/shared/templates/`,
  `skills/shared/profiles/`) — milestone/brief/decision/CLAUDE.md-section
  templates; three shipped toolchain profiles: `r-package`, `python`,
  `generic`.
- **Hooks** (`hooks/*.py`, stdlib-only) — the enforcement layer: SessionStart
  context injection (`session_context.py`), a Stop-guard on uncommitted
  `cairn/` tracking (`stop_guard.py`), a commit-guard (`commit_guard.py`), a
  PreToolUse merge-guard keyed on a single-use `cairn/.merge-approved` marker
  (`merge_guard.py`, technically backs IP1), and a non-blocking memory-boundary
  nudge (`memory_guard.py`). All no-op outside a cairn repo.
- **Scripts** (`scripts/*.py`, stdlib-only) — the deterministic read layer:
  `cairn_status` (snapshot), `cairn_next` (Depends-on readiness),
  `cairn_validate` (mechanical consistency gate), `cairn_impact` (principle →
  citing file:line). Read-only; share the hooks' `cairn_common` parser.

**State model.** Logic lives in the plugin; *state* lives in each adopting
repo under `cairn/` (ROADMAP = sole status authority; DESIGN = architecture;
DECISIONS = append-only cross-cutting decisions; LESSONS; milestone files;
references; reviews). This repo **dogfoods its own format by hand** under
`cairn/`, running the `generic` profile.

**Recent architectural evolution (the deltas that prompted this review).**

- **Toolchain-profiles system** (M45 spine → M46 rewire → M47 release →
  M48 python profile → M52 CI). Before this, the core rulebook hardcoded one
  language's commands (R/devtools/testthat). The profile mechanism pulled all
  language/toolchain specifics into `cairn/PROFILE.md`'s **six slots** —
  `verify`, `consistency-gate`, `test-doctrine`, `release-walk`,
  `init-detection`, `greenfield-openers` — that the operational skills read
  instead of hardcoding. Three reference profiles ship. Deliberate carve-out:
  D-024/D-025 keep the numeric-validation (oracle) doctrine **universal**, in
  the core rulebook, *not* a profile slot.
- **Shape-free oracle-registry doctrine** (M51). The validation doctrine
  requires every numeric result to be backed by ≥2 *independent oracle types*
  (frozen / live / invariant / closed-form / simulation-coverage), and
  requires an oracle *registry* recording each oracle by ID, type, asserting
  `test:line`, source, provenance — but the registry's **shape is the repo's
  choice** (central file, generator headers, or fixture-embedded fields), so
  long as the ≥2-types audit can read off it.
- **Greenfield openers** (M50) — the `greenfield-openers` profile slot:
  opener questions `/cairn-init` asks when adopting into a new/empty repo of a
  given toolchain type.

**Why an independent review.** The author has deep diff-blindness after ~50
milestones of self-hosted evolution. The tracking files (DESIGN, DECISIONS,
LESSONS) are dense with rationale, which makes drift between *documented*
architecture and *actual* architecture hard for the author to see. This repo
is heading toward a public v1.0 (see the ROADMAP "Public release prep"
candidate), so now is the moment to catch structural debt before external
adopters inherit it.

## Materials

Read these in roughly this order. Sizes noted so you can budget.

**Core architecture + doctrine (read fully):**
- `cairn/DESIGN.md` (~84 lines) — the architecture as documented, incl.
  principles IP1–IP3, GP1–GP4. This is the **audit baseline**: your job
  includes checking whether the code matches this doc.
- `skills/shared/tracking-rules.md` (~545 lines) — the whole rulebook. The
  single most load-bearing file in the repo.
- `cairn/PROFILE.md` (~58 lines) — this repo's own (`generic`) profile.
- `skills/shared/profiles/generic.md`, `python.md`, `r-package.md`
  (~54/95/93 lines) — the three shipped reference profiles. Compare their
  slot structure.

**Decisions (read the entries these IDs point to; the file is ~595 lines —
don't read cover-to-cover, target these):**
- `cairn/DECISIONS.md` — especially D-001 (plugin distribution), D-002
  (per-milestone files + ROADMAP index), D-003/D-019/D-022 (separate phase
  skills glued by routing chips, and their refinements), D-004 (Fable gate),
  D-008 (`cairn/` dir), D-009/D-018 (CLAUDE.md carries routing not conduct;
  the cap measures only the cairn section), D-011 (generalizable fixes → the
  plugin, not memory), D-016 ("Never Haiku"; scorer on Sonnet), D-020/D-021
  (TOC driven by chapter markers, not headers), **D-024/D-025** (oracle
  doctrine stays universal; the five-type taxonomy), D-026/D-027 (candidate
  triage / what was deliberately *not* built).

**The skills (skim all; read the three phase skills closely):**
- `skills/milestone-plan/SKILL.md` (~117), `milestone-implement/SKILL.md`
  (~102), `milestone-review/SKILL.md` (~201) — the core loop; review is the
  largest and runs the reviewer fan-out.
- `skills/cairn-init/SKILL.md` (~309 — the largest skill; adoption +
  migration), `hotfix` (~61), `milestone` (~102), `cairn-release` (~79),
  `milestone-brief` (~77), `design-interview` (~120).

**Enforcement + read layers (read to judge doc-vs-enforcement gaps):**
- `hooks/hooks.json`, `hooks/session_context.py`, `stop_guard.py`,
  `merge_guard.py`, `commit_guard.py`, `memory_guard.py`, `cairn_common.py`.
- `scripts/cairn_validate.py`, `cairn_impact.py`, `cairn_next.py`,
  `cairn_status.py`. Note what each mechanically checks vs. what the rulebook
  states as a rule (some rules are enforced, many are honor-system prose).

**Ground truth for lived friction:**
- `cairn/LESSONS.md` (~50 lines) — 30+ hard-won lessons from self-hosting.
  Read these as a signal of where the architecture generates recurring
  friction (e.g. the repeated "false-coverage trap" lessons M39/M40/M48/M50;
  the repeated 150-line-cap-at-review lessons M19/M22/M33/M50).
- `cairn/ROADMAP.md` — current status + the candidate backlog.

Do **not** read `DRAFT_2.md` (a pre-1.0 rationale draft being retired) except
to spot-check a claim; treat DESIGN.md as authoritative.

## Questions

Answer each by number in the RR.

1. **DESIGN.md vs. reality.** Read DESIGN.md as a contract, then spot-check it
   against the code. Where has the *actual* architecture drifted from what
   DESIGN.md documents? Name specific mismatches (stale counts, unlisted
   components, described behavior the code no longer has). Is the "Known
   issues" section ("Unpiloted") still honest?

2. **Toolchain-profiles system — abstraction quality.** Are the **six slots**
   (`verify`, `consistency-gate`, `test-doctrine`, `release-walk`,
   `init-detection`, `greenfield-openers`) the right decomposition — mutually
   exclusive, collectively exhaustive for what "a language toolchain" varies?
   Compare `generic.md` / `python.md` / `r-package.md`: is any slot carrying
   two concerns, or missing one an adopter of a fourth toolchain (Rust, JS/TS,
   Go) would need? Is anything language-specific still leaking into the core
   rulebook that should have moved to a slot?

3. **The core/profile boundary (D-024/D-025).** The oracle/numeric-validation
   doctrine was deliberately kept **universal** (core rulebook), not a profile
   slot, on the theory that it's domain doctrine orthogonal to language. Is
   that boundary drawn correctly? Is there anything *in* the universal oracle
   doctrine that is actually language-mechanical (and should move to a slot),
   or anything in a profile's `test-doctrine` slot that is actually universal
   doctrine (and should move up)?

4. **Shape-free oracle registry (M51).** The registry is deliberately
   *shape-free* — repos may record oracles in a central file, generator
   headers, or fixture fields. Does "shape-free" undercut the ≥2-types audit
   it exists to enable? Concretely: can a mechanical check (or even a
   disciplined human reviewer) actually verify the ≥2-independent-types bar
   when the record has no fixed shape? Is this a principled flexibility or an
   un-testable rule? If the latter, what minimal structure would make it
   auditable without forcing one shape?

5. **The rulebook's size and cohesion (GP1 self-consistency).** GP1 says cairn
   values *efficient, small, always-read files* (caps + archiving). The
   rulebook is ~545 lines and every skill reads it first, every session.
   Does cairn violate its own GP1 here? Is `tracking-rules.md` accreting
   (does any section belong in a profile, a skill, or an archive)? If you were
   to split or prune it, what would you cut or move, and what must stay
   monolithic because skills depend on reading it whole?

6. **Enforcement vs. honor-system.** Cross-reference the rules stated in the
   rulebook against what the hooks/scripts *mechanically* enforce. Which
   high-stakes rules are enforced (IP1 via `merge_guard`, tracking-with-code
   via `stop_guard`, consistency via `cairn_validate`), and which load-bearing
   rules are prose-only and rely on the agent choosing to comply? Is the
   enforced/honor-system split in the right place — anything currently
   honor-system that a hook should catch, or any hook that's brittle
   (false-positive/negative prone)?

7. **The principles (IP1–IP3, GP1–GP4).** Are these the right principles at
   the right strength? For each: is it actually load-bearing (cited, enforced,
   or shaping decisions), or aspirational filler? Is any *de-facto* inviolable
   principle missing from the list (something the architecture clearly treats
   as inviolable but never named)? Is the IP/GP two-strength system itself
   earning its keep?

8. **Self-hosting friction as an architecture signal.** LESSONS.md records
   recurring traps from dogfooding — notably the "false-coverage" guard-test
   trap (M39/M40/M48/M50) and the milestone-file 150-line-cap-collides-with-
   review-evidence trap (M19/M22/M33/M50). When the *same class* of problem
   recurs 3–4 times despite being known, that's an architectural smell, not
   bad luck. What underlying design choices generate these recurring traps,
   and what structural change would dissolve them (vs. the current approach of
   adding another lesson each time)?

9. **The skill surface.** Nine skills, glued by routing chips (D-003/D-022).
   Is the decomposition right — any skill that should merge, split, or not
   exist? `cairn-init` is the largest at ~309 lines (adoption + migration in
   one skill); `milestone-review` at ~201 runs a 3-reviewer + scorer fan-out.
   Are these over/under-scoped? Is the routing-chip gluing model sound, or does
   it fragment a workflow the agent should hold whole?

10. **Readiness for external adopters (v1.0).** This has only ever been run by
    its author, self-hosted, on the `generic` profile. What will break or
    confuse the *first external adopter* — someone running `/cairn-init` on a
    real R or Python package they didn't build with cairn in mind? Name the
    top 3–5 risks to de-risk before a public 1.0, ranked.

11. **Overall verdict.** In one paragraph: what is genuinely *good* here that
    should be protected from well-meaning refactors, and what is the single
    highest-leverage change you'd make if you could make only one?

## Constraints

These are settled architecture; **do not relitigate them** — but if your
review finds one is actively wrong, say so explicitly under "Beyond the brief"
rather than silently assuming it away.

- **D-001:** cairn is distributed as a Claude Code plugin (not a CLI/library).
- **D-004 / the Fable gate:** Fable subagents run only through this RB/RR
  protocol, gated per instance. (This is the mechanism that produced this
  brief.) It is not up for redesign here.
- **D-008:** the tracking directory is `cairn/`.
- **D-002 / D-003:** per-milestone files under a single ROADMAP status
  authority; separate phase skills glued by routing chips.
- **IP1–IP3 are inviolable** (approval-gated merges; prior state surfaced not
  silently obeyed/overridden; nothing the user asked for silently dropped).
  You may critique their *wording or completeness*, but treat the three
  guarantees as fixed intent.
- **The plugin is stdlib-only** for hooks/scripts (no third-party Python
  deps) — a portability constraint, deliberate.
- Assume the tracking-file *formats* are stable; propose changes to
  *architecture and doctrine*, not to markdown syntax bikeshedding.

## Output format

In `cairn/reviews/RR01-architecture-retrospective.md`: answer each question
**by its number** with reasoning and concrete file/line/D-entry evidence. Put
anything outside the numbered questions under a **"Beyond the brief"** heading.
End with a **"Recommendations"** section — a ranked list, each item marked
**apply** / **consider** / **reject-with-reason**, phrased as a concrete
change ("move X from the rulebook to the profile slot because Y"), not a
sentiment.
