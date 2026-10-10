# Haiku 5.5 against Sonnet 5.5 on cairn's Sonnet roles (M228)

**Provenance.** Ingested 2026-10-09 by M228 from first-hand runs: subagents
spawned with the Agent tool from a Claude Code desktop session in this repo,
each run's cost read from its subagent transcript under
`~/.claude/projects/-Users-jmgirard-github-cairn/<session>/subagents/`. Prices
from Anthropic's pricing page (cited below). Tasks replay this repo at commit
`c023018`.
Pagination: —.
Extraction: prices read directly from the pricing page 2026-10-09 and liable to change; the run records are first-hand from that day's session store, and a rerun reproduces the method, not the exact figures — observed 2026-10-09.

**Scope.** Measures whether Haiku 5.5 does the work of each role group that
tracking-rules "Model and agent strategy" gave to Sonnet (observed
2026-10-09) for less money and with a score at least 0.9 times Sonnet's. It
records a measurement and a verdict per group. It changes no rule: M229 acts
on the verdicts. This is a reference, not an authority: status lives in
`ROADMAP.md`, decisions in `DECISIONS.md`.

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
record gives the exact output of earlier calls (observed 2026-10-09), so
every row's cost is a lower bound.

Two older records predate the store this note reads. `scripts/cairn_cost.py`
and `session-cost-notes.md` (ledger row A4) say subagent turns are absent
from the session store, which held when observed on 2026-07-19; each
session's `subagents/agent-*.jsonl` now holds them, the oldest such file on
this machine dated 2026-08-13 (observed 2026-10-09). `cairn_cost.py` also
sums every assistant record, where this note groups records by
`message.id`. `session-cost-notes.md` carries the correction; the script is
the ROADMAP candidate "Session-store reading in `cairn_cost.py`".

Prices, USD per million tokens, from
<https://platform.claude.com/docs/en/about-claude/pricing> (read 2026-10-09).
The `claude-api` skill's cached model table gave Sonnet 5.5 cache reads at
0.20; the live page gives 0.10, and this note uses the page. At 0.20 every
Sonnet row costs more, so no verdict changes.

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
where A and K are sets (repeats count once) of items compared after
trimming whitespace and backticks. A reply with no `ANSWER:` line scores 0.

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

Judge prompt (added after review return 1, 2026-10-09), with `<SHA>`,
`<JLENS>`, and the two report paths per task:

> You are a judge rating code-review findings. Two reviewers, labeled A and
> B, independently reviewed commit <SHA> in /Users/jmgirard/github/cairn
> (diff `git show <SHA>`, base `<SHA>^`) with this lens: "<JLENS>" Reviewer
> A's report: <path A> Reviewer B's report: <path B> Read only those two
> files in their directory. In the repo use ref-based git only (git show,
> git log, git blame against refs); edit nothing. Rate each numbered finding
> in each report VALID or INVALID by this rule: a finding is valid when the
> history or prior review it cites exists and the diff does conflict with
> it; otherwise it is invalid. A finding that repeats an earlier one in the
> same report counts once: rate the repeat DUPLICATE. Unnumbered notes are
> not findings. Return one line per finding, `A1: VALID|INVALID|DUPLICATE —
> <one-sentence reason>`, then the B lines, then `A valid: <n>` and
> `B valid: <n>`.

`<JLENS>` for H1 and H2: "Blame-history reviewer. Runs `git log` / `git
blame` on the modified lines and judges the change against the intent of
the code it touches: does it silently undo something a past milestone added
deliberately, resurrect a fixed bug, or contradict a recorded D-entry?" For
H3: "Prior-PR-comments reviewer. Reads the repo's prior review record on the
modified files and flags only where the current diff reintroduces or
contradicts a point a past review raised on those files."

## Answer keys, target, and mutants (built 2026-10-09, before any run)

The three keys are the output of this Python 3 code, run from the repo root
(code added after review return 2; it is the code the keys were built with):

```python
import json, re, subprocess
PIN = "c023018"
sh = lambda c: subprocess.run(c, shell=True, check=True, capture_output=True, text=True).stdout

