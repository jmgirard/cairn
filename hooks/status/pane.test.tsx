import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { FIXTURES } from './fixtures.gen'
import { flowOf, width } from './band'
import { CHECKED_MARK, COMMAND_PHASE, NO_FILE, NO_ROADMAP, OPEN_MARK, PRIORITY_MARK, nextLabel, paneLines as layout } from './pane'
import type { PaneState } from './reader'
import { listNames } from './reader'

// The cairn pane (M205). Each case answers the shipped mod's file calls from
// an in-memory copy of a fixture, as band.test.tsx does, and answers the
// pane calls (`ui.open`, `ui.close`, `ui.panes`) beneath the mod from a list
// of the open panes that it keeps. The values each case expects come from
// the fixture's `expected.json`, which scripts/tests/test_status_fixtures.py
// holds to the Python helpers and scripts/cairn_next.py.

const SURFACES = ['terminal', 'desktop'] as const
const PANE = 'cairn'
const COMMAND = 'cairn-pane'
const PANE_VIEW = {
  component: 'Pane',
  requestId: PANE,
  props: {
    title: 'cairn',
    isFocused: false,
    bodyColumns: 60,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 200 },
    view: {},
  },
} as const
const BAND = {
  component: 'AbovePrompt',
  props: { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 120 },
} as const
// The phase label of each status, written out by hand.
const PHASE_LABEL: Record<string, string> = { 'in-progress': 'implement', review: 'review' }
// The fixtures whose reader finds a ROADMAP.
const WITH_ROADMAP = Object.keys(FIXTURES).filter(name => FIXTURES[name].next !== null)

type Element = { type: string; key?: string; props: Record<string, unknown>; children: unknown[] }
type Ui = {
  findAll: (q: { type?: string; key?: string }) => Promise<Element[]>
  press: (q: { key: string }) => Promise<unknown>
  unmount: () => Promise<void>
}

type Copy = {
  cwd: string
  files: Record<string, string>
  unreadable: string[]
  // The ids of the open panes, and each open and close that reached beneath
  // the mod.
  open: string[]
  opens: { id: string; title?: string }[]
  closes: string[]
  // When set, an open answers that the pane waits undrawn, for this reason,
  // and the pane stays listed with `isPlaced` false, as the API keeps it.
  notPlaced?: string
  // The open ids that wait undrawn, and those behind another pane's tab.
  unplaced?: string[]
  hidden?: string[]
  // The toasts that reached beneath the mod.
  toasts?: string[]
  // When set, every open is refused with this reason.
  refuse?: string
  // The command and args of each slash command run that reached beneath the
  // mod, and while set, a promise each run waits for before it answers
  // (M218).
  commands?: { command: string; args: string }[]
  runHold?: Promise<void>
}

function copyOf(name: string): Copy {
  const fixture = FIXTURES[name]
  return { cwd: fixture.cwd, files: { ...fixture.files }, unreadable: [...fixture.unreadable], open: [], opens: [], closes: [] }
}

let turnCount = 0
function turn() {
  turnCount += 1
  return { answer: '', durationMs: 1, isAborted: false, turnId: `t${turnCount}`, reason: 'answer' as const }
}

function seat(on: On, copy: Copy) {
  const has = (path: string) => Object.prototype.hasOwnProperty.call(copy.files, path)
  on('session.cwd', async () => ({ value: copy.cwd }))
  on('fs.stat', async ($, e, next) =>
    has(e.path) ? { value: { kind: 'file', size: copy.files[e.path].length, mtimeMs: 0, isLink: false } } : next(e),
  )
  on('fs.read', async ($, e, next) =>
    has(e.path) && !copy.unreadable.includes(e.path) ? { value: copy.files[e.path] } : next(e),
  )
  on('fs.list', async ($, e, next) => {
    const names = listNames(Object.keys(copy.files), e.path)
    if (names === null) return next(e)
    return { value: names.map(name => ({ name, kind: 'other', size: 0, mtimeMs: 0, isLink: false })) }
  })
  on('session.start', async ($, e) => ({ cwd: e.cwd }))
  on('turn.complete', async () => ({ text: '' }))
  on('classic.Stop', async () => ({}))
  on('prompt.submit', async ($, e) => ({ text: e.text, origin: e.origin }))
  on('skill.prompt', async ($, e) => ({ text: e.text }))
  on('ui.render', { component: 'AbovePrompt' }, async () => ({ type: 'Text', props: {}, children: ['engine slot'] }))
  on('ui.open', async ($, e) => {
    if (copy.refuse !== undefined) return { deny: copy.refuse }
    copy.opens.push({ id: e.id, title: e.title })
    if (!copy.open.includes(e.id)) copy.open.push(e.id)
    copy.hidden = (copy.hidden ?? []).filter(id => id !== e.id)
    if (copy.notPlaced !== undefined) {
      copy.unplaced = [...(copy.unplaced ?? []).filter(id => id !== e.id), e.id]
      return { value: { isPlaced: false, reason: copy.notPlaced } }
    }
    copy.unplaced = (copy.unplaced ?? []).filter(id => id !== e.id)
    return { value: { isPlaced: true } }
  })
  on('ui.close', async ($, e) => {
    copy.closes.push(e.id)
    copy.open = copy.open.filter(id => id !== e.id)
    return { value: undefined }
  })
  on('ui.panes', async () => ({
    value: copy.open.map(id => ({
      id,
      title: id,
      isShown: !(copy.hidden ?? []).includes(id),
      isFocused: false,
      isPlaced: !(copy.unplaced ?? []).includes(id),
    })),
  }))
  on('ui.toast', async ($, e) => {
    copy.toasts = [...(copy.toasts ?? []), e.text]
    return { value: undefined }
  })
  on('command.run', async ($, e) => {
    copy.commands = [...(copy.commands ?? []), { command: e.command, args: e.args }]
    if (copy.runHold !== undefined) await copy.runHold
    return { text: '' }
  })
}

