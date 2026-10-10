# Toolchain profile: claude-plugin
# Copilot review: on

<!-- This repo's declared cairn toolchain profile, instantiated from
     skills/shared/profiles/claude-plugin.md at M215 (it ran generic.md
     from M46 to M215). The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot. It is the orthogonal domain axis (D-024/D-025),
     stated once in the plugin's skills/shared/validation-doctrine.md. All
     seven `## <slot>` sections are defined. cairn_validate FAILs on a
     missing, empty, or unrecognized slot. -->

This repo *is* the cairn plugin: skills, rulebook, templates, Python scripts
and hooks, and the status mod under `hooks/status/`. Its marketplace file
lists the one plugin, at the repo root.

## verify
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

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- The verify checks pass on the review head.
- The marketplace validate output has no `plugins[N].version` warning. That
  warning means the marketplace entry's `version` differs from
  `.claude-plugin/plugin.json`. At install time, `plugin.json` wins.
- The declared changelog (`## changelog` slot) has an entry for this
  milestone's user-visible changes (no milestone numbers in user-facing text).

This repo has **no CI**: `gh pr checks --watch` returns "no checks reported"
and exits 1 at once (corrected M170). Treat a PR as mergeable on local green.
Never wait for a check run that will not arrive.

## test-doctrine
Layered on the universal "What gets a test" rules in tracking-rules:
- `scripts/` and `hooks/` behavior is tested by Python stdlib `unittest`
  (the two gating suites). There is no `pytest` in this repo. Never write
  `pytest …` into an acceptance criterion. It fails "No module named pytest".
- The status mod under `hooks/status/` is tested by its `*.test.ts(x)` files
  under `claude plugin test`, which import their kit from
  `claude-code/testing`. Test what the mod draws or stores, not its internal
  calls. Its reader is held to the Python helpers by the shared fixtures
  (`scripts/tests/test_status_fixtures.py`).
- A new skill or rulebook rule owes no prose guard and no mutation
  registration in this repo. The retained
  `skills/tests` prose-guards are a hand-run tripwire that gates nothing,
  not a coverage obligation (M144, D-108/D-109). The shipped "What gets a test" doctrine
  continues to govern adopting repos. No numeric/oracle doctrine applies.
- The dependency surface is Python 3 (stdlib only) for the scripts and
  hooks, and the lowest Claude Code version the mod supports. A new one is a
  dependency change. A breaking change to a skill name, a hook contract, or
  a mod state key follows the universal deprecation policy.

## release-walk
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

## init-detection
Recognized by `cairn-init` when **`.claude-plugin/plugin.json`** or
**`.claude-plugin/marketplace.json`** is present at the repo root, as here.
A language marker (`DESCRIPTION`, `pyproject.toml`, `setup.py`, `setup.cfg`)
outranks it. This repo has none.

## greenfield-openers
Plugin-specific openers `cairn-init` asks in a new/empty plugin repo: where
users install the plugin from (a marketplace file here, another
marketplace, or not listed), and whether it ships a mod with `*.test.ts(x)`
tests. This repo is not greenfield: it answered "a marketplace file here"
and "yes".

## changelog
`CHANGELOG.md`, read by `/hotfix`, the release-walk, and the consistency-gate.
