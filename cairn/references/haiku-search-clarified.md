# Haiku 5.5 against Sonnet 5.5 on search, with S2's base name clarified (M277)

**Provenance.** Ingested 2026-10-18 by M277 from first-hand runs. The runs
are subagents spawned with the Agent tool from a Claude Code desktop
session in this repo. Each run's counts come from its subagent transcript
under
`~/.claude/projects/-Users-jmgirard-github-cairn/6892c723-ced4-4892-a4be-c23fbf20ad93/subagents/`.
Tasks, keys, and the scoring rule are those of `haiku-sonnet-roles.md`
(M228), with one change to S2's prompt (Design, part 2). The tasks replay
commit `c023018`. Prices are those `haiku-sonnet-roles.md` lists.
Pagination: —.
Extraction: prices as `haiku-sonnet-roles.md` read directly from the pricing page 2026-10-09, and liable to change; the run records are first-hand from the 2026-10-18 session store, and a rerun reproduces the method, not the exact figures — observed 2026-10-18.

**Scope.** M228 and M264 gave the search group the verdict `stay`. In
M264 (`haiku-sonnet-rerun.md`) Haiku scored 1.9962 and Sonnet 2.8865.
Every Haiku S2 run there listed the nine registrations but wrote each
script without its `.py` extension, and each such run scored 0. S2's
prompt asked for "the Python file's base name" and did not say whether the
extension is part of it. This note reruns the three search tasks three
times per model with that one phrase made explicit, and states a verdict.
The ROADMAP and `DECISIONS.md` act on it. This is a reference, not an
authority.

## Design (fixed at `7da5278a` before any run, 2026-10-18)

**Part 1: runs.** Tasks S1, S2, and S3 of `haiku-sonnet-roles.md` each run
six times. The Agent tool's `model` is `sonnet` in three runs and `haiku`
in three. Every run uses the `Explore` agent type with `effort` unset
(D-157). Each run reads its own `git archive c023018` copy in the session
scratchpad, one copy per run. Every spawn runs in the foreground, so its
Agent tool result carries `usage`. Run index r is 1, 2, or 3. The expected model
id is `claude-sonnet-5-5` for `sonnet` and `claude-haiku-5-5` for `haiku`.
A run whose transcript shows other model ids is not counted. It is listed
with its ids, and a new run takes its place. A counted run's tool calls
name no path under the live checkout `/Users/jmgirard/github/cairn/`.

**Part 2: prompts.** The template is the Search group prompt of
`haiku-sonnet-roles.md`, with the repository path
`/Users/jmgirard/github/cairn` replaced by the run's copy path. S1's and
S3's `<Q>` and `<FORM>` are that note's text unchanged. S2's `<Q>` is
unchanged. S2's `<FORM>` differs in one phrase.

Old S2 FORM value (M228, M264):

> `<event> <matcher> <script>`, where matcher is `*` when the entry has
> none and script is the Python file's base name, one line per
> registration

New S2 FORM value (this note):

> `<event> <matcher> <script>`, where matcher is `*` when the entry has
> none and script is the Python file's base name including its `.py`
> extension, for example `cairn_next.py`, one line per registration

`cairn_next.py` is not a hook script, so the example names no key item.

**Part 3: scoring and cost.** Scoring is the rule of
`haiku-sonnet-roles.md` (Search group): the F1 of the `ANSWER:` items
against the key, `2·|A∩K| / (|A| + |K|)`, where A and K are sets of items
compared after trimming whitespace and backticks. A reply with no
`ANSWER:` line scores 0. The keys are that note's S1, S2, and S3 keys
(Answer keys, target, and mutants). Cost is the method of
`haiku-sonnet-rerun.md` (Design, Cost). Records are grouped by
`message.id`, and each id takes its five class counts from its last
record, times the model's price. A Haiku call whose prompt is over 100,000
tokens pays the higher row for every class. The run's final id takes its
output count from one Agent tool result in the main session transcript
`~/.claude/projects/-Users-jmgirard-github-cairn/6892c723-ced4-4892-a4be-c23fbf20ad93.jsonl`.
That result is the one whose `agentId` matches, and the count is its
`usage` output.
"Final match" says whether that `usage`'s input and cache counts equal the
final id's last-record counts. Earlier calls keep their stream-start
output counts, so every cost is a lower bound.

**Part 4: verdict rule.** This is the rule of `haiku-sonnet-rerun.md`. For
each model, take each task's mean score over its three runs and each
task's mean cost over its three runs. Sum each mean over the three tasks.
The verdict is `move` when three things hold: Sonnet's summed score is
above zero, Haiku's summed cost is below Sonnet's, and Haiku's summed
score is at least 0.9 times Sonnet's. Otherwise the verdict is `stay`.

