#!/usr/bin/env python3
"""cairn migrate: convert one repo's cairn v2 files to v3.

    python3 cairn_migrate.py [-C DIR]            say what would change
    python3 cairn_migrate.py [-C DIR] --apply    change it

Run it in the repo's main checkout. Without `--apply` it changes nothing.

In the user's own repo (`cairn/` is tracked) it:
- moves `DECISIONS.md`, `LESSONS.md`, `milestones/`, and `reviews/` to
  `cairn/archive/`;
- rewrites `cairn/ROADMAP.md` as candidate rows and `cairn/PROFILE.md` as
  the three v3 sections;
- swaps the cairn section of `CLAUDE.md`;
- moves each plan in flight to the home folder, with its labeled lines
  written and its body left as it was;
- moves the shelf to the home folder.
It stages those changes and commits nothing.

In a guest repo (`cairn/` is untracked) it moves everything to the home
folder, leaves nothing of cairn in the checkout, and takes the `cairn/`
line out of `.git/info/exclude`. The v2 ROADMAP and PROFILE are kept in the
home folder's `archive/`.

It converts what a rule can convert. Whether a row should be `[blocked]`,
promoted, or dropped, and what a Known issues entry becomes, is left to the
session that runs `setup`. Python 3 standard library only.
"""

import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cairn_status as cs  # noqa: E402

IN_FLIGHT = ("planned", "in-progress", "review", "blocked")
ARCHIVED = ("DECISIONS.md", "LESSONS.md", "milestones", "reviews")
SECTION_HEADING = "## Project tracking (cairn)"
OLD_TAGS = re.compile(r"^\[(low|parked|normal)\]\s*", re.IGNORECASE)
EMPTY = ("", "—", "-", "none")


class Stop(Exception):
    """The migration cannot run as things stand."""


def template(name):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "skills", "cairn", "templates", name)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


# ---- conversions: text in, text out ------------------------------------


def table_rows(roadmap):
    """The v2 milestone table: one dict for each row."""
    rows = []
    for line in roadmap.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not re.fullmatch(r"M\d+", cells[0]):
            continue
        rows.append({
            "id": cells[0], "title": cells[1], "status": cells[2].lower(),
            "depends": cells[3], "path": cells[5],
        })
    return rows


def convert_roadmap(roadmap):
    """The v3 ROADMAP: the candidate rows, with the v2 tags that v3 has no
    use for taken off. Returns (text, number of rows, number of tags removed)."""
    rows, removed, inside = [], 0, False
    for line in roadmap.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower() == "candidates"
            continue
        if not inside:
            continue
        if line.startswith("- "):
            body = line[2:].strip()
            while True:
                stripped = OLD_TAGS.sub("", body)
                if stripped == body:
                    break
                body, removed = stripped, removed + 1
            rows.append("- " + body)
        elif rows and line[:1] in (" ", "\t") and line.strip() and not line.strip().startswith("<!--"):
            rows[-1] += " " + line.strip()
    text = "# Roadmap\n"
    if rows:
        text += "\n" + "\n".join(rows) + "\n"
    return text, len(rows), removed


def sections(text):
    """A file's `## ` sections: {lowercase heading: body}."""
    found, name = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            name = line[3:].strip().lower()
            found[name] = []
        elif name is not None:
            found[name].append(line)
    return {key: "\n".join(lines).strip("\n") for key, lines in found.items()}


def convert_profile(profile):
    """The v3 PROFILE from a v2 one: verify (with the review-time checks of
    the consistency gate after it), changelog, and release, each as written."""
    old = sections(profile)
    verify = "\n\n".join(part for part in (old.get("verify"), old.get("consistency-gate")) if part)
    parts = ["# Profile", ""]
    for heading, body in (
        ("Verify", verify),
        ("Changelog", old.get("changelog")),
        ("Release", old.get("release-walk")),
    ):
        parts.extend(["## " + heading, "", body or "none", ""])
    return "\n".join(parts)


def plan_slug(path):
    name = os.path.splitext(os.path.basename(path))[0]
    return re.sub(r"^m\d+-", "", name.lower())


def _bullet(text, label):
    found = re.search(r"^- \*\*%s:\*\*[ \t]*(.*)$" % re.escape(label), text, re.MULTILINE)
    value = found.group(1).strip() if found else ""
    return "" if value in EMPTY else value


