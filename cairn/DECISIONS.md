# Decisions

Append-only. Never renumber; supersede with a new entry. D-entries record
choices with rationale — never deferrals ("not now" is a ROADMAP fact).

### D-001 (2026-07-11): Distribute as a Claude Code plugin

**Context:** Precursor systems were recreated per-repo and diverged.
**Decision:** Logic (skills, rules, templates) ships as this plugin; each
repo holds only state under `project/`.
**Consequences:** Updating the plugin updates every repo's workflow at once;
divergence of logic becomes structurally impossible.

### D-002 (2026-07-11): Per-milestone files + ROADMAP index

**Context:** Precursors used single board files (rotted large) or three-file
boards (fiddly moves).
**Decision:** One file per milestone; ROADMAP.md index table is the only
status authority; done milestones compress to ≤25 lines and archive.
**Consequences:** Hot files stay small; out-of-order completion is natural
(IDs are identifiers, not a sequence).

### D-003 (2026-07-11): Separate phase skills glued by routing chips

**Context:** A single multiplexed skill meant more typing; separate skills
risk rule drift.
**Decision:** Eight separate skills; every phase ends with an AskUserQuestion
chip routing to the next; all skills read one shared tracking-rules.md.
**Consequences:** One click between phases; rules stated once; every
transition is an explicit user stop.

### D-004 (2026-07-11): Fable only via the RB/RR brief protocol, gated per instance

**Context:** Fable subagents are technically spawnable from any session but
are token-billed pay-per-use.
**Decision:** Fable is reached only through a self-contained Review Brief,
behind an explicit per-instance approval gate (spawn or manual run).
**Consequences:** Escalations are reproducible, auditable, ingestible, and
never a silent cost.

### D-005 (2026-07-11): Migration entombs history, translates only live state

**Context:** Converting 50+ legacy milestones invites hallucinated dates and
lossy summaries; git already preserves history.
**Decision:** Legacy files move verbatim to `project/legacy/`; only live
items are translated, under a no-invention rule; IDs never renumbered.
**Consequences:** Migration is a small, reviewable, revertible PR; legacy
citations stay valid.

### D-006 (2026-07-11): Name the plugin "cairn"

**Context:** "rpkg-tracking" was a placeholder. Candidates spanned trail
markers (cairn, waymark, milepost), record keepers (roadbook, ledger), and
roles (steward).
**Decision:** cairn — built one stone at a time (milestones), marks the
trail for whoever comes next (stateless session resume). Action skills keep
generic names (/milestone*, /hotfix); repo-level skills carry the brand
(/cairn-init, /cairn-release).
**Consequences:** Known adjacencies accepted: CRAN's "Cairo" graphics
package (one letter apart) and the Cairn tabletop RPG; no CRAN package
claims "cairn". GitHub home: jmgirard/cairn.

### D-007 (2026-07-11): Ship marketplace.json early; advertise manual install only

**Context:** DRAFT_2 §2.3 deferred marketplace publishing until battle-tested;
a marketplace.json was nonetheless committed 2026-07-11 to validate its
structure. The M01 independent review flagged the unrecorded reversal.
**Decision:** The file ships now so the one-command path can be validated
during pilots, but README advertises only manual install until pilots pass.
**Consequences:** Partially supersedes the §2.3 deferral (structure now, promotion
later); README install-path documentation remains a tracked candidate.

### D-008 (2026-07-11): Tracking directory is `cairn/`, not `project/`

**Context:** "Project directory" already means the repo root in RStudio
parlance, `project/` is a plausible pre-existing dirname as cairn
generalizes beyond R, and the rename is cheap only before the M02/M03
pilots plant the layout in other repos.
**Decision:** All tracking artifacts live under `cairn/` (tool-named, like
`renv/` or `.github/`). Rejected: `tracking/` (telemetry connotation),
`.cairn/` (hidden dirs signal machine-managed state, these are
human-edited docs). Lineage A detection still keys on `project/` — that
was the precursors' dirname. Earlier D-entries keep `project/` verbatim
(append-only).
**Consequences:** Dirname collisions and RStudio ambiguity eliminated;
adoption detection is "does `cairn/ROADMAP.md` exist"; the dir name no
longer self-describes its contents — the CLAUDE.md section, which names
cairn and states the boundary rule, carries that load.

### D-009 (2026-07-11): The CLAUDE.md router carries routing only, not conduct

