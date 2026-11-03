# M332: Write host text so a maintainer follows it

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the skills' instructions decide what adopters' sessions post under their accounts
- **Branch/PR:** m332-clear-host-text https://github.com/jmgirard/cairn/pull/347

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

- [x] AC1: The host-text bullet in `skills/shared/tracking-rules.md` requires the session to check, before it commits, shows, or posts such text, that a maintainer who has not seen the session can tell on one read what the text says and anything it asks, and it says this comes before matching length, tone, and level of detail. `git diff --word-diff=porcelain main -- skills/shared/tracking-rules.md` shows no removed word in the bullet.
- [x] AC2: The guest session-start text from `hooks/session_context.py` states the same test, and a test in `hooks/tests/test_hooks.py` fails without that sentence.
- [x] AC3: `skills/shared/copilot-review.md` §5 states, in every mode and before host matching, that someone who has not seen the session can tell on one read what the comment says. It keeps "ordinary sentences", requires the review's `url` as a markdown link in the comment, and requires the comment to name any note a person reading the PR could ask about. It states no position for the link, no opening phrase, no outcome for every note, no paragraph-or-list rule, and no example comment. It keeps "never thanks Copilot", "asks no question", and no cairn vocabulary in guest mode. Its line on a body item no longer says the comment answers that item. §6 still reports each note's disposition to the user.
- [x] AC4: `git ls-files skills/shared skills/copilot-review README.md | xargs cat | tr -s ' \n' ' ' | grep -E "every note's outcome|each note's outcome|On \[Copilot's review\]|opens with a link|states facts only|answered in the review's comment"` finds nothing. The two Unreleased Copilot entries in `CHANGELOG.md` state the review link and the clarity test, and neither says that the comment covers every note or body note.
- [x] AC5: "The maintainer question" in `skills/milestone-plan/SKILL.md` no longer says which points the draft must contain. It still says that the draft asks as a question, follows the rulebook's host-text bullet, and carries no cairn vocabulary.
- [x] AC6: `skills/milestone-review/SKILL.md` step 8's guest body sentence and `skills/hotfix/SKILL.md`'s guest body sentence each tie "short" to the text staying clear, and each still requires the host's style.
- [x] AC7: The profile's `verify` slot passes on the branch head, and `python3 -m unittest discover -s skills/tests` exits 0.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3, T4
- AC5 → T5
- AC6 → T6
- AC7 → T7, T8

## Tasks

