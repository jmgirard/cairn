# M332: Write host text so a maintainer follows it

- **Status:** planned
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the skills' instructions decide what adopters' sessions post under their accounts
- **Branch/PR:** —

## Goal

Text a session writes for another person reads clearly on one read, because the rules ask for that and stop prescribing a shape for it.

## Scope

**In:**
- `skills/shared/tracking-rules.md`, the guest host-text bullet, and the guest session-start text in `hooks/session_context.py`: add one clarity test that comes before matching the host's length.
- `skills/shared/copilot-review.md` §5: remove the fixed opening, the outcome for every note and body item, the paragraph-or-list rule, and the example comment. Keep the review link, which later runs read.
- `skills/copilot-review/SKILL.md`, `README.md`, and `CHANGELOG.md`: follow §5.
- `skills/milestone-plan/SKILL.md`, "The maintainer question": remove the three-part draft shape.
- `skills/milestone-review/SKILL.md` step 8 and `skills/hotfix/SKILL.md` guest handoff: "short" holds only where the text stays clear.
- The hand-run guards in `skills/tests` that pin the removed wording.

**Out:**
- A checker, lint, or scored test of prose quality: none, because clarity is a judgment for the writer and the user at the draft chip.
- The simple-english lint hook: the user's `SIMPLE_ENGLISH_LINT_EXCLUDE` setting now skips these drafts, a change outside this repo made on 2026-11-02.
- The workspace `CLAUDE.md` in the easystats folder: the user's own file.
- The edges left in the parked row "Tighten the Copilot draft step edges": they stay there, and the plan commit removed only the paragraph-or-list rule from that row.
- Owner-mode PR bodies: no rule prescribes their shape, and no complaint names one.
- The guest PR body's content rules (`/milestone-review` step 8's "leads with", `/hotfix`'s order) and the outside-demand draft's line in `/milestone-plan`: they stay, because maintainers' complaints about long PR bodies set them (D-207), and no complaint today names them. Promote to a candidate row if the merge question's PR body draft shows them doing harm.

## Acceptance criteria

- [ ] AC1: The host-text bullet in `skills/shared/tracking-rules.md` requires the session to check, before it commits, shows, or posts such text, that a maintainer who has not seen the session can tell on one read what the text says and anything it asks, and it says this comes before matching length, tone, and level of detail. `git diff --word-diff=porcelain main -- skills/shared/tracking-rules.md` shows no removed word in the bullet.
- [ ] AC2: The guest session-start text from `hooks/session_context.py` states the same test, and a test in `hooks/tests/test_hooks.py` fails without that sentence.
- [ ] AC3: `skills/shared/copilot-review.md` §5 states, in every mode and before host matching, that someone who has not seen the session can tell on one read what the comment says. It keeps "ordinary sentences", requires the review's `url` as a markdown link in the comment, and requires the comment to name any note a person reading the PR could ask about. It states no position for the link, no opening phrase, no outcome for every note, no paragraph-or-list rule, and no example comment. It keeps "never thanks Copilot", "asks no question", and no cairn vocabulary in guest mode. Its line on a body item no longer says the comment answers that item. §6 still reports each note's disposition to the user.
- [ ] AC4: `git ls-files skills/shared skills/copilot-review README.md | xargs cat | tr -s ' \n' ' ' | grep -E "every note's outcome|each note's outcome|On \[Copilot's review\]|opens with a link|states facts only|answered in the review's comment"` finds nothing. The two Unreleased Copilot entries in `CHANGELOG.md` state the review link and the clarity test, and neither says that the comment covers every note or body note.
- [ ] AC5: "The maintainer question" in `skills/milestone-plan/SKILL.md` no longer says which points the draft must contain. It still says that the draft asks as a question, follows the rulebook's host-text bullet, and carries no cairn vocabulary.
- [ ] AC6: `skills/milestone-review/SKILL.md` step 8's guest body sentence and `skills/hotfix/SKILL.md`'s guest body sentence each tie "short" to the text staying clear, and each still requires the host's style.
- [ ] AC7: The profile's `verify` slot passes on the branch head, and `python3 -m unittest discover -s skills/tests` exits 0.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3, T4
- AC5 → T5
- AC6 → T6
- AC7 → T7, T8