function textOf(node: unknown): string {
  if (typeof node === 'string') return node
  if (node === null || typeof node !== 'object') return ''
  return ((node as Element).children ?? []).map(textOf).join('')
}

function keyOf(node: Element): string | undefined {
  return node.key ?? (node.props?.key as string | undefined)
}

function kids(node: Element): Element[] {
  return (node.children ?? []).filter((c): c is Element => c !== null && typeof c === 'object')
}

// The pane's lines in order, each its key and its text.
async function paneLines($, surface: (typeof SURFACES)[number]): Promise<[string, string][]> {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const out = kids(root).map(line => [keyOf(line) ?? '', textOf(line)] as [string, string])
  await ui.unmount()
  return out
}

const textAt = (lines: [string, string][], key: string) => lines.find(([k]) => k === key)?.[1]
const keysLike = (lines: [string, string][], pattern: RegExp) => lines.map(([k]) => k).filter(k => pattern.test(k))
const itemText = (item: { text: string; checked: boolean }) => `${item.checked ? CHECKED_MARK : OPEN_MARK} ${item.text}`

describe('/cairn-pane opens and closes the pane (M205 AC1)', () => {
  test('with a ROADMAP, the command opens pane cairn, and run again closes it', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const first = await $.command.run({ command: COMMAND })
    expect(copy.opens.map(open => open.id)).toEqual([PANE])
    expect(copy.open).toEqual([PANE])
    expect(first.text).toBe('cairn pane opened')
    const second = await $.command.run({ command: COMMAND })
    expect(copy.closes).toEqual([PANE])
    expect(copy.open).toEqual([])
    expect(second.text).toBe('cairn pane closed')
    // A third run opens it again.
    await $.command.run({ command: COMMAND })
    expect(copy.open).toEqual([PANE])
  })

  test('with no ROADMAP, the command opens no pane and says so', async ($, on) => {
    const copy = copyOf('no-roadmap')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const result = await $.command.run({ command: COMMAND })
    expect(copy.opens).toEqual([])
    expect(result.text).toBe(NO_ROADMAP)
  })

  test("an open the surface does not place prints the engine's reason", async ($, on) => {
    const copy = copyOf('single-in-progress')
    copy.notPlaced = 'the attached surfaces place no panes'
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const result = await $.command.run({ command: COMMAND })
    expect(copy.opens.map(open => open.id)).toEqual([PANE])
    expect(result.text).toContain('the attached surfaces place no panes')
    // The unplaced pane stays listed. A second run opens it again rather
    // than closing a pane nobody saw (M205 review).
    copy.notPlaced = undefined
    const second = await $.command.run({ command: COMMAND })
    expect(copy.closes).toEqual([])
    expect(copy.opens.map(open => open.id)).toEqual([PANE, PANE])
    expect(second.text).toBe('cairn pane opened')
  })

  test('a pane behind another tab is opened again, not closed', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    await $.command.run({ command: COMMAND })
    copy.hidden = [PANE]
    const result = await $.command.run({ command: COMMAND })
    expect(copy.closes).toEqual([])
    expect(copy.opens.length).toBe(2)
    expect(result.text).toBe('cairn pane opened')
  })

  test('a refused open gives a line, not an error', async ($, on) => {
    const copy = copyOf('single-in-progress')
    copy.refuse = 'opens are refused here'
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const result = await $.command.run({ command: COMMAND })
    expect(result.text.startsWith('cairn pane: ')).toBe(true)
    expect(result.text).toContain('opens are refused here')
  })
})

