# Medium against default reasoning effort on cairn's history reviewers (M240)

**Provenance.** Ingested 2026-10-10 by M240 from first-hand runs: subagents
spawned with the Agent tool from a Claude Code desktop session in this repo,
each run's counts read from its subagent transcript under
`~/.claude/projects/-Users-jmgirard-github-cairn/77cf25d1-1798-418e-92bb-b20494fa5f30/subagents/`.
The reused M239 default runs are under the M239 Provenance directory of
`effort-roles.md`. Prices are those `effort-roles.md` lists, read from
Anthropic's pricing page on 2026-10-10.
Pagination: —.
Extraction: the run records are first-hand from that day's session store, and a rerun reproduces the method, not the exact figures — observed 2026-10-10.

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
