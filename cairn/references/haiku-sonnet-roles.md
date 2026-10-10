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

**Cost.** For each subagent transcript, records are grouped by `message.id`,
one id per API call, and each id's counts come from its last record. Per id,
cost is the sum over five classes of count times price: `input_tokens`,
`cache_creation.ephemeral_5m_input_tokens`,
`cache_creation.ephemeral_1h_input_tokens`, `cache_read_input_tokens`,
`output_tokens`. A row's cost is the sum over its ids, recorded to four
decimal places. Haiku prices depend on each call's prompt size, the sum of
its input, both cache-write, and cache-read counts: a call over 100,000
pays the higher row of the table below for every class.

The subagent transcript records each call's `output_tokens` at stream start
(amended 2026-10-09, after the search runs). The input and cache counts are
complete, but the output counts are too low, for example 6 where the call
produced 4,227. The run's final call, the last distinct `message.id` in
record order, therefore takes its output count from the `usage` of the
Agent tool result whose `agentId` matches the transcript's file name, in
the main session transcript
`~/.claude/projects/-Users-jmgirard-github-cairn/914c172c-a7d8-4341-b5be-8f75283fc564.jsonl`.
Each row records whether that `usage`'s input and cache counts equal the
final id's last-record counts, which ties the tool result to that call. No
source gives the true output of earlier calls, so every row's cost is a
lower bound.

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

## Answer keys, target, and mutants (built 2026-10-09, before any run)

S1 key, from `git grep -l -E '^\s*(import cairn_common|from cairn_common
import)' c023018 -- scripts hooks` (10 items): `hooks/commit_guard.py`,
`hooks/force_push_guard.py`, `hooks/idea_guard.py`, `hooks/memory_guard.py`,
`hooks/merge_guard.py`, `hooks/merge_guard_post.py`,
`hooks/session_context.py`, `hooks/stop_guard.py`, `scripts/cairn_impact.py`,
`scripts/cairn_scripts.py`.

S2 key, from a JSON parse of `git show c023018:hooks/hooks.json`, taking
each `type: command` hook under `hooks`, its event, its matcher (`*` when
absent), and the first `*.py` name in its command (9 items):
`SessionStart * session_context.py`, `Stop * stop_guard.py`,
`PreToolUse Bash merge_guard.py`, `PreToolUse Bash commit_guard.py`,
`PreToolUse Bash force_push_guard.py`, `PreToolUse Write memory_guard.py`,
`PreToolUse mcp__.*__spawn_task idea_guard.py`,
`PostToolUse Bash merge_guard_post.py`,
`PostToolUseFailure Bash merge_guard_post.py`.

S3 key, from each `### D-` heading of `git show c023018:cairn/DECISIONS.md`
that matches `supersed` (case-insensitive): every `D-NNN` after the first
match, other than the heading's own id, paired with that id (88 pairs, counted by `len()` of the built key;
corrected M228 from 89).
D-027 D-026, D-038 D-037, D-058 D-049, D-058 D-052, D-062 D-004,
D-065 D-064, D-071 D-056, D-072 D-071, D-074 D-046, D-074 D-030,
D-074 D-045, D-074 D-063, D-079 D-067, D-079 D-069, D-080 D-079,
D-081 D-065, D-083 D-082, D-083 D-067, D-083 D-069, D-083 D-070,
D-083 D-081, D-084 D-083, D-085 D-083, D-085 D-084, D-086 D-085,
D-087 D-069, D-087 D-070, D-088 D-083, D-089 D-088, D-091 D-085,
D-091 D-064, D-092 D-091, D-095 D-069, D-095 D-070, D-095 D-080,
D-095 D-082, D-095 D-083, D-095 D-085, D-095 D-088, D-095 D-091,
D-095 D-079, D-095 D-067, D-095 D-090, D-096 D-095, D-099 D-091,
D-100 D-099, D-102 D-101, D-105 D-064, D-105 D-098, D-106 D-105,
D-108 D-090, D-110 D-016, D-110 D-078, D-113 D-111, D-114 D-057,
D-115 D-052, D-116 D-099, D-116 D-108, D-117 D-115, D-118 D-111,
D-118 D-098, D-120 D-118, D-120 D-111, D-120 D-098, D-121 D-120,
D-123 D-037, D-123 D-038, D-124 D-003, D-124 D-022, D-124 D-019,
D-124 D-123, D-126 D-090, D-126 D-108, D-129 D-021, D-129 D-020,
D-129 D-027, D-134 D-027, D-134 D-035, D-134 D-108, D-144 D-124,
D-144 D-067, D-144 D-110, D-144 D-003, D-144 D-022, D-144 D-050,
D-147 D-145, D-147 D-146, D-148 D-144.

