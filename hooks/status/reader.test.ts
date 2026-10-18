import { describe, expect, test } from 'claude-code/testing'

import { FIXTURES } from './fixtures.gen'
import {
  candidateRows,
  canonId,
  collaborationMode,
  dirname,
  findRoot,
  highTitle,
  loadBand,
  loadCairn,
  memorySource,
  parseDepends,
  parseRoadmapRows,
  prNumber,
  prUrl,
  pushRemote,
  recommend,
  sectionFields,
  startedTokens,
  takenRows,
  workableRows,
} from './reader'
import type { BandState, CandidateRow, FileSource } from './reader'

// loadBand gives null for a found ROADMAP it cannot read. These tests read good files.
async function loaded(source: FileSource): Promise<BandState> {
  const band = await loadBand(source)
  if (band === null) throw new Error('loadBand gave null for a readable ROADMAP')
  return band
}

describe('reader over every fixture (M193 AC5, M199 AC2)', () => {
  test('the fixture domain is not empty', () => {
    expect(Object.keys(FIXTURES).length).toBeGreaterThan(8)
  })

  for (const [name, fixture] of Object.entries(FIXTURES)) {
    test(`${name}: rows, counts and next items match expected.json`, async () => {
      const { rows } = await loaded(memorySource(fixture.files, fixture.cwd, fixture.unreadable))
      expect(rows).toEqual(fixture.rows)
    })

    test(`${name}: the workable list matches expected.json`, async () => {
      const { workable } = await loaded(memorySource(fixture.files, fixture.cwd, fixture.unreadable))
      expect(workable.map(row => row.id)).toEqual(fixture.workable)
    })

    // The pane's data against the values the Python helpers and
    // `cairn_next.py` give for the same fixture (M205 AC2, AC3).
    test(`${name}: the pane's milestones and next step match expected.json`, async () => {
      const loaded = await loadCairn(memorySource(fixture.files, fixture.cwd, fixture.unreadable))
      if (loaded === null) throw new Error('loadCairn gave null for a readable ROADMAP')
      const { pane } = loaded
      expect(pane.milestones).toEqual(fixture.pane)
      expect(pane.next === null ? null : { ...pane.next, waiting: pane.waiting }).toEqual(fixture.next)
      expect(pane.workable.map(row => row.id)).toEqual(fixture.workable)
      expect(pane.found).toBe(fixture.next !== null)
      // The candidate rows against test_status_fixtures.py (M207 AC3).
      expect(pane.candidates).toEqual(fixture.candidates)
      // The blocked rows and their numbers against `cairn_next.blocked`
      // (M223 AC3).
      expect(pane.blocked).toEqual(fixture.blocked)
    })
  }

  // `prNumber` over the header forms beyond the fixtures (M223 AC1).
  test('prNumber reads the first URL of the first Branch/PR line, before any companion entry', () => {
    const header = (value: string) => `# M1: x\n\n- **Status:** blocked\n- **Branch/PR:** ${value}\n\n## Goal\n`
    expect(prNumber(header('b, https://github.com/o/r/pull/7'))).toBe(7)
    expect(prNumber(header('b, https://github.com/o/r/pull/7, https://github.com/o/r/pull/8'))).toBe(7)
    expect(prNumber(header('b, https://github.com/o/r/pull/7/files'))).toBe(7)
    expect(prNumber(header('b, https://github.com/o/r/pull/7#discussion_r1'))).toBe(7)
    expect(prNumber(header('b, companion: /x b https://github.com/o/s/pull/9'))).toBe(null)
    expect(prNumber(header('b, https://github.com/o/r/pull/7, companion: /x b https://github.com/o/s/pull/9'))).toBe(7)
    expect(prNumber(header('b, https://github.com/o/r/issues/7'))).toBe(null)
    expect(prNumber(header('b'))).toBe(null)
    expect(prNumber('# M1: x\n\nhttps://github.com/o/r/pull/7 in the body\n')).toBe(null)
    // A BOM before the dash: JavaScript's `\s` takes it and Python's does
    // not, so both sides spell out spaces and tabs and read no number.
    expect(prNumber(`${String.fromCharCode(0xfeff)}- **Branch/PR:** b, https://github.com/o/r/pull/7\n`)).toBe(null)
    expect(prNumber('\t- **Branch/PR:** b, https://github.com/o/r/pull/7\n')).toBe(7)
    // Only the first Branch/PR line counts, only above the first `## `
    // heading, and a number past 15 digits reads as none.
    expect(prNumber('- **Branch/PR:** b\n- **Branch/PR:** c, https://github.com/o/r/pull/7\n')).toBe(null)
    expect(prNumber('# M1: x\n\n## Review\n\n- **Branch/PR:** b, https://github.com/o/r/pull/7\n')).toBe(null)
    expect(prNumber(header('b, https://github.com/o/r/pull/123456789012345'))).toBe(123456789012345)
    expect(prNumber(header('b, https://github.com/o/r/pull/1234567890123456'))).toBe(null)
  })

  // `prUrl` over the forms test_status_fixtures.py gives `pr_url` (M224):
  // the URL up to its number, which the pane hands to `gh pr view`.
  test('prUrl reads the same URL, less any trailing path or anchor', () => {
    const header = (value: string) => `# M1: x\n\n- **Status:** blocked\n- **Branch/PR:** ${value}\n\n## Goal\n`
    const seven = 'https://github.com/o/r/pull/7'
    expect(prUrl(header('b, https://github.com/o/r/pull/7'))).toBe(seven)
    expect(prUrl(header('b, https://github.com/o/r/pull/7, https://github.com/o/r/pull/8'))).toBe(seven)
    expect(prUrl(header('b, https://github.com/o/r/pull/7/files'))).toBe(seven)
    expect(prUrl(header('b, https://github.com/o/r/pull/7#discussion_r1'))).toBe(seven)
    expect(prUrl(header('b, companion: /x b https://github.com/o/s/pull/9'))).toBe(null)
    expect(prUrl(header('b, https://github.com/o/r/issues/7'))).toBe(null)
    expect(prUrl(header('b'))).toBe(null)
    expect(prUrl(header('b, https://github.com/o/r/pull/1234567890123456'))).toBe(null)
  })

  test('the pane fixtures hold the shapes M205 names', () => {
    const full = FIXTURES['pane-full']
    const long = full.pane.find(row => row.id === 'M080')?.file
    // More than five log lines in the file, five shown, the newest last.
    expect(full.files['/cairn/milestones/M080-long-log.md'].split('\n- 2026-').length - 1).toBeGreaterThan(5)
    expect(long?.log.length).toBe(5)
    expect(long?.log[4]).toBe('2026-01-07: seventh line, the newest.')
    // A wrapped task reads whole.
    expect(long?.tasks[0].text).toBe('T1: The first task, wrapped over three lines of text.')
    // A goal of several paragraphs keeps its blank line.
    expect(full.pane.find(row => row.id === 'M081')?.file?.goal).toContain('\n\n')
    // The unreadable file shows no parts.
    expect(full.unreadable).toEqual(['/cairn/milestones/M082-unreadable.md'])
    expect(full.pane.find(row => row.id === 'M082')?.file).toBe(null)
    // Every planned row waits, so the next step is planning.
    expect(FIXTURES['all-waiting'].next).toEqual(expect.objectContaining({ command: '/milestone-plan', id: null }))
  })

  test('no-roadmap expects an empty result', async () => {
    const fixture = FIXTURES['no-roadmap']
    expect(fixture.rows).toEqual([])
    expect(await loadBand(memorySource(fixture.files, fixture.cwd))).toEqual({ rows: [], workable: [] })
  })

  test('missing-file expects no counts and no next items', async () => {
    const fixture = FIXTURES['missing-file']
    const [row] = (await loaded(memorySource(fixture.files, fixture.cwd))).rows
    expect([row.tasksChecked, row.tasksTotal, row.criteriaChecked, row.criteriaTotal]).toEqual([null, null, null, null])
    expect([row.nextTask, row.nextCriterion]).toEqual([null, null])
  })

  test('nested-first names the nested task, less its box and spaces', async () => {
    const fixture = FIXTURES['nested-first']
    const [row] = (await loaded(memorySource(fixture.files, fixture.cwd))).rows
    expect(row.nextTask).toBe('T1a: Nested task, open, with extra spaces after the box.')
  })

  test('the workable list is computed while a row is active', async () => {
    const fixture = FIXTURES['six-active']
    const band = await loaded(memorySource(fixture.files, fixture.cwd))
    expect(band.rows.length).toBe(6)
    expect(band.workable).toEqual([{ id: 'M073', title: 'A planned row between them' }])
  })

  test('idle-deps: an archive file marks its id done only directly under the archive directory', async () => {
    const fixture = FIXTURES['idle-deps']
    expect(Object.keys(fixture.files)).toContain('/cairn/milestones/archive/sub/M077-nested.md')
    const ids = (await loaded(memorySource(fixture.files, fixture.cwd))).workable.map(row => row.id)
    // M040 needs M57, which only the archive file M0057-pruned.md marks done.
    expect(ids).toContain('M040')
    // M051 needs M077, whose only file sits one directory deeper.
    expect(ids).not.toContain('M051')
  })
})

