# Toolchain profile: quarto-extension

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates this into the repo's
     `cairn/PROFILE.md`. The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot here — it is the orthogonal domain axis
     (D-024/D-025), stated once in skills/shared/validation-doctrine.md
     (referenced from tracking-rules). All seven `## <slot>` sections
     are defined; cairn_validate FAILs on a missing or empty slot. -->

The Quarto extension toolchain: a repo whose deliverable is a Quarto extension
under `_extensions/<name>/` (a filter, shortcode, format, or project type),
installed with `quarto add <owner>/<repo>`. Quarto 1.10 installs from the
branch named `main`, so in a repo whose default branch is `main` a merge
reaches users at once. A `v<version>` tag and a GitHub release mark the
version for `quarto add <owner>/<repo>@v<version>` and the releases page.
Selected by `cairn-init` when `_extensions/*/_extension.yml` (or `.yaml`) is
present and no language, plugin, or `Dockerfile` marker is. With a
`Dockerfile`, the disambiguation gate asks.

## verify
Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite). Declare the
repo's own check here. It is usually a render of the repo's example or test
document, such as `quarto render example.qmd`. Add any test command the repo
has for its Lua or JavaScript. If the repo has none, state "no automated
verify" and rely on the acceptance-criteria evidence.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- Every version marker that `release-walk` names holds the same version.
- The verify render succeeds on the review head.
- The declared changelog (`## changelog` slot) has an entry for this
  milestone's user-visible changes, or the slot says "none".

## test-doctrine
Test expectations layered on the universal "What gets a test" rules in
tracking-rules. An extension is checked by rendering, not by calling functions:
- A filter or shortcode change is tested by rendering a fixture document that
  uses it and checking the output (a string in the HTML, or a snapshot of it).
- A bug fix gets a fixture document that renders wrong before the fix.
- A change to a shipped asset (JavaScript, CSS) that browsers cache by path
  raises the version wherever the repo ties the asset path to it.

## release-walk
The release procedure `/cairn-release` follows. The version marker is
`version:` in `_extensions/<name>/_extension.yml` (or `.yaml`). A repo that
keeps the same version in more files names each file here. One example is an
`add_html_dependency{ version = ... }` call in the extension's Lua filter.
Every named marker holds the same version. First read the default branch's tip
on an up-to-date checkout:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_versions.py" _extensions/<name>/_extension.yml`.
It prints the tip's version, the first commit of that version's unbroken run
of first-parent commits (`start`), and whether a `v<version>` tag exists.
- **Tag-only arm.** When the tag is absent, the tip's version is unreleased:
  merged work raised it, or it was never tagged. Skip the version decision and the changelog consolidation, raise
  nothing, and make no prep commit. Tag the run's start:
  `git tag -a v<version> <start> -m "v<version>"`, pushed at the user's approval.
- **Release-time arm.** When the tag exists, run the generic walk. Decide the
  bump (patch/minor/major) from the declared changelog. With changelog "none",
  decide it from git history and skip the consolidation. Raise every named
  marker and commit the release prep to the default branch. Tag that commit
  `v<version>`, pushed at the user's approval.
- **Release notes.** The notes are the changelog section for the version. With
  changelog "none", they are the commit subjects on the default branch since
  the previous `v*` tag:
  `git log --first-parent --format='- %s' <previous tag>..<tagged commit>`.
  For a first release, with no previous `v*` tag, drop `<previous tag>..` to
  list every subject up to the tagged commit. Where the `origin` remote is GitHub and `gh` is available, the handoff
  provides a `gh release create` command with these notes. cairn provides it
  and never runs it (the universal step 4). No registry step: the tag is the
  release.

## init-detection
Recognized by `cairn-init` from `_extensions/*/_extension.yml` or
`_extensions/*/_extension.yaml`. The repo must also have no `DESCRIPTION`, no
`pyproject.toml`/`setup.py`/`setup.cfg`, and no
`.claude-plugin/plugin.json`/`.claude-plugin/marketplace.json`. It ranks ahead
of docker-image and generic. A repo that also carries a language, plugin, or
`Dockerfile` marker is a hybrid: cairn-init runs the disambiguation gate.

## greenfield-openers
Openers `cairn-init` asks in a new or empty extension repo, on top of the
universal openers (distribution ambition and numeric-work oracles):
- **Extension type?** Filter, shortcode, format, or project type.
  - Lands in: DESIGN Purpose and the verify render's fixture document.
- **When does the version rise?** At release (reversible default), or at each
  merge that changes a shipped asset, when browsers cache that asset by a path
  that holds the version.
  - Consequence: at merge, the release walk's tag-only arm tags the tip's
    raised version. Run it after each raising merge, or earlier versions stay
    untagged. At release, the release-time arm raises the version.
  - Lands in: CLAUDE.md conventions and the `release-walk` marker list.

## changelog
The repo's changelog file, read by `/hotfix`, the release-walk, and the
consistency-gate. Declare it here, for example `CHANGELOG.md`. If the repo
keeps no changelog, write "none": `/hotfix` then skips the changelog entry,
and the release-walk writes its release notes from git history.
