# RR16: When may review skip the merge question under an up-front approval? (M203)

- **Date:** 2026-10-03
- **Brief:** `cairn/reviews/RB16-up-front-merge-state.md`
- **Read at:** commit `1ce9749` on `m203-merge-approval-up-front`. The
  working tree at `74a2997` differs only in the brief, the ROADMAP, and the
  milestone's status line.
- **Mode:** advisory. The brief's header says `not requested`.

Materials read in the brief's order: the M203 file whole. Review skill
lines 41-97, 300-620, 720-784. Rulebook lines 215-276 and 380-430.
`merge_guard.py` whole. `cairn_common.py` lines 295-480.
`TestMergeGuardUpFront` (19 tests, run: OK). D-043, D-138, D-144, D-145.
RR15 questions 2, 4, 5, 6 and its recommendations. Plan skill lines
140-170 and 320-345. Implement skill lines 100-150 and 225-260.
`git diff main...HEAD` (19 files, +1577/-89, 27 commits).

Vocabulary: "check" is used below for every test of a fact. The repo's
`verify` slot is named only in a code span.

## 1. Root cause

Each pass finds new defects for two reasons. The skip is decided by reading
an append-only prose log through predicates that were never fixed as a set.
And one fact, the approval line, is keyed four ways by four readers.

The state the skip depends on, where each piece lives, and who writes and
reads it:

| # | Fact | Lives in | Writer | Readers |
|---|------|----------|--------|---------|
| 1 | `Merge approval:` slot | default branch, plan commit | plan step 4 | review step 7 reads a git-root path. The guard reads a cairn-root path and resolves `<base>/HEAD`, else `main`, else `master`. |
| 2 | plan commit sha | git, newest `plan …` subject with the id | plan step 6 | step 7 cites step 10's recipe, which prints subjects only. |
| 3 | plan-owned text unchanged | derived from a diff against #2 | none | step 7 |
| 4 | route-back lines (four prefixes) | work log | implement step 6, review steps 5, 7, 8 | step 7 |
| 5 | ticks with evidence | AC block and Review section | review step 3 | step 7 |
| 6 | finding lines with lens, rank, disposition | Review section | step 5 | step 7 reads "no fix-now left unfixed". Nothing records that a fix landed. |
| 7 | `spawned:` line, "written by this pass" | Review section | step 5, with no pass id | step 7 |
| 8 | header slots (IP, `Resolves:`, `companion:`), guest mode | header, PROFILE | plan | step 7 |
| 9 | `### D-` added on the branch | derived from `git diff` | none | step 7 |
| 10 | the up-front approval line | work log, in its own commit | step 7 | route (a) by prefix. Route (c) by the newest approval line. Step 8's arm by any up-front line. The end-of-run list by any. The late-push pickaxe by the phrase in any commit. |
| 11 | PR head oid, check state, conversation items | GitHub | none | step 8, route (c) |
| 12 | base oid at evidence time | nowhere | nobody | route (c) compares "moved" against nothing recorded. |
| 13 | pass identity | nowhere (free-text `Pass 2 (…)` lines) | nobody | step 7 for #7, route (c) |
| 14 | marker `cairn/.merge-approved` | disk, gitignored | step 8 | guard |

Each pass found a defect where a reader and a writer disagree:

