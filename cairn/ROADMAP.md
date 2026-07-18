# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-18 (M78 done + archived; M73 pruned under terminal-row retention; two LESSONS pairs consolidated to make room for M78's; M79 planned and workable)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

_Released 1.0.0 2026-07-16 (tag v1.0.0)._

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M74 | Issue triage — /milestone enumerates untriaged inboxes into candidate rows | done | M73 | normal | milestones/archive/M74-issue-triage.md |
| M75 | Record consistency — the `leave` disposition and MCP-matcher semantics (D-044) | done | — | normal | milestones/archive/M75-record-consistency.md |
| M76 | Record correction — history vs. current knowledge, and the correct-in-place protocol (D-045) | done | — | normal | milestones/archive/M76-record-correction.md |
| M77 | Work-log cap exemption — the budget stops counting a section IP4 forbids editing (D-046) | done | — | normal | milestones/archive/M77-worklog-cap-exemption.md |
| M78 | Source-note shape — dated observations and page provenance | done | — | high | milestones/archive/M78-source-note-shape.md |
| M79 | References content check — the lint stops being a filename census | review | M78 | normal | milestones/M79-references-content-check.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- Citekey resolution + dependent discovery: `citekey (p. N)` is mandated (`validation-doctrine.md:79`) but never parsed in either direction — a citekey naming no page and a page nothing cites both pass — and `cairn_impact.py:45` excludes `references/`, so the one record type designated "current knowledge, corrected in place" (`tracking-rules.md:137-139`) is the one with no impact tooling; blocked on a standing rejection — M56 rejected "a formal query op" and "graph tooling" (`archive/M56-llm-wiki-investigation.md:17-19`), which a superseding D-entry must narrow before this is planned; promote if restatement drift produces a live wrong value (intraclass's Koo-bands and unbacked-Cicchetti chains are the candidates) — added 2026-07-18 — M79 Out
- references/ ingestion completeness (grouped): three gaps from the M78 audit — (1) no skill owns ingestion, so PDF→page is 8 lines of prose at `validation-doctrine.md:75-82` read conditionally, with D-031 having removed per-skill read directives; (2) no synthesis-note template (M78 ships the source-note one only); (3) no re-verification loop — no page records when it was last checked against its PDF and no skill re-checks, so pages are write-once in practice; promote once M78's template is in use and shows which gap actually bites — added 2026-07-18 — M78/M79 Out
- Concurrent-cairn-operator hardening: if two people ever run cairn in the same repo at once the tracking files race — milestone IDs and D-numbers are model-picked with no allocator, duplicate D-numbers auto-merge and validate GREEN (`cairn_validate.py:500-506` uses a `set`), `/milestone-plan` commits to the default branch with no fetch/pull at any step, and `check_single_in_progress` (`cairn_validate.py:61-64`) is a hard FAIL two operators trip by construction; cheapest standalone piece is a `check_d_uniqueness`; swept: no existing row or D-entry covers it — promote if a second cairn operator actually appears — added 2026-07-18 — M72 Out (D-043)
- Budget-first drafting (cap prevention): up-front per-section line budgets in the milestone template/rulebook so first drafts land under the 150-line cap by construction, rather than compressing after — reassess once M69's diagnostic + single-pass discipline is in use and we can see whether the cure suffices — added 2026-07-17 — M69 Out
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Contributor-facing scaffold: cairn ships nothing a repo can hand an outsider — no CONTRIBUTING, PR template, or issue template (`git ls-files` matches zero; there is no `.github/` in this repo), so a contributor learns the branch/commit/tracking conventions only by being told; would be a `/cairn-init` opt-in, not a core scaffold addition — promote once M72's README subsection is in use and proves insufficient — added 2026-07-18 — M72 Out
- Branch-protection compatibility: cairn structurally requires direct pushes to the default branch (`tracking-rules.md:248-252` docs-only commits; `/milestone-review`'s post-merge hygiene pass), which a repo protecting its default branch behind required PRs cannot do — needs a decision on whether hygiene commits get their own PR or the rule gains a protected-branch mode — promote if an adopting repo turns on branch protection — added 2026-07-18 — M72 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
