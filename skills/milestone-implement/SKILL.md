---
name: milestone-implement
description: Implement a planned milestone in a cairn repo on its own branch with tests-first tasks and checkpoint commits. Use when the user wants to start, resume, work on, or continue a milestone (e.g. "work on M107", "resume the milestone", "start implementing").
argument-hint: "<id>"
---

# /milestone-implement <id> — planned → review

Plugin root: every `${CLAUDE_PLUGIN_ROOT}` path below is under the plugin
install directory. When the shell has that variable unset or empty — the
symlink install in `~/.claude/skills` leaves it so — substitute the
grandparent of this skill's directory (the `Base directory for this skill:`
line the harness prints above) in every read and command below; never run a
command with the variable empty.

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: git model, tracking-travels-with-code, delegation policy,
CI waiting rules).
Phase header: `# Milestone <NN>: <title>` → `## Implement`.
Chapter markers: mark a chapter at each phase transition and at each stretch —
each task (title opens with its `Tn:` label), each plan amendment, each stop
(session start implicit).
Inside a run (tracking-rules "Question gates and phase closes") this phase
asks no question of its own. It stops for the user only at a stop on the
rulebook's list, and it ends by invoking `/milestone-review` (step 9).

## Session start

Read, in order: `cairn/ROADMAP.md`, the target milestone file,
`cairn/DECISIONS.md`. If an un-ingested RR exists for this milestone,
run ingestion first (see `/milestone-brief`).

## Workflow

1. Verify status is `planned` (fresh start) or `in-progress` / `blocked`
   with a resolved blocker (resume). Verify all `Depends on:` milestones are
   `done`, and that no OTHER milestone is `in-progress` (at most one, ever —
   if one exists, stop with the close block naming it and its resume
   command). Set `in-progress` in ROADMAP + header mirror. **On a return
   from review**, the newest `review return <n>:` work-log line names what
   failed; add one task for it (a minor amendment, step 6) before working,
   so step 9 cannot hand back with the failure unfixed.

2. **Branch.** Check `git status` first — a dirty tree with unrelated
   changes stays unstaged, with a work-log line naming it; never sweep
   strangers into a checkpoint commit. First session: detect the default branch (tracking-rules git
   model: `git symbolic-ref --short refs/remotes/<base>/HEAD`, strip
   `<base>/`, where `<base>` is the base remote — `origin` in owner mode,
   `upstream` when present in guest mode) and sync it with `<base>` first —
   `git fetch <base>`, pull (ff-only), and **push any unpushed local
   commits** — so the branch is cut from the pushed default branch and the
   PR diff will contain only milestone work; then `git checkout -b
   m<nnn>-<slug>`; record the branch in the milestone header. **Companion
   checkouts:** a milestone whose tasks also change a second repo the user
   holds a checkout of (a deployed page beside a package) cuts the same
   branch there — `cd <abs-path> && git checkout -b m<nnn>-<slug>` in one
   Bash call, since the shell cwd resets to the session repo after every
   call — and records it as a further `Branch/PR:` entry, `companion:
   <abs-path> <branch>`, one per checkout; every later command in that
   checkout is spelled `cd <abs-path> && …` the same way, and
   `/milestone-review` merges each companion before the primary (its step
   8). **Guest arm**
   (tracking-rules "Collaboration mode"): the fetch is the whole sync — the
   default branch is never pushed, and the local copy needs no pull — and
   the branch is cut directly from the base: `git checkout -b <slug>
   <base>/<default-branch>`. Resume sessions: check out the
   existing branch; if the default branch has moved since the branch was cut
   (e.g., a hotfix merged), merge it into the branch and re-run the active
   profile's `verify` slot before continuing. Guest arm: `git fetch <base>`
   then `git rebase <base>/<default-branch>` in place of the merge — the
   branch is the operator's own on the fork, so the rebased branch goes up
   with `git push --force-with-lease origin <slug>` once a PR exists (the
   force-push guard covers the default branch alone); the maintainers'
   review comments stay attached to the PR.

3. **No question round.** The agent decides the implementation choices the
   plan left open (API shape, naming, structure) and writes a work-log line
   for each. A dependency change, or an outward or irreversible action, that
   the plan question set did not grant permission for — read from the
   milestone's `question set:` work-log lines, never from recall — is a
   stop: one chip
   with a recommendation, and a D-entry for a dependency change.
   **The escalation offer is a stop.** If the plan tags an item `(RB
   tripwire: <token>)`, or a new tripwire emerges mid-work (same three
   categories; see tracking-rules), stop at that item with one chip that
   offers **Escalate via `/milestone-brief`** beside the agent's own
   recommended answer. The three tripwires are the must-offer cases, and the
   offer may also be made for a genuinely hard question the session cannot
   confidently settle (D-062 lowered this bar). Either way it stays gated per
   instance through `/milestone-brief` (D-004). Acceptance chips
   (tracking-rules): a question resting on a produced conclusion shows its
   substance compactly in the chip and verbatim in the chat above,
   best-effort (Mandated-substance rule).