**Context:** The tracking rulebook (`tracking-rules.md`) loads only once a
cairn skill fires, so plain conversation bypasses tiers and the git model.
M08 made the always-loaded CLAUDE.md cairn section a classify-first router.
The question was whether to also inline conduct (contextual chips, output
discipline) so plain conversation gets it without a skill firing.
**Decision:** The router routes only — classify, apply tiers, never on main,
and invoke the skill *first*. Conduct stays in `tracking-rules.md`, delivered
when a skill fires. The router's job is to make a skill fire early, not to
restate conduct (which would also blow the ~20-line section cap).
**Consequences:** A request handled entirely in plain conversation without
triggering a skill still won't get chip/output conduct — an accepted residual;
the router minimizes it by routing to a skill as early as possible.

### D-010 (2026-07-11): Phase headers (H2/H3) replace the inline stage banner

**Context:** The M04-era output discipline oriented each reply with an inline
`[cairn · <skill> · M<NN> · <phase>]` banner. Jeff found it hard to scan in
the terminal.
**Decision:** Skills orient with a two-level Markdown heading instead — an
`##` names the unit of work and title, a `###` names the phase
(`## Milestone <NN>: <title>` → `### Plan`/`### Implement`/`### Review`; other
skills map onto the same two levels). The `##` is emitted once per **unit of
work** (re-emitted on a routing chip into the next skill or a fresh
post-`/clear` session), the `###` at each phase entry; replies within a phase
are plain deltas. Rejected the flat single-`##`-per-phase form (doesn't group
a milestone's phases) and keying the `##` to the session (breaks when one
session spans multiple units via chips).
**Consequences:** Supersedes the inline stage banner. Rule renamed "Stage
banner" → "Phase header" in `tracking-rules.md`; all 8 skills updated (M09).

### D-011 (2026-07-11): Generalizable fixes go in the plugin, not memory

**Context:** M10's review surfaced a prose merge-approval gate that
contradicted the rulebook. The reflex fix was a personal memory — which only
helps one user, in one client, and reintroduces exactly the per-repo/per-user
divergence D-001 exists to prevent. Jeff flagged it: solve it durably.
**Decision:** Defects and lessons that generalize are encoded in the shared
artifact (skills, `tracking-rules.md`, guard tests). Claude's memory holds
only per-user meta-context and never substitutes for shared plugin logic.
Adds GP4.
**Consequences:** Durability for every user, not just the one who hit the
bug; memory stops being a silent divergence vector; reinforces D-001 and GP3.
The merge-gate hotfix (chip wording + guard test + marker-sequencing note in
the skills) is the first application; the corresponding memory was retired.

### D-012 (2026-07-11): Phase headers shift up one level — H1 unit / H2 phase

**Context:** D-010 set the phase header at two levels — `##` for the unit of
work, `###` for the phase. Claude Desktop (Jeff's primary client) builds its
table of contents from H1/H2 only, so the `###` phase headers never appeared
in the TOC — defeating the scannability the headers exist for.
**Decision:** Shift the whole convention up one level: `#` names the unit of
work, `##` names the phase (`# Milestone <NN>` → `## Plan`, and the parallel
mappings for every skill). The two-level nesting and the emission cadence
(unit once, phase at each entry) are unchanged. Rejected flattening to a
single level (loses the milestone→phase grouping in the TOC).
**Consequences:** Supersedes D-010's level choice (its H2/H3 mapping is now
historical). Both header levels index in Desktop's TOC. Applied across
`tracking-rules.md` and all 8 skills; locked by
`skills/tests/test_phase_header_levels.py` (M11).

### D-013 (2026-07-11): Design elicitation is a standalone `/design-interview` skill

**Context:** The openac pilot (references/design-interview-notes.md) found a
gold-standard two-phase interview (facts → principles) far stronger than
cairn-init's current "5–10 honest lines" DESIGN fill. The question was
whether to fold that interview into `/cairn-init` or ship it separately.
**Decision:** Ship it as a standalone `/design-interview` skill.
`/cairn-init` keeps its quick seed lines and offers a routing chip into the
interview; the skill is also re-runnable on an existing repo to deepen a
thin DESIGN.md. v1 runs both phases on Opus; phase-2-to-Fable elevation is a
deferred candidate, not part of this decision.
**Consequences:** cairn-init stays lean; the interview is reusable beyond
init. A ninth skill (`skills/<name>/SKILL.md × 9`). Locked by
`skills/tests/test_design_interview.py` (M12).

### D-014 (2026-07-11): /design-interview recommends running on Fable

