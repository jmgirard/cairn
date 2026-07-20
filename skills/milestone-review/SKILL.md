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
   acceptance-criterion checkbox (a verification mark against recorded
   evidence, never a change to the criterion text); never edit the plan-owned
   Goal/Scope or the wording of any criterion (see the never-reinterpret rule
   next).

   **Criteria are never reinterpreted at review.** If the work seems right
   but a criterion as written fails, the criterion is wrong — send the
   milestone back for a gated amendment (`/milestone-implement` step 6),
   then re-review. A charitable reading silently destroys what criteria are
   for.

   **AC fencing — evidence before the checkbox.** A criterion checkbox is
   ticked only once its fresh evidence is recorded in the Review section:
   no evidence line, no tick. An already-ticked criterion with no recorded
   evidence is a gate failure, not a pass — treat it as unverified. This
   fences the milestone's own acceptance boxes against optimistic
   check-off; the Coverage completeness check in step 4 fences the plan.

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
   line naming exactly what failed, stop. **Thrash rule:** if this is the
   milestone's third trip back from review (count the work-log), do not
   queue another retry — that's a mis-planned milestone; recommend re-plan
   or split via `/milestone-plan`.

5. **Independent fresh-context review — three lenses, then a scorer.** Spawn
   three reviewers that have not seen the implementation, in parallel, each with
   a *distinct evidence base* (a shared base just finds the same things twice).
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
   - **[S] prior-PR-comments reviewer (Sonnet).** Reads review comments on
     prior merged PRs that touched the modified files and flags only where the
     current diff *reintroduces or contradicts* a point a past PR review raised
     on those files — a regression of a lesson review already taught, not every
     prior comment resurfaced as context. Discovery recipe (prose, not a
     script): `git diff --name-only <default-branch>..HEAD` for the touched
     files → the PRs that touched them (`gh pr list --state merged
     --search "<path>"`, or map the touching commits to PRs via `git log`) →
     `gh api repos/{owner}/{repo}/pulls/{n}/comments` for each PR's review
     comments. **Always spawn this lens; it no-ops cleanly** — with no
     prior-PR evidence (few or no merged PRs, or no GitHub remote) it reports
     "no prior-PR evidence", contributes zero findings, and never errors or
     blocks the gate.

   Give **all three** reviewers this false-positive taxonomy verbatim and tell
   them to drop anything matching it before reporting:
   > Not a finding: a pre-existing issue the diff did not introduce; anything a
   > linter or formatter would catch; a pure style nitpick; a complaint about
   > an unmodified line; an intentional change the milestone's plan called for.

   **Score before triage.** Pass every surviving finding to a **[S] scorer
   (Sonnet)** — a fresh agent that did *not* generate the findings — with this
   rubric verbatim:
   > Score 0–100 your confidence that this is a real, in-scope defect the
   > author would want to fix: 90–100 certain and load-bearing; 80–89 likely;
   > 60–79 plausible but arguable; below 60 speculative or out of scope. Give
   > the integer score and one sentence of justification per finding.

   Findings scoring **below 80 are excluded from the actioned list but logged**
   in the Review section (the count, plus one line each) — surfaced, never
   silently dropped (IP3). Triage each finding scoring **80 or above**: fix now
   / spawn a follow-up (candidate row or milestone) / reject with reason — all
   logged in the Review section. Spawning a follow-up candidate sweeps first per
   the search-first candidate-creation rule (`tracking-rules.md`, Intake).

6. Final checkpoint commit on the branch.

7. **Final approval gate.** Present, outcome-first (per tracking-rules):
   what the user is approving in plain words — what the milestone does or
   changes — then acceptance-criteria evidence, problems
   found and how each was handled, diffstat, anything the user should eyeball
   directly.
   Acceptance chips (tracking-rules): each actioned finding's text appears
   verbatim in this presentation, never only a summary. Ask any remaining clarifying questions first (batched, with
   recommendations). Then put the merge authorization **itself** to the user
   as an `AskUserQuestion` chip — this is the third gate (per tracking-rules),
   never a prose yes/no: the recommended option merges (e.g. `Merge PR #N to
   <default-branch>`) and a decline option is present. Approval withheld (or declined at
   the chip) → log the requested changes as tasks, status back to
   `in-progress`, stop.

