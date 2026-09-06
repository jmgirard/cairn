#!/usr/bin/env python3
"""cairn ci-paths — report each workflow's push/pull_request triggers, or add
the `cairn/**` `paths-ignore` item under each editable `push` trigger.

Every push of a milestone or hotfix branch starts the repo's push-triggered
workflows, cairn's tracking-only commits included. A `paths-ignore` of
`cairn/**` under a workflow's `push` trigger skips those runs; a
`pull_request` trigger's filter reads the whole PR diff, so the ignore does
not help there.

    python3 scripts/cairn_ci_paths.py [ROOT] --report
    python3 scripts/cairn_ci_paths.py [ROOT] --apply [--dry-run]

ROOT defaults to the working directory; either is walked up to the enclosing
git repository root (a `.git` entry), where `.github/workflows/` is read.
Exactly one of `--report` and `--apply` is given (both, neither, or
`--dry-run` without `--apply` is a usage error, exit 2); exit 2 outside a
git repository.

`--report` (stdlib only) prints one line per `*.yml` / `*.yaml` file directly
under `.github/workflows/`, carrying one of three verdicts: the triggers
among `push` and `pull_request` the file's `on:` names, each with the filter
keys present under it (`branches`, `branches-ignore`, `paths`,
`paths-ignore`) and `cairn/**` when its `paths-ignore` holds that entry;
`no push or pull_request trigger`; or `unrecognized`, for a file the reader
cannot place or cannot read. The reader is line-based and places an
unquoted or quoted `on:` key holding a plain scalar, a flow list, or a block
map whose trigger values are block mappings, flow mappings, flow sequences,
scalars, or nothing; comments are ignored. `--report` writes nothing.

`--apply` needs PyYAML, imported only on this path: when the import fails
the script exits 3 with a message naming PyYAML and writes nothing. It
prints one line per workflow file — `<file>: applied` (`would apply` under
`--dry-run`) or `<file>: refused: <reason>` — and exits 0 whatever the
per-file verdicts. A file is edited exactly when PyYAML composes it as one
document whose top-level mapping has a plain or quoted `on` key holding a
block mapping with a `push` key whose value is a block mapping or null,
carrying no `paths` key, and whose `paths-ignore` is absent or a block
sequence not holding `cairn/**`. The edit inserts lines only, placed by the
composed nodes' marks: `- 'cairn/**'` at the existing items' column after
the last item, or a `paths-ignore:` key at the `push` children's column
(for a null `push`, one indent step under the `on` children) followed by
the item; line endings are preserved. Before writing, `yaml.safe_load` of
the edited text must equal that of the original with `cairn/**` appended
under `on` → `push` → `paths-ignore`; otherwise the file is refused with
`post-edit check failed`. Every refusal leaves the file byte-identical.
`--dry-run` writes nothing and prints `would apply` for exactly the files
`--apply` would edit.
"""

import os
import re
import sys

ENTRY = "cairn/**"
TRIGGERS = ("push", "pull_request")
FILTER_KEYS = ("branches", "branches-ignore", "paths", "paths-ignore")
NO_TRIGGER = "no push or pull_request trigger"
UNRECOGNIZED = "unrecognized"
ITEM_TEXT = "- 'cairn/**'"
NO_PYYAML = 3

# `--apply` refusal reasons (a closed list; each leaves the file byte-identical)
R_PARSE = "PyYAML cannot parse the file"
R_DOCS = "more than one document"
R_NO_ON = "no `on` key"
R_ON_NOT_BLOCK = "`on` is not a block mapping"
R_NO_PUSH = "no `push` trigger"
R_PUSH_FLOW = "`push` holds a flow mapping"
R_PUSH_PATHS = "`push` carries `paths`"
R_IGNORE_NOT_SEQ = "`paths-ignore` is not a block sequence"
R_ALREADY = "already ignores `cairn/**`"
R_POST_EDIT = "post-edit check failed"

_ON_KEY = re.compile(r"""^(?P<key>on|"on"|'on')\s*:(?P<rest>.*)$""")
_WORD = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
_MAP_KEY = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_-]*)\s*:(?P<rest>.*)$")
_SEQ_ITEM = re.compile(r"^(?P<indent>\s*)-\s+(?P<value>.*)$")
_COMMENT = re.compile(r"(^|\s)#.*$")


class Unplaced(Exception):
    """A file the reader cannot place; the verdict is `unrecognized`."""


# --------------------------------------------------------------------------
# Root and file discovery
# --------------------------------------------------------------------------

def find_git_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def workflow_files(root):
    wf = os.path.join(root, ".github", "workflows")
    if not os.path.isdir(wf):
        return wf, []
    names = sorted(
        n for n in os.listdir(wf)
        if n.endswith((".yml", ".yaml")) and os.path.isfile(os.path.join(wf, n))
    )
    return wf, [os.path.join(wf, n) for n in names]