**Context:** D-013 planned an Opus-only v1, with Fable elevation deferred to
a candidate. The openac pilot (M12 criterion 6) refuted that: on Opus the
interview's questions were too technical and hard to parse; a Fable rerun was
"a much better experience" (Jeff). An interactive multi-round interview can't
be conducted by a subagent, so the only way to get Fable-quality live
judgment is to run the whole session on Fable.
**Decision:** `/design-interview` opens by recommending the user run the
session on Fable (citing this pilot), then proceeds regardless — a soft steer,
not a hard gate. This is the user's per-instance model choice; cairn spawns no
Fable subagent, so **D-004 is unaffected** (it governs cairn-spawned Fable,
not the user's own session model) and the "orchestrator: Opus" default stands
for every other skill.
**Consequences:** Supersedes D-013's Opus-only v1 and absorbs the deferred
"phase-2-to-Fable elevation" candidate (dropped). The pilot passed on Fable,
satisfying M12 criterion 6. Locked by
`test_design_interview.py::test_recommends_running_on_fable`.

### D-015 (2026-07-11): Durable repo lessons live in `cairn/LESSONS.md`

**Context:** Milestones recorded status, decisions, and tasks but not the
durable "how this repo actually behaves" lessons — build quirks, testing
tricks — a milestone teaches. Those were re-learned each time or lived only in
per-user memory (a divergence vector D-011 warns against).
**Decision:** Add `cairn/LESSONS.md` — append-only, one lesson per line
(`- YYYY-MM-DD (M<NN>): …`), capped at 50 lines — captured at
`/milestone-review` post-merge hygiene and surfaced at `/milestone-plan`
before the question gate. Rejected a per-milestone Lessons section promoted at
archive (scatters lessons across archive files; harvest would read them all).
Lessons ≠ decisions: a *choice with rationale* stays a D-entry.
**Consequences:** Durable cross-milestone memory, distinct from decisions and
shared across every adopting repo via the plugin. A fourth top-level tracking
file (`LINE_CAPS`, date-scan, and the file-map extended for it). Locked by
`skills/tests/test_lessons_loop.py` + the over-cap fixture in `scripts/tests/`.

### D-016 (2026-07-11): Keep "Never Haiku" blanket; review scorer runs on Sonnet

**Context:** M17 adds a generate-then-verify confidence scorer to
`/milestone-review`. Anthropic's own code-review plugin
(`references/anthropic-code-review.md`) uses Haiku for exactly this mechanical
scoring step, which the reference flagged as counter-evidence to cairn's
blanket "Never Haiku. For anything." rule. The question was whether to relax
the rule for the scorer.
**Decision:** Keep the blanket rule; the scorer runs on Sonnet. Two reasons
beyond cost: cairn's review fires once per milestone (not per-PR at Anthropic's
scale), so the saving is marginal; and the scorer *gates which findings reach
the user*, so a weaker model can silently drop a real bug or bury the user in
false positives — not the low-stakes step the "mechanical" framing implies. One
clean, auditable invariant is worth more than the marginal saving. Rejected
relaxing it to a narrow scoring carve-out.
**Consequences:** Closes the doctrine challenge in
`references/anthropic-code-review.md`. The `/milestone-review` fan-out and
scorer are all Opus/Sonnet; the model-strategy section states the scorer stays
on Sonnet. If review cost ever becomes pressing at scale, this is the entry to
supersede.

### D-017 (2026-07-12): memory_guard emits a non-blocking additionalContext nudge

**Context:** M19 gives GP4 a runtime enforcement arm — a PreToolUse(Write)
hook that reminds Claude of the memory→`cairn/`-files boundary when it writes
to per-user memory in a cairn repo. The plan hedged the emission mechanism on
a contract question (T1): if PreToolUse could not emit a *non-blocking* nudge,
prose-only (tracking-rules alone, no hook) was the honest fallback.
**Decision:** T1 (official hooks docs) confirmed PreToolUse supports
`hookSpecificOutput.additionalContext` with `permissionDecision` optional, so
the hook ships. It emits `additionalContext` **and no `permissionDecision`** —
the softest lever: the reminder is injected as context Claude reads next turn
while the Write proceeds through the normal permission flow untouched (no
dialog via `ask`, no override via `allow`). Rejected `ask` (a per-write
dialog is exactly the nag fatigue to avoid) and `allow`+context (would
suppress any user-configured Write permission rules for no benefit). The
prose-only fallback was not needed.
**Consequences:** Enforces GP4 at write time for every adopting repo without
friction; fail-permissive, so a missed nudge never blocks a write. The nudge
fires unconditionally on any memory write in a cairn repo — if that proves too
noisy, the "content-gated memory guard" candidate (inspect the write, fire
only on durable-state signals) is the entry to supersede. Envelope is pinned
to the documented contract + the unit test's asserted shape; a true live-fire
(does Claude Code honor `additionalContext` from PreToolUse) needs a fresh
session after merge, since hooks snapshot at process start.
