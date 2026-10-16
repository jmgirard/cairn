---
name: milestone-plan
description: Plan one or more milestones for a cairn repo - investigate, scope, write acceptance criteria, and register them in the ROADMAP. Use when the user wants to plan a milestone, plan new work or a feature, turn an idea or candidate into a concrete plan, or asks "what would it take to build X".
argument-hint: "[title or description]"
---

# /milestone-plan — idea → planned milestone(s)

Plugin root: every `${CLAUDE_PLUGIN_ROOT}` path below is under the plugin
install directory. When the shell has that variable unset or empty — the
symlink install in `~/.claude/skills` leaves it so — substitute the
grandparent of this skill's directory (the `Base directory for this skill:`
line the harness prints above) in every read and command below; never run a
command with the variable empty.

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: sizing tripwires, status gatekeeping, question gates).
Phase header: `# Milestone <NN>: <title>` → `## Plan` (before an ID is
assigned, `# Planning`); see the tracking-rules Phase header rule.
Chapter markers: mark a chapter at each phase transition and at each stretch —
investigation, the question set, solidify-and-commit (session start implicit).

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
   an active milestone, say so in chat. Planning ahead is fine, and the plan
   then ends with the close block, not the run (step 7).

   **Tier check (before step 2).** Before it investigates, the plan checks
   that the request needs a milestone, by the tiers of tracking-rules
   "Sizing and the work tiers". It puts the request as a whole in exactly
   one tier:
   - `hotfix`: a user-visible bug whose fix restores documented behavior
     in one sitting with no design decision.
   - `trivial`: no runtime surface (a typo, a comment, a tracking edit),
     one sitting, no design decision, and, in guest mode, only files
     under `cairn/`.
   - `milestone`: anything else, a small change to running code that is
     not a bug included.

   A request whose parts fall in more than one tier, or any of whose parts
   is `milestone`, is a milestone. The check can read the code and docs the
   request names. It does not run step 2's sweeps or spawn subagents. The
   check runs on every source of request that names work: typed text, a
   candidate row, a pane press. A request that names a GitHub issue (`#N`
   or an issue URL, or any other form `/milestone`'s argument accepts) is
   not checked and is planned as a milestone, since `/milestone` with the
   issue is the door that tiers an issue. In guest mode a request that
   names a pull request is not checked either. Examples are a PR URL,
   "PR 12", and "adopt PR 12". This guest rule comes before the issue rule
   and the already-tiered list below. A PR URL, or a §3 item that is a PR,
   takes it. A bare `#N` stays an issue, as above. The plan reads
   `gh pr view <N> --repo <base-repo> --json state,headRefName,author` and
   the operator's login (`gh api user --jq .login`). An `OPEN` or `MERGED`
   PR whose head branch starts with `hotfix-` and whose author is the
   operator is the operator's own handoff. For it the plan ends with a
   close block whose fenced command is `/hotfix` with the PR reference.
   For any other PR it ends with a close block that says guest mode
   does not adopt a third party's PR (tracking-rules "Collaboration
   mode"). A `CLOSED` handoff, or a PR URL whose repo is not
   `<base-repo>`, takes that close block too. A failed read ends with a
   close block that names the cause. These close blocks write nothing.
   Three invocations are already tiered. The first is an invocation from
   `/milestone` §4's `milestone` verdict. The second is a
   `/milestone-plan` for work that `/hotfix` found over the hotfix bar
   earlier in this session, whether that hotfix stopped at step 1 or
   closed at step 7 after a merged-PR re-entry. The third is a
   `/milestone-plan` disposition that the user selected in `/milestone` §3
   earlier in this session. The check classifies all three `milestone`
   without re-judging, and the work-log reason names the router. A
   request that names no work is not checked: its work is chosen at step
   3's question set and planned as a milestone.

   **The tier chip.** On a `milestone` finding the plan asks nothing and
   goes on. On a `hotfix` or `trivial` finding it poses one chip before
   step 2. The chip's question text names, in plain words, the tier found
   and the reason. The chip comes before the run's question set and is not
   part of it (tracking-rules "Question gates and phase closes").

   **Candidate-row match (trivial route).** On a `trivial` finding, before
   the checks, the plan finds the candidate rows the edit fixes. A matched
   row is a row of `cairn/ROADMAP.md`'s Candidates section whose short
   title (tracking-rules "Candidate short title") the request quotes. A
   row whose title a `planned`, `in-progress`, `blocked`, or `review`
   milestone file quotes is not matched, since that milestone's post-merge
   hygiene graduates it. A row that ends with a ` — started` token is not
   matched either, since the record the token names graduates it. The
   edit deletes each matched row it covers in full. It narrows each row it
   covers in part to the part left, keeping the row's title, with a
   `narrowed YYYY-MM-DD by a trivial edit` note, as `/hotfix` step 7 does.
   A matched row the edit does not fix stays as it is. With a row to edit,
   `cairn/ROADMAP.md` is a file the edit touches, so the checks and the
   commit cover it. In guest mode the row changes on disk with no commit.

   **Trivial-route checks (owner mode).** Before it poses the chip on a
   `trivial` finding, the plan runs five checks in this order. The repo
   has a remote. `git fetch <base>` succeeds. The checkout is on the
   default branch and level with `<base>/<default-branch>`. Nothing is
   staged. `git status` shows no uncommitted change in a file the edit
   touches.

   The chip's options:
   - **The tier's route** (recommended). `hotfix`: invoke `/hotfix`
     through the Skill tool with the request as its argument, in
     `/milestone` §4's form. The argument opens with a one-line summary of
     the bug. The request text follows unchanged, with a candidate row's
     title quoted verbatim. The plan writes no file. `trivial`: the
     option's description names the file and the change and says where
     the edit goes. It also names each matched row and whether the edit
     deletes or narrows it. In owner mode it is committed and pushed to the
     default branch. In guest mode it is left uncommitted on disk. In
     owner mode the description also names any other uncommitted paths,
     which the commit leaves alone. If
     a check failed, the description says that the edit cannot be made
     now, and why. In owner mode the plan runs `git status` and the other
     checks before the chip, then edits and commits only the files the
     edit touches and pushes at once. If the checkout is not on the
     default branch, or one of those files holds uncommitted changes, the
     plan makes no edit and ends with a close block naming why. Any other
     failed check ends the same way. Otherwise the plan shows the edit
     verbatim in chat and runs `git add -- <paths>`,
     `git commit -m "<one-line summary>" -- <paths>`, and
     `git push <base> HEAD:<default-branch>`. If the push fails or is
     rejected, it never forces. The close block then names the local
     commit and the undo command `git reset --soft HEAD~1`. On success it
     ends with a close block naming the commit. In guest mode it writes the
     edit on disk with no commit and ends with a close block.
   - **Plan a milestone anyway.** The plan goes on to step 2.
   - **Stop.** The close block, and nothing written.

   Step 4 writes one work-log line in the first milestone file it writes:
   `tier check: milestone — <reason>` after a `milestone` finding,
   `tier check: <tier> — planned as a milestone at the user's choice`
   after the plan-anyway option, or `tier check: not run — work named at
   the question set` for a request that named no work. A request that
   names an issue writes `tier check: not run — request names an issue`,
   unless a router sent it, in which case it writes the `milestone` line
   naming the router.

2. **Investigate first.** Read the relevant code and DECISIONS.md. For
   scopes touching more than a couple of files, fan out Sonnet Explore
   subagents with specific focuses; require file:line
   citations. Draft scope, tasks,
   and the list of genuinely open decisions internally.
   **The acceptance criteria are drafted here to their final wording, not at
   step 4** — step 3's criteria audit reads the bytes step 4 will write, and an
   audit over a rougher draft certifies text that never ships.

   **Surface tier (mandatory).** Every plan classifies the milestone's
   deliverable as user-facing or internal, and records the tier and a
   one-clause reason in the milestone file's `Surface tier:` header slot.
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
   Prior state is surfaced, never silently obeyed or silently overridden. A
   disposition that changes what the user will get (a standing rejection, a
   shipped milestone that may already do it, a cut of something asked for)
   is a question of the step-3 set. The agent takes the rest itself and
   writes a work-log line for each:
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

   **Inbox sweep.** The sweep also reads the repo's open GitHub inboxes,
   in the shape of the health audit's reads (`/milestone` §2): enumerate
   both —
   `gh issue list --repo <base-repo> --state open --json number,title,url` for issues,
   `gh pr list --repo <base-repo> --state open --json number,title,url,author,headRefName`
   for PRs (the rulebook's slug recipe gives `<base-repo>`) — then drop
   cairn's own in-flight work from the PR list: a PR
   the operator authored, or whose head branch is `m<nnn>-*` or
   `hotfix-*`, is dropped (the `author.login` and `headRefName` fields are
   what the filter reads; the operator's login is what `gh api user --jq
   .login` returns). What survives is judged for overlap with the goal
   being planned, and only a hit takes a disposition here, which the agent
   decides and logs: an open issue overlapping the goal becomes a
   `Resolves:` entry (`closes` or `partial`) or a candidate row; an open PR
   overlapping it becomes a candidate row naming `/hotfix` as its door in
   owner mode, or naming the maintainers in guest mode, where the rulebook
   does not support adopting a PR through `/hotfix` (search-first applies
   to both). Items with no overlap take
   no disposition at the plan — report their count in the chat; in owner
   mode `/milestone` §3 is where they are triaged. The sweep writes nothing
   to GitHub — no labels, comments, or closes. **When `gh` is missing,
   unauthenticated, or the repo has no remote:** name which of the three it
   was, skip the sweep, and continue planning.
   **Guest mode** (tracking-rules "Collaboration mode"): these reads go to
   the base repo's inboxes, unlike `/milestone` §2's inbox bullet, which
   skips guest mode. The reason is that the plan's sweep looks for overlap
   with the planned work, such as an upstream issue that the work resolves,
   while §2 skips the maintainers' inbox, since triaging their intake is
   their act.

   **Checker-regress shape.** The sweep also names this shape: a scope
   extending or hardening a checker that the ROADMAP or archive records
   an earlier milestone of the same repo shipping, where that checker
   verifies repo-internal artifacts. On such a hit the step-3 set poses
   simplifying or deleting the checker as the recommended option and
   hardening it as a present, non-recommended alternative, since dropping
   asked-for work is never the agent's call. A repair that
   leaves the checker's promise unchanged stays outside the shape
   (D-090's Untouched clause); one that widens the checker's promise is
   the regress shape however it is framed.

   **Harvest recent lessons (before the gate).** Review `cairn/LESSONS.md`
   (read at session start) and surface any lessons bearing on this scope —
   build quirks, testing tricks, gotchas that should shape the tasks,
   acceptance bar, or a gate question. Empty file → nothing to surface. This
   is intake, not obedience: a lesson informs the plan, it doesn't dictate it.

3. **The question set** (one batched AskUserQuestion round, 2–5 questions,
   each with a recommendation): the one plan gate of the run
   (tracking-rules "Question gates and phase closes"). It asks only what the
   user alone can settle, and it looks ahead to what implement and review
   will need from the user, since the run asks nothing more until the merge
   question. Its questions are:
   - what to work on, for a request that names no work,
   - choices that the request leaves open about what the user will get,
   - files, access, or looks that only the user can supply and that
     implement or review will need,
   - permission for the outward actions and dependency changes that the work
     foresees.

   The agent decides the rest itself and writes a work-log line for each:
   criteria wording, criteria-audit findings, milestone splits and order,
   approach, test scope, and changelog entries. A question the agent cannot
   phrase without the terms of cairn is a question the agent decides itself.
   Acceptance chips (tracking-rules): a question resting on a produced
   conclusion (subagent findings, a collision verdict) shows that
   conclusion's substance compactly in the chip and verbatim in the chat
   above, best-effort (Mandated-substance rule). A split or cut the agent
   makes states **where the remainder goes** in its work-log line and in
   step 5's ledger: "M12 covers A and B, C becomes M13 (planned now, depends
   on M12), D becomes a candidate row". Dropping something the user asked
   for is never the agent's call; it is a question of the set.
   **The answers go on disk.** Step 4 writes each answer that grants a
   permission, a file, access, or a look as one work-log line in the
   milestone it serves, `question set: <what was asked> — <answer>`, so a
   resumed run reads what the user granted from the file, never from recall.

   **Issue assignment (one option).** When the `Resolves:` slot step 4
   will fill is not `—`, the set poses one option offering to assign
   the operator's own GitHub account to every slotted issue, `closes` and
   `partial` entries alike (an outward action, so it is the user's
   permission to give), unless the access read below withholds it.
   The option posts no comment. Before composing it, the agent reads the
   account's access to the repo with
   `gh repo view <base-repo> --json viewerPermission`. If the value is
   below `TRIAGE`, meaning anything but `ADMIN`, `MAINTAIN`, `WRITE`, or
   `TRIAGE` (an empty value included), or the read fails, the set poses no
   assignment option, and the chat says in one line that the account
   cannot assign on that repo, naming the read's failure where the read
   failed. That line rides in the question text of one of the set's
   questions, or in the turn's final text when the set poses none, and
   step 4 writes it as one work-log line. Otherwise the agent reads each slotted
   issue's assignees with `gh issue view <N> --json assignees`, and the
   option description names them. If another account holds an issue, the
   description says so. If the read fails, the description calls that
   issue's assignees unknown. The command runs only on selection, after
   step 4 writes the milestone file: `gh issue edit <N> --add-assignee @me`
   for each slotted issue, before step 6's commit, so any work-log line it
   writes rides in that commit. A declined option writes nothing to GitHub.
   GitHub can drop an assignee it does not accept with no error, so the
   agent re-reads each issue's assignees after the command, and an issue
   whose assignees still lack the account counts as a failed command. If
   the assign command fails for an issue, or `gh` cannot run at that
   point, the agent names the issue and the error in chat and in one
   work-log line, and writes nothing else to GitHub for that issue. Guest
   arm (tracking-rules "Collaboration mode"): the `gh issue view` and
   `gh issue edit` commands add `--repo <base-repo>`.

   **Criteria audit (runs before the questions are composed; scaled to
   stakes).** A plan author's own read of its own criteria is the check
   measured to fail — M114
   authored criteria that were unsatisfiable as written and one that mandated
   an IP4 violation, costing gated amendments and review returns, and each was
   discoverable here. The audit's mode follows the step-2 surface tier:
   a milestone whose declared tier is user-facing, or any of whose drafted
   criteria or tasks carries an RB-tripwire tag, gets the **full audit**; an
   internal-tier milestone gets the **reduced audit** (M145). Either way the
   step-2 criteria go to a fresh-context **Opus**
   reader that authored none of them (under a spawn-restricting harness
   instruction, tracking-rules' freshness-spawns clause governs). The full audit asks three mechanical
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
   property of an instrument that verifies it or records its
   verification — a test harness, a floor, a plant matrix, a checker's
   own prose, a work-log recording act, a mandated evidence quotation,
   among others (D-118; recording instruments joined the genus by
   D-120). A criterion
   binding an instrument property is a finding, disposed by the agent
   like the audit's other findings: the instrument property moves to the
   tasks or the review procedure, or the criterion narrows to the
   deliverable property it certifies. The question governs what a promise
   binds, never how a deliverable-bound promise is verified — it never
   relaxes the probe question above, in the full mode that asks it.
   Both modes ask a proportionality question of each criterion:
   is the promise's domain proportionate to the declared surface tier
   (the step-2 rule)? An internal-tier criterion outside the
   internal-tier criteria standard is a finding, disposed by the agent
   like the audit's other findings; the question governs promises and
   never relaxes the probe question above, in the mode that asks it.
   **The reduced audit asks only the bounded-promise, proportionality,
   and instrument questions** of each criterion — it omits the
   satisfiability, reachability, and probe questions — and keeps the
   disposal rule below in full.
   The agent disposes of what either mode returns itself, never silently:
   each finding is fixed or answered, and its disposition is reported in
   chat and written in a work-log line. A finding the agent could decide
   either way is decided toward the narrower promise.
   The instrument is a reader and never a check — satisfiability and
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
   registry submission, a "prepare/consolidate for vX.Y.Z". On a hit, the question set
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
     step 3's audit read**; a criterion the question set's answers changed goes back through
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
   - **Positional labels** (owner: plan): every criterion and task bullet
     opens with its positional label (`ACn:` / `Tn:`), the label equal to
     the item's position counted top-to-bottom in its section — the number
     Coverage cites; any insertion, removal, or reorder renumbers the labels
     and the Coverage lines together, never one without the other.
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
   - **Resolves** (header slot): the slot is filled from the issues the scope
     absorbs — a promoted candidate row citing one, or an issue the user
     names, or a step-2 inbox hit the plan took — one entry per issue:
     `#N closes` when this milestone's PR closes
     it, `#N partial` when only part of it ships. A `partial` entry's
     remainder is recorded as a `candidate` row in the same plan commit
     (search-first applies) and listed in step 5's remainder ledger, so the
     GitHub issue is never the remainder's only record. No issue → `—`.
     `/milestone-review` reads the slot for the PR body's closing lines and
     the post-merge check; the archive summary's status line carries it.
   - **Surface tier** (header slot): filled from step 2's classification —
     `user-facing` or `internal`, an em dash, and the one-clause reason
     (`internal — a checker over in-repo tracking files`). Never left `—`:
     step 2 makes the classification mandatory. `/milestone-review` step 5
     reads the slot to scale its review fan-out; skill conduct only — no
     validate check parses it.
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
   - **Tier-check line.** Write the `tier check:` work-log line that
     step 1's tier check names.
   - **Draft against the cap, not against the gate.** The plan-owned body
     must land under `cairn_validate`'s 150-line cap; count while writing
     rather than discovering the overrun at gate time, when the only remedy
     left is compression.
   Deferred chunks not yet plannable get `candidate` ROADMAP rows, not files.

5. **Remainder ledger (conservation check).** Before committing, enumerate
   every distinct thing the user originally asked for and its disposition:
   in this milestone / planned as M<NNN> / candidate row / dropped at the
   user's explicit request. Nothing may be silently absent. A `partial`
   entry in the `Resolves:` slot lists its remainder here with the candidate
   row that holds it. Deferral is
   NEVER recorded as a decision not to do something — D-entries are for
   genuine rejections with rationale; postponement lives in the ROADMAP.
   Include the ledger in the plan summary presented to the user.

6. **Commit atomically.** Durable-record preview first (tracking-rules):
   show each drafted durable text — the milestone files' plan-owned
   sections, any D-entry, new ROADMAP rows — verbatim in a guaranteed-rendered
   position (Mandated-substance rule). Then update ROADMAP rows (`planned` / `candidate`),
   append ` — started M<NNN>` to the end of each candidate row the plan
   absorbs in full or in part, in both modes (tracking-rules "Candidate
   started token"), and
   commit files + rows together, directly to main, no branch, no PR
   (docs-only carve-out): `plan M<NNN>[, M<NNN>…]: <title>`, naming every
   milestone ID the plan created, since `/milestone-review` step 10 reads
   this subject to find the next milestone of the plan; push. A session
   dying mid-plan must not leave a half-planned ghost.
   **Guest arm** (tracking-rules "Collaboration mode"): in guest mode there
   is no plan commit and no push — the milestone files and ROADMAP rows are
   written to disk in this same turn and stay uncommitted (`cairn/` is in
   `.git/info/exclude`); the preview and step 7 are unchanged.

7. **Hand off to implement** (tracking-rules "Question gates and phase
   closes"). After step 6, show the plan summary and
   remainder ledger in chat, then invoke `/milestone-implement M<NNN>`
   through the Skill tool for the first workable milestone this plan
   created: status `planned`, every `Depends on:` milestone `done`, in
   ROADMAP order. In guest mode one dependency may instead be a stack base
   (tracking-rules "Collaboration mode"). The run goes on from there with no further question until
   the merge question. The merge ends the run, and each later milestone of
   the plan starts from its typed command after a `/clear`.
   **Close block instead** when another milestone is `in-progress`, when the
   user asked for a plan alone, or when no milestone of the plan is workable
   (a release parked as `blocked`, an unmet dependency): recap (the plan
   summary and remainder ledger live here), status table (new milestone(s),
   status, priority), fenced next command(s) with plain labels, such as
   `/milestone-implement M<NNN>` to start the proximal one or
   `/milestone-plan` to plan another, and the adjust-or-`/clear` safety
   line; no chip.