describe('the pane shows each active milestone in full (M205 AC2)', () => {
  test('the domain holds the shapes AC2 names', () => {
    expect(WITH_ROADMAP.length).toBeGreaterThan(10)
    expect(WITH_ROADMAP).toContain('pane-full')
    expect(FIXTURES['pane-full'].unreadable.length).toBe(1)
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const want = FIXTURES[name].pane
        // The milestones in ROADMAP order, and no others.
        expect(keysLike(lines, /-head$/).filter(k => /^M\d+-head$/.test(k))).toEqual(want.map(row => `${row.id}-head`))
        for (const row of want) {
          // The head line ends with the band's percent for a row whose file
          // reads (M208 AC1).
          const band = FIXTURES[name].rows.find(b => b.id === row.id && b.status === row.status)
          const percent = row.file === null || band === undefined ? null : flowOf(band)?.percent
          const tail = percent === null || percent === undefined ? '' : `  ${percent}%`
          expect(textAt(lines, `${row.id}-head`)).toBe(`${PHASE_LABEL[row.status]} ${row.id}  ${row.title}${tail}`)
          const file = row.file
          if (file === null) {
            expect(textAt(lines, `${row.id}-nofile`)).toBe(NO_FILE)
            expect(keysLike(lines, new RegExp(`^${row.id}-(task|criterion|log|goal)-`))).toEqual([])
            continue
          }
          const goal = keysLike(lines, new RegExp(`^${row.id}-goal-\\d+$`)).map(k => textAt(lines, k))
          expect(goal).toEqual(file.goal === '' ? [] : file.goal.split('\n').map(text => (text === '' ? ' ' : text)))
          const tasks = keysLike(lines, new RegExp(`^${row.id}-task-\\d+$`)).map(k => textAt(lines, k))
          expect(tasks).toEqual(file.tasks.map(itemText))
          const criteria = keysLike(lines, new RegExp(`^${row.id}-criterion-\\d+$`)).map(k => textAt(lines, k))
          expect(criteria).toEqual(file.criteria.map(itemText))
          const log = keysLike(lines, new RegExp(`^${row.id}-log-\\d+$`)).map(k => textAt(lines, k))
          expect(log).toEqual(file.log)
          expect(log.length).toBeLessThanOrEqual(5)
        }
      })
    }
  }

  // The operator picked one line per item at the live look: each item, log
  // line, and title is cut with an ellipsis, and the goal's lines wrap.
  for (const surface of SURFACES) {
    test(`items cut to one line, the goal wraps (${surface})`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const wrapOf = async (key: string) => {
        const [box] = await ui.findAll({ key: `${key}-text` })
        return kids(box)[0].props.wrap
      }
      for (const key of ['M080-head', 'M080-task-0', 'M080-criterion-0', 'M080-log-4', 'waiting-M083', 'workable-M085', 'next']) {
        expect([key, await wrapOf(key)]).toEqual([key, 'truncate-end'])
      }
      for (const key of ['M081-goal-0', 'M081-goal-1', 'M081-goal-2']) expect([key, await wrapOf(key)]).toEqual([key, 'wrap'])
      await ui.unmount()
    })
  }

  test('with no ROADMAP, an open pane says that none was found', async ($, on) => {
    seat(on, copyOf('no-roadmap'))
    await $.turn.complete(turn())
    for (const surface of SURFACES) expect(await paneLines($, surface)).toEqual([['no-roadmap', NO_ROADMAP]])
  })
})

describe("the pane shows the queue that cairn_next.py prints (M205 AC3)", () => {
  test('the domain reaches every recommended command', () => {
    const commands = new Set(WITH_ROADMAP.map(name => FIXTURES[name].next?.command))
    expect([...commands].sort()).toEqual(['/milestone-implement', '/milestone-plan', '/milestone-review'])
    // Each one has a phase for the Next pill's color (M208 review).
    expect(Object.keys(COMMAND_PHASE).sort()).toEqual([...commands].sort())
    expect(WITH_ROADMAP.some(name => (FIXTURES[name].next?.waiting.length ?? 0) > 0)).toBe(true)
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const next = FIXTURES[name].next
        if (next === null) throw new Error('a fixture with a ROADMAP has a next step')
        // The command sits in a pill, one space of padding each side (M208).
        expect(textAt(lines, 'next')).toBe(`Next   ${next.id === null ? next.command : `${next.command} ${next.id}`} `)
        // Every id opens with `M`, and the heading lines' keys end in `head`.
        expect(keysLike(lines, /^workable-M/)).toEqual(FIXTURES[name].workable.map(id => `workable-${id}`))
        expect(keysLike(lines, /^waiting-M/)).toEqual(next.waiting.map(row => `waiting-${row.id}`))
        for (const row of next.waiting) {
          expect(textAt(lines, `waiting-${row.id}`)).toBe(`${row.id}  ${row.title} · on ${row.unmet.join(', ')}`)
        }
      })
    }
  }
})

