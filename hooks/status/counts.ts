// The two counts under an open handed-off pull request's blocked line
// (M225): its unresolved review threads, and the reviews and conversation
// comments from others that are newer than the anchor. The anchor is the
// latest of the author's newest submitted review, the author's newest
// conversation comment, and the committed date of the pull request's newest
// commit, whoever made it. GitHub links no reply to a review or a
// conversation comment, so the anchor stands in for "answered": the
// author's comment or review, or a newer commit, clears every earlier item. Bots are others, so a Copilot review
// counts, and its threads count too. Each kind is read `last: 100`, so the
// counts cover the newest 100 of each.

export type PrCounts = { unresolved: number; unanswered: number }

// One review, conversation comment, and thread as the query returns them.
// A null author is a deleted account, read as another person.
type Author = { login: string } | null
type Review = { author: Author; state: string; submittedAt: string | null }
type Comment = { author: Author; createdAt: string }
export type PrNodes = {
  author: string
  threads: { isResolved: boolean }[]
  reviews: Review[]
  comments: Comment[]
  commit: string | null
}

// The query `gh api graphql` runs for one pull request.
export const COUNTS_QUERY =
  'query($owner: String!, $repo: String!, $number: Int!) { repository(owner: $owner, name: $repo) { pullRequest(number: $number) { ' +
  'author { login } reviewThreads(last: 100) { nodes { isResolved } } ' +
  'reviews(last: 100) { nodes { author { login } state submittedAt } } ' +
  'comments(last: 100) { nodes { author { login } createdAt } } ' +
  'commits(last: 1) { nodes { commit { committedDate } } } } } }'

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

// The review states that count and that set the anchor. APPROVED,
// DISMISSED, and PENDING do neither.
const COUNTED = ['COMMENTED', 'CHANGES_REQUESTED']

// Both counts from the returned nodes. Times are GitHub's ISO-8601 UTC
// strings, compared as text, and an item counts only when strictly later
// than the anchor. A review with no `submittedAt` neither counts nor sets
// the anchor.
export function countPr(pr: PrNodes): PrCounts {
  const mine = (author: Author) => author !== null && author.login === pr.author
  const reviews = pr.reviews.filter(r => COUNTED.includes(r.state) && r.submittedAt !== null)
  let anchor = pr.commit ?? ''
  for (const r of reviews) if (mine(r.author) && (r.submittedAt as string) > anchor) anchor = r.submittedAt as string
  for (const c of pr.comments) if (mine(c.author) && c.createdAt > anchor) anchor = c.createdAt
  const unanswered =
    reviews.filter(r => !mine(r.author) && (r.submittedAt as string) > anchor).length +
    pr.comments.filter(c => !mine(c.author) && c.createdAt > anchor).length
  return { unresolved: pr.threads.filter(t => !t.isResolved).length, unanswered }
}

const isObject = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value)

// A node's author: null, or an object with a string login. Anything else
// fails the shape check (undefined).
function authorOf(value: unknown): Author | undefined {
  if (value === null) return null
  if (isObject(value) && typeof value.login === 'string') return { login: value.login }
  return undefined
}

// A connection's `nodes` list, or undefined when it is not a list of objects.
function nodesOf(value: unknown): Record<string, unknown>[] | undefined {
  if (!isObject(value) || !Array.isArray(value.nodes) || !value.nodes.every(isObject)) return undefined
  return value.nodes as Record<string, unknown>[]
}

// The nodes of a `gh api graphql` reply, or null when the reply fails the
// shape check: a null `pullRequest` or PR author, a connection that is not
// a list, or a node with a field of the wrong type.
export function prNodes(reply: unknown): PrNodes | null {
  if (!isObject(reply) || !isObject(reply.data) || !isObject(reply.data.repository)) return null
  const pr = reply.data.repository.pullRequest
  if (!isObject(pr)) return null
  const author = authorOf(pr.author)
  if (author === null || author === undefined) return null
  const threads = nodesOf(pr.reviewThreads)
  const reviews = nodesOf(pr.reviews)
  const comments = nodesOf(pr.comments)
  const commits = nodesOf(pr.commits)
  if (threads === undefined || reviews === undefined || comments === undefined || commits === undefined) return null
  const out: PrNodes = { author: author.login, threads: [], reviews: [], comments: [], commit: null }
  for (const t of threads) {
    if (typeof t.isResolved !== 'boolean') return null
    out.threads.push({ isResolved: t.isResolved })
  }
  for (const r of reviews) {
    const by = authorOf(r.author)
    if (by === undefined || typeof r.state !== 'string') return null
    if (r.submittedAt !== null && typeof r.submittedAt !== 'string') return null
    out.reviews.push({ author: by, state: r.state, submittedAt: r.submittedAt as string | null })
  }
  for (const c of comments) {
    const by = authorOf(c.author)
    if (by === undefined || typeof c.createdAt !== 'string') return null
    out.comments.push({ author: by, createdAt: c.createdAt })
  }
  for (const c of commits) {
    if (!isObject(c.commit) || typeof c.commit.committedDate !== 'string') return null
    if (out.commit === null || c.commit.committedDate > out.commit) out.commit = c.commit.committedDate
  }
  return out
}

// The counts from one `gh api graphql` call, null for a read that failed:
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
