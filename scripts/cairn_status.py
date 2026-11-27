#!/usr/bin/env python3
"""cairn status: the local listing for one repo, and plan lookup.

    python3 cairn_status.py [-C DIR]                 the listing
    python3 cairn_status.py [-C DIR] plan            the current branch's plan
    python3 cairn_status.py [-C DIR] plan SLUG       a plan by any unique start of its slug
    python3 cairn_status.py [-C DIR] plan '#N'       a plan by its issue or PR number

The listing shows the home folder, the work in flight with its phase and
what blocks it, the `[high]` and `[blocked]` candidate rows, the candidate
count, any file that could not be read, and the path of the current
branch's plan. `plan` prints one plan's path and exits 0, or says why it
cannot and exits 1.

This is the only parser of cairn's files. It reads what the listing needs
and nothing else: a plan's labeled lines, ROADMAP rows and their marks, and
a guest profile's `Maintainer:` line. It makes no network call and writes
nothing. Python 3 standard library only.

The home folder is `~/.cairn/<owner>/<repo>/`, named from the repo's base
remote: `origin` where the checkout holds `cairn/ROADMAP.md` (the user's
own repo), else `upstream` where that remote exists, else `origin`. The
`CAIRN_HOME` environment variable replaces `~/.cairn`, for tests.
"""

import os
import re
import subprocess
import sys

MARKS = ("high", "blocked")
LABELS = ("Route", "Branch", "Issue", "Phase", "Blocked on")
ROUTES = ("trail", "road")

_LABEL_LINE = re.compile(r"^(%s):[ \t]*(.*)$" % "|".join(LABELS))
_MARK = re.compile(r"^\[([^\]]*)\]\s*")
_NUMBER = re.compile(r"#(\d+)")
_WAITS = re.compile(r"\bwaits for\b\s*(.*)", re.IGNORECASE | re.DOTALL)
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_NONE_WORDS = ("", "none", "-", "—")

V2_NOTICE = (
    "This repo has cairn v2 files (`cairn/DECISIONS.md` or "
    "`cairn/milestones/`). cairn v3 does not read them. "
    "`/cairn setup` converts the repo."
)


def home_root():
    return os.environ.get("CAIRN_HOME") or os.path.join(
        os.path.expanduser("~"), ".cairn"
    )


def git(args, cwd):
    """Run git and return (returncode, stdout). Never raises."""
    try:
        done = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10
        )
        return done.returncode, done.stdout.strip()
    except Exception:
        return 1, ""


def remote_slug(url):
    """(owner, repo) from a remote URL, or None."""
    url = (url or "").strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    parts = [p for p in re.split(r"[/:]", url) if p]
    if len(parts) < 2:
        return None
    owner, repo = parts[-2], parts[-1]
    if not (_SAFE_NAME.match(owner) and _SAFE_NAME.match(repo)):
        return None
    return owner, repo


class Repo:
    """What the listing needs to know about one checkout.

    kind is "own", "guest", "v2", or None (not a cairn repo).
    """

    def __init__(self, top):
        self.top = top
        self.kind = None
        self.slug = None
        self.home = None
        self.branch = None
        self.roadmap = None
        self.profile = None
        self.problems = []


def resolve(cwd):
    """The Repo for cwd, or None outside a git checkout."""
    rc, top = git(["rev-parse", "--show-toplevel"], cwd)
    if rc != 0 or not top:
        return None
    repo = Repo(top)
    _, repo.branch = git(["branch", "--show-current"], top)
    own_roadmap = os.path.join(top, "cairn", "ROADMAP.md")
    own = os.path.isfile(own_roadmap)

    if os.path.isfile(os.path.join(top, "cairn", "DECISIONS.md")) or os.path.isdir(
        os.path.join(top, "cairn", "milestones")
    ):
        repo.kind = "v2"
        return repo

    remote = "origin"
    if not own:
        rc, names = git(["remote"], top)
        if rc == 0 and "upstream" in names.split():
            remote = "upstream"
    rc, url = git(["remote", "get-url", remote], top)
    pair = remote_slug(url) if rc == 0 else None
    if pair:
        repo.slug = "%s/%s" % pair
        repo.home = os.path.join(home_root(), pair[0], pair[1])

    if own:
        repo.kind = "own"
        repo.roadmap = own_roadmap
        repo.profile = os.path.join(top, "cairn", "PROFILE.md")
        if not repo.home:
            repo.problems.append(
                "no `%s` remote that names an owner and a repo, so the home "
                "folder cannot be found and plans are not listed" % remote
            )
    elif repo.home and os.path.isfile(os.path.join(repo.home, "ROADMAP.md")):
        repo.kind = "guest"
        repo.roadmap = os.path.join(repo.home, "ROADMAP.md")
        repo.profile = os.path.join(repo.home, "PROFILE.md")
    return repo


