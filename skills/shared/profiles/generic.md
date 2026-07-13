# Toolchain profile: generic

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates the chosen reference
     profile into the repo's `cairn/PROFILE.md`. The oracle / Validation
     doctrine is UNIVERSAL and deliberately NOT a slot here — it is the
     orthogonal domain axis (D-024/D-025), stated once in tracking-rules.
     Every profile defines all six `## <slot>` sections below; a slot with no
     toolchain-specific content says so explicitly rather than being omitted
     (cairn_validate FAILs on a missing or empty slot). -->

The language-agnostic default: cairn's core with no toolchain-specific gates.
Selected by `cairn-init` when no `DESCRIPTION` (or other recognized toolchain
marker) is present. A repo replaces the placeholder in `verify` with its own
test command; the other slots stand as-is until a richer profile is authored.

## verify
The command(s) `/milestone-implement` and `/hotfix` run to check a task before
ticking it off. Generic default: **the repo's own test command** — declare it
here (e.g. `make test`, `npm test`, `pytest`). If the repo has none, state
"no automated verify" and rely on the acceptance-criteria evidence.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`).
Generic default: **none** — the universal cairn-file checks are the whole
consistency gate.

## test-doctrine
Toolchain-specific test expectations layered on the universal "What gets a
test" rules in tracking-rules. Generic default: **none beyond the universal
rules** — every bug fix gets a regression test, every documented claim a test,
contract-not-implementation, and the oracle doctrine for any numeric result.

## release-walk
The release procedure `/cairn-release` follows. Generic default: a minimal
language-agnostic walk — no package-registry submission; the tag is the release:
- Decide the version bump (patch/minor/major) from the changelog/NEWS.
- Consolidate the changelog/NEWS: retitle the dev heading to the version,
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
