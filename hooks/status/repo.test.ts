import { describe, expect, test } from 'claude-code/testing'

import { archivedArgs, DESCRIBE_ARGS, doneSince, REPO_QUERY, repoArgv, repoCounts } from './repo'

// The summary card's reads (M286 AC3, AC4). The expected values are written
// out by hand.

const argOf = (argv: readonly string[], name: string) => argv.find(a => a.startsWith(`${name}=`))?.slice(name.length + 1)
const ok = (value: unknown) => ({ exitCode: 0, stdout: `${JSON.stringify(value)}\n` })
const reply = (pullRequests: unknown, issues: unknown) => ({ data: { repository: { pullRequests, issues } } })

describe('the repo query names only the owner and repo of a github.com remote (M286 AC3)', () => {
  const FORMS: [string, string][] = [
    ['scp-like SSH with .git', 'git@github.com:o/r.git'],
    ['ssh:// with a user and no .git', 'ssh://git@github.com/o/r'],
    ['HTTPS with userinfo', 'https://user:tok@github.com/o/r'],
    ['HTTPS with .git and a trailing slash', 'https://github.com/o/r.git/'],
  ]
  for (const [name, url] of FORMS) {
    test(name, () => {
      const argv = repoArgv(url)
      expect(argv).toEqual([
        'gh',
        'api',
        'graphql',
        '--hostname',
        'github.com',
        '-f',
        `query=${REPO_QUERY}`,
        '-f',
        'owner=o',
        '-f',
        'repo=r',
      ])
      // No userinfo, scheme, or host from the URL reaches the argv.
      expect((argv ?? []).some(a => a.includes('tok') || a.includes('user') || a.includes('@'))).toBe(false)
      expect([argOf(argv ?? [], 'owner'), argOf(argv ?? [], 'repo')]).toEqual(['o', 'r'])
    })
  }

  for (const url of ['https://gitlab.com/o/r.git', 'git@example.com:o/r.git', 'ssh://git@github.example.com/o/r', '/a/local/path', '']) {
    test(`no call for ${url === '' ? 'an empty URL' : url}`, () => {
      expect(repoArgv(url)).toBe(null)
    })
  }

  test('the query counts open pull requests and open issues', () => {
    expect(REPO_QUERY).toContain('pullRequests(states: OPEN) { totalCount }')
    expect(REPO_QUERY).toContain('issues(states: OPEN) { totalCount }')
  })
})

describe('the parser gives both numbers or none (M286 AC3)', () => {
  test('a reply with both counts as integers gives both', () => {
    expect(repoCounts(ok(reply({ totalCount: 3 }, { totalCount: 12 })))).toEqual({ prs: 3, issues: 12 })
    expect(repoCounts(ok(reply({ totalCount: 0 }, { totalCount: 0 })))).toEqual({ prs: 0, issues: 0 })
  })

  const FAILS: [string, { exitCode: number; stdout: string } | null][] = [
    ['a rejected call', null],
    ['a non-zero exit', { exitCode: 1, stdout: `${JSON.stringify(reply({ totalCount: 3 }, { totalCount: 12 }))}\n` }],
    ['text that is not JSON', { exitCode: 0, stdout: 'HTTP 502\n' }],
    ['a reply without the PR count', ok(reply(undefined, { totalCount: 12 }))],
    ['a reply without the issue count', ok(reply({ totalCount: 3 }, undefined))],
    ['a reply without both counts', ok(reply({}, {}))],
    ['a reply with no repository', ok({ data: { repository: null } })],
    ['a PR count that is not an integer', ok(reply({ totalCount: 2.5 }, { totalCount: 12 }))],
    ['an issue count that is a string', ok(reply({ totalCount: 3 }, { totalCount: '12' }))],
  ]
  for (const [name, result] of FAILS) {
    test(`${name} gives none`, () => {
      expect(repoCounts(result)).toBe(null)
    })
  }
})

describe('the done count is the archive files added since the latest v* tag (M286 AC4)', () => {
  test('the git argv: describe the newest v* tag, then list archive files added since it, renames off', () => {
    expect(DESCRIBE_ARGS).toEqual(['describe', '--tags', '--abbrev=0', '--match', 'v*'])
    expect(archivedArgs('v2.1.0')).toEqual([
      'diff',
      '--no-renames',
      '--diff-filter=A',
      '--name-only',
      'v2.1.0',
      'HEAD',
      '--',
      'cairn/milestones/archive/',
    ])
  })

  test('a count: each listed file, blank lines not counted', () => {
    const diff = 'cairn/milestones/archive/M284-a.md\ncairn/milestones/archive/M285-b.md\n\n'
    expect(doneSince(false, 'v2.1.0\n', diff)).toEqual({ tag: 'v2.1.0', count: 2 })
    expect(doneSince(false, 'v2.1.0\n', '')).toEqual({ tag: 'v2.1.0', count: 0 })
  })

  test('git describe failing gives none', () => {
    expect(doneSince(false, null, 'cairn/milestones/archive/M1.md\n')).toBe(null)
  })

  test('git describe printing nothing gives none', () => {
    expect(doneSince(false, '\n', 'cairn/milestones/archive/M1.md\n')).toBe(null)
  })

  test('a failed diff gives none', () => {
    expect(doneSince(false, 'v1.0.0\n', null)).toBe(null)
  })

  test('guest mode gives none', () => {
    expect(doneSince(true, 'v1.0.0\n', 'cairn/milestones/archive/M1.md\n')).toBe(null)
  })
})
