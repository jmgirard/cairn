# RB17: The Copilot review round's design (M231)

- **Date:** 2026-10-10
- **Output required:** write findings to `cairn/reviews/RR17-copilot-round-design.md`
- **Binding criteria:** not requested

You are performing an independent expert review. This brief is fully
self-contained. Do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

cairn is a Claude Code plugin. Its skills are markdown instructions that an
agent follows. `/hotfix` fixes a bug on a `hotfix-<slug>` branch and merges
on the user's approval. `/milestone-review` verifies a milestone and merges
on the user's approval at "the merge question". In owner mode (the operator
owns the repo) cairn merges. In guest mode (a `# Collaboration mode: guest`
line in `cairn/PROFILE.md`) the operator contributes to someone else's repo:
cairn opens the PR against the upstream repo at a "handoff" and never merges.
Decision D-138 opens the PR only after the user approves the merge, so CI
runs once on the head that merges.

The user's workflow, which milestone M231 builds into cairn: after a hotfix
or a milestone opens its PR, request a GitHub Copilot code review (Lite for a
hotfix, Balanced for a milestone), then "babysit" it: fix, reply to, and
resolve each Copilot comment. The user chose (D-152) that in an owner repo
the PR opens before the merge question so the round can run there. The opt-in
is a `# Copilot review: on` header line in `cairn/PROFILE.md`.

Facts already established:

- `gh pr edit <N> --add-reviewer @copilot` requests the review (gh 2.102.0).
  On 2026-10-10 neither the REST `requested_reviewers` endpoint nor the
  GraphQL `RequestReviewsByLoginInput` took a per-request level (Lite or
  Balanced), so GitHub's settings choose the level.
- Copilot's login is `copilot-pull-request-reviewer` in GraphQL and
  `copilot-pull-request-reviewer[bot]` in REST. A reply goes through REST
  `pulls/<N>/comments/<id>/replies` and creates an empty-body `COMMENTED`
  review by the replier. A resolve is the GraphQL `resolveReviewThread`
  mutation, whose only input is the thread id.
- A repo can turn on Copilot's automatic review of new PRs and of each push.
  Copilot's review body can list findings with no thread, and links to its
  own threads.
- The existing "PR-conversation read" (milestone-review step 7, from M177)
  reads every unresolved thread, every `COMMENTED` or `CHANGES_REQUESTED`
  review, and every conversation comment once before the merge question, and
  gives each a disposition. `/hotfix` step 6 reuses it, but offers the user
  four options per item where review's agent decides.

M231's review has run three passes with independent reviewers. Each pass
found load-bearing defects at the edges of the round, and each fix exposed
new ones: an endless wait when Copilot never reviews; resume routes keyed on
the newest line of an append-only work log; a stale "waiting" record that let
a re-review skip its own steps; a second pass requesting Copilot again; and
now an automatic Copilot review on PR open making the round wrongly report an
earlier pass and skip itself, a failing status query with no outcome, and a
hotfix decline leaving an open PR with no next command. The user removed the
timeout stop and all resume routes at the second return, and asked for this
independent review of the design at the third.

## Materials

Read on branch `m231-copilot-review-round` (use `git show
m231-copilot-review-round:<path>`, or read the working tree, which is on that
branch; do not check out other refs):

- `skills/shared/copilot-review.md` (whole file, about 124 lines): the round.
- `skills/milestone-review/SKILL.md`: step 2 (about lines 104–110), step 6
  and its "Copilot round arm" (about 394–415), step 7 including the
  "PR-conversation read (M177)" paragraph (about 417–520), and step 8's first
  paragraph and "Guest arm — the handoff sequence" (about 530–630).
- `skills/hotfix/SKILL.md`: step 1's first paragraph (about 33–45), step 5's
  "Authoring a fix" note (about 156–162), and step 6 including its "Copilot
  round arm" and "Guest arm — the handoff" (about 184–290).
- `skills/shared/tracking-rules.md`: "Waiting on CI and background work"
  (about lines 275–296), "Stops between the gates" (about 374–391), and
  "Collaboration mode" (about 297–341).
