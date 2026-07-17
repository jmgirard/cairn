# M70: Docker-image toolchain profile — done 2026-07-17

Goal: a fourth toolchain profile, `docker-image`, for repos whose sole
deliverable is a container image.

Outcome: shipped `skills/shared/profiles/docker-image.md` (seven slots —
hadolint + `docker build` verify with optional trivy/structure-test scan, a
container-registry release-walk that self-pushes nothing, CHANGELOG.md). Wired
init-detection in cairn-init (Dockerfile-only → docker-image; Dockerfile + a
language marker → a disambiguation gate; greenfield chip gains a Docker-image
option), the tracking-rules inference fallback (a Dockerfile-sole-marker branch,
language markers ranking first so a hybrid keeps its language marker at
inference, no user present), and the three→four count-claims (DESIGN ×2,
tracking-rules). Guards: TestDockerImageProfile, docker init-detection test,
Three→Four rulebook class, both shipped-profile enumeration tuples, 4 mutation
registrations.

Decisions: none promoted (works under GP3; no principle text changed). At the
plan gate: disambiguation gate over language-wins; verify kept lint+build with
optional scan; repos confirmed pure-image.

Review (PR #68): 8/8 AC verified fresh; 3 suites green (229/96/55); validate
clean (justified 8-AC sizing advisory). Fan-out F1 (scored 90, fixed): the
profile's consistency-gate wrongly blessed `--build-arg` for secrets → BuildKit
`--secret` mounts only. Blame-history clean; no prior-PR evidence.
