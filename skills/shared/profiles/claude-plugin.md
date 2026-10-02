# Toolchain profile: claude-plugin

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates this into the repo's
     `cairn/PROFILE.md`. The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot here — it is the orthogonal domain axis
     (D-024/D-025), stated once in skills/shared/validation-doctrine.md
     (referenced from tracking-rules). All seven `## <slot>` sections
     are defined; cairn_validate FAILs on a missing or empty slot. -->

The Claude Code plugin toolchain: a repo that builds one or more plugins, a
marketplace that lists them, or a mod. A mod is a TypeScript hooks module that
a plugin names in its `hooks/hooks.json`. The `claude` command-line tool checks
the manifests and runs the mod's tests. `cairn-init` selects this profile when
a plugin marker is present and no language marker outranks it.

## verify
Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite). Run each
check from the repo root and check its exit code:
- `claude plugin validate <dir>/.claude-plugin/plugin.json` for each plugin
  in the repo. It passes with warnings and fails on any error.
- `claude plugin validate .claude-plugin/marketplace.json` where the repo has
  a marketplace file.
- Where the repo has `*.test.ts` or `*.test.tsx` files:
  `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test <plugin-dir>`.
  `<plugin-dir>` is the folder whose `hooks/hooks.json` names the mod under
  `modules`. Any other folder fails with "no hooks module to load". The command
  runs every `*.test.ts(x)` file under that folder, so keep tests for other
  runners (vitest, jest) outside it. Without the variable, a process that the
  rollout switch serves "off" refuses with "hooks modules are turned off in
  this process" (observed on Claude Code 2.1.286).
- Other code the plugin ships (hook scripts in Python or shell, an MCP
  server) keeps its own test command. Declare it here.

Do not add `--strict`. It fails on warnings, and a CLAUDE.md at the plugin
root always draws one: "CLAUDE.md at the plugin root is not loaded as project
context".

A desktop app shell has no `claude` on its PATH. Find the binary here:
- A native install links `~/.local/bin/claude` to
  `~/.local/share/claude/versions/<version>`.
- The macOS desktop app keeps one binary per version under
  `~/Library/Application Support/Claude/claude-code/<version>/<hash>/claude.app/Contents/MacOS/claude`.
  Use the newest version. The `claude-code-vm/<version>/claude` file beside it
  is a Linux binary for the app's VM and does not run on the Mac.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- The verify checks pass on the review head.
- The marketplace validate output has no `plugins[N].version` warning. That
  warning means a marketplace entry's `version` differs from its plugin's
  `plugin.json`. At install time, `plugin.json` wins.
- The declared changelog (`## changelog` slot) has an entry for this
  milestone's user-visible changes (no milestone numbers in user-facing text).

## test-doctrine
Plugin-specific test expectations layered on the universal "What gets a test"
rules in tracking-rules:
- A mod's behavior is tested by `*.test.ts(x)` files that import their kit
  from `claude-code/testing`. `claude plugin test` runs each file in a child
  of the `claude` binary, in an environment like the one the mod's hooks run
  in. Test what the mod draws or stores, not its internal calls.
- Hook scripts and MCP servers are tested in their own language, under that
  language's usual runner.
- Skill, command, and agent markdown is prose and owes no test.
- The dependency surface is the plugin's runtime needs (a language runtime
  that its hooks call, an MCP server's packages) and the lowest Claude Code
  version it supports. A new one is a dependency change. A breaking change to
  a skill name, a hook contract, or a mod state key follows the universal
  deprecation policy.

## release-walk
Followed by `/cairn-release`. The tag is the release:
- Version decision (patch/minor/major) from the declared changelog.
- Changelog consolidation (the declared file): retitle the dev heading to the
  version, group entries, and prune noise.
- Bump `version` wherever it is present: in each plugin's
  `.claude-plugin/plugin.json`, including the one that each marketplace
  entry's `source` points at, and in each `.claude-plugin/marketplace.json`
  plugin entry.
- Run the verify checks. The marketplace validate shows no version warning.
- Commit the release prep to the default branch (docs/metadata only). Tag
  `v<version>` and push the tag at the user's approval.
- Where the `origin` remote is GitHub and `gh` is available, the handoff also
  provides a `gh release create` command whose body is the new changelog
  section (provided, never run).

## init-detection
Recognized by `cairn-init` when **`.claude-plugin/plugin.json`** or
**`.claude-plugin/marketplace.json`** is present at the repo root. A language
marker (`DESCRIPTION`, `pyproject.toml`, `setup.py`, `setup.cfg`) outranks
it, and it outranks a `Dockerfile`. A repo with a plugin marker and another
marker is a hybrid. cairn-init asks which deliverable is primary and
recommends the profile that the inference order picks.

## greenfield-openers
Plugin-specific openers `cairn-init` asks in a new/empty plugin repo. The
universal openers come from cairn-init's universal layer. Distribution
ambition is rendered here as the **Listing?** question below.

- **Listing?** Where do users install the plugin from?
  - Options: **a marketplace file in this repo** (reversible default) ·
    another marketplace · not listed.
  - Consequence: a marketplace file here adds the marketplace validate check
    to verify and the entry `version` bump to the release-walk.
  - Lands in: the `verify` and `release-walk` slots and DESIGN Conventions.
- **Mod?** Does the plugin ship a mod with `*.test.ts(x)` tests?
  - Options: **no** (reversible default) · yes.
  - Consequence: yes adds `claude plugin test <plugin-dir>` to verify.
  - Lands in: the `verify` slot and DESIGN Conventions.

## changelog
The repo's changelog file, read by `/hotfix`, the release-walk, and the
consistency-gate: **`CHANGELOG.md`**.