// The candidates fixture's lines, written out by hand from its ROADMAP.
const CANDIDATE_LINES = [
  '↑ High row',
  '· Normal row',
  '↓ Low row',
  '· A row with no colon and space, shown whole — added 2026-01-04',
  '· [HIGH] Upper-case token, shown whole — added 2026-01-05',
  '· [high]No space after the token, shown whole — added 2026-01-06',
  '· Token in [low] mid-row, shown whole — added 2026-01-07',
  '· A long title that runs on well past the width of any docked pane, so the pane cuts it to one line with an ellipsis at its end',
  '· `code',
]

describe('the idle pane lists the candidate rows (M207 AC1, AC2)', () => {
  for (const surface of SURFACES) {
    test(`the candidates fixture's heading, count, marks, and titles (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'candidates-head')).toBe('▎ CANDIDATES 9')
      const rows = keysLike(lines, /^candidate-\d+$/)
      expect(rows.map(k => textAt(lines, k))).toEqual(CANDIDATE_LINES)
      // The section comes after the queue.
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('candidates-head')).toBeGreaterThan(at('next'))
      expect(at('candidates-head')).toBeGreaterThan(at('workable-M031'))
    })

    test(`each priority's mark (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const markOf = async (i: number) => {
        const [lead] = await ui.findAll({ key: `candidate-${i}-lead` })
        return kids(lead)[0]
      }
      expect(textOf(await markOf(0))).toBe(PRIORITY_MARK.high.text)
      // The high mark takes the implement phase's theme key, written out
      // by hand (M217).
      expect((await markOf(0)).props.color).toBe('claude')
      expect(textOf(await markOf(1))).toBe(PRIORITY_MARK.normal.text)
      expect(textOf(await markOf(2))).toBe(PRIORITY_MARK.low.text)
      expect((await markOf(2)).props.color).toBe(PRIORITY_MARK.low.color)
      // The high mark is bold, the normal mark has no color, and only a
      // low row's title is gray.
      expect((await markOf(0)).props.bold).toBe(true)
      expect((await markOf(1)).props.color).toBe(undefined)
      const titleOf = async (i: number) => kids((await ui.findAll({ key: `candidate-${i}-text` }))[0])[0]
      expect((await titleOf(2)).props.color).toBe(PRIORITY_MARK.low.color)
      expect((await titleOf(0)).props.color).toBe(undefined)
      expect((await titleOf(1)).props.color).toBe(undefined)
      // The three marks differ.
      expect(new Set([PRIORITY_MARK.high.text, PRIORITY_MARK.normal.text, PRIORITY_MARK.low.text]).size).toBe(3)
      await ui.unmount()
    })

    test(`a long title is kept whole and cut by the truncate-end wrap (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const [box] = await ui.findAll({ key: 'candidate-7-text' })
      const text = kids(box)[0]
      expect(textOf(text)).toBe(CANDIDATE_LINES[7].slice(2))
      expect(textOf(text).length).toBeGreaterThan(PANE_VIEW.props.bodyColumns)
      expect(text.props.wrap).toBe('truncate-end')
      await ui.unmount()
    })

    test(`the skeleton's commented rows draw no section (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates-skeleton'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(keysLike(lines, /^candidate/)).toEqual([])
    })
  }

  // Every fixture: the section draws only with no active row and at least
  // one candidate row, and then holds every row (M207 AC2).
  test('the domain holds an active fixture with candidate rows and an idle one without', () => {
    expect(WITH_ROADMAP.some(name => FIXTURES[name].pane.length > 0 && FIXTURES[name].candidates.length > 0)).toBe(true)
    expect(WITH_ROADMAP.some(name => FIXTURES[name].pane.length === 0 && FIXTURES[name].candidates.length === 0)).toBe(true)
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name}: candidates only while idle (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const { pane, candidates } = FIXTURES[name]
        if (pane.length > 0 || candidates.length === 0) {
          expect(keysLike(lines, /^candidate/)).toEqual([])
          return
        }
        expect(textAt(lines, 'candidates-head')).toBe(`▎ CANDIDATES ${candidates.length}`)
        expect(keysLike(lines, /^candidate-\d+$/).map(k => textAt(lines, k))).toEqual(
          candidates.map(row => `${PRIORITY_MARK[row.priority].text} ${row.title}`),
        )
      })
    }
  }
})

