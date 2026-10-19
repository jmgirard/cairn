# M285: Copilot reviews a head that names its PR, and review reads the rest of the repo for stale text

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP3
- **Resolves:** —
- **Surface tier:** user-facing — `/milestone-review` and the rulebook ship to every adopting repo
- **Branch/PR:** m285-review-ripple-lens

## Goal

Copilot reviews a head whose header names the PR, and cairn's own review reads the rest of the repo for text that the diff made stale.

## Scope

**In:** the order of `/milestone-review` step 2's Copilot arm and step 8's sentence about the header record. A ripple reviewer on Haiku in both review modes of step 5. Two questions in the diff-bug lens's instruction, one on await races and one on untried procedure paths. tracking-rules "Model and agent strategy", README, CHANGELOG, a D-entry, and the hand-run guard `skills/tests/test_review_fanout.py`.

**Out:** `/hotfix`, which has no review fan-out and no milestone header. A repo whose GitHub settings start a Copilot review when a PR opens: Copilot then reviews before the header commit, and the arm cannot change that. The five-review check of the ripple lens's yield, which the falsifier names: it lives in the candidate row "Ripple lens yield check". The Copilot threads that asked for mutation entries for hand-run guards (4 threads), because this repo's test doctrine owes none.

## Acceptance criteria

- [ ] AC1: `/milestone-review` step 2's Copilot arm runs in this order. It pushes the branch. It opens the PR, unless the header already names an open PR. For a new PR, it adds the PR's URL to the `Branch/PR` header in a commit and pushes that commit. Then it runs the state query and requests Copilot on `none`. If the branch push or the create fails, the arm reports the failure in one line and requests nothing. If the header already names a closed PR, the create runs and the arm adds the new URL beside the old one. If the header push fails, the arm reports the failure in one line and still runs the state query and the request. That commit then stays local until step 6's checkpoint push carries it. Neither the arm nor step 8 says that step 6's push carries the header record on the normal path, and step 8 cites the new D-entry.
- [ ] AC2: Step 5 spawns a ripple reviewer on Haiku, with the slug `ripple`, in both review modes. The routing bullets say so: an internal-tier docs-only diff gets the Opus diff-bug lens and the ripple lens, and any other diff gets four lenses. The ripple reviewer's instruction tells it to list each rule statement, term, number, identifier, command, flag, and path that the diff removes or changes. For each item, it runs `git grep` on the tracked files at the branch head. It searches for the old form and for other statements of the same fact. It reports each line outside the diff's added lines that now disagrees with the diff, with its file and line. It leaves out history records: `cairn/milestones/`, `cairn/DECISIONS.md`, `cairn/legacy/`, `cairn/reviews/`, and the CHANGELOG sections of released versions. It does not report a line that states a dated measurement or record of an earlier setup. A diff that removes or changes nothing gives the report "no ripple evidence" and zero findings. The lens ranks its own findings, and the agent settles them like the findings of every lens.
- [ ] AC3: The diff-bug lens's instruction in step 5 gains two questions, and the lens reports what they find as ranked findings. (a) The diff adds or changes code that awaits: an `await`, a promise callback, or a timer. For each value that the code reads or sets before an await and relies on after it, can another handler change the value in between? Examples are a second press, a session end, and a later read. (b) The diff adds or changes a skill procedure step. Does the step hold on at least these five paths? The first is a first run with no remote branch, PR, or file yet. The second is guest mode, with `--repo <base-repo>` and a fork or base remote. The others are a PR whose head is on a fork, a dirty working tree, and a remote that moved ahead.
- [ ] AC4: tracking-rules "Model and agent strategy" lists the ripple lens under Haiku subagents. Its review bullet names the ripple lens in both modes and counts four distinct-evidence reviewers in the fan-out. README's review paragraph names the four-lens fan-out and the two-reviewer mode for an internal docs-only diff. The step-5 slug sentence names `ripple`. Run this command: `git grep -n -i -E "three-lens|three lenses|three distinct|three reviewers|three-reviewer|two lenses|other two|single reviewer|single-reviewer|one reviewer|one Opus" -- README.md CLAUDE.md cairn/DESIGN.md cairn/LESSONS.md skills hooks scripts`. Each returned line that states the review's lens count or reviewer count states the new setup, or is a dated record of an earlier setup.
- [ ] AC5: An unreleased CHANGELOG entry states three changes: the header push before the Copilot request, the ripple lens in both review modes, and the two diff-bug questions. A D-entry records the decision. It supersedes D-153's clause that the step-6 checkpoint push carries the header record. It supersedes D-112's lens count and its one-reviewer docs-only mode. It annotates D-174, because Haiku gains a third review role. It passes D-108's door on its retained trigger, with a shipped defect for each new rule. For the ripple lens, this is README's `/hotfix` row, which M73 shipped still describing the old trigger and M74 fixed. For question (a), these are the pane races fixed after they shipped (M243, M255, M256, M260, M278). For question (b), this is the guest push that did not find the fork, which M234 fixed. The entry records the cost of a second push at the start of review, which starts `pull_request` CI again in a repo that has such CI. It names the rejected alternatives: a fourth lens on Opus, the ripple search inside the diff-bug lens, and leaving these misses to Copilot. Its falsifier reads one window: the first five reviews that run the ripple lens. If the lens gives no fixed finding in that window, the lens is removed. Otherwise, if Copilot finds stale text in the lens's domain that the lens missed on two or more of those PRs, the lens moves to Opus.
- [ ] AC6: The `verify` slot passes. That is both gating `unittest` suites (`scripts/tests`, `hooks/tests`), `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test` for the status mod.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks

