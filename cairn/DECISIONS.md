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

### D-018 (2026-07-12): The CLAUDE.md weight cap measures the cairn section, not the whole file

**Context:** The `<80`-line CLAUDE.md cap in `cairn_validate` FAILed a
legitimately mature repo — the M20 ackwards pilot's CLAUDE.md was 187 lines of
real dev doctrine (dev workflow, definition-of-done, invariants, guardrails)
plus the ~26-line appended cairn section. cairn was policing content it does
not own. (references/migration-pilot-notes.md G8.)
**Decision:** Drop the whole-file CLAUDE.md cap. Instead hard-cap only the
`## Project tracking (cairn)` section cairn appends and owns, at **30 lines**
(the template's stated target stays ~25). The repo's own dev doctrine above or
below that section is not capped by cairn. Rejected: a higher flat whole-file
cap (arbitrary — the next larger repo re-breaks it, and the flat cap is itself
what the pilot flagged), and a soft non-failing warn (loses the hard signal on
a genuinely bloated cairn section).
**Consequences:** The audit passes on any mature repo while still hard-failing
a bloated cairn section — the one part cairn controls. Reinforces D-009 (the
router section carries routing only; a swelling section is the signal to trim,
not to raise a cap). Wired in three places (M16 lesson): `tracking-rules.md`
weight-caps text, `cairn_scripts.py` (new `CLAUDE_SECTION_CAP`; `LINE_CAPS`
drops `CLAUDE.md`), and `cairn_validate.check_caps` (section measurement).
Locked by `scripts/tests/`.

### D-019 (2026-07-12): Review's end is exempt from the routing-chip mandate

**Context:** D-003 established that every phase ends with an AskUserQuestion
routing chip. Two things pushed on that: Jeff's feedback that at the close of
a successful review/merge the natural next step is a fresh `/clear`, not
another in-session route; and drift — most phase skills said "routing chip"
without naming AskUserQuestion, which let an orchestrator emit prose options
instead of a chip after M22 review.
**Decision:** Refine D-003 in two parts. (1) Tighten the mandate: every phase
skill that ends with a routing chip names `AskUserQuestion` at that step (a
prose list of options is not a chip), locked by `test_gate_wording.py`.
(2) `/milestone-review` is the sole exception — its end is a plain-prose
`/clear` nudge with no routing chip. Review's separate merge-approval chip is
untouched. Rejected keeping a minimal chip at review's end (the whole point is
that a fresh context, not a route, is the right next step there).
**Consequences:** Review is the one phase whose end is deliberately chip-less;
every other phase keeps its chip. D-003's blanket "every phase ends with a
chip" is refined, not overturned. Locked by `TestRoutingChipMandate` in
`skills/tests/test_gate_wording.py`.

### D-020 (2026-07-12): In Claude Code the navigable TOC is driven by chapter markers, not markdown headers — annotates D-012

**Context:** D-010/D-012 justified the phase-header level convention partly as
"emit H1/H2 so both levels land in Claude Desktop's table of contents." M27
tested that live in Jeff's Claude Desktop, viewing a **Claude Code** (cairn)
session — cairn's actual runtime. Two messages of `#`/`##`/`###` headers
(including a real `# PROBE-A1`) produced **zero** TOC entries; a single
`mcp__ccd_session__mark_chapter` call produced a two-entry outline. Full
characterization: `references/desktop-toc-mechanism.md`.
**Decision:** Record the mechanism as it is. In a Claude Code session the
navigable TOC is built from **chapter markers**, not markdown `#`/`##`
headers. D-012's "both levels index in Claude Desktop's TOC" does **not** hold
for cairn's Claude Code runtime (tested here — zero headers indexed). Whether
it holds on any other Claude surface (e.g. a regular claude.ai / Desktop chat)
was not probed by M27; D-012's claim is annotated as **unverified for cairn's
runtime**, not confirmed elsewhere. No header-format change: the H1-unit /
H2-phase convention is **retained for in-transcript visual hierarchy**, which
it does deliver (headers render as headings). The `tracking-rules.md`
phase-header line that credited the markdown TOC is corrected to credit the
chapter-marker rule instead. Rejected AC2 option (a) (a header change — no
markdown format indexes here) and "record but leave the false rulebook line."
**Consequences:** The chapter-marker discipline (output-discipline "Chapter
markers" rule) is the load-bearing TOC driver in cairn's runtime, not the
phase headers — reinforcing that rule's importance. `test_phase_header_levels.py`
is unaffected (levels unchanged). Whether to promote the chapter-marker rule
from "where supported" to a hard per-phase mandate is banked as a ROADMAP
candidate, not decided here.

### D-021 (2026-07-12): The chapter-marker rule is a hard per-phase mandate — executes D-020's banked candidate

**Context:** D-020 established that in cairn's Claude Code runtime the
navigable TOC is driven by chapter markers, not markdown headers, and banked
"promote the chapter-marker rule to a hard per-phase mandate" as a candidate.
The output-discipline "Chapter markers" rule still read "where the harness
supports conversation chapters" — optional, unenforced, and (like the
routing-chip rule before M26) drift-prone because no guard checked it.
**Decision:** Promote the rule to a **hard per-phase mandate**: mark a chapter
at each phase transition (session start implicit). Three sub-choices, made at
the M28 plan gate: (1) **enforcement** — a one-line `Chapter markers:`
directive in every phase skill, parallel to the `Phase header:` directive,
locked per-skill by `test_chapter_marker_mandate.py` (a central rule alone is
what let the milestone-brief chip gap through); (2) **fallback** — the
directive is unconditional; where the runtime provides no chapter mechanism
the call is simply unavailable and the H1/H2 phase headers are the visual
fallback, so nothing breaks; (3) **scope** — all nine skills including
`/milestone-review`, since chapter markers are orthogonal to the routing-chip
exception (D-019) — review is chip-less but still has navigable phases.
**Consequences:** Annotates D-020 (executes its banked candidate) and
reinforces the output-discipline "Chapter markers" rule as the load-bearing
TOC driver. The mandate's list (nine, review included) deliberately differs
from `NON_REVIEW_CHIP_SKILLS` (seven — review excluded from that one). Guards are prose-guards, proving wording
not runtime (M27 already characterized runtime behavior live). If a future
harness needs a different fallback, this is the entry to supersede.

### D-022 (2026-07-12): Selecting a routing chip is an imperative to invoke the target skill — annotates D-003

**Context:** D-003 glued the phase skills with routing chips ("every phase
ends with an AskUserQuestion chip routing to the next"); the routing-chip rule
D-003 produced in `tracking-rules.md` then described the mechanism as
"selecting a chip invokes that skill in the same session." Read
descriptively, that sentence left room for the orchestrator to *hand back* to
the user — presenting the chosen option and waiting for the user to type the
skill command — which is exactly the extra-typing friction D-003 exists to
remove. An M28-era slip did this in practice. Per D-011/GP4 (generalizable
fixes go in the plugin, not memory), the fix belongs in `tracking-rules.md`
as an imperative, not in a per-user note.
**Decision:** Rewrite the routing-chip rule as an imperative on the
orchestrator: on selecting a routing-chip option the orchestrator immediately
invokes the target skill via the Skill tool and does not stop to have the user
type the command. The `→ /skill` chip-option notation names the skill the
orchestrator invokes on selection, not a command for the user to run. The
"chip is a user stop — never auto-proceed" clause is unchanged and does not
contradict this: the stop is *before* selection; the selection is the go. A
`test_gate_wording.py` guard (`TestChipInvocationImperative`) locks the
imperative and notation phrasing against reversion to the descriptive form.
Rejected per-skill invoke-on-selection tokens (the rule is uniform conduct,
stated once centrally) and rewording the `→ /skill` arrows across the eight
skills' menus (keep the arrows; clarify their meaning in the rule).
**Consequences:** Annotates D-003 — its "separate skills glued by routing
chips" stands; only the invocation *mechanism* is clarified from descriptive
to imperative. The one-click-between-phases promise is now enforced wording,
not just intent. Review's chip-less exception (D-019) and the merge-approval
chip are untouched.

### D-023 (2026-07-12): cairn_validate's slash-date matcher requires a 4-digit year — supersedes the M13 conservative-design rationale for that branch

**Context:** `cairn_validate`'s ISO-date scan flagged R CMD check
count-notation — three slash-separated counts (errors/warnings/notes) such as
`0/0/0` — as a "non-ISO date," because the slash branch matched any three
slash-separated numbers (the loose `\d{1,4}/\d{1,2}/\d{1,4}`). The gate cried
wolf on legitimate check-result reporting (M21 circumplex pilot G-C2). A real
slash *date* carries a 4-digit year on one end; a count-triple does not.
**Decision:** Tighten the slash branch to require a 4-digit year — year-first
(`2026 / 07 / 11`) or year-last (`07 / 11 / 2026`). Count-triples no longer match. The
accepted cost: a 2-digit-year slash date (`07/11/26`) goes uncaught, because
it is structurally indistinguishable from a count-triple. This is the right
side of the "a missed weird format beats a false positive" doctrine (M13):
zero 2-digit-year slash dates exist in this repo's strict-ISO format, so the
miss is theoretical while the false positive was real. Rejected: month/day
range validation of matched triples (over-engineering — the year requirement
alone kills every realistic false positive here) and context-excluding
check-result lines (brittle; the FP returns for any other count-triple).
**Consequences:** Supersedes the M13 "conservative by design" rationale *for
the slash branch only* — the other branches (dashed year-last, month-name
orders, malformed-ISO) are unchanged. Retires the M21 workaround (tracking
files may again write check results in slash form). Locked by
`test_check_result_notation_passes` (count-triples pass) plus the year-first
and year-last cases added to `test_non_iso_date_formats` (real slash dates
still caught) in `scripts/tests/test_scripts.py`. If a 2-digit-year slash date
ever needs catching, this is the entry to supersede.

### D-024 (2026-07-12): Fold ackwards' oracle-type discipline into the Validation doctrine; defer the registry file and R guard as candidates

**Context:** `jmgirard/ackwards` M57 ("Ossify oracles") built a mature oracle
system — an `ORACLES.md` registry, a frozen/live/invariant/closed-form type
taxonomy, a "≥2 independent oracle *types* per numeric result / nothing
unsourced or unreproducible ships" standard (its Invariant #8), and a
fixture-provenance guard test — itself a formalization of the reproducible
`data-raw/oracle-*.R` practice originated in `jmgirard/intraclass`. cairn's own
"Validation doctrine" section had an overlapping priority list but no named
oracle-type vocabulary, no frozen/live distinction, no ≥2-*types* bar, and no
reproducibility (as opposed to sourcing) mandate. Per GP4/D-011 the
generalizable core belongs in the plugin, not re-derived per repo. Assessed in
`references/oracle-discipline-notes.md` (E1–E8 gap ledger).
**Decision:** Fold the four generalizable principles (ledger E1–E4) into
`tracking-rules.md` "Validation doctrine": the frozen/live/invariant/closed-form
vocabulary + "live independent-impl is the stronger form, don't freeze it into a
regression pin unless expensive/network-bound", the ≥2-*independent-types* bar,
and the reproducibility hard-stop. The existing priority list is preserved (the
types refine it). The additions stay self-contained — no cross-repo citation in
the shared rulebook. The two **structural** pieces are deferred as ROADMAP
candidates, not rejected: adopting `ORACLES.md` as a cairn tracking file (E5 —
the D-015/M16 four-wiring-points path, entangled with toolchain-profiles), and
generalizing the R-specific `provenance`-attr + `test-oracle-provenance.R` guard
(E6 — an R toolchain-profile slot). Rejected: adopting the registry file into
core scaffold now (domain-specific; one-exemplar shape risk; pre-empts where the
toolchain-profiles split should place domain files) and full type-list
replacement (the priority list stays).
**Consequences:** Every adopting statistical/numeric repo inherits the stronger
oracle doctrine via the plugin. The registry-file question is intentionally
open, tied to toolchain-profiles. ackwards keeps its Invariant #8 as its own
interim home (folding it into an ackwards DESIGN IP/GP is ackwards-local, ledger
E8 — out of scope here). Locked by `skills/tests/test_oracle_doctrine.py` (the
type names + the ≥2-types bar). If a registry file is later adopted, or the
≥2-types bar proves too strong a blanket, this is the entry to supersede.

### D-025 (2026-07-12): Add simulation-coverage as the fifth oracle type — annotates D-024

**Context:** M42 validated D-024's four-type oracle taxonomy
(frozen/live/invariant/closed-form) against `jmgirard/intraclass`'s real
34-script oracle system — the practice cairn's doctrine descends from. Finding
(`references/oracle-doctrine-intraclass-notes.md`): 31/34 scripts use an oracle
that maps to **none** of the four types — simulation from known population
parameters, checking the estimator recovers the known value (point) and/or its
interval covers it at the nominal rate. It leads every one of the 20 Bayesian CI
oracles ("a CI method's oracle is coverage") plus the frequentist coverage
oracles, and is the missing cairn analog of intraclass's **inviolable** PRINCIPLES.md #1(c)
("simulation with known population variance components"). The four types are all
deterministic numeric-agreement oracles; this fifth is the one *probabilistic*
(sampling-distribution) oracle, and without it a repo following cairn's doctrine
has no named home for a CI method's primary oracle and cannot count it toward
the ≥2-*independent-types* bar. AC2 verdict: PRINCIPLES.md #1 and cairn's bar
**agree** on "≥2 independent oracle types" but **diverge** on the type list —
this is the divergence.
**Decision:** Add **simulation-coverage** as a fifth first-class oracle type in
the Validation doctrine (priority-list item (5) + the type paragraph), counting
toward the ≥2-types bar like any other type, with the freeze-only-when-expensive
nuance carried over. Chosen over (b) priority-list mention without type status
(leaves a CI method's main oracle uncountable — doesn't close the defect) and
(c) defer to a dedicated milestone (the fix is small, guard-testable text; AC4
authorized fixing an exposed defect in-milestone). User-selected at the M42
implement gate.
**Consequences:** Every adopting statistical/numeric repo gains a named home for
coverage/recovery oracles. The two deferred oracle candidates (registry file,
R-provenance guard) are **downstream** of this — a registry's `type` column
cannot describe intraclass's oracles without it (M42 T3 kept both deferred,
rows sharpened). Annotates D-024 (its four-type list stands; a fifth is added,
not a supersede). Locked by `skills/tests/test_oracle_doctrine.py`
(`test_names_the_five_oracle_types` + the coverage-oracle anchor). If the fifth
type ever needs splitting (point-recovery vs. interval-coverage) or the ≥2-types
bar proves too strong for it, this is the entry to supersede.

