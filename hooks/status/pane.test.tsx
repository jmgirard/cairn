import { describe, expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { FIXTURES } from './fixtures.gen'
import { flowOf, width } from './band'
import { CHECKED_MARK, COMMAND_PHASE, NO_FILE, NO_ROADMAP, OPEN_MARK, PRIORITY_MARK, nextLabel, paneLines as layout, prWord } from './pane'
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
  // The project root `$.session.root()` answers, when it differs from the
  // cwd (M222 review).
  root?: string
  // When set, every open is refused with this reason.
  refuse?: string
  // The command and args of each slash command run that reached beneath the
  // mod, and while set, a promise each run waits for before it answers
  // (M218).
  commands?: { command: string; args: string }[]
  runHold?: Promise<void>
  // While set, a slash command run beneath the mod throws this message
  // (M221 review).
  runThrows?: string
  // While set, the path of each `$.fs.read` call is pushed here (M236).
  reads?: string[]
  // While set, `$.ui.panes()` beneath the mod throws (M237).
  panesThrow?: boolean
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

// What `$.ui.panes()` answers the mod: the open panes, each shown unless it
// sits behind another pane's tab, and placed unless it waits undrawn.
function panesOf(copy: Copy) {
  return copy.open.map(id => ({
    id,
    title: id,
    isShown: !(copy.hidden ?? []).includes(id),
    isFocused: false,
    isPlaced: !(copy.unplaced ?? []).includes(id),
  }))
}

function seat(on: On, copy: Copy) {
  const has = (path: string) => Object.prototype.hasOwnProperty.call(copy.files, path)
  on('session.cwd', async () => ({ value: copy.cwd }))
  on('session.root', async () => ({ value: copy.root ?? copy.cwd }))
  on('fs.stat', async ($, e, next) =>
    has(e.path) ? { value: { kind: 'file', size: copy.files[e.path].length, mtimeMs: 0, isLink: false } } : next(e),
  )
  on('fs.read', async ($, e, next) => {
    copy.reads?.push(e.path)
    return has(e.path) && !copy.unreadable.includes(e.path) ? { value: copy.files[e.path] } : next(e)
  })
  on('fs.list', async ($, e, next) => {
    const names = listNames(Object.keys(copy.files), e.path)
    if (names === null) return next(e)
    return { value: names.map(name => ({ name, kind: 'other', size: 0, mtimeMs: 0, isLink: false })) }
  })
  on('session.start', async ($, e) => ({ cwd: e.cwd }))
  on('turn.complete', async () => ({ text: '' }))
  on('classic.Stop', async () => ({}))
  on('classic.SessionStart', async () => ({}))
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
  on('ui.panes', async () => {
    if (copy.panesThrow === true) throw new Error('no panes')
    return { value: panesOf(copy) }
  })
  on('ui.toast', async ($, e) => {
    copy.toasts = [...(copy.toasts ?? []), e.text]
    return { value: undefined }
  })
  on('command.run', async ($, e) => {
    copy.commands = [...(copy.commands ?? []), { command: e.command, args: e.args }]
    if (copy.runHold !== undefined) await copy.runHold
    if (copy.runThrows !== undefined) throw new Error(copy.runThrows)
    return { text: '' }
  })
  // The session end a `/clear` brings, which runs the command a Plan or
  // Implement press holds (M221).
  on('session.end', async ($, e) => ({ sessionId: e.sessionId }))
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

// The Buttons under a node, in order (M219).
function buttonsIn(node: Element): Element[] {
  return kids(node).flatMap(child => (child.type === 'Button' ? [child] : buttonsIn(child)))
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
          expect(textAt(lines, `${row.id}-head`)).toBe(`${row.id}  ${row.title}${tail}`)
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

// The blocked-prs fixture's lines, written out by hand from its milestone
// files (M223 AC1, AC2): one URL, the first of two URLs, a URL only after a
// `companion:` entry, a URL with a trailing path, no URL, a failed read, and
// a missing file.
const BLOCKED_LINES = [
  'M101  One pull request URL  #12',
  'M102  Two pull request URLs  #34',
  'M103  A URL only after a companion entry',
  'M104  A URL with a trailing path  #90',
  'M105  A branch with no URL',
  'M106  A file whose read fails',
  'M107  A missing file',
]
const blockedLine = (row: { id: string; title: string; pr: number | null }) =>
  `${row.id}  ${row.title}${row.pr === null ? '' : `  #${row.pr}`}`

describe('the pane lists the blocked milestones and their PRs (M223 AC1, AC2)', () => {
  test('the domain holds blocked rows with and without an active milestone, and fixtures with none', () => {
    expect(FIXTURES['blocked-prs'].pane.length).toBe(0)
    expect(FIXTURES['blocked-prs'].unreadable).toEqual(['/cairn/milestones/M106-unreadable.md'])
    expect(Object.keys(FIXTURES['blocked-prs'].files)).not.toContain('/cairn/milestones/M107-missing.md')
    expect(FIXTURES['blocked-active'].pane.length).toBeGreaterThan(0)
    expect(FIXTURES['blocked-active'].blocked.length).toBeGreaterThan(0)
    expect(WITH_ROADMAP.some(name => FIXTURES[name].blocked.length === 0)).toBe(true)
  })

  for (const surface of SURFACES) {
    test(`blocked-prs: the heading, each row, and its number (${surface})`, async ($, on) => {
      seat(on, copyOf('blocked-prs'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'blocked-head')).toBe('▎ BLOCKED 7')
      expect(keysLike(lines, /^blocked-M/).map(k => textAt(lines, k))).toEqual(BLOCKED_LINES)
      // After the queue's place and before the candidates.
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('blocked-head')).toBeGreaterThan(at('next'))
      expect(at('candidates-head')).toBeGreaterThan(at('blocked-M107'))
    })

    test(`blocked-active: the section beside an active milestone (${surface})`, async ($, on) => {
      seat(on, copyOf('blocked-active'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'M110-head')).toBeDefined()
      expect(keysLike(lines, /^blocked-M/).map(k => textAt(lines, k))).toEqual(['M111  Handed to the maintainers  #1250'])
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('blocked-head')).toBeGreaterThan(at('next'))
      // After the Workable rows (M223 review).
      expect(at('workable-M112')).toBeGreaterThan(at('next'))
      expect(at('blocked-head')).toBeGreaterThan(at('workable-M112'))
    })

    test(`all-waiting: the section follows the Waiting rows (${surface})`, async ($, on) => {
      seat(on, copyOf('all-waiting'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('blocked-head')).toBeGreaterThan(at('waiting-M093'))
      expect(textAt(lines, 'blocked-M092')).toBe('M092  Blocked outside')
    })

    test(`the number sits in the line's tail (${surface})`, async ($, on) => {
      seat(on, copyOf('blocked-active'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const [tail] = await ui.findAll({ key: 'blocked-M111-tail' })
      expect(textOf(tail)).toBe('  #1250')
      await ui.unmount()
    })
  }

  // Every fixture: the section holds each blocked row in ROADMAP order, and
  // a fixture with none draws no section.
  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name}: blocked rows (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const { blocked } = FIXTURES[name]
        if (blocked.length === 0) {
          expect(keysLike(lines, /^blocked/)).toEqual([])
          return
        }
        expect(textAt(lines, 'blocked-head')).toBe(`▎ BLOCKED ${blocked.length}`)
        expect(keysLike(lines, /^blocked-M/).map(k => textAt(lines, k))).toEqual(blocked.map(blockedLine))
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
      expect(textAt(lines, 'M002-head')).toBe('M002  Add the export command  77%')
      // The pane's own items hold two criteria, one checked.
      expect(keysLike(lines, /^M002-criterion-\d+$/).length).toBe(2)
    })

    test(`at 44 columns a long title leaves the percent in its own unshrinking Box (${surface})`, async ($, on) => {
      seat(on, copyOf('long-title'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface, 44)
      const head = await boxOf(ui, 'M060-head')
      if (head === undefined) throw new Error('no M060 head line')
      // The first line also carries the ↻ Box after the tail (M236).
      expect(kids(head).map(keyOf)).toEqual(['M060-head-lead', 'M060-head-text', 'M060-head-tail', 'M060-head-refresh'])
      expect(kids(head)[2].props.flexShrink).toBe(0)
      expect(kids(head)[3].props.flexShrink).toBe(0)
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
    ['blocked-prs', 'blocked-head', 'BLOCKED', PLAN_KEY],
    ['blocked-active', 'blocked-head', 'BLOCKED', PLAN_KEY],
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
    for (const fixture of ['pane-full', 'candidates', 'blocked-prs', 'blocked-active']) {
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
  implement: 'Implement',
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

// The next actions whose Button runs `/clear` first, and its command only
// at the session end the clear brings (M221).
const CLEARS_FIRST = ['implement', 'plan the next milestone']
const CLEAR_END = { reason: 'clear', sessionId: 's1' } as const

// Waits until `n` slash command runs reached beneath the mod, for at most
// `tries` waits of 5 ms, and then once more, so the last run settles (M221).
async function untilRuns(copy: Copy, n: number, tries = 200) {
  for (let i = 0; i < tries && (copy.commands ?? []).length < n; i++) await new Promise(resolve => setTimeout(resolve, 5))
  await new Promise(resolve => setTimeout(resolve, 5))
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
        blocked: [],
      }
      const next = layout(state, [], true).find(line => line.key === 'next')
      expect([action, next?.action]).toEqual([action, undefined])
      // Nor Status and Clear, which show only with the next-step Button
      // (M219 review).
      expect([action, layout(state, [], true, true).find(line => line.key === 'next')?.buttons]).toEqual([action, undefined])
    }
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        // The Next line's first Button: Status follows it (M219).
        const buttons = buttonsIn((await boxOf(ui, 'next')) as Element)
        expect(keyOf(buttons[0])).toBe(PANE_NEXT)
        expect(buttons.filter(button => keyOf(button) === PANE_NEXT).length).toBe(1)
        const want = ACTION_LABELS[FIXTURES[name].next?.action as string]
        expect([buttons[0].props.label, buttons[0].props.variant]).toEqual([want, 'secondary'])
        // The Button comes after the pill, in the Box after the pill's.
        const line = (await boxOf(ui, 'next')) as Element
        expect(kids(line).map(keyOf).slice(0, 3)).toEqual(['next-lead', 'next-text', 'next-action'])
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
        // Plan and Implement run `/clear`, and their command at the clear's
        // session end (M221).
        if (CLEARS_FIRST.includes(FIXTURES[name].next?.action as string)) {
          await $.session.end(CLEAR_END)
          await untilRuns(copy, 2)
          expect(copy.commands).toEqual([CLEAR_RUN, runOf(name)])
        } else {
          expect(copy.commands).toEqual([runOf(name)])
        }
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

// M219: the Next line's Status and Clear Buttons, with their keys and
// labels written out by hand.
const PANE_STATUS = 'cairn-pane-status'
const PANE_CLEAR = 'cairn-pane-clear'
const PANE_REFRESH = 'cairn-pane-refresh'
const STATUS_RUN = { command: 'cairn:milestone', args: '' }
const CLEAR_RUN = { command: 'clear', args: '' }

// The keys of the Next line's Buttons, in order, or null with no Next line.
async function nextKeys(ui: Ui): Promise<string[] | null> {
  const line = await boxOf(ui, 'next')
  return line === undefined ? null : buttonsIn(line).map(button => keyOf(button) as string)
}

// A cairn skill runs and its Stop ends the step, which leaves `ended` set.
async function endSkill($) {
  await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
  await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
}

describe('the Next line carries the Status Button after Next (M219 AC1)', () => {
  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
        expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
        // No other line of the pane carries a Button (M219 review), but for
        // the ↻ Refresh on the first line (M236). Before any read, no
        // blocked line carries one.
        expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual([PANE_REFRESH, PANE_NEXT, PANE_STATUS])
        const [status] = await ui.findAll({ key: PANE_STATUS })
        expect([status.props.variant, status.props.label]).toEqual(['secondary', 'Status'])
        // The Buttons come after the pill, each in its own Box.
        const line = (await boxOf(ui, 'next')) as Element
        expect(kids(line).map(keyOf)).toEqual(['next-lead', 'next-text', 'next-action', 'next-status'])
        await ui.unmount()
      })
    }
  }
})

describe('a running skill hides Status, and its end adds Clear (M219 AC2)', () => {
  for (const surface of SURFACES) {
    test(`skill prompt, Stop, then an idle typed prompt (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      expect(await ui.findAll({ key: PANE_STATUS })).toEqual([])
      expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
      await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_CLEAR, PANE_STATUS])
      const [clear] = await ui.findAll({ key: PANE_CLEAR })
      expect([clear.props.variant, clear.props.label]).toEqual(['secondary', 'Clear'])
      await $.prompt.submit({ text: 'a typed prompt', wait: false, origin: { kind: 'composer' } })
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
      expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
      await ui.unmount()
    })
  }
})

describe('a press of Status or Clear runs its command (M219 AC3)', () => {
  for (const surface of SURFACES) {
    test(`Status runs the status skill (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      await ui.press({ key: PANE_STATUS })
      expect(copy.commands).toEqual([STATUS_RUN])
      await ui.unmount()
    })

    test(`Clear, drawn after a Stop ends a step, runs clear (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      await endSkill($)
      const ui = await mountPane($, surface)
      await ui.press({ key: PANE_CLEAR })
      expect(copy.commands).toEqual([CLEAR_RUN])
      await ui.unmount()
    })

    test(`a Status press while a Next run is held runs nothing (${surface})`, async ($, on) => {
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
        await ui.press({ key: PANE_STATUS })
        expect(copy.commands).toEqual([runOf('single-in-progress')])
      } finally {
        release()
        await first
      }
      await ui.unmount()
    })
  }
})

// The pane fixtures whose next action is planning or implement (M221 AC1,
// AC2).
const PANE_CLEAR_FIRST = WITH_ROADMAP.filter(name => CLEARS_FIRST.includes(FIXTURES[name].next?.action as string))

describe("the pane's Plan and Implement run /clear and then their command (M221 AC1, AC2)", () => {
  test('the cases reach both actions', () => {
    expect([...new Set(PANE_CLEAR_FIRST.map(name => FIXTURES[name].next?.action))].sort()).toEqual([...CLEARS_FIRST].sort())
  })

  for (const name of PANE_CLEAR_FIRST) {
    for (const surface of SURFACES) {
      test(`${name}: clear, no second press adds a run, then the command at the clear's end (${surface})`, async ($, on) => {
        const copy = copyOf(name)
        seat(on, copy)
        await $.turn.complete(turn())
        // A skill that ended leaves Clear drawn too, so every action Button
        // is pressed below.
        await endSkill($)
        const ui = await mountPane($, surface)
        expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_CLEAR, PANE_STATUS])
        const [next] = await ui.findAll({ key: PANE_NEXT })
        expect(next.props.label).toBe(ACTION_LABELS[FIXTURES[name].next?.action as string])
        await ui.press({ key: PANE_NEXT })
        expect(copy.commands).toEqual([CLEAR_RUN])
        for (const key of [PANE_NEXT, PANE_CLEAR, PANE_STATUS]) await ui.press({ key })
        await untilRuns(copy, 2, 10)
        expect(copy.commands).toEqual([CLEAR_RUN])
        await $.session.end(CLEAR_END)
        await untilRuns(copy, 2)
        expect(copy.commands).toEqual([CLEAR_RUN, runOf(name)])
        await ui.unmount()
      })
    }
  }

  // M221 review: a refused clear in the pane runs nothing at the clear's
  // end, and the toast names /clear, as on the band.
  for (const surface of SURFACES) {
    test(`all-waiting: a refused clear runs nothing at the clear's end (${surface})`, async ($, on) => {
      const copy = copyOf('all-waiting')
      copy.runThrows = 'no such command here'
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      await ui.press({ key: PANE_NEXT })
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([CLEAR_RUN])
      expect(copy.toasts?.length).toBe(1)
      expect(copy.toasts?.[0]).toMatch(/^cairn: .* \(\/clear\)$/)
      await ui.unmount()
    })
  }
})

