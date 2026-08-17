---
name: milestone-implement
description: Implement a planned milestone in a cairn repo on its own branch with tests-first tasks and checkpoint commits. Use when the user wants to start, resume, work on, or continue a milestone (e.g. "work on M07", "resume the milestone", "start implementing").
argument-hint: "<id>"
---

# /milestone-implement <id> — planned → review

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: git model, tracking-travels-with-code, delegation policy,
CI waiting rules).
Phase header: `# Milestone <NN>: <title>` → `## Implement`.
Chapter markers: mark a chapter at each phase transition (session start implicit).

## Session start

Read, in order: `cairn/ROADMAP.md`, the target milestone file,
`cairn/DECISIONS.md`. If an un-ingested RR exists for this milestone,
run ingestion first (see `/milestone-brief`).

## Workflow

1. Verify status is `planned` (fresh start) or `in-progress` / `blocked`
   with a resolved blocker (resume). Verify all `Depends on:` milestones are
   `done`, and that no OTHER milestone is `in-progress` (at most one, ever —
   if one exists, stop and route there or ask). Set `in-progress` in
   ROADMAP + header mirror.

2. **Branch.** Check `git status` first — a dirty tree with unrelated
   changes means ask the user; never sweep strangers into a checkpoint
   commit. First session: detect the default branch (tracking-rules git
   model: `git symbolic-ref --short refs/remotes/origin/HEAD`, strip
   `origin/`) and sync it with origin first — `git fetch`, pull (ff-only),
   and **push any unpushed local commits** — so the branch is cut from the
   pushed default branch and the PR diff will contain only milestone work;
   then `git checkout -b m<nn>-<slug>`; record the branch in the milestone
   header. Resume sessions: check out the
   existing branch; if the default branch has moved since the branch was cut
   (e.g., a hotfix merged), merge it into the branch and re-run the active
   profile's `verify` slot before continuing.

3. **Question gate:** surface the implementation choices the plan left open
   (API shape, naming, dependency picks — dependency changes always need a
   gate + D-entry) with recommendations. Skip only if nothing is genuinely
   open.
   Acceptance chips (tracking-rules): a question resting on a produced
   conclusion shows its substance verbatim above the chip. If the plan tags an item `(RB tripwire: <token>)` — or a new
   tripwire emerges mid-work (same three categories; see tracking-rules) —
   include an **Escalate via `/milestone-brief`** option on that question; the
   three tripwires are the must-offer cases, but escalation may also be offered
   for a genuinely hard question the session cannot confidently settle (D-062
   lowered this bar). Either way it stays gated per instance through
   `/milestone-brief` — D-004.

4. **Work tasks in order, autonomously.** For each task:
   - Tests first where feasible; numeric results per the oracle doctrine;
     language-specific test and error-condition idioms per the active
     profile's `test-doctrine` slot.
   - Run the active profile's `verify` slot (`cairn/PROFILE.md`; absent →
     infer per tracking-rules "Toolchain profiles") — its checks must be clean
     before the task is checked off.
   - Checkpoint-commit per task on the branch, **including** the milestone
     file update (checkbox + one work-log line) in the same commit.
     Prose the commit adds about an artifact's behavior follows the tracking-rules derived-claims rule: derived from the artifact, never composed.
     A claim resting on an observed failure follows the tracking-rules failure-identity rule: verified to be the failure the claim is about, never read off a bare error.
   - Stay within implement-owned sections per the tracking-rules
     section-ownership table; Goal, Scope, and Acceptance criteria change
     only via the amendment gate (step 6).
   - Durable-record preview (tracking-rules): a milestone-local Decisions
     entry or promoted D-entry is shown verbatim in chat before its
     checkpoint commit (work-log one-liners and checkbox ticks are exempt).

5. **Delegate** per tracking-rules (Sonnet for well-specified mechanical
   work; Opus for design-sensitive work; never Haiku; Fable only via
   `/milestone-brief`); tier-tag the Agent description ([S]/[O]). Verify
   subagent diffs yourself; one work-log line per delegation.