Prices, USD per million tokens, as `haiku-sonnet-roles.md` lists them:

| Model | Input | 5m cache write | 1h cache write | Cache read | Output |
|---|---|---|---|---|---|
| Sonnet 5.5 | 2.00 | 2.50 | 4.00 | 0.10 | 10.00 |
| Haiku 5.5, prompt ≤ 100,000 tokens | 0.10 | 0.125 | 0.20 | 0.01 | 0.50 |
| Haiku 5.5, prompt > 100,000 tokens | 0.50 | 0.625 | 1.00 | 0.05 | 2.50 |

## Runs

Agent ids name each run's transcript, `agent-<id>.jsonl` under the
Provenance directory. "Model ids" lists every `model` value on the
transcript's assistant records. "Final match" is the Cost check of Part 3.
Token columns sum the row's calls. The table holds the 18 counted runs.
Every run's first transcript record is dated 2026-10-18 between 18:30:21Z
and 18:32:01Z. The Design commit `7da5278a` is dated 18:29:16Z.

| Task | Model | Run | Agent id | Model ids | Calls | Final match | Input | 5m write | 1h write | Cache read | Output | USD | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | sonnet | 1 | `ab004aa078497b1f4` | claude-sonnet-5-5 | 2 | yes | 4 | 38140 | 0 | 36020 | 966 | 0.1086 | 1.0000 |
| S1 | sonnet | 2 | `a881139b234b00e22` | claude-sonnet-5-5 | 4 | yes | 8 | 41695 | 0 | 112991 | 520 | 0.1208 | 1.0000 |
| S1 | sonnet | 3 | `a66711d57758ba059` | claude-sonnet-5-5 | 3 | yes | 6 | 38975 | 0 | 74163 | 677 | 0.1116 | 1.0000 |
| S1 | haiku | 1 | `a09296e8dcc96f1de` | claude-haiku-5-5 | 3 | yes | 6 | 41994 | 0 | 75987 | 1293 | 0.0067 | 1.0000 |
| S1 | haiku | 2 | `abd45788291c3d01f` | claude-haiku-5-5 | 2 | yes | 4 | 37559 | 0 | 36017 | 1143 | 0.0056 | 1.0000 |
| S1 | haiku | 3 | `a1b3c4ef38370539c` | claude-haiku-5-5 | 2 | yes | 4 | 39534 | 0 | 36017 | 1352 | 0.0060 | 1.0000 |
| S2 | sonnet | 1 | `a57419a0b573c7aae` | claude-sonnet-5-5 | 2 | yes | 4 | 38006 | 0 | 36059 | 686 | 0.1055 | 1.0000 |
| S2 | sonnet | 2 | `ac948effec005e033` | claude-sonnet-5-5 | 2 | yes | 4 | 38006 | 0 | 36059 | 371 | 0.1023 | 1.0000 |
| S2 | sonnet | 3 | `a2d71bc04f7c7542b` | claude-sonnet-5-5 | 2 | yes | 4 | 38006 | 0 | 36059 | 581 | 0.1044 | 1.0000 |
| S2 | haiku | 1 | `a625f7caf6887aae5` | claude-haiku-5-5 | 2 | yes | 4 | 38413 | 0 | 36056 | 1144 | 0.0057 | 1.0000 |
| S2 | haiku | 2 | `af1174eaa0ea69b76` | claude-haiku-5-5 | 2 | yes | 4 | 38314 | 0 | 36056 | 1232 | 0.0058 | 1.0000 |
| S2 | haiku | 3 | `ab4c38157dd4db8eb` | claude-haiku-5-5 | 2 | yes | 4 | 38187 | 0 | 36056 | 1083 | 0.0057 | 1.0000 |
| S3 | sonnet | 1 | `a4965214d3b04aac6` | claude-sonnet-5-5 | 2 | yes | 4 | 42095 | 0 | 36061 | 3901 | 0.1479 | 0.6767 |
| S3 | sonnet | 2 | `adabee7bad8f44f89` | claude-sonnet-5-5 | 2 | yes | 4 | 42092 | 0 | 36061 | 4889 | 0.1577 | 0.9943 |
| S3 | sonnet | 3 | `a2feb9645d2fe5627` | claude-sonnet-5-5 | 2 | yes | 4 | 18965 | 0 | 59190 | 3531 | 0.0886 | 0.6767 |
| S3 | haiku | 1 | `ab3bf1672a65e3267` | claude-haiku-5-5 | 5 | yes | 10 | 52030 | 0 | 157534 | 5512 | 0.0108 | 1.0000 |
| S3 | haiku | 2 | `ae3128a87d3e9564c` | claude-haiku-5-5 | 5 | yes | 10 | 45943 | 0 | 159339 | 11841 | 0.0133 | 1.0000 |
| S3 | haiku | 3 | `ad482e1243d216bcf` | claude-haiku-5-5 | 3 | yes | 6 | 53858 | 0 | 85313 | 6185 | 0.0107 | 0.9767 |