describe('the pill gives way before Clear and Status (M219 AC4)', () => {
  for (const surface of SURFACES) {
    test(`the Buttons' Boxes do not shrink, and the pill's does (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      await endSkill($)
      const ui = await mountPane($, surface)
      for (const key of ['next-clear', 'next-status']) {
        const box = (await boxOf(ui, key)) as Element
        expect([key, box.props.flexShrink]).toEqual([key, 0])
      }
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
  // A press of a Clear Button raises no `session.start`, only this (M222).
  { name: 'session start after a clear', act: $ => $.classic.SessionStart({ source: 'clear' }) },
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

// The pane across a `/clear` (M222). A press of a Clear Button ends the
// session with reason `clear` in the same process, and nothing closes the
// pane. A typed `/clear` in the desktop app ends the process with reason
// `other`, and the next process starts with no pane at the first message
// after the clear. Each case answers `$.store` from memory, which outlives
// the process as the engine's store does, and empties the open panes
// between an end and the next start, so it sees only what the mod opens.
// The panes a case reads are what `$.ui.panes()` answers the mod.
const NEW_START = { cwd: '/', surface: 'desktop', isInteractive: true } as const
const listed = (copy: Copy) => copy.open.includes(PANE)
const newProcess = (copy: Copy) => {
  copy.open = []
  copy.hidden = []
  copy.unplaced = []
}

async function openPane($, on, copy: Copy) {
  mock.store(on)
  seat(on, copy)
  await $.session.start(NEW_START)
  await $.command.run({ command: COMMAND })
  expect(listed(copy)).toBe(true)
}

describe('a clear end leaves the pane open (M222 AC1, AC2)', () => {
  const STATES = [
    { name: 'shown', set: (copy: Copy) => copy },
    { name: "behind another pane's tab", set: (copy: Copy) => { copy.hidden = [PANE] } },
    { name: 'waiting undrawn', set: (copy: Copy) => { copy.unplaced = [PANE] } },
  ]
  for (const state of STATES) {
    test(`a pane ${state.name} at a clear end is listed after it`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      await openPane($, on, copy)
      state.set(copy)
      await $.session.end(CLEAR_END)
      expect(copy.closes).toEqual([])
      const mine = panesOf(copy).find(open => open.id === PANE)
      expect(mine).toBeDefined()
      if (state.name === 'shown') {
        expect(mine?.isShown).toBe(true)
        expect(mine?.isPlaced).toBe(true)
      }
    })
  }

  test('a clear end with no pane open leaves none open', async ($, on) => {
    const copy = copyOf('single-in-progress')
    mock.store(on)
    seat(on, copy)
    await $.session.start(NEW_START)
    await $.session.end(CLEAR_END)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })
})

describe('an end of another kind opens no pane at the next start (M222 AC3)', () => {
  for (const reason of ['resume', 'prompt_input_exit', 'logout'] as const) {
    test(`after a ${reason} end, the next start opens no pane`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      await openPane($, on, copy)
      await $.session.end({ reason, sessionId: 's1' })
      newProcess(copy)
      await $.session.start(NEW_START)
      expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
    })
  }
})

describe('an other end with the pane shown opens it at the next start in the same cwd (M222 AC7)', () => {
  const OTHER_END = { reason: 'other', sessionId: 's1' } as const

  test('the same cwd lists the pane at the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).toContain(PANE)
  })

  test('a shell cd before the end still lists the pane at the next start in the root', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    copy.root = copy.cwd
    copy.cwd = '/sub'
    await $.session.end(OTHER_END)
    newProcess(copy)
    copy.cwd = copy.root
    copy.root = undefined
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).toContain(PANE)
  })

  for (const state of ['hidden', 'unplaced'] as const) {
    test(`a pane ${state} at the end lists none at the next start`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      await openPane($, on, copy)
      copy[state] = [PANE]
      await $.session.end(OTHER_END)
      newProcess(copy)
      await $.session.start(NEW_START)
      expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
    })
  }

  test('a clear end marks nothing for the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(CLEAR_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })

  test('another cwd lists no pane at the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    copy.cwd = '/sub'
    await $.session.start({ ...NEW_START, cwd: '/sub' })
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })

  test('no pane open at the end lists none at the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    mock.store(on)
    seat(on, copy)
    await $.session.start(NEW_START)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })

  // A typed `/clear` closes the pane on screen, so a `/cairn-pane` that is
  // the first message after it is a request to open, though the start that
  // message brings has just reopened the pane. It keeps the pane open, and
  // the next one closes it.
  test('a /cairn-pane that is the first message after the reopen keeps the pane open', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(listed(copy)).toBe(true)
    const first = await $.command.run({ command: COMMAND })
    expect(first.text).toBe('cairn pane opened')
    expect(listed(copy)).toBe(true)
    const second = await $.command.run({ command: COMMAND })
    expect(second.text).toBe('cairn pane closed')
    expect(listed(copy)).toBe(false)
  })

  test('after a turn ends, a /cairn-pane closes the reopened pane', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    await $.turn.complete(turn())
    const got = await $.command.run({ command: COMMAND })
    expect(got.text).toBe('cairn pane closed')
    expect(listed(copy)).toBe(false)
  })

  test('a start with no reopen leaves the first /cairn-pane a close of a shown pane', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    const got = await $.command.run({ command: COMMAND })
    expect(got.text).toBe('cairn pane closed')
    expect(listed(copy)).toBe(false)
  })

  test('the reopen happens once: a close and a later exit end list no pane', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(listed(copy)).toBe(true)
    await $.turn.complete(turn())
    await $.command.run({ command: COMMAND })
    expect(listed(copy)).toBe(false)
    await $.session.end({ reason: 'prompt_input_exit', sessionId: 's2' })
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })
})

// Each blocked line's pull request state (M224). A case answers the mod's
// `gh pr view` calls from `answer`, by the URL each call names, and records
// each call's argv and each `$.clock` wait the mod asks for. A `reject`
// answer throws, so the engine skips the hook and the mod's call rejects,
// as it does when `gh` cannot start. The words and Buttons each case expects
// are written out by hand.
// The `gh api graphql` calls of M225 are recorded apart in `graphql`, and
// `graph` answers them by the URL that the call's owner, repo, and number
// name, by default with a reply whose counts are both zero. Its answer may
// be a promise, which holds the call until it settles.
// The `git` calls and the `gh pr list` calls of M226 are recorded apart too,
// in `git` and `lists`. `git` answers from `remotes`, a remote's URL by its
// name, and by default the repo has no remote, so no list call runs.
// `list` answers each `gh pr list` call.
// An open does not wait for the read (M230), so a case waits with
// `settled` until no `process.run` call is in flight at four checks 5 ms
// apart, or until 400 checks (about 2 s) pass. The
// `answer` and `list` answers may be promises too, which hold their calls.
type GhAnswer = { exitCode: number; stdout: string } | 'reject'
type Gh = {
  calls: (readonly string[])[]
  graphql: (readonly string[])[]
  git: (readonly string[])[]
  lists: (readonly string[])[]
  clocks: string[]
  settled: () => Promise<void>
}
type GhRepo = { remotes?: Record<string, string>; list?: () => GhAnswer | Promise<GhAnswer> }
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))
// The newest `gh` set-up's `settled`, which the drawing helpers below wait
// on before they mount the pane. It holds one set-up only, the newest.
let ghSettled: () => Promise<void> = async () => {}
const URL_1250 = 'https://github.com/upstream/repo/pull/1250'
const LINE_1250 = 'M111  Handed to the maintainers  #1250'

// The value of a `name=value` argument in a recorded argv.
const argOf = (argv: readonly string[], name: string) => argv.find(a => a.startsWith(`${name}=`))?.slice(name.length + 1)

function gh(
  on: On,
  answer: (url: string) => GhAnswer | Promise<GhAnswer>,
  graph: (url: string) => GhAnswer | Promise<GhAnswer> = () => countsReply(0),
  repo: GhRepo = {},
): Gh {
  let pending = 0
  const settled = async () => {
    for (let quiet = 0, i = 0; quiet < 4 && i < 400; i++) {
      await sleep(5)
      quiet = pending === 0 ? quiet + 1 : 0
    }
  }
  const out: Gh = { calls: [], graphql: [], git: [], lists: [], clocks: [], settled }
  ghSettled = settled
  const remotes = repo.remotes ?? {}
  const value = (got: { exitCode: number; stdout: string }) => ({
    value: { exitCode: got.exitCode, stdout: got.stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false },
  })
  const reply = async (e: { argv: readonly string[] }) => {
    if (e.argv[0] === 'git') {
      out.git.push(e.argv)
      if (e.argv[1] === 'remote' && e.argv.length === 2) return value({ exitCode: 0, stdout: Object.keys(remotes).map(n => `${n}\n`).join('') })
      const name = e.argv[3]
      const has = Object.prototype.hasOwnProperty.call(remotes, name)
      return value(has ? { exitCode: 0, stdout: `${remotes[name]}\n` } : { exitCode: 2, stdout: '' })
    }
    if (e.argv[1] === 'pr' && e.argv[2] === 'list') {
      out.lists.push(e.argv)
      const got = await (repo.list ?? (() => ({ exitCode: 0, stdout: '[]\n' })))()
      if (got === 'reject') throw new Error('gh cannot start')
      return value(got)
    }
    const isGraph = e.argv[1] === 'api'
    if (isGraph) out.graphql.push(e.argv)
    else out.calls.push(e.argv)
    const url = `https://github.com/${argOf(e.argv, 'owner')}/${argOf(e.argv, 'repo')}/pull/${argOf(e.argv, 'number')}`
    const got = isGraph ? await graph(url) : await answer(e.argv[3])
    if (got === 'reject') throw new Error('gh cannot start')
    return value(got)
  }
  on('process.run', async ($, e) => {
    pending += 1
    try {
      return await reply(e)
    } finally {
      pending -= 1
    }
  })
  for (const name of ['clock.sleep', 'clock.after', 'clock.every'] as const) {
    on(name, async () => {
      out.clocks.push(name)
      return { value: undefined }
    })
  }
  return out
}

const prView = (state: string, decision?: string) =>
  ({ exitCode: 0, stdout: `${JSON.stringify(decision === undefined ? { state } : { state, reviewDecision: decision })}\n` }) as const

// A `gh api graphql` reply in the shape GitHub returns (M236), with `t`
// unresolved threads and one resolved.
function countsReply(t: number): GhAnswer {
  const pr = { reviewThreads: { nodes: [{ isResolved: true }, ...Array.from({ length: t }, () => ({ isResolved: false }))] } }
  return { exitCode: 0, stdout: `${JSON.stringify({ data: { repository: { pullRequest: pr } } })}\n` }
}

// The pane's line for a key, and the keys of the Buttons on it.
async function blockedView($, key: string): Promise<{ text: string; buttons: string[] }> {
  await ghSettled()
  const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const line = kids(root).find(child => keyOf(child) === key)
  await ui.unmount()
  return { text: line === undefined ? '' : textOf(line), buttons: line === undefined ? [] : buttonsIn(line).map(b => keyOf(b) ?? '') }
}

describe('each blocked line shows its pull request state (M224 AC1)', () => {
  const SHAPES: { name: string; answer: GhAnswer; word: string }[] = [
    { name: 'MERGED', answer: prView('MERGED', 'APPROVED'), word: 'merged' },
    { name: 'CLOSED', answer: prView('CLOSED', ''), word: 'closed' },
    { name: 'OPEN with CHANGES_REQUESTED', answer: prView('OPEN', 'CHANGES_REQUESTED'), word: 'changes requested' },
    { name: 'OPEN with APPROVED', answer: prView('OPEN', 'APPROVED'), word: 'approved' },
    { name: 'OPEN with REVIEW_REQUIRED', answer: prView('OPEN', 'REVIEW_REQUIRED'), word: 'in review' },
    { name: 'OPEN with an empty decision', answer: prView('OPEN', ''), word: 'in review' },
    { name: 'OPEN with no decision', answer: prView('OPEN'), word: 'in review' },
  ]
  for (const shape of SHAPES) {
    test(`${shape.name} shows \`${shape.word}\``, async ($, on) => {
      const calls = gh(on, () => shape.answer)
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      const opened = await $.command.run({ command: COMMAND })
      expect(opened.text).toBe('cairn pane opened')
      await calls.settled()
      expect(calls.calls).toEqual([['gh', 'pr', 'view', URL_1250, '--json', 'state,reviewDecision']])
      expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  ${shape.word}`)
    })
  }

  test('a line not yet read shows no state word and no Button', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.calls).toEqual([])
    const line = await blockedView($, 'blocked-M111')
    expect(line.text).toBe(LINE_1250)
    expect(line.buttons).toEqual([])
  })
})

describe('the merged, changes-requested, and closed lines carry a Button (M224 AC2)', () => {
  const BUTTONS = [
    { answer: prView('MERGED', ''), key: 'cairn-pane-finish-M111', command: { command: 'cairn:milestone-review', args: 'M111' } },
    {
      answer: prView('OPEN', 'CHANGES_REQUESTED'),
      key: 'cairn-pane-revise-M111',
      command: { command: 'cairn:milestone-implement', args: 'M111' },
    },
    { answer: prView('CLOSED', ''), key: 'cairn-pane-check-M111', command: { command: 'cairn:milestone', args: '' } },
  ]
  for (const each of BUTTONS) {
    test(`${each.key} runs /${each.command.command} with no /clear first`, async ($, on) => {
      gh(on, () => each.answer)
      const copy = copyOf('blocked-active')
      seat(on, copy)
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      expect((await blockedView($, 'blocked-M111')).buttons).toEqual([each.key])
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      await ui.press({ key: each.key })
      await ui.unmount()
      expect(copy.commands).toEqual([each.command])
    })
  }

  // A press while a cairn skill's step runs does nothing, as the Next,
  // Status, and Clear presses do (M224 review). The Button stays drawn.
  test('a press while a cairn skill runs runs nothing', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await ui.press({ key: 'cairn-pane-finish-M111' })
    await ui.unmount()
    expect(copy.commands ?? []).toEqual([])
    // After the step ends, the same press runs its command.
    await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
    const after = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await after.press({ key: 'cairn-pane-finish-M111' })
    await after.unmount()
    expect(copy.commands).toEqual([{ command: 'cairn:milestone-review', args: 'M111' }])
  })

  const PLAIN = [
    { answer: prView('OPEN', 'APPROVED'), word: 'approved' },
    { answer: prView('OPEN', 'REVIEW_REQUIRED'), word: 'in review' },
  ]
  for (const each of PLAIN) {
    test(`an \`${each.word}\` line carries no Button`, async ($, on) => {
      gh(on, () => each.answer)
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      const line = await blockedView($, 'blocked-M111')
      expect(line.text).toBe(`${LINE_1250}  ${each.word}`)
      expect(line.buttons).toEqual([])
    })
  }
})

// `prWord` over shapes beyond the register cases (M224 review): a JSON
// value that is not an object, an object with no state, and a state in
// another case all read as `unknown`.
describe('prWord reads only the shapes it names', () => {
  test('a rejected call, a non-object, and an unknown state read as unknown', () => {
    const ok = (stdout: string) => ({ exitCode: 0, stdout })
    expect(prWord(null)).toBe('unknown')
    expect(prWord({ exitCode: 1, stdout: '{"state":"MERGED"}' })).toBe('unknown')
    expect(prWord(ok('null'))).toBe('unknown')
    expect(prWord(ok('[]'))).toBe('unknown')
    expect(prWord(ok('"MERGED"'))).toBe('unknown')
    expect(prWord(ok('{}'))).toBe('unknown')
    expect(prWord(ok('{"state":"open"}'))).toBe('unknown')
    expect(prWord(ok('{"state":"MERGED","reviewDecision":"CHANGES_REQUESTED"}'))).toBe('merged')
    expect(prWord(ok('{"state":"OPEN","reviewDecision":"SOMETHING_NEW"}'))).toBe('in review')
  })
})

// Paths that run no `gh` call (M224 review): a close of a shown pane, and
// an open that a hook refuses. The pull request is open, so a read there
// would also run the `gh api graphql` call (M225 AC1).
describe('a close or a refused open reads no state (M224 AC3)', () => {
  test('/cairn-pane that closes a shown pane runs no gh call', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.graphql.length).toBe(1)
    calls.calls.length = 0
    calls.graphql.length = 0
    const closed = await $.command.run({ command: COMMAND })
    expect(closed.text).toBe('cairn pane closed')
    await calls.settled()
    expect(calls.calls).toEqual([])
    expect(calls.graphql).toEqual([])
  })

  test('a refused open runs no gh call, by the command or the band', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    copy.refuse = 'opens are refused here'
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    await ui.press({ key: 'cairn-open' })
    await ui.unmount()
    await calls.settled()
    expect(calls.calls).toEqual([])
    expect(calls.graphql).toEqual([])
  })
})

