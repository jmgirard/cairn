# Haiku 5.5 against Sonnet 5.5 on cairn's Sonnet roles (M228)

**Provenance.** Ingested 2026-10-09 by M228 from first-hand runs: subagents
spawned with the Agent tool from a Claude Code desktop session in this repo,
each run's cost read from its subagent transcript under
`~/.claude/projects/-Users-jmgirard-github-cairn/<session>/subagents/`. Prices
from Anthropic's pricing page (cited below). Tasks replay this repo at commit
`c023018`.
Pagination: —.
Extraction: first-hand record, nothing to re-verify against; a rerun reproduces the method, not the exact figures — observed 2026-10-09.

**Scope.** Measures whether Haiku 5.5 does the work of each role group that
tracking-rules "Model and agent strategy" gives to Sonnet for less money and
with no loss of quality. It records a measurement and a verdict per group.
It changes no rule: M229 acts on the verdicts. This is a reference, not an
authority: status lives in `ROADMAP.md`, decisions in `DECISIONS.md`.

## Design (fixed before any run, 2026-10-09)

**Models.** The Agent tool's `model` setting `sonnet` resolved to
`claude-sonnet-5-5` and `haiku` to `claude-haiku-5-5` in a one-word probe
spawn of each, read from the probes' transcripts on 2026-10-09.

**Runs.** Nine tasks, three per role group. Each task runs once with
`model: "sonnet"` and once with `model: "haiku"`, from the same prompt
(below), at default effort. Search runs use the `Explore` agent type. Edit
runs use `general-purpose` with `isolation: "worktree"`. Review runs use
`general-purpose`. One run per model per task: a verdict near the margin is
not robust to rerun variance, which the re-measurement procedure covers.

**Cost.** For each transcript, records are grouped by `message.id`, and the
last record of each id carries that API call's usage (earlier records of the
same id repeat the input counts and carry partial `output_tokens`). Per id,
cost is the sum over five classes of count times price: `input_tokens`,
`cache_creation.ephemeral_5m_input_tokens`,
`cache_creation.ephemeral_1h_input_tokens`, `cache_read_input_tokens`,
`output_tokens`. A row's cost is the sum over its ids. Haiku prices depend on
each call's prompt size: a call whose input, cache-write, and cache-read
tokens sum to more than 100,000 pays the higher row for every class.

Prices, USD per million tokens, from
<https://platform.claude.com/docs/en/about-claude/pricing> (read 2026-10-09):

| Model | Input | 5m cache write | 1h cache write | Cache read | Output |
|---|---|---|---|---|---|
| Sonnet 5.5 | 2.00 | 2.50 | 4.00 | 0.10 | 10.00 |
| Haiku 5.5, prompt ≤ 100,000 tokens | 0.10 | 0.125 | 0.20 | 0.01 | 0.50 |
| Haiku 5.5, prompt > 100,000 tokens | 0.50 | 0.625 | 1.00 | 0.05 | 2.50 |

**Verdict rule.** Per group, sum each model's cost and score over the
group's three tasks. The verdict is `move` exactly when Sonnet's summed score
is above zero, Haiku's summed cost is below Sonnet's, and Haiku's summed
score is at least 0.9 times Sonnet's. Otherwise it is `stay`. Every scoring
rule below yields a score of zero or more.

### Search group (Explore fan-outs)

Prompt, with `<Q>` and `<FORM>` per task:

> You are searching the git repository at /Users/jmgirard/github/cairn to
> answer a question. Read-only: do not edit files, and do not run any git
> command that moves HEAD (checkout, switch, reset, worktree). Read the
> working tree. Question: <Q> End your reply with a line `ANSWER:` followed
> by one item per line in the form <FORM>, and nothing after the list.

- S1. Q: "Which Python files under `scripts/` and `hooks/`, tests included,
  contain an import statement for the module `cairn_common`, either
  `import cairn_common` or `from cairn_common import ...`?" FORM: "a
  repo-relative file path".
- S2. Q: "Which hook commands does `hooks/hooks.json` register under its
  `hooks` key (not its `modules` key), with each one's event and matcher?"
  FORM: "`<event> <matcher> <script>`, where matcher is `*` when the entry
  has none and script is the Python file's base name, one line per
  registration".
- S3. Q: "In `cairn/DECISIONS.md`, which earlier entries does a later
  entry's own `### D-` heading say it supersedes? Count an id as superseded
  when it appears after a form of the word 'supersede' (supersedes,
  superseding, superseded) in that heading." FORM: "`<superseding id>
  <superseded id>`, for example `D-110 D-016`".

