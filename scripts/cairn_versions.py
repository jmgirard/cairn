#!/usr/bin/env python3
"""cairn versions — read a version marker's history on the default branch.

A Quarto extension keeps its version in `version:` in
`_extensions/<name>/_extension.yml`. The quarto-extension profile's release
walk (M303) and the merge-time handoff (M304) read that line through this
script.

    python3 scripts/cairn_versions.py FILE [--root DIR] [--at REV]
    python3 scripts/cairn_versions.py FILE [--root DIR] --changed-by SHA

FILE is the marker file's path relative to the repository root. ROOT is the
repository (default: the working directory). History is the first-parent
chain from REV (default `HEAD`), so a squash merge or a merge commit on the
default branch is where a version enters it.

The default mode prints three lines for REV:

    version <the version at REV>
    start <the first commit of that version's unbroken run back from REV>
    tag <present|absent>   (a `v<version>` tag, annotated or lightweight)

`--changed-by SHA` prints the version SHA set, compared with its first
parent, and prints nothing when the version did not change. A commit where
the file or its `version:` line is absent has no version: it ends a run, and
a commit that adds the line after it sets that version. The value may be
quoted; an unquoted value ends at the first space or `#`, and a leading
byte-order mark is ignored. The release walk passes the version to
`git tag`, so a printed version is dot-separated parts of letters, digits,
and `+_-`, each part starting and ending with a letter or digit, the first
starting with a digit, and not ending in `.lock`; any other value is an
error (exit 2, naming it). In the default mode a missing
file or `version:` line at REV is an error (exit 2, naming FILE). So are a
ROOT that is not a git repository or is a shallow clone (exit 2, naming
it), a revision git cannot resolve (exit 2, naming it), and a usage error
(exit 2, for example `--at` with `--changed-by`). Stdlib only.
"""

import re
import subprocess
import sys

VERSION_LINE = re.compile(r"^version:[ \t]*(?:\"([^\"]*)\"|'([^']*)'|([^\s#]+))", re.M)
# A version the release walk may pass to `git tag`: dot-separated parts of
# letters, digits, and `+_-`, each part starting and ending with a letter or
# digit, the first starting with a digit (so `v1.0` cannot become `vv1.0`),
# and no `.lock` ending, which git refuses in a ref name.
PART = r"[0-9A-Za-z](?:[0-9A-Za-z+_-]*[0-9A-Za-z])?"
PLAIN_VERSION = re.compile(rf"^[0-9](?:[0-9A-Za-z+_-]*[0-9A-Za-z])?(?:\.{PART})*$")


class GitError(Exception):
    pass


def git(root, *args):
    proc = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise GitError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def check_root(root):
    try:
        shallow = git(root, "rev-parse", "--is-shallow-repository").strip()
    except (GitError, OSError):
        raise GitError(f"not a git repository: {root}") from None
    if shallow == "true":
        raise GitError(f"{root} is a shallow clone, so its history is cut short; run `git fetch --unshallow` first")


def plain(version, path):
    """The version, refused unless it is safe to pass to `git tag`."""
    if version is not None and (not PLAIN_VERSION.match(version) or version.endswith(".lock")):
        raise GitError(f"the version: value in {path} is not a plain version: {version!r}")
    return version


def resolve(root, rev):
    try:
        return git(root, "rev-parse", "--verify", "-q", f"{rev}^{{commit}}").strip()
    except GitError:
        raise GitError(f"unknown revision: {rev}") from None


def parse_version(text):
    """The top-level `version:` value in a YAML text, or None."""
    m = VERSION_LINE.search(text.lstrip("﻿"))
    if m is None:
        return None
    value = next(g for g in m.groups() if g is not None).strip()
    return value or None


def versions_at(root, path, commits):
    """The marker's version at each commit, read in one `git cat-file --batch`
    call. A commit whose tree lacks the file maps to None."""
    if not commits:
        return {}
    request = "".join(f"{c}:{path}\n" for c in commits)
    proc = subprocess.run(
        ["git", "-C", root, "cat-file", "--batch"],
        input=request.encode(),
        capture_output=True,
    )
    if proc.returncode != 0:
        raise GitError(proc.stderr.decode(errors="replace").strip())
    out, pos, found = proc.stdout, 0, {}
    for c in commits:
        end = out.index(b"\n", pos)
        header = out[pos:end].decode(errors="replace")
        pos = end + 1
        if header.endswith(" missing"):
            found[c] = None
            continue
        size = int(header.rsplit(" ", 1)[1])
        body = out[pos:pos + size].decode(errors="replace")
        pos += size + 1
        found[c] = parse_version(body)
    return found


def first_parent_chain(root, rev):
    return git(root, "rev-list", "--first-parent", rev).split()


def tag_present(root, version):
    try:
        git(root, "rev-parse", "--verify", "-q", f"refs/tags/v{version}")
        return True
    except GitError:
        return False


def tip_report(root, path, rev):
    chain = first_parent_chain(root, rev)
    found = versions_at(root, path, chain)
    version = plain(found[chain[0]], path)
    if version is None:
        raise GitError(f"no version: line in {path} at {rev} (the file or the line is missing)")
    start = chain[0]
    for c in chain[1:]:
        if found[c] != version:
            break
        start = c
    present = "present" if tag_present(root, version) else "absent"
    return f"version {version}\nstart {start}\ntag {present}\n"


def changed_by(root, path, sha):
    parents = git(root, "rev-list", "--parents", "-n", "1", sha).split()[1:]
    commits = [sha] + parents[:1]
    found = versions_at(root, path, commits)
    after = plain(found[sha], path)
    before = found[parents[0]] if parents else None
    if after is not None and after != before:
        return f"{after}\n"
    return ""


USAGE = "usage: cairn_versions.py FILE [--root DIR] [--at REV | --changed-by SHA]"


def parse_args(argv):
    """FILE and the three options, or None on a usage error."""
    opts, files, args = {"--root": ".", "--at": None, "--changed-by": None}, [], list(argv)
    while args:
        arg = args.pop(0)
        if arg in opts:
            if not args:
                return None
            opts[arg] = args.pop(0)
        elif arg.startswith("-"):
            return None
        else:
            files.append(arg)
    if len(files) != 1 or (opts["--at"] is not None and opts["--changed-by"] is not None):
        return None
    return files[0], opts["--root"], opts["--at"] or "HEAD", opts["--changed-by"]


def main(argv=None):
    parsed = parse_args(sys.argv[1:] if argv is None else argv)
    if parsed is None:
        print(USAGE, file=sys.stderr)
        return 2
    path, root, at, sha = parsed
    try:
        check_root(root)
        if sha is not None:
            sys.stdout.write(changed_by(root, path, resolve(root, sha)))
        else:
            sys.stdout.write(tip_report(root, path, resolve(root, at)))
    except GitError as err:
        print(f"cairn_versions: {err}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