// Each trigger reads an open pull request, so it runs one `gh pr view` and
// one `gh api graphql` call, and a turn end runs neither (M224 AC3, M225
// AC1).
describe('the states are read at each pane open and at a Refresh press, and never on a timer (M224 AC3)', () => {
  const ONE_READ = [['gh', 'pr', 'view', URL_1250, '--json', 'state,reviewDecision']]
  const graphOf = (calls: Gh) => calls.graphql.map(argv => [argOf(argv, 'owner'), argOf(argv, 'repo'), argOf(argv, 'number')])
  const ONE_QUERY = [['upstream', 'repo', '1250']]

  test('the /cairn-pane command reads once', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.calls).toEqual(ONE_READ)
    expect(graphOf(calls)).toEqual(ONE_QUERY)
    expect(calls.clocks).toEqual([])
  })

  test("the band's open button reads once", async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.graphql).toEqual([])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    await ui.press({ key: 'cairn-open' })
    await ui.unmount()
    await calls.settled()
    expect(calls.calls).toEqual(ONE_READ)
    expect(graphOf(calls)).toEqual(ONE_QUERY)
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
    expect(calls.clocks).toEqual([])
  })

  test('the session-start reopen reads once', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    await openPane($, on, copy)
    await calls.settled()
    await $.session.end({ reason: 'other', sessionId: 's1' })
    newProcess(copy)
    calls.calls.length = 0
    calls.graphql.length = 0
    await $.session.start(NEW_START)
    await calls.settled()
    expect(listed(copy)).toBe(true)
    expect(calls.calls).toEqual(ONE_READ)
    expect(graphOf(calls)).toEqual(ONE_QUERY)
    expect(calls.clocks).toEqual([])
  })

  test('a press of the ↻ Refresh Button reads once', async ($, on) => {
    let state = 'OPEN'
    const calls = gh(on, () => prView(state, ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
    expect((await blockedView($, 'blocked-head')).buttons).toEqual([])
    expect((await blockedView($, 'M110-head')).buttons).toEqual(['cairn-pane-refresh'])
    const press = async () => {
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      await ui.press({ key: 'cairn-pane-refresh' })
      await ui.unmount()
    }
    await press()
    expect(calls.calls).toEqual([...ONE_READ, ...ONE_READ])
    expect(graphOf(calls)).toEqual([...ONE_QUERY, ...ONE_QUERY])
    // A merged pull request gets no query.
    state = 'MERGED'
    await press()
    expect(calls.calls).toEqual([...ONE_READ, ...ONE_READ, ...ONE_READ])
    expect(graphOf(calls)).toEqual([...ONE_QUERY, ...ONE_QUERY])
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  merged`)
    expect(calls.clocks).toEqual([])
  })

  test('a turn end runs no gh call', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.graphql.length).toBe(1)
    calls.calls.length = 0
    calls.graphql.length = 0
    await $.turn.complete(turn())
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.calls).toEqual([])
    expect(calls.graphql).toEqual([])
    expect(calls.clocks).toEqual([])
  })
})

describe('a failed read shows `unknown` and no Button (M224 AC4)', () => {
  // blocked-prs: M101's read fails, and M102 and M104 read as merged, so
  // the other lines are seen to draw as before.
  const URL_12 = 'https://github.com/upstream/repo/pull/12'
  const FAILS: { name: string; answer: GhAnswer }[] = [
    { name: 'a call that rejects', answer: 'reject' },
    { name: 'a non-zero exit', answer: { exitCode: 1, stdout: '' } },
    { name: 'text that is not JSON', answer: { exitCode: 0, stdout: 'no pull requests found\n' } },
    { name: 'JSON with an unknown state', answer: prView('DRAFT', '') },
  ]
  for (const fail of FAILS) {
    test(`${fail.name} shows \`unknown\``, async ($, on) => {
      gh(on, url => (url === URL_12 ? fail.answer : prView('MERGED')))
      seat(on, copyOf('blocked-prs'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      const opened = await $.command.run({ command: COMMAND })
      expect(opened.text).toBe('cairn pane opened')
      const failed = await blockedView($, 'blocked-M101')
      expect(failed.text).toBe('M101  One pull request URL  #12  unknown')
      expect(failed.buttons).toEqual([])
      expect((await blockedView($, 'blocked-M102')).text).toBe('M102  Two pull request URLs  #34  merged')
      expect((await blockedView($, 'blocked-M102')).buttons).toEqual(['cairn-pane-finish-M102'])
      expect((await blockedView($, 'blocked-M104')).text).toBe('M104  A URL with a trailing path  #90  merged')
      expect((await blockedView($, 'blocked-M103')).text).toBe('M103  A URL only after a companion entry')
      expect((await blockedView($, 'blocked-M105')).text).toBe('M105  A branch with no URL')
    })
  }
})

// The counts of an open handed-off pull request (M225). The texts each case
// expects are written out by hand.

// The keys, texts, and indents of the pane's lines, at a width.
async function linesAt(
  $,
  bodyColumns = 60,
  surface: (typeof SURFACES)[number] = 'desktop',
): Promise<{ key: string; text: string; indent: number }[]> {
  await ghSettled()
  const ui = await mountPane($, surface, bodyColumns)
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const out = kids(root).map(line => ({
    key: keyOf(line) ?? '',
    text: textOf(line),
    indent: (line.props.paddingLeft as number | undefined) ?? 0,
  }))
  await ui.unmount()
  return out
}
const countsOf = async ($, id = 'M111', surface: (typeof SURFACES)[number] = 'desktop') =>
  (await linesAt($, 60, surface)).find(line => line.key === `blocked-${id}-counts`)

describe('each open pull request is queried once, by its own owner, repo, and number (M225 AC1)', () => {
  // blocked-prs with M101 and M104 pointed at two other repos: both read
  // OPEN, and M102 reads MERGED, so two queries run.
  test('two lines with different owners, repos, and numbers', async ($, on) => {
    const copy = copyOf('blocked-prs')
    copy.files['/cairn/milestones/M101-one.md'] = copy.files['/cairn/milestones/M101-one.md'].replace(
      'https://github.com/upstream/repo/pull/12',
      'https://github.com/alpha/one/pull/12',
    )
    copy.files['/cairn/milestones/M104-trailing.md'] = copy.files['/cairn/milestones/M104-trailing.md'].replace(
      'https://github.com/upstream/repo/pull/90',
      'https://github.com/beta/two/pull/90',
    )
    const calls = gh(
      on,
      url => (url.includes('/upstream/') ? prView('MERGED') : prView('OPEN', '')),
      url => (url.includes('/alpha/') ? countsReply(1) : countsReply(2)),
    )
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    const asked = calls.graphql.map(argv => [argv.slice(0, 3).join(' '), argOf(argv, 'owner'), argOf(argv, 'repo'), argOf(argv, 'number')])
    expect(asked.sort()).toEqual([
      ['gh api graphql', 'alpha', 'one', '12'],
      ['gh api graphql', 'beta', 'two', '90'],
    ])
    // Each query names the fields AC1 lists.
    for (const argv of calls.graphql) {
      const query = argOf(argv, 'query') ?? ''
      expect(query.includes('reviewThreads(last: 100) { nodes { isResolved } }')).toBe(true)
    }
    expect((await countsOf($, 'M101'))?.text).toBe('1 unresolved thread')
    expect((await countsOf($, 'M104'))?.text).toBe('2 unresolved threads')
    expect(await countsOf($, 'M102')).toBe(undefined)
  })

  const NOT_OPEN: { name: string; answer: GhAnswer }[] = [
    { name: 'merged', answer: prView('MERGED', '') },
    { name: 'closed', answer: prView('CLOSED', '') },
    { name: 'unknown, by a rejected call', answer: 'reject' },
    { name: 'unknown, by an unknown state', answer: prView('DRAFT', '') },
  ]
  for (const each of NOT_OPEN) {
    test(`a ${each.name} line gets no query`, async ($, on) => {
      const calls = gh(on, () => each.answer, () => countsReply(3))
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.calls.length).toBe(1)
      expect(calls.graphql).toEqual([])
      expect(await countsOf($)).toBe(undefined)
    })
  }

  // Each word `prWord` gives an OPEN pull request gets the query (M225
  // review), so the open words and `prWord` stay in step.
  const OPEN: { decision: string; word: string }[] = [
    { decision: 'CHANGES_REQUESTED', word: 'changes requested' },
    { decision: 'APPROVED', word: 'approved' },
    { decision: 'REVIEW_REQUIRED', word: 'in review' },
  ]
  for (const each of OPEN) {
    test(`an \`${each.word}\` line gets one query`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', each.decision), () => countsReply(1))
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.graphql.length).toBe(1)
      expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  ${each.word}`)
      expect((await countsOf($))?.text).toBe('1 unresolved thread')
    })
  }
})

describe('the count line under a blocked line (M225 AC3)', () => {
  const LINES: { t: number; text: string | undefined }[] = [
    { t: 3, text: '3 unresolved threads' },
    { t: 2, text: '2 unresolved threads' },
    { t: 1, text: '1 unresolved thread' },
    { t: 0, text: undefined },
  ]
  for (const each of LINES) {
    test(`${each.t} threads draw ${each.text === undefined ? 'no line' : `\`${each.text}\``}`, async ($, on) => {
      gh(on, () => prView('OPEN', 'CHANGES_REQUESTED'), () => countsReply(each.t))
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      const lines = await linesAt($)
      const at = lines.findIndex(line => line.key === 'blocked-M111-counts')
      expect(lines.find(line => line.key === 'blocked-M111')?.text).toBe(`${LINE_1250}  changes requested`)
      if (each.text === undefined) {
        expect(at).toBe(-1)
        return
      }
      expect(lines[at]).toEqual({ key: 'blocked-M111-counts', text: each.text, indent: 4 })
      expect(lines[at - 1].key).toBe('blocked-M111')
    })
  }

  test('no line before the first read', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''), () => countsReply(3))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.graphql).toEqual([])
    expect(await countsOf($)).toBe(undefined)
  })

  // A Refresh whose query is held: the earlier counts stay drawn until it
  // returns, and then the new ones draw. A later Refresh whose query fails
  // takes the line away.
  test('a Refresh keeps the earlier counts until the new read returns', async ($, on) => {
    let hold: Promise<void> | null = null
    let reply = countsReply(2)
    const calls = gh(
      on,
      () => prView('OPEN', ''),
      async () => {
        if (hold !== null) await hold
        return reply
      },
    )
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await countsOf($))?.text).toBe('2 unresolved threads')
    let release = () => {}
    hold = new Promise<void>(resolve => {
      release = resolve
    })
    reply = countsReply(5)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: 'cairn-pane-refresh' })
    try {
      for (let i = 0; i < 200 && calls.graphql.length < 2; i++) await new Promise(resolve => setTimeout(resolve, 5))
      expect(calls.graphql.length).toBe(2)
      // The desktop pane holds the press, so the terminal one is read.
      expect((await countsOf($, 'M111', 'terminal'))?.text).toBe('2 unresolved threads')
    } finally {
      release()
      await pressing
    }
    await ui.unmount()
    expect((await countsOf($))?.text).toBe('5 unresolved threads')
    hold = null
    reply = { exitCode: 1, stdout: '' }
    const again = await mountPane($, 'desktop')
    await again.press({ key: 'cairn-pane-refresh' })
    await again.unmount()
    expect(await countsOf($)).toBe(undefined)
  })

  // 3-digit counts fit a 44-column dock: the whole line, as well as each
  // line's lead and tail as the M208 check reads them.
  test('3-digit counts fit 44 columns', async ($, on) => {
    gh(on, () => prView('OPEN', ''), () => countsReply(100))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const counts = (await linesAt($, 44)).find(line => line.key === 'blocked-M111-counts')
    expect(counts?.text).toBe('100 unresolved threads')
    expect((counts?.indent ?? 99) + width(counts?.text ?? '')).toBeLessThanOrEqual(44)
    const ui = await mountPane($, 'desktop', 44)
    const [root] = await ui.findAll({ key: 'cairn-pane' })
    for (const line of kids(root)) {
      const key = keyOf(line) ?? ''
      const indent = (line.props.paddingLeft as number | undefined) ?? 0
      const sum = async (part: string) => (await partOf(ui, `${key}-${part}`)).map(t => width(textOf(t))).reduce((a, b) => a + b, 0)
      expect([key, indent + (await sum('lead')) + (await sum('tail')) <= 44]).toEqual([key, true])
      expect([key, line.props.minWidth]).toEqual([key, 0])
    }
    await ui.unmount()
  })
})

describe('a failed count read draws no count line and leaves the state word (M225 AC4)', () => {
  const reply = (pr: unknown): GhAnswer => ({ exitCode: 0, stdout: `${JSON.stringify({ data: { repository: { pullRequest: pr } } })}\n` })
  const good = JSON.parse((countsReply(2) as { stdout: string }).stdout).data.repository.pullRequest
  const FAILS: { name: string; answer: GhAnswer }[] = [
    { name: 'a call that rejects', answer: 'reject' },
    { name: 'a non-zero exit', answer: { exitCode: 1, stdout: '' } },
    { name: 'text that is not JSON', answer: { exitCode: 0, stdout: 'gh: Could not resolve to a PullRequest\n' } },
    { name: 'a null pullRequest', answer: reply(null) },
    { name: 'threads that are not a list', answer: reply({ ...good, reviewThreads: { nodes: null } }) },
    { name: 'a malformed node', answer: reply({ ...good, reviewThreads: { nodes: [{ isResolved: 'no' }] } }) },
  ]
  for (const fail of FAILS) {
    test(`${fail.name}`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', 'CHANGES_REQUESTED'), () => fail.answer)
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      const opened = await $.command.run({ command: COMMAND })
      expect(opened.text).toBe('cairn pane opened')
      await calls.settled()
      expect(calls.graphql.length).toBe(1)
      const line = await blockedView($, 'blocked-M111')
      expect(line.text).toBe(`${LINE_1250}  changes requested`)
      expect(line.buttons).toEqual(['cairn-pane-revise-M111'])
      expect(await countsOf($)).toBe(undefined)
    })
  }
})

// The open hotfix pull requests (M226). A case answers the mod's `git` calls
// from the remotes it names and its `gh pr list` calls from `list`, as `gh`
// above records them. The blocked-prs fixture holds blocked rows and a
// candidate row, and most cases answer its blocked pull requests as
// merged. The lines each case expects are written out by hand.
const ORIGIN = 'https://github.com/fork/repo.git'
const UPSTREAM = 'git@github.com:upstream/repo.git'
const GUEST_PROFILE = '# Toolchain profile: generic\n# Collaboration mode: guest\n\n## verify\n'
const listCall = (url: string) => [
  'gh', 'pr', 'list', '--repo', url, '--state', 'open', '--author', '@me', '--limit', '100', '--json', 'number,title,url,headRefName',
]
const prUrl = (n: number) => `https://github.com/upstream/repo/pull/${n}`
const pr = (n: number, branch: string, title = `Fix ${n}`) => ({ number: n, title, url: prUrl(n), headRefName: branch })
const listReply = (entries: unknown[]): GhAnswer => ({ exitCode: 0, stdout: `${JSON.stringify(entries)}\n` })
const HOTFIX_KEY = /^hotfix(es-head(-gap)?|-\d+(-counts)?)$/
const keysOf = async $ => (await linesAt($)).map(line => line.key)
const withoutHotfixes = (lines: { key: string }[]) => lines.filter(line => !HOTFIX_KEY.test(line.key))

async function pressKey($, key: string) {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
  await ui.press({ key })
  await ui.unmount()
}

describe('each pane open and Refresh press lists the open pull requests on the base remote once (M226 AC1)', () => {
  const MODES = [
    { name: 'an owner-mode repo uses origin', profile: null, remotes: { origin: ORIGIN, upstream: UPSTREAM }, url: ORIGIN },
    { name: 'a guest-mode repo with upstream uses upstream', profile: GUEST_PROFILE, remotes: { origin: ORIGIN, upstream: UPSTREAM }, url: UPSTREAM },
    { name: 'a guest-mode repo without upstream uses origin', profile: GUEST_PROFILE, remotes: { origin: ORIGIN }, url: ORIGIN },
  ]
  for (const mode of MODES) {
    test(mode.name, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, { remotes: mode.remotes })
      const copy = copyOf('blocked-prs')
      if (mode.profile !== null) copy.files['/cairn/PROFILE.md'] = mode.profile
      seat(on, copy)
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.lists).toEqual([listCall(mode.url)])
    })
  }

  test("the band's open button lists once", async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN } })
    seat(on, copyOf('blocked-prs'))
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.lists).toEqual([])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    await ui.press({ key: 'cairn-open' })
    await ui.unmount()
    await calls.settled()
    expect(calls.lists).toEqual([listCall(ORIGIN)])
  })

  test('the session-start reopen lists once, and a turn end lists nothing', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN } })
    const copy = copyOf('blocked-prs')
    await openPane($, on, copy)
    await calls.settled()
    await $.session.end({ reason: 'other', sessionId: 's1' })
    newProcess(copy)
    calls.lists.length = 0
    await $.session.start(NEW_START)
    await calls.settled()
    expect(listed(copy)).toBe(true)
    expect(calls.lists).toEqual([listCall(ORIGIN)])
    await $.turn.complete(turn())
    expect(calls.lists).toEqual([listCall(ORIGIN)])
  })
})