// M208: the operator's picked look. The values below are written out by
// hand from the fixtures.
const view = (bodyColumns: number) => ({ ...PANE_VIEW, props: { ...PANE_VIEW.props, bodyColumns } })
// The theme keys for implement, review, and plan, and the pill's text key
// (M217).
const IMPLEMENT_KEY = 'claude'
const REVIEW_KEY = 'success'
const PLAN_KEY = 'planMode'
const PILL_TEXT_KEY = 'inverseText'

async function mountPane($, surface: (typeof SURFACES)[number], bodyColumns = 60) {
  return (await $.ui.mount({ plugin: 'cairn', surface, ...view(bodyColumns) })) as Ui
}
async function boxOf(ui: Ui, key: string): Promise<Element | undefined> {
  return (await ui.findAll({ key }))[0]
}
// The Text children of a line's lead, text, or tail Box.
async function partOf(ui: Ui, key: string): Promise<Element[]> {
  const box = await boxOf(ui, key)
  return box === undefined ? [] : kids(box)
}

describe('the head line ends with the band percent (M208 AC1)', () => {
  // M002 as a review row: one checked criterion, one open, and one open box
  // inside a comment, which the band counts and the pane's items do not.
  // Band: review 1/3, so floor(100 × (1 + 1 + 1/3) / 3) = 77. Over the
  // pane's items it would be 1/2, so 83.
  const REVIEW_FILE = [
    '# M002: Add the export command',
    '',
    '## Goal',
    '',
    'Export things.',
    '',
    '## Acceptance criteria',
    '',
    '- [x] AC1: done.',
    '<!--',
    '- [ ] AC9: hidden in a comment.',
    '-->',
    '- [ ] AC2: open.',
    '',
    '## Tasks',
    '',
    '- [x] T1: Write the parser.',
    '',
  ].join('\n')
  const reviewCopy = () => {
    const copy = copyOf('single-in-progress')
    copy.files['/cairn/ROADMAP.md'] = copy.files['/cairn/ROADMAP.md'].replace(
      '| M002 | Add the export command | in-progress |',
      '| M002 | Add the export command | review |',
    )
    copy.files[M002] = REVIEW_FILE
    return copy
  }

  for (const surface of SURFACES) {
    test(`an in-progress row, a review row, and a row with no file (${surface})`, async ($, on) => {
      // pane-full: M080 in-progress, tasks 1/3, so floor(100 × (1 + 1/3) / 3) = 44.
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      expect((await partOf(ui, 'M080-head-tail')).map(textOf).join('')).toBe('  44%')
      // M082's file cannot be read: no percent, and its warning line stays.
      expect(await boxOf(ui, 'M082-head-tail')).toBe(undefined)
      expect(textOf((await partOf(ui, 'M082-nofile-text'))[0])).toBe(NO_FILE)
      // No track on any head line: no desktop Svg and no terminal braille.
      expect(await ui.findAll({ type: 'Svg' })).toEqual([])
      for (const id of ['M080', 'M081', 'M082']) {
        expect([id, /[⠀-⣿]/.test(textOf((await boxOf(ui, `${id}-head`)) as Element))]).toEqual([id, false])
      }
      await ui.unmount()
    })

    test(`a review row takes the band's count, not the pane's items (${surface})`, async ($, on) => {
      seat(on, reviewCopy())
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'M002-head')).toBe('review M002  Add the export command  77%')
      // The pane's own items hold two criteria, one checked.
      expect(keysLike(lines, /^M002-criterion-\d+$/).length).toBe(2)
    })

    test(`at 44 columns a long title leaves the percent in its own unshrinking Box (${surface})`, async ($, on) => {
      seat(on, copyOf('long-title'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface, 44)
      const head = await boxOf(ui, 'M060-head')
      if (head === undefined) throw new Error('no M060 head line')
      expect(kids(head).map(keyOf)).toEqual(['M060-head-lead', 'M060-head-text', 'M060-head-tail'])
      expect(kids(head)[2].props.flexShrink).toBe(0)
      const title = textOf(kids(await boxOf(ui, 'M060-head-text') as Element)[0])
      expect(title.length).toBeGreaterThan(44)
      expect((await partOf(ui, 'M060-head-tail')).map(textOf).join('')).toMatch(/^ {2}\d+%$/)
      await ui.unmount()
    })
  }
})

