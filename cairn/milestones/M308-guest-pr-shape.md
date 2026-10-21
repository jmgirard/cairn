# M308: Fit guest PRs to the host and to one change

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes the text, names, scope, and PR body of guest-mode contributions
- **Branch/PR:** m308-guest-pr-shape

## Goal

In guest mode, a contribution follows the host's writing and naming and holds one change.

## Scope

**In:** Four guest-mode rules, from maintainer review on easystats PRs. First, the host's length, tone, and detail
win over other writing-style instructions for host text (datawizard #726 and #730). Second, new names reuse the
host's names (performance #973, bayestestR #793). Third, the plan holds one change and checks for deliberate
maintainer behavior and proposed approaches (bayestestR #797 and #794, datawizard #730). Fourth, the PR body maps
each failure an issue reports (datawizard #725). A D-entry supersedes D-161's order clause and its rejection.
Folded at implement from the row "Write short guest PR bodies and replies" (modelbased #698): the guest PR body is
short, styled on maintainers' PR bodies, and `/milestone` §2 names unanswered maintainer comments on a blocked
guest PR, with a reply rule.

**Out:** Owner-mode text and PR bodies stay as they are. The simple-english plugin's lint is the user's to exclude
for guest checkouts with `SIMPLE_ENGLISH_LINT_EXCLUDE`, because cairn writes nothing outside `cairn/`. Merge conflicts
between open guest PRs go to M309.

## Acceptance criteria

- [ ] AC1: In `skills/shared/tracking-rules.md`, the guest-mode bullet "Text written for the host matches the host's
      own" says that host matching wins over another writing-style instruction in the session for host text. It says
      that the other instruction governs only what host matching leaves open.
- [ ] AC2: `hooks/session_context.py`'s guest-mode text and README.md's guest-mode bullet state the AC1 order. The
      `hooks/tests` assertion on that text checks the new order.
- [ ] AC3: `skills/shared/tracking-rules.md` gains a guest-mode bullet. It says that a new name in host code (an
      argument, a function, or a file) reuses the name that the host already uses for the same thing, read from the
      host's code before the name is chosen.
- [ ] AC4: `skills/milestone-plan/SKILL.md` gains a guest-mode rule. Scope In holds only the change that the request or
      issue asks for. Each other fix or feature that the investigation finds becomes a candidate row for its own PR.
- [ ] AC5: The AC4 rule also says two things. When the issue's comments or the code's git history show that a
      maintainer chose the changed behavior on purpose, the idea vet poses that as a concern. When a maintainer
      proposed an approach in the issue's comments, the plan takes it or writes a work-log line that says why not.
- [ ] AC6: In guest mode, `skills/milestone-review/SKILL.md` step 8 and the guest PR-create site of
      `skills/hotfix/SKILL.md` say this: when an issue that the PR closes reports more than one failing call or error,
      the PR body names each one and says whether the PR fixes it.
- [ ] AC7: In guest mode, `skills/milestone-review/SKILL.md` step 8 says that the PR body gives the reason when the
      work log records a maintainer's proposed approach that the plan did not take.
- [ ] AC8: In guest mode, `skills/milestone-review/SKILL.md` step 8 says that the PR body takes its host style from PR
      bodies whose author's association is OWNER, MEMBER, or COLLABORATOR, never from the operator's own PRs. The body
      leads with what changed for users, at most one usage example apart from the failing calls that AC6's rule
      names, and the points a maintainer must decide. Beyond the other items step 8 requires, AC6's and AC7's
      included, review evidence, internal function names, and test lists stay in `cairn/`.
- [ ] AC9: In guest mode, the `OPEN`-otherwise arm of `skills/milestone/SKILL.md` §2's route for a blocked PR also
      reads the conversation comments and review bodies that `gh pr view <N> --repo <base-repo> --json
      comments,reviews` returns. Its report names each one whose author is not the PR's author, has the association
      OWNER, MEMBER, or COLLABORATOR, and is followed in time by no comment or review by the PR's author. It says that
      the operator's reply to such a comment leads with the answer or the question at about the comment's length,
      with probe evidence left in `cairn/`.
- [ ] AC10: The `verify` slot of `cairn/PROFILE.md` is green at the branch head: its five commands, each exit code
      checked.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T3
- AC6 → T4
- AC7 → T4
- AC8 → T4
- AC9 → T5
- AC10 → T6

## Tasks

- [x] T1: Edit the "Collaboration mode" section of `skills/shared/tracking-rules.md` (the host-text bullet near line
      405) for AC1, and add the names bullet after it for AC3.
- [x] T2: Edit the guest-mode text in `hooks/session_context.py` (near line 380) and README.md's guest bullet (near
      line 1044). Change the assertion in `hooks/tests/test_hooks.py` (near line 398) to the new order.
- [x] T3: Add the guest scope rule to `skills/milestone-plan/SKILL.md`, beside the idea vet and the step 4 Scope
      bullets, for AC4 and AC5.
- [x] T4: Edit `skills/milestone-review/SKILL.md` step 8's guest arm for AC6, AC7, and AC8, and the guest
      `gh pr create` site in `skills/hotfix/SKILL.md` for AC6, rewording its "the changelog entry is the branch's only
      prose" note.
- [ ] T5: Edit the `OPEN`-otherwise arm of `skills/milestone/SKILL.md` §2's blocked-PR route for AC9.
- [ ] T6: Append a D-entry that supersedes D-161's order clause and its rejection, on the user's choice at this plan's
      question set. Its trigger is D-161's own falsifier, met on datawizard #726. Add the CHANGELOG entry. Run the
      five `verify` commands.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — four guest-mode rule changes and a superseded decision.
- 2026-10-21: idea vet: two concerns. Reversing the M247 style choice: answer, host style wins. One change per PR can raise the number of PRs: answer, build it.
- 2026-10-21: question set: host style — host style wins; the user excludes guest checkouts from the simple-english lint.
- 2026-10-21: question set: guest PR scope — one change per PR, side fixes as candidate rows.
- 2026-10-21: plan gate chose host style winning over keeping D-161's order, at the user's choice; falsified by a guest PR whose maintainers ask for plainer or longer text than the host's own.
- 2026-10-21: criteria audit (full, fresh Opus reader): for M308, added the superseding D-entry (T5) and the hook test change (AC2); moved the names rule to its own bullet (AC3); made AC6 and AC7 skill rules in guest mode, named both hotfix sites, and kept the why-not rule to review; dropped the prose-guard criterion per D-109; cited the verify slot in full.
- 2026-10-21: collision check: D-161 superseded in part (T5); D-137 and D-139 stand; D-204's idea vet gains the deliberate-behavior concern.
- 2026-10-21: in-progress; branch m308-guest-pr-shape cut from main at ec99e5a4. Untracked cairn-probe.log and tsconfig.json left unstaged.
- 2026-10-21: the user chose at a chip to fold the candidate row "Write short guest PR bodies and replies" into M308, as the row asked; amendment held for its re-audit.
- 2026-10-21: T1 done: host-text bullet now says host matching wins and samples maintainers' text, never the operator's; new names bullet after it. The new D-entry is D-207 (cited ahead of T6). The simple-english lint hook reports 522 hits over the whole rulebook, nearly all older than this edit; left as is.
- 2026-10-21: re-audit: AC6 (full) — no wording finding; hotfix's "the changelog entry is the branch's only prose" note conflicts with a failure map in the guest body, so T4 rewords it. "Closes" kept over "Refs" as the narrower promise.
- 2026-10-21: re-audit: AC9 (full) — read as a full content list it contradicts D-206's edge list and AC6/AC7; "one example" read as exactly one. Reworded: "leads with", "at most one example", "beyond the items step 8 already requires".
- 2026-10-21: re-audit: AC10 (full) — "reports" ambiguous, no read named, "maintainer" undefined, arm unclear. Reworded to the OPEN-otherwise arm, a named read, OWNER/MEMBER/COLLABORATOR, and an unanswered-comment test.
- 2026-10-21: re-audit: AC9 (full) — "one example" clashes with AC6's named failing calls; "already" reads two ways; maintainers undefined; "what changed for users" has no answer for a CI-only PR (answered: guest PRs here change user-facing behavior; the body says what changed where users see nothing).
- 2026-10-21: re-audit: AC10 (full) — inline review comments fall outside `gh pr view --json comments,reviews`; the PR's author can be a MEMBER; "later" reads two ways. Second re-audit on AC9 and AC10: stop for the user on the final wording.
- 2026-10-21: T2 done: hook guest line and README guest bullet state that host matching wins and samples maintainers' text; README gains the names bullet; hook test asserts the new order and the old phrase's absence (failed before the hook edit, passes after). Verify: five commands exit 0.
- 2026-10-21: substantive amendment: the user accepted the final AC9/AC10 wording at the stop. Scope In gains the folded row; AC6 names the one guest hotfix create site; new AC8 (short guest PR body) and AC9 (maintainer-comment route and reply rule); the verify criterion is renumbered AC10; T4 widened, new T5 for `/milestone` §2, the D-entry task renumbered T6 and gains the CHANGELOG entry. The re-audit lines above that name AC9 and AC10 refer to what are now AC8 and AC9; both have had their two re-audits.
- 2026-10-21: T3 done: a "Guest scope" paragraph after step 2's idea vet holds Scope In to the asked change, sends side finds to candidate rows, reads issue comments and git history for deliberate behavior (posed as a vet concern), and takes a maintainer's proposed approach or writes the fixed-shape line `maintainer approach: <approach> — not taken: <reason>`, chosen so review step 8 can read it. Verify: five commands exit 0.
- 2026-10-21: T4 done: step 8's guest arm gains a body paragraph (maintainer PR bodies read through `gh api .../pulls` filtered on `author_association` and the operator's login, since `gh pr list` has no association field; lead content; failure map from `gh issue view`; the `maintainer approach:` reason; what stays in `cairn/`). Hotfix's guest create gains the failure map, and its "only prose" note is reworded. Verify: five commands exit 0.

## Decisions

## Review