describe('the Hotfixes section lists the hotfix-* pull requests before the candidates (M226 AC2)', () => {
  test('only the hotfix-* entry draws, after Blocked and before Candidates', async ($, on) => {
    const list = () => listReply([pr(1265, 'hotfix-clmm', 'Return only fixed effects'), pr(1300, 'm226-pane'), pr(1301, 'feature-x')])
    gh(on, url => (url === prUrl(1265) ? prView('OPEN', '') : prView('MERGED')), () => countsReply(0), { remotes: { origin: ORIGIN }, list })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const keys = await keysOf($)
    expect(keys.filter(key => HOTFIX_KEY.test(key))).toEqual(['hotfixes-head-gap', 'hotfixes-head', 'hotfix-1265'])
    expect(keys.indexOf('blocked-head')).toBeLessThan(keys.indexOf('hotfixes-head'))
    expect(keys.indexOf('hotfixes-head')).toBeLessThan(keys.indexOf('candidates-head'))
    expect(keys.slice(keys.indexOf('hotfix-1265') + 1)[0]).toBe('candidates-head-gap')
    expect((await blockedView($, 'hotfixes-head')).text).toBe('▎ HOTFIXES 1')
    expect((await blockedView($, 'hotfix-1265')).text).toBe('#1265  Return only fixed effects  in review')
  })
})