def _read(path):
    with open(path, encoding="utf-8-sig") as handle:
        return handle.read()


def _value(text):
    text = text.strip()
    return None if text.lower() in _NONE_WORDS else text


def read_plan(path):
    """One plan's labeled lines, read from the top of the file down to its
    first `## ` heading. Returns (plan, problems)."""
    slug = os.path.splitext(os.path.basename(path))[0]
    plan = {"slug": slug, "path": path}
    name = "plans/%s.md" % slug
    try:
        text = _read(path)
    except Exception as err:
        return plan, ["%s: cannot be read (%s)" % (name, type(err).__name__)]
    for line in text.splitlines():
        if line.startswith("## "):
            break
        found = _LABEL_LINE.match(line)
        if found and found.group(1) not in plan:
            plan[found.group(1)] = _value(found.group(2))

    problems = []
    for label in ("Route", "Branch", "Phase"):
        if not plan.get(label):
            problems.append("%s: no `%s:` line with a value" % (name, label))
    route = plan.get("Route")
    if route and route.lower() not in ROUTES:
        problems.append(
            "%s: `Route:` is `%s`, not trail or road" % (name, route)
        )
    issue = plan.get("Issue")
    if issue:
        number = _NUMBER.search(issue) or re.fullmatch(r"(\d+)", issue)
        if number:
            plan["issue_number"] = number.group(1)
        else:
            problems.append("%s: `Issue:` is `%s`, not `#N`" % (name, issue))
    return plan, problems


def read_plans(home):
    """Every plan under <home>/plans, by slug. Returns (plans, problems)."""
    folder = os.path.join(home, "plans")
    plans, problems = [], []
    try:
        names = sorted(os.listdir(folder))
    except FileNotFoundError:
        return plans, problems
    except Exception as err:
        return plans, ["plans/: cannot be read (%s)" % type(err).__name__]
    for name in names:
        if not name.endswith(".md") or name.startswith("."):
            continue
        plan, found = read_plan(os.path.join(folder, name))
        plans.append(plan)
        problems.extend(found)
    return plans, problems


def read_roadmap(path):
    """Candidate rows: the file's top-level list items. Returns (rows,
    problems). A row is {"title", "marks", "waits"}."""
    try:
        text = _read(path)
    except Exception as err:
        return [], ["ROADMAP.md: cannot be read (%s)" % type(err).__name__]
    items = []
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("- "):
            items.append([number, line[2:].strip()])
        elif items and items[-1] and line[:1] in (" ", "\t") and line.strip():
            items[-1][1] += " " + line.strip()
        elif line.strip():
            items.append(None)  # any other text ends the row above it
    rows, problems = [], []
    for item in items:
        if item is None:
            continue
        number, body = item
        marks = []
        while True:
            found = _MARK.match(body)
            if not found:
                break
            mark = found.group(1).strip().lower()
            if mark in MARKS:
                marks.append(mark)
            else:
                problems.append(
                    "ROADMAP.md line %d: `[%s]` is not a mark (the marks are "
                    "`[high]` and `[blocked]`)" % (number, found.group(1))
                )
            body = body[found.end():]
        title, colon, rest = body.partition(": ")
        if not colon and body.endswith(":"):
            title, colon = body[:-1], ":"
        if not colon or not title.strip():
            problems.append(
                "ROADMAP.md line %d: the row has no title before a colon"
                % number
            )
            title, rest = body, ""
        waits = None
        if "blocked" in marks:
            found = _WAITS.search(rest)
            if found and found.group(1).strip():
                waits = found.group(1).strip().rstrip(".")
        rows.append({"title": title.strip(), "marks": marks, "waits": waits})
    return rows, problems


def read_maintainer(path):
    """True where a guest profile says `Maintainer: yes`. Returns (flag,
    problems)."""
    try:
        text = _read(path)
    except Exception as err:
        return False, ["PROFILE.md: cannot be read (%s)" % type(err).__name__]
    for line in text.splitlines():
        if line.startswith("## "):
            break
        found = re.match(r"^Maintainer:[ \t]*(.*)$", line)
        if found:
            return found.group(1).strip().lower() == "yes", []
    return False, []


def plans_for_branch(plans, branch):
    return [p for p in plans if branch and p.get("Branch") == branch]


def plans_for_number(plans, number):
    """Plans whose `Issue:` is #number or whose `Phase:` names #number (the
    PR, once it is open)."""
    hits = []
    for plan in plans:
        phase = _NUMBER.findall(plan.get("Phase") or "")
        if plan.get("issue_number") == number or number in phase:
            hits.append(plan)
    return hits


