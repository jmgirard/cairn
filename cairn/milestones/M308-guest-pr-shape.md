# M308: Fit guest PRs to the host and to one change

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes the text, names, scope, and PR body of guest-mode contributions
- **Branch/PR:** —

## Goal

In guest mode, a contribution follows the host's writing and naming and holds one change.

## Scope

**In:** Four guest-mode rules, from maintainer review on easystats PRs. First, the host's length, tone, and detail
win over other writing-style instructions for host text (datawizard #726 and #730). Second, new names reuse the
host's names (performance #973, bayestestR #793). Third, the plan holds one change and checks for deliberate
maintainer behavior and proposed approaches (bayestestR #797 and #794, datawizard #730). Fourth, the PR body maps
each failure an issue reports (datawizard #725). A D-entry supersedes D-161's order clause and its rejection.

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
- [ ] AC6: In guest mode, `skills/milestone-review/SKILL.md` step 8 and both PR-create sites of
      `skills/hotfix/SKILL.md` say this: when an issue that the PR closes reports more than one failing call or error,
      the PR body names each one and says whether the PR fixes it.
- [ ] AC7: In guest mode, `skills/milestone-review/SKILL.md` step 8 says that the PR body gives the reason when the
      work log records a maintainer's proposed approach that the plan did not take.
- [ ] AC8: The `verify` slot of `cairn/PROFILE.md` is green at the branch head: its five commands, each exit code
      checked.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T3
- AC6 → T4
- AC7 → T4
- AC8 → T5

## Tasks

- [ ] T1: Edit the "Collaboration mode" section of `skills/shared/tracking-rules.md` (the host-text bullet near line
      405) for AC1, and add the names bullet after it for AC3.
- [ ] T2: Edit the guest-mode text in `hooks/session_context.py` (near line 380) and README.md's guest bullet (near
      line 1044). Change the assertion in `hooks/tests/test_hooks.py` (near line 398) to the new order.
- [ ] T3: Add the guest scope rule to `skills/milestone-plan/SKILL.md`, beside the idea vet and the step 4 Scope
      bullets, for AC4 and AC5.
- [ ] T4: Edit `skills/milestone-review/SKILL.md` step 8's guest arm and both `gh pr create` sites in
      `skills/hotfix/SKILL.md` for AC6 and AC7.
- [ ] T5: Append a D-entry that supersedes D-161's order clause and its rejection, on the user's choice at this plan's
      question set. Its trigger is D-161's own falsifier, met on datawizard #726. Run the five `verify` commands.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — four guest-mode rule changes and a superseded decision.
- 2026-10-21: idea vet: two concerns. Reversing the M247 style choice: answer, host style wins. One change per PR can raise the number of PRs: answer, build it.
- 2026-10-21: question set: host style — host style wins; the user excludes guest checkouts from the simple-english lint.
- 2026-10-21: question set: guest PR scope — one change per PR, side fixes as candidate rows.
- 2026-10-21: plan gate chose host style winning over keeping D-161's order, at the user's choice; falsified by a guest PR whose maintainers ask for plainer or longer text than the host's own.
- 2026-10-21: criteria audit (full, fresh Opus reader): for M308, added the superseding D-entry (T5) and the hook test change (AC2); moved the names rule to its own bullet (AC3); made AC6 and AC7 skill rules in guest mode, named both hotfix sites, and kept the why-not rule to review; dropped the prose-guard criterion per D-109; cited the verify slot in full.
- 2026-10-21: collision check: D-161 superseded in part (T5); D-137 and D-139 stand; D-204's idea vet gains the deliberate-behavior concern.

## Decisions

## Review