describe('the workable list (M199 AC1)', () => {
  const roadmap = (lines: string[]) =>
    parseRoadmapRows(['| ID | Title | Status | Depends on | Priority | File/Archive |', '|---|---|---|---|---|---|', ...lines].join('\n'))

  test('Depends-on cells in their comma, space, dash, and malformed forms', () => {
    expect(parseDepends('M001, M002')).toEqual(['M001', 'M002'])
    expect(parseDepends('M001 M002')).toEqual(['M001', 'M002'])
    expect(parseDepends('M001,M002')).toEqual(['M001', 'M002'])
    expect(parseDepends('—')).toEqual([])
    expect(parseDepends('')).toEqual([])
    expect(parseDepends('m001 M M1a')).toEqual([])
  })

  test('ids compare at three-digit padding', () => {
    expect(canonId('M57')).toBe('M057')
    expect(canonId('M0057')).toBe('M057')
    expect(canonId('M1000')).toBe('M1000')
    expect(canonId('Mfoo')).toBe('Mfoo')
  })

  test('a done row meets a dependency spelled at another padding', () => {
    const rows = roadmap(['| M57 | Shipped | done | — | normal | m |', '| M060 | Next | planned | M057 | normal | m |'])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M060'])
  })

  test('only an archive file ending in .md marks its id done', async () => {
    const text = [
      '| ID | Title | Status | Depends on | Priority | File/Archive |',
      '|---|---|---|---|---|---|',
      '| M091 | On a text file | planned | M090 | high | m |',
      '| M093 | On a markdown file | planned | M092 | normal | m |',
    ].join('\n')
    const files = {
      '/cairn/ROADMAP.md': text,
      '/cairn/milestones/archive/M090-notes.txt': '',
      '/cairn/milestones/archive/M092-shipped.md': '',
    }
    expect((await loaded(memorySource(files, '/'))).workable.map(r => r.id)).toEqual(['M093'])
  })

  test('a priority word that names an object property reads as normal', () => {
    const rows = roadmap([
      '| M002 | Low | planned | — | low | m |',
      '| M003 | Odd | planned | — | constructor | m |',
      '| M004 | Normal | planned | — | normal | m |',
    ])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M003', 'M004', 'M002'])
  })

  test('a dependency on a planned, blocked, or unknown milestone holds a row back', () => {
    const rows = roadmap([
      '| M001 | Base | planned | — | low | m |',
      '| M002 | Held | blocked | — | low | m |',
      '| M010 | On planned | planned | M001 | high | m |',
      '| M011 | On blocked | planned | M002 | high | m |',
      '| M012 | On unknown | planned | M099 | high | m |',
      '| M013 | On archive | planned | M99 | high | m |',
    ])
    expect(workableRows(rows, ['M099']).map(r => r.id)).toEqual(['M012', 'M013', 'M001'])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M001'])
  })

  test('only planned rows are workable', () => {
    const rows = roadmap([
      '| M001 | A | in-progress | — | high | m |',
      '| M002 | B | review | — | high | m |',
      '| M003 | C | blocked | — | high | m |',
      '| M004 | D | done | — | high | m |',
      '| M005 | E | candidate | — | high | m |',
      '| M006 | F | Planned | — | low | m |',
    ])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M006'])
  })
})

