---
name: cairn-release
description: Prepare a release following the active toolchain profile's release-walk - an r-package profile runs the CRAN walk (version bump, NEWS, checks, cran-comments, human submission checklist); a generic profile does a version bump + changelog + tag. Use when the user wants to release, submit to CRAN, cut a version, or prepare a release. Never self-submits.
argument-hint: "[patch | minor | major]"
---

# /cairn-release — release walk (profile-driven)

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first. This skill
prepares a release and hands any outward action to the user — **it never
self-submits** (no registry submission, no tag push without approval). The
toolchain-specific steps come from the active profile's `release-walk` slot;
this skill is the universal spine around it.
Phase header: `# Release <version>` → `## <step>`.
Chapter markers: mark a chapter at each phase transition (session start implicit).

## Preconditions

- Session start: read `cairn/ROADMAP.md` and `cairn/DECISIONS.md` (standing
  constraints bind the release too); if an un-ingested RR sits in
  `cairn/reviews/`, handle ingestion first (see `/milestone-brief`).
- No milestone `in-progress` — release from a clean, green default branch. (A
  milestone at `review` should be merged or explicitly deferred first.)
- Clean `git status`; local default branch up to date with origin (detect it
  per the tracking-rules git model).
- **Read the active profile's `release-walk` slot** (`cairn/PROFILE.md`; absent
  → infer per tracking-rules "Toolchain profiles"): it names the release steps
  for this repo's toolchain. Toolchain preconditions gate on the profile — a
  `DESCRIPTION` file, a registry toolchain install — are required **only when
  the profile's `release-walk` names them** (an r-package profile does; a
  generic profile does not). Never assume a toolchain the profile doesn't
  declare.

## Workflow

The `release-walk` slot is authoritative — read it, never recall a hardcoded
walk. The steps below are the universal spine; the slot fills in the
toolchain-specific work at step 3.

1. **Version decision** (question gate, one round): review the declared
   changelog — the file the active profile's `changelog` slot names ("none" →
   review git history since the last tag instead) — and recommend patch /
   minor / major with rationale (breaking changes force minor/major; pre-1.0
   conventions per DESIGN.md). Confirm the target version with the user.

2. **Changelog consolidation** (the declared file; a "none" declaration skips
   this step): retitle the development heading to the release version; group
   entries (breaking changes first, then new features, fixes); prune noise;
   no milestone numbers or internal jargon.

3. **Follow the active profile's `release-walk` slot.** Run each step the slot
   names, in order, recording results as you go:
   - An **r-package** profile's slot is the CRAN walk — full local
     verification, wide checks, `cran-comments.md`, the version bump, and a
     human submission checklist. It is CRAN-flavored end to end and never
     self-submits.
   - A **generic** profile's slot is the minimal walk — bump the version marker,
     commit the release prep to the default branch, and tag the release. The tag
     is the release; there is no registry step.
   For any slow checks the slot names (wide/registry checks, reverse-dependency
   runs), follow the tracking-rules CI waiting rules — one blocking wait each,
   report results when they arrive. Any outward action (submitting, pushing a
   tag) is the user's to take at the approval gate; this skill prepares, it does
   not push.

4. **Handoff / final actions.** Lead outcome-first: what this release contains
   and why the version was chosen, in plain words, before the mechanics. Then
   present the slot's terminal actions as a checklist for the user to run
   (r-package: the CRAN submission checklist — submit, confirm the email, then
   tag the GitHub release and bump to the next dev version; generic: the
   tag/push commands), never performed on their behalf. Every command in that
   checklist is a **handoff** — the whole step exists to hand the user work to
   run — so each goes in a fenced block, never inline backticks
   (tracking-rules "Copy-run commands"). Offer to prepare the
   post-acceptance steps as a follow-up when the user returns.

5. Work-log/ROADMAP note: one line in ROADMAP ("Released <version>
   YYYY-MM-DD") is permitted as a Done-section annotation; nothing else in
   tracking changes.

6. **Routing chip (AskUserQuestion)**, composed from the release's end state
   (chip rules per tracking-rules) — e.g. **Stop here — run the submission /
   tag checklist yourself** (recommended) / Plan the next milestone →
   `/milestone-plan` / Run a health check → `/milestone`.