describe('each hotfix line shows the word and counts a blocked line shows, and no Button (M226 AC3)', () => {
  test('an open PR with counts, a changes-requested PR, and a merged PR', async ($, on) => {
    const list = () => listReply([pr(1265, 'hotfix-a'), pr(1264, 'hotfix-b'), pr(1263, 'hotfix-c')])
    const views: Record<string, GhAnswer> = {
      [prUrl(1265)]: prView('OPEN', 'REVIEW_REQUIRED'),
      [prUrl(1264)]: prView('OPEN', 'CHANGES_REQUESTED'),
      [prUrl(1263)]: prView('MERGED', 'APPROVED'),
    }
    const calls = gh(on, url => views[url] ?? prView('MERGED'), url => (url === prUrl(1265) ? countsReply(2) : countsReply(0)), {
      remotes: { origin: ORIGIN },
      list,
    })
    // blocked-active's M111 is not in `views`, so it reads as merged here.
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const lines = await linesAt($)
    const textOf_ = (key: string) => lines.find(line => line.key === key)?.text
    expect(textOf_('hotfix-1265')).toBe('#1265  Fix 1265  in review')
    expect(textOf_('hotfix-1264')).toBe('#1264  Fix 1264  changes requested')
    expect(textOf_('hotfix-1263')).toBe('#1263  Fix 1263  merged')
    expect(textOf_('hotfix-1265-counts')).toBe('2 unresolved threads')
    expect(textOf_('hotfix-1264-counts')).toBe(undefined)
    expect(textOf_('hotfix-1263-counts')).toBe(undefined)
    for (const key of ['hotfix-1265', 'hotfix-1264', 'hotfix-1263']) expect((await blockedView($, key)).buttons).toEqual([])
    // A merged one gets no count query, as a merged blocked line gets none.
    expect(calls.graphql.map(argv => argOf(argv, 'number'))).not.toContain('1263')
    expect(calls.graphql.map(argv => argOf(argv, 'number'))).toContain('1264')
  })

  test('a hotfix line shows the same word and counts as a blocked line with the same replies', async ($, on) => {
    const copy = copyOf('blocked-active')
    gh(on, () => prView('OPEN', 'CHANGES_REQUESTED'), () => countsReply(1), {
      remotes: { origin: ORIGIN },
      list: () => listReply([pr(1265, 'hotfix-a')]),
    })
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const lines = await linesAt($)
    const textOf_ = (key: string) => lines.find(line => line.key === key)?.text ?? ''
    expect(textOf_('blocked-M111')).toBe(`${LINE_1250}  changes requested`)
    expect(textOf_('hotfix-1265').endsWith('  changes requested')).toBe(true)
    expect(textOf_('hotfix-1265-counts')).toBe(textOf_('blocked-M111-counts'))
    expect(textOf_('hotfix-1265-counts')).toBe('1 unresolved thread')
  })
})

