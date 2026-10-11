# Medium against default reasoning effort on cairn's history reviewers (M240)

**Provenance.** Ingested 2026-10-10 by M240 from first-hand runs: subagents
spawned with the Agent tool from a Claude Code desktop session in this repo,
each run's counts read from its subagent transcript under
`~/.claude/projects/-Users-jmgirard-github-cairn/77cf25d1-1798-418e-92bb-b20494fa5f30/subagents/`.
The reused M239 default runs are under the M239 Provenance directory of
`effort-roles.md`. Prices are those `effort-roles.md` lists, read from
Anthropic's pricing page on 2026-10-10.
Pagination: —.
Extraction: prices as `effort-roles.md` read directly from the pricing page 2026-10-10, and liable to change; the run records are first-hand from that day's session store, and a rerun reproduces the method, not the exact figures — observed 2026-10-10.

**Scope.** Measures whether the history-review group of
`haiku-sonnet-roles.md` (the blame-history and prior-PR-comments reviewers,
Sonnet) keeps its judged findings at `medium` reasoning effort for less money
than at default effort. M239 (`effort-roles.md`) gave this group the verdict
`default` against `low`, on a gap that equals M228's run-to-run spread. This
note records a measurement and a verdict. The rulebook's model section acts
on the verdict. This is a reference, not an authority: status lives in
`ROADMAP.md`, decisions in `DECISIONS.md`.

## Design (fixed before any task run, 2026-10-10)

**Arms.** Three arms over the three history-review tasks H1, H2, and H3:

| Arm | Runs | `effort` setting |
|---|---|---|
| M239 default | M239's default runs, reused: H1 `aa3398a8cbe013dcd`, H2 `a19090c5879113da4`, H3 `a358c3f0ff2386c3e` | unset (recorded `high`) |
| New default | one new run per task | unset |
| Medium | one new run per task | `medium` |

Every new run sets `model: "sonnet"` and the `general-purpose` agent type,
as M228 and M239 did. Each new run's prompt is the first user record of the
M239 default run of the same task, verbatim. That prompt is the M228 prompt
of `haiku-sonnet-roles.md` (History-review group) with its `<SHA>`, `<FILE>`,
and `<LENS>` filled in. The two new runs of a task are spawned in the same
message, in the foreground, so each Agent tool result carries its `usage`.

**Pinned inputs.** History-review runs read refs of this repository, and
every ref they name predates `c023018`. The H3 lens also reads archived
`## Review` sections from the working tree, which now holds archives that
M239's runs did not see. The prompt limits each review to history at or
before the commit under review. The live tree also holds
`haiku-sonnet-roles.md` and `effort-roles.md`, which list earlier findings
on the same three commits. After the runs, every new run and judge
transcript is searched for both file names, and the note records the result.

**Cost.** The method of `haiku-sonnet-roles.md` (Design, Cost): records
grouped by `message.id`, each id's five class counts from its last record,
times the Sonnet price. The run's final id takes its output count from the
`usage` of the Agent tool result whose `agentId` matches, in this session's
main transcript
`~/.claude/projects/-Users-jmgirard-github-cairn/77cf25d1-1798-418e-92bb-b20494fa5f30.jsonl`.
Every row's cost is a lower bound, as there. The M239 default arm's three
costs are the USD figures that `effort-roles.md` records for those runs,
which used that note's amended background method.

**Judging.** One Opus judge per task (`model: "opus"`, `effort` unset)
reads the three reports of its task under labels A, B, and C. Each report
is the run's final answer: the `message` input of its `SubagentHandback`
call, else its last assistant text. The labels are drawn with
`random.SystemRandom` and written to a mapping directory before the judge
runs, apart from the reports directory the judge reads. The judge prompt
is the M228 prompt of `haiku-sonnet-roles.md` (History-review group),
widened to three reviewers:

> You are a judge rating code-review findings. Three reviewers, labeled A,
> B, and C, independently reviewed commit <SHA> in
> /Users/jmgirard/github/cairn (diff `git show <SHA>`, base `<SHA>^`) with
> this lens: "<JLENS>" Reviewer A's report: <path A> Reviewer B's report:
> <path B> Reviewer C's report: <path C> Read only those three files in
> their directory. In the repo use ref-based git only (git show, git log,
> git blame against refs); edit nothing. Rate each numbered finding in each
> report VALID or INVALID by this rule: a finding is valid when the history
> or prior review it cites exists and the diff does conflict with it;
> otherwise it is invalid. A finding that repeats an earlier one in the
> same report counts once: rate the repeat DUPLICATE. Unnumbered notes are
> not findings. Return one line per finding, `A1: VALID|INVALID|DUPLICATE —
> <one-sentence reason>`, then the B lines, then the C lines, then
> `A valid: <n>`, `B valid: <n>`, and `C valid: <n>`.