## Tasks

- [ ] T1: Add the clarity test to the host-text bullet in `skills/shared/tracking-rules.md`. Re-seed the rulebook's mass baseline at all three sites.
- [ ] T2: Add the sentence to the guest session-start text, with its test in `hooks/tests/test_hooks.py`.
- [ ] T3: Rewrite §5's comment rule, its body-item line, and its line on a note settled on an earlier pass in `skills/shared/copilot-review.md`. Write D-236: it supersedes D-235's opening and every-note clauses and its paragraph-or-list rule, narrows D-187's "answers its summary" and D-212's record clause, and annotates D-207.
- [ ] T4: Follow §5 in `skills/copilot-review/SKILL.md` (description and step 6), `README.md` (the two Copilot sites and the host-text line near :1133), and `CHANGELOG.md` (the two Unreleased Copilot entries).
- [ ] T5: Remove the three-part shape from "The maintainer question".
- [ ] T6: Tie "short" to clarity in `/milestone-review` step 8 and `/hotfix`'s guest handoff.
- [ ] T7: Update the guards in `skills/tests/test_copilot_review_round.py` and `skills/tests/test_mutation_harness.py` that pin removed wording. Add no new guard for the clarity test's wording beyond the one in AC2.
- [ ] T8: Run the suites. Give a fresh subagent the new rules and the facts of three real cases, then put its drafts in the merge question so the user can judge them: a Copilot comment (bayestestR#800), a maintainer question (bayestestR#431), and a guest PR body (bayestestR#801).

## Work log

- 2026-11-02: tier check: milestone — changes what the skills tell sessions to write, with a choice about which rules to remove.
- 2026-11-02: idea vet: gap — a resolved thread with no mention could puzzle a reader; reading taken: the comment names a note someone reading the PR could ask about, and the user asked to remove the every-note rule. No flaw.
- 2026-11-02: lessons used: 2026-07-24 (M112) grep the old phrasing across the surface; 2026-08-17 (M149) re-seed the rulebook baseline; 2026-08-17 (M148) guards near edited prose; 2026-08-22 (M152) a repair that changes a decision owes a D-entry; 2026-11-02 (M331) write checks from the criterion's words.
- 2026-11-02: question set: none posed — the user chose the scope ("Yes, fix both") after the diagnosis, and no open choice is the user's alone.
- 2026-11-02: collision: M331 done today and D-235 set the form this removes; the plan supersedes those clauses at the user's request. D-207 stands, annotated. The row "Tighten the Copilot draft step edges" narrows, because the paragraph-or-list rule it names goes away.
- 2026-11-02: approach: remove shape rules and add one clarity test. Rejected: a new example comment, because M331's example became the opening of every later comment (see bayestestR#800, parameters#1292, datawizard#738). Falsified by drafts that the user still calls unclear after this ships, which would point at the model's habits and not at the rules.
- 2026-11-02: approach: no prose checker. Rejected: a lint for stock phrases, because the checker spiral costs more than it catches, and clarity is a judgment. Falsified by the same stock phrase recurring across many drafts after this ships.
- 2026-11-02: checkpoint: the plan is committed with its full criteria audit still running; the audit's findings and dispositions land in a later line, and implement does not start before them.
- 2026-11-02: criteria audit (full): 10 findings. Taken: owner rounds lost the shape rules with no test (AC3); AC4's grep missed wrapped text; AC3 required nothing positive; AC1's wording placed no duty; AC4's CHANGELOG clause was uncheckable; AC1's diff could not tell a rewrap from a removal; AC5 passed a reorder; README's host-text line and T3's D-212 clause. Rejected: a new AC8 for the merge-question drafts, because showing them binds an instrument, so T8 stays a task, widened to a PR body. Kept out with a reason: the guest PR body's content rules (Scope Out). The baseline re-seed stays in T1 with no AC. The row edit landed in the plan commit.

## Decisions

## Review