describe('a failed list keeps the last good read for the root, and an empty one draws none (M226 AC4)', () => {
  const GOOD = () => listReply([pr(1265, 'hotfix-a')])
  const FAILS: { name: string; answer: GhAnswer }[] = [
    { name: 'a call that rejects', answer: 'reject' },
    { name: 'a non-zero exit', answer: { exitCode: 1, stdout: '[]\n' } },
    { name: 'text that is not JSON', answer: { exitCode: 0, stdout: 'HTTP 502\n' } },
    { name: 'JSON that is not an array', answer: { exitCode: 0, stdout: '{"number":1265}\n' } },
  ]
  // Opens with no remote for the baseline lines, then lists once with a
  // good reply, and answers the next list with `next`.
  async function setUp($, on, next: () => GhAnswer) {
    const remotes: Record<string, string> = {}
    let answer = GOOD
    const calls = gh(on, url => (url === prUrl(1265) ? prView('OPEN', '') : prView('MERGED')), undefined, { remotes, list: () => answer() })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.lists).toEqual([])
    const baseline = await linesAt($)
    expect(baseline.filter(line => HOTFIX_KEY.test(line.key))).toEqual([])
    remotes.origin = ORIGIN
    await pressKey($, 'cairn-pane-refresh')
    expect((await keysOf($)).includes('hotfix-1265')).toBe(true)
    answer = next
    await pressKey($, 'cairn-pane-refresh')
    expect(calls.lists.length).toBe(2)
    return baseline
  }

  for (const fail of FAILS) {
    test(`${fail.name} keeps the hotfix line`, async ($, on) => {
      const baseline = await setUp($, on, () => fail.answer)
      const lines = await linesAt($)
      expect(lines.find(line => line.key === 'hotfix-1265')?.text).toBe('#1265  Fix 1265  in review')
      expect(withoutHotfixes(lines)).toEqual(baseline)
    })
  }

  test('an entry with a missing field is skipped', async ($, on) => {
    const { url: _url, ...noUrl } = pr(1262, 'hotfix-b')
    const { headRefName: _head, ...noBranch } = pr(1261, 'hotfix-c')
    const baseline = await setUp($, on, () =>
      listReply([
        noUrl,
        noBranch,
        { ...pr(1260, 'hotfix-d'), number: '1260' },
        null,
        'hotfix-e',
        pr(1259, 'hotfix-f'),
        // A repeated entry draws once, so no two lines share a key (M226 review).
        pr(1259, 'hotfix-f'),
      ]),
    )
    const lines = await linesAt($)
    expect(lines.filter(line => HOTFIX_KEY.test(line.key)).map(line => line.key)).toEqual([
      'hotfixes-head-gap',
      'hotfixes-head',
      'hotfix-1259',
    ])
    expect(withoutHotfixes(lines)).toEqual(baseline)
  })

  test('an empty array replaces the kept lines and draws no section', async ($, on) => {
    const baseline = await setUp($, on, () => listReply([]))
    expect(await linesAt($)).toEqual(baseline)
  })

  test('a kept read from another root is not drawn', async ($, on) => {
    const remotes: Record<string, string> = { origin: ORIGIN }
    let answer = GOOD
    const calls = gh(on, () => prView('OPEN', ''), undefined, { remotes, list: () => answer() })
    const copy = copyOf('blocked-prs')
    for (const path of Object.keys(copy.files)) copy.files[`/other${path}`] = copy.files[path]
    copy.unreadable.push(...copy.unreadable.map(path => `/other${path}`))
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await keysOf($)).includes('hotfix-1265')).toBe(true)
    copy.cwd = '/other'
    await $.turn.complete(turn())
    const moved = await linesAt($)
    expect(moved.filter(line => HOTFIX_KEY.test(line.key))).toEqual([])
    answer = () => 'reject'
    const viewsOf1265 = () => calls.calls.filter(argv => argv[3] === prUrl(1265)).length
    const before = viewsOf1265()
    await pressKey($, 'cairn-pane-refresh')
    expect(await linesAt($)).toEqual(moved)
    // The read itself drops the other root's list, so its URL is not read
    // again, apart from the drawing's root check (M226 review).
    expect(viewsOf1265()).toBe(before)
  })

  test('a repo with no remote runs no list call and draws no section', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { list: GOOD })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.git).toEqual([['git', 'remote', 'get-url', 'origin']])
    expect(calls.lists).toEqual([])
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
  })
})

// M236: the pane's first line, the Button keys the drawn pane holds, and
// the ↻ Button.
async function refreshOf($, surface: (typeof SURFACES)[number] = 'desktop') {
  const ui = await mountPane($, surface)
  const keys = (await ui.findAll({ type: 'Button' })).map(keyOf)
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const lines = root === undefined ? [] : kids(root)
  const [button] = await ui.findAll({ key: PANE_REFRESH })
  await ui.unmount()
  return { keys, lines, first: lines[0], button }
}
// The keys of a line Box's children, and the key and `flexGrow` of every
// line Box and child Box that sets one.
const childKeys = (line: Element | undefined) => (line === undefined ? [] : kids(line).map(keyOf))
const grows = (lines: Element[]) =>
  lines.flatMap(line => [line, ...kids(line)].filter(box => box.props.flexGrow !== undefined).map(box => [keyOf(box), box.props.flexGrow]))