Score: F1 of the `ANSWER:` items against the key, `2·|A∩K| / (|A| + |K|)`,
items compared after trimming whitespace and backticks. A reply with no
`ANSWER:` line scores 0.

### Edit-work group (mechanical sweep, test writing)

- E1 (sweep). Prompt: "In this git worktree, rename the Python function
  `find_cairn_root` (defined in `hooks/cairn_common.py`) to
  `locate_cairn_root`. Update every occurrence of the identifier
  `find_cairn_root` in Python files under `scripts/` and `hooks/`, tests,
  comments, and docstrings included. Change no non-Python file and make no
  other change. Do not commit. Reply with the list of files you changed."
  Score: Jaccard similarity `|R∩T| / |R∪T|` of the run's changed-line set R
  against the target's T, each line a `(path, +/-, text)` triple from
  `git diff -U0`.
- E2 (tests). Prompt: "In this git worktree, write a unittest test file at
  `hooks/tests/test_m228_collab_mode.py` for the function
  `collaboration_mode(root)` in `hooks/cairn_common.py`. Spec: it returns
  the word from a `# Collaboration mode: <word>` header line of
  `<root>/cairn/PROFILE.md`, lowercased. The key is matched
  case-insensitively, and a UTF-8 byte-order mark at the file start is
  tolerated. Only lines before the first line that starts with `## ` are
  read. It returns `owner` when the file or the line is absent, and it never
  raises. The tests must pass against the current code when run from the
  repo root with `python3 -m unittest hooks/tests/test_m228_collab_mode.py`.
  Write only that file. Do not commit. Reply with the number of tests."
- E3 (tests). Prompt: as E2, for `parse_roadmap_rows_full(roadmap_text)` in
  `hooks/cairn_common.py`, file `hooks/tests/test_m228_roadmap_rows.py`.
  Spec: "for each line whose text, after leading whitespace, starts with
  `|`, it splits the line on `|`, drops the first and last pieces, and
  strips each cell. A line with fewer than six cells, or whose first cell
  does not start with `M`, yields nothing. Otherwise it yields the tuple
  (id, title, status, depends, priority, relpath) from the first six cells,
  with status lowercased."
- Score for E2 and E3: the fraction of the six mutants below that the run's
  test file kills (a mutant is killed when the file's unittest run exits
  non-zero on it). A file that fails or errors on the unmutated code scores
  0. Each run is scored in a fresh `git archive c023018` copy, from its
  root, under `PYTHONDONTWRITEBYTECODE=1`.

### History-review group (blame-history, prior-PR-comments)

Prompt, with `<SHA>`, `<FILE>`, and `<LENS>` per task:

> You are a fresh-context reviewer. You did not write this change. The change
> under review is commit <SHA> in /Users/jmgirard/github/cairn, a squash
> merge of one milestone. Its diff is `git show <SHA>` and its base is
> `<SHA>^`. Its milestone file at that commit is
> `git show <SHA>:cairn/milestones/<FILE>`. The working tree is shared:
> use ref-based git only (`git show`, `git log`, `git blame` against refs,
> for example `git blame <SHA>^ -- <path>`), never checkout, switch, reset,
> or worktree, and edit nothing. Review history at or before <SHA> only.
> <LENS> Report each candidate finding, filtering nothing before reporting,
> and rank your own findings: most severe first, one sentence of
> justification each, no numeric scores. Give each finding as a numbered
> item with its file and line. If you find nothing, say so.

`<LENS>` is the lens paragraph of `skills/milestone-review/SKILL.md` at
`c023018` for that reviewer, quoted from its bold name to the end of its
bullet, with `<default-branch>..HEAD` read as `<SHA>^..<SHA>`.

- H1. Blame-history lens on `c433537` (M226, pane code),
  `<FILE>` = `M226-pane-hotfix-prs.md`.
- H2. Blame-history lens on `5ec2bb3` (M227, skill prose),
  `<FILE>` = `M227-status-hotfix-prs.md`.
- H3. Prior-PR-comments lens on `d453629` (M225, pane code, whose files
  the M222 to M224 archive reviews also touch), `<FILE>` = `M225-pane-pr-comments.md`.

Score: the number of distinct findings that a model-blind Opus judge rates
valid. One judge per task sees both runs' finding lists under shuffled
labels A and B, with the diff and refs, and rates each finding valid (the
history or prior review it cites exists and the diff does conflict with it)
or invalid. A finding that repeats an earlier one in the same list counts
once. The label-to-model mapping is recorded only after the judge returns.
