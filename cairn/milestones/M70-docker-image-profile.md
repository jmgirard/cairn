<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M70: Docker-image toolchain profile

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m70-docker-image-profile   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Ship a fourth toolchain profile, `docker-image`, for repos whose sole
deliverable is a container image — its seven slots plus the init-detection,
inference, count-claim, greenfield-chip, and shipped-profile-test wiring.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- `skills/shared/profiles/docker-image.md` — all seven slots, under the 120-line
  PROFILE cap. `verify` = `hadolint` + `docker build` as the hard gate, with a
  vulnerability scan (trivy/grype) + container-structure-test named
  recommended-but-optional. `release-walk` = tag, `buildx`/`docker build`,
  `docker push` to a container registry (GHCR / Docker Hub), self-submits
  nothing. `changelog` = `CHANGELOG.md`.
- init-detection wiring in `skills/cairn-init/SKILL.md`: `Dockerfile` as the
  sole toolchain marker → `docker-image`; `Dockerfile` **plus** a language
  marker (`DESCRIPTION` / `pyproject.toml` / `setup.py` / `setup.cfg`) → a
  **disambiguation gate** asking which is the primary deliverable (cairn-init
  only, where a user is present); language marker without a Dockerfile →
  precedence unchanged. Add a fourth greenfield project-type chip option
  ("Docker image").
- Inference-fallback update in `tracking-rules.md` "Toolchain profiles": absent
  `PROFILE.md`, no user → deterministic order `DESCRIPTION` → `pyproject`/
  `setup` → `Dockerfile`-only → `generic`; when both a Dockerfile and a
  language marker are present at inference time the **language marker wins**
  (back-compat: a pre-profile repo shipping a Dockerfile beside `pyproject`
  still infers `python`). The disambiguation gate is cairn-init-only.
- Bump every "three profiles ship" count-claim to four naming `docker-image`:
  `DESIGN.md` (Purpose & Scope + Architecture) and `tracking-rules.md`
  "Toolchain profiles".

**Out:**
- Docker Compose / multi-image repos — this profile targets a single-image
  deliverable; multi-image orchestration → a new candidate row if it ever bites.
- Making trivy / container-structure-test **mandatory** — deliberately optional
  per the M70 plan gate; tightening the gate → a future milestone if adopters
  ask.
- Multi-arch platform / registry auto-selection — lives in the profile's
  `greenfield-openers` slot + DESIGN Conventions, not init-detection.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `skills/shared/profiles/docker-image.md` exists and defines exactly
      the seven known slots, each non-empty (the same schema `cairn_validate`
      enforces on a repo `PROFILE.md`).
- [ ] AC2 — its `verify` slot names `hadolint` and `docker build` as the hard
      gate and names a vulnerability scan (trivy/grype) + container-structure-test
      as recommended-but-optional (not mandatory).
- [ ] AC3 — its `release-walk` slot targets a container registry (`docker push`,
      GHCR/Docker Hub) and self-submits nothing (parity with r-package/python).
- [ ] AC4 — init-detection classifies: Dockerfile-only → `docker-image`;
      Dockerfile + a language marker → a disambiguation gate (cairn-init only);
      language marker without Dockerfile → unchanged. The inference fallback
      (`PROFILE.md` absent) deterministically keeps the language marker when
      both are present.
- [ ] AC5 — the greenfield project-type chip offers a Docker-image option (≤4
      options total).
- [ ] AC6 — every "three profiles ship" count-claim (`DESIGN.md`,
      `tracking-rules.md`) reads "four" and names `docker-image`, and the
      shipped-profile test enumeration includes `docker-image` so the real
      validator (`test_shipped_reference_profiles_are_valid`) exercises it.
- [ ] AC7 — the `generic` profile carries no docker toolchain tokens (negative
      parity with the r/python no-bleed tests); new prose-guards are
      mutation-registered (`test_mutation_harness.py`).
- [ ] AC8 — the `verify` slot is clean: all three stdlib `unittest` suites
      (`skills/tests`, `scripts/tests`, `hooks/tests`) green.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. Review reads to fence evidence. -->

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T2, T3
- AC5 → T2
- AC6 → T1, T3, T4
- AC7 → T1
- AC8 → T1, T2, T3, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Author `skills/shared/profiles/docker-image.md` (seven slots, per
      Scope), and ship its guards in the same commit: extend
      `test_toolchain_profiles.py`'s shipped-profile tuple + the
      `test_shipped_reference_profiles_are_valid` iteration to include
      `docker-image`; add a docker-token positive test and a generic-no-docker
      negative test; mutation-register the new prose-guards. Suite green.
- [x] T2 — Wire init-detection in `skills/cairn-init/SKILL.md` (Dockerfile-only
      → docker-image; Dockerfile + language marker → disambiguation gate) and
      add the fourth greenfield project-type chip option; ship the gate-wording
      guard in cairn-init's test file, mutation-registered. Suite green.
- [x] T3 — Update the inference fallback + "three→four" count-claim in
      `tracking-rules.md` "Toolchain profiles" (deterministic language-wins at
      inference), with its guard update. Suite green.
- [x] T4 — Bump the `DESIGN.md` count-claims (Purpose & Scope + Architecture)
      to four naming `docker-image`; update any DESIGN-count guard. Suite green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-17: created by /milestone-plan.
- 2026-07-17: T1 — authored docker-image.md (113 lines, <120 cap); extended both shipped-profile enumeration tuples (test_toolchain_profiles + test_scripts); added TestDockerImageProfile + 2 mutation registrations. All three suites green (227/96/55).
- 2026-07-17: T2 — cairn-init init-detection: Dockerfile-only → docker-image, Dockerfile+language-marker → disambiguation gate; greenfield project-type chip gains a Docker-image option; repair backfill keeps language marker on a hybrid. Guard + mutation added; caught the M59 reflow trap (anchor phrase wrapped mid-line, reflowed). Suites green.
- 2026-07-17: T3 — tracking-rules "Toolchain profiles": three→four profiles, inference order gains a Dockerfile-sole-marker branch (language ranks first at inference). Renamed the guard class Three→Four, added order+count asserts and a "Four profiles ship" mutation. Suites green.
- 2026-07-17: T4 — DESIGN.md count-claims (Purpose & Scope + Architecture) bumped three→four naming docker-image. All tasks done; status → review. All three suites green; validate clean (only the justified 8-AC sizing advisory).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->
