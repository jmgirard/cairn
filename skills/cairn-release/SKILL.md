---
name: cairn-release
description: Prepare an R package release to CRAN - version bump, NEWS consolidation, full checks, cran-comments, and a final human checklist. Use when the user wants to release, submit to CRAN, cut a version, or prepare a release. Never self-submits.
argument-hint: "[patch | minor | major]"
---

# /cairn-release — CRAN release walk

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first. This
skill prepares everything and hands the actual submission to the user —
**it never self-submits to CRAN.**
Phase header: `# Release <version>` → `## <step>`.
Chapter markers: mark a chapter at each phase transition (session start implicit).

## Preconditions

- Session start: read `cairn/ROADMAP.md` and `cairn/DECISIONS.md`
  (standing constraints bind the release too); if an un-ingested RR sits
  in `cairn/reviews/`, handle ingestion first (see `/milestone-brief`).
- No milestone `in-progress` — release from a clean, green default branch. (A
  milestone at `review` should be merged or explicitly deferred first.)
- Clean `git status`; local default branch up to date with origin (detect it
  per the tracking-rules git model).

## Workflow

1. **Version decision** (question gate, one round): review NEWS.md since the
   last release and recommend patch / minor / major with rationale
   (breaking changes force minor/major; pre-1.0 conventions per DESIGN.md).
   Confirm the target version with the user.

2. **NEWS consolidation:** retitle the development heading to the release
   version; group entries (breaking changes first, then new features,
   fixes); prune noise; no milestone numbers or internal jargon.

3. **Full local verification:**
   - `devtools::document()` — no diff.
   - `devtools::test()` and `devtools::check()` — clean (0 errors,
     0 warnings; justify any NOTEs).
   - `devtools::build_readme()` if README.Rmd exists.
   - `pkgdown::check_pkgdown()` if a site exists.
   - `urlchecker::url_check()` for stale URLs.
4. **Wide checks** as applicable: `devtools::check_win_devel()` and/or
   R-hub; reverse-dependency checks (`revdepcheck`) if the package has
   downstream dependents. These are slow — one blocking wait each, per the
   CI waiting rules; report results when they arrive.

5. **cran-comments.md:** update with test environments, check results, NOTE
   justifications, and (for updates) reverse-dependency summary and any
   CRAN-policy responses.

6. Bump `Version:` in DESCRIPTION. Commit release prep directly to the
   default branch (docs/metadata only) or via a short branch + PR if code had to change —
   user's call at the approval gate.

7. **Handoff checklist** (present to the user; do not perform). Lead
   outcome-first: what this release contains and why the version was
   chosen, in plain words, before the checklist:
   - [ ] `devtools::submit_cran()` — run this yourself.
   - [ ] Confirm the CRAN email.
   - [ ] After acceptance: `usethis::use_github_release()` (or tag
     `v<version>` manually), then bump to the next dev version
     (`usethis::use_dev_version()`).
   Offer to prepare the post-acceptance steps as a follow-up when the user
   returns with the acceptance email.

8. Work-log/ROADMAP note: one line in ROADMAP ("Released <version>
   YYYY-MM-DD") is permitted as a Done-section annotation; nothing else in
   tracking changes.

9. **Routing chip (AskUserQuestion)**, composed from the release's end state
   (chip rules per tracking-rules) — e.g. **Stop here — run the submission
   checklist
   yourself** (recommended) / Plan the next milestone → `/milestone-plan` /
   Run a health check → `/milestone`.