describe('candidate rows (M207 review)', () => {
  const rows = [
    { priority: 'high', title: 'High row' },
    { priority: 'normal', title: 'Normal row' },
  ]

  test('CRLF line breaks read as LF ones', () => {
    const lf = '# Roadmap\n\n## Candidates\n\n- [high] High row: x\n- Normal row: y\n'
    expect(candidateRows(lf)).toEqual(rows)
    expect(candidateRows(lf.replace(/\n/g, '\r\n'))).toEqual(rows)
  })

  test("a comment opened in another section hides no candidate row", () => {
    const text = '## Milestones\n\n`<!--` in a title\n\n## Candidates\n\n- [high] High row: x\n- Normal row: y\n\n## Notes\n\n`-->`\n'
    expect(candidateRows(text)).toEqual(rows)
  })

  test('a comment inside the section hides the rows it holds', () => {
    const text = '## Candidates\n<!--\n- [low] Hidden: x\n-->\n- [high] High row: x\n- Normal row: y\n'
    expect(candidateRows(text)).toEqual(rows)
  })
})

// The short title (M251 AC1): the text after the token up to the first
// `: `, else up to the first ` — `, else all of it. The first two rows
// open as glmmTMB's ROADMAP rows do.
describe('the short title is cut at the first `: `, else at the first ` — ` (M251 AC1)', () => {
  const table: [string, CandidateRow][] = [
    ['ordinal: REML. The fit warns — added 2026-10-01', { priority: 'normal', title: 'ordinal' }],
    ['loglog link for `binomial`. Needs a case — added 2026-10-15', { priority: 'normal', title: 'loglog link for `binomial`. Needs a case' }],
    ['Title — detail: more — added 2026-01-01', { priority: 'normal', title: 'Title — detail' }],
    ['[low] Low row — added 2026-01-02', { priority: 'low', title: 'Low row' }],
    ['A `a — b` dash in backticks — added 2026-01-03', { priority: 'normal', title: 'A `a' }],
    ['A row with no colon and no dash', { priority: 'normal', title: 'A row with no colon and no dash' }],
    [': an empty short title — added 2026-01-04', { priority: 'normal', title: '' }],
    // The trim edges where Python's bare strip() differs from trim(), held
    // on the Python side by test_python_candidates_cut_and_trim_edges
    // (M251 review).
    ['Trailing byte-order mark\uFEFF: x — added 2026-01-05', { priority: 'normal', title: 'Trailing byte-order mark' }],
    ['Trailing unit separator\u001F: x — added 2026-01-06', { priority: 'normal', title: 'Trailing unit separator\u001F' }],
  ]
  for (const [text, row] of table) {
    test(text, () => {
      expect(candidateRows(`## Candidates\n\n- ${text}\n`)).toEqual([row])
    })
  }
})