def plans_for_slug(plans, start):
    exact = [p for p in plans if p["slug"] == start]
    return exact or [p for p in plans if p["slug"].startswith(start)]


def find_plan(repo, arg):
    """(path, None) for the one plan that arg names, else (None, reason).
    No arg means the current branch."""
    if repo is None or repo.kind not in ("own", "guest"):
        return None, "not a cairn v3 repo"
    if not repo.home:
        return None, "the home folder cannot be found"
    plans, _ = read_plans(repo.home)
    if not arg:
        hits = plans_for_branch(plans, repo.branch)
        what = "branch `%s`" % (repo.branch or "(detached)")
    elif re.fullmatch(r"#?\d+", arg):
        hits = plans_for_number(plans, arg.lstrip("#"))
        what = "#%s" % arg.lstrip("#")
    else:
        hits = plans_for_slug(plans, arg)
        what = "`%s`" % arg
    if len(hits) == 1:
        return hits[0]["path"], None
    if not hits:
        return None, "no plan for %s in %s" % (
            what, os.path.join(repo.home, "plans")
        )
    return None, "%d plans match %s: %s" % (
        len(hits), what, ", ".join(p["slug"] for p in hits)
    )


def _plan_line(plan):
    parts = [
        plan["slug"],
        (plan.get("Route") or "no route").lower(),
        plan.get("Phase") or "no phase",
        "branch %s" % (plan.get("Branch") or "none"),
    ]
    if plan.get("Issue"):
        parts.append("issue %s" % plan["Issue"])
    if plan.get("Blocked on"):
        parts.append("BLOCKED on: %s" % plan["Blocked on"])
    return "- " + " · ".join(parts)


def render(repo):
    """The listing as text, or None where cwd is not a cairn repo."""
    if repo is None or repo.kind is None:
        return None
    if repo.kind == "v2":
        return V2_NOTICE

    problems = list(repo.problems)
    kind = "own repo"
    if repo.kind == "guest":
        maintainer, found = read_maintainer(repo.profile)
        problems.extend(found)
        kind = "guest repo, `Maintainer: yes`" if maintainer else "guest repo"
    lines = [
        "cairn: %s (%s)" % (repo.slug or os.path.basename(repo.top), kind),
        "Home folder: %s" % (repo.home or "not found"),
        "",
    ]

    plans = []
    if repo.home:
        plans, found = read_plans(repo.home)
        problems.extend(found)
    if plans:
        lines.append("Work in flight (%d):" % len(plans))
        lines.extend(_plan_line(p) for p in plans)
    else:
        lines.append("Work in flight: none")
    lines.append("")

    rows, found = read_roadmap(repo.roadmap)
    problems.extend(found)
    high = [r for r in rows if "high" in r["marks"]]
    blocked = [r for r in rows if "blocked" in r["marks"]]
    if high:
        lines.append("`[high]` candidates (%d):" % len(high))
        lines.extend("- %s" % r["title"] for r in high)
        lines.append("")
    if blocked:
        lines.append("`[blocked]` candidates (%d):" % len(blocked))
        for row in blocked:
            waits = ": waits for %s" % row["waits"] if row["waits"] else ""
            lines.append("- %s%s" % (row["title"], waits))
        lines.append("")
    lines.append(
        "Candidates: %d (%d high, %d blocked)"
        % (len(rows), len(high), len(blocked))
    )

    if problems:
        lines.append("")
        lines.append("Problems (%d):" % len(problems))
        lines.extend("- %s" % p for p in problems)

    lines.append("")
    branch = repo.branch or "(detached)"
    hits = plans_for_branch(plans, repo.branch)
    if len(hits) == 1:
        lines.append("Plan for this branch (%s): %s" % (branch, hits[0]["path"]))
    elif hits:
        lines.append(
            "Plan for this branch (%s): %d plans name it: %s"
            % (branch, len(hits), ", ".join(p["slug"] for p in hits))
        )
    else:
        lines.append("Plan for this branch (%s): none" % branch)
    return "\n".join(lines)


def main(argv):
    args = list(argv[1:])
    cwd = os.getcwd()
    if args[:1] == ["-C"]:
        if len(args) < 2:
            print("usage: cairn_status.py [-C DIR] [plan [SLUG | #N]]")
            return 2
        cwd, args = args[1], args[2:]
    repo = resolve(cwd)
    if args[:1] == ["plan"] and len(args) <= 2:
        path, reason = find_plan(repo, args[1] if len(args) == 2 else None)
        print(path or reason)
        return 0 if path else 1
    if args:
        print("usage: cairn_status.py [-C DIR] [plan [SLUG | #N]]")
        return 2
    text = render(repo)
    if text is None:
        print("Not a cairn repo: no `cairn/ROADMAP.md` here and no home folder for it.")
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
