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

### D-062 (2026-07-24): Fable no longer pay-on-demand — gate retained on token-cost grounds (supersedes D-004's premise)

**Context:** A policy change removed Fable's pay-per-use billing, so D-004's
Context ("token-billed pay-per-use") and Consequences ("never a silent cost")
no longer hold. Fable still typically uses more tokens than Opus, so it is not
free to reach for, but it is no longer a per-call charge.
**Decision:** Keep D-004's core — Fable is reached only through the RB/RR brief
protocol behind an explicit per-instance approval gate. Drop the billing-hazard
framing (no "token-billed", "no standing authorization", "silent cost") in
favour of neutral token-cost wording. Lower the bar for *recommending*
escalation: it may be offered on an RB-tripwire hit OR for a genuinely hard
question the session cannot confidently settle, with the three tripwire
categories remaining the canonical must-offer cases.
**Consequences:** Escalations stay reproducible, auditable, and ingestible via
the gate; the gate now guards token cost, not billing. D-004 stands as history
(unedited, IP4); this entry supersedes only its cost premise and the
recommend-bar strictness.

### D-063 (2026-07-25): The active milestone file is a fifth always-read surface; its cap-exempt sections are read-bounded newest-first at injection — annotates D-060, applies D-054's shape

**Context:** A `/milestone` audit in the circumplex repo (2026-07-25) applied
D-060's §2 check and found the gap the frame exists to surface. The
`session_context` SessionStart hook injects a fifth always-read surface — every
active milestone file, whole — that the frame's worked table does not cover.
Measured there: a 30,256-byte injection, 65% of it one milestone's work log,
silently chopped by `MAX_CHARS` at the *old* end, so the entries recording what
that milestone was blocked on were exactly what got dropped. Against the frame
the surface has an inflow test (the milestone-file section ownership table) and
neither of the other two: the 150-line cap explicitly exempts `## Work log`
(D-046) and `## Review` (M55), and nothing reads less of either — the hook
reads all of both. The failure is latent in this repo too: M95's own work log
measured 23,147 chars / 65 entries, within a few KB of the cap once the ROADMAP
is added. IP4/D-045/D-046 forbid the storage-side remedy, so the only legal
direction is read-bounding.

**Decision:** Four choices at the M113 plan gate (2026-07-25). (1) **Both
surfaces, one milestone** — the hook gains the read-bound, then the frame's
table gains the row that names it; a row naming a bound nothing applies would
be false on the record. (2) **Newest-first, by measured size budget.** The
injection takes a cap-exempt section's newest content up to a per-section
character budget set above the measured p90 of both types (work log 3,740,
review 5,866, over 111 milestone files), with a floor of the newest 3 entries;
a size budget rather than a fixed entry count because entry length varies by an
order of magnitude, and newest-first because a resume needs current state, which
is what today's tail chop discards first. Every elision carries a marker naming
what was cut and the path to read for the rest — the M100 "fail loud, never
open" rule applied to injection. (3) **Every cap-exempt section, not the work
log alone.** The rule is derived from the cap rather than enumerated: sections
the 150-line cap exempts are read-bounded, sections it governs are injected
whole. Rejected bounding the work log alone (leaves the identical gap on
`## Review` for a milestone at `review` status) and bounding capped sections too
(already governed; the cap is their bound). (4) **No separate size signal.**
The elision markers are the read-bound's own honesty requirement; no measurement
of injection mass is added. Rejected a `cairn_validate` injection-size advisory:
it measures mass, which D-057 closed and D-060 put outside the frame
("completeness-only"), and D-054's row already sets the precedent that a
read-bounded history surface needs no attention signal.

