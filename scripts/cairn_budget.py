#!/usr/bin/env python3
"""Report one capped cairn artifact against its cap, while it is being drafted.

The other reporters in this directory answer "what is the state of this repo?"
and run at a gate. This one answers "how much of my budget have I spent?" and
runs mid-draft, which is why it takes a FILE rather than the optional ROOT its
siblings take (``cairn_next.py`` with no argument means "this repo"; a bare
``cairn_budget.py`` means nothing, so it prints usage and exits 2 — M99 gate).

The problem it exists for: ``cairn_validate`` reports a cap only once the
artifact is finished and over it, so the remedy is always compression after the
fact. Measured across this repo's history (M99 T1), 55 of 96 archive summaries
sit at EXACTLY the cap — a distribution censored at the ceiling, which is what
compress-until-it-fits looks like from the outside. Showing the number during
drafting is what lets a first draft land under cap instead.

Every cap here is read from ``cairn_scripts``; none is restated. That is load-
bearing rather than tidy: a drafting counter that disagreed with the gate
counter would send an author to compress prose that was never over, or bless a
draft the gate then rejects. For the same reason the plan-owned body figure is
``milestone_body_line_count`` itself, not a re-implementation of it.

What is deliberately NOT here: the per-section drafting budgets. Those live in
``skills/shared/templates/``, where the drafting happens, and are guidance
rather than enforcement — this script reports the enforced caps and the
measured sections, and never asserts what a section's right size is. Keeping
the two apart is what stops the budgets from acquiring a second home that can
drift from the first (M99 Scope).

Usage: ``python3 scripts/cairn_budget.py <path>``. Exit 0 within every axis,
1 if any axis is over, 2 if the path is unusable or carries no cap.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cairn_scripts as cs  # noqa: E402  (after sys.path shim)


class Axis:
    """One measured quantity against one cap.

    ``strict`` mirrors the comparison the gate makes, and the two really do
    differ: ``check_caps`` fails a line cap on ``n >= cap`` but an archive
    summary on ``n > cap``, so `<150` permits 149 while `≤25` permits 25.
    Deriving the permitted value and the shed figure through the operator —
    never by assuming cap-1 — is M87's rule, and it is the difference between
    telling an author they have one line left and telling them they have none.
    """

    def __init__(self, label, value, cap, strict=True, unit="lines", note=""):
        self.label = label
        self.value = value
        self.cap = cap
        self.strict = strict
        self.unit = unit
        self.note = note

    @property
    def permitted(self):
        return self.cap - 1 if self.strict else self.cap

    @property
    def over(self):
        return self.value > self.permitted

    def render(self):
        marker = f"cap <{self.cap:,}" if self.strict else f"cap ≤{self.cap:,}"
        head = f"  {self.label:<18} {self.value:>7,} / {self.permitted:,} {self.unit} ({marker})"
        if self.over:
            return f"{head}  OVER by {self.value - self.permitted:,} — shed ≥{self.value - self.permitted:,}"
        return f"{head}  headroom {self.permitted - self.value:,}"


def classify(root, path):
    """Return (label, relpath) for a capped artifact, or (None, relpath).

    Dispatch is by path, matching how ``check_caps`` finds the same files.
    A path outside the repo, or one no cap covers, returns a None label so the
    caller can say so rather than report a misleading zero.
    """
    rel = os.path.relpath(os.path.abspath(path), root).replace(os.sep, "/")
    if rel.startswith(".."):
        return None, rel
    if rel in cs.LINE_CAPS:
        return "tracking file", rel
    if rel == "CLAUDE.md":
        return "CLAUDE.md cairn section", rel
    base = os.path.basename(rel)
    if base.startswith("M") and base.endswith(".md"):
        if rel.startswith("cairn/milestones/archive/"):
            return "archive summary", rel
        if rel.startswith("cairn/milestones/"):
            return "live milestone", rel
    return None, rel


def axes(root, kind, rel):
    """The axes that apply to one artifact, in reporting order.

    Each file class carries exactly the axes the gate applies to it — a
    ``PROFILE.md`` has an item cap and no mass threshold, and inventing one
    here would report a budget nothing enforces.
    """
    path = os.path.join(root, rel)
    out = []
    if kind == "tracking file":
        out.append(Axis("items", cs.line_count(path), cs.LINE_CAPS[rel]))
        if rel in cs.CHAR_CAPS:
            out.append(
                Axis("mass", cs.char_count(path), cs.CHAR_CAPS[rel], unit="chars")
            )
            # The per-line axis, as a real Axis rather than trailing text, so it
            # reaches the exit code like every other (M99 review F1: it printed
            # OVER and exited 0, contradicting this module's stated contract).
            # Reported even when clean, because the stamp it exists for is
            # rewritten by hand and the author needs the number before the
            # rewrite, not after (M93). Only the longest line: a file-level
            # number cannot point at the line responsible, and the longest one
            # is the only one whose fix is load-bearing.
            longest = sorted(cs.non_item_lines(path), key=lambda p: -p[1])[:1]
            for lineno, length in longest:
                out.append(
                    Axis(
                        "longest non-item",
                        length,
                        cs.NON_ITEM_LINE_CAP,
                        unit="chars",
                        note=f"line :{lineno} — replace it, don't append to it",
                    )
                )
    elif kind == "CLAUDE.md cairn section":
        # A None here means the file carries no `## Project tracking` section —
        # a repo mid-adoption, or one that never adopted cairn. `check_caps`
        # passes that silently and so must this: the Axis is simply absent, and
        # `report` says so rather than calling a readable file unreadable
        # (M99 review F2, which had it exit 2 — this repo's not-a-cairn-repo
        # signal — over a file that is fine).
        out.append(
            Axis("section", cs.claude_section_line_count(path), cs.CLAUDE_SECTION_CAP)
        )
    elif kind == "archive summary":
        # `>` not `>=` — the rulebook writes this one as ≤25, so 25 passes.
        out.append(Axis("whole file", cs.line_count(path), cs.ARCHIVE_CAP, strict=False))
    elif kind == "live milestone":
        out.append(
            Axis(
                "plan-owned body",
                cs.milestone_body_line_count(path),
                cs.MILESTONE_CAP,
                note="less ## Review and ## Work log (M55, D-046)",
            )
        )
    return [a for a in out if a.value is not None]


def report(root, path):
    """The rendered report, and whether any axis is over. Returns (text, over)."""
    kind, rel = classify(root, path)
    if kind is None:
        return f"{rel}: no cairn cap applies to this path\n", None
    lines = [f"{rel} — {kind}"]
    found = axes(root, kind, rel)
    if not found:
        if kind == "CLAUDE.md cairn section" and os.path.exists(
            os.path.join(root, rel)
        ):
            # Readable, just not carrying a cairn section. Not a cap failure
            # (check_caps agrees), so this reports and exits clean.
            return f"{rel}: no cairn section — nothing capped here\n", False
        return f"{rel}: unreadable\n", None
    for a in found:
        lines.append(a.render())
        if a.note:
            lines.append(f"  {'':<18} {a.note}")
    full = os.path.join(root, rel)
    if kind == "live milestone":
        sections = cs.milestone_section_line_counts(full) or []
        if sections:
            ranked = sorted(sections, key=lambda s: s[1], reverse=True)
            lines.append(
                "  sections, heaviest first: "
                + " · ".join(f"{h} {n}" for h, n in ranked)
            )
    return "\n".join(lines) + "\n", any(a.over for a in found)


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(
            "usage: cairn_budget.py <path>\n"
            "  reports one capped cairn artifact against its cap, for use "
            "while drafting it.\n"
            "  Unlike the other reporters, the argument is a FILE, not a "
            "repo root.\n"
        )
        return 2
    path = argv[1]
    try:
        root = cs.resolve_root([argv[0], os.path.dirname(os.path.abspath(path))])
    except cs.NotCairn:
        cs.die_not_cairn(path)
        return 2
    text, over = report(root, path)
    if over is None:
        sys.stderr.write(text)
        return 2
    print(text, end="")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
