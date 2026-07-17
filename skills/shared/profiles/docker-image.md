# Toolchain profile: docker-image

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates this into the repo's
     `cairn/PROFILE.md`. The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot here — it is the orthogonal domain axis
     (D-024/D-025), stated once in skills/shared/validation-doctrine.md
     (referenced from tracking-rules). All seven `## <slot>` sections
     are defined; cairn_validate FAILs on a missing or empty slot. -->

The container-image toolchain: a repo whose sole deliverable is a Docker image
(a base image, tool/CI image, or appliance image — no language package shipped
to a language registry). Build with `docker build`/`buildx`, lint with hadolint,
publish to a container registry (GHCR / Docker Hub). Selected by `cairn-init`
when a `Dockerfile` is the repo's only toolchain marker; a repo that also
carries a language marker goes through the disambiguation gate.

## verify
Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite). The hard
gate is lint + build; scanning is recommended-but-optional:
- After Dockerfile or build-context changes, before a task is checked off:
  `hadolint Dockerfile` clean and `docker build` succeeds.
- Recommended-but-optional (not a hard gate): a vulnerability scan
  (`trivy image` / `grype`) with no new high/critical findings, and a
  `container-structure-test` run when a structure spec exists.
- `/hotfix` gate-lite: `hadolint` clean + `docker build` succeeds; run the scan
  / structure test only if the repo already wires one.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- `docker build` succeeds from a clean context and `hadolint Dockerfile` reports
  no violations.
- The base image is pinned (a digest `@sha256:…` or explicit version tag, never
  a bare `latest`) so the build is reproducible.
- No secrets are baked into layers (no credentials/tokens in `ENV`/`COPY`);
  build secrets use `--secret`/build args, not committed files.
- A `.dockerignore` is present and excludes build-context noise (`.git`, local
  caches) — stray context is drift.
- The declared changelog (`## changelog` slot) has an entry for this milestone's
  user-visible changes (no milestone numbers in user-facing text).

## test-doctrine
Container-mechanical test expectations layered on the universal "What gets a
test" rules in tracking-rules. An image is verified by build + run + inspect,
not by unit-testing functions — the floor still holds for any scripts baked in,
but the image itself is checked at the image level:
- The image builds reproducibly and a container starts and passes its smoke
  check (the entrypoint runs, the expected process / healthcheck comes up).
- When the image's contents are the contract, assert them with
  `container-structure-test` (files present, command output, exposed ports) —
  the container analog of a snapshot test; assert the contract, not incidental
  layer details.
- A vulnerability scan (`trivy` / `grype`) is a diagnostic surfaced in CI, never
  a merge gate — the scan-optional stance mirrors the `covr`/`coverage.py`
  diagnostic framing in the language profiles.
- GitHub Actions CI: a build workflow runs `docker build` + `hadolint` on
  push/PR (a normal CI check — cairn's git model never merges red or pending
  CI); a publish workflow builds and pushes on a tag (see release-walk).
- Change governance renders here as: the dependency surface is the base image
  and the packages a layer installs (`apt-get`/`apk`/`pip` inside the
  Dockerfile) — a base-image bump or a newly installed package is a dependency
  change; a breaking change to the image's interface (entrypoint, env contract,
  exposed ports) follows the universal deprecation policy. The gates themselves
  — question-gate + D-entry for dependencies, pre-1.0 waiver — are universal
  (tracking-rules "Universal tracking rules").

## release-walk
Followed by `/cairn-release` — a container-registry release (never self-pushes):
- Version decision (patch/minor/major) from the declared changelog; pre-1.0
  conventions per DESIGN.md.
- Changelog consolidation (the declared file): retitle the dev heading to the
  version; group entries; prune noise.
- Full local verification: `hadolint` clean and `docker build` succeeds; run the
  scan / structure test if wired.
- Build the release image and tag it `v<version>` (and the moving `:latest` if
  the repo publishes one); a multi-arch repo builds with `docker buildx
  --platform`.
- Handoff checklist (user runs): `docker push <registry>/<image>:v<version>`
  (GHCR / Docker Hub / the declared registry), confirm the pushed tag, then tag
  the git commit `v<version>` and cut the GitHub release. cairn pushes nothing.

## init-detection
Recognized by `cairn-init` when a **`Dockerfile`** is present at the repo root
and it is the **only** toolchain marker — no `DESCRIPTION` and no
`pyproject.toml`/`setup.py`/`setup.cfg`. A repo carrying both a `Dockerfile` and
a language marker is a hybrid: cairn-init runs the disambiguation gate (asks
which is the primary deliverable) rather than guessing, and the `PROFILE.md`-
absent inference keeps the language marker (tracking-rules "Toolchain
profiles"). `cairn/` is not part of the build context, so add a `.dockerignore`
`cairn/` entry to keep the tracking dir out of the image.

## greenfield-openers
Language-specific openers `cairn-init` asks in a new/empty image repo. The
universal openers — distribution ambition (rendered here as **registry
intent**) and numeric-work-needs-oracle-verification — come from cairn-init's
universal layer, so they are not repeated here.

- **Registry?** Where does the image publish — GHCR, Docker Hub, or private?
  - Options: **GHCR** (reversible default) · Docker Hub · private.
  - Consequence: sets the `release-walk` push target and the CI publish
    workflow; GHCR is the reversible default (same host as the repo, no extra
    account), switchable later by changing the tag prefix.
  - Lands in: the `release-walk` push target and DESIGN Conventions.
- **Multi-arch?** Build for more than one platform (`linux/amd64` + arm64)?
  - Options: **single-arch** (reversible default) · multi-arch.
  - Consequence: multi-arch ⇒ `docker buildx` + QEMU in CI; adding a platform
    later is additive, so the reversible default is single-arch.
  - Lands in: the `verify`/`release-walk` build command and DESIGN Conventions.

## changelog
The repo's changelog file, read by `/hotfix`, the release-walk, and the
consistency-gate: **`CHANGELOG.md`**.
