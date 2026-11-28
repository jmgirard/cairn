# Profile

## Verify

Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite). Two
stdlib `unittest` suites test the Python scripts and hooks, and three
`claude plugin` checks cover the manifests and the mod. The plugin validate
and the mod test gate since M191 (D-143), the marketplace validate since
M215. All five must be green:

```
python3 -m unittest discover -s scripts/tests
python3 -m unittest discover -s hooks/tests
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .
```

Run them from the repo root and check each exit code explicitly. Both suites
take a dotted path fine (`python3 -m unittest scripts.tests.test_scripts -k <sub>`);
to narrow a `discover` run, add `-k <substring>`. The validate checks pass
with warnings and fail on any error. Do not add `--strict`: it fails on
warnings, and the root `CLAUDE.md` always draws one. `claude plugin test .`
runs every `*.test.ts(x)` file under the repo root, today only the status
mod's under `hooks/status/`. Keep tests for other runners (vitest, jest) out
of the repo, because this command runs them too. Without the
variable, a process that the rollout switch serves "off" refuses to run them
with "hooks modules are turned off in this process" (M191, observed on
2.1.286).

A desktop app shell has no `claude` on its PATH. The app keeps one binary
per version under `~/Library/Application Support/Claude/claude-code/<version>/<hash>/claude.app/Contents/MacOS/claude`.
Use the newest version's binary. The `claude-code-vm/<version>/claude` file beside
it is a Linux binary for the app's VM and does not run on the Mac.

Non-gating: `skills/tests`, the prose-guard suite over the skills/rulebook
markdown, gates nothing: no commit, merge, or check-off waits on it (M144,
D-109, which also holds the falsifier that re-arms it). It stays in
the repo and is run by hand when wanted: `python3 -m unittest discover -s
skills/tests`. It must go through `discover`, never a dotted module name: the
mutation harness does a bare `import mutation_engine`, so `python3 -m
unittest skills.tests.test_mutation_harness` dies `ModuleNotFoundError`.

Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- The verify checks pass on the review head.
- The marketplace validate output has no `plugins[N].version` warning. That
  warning means the marketplace entry's `version` differs from
  `.claude-plugin/plugin.json`. At install time, `plugin.json` wins.
- The declared changelog (`## changelog` slot) has an entry for this
  milestone's user-visible changes (no milestone numbers in user-facing text).
  A feature series milestone (its work log carries a `feature series:` line; tracking-rules "Feature series") may instead edit
  the series' existing entry, and one before the series' last with no user-visible change needs no entry.

This repo has **no CI**: `gh pr checks --watch` returns "no checks reported"
and exits 1 at once (corrected M170). Treat a PR as mergeable on local green.
Never wait for a check run that will not arrive.

## Changelog

`CHANGELOG.md`, read by `/hotfix`, the release-walk, and the consistency-gate.

## Release

Followed by `/cairn-release`. The tag is the release:
- Version decision (patch/minor/major) from the declared changelog.
- Changelog consolidation (the declared file): retitle the dev heading to the
  version, group entries, and prune noise.
- Bump `version` in `.claude-plugin/plugin.json` and in the plugin entry of
  `.claude-plugin/marketplace.json`.
- Run the verify checks. The marketplace validate shows no version warning.
- Commit the release prep to the default branch (docs/metadata only). Tag
  `v<version>` and push the tag at the user's approval.
- The handoff also provides a `gh release create` command whose body is the
  new changelog section (provided, never run).
