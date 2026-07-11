# Competitive landscape synthesis (M06)

Sources: the eight per-system notes in this directory (feature-dev,
claude-md-management, anthropic-code-review, ccpm, spec-kit,
task-master, bmad-method, backlog-meridian), 2026-07-11.

## The uniqueness case, differentiator by differentiator

**1. Markdown-native tracking — CONCEDED as commodity.** Backlog.md,
ccpm, BMAD, and spec-kit all keep state in frontmatter'd markdown;
Task Master proves the JSON alternative exists too. File-based state is
table stakes, not a moat. What no one else has is the *governance* of
those files: single status authority, ownership boundaries, weight
caps, compressed archives. Every surveyed system lets its artifacts
grow unboundedly or scatter status across files.

**2. Status gatekeeping — DEFENDED.** No surveyed system binds status
transitions to dedicated gatekeeping skills. ccpm and Task Master
statuses are freely settable writes; BMAD's dev agent self-polices;
Backlog.md's staged guides are prose. Cairn's "only /milestone-review
sets done" is unique in kind. Caveat: Meridian proves enforcement can
be *technical* (blocking hooks) rather than conventional — cairn's
version is currently the weaker form.

**3. Review/approval gates — DEFENDED, cairn's sharpest edge.** A
mandatory human merge approval with fresh-evidence criteria
verification exists in none of the eight. ccpm merges on instruction;
BMAD hands off agent-to-agent; spec-kit's git extension can
auto-commit; Backlog.md asks for evidence in prose with no aggregation
or gate. The trial showed why this matters: feature-dev's reviewers
are good, but their findings evaporate with the transcript.

**4. R-toolchain doctrine (oracles, primary sources) — DEFENDED,
no analogue anywhere.** Nothing in the survey even gestures at
domain-specific verification doctrine. Unique but narrow-audience —
strengthens the toolchain-profiles candidate: the doctrine slot is the
differentiator; R is one profile of it.

**Emergent fifth differentiator**: longitudinal memory + change
control *combined*. spec-kit is strongest pre-implementation but has
no cross-feature continuity by design; ccpm has throughput but no
audit; feature-dev has choreography but no persistence. The closest
rival is Meridian — it has both memory re-injection and blocking
enforcement — but it enforces *process*, not project state: no
task/milestone concept of its own, no cross-milestone memory, no
decision ledger; it re-injects docs without governing them. Cairn's
niche — auditable, governed project memory with human-gated change
control — is genuinely unoccupied.

**Verdict: cairn is justified; no refocus needed.** Positioning should
say "change control + project memory for agent-driven development",
not generic "project tracking".

## Where the field is ahead of cairn (steal-list, ranked)

1. **Deterministic tracking scripts** (ccpm): status/next/validate as
   shipped bash over the cairn/ dir — instant, token-free, drift-proof
   vs. re-deriving by LLM each session.
2. **Blocking hooks + context re-injection** (Meridian): technically
   prevent merge-without-approval and end-of-session uncommitted work;
   SessionStart re-injection of ROADMAP + active milestone. Upgrades
   the existing hooks candidate from "reminders" to "enforcement".
3. **Review pipeline mechanics** (anthropic-code-review, feature-dev,
   Backlog.md, spec-kit): distinct-evidence-base reviewer fan-out
   (blame history, prior-PR comments), verbatim confidence rubric +
   false-positive taxonomy, evidence-before-checkbox AC fencing,
   criterion→task coverage table. Also: revisit the blanket never-Haiku
   rule — Anthropic's own pipeline uses Haiku for mechanical
   triage/scoring (D-entry question for the user).
4. **Milestone file mechanics** (BMAD, spec-kit, Task Master):
   section-level write allow-lists per skill; baseline-commit capture
   at implement start; prior-milestone lessons harvest at plan time;
   Sync Impact Report when tracking-rules/principles change;
   complexity-scored split advisory.
5. **Session-end learning harvest** (claude-md-management): capture
   repo lessons (build quirks, testing tricks) into a durable home —
   cairn logs what happened, not what was learned.

## Known risks confirmed empirically

- Two tracking systems in one repo actively mislead agents: trial
  agents treated a foreign system's task files as binding acceptance
  criteria (see feature-dev.md hands-on). "Issues are inboxes" needs
  its generalization stated: *any* second planning artifact is a hazard.
- claude-md-improver's rubric penalizes cairn's pointer-based
  CLAUDE.md (~70/100); coexistence is survivable but noisy.
