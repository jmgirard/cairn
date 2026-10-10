// The count under an open handed-off pull request's line (M225): its
// review threads not marked resolved. A thread opened by a bot, such as
// Copilot, counts too. Until M236 a second count showed the reviews and
// conversation comments that came after the author's last comment, review,
// or commit. It was dropped because GitHub links no reply to a review, so it
// counted items that had nothing to answer, such as a Copilot summary review
// with no threads. The threads are read `last: 100`, so the count covers the
// newest 100.

import type { CairnPrRead } from '../../types'

// The counts as the state contract holds them.
export type PrCounts = NonNullable<CairnPrRead['counts']>

// The threads as the query returns them.
export type PrNodes = { threads: { isResolved: boolean }[] }

// The query `gh api graphql` runs for one pull request.
export const COUNTS_QUERY =
  'query($owner: String!, $repo: String!, $number: Int!) { repository(owner: $owner, name: $repo) { pullRequest(number: $number) { ' +
  'reviewThreads(last: 100) { nodes { isResolved } } } } }'

// The URL `prUrl` in reader.ts keeps: owner, repo, and number.
const URL = /^https:\/\/github\.com\/([^/ \t]+)\/([^/ \t]+)\/pull\/([0-9]{1,15})$/

// The `gh api graphql` argv for a pull request URL, null for a URL of
// another form. The owner and repo go as strings (`-f`) and the number as
// an Int (`-F`), so an owner named like a number stays a string.
export function countsArgv(url: string): string[] | null {
  const match = URL.exec(url)
  if (match === null) return null
  const [, owner, repo, number] = match
  return ['gh', 'api', 'graphql', '-f', `query=${COUNTS_QUERY}`, '-f', `owner=${owner}`, '-f', `repo=${repo}`, '-F', `number=${number}`]
}

// The count from the returned nodes.
export function countPr(pr: PrNodes): PrCounts {
  return { unresolved: pr.threads.filter(t => !t.isResolved).length }
}

const isObject = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value)

// A connection's `nodes` list, or undefined when it is not a list of objects.
function nodesOf(value: unknown): Record<string, unknown>[] | undefined {
  if (!isObject(value) || !Array.isArray(value.nodes) || !value.nodes.every(isObject)) return undefined
  return value.nodes as Record<string, unknown>[]
}

// The nodes of a `gh api graphql` reply, or null when the reply fails the
// shape check: a null `pullRequest`, threads that are not a list, or a
// thread whose `isResolved` is not a boolean.
export function prNodes(reply: unknown): PrNodes | null {
  if (!isObject(reply) || !isObject(reply.data) || !isObject(reply.data.repository)) return null
  const pr = reply.data.repository.pullRequest
  if (!isObject(pr)) return null
  const threads = nodesOf(pr.reviewThreads)
  if (threads === undefined) return null
  const out: PrNodes = { threads: [] }
  for (const t of threads) {
    if (typeof t.isResolved !== 'boolean') return null
    out.threads.push({ isResolved: t.isResolved })
  }
  return out
}

// The count from one `gh api graphql` call, null for a read that failed:
// a call that rejected, a non-zero exit, text that is not JSON, or a reply
// that fails the shape check.
export function prCounts(result: { exitCode: number; stdout: string } | null): PrCounts | null {
  if (result === null || result.exitCode !== 0) return null
  let reply: unknown
  try {
    reply = JSON.parse(result.stdout)
  } catch {
    return null
  }
  const nodes = prNodes(reply)
  return nodes === null ? null : countPr(nodes)
}
