---
name: milestone-plan
description: Plan one or more milestones for a cairn repo - investigate, scope, write acceptance criteria, and register them in the ROADMAP. Use when the user wants to plan a milestone, plan new work or a feature, turn an idea or candidate into a concrete plan, or asks "what would it take to build X".
argument-hint: "[title or description]"
---

# /milestone-plan — idea → planned milestone(s)

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: sizing tripwires, status gatekeeping, question gates).
Phase header: `# Milestone <NN>: <title>` → `## Plan` (before an ID is
assigned, `# Planning`); see the tracking-rules Phase header rule.

## Session start

Read, in order: `cairn/ROADMAP.md`, any active milestone file,
`cairn/DECISIONS.md`. If an un-ingested RR exists in `cairn/reviews/`,
handle ingestion first (see `/milestone-brief`).

## Workflow

1. Confirm nothing else is `in-progress` — run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_next.py"` for the mechanical
   active/workable picture rather than eyeballing the ROADMAP. If it reports
   an active milestone, get explicit user sign-off to plan ahead anyway
   (planning ahead is fine; it just needs saying).

2. **Investigate first.** Read the relevant code and DECISIONS.md. For
   scopes touching more than a couple of files, fan out Explore subagents
   ([S]-tagged descriptions) with specific focuses; require file:line
   citations. Draft scope, tasks,
   and the list of genuinely open decisions internally.

   **Collision check (mandatory).** Sweep the ROADMAP (all statuses), the
   archive, and DECISIONS.md for overlap with what the user described.
   Prior state is *surfaced at the question gate*, never silently obeyed or
   silently overridden:
   - `candidate` row → the normal promotion path: absorb the row, note the
     lineage.
   - `planned` milestone → no duplicates: amend it, supersede its plan, or
     confirm the scopes are distinct and cross-reference.
   - `in-progress` milestone → fold in via the amendment protocol
     (`/milestone-implement` step 6) or plan separately with `Depends on:`.
   - `done` (archived) → it shipped; tell the user (it may already do what
     they want); otherwise plan an extension referencing the old ID.
   - `dropped` milestone or D-entry rejection → quote the prior rationale
     verbatim ("D-014 rejected X because Y — does that still hold?"). To
     proceed: **supersede, don't ignore** — append a superseding D-entry
     first. Never plan against a standing rejection without superseding it;
     never refuse merely because a rejection exists.

3. **Question gate** (one batched AskUserQuestion round, 2–5 questions, each
   with a recommendation): scope boundary, sequencing, acceptance bar, and
   any collision dispositions. Every proposed scope cut must state **where
   the remainder goes** — never "M12 covers A and B" alone, but "M12 covers
   A and B; C becomes M13 (planned now, depends on M12); D becomes a
   candidate row; E sounds unwanted — drop entirely?".

4. **Solidify autonomously** (no further questions). Create **one or more**
   milestone files from
   `${CLAUDE_PLUGIN_ROOT}/skills/shared/templates/milestone.md` — when the
   sizing tripwires fire, the answer is multiple milestones in one run, not
   shrink-to-fit and discard. For each file:
   - Acceptance criteria verifiable with evidence; never vibes. Criteria
     that cite a formula or reference value must name their source
     (`citekey (p. N)` — see the primary-sources rule).
   - Acceptance criteria set the test scope for the milestone (see "What
     gets a test" in tracking-rules): name the behavior that must be tested.
   - `Out:` items name where the excluded work lives instead.
   - Tasks ≤ one working session each, ordered by dependency.
   - Open questions that hit an RB tripwire (see tracking-rules) are
     tagged inline on the affected task or criterion with the canonical
     token — `(RB tripwire: no-oracle | irreversible-api | ip-touching)` —
     so implement inherits them.
   - Write only the plan-owned sections — Goal, Scope, Acceptance criteria,
     Tasks, and the Priority/Depends-on header — per the section-ownership
     table in tracking-rules; leave Work log, Decisions, and Review to their
     owners.
   Deferred chunks not yet plannable get `candidate` ROADMAP rows, not files.

5. **Remainder ledger (conservation check).** Before committing, enumerate
   every distinct thing the user originally asked for and its disposition:
   in this milestone / planned as M<NN> / candidate row / dropped at the
   user's explicit request. Nothing may be silently absent. Deferral is
   NEVER recorded as a decision not to do something — D-entries are for
   genuine rejections with rationale; postponement lives in the ROADMAP.
   Include the ledger in the plan summary presented to the user.

6. **Commit atomically.** Update ROADMAP rows (`planned` / `candidate`) and
   commit files + rows together, directly to main, no branch, no PR
   (docs-only carve-out): `plan M<NN>[, M<NN>…]: <title>`; push. A session
   dying mid-plan must not leave a half-planned ghost.

7. **Routing chip**, composed from what was just planned (chip rules per
   tracking-rules) — e.g.:
   - **Start implementing M<NN>** (the proximal one) → `/milestone-implement`
     (recommended)
   - Plan another milestone → `/milestone-plan`
   - Stop here