6. **Plan amendments** (implementation always learns things planning
   didn't know):
   - *Minor* (reorder tasks, refine wording outside the amendment-gated
     sections — Goal, Scope, Acceptance criteria — add a discovered
     sub-task): edit the milestone file; one work-log line.
   - *Substantive* (a criterion or scope must change; a change to
     acceptance-criterion wording is *Substantive* by definition): mini
     question gate with a recommendation, the proposed text shown verbatim
     above the
     mini gate's chip (acceptance chips, tracking-rules); record the
     amendment as a dated work-log line
     (+ D-entry if cross-cutting); show the amended criterion/scope text
     verbatim in chat before its commit (durable-record preview).
     **Return-adjacent direction rule (D-118).** On a milestone whose
     work log records one or more defect returns, a proposed amendment
     that widens the criteria set — adding an acceptance criterion, or
     extending an existing criterion's promise to a property or domain
     it did not previously bind — is presented at the mini gate with
     narrowing-or-holding the criteria set as the one recommended option and
     the widening as an explicitly non-recommended alternative, the
     motivating finding offered a follow-up home (a candidate ROADMAP
     row or a split milestone) instead. A widening adopted at the user's
     selection records a work-log line naming each criterion widened or
     added. An amendment that executes a widening-test-reclassified
     return is carved out of this rule by name — D-101's inadmissibility
     (below) governs it unchanged.
     Amended acceptance-criterion wording — an amendment return from
     `/milestone-review` included — is asked every question the criteria
     audit asks in the mode `/milestone-plan` step 3 assigns the
     milestone's tier — the proportionality question and, in full mode,
     the instrument question included — by a fresh-context
     **[O]** reader that did not author the amended wording, before the
     amended text is written to the milestone file.
     Wording whose clearance the `/milestone-brief` ingest audit's work-log
     line already covers is exempt.
     Per criterion, wording fixed at the mini gate re-enters the questions
     once with its own fresh reader, and further churn on that criterion
     goes to the user. An
     amendment executing an amendment return from `/milestone-review` writes
     its work-log line in that skill's fixed shape —
     `amendment return: AC<N> — "<amended clause, verbatim>"` — the line the
     amendment-return count and its second-occurrence stop read (M130).
     An amendment executing a return reclassified under `/milestone-review`'s
     widening test takes the narrowing repair `/milestone-plan` step 4's
     bounded-promise rule states; a wider enumeration is not an admissible
     amendment. An amendment
     that grows a plan-owned section re-checks the body against the 150-line
     cap; if it now exceeds it, compress the single heaviest plan-owned
     section in one pass (tracking-rules), never a nibble-and-recount loop.
   - *The goal itself is wrong*: stop; status back to `planned`; routing
     chip to `/milestone-plan` for a proper re-cut.
   Never silently deliver something other than what the plan promised —
   review checks criteria as written.

7. **Blocked?** External blocker → status `blocked` + work-log line naming
   it, stop. Needs Fable-level judgment → routing chip to
   `/milestone-brief`, stop.

8. **Completion.** When all tasks are checked and the active profile's
   `verify` slot passes clean (for a toolchain whose profile names a fuller
   pre-review check, that check), set status `review`, checkpoint-commit, then
   stop with a recap —
   outcome-first (per tracking-rules): what the milestone now does or
   changes, in plain words, before the mechanics —
   file-level summary of the branch diff, test/check results, deviations
   from plan, open concerns — and a **routing chip (AskUserQuestion)**, one
   question, composed per the tracking-rules chip rules; the natural menu, in
   this order):
   - **Proceed to review** → `/milestone-review <id>` (recommended)
   - **Adjust first** — changes on the branch before review
   - **Pause here** — stop; milestone stays at `review`
   Honor "Other" free-text as adjustment instructions. The chip is a stop,
   never an auto-proceed. Note in the recap that the checkpoint makes this
   a safe `/clear` point — review resumes statelessly in a fresh session
   (same-session review via the chip is also fine; see tracking-rules
   context hygiene).