`<JLENS>` is the M228 text for each task.

**Verdict rule.** An arm's score is the sum over H1 to H3 of the findings
this milestone's judges rate valid. An arm's cost is the sum of its three
USD figures. The verdict is `untested` when a `medium` run's assistant
records carry no `effort` value or any value other than `medium`, or when a
new default run's records carry any value other than `high`. Otherwise it
is `medium` exactly when three conditions hold:

1. The mean score of the two default arms is above zero.
2. The `medium` arm's cost is below the two default arms' mean cost.
3. The `medium` arm's score is at least 0.9 times the two default arms'
   mean score.

Otherwise the verdict is `default`.

## Runs

The new runs ran on 2026-10-11 UTC (2026-10-10 local), all six spawned in
one message. The Design section's commit, `40d6ce7`, is dated
2026-10-11T03:43:14Z, and the first record of the first run transcript is
dated 2026-10-11T03:43:49Z. Agent ids name each new run's transcript,
`agent-<id>.jsonl` under the Provenance directory. "Effort" and "Model ids"
list every value on the transcript's assistant records. "Final match" says
whether the Agent tool result's `usage` input and cache counts equal the
final id's last-record counts, as in `haiku-sonnet-roles.md`. Token columns
sum the row's calls. The M239 default rows repeat that note's run table.

| Task | Arm | Agent id | Effort | Model ids | Calls | Final match | Input | 5m write | 1h write | Cache read | Output | USD | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | M239 default | `aa3398a8cbe013dcd` | high | claude-sonnet-5-5 | 16 | (M239) | 32 | 93647 | 0 | 1167753 | 2735 | 0.3783 | 2 |
| H1 | new default | `aca53b8c7b862067c` | high | claude-sonnet-5-5 | 21 | yes | 42 | 104235 | 0 | 1721212 | 2736 | 0.4602 | 1 |
| H1 | medium | `a5fc1e95b40e18d95` | medium | claude-sonnet-5-5 | 6 | yes | 12 | 77770 | 0 | 342726 | 1348 | 0.2422 | 0 |
| H2 | M239 default | `a19090c5879113da4` | high | claude-sonnet-5-5 | 8 | (M239) | 16 | 69133 | 0 | 422133 | 1133 | 0.2264 | 1 |
| H2 | new default | `a0bf3ea30a1bc24aa` | high | claude-sonnet-5-5 | 7 | yes | 14 | 77033 | 0 | 394188 | 1736 | 0.2494 | 1 |
| H2 | medium | `abce8a8149df5be76` | medium | claude-sonnet-5-5 | 4 | yes | 8 | 64188 | 0 | 169704 | 1043 | 0.1879 | 1 |
| H3 | M239 default | `a358c3f0ff2386c3e` | high | claude-sonnet-5-5 | 11 | (M239) | 22 | 78742 | 0 | 653107 | 1248 | 0.2747 | 0 |
| H3 | new default | `a85097caad83f3fce` | high | claude-sonnet-5-5 | 11 | yes | 22 | 78536 | 0 | 644040 | 1260 | 0.2734 | 1 |
| H3 | medium | `ab7db947583fda15c` | medium | claude-sonnet-5-5 | 10 | yes | 20 | 69091 | 0 | 549814 | 1211 | 0.2399 | 1 |

Scores are this milestone's judgings. M239's own judging scored its
default reports 3, 1, and 0.

Contamination check. No new run or judge transcript contains
`effort-roles` or `haiku-sonnet-roles` except the H3 new default run's,
where `effort-roles.md` appears once as a file path in the output of a
`gh api` listing of PR #249's review comments. That run read no file of
either name. No judge transcript contains the mapping directory's path.

## Judging

Judges (Opus, `claude-opus-5-5`, effort `high` on every record): H1
`a41c32e3c90c9a2fa`, H2 `a76b12c37e9f43117`, H3 `addd3f45a37e9e7ec`. The
mappings, read after all three judges returned: H1 A new default, B M239
default, C `medium`; H2 A `medium`, B M239 default, C new default; H3 A new
default, B M239 default, C `medium`. No finding was rated a duplicate.

