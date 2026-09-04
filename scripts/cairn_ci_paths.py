#!/usr/bin/env python3
"""cairn ci-paths — report or apply a `cairn/**` `paths-ignore` on push triggers.

Every push of a milestone or hotfix branch starts the repo's push-triggered
workflows, cairn's tracking-only commits included. A `paths-ignore` of
`cairn/**` under a workflow's `push` trigger skips those runs; a
`pull_request` trigger's filter reads the whole PR diff, so the ignore is
never applied there.

    python3 scripts/cairn_ci_paths.py [ROOT] --report
    python3 scripts/cairn_ci_paths.py [ROOT] --apply

ROOT defaults to the working directory; either is walked up to the enclosing
git repository root (a `.git` entry), where `.github/workflows/` is read.
Exits 0 on success, 2 outside a git repository or on a usage error.

`--report` prints one line per `*.yml` / `*.yaml` file directly under
`.github/workflows/`: the file's verdict, then `applicable` or `would
refuse: <reason>` from the same shape check `--apply` runs. `--apply` edits
each applicable file and names each refusal, leaving refused files
byte-identical. Three `on:` shapes are recognized — an unquoted scalar
(`on: push`), an unquoted flow list (`on: [push, pull_request]`), and an
unquoted block map whose `push:` key holds a block mapping or nothing;
everything else is refused with the reason. A comment on the `on:` line or
inside its block is a refusal, but the file is still placed for the report
(comment text stripped), as is a `push:`/`pull_request:` flow-mapping value,
whose filter keys the report reads.
"""

import os
import re
import sys

ENTRY = "cairn/**"
ITEM = "- 'cairn/**'"
TRIGGERS = ("push", "pull_request")
FILTER_KEYS = ("branches", "branches-ignore", "paths", "paths-ignore")

_ON_KEY = re.compile(r"""^(?P<key>on|"on"|'on')\s*:(?P<rest>.*)$""")
_WORD = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
_MAP_KEY = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_-]*)\s*:(?P<rest>.*)$")
_SEQ_ITEM = re.compile(r"^(?P<indent>\s*)-\s+(?P<value>.*)$")
_COMMENT = re.compile(r"(^|\s)#.*$")


class Refuse(Exception):
    """A file `--apply` will not edit; str(self) is the reason."""


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
# Parsing — a line-based reader for exactly three `on:` shapes
# --------------------------------------------------------------------------

def split_lines(data):
    """Decode bytes; return (lines without endings, eol, trailing_newline)."""
    text = data.decode("utf-8")
    if "\r\n" in text:
        if text.replace("\r\n", "").count("\n") or "\r" in text.replace("\r\n", ""):
            raise Refuse("mixed line endings")
        eol = "\r\n"
    else:
        eol = "\n"
    body = text
    trailing = body.endswith(eol)
    if trailing:
        body = body[: -len(eol)]
    lines = body.split(eol) if body else []
    return lines, eol, trailing


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _is_blank(line):
    return line.strip() == ""


def _strip_comment(line):
    """(line without its YAML comment, whether one was there)."""
    m = _COMMENT.search(line)
    if not m:
        return line, False
    return line[: m.start()].rstrip(), True


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