// M258 AC4: a started token appended to a row leaves its short title as it
// was, for a row cut at `: `, one cut at ` — `, and one with neither.
describe('a started token leaves the short title unchanged (M258 AC4)', () => {
  const rows = [
    'Colon row: detail — added 2026-10-15',
    '[low] Dash row — added 2026-10-15',
    'A row with no colon and no dash',
  ]
  const tokens = [' — started M258', ' — started #301', ' — started M258 — started #301']
  for (const row of rows) {
    for (const token of tokens) {
      test(`${row} + ${token}`, () => {
        expect(candidateRows(`## Candidates\n\n- ${row}${token}\n`)).toEqual(candidateRows(`## Candidates\n\n- ${row}\n`))
      })
    }
  }
})

describe('started tokens of the candidate rows (M258)', () => {
  const roadmap = [
    '| ID | Title | Status | Depends on | Priority | File/Archive |',
    '|---|---|---|---|---|---|',
    '| M258 | P | planned | — | normal | m |',
    '| M240 | B | blocked | — | normal | m |',
    '| M230 | D | done | — | normal | m |',
    '| M231 | X | dropped | — | normal | m |',
    '| M232 | I | in-progress | — | normal | m |',
    '',
    '## Candidates',
    '',
    '- Planned row: x — added 2026-10-15 — started M258',
    '- Blocked row: x — started M240 — added 2026-10-15',
    '- Done row: x — started M230',
    '- Dropped row: x — started M231',
    '- Absent row: x — started M999',
    '- Active row: x — started M232',
    '- Two ids: x — started M300 — started M0258',
    '- Hotfix row: x — started #301',
    '- Noted row: x — started M258; narrowed 2026-10-15 by the PR #9 hotfix',
    '- Spaced row: x — started #302 ',
    '- Not a token: x — started M258x — started #12x — started  M258 — startedM258',
    '- : empty title — started M258',
  ].join('\n')

  test('startedTokens reads each token with its row title', () => {
    expect(startedTokens(roadmap)).toEqual([
      { title: 'Planned row', ref: 'M258' },
      { title: 'Blocked row', ref: 'M240' },
      { title: 'Done row', ref: 'M230' },
      { title: 'Dropped row', ref: 'M231' },
      { title: 'Absent row', ref: 'M999' },
      { title: 'Active row', ref: 'M232' },
      { title: 'Two ids', ref: 'M300' },
      { title: 'Two ids', ref: 'M0258' },
      { title: 'Hotfix row', ref: '#301' },
      { title: 'Noted row', ref: 'M258' },
      { title: 'Spaced row', ref: '#302' },
    ])
  })

  test('takenRows keeps an id only while its row is planned or blocked, padded, and every #n', () => {
    expect(takenRows(roadmap, parseRoadmapRows(roadmap))).toEqual([
      { title: 'Planned row', ref: 'M258' },
      { title: 'Blocked row', ref: 'M240' },
      { title: 'Two ids', ref: 'M258' },
      { title: 'Hotfix row', ref: '#301' },
      { title: 'Noted row', ref: 'M258' },
      { title: 'Spaced row', ref: '#302' },
    ])
  })

  test('loadCairn gives the pane the counted tokens', async () => {
    const files = { '/cairn/ROADMAP.md': `# Roadmap\n\n## Milestones\n\n${roadmap}\n` }
    const loaded = await loadCairn(memorySource(files, '/'))
    expect(loaded?.pane.taken.map(item => item.ref)).toEqual(['M258', 'M240', 'M258', '#301', 'M258', '#302'])
  })

  // A blocked row whose file was archived as done (M246) shipped, so its
  // token no longer counts (M258 review).
  test('a blocked id whose file was archived as done does not count', async () => {
    const files = {
      '/cairn/ROADMAP.md': `# Roadmap\n\n## Milestones\n\n${roadmap}\n`,
      '/cairn/milestones/archive/M240-b.md': '# M240: B\n\n**Status:** done (2026-10-15)\n',
    }
    const loaded = await loadCairn(memorySource(files, '/'))
    expect(loaded?.pane.blocked.map(row => [row.id, row.archived])).toEqual([['M240', true]])
    expect(loaded?.pane.taken.map(item => item.ref)).toEqual(['M258', 'M258', '#301', 'M258', '#302'])
  })
})