Per-finding ratings (V valid, I invalid; the number is the reviewer's own):

| Task | Arm | # | Finding, in short | Rating |
|---|---|---|---|---|
| H1 | M239 default | 1 | `register.tsx` comments still name only the Blocked heading's Refresh, though the review log says fixed | V |
| H1 | M239 default | 2 | `collaborationMode` contradicts the "one parser" comment in `cairn_common.py` | I |
| H1 | M239 default | 3 | older DESIGN.md M224 sentences disagree with the new M226 text | I |
| H1 | M239 default | 4 | `readPrs` no longer makes no calls when no blocked row has a URL | V |
| H1 | M239 default | 5 | the `hotfix-` filter misses adopted PRs | I |
| H1 | M239 default | 6 | `/hotfix` step 6 wording about `/milestone` | I |
| H1 | new default | 1 | `readPrs` no longer makes no calls when no blocked row has a URL | V |
| H1 | new default | 2 | README and `readPrs` comments still read as Blocked-only | I |
| H1 | new default | 3 | a third hand-kept copy of the mode parser | I |
| H1 | new default | 4 | the `hotfix-` filter misses adopted PRs | I |
| H1 | new default | 5 | the remote URL reaches the `gh` argument list | I |
| H1 | medium | 1 | the new early-return branch and the missing Refresh | I |
| H1 | medium | 2 | the `hotfix-` filter misses adopted PRs | I |
| H1 | medium | 3 | a third copy of the mode logic, with no cross-language test | I |
| H1 | medium | 4 | no new duplicate type was added | I |
| H2 | M239 default | 1 | the commit promises a rewrap, but the line is 117 characters | V |
| H2 | M239 default | 2 | a ragged wrap in the hotfix skill | I |
| H2 | M239 default | 3 | someone else's `hotfix-*` PR is still reported nowhere | I |
| H2 | M239 default | 4 | the guest handoff keeps M185's intent | I |
| H2 | new default | 1 | the review log says rewrapped, but the line is 117 characters | V |
| H2 | new default | 2 | a ragged wrap in the hotfix skill | I |
| H2 | new default | 3 | a failed `gh` read is reported by two bullets | I |
| H2 | new default | 4 | checks found fine | I |
| H2 | medium | 1 | the line is still 117 characters after the rewrap commit | V |
| H2 | medium | 2 | two definitions of "your" PR | I |
| H2 | medium | 3 | the plan skill's inbox drops `hotfix-*` PRs | I |
| H3 | M239 default | 1–5 | five past review points, each found to hold | I (each) |
| H3 | new default | 1 | a second sequential `gh` call worsens M224's flagged wait | V |
| H3 | medium | 1 | a second copy of the PR URL pattern | I |
| H3 | medium | 2 | a second sequential `gh` call worsens M224's flagged wait | V |

## Verdict

| Arm | USD | Score |
|---|---|---|
| M239 default | 0.8794 | 3 |
| New default | 0.9830 | 3 |
| Mean of the two default arms | 0.9312 | 3.0 |
| Medium | 0.6700 | 2 |

Every `medium` row records only `medium`, and every new default row
records only `high`, so the verdict is not `untested`. The mean default
score is above zero, and the `medium` arm's cost is below the mean default
cost. The `medium` arm's score, 2, is below 0.9 times the mean default
score, 2.7. The verdict is `default`.

Readings that bear on the verdict:

- The whole score gap is H1. Both default arms found that `readPrs` lost
  M224's no-call path, and the `medium` run did not. On H2 all three arms
  found the same valid finding, and on H3 the new default and `medium`
  arms found the same one.
- The `medium` arm cost 28% less than the mean default arm. On H1 it made
  6 calls against 16 and 21.
- The two default arms differ by 1 on H1 and by 1 on H3 under one judging.
  One more valid finding for `medium` would leave it at 3 and flip the
  verdict, so the verdict rests on one finding, as M239's did.
- M239 measured `low` at 2 against 4 on the same tasks. Together the two
  notes show the same pattern: at lower effort the reviewer makes fewer
  calls and costs less, and on H1 it misses a finding that default effort
  finds.

## Limits and re-measurement

One new run per arm per task, three tasks, all from this repo. One Opus
judge per task, one judging. The score counts reported findings that the
judge rated valid. It does not measure real conflicts a reviewer missed.
The measurement helpers (report extractor, cost script, label drawing)
were session-local and are not committed (observed 2026-10-10). To
re-measure: re-run the three history-review prompts of
`haiku-sonnet-roles.md` with `effort` unset and set to `medium`, read each
run's `effort` and `model` values and its counts from its subagent
transcript, take the final call's output from the Agent tool result's
`usage`, judge each task's reports together under shuffled labels with the
prompt above, and apply the verdict rule. A rerun that flips the verdict
falsifies this note's verdict.
