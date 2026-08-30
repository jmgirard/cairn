---
name: milestone-review
description: Verify and ship a finished milestone in a cairn repo - fresh evidence for every acceptance criterion, consistency gate, independent code review, and merge on user approval. Use when the user wants to review, verify, finish, ship, or merge a milestone.
argument-hint: "<id>"
---

# /milestone-review <id> — review → done

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: approval model, CI waiting rules, archive protocol).
Phase header: `# Milestone <NN>: <title>` → `## Review`.
Chapter markers: mark a chapter at each phase transition (session start implicit).

## Session start

Read, in order: `cairn/ROADMAP.md`, the target milestone file,
`cairn/DECISIONS.md`. Status must be `review` (or the user explicitly
overrides — log the override).

## Workflow

1. **Sync with the default branch first** — detect it (tracking-rules git
   model) and read it as its origin ref: `git fetch` before comparing, and
   push the default branch if it has unpushed local commits. If it has
   moved since the branch was cut, merge it into the branch and re-run
   tests before gathering any evidence — evidence from a stale branch is
   worthless and the squash-merge would conflict anyway.

2. Push the branch; open a **draft PR** (`gh pr create --draft`) so CI runs
   in the background while the review proceeds. Record the PR URL in the
   milestone header.

3. **Execute every acceptance criterion with fresh evidence** — actually run
   the tests and the active profile's checks (its `verify` / `consistency-gate`
   slots); record results per criterion
   in the milestone's Review section (summaries, never pasted output). Write
   the Review section — review-exclusive per the tracking-rules
   section-ownership table — and, under AC fencing, tick each verified
   acceptance-criterion checkbox as its evidence line is recorded (a
   verification mark against recorded evidence, never a change to the
   criterion text); never edit the plan-owned
   Goal/Scope or the wording of any criterion (see the never-reinterpret rule
   next).

   **Criteria are never reinterpreted at review.** If the work seems right
   but a criterion as written fails, the criterion is wrong — send the
   milestone back for a gated amendment (`/milestone-implement` step 6),
   then re-review. A charitable reading silently destroys what criteria are
   for.

   **AC fencing — evidence before the checkbox.** A criterion checkbox is
   ticked only once its fresh evidence is recorded in the Review section:
   no evidence line, no tick. Tick each box as its evidence line is recorded
   — criterion by criterion, in the same step, never one batch pass at phase
   end; this mirrors how `/milestone-implement` ticks each task box at its
   checkpoint commit, and a batch tick at the end is the optimistic check-off
   fencing exists to prevent. An already-ticked criterion with no recorded
   evidence is a gate failure, not a pass — treat it as unverified. This
   fences the milestone's own acceptance boxes against optimistic
   check-off; the Coverage completeness check in step 4 fences the plan.

   **Projection-vs-outcome (Driving RR).** When the milestone's header names
   a `Driving RR:`, record in the Review section each numeric projection
   carried from that RR beside its measured outcome — side by side, both
   numbers verbatim ("measured X against projected Y"), never one without
   the other (M95's −9 against a projected 60–100 passed review because no
   surface ever juxtaposed the two numbers). No driving RR, or none of its
   criteria numeric → this no-ops cleanly.