// The cases test_scripts.py gives `high_title` through `recommend` (M272
// AC1), held here to `highTitle`.
describe('highTitle names the first unstarted [high] row (M272)', () => {
  const rows = (...lines: string[]) => `# Roadmap\n\n## Candidates\n\n${lines.map(line => `- ${line}`).join('\n')}\n`
  test('a [high] row is chosen over an earlier untagged row, and trimmed', () => {
    expect(highTitle(rows('Untagged first: detail', '[high]  Chosen row : detail — added 2026-01-01'))).toBe('Chosen row')
  })
  test('a started [high] row is passed over, and a token run on into a letter is not a token', () => {
    for (const started of [
      '[high] Taken: x — started M271',
      '[high] Taken: x — started #12',
      '[high] Taken: x — started M271; narrowed',
      '[high] Taken: x — started #12 ',
      '[high] Taken: x — started #1234567890123456',
    ]) {
      expect(highTitle(rows(started, '[high] Next high: y'))).toBe('Next high')
    }
    expect(highTitle(rows('[high] Not taken: x — started M271a', '[high] Next high: y'))).toBe('Not taken')
  })
  test('a [high] row inside a comment and one with an empty title are passed over', () => {
    expect(highTitle(rows('<!--', '[high] Commented out: x', '-->', '[high] : empty title', '[high] Visible: y'))).toBe('Visible')
  })
  test('no [high] row gives null', () => {
    expect(highTitle(rows('Plain: x', '[low] Low: y', '[HIGH] Upper: z', '[high]Tight: w'))).toBe(null)
  })
  test('only planning carries the title', () => {
    const roadmap = rows('[high] Waiting row: x')
    expect(recommend([], [{ id: 'M003', title: 'T' }], roadmap).title).toBe(null)
    expect(recommend([], [], roadmap).title).toBe('Waiting row')
  })
})

