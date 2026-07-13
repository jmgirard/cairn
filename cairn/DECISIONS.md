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