4. **Work tasks in order, autonomously.** For each task:
   - Tests first where feasible; numeric results per the oracle doctrine;
     language-specific test and error-condition idioms per the active
     profile's `test-doctrine` slot.
   - Run the active profile's `verify` slot (`cairn/PROFILE.md`; absent →
     infer per tracking-rules "Toolchain profiles") — its checks must be clean
     before the task is checked off.
   - Checkpoint-commit per task on the branch, **including** the milestone
     file update (checkbox + one work-log line) in the same commit.
     **Guest arm** (tracking-rules "Collaboration mode"): the checkpoint
     commit carries the code only — the milestone file update is written to
     disk in the same turn and never staged (the commit guard denies a
     `cairn/` path); the branch is `<slug>` alone and the commit message
     carries no `M<NNN>` or cairn vocabulary.
     Prose the commit adds about an artifact's behavior follows the tracking-rules derived-claims rule: derived from the artifact, never composed.
     A claim resting on an observed failure follows the tracking-rules failure-identity rule: verified to be the failure the claim is about, never read off a bare error.
   - Stay within implement-owned sections per the tracking-rules
     section-ownership table; Goal, Scope, and Acceptance criteria change
     only via the substantive amendment of step 6.
   - Durable-record preview (tracking-rules): a milestone-local Decisions
     entry or promoted D-entry is shown verbatim in a guaranteed-rendered
     position (Mandated-substance rule; work-log
     one-liners and checkbox ticks are exempt).

5. **Delegate** per tracking-rules (Sonnet for well-specified mechanical
   work; Opus for design-sensitive work; never Haiku; Fable only via
   `/milestone-brief`), setting the model the work calls for on each
   spawn. Verify
   subagent diffs yourself; one work-log line per delegation.