describe('reader details', () => {
  test('the walk goes up two levels from a subdirectory', async () => {
    const fixture = FIXTURES['subdirectory']
    expect(fixture.cwd).toBe('/pkg/src')
    expect(await findRoot(memorySource(fixture.files, fixture.cwd), fixture.cwd)).toBe('/')
  })

  test('counts only the first ## Tasks section, any indent, x or X', () => {
    const text = [
      '## Acceptance criteria',
      '- [x] AC1',
      '## Tasks',
      '- [x] T1',
      '    - [X] T1a',
      '- [ ] T2',
      '### Inside',
      '- [ ] T3',
      '## Work log',
      '- [x] not a task',
      '## Tasks',
      '- [x] a second Tasks section, not read',
    ].join('\n')
    expect(sectionFields(text, 'Tasks')).toEqual({ checked: 2, total: 4, next: 'T2' })
    expect(sectionFields(text, 'Acceptance criteria')).toEqual({ checked: 1, total: 1, next: null })
  })

  test('a milestone path that is not a regular file is never read', async () => {
    const fixture = FIXTURES['single-in-progress']
    const files = fixture.files
    const reads: string[] = []
    const source = {
      cwd: async () => '/',
      // The ROADMAP is a file; the milestone path exists but is a pipe.
      isFile: async (path: string) => path === '/cairn/ROADMAP.md',
      read: async (path: string) => {
        reads.push(path)
        return files[path] ?? null
      },
      list: async () => null,
    }
    const { rows } = await loaded(source)
    expect(rows.map(r => [r.id, r.tasksChecked, r.tasksTotal, r.nextTask])).toEqual([['M002', null, null, null]])
    expect(reads).toEqual(['/cairn/ROADMAP.md'])
  })

  test('a found ROADMAP that cannot be read gives null, and no ROADMAP found gives an empty band (M200)', async () => {
    const fixture = FIXTURES['single-in-progress']
    const source = { ...memorySource(fixture.files, fixture.cwd), read: async () => null }
    expect(await loadBand(source)).toBeNull()
    const none = FIXTURES['no-roadmap']
    expect(await loadBand({ ...memorySource(none.files, none.cwd), read: async () => null })).toEqual({ rows: [], workable: [] })
  })

  test('an archive directory that cannot be listed marks nothing done', async () => {
    const fixture = FIXTURES['idle-deps']
    const source = { ...memorySource(fixture.files, fixture.cwd), list: async () => null }
    const ids = (await loaded(source)).workable.map(row => row.id)
    expect(ids).not.toContain('M040')
    expect(ids).toContain('M041')
  })

  test('dirname stops at the root', () => {
    expect(dirname('/a/b')).toBe('/a')
    expect(dirname('/a')).toBe('/')
    expect(dirname('/')).toBe('/')
    expect(dirname('C:\\a')).toBe('C:\\')
  })

  test('dirname stops at a UNC share root (M210 AC1)', () => {
    expect(dirname('\\\\srv\\share')).toBe('\\\\srv\\share')
    expect(dirname('//srv/share')).toBe('//srv/share')
    expect(dirname('\\\\srv\\share\\')).toBe('\\\\srv\\share')
    expect(dirname('\\\\srv\\share\\a')).toBe('\\\\srv\\share')
  })

  test('findRoot probes no path above a UNC share root (M210 AC1)', async () => {
    const probed: string[] = []
    const source = {
      cwd: async () => '\\\\srv\\share\\a\\b',
      isFile: async (path: string) => {
        probed.push(path)
        return false
      },
      read: async () => null,
      list: async () => null,
    }
    expect(await findRoot(source, await source.cwd())).toBeNull()
    expect(probed).toEqual([
      '\\\\srv\\share\\a\\b/cairn/ROADMAP.md',
      '\\\\srv\\share\\a/cairn/ROADMAP.md',
      '\\\\srv\\share/cairn/ROADMAP.md',
    ])
  })
})