- Fact 10 is the worst. Four readers key the same line four ways. After a
  route-back, the chip approval appends `approved for merge`. Route (c)
  reads "newest" and goes to the chip. Step 8 reads "any up-front line" and
  runs the up-front arm. Its late-push check then fails, because the PR
  head is now the chip-approval commit (pass 3 diff-bug #1). The pickaxe
  keys on a phrase that this milestone's own Review section quotes (blame
  #4).
- Facts 7 and 13: the reader wants "this pass". No writer records a pass.
  M203's pass 3 appended `— pass 3` to its `spawned:` line by hand.
- Fact 6: the reader wants "fixed". No writer records a fix.
- Fact 12: the reader wants "moved since". No writer records a base oid.
- Fact 1: two readers resolve the default branch and the path differently
  (pass 3 diff-bug #6, blame #3).
- The route-back list is written by hand in six places: D-145, the
  rulebook bullet, review step 7, README, CHANGELOG, and the plan question.
  IP1's text delegates to "the cases the rulebook lists". T9 added three
  cases to the rulebook that D-145 does not list: a moved default branch,
  a `spawned:` line not from this pass, and any PR-conversation item. Ten
  of the 44 pass-2 and pass-3 findings are one surface lagging another.

The 44 findings of passes 2 and 3 sort into six classes. Nine are resume,
re-entry, or line keying (pass 2 diff #1-#3, blame #2, #7. Pass 3 diff
#1-#3, blame #4). Five are writer/reader line shapes (pass 2 diff #4, #7.
Pass 3 diff #4, #5, blame #6). Ten are enumeration sync across surfaces.
Thirteen are guard internals, now green. Five are the conversation read
and its doctrine. Two were rejected. The resume class is where AC3 failed
in passes 2 and 3.

**Open or closed?** Open. The transitions are prose across three skills
and four resume routes. The states are predicates over free-text lines
with "newest" and "this pass" semantics that no writer records. A reviewer
cannot list the reachable states, because two inputs (facts 12 and 13)
have no on-disk form. Each new reader clause (`step-8 route-back:`, the
late-push definition, the second conversation read) patched one path
without a re-derivation of the others. The pattern across passes is a
sequence of ad hoc readers over an append-only log. Each pass adds a
prefix for the case the last pass found. That does not converge by
construction. It converges at the point where a reviewer runs out of paths
to try.

## 2. A verifiable full design

Yes, one exists, on one condition. The predicates must be **monotone over
the append-only log**, and the two missing writers must be added. A
monotone predicate ("a line with prefix X exists") is the only kind a
later reader can evaluate without knowing which pass wrote what. Every
"newest" and "this pass" clause is non-monotone. That is where passes 2
and 3 broke.

State variables and their records:

- **V1 slot**: the default-branch plan commit (exists).
- **V2 plan sha**: `git log --format='%H %s' --grep='^plan ' <base>/<default>`,
  filtered to the id. Fix the recipe to print the sha.
- **V3 promise unchanged**: `git diff <plan-sha> HEAD -- <file>` over
  Goal, Scope, and AC with `[x]` read as `[ ]` (exists).
- **V4 blocked**: any of `substantive amendment:`, `amendment return:`,
  `step-7 decline:`, `step-7 approval:`, `review return`, or `resume:`
  exists in the work log. One monotone set. It includes the up-front
  approval line itself, so the path is **one-shot per milestone**. Once the
  line is written, no later pass can take the up-front path. This replaces
  `step-8 route-back:`, the "newest approval line" read, and the late-push
  oid comparison.
- **V5 evidence**: every AC ticked with an evidence line (exists).
- **V6 findings**: every finding line carries a disposition. A fix-now
  line carries `fixed <sha>` once the fix lands (new writer, step 5). No
  `#1` or user-facing reject as false (exists).
- **V7 spawned**: a `spawned:` line names every lens the routing requires.
  "This pass" is replaced by the one-shot rule plus an empty Review section
  at the invocation's start (question 3).
- **V8 header and mode**: IP, `Resolves:`, `companion:`, guest (exist).
- **V9 D-heading diff** (exists).
- **V10 PR state at step 8**: checks green or the no-checks case. No
  non-bot conversation item. The PR head is the commit the agent pushed in
  this invocation, known by control flow, not by a log read.
- **V11 base oid**, recorded in the approval line, so a later reader can
  see whether the default branch moved. Only a design that lets a resume
  skip needs it. Under question 3 it is unnecessary.

Rule: the skip needs V1 to read `up front` and V4 to be empty. It needs
V3, V5, V6, and V7 to hold. It needs V8 to be clean and V9 to be empty.
Then V10 must hold at step 8. With V4 containing the approval line itself, no resume can
re-enter the skip.
Facts 11, 12, and 13 of the table are then not needed.

**Can a script compute it?** Yes. `cairn_upfront.py M<NNN>` reads the
branch milestone file (header slots, AC ticks, work-log prefixes, Review
lines). It reads `git show <base>/<default>:./<file>` for the slot, `git
log` for the plan sha, and `git diff` for V3 and V9. It reads
`cairn/PROFILE.md` for the mode. For V10 it reads `gh pr view --json
headRefOid,state`, `gh pr checks`, and the three conversation reads. It
prints `skip` or `ask: <first failing check>`. About 250 lines plus tests,
modelled on `cairn_validate.py`.

I do not recommend building it now. The script owns the readers, but the
writers stay in prose across three skills. So the writer/reader drift that
produced classes 2 and 3 above remains. To close it, the script must also
write the lines, a larger surface than the skip is worth. D-043 makes the
guards drift defense. A script that the agent must still obey is the same
kind of defense the prose already is. The maintainer's rule, descope over
hardening, points at question 3 first. Keep the script as the fallback for
the case where the narrowed design still returns.

## 3. The one-pass narrowing

Stated so that it is file-checkable. **The up-front check runs only in a
first-pass invocation of `/milestone-review`**. A first-pass invocation
found, at its start, an empty Review section and no PR for the branch.
"No PR" means the header names none and `gh pr list --head <branch>
--state all` is empty. Step 8's
up-front arm is entered only by control flow from a step 7 that passed in
that same invocation. Any stop after the approval line is written ends the
path for that milestone. The next invocation finds either a PR or the
approval line, and both are route-back facts.

Does it remove the pass-3 defects?

- diff-bug #1 (keys on any up-front line, loops after a chip approval):
  removed. No step reads the approval line to pick the arm. The chip path
  is entered by control flow after the chip. A later invocation always
  poses the chip, because the approval line exists (V4).
- diff-bug #2 (`spawned:` has no pass id): removed. An empty Review
  section at start means this pass wrote every line in it.
- diff-bug #3 (moved default branch on resume): removed. There is no
  resume on the up-front path. Step 1's sync in the one pass is the only
  moved-default handling, and it runs before any evidence is gathered.
- blame #4 (pickaxe): removed with the late-push oid check. In one pass
  the only push after the PR opens is a red-CI fix, which already asks.

What remains, with its cost:

- The route-back cases inside the pass: amendment, false reject, IP or
  D-entry, spawned, step-7 adders, red CI, conversation items. Each is a
  file read or a `gh` call at step 7 or step 8. None is pass-relative.
- diff-bug #4 (no writer for "fixed"): one line in step 5, a `fixed
  <sha>` suffix. Or drop the file check and keep the re-run of the
  `verify` slot as the evidence. Either is one edit.
- diff-bug #5 (lens slugs), #6 (git-root path: use `:./cairn/…` or
  `$(git rev-parse --show-prefix)`), #7 (plan-sha recipe): three one-line
  edits.
- diff-bug #8 and blame #1, #2 (bots, D-138): question 6.
- blame #3 and diff-bug #10 (guard default branch): question 7.
- Enumeration sync (diff-bug #9, blame #5, #7, prior #1): shrinks by three
  cases per surface. It stays a hand task unless the surfaces point to one
  list (recommendation 4).
- When a CI run outlasts the foreground Bash ceiling, the run stops at the
  timeout close, and the resume asks the chip. The skip then buys nothing for that
  milestone. This repo has no CI (`cairn/PROFILE.md:59`), so the no-checks
  case returns at once and the skip always completes in one invocation.
  Adopters with slow CI get the chip on resume.
- The end-of-run list at every run-ending close (pass 1's fix) stays as
  is. A later milestone's stop can still follow an up-front merge.

Is "one uninterrupted pass" checkable from the files? Yes. It is the
conjunction of three monotone facts at the invocation's start: no PR for
the branch, no line in V4, and an empty Review section. The third is
observed at start. It can be audited afterwards by git, because every
Review line lands in commits after the `status review` checkpoint of the
handoff. One gap: routes (c) and (d) write no `resume:` line today. A
session that stopped before step 7 with no log line and resumed through
route (d) finds a non-empty Review section and asks. That is the safe
direction. No new line is needed.

## 4. Removal

What of the branch is worth keeping without the skip:

- `Merge approval:` slot: nothing reads it. Drop.
- Guard slot read (`marker_up_front_milestone`, `slot_is_up_front`,
  `default_branch_merge_slot`, 19 tests, +91/+57/+237 lines): no marker
  will ever carry `up front`. Drop. Dead code behind a guard invites the
  drift D-043 names.
- End-of-run list: the merge question already lists each disposition.
  Drop.
- Finding line shape `<lens> #<rank>: … — <disposition>` and `spawned:`:
  keep. They give D-078's ranked list a greppable shape. They record a
  degraded review (D-127) on disk. No reader depends on pass identity.
  Cost nil.
- `step-7 decline:` and implement's `substantive amendment:` prefix: keep.
  The merge question's "names how many amendments there were" becomes a
  grep instead of a recall. Cost nil.
- Stale-prose fixes (pass 2 blame #8): they changed "ends at the merge
  question" to "or merges up front". Under removal they revert. Not kept.
- RB15, RR15, RB16, this RR, M203's work log and Review section: keep as
  archive. They are the record of why the path was tried and dropped.
- D-145: it is on the branch, unmerged. Merge it with a superseding
  D-146 rather than drop it. The trail stays append-only in spirit (IP4),
  and the user's gate decision stays on record.

Cost of removal. In this repo, none from D-138. With no CI the "serial
wait" is zero seconds. The cost of the merge question is the user's
presence once at the end of each milestone, and no unattended chaining of
a plan's milestones. For an adopter with CI, the chip answer is followed
by an attended wait, or by a timeout stop and a resume. D-138 accepted
that cost on 2026-09-10. Against that, removal deletes about 1,300 of the
branch's 1,577 added lines. It returns the review skill to its M202
length. It ends a class of defect that three passes did not close.

Note also how often the skip fires here. The plan question recommends
`at the end` for user-facing or IP-touching milestones. This repo's tier
definition (M203's own slot: "the skills and the merge guard ship in the
plugin to every adopter") makes nearly every milestone user-facing. The
skip's domain in the dogfood repo is internal milestones with no false
reject, no IP, no `Resolves:`, and no PR comment.

## 5. Recommendation

**Choose 3, the one-pass narrowing as question 3 states it, with 4 as the
named fallback.** The evidence that decides it:

- The two AC3 failures of passes 2 and 3, and 9 of the 44 findings, are in
  the resume and re-entry class. The one-pass rule deletes that class by
  construction, because V4 contains the approval line and the path is
  one-shot. It adds no reader. The remaining classes are done (guard
  internals, 19 tests green), or one-line edits, or a D-entry.
- The maintainer's rule is descope over hardening. Option 2 hardens: a
  script, pass ids, a base-oid writer. Option 3 descopes. Option 4
  descopes further, but gives up the chaining gain that D-145 recorded as
  the point of the path. The user chose the path twice, at the plan gate
  and at the thrash stop.
- Removal is the right answer under one condition: the user reads
  question 4's domain note and judges the skip too rare to carry even the
  narrowed machinery. That is a product judgment for the user alone. The
  plain cost of 3 is about 40 lines of review-skill prose, the guard read
  as it stands, and one D-entry.

AC disposition under 3:

- AC1 holds. IP1's text stands. D-146 records the narrowing and restates
  the route-back list as the one authoritative list (recommendation 4).
- AC2 holds unchanged.
- AC3 narrows. Replace the two-paragraph mechanism with four sentences.
  The check runs only in a first-pass invocation (question 3's three
  facts). The work-log line is written before the push. Step 8 merges
  when CI is green or the no-checks case applies, and the conversation
  read finds no non-bot item. Red CI, a non-bot item, or any stop poses
  the chip, in this invocation or the next. Drop the late-push oid
  definition, `step-8 route-back:`, the "newest approval line" and "this
  pass" clauses, and route (c)'s up-front branch. Keep the end-of-run list
  clause. This narrows the skip's domain (more cases ask), which the
  brief's constraint allows without an IP1 change. The late-push case
  stays as a rule (any push after the PR opens asks). It loses only its
  resume-time detector. State that in D-146, so no one reads it as a
  dropped case.
- AC4 holds. Question 7 changes one test.
- AC5 holds. README and CHANGELOG shrink to a pointer (recommendation 4).

Pass-3 "fix now" findings under 3: diff-bug #1, #2, #3 and blame #4 are
moot, because the text they fault is deleted. Diff-bug #4, #5, #6, #7 are
applied as the one-line edits above. Diff-bug #8, blame #1, #2 go to D-146
(question 6). Diff-bug #9, blame #5, #7, prior #1 are applied by the
shrink of the surfaces to a pointer. Blame #3 goes per question 7. Blame
#6 is applied. Diff-bug #10 stays a follow-up, or question 7 subsumes it.

This is the third defect return, so the thrash rule's descope route
applies. Amend AC3 through `/milestone-implement` step 6 at the user's
answer, then run one more review pass. If that pass returns on AC3 again,
take option 4 with no further brief.

## 6. PR conversation items

Route back on **non-bot items only**. Authorship is the `type` field of
the review or comment's author, the rule M177 already uses for the
blocking rule: a review whose author `type` is `Bot` never changes the
chip. Bot items are still read. Each gets a disposition line, and each
appears in the end-of-run list. Two reasons. A repo with a coverage or
lint bot that comments on every PR never skips, which empties the path.
And D-138's own falsifier already names the risk and the detector. That
falsifier is a bot comment on a fresh PR, found after the merge, that
named a defect the review fan-out missed. So a log of bot items after the
merge is the recorded trade. The human case the read exists for is the operator
requesting changes in the GitHub UI while the agent waits on CI. That is
a `User` item, and it routes back.

Yes, the read after CI on a fresh PR needs a D-entry. D-138 rejected "a
second conversation read after CI green on a fresh PR" by name. Its
reason: the read re-poses the chip after the marker is written. D-145
narrowed D-138 only on "the PR opens after the user's approval". On the
up-front arm no chip was posed and no marker exists before the read, so
D-138's reason does not apply. But a rejected alternative is being taken,
and IP2 wants that surfaced. Fold it into D-146 rather than a separate
entry. It narrows D-138 a second time, and it records the bot rule as a
narrowing of M177's grading for this path only.

## 7. Default-branch resolution in the guard

**For an unset `<base>/HEAD`, deny. Name `git remote set-head <base> -a`
in the deny text. Have review step 1 run that command as part of its
sync.** Reasons: the rulebook's recipe is `symbolic-ref`, then
`ls-remote --symref` (network), then ask, never guess. The guard can do
neither of the last two inside a 15-second hook. A deny is the guard's
safe direction, and the message is one command. Review step 1 already
fetches. With `set-head -a` added there, the ref is set before the guard
reads it in any review run. That also clears the stale-HEAD case of pass
3 diff-bug #10.

The current fallback fails safe in practice. A repo whose default is
neither `main` nor `master` denies with "no remote-tracking default branch
resolves". A wrong allow needs an `up front` slot on a non-default `main`.
So the fallback is not dangerous. It is a stated exception to a stated
rule, and the test `test_reads_main_when_remote_head_is_unset` enshrines
it. Flip that test to a deny. If the skills tests cover step 1, add one
for the `set-head` path. Under option 4 the question is moot.

## Beyond the brief

- IP1 delegates its enumeration to "the route-back cases the rulebook
  lists". T9 edited that rulebook list on the branch after D-145 fixed its
  list. It added the moved default branch, the `spawned:`-not-this-pass
  case, and the conversation items. By D-145's own clause, a change to
  the list is an IP1 change and takes the IP procedure. Pass 3 caught the
  conversation widening (blame #1, #2) but not the other two. D-146 must
  restate the full list once, and the rulebook must mirror it. The other
  four surfaces point, not enumerate.
- Routes (c) and (d) write no `resume:` line, while (a) and (b) do. Not
  a defect under option 3, since the safe direction holds. A one-line
  addition makes every resume visible in the log.
- Step 7's `git show <base>/<default-branch>:cairn/milestones/<file>` is
  git-root-relative. The guard reads cairn-root-relative (`:./path`).
  Pass 3 diff-bug #6 has it. The scripts resolve the cairn root the way
  the guard does, so the skill is the odd one out.
- Routes (a) and (c) read the `step-7 approval:` prefix, and the chip
  form and the up-front form share it. Under option 3 that is correct:
  both mean "a PR exists and was approved for something". The route text
  must say so in one sentence, to stop a fourth reader from keying on the
  suffix again.
- The plan question promises "merges with no further question" in words.
  The plan skill's own step-3 list recommends `at the end` for
  user-facing and IP milestones. In a repo where nearly every milestone is
  user-facing, the question usually recommends against its own offer.
  Consider a narrower trigger: the plan has at least one internal,
  IP-free milestone. Otherwise write `at the end` and skip the question.

## Recommendations

1. **Apply.** Narrow AC3 to the one-pass rule as question 3 states it.
   The up-front check runs only in an invocation that started with an
   empty Review section and no PR for the branch. The approval line joins
   the route-back prefix set (one-shot). Step 8's arm is entered by
   control flow only. Delete the late-push oid check, `step-8
   route-back:`, the "newest approval line" and "this pass" clauses, and
   route (c)'s up-front branch. Keep the end-of-run list.
2. **Apply.** D-146. It records the narrowing. It restates the route-back
   list as the one authoritative enumeration. It narrows D-138 for the
   post-CI read on the up-front arm. It narrows M177's grading to non-bot
   items for that read. It states that the late-push case keeps its rule
   and loses only its resume-time detector.
3. **Apply.** The one-line fixes from pass 3. A `fixed <sha>` suffix on a
   fix-now line (diff-bug #4). Lens slugs named in step 5's routing table
   (#5). A cairn-root-relative `git show` path in step 7 (#6). A plan-sha
   recipe that prints `%H` (#7). Implement step 6 "carries" (blame #6).
   The template header line count (blame #7).
4. **Apply.** README "Merges are yours", CHANGELOG, and the plan question
   point to the rulebook's approval bullet for the cases instead of a
   list. The routing template and the CLAUDE.md section already do this
   after AC5's amendment. One list, one place.
5. **Apply.** Guard: for an unset `<base>/HEAD`, deny and name
   `git remote set-head <base> -a`. Review step 1 runs that command with
   its fetch. Flip `test_reads_main_when_remote_head_is_unset` to a deny.
6. **Apply.** Bot items never route back. They are logged and listed.
   Non-bot items route back. Authorship is the `type` field, as in M177.
7. **Consider.** Pose the plan's merge question only for a plan with at
   least one internal, IP-free milestone. Otherwise write `at the end`
   with no question. This cuts a question whose recommendation is "no".
8. **Consider.** A `resume:` line on routes (c) and (d).
9. **Consider.** Option 4, removal, in two cases: the user judges the
   skip's domain in this repo (question 4's note) too small to carry even
   the narrowed machinery, or the next review pass returns on AC3 again.
   Under it, keep the finding-line and `spawned:` shapes and the two
   prefixes, merge D-145 with a superseding D-146, and archive the RB/RR
   pair.
10. **Reject with reason.** Option 2's script (`cairn_upfront.py`). It
    moves the readers into one file, but leaves the writers in prose
    across three skills, so the writer/reader drift stays. To close it,
    the script must write the lines too. That is more surface than the
    skip is worth under D-043 and the descope-over-hardening rule.
    Fallback only.
11. **Reject with reason.** Any pass id, base-oid record, or other new
    writer added to support a skip on a resume. Each is one more
    non-monotone fact for a later reader to key on, the mechanism of all
    three returns. The one-shot rule makes them unnecessary.
12. **Reject with reason.** The `main`/`master` fallback as the guard's
    answer to an unset `<base>/HEAD`. It is a guess the rulebook forbids.
    The deny with an instruction costs one command, once.

No disagreement with the brief's constraints. One note on the first. The
late-push change in recommendation 1 is argued above as a narrowing of
the skip's domain, not of a route-back case. If the user reads it as
the latter, D-146 is the IP procedure and covers it.