**Consequences:** Annotates D-060 — the frame's worked table goes from four
rows to five, which is D-060's own audit bullet ("any newly-added always-read
surface not covered") executing as designed, not a supersession; the frame stays
completeness-only. Applies D-054's shape (history bounded by reading less, never
shrunk) to a second surface. IP4, D-045, and D-046 are untouched in wording and
in reading: nothing a milestone file *stores* changes, and the cap-exempt
sections stay exempt for their original reasons. Serves GP1, and the surface is
the first to split across two of GP1's three mechanisms within one file — its
capped sections bounded by a cap with an outflow, its cap-exempt sections by
reading less — so D-053's "fits none of the three named mechanisms" supersession
trigger is not reached. D-057's closed stock-side program stays closed: this is
flow-side, the direction that entry endorsed ("growth is made visible at the
door"). Delivered by M113. If a bounded injection is ever observed leaving a
resuming session less oriented than the whole file did, this is the entry to
supersede.

### D-064 (2026-07-26): Thrash is counted per milestone and fires on a repeated failure SHAPE — supersedes the third-trip rule's per-cut reading; adds falsifying promotion conditions and detector-rendering guard doctrine

**Context:** A `/milestone` audit (2026-07-26) post-mortemed intraclass M93 —
eight review passes and three plan re-cuts on one milestone — and found the same
signature one milestone earlier, in intraclass M92 (seven passes, "1-6 each
failed AC5 on prose authored about the work, never on the code"). Three
mechanisms, each cairn's. First, the thrash rule fired once, at the third
return, and then went silent for four more: a `/milestone-plan` re-cut unticks
every criterion and supersedes the tasks, so the next pass reads as the re-cut's
first, and intraclass M93's own work log records the disposition drifting to
"thrash-rule disposition left to the maintainer". Second, counting trips is the
wrong measure — intraclass M93's passes 2-5 failed the SAME criterion four
times, each by a new mechanism of one shape ("the hint names a method that then
fails"), which is a wrong-design signature a trip count cannot distinguish from
three unrelated defects. Third, the approach that finally worked was recorded as
a candidate whose promotion condition read "Promote if a fifth mechanism
appears"; it was met exactly as written, at pass 5, after the same approach had
been measured feasible and prototyped correct at the pass-4 gate and declined
for a smaller diff. Passes 6-8 then failed on evidence quality with shipped code
byte-identical and clean across ~33,000 adversarial cells — including a leak
detector that matched about four significant figures and passed a real violation
rendered `round(v, 3)`.

**Decision:** Six choices at the M114 plan gate (2026-07-26). (1) **Count
returns per milestone, never per cut** — a re-cut increments and never resets,
stated in so many words because the per-cut reading is what the old wording
permitted and what actually happened. (2) **A second trigger on the same
criterion failing twice by a new mechanism of the same shape**, remedied by
reconsidering the alternative the plan gate recorded against rather than
re-cutting around the same predicate, which buys the next mechanism and not a
fix. (3) **Where the gate recorded no alternative, offer escalation via
`/milestone-brief`** — an approach wrong this often is the hard question the
brief protocol exists for; gated per instance, never automatic (D-004). (4)
**The rule stays in `/milestone-review`**, its single surface, rather than being
lifted into the always-read rulebook, which is +83 lines over its M95 baseline
with D-057 governing growth at the door. (5) **A promotion condition names the
class of evidence that would falsify the chosen approach, never a count of
failures** — placed in `tracking-rules.md` beside search-first rather than in
the records-hygiene module, because candidate rows are created conversationally
and a conditionally-read module would never fire on that path. (6) **No
`cairn_validate` check for any of the three.** Rejected: the counting half is
mechanical but inert, and the shape-recurrence half is a judgment — the same
call D-059 made when it retired an advisory measured not to work.

**Consequences:** The thrash rule gains its first guard; it was unguarded prose
until now, with every phrase of it (`third trip`, `queue another retry`,
`mis-planned`, `re-plan or split`) occurring in the skill and in no test, so
deleting it outright kept the suite green. That guard also pins the rule to one
surface, so a later restatement in another skill or the README reds rather than
silently forking it. `guard-doctrine.md` gains two rules from the same
post-mortem: §3 that a detector's matcher must be exercised at every rendering
its target can take, carrying the renderings in as positive controls, since
external mutation-verification proves only that a guard catches the mutation its
author thought of; and §7 that a sweep permitting silent cells passes for free
on silence unless each cell asserts a positive check count and the converse is
asserted beside the claim. Delivered by M114. No prior D-entry is superseded —
the thrash rule never had one, which is part of what this entry fixes. If a
milestone is ever sent back by trigger (b) where the recorded alternative was
the wrong call, this is the entry to supersede.

### D-065 (2026-07-26): The one-surface pin was re-cut out of M114 — supersedes D-064's Consequences claim that a guard pins the thrash rule to one surface

**Context:** D-064 was appended when M114 shipped a guard asserting the thrash
rule's phrase occurred in exactly one file, so a restatement elsewhere would red
rather than silently fork it. Its Consequences say so: "That guard also pins the
rule to one surface, so a later restatement in another skill or the README reds
rather than silently forking it." That guard no longer exists. It was re-cut out
at M114's third return, after consuming all three returns across six findings of
one shape — the detector, or the controls exercising it, did not cover a
rendering the phrase can take (a line wrap, a blockquote continuation marker,
nested blockquotes in two spellings, partial emphasis, case, word boundaries,
and finally corpora that passed while empty). As of M114's merge no guard pins
the rule to one surface, and D-064's sentence is false about the shipped system.

**Decision:** Supersede rather than edit. D-064's appended bytes stand
unaltered; this entry carries the correction. The route was chosen at RR06's
instruction (BC1) after review pass 5 found the entry had been corrected in
place — an IP4 violation that M114's own pass 4 had already refused when it met
the identical situation in a work log and superseded instead. Two things settled
with it. **IP4 attaches at append time, not at merge time:** an entry's
not-yet-merged status is no carve-out, because the rule is about the record's
form, not its distribution, and a carve-out would make every unmerged history
file editable by whoever is holding it. And **the pin itself is not abandoned**
— it is a ROADMAP candidate, promotable on a rendering-independent detection
approach (a markdown or AST parse, a content hash over normalized doctrine
blocks) and explicitly never on a further count of attempts at a wider matcher.

**Consequences:** D-064's other content is untouched and still governs: its six
plan-gate choices, the per-milestone counting rule, and the promotion-condition
and guard-doctrine additions. Readers of D-064 reach this entry by the
back-reference discipline (D-054) — its heading names D-064 as superseded.
Delivered by M114. If a rendering-independent fork detector is ever built, the
candidate row is where it starts, and this entry is the record of why the first
three attempts were abandoned rather than iterated.

### D-066 (2026-07-26): A frozen scope is derived, an out-of-scope defect is admitted on three legs, and an oversized RR criteria set is carried by reference — annotates D-030/D-046 (the milestone cap) and D-004/D-062 (escalation gating)

**Context:** RR06 froze M114's sixth review pass by enumerating the files it
could touch, and authored that enumeration as free prose. It confined
`cairn/ROADMAP.md` changes to "status mirroring" while its own BC8 mandated
three candidate rows in that same file — jointly unsatisfiable, discovered at
the review gate rather than at ingest. The same set left two confirmed 90+
defects outside the scope with no rule saying whether to fix or bank them.
RR07 answered all three, and its own criteria set then hit a fourth collision
at ingestion: at ~99 lines it does not fit the 150-line plan-owned cap beside
an append-only `## Decisions` section that three RR ingestions had grown to 43
lines. D-030 and D-046 both declined to exempt that section, on the stated
premise that it "is meant to stay brief, with cross-cutting entries promoted
here" — a premise a three-RR milestone falsifies.

**Decision:** Four choices, the first three RR07's and the fourth this gate's.
(1) **A frozen scope's file list is derived, never authored** — it is the union
of the write obligations of the other criteria in the same set, plus explicitly
named mirroring, and it is re-derived whenever the set changes. RR07's own BC1
shows its derivation inline so the ingesting session can check it rather than
trust it. (2) **A defect outside a frozen scope is fixed inside the pass
exactly when three legs hold**: its subject is the milestone's own deliverable
and it is at or above the confidence threshold; the gate that owns the scope
can specify the fix in closed form, so admitting it adds no authorship; and the
fix is verifiable by replayed probes and measured counts. Fail any leg and it
is banked with an IP3 disposition. The scope's enumeration is an instrument
derived from the fix set; the fix set is never trimmed to preserve the
enumeration. (3) **No numeric cap on escalations per milestone** — a count
pre-commits to paying for every escalation below it and then fires exactly at
the cap, the shape the falsifying-promotion-condition rule forbids; the
per-instance human gate (D-004, D-062) is the working bound, and a
disposition-shaped terminus is how a bound is written here. (4) **Where an RR's
binding-criteria set cannot fit the milestone cap, criteria are carried by
reference to the archived RR through the shown Deviations table** — never
softened, never silently trimmed. The RR is append-only history, so exactly one
permanent copy of the text exists and the implementer transcribes from it; the
departure is tabled and shown at the ingest gate (IP3). Criteria the review
gate reads directly — numeric projections, a terminus — stay verbatim.
Rejected: exempting the milestone-local `## Decisions` section from the cap
(D-030 and D-046 both declined it, and this entry does not reopen that);
splitting M114 (RR07 Q4); and letting `weight caps` FAIL as an accepted
divergence, which would block every later review of the file.

**Consequences:** Annotates D-030 and D-046 — the cap's scoping is unchanged
and no new exemption is created; what changes is what may be *restated* inside
the budget. Annotates D-004/D-062 — escalation stays gated per instance with no
count added. The derived-scope rule and the three-leg test bind any future RR
that freezes a scope, and RR07 is the worked example of both. Delivered by
M114. The residual is real and recorded as a ROADMAP candidate: at 149/149 the
file has zero headroom, and the `## Decisions` section is append-only and grows
once per RR ingestion, so a milestone driven by several RRs will hit this again
— the entry to supersede is whichever of D-030/D-046 the fix lands against.

### D-067 (2026-07-26): Two fresh-context reader instruments adopted — the criteria audit at plan/ingest gates and description-layer certification before review; author self-certification of guard coverage is retired (D-059's shape) — annotates D-031, stays clear of D-057's door

**Context:** M114 returned from review seven times. Its seventh return came
with every suite green, every numeric projection met exactly and the validator
clean, and was still two records describing that milestone's own artifact
wrongly; earlier returns had cost it criteria that were unsatisfiable as
written or that mandated an IP4 violation, and coverage claimed but not
pinned. The single diagnosed root cause is that an author
verifies a description against its generative model of the artifact rather
than against the artifact, which is why running the suites, the harness, and
the sweeps self-corrects while certifying coverage does not. Two instruments
were prescribed and deliberately banked outside M114 as their own milestone;
that milestone is M115, and adopting them is M114's recorded unblock
condition.

**Decision:** Adopt both, as readers and never as checks. (1) A
**criteria audit** at `/milestone-plan`'s step-3 gate and at
`/milestone-brief`'s RR ingestion: a fresh-context `[O]` reader that authored
none of the criteria asks two mechanical questions of each — what state of the
world satisfies this exactly as written, and does any IP or D-entry make that
state unreachable — asked of a binding-criteria *set* as well as of each
member, since criteria individually satisfiable can be jointly unsatisfiable.
Findings with one clear answer are fixed and reported; judgment calls become
gate questions under the three-marker cap. Because the audit must read the
bytes that ship, criteria authoring moves from step 4 up into step 2 and step
4 writes the audited wording. (2) **Description-layer certification** as
`guard-doctrine.md` §8, fired by `/milestone-implement` step 8 before
`status -> review` when a milestone authored or edited a prose-guard: a
fresh-context `[O]` reader checks AC-clause-to-assert coverage, claim-vs-file
accuracy, and anchor-vs-shipped-bytes fidelity, and the gate is entered only
at zero unresolved. **Author self-certification of guard coverage is thereby
retired, not repaired** — D-059's move, applied to a mechanism measured across
seven consecutive passes. Operation stays with the author; only certification
moves. Rejected: a mandatory re-derivation step (it instructs the same
judgment that failed while citing the same instructions); any rubric or
threshold change; and any `cairn_validate` mechanization of either instrument
— satisfiability and claim accuracy are judgments about prose meaning, the
shape D-059 retired rather than rebuilt.

**Consequences:** Annotates D-031 — §8 is new doctrine landing in a module
rather than in the rulebook, and `tracking-rules.md` is untouched, so D-057's
door stays shut and the three question gates are unchanged in number. §8 is
conditionally read at guard-authoring time, so a milestone writing no guard
pays nothing; the criteria audit costs one reader per plan. §8 carries its own
stated falsifier — if guard-authoring milestones still average multiple
description-layer returns after adoption, retire the step rather than tune it
— which is this entry's own exit condition too. **D-064 through D-066 are
reserved, not skipped:** they are appended on M114's unmerged branch and
nothing checks D-id uniqueness, so taking D-064 here would produce a duplicate
that `cairn_validate` passes green on merge. IP4 forbids reuse, not gaps, and
`cairn_validate` has no contiguity check. The review report prescribing both
instruments — **RR06**, likewise unmerged on M114's branch and resolvable only
once M114 lands — is for that reason named here and nowhere in the shipped
prose: its rules travel verbatim instead, rather than behind a citation that
resolves to nothing.
Delivered by M115. If either reader proves to cost more than the returns it
prevents, this is the entry to supersede.

### D-068 (2026-07-26): D-064's description of guard-doctrine §7 is wrong twice over — supersedes that sentence; shipped §7 requires the across-sweep positive and leaves the converse optional

**Context:** D-064's Consequences describe the §7 rule M114 ships as firing
"unless each cell asserts a positive check count and the converse is asserted
beside the claim". Shipped §7 says something different in two places. It
requires two things where D-064 records one and a half — "Assert per cell that
it checked a positive number of things, and assert across the sweep that the
positive case fired somewhere, so universal silence cannot satisfy it" — and it
frames the converse as an optional strengthening, "Stronger still, assert the
CONVERSE beside the claim", never as a requirement. So the entry drops the
across-sweep half and promotes an optional clause to a mandatory one. Found by
M114's own review pass 7 (F5, 85), after pass 4's K1 (verified verbatim) had
found the same class of error in the same entry on a different sentence. D-064
had not reached the default branch, so without this the false description would
have landed in append-only history at merge.

**Decision:** Supersede, never edit. D-064's appended bytes stand and this entry
carries the correction, on exactly the route D-065 settled for the one-surface
sentence: IP4 attaches at append time, not at merge time, so an entry's
not-yet-merged status is no carve-out. The correct reading of shipped §7 is that
a sweep whose cells may legitimately be silent passes for free on silence, so
**assert per cell that it checked a positive number of things AND assert across
the sweep that the positive case fired somewhere**; asserting the converse
beside the claim (`named == usable` rather than `named ⇒ usable`) is a stronger
option, not a requirement. The shipped prose is unchanged and stays
authoritative — this entry corrects the record about the rule, never the rule.

**Consequences:** D-064's other content is untouched and still governs — its six
plan-gate choices, the per-milestone counting rule, and the promotion-condition
and matcher-rendering additions; D-065 continues to carry the one-surface
correction. The half D-064 dropped is the operative one: M114's pass 6 found
exactly the across-sweep clause unpinned and deleting green (F1, 92), so a
reader taking D-064's description for the rule would have missed the very clause
this milestone had already returned on. That clause and the converse are both
pinned whole now, so a future edit to either reds rather than drifting. Readers
reach this entry from D-064 by the back-reference discipline (D-054) — this
heading names it, and D-064 now carries two corrections, which is itself the
evidence for RR06's diagnosis that an author verifies a description against its
model of the artifact rather than against the artifact. Delivered by M114. If
§7 is ever restated so the converse becomes mandatory, this is the entry to
supersede.

### D-069 (2026-07-27): A certification's report is outside its own certified scope — AC9 amended at the gate (route c); annotates D-067, cites D-068

**Context.** M114 pass 8's §8 description-layer certification ran four rounds
without reaching AC9's zero-unresolved gate. Rounds 1–2 found real defects in
records about the work; all were fixed and confirmed landed. Rounds 3–4 found
defects only in newly-authored work-log narrative about the certification
rounds themselves. The work log is append-only (IP4) and §8 obliges each round
to record its verdict, so every round manufactures uncertified surface for the
next round to audit: with the report inside the certified scope, zero
unresolved is reachable by luck, never by convergence. Measured cost curve:
15, 14, 17, 38 minutes. Parked 2026-07-27 for a maintainer decision among
(a) a narrowed fifth round, (b) review with AC9 unticked, (c) a scope
amendment.

**Decision.** Route (c), maintainer's call 2026-07-27. AC9 is amended via the
gate: the certified scope is the work and the records describing the work; a
record whose subject is a certification round itself — the final round's own
report included — is outside it. Rationale: the instrument (RR06 rec 5,
adopted by D-067) targets the author's description of the artifact, never
meta-narrative about the certifying step; a report cannot sit inside its own
scope without regress.

**Consequences.** The scope rule belongs in guard-doctrine §8 for every future
guard-authoring milestone, but §8 is doctrine M114 ships and pass 8 holds
`guard-doctrine.md` byte-identical, so the §8 edit is banked as a ROADMAP
candidate row this entry backs rather than made here. §8's own falsifier
(retire, don't tune — D-059's shape) is not met: it reads on an average across
milestones at n=1, and every discrepancy all four rounds found was real — the
instrument stands; only its scope was wrong. A work-log style lesson
(decision-relevant facts only; characterizations are falsifiable surface) is
owed at review's post-merge hygiene capture.

### D-070 (2026-07-27): D-069's premise sentence narrowed and its heading's cites clause withdrawn — supersedes those two claims; the route-(c) amendment stands

**Context.** The final §8 certification round, run under AC9 as amended, found
two discrepancies in D-069 itself. Its Context states "Rounds 3–4 found
defects only in newly-authored work-log narrative about the certification
rounds themselves"; round 3's two counted discrepancies were in the T20 entry
and in a CLARIFIES entry about the gated amendment — both records describing
the work, inside the amended scope. The claim holds of round 4 alone. And its
heading says "cites D-068" where the body engages nothing from D-068.

**Decision.** Both claims are superseded — appended, never edited (IP4
attaches at append time, D-065's route). The corrected premise: rounds 1–3
found real defects in records about the work, each fixed and confirmed;
round 4's discrepancies were in certification narrative alone.

**Consequences.** The route-(c) amendment is unaffected: its ground is
structural — §8 obliges each round to record a report that is uncertified
surface for the next round, so zero-unresolved cannot converge while the
report sits inside the certified scope — and round 4 is what instantiates
that mechanism. Nothing else in D-069 is touched.

### D-071 (2026-07-27): The placement test takes the deletion arm for retention and moves inversion to guard verification, gaining a step-0 single-home check — narrowly supersedes D-056's part 2 and its yield clause; parts 1 and 3 stand (RR04 rec 9)

**Context:** D-056 stated the placement test's first step as "deleted **or**
inverted", and RR04 §6 found the disjunction defective: "Deleting a duplicate
changes nothing (the other copy still governs → route to delete), but
*inverting* a duplicate creates a contradiction, which does change behavior →
'yes → the rulebook owns it.' Any rule-shaped text passes the inversion arm,
copies included." The two probes answer different questions — inversion detects
*rules*, deletion detects *necessary* text — so a retention test for an
always-read file needs the deletion arm, and restatement is a relation between
blocks that no per-block test can see. Separately, D-056's Consequences claimed
"The test predicts no yield"; the committed ledger measured otherwise, and
D-057 recorded the claim as remaining "false on the record" while parking the
supersession as no longer urgent. This entry is that supersession, taken now
because a milestone touching the placement test is the promotion condition the
parked row named.

**Decision:** Three edits, narrow.

**(1) Step 0 — single home.** Before the retention test: is this stated
elsewhere in `tracking-rules.md`? One home keeps the statement; every other site
carries at most a cross-reference. This is not new doctrine — it is
`DESIGN.md`'s "nothing is said twice" and the file map's "substance lives in the
owner", applied intra-file and finally made a test step. It governs text
authored or edited from here on; **no retroactive compliance sweep is owed or
implied**, and reading it as one would reopen the stock-side work D-057 closed.

**(2) The probes split.** Retention in the rulebook requires
**deletion-changes-behavior**. The inversion procedure — relabel, negate, or
transpose the rule in place, run the suite, require red — is the
**guard-verification** protocol (its M74 role), and is not the placement test.

**(3) The yield clause is replaced by the measurement.** D-056 told a reader to
treat M95's net −9 as evidence about the file's composition and to expect no
yield. `cairn/references/rulebook-classification-ledger.md` measures ~65 line-
equivalents of class 3+4 — 8.4% of 779 — and states that it "confirms D-056's
headline claim" that the mass is mostly class 1/2 (90.6% of content lines) "and
contradicts only its yield clause … by ~56 lines net". The measurement replaces
the prediction. It is not a quota: D-057 still governs whether any pass is run.

**D-056's parts 1 and 3 stand unchanged** — `tracking-rules.md` is current
knowledge, and guard-pinning is a deletion screen rather than a licence to keep.
Only part 2's test and the yield clause are superseded. D-056's own bytes are
untouched under IP4, and `skills/tests/test_rule_placement.py` reds on any edit
to them.

**Consequences:** The rulebook's "What gets a test" section states the repaired
test, and the always-read governance table's inflow cell points at it instead of
restating it — step 0's first application, and one the mutation harness enforces
mechanically, since `blank_block` errors on a registered locator occurring twice
as loudly as on zero. D-057 is untouched: the stock-side program stays closed,
this repairs a test rather than harvesting the file, and the ledger remains a
record of what *could* be cut rather than a work order. D-056's supersession
trigger was directional — "if this test [admits] a deletion that loses a rule" —
anticipating over-deletion only, which RR04 read as a signature of defensive
drafting; this entry's runs both ways. If the deletion arm is found retaining
text no reader needs, **or** step 0 found suppressing a statement whose second
site was load-bearing, this is the entry to supersede. Delivered by M116.

### D-072 (2026-07-27): D-071's "reds on any edit" claim is narrowed to the five spans the guard actually pins — supersedes that clause; D-071's three edits stand

**Context.** M116's §8 description-layer certification found D-071's closing
sentence overclaims its mechanical backing. D-071 states that D-056's bytes are
untouched under IP4 "and `skills/tests/test_rule_placement.py` reds on any edit
to them". `TestDecisionRecord` pins five spans of D-056 — the heading regex, the
part-1 classification sentence, the three step labels, the no-backfill clause,
and the IP4 clause. The certifier verified by mutation that rewriting D-056's
yield clause ("The test predicts no yield" → "XXXX predicts no yield") leaves
`test_rule_placement` fully green, so "any edit" is false as written.

**Decision.** The clause is narrowed: the guard reds on an edit to D-056's
classification sentence, its three step labels, its no-backfill clause or its
IP4 clause, and not on an edit elsewhere in the entry. Everything else in D-071
stands — the step-0 check, the probe split, and the yield-clause replacement are
unaffected. So is the underlying fact: D-056's bytes **are** untouched, which
M116's AC1 verifies by `git diff` against `main`, never by the guard.

**Consequences.** Appended rather than edited: IP4 attaches at append time
(D-070, D-065's route), and D-071 was already appended when the certification
ran. What narrows is a claim about what a guard proves, never a claim about what
was done. Note the shape: this is the second consecutive milestone whose
certification round caught an overclaimed guard-coverage sentence inside its own
D-entry — D-070 was the first — which is evidence for the instrument D-067
adopted rather than against it. If a later pass widens `TestDecisionRecord` to
pin D-056 whole, this is the entry to supersede.

### D-073 (2026-07-27): D-071's "parts 1 and 3 stand unchanged" is narrowed to part 3's asymmetry, and D-072's Decision clause is corrected to the five spans its own heading names — supersedes those two claims; both entries' substance stands

**Context.** M116's fresh-context diff review found two records of this
milestone describing their own subject wrongly, one in each of the entries
M116 had already appended.

(1) D-071 states that D-056's "parts 1 and 3 stand unchanged". D-056's part 3
opens "The behavioral inversion test is the doctrine; guard-reddening is its
mechanical proof procedure where a guard exists (M74's relabel/negate/transpose),
and a recorded by-hand inversion where none does." D-071's own edit (2)
reassigns exactly that procedure to guard verification, so part 3 does **not**
stand unchanged — its framing sentence is precisely what D-071 supersedes.
D-056 is still cited from the repaired rulebook paragraph, so a reader
following the cite and told part 3 stands would read the superseded doctrine
as live.

(2) D-072's heading claims a narrowing "to the **five** spans the guard
actually pins" and its Context lists five, but its Decision enumerates four —
dropping the heading regex — while asserting the guard reds "not on an edit
elsewhere in the entry". `test_entry_exists_and_annotates_d045` pins D-056's
heading, so that clause is false as written.

**Decision.** (1) D-071's scope claim is narrowed: **D-056's part 1 and part
3's asymmetry stand** — the rulebook is current knowledge; guard-reddening is a
deletion screen, never a licence to keep; the text owns the guard. **Part 3's
first sentence, naming the behavioral inversion test as the doctrine and
guard-reddening as its proof procedure, is superseded by D-071(2).**
(2) D-072's narrowed clause is restated whole: the guard reds on an edit to
D-056's **heading, its part-1 classification sentence, its three step labels,
its no-backfill clause, or its IP4 clause** — the five spans its Context and
heading both name — and not elsewhere in the entry.

Nothing else in either entry changes. D-071's three edits and D-072's
correction of the "reds on any edit" overclaim both stand.

**Consequences.** Appended, never edited: IP4 attaches at append time (D-070,
D-065's route). This is the third appended correction in one milestone —
D-071 overclaimed, D-072 miscounted while fixing it, D-073 fixes both — and
the pattern is the finding, not the individual slips: each entry made a precise
claim about a mechanism it had not re-read at the moment of writing. The
instrument that caught all three was a fresh-context reader (D-067's §8
certification for the first, the review fan-out for these two), never a test;
`cairn_validate` and all three suites were green at every step. If a later
milestone finds this correction chain repeating, the entry to write is one
governing how D-entries make mechanical claims, not a fourth correction.

### D-074 (2026-07-27): The milestone-local `## Decisions` section is history and joins the cap-exempt set — supersedes D-046's choice (3) and the D-030 rejection clause it rests on; annotates D-045 (the classification) and D-063 (the read-bound)

**Context:** D-030 declined to exempt the milestone-local `## Decisions`
section from the 150-line plan-owned cap, on the stated premise that it "is
meant to stay brief, with cross-cutting entries promoted here". D-046
reaffirmed that as its choice (3), distinguishing the work log on the ground
that the promotion valve "is real and absent from the work log". D-066 hit the
collision at RR07's ingestion — M114 at 149/149 with a 43-line Decisions
section — deliberately did not reopen it, and recorded the residual as a
candidate naming D-030/D-046 as the entry to supersede. Measured at the M118
plan gate over all 116 milestone files this repo has had: the section runs a
median of 4 lines and the brevity premise holds for 79 of them — but every one
of the 7 files that ever reached ≥145 plan-owned lines carries 24–43, and only
M114 of those 7 was RR-driven. So the phenomenon is not RR ingestion, and the
valve does not reach the content that grows: M114's 13 entries are dated
dispositions of its own review rounds, milestone-local by construction, with
nothing cross-cutting to promote.

**Decision:** Three parts. (1) **The section is history under D-045** — the
ownership table already makes it append-only, and its entries record what was
decided at a time. The alternative classification is self-defeating: current
knowledge is corrected in place, hence trimmable, and a trimmable section has
no claim to an exemption grounded in un-editability. (2) **It joins the
cap-exempt set**, for D-046's reason and not D-030's — the cap must never leave
a file fixable only by an edit IP4 forbids. The set becomes three members
carrying three distinct reasons, and every site that enumerates it says so
rather than naming a pair. (3) **A `decisions format` advisory** WARNs,
exit-code neutral, on an entry that is not one line: D-046 rejected shipping
its exemption bare because nothing would then notice bloat in a section that
had stopped costing budget, and that reasoning binds here unchanged. Rejected:
raising the 150 cap (it governs plan discipline, which is not what overran);
exempting an RR-bound AC block (would have relieved 1 of the 7 measured files);
and a separate Decisions sub-cap, which reprises the second-number complexity
D-030 and D-046 each declined.

**Consequences:** Supersedes D-046's choice (3) and the D-030 rejection clause
it rests on; every other part of both entries stands — D-030's plan-owned-body
scoping and `## Review` exemption, D-046's work-log exemption and its advisory
severity. Annotates D-045 by classifying one further section, and D-063, whose
newest-first read-bound is scoped to cap-exempt sections and therefore now
reaches a third. IP4 is untouched in wording and in reading; what changes is
the set of sections the cap may aim at. Frees the ≥21 lines the milestone
template reserved for the section — redistributing them into the per-section
drafting budgets is deliberately out of scope here and recorded as a candidate,
because that block has drifted twice before and is a measurement pass of its
own. Delivered by M118. If an unbudgeted Decisions section is ever observed
absorbing pasted output despite the advisory, the advisory's severity is the
entry to supersede.

### D-075 (2026-07-27): The `decisions format` advisory takes the section's own genre, not the work log's one-line grammar — narrows D-074 part 3's grammar clause; D-074 parts 1 and 2 stand (RR08 Q5)

**Context:** D-074 part 3 specified the counterweight advisory for the
newly-unbudgeted `## Decisions` section as WARNing on "an entry that is not one
line", transplanting the `work-log format` advisory's grammar. RB08 escalated
the record-class question that D-074 part 1 settles; RR08 upheld that
classification and, beyond the brief, found the grammar clause defective. The
work log had a pre-existing one-line mandate its advisory merely enforces; the
`## Decisions` section has never had one, and its observed genre at size is the
opposite. Measured over the corpus RR08 read: all 13 of M114's entries wrap to
2–3 physical lines, M83's are paragraphs, M84 and M98 use `### M<NN>-D<n>`
sub-headings with paragraph bodies, M94's run 2–5 lines each. A decision entry
structurally carries its rationale the way a `DECISIONS.md` entry does. So the
grammar as written would either strip rationale out of the record — destroying
the value that makes the section history at all — or WARN permanently on every
normal entry in exactly the M114-shaped files the exemption exists to serve.
A permanently-warning advisory trains the operator to ignore advisories.

**Decision:** The advisory's subject is **pasted output and fenced transcript
blocks inside the section**, not entry length. Its measurable form is RR08's
BC3, ingested into M118 as AC10: exactly 0 WARNs over the whole `## Decisions`
sections of M83, M84, M94, M98 and M114 as fixtures, and ≥1 on a constructed
pasted-output fixture. Where BC3 left the 0-WARN arm open between "the whole
sections" and "the enumerated forms only", the ingest gate bound it to the
whole sections: the enumeration omits forms the corpus actually contains
(M83's undated `- **M83-D1:` bullets, M94's bare pointer prose), and the weaker
reading would let a detector pass by dodging them. Rejected: keeping the
one-line grammar (measured to WARN on every entry in the corpus); dropping the
advisory entirely (D-046 rejected shipping an exemption bare, and that
reasoning is unchanged — something must watch a section that has stopped
costing budget).

**Consequences:** Narrows D-074 part 3's grammar clause only. D-074 parts 1
(the history classification) and 2 (the cap exemption and its reason) stand
unchanged, and RR08 independently upheld part 1 on forward-direction grounds.
D-046's underlying concern is preserved, not weakened — what changes is what
the watch is looking for. The concrete detection mechanism stays the
implementer's choice, bounded by AC10's two arms. Delivered by M118. If the
pasted-output detector proves unable to hit both arms over the named corpus,
the entry to supersede is this one, and the alternative on the table is a
narrower fenced-block-only subject.

### D-076 (2026-07-27): The cap-exempt set carries two grounds, not three reasons — narrows D-074 part 2's "three distinct reasons" clause; D-074 parts 1 and 2's exemption stand (M118 review)

**Context:** D-074 part 2 admitted the milestone-local `## Decisions` section to
the cap-exempt set and instructed that "the set becomes three members carrying
three distinct reasons, and every site that enumerates it says so rather than
naming a pair." M118 shipped every enumeration site naming all three members,
but stated **two** grounds rather than three, and recorded the departure only in
its own `## Decisions` section. The M118 review's diff-bug lens scored the
divergence 82: a milestone-local record compresses into a ≤25-line archive
summary at `done`, while the bounded `DECISIONS.md` read (D-054) scans `### D-`
headings and never milestone archives — so a later reader meeting cap pressure
on a fourth section would find a live instruction the shipped rulebook does not
satisfy, with nothing saying which won.

The clause was also internally inconsistent as written: the same part 2 admits
the section "for D-046's reason and not D-030's", which is the work log's
reason, so part 2 simultaneously required a distinct third reason and named a
shared second one.

**Decision:** The cap-exempt set carries **two grounds across three members**.
(1) `## Review` is exempt because it is review-owned and accumulates evidence at
review time, which must never scramble plan-owned content (M55). (2) `## Work
log` and `## Decisions` are exempt because D-045 makes each of them history —
never edited — so counting either could leave an over-cap file fixable only by
an edit IP4 forbids; they reach that one ground by two independent
classifications, D-046 for the work log and D-074 part 1 for the decisions
section. What every enumerating site must still do is name **all three members
and each member's own stated reason**, never a pair — that requirement of part 2
is unchanged and is what M118 delivered.

**Consequences:** Narrows D-074 part 2's "three distinct reasons" clause only.
D-074 part 1 (the history classification, independently upheld by RR08 on
forward-direction grounds) stands; part 2's exemption and its no-pair rule
stand; part 3 is already narrowed by D-075. Nothing on disk changes — this
entry records which of two live wordings governs, and the wording it endorses
is the one M118 shipped. If a fourth section is ever admitted on a ground that
is neither review-ownership nor un-editability, the count in this entry is what
gets superseded, not the no-pair rule.

### D-077 (2026-07-27): D-075's "WARN on every entry" is narrowed to 23 of 24 — supersedes that measurement clause; the rejection it supports stands (M119)

**Context:** D-075 rejected the transplanted one-line grammar for the
`## Decisions` section on the ground that it was "measured to WARN on every
entry in the corpus". M119 re-measured that grammar over the same five sections
read at their archiving commits, because the claim is restated in shipped code
comments and guard docstrings and guard-doctrine §6 makes an inherited finding
unverified until read out of the implementation. The corpus carries **24** `- `
entries; **23** wrap and would WARN, and one does not — M84's single-line review
entry, `- 2026-07-18: review — 3 lenses (7 findings, ...)`. The grammar's total
over the five sections is 117 WARNs.

**Decision:** The measurement is **117 WARNs, with 23 of the corpus's 24 `- `
entries wrapping**, and the shipped restatements say so. "Every entry" is
withdrawn as a measurement; nothing else in D-075 moves.

**Consequences:** Supersedes D-075's "measured to WARN on every entry in the
corpus" clause and nothing else. The rejection that clause supports is unchanged
and does not depend on the exception: 23 of 24 entries WARNing is a permanently
warning advisory on the same reasoning, and the lone exception is an entry of
the work log's own genre sitting in a decisions section. D-075's subject
(pasted output and fenced transcript blocks), its BC3 arms, and D-074 parts 1
and 2 all stand. Recorded here rather than only in M119's own `## Decisions`
section for D-076's reason: a milestone-local record compresses into an archive
summary at `done`, and the bounded `DECISIONS.md` read (D-054) never scans
archives, so a later reader would meet the withdrawn measurement as live.

### D-078 (2026-07-27): The review fan-out's false-positive taxonomy moves from the reviewers' instruction into the scorer's rubric — annotates D-016 (the scorer gates what reaches the user), closes an IP3 gap

**Context:** `/milestone-review` step 5 gave all three reviewers the
false-positive taxonomy and told them to "drop anything matching it before
reporting". Anthropic's Opus 5 prompting guide
(`references/prompting-opus-5.md`, § Capability improvements) reports the
failure mode directly: "If your review prompt says 'only report high-severity
issues' or 'be conservative,' the model may follow that instruction literally
and report less; ask it to report everything and filter in a separate pass
instead." cairn's instruction is that shape. The gap it opens is IP3's, not
merely a quality one: a finding dropped at the reviewer reaches neither the
scorer nor the `## Review` section, so it is dropped *silently*, while the same
step refuses exactly that two paragraphs below — sub-80 findings are "excluded
from the actioned list but logged … surfaced, never silently dropped (IP3)".
Two filters ran, and only the second one kept a record.

**Decision:** The reviewers are told to report every candidate finding and
filter nothing. The taxonomy is carried verbatim inside the `[S]` scorer's
rubric instead, framed as an out-of-scope-for-this-diff judgment that scores
below 60 — the rubric's existing band for "speculative or out of scope" — so a
taxonomy match lands in the logged sub-80 list rather than vanishing. Rejected:
leaving the taxonomy with the reviewers and adding a "log what you dropped"
instruction, which asks a filtered channel to report on its own filtering, the
unfalsifiable arrangement guard-doctrine §3 names. Also rejected: deleting the
taxonomy outright — it encodes real triage judgment and the guide's own remedy
is to move the filter downstream, not to remove it.

**Consequences:** One filter now runs, once, at a station that already keeps a
record. The relocation moves three diff-relative judgments — pre-existing,
unmodified line, plan-called-for — to a station that previously held no diff, so
step 5 now states the scorer's evidence base explicitly: it is given the diff and
the milestone file, and its independence means it did not *generate* the
findings, never that it is blind to what they are about (M120 review, F7). D-016 needs no supersession and is annotated instead: its stated
rationale — the scorer "gates which findings reach the user", which is why the
step stays on Sonnet and never Haiku — now covers strictly more surface, since
the taxonomy judgment moved onto that same station. The scorer's load grows by
whatever the reviewers used to absorb, which is the falsifier to watch: a review
pass whose logged sub-80 findings are dominated by taxonomy matches would mean
the volume was worth the reviewer-side filter after all. `test_review_fanout.py`
locates the rubric by its own first line and walks the contiguous blockquote, so
moving the taxonomy back out of the rubric reds. That is the bound, not a
closure: a fresh restatement of the taxonomy *added* to the reviewers'
instruction, in wording the absence-assert does not name, leaves both tests
green. The paired absence-assert on the old instruction registers the
report-everything phrase as its positive framing.

### D-079 (2026-07-27): D-067's two fresh-context readers are both narrowed, not retired — §8's certified scope excludes text a previous round's own fix authored, and the criteria audit gains a mandatory record — narrowly supersedes D-067, at the "don't tune it" half of §8's falsifier; extends D-069's scope bound, cites `prompting-opus-5`

**Context:** Anthropic's Opus 5 prompting guide reports that explicit
self-verification instructions "cause over-verification on Claude Opus 5, and
removing them reduces wasted tokens with no loss in quality", on the stated
mechanism that "Claude Opus 5 verifies its own work without being told to"
(`references/prompting-opus-5.md`, § Task scope and over-verification). Its
delegation instruction carries a third clause M120 deliberately did not take —
"do not use subagents to verify or double-check your own work" — which reads,
unqualified, straight onto D-067's two readers. M121 swept the nine
`skills/*/SKILL.md` files and five `skills/shared/*.md` modules and classified
all 79 hits (`references/self-verification-ledger.md`): 31 gather evidence by
command, 36 are not instructions at all, exactly **one** is an author re-reading
work it just produced, and the remaining 11 are these two instruments. The
guide's finding therefore lands almost entirely on D-067 and nearly nowhere
else, so D-067 is where it had to be answered.

The measured yield and cost, per instrument, read from the milestones' own
records:

**Instrument 1 — the plan-gate criteria audit.** M115 recorded gated amendments
to AC2/AC6 after a plan-time criteria re-read, with AC5's ambiguous `verbatim`
settled at the gate (`milestones/archive/M115-fresh-context-reader-instruments.md`,
Decisions) — but that re-read was the plan author's own, standing in for the
instrument M115 was building, and M115's work log says so
(`milestones/M115-fresh-context-reader-instruments.md:123`, pre-archive at
`67a6e96^`): "I authored these criteria, so this is the weaker self-check rec 4
exists to replace." It is evidence the questions find things, not evidence
about the fresh-context reader, which did not exist yet. M116 audited twice: round 1 found {AC2, AC5, AC6} jointly
unsatisfiable — the class no per-criterion read reaches — and round 2 four
drafting defects plus the exactly-once locator constraint
(`milestones/M116-placement-test-repair.md:52`, work log, pre-archive; live in
git only, at `32122ab^`). M118 bound four criteria-audit ambiguities at its
gate, each as a Deviations row
(`milestones/M118-decisions-section-cap-exempt.md:193`, pre-archive at
`c76fa65^`). **M117 and M119 carry
no audit record anywhere in their files.** Cost is one reader per plan, two
where a round found something; M116 stopped at two on D-069's regress ground.
So: two measured firings of the instrument itself (M116, M118), both
productive, one earlier self-check that found the same class of defect, and two
milestones where "did not run" and "ran and found nothing" cannot be told
apart. Counted over the five milestones that followed M115's adoption — M116
through M120 — three carry no record at all; this entry's window is the
M115-M119 one its evidence is drawn from.

**Instrument 2 — `guard-doctrine.md` §8 description-layer certification.** Round
counts and findings: M116 two rounds, 9 + 2 (`milestones/archive/M116-placement-test-repair.md`,
Review); M117 four, 8 → 6 → 6 → 2, round 1's first two being genuinely unasserted
AC clauses (`milestones/archive/M117-detector-site-axis-and-recorded-alternative.md`,
Review); M118 three, 16 → 10 → 2, round 1's sixteen including eleven blocking
(`milestones/M118-decisions-section-cap-exempt.md:123,139`, pre-archive at
`c76fa65^`); M119 **nine**
(`milestones/M119-decisions-advisory-and-consistency-guards.md:99-123`, with
the review-entry override at `:125`, pre-archive at `8dace78^`). Every one of those four files is archived now, so
those line numbers resolve in the named pre-archive revisions and nowhere in
the working tree. The
shape is not a flat cost. Round 1 returned real defects in every milestone that
ran it. M119's own summary states what rounds 5–9 returned: "zero
shipped-behaviour defects apart from round 7's live `^diff --git ` false
positive; what repeated was a false claim in the previous round's own fix
comment — round 9's two findings sit in round 8's text", with the thrash rule
unable to fire because it counts review returns and this loop runs before
review. M119's review-entry override logged the same finding and deferred the
durable call here: "Not a precedent: M121 owns the durable disposition."

**Decision:** Both instruments are **narrowed**; neither is retired and neither
is kept unchanged.

1. **§8's certified scope excludes text a previous round's own fix authored:
   a finding whose only subject is such a record is fixed in place and opens
   no further round.** It is still fixed — leaving an inaccurate record
   unexamined ships the defect §8 exists to catch — but it no longer drives a
   further round. The zero-unresolved bar and the round count are untouched.
   Wired at `guard-doctrine.md` §8; `/milestone-implement` step 8 is unchanged.
2. **The criteria audit records one work-log line either way** — what it
   returned, or that it returned nothing — so an absent line means the reader
   did not run, never that it ran and was silent. Stated once at
   `/milestone-plan` step 3 and cross-referenced from `/milestone-brief`'s RR
   ingestion.
3. **`tracking-rules.md` "Model and agent strategy" names both classes of
   self-checking** — an author re-checking work it just produced, which the
   delegation warrant governs, and an independent fresh-context reading by a
   reader that authored none of it, which it does not. Without this the guide's
   third clause reads onto both instruments.

**Consequences:** What this supersedes is the "don't tune it" half of §8's own
falsifier — "if guard-authoring milestones still average multiple
description-layer returns after adoption, the step didn't work — retire it
(D-059), don't tune it". That falsifier **fired**: the average over M116–M119
is 4.5 rounds. What the measurement does not support is its prescribed remedy.
Round 1's yield was real in all four milestones, and **every one of M119's
rounds 5–9 also returned a real guard-coverage gap** — round 9's was a
`--- a/|+++ b/` widening that would have WARNed forever. What repeated was
narrower than "another round": eleven of those rounds' findings were record
errors in an earlier round's own fix text, round 9's two sitting in round 8's.
So the object narrowed here is the certified scope, which D-069 already
narrows, and not the round count, which D-059's precedent forbids tuning.
D-067's own exit line — "If either reader proves to cost more than the returns
it prevents, this is the entry to supersede" — is what is being executed here.

**A round-bounding rule was drafted first and withdrawn**, recorded because the
reasoning is the finding: "the loop stops at the first round returning no
shipped-behaviour defect and no regression" reads two ways and fails both. If
guard-coverage gaps are not shipped-behaviour defects it fires at M119's round
5, discarding nine later gaps; if they are, it never fires. M121's own §8
certification returned that as round 1's finding against the milestone that
wrote it, which is the instrument working on its author.

Extends D-069: that entry put a certification round's own report outside the
certified scope; this puts the *fixes* those rounds write outside it too, on
the same convergence ground, since round N's fix is round N+1's uncertified
surface. Rejected: retiring §8 outright (it would discard round 1's measured
yield and rounds 5–9's coverage gaps alike); bounding the round count (above);
extending the thrash counter to implement-phase loops (a counter is the
round-count tuning the falsifier forbids; the ROADMAP row proposing it stays
open for the reverse case); budgeting the description layer by length (M120's
third candidate disposition — it addresses prose volume, not the
re-certification regress that actually repeated). The falsifier's exit
condition is re-armed against the narrowed form: if guard-authoring milestones
still average multiple returns with this scope in force, retire the step.

### D-080 (2026-07-27): D-079's §8 scope exclusion is withdrawn on RR09's evidence — it is inert on its own motivating case under one reading and discards real findings under the other — supersedes D-079's clause 1 and the exclusion claim in D-079's heading; D-079's clauses 2 and 3 stand

**Context:** M121 shipped a scope exclusion in `guard-doctrine.md` §8: a finding
whose only subject is text a previous round's own fix authored is fixed in place
but opens no further round. Its own §8 certification challenged it at round 1
(after an earlier round-bounding rule had already been drafted and withdrawn),
and `/milestone-review`'s three-lens fan-out challenged it again on three
grounds scoring 80, 74 and 62. It was escalated as RB09.

RR09 confirmed all three objections in refined form and returned verdict (d) —
rebuild the exclusion rather than keep or retire it — with nine recommendations
and eight binding criteria. Its decisive measurement is a round-by-round
classification of M119's rounds 5–9 (RR09 §2, from `8dace78^`): **the shipped
rule has two readings, selected by an operative noun the paragraph never
defines.** Under the *record* reading the exclusion reaches the description
layer only, every one of rounds 5–9 returned at least one non-excluded finding
(counts 3, 4, 2, 2, 1), the round count is unchanged and the loop still ends by
override — inert on the very case that produced it. Under the *text* reading it
reaches anything a fix wrote, and the loop stops at round 5 — the exact stopping
point of the withdrawn round bound, which D-079 itself records as unacceptable,
losing round 9's forever-WARN widening set among others.

The mandatory pre-ingest criteria audit (D-067's first instrument, run on the
binding-criteria set) then found ten blocking defects in RR09's own BC1–BC8,
including two the set cannot resolve internally: BC1 and BC7 assign opposite
reopening status to the same objects, and BC6 replaces D-067's falsifier with no
criterion requiring a superseding entry — the supersede-don't-ignore violation
RR09 charges against the shipped exclusion, reproduced in its remedy.

**Correction owed to the record:** RB09 supplied as a fixed constraint that
"D-079 has not merged, so the authoring milestone may still amend it in place
(M115's precedent)". That is false. **D-065** settles it — "IP4 attaches at
append time, not at merge time: an entry's not-yet-merged status is no
carve-out" — and D-065 was written to close the M115 precedent the brief cited.
The reviewer took the constraint at face value, as a brief instructs, so **BC3
mandates an IP4 violation and its check is unsatisfiable by the legal route.**
Recorded here so a later reader does not treat BC3 as usable.

**Decision:** Withdraw the exclusion. `guard-doctrine.md` §8 returns to its
pre-M121 bytes, and the three asserts and three mutation entries that pinned the
exclusion go with it. D-079's clause 2 (the criteria audit records one work-log
line either way) and clause 3 (the rulebook names both classes of self-checking)
are untouched and ship — neither was challenged at any gate. §8's rebuild is
banked on the existing ROADMAP row, with RB09/RR09 archived as its evidence and
this entry as its lineage.

**Consequences:** This is a **departure from RR09's verdict**, which rejected
option (b), reverting to §8 unchanged, on the ground that it "leaves a fired
falsifier with its remedy owed, and discards a real convergence guarantee".
Both halves of that objection are accepted and neither is answered here: the
falsifier stayed fired, its remedy stays owed, and the convergence guarantee
D-069 gives is unchanged while the one M121 attempted is gone. The ground for
departing is narrower than disagreement — the rebuild RR09 prescribes is
carried by a criteria set with ten blocking defects, so shipping it inside M121
would ship the defects; and `guard-doctrine.md` is not in M121's Scope, which
would need a gated amendment to reach a rewrite this size. D-067's falsifier
therefore stands exactly as D-079 re-armed it, and the round-count problem it
names is open, not solved.

RR09's recommendations 1–6 travel to the banked rebuild rather than being
applied here; recommendation 7 (a one-shot robustness read beside round 1) is
noted on the same row and RR09 itself says not to adopt it inside M121;
recommendations 8 and 9 — rejecting revert-unchanged and rejecting outright
retirement — are recorded, and the first is the one this entry departs from,
stated above rather than worked around.

### D-081 (2026-07-28): M121 edited D-079 in place twice after appending it — an IP4 violation recorded, not repaired; and D-079's "eleven … in an earlier round's own fix text" is corrected to ten of eleven — supersedes that measurement clause; cites D-065

**Context:** M121's second review pass found two defects in this milestone's own
handling of `DECISIONS.md`, both raised independently by the blame-history and
diff-bug lenses and scored 85.

**The violation.** D-079 was appended at `abe04f2`. It was then edited **in
place** at `fb663cb` — heading rewritten, Decision clause 1 rewritten wholesale,
Consequences substantially rewritten — and again at `124da58`, heading rewritten
a second time. D-065 forbids exactly this: "IP4 attaches at append time, not at
merge time: an entry's not-yet-merged status is no carve-out, because the rule
is about the record's form, not its distribution, and a carve-out would make
every unmerged history file editable by whoever is holding it." D-065 exists
because M114's review pass 5 caught D-064 corrected in place and ruled it a
violation. The compounding fact is that **D-080 condemns RB09 for proposing the
same move**, citing D-065 — while M121's own commits had already made it twice,
and no record acknowledged it until now.

**Decision:** Record, do not repair. Rewriting the branch to un-edit D-079 would
be a second and larger history rewrite, and IP4's remedy for a record proven
wrong is a superseding entry, never an edit — the rule cannot be honoured by
breaking it again. So: `git log -p cairn/DECISIONS.md` is authoritative for what
D-079 said when appended; `abe04f2` is the append, `fb663cb` and `124da58` are
the two edits. This entry is the pointer a later reader needs, and it is the
correction D-065's own route prescribes.

**Second, the measurement.** D-079's Consequences reads "eleven of those rounds'
findings were record errors in an earlier round's own fix text, round 9's two
sitting in round 8's." That clause is superseded: the supported figure is
**eleven record errors, ten of them in an earlier round's own fix text**. M121's
own §8 round 2 corrected this in `guard-doctrine.md`, but not here, and the
paragraph carrying the corrected copy was later withdrawn with the exclusion —
leaving the imprecise figure as the only surviving instance in an append-only
file. The work log recorded the finding as closed on the strength of `grep
eleven skills/`, a command that structurally cannot reach `cairn/DECISIONS.md`;
that verification claim is withdrawn here. (RR09 §2's own table sums the per-
round record errors to eleven and describes each as fix-authored, so the
ten-of-eleven split is itself contested — RR09 BC4/BC8 assert ten. What is
recorded here is that the unqualified "eleven … in fix text" overstates what
either source establishes.)

**Consequences:** Two lessons are owed at post-merge hygiene, both about this
milestone rather than about §8. First, a durable record edited on a branch is
still edited — the append-only rule has no unmerged grace period, and a session
that appends an entry early in a milestone must supersede rather than revise it
when the milestone's thinking moves. Second, a verification command must be
scoped to the tree that holds the claim: `grep … skills/` cannot close a finding
about `cairn/DECISIONS.md`, and a green result from the wrong scope reads
identically to a green result from the right one.

D-079's other now-false sentences are left standing and are **not** superseded
here — D-080 scoped itself to clause 1 and the heading's exclusion claim, and
its Consequences section still argues from the withdrawn narrowing. That gap is
recorded as a review finding scoring 78, below the action threshold, and logged
in M121's Review section rather than fixed, because superseding a Consequences
section wholesale is a larger act than this milestone's remaining scope.

### D-082 (2026-07-28): D-080's supersession is widened to reach every claim the withdrawn narrowing supports — D-079's heading pair and its whole Consequences section — and D-080's own three misstatements are corrected; D-067's falsifier is restored in full, "don't tune it" included

**Context:** M121's second review pass found D-080 under-scoped. D-080 named
"D-079's clause 1 and the exclusion claim in D-079's heading" as superseded, but
D-079 argues from the withdrawn narrowing in three further places, and D-080
itself misstates RR09 three times. Four findings scored 78, 78, 68 and 60, below
the action threshold, and were logged rather than fixed; the maintainer held the
merge at the approval gate to close them. Each claim below was re-read out of
the shipped bytes before this entry was written.

**Decision, part 1 — D-079's surviving false claims are superseded.** Its
heading still reads "D-067's two fresh-context readers are **both narrowed**"
and "**extends D-069's scope bound**". One instrument is narrowed at HEAD (the
criteria audit); nothing extends D-069. Under D-054 the heading is the surface a
later sweep reads first, so both clauses are superseded here. Its
**Consequences** section is superseded whole, on the ground that every
load-bearing sentence in it presupposes the narrowing: "So the object narrowed
here is the certified scope, which D-069 already narrows, and not the round
count"; "Extends D-069: that entry put a certification round's own report
outside the certified scope; this puts the *fixes* those rounds write outside it
too"; and "The falsifier's exit condition is re-armed against the narrowed form:
if guard-authoring milestones still average multiple returns with this scope in
force, retire the step". The last has no referent at all once clause 1 is gone.
What survives from D-079 is exactly clause 2, clause 3, and its Context's
measurement of what each instrument caught.

**Decision, part 2 — §8's falsifier stands in its original D-067 form.** D-079
narrowly superseded the "don't tune it" half on the strength of a narrowing it
was shipping. That narrowing was withdrawn, so the ground is gone and the half
is **restored**: §8's falsifier reads as D-067 wrote it — "if guard-authoring
milestones still average multiple description-layer returns after adoption, the
step didn't work — retire it (D-059), don't tune it". It has fired: the average
over M116–M119 is 4.5 rounds, and M121 added two more. Its remedy is owed and
unpaid, and the ROADMAP's §8 row is where that debt is recorded. This replaces
D-080's "D-067's falsifier therefore stands exactly as D-079 re-armed it", which
named a condition that could not fire.

**Decision, part 3 — D-080's two misreadings of RR09 are corrected.** D-080
says "RR09 confirmed all three objections in refined form"; RR09 §3 answers
objection C "**Only under reading 2** — where it is worse than the objection
states. **Under reading 1 it fails.**" Objections A and B were confirmed; C was
confirmed conditionally, on the reading M121 did not take. And D-080 renders the
verdict as "(d) — rebuild the exclusion **rather than keep** or retire it";
RR09 §5 reads "**(d): keep the exclusion, rebuilt**". The distinction is not
cosmetic — RR09 rejected retirement *and* rejected reverting, and its (d) is a
repair of the exclusion, not a replacement of it. D-080's disposition is
unaffected: it departs from RR09's rejection of option (b) and says so.

**Consequences:** Nothing in the shipped prose changes — `guard-doctrine.md`
remains byte-identical to its pre-M121 state, and no skill, guard or test is
touched. This entry is record repair only, and it is the fourth entry in a chain
(D-079 → D-080 → D-081 → D-082) that a later reader must follow to reconstruct
what M121 decided about §8. That chain length is itself the cost of appending an
entry before the milestone's thinking had settled, which is the lesson D-081
names and which post-merge hygiene captures. A reader wanting the short answer:
**M121 changed nothing in §8; D-067's falsifier stands, fired, with its remedy
owed; the rebuild is banked on the ROADMAP row with RR09 as its evidence.**

### D-083 (2026-07-30): §8's rebuild — provenance draws what reopens, a mandate boundary draws what counts, and the round-count falsifier is replaced by a yield-based pair — supersedes D-082 part 2's restoration of that falsifier and narrows D-067's zero-unresolved bar twice; annotates D-069/D-070 as compatible rather than superseded; corrects D-081's ten-of-eleven measurement (RR09 verdict (d))

**Context:** D-067's §8 carries a falsifier — "if guard-authoring milestones
still average multiple description-layer returns after adoption, the step didn't
work — retire it (D-059), don't tune it". It **fired**: the average over
M116-M119 is 4.5 rounds and M121 added two more. M121 attempted a narrowing,
withdrew it at D-080 on RR09's evidence, and D-082 restored the falsifier in
full, recording that "its remedy is owed and unpaid, and the ROADMAP's §8 row is
where that debt is recorded". This entry pays that debt, and does so by
replacing the falsifier rather than by retiring the step — which needs an
argument, not an assertion, because D-059's precedent says retire, don't tune.

**Decision, part 1 — the step is not retired.** Round 1's yield is measured and
real in every milestone that ran it: M116 9 findings, M117 8, M118 16 of which
eleven were blocking, M119 2 code defects, M121 1 shipped-behaviour defect plus
10 description-layer (`8763368^`, and the archived Review sections for the
rest). M121's round 1 also refuted the milestone's own shipped rule — the
instrument working on its author. `/milestone-review`'s three-lens fan-out does
not replace it: that fan-out runs *after* `status -> review` and is
diff-anchored, while §8 reads the whole description layer before the gate. RR09
recommendations 8 and 9 reject both reverting unchanged and retiring outright,
and this entry follows them.

**Decision, part 2 — the falsifier's counted quantity is replaced, and this is
why that is not tuning.** The distinction is a checkable fact about the two
measures, not a claim about intent. The old falsifier counts **rounds**. §8's
two new rules — the provenance shield on fix-authored records, and the mandate
boundary — both act directly on the round count, so the measure is satisfiable
by construction by the very rules it is supposed to police; RR09 §4 shows both
horns, the measure firing on a rule that changed nothing and the measure made
unfireable by a rule that changed too much. The replacement counts, instead,
shipped-behaviour defects and findings on pre-round-1 surface returned by rounds
after the first, and separately any in-place record correction later found
false. Neither quantity is the round count. D-059 forbids tuning a threshold on
a measure that works; what is done here is replacing a measure of the wrong
quantity, and the two are told apart by reading what each counts. Shipped at
`guard-doctrine.md` §8; the window is three guard-authoring milestones and
counts only if at least one of them convened a round after its first.

**Decision, part 3 — D-067's zero-unresolved bar is narrowed twice, and the
narrowings are named.** (a) The mandate boundary: a round reopens only on a
finding within §8's three named checks, so a robustness observation no
acceptance-criterion clause pins is fixed as ordinary §§1-7 work and does not
hold the gate. (b) The confirmation split: a fix-authored record is corrected in
place and confirmed by the next round's reader, or by the three-lens fan-out
where no further round occurs, so the gate is reachable with those corrections
not yet independently confirmed. **No confirmation obligation falls on the
author** — D-067 rejected "a mandatory re-derivation step (it instructs the same
judgment that failed while citing the same instructions)", and an author
re-reading its own corrected record is that rejected move under another name.
The cost (b) creates is what the new falsifier's clause (ii) counts.

**Decision, part 4 — D-069 and D-070 are annotated, not superseded.** D-070 drew
the certified-scope line on subject matter: records about the work are inside,
narrative about the certifying process is outside. The provenance rule draws a
*different* line, on what a finding reopens, and a fix-authored record never
leaves the certified scope — it is still read and still corrected. M121's
withdrawn attempt framed the same rule as a certified-scope exclusion and so
collided with D-070 without naming it; stating the two axes apart removes the
collision. Nothing in D-069 or D-070 is superseded here.

**Decision, part 5 — D-081's measurement is corrected.** D-081 states "the
supported figure is eleven record errors, ten of them in an earlier round's own
fix text". Re-derived from `016a210` (M119's pre-archive work log), the eleven
holds — rounds 5-9 returned 2, 4, 0, 3 and 2 record errors — but the
ten-of-eleven split does not: the log locates the authoring round for at least
eight of them, identifies **none** as sitting in text that existed before round
1, and RR09 §2's table classifies all eleven as fix-authored. The "ten" traces
to `8763368^`, where M121's round 2 asserted it with no shown derivation.
D-081's own parenthetical half-concedes the point. That clause is superseded;
everything else in D-081, including its record of the IP4 violation, stands.

**Consequences:** §8 grows by roughly 60 lines and is read at every
guard-authoring milestone; the growth was taken deliberately at M123's implement
gate over a compressed form, on the ground that this section's failure history
is rules whose reasoning was left implicit being read two ways. The projection
recorded with the mandate boundary is that M119 replayed under it stops after
round 6, saving three rounds, ±1 on round 6's `kind`-label classification —
which differs from RR09's own tolerance placement (RR09 put the ±1 on round 5).
M123's derivation from M119's acceptance criteria is the basis for the move.
If the yield falsifier's clause (i) fires, §8 runs as a single certification
pass; if clause (ii) fires, fix-authored records return to round-opening. This
entry is the one to supersede if either happens.

### D-084 (2026-07-30): Two measurement claims in D-083 are corrected — §8's growth is +116 lines, not "roughly 60", and the M118 blocking-count figure is sourced to a revision D-083 does not name — supersedes those two clauses; D-083's decision and every other claim in it stand (M123 §8 round 1)

**Context:** M123's own §8 certification round 1, run by a fresh-context [O]
reader under the *pre-rebuild* rules this milestone certifies against, returned
sixteen discrepancies. Two are false claims in D-083, which was appended earlier
in the same milestone. IP4 attaches at append time (D-065, and D-081's record of
M121 violating exactly this), so they are superseded here rather than edited.

**Decision, part 1 — the growth figure.** D-083's Consequences states "§8 grows
by roughly 60 lines". Measured at this entry's append: §8 is **46 lines on
`main` and 162 at HEAD, a growth of +116**; the whole file goes 301 → 417. The
figure was already wrong when written — §8 stood at 155 lines at `cde1066`, the
commit that appended D-083 — and the round-1 fixes added the rest. The
implement-gate work-log line projecting "~35 added lines over ~20" is likewise
unmet and is corrected by the same measurement; the gate's *choice* (rules with
their reasoning, over compressed rules) stands and is what produced the length.
These counts are a dated observation of the tree at this append, not a standing
fact: §8 is inside the corpus M123 is still editing (M99's fixed-point lesson,
third instance), so a later measurement supersedes rather than contradicts.

**Decision, part 2 — the M118 sourcing.** D-083 part 1 states "M118 16 of which
eleven were blocking" with the parenthetical "(`8763368^`, and the archived
Review sections for the rest)". Neither source establishes the split:
`8763368^`'s work log gives "M118 16" with no blocking figure, and M118's
archived Review section gives only the round sequence "16 -> 10 -> 2". The
eleven-blocking figure lives at **`c76fa65^`**, M118's pre-archive milestone
file, which D-083 does not name. The figure is correct; its citation was not.
Both are now recorded here, so a later reader can reach the source.

**Consequences:** Nothing in D-083's decision changes — the step is still not
retired, the falsifier's counted quantity is still replaced on the same ground,
the two narrowings of D-067's bar and the annotation of D-069/D-070 all stand,
and part 5's correction of D-081 is untouched. This entry exists because a
measurement claim about the milestone's own artifact was written before the
artifact stopped moving, which is the failure M99's lesson names and which
D-081's chain-length cost warns about. The general remedy is the one already in
the rulebook: settle numeric records last, after the content has stopped moving
(`guard-doctrine.md` §6). D-083 was appended at T6, three tasks before the
content settled.

### D-085 (2026-07-30): §8's evidence derivations move here from the doctrine, the round-count falsifier's defect is restated in its independent form, and clause (iii) extends D-083's supersede-on-firing trigger to a third clause — annotates D-083 and D-084; records RR10's verdict (e) and the re-visit of RR09 recs 8-9 (RR10, M123)

**Context:** RR10 reviewed whether `guard-doctrine.md` §8 should survive at all,
given that its own rebuild took two certification rounds returning 16 and 13
discrepancies. Verdict **(e)**: keep §8, with four amendments. It rejected
retiring the step, decreeing a single pass, and folding the instrument into
`/milestone-review`'s three-lens fan-out. The fold rejection rests on a measured
fact rather than a preference: that fan-out's scorer put M121's four
description-layer findings at 78, 78, 68 and 60, all below the action threshold,
and they were logged rather than fixed (D-082).

**Decision, part 1 — the round-count falsifier's defect, in its independent
form.** D-083 part 2 argued that the old falsifier counted the wrong quantity
because §8's two new rules act directly on the round count. That argument
presupposes the rules it defends. RR10 supplies the ground that does not:
**under the pre-rebuild rule "a discrepancy is fixed and re-certified", a second
round is convened if and only if round 1 returns at least one finding.** So
"guard-authoring milestones still average multiple description-layer returns"
fired exactly when the instrument had yield — it measured yield and reported it
as failure, and a milestone could satisfy it only by having a round 1 that found
nothing. This supersedes nothing in D-083; it replaces D-083's weaker leg with a
stronger one for the same conclusion, and it is the load-bearing ground for the
replacement.

**Decision, part 2 — clause (iii), and what it extends.** RR10 found a real
deficiency in what D-083 shipped: after the replacement, **no condition anywhere
retired the whole step**, so round 1 itself had become unfalsifiable. §8 now
carries a third falsifier clause under which round 1's own yield decay retires
the step whole. It counts four quantities, not the three RR10's binding
criterion named — the fourth is anchor-fidelity findings, §8's third check,
whose omission would let a window returning only those findings read zero and
retire an instrument demonstrably working, which is the same anti-calibration
RR10 convicts the old falsifier of. §8 also states that clauses (i) and (iii)
cannot both fire. D-083 closes "This entry is the one to supersede if either
happens"; **this entry extends that trigger to a third clause.**

**Decision, part 3 — §8's evidence derivations live here, not in the doctrine.**
Each of the following was stated in §8 and is relocated, with §8 keeping a
one-sentence pointer. Every figure is a dated observation of the sources named,
read 2026-07-30, not a standing fact.

- **The record-churn class, the provenance rule's ground.** M114 pass 8's round
  4 found discrepancies only in narrative its own earlier rounds had written —
  four false claims in a round-3 entry, plus a neighbour re-recording two
  observations logged three entries earlier (`a25e6dd^`). M119's rounds 5-9
  returned eleven record errors, and `016a210` locates the authoring round for
  at least eight of them while identifying none as sitting in text that existed
  before round 1. M121's round 2 returned twelve findings, five of which had
  round 1's own fix prose as their only subject (`8763368^`).
- **Why the provenance rule changes M119's round count by zero.** Each of rounds
  5-9 also returned coverage gaps — three, four, two, two and one (`016a210`) —
  and a coverage gap is a finding about executable surface, which the rule never
  shields. That sentence stays in §8 because it is a rule; the sequence moves
  here.
- **The mandate boundary's replay projection.** Replayed under it, M119 stops
  after round 6, saving three rounds. Round 6's `kind`-label gap is the one
  classification that could go either way, since those two labels are M119's own
  AC1 pasted-output-or-fenced-block distinction, and reading it as in-mandate
  stops the replay after round 7 instead. Tolerance: ±1 round, on that gap.
  RR09 placed the same ±1 on round 5; M123's derivation from M119's own
  acceptance criteria puts round 5 beyond doubt and the coin-flip on round 6.
- **What each falsifier clause counts.** Clause (i) counts whether the later
  rounds still find anything the two reopening rules have not already disposed
  of. Clause (ii) counts the cost those rules create — records corrected without
  an independent read — which the round-count falsifier could not see. Clause
  (iii) counts whether round 1 itself still earns its reader. All three are
  countable from work logs as milestones already write them.

**Decision, part 4 — RR09 recs 8 and 9, re-visited.** RR10 re-examined both
against M123's own two-round cost, which RR09 did not have, and **re-affirmed
them**: reverting §8 unchanged and retiring it outright both stay rejected.
Recorded as the outcome of the re-visit rather than as a conclusion mandated in
advance. One divergence from RR10 is noted rather than smoothed: RR09's
falsifier clause (ii) offered "returns that class to round-opening **or** the
step is retired", and M123 selected the first consequence and dropped the
disjunction, because a single falsified in-place fix retiring the whole step is
disproportionate when clause (iii) already governs whole-step retirement.

**Consequences:** §8 falls from 183 lines to under 150 with no rule removed —
every sentence an assert pins survives or is re-anchored, and the asserts whose
only anchor was relocated evidence retire with their registry entries. The
figures above are now the single home for these derivations; §8 points here, and
a later reader chasing a count reads this entry rather than the doctrine. If
falsifier clause (i) or (iii) fires, the retirement edit should prune the
convergence apparatus — the two axes, the shield, the per-class obligations —
along with the rounds it governs, rather than leaving doctrine about rounds that
no longer run; that is RR10 recommendation 8, banked here rather than acted on.

### D-086 (2026-07-30): Three measurement claims in D-085 are corrected and its replay projection gains the revision AC7 requires — supersedes those clauses; D-085's decision and its other content stand (M123 §8 round 3)

**Context:** M123's §8 certification round 3 — the first run under the rebuilt
rules — returned ten findings. Four bear on D-085, which was appended earlier in
the same milestone. IP4 attaches at append time (D-065), so they are superseded
here rather than edited. This is the fourth entry in M123's own chain
(D-083 → D-084 → D-085 → D-086), and the cause is the one D-081 already named
and D-085 restated: a numeric record written before the artifact stopped moving.

**Decision, part 1 — "with no rule removed" is false as written.** D-085's
Consequences states that §8 "falls from 183 lines to under 150 with no rule
removed — every sentence an assert pins survives or is re-anchored, and the
asserts whose only anchor was relocated evidence retire with their registry
entries." The compression retired **nine** test methods, not eight. The ninth,
`test_the_class_is_never_called_by_a_synonym`, was a structural test over §8
whole; its anchor was not relocated evidence and it had no registry entry to
retire with, and it was the only pin on AC1's no-unmarked-synonym clause. With
it gone, `Fix-authored text is neither read nor corrected` shipped green over
the whole suite. It is restored at round 3, and its comment now records the
deletion. Nothing else in the compression removed a rule.

**Decision, part 2 — the line figure is exact, not approximate.** "Falls from
183 lines to under 150" is superseded: §8 is **exactly 150 lines** at the
compression commit and 149 after round 3's paragraph merge. AC12's ceiling is
`≤150`, so "under 150" understates the margin and misdescribes the result.

**Decision, part 3 — the movable-evidence figure.** M123's "Deviations from
RR10" table records "movable evidence ~23 not ~40" as the ground for raising
RR10's ceiling from 135 to 150. Against the shipped result that is wrong: 164
lines at ingestion, +19 added by the sufficiency arm and clause (iii), −33
removed by the compression = 150. So ~33 lines moved, not ~23, and the shipped
result beat the row's own stated best case of 151. The extra ten came from four
justification passages that RR10's BC3 does not name among its permitted
removals — a real over-reach against BC3's letter, disclosed here rather than
left in the arithmetic. The maintainer's ceiling decision is unaffected: 150 was
reachable, and the row's error was pessimism about how much was movable.

**Decision, part 4 — the replay projection gains its revision.** D-085 part 3's
third bullet states that M119 replayed under the mandate boundary stops after
round 6, saving three rounds, ±1 on round 6's `kind`-label classification, and
attributes it to "M123's derivation from M119's own acceptance criteria" without
naming a revision. AC7 requires every count to carry the revision it was derived
from. The revision is **`016a210`** — M119's pre-archive milestone file, whose
`## Acceptance criteria` section supplies the AC1 clauses the classification is
made against and whose work log supplies the per-round gap counts. The figure is
unchanged; only its citation was missing.

**Consequences:** D-085's decision stands in full — the relocation, the
independent wrong-quantity ground, clause (iii)'s extension of D-083's trigger,
and the RR09 re-visit are all untouched. What is corrected is four claims about
this milestone's own artifact, every one of them found by the instrument this
milestone exists to rebuild, and three of them written by an earlier round's own
fix. That distribution is itself the evidence D-085 part 1 grounds the
provenance rule on, produced once more by the milestone that ships it.

### D-087 (2026-07-30): D-083 part 4's "a fix-authored record never leaves the certified scope" is the absolute round 1 convicted in §8 and is narrowed to the non-removal rule §8 ships — supersedes that clause; part 4's annotation of D-069/D-070 stands (M123 review return 1)

**Context:** M123's `/milestone-review` fan-out returned finding A2 (scored 80).
D-083 part 4 argues that D-069 and D-070 are annotated rather than superseded,
and rests that argument on the sentence "the provenance rule draws a *different*
line, on what a finding reopens, and a fix-authored record never leaves the
certified scope — it is still read and still corrected". That is the formulation
§8's own certification round 1 convicted at D6, three commits after D-083 was
appended: a record whose subject IS a certification round sits outside the
certified scope for D-069's reason, so "never leaves" is false for exactly the
case D-069 exists to cover. §8 was restated then to a non-removal rule and
D-083 was not, because IP4 attaches at append time (D-065). The entry has
carried the convicted absolute ever since, inside the paragraph whose job is to
prove no collision with D-070.

**Decision, part 1 — the clause is narrowed, not withdrawn.** What D-083 part 4
should have said, and what §8 ships, is that *being* a fix-authored record never
**removes** a record from the certified scope. The provenance rule takes nothing
out of scope; it removes only the power to force another round. A record can
still be outside that scope for D-069's own reason — its subject being a
certification round — and that is D-069 operating, never the provenance rule.
The difference is between an absolute about the record ("never leaves") and a
rule about what this classification does ("never removes"), and only the second
is true.

**Decision, part 2 — part 4's conclusion stands on the narrowed clause.** The
argument D-083 part 4 makes does not need the absolute. D-070 rules on the
subject-matter axis; the provenance rule rules on what reopens; a rule that
takes nothing out of the certified scope cannot narrow a line drawn on what is
in it. So "Nothing in D-069 or D-070 is superseded here" survives, and D-083
part 4 is corrected in its premise rather than in its conclusion. D-069 and
D-070 remain annotated, not superseded.

**Consequences.** D-083 parts 1, 2, 3 and 5 are untouched, as are D-084, D-085
and D-086. §8 needs no edit: it already carries the narrowed form, pinned by
`test_the_provenance_rule_does_not_narrow_the_certified_scope`. What this entry
buys is that the decision record and the doctrine now say the same thing — the
gap A2 found was between them, not inside either. This is the fifth entry in
M123's chain (D-083 → D-084 → D-085 → D-086 → D-087) and the second whose
subject is a claim D-083 made before the artifact stopped moving; the general
cause is the one guard-doctrine §6 already states, settle numeric and
quotable records last.

### D-088 (2026-07-30): D-083 part 3(a)'s "ordinary §§1-7 work" no longer describes shipped §8, which routes to §9 as well — supersedes that enumeration; part 3(a)'s narrowing and every other claim in D-083 stand (M124)

**Context:** M124 appends `guard-doctrine.md` §9, "Presence is not
consistency", and updates §8's two routing enumerations to name it — the plan
gate's call, on the ground that §9 carries the section-consistency ledger and
an out-of-mandate consistency finding is fixed by applying it. §8 now reads
"recorded and fixed as ordinary milestone work under §§1–7, §9 and the
mutation harness", and "routing one to §§1–7 or §9 does not remove it from the
count". D-083 part 3(a) describes the first of those as "fixed as ordinary
§§1-7 work". That was true when appended and is incomplete against the shipped
section from this milestone forward. IP4 forbids repairing it in place, and
D-083's own family is the precedent: D-084, D-086 and D-087 each corrected a
D-083 claim by appending rather than editing.

**Decision:** Supersede the enumeration in part 3(a)'s sentence, and only
that. Shipped §8 routes an out-of-mandate robustness observation to §§1–7, to
§9, and to the mutation harness. Part 3(a)'s substance — that a finding no
acceptance-criterion clause pins does not hold the gate — is untouched and
still governs; what changes is the list of sections the fix happens under.
Nothing in part 3(b), part 4, or any other part of D-083 is reached.

**Consequences:** A reader of D-083 reaches this entry by the back-reference
discipline (D-054); its heading names D-083 as superseded. The enumeration is
a surface that now goes stale on every section append — the same defect class
§9 itself names — so the durable statement lives in §8, where a guard pins it,
and D-083's copy is a dated description rather than a second authority. The
plan gate considered rewording §8 to stop enumerating and declined, preferring
an accurate list to an unfalsifiable phrase; that trade is what this entry
pays for. If §9 is renumbered or retired, this is the entry to supersede.

### D-089 (2026-07-30): D-088's precedent list is wrong about D-086, whose subject is D-085 — supersedes that clause; D-088's decision and every other claim in it stand (M124 §8 certification round 1)

**Context:** D-088, appended earlier in this milestone, says "D-083's own
family is the precedent: D-084, D-086 and D-087 each corrected a D-083 claim by
appending rather than editing." M124's §8 description-layer certification read
that against the entries rather than against the narrative. D-084 and D-087 do
correct D-083. D-086 does not: its heading reads "Three measurement claims in
D-085 are corrected", and its body opens "Four bear on D-085, which was
appended earlier in the same milestone." The claim is false of one of its three
members.

**Decision:** Supersede that sentence and nothing else. The precedent for
correcting a D-083 claim by appending is D-084 and D-087; D-086 is the same
move applied to D-085, one link along the same chain — precedent for the
practice, not for the subject. D-088's decision, that shipped §8 routes an
out-of-mandate observation to §§1–7, §9 and the mutation harness and that
D-083 part 3(a)'s enumeration is superseded, is untouched and still governs.

**Consequences:** Appended rather than edited, though D-088 is minutes old and
sits unmerged on this milestone's branch: IP4 attaches at append time, not at
merge time (D-065), and M114's pass-5 finding is the precedent for refusing to
treat an unmerged entry as editable. This is the second entry in one milestone
whose subject is another entry's measurement claim — the record-churn class
D-085 grounds §8's provenance rule on, produced once more by the milestone
shipping a guard against a neighbouring failure. A reader of D-088 reaches this
entry by the back-reference discipline (D-054).

### D-090 (2026-07-30): The verification-apparatus program is closed at the door — a new apparatus milestone needs a shipped-behavior defect as its trigger — D-057's move applied to the flow side; annotates D-067

**Context:** Four consecutive milestones were verification apparatus — M119,
M121, M123, M124 — plus two Fable escalations about §8 itself (RR09, RR10) and
a same-day run of correction entries, D-083 through D-087 on main with M124's
unmerged branch appending two more after D-087 (those two ids are reserved,
not skipped — the D-067 precedent — and this entry takes the next id after
them). M123, the milestone rebuilding §8 so its certification loop converges,
ran seven certification rounds on its own rebuild; M124 ran seven more and
terminated only by maintainer override, rounds 5–7 each finding one instance
of a single class with each fix one more enumeration. This is the signature
D-057 recorded for the size-governance program: the anti-cost program
maximizes the cost it exists to reduce, because an apparatus milestone is
itself guard-authoring and receives maximal certification. The maintainer
asked on 2026-07-30 for a durable fix to the thrash; the shape-repeat stop
rule (M125, planned at this same gate) is the mechanical half, and this entry
is the supply-side half.

**Decision:** No new milestone is planned whose deliverable is verification
apparatus — a new instrument, a new meta-guard, a new certification or audit
step, doctrine about the verification of doctrine — unless its trigger is a
defect in shipped behavior: what the plugin's skills, hooks, and scripts do
for their users. A defect in doctrine prose, in records, or in the apparatus's
own coverage is fixed as ordinary work within the milestone that surfaces it,
never promoted into its own apparatus milestone. M125 is excepted by name as
the program's in-flight closing act, planned beside this entry at the same
gate; the door binds every plan gate after it. Parked behind the door: the
ROADMAP's falsifier-state-disclosure row and its audit-over-falsifiers row
(RR10 recs 7 and 9) — each now requires this entry's trigger in addition to
its own stated condition. Untouched: §8's own falsifier clauses, which are the
measured retirement path and whose firing removes apparatus rather than adds
it; the RB/RR escalation protocol; and repairs to existing apparatus surfaced
as ordinary work.

**Consequences:** The plan-time collision check surfaces this entry on any
apparatus-shaped scope, and the standing-rejection discipline applies:
supersede, don't ignore. If a shipped-behavior defect class appears that a
parked apparatus candidate would have prevented, this is the entry to
supersede.

### D-091 (2026-07-30): Certification gains a third ending — the shape-repeat stop — and recorded counts gain a verbatim-reproducible procedure rule; narrowly supersedes D-085's clause-(i) gloss; reuses D-064's trigger (b) beyond review returns (M125)

**Context:** M124's §8 certification ran seven rounds and terminated only by
maintainer override, rounds 5–7 each finding one instance of a single class
with each fix one more enumeration — the repeated-shape signature D-064's
trigger (b) names for review returns (read from
`cairn/milestones/archive/M124-section-consistency-ledger.md`). Separately,
M124 spent adjudication on counts that disagreed only because no record
stated the procedure producing its figure: the reflow suite count ran 21,
then 75, then "75 errors and 11 failures", with the one discriminator —
whether bullet paragraphs are re-wrapped — stated in none of the three (read
from the round-4 O1 work-log line at
`git show a5a7007:cairn/milestones/M124-section-consistency-ledger.md`).
The maintainer asked on 2026-07-30 for a durable fix to the thrash; M125
ships these two mechanical halves, and D-090, appended at the same plan
gate, is the supply-side half.

**Decision, part 1 — the stop rule.** `guard-doctrine.md` §8 now ends a
certification by rule when two consecutive rounds each return a reopening
finding of the same defect shape: no further round is convened, and the
second same-shape finding forms its own class — the shape-repeat finding —
whose one confirmation obligation is a structural remedy closing the shape's
class rather than its instance, confirmed by operation. Whether two findings
share a shape is the judgment D-064's trigger (b) applies to review returns,
applied here to certification rounds. A certification therefore ends in one
of three ways: the gate opens at zero unresolved; a falsifier clause retires
rounds across the measured window; or the stop rule ends the rounds on a
repeated shape. The stop rule carries its own falsifier in clause (ii)'s
form (tolerance: one occurrence), and a shape-stopped certification counts
toward the falsifier window exactly as run — no round it declined to convene
is imputed.

**Decision, part 2 — the clause-(i) gloss, narrowly superseded.** D-085's
"What each falsifier clause counts" bullet glosses clause (i) as counting
whether the later rounds still find "anything the two reopening rules have
not already disposed of." The stop rule makes that enumeration incomplete:
the shape-repeat stop now also disposes of later-round findings, and under
the old gloss a shape-stopped certification's disposed findings would read
as still countable. The gloss is superseded to "anything the two reopening
rules and the shape-repeat stop have not already disposed of"; everything
else in D-085 — its parts 1, 2 and 4, the other three derivation bullets,
and its Consequences — stands.

**Decision, part 3 — the recorded-counts rule.** `guard-doctrine.md` §6 now
requires a count recorded in a milestone record — a work-log line, a
docstring, a comment, or a D-entry — to carry the procedure that produced it
at verbatim-reproducible grade: the command as run, or the committed
artifact it is read from, at the granularity that discriminates it from a
disagreeing record. The counts in this entry's Context carry theirs.

**Decision, part 4 — the candidate row's promotion, a logged deviation.**
The ROADMAP's §8-stop-condition candidate row (added 2026-07-30 from M124's
round-7 maintainer override) stated its promotion condition as a second
override. The user promoted it the same day, at M125's plan gate, before any
second override occurred — recorded here as a deliberate deviation from the
row's own condition (IP2: surfaced, never silently overridden).

**Consequences:** §8's obligation sentences enumerate four classes, and the
obligations proxy counts four. If a structural remedy authored under the
stop rule is later found not to have closed its shape's class, the stop
rule's own falsifier returns that shape to round-opening; and if the stop
rule itself proves the wrong instrument — a certification that repeats no
shape yet fails to converge — this is the entry to supersede.

### D-092 (2026-07-30): Four claims in D-091 are corrected — the rounds-5–7 citation, the D-085-Consequences clause, the candidate-row reference, and part 1's circular trigger description — supersedes those clauses; D-091's decision and its other content stand (M125 §8 round 1)

**Context:** M125's §8 certification round 1 (fresh-context [O] reader)
returned four record defects in D-091, appended hours earlier. IP4 forbids
repairing them in place; this entry supersedes each narrowly, the
D-084/D-086/D-089 shape.

**Correction 1 — the rounds-5–7 citation.** D-091's Context attributes
"rounds 5–7 each finding one instance of a single class with each fix one
more enumeration" to
`cairn/milestones/archive/M124-section-consistency-ledger.md`. That 24-line
archive summary records only the round tally and the override; the
rounds-5–7 enumeration detail is carried by the pre-archive file, read at
`git show a5a7007:cairn/milestones/M124-section-consistency-ledger.md` —
the artifact D-091 cites only for its other count. The claim was true; its
citation did not support it, which is the defect class D-091's own part 3
ships a rule against.

**Correction 2 — "its Consequences — stands".** D-091 part 2 lists D-085's
Consequences among what stands. Two of that section's clauses were already
superseded by D-086 before D-091 was written. Narrowed to: D-085's
Consequences stand as corrected by D-086.

**Correction 3 — the candidate-row reference.** D-091 part 4's "The
ROADMAP's §8-stop-condition candidate row" reads as naming a live row. The
row lived on M124's branch and was removed by M124's post-merge hygiene
pass before D-091 was appended; the reference is historical, to the row as
it stood at M125's plan gate.

**Correction 4 — part 1's trigger description.** D-091 part 1 describes the
stop rule's trigger as "two consecutive rounds each return a reopening
finding of the same defect shape". Round 1 convicted that phrasing as
circular — the rule it describes reclassifies the second such finding out
of the reopening class, so its own precondition could never be met — and
the shipped rule now reads: a finding that clears both lines repeating the
defect shape of the previous round's reopening finding ends the rounds.
AC1 was amended to match at the same gate (user decision, 2026-07-30).

**Consequences:** none of D-091's four decisions changes; the stop rule,
the gloss supersession, the count rule, and the logged deviation all stand
as decided. What changes is only the four claims named above.

### D-093 (2026-07-30): D-090's and D-091's "rounds 5–7 each finding one instance of a single class" is corrected — each round returned two reopening findings, across two threads — supersedes that clause in both entries; both decisions stand (M125 §8 round 2)

**Context:** M125's §8 certification round 2 (finding 5) caught the
undercount in D-091; the same sentence appears in D-090, written at the
same plan gate. This entry lands with the one-pass re-verification of
D-091/D-092's factual claims that round 2's stop obliged (Remedy C).

**Correction:** Read from
`git show a5a7007:cairn/milestones/M124-section-consistency-ledger.md`
(lines 205–219, the round-5/6/7 log lines): rounds 5, 6 and 7 each opened
"2 reopening", and the six findings run in two threads — the
enumeration-widening thread (round 5 F1, round 6 F2, round 7 F1) and the
extractor-instrument thread (round 5 F2, round 6 F1, round 7 F2). "One
instance of a single class with each fix one more enumeration" describes
the first thread alone.

**Consequences:** both entries' decisions stand — the maintainer's
override diagnosis those entries rest on ("every round's fix had been one
more enumeration") is quoted verbatim in the same artifact and survives:
it convicts the thread the stop rule was built for, and the second thread
ended the same way, closed by a structural remedy (the extractor
contract) rather than by a further round — which is the disposition the
stop rule now makes the rule.

### D-094 (2026-07-31): `CLAUDE.md`'s cairn section is a sixth always-read surface, and the frame governs the section rather than the file — annotates D-060 and D-063, superseding nothing

**Context:** The 2026-07-30 `/milestone` audit ran D-060's §2 check and reported
the gap the frame exists to surface: the harness injects `CLAUDE.md` into every
session, and the frame's worked table did not cover it. All three of its
governance elements already existed elsewhere in the rulebook — D-009's
routing-only rule, the weight-caps remedy that trims the section back to the
template, and the <30-line section cap `cairn_validate`'s `weight caps` CHECK
enforces (D-018) — so what was missing was coverage, never governance. M126's
sweep, derived from `hooks/hooks.json`'s sole `SessionStart` entry and
`session_context.build_context` plus the harness-loaded project instructions,
found six surfaces: `ROADMAP.md` and each active milestone file already covered,
`CLAUDE.md` uncovered, and three out of scope.

**Decision:** Four parts.
(1) **A sixth row, appended after the fifth.** This is D-060's own audit bullet
("any newly-added always-read surface not covered") executing as designed, the
second time after D-063 — an application of the frame, superseding nothing, and
the frame stays completeness-only, so D-057's closed stock-side program is
untouched. Appending rather than inserting keeps the guarded sentence "The fifth
surface differs from the four above it" true on the record.
(2) **The governed unit is the section, not the file.** The row's first cell
reads "`CLAUDE.md`'s `## Project tracking` section", because all three of its
dispositions are section-scoped: D-018 caps that section alone and D-009 confines
it to routing. A cell naming the file would make every one of the three overclaim
against a file cairn does not own — the file-map table's own `CLAUDE.md` row owns
the whole file, which is why the inflow cell cites D-009 and not that row.
Nothing about what cairn governs in `CLAUDE.md` changes here.
(3) **The frame's opening definition stays unamended.** "One this repo re-reads
at the start of most sessions" excludes nothing this row needs — a section-scoped
surface is still a file the repo re-reads — so an amendment would buy no
coverage while shipping new prose against D-060's prose-guarded mandate, on a
line that wraps. The definition's real defect runs the other way: three rows
already in the table are read when a skill or a gate fires and not at session
start. That is a membership rule the frame has never had, and it is parked as a
candidate row rather than settled here, because settling it is doctrine revision
and not a table row.
(4) **Three surfaces are out of scope, each for its own reason.**
`cairn/PROFILE.md` reaches a session as its profile NAME only; the seven slots
the rulebook governs are read when a skill fires, so a row for it would decide
the membership question part 3 parks. The hook's `PREAMBLE` is plugin source
rather than a repo record — a fixed string no repo writes to, so it has no
inflow to test and cannot grow with use. Per-user memory is not a repo file and
never holds project state ("Tracking files outrank memory", the GP4 intake
gate), so no repo's frame can bound it.

**Consequences:** Annotates D-060 (its table goes from five rows to six) and
D-063 (whose row is the one the new boundary statement contrasts against: a
milestone file's cap-exempt sections stay governed by a read-bound, where
`CLAUDE.md`'s remainder is governed by nothing cairn owns). The statement claims
no uniqueness for that split — an always-read unit and a governed unit that
differ is a shape both surfaces carry. No IP touched; GP1 worked under, wording
unchanged. D-018 and D-009 are cited, not narrowed: neither the cap's scope nor
the router's content changes. Delivered by M126, guarded by
`skills/tests/test_always_read_frame.py` and mutation-registered. If a surface
ever arrives that the sweep cannot classify without a membership rule, that is
the parked candidate promoting, and this is the entry it annotates.

### D-095 (2026-07-31): Guard-doctrine §8 is retired whole at user mandate — no certification step, no rounds, no replacement instrument — supersedes the operative clauses of D-069, D-070, D-080, D-082, D-083, D-085, D-088 and D-091, re-scopes D-079's clauses 2–3 to the surviving reader, and narrows D-067 to the criteria audit alone; a logged deviation from D-090's Untouched clause (M127)

**Context:** The user mandated retirement on 2026-07-31 after an evidence
review of §8's measured yield. What the rounds after the first distinctively
produced was record-accuracy correction about the certification's own records
— the chains D-084→D-086, D-088→D-089 and D-091→D-092→D-093, six per-claim
correction entries among the eleven D-083–D-093 headings of this file —
while every ≥80-scored real defect of the same era was found by an instrument
this entry keeps: M120's three asserts that survived inverting their own rule
(§1 inversion had not been run; review scores topping at 92/88/87, archive
`M120-opus5-guide-adoptions.md`), M123's A5 (80, archive
`M123-section8-convergence-rebuild.md`), and M124's F1/F2/F12 (92/85/88,
archive `M124-section-consistency-ledger.md`) — that is, inversion, the
mutation harness, and the three-lens review fan-out. The cost side: M127's
goal records the loop as the measured majority of this repo's session cost,
and M126 ran a multi-round certification the day after M125's stop rule
shipped (460 turns, 19 agents — the figures as recorded in the M127
plan-gate work-log line of 2026-07-31). The plan first re-cut §8 to a single
pass; a second gate round chose full retirement because §8's distinctive
yield was record-accuracy-class while its cost was the dominant burn.

**Decision, part 1 — the step retires whole, with no replacement.** §8 is
removed from `guard-doctrine.md`; §9 keeps its number and heading (retired
numbers are never reused). The `/milestone-implement` completion clause that
fired it and the rulebook's fresh-reader-loop sentence are removed. Guard
verification remains what it already was beside §8: §1 inversion, the
mutation harness, the §7 sweeps, AC fencing, and `/milestone-review`'s
three-lens fan-out with its scorer. No absence guard pins §8's removal — an
absence guard would be new apparatus at D-090's door — so re-adding a §8
would ship green: a recorded, accepted exposure. The M124 ledger machinery
(`section_ledger.py`, its guard, both committed ledgers) is deleted whole,
restorable from git: with §8 gone its only committed subject is gone, and a
guard instrument testing only itself is the shape D-057/D-090 close doors
on.

**Decision, part 2 — the deviation, under IP2.** D-090's Untouched clause
names §8's falsifier clauses as the measured retirement path. Clause (iii)'s
own named remedy — "the step retires whole" — is executed here by user
mandate ahead of its three-milestone window, as D-091 part 4 promoted a
candidate row ahead of its stated condition: a deliberate deviation,
surfaced rather than silently overridden. D-085's Consequences prescribe
what a clause-(iii) retirement edit should do — prune the convergence
apparatus together with the rounds it governs (RR10 rec 8) — and this
retirement follows that prescription.

**Decision, part 3 — standing rejections superseded, not ignored.** D-085
records RR10's verdict (e) (keep §8) and its part-4 re-affirmation of RR09
recs 8–9 (neither revert nor retire). Those rejections rested on round-1
yield as measured in the rebuild's first days; the record above is evidence
they did not have. Both are superseded by this entry — the standing-rejection
discipline's supersede-don't-ignore route, taken on new evidence.

**Decision, part 4 — the per-entry supersessions.** D-067 is narrowed to its
first instrument: the criteria audit at the plan and ingest gates stands
unchanged; everything in D-067 adopting or governing description-layer
certification is superseded. D-069 and D-070 drew the certified scope of
certification rounds; with no rounds convened anywhere, their operative
clauses govern nothing and are superseded (the entries stand as history,
IP4). D-079's surviving clauses 2–3 are re-scoped from D-067's two readers
to the one that survives: clause 2's record rule continues unchanged for the
criteria audit, and clause 3's both-classes rule keeps both classes in the
rulebook but loses its fresh-reader-loop bound, whose cited instrument no
longer exists. D-080's and D-082's operative residue — the banked §8 rebuild
and the restored round-count falsifier — was consumed by D-083's rebuild and
closes with it. D-083 parts 1–4 (keep-the-step, the yield falsifier, the two
narrowings of the zero-unresolved bar, the D-069/D-070 annotation) are
superseded whole; its part-5 correction of D-081 stands. D-085 parts 1–3
(the round-count falsifier's independent defect, clause (iii), the relocated
derivations) are superseded as governing text and stand as the record of
what §8's clauses counted. D-088's routing enumeration described shipped §8
and now describes nothing. D-091 parts 1–2 (the shape-repeat stop and the
clause-(i) gloss) are superseded; **part 3 — guard-doctrine §6's
recorded-counts rule — survives in full**, since it binds records rather
than certifications; part 4 stands as history.

**Decision, part 5 — the candidate rows, so D-090's parking references
resolve.** The mixed-round-precedence, falsifier-state-disclosure and
audit-over-falsifiers rows are dropped: each is about the conduct of rounds
that no longer exist, and the latter two are the rows D-090 parks by name —
their disposal is recorded here, where D-090's references now resolve. The
polarity/vocabulary row is dropped and the ledger-rollout row is restated to
name git as the deleted mechanism's home, both being bound to the M124
ledger. The RR11 row is re-cut to BC5 alone, BC6's subject — §8's
shape-repeat remedy clause — being retired.

**Consequences:** A guard-authoring milestone now goes to review on the
suites, the harness, the sweeps and the fan-out alone. If a claim-accuracy
defect — a false record claim about a guard — reaches main undetected by the
review fan-out, that is this retirement's falsifier and this is the entry to
supersede.

### D-096 (2026-07-31): Five claims in D-095 are corrected in one batched entry — the correction chains, the rounds-after-first attribution, the A5 score, the instrument credit, and the absence-guard exposure — supersedes those clauses; D-095's decision and every other claim in it stand (M127 review)

**Context:** M127's three-lens review fan-out reported record-accuracy
defects in D-095, and its scorer confirmed five at 82–85 against the archives
and the diff. IP4 forbids repairing them in place; they are corrected here in
one batched entry rather than one entry per claim — the shape the ROADMAP's
correction-batching candidate row records, applied at its first occasion
(that row stays parked; one batched entry is its prescribed form, not its
promotion trigger).

**Corrections.**

1. *(F3, 82; F4, 72)* "the chains D-084→D-086, D-088→D-089 and
   D-091→D-092→D-093" — D-086 corrects D-085, not D-084 (the misattribution
   D-089 was written to fix, reproduced here), and D-092/D-093 are parallel
   corrections of D-091 (D-093 also correcting D-090), not a three-link
   chain. Corrected: D-084 and D-086 correct D-083 and D-085 respectively;
   D-089 corrects D-088; D-092 and D-093 each correct D-091, D-093 also
   D-090. The six-of-eleven count stands.
2. *(F5, 84)* "What the rounds after the first distinctively produced" — the
   cited entries' own tags place D-084, D-089 and D-092 at round 1; only
   D-086 (round 3) and D-093 (round 2) are later-round products. Corrected:
   certification rounds at every position produced record-accuracy
   correction as their dominant recorded output; the retirement decision is
   unchanged by the corrected attribution.
3. *(F15, 82)* "M123's A5 (80, …)" — the archive records "1 ≥80 (A5 …)", a
   threshold, not a score. Corrected to: A5, M123's one finding at or above
   80.
4. *(F16, 83)* "found by … inversion, the mutation harness, and the
   three-lens review fan-out" — all three cited cases are review-fan-out
   findings (M120's are the fan-out reporting asserts that survived
   inversion of their own rule, §1 inversion not having been run); the
   harness found none of the cited set. Corrected credit: the three-lens
   review fan-out, in M120's case applying §1's inversion protocol.
5. *(F2, 85)* "re-adding a §8 would ship green" (also the milestone Scope's
   wording) — overbroad: the kept-and-updated numbering guard asserts the
   exact gapped heading list, so re-adding a numbered `## 8.` heading reds
   the suite. What ships green is §8's content under any other heading — the
   exposure stands, narrower than recorded. No *dedicated* absence guard was
   added, which is what the Scope clause decided and D-090's door required.
6. *(minor, F9, 63)* part 1's "both committed ledgers" — one section ledger
   was committed (`guard-doctrine-8.txt`); the other two deleted fixture
   files were the extractor's contract. §9's copy of the phrase is current
   knowledge and was corrected in place; this clause corrects the record's.

**Consequences:** D-095's decision and every other claim in it stand,
including every per-entry supersession. The batched form is deliberate: the
per-claim correction cascade was the §8-era behavior D-095 retires, and one
entry per claim would reproduce it at the retirement's own doorstep.

### D-097 (2026-08-01): Amendment returns are counted on their own track with a second-occurrence stop — narrows D-064's counting clause; the defect-return count and both triggers stand (M130)

**Context:** intraclass M100 ran three full review returns on one milestone,
each pass falsifying the previous pass's repair of an acceptance criterion no
stated procedure could check ("messages assert nothing false about the user's
data"). D-064's counting clause reads every return into one per-milestone
count, so a return whose only fault is an unbounded promise burns the same
strike as an implementation defect, and trigger (a) can force a re-plan of
sound work. M130 ships the distinction: a finding that falsifies a criterion
only outside the domain of the procedure it names is evidence about the
criterion, not the work.

**Decision:** `/milestone-review` routes that case to the gated
criterion-amendment protocol as an "amendment return": the amendment is the
only work convened, its work-log line carries a fixed shape (`amendment
return: AC<N> — "<amended clause, verbatim>"`), and these lines are counted
per milestone on their own track — never reset by a re-cut, and never added
to the defect-return count D-064's triggers read. The track has its own stop:
a second amendment return naming the same AC<N> on one milestone convenes no
further round and goes to the user. Narrowed, not superseded: D-064's
per-milestone-never-per-cut counting, both triggers, and their remedies stand
for defect returns.

**Consequences:** the thrash counter measures implementation thrash only;
promise-wording thrash has its own, tighter stop (one repeat, not two). The
positional id plus the verbatim clause is what makes "the same criterion"
decidable after renumbering or a re-cut. If an amendment-return loop ever
survives this stop — rewording churning across different AC ids on one
milestone — this is the entry to supersede. Delivered by M130 beside the
return floor (its ≥80/≥90 bands), which D-064 never governed.

### D-098 (2026-08-02): A downstream repo's surfacing of a defect in cairn's shipped rules is hosted by a cairn milestone — annotates D-090's within-the-surfacing-milestone clause, whose prescribed host does not exist across repos

**Context:** intraclass M102's AC2 promised that no command in a committed
ledger reads git history, naming "an enumerated set of history-dependent
forms". It passed cairn's plan gate on 2026-08-02 with M130's bounded-promise
rule live, because that rule's question is whether a criterion names a
procedure enumerating its domain and an enumerated set reads as a yes — while
the set enumerated command spellings its author recalled, not the domain the
promise quantifies over. Three review returns followed, each defeated by a
genuinely new counterexample: ref spellings past a blacklist, a flag-value
versus `--` ordering bug past a positive rule over the revision slot, and
`awk 'BEGIN{ "git rev-list …" | getline x }'` past a rule closing the whole
git-parsing family, awk being no git command at all. M102 is parked `blocked`.
cairn's own M114 consumed three returns on the identical shape and banked the
lesson in a ROADMAP candidate row; `guard-doctrine.md` §6 and §9 both state
the stronger test, but that module is read only when authoring a guard, so a
plan gate writing a criterion never reaches it and meets only
`/milestone-plan`'s weaker copy.

**Decision:** D-090's trigger clause is satisfied, not superseded — the defect
is in shipped skill behavior, what `/milestone-plan` does for its user, and it
is measured in a user repo at a cost of three returns and a parked milestone.
What this entry annotates is D-090's remedy clause, "A defect in doctrine
prose, in records, or in the apparatus's own coverage is fixed as ordinary work
within the milestone that surfaces it, never promoted into its own apparatus
milestone." Where the surfacing milestone lives in another repo, that host does
not exist: a downstream milestone cannot edit cairn's shipped prose, and the
plugin is the shared artifact by GP4. So a cross-repo surfacing is hosted by a
cairn milestone of its own, and the clause binds unchanged within a repo. The
door's own bar is unrelaxed — the trigger stays a shipped-behavior defect, and
a defect in cairn's records or in its apparatus's own coverage still gets no
milestone whatever repo notices it.

**Consequences:** M132 is planned under this reading. A downstream repo
carrying an unrepairable-in-place defect against the plugin now has a stated
route rather than a choice between editing another repo's records and dropping
the finding. If a cross-repo surfacing ever proves fixable inside the
surfacing repo's own milestone — the falsifier — this is the entry to
supersede.

### D-099 (2026-08-08): The recorded-counts rule relocates to tracking-rules as the derived-figures rule — widened to derived figures across the derived-claims domain and strengthened by the pin requirement — narrowly supersedes D-091 part 3's placement clause; D-091's decision otherwise stands (M137)

**Context:** The 2026-08-08 effort audit
(`cairn/references/effort-experiment-notes.md`) classified the actioned ≥80
findings across M113–M136's reviews and found the dominant class to be record
defects — stale or false hand-written counts and evidence claims rather than
code — including M134's D14/88 stale work-log count and M135's two record
defects that forced a gated amendment. The mechanism: the rulebook demands
quantified evidence, authors hand-write derived values, and the next edit
strands them. D-091 part 3 already governed counts in milestone records, but
a count carrying its procedure still goes stale when the corpus moves, and
its home in §6 is read only at guard-authoring moments while records are
written everywhere.

**Decision:** The operative rule now lives in `tracking-rules.md`'s
"Universal tracking rules" as the derived-figures rule: a derived count or
figure — in tracking records, code comments, docstrings, changelog entries,
or docs, the derived-claims rule's domain — is written pinned (beside the
procedure that produced it and the commit or dated artifact it was measured
at, a dated observation) or procedural (replaced by its derivation, no
figure stated), never free-standing. This narrowly supersedes D-091 part 3's
placement clause: §6 keeps a deference headline, the verbatim-reproducible
grade a milestone-record pin owes, and the M124 story with its citation.
D-091's decision otherwise stands — the stop rule, the gloss supersession,
and the logged deviation are untouched. Rejected at the plan gate:
annotation-with-overlap (two live statements of one rule is the drift class
this rule targets) and no-D-entry (DECISIONS would point at prose the
shipped bytes contradict).

**Consequences:** No checker enforces the rule — the validator alternative
was declined at the candidate row (delete-over-govern; a validator reaches
machine-derivable figures only). If a case D-091's original §6 scope
governed proves ungoverned by the widened rule, this is the entry to
supersede.

### D-100 (2026-08-08): Two claims in D-099 are corrected — the "otherwise stands" enumeration and the classification's attribution — supersedes those clauses; D-099's decision and its other content stand (M137 review)

**Context:** M137's review fan-out (diff-bug lens, findings F1 and F3, scored
85 each) returned two record defects in D-099, appended hours earlier on the
same branch. IP4 forbids repairing them in place; this entry supersedes each
narrowly — the D-092/D-096 batched shape.

**Correction 1 — the "otherwise stands" enumeration.** D-099 closes
"D-091's decision otherwise stands — the stop rule, the gloss supersession,
and the logged deviation are untouched." Untouched by D-099, true; standing,
false for two of the three: D-095 had already superseded D-091 parts 1–2
(the shape-repeat stop and the clause-(i) gloss) when it retired §8 whole.
Narrowed to: D-099 touches nothing in D-091 beyond part 3's placement
clause; what else stands is what D-095 left standing — part 3 in full, and
part 4's logged deviation.

**Correction 2 — the classification's attribution.** D-099's Context
attributes the finding classification to
`cairn/references/effort-experiment-notes.md`. That page carries the effort
experiment's cohorts, cost tables, and re-measurement procedure — not the
per-finding classification, which was performed in the 2026-08-08
effort-audit conversation and recorded in the candidate row this milestone
absorbed (its text at commit `08bbb07`, `cairn/ROADMAP.md`), whose own
wording is "roughly half are record defects". The page is the audit's
context; the row is the classification's record.

**Consequences:** D-099's decision — the relocation, the widening, the pin
requirement, the narrow supersession of the placement clause — stands as
decided. What changes is only the two claims named above.

### D-101 (2026-08-13): A return whose only repair widens an author-recalled enumeration is an amendment return, counted on that track — annotates D-097's amendment-return track and leaves D-064's triggers intact; satisfies D-090's trigger under D-098's cross-repo host reading (M139)

**Context:** intraclass M117's AC2 consumed four defect returns. Returns #1–#3
each answered a counterexample with a wider matcher — a sentence filter keyed
on one token, figure shapes outside the pinned two, a greedy table strip
erasing 96% of a surface — and the narrowing to declared classes arrived only
with the 2026-08-09 re-cut; return #4 then landed inside the declared domain,
which is the narrowed promise working as intended. The repair already existed:
`/milestone-plan` step 4's bounded-promise rule states that a counterexample
defeating an author-recalled enumeration is not answered by a wider one (M132,
D-098). Nothing at the return surface reached it, and the geometry is why.
D-097's amendment return keys on a criterion falsified *only outside* the
domain of the procedure it names, while this failure lands *inside* the domain
the promise quantifies over — the named procedure enumerates a proxy for that
domain — so the case read as an ordinary defect return under the return floor
and its repair read as "widen the matcher". Reaching the narrowing repair
therefore cost a routing through `/milestone-plan` and a full re-cut.

**Decision:** `/milestone-review` gains the widening test — a finding
demonstrating an acceptance criterion failing inside the domain its promise
quantifies over is an amendment return rather than a defect return when the
**only** repair available to it widens an enumeration whose membership is fixed
by author recall rather than decided by a procedure over that domain. "Only" is
load-bearing: without it every defect return for which some widening repair
exists lands on the amendment track and its tighter stop. The two clauses it
collides with are amended to name it as their explicit carve-out — the return
floor's inside-the-domain limb, and the amendment return's "only outside". Such
a return counts on D-097's existing amendment-return track under its
second-occurrence stop and never increments the defect-return count D-064's
triggers read; a third counter was weighed at the M139 plan gate and rejected as
machinery a two-track surface does not yet need. `/milestone-implement` step 6
states the repair direction: the amendment takes the narrowing repair step 4
states, and a wider enumeration is not an admissible amendment. Both surfaces
cite step 4 rather than restating it, so the rule keeps one home.

**Consequences:** on the case that motivated this, the stop fires after two
rounds rather than four. D-097 is annotated, not superseded — its track, its
fixed work-log shape and its second-occurrence stop are reused unchanged, and
what widens is only what routes onto them. D-064's triggers and its
per-milestone counting are untouched; the defect-return count simply stops
absorbing this class. D-090's door is cleared by its own trigger clause rather
than superseded: the defect is in shipped skill behavior, measured in a user
repo at a cost of four returns, and D-098 hosts a cross-repo surfacing in a
cairn milestone. Two falsifiers, with different owners. If a milestone churns
amendment returns across different AC ids under this classification, that is the
loop D-097 names as its own exit and D-097 is the entry to supersede. If a
return is reclassified here whose repair genuinely was a widening that a stated
procedure settles, this entry is the one to supersede.

### D-102 (2026-08-13): D-101's "two clauses" is corrected to the three limbs the shipped file carves, and D-101's in-place edit is recorded as an IP4 violation, not repaired — supersedes that clause; D-101's decision and its other content stand (M139 review pass 3)

**Context:** D-101 records that the widening test's colliding clauses "are
amended to name it as their explicit carve-out — the return floor's
inside-the-domain limb, and the amendment return's 'only outside'". Two limbs.
The shipped file carves three: M139's own review pass 1 found the return floor's
`≥90` deliverables limb uncarved, so a finding could satisfy the floor and the
widening test at once with no tiebreak, and the repair added a third carve-out.
D-101 was appended before that repair and was never true of what ships.

**Decision, part 1 — the correction.** The clause is superseded here: **three**
limbs name the widening test as their explicit carve-out — the return floor's
inside-the-domain limb, that floor's `≥90` deliverables limb, and the amendment
return's "only outside". D-101's decision, its counting disposition, its
cross-entry claims about D-064, D-090, D-097 and D-098, and its two falsifiers
all stand as appended.

**Decision, part 2 — the violation, recorded under IP2 rather than hidden.**
M139's review pass 2 scored this misdescription at 85 and the milestone repaired
it by **editing D-101's sentence in place**, on the reasoning that an unmerged
D-entry is branch-added prose rather than history. That reasoning is wrong and
the edit was an IP4 violation. D-045 classifies `DECISIONS.md` as history,
"never edited: supersede, never rewrite"; IP4 states the same; `DECISIONS.md`'s
own header states it a third time. `guard-doctrine.md`'s delete-first remedy for
a false claim in branch-added prose is scoped to the branch's own skill prose and
is immediately followed by the unqualified reaffirmation that IP4 history is
superseded, never edited. No clause anywhere carves out an unmerged or
same-branch D-entry. The in-place edit was reverted at pass 3 — D-101 carries its
originally appended bytes — and this entry is the supersession that should have
been written instead. Two independent review lenses reached this reading before
the scorer confirmed it at 92.

**Consequences:** the precedent this closes is the dangerous one — that merge
status decides whether a record is history. It does not: a D-entry is history
from the moment it is appended, and an in-flight decision under active review is
exactly where a false claim is most likely, so it is exactly where the
append-only guarantee is worth most. If a case ever arises where superseding an
unmerged entry is genuinely worse than editing it, this is the entry to
supersede.

### D-103 (2026-08-14): AC4's instrument is normalized whole-slice equality against verbatim in-test fixtures, and M139 splits — the doctrine ships on its verified criteria while a child milestone carries RR12's binding criteria — annotates D-101; corpus-wide remediation is refused at D-090's unsatisfied trigger (RR12, M139)

**Context:** M139's AC4 failed three review passes, each by one shape — a guard
anchor whose reach differs from the extent of the rule it pins. RR12's
diagnosis: the failures are two conditions of a single invariant violated
alternately — totality (the pinned extent equals the slice, leaving no unpinned
complement) and granularity (the slice equals one rule) — and any
fragment-anchor family short of whole-slice equality leaves a free complement
whose text can invert the rule with the suite green; RR12 re-reproduced pass
3's R1 independently, the full suite OK at 784. A regex family delivers AC4's
property only in the degenerate limit where it collapses to one whole-slice
equality check per rule, at which point it has stopped being an anchor family.

**Decision:** the instrument for AC4-strength coverage is normalized
whole-slice equality — per rule slice, one test method holding one
`assertEqual(normalize(<slice>), <fixture>)` against a verbatim in-test copy of
the rule's full text, replacing the per-fragment regexes, keeping the
marker-uniqueness asserts, registered per slice in the mutation harness. And
M139 splits, per the thrash rule's own remedy: AC4 is pruned through the gated
amendment protocol, the two doctrine rules ship on AC1–AC3/AC5/AC6 (each
verified across three passes), and a child milestone carries RR12's BC1–BC7
verbatim as its acceptance floor with `Driving RR: RR12`. Rejected with RR12's
reasons: a content hash (coverage-identical but opaque at discharge — the
update diff shows one constant replacing another, making M124's measured
failure mode the default), a markdown/AST parse (solves the already-solved
boundary half, not the reference half, at a non-stdlib or hand-rolled-splitter
cost), and a standing probe generator (negation is not mechanically
generatable, and a standing generation stage is the certification shape D-095
retired at D-090's door).

**Consequences:** until the child lands, the two shipped rules carry a recorded
exposure — an edit inserting between pinned fragments or stranding a slice tail
would run green; bounded by stable user-approved doctrine text and PR review of
any skill diff, and precedented as a recorded exposure by D-095's own §8-re-add
clause. Thereafter every legitimate edit to an equality-guarded rule reds the
suite and updates the fixture in the same commit — a deliberate two-site act,
the correct default for the return-classification doctrine the thrash counter
itself reads. Corpus-wide remediation is refused: every recorded instance of
the anchor-reach class was produced by a probe or review lens examining the
apparatus's own coverage, which D-090 fixes as ordinary work where it surfaces;
the licensing trigger would be a shipped-behavior defect misrouting a skill in
a user repo, and none is on record. If such a defect appears, D-090 names
itself as the entry to supersede and RR12 §§1–2 is its evidence file. If a
fixture is ever updated without its diff being read and a doctrine change ships
unnoticed — the instrument's own stated residual — this entry is the one to
supersede.

### D-104 (2026-08-14): The annotation D-103's heading asserts on D-101 is drawn here — D-103's instrument and split govern the guarding and completion of the rule D-101 shipped, touching nothing in D-101's classification — annotates D-103; D-103's decision and every other claim in it stand (M139 review pass 4)

**Context:** D-103's heading reads "annotates D-101", but its body names D-101
nowhere, so the asserted relationship has no substantiating clause (M139
pass-4 finding R4-09, scored 82). Under IP4 the entry is history and is not
edited; the relationship is drawn by this entry instead.

**Decision:** the annotation is this: D-103 decides the *instrument* for
AC4-strength coverage of the doctrine D-101 shipped — the widening test and
its three carve-outs — and the split that completes that coverage in a child
milestone; it changes nothing in D-101's classification rule, its counting
disposition, or its falsifiers, which stand as appended (and as corrected by
D-102). D-103's decision and every other claim in it stand.

### D-105 (2026-08-15): The thrash threshold's remedy is descope-or-park; a same-objective re-cut is present, never recommended — narrowly supersedes D-064's trigger-(a) remedy clause; hosted per D-098 (M143)

**Context:** D-064's trigger (a) prescribed "recommend re-plan or split via
`/milestone-plan`" at the third defect return. Measured downstream, that remedy
bought returns rather than fixes. intraclass M120, derived from the return and
thrash lines of its milestone work log read at intraclass commit `1e95baf`
(branch `m120-checkpoint-staleness-guard`): four defect returns (returns 1–3
whole, return 4's F1 leg) and one amendment return (return 4's F4 leg,
recorded there under the widening test) — so the threshold was genuinely
reached at return 3 on the defect track alone, not inflated by amendment
returns; the prescribed re-cut was then spent, was followed by a fourth defect
return, and the milestone was parked `blocked` at the maintainer's decision
(2026-08-15) — the exit this entry promotes to the recommended default.
circumplex carries the same shape at milestone granularity: fifteen
consecutive norms milestones, M72–M86 — the fourteen files `grep norms`
matches over `cairn/milestones/archive/` at circumplex commit `b343054f`, plus
M86 in flight — each hardening or repairing the checker the previous one
shipped. The defect is in shipped skill behavior — what `/milestone-review`
recommends at its threshold — measured in user repos, and D-098 hosts the
cross-repo surfacing here.

**Decision:** At trigger (a)'s threshold the recommended option is
descope-or-park: descope — narrow the milestone to its already-verified
criteria via the gated amendment protocol (`/milestone-implement` step 6), the
unverified remainder exiting to candidate rows or a split milestone, then
re-review the narrowed set — or park as `blocked` with the blocker named. A
same-objective re-cut via `/milestone-plan` and dropping at the user's
explicit decision stay present options; the re-cut is never the recommended
one. The both-triggers composition paragraph composes the chip from this menu
with (b)'s diagnosis and escalation offer carried in; once a re-plan or split
is spent, the re-cut leaves the menu entirely. Narrowly superseded: D-064's
trigger-(a) remedy clause alone — its per-milestone counting, both triggers,
trigger (b)'s remedy, and the amendment-return tracks (D-097, D-101) stand.

**Consequences:** the thrash block gains a whole-slice equality fixture beside
its per-property pins (D-103's instrument). If a descoped remainder repeatedly
re-enters as its own thrashing milestone — the plan gate's recorded falsifier
— this is the entry to supersede; a milestone genuinely mis-sized rather than
mis-approached still reaches a re-cut, present on the menu at every firing.

### D-106 (2026-08-15): Two D-105-adjacent gaps are fixed at the merge gate — the "at every firing" Consequences clause is narrowed, and the composition paragraph states where (b)'s remedy lives — supersedes that clause; D-105's decision and its other content stand (M143 review)

**Context:** M143's review fan-out surfaced two sub-threshold findings the
maintainer directed fixed at the merge gate rather than accepted as logged.
F1 (scored 60): D-105's Consequences assert a genuinely mis-sized milestone
"still reaches a re-cut, present on the menu at every firing," which D-105's
own Decision falsifies for the already-spent state, where the re-cut has left
the menu. F2 (scored 60): the composition paragraph carried (b)'s diagnosis
and escalation offer into the composed chip but not (b)'s remedy —
reconsidering the recorded alternative — leaving that remedy to live,
unnamed, inside the never-recommended re-cut option.

**Decision:** (1) D-105's Consequences claim is narrowed: a genuinely
mis-sized milestone still reaches a re-cut at every firing *before a re-plan
or split is spent*; after one is spent the exits are descope, park,
escalation, and drop, exactly as the Decision states. (2) The composition
paragraph now says it in so many words: "While the recorded alternative is
unspent, (b)'s remedy — reconsidering it — rides the present,
never-recommended re-cut option; after that, escalation is what remains of
(b)." The whole-slice fixture, a new per-property pin, and a registry entry
are re-anchored to the amended bytes in the same commit.

**Consequences:** D-105's falsifier — a descoped remainder repeatedly
re-entering as its own thrashing milestone — and every other claim in it
stand.

### D-107 (2026-08-15): The plan gate scales criteria rigor to the deliverable's surface tier, and a checker-regress hit poses deletion as the recommended option — annotates D-090, whose Untouched clause stands; hosted per D-098 (M142)

**Context:** Two downstream repos measured the failure this entry closes.
intraclass M120 consumed four review returns in one day hardening an in-repo
checker; circumplex M72–M86 ran a fifteen-milestone arc extending checkers
over internal artifacts. In both, verification effort grew without limit on
internal tooling because `/milestone-plan` as shipped classifies no
deliverable and holds every criterion to one rigor standard. D-090 closed
cairn's own verification-apparatus program at the door; its trigger clause
requires a shipped-behavior defect, and that trigger is satisfied here — the
defect is in what `/milestone-plan` does for its users, measured in the
downstream repos: the plan gate as shipped accepts internal-tier scopes whose
criteria demand unbounded specification. The cross-repo host is a cairn
milestone per D-098.

**Decision:** M142 ships four rules in `/milestone-plan`. Step 2 classifies
every milestone's deliverable as user-facing or internal — internal means no
external consumer of the repo relies on it; unclear or spanning deliverables
are user-facing — and records the tier in the milestone file. An
internal-tier criterion's promise quantifies over a domain its named
procedure enumerates directly — never an exemption registry, a per-rendering
enumeration, or a demonstration family spanning process or environment
boundaries — and a draft needing those is repaired by narrowing or
descoping, never by widening; the standard governs promises, never a guard's
construction. The step-3 criteria audit asks a proportionality question of
each criterion against the declared tier. The step-2 collision check names
the checker-regress shape — a scope extending or hardening a checker an
earlier milestone of the same repo shipped, where the checker verifies
repo-internal artifacts — and on a hit poses simplifying or deleting the
checker as the recommended option, with hardening present but
non-recommended; a repair leaving the checker's promise unchanged stays
outside the shape (D-090's Untouched clause, intact), one widening the
promise is the shape however framed. This annotates D-090 — the door and its
Untouched clause stand unchanged; the regress question is a plan-gate
counterpart on the demand side, a recommendation and never a hard door,
because a hard door would narrow the Untouched clause and add supersede
ceremony to legitimate hardenings.

**Consequences:** Falsifiers, each recorded at the plan gate: the regress
recommendation is falsified by a tracked repo accepting the recommended
deletion where the checker's absence then admits a user-facing defect it
would have caught; the domain-bounded standard is falsified by an
internal-tier criterion within the standard still consuming three defect
returns. Either firing supersedes the corresponding rule here.

### D-108 (2026-08-16): D-090's door widens to new conduct rules about verification or records — removal-shaped milestones are outside the door; supersedes D-090's Decision subject clause by extension, trigger clause retained; M144 excepted by name (RR13, M144)

**Context:** RR13 (ingested 2026-08-16) measured the post-D-090 recurrence:
with new apparatus barred, the generator survived as conduct rules —
M130–M143 shipped a new rule about verification or records roughly weekly,
each carrying guard surface and each reviewed by the machinery it modified,
and the correction cascade D-090's Context predicted recurred at M139 (the
ROADMAP batching row: "arguably fired at M139"). D-090's Context named the
signature: "the anti-cost program maximizes the cost it exists to reduce."
RR13 Q1 identifies one generator behind both forms — code-grade verification
discipline applied to artifacts with no oracle — and rec 2 (apply) grounds
this widening.

**Decision:** D-090's Decision subject clause — "No new milestone is planned
whose deliverable is verification apparatus" — is superseded by extension: no
new milestone is planned whose deliverable is a new conduct rule about
verification or records (how records are authored, measured, or audited; how
verification is conducted), on the same terms as apparatus. D-090's trigger
clause is retained unchanged and reads, verbatim: "unless its trigger is a
defect in shipped behavior: what the plugin's skills, hooks, and scripts do
for their users." Carve-out: a milestone whose deliverable removes or narrows
a conduct rule about verification or records is outside this door. The
apparatus-side precedent is D-095, which executed §8's retirement as a
logged deviation from D-090's Untouched clause at user mandate — that clause
itself reached only §8's own falsifier path, so this carve-out converts what
D-095 did as a per-instance deviation into standing permission for
removal-shaped work, on RR13 rec 2's grounds; it does not claim D-090
already provided it. A firing of D-109's falsifier is a named exception to
this door: the superseding entry it convenes is in-scope work, not a barred
new conduct rule. M144 is excepted by name as the
widening's own act; the door binds every plan gate after it.

**Consequences:** The plan-time collision check surfaces this entry on any
scope shaped as a rule about verification or records. RR13 steps 2–3 proceed
under the carve-out with no further exceptions. If a shipped-behavior defect
class appears that a barred conduct rule would have prevented, this is the
entry to supersede.

### D-109 (2026-08-16): The prose-guard suite leaves every gate — skills/tests retained and hand-run, gating nothing; the probe's exit falsifier (RR13, M144)

**Context:** RR13 rec 1 (apply). Measured yield: RR10 §3's 11-of-13 and
M127's zero-operative-losses ledger measured the §8 certification apparatus,
retired at D-095 — cited as the prose-verification stratum's nearest
measured yield, not as `skills/tests`'s own record; that suite's own cost
record is the guard-craft mass RR13 Q3 inventories (the LESSONS
guard-authoring lines; the M117–M140 guard-fix milestones). Against it, the
hooks/scripts behavioral tests show no comparable thrash on the record
(RR13 Q3: "the pathology is confined to tests over markdown"). Nothing is
deleted, which is what keeps the probe reversible and its falsifier
decidable.

**Decision, part 1 — the ungating:** `cairn/PROFILE.md`'s `verify` slot
names `scripts/tests` and `hooks/tests` as the two gating suites;
`skills/tests` stays in the repo, runnable by hand, gating no commit, merge,
or check-off; a new rulebook or skill rule in this repo owes no prose guard
or mutation registration (plan gate 2026-08-16). M144's own AC4 evidence
run is the named exception — a one-time transitional check, not a gate.

**Decision, part 2 — the exit falsifier**, stated as the class of evidence
that would falsify the ungating: the gate re-arms if an unintended prose
regression reaches the default branch that the review fan-out missed and
that a guard under `skills/tests` reds on; decided by running `python3 -m
unittest discover -s skills/tests` against the merged default-branch tree.
Cadence: the suite is run once at each `/milestone-review` post-merge
hygiene pass and its red/green noted in the hygiene stamp; a red traced to
an intentional re-wording is noted as intentional and is not a firing, so a
falsifier-relevant red stays distinguishable. Firing does not re-arm the
gate of itself: it obliges a superseding entry deciding the re-armed form —
a named exception to D-108's door.

**Consequences:** If the falsifier fires, this is the entry to supersede —
the re-armed form and its scope are decided then, against the regression's
evidence, not pre-committed here. D-095's Consequences clause — "A
guard-authoring milestone now goes to review on the suites, the harness,
the sweeps and the fan-out alone" — is narrowed: the prose suite and the
mutation harness no longer gate; the sweeps and the fan-out stand.