6. **Plan amendments** (implementation always learns things planning
   didn't know):
   - *Minor* (reorder tasks, refine wording outside the amendment-gated
     sections — Goal, Scope, Acceptance criteria — add a discovered
     sub-task): edit the milestone file; one work-log line. A change that
     adds, removes, or reorders a criterion or task renumbers the `ACn:` /
     `Tn:` labels and the Coverage lines together.
   - *Substantive* (a criterion or scope must change; a change to
     acceptance-criterion wording is *Substantive* by definition): the
     agent makes the amendment and records it as a dated work-log line
     that opens `substantive amendment:` (the prefix `/milestone-review`
     step 7's up-front check reads) (+ D-entry if cross-cutting); show the amended criterion/scope text
     verbatim in a guaranteed-rendered position (durable-record preview).
     **The stop.** If the amendment drops something the user asked for, or
     changes what the user sees from the plan, stop for the user instead:
     one chip with a recommendation, the proposed text shown verbatim in a
     guaranteed-rendered position at the chip (acceptance chips,
     tracking-rules). A change to the wording alone, the deliverable the
     user sees unchanged, takes no stop.
     A change that adds, removes, or reorders a criterion or task renumbers
     the `ACn:` / `Tn:` labels and the Coverage lines together.
     **Return-adjacent direction rule (D-118).** On a milestone whose
     work log records one or more defect returns, the agent never takes an
     amendment that widens the criteria set — adding an acceptance
     criterion, or extending an existing criterion's promise to a property
     or domain it did not previously bind. It narrows or holds the criteria
     set and gives the motivating finding a follow-up home (a candidate
     ROADMAP row or a split milestone) instead. A widening changes what the
     user sees from the plan, so it reaches the criteria only at the stop
     above, offered there as an explicitly
     non-recommended option, and a widening adopted at the user's selection
     records a work-log line naming each criterion widened or added. An amendment that executes a widening-test-reclassified
     return is carved out of this rule by name — D-101's inadmissibility
     (below) governs it unchanged.
     Amended acceptance-criterion wording — an amendment return from
     `/milestone-review` included — is asked every question the criteria
     audit asks in the mode `/milestone-plan` step 3 assigns the
     milestone's tier — the proportionality and instrument questions
     included in either mode — by a fresh-context
     **Opus** reader that did not author the amended wording, before the
     amended text is written to the milestone file (under a
     spawn-restricting harness instruction, tracking-rules' freshness-spawns
     clause governs).
     The re-audit records one work-log line either way, one line per
     criterion re-entered, in the fixed shape
     `re-audit: AC<N> (<full|reduced>) — <what it returned, or "nothing">`;
     an absent line means the reader did not run, never that it ran and
     was silent. A criterion's first line is the reader's audit of its
     amended wording; the once re-entry below writes its second.
     Wording whose clearance the `/milestone-brief` ingest audit's work-log
     line already covers is exempt, read from that line by name (its shape
     `ingest audit RR<NN> (full): cleared AC<list> — …`, `/milestone-brief`
     step 3): the ingest line's cleared list names the criterion, and the
     amended text equals the ingested text — the criterion as the milestone
     file carried it at the ingest commit — whitespace-normalized as the
     `binding criteria` check normalizes (`" ".join(s.split())`); an ingest
     line that does not name the criterion exempts nothing, and an exempt
     criterion writes no re-audit line and spends no re-entry.
     Per criterion, wording the agent fixes after the reader's findings, or
     a user fixes at a stop, re-enters the questions once with its own fresh
     reader, and further churn on that criterion goes to the user (the
     repeated review-failure stop of the rulebook's list) — the bound and the stop both read from the
     `re-audit: AC<N>` lines, never from session memory: a second
     `re-audit: AC<N>` line naming the same criterion on one milestone is
     the stop, and with it present no further reader is spawned for that
     criterion. An
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
   - *The goal itself is wrong* (a stop on the rulebook's list): status
     back to `planned`; close block pointing at `/milestone-plan` for a
     proper re-cut.
   Never silently deliver something other than what the plan promised —
   review checks criteria as written.

7. **Claim audit** (user-facing prose read against the code before
   review). Owed when the milestone file's `Surface tier:` slot reads
   `user-facing` and `git diff <default-branch>...HEAD -- . ':!cairn/'`
   adds lines; otherwise not owed. Spawn a fresh-context **Opus** reader that
   authored none of those lines; it reads every added line of that diff,
   reports each claim it finds there about what an artifact does, and
   reads each against that artifact in the same session — a spawn refused
   under a spawn-restricting harness instruction stops the step with a
   close block posing it (tracking-rules' freshness-spawns clause), never
   an unlogged author-inline run. Stopping rule: one pass; a claim the
   pass corrects is re-read once by the same reader; no second pass. The
   step's work-log line takes the fixed shape
   `claim audit: <N> claims read, <K> corrected — <files>`, N the claims
   the reader reported, or `claim audit: not owed — <reason>`, the reason
   the first that applies of `internal tier`, `no added lines outside
   cairn/`; an absent line means the reader did not run. This is the
   first read of the branch's added claims against the code by a reader
   other than their author, before review (D-136).

8. **Stops.** Implement stops only at a stop on the rulebook's list
   (tracking-rules "Question gates and phase closes"). An external blocker
   → status `blocked` + work-log line naming it. Needs Fable-level
   judgment → the escalation offer of step 3. A context-hygiene stop →
   checkpoint-commit at the task boundary. Each stop that is not a chip
   ends with the **close block**: an outcome-first recap of what is done
   and why it stopped; a status table (milestone, status, branch/PR, suite
   results); the implement-stop **CI line** (tracking-rules close-block
   shape), one plain sentence saying there is nothing to wait for now: no
   PR exists yet, and `/milestone-review` pushes the branch, opens the PR,
   and waits on CI itself at its merge step, after the user's approval (on
   a return from a review that stopped between its post-approval open and
   the merge, where the header already names an open PR, the line instead
   says there is still nothing to wait for now: review re-pushes and
   re-waits on that PR's checks at its merge step, and any check state the
   PR shows was run against the pre-return head); the fenced next command,
   `/milestone-implement <id>` labeled as the command that resumes the run;
   and the safety line (the checkpoint makes this a safe `/clear` point).
   No chip.

9. **Completion: hand off to review.** When all tasks are checked and the
   active profile's `verify` slot passes clean (for a toolchain whose
   profile names a fuller pre-review check, that check), set status
   `review`, checkpoint-commit, then invoke `/milestone-review <id>`
   through the Skill tool in place of a close block. Before the call, state
   in a few plain sentences what the milestone now does or changes,
   deviations from plan, and open concerns; review's merge question carries
   the full outcome-first account. Review re-reads its state from the files
   and gathers its evidence by command, never from this session's recall
   (tracking-rules "Context hygiene").