// `collaborationMode` against `collaboration_mode` in hooks/cairn_common.py
// (M226 review). Each expected value is what the Python reader gave for the
// same PROFILE.md text on 2026-10-09, written out by hand.
describe('collaborationMode reads the mode as cairn_common does (M226)', () => {
  const CASES: [string, string, string][] = [
    ['an empty file', '', 'owner'],
    ['a guest line', '# Collaboration mode: guest\n', 'guest'],
    ['the key and value in other cases', '# collaboration MODE:   Guest\n', 'guest'],
    ['a leading BOM', '﻿# Collaboration mode: guest\n', 'guest'],
    ['a line after the first slot heading', '# Toolchain profile: x\n\n## verify\n# Collaboration mode: guest\n', 'owner'],
    ['an owner line', '# Collaboration mode: owner\n', 'owner'],
    ['no spaces', '#Collaboration mode:guest\n', 'guest'],
    ['an indented line', '  # Collaboration mode: guest\n', 'owner'],
    ['two lines, the first wins', '# Toolchain profile: x\n# Collaboration mode: guest\n# Collaboration mode: owner\n', 'guest'],
  ]
  for (const [name, text, mode] of CASES) {
    test(`${name} reads as ${mode}`, () => {
      expect(collaborationMode(text)).toBe(mode)
    })
  }
})

describe('pushRemote reads the line as cairn_common does (M268)', () => {
  const CASES: [string, string, string | null][] = [
    ['an empty file', '', null],
    ['a base line under the mode line', '# Collaboration mode: guest\n# Push remote: base\n', 'base'],
    ['the key and value in other cases', '#push REMOTE:  Base\n', 'base'],
    ['a leading BOM', '﻿# Push remote: base\n', 'base'],
    ['a line after the first slot heading', '# Toolchain profile: x\n\n## verify\n# Push remote: base\n', null],
    ['the mode line alone', '# Collaboration mode: guest\n', null],
  ]
  for (const [name, text, value] of CASES) {
    test(`${name} reads as ${value}`, () => {
      expect(pushRemote(text)).toBe(value)
    })
  }
})
