# Decisions

Append-only. Never renumber; supersede with a new entry. D-entries record
choices with rationale — never deferrals ("not now" is a ROADMAP fact).

### D-001 (2026-07-11): Distribute as a Claude Code plugin

**Context:** Precursor systems were recreated per-repo and diverged.
**Decision:** Logic (skills, rules, templates) ships as this plugin; each
repo holds only state under `project/`.
**Consequences:** Updating the plugin updates every repo's workflow at once;
divergence of logic becomes structurally impossible.

### D-002 (2026-07-11): Per-milestone files + ROADMAP index

**Context:** Precursors used single board files (rotted large) or three-file
boards (fiddly moves).
**Decision:** One file per milestone; ROADMAP.md index table is the only
status authority; done milestones compress to ≤25 lines and archive.
**Consequences:** Hot files stay small; out-of-order completion is natural
(IDs are identifiers, not a sequence).

### D-003 (2026-07-11): Separate phase skills glued by routing chips

**Context:** A single multiplexed skill meant more typing; separate skills
risk rule drift.
**Decision:** Eight separate skills; every phase ends with an AskUserQuestion
chip routing to the next; all skills read one shared tracking-rules.md.
**Consequences:** One click between phases; rules stated once; every
transition is an explicit user stop.

### D-004 (2026-07-11): Fable only via the RB/RR brief protocol, gated per instance

**Context:** Fable subagents are technically spawnable from any session but
are token-billed pay-per-use.
**Decision:** Fable is reached only through a self-contained Review Brief,
behind an explicit per-instance approval gate (spawn or manual run).
**Consequences:** Escalations are reproducible, auditable, ingestible, and
never a silent cost.

### D-005 (2026-07-11): Migration entombs history, translates only live state

**Context:** Converting 50+ legacy milestones invites hallucinated dates and
lossy summaries; git already preserves history.
**Decision:** Legacy files move verbatim to `project/legacy/`; only live
items are translated, under a no-invention rule; IDs never renumbered.
**Consequences:** Migration is a small, reviewable, revertible PR; legacy
citations stay valid.

### D-006 (2026-07-11): Name the plugin "cairn"

**Context:** "rpkg-tracking" was a placeholder. Candidates spanned trail
markers (cairn, waymark, milepost), record keepers (roadbook, ledger), and
roles (steward).
**Decision:** cairn — built one stone at a time (milestones), marks the
trail for whoever comes next (stateless session resume). Action skills keep
generic names (/milestone*, /hotfix); repo-level skills carry the brand
(/cairn-init, /cairn-release).
**Consequences:** Known adjacencies accepted: CRAN's "Cairo" graphics
package (one letter apart) and the Cairn tabletop RPG; no CRAN package
claims "cairn". GitHub home: jmgirard/cairn.
