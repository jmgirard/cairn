# Toolchain profile: generic

<!-- This repo's declared cairn toolchain profile (instantiated from
     skills/shared/profiles/generic.md at M46). cairn is a Claude Code plugin,
     not an R package, so it runs the language-agnostic core with no R gates;
     the `verify` slot names this repo's own test command. The oracle /
     Validation doctrine is UNIVERSAL and deliberately NOT a slot — it is the
     orthogonal domain axis (D-024/D-025), stated once in the plugin's
     skills/shared/validation-doctrine.md (referenced from tracking-rules). All
     seven `## <slot>` sections are defined; cairn_validate FAILs on a missing,
     empty, or unrecognized slot. -->

The language-agnostic default: cairn's core with no toolchain-specific gates.
This repo *is* the cairn plugin (skills, rulebook, templates, scripts, hooks),
tested by Python stdlib `unittest`, so the R-package gates do not apply.

## verify
The command(s) `/milestone-implement` (per task) and `/hotfix` (gate-lite) run
to check work before it is checked off. This repo is tested by three stdlib
`unittest` suites — all three must be green:

```
python3 -m unittest discover -s skills/tests
python3 -m unittest discover -s scripts/tests
python3 -m unittest discover -s hooks/tests
```

Run them from the repo root. `skills/tests` must go through `discover`, never a
dotted module name: the mutation harness does a bare `import mutation_engine`,
so `python3 -m unittest skills.tests.test_mutation_harness` dies
`ModuleNotFoundError`. The `scripts` and `hooks` suites take a dotted path
fine (`python3 -m unittest scripts.tests.test_scripts -k <sub>`). To narrow a
`discover` run, add `-k <substring>`.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`).
Generic default: **none** — the universal cairn-file checks are the whole
consistency gate. (The `verify` suites are re-run at review via the
acceptance-criteria evidence step, so no separate toolchain check is needed.)

This repo has **no CI**: `gh pr checks --watch` returns "no checks reported"
and exits 0. Treat a PR as mergeable on local green; never wait for a check
run that will not arrive.

## test-doctrine
Toolchain-specific test expectations layered on the universal "What gets a
test" rules in tracking-rules. This repo: guard tests are Python stdlib
`unittest` over the skills/rulebook prose (single-line asserted phrases; steer
clear of `**bold**` splits) and the scripts/hooks behavior. No numeric/oracle
doctrine applies here. There is no `pytest` in this repo — never write
`pytest …` into an acceptance criterion; it fails "No module named pytest".
Nothing beyond the universal rules otherwise.

## release-walk
The release procedure `/cairn-release` follows. Generic default: a minimal
language-agnostic walk — no package-registry submission; the tag is the release:
- Decide the version bump (patch/minor/major) from the declared changelog
  (`## changelog` slot).
- Consolidate the declared changelog: retitle the dev heading to the version,
  group entries, prune noise.
- Bump the repo's version marker and commit the release prep to the default
  branch (docs/metadata only).
- Tag `v<version>` and push the tag at the user's approval — no registry step.

## init-detection
How `cairn-init` recognizes this toolchain. Generic is the **fallback**: no
`DESCRIPTION` and no other recognized toolchain marker.

## greenfield-openers
Opener questions `cairn-init` asks in a new/empty repo of this type. Generic
default: **none** — the greenfield opener flow is a downstream candidate; this
slot is a declared placeholder until it ships.

## changelog
`CHANGELOG.md` — read by `/hotfix`, the release-walk, and the consistency-gate.