8. **On approval — and only then:** record the approval for the merge
   guard — write `cairn/.merge-approved` (gitignored; one line:
   `M<NN> approved YYYY-MM-DD for PR #<N>` — the marker names the PR it
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
   `cairn/milestones/archive/M<NN>-<slug>.md` and **deleting the live
   `cairn/milestones/M<NN>-<slug>.md`**: the summary REPLACES the milestone
   file rather than joining it, and git holds the full text. (Authoring from a
   template makes this an explicit step; when the summary was made by
   compressing the file in place, the move did it implicitly. Skip it and
   `cairn_validate`'s `roadmap<->disk orphans` fires later in this same step.)
   **Budget it to 22 of the 25 permitted:**
   Goal 2 · Outcome 7 · Decisions 3 · Review 3, over the 7 fixed lines
   (title, status, blanks). Measured across 96 summaries, 55 sit at *exactly*
   25 — a distribution censored at the cap, which is what compress-until-it-
   fits looks like from outside — so draft to the allocation and count as you
   go, never trim afterward:

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_budget.py" cairn/milestones/archive/M<NN>-<slug>.md
   ```

   Then: ROADMAP row → `done` + archive path;
   archive any resolved RB/RR pairs; **replace** "Last hygiene check" — overwrite the previous text, never append to it and never demote it to a `Prior:` clause (D-052); verify
   weight caps. **Capture durable lessons:** append any repo lessons this
   milestone taught — build quirks, testing tricks, gotchas worth
   remembering — to `cairn/LESSONS.md`, one per line
   (`- YYYY-MM-DD (M<NN>): <lesson>`, one line each); lessons, not status or a
   *choice* (a choice is a D-entry). None learned → skip.
   **Retire what this milestone covered:** if the milestone shipped a guard, or
   moved content into another file's slot, check whether that retires an
   existing lesson (tracking-rules "Retiring a lesson that no longer earns its
   line"): a test that now **fails on the mistake a lesson warns about** retires
   it, as does content another file's slot now owns, as does **maturation — a
   stabilized family graduating whole into a doctrine module** (D-055); a
   partly-covered lesson is trimmed to its uncovered remainder.
   **Scope this to what the milestone shipped — never re-sweep every lesson.**
   Delete the retired line and name what was graduated in the archive summary;
   nothing else records it.
   Retirement runs before the cap bites, and only if it cannot free the budget
   is the 50-line cap met by pruning the stalest lines in this same commit.
   Durable-record preview (tracking-rules): show the archive summary,
   each LESSONS line, any D-entry, and any candidate graduation verbatim
   in chat before the commit. Docs-only commit:
   `review M<NN>: done`; push. The done
   recap leads with what shipped, in plain words; hygiene mechanics
   compress to one line.

10. **Close with a `/clear` nudge — no routing chip.** Review is the one
    phase whose end is deliberately chip-less (tracking-rules "Question gates
    and routing chips"): M<NN> is archived and all state is on disk, so the
    natural next step is a fresh context, not another in-session route.
    Close in plain prose — tell the user this is a clean `/clear` point and
    recommend starting the next milestone in a fresh session. This close is a
    handoff, so
    emit the commands in a fenced block, never inline backticks
    (tracking-rules "Copy-run commands") — the user is being asked to go run
    them. Emit `/clear` and the obvious next action (`/milestone-plan` when
    planned or candidate work exists, else `/milestone` for a health audit)
    as copyable lines. Do **not** end review
    with an AskUserQuestion — the step-7 merge-approval gate was the last
    chip this phase emits.