# --------------------------------------------------------------------------
# Reading — a line-based reader for the `on:` key
# --------------------------------------------------------------------------

def split_lines(data):
    """Decode bytes to lines without endings (LF or CRLF)."""
    text = data.decode("utf-8")
    return text.replace("\r\n", "\n").split("\n")


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _strip_comment(line):
    """The line without its YAML comment."""
    m = _COMMENT.search(line)
    return line[: m.start()].rstrip() if m else line


def _is_blank(line):
    """Blank or comment-only: contributes nothing to structure."""
    return _strip_comment(line).strip() == ""


def _flow_map_keys(rest):
    """Top-level `key: value` pairs of a flow mapping `{...}` as (key, value text)."""
    inner = rest.strip()
    if not (inner.startswith("{") and inner.endswith("}")):
        return []
    pairs, depth, buf = [], 0, ""
    for ch in inner[1:-1] + ",":
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            if ":" in buf:
                key, value = buf.split(":", 1)
                pairs.append((key.strip(), value.strip()))
            buf = ""
        else:
            buf += ch
    return pairs


def _strip_quotes(value):
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    return v


def _flow_list_items(text):
    return [_strip_quotes(x) for x in text.strip().strip("[]").split(",")]


class Workflow:
    """One read workflow file.

    Attributes: triggers (names `on:` lists, in order; None when unplaced),
    filters (trigger -> dict of FILTER_KEYS presence plus "cairn" for a
    `cairn/**` entry under `paths-ignore`).
    """

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.triggers = None
        self.filters = {}
        self.lines = []
        try:
            with open(path, "rb") as fh:
                self.lines = split_lines(fh.read())
            self._read()
        except (Unplaced, UnicodeDecodeError, OSError):
            self.triggers = None

    # -- locating `on:` ----------------------------------------------------

    def _read(self):
        hits = [i for i, l in enumerate(self.lines) if _ON_KEY.match(_strip_comment(l))]
        if len(hits) != 1:
            raise Unplaced("no single top-level `on:` key")
        i = hits[0]
        rest = _ON_KEY.match(_strip_comment(self.lines[i])).group("rest").strip()
        # the block extends to the next structural column-0 line
        j = i + 1
        while j < len(self.lines) and (_is_blank(self.lines[j]) or _indent(self.lines[j]) > 0):
            j += 1
        if rest == "":
            self._read_block(i + 1, j)
        elif rest.startswith("["):
            self._read_flow(rest, i + 1, j)
        else:
            self._read_scalar(rest, i + 1, j)

    def _read_scalar(self, rest, start, end):
        if any(not _is_blank(l) for l in self.lines[start:end]):
            raise Unplaced("content indented under a scalar `on:`")
        if not _WORD.match(rest):
            raise Unplaced("`on:` scalar is not a plain word")
        self.triggers = [rest]
        self.filters = {rest: self._no_filters()} if rest in TRIGGERS else {}

    def _read_flow(self, rest, start, end):
        if any(not _is_blank(l) for l in self.lines[start:end]):
            raise Unplaced("content indented under a flow-list `on:`")
        if not rest.endswith("]"):
            raise Unplaced("flow list does not close on the `on:` line")
        inner = rest[1:-1].strip()
        if not inner:
            raise Unplaced("empty flow list")
        items = [x.strip() for x in inner.split(",")]
        if any(not _WORD.match(x) for x in items):
            raise Unplaced("flow-list item is not a plain word")
        if len(set(items)) != len(items):
            raise Unplaced("duplicate trigger in flow list")
        self.triggers = items
        self.filters = {t: self._no_filters() for t in items if t in TRIGGERS}

    def _read_block(self, start, end):
        body = []
        for k in range(start, end):
            l = _strip_comment(self.lines[k])
            if l.strip() != "":
                body.append((k, l))
        if not body:
            raise Unplaced("`on:` holds nothing")
        for _, l in body:
            if "\t" in l[: _indent(l) + 1]:
                raise Unplaced("tab indentation in the `on:` block")
        key_indent = _indent(body[0][1])
        order, values = [], {}
        idx = 0
        while idx < len(body):
            k, l = body[idx]
            if _indent(l) != key_indent:
                raise Unplaced("inconsistent indentation in the `on:` block")
            m = _MAP_KEY.match(l)
            if not m:
                raise Unplaced("`on:` block entry is not a mapping key")
            trig = m.group("key")
            if trig in order:
                raise Unplaced("duplicate trigger in the `on:` block")
            j = idx + 1
            while j < len(body) and _indent(body[j][1]) > key_indent:
                j += 1
            order.append(trig)
            values[trig] = (m.group("rest").strip(), [l for _, l in body[idx + 1: j]])
            idx = j
        self.triggers = order
        for trig in order:
            if trig in TRIGGERS:
                self.filters[trig] = self._block_filters(*values[trig])

    def _block_filters(self, rest, value_lines):
        present = self._no_filters()
        if rest.startswith("{"):
            for key, value in _flow_map_keys(rest):
                if key in FILTER_KEYS:
                    present[key] = True
                    if key == "paths-ignore" and ENTRY in _flow_list_items(value):
                        present["cairn"] = True
            return present
        if rest != "" or not value_lines:
            return present  # scalar or flow-sequence value, or a bare key: no filter keys
        child_indent = _indent(value_lines[0])
        for n, l in enumerate(value_lines):
            if _indent(l) != child_indent:
                continue
            m = _MAP_KEY.match(l)
            if m and m.group("key") in FILTER_KEYS:
                present[m.group("key")] = True
                if m.group("key") == "paths-ignore" and self._has_entry(m, value_lines[n + 1:]):
                    present["cairn"] = True
        return present

    @staticmethod
    def _has_entry(m, following):
        rest = m.group("rest").strip()
        if rest.startswith("["):
            return ENTRY in _flow_list_items(rest)
        # items may sit deeper than the key or at its own indent (a legal,
        # common style); the sequence ends at the first line that is neither
        key_indent = len(m.group("indent"))
        for l in following:
            s = _SEQ_ITEM.match(l)
            if not s or _indent(l) < key_indent:
                break
            if _strip_quotes(s.group("value")) == ENTRY:
                return True
        return False

    @staticmethod
    def _no_filters():
        return {k: False for k in FILTER_KEYS + ("cairn",)}

    # -- reporting ---------------------------------------------------------

    def verdict(self):
        if self.triggers is None:
            return UNRECOGNIZED
        named = [t for t in self.triggers if t in TRIGGERS]
        if not named:
            return NO_TRIGGER
        parts = []
        for t in named:
            f = self.filters[t]
            present = [k for k in FILTER_KEYS if f[k]]
            if f["cairn"]:
                present.append(ENTRY)
            parts.append(f"{t} ({', '.join(present) if present else 'no filters'})")
        return ", ".join(parts)

    def report_line(self):
        return f"{self.name}: {self.verdict()}"



