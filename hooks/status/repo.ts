// The summary card's reads (M286): the open pull requests and open issues
// of the base remote's repo, from one `gh api graphql` call, and the latest
// release tag, its age, and the milestones done since it, from three git
// calls, and the project name (M291), from the URL or from one more git
// call when the URL is not a github.com one. `readPrs` in register.tsx
// makes them all, through `readRepo`, at the times it reads the pull
// request states, and at no other time.

import type { CairnRepoCounts, CairnRepoDone } from '../../types'

// The query `gh api graphql` runs for the repo. `totalCount` counts every
// open item, with no page limit.
export const REPO_QUERY =
  'query($owner: String!, $repo: String!) { repository(owner: $owner, name: $repo) { ' +
  'pullRequests(states: OPEN) { totalCount } issues(states: OPEN) { totalCount } } }'

// The github.com remote URL forms, each giving the owner and the repo: the
// scp-like `[user@]github.com:o/r`, `ssh://[user@]github.com[:port]/o/r`,
// and `http(s)://[userinfo@]github.com[:port]/o/r`, each with an optional
// `.git` and trailing `/`. The host matches in any case. An ssh host alias
// names no host, so it runs no call.
const REMOTE_FORMS = [
  /^(?:[^@\s/]+@)?github\.com:([^/\s]+)\/([^/\s]+?)(?:\.git)?\/?$/i,
  /^ssh:\/\/(?:[^@/\s]+@)?github\.com(?::[0-9]+)?\/([^/\s]+)\/([^/\s]+?)(?:\.git)?\/?$/i,
  /^https?:\/\/(?:[^@/\s]+@)?github\.com(?::[0-9]+)?\/([^/\s]+)\/([^/\s]+?)(?:\.git)?\/?$/i,
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

// The git argv that prints the tagged commit's time in Unix seconds. The
// release walk tags the release commit, so its time is the release's. The
// `--` keeps a path named like the tag from being read as one.
export function tagTimeArgs(tag: string): string[] {
  return ['log', '-1', '--format=%ct', tag, '--']
}

// The git argv that prints the absolute path of the repo's common git dir,
// which a linked worktree shares with its main working tree (M291).
export const COMMON_DIR_ARGS = ['rev-parse', '--path-format=absolute', '--git-common-dir']

// The last path segment of a path, split on `/` and `\`, with trailing
// separators dropped. A path with no segment, such as `/`, gives ''.
export function lastSegment(path: string): string {
  const parts = path.split(/[\\/]/).filter(part => part !== '')
  return parts.length === 0 ? '' : parts[parts.length - 1]
}

// The project name the card shows (M291) from the base remote's URL, the
// common git dir call's stdout, and the repo root. The repo part of a
// github.com URL comes first. Otherwise, when the trimmed common dir's own
// name is `.git`, the name of the folder that holds it, which is the main
// working tree's, so a linked worktree shows the repo's name. Otherwise,
// or when the call failed (null), the root's last segment. Only the last
// output line counts: a git before 2.31 echoes the unknown
// `--path-format=absolute` on a line of its own before the dir.
export function projectName(url: string | null, common: string | null, root: string): string {
  const named = url === null ? null : remoteRepo(url)
  if (named !== null) return named.repo
  const dir = (common ?? '').trim().split(/\r?\n/).pop()?.trim() ?? ''
  if (lastSegment(dir) === '.git') {
    const holder = lastSegment(dir.replace(/[\\/]*\.git[\\/]*$/, ''))
    if (holder !== '') return holder
  }
  return lastSegment(root)
}

const DAY_MS = 86_400_000

// The release read from the guest flag, the three git calls' stdout, each
// null when its call failed, and the read's start in milliseconds. Null in
// guest mode, where `cairn/` is never committed, when `git describe` failed
// or printed nothing, when the `git log` call failed or its trimmed output
// is not a whole number, and when the `git diff` call failed. The days are
// whole days from the commit's time to the read's start, rounded down, and
// 0 for a commit time after it. The count is the diff's non-blank lines.
export function doneSince(
  guest: boolean,
  describe: string | null,
  log: string | null,
  diff: string | null,
  now: number,
): CairnRepoDone | null {
  if (guest || describe === null) return null
  const tag = describe.trim()
  const seconds = log?.trim() ?? ''
  if (tag === '' || !/^\d+$/.test(seconds) || diff === null) return null
  const days = Math.max(0, Math.floor((now - Number(seconds) * 1000) / DAY_MS))
  return { tag, days, count: diff.split('\n').filter(line => line.trim() !== '').length }
}