- `cairn/milestones/M231-copilot-review-round.md`: the Acceptance criteria,
  and the `## Review` section's pass 1, pass 2, and pass 3 findings with their
  dispositions. The `## Work log` records each choice and rejection.
- `cairn/DECISIONS.md`: D-138, D-147, and D-152 (find them with
  `grep -n '^### D-1\(38\|47\|52\)' cairn/DECISIONS.md` and read each whole).
- For the real API shapes, read-only queries are allowed, for example
  `gh api graphql` against `easystats/insight` PR 1253, which has a Copilot
  review with two resolved threads. Run no GitHub write of any kind.

## Questions

1. **Detection without state.** The round has no record it can trust across
   passes except the PR itself. Given manual requests, automatic Copilot
   reviews on PR open and on push, and later passes after a decline or a
   return, what signal on the PR should decide whether to request, wait, or
   read, and how does that signal tell "this round already handled these
   items" from "nobody has read them yet"? If no PR signal is reliable, say
   so and say what follows.
2. **Placement.** Would the round hold up better if it were not a separate
   step? For example: open the PR and request Copilot at the start of
   `/milestone-review`, so Copilot works in parallel with cairn's own
   verification and fan-out, and handle Copilot's items inside the existing
   PR-conversation read at step 7, with reply and resolve added as actions
   that read takes for Copilot items. Compare this with the current
   separate round on the edges listed in Background.
3. **The wait.** Is a blocking wait needed at all? If yes, what bound, what
   happens at the bound, and what happens to a review that arrives after it,
   given that the conversation read runs once and is not re-run?
4. **`/hotfix`.** The round arm opens the PR before the approval chip. A
   decline then leaves an open PR, and `/hotfix` has no re-entry for an open
   authored PR (a separate candidate row tracks that). Should the hotfix round
   run at all in owner mode, run only in guest mode, run with the PR opened
   only after approval, or something else? How should Copilot items fit
   hotfix's rule that the user chooses each item's disposition?
5. **Guest mode.** After the handoff the maintainers own the PR's merge.
   Should the guest round run in the same session after the handoff, be a
   separate later step, or be left to the operator? Consider the session's
   wait and the replies landing on the maintainers' repo.
6. **Failure modes.** For whichever design you recommend, state what happens
   when the request fails, the status query errors, Copilot never reviews, a
   review links body findings to its own threads, several Copilot reviews
   exist, and a Copilot finding shows an acceptance criterion failing.
7. **Scope and criteria.** Read M231's acceptance criteria. Which should
   change under your design? Name the smallest version of M231 worth
   shipping, and list what could move to later work, including removal of
   the automated reply and resolve if the design is simpler without them.

## Constraints

- IP1: nothing reaches the default branch without the user's explicit
  approval at the merge question; the merge guard checks a marker file that
  only the approval writes. D-147 removed an up-front merge approval and
  keeps the merge question as the only gate for a milestone merge.
- D-152 (the user's choice): in an owner repo that opts in, the PR opens
  before the merge question. You may recommend a different placement within
  that, or argue against it explicitly.
- The user wants the round unattended: Copilot items are fixed, answered, and
  resolved without a question per item, and replies to bots carry no thanks.
- Guest mode never commits `cairn/` files and carries no cairn vocabulary
  (milestone ids, criterion or task labels, decision ids) into anything the
  maintainers see.
- The tracking-rules wait rule: one watcher per wait, and no watcher left
  armed at a commit or turn end.
- Flag disagreement with a constraint explicitly rather than working around it.

## Output format

In `RR17-copilot-round-design.md`: answer each question by number with your
reasoning and evidence (file:line where it matters); list any additional
findings separately under "Beyond the brief"; end with concrete
recommendations, each marked apply / consider / reject-with-reason. Your
report is advisory: emit a `## Binding criteria` section ONLY if this brief's
header slot says `requested`. It says `not requested`, so do not emit one.