E1 target: in a `git archive c023018` copy, `perl -pi -e
's/\bfind_cairn_root\b/locate_cairn_root/g'` over each file that
`git grep -l -w find_cairn_root -- 'scripts/*.py' 'hooks/*.py'` lists. The
target diff changes 32 lines in 11 files.

Mutants, each one exact-string replacement in `hooks/cairn_common.py` that
occurs once at `c023018`:

| Task | Mutant | Change |
|---|---|---|
| E2 | m1 | `return m.group(1).lower()` loses `.lower()` |
| E2 | m2 | the `if line.startswith("## "): break` lines are removed |
| E2 | m3 | `encoding="utf-8-sig"` becomes `"utf-8"` |
| E2 | m4 | the `except` branch returns `"guest"` |
| E2 | m5 | the final `return "owner"` becomes `return None` |
| E2 | m6 | `COLLAB_MODE_LINE` loses `re.IGNORECASE` |
| E3 | n1 | `line.lstrip().startswith("\|")` becomes `line.startswith("\|")` |
| E3 | n2 | `len(cells) < 6` becomes `< 7` |
| E3 | n3 | the `not cells[0].startswith("M")` test is removed |
| E3 | n4 | `cells[2].lower()` becomes `cells[2]` |
| E3 | n5 | cells are not stripped |
| E3 | n6 | the depends and priority cells swap places |

Controls: a hand-written reference test file kills 6 of 6 mutants for E2
and 6 of 6 for E3 and passes on the unmutated code. A file holding one
always-true test kills 0 of 6 for E2.

## Runs

Agent ids name each run's subagent transcript, `agent-<id>.jsonl` under
`~/.claude/projects/-Users-jmgirard-github-cairn/914c172c-a7d8-4341-b5be-8f75283fc564/subagents/`.
"Model ids" lists every `model` value on the transcript's assistant records.
"Final match" says whether the Agent tool result's input and cache counts
equal the final id's last-record counts. Token columns sum the row's calls.

| Task | Model | Agent id | Model ids | Calls | Final match | Input | 5m write | 1h write | Cache read | Output | USD | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | sonnet | `a507fc85cce3e1c5d` | claude-sonnet-5-5 | 4 | yes | 8 | 39506 | 0 | 111383 | 624 | 0.1162 | 1.0000 |
| S1 | haiku | `aa6923d0993e9e008` | claude-haiku-5-5 | 2 | yes | 4 | 38858 | 0 | 36121 | 1177 | 0.0058 | 1.0000 |
| S2 | sonnet | `a40aa40dd7410ef86` | claude-sonnet-5-5 | 2 | yes | 4 | 38029 | 0 | 36142 | 587 | 0.1046 | 1.0000 |
| S2 | haiku | `af8e9566575845fca` | claude-haiku-5-5 | 2 | yes | 4 | 38448 | 0 | 36140 | 1378 | 0.0059 | 0.0000 |
| S3 | sonnet | `a7d06115f06e661f5` | claude-sonnet-5-5 | 2 | yes | 4 | 42137 | 0 | 36164 | 3519 | 0.1442 | 0.6767 |
| S3 | haiku | `a08640fdf2c9f753a` | claude-haiku-5-5 | 3 | yes | 6 | 56781 | 0 | 84338 | 4237 | 0.0101 | 1.0000 |

Search notes. S2 Haiku listed all nine registrations correctly but wrote
each script without its `.py` extension (`session_context`), so no item
matched the key and the fixed rule scores it 0. The prompt's "base name"
allows that reading. S3 Sonnet applied its own reading of which heading
clauses "supersede" and listed 45 pairs, all in the key, where the prompt's
rule counts every id after the word (88 pairs). Haiku followed the stated
rule.