- [x] T1: Reorder the Copilot arm (`skills/milestone-review/SKILL.md:142-157`) and edit step 8's header sentence (`:588-591`). Grep the skill and `skills/shared/copilot-review.md` for other sentences that put the header push at step 6.
- [ ] T2: Add the ripple reviewer to step 5: the routing bullets (`:287-294`), the lens list (`:305-338`), and the slug sentence (`:374-377`). Write its instruction in the shape of the prior-PR lens's bullet, with its own no-op clause.
- [ ] T3: Add the two questions to the diff-bug lens bullet (`:306-308`).
- [ ] T4: Edit tracking-rules "Model and agent strategy" (`skills/shared/tracking-rules.md:646-657`) and `README.md:629`. Run the AC4 sweep and fix each line it returns. Update `skills/tests/test_review_fanout.py`, which pins "three", and hand-run `python3 -m unittest discover -s skills/tests` (LESSONS M148).
- [ ] T5: Write the CHANGELOG Unreleased entry and the D-entry (D-185).
- [ ] T6: Run the `verify` slot.

## Work log

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: milestone — new review conduct in `/milestone-review` and the rulebook, with design choices.
- 2026-10-18: source: an analysis of Copilot's 91 threads on PRs 240 to 290. 32 threads named the header with no PR URL. 17 threads in 12 PRs named text left stale in another file or a later step. 5 PRs had await races in `hooks/status/register.tsx`. 13 threads named a procedure path not walked.
- 2026-10-18: collision check: D-108's door (new verification conduct needs a shipped defect) is passed on its trigger, with one shipped defect for each new rule (AC5). D-153 placed the header record at step 6, superseded in part. D-112 set the lens routing, superseded in part. D-174 moved the history lenses to Haiku, annotated. No candidate row overlaps. The parked row "Plan-gate clauses for standing instruments" names this case: its condition (a milestone proposes a standing instrument) holds, and this plan states a yield test and a removal falsifier (AC5) without adopting that row's general clauses. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-18: lessons harvested: M112 and M157 (grep the old wording, and DESIGN.md profile lists went stale) shape AC2 and AC4. M278 (cleanup across awaits) shapes AC3(a). M185 (sweep guest arms per remote command) shapes AC3(b). M148 (prose-guard pins) shapes T4.
- 2026-10-18: criteria audit (full): 12 findings, all fixed. AC1 now covers step 8's sentence, the failed header push, and a header that already names the PR. AC2 names the routing bullets, a no-op case, wider history exclusions, and that the lens ranks while the agent settles. AC3(b) says "at least these five paths". AC4's sweep gained patterns and files, and its pass condition no longer rests on the work log. AC5 supersedes D-112 instead of annotating it, names a shipped defect for each rule (it dropped M274's series sentence, which review had caught), records the second push's CI cost, and adds a move-to-Opus falsifier. The auto-review repo setting went to Out.
- 2026-10-18: question set: how to judge the ripple lens — the user restores Copilot, and the falsifier compares Copilot's stale-text threads on the next five reviewed PRs with the rate before (12 of 51 PRs).
- 2026-10-18: question set: ripple lens on internal docs-only reviews — both review modes, so those reviews get two reviewers.
- 2026-10-18: criteria audit (full) re-run on AC2, AC4, and AC5 after the question set changed them: 6 findings, all fixed. AC4's sweep gained `single-reviewer|one Opus`, and its pass condition reads only lines that state a lens or reviewer count. AC2 keeps `cairn/references/` in the search and skips dated measurements instead. AC5's ripple trigger is README's `/hotfix` row (M73 shipped it stale, M74 fixed it), not this repo's DESIGN.md. Its falsifier reads one five-review window, removal first. AC1 states the failed branch push and a header that names a closed PR.
- 2026-10-18: plan gate chose a separate Haiku ripple lens over adding the search to the Opus diff-bug lens, at the user's request, because a lens with its own evidence base finds what a shared base misses (step 5); falsified by Copilot stale-text threads in the lens's domain, missed by the lens, on two or more of its first five reviews.
- 2026-10-18: plan gate chose pushing the header commit before the Copilot request over telling Copilot to ignore the header in a `.github/copilot-instructions.md`, because the push fixes the record and adds no file to adopting repos; falsified by a header thread from Copilot on a PR whose header commit was on the remote before the request.
- 2026-10-18: implement started on branch m285-review-ripple-lens; the untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-18: T1: the Copilot arm now reports a failed branch push or create and requests nothing, adds a new PR's URL to the header (beside a closed PR's URL), and pushes that commit before the request; a failed header push leaves the commit for step 6. Step 8 cites D-185. No other sentence in the skill, `copilot-review.md`, `/hotfix`, or README placed the header push at step 6. The arm's `D-152, D-153` citation stays, because a hand-run guard pins it, and the arm cites D-185 inline.