# --------------------------------------------------------------------------
# Applying — insertion placed by PyYAML's node marks
# --------------------------------------------------------------------------

_LINE = re.compile(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$")


class Refused(Exception):
    """The file is left untouched; `args[0]` is the reason."""


def _split_keepends(text):
    """Lines with their own endings (LF, CRLF, or lone CR), PyYAML's line count."""
    return _LINE.findall(text)


def _scalar_key(node, name):
    """True when `node` is the mapping key `name`, plain or single/double-quoted."""
    return (
        node.__class__.__name__ == "ScalarNode"
        and node.value == name
        and node.style in (None, "'", '"')
    )


def _mapping_get(mapping, name):
    """The (key, value) pair for `name` in a MappingNode, the last one when repeated."""
    found = None
    for key, value in mapping.value:
        if _scalar_key(key, name):
            found = (key, value)
    return found


def _is_null(node):
    return node.__class__.__name__ == "ScalarNode" and node.tag.endswith(":null")


def _first_content_line_before(lines, index):
    """Walk back from `index` over blank and comment-only lines."""
    while index > 0 and _is_blank(lines[index - 1].rstrip("\r\n")):
        index -= 1
    return index


def _end_index(lines, node):
    """The line index just past `node`, by its end mark.

    A block collection's end mark sits on the next token after it (the
    following key, or the stream end); a scalar's sits just past its text.
    """
    m = node.end_mark
    if node.__class__.__name__ != "ScalarNode" or m.column == 0:
        return m.line
    return m.line + 1


def plan_edit(yaml, text):
    """Where the insertion goes: (insert_index, [line bodies without endings]).

    Raises Refused with the reason when the file is not editable.
    """
    try:
        docs = list(yaml.compose_all(text))
    except yaml.YAMLError:
        raise Refused(R_PARSE)
    if len(docs) > 1:
        raise Refused(R_DOCS)
    root = docs[0] if docs else None
    if root is None or root.__class__.__name__ != "MappingNode":
        raise Refused(R_NO_ON)
    on = _mapping_get(root, "on")
    if on is None:
        raise Refused(R_NO_ON)
    on_key, on_value = on
    if on_value.__class__.__name__ != "MappingNode" or on_value.flow_style:
        raise Refused(R_ON_NOT_BLOCK)
    push = _mapping_get(on_value, "push")
    if push is None:
        raise Refused(R_NO_PUSH)
    push_key, push_value = push
    kind = push_value.__class__.__name__
    if kind in ("MappingNode", "SequenceNode") and push_value.flow_style:
        raise Refused(R_PUSH_FLOW)
    if kind != "MappingNode" and not _is_null(push_value):
        raise Refused(R_NO_PUSH)  # a scalar or block-sequence value is no push trigger
    lines = _split_keepends(text)
    if kind == "MappingNode":
        if _mapping_get(push_value, "paths") is not None:
            raise Refused(R_PUSH_PATHS)
        ignore = _mapping_get(push_value, "paths-ignore")
        if ignore is not None:
            ignore_key, seq = ignore
            if seq.__class__.__name__ != "SequenceNode" or seq.flow_style:
                raise Refused(R_IGNORE_NOT_SEQ)
            if any(_scalar_key(item, ENTRY) for item in seq.value):
                raise Refused(R_ALREADY)
            if not seq.value:  # composed as a block sequence only when it has items
                raise Refused(R_IGNORE_NOT_SEQ)
            column = seq.start_mark.column
            index = _end_index(lines, seq.value[-1])
            return index, [" " * column + ITEM_TEXT]
        child_col = push_value.value[0][0].start_mark.column
        step = child_col - push_key.start_mark.column
        index = _first_content_line_before(lines, _end_index(lines, push_value))
    else:
        step = push_key.start_mark.column - on_key.start_mark.column
        child_col = push_key.start_mark.column + step
        index = push_key.start_mark.line + 1
    if step <= 0:
        raise Refused(R_POST_EDIT)
    return index, [" " * child_col + "paths-ignore:", " " * (child_col + step) + ITEM_TEXT]


def apply_edit(text, index, bodies):
    """The edited text: `bodies` inserted before line `index`, endings preserved."""
    lines = _split_keepends(text)
    if index > 0:
        ref = lines[index - 1]
    elif lines:
        ref = lines[0]
    else:
        ref = "\n"
    ending = ref[len(ref.rstrip("\r\n")):] or ("\r\n" if "\r\n" in text else "\n")
    if index == len(lines) and lines and not lines[-1].endswith(("\r", "\n")):
        lines[-1] += ending  # the last line gains an ending so the insertion follows it
    return "".join(lines[:index] + [b + ending for b in bodies] + lines[index:])


def expected_after(yaml, text):
    """`safe_load` of the original with `cairn/**` appended under on → push → paths-ignore."""
    doc = yaml.safe_load(text)
    key = True if True in doc else "on"
    push = doc[key].get("push")
    if push is None:
        push = doc[key]["push"] = {}
    push.setdefault("paths-ignore", []).append(ENTRY)
    return doc


def apply_file(yaml, path, dry_run):
    """The verdict line for one workflow file, writing it when edited."""
    name = os.path.basename(path)
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return f"{name}: refused: {R_PARSE}"
    try:
        index, bodies = plan_edit(yaml, text)
        edited = apply_edit(text, index, bodies)
        try:
            if yaml.safe_load(edited) != expected_after(yaml, text):
                raise Refused(R_POST_EDIT)
        except yaml.YAMLError:
            raise Refused(R_POST_EDIT)
    except Refused as exc:
        return f"{name}: refused: {exc.args[0]}"
    if dry_run:
        return f"{name}: would apply"
    with open(path, "wb") as fh:
        fh.write(edited.encode("utf-8"))
    return f"{name}: applied"


def apply_files(files, dry_run):
    try:
        import yaml
    except ImportError:
        sys.stderr.write(
            "--apply needs PyYAML (`import yaml` failed); install PyYAML, "
            "or add the item by hand as --report shows\n"
        )
        return NO_PYYAML
    for path in files:
        print(apply_file(yaml, path, dry_run))
    return 0

# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def usage(code=2):
    sys.stderr.write("usage: cairn_ci_paths.py [ROOT] (--report | --apply [--dry-run])\n")
    return code


def main(argv):
    args = argv[1:]
    modes = [a for a in args if a in ("--report", "--apply")]
    dry_run = "--dry-run" in args
    rest = [a for a in args if a not in ("--report", "--apply", "--dry-run")]
    if len(modes) != 1 or len(rest) > 1 or any(a.startswith("-") for a in rest):
        return usage()
    if dry_run and modes[0] != "--apply":
        return usage()
    start = rest[0] if rest else os.getcwd()
    root = find_git_root(start)
    if root is None:
        sys.stderr.write(f"not a git repository: no .git at or above {start}\n")
        return 2
    wf, files = workflow_files(root)
    if not files:
        print(f"no workflow files under {wf}")
        return 0
    if modes[0] == "--apply":
        return apply_files(files, dry_run)
    for path in files:
        print(Workflow(path).report_line())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
