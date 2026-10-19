// The summary card's reads (M286): the open pull requests and open issues
// of the base remote's repo, from one `gh api graphql` call, and the
// milestones done since the latest release, from two git calls. `readPrs`
// in register.tsx makes all three, at the times it reads the pull request
// states, and at no other time.

import type { CairnRepoCounts, CairnRepoDone } from '../../types'

// The query `gh api graphql` runs for the repo. `totalCount` counts every
// open item, with no page limit.
export const REPO_QUERY =
  'query($owner: String!, $repo: String!) { repository(owner: $owner, name: $repo) { ' +
  'pullRequests(states: OPEN) { totalCount } issues(states: OPEN) { totalCount } } }'

// The github.com remote URL forms, each giving the owner and the repo: the
// scp-like `git@github.com:o/r`, `ssh://[user@]github.com[:port]/o/r`, and
// `http(s)://[userinfo@]github.com/o/r`, each with an optional `.git` and
// trailing `/`. The host matches in any case.
const REMOTE_FORMS = [
  /^[^@\s/]+@github\.com:([^/\s]+)\/([^/\s]+?)(?:\.git)?\/?$/i,
  /^ssh:\/\/(?:[^@/\s]+@)?github\.com(?::[0-9]+)?\/([^/\s]+)\/([^/\s]+?)(?:\.git)?\/?$/i,
  /^https?:\/\/(?:[^@/\s]+@)?github\.com\/([^/\s]+)\/([^/\s]+?)(?:\.git)?\/?$/i,
]

// The owner and repo of a github.com remote URL, or null for any other URL.
export function remoteRepo(url: string): { owner: string; repo: string } | null {
  for (const form of REMOTE_FORMS) {
    const match = form.exec(url)
    if (match !== null) return { owner: match[1], repo: match[2] }
  }
  return null
}

// The `gh api graphql` argv for a base remote URL, or null for a URL that
// is not a github.com one, which runs no call. The argv holds only the
// owner and the repo from the URL, so no userinfo reaches it. It names
// `--hostname github.com`, as `countsArgv` in counts.ts does.
export function repoArgv(url: string): string[] | null {
  const named = remoteRepo(url)
  if (named === null) return null
  return [
    'gh',
    'api',
    'graphql',
    '--hostname',
    'github.com',
    '-f',
    `query=${REPO_QUERY}`,
    '-f',
    `owner=${named.owner}`,
    '-f',
    `repo=${named.repo}`,
  ]
}

const isObject = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value)

// A connection's `totalCount`, or null when it is not an integer.
function totalOf(value: unknown): number | null {
  if (!isObject(value)) return null
  const total = value.totalCount
  return typeof total === 'number' && Number.isInteger(total) ? total : null
}

// The two numbers of one call, whose result is null when the call rejected.
// A rejected call, a non-zero exit, text that is not JSON, a reply without
// one or both counts, or a count that is not an integer gives null.
export function repoCounts(result: { exitCode: number; stdout: string } | null): CairnRepoCounts | null {
  if (result === null || result.exitCode !== 0) return null
  let reply: unknown
  try {
    reply = JSON.parse(result.stdout)
  } catch {
    return null
  }
  if (!isObject(reply) || !isObject(reply.data) || !isObject(reply.data.repository)) return null
  const prs = totalOf(reply.data.repository.pullRequests)
  const issues = totalOf(reply.data.repository.issues)
  return prs === null || issues === null ? null : { prs, issues }
}

// The git argv that names the latest release tag: the newest `v*` tag that
// `git describe` reaches from HEAD.
export const DESCRIBE_ARGS = ['describe', '--tags', '--abbrev=0', '--match', 'v*']

// The git argv that lists the milestone files archived since a tag.
// `--no-renames` lists a file moved into the archive as added, so a file
// planned before the tag counts, and the pathspec keeps the root archive
// only, not a fixture tree that holds one.
export function archivedArgs(tag: string): string[] {
  return ['diff', '--no-renames', '--diff-filter=A', '--name-only', tag, 'HEAD', '--', 'cairn/milestones/archive/']
}

// The done count from the guest flag and the two git calls' stdout, each
// null when its call failed. Null in guest mode, where `cairn/` is never
// committed, when `git describe` failed or printed nothing, and when the
// `git diff` call failed. The count is the diff's lines that are not blank.
export function doneSince(guest: boolean, describe: string | null, diff: string | null): CairnRepoDone | null {
  if (guest || describe === null) return null
  const tag = describe.trim()
  if (tag === '' || diff === null) return null
  return { tag, count: diff.split('\n').filter(line => line.trim() !== '').length }
}
