# M163: External adoption pass (RR13 step 3)

**Status:** done (2026-08-29, PR #164 https://github.com/jmgirard/cairn/pull/164)

**Goal:** Run cairn's first external adoption pass — `/cairn-init` (migration
path) plus one full milestone loop on bsync — logging friction, fixing what breaks.

**Outcome:** bsync migrated (pre-init MILESTONES.md M1–M7 entombed verbatim,
r-package profile, validate exit 0 at bsync 5112c2f) and bsync M008 ran the full
plan→implement→review→merge→archive loop (landed a8f269a). Friction ledger F1–F4,
all dispositioned: F1 declined (harness cwd-reset is harness-owned); F2 fixed —
`templates/lessons.md` + `templates/decisions.md` now ship, cairn-init references
them, `scripts/tests/test_shipped_templates.py` guards; F3 fixed — merge_guard
denies cd-compound `gh pr merge` spellings with session-cwd guidance before any
marker check; F4 fixed — heredoc/quoted-text false positive documented with the
Write-tool workaround.

**Decisions:** none.

**Review:** three-lens fan-out; 13 findings — 10 fixed at the gate (cd-check
extended to every merge occurrence; same-repo-cd respell escape and ask-the-user
path added to the denial; docstring limitations rewritten incl. pushd/`cd;`;
template sweep widened to all `skills/` .md; 3 DESIGN wording fixes; 2 new
discriminating tests — hooks 121, scripts 327), 2 rejected, 1 informational.
Nothing graduated or retired.
