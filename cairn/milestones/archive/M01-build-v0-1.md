# M01: Build plugin v0.1 from DRAFT_2 spec — done 2026-07-11

**Goal:** Translate DRAFT_2.md into a working v0.1 plugin: manifest, shared
rulebook, templates, all eight skills, README, changelog.

**Outcome:** Shipped. Eight skills with complete frontmatter, each reading
the shared rulebook first; rulebook covers all eleven required topic areas;
four templates matching DRAFT_2 §6; README carries the §12 user guide +
install section; dogfooded `project/` in this repo.

**Review (2026-07-11):** All criteria passed with command-gathered evidence.
Plugin-adapted consistency gate clean (manifests parse, D-006 name, 0.1.0
CHANGELOG entry). Independent fresh-context Opus review: 0 blockers,
3 should-fix (fixed same day: D-007 marketplace timing, full skill list in
claude-md-section template, single-in-progress guard in
/milestone-implement), 7 nits (4 bundled into a v0.2-polish candidate; rest
already tracked). Approved by Jeff 2026-07-11.

**Key decisions:** D-001…D-007 (plugin distribution, per-milestone files +
ROADMAP authority, chip-glued phase skills, gated Fable RB/RR, entombing
migration, "cairn" naming, marketplace.json early-ship).

**PR:** none — built directly on main before the repo had git history;
review fixes committed to main under the same logged exception.