def key_s1():
    out = sh(f"git grep -l -E '^\\s*(import cairn_common|from cairn_common import)' {PIN} -- scripts hooks")
    return sorted(l.split(":", 1)[1] for l in out.split())

def key_s2():
    d = json.loads(sh(f"git show {PIN}:hooks/hooks.json"))
    items = []
    for ev, arr in d["hooks"].items():
        for m in arr:
            for h in m["hooks"]:
                if h.get("type") == "command":
                    script = re.search(r"([A-Za-z0-9_]+\.py)", h["command"]).group(1)
                    items.append(f"{ev} {m.get('matcher') or '*'} {script}")
    return items

def key_s3():
    pairs = []
    for line in sh(f"git show {PIN}:cairn/DECISIONS.md").splitlines():
        if not line.startswith("### D-"):
            continue
        own = re.match(r"### (D-\d+)", line).group(1)
        m = re.search(r"supersed", line, re.I)
        if m:
            for old in re.findall(r"D-\d+", line[m.start():]):
                if old != own and f"{own} {old}" not in pairs:
                    pairs.append(f"{own} {old}")
    return pairs
```

S1 key (10 items): `hooks/commit_guard.py`,
`hooks/force_push_guard.py`, `hooks/idea_guard.py`, `hooks/memory_guard.py`,
`hooks/merge_guard.py`, `hooks/merge_guard_post.py`,
`hooks/session_context.py`, `hooks/stop_guard.py`, `scripts/cairn_impact.py`,
`scripts/cairn_scripts.py`.

S2 key (9 items):
`SessionStart * session_context.py`, `Stop * stop_guard.py`,
`PreToolUse Bash merge_guard.py`, `PreToolUse Bash commit_guard.py`,
`PreToolUse Bash force_push_guard.py`, `PreToolUse Write memory_guard.py`,
`PreToolUse mcp__.*__spawn_task idea_guard.py`,
`PostToolUse Bash merge_guard_post.py`,
`PostToolUseFailure Bash merge_guard_post.py`.

S3 key (88 distinct pairs, counted by `len()` of the built key; corrected
M228 from 89). Without the code's repeat check the same rule lists 91,
because two headings name an id twice after the word.
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
target diff removes 21 lines and adds 21 over 11 files (`git diff --stat`,
corrected M228 from "32 lines"). Its changed-line set T, the set the Jaccard
score compares, holds 32 distinct triples, because some files repeat an
identical line.

Mutants (exact strings corrected M228 after review return 1), each one
`str.replace` of an old string that occurs exactly once in
`hooks/cairn_common.py` at `c023018`. In the strings, `\n` is a line break
and leading spaces are as in the file; "(empty)" is the empty string.

| Task | Mutant | Old string | New string |
|---|---|---|---|
| E2 | m1 | `return m.group(1).lower()` | `return m.group(1)` |
| E2 | m2 | `                if line.startswith("## "):\n                    break\n` | (empty) |
| E2 | m3 | `open(path, encoding="utf-8-sig")` | `open(path, encoding="utf-8")` |
| E2 | m4 | `    except Exception:\n        return "owner"\n    return "owner"` | `    except Exception:\n        return "guest"\n    return "owner"` |
| E2 | m5 | `        return "owner"\n    return "owner"` | `        return "owner"\n    return None` |
| E2 | m6 | `r"#\s*Collaboration mode:\s*(\S+)", re.IGNORECASE)` | `r"#\s*Collaboration mode:\s*(\S+)")` |
| E3 | n1 | `if not line.lstrip().startswith("\|"):` | `if not line.startswith("\|"):` |
| E3 | n2 | `if len(cells) < 6 or` | `if len(cells) < 7 or` |
| E3 | n3 | ` or not cells[0].startswith("M"):` | `:` |
| E3 | n4 | `cells[2].lower(), cells[3]` | `cells[2], cells[3]` |
| E3 | n5 | `cells = [c.strip() for c in line.split("\|")][1:-1]` | `cells = [c for c in line.split("\|")][1:-1]` |
| E3 | n6 | `cells[2].lower(), cells[3], cells[4], cells[5]` | `cells[2].lower(), cells[4], cells[3], cells[5]` |

In the n-rows, `\|` is a literal `|` escaped for the table.

Controls: a hand-written reference test file kills 6 of 6 mutants for E2
and 6 of 6 for E3 and passes on the unmutated code. A file holding one
always-true test kills 0 of 6 for E2 and 0 of 6 for E3 (the E3 run added
2026-10-09, after review pass 2).

## Runs

Agent ids name each run's subagent transcript, `agent-<id>.jsonl` under
`~/.claude/projects/-Users-jmgirard-github-cairn/914c172c-a7d8-4341-b5be-8f75283fc564/subagents/`.
"Model ids" lists every `model` value on the transcript's assistant records.
"Final match" says whether the Agent tool result's input and cache counts
equal the final id's last-record counts. Token columns sum the row's calls.
The run table holds all 18 runs; the notes after it go by group.

| Task | Model | Agent id | Model ids | Calls | Final match | Input | 5m write | 1h write | Cache read | Output | USD | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | sonnet | `a507fc85cce3e1c5d` | claude-sonnet-5-5 | 4 | yes | 8 | 39506 | 0 | 111383 | 624 | 0.1162 | 1.0000 |
| S1 | haiku | `aa6923d0993e9e008` | claude-haiku-5-5 | 2 | yes | 4 | 38858 | 0 | 36121 | 1177 | 0.0058 | 1.0000 |
| S2 | sonnet | `a40aa40dd7410ef86` | claude-sonnet-5-5 | 2 | yes | 4 | 38029 | 0 | 36142 | 587 | 0.1046 | 1.0000 |
| S2 | haiku | `af8e9566575845fca` | claude-haiku-5-5 | 2 | yes | 4 | 38448 | 0 | 36140 | 1378 | 0.0059 | 0.0000 |
| S3 | sonnet | `a7d06115f06e661f5` | claude-sonnet-5-5 | 2 | yes | 4 | 42137 | 0 | 36164 | 3519 | 0.1442 | 0.6767 |
| S3 | haiku | `a08640fdf2c9f753a` | claude-haiku-5-5 | 3 | yes | 6 | 56781 | 0 | 84338 | 4237 | 0.0101 | 1.0000 |
| E1 | sonnet | `a9dfb4d4c5d75cf2d` | claude-sonnet-5-5 | 4 | yes | 8 | 54344 | 0 | 157944 | 533 | 0.1570 | 1.0000 |
| E1 | haiku | `a2fcaa827b9415e99` | claude-haiku-5-5 | 9 | yes | 18 | 58653 | 0 | 448108 | 556 | 0.0121 | 1.0000 |
| E2 | sonnet | `a260f9308a2bc485b` | claude-sonnet-5-5 | 4 | yes | 8 | 59189 | 0 | 160585 | 421 | 0.1683 | 1.0000 |
| E2 | haiku | `a402fd9aeaa7d5d4f` | claude-haiku-5-5 | 6 | yes | 12 | 69489 | 0 | 300615 | 320 | 0.0119 | 1.0000 |
| E3 | sonnet | `ac124eccb4da7fbdb` | claude-sonnet-5-5 | 4 | yes | 8 | 57058 | 0 | 158507 | 463 | 0.1631 | 1.0000 |
| E3 | haiku | `a59fa08d0b88b3b84` | claude-haiku-5-5 | 7 | yes | 14 | 73988 | 0 | 373525 | 7503 | 0.0167 | 1.0000 |
| H1 | sonnet | `ab3cb7532d6192593` | claude-sonnet-5-5 | 12 | yes | 24 | 60378 | 0 | 903735 | 2553 | 0.2669 | 1 |
| H1 | haiku | `a8ce7b385db7f0e77` | claude-haiku-5-5 | 36 | yes | 72 | 113496 | 0 | 3716111 | 4059 | 0.1844 | 1 |
| H2 | sonnet | `a08bb633f7bea0b4b` | claude-sonnet-5-5 | 8 | yes | 16 | 38171 | 0 | 491838 | 1764 | 0.1623 | 1 |
| H2 | haiku | `a60621730679c16bd` | claude-haiku-5-5 | 15 | yes | 30 | 78929 | 0 | 1328999 | 1250 | 0.0646 | 0 |
| H3 | sonnet | `ab840bc451b9aa0ca` | claude-sonnet-5-5 | 8 | yes | 16 | 45229 | 0 | 466325 | 1771 | 0.1774 | 2 |
| H3 | haiku | `a2a141b30ecb7543f` | claude-haiku-5-5 | 32 | yes | 64 | 119622 | 0 | 3468124 | 1455 | 0.1828 | 3 |

Search notes. S2 Haiku listed all nine registrations correctly but wrote
each script without its `.py` extension (`session_context`), so no item
matched the key and the fixed rule scores it 0. The prompt said "base
name" and did not say whether the extension is part of it. S3 Sonnet
applied its own reading of which heading clauses "supersede" and listed 45
pairs, all in the key, where the prompt's rule counts every id after the
word (88 pairs). Haiku followed the stated rule.

Edit-work notes. Both E1 runs produced the target diff exactly, 11 files.
All four test files passed on the unmutated code and killed all six
mutants: Sonnet wrote 23 and 18 tests, Haiku 21 and 30. The mutant scoring
can tell runs apart (the always-true control kills 0 of 6), but both models
reached 1.0 on every task. The test files were written in non-final calls,
whose output counts are too low, so these rows' output columns leave out
most of the test code each run wrote.

Review notes. Judges (Opus, model `claude-opus-5-5`), run with the judge
prompt above: H1 `a712b3ed31e25ea06`, H2 `a1f764706bb2969f0`, H3
`a7849bedfc57f6132`. Labels were drawn with `random.SystemRandom` and
written to a mapping file in the session scratchpad, beside the report
files, before the judges ran; the judges were told to read only their two
report files, and their transcripts show no read of the mapping. The
mappings were read after all three judges returned: H1 A was Sonnet and B
Haiku, H2 A Sonnet and B Haiku, H3 A Haiku and B Sonnet. No finding was
rated a duplicate. A first judging (H1 `a0fdaeea99a7f83ab`, H2
`a1e319f359d98aa70`, H3 `a4663e806d063642e`) used a prompt that also
counted a finding valid when the diff left something stale or
inconsistent, which is wider than the rule above. It gave Sonnet 5, 3, 2
and Haiku 3, 2, 4, and review return 1 replaced it. On the three review
tasks Haiku used 1.9 to 4.0 times as many calls as Sonnet (36 against 12,
15 against 8, 32 against 8). On H3, its 32 calls against Sonnet's 8, 19 of
them over the 100,000-token prompt tier, made its row cost more than
Sonnet's; H1 Haiku had 20 of 36 calls over the tier and still cost less.

Per-finding ratings, rebuilt from both judgings' reports and their label
mappings (1st = first judging, 2nd = the judging the scores use; V valid,
I invalid). The finding number is the reviewer's own.

| Task | Model | # | Finding, in short | 1st | 2nd |
|---|---|---|---|---|---|
| H1 | sonnet | 1 | a failed `git` call empties the hotfix list | V | I |
| H1 | sonnet | 2 | two separate state writes can draw a torn state | V | V |
| H1 | sonnet | 3 | `readPrs` is no longer free with no URL; comment stale | I | I |
| H1 | sonnet | 4 | the Hotfixes heading's Refresh rule differs from Blocked | V | I |
| H1 | sonnet | 5 | an in-process `/clear` also empties the hotfix list | V | I |
| H1 | sonnet | 6 | AC4 says seven cases, the evidence says 8 | V | I |
| H1 | haiku | 1 | first use of `cwd` in the mod is untested | V | I |
| H1 | haiku | 2 | timeout and Refresh comments and DESIGN text stale | V | V |
| H1 | haiku | 3 | a failed `git` call empties the list, unlike M210 | V | I |
| H1 | haiku | 4 | every pane open now runs `git` and `gh` | I | I |
| H2 | sonnet | 1 | the review record says rewrapped, the line is 117 characters | V | V |
| H2 | sonnet | 2 | someone else's `hotfix-*` PR is dropped and unreported | V | I |
| H2 | sonnet | 3 | a short orphan line in the hotfix skill | V | I |
| H2 | haiku | 1 | the inbox filter keeps the `hotfix-*` drop | V | I |
| H2 | haiku | 2 | the plan skill's inbox has the same drop | V | I |
| H3 | sonnet | 1 | `counts.ts` keeps a second copy of the PR URL pattern | V | V |
| H3 | sonnet | 2 | serial `gh` calls double the wait to 30 s | V | V |
| H3 | haiku | 1 | DESIGN still names the old pane shape tag | V | I |
| H3 | haiku | 2 | DESIGN's count-call timeout text is stale | V | V |
| H3 | haiku | 3 | README lines run past the wrap width | V | V |
| H3 | haiku | 4 | a ragged wrap in CHANGELOG | V | V |
| H3 | haiku | 5 | the state-contract type change has no type check | I | I |

The two judgings rate 11 of these 22 findings differently, and the second
rates none valid that the first rated invalid.

## Verdicts

| Group | Sonnet USD | Haiku USD | Sonnet score | Haiku score | Haiku ÷ Sonnet score | Verdict | What could flip it |
|---|---|---|---|---|---|---|---|
| Search | 0.3650 | 0.0218 | 2.6767 | 2.0000 | 0.7472 | stay | Rescoring S2's format miss (not done) |
| Edit work | 0.4884 | 0.0407 | 3.0000 | 3.0000 | 1.0000 | move | Nothing measured here |
| History review | 0.6066 | 0.4318 | 4 | 4 | 1.0000 | move | The output undercount (cost); the judging rule (score) |

Each verdict applies the rule fixed in the design: `move` when Sonnet's
summed score is above zero, Haiku's summed cost is below Sonnet's, and
Haiku's summed score is at least 0.9 times Sonnet's.

Readings that bear on the verdicts:

- Search is `stay`. S2's zero is the whole gap: with the `.py` extensions
  Haiku would score 3.0, above Sonnet's 2.6767. The rule was fixed before
  the runs and is not rescored here.
- Edit work is at the ceiling for both models. Haiku did these three tasks
  as well as Sonnet, and the tasks cannot show a gap on harder edits.
- History review is `move` with equal scores, 4 against 4, on one run per
  task. Per task it is 1 against 1, 0 against 1 (H2, Haiku lower), and 3
  against 2. One fewer Haiku finding leaves it at 3 against 4 (0.75),
  which is `stay`. Under the first judging's wider rule it was 9 against 10
  (0.9), exactly at the margin.
- The history-review score counts reported findings that the judge rated
  valid. It does not measure real conflicts that a reviewer missed, which
  is the risk D-016 named for a weaker model in a review step ("can
  silently drop a real bug"). This note does not test that risk.
- Costs are lower bounds (see Cost). For a group's comparison to reverse,
  Haiku's unrecorded output, priced at its higher tier, would need to
  exceed the cost gap even with Sonnet's unrecorded output taken as zero.
  That break-even is about 137,000 tokens for search (34,000 per non-final
  Haiku call), 179,000 for edit work (9,400 per call), and 70,000 for
  history review (870 per call). The search and edit comparisons need tens
  of thousands of unrecorded tokens per call to reverse. The history-review
  comparison reverses at 870 unrecorded output tokens per call, thinking
  included, and this note has no measure of how many there were.

## Limits and re-measurement

One run per model per task, three tasks per group, at default effort, on
tasks drawn from this repo. The judge is one Opus reader per task, and two
judgings under different rules rated 11 of 22 findings differently. The
measurement helpers were session-local and are not committed (observed
2026-10-09). To re-measure: re-run the nine task prompts and the judge
prompt above with the same models, take each run's input and cache counts
from its subagent transcript and its final call's output from the session
transcript's Agent tool result, score with the keys and mutants above, and
apply the verdict rule. A rerun that flips a group's verdict falsifies
M228's single-run choice for that group.
