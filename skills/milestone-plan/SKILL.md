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
Chapter markers: mark a chapter at each phase transition (session start implicit).

## Session start

Read, in order: `cairn/ROADMAP.md`, any active milestone file,
`cairn/DECISIONS.md`, `cairn/LESSONS.md`. If an un-ingested RR exists in
`cairn/reviews/`, handle ingestion first (see `/milestone-brief`).
`cairn/DECISIONS.md` is read per the tracking-rules **bounded
`DECISIONS.md` read** — scan the `### D-` headings, never the whole file.
Read every matched entry whole before surfacing it, and back-reference it by
its own `D-0NN` id; the headings decide what to open, never what to report.

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
   **The acceptance criteria are drafted here to their final wording, not at
   step 4** — step 3's criteria audit reads the bytes step 4 will write, and an
   audit over a rougher draft certifies text that never ships.

   **Surface tier (mandatory).** Every plan classifies the milestone's
   deliverable as user-facing or internal, and records the tier and a
   one-clause reason in the milestone file's Goal or Scope prose.
   Internal means no external consumer of the repo relies on the
   deliverable — dev tooling, data-generation scripts, in-repo checkers
   over internal artifacts, tracking records; user-facing is everything
   else, including any deliverable whose tier is unclear or spans both.

   **Internal-tier criteria standard.** An internal-tier acceptance
   criterion's promise quantifies over a domain its named procedure
   enumerates directly — never an exemption registry, a per-rendering
   enumeration, or a demonstration family spanning process or
   environment boundaries. A draft needing those is repaired at this
   gate by narrowing the promise (step 4's bounded-promise rule) or by
   descoping, never by widening the specification. The standard governs
   a criterion's promise, never a guard's construction — a detector's
   per-rendering positive controls stay mandated by their own doctrine.

   **Exploring a source corpus.** A scope that points at a corpus of
   maybe-relevant sources on the `references/sources/` shelf is a supply-push
   case (tracking-rules "Exploring prospective sources"):
   investigation may triage them for prospective oracles or methods rather than dismissing them as uncited, emitting ROADMAP candidate rows for what it finds and a survey synthesis note only when the triage outlives this planning, never a per-source page.

   **Collision check (mandatory).** Sweep the ROADMAP (all statuses), the
   archive, and DECISIONS.md for overlap with what the user described.
   Sweep DECISIONS.md per the tracking-rules **bounded `DECISIONS.md` read**:
   scan the `### D-` headings, **read every matched entry whole before
   surfacing it**, and **back-reference each match by its own `D-0NN` id** so a
   later entry superseding it surfaces too.
   Quote a collision verbatim from the full entry, never from the heading.
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

   **Checker-regress shape.** The sweep also names this shape: a scope
   extending or hardening a checker that the ROADMAP or archive records
   an earlier milestone of the same repo shipping, where that checker
   verifies repo-internal artifacts. On such a hit the gate poses
   simplifying or deleting the checker as the recommended option and
   hardening it as a present, non-recommended alternative. A repair that
   leaves the checker's promise unchanged stays outside the shape
   (D-090's Untouched clause); one that widens the checker's promise is
   the regress shape however it is framed.

   **Harvest recent lessons (before the gate).** Review `cairn/LESSONS.md`
   (read at session start) and surface any lessons bearing on this scope —
   build quirks, testing tricks, gotchas that should shape the tasks,
   acceptance bar, or a gate question. Empty file → nothing to surface. This
   is intake, not obedience: a lesson informs the plan, it doesn't dictate it.

3. **Question gate** (one batched AskUserQuestion round, 2–5 questions, each
   with a recommendation): scope boundary, sequencing, acceptance bar, and
   any collision dispositions.
   Acceptance chips (tracking-rules): a question resting on a produced
   conclusion — subagent findings, a collision verdict — shows that
   conclusion's substance verbatim above the chip. Every proposed scope cut must state **where
   the remainder goes** — never "M12 covers A and B" alone, but "M12 covers
   A and B; C becomes M13 (planned now, depends on M12); D becomes a
   candidate row; E sounds unwanted — drop entirely?".

   **Criteria audit (runs before the questions are composed; scaled to
   stakes).** A plan author's own read of its own criteria is the check
   measured to fail — M114
   authored criteria that were unsatisfiable as written and one that mandated
   an IP4 violation, costing gated amendments and review returns, and each was
   discoverable here. The audit's mode follows the step-2 surface tier:
   a milestone whose declared tier is user-facing, or any of whose drafted
   criteria or tasks carries an RB-tripwire tag, gets the **full audit**; an
   internal-tier milestone gets the **reduced audit** (M145). Either way the
   step-2 criteria go to a fresh-context **[O]**
   reader that authored none of them. The full audit asks three mechanical
   questions of
   each: *what state of the world satisfies this exactly as written*,
   *does any IP or D-entry make that state unreachable*, and
   *does it make a universal claim over a domain no procedure it names enumerates*
   (the bounded-promise rule, step 4; M130). It reads the wording
   step 4 will write, never a paraphrase of it. The third question is asked of the
   domain the claim quantifies over, never of a proxy the named procedure
   happens to enumerate (M132).
   Where a criterion cites a mutation, inversion, or planted-defect
   verification, the full audit asks whether the probes vary every axis the
   verified domain is free in — form as well as location — or stand one
   exemplar in for the family.
   The audit — in both modes — also asks of each criterion whether its
   promise states a property of the milestone's deliverable or a
   property of an instrument that verifies it — a test harness, a
   floor, a plant matrix, a checker's own prose, a work-log recording
   act, a mandated evidence quotation, among others (D-118; record
   properties joined the genus by D-120). A criterion
   binding an instrument property is a finding, disposed at this gate
   like the audit's other findings: the instrument property moves to the
   tasks or the gate procedure, or the criterion narrows to the
   deliverable property it certifies. The question governs what a promise
   binds, never how a deliverable-bound promise is verified — it never
   relaxes the probe question above, in the full mode that asks it.
   Both modes ask a proportionality question of each criterion:
   is the promise's domain proportionate to the declared surface tier
   (the step-2 rule)? An internal-tier criterion outside the
   internal-tier criteria standard is a finding, disposed at this gate
   like the audit's other findings; the question governs promises and
   never relaxes the probe question above, in the mode that asks it.
   **The reduced audit asks only the bounded-promise, proportionality,
   and instrument questions** of each criterion — it omits the
   satisfiability, reachability, and probe questions — and keeps the
   disposal rule below in full.
   Dispose of what either mode returns at
   this gate, never silently: a finding with one clear right answer is fixed
   and the fix reported in chat, and a finding you could reasonably decide
   either way becomes one of this round's questions, within the three-marker
   cap. The instrument is a reader and never a check — satisfiability and
   IP-conflict are judgments about prose meaning, which D-059's retirement
   precedent says to route to the mechanism that works rather than mechanize.
   **The audit records one work-log line either way, naming the mode it ran
   in** — what it returned, or
   that it returned nothing — so an absent line means the reader did not run,
   never that it ran and was silent (M121). Three of the five milestones after
   this instrument was adopted carry no such line, and which of the two
   happened is no longer recoverable from the record.

   **Release-shaped tripwire.** Release timing is user-declared, never agent-proposed (tracking-rules; D-050) — so a release-framed scope stops here for an explicit window declaration.
   It fires when the scope in hand would ship a version: a release, a CRAN or
   registry submission, a "prepare/consolidate for vX.Y.Z". On a hit, the gate
   asks the user to declare the window in so many words, and
   the default answer is no — absent a declaration the work lands as a `candidate` row, never as a `planned` milestone, and never at `Priority: high`.
   A declared window is the user saying to queue this release now; the
   dependency list going green is not, since it says only that the bundle is
   complete.
   Two things the tripwire does not touch.
   Work *about* release tooling — a release-walk slot, release docs — is ordinary milestone work, not a release.
   And a milestone the user has already declared a window for plans normally.
   When a release milestone exists but its window is not open, its home is
   `blocked` — park it there rather than planning around it.

4. **Solidify autonomously** (no further questions). Create **one or more**
   milestone files from
   `${CLAUDE_PLUGIN_ROOT}/skills/shared/templates/milestone.md` — when the
   sizing tripwires fire, the answer is multiple milestones in one run, not
   shrink-to-fit and discard. For each file:
   - Acceptance criteria verifiable with evidence; never vibes. Criteria
     that cite a formula or reference value must name their source
     (`citekey (p. N)` — see the primary-sources rule). **Write the wording
     step 3's audit read**; a criterion the gate changed goes back through
     the audit's questions — in the mode step 3 assigns the milestone's
     tier — before it is written, and the change is reported.
   - **Bounded promises only (M130).** An acceptance criterion that makes a
     universal claim ("no X", "every Y", "nothing Z") names the procedure —
     a search, a sweep, or a test run — that enumerates its domain; where no
     stated procedure can enumerate the domain, the criterion instead
     claims what a procedure it names actually swept. A hand-list of sites is
     not a procedure — the list becomes the sweep and every site it omits
     ships stale (the M118 lesson).
     **The procedure must enumerate the domain the criterion's own universal
     quantifies over, not a proxy for it.** Naming a procedure is not passing
     this test: an enumeration whose membership is fixed by what the author
     recalled, rather than decided by a procedure over the domain, is a proxy
     however long its list — spellings, renderings, known cases and whole
     families among others, never only those. A counterexample defeating such
     an enumeration is therefore not answered by a wider one; the repair is to
     narrow the promise until a stated procedure settles it. intraclass M102's
     "no command reads git history", built as a set of refused command forms,
     took three returns beaten by a ref spelling, an argument-order bug, and
     then `awk`, which is no git command at all.
   - Acceptance criteria set the test scope for the milestone (see "What
     gets a test" in tracking-rules): name the behavior that must be tested.
   - `Out:` items name where the excluded work lives instead.
   - Tasks ≤ one working session each, ordered by dependency.
   - **Coverage map** (owner: plan): after the criteria and tasks are
     written, author the Coverage section — one line per acceptance
     criterion mapping it to the task(s) that satisfy it, by positional
     number (`AC1 → T1, T3`; AC/Task numbers run top-to-bottom in their
     sections). Every criterion maps to ≥1 task; a criterion no task
     satisfies is a planning gap — add the missing task or cut the
     criterion, never ship an unmapped criterion. Review reads this map to
     fence evidence.
   - **Principles touched** (header slot): fill it with the DESIGN.md
     `IPn`/`GPn` ids this milestone adds, changes, or works under — or `—`
     if none. It is the authoritative source `cairn_impact` and
     `cairn_validate` read for principle impact; an accurate slot beats an
     incidental `(IPn)` in prose (M17).
   - **Driving RR** (header slot): a milestone planned from an RR that
     carries Binding criteria sets the slot to `RR<NN>`, ingests each
     criterion verbatim into the AC block (the `binding criteria` check
     string-compares them; departures go in the shown "Deviations from
     RR<NN>" table), and copies the RR's numeric projections beside the
     criteria with their stated tolerances — an unstated tolerance is
     strict, so review's shortfall chip fires on any gap. Otherwise `—`.
   - **Record the alternative the gate rejected.** Wherever this plan settled
     which approach a criterion will be met by — at step 3's question gate or
     autonomously at step 2, since most approach choices are never posed as
     questions — append a work-log line naming the alternative rejected, why
     it lost, and the class of evidence that would falsify the choice — one
     line per approach choice the gate actually weighed. The work log is the
     home for the reason `/milestone-review`'s thrash rule already counts
     returns there — it is what a re-cut leaves standing — and trigger (b)
     reads the record from it. A plan that weighed
     no alternative writes no line: absence means none was weighed, and
     trigger (b)'s escalation offer is the correct reading of it.
   - Open questions that hit an RB tripwire (see tracking-rules) are
     tagged inline on the affected task or criterion with the canonical
     token — `(RB tripwire: no-oracle | irreversible-api | ip-touching)` —
     so implement inherits them.
   - Write only the plan-owned sections per the tracking-rules
     section-ownership table; leave the others to their owners.
   - **Draft against the cap, not against the gate.** The plan-owned body
     must land under `cairn_validate`'s 150-line cap; count while writing
     rather than discovering the overrun at gate time, when the only remedy
     left is compression.
   Deferred chunks not yet plannable get `candidate` ROADMAP rows, not files.

5. **Remainder ledger (conservation check).** Before committing, enumerate
   every distinct thing the user originally asked for and its disposition:
   in this milestone / planned as M<NN> / candidate row / dropped at the
   user's explicit request. Nothing may be silently absent. Deferral is
   NEVER recorded as a decision not to do something — D-entries are for
   genuine rejections with rationale; postponement lives in the ROADMAP.
   Include the ledger in the plan summary presented to the user.

6. **Commit atomically.** Durable-record preview first (tracking-rules):
   show each drafted durable text — the milestone files' plan-owned
   sections, any D-entry, new ROADMAP rows — verbatim in chat before the
   commit. Then update ROADMAP rows (`planned` / `candidate`) and
   commit files + rows together, directly to main, no branch, no PR
   (docs-only carve-out): `plan M<NN>[, M<NN>…]: <title>`; push. A session
   dying mid-plan must not leave a half-planned ghost.

7. **Routing chip (AskUserQuestion)**, composed from what was just planned
   (chip rules per tracking-rules) — e.g.:
   - **Start implementing M<NN>** (the proximal one) → `/milestone-implement`
     (recommended)
   - Plan another milestone → `/milestone-plan`
   - Stop here
