# M14: Section write allow-lists per skill — done 2026-07-11

**Goal:** formalize which skill may write which milestone-file section, so
plan/implement/review can't silently clobber each other's sections.

**Outcome:** a section-ownership table (section → writing skill → write-mode)
in `tracking-rules.md`, `owner:` tags on every template section, and pointer
cross-refs in the three phase skills. Locked by
`skills/tests/test_section_allow_lists.py`, which fails if the table and
template disagree on any section's **name or owner** (both guards verified
non-vacuous against injected drift). Authorship itself isn't mechanizable
(git records no which-skill-wrote-what signal) — the structural parity is the
lock. Write-modes: create · append-only · amend-via-gate · mirror-update ·
check-off · exclusive.

**Review:** SHIP WITH NITS. F1 (name-only lock missed owner drift) → added
owner-parity test; F2 (restated sections) → trimmed to pointers; F3
(`create-once` undefined) → vocab reconciled; F4 (cosmetic-rename masking) →
rejected as cosmetic. No D-entries.

PR #12 (squash-merged).