def convert_plan(text, row, titles):
    """A v2 plan as a v3 plan: the labeled lines on top, the body as it was."""
    slug = plan_slug(row["path"])
    where = _bullet(text, "Branch/PR")
    branch = where.split()[0].strip("`,;") if where else ""
    if branch.lower().startswith(("http", "companion")):
        branch = ""
    pull = re.search(r"/pull/(\d+)", where)
    issue = re.search(r"#(\d+)", _bullet(text, "Resolves"))

    if pull:
        phase = "pr #" + pull.group(1)
    elif not branch:
        phase = "plan"  # no branch yet, so the work has not started
    else:
        phase = {"planned": "plan", "review": "review"}.get(row["status"], "build")
    blocked = ""
    if row["status"] == "blocked" and not pull:
        needs = [
            titles.get(found) or "%s, a v2 plan now in the archive" % found
            for found in re.findall(r"M\d+", row["depends"])
        ]
        blocked = "; ".join(needs) if needs else "not recorded, see the work log below"

    head = [
        "# " + slug, "",
        "Route: road",
        "Branch: " + branch,
        "Issue: " + ("#" + issue.group(1) if issue else ""),
        "Phase: " + phase,
        "Blocked on: " + blocked,
        "",
        "Converted from a cairn v2 plan. The text below is as it was written.",
        "",
    ]
    return slug, "\n".join(line.rstrip() for line in head) + "\n" + text


def swap_section(claude_md, section):
    """CLAUDE.md with its cairn section replaced. Returns (text, swapped)."""
    lines = claude_md.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == SECTION_HEADING)
    except StopIteration:
        return claude_md, False
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if re.match(r"^#{1,2} ", lines[index]):
            end = index
            break
    # The comment cairn-init left above the heading goes with the section.
    above = start
    while above > 0 and not lines[above - 1].strip():
        above -= 1
    if above > 0 and lines[above - 1].rstrip().endswith("-->"):
        top = above - 1
        while top > 0 and "<!--" not in lines[top]:
            top -= 1
        if "cairn" in "\n".join(lines[top:above]).lower():
            start = top
    kept = lines[:start] + section.rstrip("\n").splitlines()
    if end < len(lines):
        kept += [""] + lines[end:]
    return "\n".join(kept) + "\n", True


# ---- the plan of work: what to do, in order ----------------------------