class Workflow:
    """One parsed workflow file.

    Attributes: shape ("scalar" | "flow" | "block" | None), triggers (list of
    trigger names named by `on:`, in order), filters (trigger -> dict of
    FILTER_KEYS presence plus "cairn" for a `cairn/**` entry), on_index,
    on_end (exclusive line index where the `on:` block ends), and the refusal
    reason (None when applicable). `verdict` renders the report text.
    """

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.shape = None
        self.triggers = []
        self.filters = {}
        self.refusal = None
        self.lines = []
        self.eol = "\n"
        self.trailing = True
        self.on_index = None
        self.on_end = None
        self.quoted_key = False
        self.block = None  # per-trigger line ranges for the block shape
        self.deferred = None  # a refusal `--apply` keeps while the file is still placed
        try:
            with open(path, "rb") as fh:
                self.lines, self.eol, self.trailing = split_lines(fh.read())
            self._parse()
        except Refuse as exc:
            self.refusal = str(exc)
        except UnicodeDecodeError:
            self.shape = None
            self.refusal = "unrecognized: not UTF-8"
        if self.refusal is None:
            self.refusal = self._shape_check()

    # -- locating `on:` ----------------------------------------------------

    def _parse(self):
        hits = [i for i, l in enumerate(self.lines) if _ON_KEY.match(l)]
        if len(hits) != 1:
            raise Refuse("unrecognized: no single top-level `on:` key")
        i = hits[0]
        self.on_index = i
        m = _ON_KEY.match(self.lines[i])
        self.quoted_key = m.group("key") != "on"
        rest, commented = _strip_comment(m.group("rest"))
        if commented:
            self.deferred = "a comment on the `on:` line"
        rest = rest.strip()
        # the block extends to the next non-blank column-0 line
        j = i + 1
        while j < len(self.lines) and (_is_blank(self.lines[j]) or _indent(self.lines[j]) > 0):
            j += 1
        self.on_end = j
        if rest == "":
            self._parse_block(i + 1, j)
        elif rest.startswith("["):
            self._parse_flow(rest, i + 1, j)
        else:
            self._parse_scalar(rest, i + 1, j)

    def _parse_scalar(self, rest, start, end):
        if any(not _is_blank(l) for l in self.lines[start:end]):
            raise Refuse("unrecognized: content indented under a scalar `on:`")
        if not _WORD.match(rest):
            raise Refuse("unrecognized: `on:` scalar is not a plain word")
        self.shape = "scalar"
        self.triggers = [rest]
        self.filters = {rest: self._no_filters()} if rest in TRIGGERS else {}

    def _parse_flow(self, rest, start, end):
        if any(not _is_blank(l) for l in self.lines[start:end]):
            raise Refuse("unrecognized: content indented under a flow-list `on:`")
        if not rest.endswith("]"):
            raise Refuse("unrecognized: flow list does not close on the `on:` line")
        inner = rest[1:-1].strip()
        if not inner:
            raise Refuse("unrecognized: empty flow list")
        items = [x.strip() for x in inner.split(",")]
        if any(not _WORD.match(x) for x in items):
            raise Refuse("unrecognized: flow-list item is not a plain word")
        if len(set(items)) != len(items):
            raise Refuse("unrecognized: duplicate trigger in flow list")
        self.shape = "flow"
        self.triggers = items
        self.filters = {t: self._no_filters() for t in items if t in TRIGGERS}

    def _parse_block(self, start, end):
        body = []
        for k in range(start, end):
            l, commented = _strip_comment(self.lines[k])
            if commented:
                self.deferred = self.deferred or "a comment inside the `on:` block"
            if not _is_blank(l):
                body.append((k, l))
        if not body:
            raise Refuse("unrecognized: `on:` holds nothing")
        for _, l in body:
            if "\t" in l[: _indent(l) + 1]:
                raise Refuse("unrecognized: tab indentation in the `on:` block")
        key_indent = _indent(body[0][1])
        self.shape = "block"
        self.block = {}
        order = []
        idx = 0
        while idx < len(body):
            k, l = body[idx]
            if _indent(l) != key_indent:
                raise Refuse("unrecognized: inconsistent indentation in the `on:` block")
            m = _MAP_KEY.match(l)
            if not m:
                raise Refuse("unrecognized: `on:` block entry is not a mapping key")
            trig = m.group("key")
            rest = m.group("rest").strip()
            # the trigger's value: following body lines indented deeper
            j = idx + 1
            while j < len(body) and _indent(body[j][1]) > key_indent:
                j += 1
            value_lines = body[idx + 1: j]
            if trig in order:
                raise Refuse("unrecognized: duplicate trigger in the `on:` block")
            order.append(trig)
            line_end = body[j][0] if j < len(body) else end
            self.block[trig] = {
                "line": k, "rest": rest, "end": line_end,
                "value": value_lines, "indent": key_indent,
            }
            idx = j
        self.triggers = order
        for trig in order:
            if trig in TRIGGERS:
                self.filters[trig] = self._block_filters(self.block[trig])

    def _block_filters(self, entry):
        present = self._no_filters()
        if entry["rest"].startswith("{"):
            for key, value in _flow_map_keys(entry["rest"]):
                if key in FILTER_KEYS:
                    present[key] = True
                    if key == "paths-ignore" and ENTRY in [
                        _strip_quotes(x) for x in value.strip("[]").split(",")
                    ]:
                        present["cairn"] = True
            return present
        if entry["rest"] != "" or not entry["value"]:
            return present  # scalar or flow-sequence value, or a bare key: nothing readable here
        child_indent = _indent(entry["value"][0][1])
        for k, l in entry["value"]:
            if _indent(l) != child_indent:
                continue
            m = _MAP_KEY.match(l)
            if m and m.group("key") in FILTER_KEYS:
                present[m.group("key")] = True
                if m.group("key") == "paths-ignore" and self._has_entry(entry, k, m):
                    present["cairn"] = True
        return present

    def _has_entry(self, entry, key_line, m):
        rest = m.group("rest").strip()
        if rest.startswith("["):
            return ENTRY in [_strip_quotes(x) for x in rest.strip("[]").split(",")]
        # items may sit deeper than the key or at its own indent (a legal,
        # common style); the sequence ends at the first line that is neither
        for k, l in entry["value"]:
            if k <= key_line:
                continue
            s = _SEQ_ITEM.match(l)
            if not s or _indent(l) < _indent(self.lines[key_line]):
                break
            if _strip_quotes(s.group("value")) == ENTRY:
                return True
        return False

    @staticmethod
    def _no_filters():
        return {k: False for k in FILTER_KEYS + ("cairn",)}

    # -- the shape check `--apply` uses ----------------------------------

    def _shape_check(self):
        if self.quoted_key:
            return "a quoted `on:` key"
        if self.deferred is not None:
            return self.deferred
        if "push" not in self.triggers:
            return "no `push` trigger"
        if self.shape != "block":
            return None
        entry = self.block["push"]
        if entry["rest"] != "":
            if entry["rest"].startswith("{"):
                return "`push:` holds a flow mapping"
            if entry["rest"].startswith("["):
                return "`push:` holds a flow sequence"
            return "`push:` holds a scalar value"
        if not entry["value"]:
            return None
        child_indent = _indent(entry["value"][0][1])
        seen_key = False
        for k, l in entry["value"]:
            if _indent(l) != child_indent:
                continue
            m = _MAP_KEY.match(l)
            if not m:
                if seen_key and _SEQ_ITEM.match(l):
                    continue  # an item of the preceding key, at the key's own indent
                return "unrecognized: `push:` child is not a mapping key"
            seen_key = True
            key, rest = m.group("key"), m.group("rest").strip()
            if key == "paths":
                return "`push:` already carries `paths`"
            if key == "paths-ignore":
                if rest.startswith("["):
                    return "`paths-ignore` is a flow list"
                if rest != "":
                    return "`paths-ignore` holds a scalar value"
                if self.filters["push"]["cairn"]:
                    return "`push:` already ignores `cairn/**`"
                if not self._seq_items(entry, k):
                    return "`paths-ignore` holds no block-sequence item"
        return None

    def _seq_items(self, entry, key_line):
        """(line index, indent) of each block-sequence item under the key at key_line."""
        key_indent = _indent(self.lines[key_line])
        items = []
        for k, l in entry["value"]:
            if k <= key_line:
                continue
            s = _SEQ_ITEM.match(l)
            if not s or _indent(l) < key_indent:
                break
            items.append((k, _indent(l)))
        return items

    # -- reporting ---------------------------------------------------------

    def verdict(self):
        if self.shape is None:
            return "unrecognized"
        named = [t for t in self.triggers if t in TRIGGERS]
        if not named:
            return "no push or pull_request trigger"
        parts = []
        for t in named:
            f = self.filters[t]
            present = [k for k in FILTER_KEYS if f[k]]
            if f["cairn"]:
                present.append(ENTRY)
            parts.append(f"{t} ({', '.join(present) if present else 'no filters'})")
        return ", ".join(parts)

    def report_line(self):
        status = "applicable" if self.refusal is None else f"would refuse: {self.refusal}"
        return f"{self.name}: {self.verdict()} — {status}"

    # -- applying ----------------------------------------------------------

    def step(self):
        """The file's indent step, read from its first indented line (else 2)."""
        for l in self.lines:
            if not _is_blank(l) and _indent(l) > 0:
                return _indent(l)
        return 2

    def applied_lines(self):
        """The edited line list; raises Refuse when the shape check refuses."""
        if self.refusal is not None:
            raise Refuse(self.refusal)
        lines = list(self.lines)
        step = self.step()
        if self.shape in ("scalar", "flow"):
            block = ["on:"]
            for t in self.triggers:
                block.append(" " * step + f"{t}:")
                if t == "push":
                    block.append(" " * (2 * step) + "paths-ignore:")
                    block.append(" " * (3 * step) + ITEM)
            lines[self.on_index: self.on_index + 1] = block
            return lines
        entry = self.block["push"]
        key_indent = entry["indent"]
        if not entry["value"]:
            child = key_indent + step
            insert = [" " * child + "paths-ignore:", " " * (child + step) + ITEM]
            lines[entry["line"] + 1: entry["line"] + 1] = insert
            return lines
        child = _indent(entry["value"][0][1])
        for k, l in entry["value"]:
            m = _MAP_KEY.match(l)
            if _indent(l) == child and m and m.group("key") == "paths-ignore":
                items = self._seq_items(entry, k)
                last_line, item_indent = items[-1]
                lines[last_line + 1: last_line + 1] = [" " * item_indent + ITEM]
                return lines
        # no paths-ignore yet: append it after push's last value line
        last = entry["value"][-1][0]
        item_indent = child + step
        lines[last + 1: last + 1] = [" " * child + "paths-ignore:", " " * item_indent + ITEM]
        return lines

    def applied_bytes(self):
        lines = self.applied_lines()
        text = self.eol.join(lines) + (self.eol if self.trailing else "")
        return text.encode("utf-8")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def usage(code=2):
    sys.stderr.write("usage: cairn_ci_paths.py [ROOT] --report | --apply\n")
    return code


def main(argv):
    args = argv[1:]
    modes = [a for a in args if a in ("--report", "--apply")]
    rest = [a for a in args if a not in ("--report", "--apply")]
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
    mode = modes[0]
    for path in files:
        w = Workflow(path)
        if mode == "--report":
            print(w.report_line())
            continue
        if w.refusal is not None:
            print(f"refused: {w.name} — {w.refusal}")
            continue
        data = w.applied_bytes()
        with open(path, "wb") as fh:
            fh.write(data)
        print(f"applied: {w.name} — added {ITEM} under push → paths-ignore")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