4. **Consistency gate** — mechanical checks, by command, never recall. Two
   halves: the **universal cairn-file checks** below run unconditionally in
   every repo; the **toolchain checks** come from the active profile's
   `consistency-gate` slot.

   **Universal cairn-file checks (always, every profile):**
   - `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"` passes
     (exit 0). Run it first and read its output — one line per check; never
     restate or recall its internals (a restated list is a stale-count trap,
     M28). Any non-zero exit is a gate failure like any other. Two FAILs
     carry their own disposition: a `scaffold present` FAIL means the repo's
     §1 scaffold has drifted (a missing tracking file or ignore entry) — fix
     it by running `/cairn-init` (repair mode), never by hand-patching; a
     `coverage complete` FAIL (the Coverage completeness map —
     mechanical since M34: every acceptance criterion maps in the Coverage
     section to ≥1 task that exists) is a plan gap — it sends the milestone back to `/milestone-implement` for a
     gated Coverage amendment, never a review-side patch. Read the map,
     don't reinterpret it.
   - If the milestone changed a `DESIGN.md` principle (IPn/GPn):
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_impact.py" --changed` — a
     Sync Impact Report of every `cairn/` file:line citing a changed
     principle. Each listed reference is reconciled in this milestone, or the
     divergence is deliberate and logged. No principle change → skip.

   **Toolchain checks — the active profile's `consistency-gate` slot**
   (`cairn/PROFILE.md`; absent → infer per tracking-rules "Toolchain
   profiles"): run each check the slot names and record its result like any
   other gate check. The slot is authoritative — read it, never recall a
   hardcoded list. A profile whose slot names no toolchain checks (e.g.
   `generic`) makes this half a clean no-op.

   Any criterion or gate failure → status back to `in-progress`, work-log
   line naming exactly what failed, stop.

   **Thrash rule.** Count returns **per milestone, never per cut** — a
   `/milestone-plan` re-cut increments the count and never resets it, since a
   re-cut is itself evidence of thrash. **Count them in the work log**, the one
   record a re-cut leaves standing: it supersedes the tasks and unticks every
   criterion, so current file state reads as a first pass however many returns
   preceded it. The count here is of defect returns; amendment returns run
   on their own track (the step-5 return floor, M130). Two triggers, with
   different remedies:

   - **(a) The third return, and every return after it** — a mis-planned
     milestone. It is a threshold, not a single moment: once reached it holds.
     Do not queue another retry; the recommended option is descope-or-park
     (M143): descope — narrow the milestone to its already-verified criteria
     via the gated amendment protocol (`/milestone-implement` step 6), the
     unverified remainder exiting to candidate rows or a split milestone,
     then re-review the narrowed set — or park as `blocked` with the blocker
     named in a work-log line. A same-objective re-cut via `/milestone-plan`
     and dropping at the user's explicit decision stay present options; the
     re-cut is never the recommended one — both downstream lineages on record
     show a re-cut buying further returns, not a fix (D-105 narrows D-064).
   - **(b) The same acceptance criterion failing twice, each by a new mechanism
     of the same shape** — a wrong approach rather than a mis-sized one.
     Re-cutting around the same predicate buys the next mechanism, not a fix,
     so the remedy is to reconsider the alternative the plan gate recorded
     against — step 4 of `/milestone-plan` records it in the work log.
     Where it recorded none, offer escalation via `/milestone-brief` —
     per instance, never automatically (D-004).

   **Where both fire they compose.** (a) governs the disposition — no further
   retry under the current plan, the chip composed from (a)'s descope-or-park
   menu — while (b)'s diagnosis and its `/milestone-brief`
   escalation offer carry INTO that composed chip rather than being discarded.
   While the recorded alternative is unspent, (b)'s remedy — reconsidering
   it — rides the present, never-recommended re-cut option; after that,
   escalation is what remains of (b).
   They answer different questions, and only the retry question is a conflict.

   **When (a) fires and the work log already records a re-plan or split spent
   on this milestone**, the same-objective re-cut leaves the menu entirely:
   that is the move which just failed. Descope-or-park stays the recommended
   option; beside it the chip carries an offered `/milestone-brief` escalation
   and dropping at the user's explicit decision — never a
   bare retry as the recommended option. Every escalation here stays an offer,
   gated per instance, never automatic and never a standing menu item.

5. **Independent fresh-context review — scaled to stakes.** Review rigor
   follows the milestone's declared surface tier (recorded in its Goal or
   Scope prose at plan time) and the diff's content:
   - **Internal tier, docs-only diff** — the declared tier is internal and
     `git diff <default-branch>...HEAD --name-only` shows only
     markdown/tracking files (no scripts, hooks, or other executable
     surface): spawn **one** fresh-context reviewer — the [O] diff-bug lens
     below — and skip the other two lenses.
   - **Any other diff** — executable surface touched, user-facing tier, or
     no declared tier: spawn the full three-lens fan-out.

   Spawn the reviewer(s) the routing selected — fresh-context, none having
   seen the implementation (under a spawn-restricting harness instruction,
   tracking-rules' freshness-spawns clause governs); in the fan-out they run in parallel, each with
   a *distinct evidence base* (a shared base just finds the same things
   twice), while single-reviewer mode applies the same spawn rules to its
   one [O] lens and the lens list below describes the fan-out.
   **Reviewers share this working tree — ref-based git only:** `git diff`/`log`/`blame`
   against refs (e.g. `git diff <default-branch>..HEAD`), never `git checkout`
   or `git worktree add` in it, which parks the primary checkout on another
   branch mid-review (tracking-rules subagent conduct; hit in M36). The three lenses:
   - **[O] diff-bug reviewer (Opus).** Reviews the full diff
     (`git diff <default-branch>..HEAD`) against the acceptance criteria, DESIGN.md
     conventions, and DECISIONS.md — correctness, contract, convention.
   - **[S] blame-history reviewer (Sonnet).** Runs `git log` / `git blame` on
     the modified lines and judges the change *against the intent of the code
     it touches*: does it silently undo something a past milestone added
     deliberately, resurrect a fixed bug, or contradict a recorded D-entry? It
     reads history, not just the diff.
   - **[S] prior-PR-comments reviewer (Sonnet).** Reads the repo's prior
     review record on the modified files and flags only where the current
     diff *reintroduces or contradicts* a point a past review raised on
     those files — a regression of a lesson review already taught, not every
     prior finding resurfaced as context. **Primary evidence: archived
     `## Review` sections** — in a cairn repo the substantive
     findings-and-triage record lives in `cairn/milestones/archive/`, not in
     PR threads (M91 measured the threads empty across every merged PR the
     lens enumerated). Discovery recipe (prose, not a script):
     `git diff --name-only <default-branch>..HEAD` for the touched files →
     search `cairn/milestones/archive/` for `## Review` sections whose
     findings touch those files → judge the diff against the findings and
     triage recorded there. **Secondary surface, probe-gated: GitHub PR
     threads.** Run one cheap existence probe first —
     `gh api repos/{owner}/{repo}/pulls/comments?per_page=1` (any inline
     review comment at all, bots aside?) — and only when the probe finds
     real review threads walk them per PR
     (`gh api repos/{owner}/{repo}/pulls/{n}/comments` for the PRs that
     touched the files); a repo that reviews on GitHub keeps the surface, a
     repo whose threads hold only bot noise never pays for the walk.
     **Always spawn this lens; it no-ops cleanly** — with no prior-review
     evidence on either surface (no archived `## Review` findings on the
     touched files, a probe finding no real threads, or no GitHub remote) it
     reports "no prior-review evidence", contributes zero findings, and
     never errors or blocks the gate.

   Tell every reviewer spawned to report each candidate finding, filtering
   nothing before reporting, and to **rank its own findings** — most severe
   first, one sentence of justification each, no numeric scores. A reviewer
   told to be conservative reports less and never says what it withheld
   (D-078), so nothing is filtered before it reaches the record.

   **Triage at the gate.** Ranked findings go to the maintainer at the
   step-7 approval gate — that presentation is the triage surface: fix
   now / spawn a follow-up (candidate row or milestone; sweep first per the
   search-first candidate-creation rule, `tracking-rules.md` Intake) /
   reject with reason. Every reported finding and its disposition is logged
   in the Review section — surfaced, never silently dropped (IP3). Two
   triage heuristics survive the scorer they were written for: treat any
   finding that authorizes an outward-facing irreversible action as worth
   fixing regardless of rank, and verify a refutation against the
   implementation, never against the refuter's own account of it. Findings
   matching the out-of-scope taxonomy are ordinarily rejected at triage:
   a pre-existing issue the diff did not introduce; anything a linter or
   formatter would catch; a pure style nitpick; a complaint about an
   unmodified line; an intentional change the milestone's plan called for —
   though a real defect *inside* an intentional change is still a defect,
   since the member covers the change being planned, never a flaw in how it
   was carried out. **The actioned list is the findings triaged fix-now or
   follow-up.** Fix-now work directed at the gate is committed on the branch
   and the branch re-pushed before the approval marker is written (step 8;
   the M105 squash lesson), with approval re-requested when a fix was
   nontrivial; a floor-qualifying finding returns status from the gate
   itself — the return floor below states when.

   **Return floor (M130).** Over the actioned list, a finding moves the
   milestone back to `in-progress` only when it demonstrates an acceptance
   criterion failing — inside its named procedure's domain, where the
   criterion names one, save where the widening test below carves that
   failure out as an amendment return —
   or when the maintainer judges it a load-bearing defect in what the
   repo's deliverables do for their users (for this plugin: what the skills,
   hooks, and scripts do, not the doctrine prose about how work is verified),
   save where that same test carves that finding out.
   Every other actioned finding takes the triage above — fix now / follow-up
   / reject — with no status change, and is logged. The amendment return
   below is the one named exception to this "only when". A floor return
   takes step 4's exit — a work-log line naming exactly what failed, stop.
   The defect-return count the thrash rule reads is step-4 gate returns
   plus returns under this floor; amendment returns stay off it.

   **Amendment return (M130).** A finding that shows the criterion itself
   is wrong — falsifying it only outside the domain of the procedure it
   names, or showing a criterion that names no procedure to be unbounded
   (the never-reinterpret rule's case, step 3), or meeting the widening
   test below, which carves that third case out of this clause's "only
   outside" — is evidence about the
   promise, not the work. It routes to the gated
   criterion-amendment protocol (`/milestone-implement` step 6) and
   re-review, the amendment the only work convened; status is set to
   `in-progress` for that amendment alone, and review stops there. Its
   work-log line carries a fixed
   shape — `amendment return: AC<N> — "<amended clause, verbatim>"` — and
   these lines are counted per milestone on their own track: never reset by
   a re-cut, and never added to the defect-return count (D-097 narrows
   D-064). A second amendment return naming the same AC<N> on one milestone
   stops — no further round is convened; the disposition goes to the user.

   **Widening test (M139).** A finding demonstrating an acceptance criterion
   failing *inside* the domain its promise quantifies over is an amendment
   return rather than a defect return when the only repair available to it
   widens an enumeration whose membership is fixed by author recall rather
   than decided by a procedure over that domain. That discriminator is
   `/milestone-plan` step 4's, and the repair such a return takes is the one
   step 4 states; read it there rather than here. A return reclassified this
   way carries the fixed work-log shape above, counts on the amendment-return
   track under its second-occurrence stop, and never increments the
   defect-return count the thrash rule reads.

6. Checkpoint commit on the branch — the pre-gate checkpoint; fix-now work
   the step-7 gate directs lands after it and is committed and re-pushed
   before the approval marker (step 5's triage ordering clause).

7. **Final approval gate.** Present, outcome-first (per tracking-rules):
   what the user is approving in plain words — what the milestone does or
   changes — then acceptance-criteria evidence, problems
   found and how each was handled, diffstat, anything the user should eyeball
   directly. The presentation and the merge chip share one turn
   (Mandated-substance rule): the chip's question text carries the compact
   decision summary and cites the milestone file's Review section by path,
   and the full presentation rides best-effort in the chat above it.
   Acceptance chips (tracking-rules): each actioned finding's text appears
   verbatim in this presentation, never only a summary. With a Driving RR:
   repeat the measured-vs-projected pairs in the merge chip's question text, compact, and verbatim in the chat above, and a shortfall past the milestone's stated tolerance (an unstated
   tolerance is strict — any shortfall counts) adds an explicit chip option
   **"accept shortfall, recorded as such"** — the maintainer decides seeing
   the gap, and selecting it logs the accepted shortfall in the Review
   section. Ask any remaining clarifying questions first (batched, with
   recommendations). Then put the merge authorization **itself** to the user
   as an `AskUserQuestion` chip — this is the third gate (per tracking-rules),
   never a prose yes/no: the recommended option merges (e.g. `Merge PR #N to
   <default-branch>`) and a decline option is present. Approval withheld (or declined at
   the chip) → log the requested changes as tasks, status back to
   `in-progress`, stop.

8. **On approval — and only then:** record the approval for the merge
   guard — write `cairn/.merge-approved` (gitignored; one line:
   `M<NNN> approved YYYY-MM-DD for PR #<N>` — the marker names the PR it
   approves, and the guard refuses a merge that names a different PR or
   none). The plugin's PreToolUse hook denies
   merges to the default branch without this marker and consumes it per merge attempt;
   if a merge fails and is retried under the same approval, rewrite the
   marker. Write the marker in a **separate** step before the `gh pr merge`
   command — the hook checks it before the command runs, so writing it in
   the same shell line as the merge is denied. Then mark the PR ready;
   require green CI
   (`gh pr checks <pr> --watch` with a timeout — one blocking wait; on
   timeout report fresh state and stop). Red CI → fix on the branch,
   re-verify, re-request approval if the fix was nontrivial. When green:
   `gh pr merge <N> --squash --delete-branch` with a clean summary message —
   name the PR number explicitly; a bare `gh pr merge` is denied by the guard
   because the approval cannot be checked against it.

9. **Post-merge hygiene pass on the default branch:** check it out and pull
   first — after a squash-merge, the local default branch is behind origin and
   any leftover local
   commits mean divergence to resolve before committing. Then write the
   milestone's archive summary **from**
   `${CLAUDE_PLUGIN_ROOT}/skills/shared/templates/archive-summary.md` — a
   comment-free skeleton, so nothing scaffolding-shaped can leak into a
   25-line artifact — writing it to
   `cairn/milestones/archive/M<NNN>-<slug>.md` and **deleting the live
   `cairn/milestones/M<NNN>-<slug>.md`**: the summary REPLACES the milestone
   file rather than joining it, and git holds the full text. (Authoring from a
   template makes this an explicit step; when the summary was made by
   compressing the file in place, the move did it implicitly. Skip it and
   the explicit `cairn_validate.py` run below fails on `roadmap<->disk
   orphans`.)
   Draft the summary to the ≤25-line cap, counting as you go, never trimming
   afterward.

   Then: ROADMAP row → `done` + archive path;
   archive any resolved RB/RR pairs; **replace** "Last hygiene check" with one short line — overwrite the previous text, never append to it or demote it to a `Prior:` clause; verify
   weight caps, the byte budgets by hand (`wc -c cairn/ROADMAP.md
   cairn/LESSONS.md` — `cairn_validate` does not measure them), and each of
   the repo's doctrine modules by hand against the budget its own header
   states (`wc -l -c`; the maturation exit's rule).
   Where the repo ships hand-run prose-guard suites (this plugin's
   `skills/tests`), hand-run them here and note red/green in the stamp (D-109).
   **Capture durable lessons:** append any repo lessons this
   milestone taught — build quirks, testing tricks, gotchas worth
   remembering — to `cairn/LESSONS.md`, one per line
   (`- YYYY-MM-DD (M<NNN>): <lesson>`, one line each); lessons, not status or a
   *choice* (a choice is a D-entry). None learned → skip.
   **Disposition finding-absorbing candidate rows:** when this pass is about
   to extend a candidate row already carrying deferred review findings filed
   from two or more distinct milestones — including by absorbing this
   milestone's deferred findings into it — pose, before writing the
   extension, the disposition chip whose options
   `skills/shared/records-hygiene.md` §7 states, rather than restating them
   here (a routed item then lands via the accepted-limitations block below).
   No such row touched → skip.
   **Route accepted limitations:** a durable limitation this milestone
   surfaced that the user chose to live with — no candidate row, no fix
   planned — gets an entry in `cairn/DESIGN.md`'s Known issues section,
   written in this same hygiene commit. None accepted → skip.
   **Retire what this milestone covered:** if the milestone shipped a guard, or
   moved content into another file's slot, check whether that retires an
   existing lesson (tracking-rules "Retiring a lesson that no longer earns its
   line"): a test that now **fails on the mistake a lesson warns about** retires
   it, as does content another file's slot now owns, as does **maturation — a
   stabilized family graduating whole into a doctrine module** (D-055); a
   partly-covered lesson is trimmed to its uncovered remainder. A graduation
   writes the new module's budget header (the maturation exit's rule), and
   the module read above covers the module this pass just minted.
   **Scope this to what the milestone shipped — never re-sweep every lesson.**
   Delete the retired line and name what was graduated in the archive summary;
   nothing else records it.
   Retirement runs before the cap bites, and only if it cannot free the budget
   is the 50-line / 20,000-byte cap met by pruning the stalest lines in this same commit.
   Durable-record preview (tracking-rules): show the archive summary,
   each LESSONS line, any D-entry, any Known issues entry, and any
   candidate graduation verbatim
   in a guaranteed-rendered position (Mandated-substance rule).
   Then run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"` over
   the completed hygiene edits, before the docs-only commit — it must pass,
   and whether its `release window` advisory fired is the signal step 10's
   displacement clause reads. Docs-only commit:
   `review M<NNN>: done`; push. The done
   recap leads with what shipped, in plain words; hygiene mechanics
   compress to one line.

10. **Close with the close block — no chip.** (tracking-rules "Question
    gates and phase closes" — the shape every phase now shares, generalized
    from what was once review's sole exception.) M<NNN> is archived and all
    state is on disk, so the natural next step is a fresh context: after the
    step-9 hygiene commit lands, run
    `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_next.py"` and take the
    next action from its recommendation. The recap leads with what shipped,
    the status line names the merge and archive state, and the fenced
    commands emit `/clear` and the recommendation's command
    as copyable lines. One displacement (D-050): when step 9's
    `cairn_validate.py` run fired the `release window` advisory, offer
    parking exactly as `/milestone` §3 prescribes — a decision put to the
    user, so it keeps its chip (tracking-rules: a gate is a choice, a
    phase end is a handoff) — and it displaces the recommendation's lead
    only when that recommendation names the flagged release milestone.
    This close is
    a handoff, so commands go in fenced blocks, never inline backticks
    (tracking-rules "Copy-run commands"). Apart from that parking
    decision, do **not** end review with an AskUserQuestion — the step-7
    merge-approval gate was the last chip this phase emits.