### D-026 (2026-07-12): Drop the parallel-task-metadata and tiered-tool-exposure M06 steals — they don't fit cairn's execution model

**Context:** The M06 competitive survey banked five "minor steals" as
candidate sub-items (`references/competitive-landscape.md`, steal-list C6).
Three have since been decided — principles-touched slot (M38), search-first
candidate creation (M39), and now the sizing advisory + Priority-field schema
(M44). Planning M44 surfaced that two of the remaining sub-items are structural
mismatches, not deferrals: **conflicts_with / parallel task metadata**
(task-master) presumes a parallel-agent execution model, and **tiered tool
exposure** presumes per-tier tool gating.
**Decision:** Drop both. cairn runs one milestone at a time, human-gated, with
tasks ordered by dependency inside a single reviewable PR — there is no
parallel-agent scheduler for `conflicts_with` metadata to feed, and tools are
already scoped per spawned agent by the model-strategy section, so a tiering
layer adds ceremony with no gate it serves. Rejected keeping them as parked
candidates (they are not "not yet" — they contradict the execution model, so a
recorded rejection is the honest state, re-openable by superseding this entry).
The scored-rubric hygiene-audit sub-item is **not** dropped here — it stays a
candidate (contestable on the binary-gate-audit axis, but not a model mismatch).
**Consequences:** The M06 candidate row loses two sub-items; the row now tracks
only the scored-rubric sub-item plus its shipped-item ledger. If cairn ever
grows a parallel-execution or tool-tiering model, this is the entry to
supersede.

### D-027 (2026-07-12): Prune three candidates in a triage pass — refuted, YAGNI, and off-model — supersedes D-026's scored-rubric retention

**Context:** A `/milestone-plan` candidate-triage pass sorted the 12 ROADMAP
candidates into higher/lower priority and flagged three for removal. Two of the
three were deliberately-kept state, so removing them supersedes prior decisions
rather than merely pruning a deferral.
**Decision:** Drop three candidate rows. (1) **Session opening-phase TOC label**
— premise refuted: M31 was planned, built, and dropped, and its lesson records
that the opening phase is already navigable (an implicit "Session Start" node)
with first-message marking discouraged by the tool docstring; the residue is
marginal and verifiable only by unobservable live Desktop probing (D-020).
(2) **Scripts `--json` output mode** — speculative YAGNI with no consumer; the
only readers (the skills) parse text fine, and none is planned. (3) **M06
scored-rubric hygiene audit for `/milestone`** — rejected on principle: a scored
rubric cuts against cairn's binary-gate audit model. This closes the last live
sub-item of the M06 steal-list (the rest shipped via M38/M39/M44/M17 or were
dropped in D-026), so the whole M06 row leaves the Candidates park. Rejected
keeping any of the three as parked candidates — a recorded rejection is the
honest state (search-first then finds it instead of re-adding the idea).
**Consequences:** Candidates drop 12 → 9; the survivors are reordered
higher-priority-first (toolchain profiles, public release prep, then seven
gated/parked items). Supersedes D-026's "the scored-rubric sub-item is **not**
dropped here" — it is now dropped. Higher/lower is advisory ordering, not a
status field (candidates carry no Priority). Each removal is re-openable by
superseding this entry.

### D-028 (2026-07-13): The r-package fixture-provenance mandate fixes the required content, not the shape

**Context:** cairn's universal Validation doctrine carries a "Reproducibility
(hard stop)" — a committed numeric fixture must ship with a generator that
reproduces it from scratch. M49 folds the R-mechanical concretization of that
rule into the r-package profile's `test-doctrine` slot. The two exemplars this
descends from implement it in *different shapes*: `jmgirard/ackwards` uses a
`provenance` attribute on the fixture plus a blocking `test-oracle-provenance.R`
guard; `jmgirard/intraclass` embeds the provenance as named fields *inside* the
`.rds` (`source`/`generated`/`base_seed`/`dgp`) with no guard. Mandating one
exemplar's shape would reject the other's working practice.
**Decision:** The r-package `test-doctrine` mandate fixes the required
provenance *content* — source + committed generator (a `data-raw/` script that
regenerates the fixture from scratch) + any seed — and leaves the *shape* to the
adopting repo: a `provenance` attribute, embedded `.rds`/`.rda` fields, or a
header comment all satisfy it. Rejected pinning ackwards' exact `provenance`-attr
+ guard-test form (the two-exemplar variance shows it is not the only working
shape) and mandating only the universal principle without an R-mechanical bullet
(leaves R adopters without the concrete "which pieces, in what" the profile
exists to supply). No guard *test* is mandated on the adopting repo — the slot
states the content bar; whether a repo enforces it with a guard test (ackwards)
or by convention (intraclass) is its choice.
**Consequences:** Every R adopter inherits the reproducibility content bar via
the profile while keeping shape freedom; graduates the M42-revised "R-profile
provenance guard" candidate. Locked by `TestRPackageFixtureProvenance` in
`skills/tests/test_toolchain_profiles.py`. If a single canonical shape (or a
mandated guard test) ever proves worth enforcing across R adopters, this is the
entry to supersede.

### D-029 (2026-07-12): The oracle registry generalizes as shape-free content doctrine, not a central `ORACLES.md` tracking file — annotates D-024/D-025