describe('the Tasks and Criteria headings draw eight squares (M208 AC2)', () => {
  for (const surface of SURFACES) {
    test(`partly checked and all checked (${surface})`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      // M080 tasks 1/3: three of eight filled, in the implement color.
      expect(textAt(lines, 'M080-tasks-head')).toBe('▎ TASKS 1/3 ■■■□□□□□')
      // M081 tasks 1/1: all eight filled.
      expect(textAt(lines, 'M081-tasks-head')).toBe('▎ TASKS 1/1 ■■■■■■■■')
      const ui = await mountPane($, surface)
      const lead = await partOf(ui, 'M080-tasks-head-lead')
      expect(lead.find(t => textOf(t) === '■■■')?.props.color).toBe(IMPLEMENT_KEY)
      expect(lead.find(t => textOf(t) === '□□□□□')?.props.color).toBe('subtle')
      const review = await partOf(ui, 'M081-tasks-head-lead')
      expect(review.find(t => textOf(t) === '■■■■■■■■')?.props.color).toBe(REVIEW_KEY)
      await ui.unmount()
    })

    test(`all open (${surface})`, async ($, on) => {
      // single-in-progress criteria 0/1: none filled.
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'M002-criteria-head')).toBe('▎ CRITERIA 0/1 □□□□□□□□')
      const ui = await mountPane($, surface)
      const lead = await partOf(ui, 'M002-criteria-head-lead')
      expect(lead.find(t => textOf(t) === '□□□□□□□□')?.props.color).toBe('subtle')
      expect(lead.some(t => textOf(t).includes('■'))).toBe(false)
      await ui.unmount()
    })
  }
})

describe('section headings and Next in the set-off form (M208 AC3)', () => {
  // The accent takes the phase color: the milestone's own for its sections
  // (M080 in implement, M081 in review), and plan's for the queue.
  const HEADS: [string, string, string, string][] = [
    ['pane-full', 'M080-goal-head', 'GOAL', IMPLEMENT_KEY],
    ['pane-full', 'M080-tasks-head', 'TASKS', IMPLEMENT_KEY],
    ['pane-full', 'M080-criteria-head', 'CRITERIA', IMPLEMENT_KEY],
    ['pane-full', 'M080-log-head', 'WORK LOG', IMPLEMENT_KEY],
    ['pane-full', 'M081-goal-head', 'GOAL', REVIEW_KEY],
    ['pane-full', 'M081-tasks-head', 'TASKS', REVIEW_KEY],
    ['pane-full', 'M081-criteria-head', 'CRITERIA', REVIEW_KEY],
    ['pane-full', 'M081-log-head', 'WORK LOG', REVIEW_KEY],
    ['pane-full', 'workable-head', 'WORKABLE', PLAN_KEY],
    ['pane-full', 'waiting-head', 'WAITING', PLAN_KEY],
    ['candidates', 'candidates-head', 'CANDIDATES', PLAN_KEY],
  ]
  for (const surface of SURFACES) {
    for (const [fixture, key, label, accent] of HEADS) {
      test(`${key} on ${fixture} (${surface})`, async ($, on) => {
        seat(on, copyOf(fixture))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        // A blank row comes right before the heading.
        const at = lines.findIndex(([k]) => k === key)
        expect(lines[at - 1]).toEqual([`${key}-gap`, ' '])
        const ui = await mountPane($, surface)
        const lead = await partOf(ui, `${key}-lead`)
        expect(textOf(lead[0])).toBe('▎')
        expect(lead[0].props.color).toBe(accent)
        expect(textOf(lead[2])).toBe(label)
        expect(lead[2].props).toEqual(expect.objectContaining({ color: 'inactive', bold: true }))
        await ui.unmount()
      })
    }

    // The pill takes the color of the phase its command runs.
    const PILLS: [string, string, string][] = [
      ['pane-full', ' /milestone-review M081 ', REVIEW_KEY],
      ['single-in-progress', ' /milestone-implement M002 ', IMPLEMENT_KEY],
      ['all-waiting', ' /milestone-plan ', PLAN_KEY],
    ]
    for (const [fixture, command, color] of PILLS) {
      test(`the Next command sits in a pill of its phase's color on ${fixture} (${surface})`, async ($, on) => {
        seat(on, copyOf(fixture))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const [pill] = await partOf(ui, 'next-text')
        expect(textOf(pill)).toBe(command)
        expect(pill.props).toEqual(expect.objectContaining({ backgroundColor: color, color: PILL_TEXT_KEY, bold: true }))
        await ui.unmount()
      })
    }
  }
})

// The test computes no layout, so it checks the widths the line keeps and
// the prop that lets the line shrink; the live look shows the drawing.
describe("each line's lead and tail fit a 44-column dock, and the line may shrink (M208 AC4)", () => {
  for (const surface of SURFACES) {
    for (const fixture of ['pane-full', 'candidates']) {
      test(`${fixture} (${surface})`, async ($, on) => {
        seat(on, copyOf(fixture))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface, 44)
        const [root] = await ui.findAll({ key: 'cairn-pane' })
        const lines = kids(root)
        expect(lines.length).toBeGreaterThan(10)
        for (const line of lines) {
          const key = keyOf(line) ?? ''
          const indent = (line.props.paddingLeft as number | undefined) ?? 0
          const sum = async (part: string) => (await partOf(ui, `${key}-${part}`)).map(t => width(textOf(t))).reduce((a, b) => a + b, 0)
          expect([key, indent + (await sum('lead')) + (await sum('tail')) <= 44]).toEqual([key, true])
          expect([key, line.props.minWidth]).toEqual([key, 0])
        }
        await ui.unmount()
      })
    }
  }
})

