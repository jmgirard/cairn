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

## Design (fixed before any run, 2026-10-18)

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