**Context:** D-024 deferred adopting ackwards' `cairn/ORACLES.md` registry as a
cairn tracking file (ledger E5); D-025 (M42) kept it deferred, sharpening the
row with two findings: (a) the `type` column could not describe intraclass's
oracles until the taxonomy gained the simulation-coverage type — which D-025
itself then added, clearing that gate — and (b) intraclass implements the same
per-oracle registry *content* **distributed** (structured `oracle-*.R`
provenance headers + fields embedded in the `.rds`), with **no** central file,
proving the central-file shape is not the only working one. Both original
deferral gates are now down: the fifth type shipped (D-025) and the
toolchain-profiles split that the row was entangled with is built out
(M45–M49). The question at the M51 plan gate was *how* to adopt it — a central
`ORACLES.md` tracking file (ackwards' shape) vs. shape-free content doctrine.
**Decision:** Fold a **shape-free registry requirement** into the
`tracking-rules.md` Validation doctrine — every oracle is recorded by ID, type,
asserting `test:line`, source, and provenance so the ≥2-independent-types bar
stays auditable at scale, the asserting test being the single source of truth
the record maps to — and leave the *shape* (a central registry file,
distributed generator headers, or embedded fixture fields) to the adopting
repo. This is the symmetric move to D-028: fix the required *content*, not the
*shape*, since the two exemplars (ackwards central / intraclass distributed)
show the central file is not the only working form. **Rejected** adopting a
central `ORACLES.md` as a new cairn tracking file: it would over-fit one
exemplar exactly as D-028 refused to for provenance, it is an *optional,
statistical-only* file that does not fit the universal-scaffold model (the
D-015/M16 four-wiring-points path + a cap + an opt-in), and no cairn-tracked
repo currently needs cairn to *supply* the central index (ackwards hand-built
its own; intraclass is not cairn-tracked). Also rejected a `cairn_validate`
CHECK — the whole Validation doctrine is advisory prose enforced by review
judgment, never a validate gate (M33/M42/M49).
**Consequences:** Annotates D-024/D-025 — their four/five-type taxonomy and the
E6 provenance graduation (D-028) stand; only the E5 registry disposition is
resolved here, as doctrine rather than a file. Every adopting statistical/numeric
repo inherits the auditability requirement via the plugin while keeping shape
freedom. The rulebook text stays self-contained — no cross-repo citation
(D-024) — so exemplar grounding lives here and in `references/oracle-*-notes.md`.
Graduates the ROADMAP "oracle registry" candidate (at post-merge hygiene, M35).
Locked by `test_oracle_registry_records_the_audit_fields` +
`test_oracle_registry_is_shape_free` in `skills/tests/test_oracle_doctrine.py`.
If a cairn-tracked statistical repo later needs cairn to supply a central
`ORACLES.md` shape (or a mechanical validate CHECK), this is the entry to
supersede.

### D-030 (2026-07-13): The milestone weight cap measures the plan-owned body only; the `## Review` section is exempt — parallels D-018

**Context:** The 150-line milestone cap measured the whole file, so review
evidence (written to the review-exclusive `## Review` section at review time)
competed with plan-owned Scope/AC/Coverage for one budget. Because AC wording is
plan-owned/amend-via-gate and cannot be trimmed, evidence overflow forced
trimming elsewhere — a recurring end-of-milestone scramble that twice damaged
content (M19/M22/M33/M50).
**Decision:** `check_caps` measures only the plan-owned body — every line before
the first `## Review` heading — against `MILESTONE_CAP` (kept at 150); the
`## Review` section is exempt. A fence-aware `milestone_body_line_count` does the
measure (tracking ```/~~~ so a fenced `## Review` in the body is not the
boundary — M45); a file with no Review section counts whole (back-compat).
Rejected: splitting the budget 120/40 and adding a separate Review sub-cap —
both add a second number and complicate/tighten plan discipline for marginal
benefit; the point is that plan discipline stays at 150, unchanged. Also
rejected exempting the milestone-local `## Decisions` section (kept counted — it
is meant to stay brief, with cross-cutting entries promoted here).
**Consequences:** Review evidence no longer scrambles plan-owned content; plan
discipline is unchanged. Parallels D-018 (cap only the part cairn's discipline
governs). The `## Review` section is technically unbounded during the
review→done window but compresses to ≤25 lines at archive and is governed by
"never paste output — summarize." Locked by the over-cap fixtures in
`scripts/tests` + `test_milestone_cap_exemption.py` (wording + stated↔enforced,
mutation-registered). If an unbounded Review section ever bites, a Review
sub-cap is the entry to supersede.

### D-031 (2026-07-16): New domain doctrine gets a module, not a rulebook section — annotates D-024/D-025/D-029

**Context:** The Validation doctrine (+ oracle registry, reproducibility and
primary-sources hard stops, source ingestion) had grown to ~68 always-read
rulebook lines that apply only to repos with numeric/scoring work — ~11% of
every non-numeric session's core read (RR01 §5/rec 9). RR01's counter-case for
splitting the rulebook (one rules-home, guard-test anchoring, whole-read
guarantees) argues against *fragmenting the cross-skill contract*, not against
extracting a self-contained, conditionally-relevant domain block. M58 executed
the extraction with the mutation harness (M53) in place to keep the guard
re-anchor honest.
**Decision:** Domain doctrine lives in its own module under `skills/shared/`
(`validation-doctrine.md`), referenced from the rulebook in a short section
that states what it covers and when to read it; the norm for the future is
**new domain doctrine gets a module, not a rulebook section**. Wiring is
rulebook-reference-only — skills read the rulebook whole, so the pointer
travels everywhere; no per-skill read directives (that would restate the
pointer in four places, the drift pattern RR01 rec 7 fixes elsewhere). The
boundary is domain-conditional vs. universal: the M57 references/ page-type
rules stayed in core (a new "References pages" section) because they are
universal file-family rules this very non-numeric repo uses — refining RR01
rec 9's literal "through Source ingestion" cut, which predates M57. The
cross-skill contract (file map, caps, status, git model, gates, output
discipline, profiles mechanism) stays monolithic per RR01 rec 15.
**Consequences:** Annotates D-024/D-025 (universal-vs-profile stands; the
doctrine's *packaging* is now a module) and D-029 (the shape-free registry
gains a declared pointer: a numeric-work repo names where its records live in
DESIGN.md Conventions; absence is the audit finding — still no validate
CHECK). Non-numeric sessions stop paying for doctrine that never applies.
Locked by `TestModuleExtraction`/`TestRegistryPointer` in
`test_oracle_doctrine.py` (mutation-registered). If a second domain module
ever needs skills to read it unprompted, per-skill wiring is the entry to
supersede.

### D-032 (2026-07-16): History integrity is named IP4

**Context:** RR01 (Q7/rec 10) found "never fabricate, never rewrite, never
renumber" treated as inviolable in at least five places — append-only
work-logs/DECISIONS ("supersede, never edit history"), IDs never reused, the
migration no-invention rule, entomb-verbatim (D-005), catch-up-line
reconciliation — yet unnamed in DESIGN.md's IP list, which is what
`/design-interview`, `cairn_impact`, and the RB `ip-touching` tripwire key
on: work weakening the no-invention rule would not have tripped the tripwire.
Banked as a candidate row pending the user decision an IP change requires.
**Decision:** Name it **IP4** ("History is never fabricated, rewritten, or
renumbered — append-only work-logs and DECISIONS, no-invention migration,
entomb-verbatim, IDs never reused"), approved by the user at the 2026-07-16
plan gate. Docs-only: the practice was already inviolable; this assigns the
checkable id. Rejected leaving it unnamed (the tripwire and impact tracing
stay blind to it) — the candidate row's own framing.
**Consequences:** The `ip-touching` RB tripwire and `cairn_impact` now cover
history-integrity work; the number IP4 is assigned and never reused.
Graduates the "Name IP4" candidate row. If the wording ever needs weakening,
that change is itself IP-touching and requires a superseding D-entry.

### D-033 (2026-07-16): Drop the live-openac router-test candidate

**Context:** M08's Out banked "run the classify-first router empirically in
openac" as a candidate. By its own wording, openac is a separate repo and no
automated evidence can land here — the row could never be crossed off, only
informally remembered. Surfaced at the 2026-07-16 pre-release candidate
triage (`/milestone-plan`), same pattern as the D-027 prunes.
**Decision:** Drop the row, at the user's explicit choice at the plan gate.
Rationale: the router is exercised naturally by every plain-conversation
request in every cairn-adopting repo; a routing defect surfaces as lived
friction and comes back as a concrete bug report or candidate, which is
strictly better evidence than a one-off staged probe. Rejected keeping it as
a parked reminder — a row that cannot ever produce evidence in this repo is
rot, and search-first will find this entry if the idea recurs.
**Consequences:** Candidates drop by one; the M08 archive summary keeps the
historical Out note. If router misrouting is ever actually observed in an
adopting repo, that observation arrives as its own candidate/hotfix — or
supersede this entry to reinstate a deliberate probe.

### D-034 (2026-07-16): PROFILE.md weight cap raised to <120 — supersedes M45's <90

**Context:** M61 T4 (python CI-pair parity) surfaced a latent first-contact
bug: both shipped reference profiles had grown to 97 lines (M49 provenance +
M52 CI blocks landed after the pilots instantiated theirs), while
`cairn/PROFILE.md` — which `cairn-init` copies verbatim from the reference —
was capped at <90. A fresh python/R adopter would fail `cairn_validate`'s
weight-caps check immediately, before ever editing a slot. Exactly the
first-contact breakage M61 exists to prevent, discovered because T4's
addition would have widened it.
**Decision:** Raise the cap to **<120** (tracking-rules weight caps,
`cairn_scripts.LINE_CAPS`, cairn-init §1 comment), and mechanically couple
shipped references to the instantiation cap:
`test_shipped_reference_profiles_are_valid` now asserts every shipped
profile fits under `LINE_CAPS["cairn/PROFILE.md"]`, so profile growth can
never silently outrun the cap again. Rejected: trimming both profiles under
90 (risks mangling guard-locked doctrine across two files; r-package was out
of M61's scope) and banking a candidate while shipping the collision (leaves
first-contact validate broken — the failure mode under repair). User-gated
at the M61 implement amendment gate.
**Consequences:** Profiles keep honest headroom (97 and 104 vs 120); the
coupling test turns the next overrun into a red suite at authoring time.
Supersedes the M45 `<90` choice; if profiles ever approach 120 the remedy
conversation is "move doctrine to a module" (M58 norm), not another silent
raise.

### D-035 (2026-07-16): Candidates stay a flat list — no category grouping in ROADMAP.md

**Context:** A `/milestone-plan` evaluation asked whether the ROADMAP
Candidates section should group rows into categories like "parked" or
"blocked". The parked/actionable signal already exists per row: D-027's
advisory higher-priority-first ordering plus inline trigger prose ("promote
when/if …") on every gated row, which is richer than any category label.
**Decision:** Reject grouping; the flat one-line-per-candidate list stands.
Category names would become de facto sub-statuses (candidates deliberately
carry none — D-027), "blocked" would overload an existing status-vocabulary
word that means something else (in-flight, external blocker, work-log line),
grouping creates a two-places-encode-one-fact drift surface (section
placement vs. trigger prose), and `candidate_count()` plus new validate/audit
machinery would have to learn the convention — structure serving a list the
60-line ROADMAP cap already keeps small (cap remedies cluster rows, never
section them). Also rejected the middle path (a mandated uniform
"promote when:" opener): current rows already state triggers clearly;
formalizing the phrasing is ceremony without new information.
**Consequences:** The Candidates section stays the lightest object in the
system: one line, no file, no ID, no sub-status. Trigger conditions continue
to live in row prose. If the candidate list ever sustainably outgrows
triage-by-ordering (D-027 handled 12 rows without grouping), this is the
entry to supersede.

### D-036 (2026-07-16): Durable-record preview is show-then-commit, four skills, per-skill wired

**Context:** D-035's rationale reached main sight-unseen — `/milestone-plan`
authors D-entries and milestone files post-gate ("solidify autonomously"),
and "deltas, not dumps" biased recaps toward compressing exactly the text
that outlives the chat. The user flagged it live (2026-07-16); per GP4/D-011
the fix is plugin conduct, not memory. Three design choices at the M64 plan
gate.
**Decision:** (1) **Mechanics:** show the drafted text verbatim in chat
immediately before its commit — same turn, no new approval stop; objections
are handled by amend/supersede right after. Rejected a hard pre-commit chip
(adds a stop to every plan/review closeout, against
work-autonomously-between-gates) and summary-only preview (summaries are what
compressed the text away today). (2) **Coverage:** the four gap skills
(plan, review, implement, brief) over D-entries, plan-owned milestone
sections (new + gated amendments), LESSONS lines, archive summaries, and
ROADMAP candidate/graduation rows; exempt work-log one-liners, checkbox
ticks, status mirrors, and PR-branch content (hotfix NEWS/code — reviewable
at the PR), `/design-interview` (co-authors in chat by construction), and
`/cairn-init` (template boilerplate). Rejected extending to `/cairn-release`
changelog consolidation — it mostly reorganizes entries the user already saw
land; re-raise via a candidate if release-time text surprises. (3) **Wiring:**
central rule + a per-skill directive at each commit step, per-skill
guard-locked — the D-021 pattern, because conduct-at-specific-steps drifted
under central-only rules before (M26/M28).
**Consequences:** The pre-commit moment becomes a review moment without a new
gate; "Deltas, not dumps" gains an explicit carve-out. Delivered by M64. If
show-then-commit proves too weak (a veto before main is wanted), the
hard-stop option is the entry to supersede.

### D-037 (2026-07-16): Acceptance chips show what's accepted — gate-time sibling of D-036

**Context:** Hit live in the circumplex repo (2026-07-16): a
`/milestone-plan` session ran a review, then asked the user to accept its
conclusion without the substance ever appearing in chat. "Chips carry
choices, not evidence" states the principle but is the only chip-conduct
rule with no guard and no per-skill wiring, and summarize-don't-paste
pressure compresses exactly the text being accepted — D-036's failure mode,
one gate earlier. Three design choices at the M65 plan gate.
**Decision:** (1) **Form:** a new standalone "Acceptance chips" rule
adjacent to "Chips carry choices, not evidence", plus a cross-reference
from that rule — cleanly anchorable for guards, parallel to M64. Rejected
folding a clause into the existing rule (denser, weaker anchors).
(2) **Wiring:** the five conclusion-feeding skills — plan (question gate),
implement (gate + amendment mini-gates), review (approval gate / fan-out
findings), brief (RB gate + RR routing), milestone (audit triage). Rejected
all nine chip-emitting skills (init/release/hotfix/design-interview chips
choose among user-known options — dead weight) and central-rule-only (the
unwired shape is what drifted here and in the chip/chapter-marker history).
(3) **Verbatim bar:** the verdict and each actioned finding appear
verbatim; a long artifact shows its conclusions section verbatim + the
file path for the rest; a paraphrase never stands in for the accepted
text. Rejected full-text-always (floods chat on big reports) and
summary+path (a summary is what hid the circumplex conclusion).
**Consequences:** Every conclusion gate becomes a decision made with the
evidence in view; the previously-unguarded chip rule gains a guarded,
cross-referenced sibling. Delivered by M65. If a conclusion chip ever
appears in one of the four unwired skills, extend the wiring by
superseding this entry.

### D-038 (2026-07-16): cairn-init's migration gates are acceptance chips — supersedes D-037's init exclusion

**Context:** D-037 wired the acceptance-chips rule into the five
conclusion-feeding skills and rejected the other four on the premise that
their chips "choose among user-known options — dead weight," while
pre-authorizing extension: "If a conclusion chip ever appears in one of the
four unwired skills, extend the wiring by superseding this entry." Hit live
in the hitop repo (2026-07-16): a `/cairn-init` migration ran the step-3
inventory sweep, then fired the disposition gate's AskUserQuestion with no
proposal text in chat (transcript: mark_chapter → two AskUserQuestion calls,
no intervening prose). The premise fails for the migration gates: the
step-3 disposition proposal and the step-7 merge ledger are *produced*
content, not user-known options. A secondary loophole: a disposition
*proposal* is arguably not a "produced conclusion," so the rule's
enumeration could be read as not applying at all.
**Decision:** Extend the wiring to `/cairn-init`'s two migration gates —
step 3 (inventory + proposed-disposition ledger verbatim in chat above the
chip, the adopt-in-place variant included) and step 7 (the migration ledger
in chat above the merge-approval chip, not only in the PR description) —
and extend the rule's enumeration to name a proposed disposition or action
plan awaiting confirmation, closing the proposal-isn't-a-conclusion
reading. Rejected a standalone third rule (the mechanism — substance
verbatim above the chip — is identical to D-037's; a parallel rule would
restate it) and leaving the decision record untouched (planning against a
standing rejection without superseding it). The rejection's premise stands
elsewhere: init's profile/opener/routing chips, release's version confirm,
hotfix's merge chip (diff reviewable at the PR), and `/design-interview`
(co-authors in chat by construction) stay unwired.
**Consequences:** Migration gates become decisions made with the proposal
in view; the dry-run path's existing "present them in chat" bar now binds
the real path's gates too. Supersedes D-037's wiring scope only — its rule
form and verbatim bar stand. Delivered by M66. If a produced-content chip
surfaces in a still-unwired skill, extend by superseding this entry.

### D-039 (2026-07-16): Narration discipline — outcomes and signposts, never a deliberation readout; central rule only

**Context:** Observed live in the hitop repo (2026-07-16): a `/cairn-init`
+ `/design-interview` session narrated its reasoning in italic running
commentary between tool calls. No skill text invites this; the only
adjacent rule, "Deltas, not dumps," governs recaps between gates and says
nothing about the space between tool calls. The M64–M66 verbatim-show
mandates (D-036/D-037/D-038) push sessions toward "show more," and without
a counterweight the showing spills from artifact text into deliberation.
Three choices at the M67 plan gate (2026-07-16).
**Decision:** (1) **Bar:** interstitial chat carries findings, decisions,
and the mandated previews; a one-line signpost before a long step is fine;
a compact summary where a question needs context is fine; a running
readout of reasoning is never emitted. Rejected strict outcome-only (long
silent stretches read as stalled) and banning only the italic format (the
same readout in plain text would comply). (2) **Wiring:** central rule
only, in the rulebook's Output & interaction discipline adjacent to
"Deltas, not dumps" — narration discipline is continuous conduct with no
step to anchor a per-skill directive to, unlike the preview rules (commit
steps, gates). Rejected wiring init/design-interview (no skill text
invited the narration; the conduct is orchestrator-generic) — a deliberate
deviation from the D-036/D-037 per-skill pattern, which exists for
conduct-at-specific-steps. (3) **Carve-outs:** the rule names the
Durable-record preview and Acceptance chips rules as mandated substance it
never licenses compressing; no design-interview carve-out (its grounding
context above question rounds is already mandated by the chip rules).
**Consequences:** Sessions stop reading as a reasoning transcript while
gates keep their verbatim substance. Delivered by M67. If central-only
drifts (narration returns despite the rule), per-skill wiring is the entry
to supersede.

### D-040 (2026-07-16): `changelog` is a required seventh profile slot; "none" legal; all three consumers read the declaration

**Context:** The changelog file was a toolchain fact with no slot: `/hotfix`
step 5 hardcoded "`NEWS.md` for r-package, else the repo's `CHANGELOG.md` /
convention," and each richer profile hardcoded its file name in both its
release-walk and consistency-gate bullets. RR01 rec 11/Q2 banked the slot for
"when the next non-R/non-Python profile is authored." The v1.0 release will
freeze the adopter-facing profile schema, so the M68 plan gate (2026-07-16)
promoted the row early — a schema addition costs one audit-fix line per
adopting repo today versus a repair pass across every adopter after v1.0.
**Decision:** (1) `changelog` is a **required** seventh slot —
`cairn_validate` FAILs a missing/empty slot. Uniform schema over an optional
two-shape form: the profile doctrine already requires a slot with nothing to
declare to say so explicitly. Accepted migration cost: an existing adopting
repo's PROFILE.md gets one FAIL, fixed by an ordinary one-line `/milestone`
audit commit — no cairn-init repair machinery. (2) **"none" is a legal
value**: `/hotfix` skips the changelog-entry step; the release-walk skips
consolidation and derives the version bump from commit history. Rejected
forbidding it (forces ceremony on internal-only repos). (3) **All three
consumers read the declaration** — `/hotfix` step 5 (today's inference
demoted to the absent-PROFILE fallback), and the richer profiles'
release-walk + consistency-gate bullets point at the declared file instead
of restating it. Rejected hotfix-only minimal wiring (leaves the same fact
in three places per profile — the drift the slot exists to end).
**Consequences:** The changelog becomes a declared toolchain fact read
everywhere it is needed; profiles grow ~5 lines each, staying under D-034's
<120. Supersedes the candidate row's own wait-for-next-profile trigger
(early promotion, user-gated at the M68 plan chip). Delivered by M68. If a
repo ever needs a multi-file or per-package changelog declaration, this is
the entry to supersede.

### D-041 (2026-07-17): No auto-increment of the r-package dev version; `.9000` is set once at release

**Context:** A `/milestone-plan` session asked whether the r-package profile
should auto-increment the dev-version suffix as commits land
(`0.1.0.9000 → .9001 → …`). cairn today touches the version only at release —
the `release-walk` slot bumps `Version:` and the handoff has the user run
`usethis::use_dev_version()`, which sets `.9000` once.
**Decision:** No auto-increment, per commit or per milestone. The documented R
convention (usethis / *R Packages*) sets `.9000` once via `use_dev_version()`
and bumps the fourth component only when a downstream package must *detect* a
feature via a version check — not on a commit or milestone cadence. Three
reasons beyond convention: the git SHA already uniquely identifies any dev
build (`remotes`/`pak` record `RemoteSha` on install), so a counter is
redundant; rewriting DESCRIPTION on every checkpoint commit churns the file and
makes it a merge-conflict magnet; and it would require a new content-mutating
pre-commit hook class cairn deliberately lacks (its hooks are advisory/guard).
Rejected the per-milestone middle variant (keys the counter to a real unit but
still exceeds the convention for a modest payoff) and the literal per-commit
form.
**Consequences:** The r-package profile's single-`.9000`-at-release model
stands unchanged; no profile edit, no milestone. If a cairn-tracked R package
ever needs machine-detectable dev increments (e.g. a downstream that gates on a
mid-cycle feature), the maintainer bumps the suffix by hand per the convention
— or supersede this entry to add cadence machinery.

### D-042 (2026-07-18): Out-of-band idea capture is paired with a candidate row, never forbidden — rulebook rule + a D-017-shaped hook

**Context:** Hit live in the circumplex repo: an idea surfaced as a
background-task ("suggested fix") chip and was never logged through cairn, so
the only record of it lived in a runtime affordance the tracking files know
nothing about. The escape happened in plain conversation with no cairn skill
active — precisely the residual D-009 accepts, which is why the memory
boundary needed a hook (M19/D-017) rather than prose alone. Four choices at
the M71 plan gate (2026-07-18).
**Decision:** (1) **Enforcement:** rulebook rule **and** hook. Prose alone
would not have caught this instance, since `tracking-rules.md` never loaded;
hook alone would leave no citable, guard-testable doctrine. Rejected both
single-layer forms. (2) **Stance:** the chip is *paired*, not forbidden — it
usefully spins work into its own session; the defect was it being the sole
record. The rule denies it record-of-record status and requires the idea to
also land as a ROADMAP candidate row (search-first applies). Rejected
discouraging chips in cairn repos (throws away a working affordance to fix a
bookkeeping gap). (3) **Scope:** the rule is written channel-agnostically —
any out-of-band capture channel (task chips, scratch TODOs, ad-hoc notes) —
while the hook wires the one channel that mechanically exists today, so a
future channel inherits the doctrine without a rulebook edit. Rejected naming
the chip tool in the rule (the next channel repeats the escape).
(4) **Strength:** the softest lever, D-017's exactly — `additionalContext`
with no `permissionDecision`, so the chip is created normally and Claude
reads the reminder next turn. Rejected a per-chip confirmation dialog (the
nag fatigue D-017 already rejected).
**Consequences:** Ideas stop having a second, invisible home; IP3's
conservation guarantee extends from "what the user asked for" to "what the
session surfaced." A second guard joins `memory_guard` in the
boundary-nudge family, so the pattern is now a family, not a one-off.
Delivered by M71. Live-fire waits for a brand-new conversation (hook
registrations snapshot at process start — M60). If the nudge proves noisy, or
a channel needs blocking rather than pairing, this is the entry to supersede.

### D-043 (2026-07-18): cairn's collaboration model is one operator plus outside contributions — the single-writer assumption is stated, not engineered away

**Context:** Asked how cairn would survive a collaborative workflow with
occasional outside PRs and issues, three Explore sweeps found the
single-writer assumption is nowhere stated (`solo|team|concurrent|contributor`
returns zero hits in `tracking-rules.md`, `DESIGN.md`, and `README.md`) and
therefore nowhere reasoned about. Two distinct failure families surfaced.
(a) **Intake:** the doctrine names a destination with no door — external PRs
are to be "reviewed to the hotfix bar" (`tracking-rules.md:199-203`) but
`/hotfix` is branch-creation-first (`skills/hotfix/SKILL.md:27-30,45`), its
`description:` fires only on bug *reports*, and no skill or script ever reads
GitHub (zero `gh`/`urllib` hits across all five `scripts/*.py`). (b)
**Concurrency:** two operators race the tracking files — no ID allocator,
duplicate D-numbers auto-merge and validate green, `/milestone-plan` never
fetches, and `check_single_in_progress` is a hard FAIL they trip by
construction. Separately, RR01 §10 rec 4 had already recorded that a
GitHub-UI merge, a merge queue, or an unplugged contributor bypasses
`merge_guard` entirely; it was never actioned.

**Decision:** cairn's supported collaboration model is **one cairn operator,
with contributions arriving from people who do not run cairn**. Three choices
follow. (1) **Boundary over machinery:** where enforcement is
agent-session-scoped and degrades to honor-system, cairn says so in the
rulebook and README rather than pretending otherwise — every guard is a
PreToolUse hook on the local agent's own Bash calls, so no amount of prose
makes it cover a UI merge. Closes RR01 rec 4. (2) **The marker gains a
binding:** `merge_guard` today only checks that `cairn/.merge-approved`
*exists* (`hooks/merge_guard.py:46-60`) and never reads it, so a marker
written for one PR authorizes any merge in that clone; it will parse the body
and refuse a `gh pr merge` for a PR the marker does not name, with the
no-PR-token body keeping today's behavior for back-compat. (3) **Intake gets
a door, not a new skill:** `/hotfix` learns to adopt an existing PR
(`gh pr checkout`) rather than always creating one, and `/milestone` learns to
enumerate open issues; a tenth skill was rejected — most steps would duplicate
`/hotfix`, and the DESIGN skills count is guard-asserted. Rejected: writing
the doctrine down without the marker fix (leaves a live forgery-adjacent hole
the same milestone is documenting); a standalone `/pr-intake` skill; and
solving concurrency now (it is not the described need — postponed in the
ROADMAP, which is where postponement lives, not rejected here).

**Consequences:** The single-writer assumption stops being invisible. The
approval marker becomes a token about a specific PR rather than a bare
presence bit. `/hotfix` becomes bidirectional — it can author a fix or adopt
one — which makes the intake paragraph's hotfix-bar disposition executable for
the first time. Delivered by M72 (boundary + binding), M73 (the PR door), M74
(issue enumeration). IP1 is touched only in its documentation and mechanical
backing, never weakened. If a second cairn operator ever appears, the
concurrent-operator candidate row is the entry point; if the marker binding
proves too strict for a workflow that merges without `gh pr merge`, this is
the entry to supersede.

### D-044 (2026-07-18): `leave` is a legal fourth issue disposition, narrowed to noise/duplicates/already-covered — annotates D-042

**Context:** M74 shipped `/milestone` §3 with four dispositions (candidate
row / `/hotfix` / `/milestone-plan` / **leave**), but the rulebook's Intake
enumeration (`tracking-rules.md:199-200`) names only "`candidate` rows or the
hotfix path". M74 knew and deferred it — its archive records "`leave` shipped
though the rulebook's Intake enumeration omits it → candidate row" — and its
review scored the finding 40 (sub-threshold) because AC3 named `leave`, so
review correctly declined to reinterpret its own criterion. The gap is not
cosmetic: an acknowledged-but-left item persists with the GitHub issue as its
only record, which sits awkwardly beside D-042's "an inbox feeds the ROADMAP,
it never substitutes for it" and beside that entry's extension of IP3's
conservation guarantee from "what the user asked for" to "what the session
surfaced".
**Decision:** Legitimize `leave` in the rulebook, **narrowed** to noise,
duplicates, and items already cross-referenced in cairn — never anything
genuinely new. The IP3 reading this rests on: IP3 forbids a *silent* drop,
and a `leave` is neither silent nor unilateral — it is proposed verbatim
above an acceptance chip (D-037/D-038) and chosen by the user with a stated
reason. What the narrowing adds is that the only items eligible are ones
cairn's record already covers or that carry no information to conserve, so
conservation is preserved in substance rather than merely in ceremony.
Rejected: **dropping `leave` from the skill** to match the rulebook's
three-way form (forces a ROADMAP row for spam and duplicate issues — row
rot, and D-035 keeps candidates a flat list precisely because the section
stays small); and **legitimizing it unnarrowed** with only "state the reason"
as the bar (leaves the D-042 tension intact — a real idea could be left with
the GitHub issue as its only record, which is the substitution D-042
forbids). Settled in-session rather than escalated to Fable at the M75 plan
gate; the question is narrow and the narrowing is what answers it.
**Consequences:** Annotates D-042 — its inbox-never-substitutes rule stands
and is *sharpened*: what may be left is exactly what the ROADMAP would learn
nothing from. The skill's four dispositions are unchanged; the rulebook moves
to meet what M74 shipped. Delivered by M75, guarded label-inclusively per the
M74/F3 lesson. If `leave` is ever observed absorbing items that were
genuinely new, the narrowing is the entry to tighten — supersede here.

### D-045 (2026-07-18): Tracking files split into history and current knowledge; current-knowledge records are corrected in place, marked — annotates D-015

**Context:** M75 found `LESSONS.md:41` (written by M71) stated the Claude Code
hook matcher rule wrongly, and corrected it in place — marked
`(M71, corrected M75)` — because appending a correction would leave the wrong
rule readable to every plan-time harvest, which is the only thing the file is
read for. Review accepted that as the lesser evil while recording that **no
rule sanctions it**, and spun the gap off as a candidate. The gap is real and
self-contradictory: D-015 and the file map both call `LESSONS.md`
"append-only", yet the same sentence caps it at 50 lines and instructs pruning
the stalest entries — the file has never been append-only in the DECISIONS
sense, and at 49/50 lines a prune was already due. Separately, M75 also
corrected `references/claude-code-hooks.md` in place with no rule covering
that either, so the gap was already wider than LESSONS.

**Decision:** Split the tracking files by what they are for. **History** —
`DECISIONS.md`, work-logs, milestone IDs, entombed `legacy/` files — records
what was decided or done at a time, and is never edited: supersede, never
rewrite. **Current knowledge** — `LESSONS.md`, `references/` pages,
`DESIGN.md` — records what is true *now*, is read to act on, and is
**corrected in place when proven false**, with the correction marked
(`(M71, corrected M75)`) and git holding the original. Three sub-choices at
the M76 plan gate (2026-07-18). (1) **Mechanism:** correct in place, marked.
Rejected appending a superseding line and deleting the old (same end state,
loses the visible link) and strike-through-keep-both (burns two lines of a
50-line cap per correction and leaves the wrong text readable — the failure
being fixed). (2) **Scope:** the general split, not a LESSONS-only protocol —
M75's reference-page correction proves the narrow form leaves the same hole.
Rejected extending the milestone-file write-mode table to every tracking file
(over the sizing tripwires for the payoff). (3) **IP4:** record the reading,
do not amend the principle. IP4 enumerates "append-only work-logs and
DECISIONS … no-invention migration, entomb-verbatim, IDs never reused" —
`LESSONS.md` was never in that set, so M75's in-place correction never
violated IP4; what was wrong was the file map's loose "append-only" label.
IP4's wording is unchanged. Also rejected: a `cairn_validate` CHECK for
correction markers — **declined, not deferred** — since advisory doctrine has
never been a validate gate (M33/M42/M49) and a marker is prose a reviewer
reads, not a parseable invariant.

**Consequences:** Annotates D-015 — its lessons-loop, one-line format, and
50-line cap stand; only the "append-only" label is corrected, to the mode the
file always actually had. Correcting a false lesson stops being an unsanctioned
deviation and becomes the documented path, which matters because a wrong lesson
is *actively* misleading: it is harvested into every subsequent plan. IP4 is
narrowed in nothing — it is read as already excluding LESSONS. Delivered by
M76. If a correction marker ever needs to be machine-checkable, or if
in-place correction is observed erasing something git alone did not preserve,
this is the entry to supersede.

### D-046 (2026-07-18): The milestone cap exempts the work log too; wrapped entries warn rather than fail — annotates D-030

**Context:** D-030 narrowed the 150-line milestone cap to the plan-owned body
and exempted the review-exclusive `## Review` section, because evidence written
at review time was scrambling plan-owned content. D-045 then classified the work
log as **history** — never edited. The two meet badly: the work log is inside
the plan-owned body, so the sanctioned cap remedy ("compress the heaviest
section") can land on a section IP4 forbids touching. M76 hit it live at
158/150 with the work log the heaviest section at 58 lines, and escaped by
reflowing every entry to the one-physical-line format the rulebook already
mandates — no entry removed, no substance changed — while recording that the
escape is finite and spinning the gap off as a candidate. Measurement at the
M77 plan gate (2026-07-18) put the mechanism beyond doubt: across M72–M76 the
work log runs 15–24 lines and is never the heaviest section *once reflowed*,
and M76's own 15 entries measured 58 lines wrapped versus 21 reflowed. The leak
is hard-wrapping — this repo writes ~80-column prose, the rulebook says
"Work-log entries are one line each", and nothing distinguished the two.

**Decision:** Three choices at the M77 plan gate. (1) **Exempt the work log**
from the plan-owned cap, as `## Review` already is, and drop it from the
heaviest-first diagnostic so the breakdown never names a section the operator
may not trim. This removes the collision structurally rather than relying on an
author noticing that the heaviest section is off-limits. (2) **Add a
wrapped-entry advisory, not a check** — a work-log entry spanning more than one
physical line renders `WARN`, exit-code neutral. The guard is what keeps a
now-unbudgeted section from filling with pasted output, but once the section
costs no budget a wrap is untidiness, not damage; a hard FAIL would block a
milestone at the gate over formatting. Rejected FAIL severity for that reason,
and rejected shipping the exemption bare (nothing would then notice bloat, since
the one-line mandate has never had enforcement). (3) **The milestone-local
`## Decisions` section stays counted** — D-030 rejected exempting it because it
is meant to stay brief with cross-cutting entries promoted to this file, and
that release valve is real and absent from the work log. Also rejected: a
separate work-log sub-cap, which reprises exactly the second-number complexity
D-030 declined for `## Review`.

**Consequences:** Annotates D-030 — its plan-owned-body scoping and `## Review`
exemption stand; the exempt set gains one member for a different reason
(un-editable rather than differently-owned). The cap stops being able to demand
an IP4 violation, so M76's reflow escape stops being load-bearing. IP4 is
untouched in wording and in reading. Graduates the work-log-vs-cap candidate at
post-merge hygiene (M35). The adjacent budget-first-drafting candidate is
unaffected — it concerns first drafts landing under cap, not monotonic growth.
Delivered by M77. If an unbudgeted work log is ever observed absorbing pasted
output despite the advisory, the FAIL severity is the entry to supersede.

### D-047 (2026-07-18): The gitignored source shelf is `references/sources/`, not `references/pdf/` — a post-1.0 scaffold rename on a deprecation cycle

**Context:** M78 shipped a `**Provenance.**` block whose source pointer is
explicitly either a shelf path *or* "the URL plus how it was retrieved" for a
non-PDF source — but the shelf cairn scaffolds is named `pdf/`, so a retrieved
HTML page, dataset, or transcript has no home that matches its name. The name
was cairn's own from the start (`cairn_scripts.REQUIRED_GITIGNORE`, the
`cairn-init` §1 tree, the rulebook file map, the ingestion recipe, the
source-note template), not an adopting repo's choice, so every adopter
inherited the mismatch. Raised by the user at the M79 implement gate and
folded into that milestone's scope.
**Decision:** Rename to `cairn/references/sources/` everywhere cairn writes
it. Because cairn is post-1.0 (v1.0.0, 2026-07-16) and the required
`.gitignore` entry is adopter-facing behavior, the rename follows the
deprecation cycle rather than breaking adopters: `check_scaffold` accepts the
legacy `cairn/references/pdf/` entry in place of the new one, and a new
non-failing `scaffold deprecations` advisory names the successor. Rejected a
hard FAIL on the old entry (the D-040 `changelog`-slot precedent, but that was
a slot a repo had to author — this is a rename with a mechanical successor, so
failing a repo for cairn's own rename is the wrong severity) and keeping
`pdf/` with prose explaining it holds non-PDFs (the name is the documentation;
prose that contradicts it is the defect).
**Consequences:** The shelf name stops contradicting the provenance block
above it. Adopting repos keep passing until they migrate, then the advisory
goes quiet; `check_references` skips both shelf names when walking, so an
un-migrated repo's shelf is never mistaken for pages. Delivered by M79. If a
second scaffold entry is ever renamed, `DEPRECATED_GITIGNORE` is the map to
extend; if the deprecation window should ever close into a hard FAIL,
supersede here.

### D-048 (2026-07-18): The copy-run rule names three cases, and wires per-skill at the steps that hand over

**Context:** M35 shipped "copy-run commands get their own fenced block" into
`tracking-rules.md` as one of five wording tweaks, guard-locked centrally and
mutation-registered — but with no per-skill wiring. It drifted exactly as
D-021/D-036/D-037/D-038 each found a central-only conduct rule does:
`/milestone-review` step 10 came to instruct the violation outright ("naming
the obvious next action **inline**"), `/milestone-brief`'s manual-run option
hands over a Fable prompt in a blockquote (no copy button), and
`/cairn-release` step 4 gives its terminal-actions checklist no format
directive at all. Reported by the user (2026-07-18) as post-review messages
suggesting commands the user cannot copy.
**Decision:** (1) **Rule text:** state three cases, not two — a command handed
to the user to run gets its own fenced block; naming a command, path, or
symbol in prose gets inline backticks; a routing-chip arrow gets
neither, because the orchestrator invokes it on selection (D-022). The third
case was true but unstated, which is what let the boundary blur. Slash
commands (`/clear`, `/milestone-plan`) are named as covered, since every
observed instance is a slash command and "a command" read as shell-only.
(2) **Wiring:** the three skills that actually hand a command over, not all
nine — the D-036/D-037 scoping, on the grounds that a directive in six skills
that never hand over is dead text that dilutes the signal.
(3) **Handoff vs. mention:** `/milestone-implement`'s "a safe `/clear` point"
stays inline. It states a property of the moment rather than telling the user
to act, and a routing chip sits immediately beside it offering the routes; a
guard asserts it stays inline so a later over-fire is caught mechanically
rather than left to judgment. Rejected fencing every command the user might
type (uniform but fences description, not instruction) and central-rule-only
(the shape that already drifted once).
**Consequences:** The handoff moment becomes copyable at every step that has
one. Delivered by M86. If a fourth handoff site appears in a still-unwired
skill, extend the wiring by superseding this entry; if the three-way
distinction proves too fine to apply, the two-case form is the entry to
supersede.

### D-049 (2026-07-18): Density thresholds are the mass each line cap permits at MEASURED item length — supersedes M84-D1's assumed means

**Context:** M84-D1 derived both `record density` thresholds as
`item_cap × target_mean` — ROADMAP `60 × 150`, LESSONS `50 × 340`. Neither mean
was measured. At the moment M84 set it LESSONS' real mean was **581** (41% above
the assumed 340), and ROADMAP's 150 described only its table rows (154) while
candidate rows ran **679**, 4.4× that. Both thresholds therefore bound before the
line caps they exist to backstop: LESSONS' 17,000 admitted 29 lessons against an
item capacity of 35 (83%), ROADMAP's 9,000 admitted 16 against 40 (40%). The
advisory fired at ordinary density, and for three consecutive hygiene passes
(M84/M85/M86) its only available remedy was compressing unrelated lessons — a
per-milestone tax on records the milestone never touched, against a file M61
records has already been damaged once by bulk edits. The item axis meanwhile went
inert: LESSONS held 36 lessons from M41 through M83 and 29 since, never
approaching 50, because lessons are consolidated rather than appended.

**Decision:** A threshold is **the mass its own line cap permits at measured item
length** — non-item mass + capacity × the measured mean item length, rounded up
to the next 500 so it can never sit below what the line cap allows, where
capacity is `(line cap − 1) − fixed non-item lines` (the cap FAILs at `>=`, so
49 and 59 lines are the permitted counts). Measured 2026-07-18 (M87-D1):
ROADMAP **< 21,000**, LESSONS **< 20,500**. The mean is *measured*, never assumed or carried over:
compression is the prescribed weight remedy and consolidating items raises the
mean, so the derivation's own input moves every time the remedy is applied.
Rejected a mechanical mean-drift test (D-034's coupling move), chosen at the M87
plan gate in favour of stating the basis in prose — a drift tolerance loose
enough not to cry wolf is not obviously stronger than the rulebook sentence;
re-openable by superseding this entry. Also retired M84's prune regression
anchor: `dbf1068`, the state it calibrated on, was a boundary-rule cleanup
(graduation breadcrumbs restating archive-owned history), not a density
judgment — its own commit message says the density defect stayed unfixed there.

**Consequences:** Supersedes M84-D1's derivation; M84's two-axis design, its
opposite remedies, and its WARN-not-FAIL severity stand untouched. The advisory
returns to its stated job — flagging prose bloating *inside* lines — instead of
firing at ordinary density. Trades against GP1 ("caps keep always-read files
small"): the item cap remains the hard small-keeper, and a threshold binding
before it was not keeping files small but taxing unrelated records. Both files
now carry real headroom (16,998/20,500 and 9,186/21,000). ROADMAP's mean is
blended over a bimodal population — table rows ~158, candidate rows ~683 — so it
tracks composition as well as prose length; a re-measurement checks the mix, not
just the mean, this being the mirror of the error charged above (M87 review F2).
And because a threshold is capacity at FULL item count, a file below its item cap
carries slack proportional to its unused slots: the two axes divide labour, and
neither backstops the other's saturation (F3). Locked by the re-based
fixtures in `scripts/tests/test_scripts.py` and the stated↔enforced coupling in
`skills/tests/test_record_density.py`. If measured means ever drift far enough
that the prose mandate proves too weak, the drift test is the entry to supersede.

### D-050 (2026-07-19): Release timing is user-declared — a release milestone parks as `blocked`, not as a routable next action

**Context:** cairn repeatedly nominated a CRAN release as the next action in
two downstream repos long before the maintainer wanted to ship, then kept
nominating it. `/cairn-release` is careful never to self-submit, but nothing
protects the release *milestone*: it is modelled as an ordinary milestone
carrying `Priority: high` and a dependency fan, while every routing surface
(`cairn_next.py`, `/milestone` §3, the routing chips) reads only
`(status, priority, deps)`. A release's readiness condition is not a
dependency graph — it is a maintainer judgment about when to ship — so once
such a milestone exists it is recommended forever. Reproduced live:
circumplex M7 (`review`, high) is the top recommendation, `review` being the
highest-precedence branch (`cairn_next.py:31`); intraclass M48 (`planned`,
high, all 8 deps satisfied) is the only workable planned row. The maintainer
had already recorded the no-pressure intent twice — M21 (2026-07-12) parked
circumplex release-prep as a `blocked` milestone at a user gate, and
circumplex D-008 plus M7's own Goal both state there is no release-time
pressure — and ordinary status progression erased the parking while the prose
stayed invisible to routing.
**Decision:** Release timing is declared by the user, never proposed by cairn.
Mechanically: reuse the existing `blocked` status, widening it so "the
maintainer has not opened the release window" is a legitimate blocker, and
legalize `planned → blocked` and `review → blocked` so parking is reachable
from the states a release milestone actually sits in. `blocked` already earns
this for free — `cairn_next` excludes it from `_workable` and from the
recommendation ladder, printing it under "Externally blocked"
(`cairn_next.py:61-64`) — so no script, parser, or vocabulary change is
needed. `/milestone-plan` gains a release-shaped tripwire: release framing
must ask the user to declare the window, and absent a declaration lands as a
`candidate` row. `cairn_validate` gains a `release window` advisory catching
the drift back. Rejected: (1) a new status word (`held`/`deferred`) — the
vocabulary is "exactly these seven" and is threaded through validate, next,
every skill, and the guard tests, a large change for identical routing
behaviour; (2) a `Release-window:` header slot — adds a field to parse,
validate, and guard, and creates a second place where release intent is
encoded, the two-places-encode-one-fact drift surface D-035 rejected.
**Consequences:** A release milestone is silent until its window opens; the
maintainer's "not yet" survives as status rather than as prose no surface
reads. Distinguished from D-035, which rejected "blocked" as a *candidate
section grouping label* partly because it "would overload an existing
status-vocabulary word that means something else (in-flight, external
blocker, work-log line)" — that reasoning is about candidate rows and affirms
what `blocked` means on a real milestone; this decision widens the "external"
gloss, which had been read as CI/upstream only. If an expiry model is ever
needed — a declared window going stale — this is the entry to supersede.

### D-051 (2026-07-19): Lessons retire by enforcement or ownership — LESSONS.md gets an outflow, not just a ceiling — annotates D-015

**Context:** `cairn/LESSONS.md` had one way out — D-015's "prune the stalest
when full" — and it fires only at the cap, ranks by age, and loses content
outright. Everything else was inflow. The file reached both its limits at once:
49 lines against `LINE_CAPS` `<50` (`check_caps` FAILs at `>=`, so 49 is the
last permitted count) and 20,466 chars against the 20,500 threshold D-049 set —
zero item headroom, 34 characters of weight headroom. The next milestone's
post-merge hygiene could not capture a lesson without failing the hard `weight
caps` CHECK, and could not compress its way in either. Meanwhile the practice
this entry formalizes already existed unsanctioned: M53 graduated M39/M40/M47
when the mutation harness mechanized the trap they warned about
(`archive/M53-prose-guard-mutation-harness.md:17`), by hand, with no criterion —
so it was unrepeatable and invisible to every later pass. And the file's real
redundancy is invisible to age: `LESSONS.md:16` taught the three unittest
commands `cairn/PROFILE.md`'s `verify` slot already stated.

**Decision:** A lesson leaves `LESSONS.md` on either of two criteria.
**Enforcement** — a test *fails on the mistake the lesson warns about*. The
discriminating word is *fails*, not *exists*: a guard in the same area is not
enforcement, because most guard-naming lessons here teach the judgment the
guard does not make, and `LESSONS.md:34` says so in its own words ("The harness
catches neither"). **Ownership** — another tracking file's slot owns the
content; the retiring milestone may *move* it there, not merely find it already
duplicated. A lesson covered only in part is **trimmed to its uncovered
remainder**, never kept whole. A retired lesson leaves no line behind: it is
deleted, git holds the original, and the retiring milestone's archive summary
names what it graduated — the form M53 already used. The check runs at
`/milestone-review` post-merge hygiene beside capture, **scoped to what the
milestone shipped**, never as a full re-sweep. Rejected: (1) an in-file
graduation breadcrumb — D-049 already retired that pattern as restating
archive-owned history, and it spends the budget it exists to free; (2) a
separate graduated-lessons file — a second record of what LESSONS holds, the
divergence vector M56 rejected; (3) mechanizing age-based retirement — D-015's
prune stands as the last resort, but age is the weakest signal and automating it
would evict load-bearing lessons by date; (4) re-evaluating every lesson each
hygiene pass — that taxes every milestone with judgment over records it never
touched, the cost D-049 objected to in the compression remedy.

**Consequences:** Annotates D-015 — its one-line format, its 50-line cap, and
its prune-when-full all stand; retirement is a second and stronger outflow that
runs first, so pruning by age becomes the genuine last resort it was always
meant to be. Distinct from D-045, and the distinction is load-bearing: a
retired lesson is **not a false one**. Correction fixes what is wrong;
retirement removes what is redundant. Conflating them would license deleting a
lesson merely disputed, which is why the criteria are about coverage and
ownership, never about whether the lesson still reads as true. Serves GP1 by
giving the cap an outflow rather than only a ceiling, and GP4 by making the
guard the lesson's endpoint instead of a parallel record of the same rule.
Delivered by M92. If retirement is ever observed removing a lesson whose trap
then recurs, this is the entry to supersede.

### D-052 (2026-07-19): The per-line axis covers non-item lines; `ROADMAP.md` joins current knowledge — narrows M84, annotates D-045

**Context:** cairn's `Last hygiene check` stamp had no stated shape. All three
write sites said only "update" it (`skills/milestone/SKILL.md:104`,
`skills/milestone-review/SKILL.md:185`, `skills/cairn-init/SKILL.md:109`), which
reads as "add to", so each pass prepended a parenthetical and demoted the last
to `Prior:`/`Earlier:`. In two adopting repos the stamp reached 1,870 chars
(intraclass) and 3,152 chars (circumplex) — the latter 28% of its whole
ROADMAP, on one line. Both measured 2026-07-19; circumplex's changed again the
same day, and the way it changed is the sharpest evidence for this entry. Its
`review M42: done` hygiene pass (19:27) rewrote the stamp and left it at 2,568
chars — still 6.4x over the cap set below — because the instruction it followed
said "update", so it compressed the chain instead of replacing it. Both weight axes were structurally blind: the item cap
counts lines (35 of 60) and D-049's `record density` counts whole-file mass
(11,410 of 21,000), so `cairn_validate` printed `OK record density` over the
defect, verified live in intraclass. cairn's own instance was pruned by hand on
2026-07-18 (`dbf1068`) touching one file and no skill, scaffold, or guard —
which is why it neither propagated nor prevented regrowth, and why the same
complaint returned a day later. That commit's own message said the defect
"wants its own milestone".

**Decision:** Two narrowings, one milestone (M93).

**(1) The per-line axis covers non-item lines only.** M84 rejected a per-line
warn outright, and `tracking-rules.md` recorded the rationale verbatim:
"pressure on individual line length would reward splitting an item across lines
and corrode the one-item-per-line format both parsers depend on." That reasoning
is sound and is **kept, not overturned** — it is a statement about *item* lines,
where a parser reads one record per line and splitting corrupts it. It has no
purchase on a heading, preamble, stamp, or HTML comment, which no parser reads
positionally and which can therefore be capped without any incentive to split.
Item lines (table rows, candidate bullets, lessons) remain exempt by
construction, not by threshold. `NON_ITEM_LINE_CAP = 400`, WARNing at `>=` per
the severity split that keeps the weight axis advisory and the item axis a hard
CHECK. The number is derived from a survey of real non-item lines across all
six cairn repos on 2026-07-19, both capped files each (healthy max 245 —
intraclass's terminal-row-retention comment — then 230/194/141/119/105/102/101),
leaving 154 characters — 63% — of headroom over the worst healthy line while
sitting 4.7× below intraclass's 1,870 and 6.4× below circumplex's post-rewrite
2,568. Measured, never assumed (M87). The peak circumplex figure quoted in the
Context above (3,152, i.e. 7.9×) is the pre-rewrite value and is kept there as
history; every ratio stated here is against the current measurement, since one
entry stating a defect at two different multiples is the drift this very
milestone exists to stop (M93 review F3/88 — the first draft did exactly that).

**(2) `ROADMAP.md` is current knowledge.** D-045 split the tracking files into
history and current knowledge but enumerated neither list to include
`ROADMAP.md`, leaving the most-corrected file in the system unclassified. It
meets every term of the current-knowledge definition: it is the sole authority
on *current* status, every transition rewrites a row in place, and terminal-row
retention already deletes rows outright on the grounds that archive and git stay
authoritative. So replacing the stamp is not an IP4 history edit — `git log`
holds every earlier stamp verbatim and `milestones/archive/` holds the detail
behind it. Rejected: classifying the stamp line alone, which would leave the
next ROADMAP-correction question hitting the same void.

Also rejected: exempting the `_Released …_` line from the cap. It grows ~33
chars per release and crosses 400 in roughly nine, but the remedy there is this
entry's own thesis — keep the current version, let git hold the rest — and an
exemption would carve out precisely the growth pattern being fixed.

**Consequences:** Narrows M84's rejection; annotates D-045 by naming the file it
omitted; leaves D-049's whole-file thresholds untouched (this is an axis beside
them, not a retune). The stamp becomes a one-line record of the current check
only. intraclass and circumplex are not edited here — their own next
`/milestone` audit will flag them, which is the advisory proving itself in the
field. If a non-item line ever legitimately needs to exceed 400 characters, this
is the entry to supersede.

### D-053 (2026-07-19): GP1 names a bounded read cost, with the mechanism stated per file-class — supersedes its "caps + archiving" clause

**Context:** GP1 read "Efficient — store decisions and outcomes, not minutiae;
caps + archiving keep always-read files small." RR02 found the second clause
false of the two largest always-read files. RR03 (Q6) established that it
cannot be repaired by practice: no cap or archive is legal for `DECISIONS.md`
under IP4, and `skills/shared/tracking-rules.md` was never capped on either
axis. D-049 had already recorded a formal trade against GP1 in its
Consequences. Nine weight-management milestones (M84-M94) chased a quantity the
principle named but could not deliver, and RR02's own "Beyond the brief" found
weight governance to be the largest single contributor to the growth it exists
to govern.

**Decision:** Amend GP1, keeping the number (never renumbered, never reused):

> GP1: Efficient — store decisions and outcomes, not minutiae; every
> always-read surface keeps a bounded read cost: caps with outflows bound the
> item-listed files, recorded editorial passes bound the rulebook, and history
> is bounded by reading less of it, never by shrinking it.

Wording is RR03 §6's proposal verbatim, approved by the user at the RR03 ingest
gate on 2026-07-19. Rejected **retiring** GP1: the item caps and archive
discipline it licenses are the parts of weight governance that settled on first
shipping (RR02 Q2), and retiring the principle would discard them along with the
false clause. Rejected **keeping the wording and correcting the practice**: that
is impossible for `DECISIONS.md`, where IP4 makes both named mechanisms illegal.

**Consequences:** The principle names the goal (bounded read cost) rather than a
single mechanism, and states a distinct mechanism per file class — RR03 Q5's
"three fitted mechanisms, one shared frame", where the frame is D-045's
history/current-knowledge split. IP4 is untouched and explicitly confirmed as
the right constraint (RR03 Q4, which looked for the case against it and found
none). D-049's recorded trade against GP1 is retrospectively coherent: it traded
against a clause this entry removes. M95 (re-cut) and M96 inherit the amended
wording as their editorial criterion; M97 is the "reading less of it" mechanism
for history. If a future always-read surface fits none of the three named
mechanisms, this is the entry to supersede.

### D-054 (2026-07-19): The DECISIONS sweep is bounded — headings scanned, matched entries read whole and back-referenced — annotates IP2's collision-check reading

**Context:** `/milestone-plan`'s session start and its collision / search-first
sweeps read all of `cairn/DECISIONS.md` — 95,374 chars across 53 entries, over
half of a ~183,000-char plan-time read. Under IP4 the file is append-only and
can never shrink, so the only available remedy is reading less of it (RR02 Q4,
RR03 Q4). A *generated* index was rejected as the divergence vector M56 and
D-051 already refused: the `### D-` headings are themselves a zero-divergence
index at 5,326 chars flat (5,378 newline-inclusive), 5.6% of the file, measured
2026-07-19.

**Decision:** The sweep scans the `### D-` headings, reads every matched entry
**whole** before surfacing anything, and **back-references** each match by
searching its own `D-0NN` id across the file. Three mitigations bound the
recall cost, and the trade is stated rather than slipped in as an
optimization:

1. **Heading quality (prospective).** A heading names its subject and any entry
   it supersedes, annotates, or narrows. A `cairn_validate` advisory reports
   failing headings by id. It **WARNs and never FAILs**, per the severity split
   D-049/D-052 settled — heading quality is a judgment about prose, not a
   structural fact — and it is scoped to entries from **D-054 onward**.
2. **Back-reference.** Three legacy headings hide a supersession in their body:
   D-012 omits D-010, D-014 omits D-013, D-019 omits D-003. IP4 forbids
   repairing them, so the read protocol closes the gap instead — matching
   D-013 and searching `D-013` surfaces D-014. Grandfathering without this step
   would have left the recall hole those three entries create.
3. **The scan is a model read, not a literal grep.** A heading is matched
   semantically, so a subject named in different words than the query still
   matches; the bound is heading *quality*, not keyword identity.

**Consequences:** Annotates IP2 — prior state is still surfaced, never silently
obeyed or overridden, and a collision is still **quoted verbatim from the full
entry, never from the heading**. What changes is recall, not the obligation:
recall shifts from full-text to heading-plus-targeted-read, so a collision whose
heading fails to name its subject *can* be missed where a whole-file read would
have caught it. The user was shown this cost and accepted it at the RR02 ingest
gate on 2026-07-19. IP4 is untouched — nothing is edited, moved, deleted, or
renumbered; this entry changes how the file is read, never what it holds.
Archival-with-tombstone stays parked (RR02 rec 6): once the read is bounded it
buys almost nothing, the heading scan growing ~100 chars per decision. If the
heading scan itself ever becomes the cost, that candidate is the entry to
supersede.

### D-055 (2026-07-20): Lessons also leave by maturation — a stabilized family graduates whole into a doctrine module — annotates D-051

**Context:** D-051 gave `LESSONS.md` an outflow, and the file grew anyway:
20,466 chars at M92 to 21,085 at M98, reaching 49/50 lines and 585 chars over
its 20,500 threshold — one line of headroom, so the next milestone's hygiene
pass could not capture a lesson at all. RR03 diagnosed why. Consolidation, the
prescribed weight remedy, conserves content while relaxing the item axis: the
mean item length rises, and D-049 derives the threshold *from* that mean, so
re-measuring after a compression pass ratifies the accretion it was meant to
check. The weight axis can tax each hygiene pass but can never bind. Meanwhile
D-051's two criteria had no exit for the file's largest holding. M98's
re-derived classification found 18 of 32 items — 13,316 chars, 66% of item
mass — to be one subject: how to author a prose-guard, fixture, matcher, or
validator that actually falsifies what it claims. They fail **both** D-051
criteria forever by construction. Not enforcement: they teach the judgment a
guard does not make. Not ownership: no tracking-file slot holds
guard-authoring craft, because none existed.

**Decision:** A lesson family also leaves by **maturation**. The bar is
conjunctive: (a) it teaches transferable craft about authoring or verifying,
not a fact about this repo's tools or runtime; (b) it has stabilized —
extended or consolidated at least twice, later milestones adding instances
rather than changing the principle; (c) it has no existing exit under D-051.
The retiring milestone distils the family into a doctrine **module** under
`skills/shared/` — D-031's shape, conditionally read at the moment the craft
applies rather than surfaced at plan time — and the covered lessons leave
whole. D-051's existing discipline carries over unchanged: a lesson covered
only in part is trimmed to its uncovered remainder, and a graduated lesson
leaves no line behind, the retiring milestone's archive summary naming what
it graduated. Delivered by M98 as `skills/shared/guard-doctrine.md`.

**Why this is not the graduated-lessons file D-051 rejected.** That rejection
named "a second record of what LESSONS holds, the divergence vector M56
rejected" — two live records of the same lessons, drifting apart. Graduation
is the opposite operation: the content moves and the source line is deleted,
so exactly one record exists at every moment, and the count of records never
rises. The rejection stands as written; it simply does not reach this case. A
module is also not a new tracking file — it is plugin logic wired once by a
rulebook pointer (D-031), never the four-wiring-points-plus-cap path D-015 and
D-029 price when refusing one.

**Rejected:** (1) a repo-local synthesis note under `cairn/references/` —
nothing triggers its read, and the craft binds every adopting repo, not this
one; (2) re-deriving D-049's threshold from the post-consolidation mean — it
would ratify the treadmill (RR03 rec 12); a fresh measurement becomes
legitimate only once a graduation has made the mean *fall*; (3) graduating the
records-hygiene family in the same move — M98 found it a real second family of
8 items, but it fires at a hygiene or plan gate rather than at guard-authoring,
so it needs its own read-trigger; banked as a candidate row.

**Consequences:** Annotates D-051 — its two criteria, its trim rule, its
no-breadcrumb rule, and its review-time scoping all stand; maturation is a
third and rarer outflow that moves content rather than removing it. Restores
D-015's charter: `LESSONS.md` returns to build quirks and gotchas. The
graduation removed 15 lessons whole and trimmed 3 to uncovered remainders,
taking the file from 49 lines / 21,085 chars to 35 / 8,605 as merged, before
this milestone's own hygiene capture appends to it. Headroom on both axes.
Serves GP1 by
bounding an always-read surface with an outflow rather than a ceiling, and
GP4 by putting craft in the shared artifact where every adopting repo
inherits it. Locked by `skills/tests/test_lesson_graduation.py`
(mutation-registered). If a graduated family is ever found to need surfacing
at plan time after all — the moment a module's conditional read does not
reach — this is the entry to supersede.

### D-056 (2026-07-20): `tracking-rules.md` is current knowledge; rationale is placed by a three-step test — annotates D-045, extends D-052's precedent

**Context:** RR02 diagnosed the rulebook's growth as restated rationale and
prescribed "state the rule, cite the D-entry, delete the defense". M95's first
implement run built a 21-block ledger (B1–B21) to execute exactly that, and
stopped: **9 of 21 blocks had no D-entry home at all** and 14 were guard-pinned,
so for much of the targeted text the rulebook is the sole home and there was
nothing to delete back to. The binding constraint was M95's own AC1 — "every
block removed is evidenced as **already recorded** in a named D-entry" — and the
ledger recorded its cost in entry B15: AC1 "forbids the milestone's cleanest
win". RB03 escalated the impasse to a Fable audit. RR03 found AC1 had conflated
*preserved somewhere* with *recorded as a decision*, and that what was missing
underneath was a file classification nobody had ever made.

**Decision:** Three parts, one boundary.

**(1) `skills/shared/tracking-rules.md` is current knowledge under D-045.**
D-045 enumerated history (`DECISIONS.md`, work-logs, milestone IDs, entombed
`legacy/`) and current knowledge (`LESSONS.md`, `references/`, `DESIGN.md`, and
per D-052 `ROADMAP.md`) — but both lists cover *tracking files*, and the rulebook
is plugin logic. It meets every term of the current-knowledge definition and none
of history's: edited in place at every milestone that touches it, read to act on,
guarded by tests rather than by IP4, with git holding every prior state. So
deleting justification from it is **not an IP4 history edit**, by exactly
D-052(2)'s reasoning for the hygiene stamp — "`git log` holds every earlier stamp
verbatim". A defense that recorded no choice was never history. D-052 classified
a file governed by the rules; this classifies the file that states them.

**(2) Rationale is four classes, placed by a three-step test** — applied at
authoring time and editing time alike:

1. **Inversion test.** If this text were deleted or inverted, would a compliant
   agent's behavior change — misapply a rule, miss a failure mode, make a
   judgment the text forecloses? **Yes → the rulebook owns it** (class 1 *rules*
   and class 2 *application doctrine*, text that changes how a compliant agent
   *applies* a rule). A D-entry may also exist; the rulebook text is not a
   restatement of it and is never "slimmed back" to it.
2. **Decision test.** Does it record a choice among alternatives made at a point
   in time — rejected options, decision-time measurements, the forcing incident?
   **Yes → the D-entry or milestone-local decision owns it** (class 3); the
   rulebook keeps the rule plus a cite. If no record exists and the choice is
   cross-cutting, *that* is the defect — author the entry when the choice is next
   touched, never as a backfill sweep.
3. **Neither → free-floating justification** (class 4). **Default delete**, or
   compress to a clause. Justification serving a future *editor* belongs in the
   D-entry where one exists; justification serving the acting *agent* is class 2
   by definition and stays.

**(3) Guard-pinning is a deletion screen, never keep-verbatim.** The behavioral
inversion test is the doctrine; guard-reddening is its mechanical proof procedure
where a guard exists (M74's relabel/negate/transpose), and a recorded by-hand
inversion where none does. The asymmetry: reddening is **sufficient** to block a
careless deletion, **never necessary** to justify one, and **never sufficient**
to keep prose that fails the behavioral test. The text owns the guard, not the
reverse — harness anchors are chosen as exemplar blocks per file, partly for
matchability rather than because each anchored sentence is doctrine, so a guard
can pin scaffolding. Reading pinned as frozen is how a rulebook's editability
dies one guard at a time.

Rejected: **"author the missing D-entries, then slim"**, the remedy M95's own
work log proposed — it converts editable mass into permanent history at ~1,900
chars per entry to license ~3-line deletions, and misclassifies operative
application doctrine (the ledger's B17) as displaced rationale (RR03 rec 9).
Rejected: **any change to IP4** — RR03 looked for the case against it and found
none; the supersession chains are what made RR01, RR02, M95's ledger, and RR03
itself possible. IP4's wording is untouched, and the clarification runs the other
way: the rulebook is not in IP4's set.

**Consequences:** Annotates D-045 by naming a class its two lists omitted —
plugin logic — the same omission D-052(2) fixed for `ROADMAP.md`. M95's AC1 is
replaced by this test. The test predicts no yield, and the one pass run under it
undershot its own projection: M95 removed 25 lines gross — net −9 against the 16
this entry's doctrine obliged it to add — where its ledger had projected ~35-40
under the old bar. Read that as evidence the rulebook's mass is mostly class 1/2,
not as a quota a later pass owes. GP1 as amended by D-053 names
"recorded editorial passes" as the rulebook's bounding mechanism; this entry is
the criterion such a pass applies, and M96 stamps them. Delivered by M95, which
needs it as its license. If an editorial pass ever finds this test admitting a
deletion that loses a rule, this is the entry to supersede.

### D-057 (2026-07-20): The stock-side weight-governance program is closed; rulebook growth is governed at the door and triggered by measured cost — annotates D-053, retires the felt-slowness trigger

**Context:** Ten milestones and four Fable reviews have targeted the size of
`skills/shared/tracking-rules.md`. The program did not work and was
self-defeating: the four *anti-growth* milestones (M92, M93, M97, M98) added
+53 lines between them, and M95 — the editorial pass itself — removed 25 while
adding 16, net −9 against RR03's projected 60-100. RR04 Q9 rated the null
option ("stop governing size entirely") **~80% right**, and `cairn_cost`, the
instrument M94 built precisely to settle this, confirms it: across 117 sessions
and 24,322 turns, **the two most expensive sessions in the repo's history are
the M95 governance sessions**. Implement/review/plan turns average ~139k
cache-read; the rulebook is ~13k tokens of that, but the *recoverable* mass —
the 65 line-equivalents in `cairn/references/rulebook-classification-ledger.md`
— is ~1.1k tokens, **under 1% of context**. The dominant cost variable is
session length and turn count, which governance milestones maximize.

**Decision:** The stock-side program is **closed**. No milestone targets the
rulebook's size absent a **measured `cairn_cost` regression** as its trigger;
felt slowness is retired as a trigger in favour of the instrument built to
replace it (RR04 rec 11, RR02 rec 4). **M96 folds to a reporting line** in
`/milestone`'s audit — mass plus growth since stamp — with no pass machinery
built. Governance moves to the flow: growth is made visible at the door and
cheap to control there, not harvested periodically.

Rejected: **re-cutting M96 as a delta-scoped audit** (RR04's own preferred Q7
outcome, a ratchet on unreviewed delta whose remedy never exhausts) — sound in
design, but it costs another milestone for a mechanism the cost data does not
justify. Rejected: **capturing the one-time ~50-60 line yield first** — bounded
and specified, but it buys under 1% of context at the price of another long
session, which is the exact trade this entry exists to stop. Rejected:
**keeping the program open**.

**Consequences:** `cairn/references/rulebook-classification-ledger.md` becomes
a record of what *could* be cut, not a work order; a future pass triggered by
measured regression may use it, re-locating by content since its line numbers
are stale. D-053's GP1 ("every always-read surface keeps a bounded read cost")
is annotated, not contradicted — this entry names the mechanism as flow-side
and data-triggered rather than periodic and felt. D-056's yield clause remains
false on the record; superseding it is no longer urgent because no pass depends
on it, and it is parked as a candidate rather than silently dropped. The
anti-softening mechanisms of RR04 Q8 are unaffected and proceed independently —
they govern review enforcement, not size. If `cairn_cost` ever shows a
regression attributable to read volume, this is the entry to supersede.

### D-058 (2026-07-20): The whole-file density thresholds are removed — supersedes D-049's threshold clause; the item caps and D-052's per-line axis stand

**Context:** M101's decommissioning brief: remove machinery measured not to
work, on those grounds and never on "the file is too big" (D-057). The
whole-file character axis had two lives. Under M84-D1's assumed means it
fired at ordinary density for three consecutive hygiene passes (M84–M86),
taxing records the milestone never touched — D-049's own charge sheet. Under
D-049's re-derivation a threshold is the mass its own line cap permits at
measured item length, which by construction leaves it slack proportional to
the file's unused item slots: D-049 itself records that the two axes divide
labour and "neither backstops the other's saturation". An axis that fires
wrongly when set low and sits behind the item cap when set right taxes
hygiene passes (each one re-measures a mean the previous remedy moved) and
never catches what its sibling axes cannot: prose in *non-item* lines is
D-052's per-line cap's job, and item-count growth is the item caps' job.

**Counter-evidence weighed:** the axis fired correctly once — on the M100/
M101 NEXT UP candidate row, an item line grown to ~2,900 chars, where it
forced the compression that shipped the row. That fire is real and is the
one case the surviving axes structurally cannot flag (the per-line axis
never measures item lines, deliberately — D-052). It was judged not worth
the axis: one useful fire across the 17 milestones since M84, against a
standing per-pass measurement tax and two derivation rewrites, and the
monster-row case has a human at exactly the right surface — candidate rows
are read at every plan-time harvest and hygiene pass, which is where that
row's compression was actually decided.

**Decision:** `CHAR_CAPS`, the whole-file loop in `check_record_density`,
and `char_count` are removed; the per-line axis iterates its own
`DENSITY_FILES` roster; `cairn_budget` prints item + per-line axes only;
the rulebook's two-axes block and LESSONS.md's header teach the surviving
axes. Superseded in D-049: the threshold-derivation clause, its two
constants, and the measure-the-mean application rule, which retires with
the thresholds it governed. Standing from D-049: the WARN-not-FAIL
severity split, the measure-don't-assume diagnosis as method, and its
retirement of M84's prune anchor. D-052 (per-line axis, item-line
exemption) and the item caps are untouched.

**Consequences:** `record density` now reports exactly one thing — an
over-cap non-item line — and its remedy line ("replace it, don't append to
it") is the whole advisory. A file's whole-body prose bloat inside item
lines is governed by judgment at the surfaces that read those items, not by
a gate. If a real defect ever slips through that the removed axis would
have caught — an item file bloating at stable line count with no human
catching it at harvest — this is the entry to supersede, and D-049's
derivation is the recipe to rebuild from.

### D-059 (2026-07-20): The `decision heading quality` advisory is retired — annotates D-054 (mitigation 1 withdrawn); the back-reference step carries recall

**Context:** D-054 bounded the DECISIONS read and named three mitigations;
mitigation 1 was a prospective heading-quality advisory, built at M97. Its
own review measured the claim matcher defective (M97 F1–F4/F6, all scored
sub-80 and logged): a four-stem regex with a single-line window that misses
the noun form ("this supersession of D-031" — the file's own idiom, used in
D-054's body), claims split across a wrap (this repo hard-wraps), reversed
order, and synonyms ("replaces", "overrides", "retires"); it excludes
neither fences nor quotes, so an example can read as a claim — the false-
positive direction D-023 calls worse. The findings interact: the noun-form
miss was safe to close only while the wrap limit suppressed the false
positive it would otherwise raise, so independent patches leave the
advisory's green contingent on where a paragraph wraps.

**Decision:** Retire rather than repair, chosen at the M101 plan gate (the
classifier-redesign candidate row graduates with this entry). The check,
its ADVISORIES registration, and `test_decision_heading_quality.py` are
removed; git holds them. The heading-authoring rule stands as conduct, its
enforcement sentence rewritten to say so. Recall never rested on the
matcher: D-054's mitigation 2 — every match back-referenced by its own id —
covers a heading that omits a relationship, legacy and prospective alike,
and mitigation 3 (the scan is a model read) is untouched.

**Consequences:** Annotates D-054 — its recall trade now leans on
mitigations 2 and 3 alone, which is where D-054 already placed the load for
the three legacy headings. A heading that hides a relationship costs one
extra targeted read, never a silent miss, provided the back-reference step
is actually run — that step is rulebook conduct pinned by
`test_bounded_decisions_read.py`. Re-open trigger unchanged from the
graduated candidate row: a real supersession missed in practice, or another
repo relying on heading-scan recall — a repaired classifier must be
sentence-scoped, fence/quote-aware, claim-vs-description discriminating,
and verified against a fixture set varying phrasing, wrap, and voice
independently (M57/M81).

### D-060 (2026-07-23): The always-read audit frame — every always-read file names its three governance elements, checked at the /milestone audit — annotates D-045, cites D-053/D-056/D-057

**Context:** RR03 (Q5/rec 7) derived a shared frame across cairn's always-read
files: each names an **inflow test** (what belongs here), an **outflow or
read-bound** (how content leaves, or how the read stays bounded), and an
**attention signal** (what reports growth), with D-045's history/
current-knowledge split deciding which outflows are legal. RR03 §5 showed the
rulebook's own ~30-milestone weight saga (M84–M98) was the cost of having none
of the three — invisible because nothing checked completeness. Rec 7
("consider") banked the frame as a candidate, promotable once the rulebook had
all three elements so the frame is derived from a worked case, not projected.
That condition is now met: M95 gave the rulebook an editorial outflow, D-057 its
attention-signal reporting line plus door-side inflow governance, M97 bounded the
DECISIONS read, M98 gave LESSONS a maturation outflow.

**Decision:** Add the frame as one doctrine paragraph in
`skills/shared/tracking-rules.md` — universal cross-cutting conduct, not a
conditionally-read module, since every repo has always-read files (M78's home
test) — enumerating GP1's four always-read files (ROADMAP.md, LESSONS.md,
tracking-rules.md, DECISIONS.md) with their three elements as the worked case,
and stating that a file missing an element is the gap the frame surfaces.
`/milestone`'s §2 audit gets one judgment bullet applying it, in the form of the
existing staleness / references-staleness advisories: it flags any always-read
file missing an element, or any newly-added always-read surface not covered, and
never `FAIL`s or auto-fixes. Prose-only, prose-guarded, mutation-registered
(RR03 rec 7 "no new mechanism"; rec 10 rejects a shared machine). The frame is
**completeness-only** — it reports whether each file *has* the three elements,
never measures or gates mass — so D-057's closed stock-side size program stays
closed. User-approved at the M108 plan gate (2026-07-23): rulebook + audit-bullet
home, prose-only, GP1's four files, completeness-only.

**Consequences:** Annotates D-045 — its two file-classes now carry a
completeness demand (three elements per always-read file), not only a
correction rule. Cites D-053 (the frame is where GP1's per-file-class mechanisms
sit), D-056 (the rulebook's inflow test is its three-step placement), and D-057
(the rulebook's attention signal is the audit's mass+growth line, and the size
boundary this entry stays inside). No IP touched; GP1/GP2 worked under, wording
unchanged. Graduates the "Always-read audit frame" candidate row (executed at
M108 review post-merge hygiene — M35). If a future always-read surface ever needs
the frame enforced mechanically rather than by audit judgment, that is a new
candidate superseding rec 7's "no mechanism", and this is the entry to supersede.

### D-061 (2026-07-23): The records-hygiene lesson family graduates into a second module; M69/M77 graduate rather than ownership-retire — annotates D-055

**Context:** D-055 established maturation as a third LESSONS.md outflow and
delivered `skills/shared/guard-doctrine.md` as the first module, banking
(its Rejected §3) the records-hygiene family — 8 items that fire at a hygiene
or plan gate rather than at guard-authoring — as a candidate needing its own
read-trigger (ROADMAP M98-D1). LESSONS.md reached 49/50 lines again at the
M110 plan, the trigger the candidate named. This is maturation's second
application, exercising D-055's mechanism rather than changing it.

**Decision:** Distil the family (M35, M51, M69, M73, M77, M78×2, M87) into
`skills/shared/records-hygiene.md`, a conditionally-read module (D-031 shape)
pointed at from the LESSONS retirement rule, read-trigger "a milestone hygiene
or plan gate." All eight graduate **whole** — zero trims: each line is
single-subject, and the nearest overlap (M78's own-artifacts rule vs
`guard-doctrine.md` §7's grep-criterion instance) is general-rule vs
specific-instance across two different read-triggers, so both coexist with no
LESSONS.md duplication. **M69 and M77 graduate into the module rather than
retire by D-051 ownership:** D-051's ownership criterion is defined against a
*tracking-file* slot, and `/milestone-implement` step 6 and `/milestone-plan`'s
collision sweep are skill prose, not tracking files; ownership-retiring would
require writing the lesson content into guarded skill prose (M104 reddening
risk) for no gain over graduation. Rejected: ownership-retiring M69/M77
(above); a lighter, non-mutation-registered guard (this repo's guard doctrine
wants mutation coverage).

**Consequences:** Annotates D-055 — its maturation mechanism, conjunctive bar,
trim rule, and no-breadcrumb rule all stand; this is the second family to use
it, confirming the mechanism generalizes past guard-authoring craft. LESSONS.md
falls 49→41 lines. Serves GP1 (bounding an always-read surface by outflow) and
GP4 (craft in the shared artifact every adopting repo inherits). Graduates the
M98-D1 candidate at M110 completion (M35). Locked by
`test_records_hygiene_graduation.py` (mutation-registered). If the module's
conditional read is ever found not to reach a session needing the craft at a
gate, this is the entry to supersede.