**Run not counted.** The first S3 Sonnet run 3 (`abc4d030d6c872307`,
claude-sonnet-5-5, USD 0.1506, score 1.0000) read only its own copy. Its
report, which it delivered through a tool call, names the live checkout's
`DECISIONS.md` as the file it read. Part 1 counts no run whose tool calls
name a live checkout path, so this run was set aside, and
`a2feb9645d2fe5627` ran on a fresh copy with the same prompt. No counted
run's tool calls name a path under the live checkout. A search of each
transcript's tool calls and tool results for `/Users/jmgirard/github/cairn/`
found none.

Search notes. Every S1 and S2 run on both models scored 1.0, and every S2
run listed all nine registrations with the `.py` extension. S3 Sonnet runs
1 and 3 applied their own reading of which heading clauses supersede and
listed the same 45 pairs, as one Sonnet run did in M228 and in M264. S3
Sonnet run 2 misses `D-072 D-071`. S3 Haiku runs 1 and 2 match the key.
Haiku run 3 misses the two pairs from D-085's "supersede-on-firing" and
the two from D-126's "supersedes nothing in D-090 or D-108". No run lists
an item outside its key.

## Verdict

Per task, the mean over three runs, with each score's range over its runs:

| Task | Sonnet score | Sonnet range | Haiku score | Haiku range | Sonnet USD | Haiku USD | Sonnet calls | Haiku calls |
|---|---|---|---|---|---|---|---|---|
| S1 | 1.0000 | 1.0000 to 1.0000 | 1.0000 | 1.0000 to 1.0000 | 0.1137 | 0.0061 | 2, 4, 3 | 3, 2, 2 |
| S2 | 1.0000 | 1.0000 to 1.0000 | 1.0000 | 1.0000 to 1.0000 | 0.1041 | 0.0057 | 2, 2, 2 | 2, 2, 2 |
| S3 | 0.7826 | 0.6767 to 0.9943 | 0.9922 | 0.9767 to 1.0000 | 0.1314 | 0.0116 | 2, 2, 2 | 5, 5, 3 |

| Group | Sonnet USD | Haiku USD | Sonnet score | Haiku score | Haiku ÷ Sonnet score | Verdict |
|---|---|---|---|---|---|---|
| Search | 0.3491 | 0.0234 | 2.7826 | 2.9922 | 1.0754 | move |

The verdict applies Part 4's rule to the sums above: Sonnet's summed score
is above zero, Haiku's summed cost is below Sonnet's, and Haiku's summed
score is at least 0.9 times Sonnet's.

Readings that bear on the verdict:

- The S2 change is the whole difference from M264. With S2's base name
  stated to include `.py`, all three Haiku S2 runs scored 1.0, where all
  three scored 0 in M264. With every Haiku S2 run at 0, as in M264,
  Haiku's sum is 1.9922, below 0.9 times Sonnet's (2.5043), and the
  verdict is `stay`.
- The run set aside does not decide the verdict. Counted in place of its
  replacement, it makes Sonnet's S3 mean 0.8903 and Sonnet's sum 2.8903,
  and Haiku's 2.9922 is still above 0.9 times that (2.6013).
- Haiku leads on S3 for the same reason as in M264. Two of three Sonnet
  runs read past S3's stated counting rule and listed 45 of the 88 pairs.
  Every Haiku S3 run followed the rule.
- Costs are lower bounds (Part 3). The search gap is 0.3257 USD. To close
  it, Haiku's unrecorded output, priced at Haiku's higher tier, must exceed
  about 130,000 tokens. That is about 23,000 per non-final Haiku call
  (5.67 such calls per group sum of means).
- These are three closed-answer tasks from this repo, each with a key. A
  plan-time investigation, whose answer has no key and whose reader acts
  on cited sites, is not measured here.

## Limits and re-measurement

Three runs per model per task, three tasks, at default effort, in one
session. S2's prompt differs from M228's and M264's, so this note's S2
scores do not compare with theirs. The measurement helper was
session-local and is not committed (observed 2026-10-18). To re-measure,
follow the Design section with the same models and prompts, and apply the
verdict rule. A rerun that flips the verdict falsifies this note's
verdict.