describe("the band's open button opens the pane (M205 AC4)", () => {
  for (const surface of SURFACES) {
    test(`a press opens pane cairn (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-open' })
      expect(copy.opens.map(open => open.id)).toEqual([PANE])
      expect(copy.open).toEqual([PANE])
      expect(copy.toasts ?? []).toEqual([])
      await ui.unmount()
    })

    test(`a press the surface does not place says why in a toast (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      copy.notPlaced = 'the attached surfaces place no panes'
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-open' })
      expect(copy.toasts).toEqual(['cairn pane not placed: the attached surfaces place no panes'])
      await ui.unmount()
    })

    // With no ROADMAP, a running cairn skill draws no row, so the band yields
    // the slot and draws neither button (M206 removed the skill row, which
    // drew the close button alone here).
    test(`a running skill with no ROADMAP yields the slot (${surface})`, async ($, on) => {
      seat(on, copyOf('no-roadmap'))
      await $.turn.complete(turn())
      await $.skill.prompt({ skill: 'cairn:milestone-plan', text: 'the plan prompt' })
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await ui.findAll({ key: 'cairn-stack' })).toEqual([])
      expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual([])
      expect(JSON.stringify(await ui.findAll({ type: 'Text' }))).toContain('engine slot')
      await ui.unmount()
    })
  }
})

// M218: the Next line's Button. Its label by the next step's action, and
// one fixture of each action, written out by hand.
const PANE_NEXT = 'cairn-pane-next'
const ACTION_LABELS: Record<string, string> = {
  implement: 'Start',
  resume: 'Resume',
  review: 'Review',
  'plan the next milestone': 'Plan',
}
const BY_ACTION: [string, string][] = [
  ['single-in-progress', 'resume'],
  ['states-review', 'review'],
  ['idle-order', 'implement'],
  ['all-waiting', 'plan the next milestone'],
]
// What a press runs for a fixture: `cairn:` and the command less its slash,
// and the id, or no args for planning.
function runOf(name: string): { command: string; args: string } {
  const next = FIXTURES[name].next as { command: string; id: string | null }
  return { command: `cairn:${next.command.slice(1)}`, args: next.id ?? '' }
}

describe("the Next line carries the next step's Button (M218 AC1)", () => {
  test('the fixtures reach every action', () => {
    expect([...new Set(WITH_ROADMAP.map(name => FIXTURES[name].next?.action))].sort()).toEqual(Object.keys(ACTION_LABELS).sort())
    expect(BY_ACTION.map(([name]) => FIXTURES[name].next?.action)).toEqual(BY_ACTION.map(([, action]) => action))
  })

  // An action named like an object property has no label, so its line
  // carries no action (M218 review).
  test('an action outside the map, an inherited property name among them, has no label', () => {
    for (const action of Object.keys(ACTION_LABELS)) expect([action, nextLabel(action)]).toEqual([action, ACTION_LABELS[action]])
    for (const action of ['toString', 'constructor', '__proto__', 'hasOwnProperty', 'blocked']) {
      expect([action, nextLabel(action)]).toEqual([action, undefined])
      const state: PaneState = {
        found: true,
        milestones: [],
        next: { action, command: '/milestone-plan', id: null, waiting: [] },
        workable: [],
        waiting: [],
        candidates: [],
      }
      const next = layout(state, [], true).find(line => line.key === 'next')
      expect([action, next?.action]).toEqual([action, undefined])
    }
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const buttons = await ui.findAll({ type: 'Button' })
        expect(buttons.map(keyOf)).toEqual([PANE_NEXT])
        const want = ACTION_LABELS[FIXTURES[name].next?.action as string]
        expect([buttons[0].props.label, buttons[0].props.variant]).toEqual([want, 'secondary'])
        // The Button comes after the pill, in the Next line's last Box.
        const line = (await boxOf(ui, 'next')) as Element
        expect(kids(line).map(keyOf)).toEqual(['next-lead', 'next-text', 'next-action'])
        expect(kids(kids(line)[2]).map(keyOf)).toEqual([PANE_NEXT])
        await ui.unmount()
      })
    }
  }
})