- [x] T1: Add the clarity test to the host-text bullet in `skills/shared/tracking-rules.md`. Re-seed the rulebook's mass baseline at all three sites.
- [x] T2: Add the sentence to the guest session-start text, with its test in `hooks/tests/test_hooks.py`.
- [x] T3: Rewrite §5's comment rule, its body-item line, and its line on a note settled on an earlier pass in `skills/shared/copilot-review.md`. Write D-236: it supersedes D-235's opening and every-note clauses and its paragraph-or-list rule, narrows D-187's "answers its summary" and D-212's record clause, and annotates D-207.
- [x] T4: Follow §5 in `skills/copilot-review/SKILL.md` (description and step 6), `README.md` (the two Copilot sites and the host-text line near :1133), and `CHANGELOG.md` (the two Unreleased Copilot entries).
- [x] T5: Remove the three-part shape from "The maintainer question".
- [x] T6: Tie "short" to clarity in `/milestone-review` step 8 and `/hotfix`'s guest handoff.
- [x] T7: Update the guards in `skills/tests/test_copilot_review_round.py` and `skills/tests/test_mutation_harness.py` that pin removed wording. Add no new guard for the clarity test's wording beyond the one in AC2.
- [x] T8: Run the suites. Give a fresh subagent the new rules and the facts of three real cases, then put its drafts in the merge question so the user can judge them: a Copilot comment (bayestestR#800), a maintainer question (bayestestR#431), and a guest PR body (bayestestR#801).

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
- 2026-11-02: T1-T7 done in one checkpoint, since the guards, the baseline, and the wording move together: clarity check in the bullet and session-start text, §5 rewritten, surfaces followed, D-236 written, baseline re-seeded to 894 lines / 88,613 bytes. The simple-english hook flagged older text across the edited files; those hits stay as M331 left them. Unrelated untracked cairn-probe.log and tsconfig.json stay unstaged.
- 2026-11-02: claim audit: 45 claims read, 1 corrected — CHANGELOG.md (an older Unreleased line still said a guest PR body is short); re-read by the same reader.
- 2026-11-02: T8: suites green (mod test 2466 pass); a fresh subagent wrote drafts of a Copilot comment (bayestestR#800), a maintainer question (#431), and a PR body (#801), held in the session scratchpad for the merge question; nothing was posted.
- 2026-11-02: step-7 approval: m332-clear-host-text approved for merge

## Decisions

## Review

- AC1: the flattened bullet holds the sentence once; `git diff --word-diff=porcelain main...HEAD` on the file shows 0 removed words.
- AC2: `test_guest_mode` passes, and fails with the sentence removed from `hooks/session_context.py` (restored, tree clean).
- AC3: §5 holds the clarity sentence, "first in every mode", ordinary sentences, the link, "Name any note", no thanks, no question, no cairn vocabulary; holds none of "Open with", "Up to three", "four or more", "For example", "Give every". The body-item line reads "takes a disposition". §6 keeps its `copilot:` report line.
- AC4: the flattened grep over the named paths counts 0. Both Unreleased Copilot entries state the link and the on-one-read test, and "gives each note's outcome" and "cover body notes" count 0 in the Unreleased section.
- AC5: the paragraph states no list of points, and keeps the host-text bullet, no cairn vocabulary, and "asks as a question".
- AC6: `/milestone-review` step 8 and `/hotfix` each say "short only where that leaves it clear" and name the host's style.
- AC7: scripts, hooks, and skills suites exit 0; both plugin validates exit 0 with no version warning; `claude plugin test` 2466 pass, 0 fail; `cairn_validate` exit 0. The changelog has an entry with no milestone number.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: "short only where clear" dropped the duty to be short — fix now (also blame-history #1, prior-review #3), now "short unless that costs clarity"; D-236 names the narrowing.
- diff-bug #2: fixes had no naming rule, and a review with no named note had no content — fix now, §5 names each fix and allows one sentence when none needs naming.
- diff-bug #3: the check had no action on failure — fix now, "rewrites text that fails it" in the bullet and session-start text.
- diff-bug #4: D-236 did not address D-108's door — fix now (also blame-history #3).
- diff-bug #5: the check against a host's written style was undecided — fix now, D-236 ranks the check first.
- diff-bug #6: the one-line close comment is unranked — reject, false: rule (3)'s one line is its own rule, not host matching, and a one-line comment can pass the check.
- diff-bug #7: a typed edit posts unchecked — reject, false: typed text is the user's own act.
- diff-bug #8: the restored link has no stated place — reject, style (also prior-review #5): the detection reads it anywhere.
- diff-bug #9: README and CHANGELOG did not say a thread can resolve with no mention — fix now.
- diff-bug #10: the guest-tone test no longer pinned "guest" — fix now (also blame-history #6).
- diff-bug #11: most changelog claims have no guard — reject, planned change (also prior-review #4): T7 adds none, per the hand-run guards decision (D-109).
- diff-bug #12: D-236 narrowed a clause already gone — fix now (also blame-history #2), the heading names the live clauses.
- diff-bug #13: the settled-note sentence lacked "named" — fix now.
- diff-bug #14: D-236 was looser than §5 — fix now.
- diff-bug #15: an unnamed note's reason lives only in the report — reject, planned change (also prior-review #1): D-236 accepts it at the user's request.
- diff-bug #16: a comment citing another review's URL marks it answered — follow-up, pre-existing, parked row "Tighten the Copilot draft step edges", because no documented use reaches it.
- diff-bug #17: the hook's "any other instruction" could cover the check — reject, false: the next sentence ranks the check first.
- diff-bug #18: D-236's title overstated the scope — fix now.
- diff-bug #19: the bullet did not cite D-236 — fix now, cited at the new sentence.
- diff-bug #20: "can follow" against "tell" — reject, style.
- diff-bug #21: "tone and length" against the rulebook's wording — reject, style.
- diff-bug #22: T8's drafts not yet in the merge question — reject, false: they go in this review's merge question.
- diff-bug #23: test comment and docstring nits — fix now for the docstring (also blame-history #5); reject the comment, style.
- diff-bug #24: cosmetic wrapping — fix now for the long CHANGELOG line (also blame-history #8, prior-review #6, ripple); reject the rest, style.
- blame-history #4: D-233 not named for the removed points — reject, false: D-233 did not set those points.
- blame-history #7: D-161's "Owner mode is unchanged" — reject, false: that clause covers host matching, and the owner-mode Copilot comment is not host text.
- prior-review #2: the question loses its content list — reject, planned change (AC5).
- prior-review #7: the baseline re-seed — reject, false: the rule allows one after a deliberate change.
- ripple #1: an older Unreleased entry omits the check — reject, false: the new top entry states it.
- ripple #2: the module's budget header credits D-235 — reject, false: a dated record of the reset.
- ripple #3: "once every note has an outcome" — fix now, now "is settled".
- ripple (inside diff): the top CHANGELOG entry said guest mode only, while §5 binds every mode — fix now.
- copilot: review body — rejected, not a problem: the clarity bullet sits in the rulebook's guest-mode list.
- Copilot level: Balanced was asked; the review body names none in the part read, GitHub's settings choose it.
