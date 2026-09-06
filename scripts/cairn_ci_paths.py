#!/usr/bin/env python3
"""cairn ci-paths — report each workflow's push/pull_request triggers and filters.

Every push of a milestone or hotfix branch starts the repo's push-triggered
workflows, cairn's tracking-only commits included. A `paths-ignore` of
`cairn/**` under a workflow's `push` trigger skips those runs; a
`pull_request` trigger's filter reads the whole PR diff, so the ignore does
not help there. This script only reports; the operator edits by hand.

    python3 scripts/cairn_ci_paths.py [ROOT] --report

ROOT defaults to the working directory; either is walked up to the enclosing
git repository root (a `.git` entry), where `.github/workflows/` is read.
Exits 0 on success, 2 outside a git repository or on a usage error.
`--report` is the only mode.

One line per `*.yml` / `*.yaml` file directly under `.github/workflows/`,
carrying one of three verdicts: the triggers among `push` and `pull_request`
the file's `on:` names, each with the filter keys present under it
(`branches`, `branches-ignore`, `paths`, `paths-ignore`) and `cairn/**` when
its `paths-ignore` holds that entry; `no push or pull_request trigger`; or
`unrecognized`, for a file the reader cannot place or cannot read. The
reader is line-based and places an unquoted or quoted `on:` key holding a
plain scalar, a flow list, or a block map whose trigger values are block
mappings, flow mappings, flow sequences, scalars, or nothing; comments are
ignored. Nothing is written.
"""

import os
import re
import sys

ENTRY = "cairn/**"
TRIGGERS = ("push", "pull_request")
FILTER_KEYS = ("branches", "branches-ignore", "paths", "paths-ignore")
NO_TRIGGER = "no push or pull_request trigger"
UNRECOGNIZED = "unrecognized"

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
# CLI
# --------------------------------------------------------------------------

def usage(code=2):
    sys.stderr.write("usage: cairn_ci_paths.py [ROOT] --report\n")
    return code


def main(argv):
    args = argv[1:]
    modes = [a for a in args if a == "--report"]
    rest = [a for a in args if a != "--report"]
    if len(modes) != 1 or len(rest) > 1 or any(a.startswith("-") for a in rest):
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
    for path in files:
        print(Workflow(path).report_line())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