describe('the pane has one ↻ Refresh Button, at the right end of its first line (M236 AC2)', () => {
  // The checks AC2 makes in every state with a ROADMAP. `firstKey` is the
  // first line's key, the head line of the first milestone or `no-active`.
  const one = async ($, firstKey: string) => {
    const got = await refreshOf($)
    expect(got.keys.filter(key => key === PANE_REFRESH)).toEqual([PANE_REFRESH])
    expect(got.keys.filter(key => (key ?? '').endsWith('-hotfixes'))).toEqual([])
    expect(keyOf(got.first as Element)).toBe(firstKey)
    const children = childKeys(got.first)
    expect(children[children.length - 1]).toBe(`${firstKey}-refresh`)
    expect(grows(got.lines)).toEqual([[`${firstKey}-text`, 1]])
    expect(got.lines.filter(line => line.props.justifyContent !== undefined).map(keyOf)).toEqual([])
    expect(got.button?.props.label).toBe('↻')
    return got
  }

  test('blocked PRs and hotfix PRs, no active milestone', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''), undefined, { remotes: { origin: ORIGIN }, list: () => listReply([pr(1265, 'hotfix-a')]) })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect((await keysOf($)).includes('hotfixes-head')).toBe(true)
    expect((await blockedView($, 'blocked-head')).buttons).toEqual([])
    expect((await blockedView($, 'hotfixes-head')).buttons).toEqual([])
    await one($, 'no-active')
  })

  test('an in-progress and a review milestone: only the first head line carries ↻', async ($, on) => {
    gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('pane-full'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const got = await one($, 'M080-head')
    const second = got.lines.find(line => keyOf(line) === 'M081-head')
    expect(second).toBeDefined()
    expect(buttonsIn(second as Element)).toEqual([])
  })

  test('the Next line with Status and Clear, and one active milestone', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await endSkill($)
    const got = await one($, `${FIXTURES['single-in-progress'].pane[0].id}-head`)
    expect(got.keys).toEqual([PANE_REFRESH, PANE_NEXT, PANE_CLEAR, PANE_STATUS])
  })

  test('one active milestone and no PRs', async ($, on) => {
    gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('single-in-progress'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await keysOf($)).filter(key => key.startsWith('blocked') || key.startsWith('hotfix'))).toEqual([])
    await one($, `${FIXTURES['single-in-progress'].pane[0].id}-head`)
  })

  test('no ROADMAP draws no ↻ Button', async ($, on) => {
    seat(on, copyOf('no-roadmap'))
    await $.turn.complete(turn())
    const got = await refreshOf($)
    expect(got.keys.filter(key => key === PANE_REFRESH)).toEqual([])
  })

  test('a press of ↻ lists the hotfix PRs and reads each PR again', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: () => listReply([pr(1265, 'hotfix-a')]) })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.lists.length).toBe(1)
    await pressKey($, PANE_REFRESH)
    expect(calls.lists.length).toBe(2)
    expect(calls.calls.filter(argv => argv[3] === prUrl(1265)).length).toBe(2)
  })
})

describe('a head line starts with the id in its phase color, with no phase word (M236 AC3)', () => {
  // pane-full holds M080 in-progress and M081 review.
  for (const [id, color] of [
    ['M080', IMPLEMENT_KEY],
    ['M081', REVIEW_KEY],
  ] as const) {
    test(`${id}`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = await mountPane($, 'desktop')
      const lead = await partOf(ui, `${id}-head-lead`)
      await ui.unmount()
      expect(lead.map(span => [textOf(span), span.props.color ?? null, span.props.bold ?? null])).toEqual([
        [id, color, true],
        ['  ', null, null],
      ])
    })
  }
})

describe('the ↻ Button reads ⋯ while a read runs, and a press during a press read does nothing (M236 AC4)', () => {
  // A gate: `wait` settles when `release` runs, so a `gh pr view` answer
  // that awaits it is held until then.
  function gate() {
    let release = () => {}
    const wait = new Promise<void>(resolve => {
      release = resolve
    })
    return { wait, release: () => release() }
  }
  const until = async (ok: () => boolean) => {
    for (let i = 0; i < 200 && !ok(); i++) await sleep(5)
    expect(ok()).toBe(true)
  }
  // The ↻ Button's label, read through a terminal mount, which no press
  // holds.
  const labelOf = async $ => (await refreshOf($, 'terminal')).button?.props.label
  const total = (calls: Gh, reads: string[]) => reads.length + calls.calls.length + calls.graphql.length + calls.lists.length + calls.git.length

  const ENDS: { name: string; answer: GhAnswer }[] = [
    { name: 'succeeds', answer: prView('OPEN', '') },
    { name: 'exits 1', answer: { exitCode: 1, stdout: '' } },
    { name: 'rejects', answer: 'reject' },
  ]
  for (const end of ENDS) {
    test(`a held read reads ⋯ on the first line, and ↻ after it ${end.name}`, async ($, on) => {
      const held_ = gate()
      const calls = gh(on, async () => {
        await held_.wait
        return end.answer
      })
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      expect(await labelOf($)).toBe('↻')
      await $.command.run({ command: COMMAND })
      await until(() => calls.calls.length === 1)
      const during = await refreshOf($, 'terminal')
      expect(during.button?.props.label).toBe('⋯')
      const children = childKeys(during.first)
      expect(children[children.length - 1]).toBe(`${keyOf(during.first as Element)}-refresh`)
      held_.release()
      await calls.settled()
      expect(await labelOf($)).toBe('↻')
    })
  }

  test('an open and a press overlap: ↻ once the newer read settles', async ($, on) => {
    const older = gate()
    const newer = gate()
    let n = 0
    const calls = gh(on, async () => {
      n += 1
      await (n === 1 ? older.wait : newer.wait)
      return prView('OPEN', '')
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await until(() => calls.calls.length === 1)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.calls.length === 2)
      expect(await labelOf($)).toBe('⋯')
      newer.release()
      await pressing
      expect(await labelOf($)).toBe('↻')
    } finally {
      newer.release()
      older.release()
      await pressing
      await ui.unmount()
    }
    await calls.settled()
    expect(await labelOf($)).toBe('↻')
  })

  // The case the newest-read check exists for: the older read settles
  // first, and ⋯ stays while the newer one runs.
  test('an open and a press overlap: ⋯ stays when the older read settles first', async ($, on) => {
    const older = gate()
    const newer = gate()
    let n = 0
    const calls = gh(on, async () => {
      n += 1
      await (n === 1 ? older.wait : newer.wait)
      return prView('OPEN', '')
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await until(() => calls.calls.length === 1)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.calls.length === 2)
      older.release()
      await sleep(50)
      expect(await labelOf($)).toBe('⋯')
      newer.release()
      await pressing
      expect(await labelOf($)).toBe('↻')
    } finally {
      older.release()
      newer.release()
      await pressing
      await ui.unmount()
    }
  })

  test('a second press during a held press read reads no file and runs no call', async ($, on) => {
    const held_ = gate()
    let holding = false
    const calls = gh(on, async () => {
      if (holding) await held_.wait
      return prView('OPEN', '')
    })
    const copy = copyOf('blocked-active')
    const reads: string[] = []
    copy.reads = reads
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    holding = true
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.calls.length === 2)
      const second = await mountPane($, 'terminal')
      // The count starts after the second mount, so it holds only what the
      // press does.
      const before = total(calls, reads)
      await second.press({ key: PANE_REFRESH })
      await sleep(50)
      expect(total(calls, reads)).toBe(before)
      await second.unmount()
    } finally {
      held_.release()
      await pressing
      await ui.unmount()
    }
    await calls.settled()
    // Once the first press's read settles, a press reads again.
    holding = false
    await pressKey($, PANE_REFRESH)
    expect(calls.calls.length).toBe(3)
  })

  test('a stored reading state with no press read in this module lets a press read', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    // A read that a reloaded module ended leaves the stored state true: the
    // store answers true until the mod writes the key.
    let stale = true
    on('state.get', async ($, e, next) => {
      const got = await next(e)
      if (!stale || e.plugin !== 'cairn' || e.key !== 'reading') return got
      // The hook answers `{ value }`, a StateRead of `{ value, version }`.
      const read_ = (got as { value?: { version?: number } } | undefined)?.value
      return { value: { version: read_?.version ?? 0, value: { shape: 'reading-1', value: true } } }
    })
    on('state.set', async ($, e, next) => {
      if (e.plugin === 'cairn' && e.key === 'reading') stale = false
      return next(e)
    })
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    expect(await labelOf($)).toBe('⋯')
    await pressKey($, PANE_REFRESH)
    await calls.settled()
    expect(calls.calls.length).toBe(1)
    expect(await labelOf($)).toBe('↻')
  })
})

// M230. `held` answers every `gh` call only after `release`, so an open
// that waited for the read could not finish first. `finishes` says whether
// a call finished within 300 ms. `until` waits for a condition, for at most
// 200 waits of 5 ms.
function held(on: On, list: () => GhAnswer = () => listReply([pr(1265, 'hotfix-a')])) {
  let release = () => {}
  const gate = new Promise<void>(resolve => {
    release = resolve
  })
  let listSettled = false
  const calls = gh(
    on,
    async () => {
      await gate
      return prView('OPEN', '')
    },
    async () => {
      await gate
      return countsReply(0)
    },
    {
      remotes: { origin: ORIGIN },
      list: async () => {
        await gate
        listSettled = true
        return list()
      },
    },
  )
  return { calls, release, listSettled: () => listSettled }
}
const finishes = (work: Promise<unknown>) => Promise.race([work.then(() => 'finished'), sleep(300).then(() => 'waiting')])
async function until(ok: () => boolean) {
  for (let i = 0; i < 200 && !ok(); i++) await sleep(5)
}

