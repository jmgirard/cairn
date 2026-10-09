import { describe, expect, test } from 'claude-code/testing'

import { FIXTURES } from './fixtures.gen'
import {
  candidateRows,
  canonId,
  collaborationMode,
  dirname,
  findRoot,
  loadBand,
  loadCairn,
  memorySource,
  parseDepends,
  parseRoadmapRows,
  prNumber,
  prUrl,
  sectionFields,
  workableRows,
} from './reader'
import type { BandState, FileSource } from './reader'

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
