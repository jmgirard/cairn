# M11: Shift phase headers up one level (H1 unit / H2 phase) — done

**Shipped:** 2026-07-11 · PR #9 · docs-only.

**Goal/outcome:** Phase-header convention shifted up one level so both levels
appear in Claude Desktop's TOC (it indexes only H1/H2): unit of work `##`→`#`,
phase `###`→`##`. Two-level nesting and emission cadence unchanged. Applied to
the `Phase header` rule in `skills/shared/tracking-rules.md` and the one
`Phase header:` directive in each of the 8 skills.

**Verification:** New `skills/tests/test_phase_header_levels.py` locks the
convention — proven to fail on both an old-form (H3 phase) revert and an
over-shift (phase at H1). Full suite green (6 tests). Independent Opus review:
SHIP, no correctness defects; its two low-severity guard-hardening flags fixed
in-branch.

**Key decisions:** D-012 (supersedes D-010's level choice; D-010 left verbatim
per append-only). Redundant user memory `scannable-h2-phase-headers` retired —
the convention now lives durably in the plugin (D-011/GP4).

**Note:** takes effect in new conversations once skills reload; the
implementing session still rendered the old `##`/`###` levels.