describe('an open finishes before the pull request reads settle (M230 AC1)', () => {
  test('/cairn-pane prints its line before any gh call settles', async ($, on) => {
    const { calls, release } = held(on)
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    try {
      const run = $.command.run({ command: COMMAND })
      expect(await finishes(run)).toBe('finished')
      expect((await run).text).toBe('cairn pane opened')
      await until(() => calls.calls.length > 0)
      expect(calls.calls.map(argv => argv[3])).toEqual([URL_1250])
    } finally {
      release()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
  })

  test("the band's open Button's press returns before any gh call settles", async ($, on) => {
    const { calls, release } = held(on)
    seat(on, copyOf('blocked-active'))
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    try {
      expect(await finishes(ui.press({ key: 'cairn-open' }))).toBe('finished')
      await until(() => calls.calls.length > 0)
      expect(calls.calls.map(argv => argv[3])).toEqual([URL_1250])
    } finally {
      release()
      await ui.unmount()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
  })

  test("the session-start reopen's handler returns before any gh call settles", async ($, on) => {
    const { calls, release } = held(on)
    const copy = copyOf('blocked-active')
    try {
      await openPane($, on, copy)
      await until(() => calls.calls.length > 0)
      await $.session.end({ reason: 'other', sessionId: 's1' })
      newProcess(copy)
      calls.calls.length = 0
      expect(await finishes($.session.start(NEW_START))).toBe('finished')
      expect(listed(copy)).toBe(true)
      await until(() => calls.calls.length > 0)
      expect(calls.calls.map(argv => argv[3])).toEqual([URL_1250])
    } finally {
      release()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
  })
})

describe('the blocked reads start before the hotfix list settles (M230 AC2)', () => {
  test("the blocked URL's gh pr view runs while gh pr list is held", async ($, on) => {
    const { calls, release, listSettled } = held(on)
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    try {
      await $.command.run({ command: COMMAND })
      await until(() => calls.calls.length > 0 && calls.lists.length > 0)
      expect(calls.lists).toEqual([listCall(ORIGIN)])
      expect(listSettled()).toBe(false)
      expect(calls.calls).toEqual([['gh', 'pr', 'view', URL_1250, '--json', 'state,reviewDecision']])
    } finally {
      release()
    }
    await calls.settled()
    // Once the list settles, its hotfix URL is read too.
    expect(calls.calls.map(argv => argv[3])).toEqual([URL_1250, prUrl(1265)])
  })
})

describe('a /clear in the same process reads the states again while the pane shows (M230 AC3)', () => {
  // The pane is listed open with no read run, as after an in-process
  // `/clear`, whose host state starts empty (M222).
  async function setUp($, on, place: (copy: Copy) => void) {
    const got = held(on)
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start(NEW_START)
    place(copy)
    expect((await blockedView($, 'blocked-M111')).text).toBe(LINE_1250)
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
    return got
  }

  test('a placed and shown pane reads the words and the hotfix list, and the hook does not wait', async ($, on) => {
    const { calls, release } = await setUp($, on, copy => {
      copy.open = [PANE]
    })
    try {
      expect(await finishes($.classic.SessionStart({ source: 'clear' }))).toBe('finished')
      await until(() => calls.calls.length > 0 && calls.lists.length > 0)
      expect(calls.lists).toEqual([listCall(ORIGIN)])
      expect(calls.calls.map(argv => argv[3])).toEqual([URL_1250])
    } finally {
      release()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
    expect((await blockedView($, 'hotfix-1265')).text).toBe('#1265  Fix 1265  in review')
  })

  test('a closed pane runs no gh call', async ($, on) => {
    const { calls, release } = await setUp($, on, copy => {
      copy.open = []
    })
    try {
      await $.classic.SessionStart({ source: 'clear' })
      await calls.settled()
      expect(calls.calls).toEqual([])
      expect(calls.lists).toEqual([])
      expect(calls.graphql).toEqual([])
    } finally {
      release()
    }
  })
})

// A `/resume` empties the host's state as a `/clear` does, and either reads
// the files again (M237 AC1). Each case compares the drawing with the one a
// turn end, a read the band already trusts, gives right after.
describe('a resume start reads the files again, as a clear start does (M237 AC1)', () => {
  async function bandText($): Promise<string> {
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })) as Ui
    const [root] = await ui.findAll({ key: 'cairn-band' })
    const out = root === undefined ? '' : textOf(root)
    await ui.unmount()
    return out
  }
  for (const source of ['clear', 'resume'] as const) {
    test(`a ${source} start with empty state draws the fixture's rows and lines`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      expect(await bandText($)).toBe('')
      expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBeUndefined()
      await $.classic.SessionStart({ source })
      const band = await bandText($)
      const lines = await paneLines($, 'terminal')
      expect(band).toContain('M002')
      expect(textAt(lines, 'M002-task-1')).toBe(T2_OPEN)
      await $.turn.complete(turn())
      expect(await bandText($)).toBe(band)
      expect(await paneLines($, 'terminal')).toEqual(lines)
    })

    test(`a ${source} start replaces rows from the same root that differ from the files`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const before = await bandText($)
      expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBe(T2_OPEN)
      tick(copy)
      await $.classic.SessionStart({ source })
      const band = await bandText($)
      const lines = await paneLines($, 'terminal')
      expect(band).not.toBe(before)
      expect(textAt(lines, 'M002-task-1')).toBe(T2_DONE)
      await $.turn.complete(turn())
      expect(await bandText($)).toBe(band)
      expect(await paneLines($, 'terminal')).toEqual(lines)
    })
  }

  for (const source of ['startup', 'compact'] as const) {
    test(`a ${source} start reads no file`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      copy.reads = []
      await $.classic.SessionStart({ source })
      expect(copy.reads).toEqual([])
    })
  }
})

// A clear or resume start reads the pull request states for a placed pane,
// shown or behind another tab, and for no other pane (M237 AC2). No
// `session.start` opens the pane first, so every `gh` call is the hook's.
describe('a clear or resume start reads the states for a placed pane (M237 AC2)', () => {
  const CASES: { name: string; place: (copy: Copy) => void; reads: boolean }[] = [
    { name: 'a placed and shown pane', place: copy => { copy.open = [PANE] }, reads: true },
    { name: 'a placed pane behind another tab', place: copy => { copy.open = [PANE]; copy.hidden = [PANE] }, reads: true },
    { name: 'a pane that is not listed', place: copy => { copy.open = [] }, reads: false },
    { name: 'a listed pane that is not placed', place: copy => { copy.open = [PANE]; copy.unplaced = [PANE] }, reads: false },
    { name: 'a pane list that throws', place: copy => { copy.open = [PANE]; copy.panesThrow = true }, reads: false },
  ]
  for (const source of ['clear', 'resume'] as const) {
    for (const { name, place, reads } of CASES) {
      test(`at a ${source} start, ${name} ${reads ? 'reads' : 'runs no gh call'}`, async ($, on) => {
        const calls = gh(on, () => prView('OPEN', ''), undefined, {
          remotes: { origin: ORIGIN },
          list: () => listReply([pr(1265, 'hotfix-a')]),
        })
        const copy = copyOf('blocked-active')
        seat(on, copy)
        place(copy)
        await $.classic.SessionStart({ source })
        await calls.settled()
        const all = [...calls.calls, ...calls.graphql, ...calls.lists]
        if (reads) {
          expect(calls.lists).toEqual([listCall(ORIGIN)])
          expect(all.length).toBeGreaterThan(1)
        } else {
          expect(all).toEqual([])
        }
      })
    }
  }
})

describe("a hotfix whose URL is a blocked row's draws on the blocked line only (M230 AC4)", () => {
  const SHARED = { number: 1250, title: 'Fix 1250', url: URL_1250, headRefName: 'hotfix-shared' }

  test('beside another hotfix, the shared one draws once and the count leaves it out', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''), undefined, {
      remotes: { origin: ORIGIN },
      list: () => listReply([SHARED, pr(1265, 'hotfix-a')]),
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    await $.command.run({ command: COMMAND })
    const keys = await keysOf($)
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
    expect(keys.filter(key => HOTFIX_KEY.test(key))).toEqual(['hotfixes-head-gap', 'hotfixes-head', 'hotfix-1265'])
    expect((await blockedView($, 'hotfixes-head')).text).toBe('▎ HOTFIXES 1')
    expect(calls.calls.filter(argv => argv[3] === URL_1250).length).toBe(1)
  })

  test('when the shared one is the only hotfix, no Hotfixes heading draws', async ($, on) => {
    gh(on, () => prView('OPEN', ''), undefined, { remotes: { origin: ORIGIN }, list: () => listReply([SHARED]) })
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
  })
})

describe('the gh pr list call names an http(s) remote without its userinfo (M230 AC5)', () => {
  const FORMS: { name: string; remote: string; repo: string }[] = [
    { name: 'a user and token', remote: 'https://user:token@github.com/o/r.git', repo: 'https://github.com/o/r.git' },
    { name: 'a token alone', remote: 'https://token@github.com/o/r.git', repo: 'https://github.com/o/r.git' },
    { name: 'an scp-form ssh URL, kept as it is', remote: 'git@github.com:o/r.git', repo: 'git@github.com:o/r.git' },
  ]
  for (const form of FORMS) {
    test(form.name, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, {
        remotes: { origin: form.remote },
        list: () => listReply([pr(1265, 'hotfix-a')]),
      })
      seat(on, copyOf('blocked-active'))
      await $.session.start(NEW_START)
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.lists).toEqual([listCall(form.repo)])
      const recorded = [...calls.calls, ...calls.graphql, ...calls.git, ...calls.lists].flat()
      expect(recorded.filter(arg => arg.includes('token'))).toEqual([])
    })
  }
})
