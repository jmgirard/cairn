import { describe, expect, test } from 'claude-code/testing'

import { archivedArgs, DESCRIBE_ARGS, doneSince, lastSegment, projectName, REPO_QUERY, repoArgv, repoCounts, tagTimeArgs } from './repo'

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
    // M286 review: a port, an upper-case host, and scp-like with no user.
    ['HTTPS with a port', 'https://github.com:443/o/r'],
    ['ssh:// with a port and upper-case host', 'ssh://git@GitHub.com:22/o/r.git'],
    ['scp-like with no user', 'github.com:o/r.git'],
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

describe('the release read: the latest v* tag, the days since its commit, and the archive files added since it (M286 AC4)', () => {
  // The read's start and the commit times, in whole seconds, written out by
  // hand.
  const NOW_S = 1_800_000_000
  const NOW = NOW_S * 1000
  const DAY = 86_400
  const DIFF = 'cairn/milestones/archive/M284-a.md\ncairn/milestones/archive/M285-b.md\n'
  const at = (seconds: number) => `${seconds}\n`

  test('the git argv: describe the newest v* tag, the commit time, and archive files added, renames off', () => {
    expect(DESCRIBE_ARGS).toEqual(['describe', '--tags', '--abbrev=0', '--match', 'v*'])
    expect(tagTimeArgs('v2.1.0')).toEqual(['log', '-1', '--format=%ct', 'v2.1.0', '--'])
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

  const GOOD: [string, string | null, number | null][] = [
    ['29 days 23 hours rounds down to 29', at(NOW_S - 29 * DAY - 23 * 3600), 29],
    ['exactly 30 days is 30', at(NOW_S - 30 * DAY), 30],
    ['one day', at(NOW_S - DAY - 60), 1],
    ['a commit time after the read is 0', at(NOW_S + 3600), 0],
    ['git log output without a trailing newline', `${NOW_S - 2 * DAY}`, 2],
  ]
  for (const [name, log, days] of GOOD) {
    test(name, () => {
      expect(doneSince(false, 'v2.1.0\n', log, DIFF, NOW)).toEqual({ tag: 'v2.1.0', days, count: 2 })
    })
  }

  test('a describe output with a trailing newline gives the trimmed tag', () => {
    expect(doneSince(false, '  v1.0.0\n', at(NOW_S), DIFF, NOW)?.tag).toBe('v1.0.0')
  })

  test('a diff that prints nothing counts 0, and a blank line does not count', () => {
    expect(doneSince(false, 'v2.1.0\n', at(NOW_S), '', NOW)?.count).toBe(0)
    expect(doneSince(false, 'v2.1.0\n', at(NOW_S), `${DIFF}\n  \n`, NOW)?.count).toBe(2)
  })

  const NONE: [string, boolean, string | null, string | null, string | null][] = [
    ['git describe failing', false, null, at(NOW_S), DIFF],
    ['git describe printing nothing', false, '\n', at(NOW_S), DIFF],
    ['a failed git log', false, 'v2.1.0\n', null, DIFF],
    ['a git log that is not a whole number', false, 'v2.1.0\n', '17.5\n', DIFF],
    ['a git log that prints a word', false, 'v2.1.0\n', 'fatal\n', DIFF],
    ['a failed diff', false, 'v2.1.0\n', at(NOW_S), null],
    ['guest mode', true, 'v2.1.0\n', at(NOW_S), DIFF],
  ]
  for (const [name, guest, describe, log, diff] of NONE) {
    test(`${name} gives none`, () => {
      expect(doneSince(guest, describe, log, diff, NOW)).toBe(null)
    })
  }
})

describe('the project name: the github.com repo, else the main tree folder, else the root folder (M291 AC2)', () => {
  const CASES: [string, string | null, string | null, string, string][] = [
    ['a github.com URL', 'git@github.com:o/alpha.git', '/work/x/.git\n', '/work/x', 'alpha'],
    ['a URL on another host', 'https://gitlab.com/o/r.git', '/work/gamma/.git\n', '/work/gamma', 'gamma'],
    ['no URL, a worktree root', null, '/work/main/.git\n', '/work/main/.claude/worktrees/w1', 'main'],
    ['a common dir with a trailing slash', null, '/work/main/.git/\n', '/work/w', 'main'],
    ['a Windows common dir', null, 'C:\\work\\main\\.git\r\n', 'C:\\work\\w', 'main'],
    ['a submodule common dir', null, '/work/super/.git/modules/sub\n', '/work/super/subdir', 'subdir'],
    ['a bare repo common dir', null, '/work/repo.git\n', '/work/wt', 'wt'],
    ['a failed call', null, null, '/work/epsilon/', 'epsilon'],
    ['a root with no segment', null, null, '/', ''],
  ]
  for (const [name, url, common, root, want] of CASES) {
    test(name, () => {
      expect(projectName(url, common, root)).toBe(want)
    })
  }

  test('lastSegment splits on both separators and drops trailing ones', () => {
    expect(lastSegment('/a/b/')).toBe('b')
    expect(lastSegment('C:\\a\\b')).toBe('b')
    expect(lastSegment('')).toBe('')
  })
})