describe("a running cairn skill hides the pane's Button (M218 AC2)", () => {
  for (const surface of SURFACES) {
    test(`the Button goes at a skill's prompt and comes back at its Stop (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const pill = async () => textOf((await partOf(ui, 'next-text'))[0])
      expect((await ui.findAll({ key: PANE_NEXT })).length).toBe(1)
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      expect(await ui.findAll({ key: PANE_NEXT })).toEqual([])
      expect(await pill()).toBe(' /milestone-implement M002 ')
      await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
      expect((await ui.findAll({ key: PANE_NEXT })).length).toBe(1)
      expect(await pill()).toBe(' /milestone-implement M002 ')
      await ui.unmount()
    })
  }
})

describe("a press of the pane's Button runs the next command (M218 AC3)", () => {
  for (const [name] of BY_ACTION) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf(name)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        await ui.press({ key: PANE_NEXT })
        expect(copy.commands).toEqual([runOf(name)])
        await ui.unmount()
      })
    }
  }

  // The runs written out by hand for two of them.
  test('the runs for planning and for a milestone', () => {
    expect(runOf('all-waiting')).toEqual({ command: 'cairn:milestone-plan', args: '' })
    expect(runOf('single-in-progress')).toEqual({ command: 'cairn:milestone-implement', args: 'M002' })
  })

  for (const surface of SURFACES) {
    test(`a second press during a held run reaches no second run (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      let release = () => {}
      copy.runHold = new Promise<void>(resolve => {
        release = resolve
      })
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const first = ui.press({ key: PANE_NEXT })
      try {
        for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
        expect(copy.commands).toEqual([runOf('single-in-progress')])
        await ui.press({ key: PANE_NEXT })
        expect(copy.commands).toEqual([runOf('single-in-progress')])
      } finally {
        release()
        await first
      }
      // The settled run frees the Button, so the next press runs again
      // (M218 review).
      copy.runHold = undefined
      await ui.press({ key: PANE_NEXT })
      expect(copy.commands).toEqual([runOf('single-in-progress'), runOf('single-in-progress')])
      await ui.unmount()
    })
  }
})

describe('the pill gives way before the Button (M218 AC4)', () => {
  for (const surface of SURFACES) {
    test(`the Button's Box does not shrink, and the pill's does (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const action = (await boxOf(ui, 'next-action')) as Element
      expect(action.props.flexShrink).toBe(0)
      const pill = (await boxOf(ui, 'next-text')) as Element
      expect([pill.props.flexShrink, pill.props.minWidth]).toEqual([1, 0])
      await ui.unmount()
    })
  }
})

// M002's task T2 is open in the fixture, and each case ticks it before the
// event, so the drawing after the event shows it checked.
const M002 = '/cairn/milestones/M002-export.md'
const T2_OPEN = `${OPEN_MARK} T2: Write the command.`
const T2_DONE = `${CHECKED_MARK} T2: Write the command.`
const tick = (copy: Copy) => {
  copy.files[M002] = copy.files[M002].replace('- [ ] T2:', '- [x] T2:')
}

type Event = { name: string; before?: ($) => Promise<void>; act: ($) => Promise<void> }

const EVENTS: Event[] = [
  { name: 'session start', act: $ => $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true }) },
  { name: 'turn end', act: $ => $.turn.complete(turn()) },
  { name: 'cairn skill prompt', act: $ => $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' }) },
  {
    name: 'Stop that ends a step',
    before: $ => $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' }),
    act: $ => $.classic.Stop({ stop_hook_active: false, background_tasks: [] }),
  },
  {
    name: 'idle typed prompt that ends a step',
    before: async $ => {
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      // A Stop with work in flight keeps the step and reads no files.
      await $.classic.Stop({
        stop_hook_active: false,
        background_tasks: [{ id: 'b1', type: 'subagent', status: 'running', description: 'a reviewer', agent_type: 'general-purpose' }],
      })
    },
    act: $ => $.prompt.submit({ text: 'a typed prompt', wait: false, origin: { kind: 'composer' } }),
  },
]

describe('an open pane draws again at each refresh the band takes (M205 AC5)', () => {
  for (const event of EVENTS) {
    // One pane stays mounted across the event, so the case shows that the
    // drawing already open changes, not only a new one (M205 review).
    test(`the ${event.name} shows an edit made before it`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      if (event.before !== undefined) await event.before($)
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...PANE_VIEW })) as Ui
      const t2 = async () => textOf((await ui.findAll({ key: 'M002-task-1' }))[0])
      expect(await t2()).toBe(T2_OPEN)
      tick(copy)
      // The edit alone draws nothing new.
      expect(await t2()).toBe(T2_OPEN)
      await event.act($)
      expect(await t2()).toBe(T2_DONE)
      await ui.unmount()
    })
  }
})