class Migration:
    def __init__(self, top):
        self.top = top
        self.cairn = os.path.join(top, "cairn")
        self.steps = []   # (description, function)
        self.notes = []   # things for the session to look at

    def git(self, *args):
        code, out = cs.git(list(args), self.top)
        return code, out

    def check(self):
        roadmap = os.path.join(self.cairn, "ROADMAP.md")
        if not os.path.isfile(roadmap):
            raise Stop("No cairn/ROADMAP.md here, so there is nothing to migrate.")
        if not any(os.path.exists(os.path.join(self.cairn, name)) for name in ("DECISIONS.md", "milestones")):
            raise Stop("These are not cairn v2 files: no cairn/DECISIONS.md and no cairn/milestones/.")
        _, git_dir = self.git("rev-parse", "--absolute-git-dir")
        _, common = self.git("rev-parse", "--path-format=absolute", "--git-common-dir")
        if os.path.realpath(git_dir) != os.path.realpath(common):
            raise Stop("This is a linked worktree. Run the migration in the repo's main checkout.")
        code, _ = self.git("ls-files", "--error-unmatch", "cairn/ROADMAP.md")
        self.own = code == 0

        remote = "origin"
        if not self.own:
            _, names = self.git("remote")
            if "upstream" in names.split():
                remote = "upstream"
        code, url = self.git("remote", "get-url", remote)
        pair = cs.remote_slug(url) if code == 0 else None
        if not pair:
            raise Stop("No `%s` remote that names an owner and a repo, so the home folder cannot be found." % remote)
        self.slug = "%s/%s" % pair
        self.home = os.path.join(cs.home_root(), pair[0], pair[1])

    def _read(self, *parts):
        with open(os.path.join(self.cairn, *parts), encoding="utf-8-sig") as handle:
            return handle.read()

    def _fresh(self, path):
        if os.path.exists(path):
            raise Stop("%s already exists. Move it away first." % path)
        return path

    def plan(self):
        self.check()
        roadmap = self._read("ROADMAP.md")
        rows = table_rows(roadmap)
        titles = {row["id"]: row["title"] for row in rows}

        # Plans in flight go to the home folder.
        for row in rows:
            if row["status"] not in IN_FLIGHT:
                continue
            source = os.path.join(self.cairn, row["path"])
            if not os.path.isfile(source):
                self.notes.append("%s (%s) is %s but has no file at cairn/%s." % (
                    row["id"], row["title"], row["status"], row["path"]))
                continue
            slug, text = convert_plan(self._read(row["path"]), row, titles)
            target = self._fresh(os.path.join(self.home, "plans", slug + ".md"))
            self.steps.append((
                "plan %s (%s): cairn/%s -> %s" % (slug, row["status"], row["path"], target),
                lambda s=source, t=target, x=text: self._move_plan(s, t, x),
            ))
            if row["status"] == "blocked":
                self.notes.append("Check the `Blocked on:` line of plan %s." % slug)

        new_roadmap, count, tags = convert_roadmap(roadmap)
        profile = self._read("PROFILE.md") if os.path.isfile(os.path.join(self.cairn, "PROFILE.md")) else None
        if profile is None:
            self.notes.append("There is no cairn/PROFILE.md. Write one from the template.")
        if tags:
            self.notes.append(
                "%d rows lost a `[low]` or `[parked]` tag. A row that waits on "
                "something outside is `[blocked]` in v3." % tags)

        shelf = os.path.join(self.cairn, "references", "sources")
        shelf_files = sorted(os.listdir(shelf)) if os.path.isdir(shelf) else []
        for name in shelf_files:
            self._fresh(os.path.join(self.home, "shelf", name))

        if self.own:
            self._fresh(os.path.join(self.cairn, "archive"))
            for name in ARCHIVED:
                if os.path.exists(os.path.join(self.cairn, name)):
                    self.steps.append((
                        "cairn/%s -> cairn/archive/%s" % (name, name),
                        lambda n=name: self._archive(n),
                    ))
            self.steps.append((
                "rewrite cairn/ROADMAP.md: %d candidate rows, the milestone table dropped" % count,
                lambda: self._write_tracked("cairn/ROADMAP.md", new_roadmap),
            ))
            if profile is not None:
                self.steps.append((
                    "rewrite cairn/PROFILE.md as Verify, Changelog, and Release",
                    lambda: self._write_tracked("cairn/PROFILE.md", convert_profile(profile)),
                ))
            claude = os.path.join(self.top, "CLAUDE.md")
            swapped = False
            if os.path.isfile(claude):
                with open(claude, encoding="utf-8") as handle:
                    text, swapped = swap_section(handle.read(), template("claude-md-section.md"))
                if swapped:
                    self.steps.append((
                        "swap the cairn section of CLAUDE.md",
                        lambda t=text: self._write_tracked("CLAUDE.md", t),
                    ))
            if not swapped:
                self.notes.append("CLAUDE.md has no \"%s\" section. Add it from the template." % SECTION_HEADING)
            if shelf_files:
                self.steps.append((
                    "shelf: %d files, cairn/references/sources/ -> %s" % (
                        len(shelf_files), os.path.join(self.home, "shelf")),
                    lambda: self._move_shelf(shelf, shelf_files),
                ))
        else:
            for name in ("ROADMAP.md", "PROFILE.md", "DESIGN.md", "references", "archive"):
                self._fresh(os.path.join(self.home, name))
            self.steps.append((
                "everything under cairn/ -> %s (v2 records, and anything else, under archive/)" % self.home,
                lambda: self._move_guest(new_roadmap, profile, shelf, shelf_files),
            ))
            self.steps.append((
                "take the cairn/ line out of .git/info/exclude",
                self._clean_exclude,
            ))
        design = os.path.join(self.cairn, "DESIGN.md")
        if os.path.isfile(design) and re.search(
                r"^## Known issues", self._read("DESIGN.md"), re.MULTILINE | re.IGNORECASE):
            self.notes.append("DESIGN.md has a Known issues section for the setup table.")
        return self

    # ---- the steps ---------------------------------------------------

    def _write(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def _write_tracked(self, relative, text):
        self._write(os.path.join(self.top, relative), text)
        self.git("add", "--", relative)

    def _move_plan(self, source, target, text):
        self._write(target, text)
        relative = os.path.relpath(source, self.top)
        code, _ = self.git("rm", "-q", "--", relative)
        if code != 0 and os.path.exists(source):
            os.remove(source)

    def _archive(self, name):
        source = os.path.join(self.cairn, name)
        if not os.path.exists(source):
            return
        os.makedirs(os.path.join(self.cairn, "archive"), exist_ok=True)
        code, _ = self.git("mv", "-k", "cairn/" + name, "cairn/archive/" + name)
        if os.path.exists(source):  # untracked, or what git left behind
            target = os.path.join(self.cairn, "archive", name)
            if os.path.isdir(source) and os.path.isdir(target):
                if not _has_files(source):
                    shutil.rmtree(source)
                    return
                target = os.path.join(target, "untracked")
            shutil.move(source, target)

    def _move_shelf(self, shelf, names):
        target = os.path.join(self.home, "shelf")
        os.makedirs(target, exist_ok=True)
        for name in names:
            shutil.move(os.path.join(shelf, name), os.path.join(target, name))
        if not os.listdir(shelf):
            os.rmdir(shelf)

    def _move_guest(self, new_roadmap, profile, shelf, shelf_files):
        home = self.home
        archive = os.path.join(home, "archive")
        os.makedirs(archive, exist_ok=True)
        if shelf_files:
            self._move_shelf(shelf, shelf_files)
        elif os.path.isdir(shelf):
            os.rmdir(shelf)
        shutil.move(os.path.join(self.cairn, "ROADMAP.md"), os.path.join(archive, "ROADMAP-v2.md"))
        self._write(os.path.join(home, "ROADMAP.md"), new_roadmap)
        if profile is not None:
            shutil.move(os.path.join(self.cairn, "PROFILE.md"), os.path.join(archive, "PROFILE-v2.md"))
            self._write(os.path.join(home, "PROFILE.md"), convert_profile(profile))
        for name in sorted(os.listdir(self.cairn)):
            source = os.path.join(self.cairn, name)
            keep = name in ("DESIGN.md", "references")
            shutil.move(source, os.path.join(home if keep else archive, name))
        os.rmdir(self.cairn)

    def _clean_exclude(self):
        _, path = self.git("rev-parse", "--git-path", "info/exclude")
        path = os.path.join(self.top, path)
        try:
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines()
        except OSError:
            return
        kept = [line for line in lines if line.strip().strip("/") != "cairn"]
        if kept != lines:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("\n".join(kept) + "\n")

    def apply(self):
        for _, step in self.steps:
            step()

    def report(self, applied):
        kind = "the user's own repo" if self.own else "a guest repo"
        lines = ["%s (%s)" % (self.slug, kind), "Home folder: %s" % self.home, ""]
        lines.append("Done:" if applied else "Would do:")
        lines.extend("- " + description for description, _ in self.steps)
        if self.notes:
            lines.extend(["", "For the session to look at:"])
            lines.extend("- " + note for note in self.notes)
        lines.append("")
        if not applied:
            lines.append("Nothing was changed. Run again with --apply to do it.")
        elif self.own:
            lines.append("The changes are staged and not committed.")
        else:
            lines.append("Nothing of cairn is left in the checkout. Commit ~/.cairn to record the move.")
        return "\n".join(lines)


def _has_files(folder):
    return any(files for _, _, files in os.walk(folder))


def main(argv):
    args = list(argv[1:])
    cwd = os.getcwd()
    if args[:1] == ["-C"] and len(args) >= 2:
        cwd, args = args[1], args[2:]
    if args not in ([], ["--apply"]):
        print("usage: cairn_migrate.py [-C DIR] [--apply]")
        return 2
    code, top = cs.git(["rev-parse", "--show-toplevel"], cwd)
    if code != 0 or not top:
        print("Not a git checkout.")
        return 1
    try:
        migration = Migration(top).plan()
        if args:
            migration.apply()
        print(migration.report(applied=bool(args)))
    except Stop as err:
        print(str(err))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
