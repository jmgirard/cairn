import { describe, expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { FIXTURES } from './fixtures.gen'
import { GRAY, flowOf, width } from './band'
import {
  CHECKED_MARK,
  COMMAND_PHASE,
  NO_FILE,
  NO_ROADMAP,
  OPEN_MARK,
  PRIORITY_MARK,
  nextLabel,
  paneLines as layout,
  prWord,
  startedRows,
} from './pane'
import type { PaneState } from './reader'
import { candidateRows, listNames, parseRoadmapRows, takenRows } from './reader'

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
  // While set, the next `$.ui.panes()` beneath the mod computes its answer,
  // clears this field, keeps that answer in `panesHeld`, and waits for this
  // promise before it answers (M256).
  panesHold?: Promise<void>
  panesHeld?: ReturnType<typeof panesOf>
  // While set, the session end beneath the mod throws, and while set, it
  // waits for this promise before it answers (M255).
  endThrows?: boolean
  endHold?: Promise<void>
  // The text and mode of each prompt box fill that reached beneath the mod
  // (M260).
  fills?: { text: string; mode: string }[]
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
    const value = panesOf(copy)
    const hold = copy.panesHold
    if (hold !== undefined) {
      copy.panesHold = undefined
      copy.panesHeld = value
      await hold
    }
    return { value }
  })
  on('ui.toast', async ($, e) => {
    copy.toasts = [...(copy.toasts ?? []), e.text]
    return { value: undefined }
  })
  on('prompt.fill', async ($, e) => {
    copy.fills = [...(copy.fills ?? []), { text: e.text, mode: e.mode }]
    return { isFilled: true }
  })
  on('command.run', async ($, e) => {
    copy.commands = [...(copy.commands ?? []), { command: e.command, args: e.args }]
    if (copy.runHold !== undefined) await copy.runHold
    if (copy.runThrows !== undefined) throw new Error(copy.runThrows)
    return { text: '' }
  })
  // The session end a `/clear` brings, which runs the command a Plan or
  // Implement press holds (M221).
  on('session.end', async ($, e) => {
    if (copy.endHold !== undefined) await copy.endHold
    if (copy.endThrows === true) throw new Error('the end failed')
    return { sessionId: e.sessionId }
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

// Each priority's mark, written out by hand rather than read from
// `PRIORITY_MARK` (M253).
const MARKS = {
  high: { text: '↑', color: 'claude', bold: true },
  normal: { text: '○' },
  low: { text: '↓', color: 'inactive' },
} as const

// The candidates fixture's lines, written out by hand from its ROADMAP.
const CANDIDATE_LINES = [
  '↑ High row',
  '○ Normal row',
  '↓ Low row',
  '○ A row with no colon and space, cut at its dash',
  '○ [HIGH] Upper-case token, kept in the title',
  '○ [high]No space after the token, kept in the title',
  '○ Token in [low] mid-row, read as normal',
  '○ A long title that runs on well past the width of any docked pane, so the pane cuts it to one line with an ellipsis at its end',
  '○ `code',
  '○ ordinal',
  '○ loglog link for `binomial`. Needs a case',
  '○ Title — detail',
  '↓ Low row',
  '○ A `a',
  '○ A row with no colon and no dash',
]

describe('the idle pane lists the candidate rows (M207 AC1, AC2)', () => {
  for (const surface of SURFACES) {
    test(`the candidates fixture's heading, count, marks, and titles (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'candidates-head')).toBe('▎ CANDIDATES 15')
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
      // Each mark and its color are written out by hand (M253): ↑ high, ○
      // normal (the open circle, M253), and ↓ low.
      expect(textOf(await markOf(0))).toBe('↑')
      // The high mark takes the implement phase's theme key, written out
      // by hand (M217).
      expect((await markOf(0)).props.color).toBe('claude')
      expect(textOf(await markOf(1))).toBe('○')
      expect(textOf(await markOf(2))).toBe('↓')
      expect((await markOf(2)).props.color).toBe('inactive')
      // The high mark is bold, the normal mark has no color, and only a
      // low row's title is gray.
      expect((await markOf(0)).props.bold).toBe(true)
      expect((await markOf(1)).props.color).toBe(undefined)
      expect((await markOf(1)).props.bold).toBe(undefined)
      const titleOf = async (i: number) => kids((await ui.findAll({ key: `candidate-${i}-text` }))[0])[0]
      expect((await titleOf(2)).props.color).toBe('inactive')
      expect((await titleOf(0)).props.color).toBe(undefined)
      expect((await titleOf(1)).props.color).toBe(undefined)
      // The constant holds exactly these marks, so no stray color or bold
      // rides on the normal mark.
      expect(PRIORITY_MARK).toEqual(MARKS)
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
          candidates.map(row => `${MARKS[row.priority].text} ${row.title}`),
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
const blockedLine = (row: { id: string; title: string; pr: number | null; archived: boolean }) =>
  `${row.id}  ${row.title}${row.pr === null ? '' : `  #${row.pr}`}${row.archived ? '  archived' : ''}`

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
      // The first line also carries the ⌂ and ↻ Boxes after the tail (M236,
      // M241).
      expect(kids(head).map(keyOf)).toEqual([
        'M060-head-lead',
        'M060-head-text',
        'M060-head-tail',
        'M060-head-home',
        'M060-head-refresh',
      ])
      expect(kids(head)[2].props.flexShrink).toBe(0)
      expect(kids(head)[3].props.flexShrink).toBe(0)
      expect(kids(head)[4].props.flexShrink).toBe(0)
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
    for (const fixture of ['pane-full', 'candidates', 'blocked-prs', 'blocked-active', 'blocked-archived']) {
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
        taken: [],
      }
      const next = layout(state, [], true).find(line => line.key === 'next')
      expect([action, next?.action]).toEqual([action, undefined])
      // Nor Status, which shows only with the next-step Button (M219
      // review).
      expect([action, next?.buttons]).toEqual([action, undefined])
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

// M219: the Next line's Status Button, the Clear Button it carried until
// M241, and the first line's ⌂ (M241) and ↻ (M236), with their keys and
// labels written out by hand.
const PANE_STATUS = 'cairn-pane-status'
const PANE_CLEAR = 'cairn-pane-clear'
const PANE_HOME = 'cairn-pane-home'
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
        // the ⌂ and ↻ on the first line (M236, M241) and the ✎ of each
        // candidate line with a short title (M242). Before any read, no
        // blocked line carries one.
        const candidates = FIXTURES[name].pane.length === 0 ? FIXTURES[name].candidates : []
        const plans = candidates.flatMap((row, i) => (row.title === '' ? [] : [`cairn-pane-plan-${i}`]))
        expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual([PANE_HOME, PANE_REFRESH, PANE_NEXT, PANE_STATUS, ...plans])
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

// Until M241 a skill's end added Clear before Status. The pane now draws no
// Clear at any of these points, and the band's Clear is as its own tests
// assert (M241 AC4).
describe('a running skill hides Status, and its end adds no Clear (M219 AC2, M241 AC4)', () => {
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
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
      expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
      await $.prompt.submit({ text: 'a typed prompt', wait: false, origin: { kind: 'composer' } })
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
      expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
      await ui.unmount()
    })
  }

  test('paneLines gives the Next line Status alone while it acts', () => {
    const state: PaneState = {
      found: true,
      milestones: [],
      next: { action: 'plan the next milestone', command: '/milestone-plan', id: null, waiting: [] },
      workable: [],
      waiting: [],
      candidates: [],
      blocked: [],
      taken: [],
    }
    expect(layout(state, [], true).find(line => line.key === 'next')?.buttons).toEqual(['status'])
  })
})

describe('a press of Status runs its command (M219 AC3)', () => {
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
        // Every action Button is pressed below, ⌂ among them (M241), after
        // a skill's Stop, as before M241 (M241 review).
        await endSkill($)
        const ui = await mountPane($, surface)
        expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
        const [next] = await ui.findAll({ key: PANE_NEXT })
        expect(next.props.label).toBe(ACTION_LABELS[FIXTURES[name].next?.action as string])
        await ui.press({ key: PANE_NEXT })
        expect(copy.commands).toEqual([CLEAR_RUN])
        for (const key of [PANE_NEXT, PANE_HOME, PANE_STATUS]) await ui.press({ key })
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

// M241: the first line's ⌂, written out by hand.
const HOME = '⌂'

// The first line's key for a fixture: its first milestone's head line, or
// `no-active`.
function firstKey(name: string): string {
  const first = FIXTURES[name].pane[0]
  return first === undefined ? 'no-active' : `${first.id}-head`
}

// Waits up to `tries` waits of 5 ms for the opens beneath the mod to reach
// `n`, and then once more, so an unawaited open lands (M241).
async function untilOpens(copy: Copy, n: number, tries = 200) {
  for (let i = 0; i < tries && copy.opens.length < n; i++) await new Promise(resolve => setTimeout(resolve, 5))
  await new Promise(resolve => setTimeout(resolve, 5))
}

describe('the first line carries ⌂ before ↻ while no cairn skill runs (M241 AC1)', () => {
  for (const name of ['single-in-progress', 'no-active']) {
    for (const surface of SURFACES) {
      test(`${name}: ⌂ then ↻, and ↻ alone while a skill runs (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const key = firstKey(name)
        const first = (await boxOf(ui, key)) as Element
        expect(buttonsIn(first).map(keyOf)).toEqual([PANE_HOME, PANE_REFRESH])
        expect(kids(first).map(keyOf).slice(-2)).toEqual([`${key}-home`, `${key}-refresh`])
        expect((await boxOf(ui, `${key}-home`))?.props.flexShrink).toBe(0)
        const [home] = await ui.findAll({ key: PANE_HOME })
        expect([home.props.variant, home.props.label]).toEqual(['secondary', HOME])
        await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
        expect(buttonsIn((await boxOf(ui, key)) as Element).map(keyOf)).toEqual([PANE_REFRESH])
        expect(await ui.findAll({ key: PANE_HOME })).toEqual([])
        await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
        expect(buttonsIn((await boxOf(ui, key)) as Element).map(keyOf)).toEqual([PANE_HOME, PANE_REFRESH])
        await ui.unmount()
      })
    }
  }

  test('paneLines gives the first line home and refresh while it acts, and refresh alone otherwise', () => {
    const state: PaneState = {
      found: true,
      milestones: [],
      next: null,
      workable: [],
      waiting: [],
      candidates: [],
      blocked: [],
      taken: [],
    }
    expect(layout(state, [], true)[0]).toMatchObject({ key: 'no-active', buttons: ['home', 'refresh'] })
    expect(layout(state, [], false)[0]).toMatchObject({ key: 'no-active', buttons: ['refresh'] })
  })
})

describe('a press of ⌂ runs /clear once, and a guarded press runs nothing (M241 AC2)', () => {
  // On a milestone's head line and on the `no active milestone` line.
  for (const name of ['single-in-progress', 'no-active']) {
    test(`${name}: a free press runs clear with empty args`, async ($, on) => {
      const copy = copyOf(name)
      seat(on, copy)
      await $.turn.complete(turn())
      await pressKey($, PANE_HOME)
      expect(copy.commands).toEqual([CLEAR_RUN])
    })
  }

  // single-in-progress's Next is `Resume`, which runs its command with no
  // `/clear` first, so both presses hold a run in flight.
  for (const [label, key, want] of [
    ['Status', PANE_STATUS, STATUS_RUN],
    ['Resume', PANE_NEXT, runOf('single-in-progress')],
  ] as const) {
    test(`a press while a ${label} run is in flight runs nothing`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      let release = () => {}
      copy.runHold = new Promise<void>(resolve => {
        release = resolve
      })
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      const first = ui.press({ key })
      try {
        for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
        expect(copy.commands).toEqual([want])
        await ui.press({ key: PANE_HOME })
        expect(copy.commands).toEqual([want])
      } finally {
        release()
        await first
      }
      await ui.unmount()
    })
  }

  // One fixture for each held next step, `Plan` and `Implement`.
  const HELD = CLEARS_FIRST.map(action => PANE_CLEAR_FIRST.find(name => FIXTURES[name].next?.action === action) as string)
  test('the held cases reach both Plan and Implement', () => {
    expect(HELD.map(name => ACTION_LABELS[FIXTURES[name].next?.action as string]).sort()).toEqual(['Implement', 'Plan'])
  })

  for (const name of HELD) test(`${name}: a press while its command is held runs nothing`, async ($, on) => {
    const copy = copyOf(name)
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, PANE_NEXT)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, PANE_HOME)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    // The held command's end runs it, and opens no pane for a ⌂ press.
    const before = copy.opens.length
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, runOf(name)])
    expect(copy.opens.length).toBe(before)
  })

  // Two presses in the same tick: the mark is set before the press's first
  // await, so only one passes (M241 review, PR #251).
  test('two presses at once run clear once', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await Promise.all([ui.press({ key: PANE_HOME }), ui.press({ key: PANE_HOME })])
    await ui.unmount()
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
  })

  test('a second press, or a Status press, before the first press ends runs nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, PANE_HOME)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, PANE_HOME)
    await pressKey($, PANE_STATUS)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    // The end frees the Buttons again.
    await $.session.end(CLEAR_END)
    await pressKey($, PANE_STATUS)
    expect(copy.commands).toEqual([CLEAR_RUN, STATUS_RUN])
  })
})

describe("a ⌂ press's /clear opens the pane at its end, and nothing else does (M241 AC3)", () => {
  // The pane is open and sits behind another pane's tab, so the open shows.
  async function homeReady($, on) {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    copy.hidden = [PANE]
    return copy
  }

  // The fake `ui.open` shows a hidden pane, so the check below holds the
  // mod to the open call, not to what the desktop app does with it.
  test('a clear end after a press opens the pane once', async ($, on) => {
    const copy = await homeReady($, on)
    const before = copy.opens.length
    await pressKey($, PANE_HOME)
    expect(copy.opens.length).toBe(before)
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1)
    expect(copy.opens.slice(before)).toEqual([{ id: PANE, title: 'cairn' }])
    expect(panesOf(copy).find(each => each.id === PANE)?.isShown).toBe(true)
    // A later clear end opens nothing more.
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 2, 10)
    expect(copy.opens.length).toBe(before + 1)
  })

  // `other` also marks a reopen (M222), so `resume` is checked too (M241
  // review).
  for (const reason of ['other', 'resume'] as const) {
    test(`an end with reason ${reason} after a press opens nothing`, async ($, on) => {
      const copy = await homeReady($, on)
      const before = copy.opens.length
      await pressKey($, PANE_HOME)
      await $.session.end({ reason, sessionId: 's1' })
      await untilOpens(copy, before + 1, 10)
      expect(copy.opens.length).toBe(before)
    })
  }

  test('a refused clear leaves no open for a later clear end', async ($, on) => {
    const copy = await homeReady($, on)
    copy.runThrows = 'no such command here'
    const before = copy.opens.length
    await pressKey($, PANE_HOME)
    expect(copy.commands).toEqual([CLEAR_RUN])
    expect(copy.toasts?.[0]).toMatch(/^cairn: .* \(\/clear\)$/)
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1, 10)
    expect(copy.opens.length).toBe(before)
  })

  test('a clear end with no press opens nothing', async ($, on) => {
    const copy = await homeReady($, on)
    const before = copy.opens.length
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1, 10)
    expect(copy.opens.length).toBe(before)
  })
})

// A candidate line's ✎ (M242). The candidates fixture with three more rows
// at its end: one whose short title is empty, and two that share a title.
// The fixture's rows 2 and 12 also share the title `Low row` (M251).
const PANE_PLAN = 'cairn-pane-plan'
const PLAN_MARK = '✎'
const PLAN_COMMAND = 'cairn:milestone-plan'
const EMPTY_AT = 15
const SAME_AT = [16, 17]
function candidatesPlus(): Copy {
  const copy = copyOf('candidates')
  const path = Object.keys(copy.files).find(each => each.endsWith('cairn/ROADMAP.md')) as string
  copy.files[path] = copy.files[path].replace(
    '\n## Notes',
    '- : an empty short title — added 2026-01-10\n- Same title: one — added 2026-01-11\n- Same title: two — added 2026-01-12\n\n## Notes',
  )
  return copy
}
// The same copy with its one planned row done, so its Next is `Plan`.
function candidatesPlanNext(): Copy {
  const copy = candidatesPlus()
  const path = Object.keys(copy.files).find(each => each.endsWith('cairn/ROADMAP.md')) as string
  copy.files[path] = copy.files[path].replace('| M031 | Next up | planned |', '| M031 | Next up | done |')
  return copy
}
const TITLES = [...CANDIDATE_LINES.map(text => text.slice(2)), '', 'Same title', 'Same title']

describe('each candidate line with a short title carries ✎ while no cairn skill runs (M242 AC1)', () => {
  // The reader's lines for the copy, so the titles below are read, not
  // assumed (M242 review).
  test('the extra rows read as planned: an empty title and two equal ones', async ($, on) => {
    seat(on, candidatesPlus())
    await $.turn.complete(turn())
    const lines = await paneLines($, 'desktop')
    const rows = keysLike(lines, /^candidate-\d+$/).map(k => textAt(lines, k))
    expect(rows).toEqual([...CANDIDATE_LINES, '○ ', '○ Same title', '○ Same title'])
    expect(rows.map(text => (text as string).slice(2))).toEqual(TITLES)
  })

  for (const surface of SURFACES) {
    test(`✎ on each line with a title, none on the empty one, none while a skill runs (${surface})`, async ($, on) => {
      seat(on, candidatesPlus())
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const planKeys = async () => {
        const out: string[][] = []
        for (let i = 0; i < TITLES.length; i++) out.push(buttonsIn((await boxOf(ui, `candidate-${i}`)) as Element).map(keyOf) as string[])
        return out
      }
      const want = TITLES.map((title, i) => (title === '' ? [] : [`${PANE_PLAN}-${i}`]))
      expect(await planKeys()).toEqual(want)
      // The two rows with one title draw two keys.
      expect(new Set(SAME_AT.map(i => want[i][0])).size).toBe(2)
      for (const button of await ui.findAll({ type: 'Button' })) {
        if (!(keyOf(button) ?? '').startsWith(`${PANE_PLAN}-`)) continue
        expect([button.props.variant, button.props.label]).toEqual(['secondary', PLAN_MARK])
      }
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      expect(await planKeys()).toEqual(TITLES.map(() => []))
      await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
      expect(await planKeys()).toEqual(want)
      await ui.unmount()
    })
  }

  test('paneLines gives plan, the index, and the title to each titled row while it acts, and nothing otherwise', () => {
    const state: PaneState = {
      found: true,
      milestones: [],
      next: null,
      workable: [],
      waiting: [],
      candidates: [
        { priority: 'high', title: 'High' },
        { priority: 'normal', title: 'Normal' },
        { priority: 'low', title: 'Low' },
        { priority: 'normal', title: '' },
      ],
      blocked: [],
      taken: [],
    }
    const rows = (acts: boolean) => layout(state, [], acts).filter(line => /^candidate-\d+$/.test(line.key))
    expect(rows(true).map(line => [line.buttons, line.target, line.title])).toEqual([
      [['plan'], '0', 'High'],
      [['plan'], '1', 'Normal'],
      [['plan'], '2', 'Low'],
      [undefined, undefined, undefined],
    ])
    expect(rows(false).map(line => [line.key, line.buttons, line.target, line.title])).toEqual([
      ['candidate-0', undefined, undefined, undefined],
      ['candidate-1', undefined, undefined, undefined],
      ['candidate-2', undefined, undefined, undefined],
      ['candidate-3', undefined, undefined, undefined],
    ])
  })
})

describe("a press of ✎ runs /clear, and /cairn:milestone-plan with the row's title at its end (M242 AC2)", () => {
  // A high, a low, the backtick row, and the second of the two equal titles.
  for (const i of [0, 2, 8, SAME_AT[1]]) {
    test(`row ${i}: clear first, then the plan with the title`, async ($, on) => {
      const copy = candidatesPlus()
      seat(on, copy)
      await $.turn.complete(turn())
      await pressKey($, `${PANE_PLAN}-${i}`)
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([CLEAR_RUN])
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[i] }])
    })
  }
})

// The copy's first row gains a counted started token, so it is hidden, and
// a press on the row after it plans that row's own title (M261 AC3).
describe('a ✎ press on a line drawn after a hidden row plans its own row (M261 AC3)', () => {
  test('the hidden row draws no line or ✎, and the next row plans its title', async ($, on) => {
    const copy = candidatesPlus()
    const path = Object.keys(copy.files).find(each => each.endsWith('cairn/ROADMAP.md')) as string
    copy.files[path] = copy.files[path].replace(
      '- [high] High row: the text after the first colon and space is not shown — added 2026-01-01',
      '- [high] High row: the text after the first colon and space is not shown — added 2026-01-01 — started M031',
    )
    expect(copy.files[path]).toContain('— started M031')
    seat(on, copy)
    await $.turn.complete(turn())
    const keys = await keysOf($)
    expect(keys.filter(key => /^candidate-\d+$/.test(key))[0]).toBe('candidate-1')
    expect(keys).not.toContain('candidate-0')
    await pressKey($, `${PANE_PLAN}-1`)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[1] }])
    expect(TITLES[1]).toBe('Normal row')
  })
})

describe('a guarded ✎ press runs nothing (M242 AC3)', () => {
  test('a press while a Status run is in flight runs nothing', async ($, on) => {
    const copy = candidatesPlus()
    let release = () => {}
    copy.runHold = new Promise<void>(resolve => {
      release = resolve
    })
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    const first = ui.press({ key: PANE_STATUS })
    try {
      for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
      expect(copy.commands).toEqual([STATUS_RUN])
      await ui.press({ key: `${PANE_PLAN}-0` })
      expect(copy.commands).toEqual([STATUS_RUN])
    } finally {
      release()
      await first
    }
    await ui.unmount()
  })

  test('a press while a Plan command is held runs nothing, and the held Plan runs at the end', async ($, on) => {
    const copy = candidatesPlanNext()
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    const [next] = await ui.findAll({ key: PANE_NEXT })
    expect(next.props.label).toBe('Plan')
    await ui.unmount()
    await pressKey($, PANE_NEXT)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, `${PANE_PLAN}-0`)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: '' }])
  })

  test('a press while a ⌂ press is pending runs nothing, and the end opens the pane only', async ($, on) => {
    const copy = candidatesPlus()
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, PANE_HOME)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, `${PANE_PLAN}-0`)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    const before = copy.opens.length
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1)
    expect(copy.opens.length).toBe(before + 1)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
  })

  test('two presses at once run clear once', async ($, on) => {
    const copy = candidatesPlus()
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await Promise.all([ui.press({ key: `${PANE_PLAN}-0` }), ui.press({ key: `${PANE_PLAN}-1` })])
    await ui.unmount()
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    // The first press's title runs, not the second's (M242 review).
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[0] }])
  })

  // A refused `/clear` drops the hold, so a later clear end runs no plan,
  // and the next press is free (M242 review).
  test('a refused clear drops the held plan', async ($, on) => {
    const copy = candidatesPlus()
    copy.runThrows = 'no such command here'
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, `${PANE_PLAN}-1`)
    expect(copy.commands).toEqual([CLEAR_RUN])
    expect(copy.toasts?.[0]).toMatch(/^cairn: .* \(\/clear\)$/)
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    copy.runThrows = undefined
    await pressKey($, `${PANE_PLAN}-2`)
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 3)
    expect(copy.commands).toEqual([CLEAR_RUN, CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[2] }])
  })
})

describe('✎ sits at the right end of a candidate line, and the title gives way (M242 AC4)', () => {
  for (const surface of SURFACES) {
    // Row 1's title is short, and row 7's is longer than 44 columns.
    for (const i of [1, 7]) {
      test(`row ${i} at 44 columns (${surface})`, async ($, on) => {
        seat(on, candidatesPlus())
        await $.turn.complete(turn())
        const ui = await mountPane($, surface, 44)
        const text = (await boxOf(ui, `candidate-${i}-text`)) as Element
        expect([text.props.flexGrow, text.props.minWidth]).toEqual([1, 0])
        expect(kids(text)[0].props.wrap).toBe('truncate-end')
        if (i === 7) expect(width(textOf(kids(text)[0]))).toBeGreaterThan(44)
        const line = (await boxOf(ui, `candidate-${i}`)) as Element
        expect(kids(line).map(keyOf).slice(-2)).toEqual([`candidate-${i}-text`, `candidate-${i}-plan`])
        expect((await boxOf(ui, `candidate-${i}-plan`))?.props.flexShrink).toBe(0)
        await ui.unmount()
      })
    }
  }
})

describe('the pill gives way before Status (M219 AC4)', () => {
  for (const surface of SURFACES) {
    test(`the Button's Box does not shrink, and the pill's does (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      await endSkill($)
      const ui = await mountPane($, surface)
      for (const key of ['next-status']) {
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
// Since M237 a github.com URL takes one `gh api graphql` call for its word
// and its count, recorded apart in `graphql`, and only a URL of another
// form takes a `gh pr view` call, in `calls`. The fake answers the graphql
// call by the URL that its owner, repo, and number name, from both
// answers: `answer` gives the word's JSON as `gh pr view` prints it, and
// `graph` the threads, by default a reply with no unresolved thread. A
// rejecting, failing, or non-JSON `answer` is the call's answer as it is.
// A failing `graph` answer stands for threads that fail the shape check, so
// the reply carries the word and no threads. Either answer may be a
// promise, which holds the call until it settles. `reads` holds the URL of
// each pull request read, by either call, in order.
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
  reads: string[]
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
  const out: Gh = { calls: [], graphql: [], reads: [], git: [], lists: [], clocks: [], settled }
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
    if (!isGraph) {
      out.calls.push(e.argv)
      out.reads.push(e.argv[3])
      const got = await answer(e.argv[3])
      if (got === 'reject') throw new Error('gh cannot start')
      return value(got)
    }
    out.graphql.push(e.argv)
    const url = `https://github.com/${argOf(e.argv, 'owner')}/${argOf(e.argv, 'repo')}/pull/${argOf(e.argv, 'number')}`
    out.reads.push(url)
    const [word, part] = await Promise.all([answer(url), graph(url)])
    if (word === 'reject') throw new Error('gh cannot start')
    return value(graphReply(word, part))
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

// One graphql reply from a word answer and a threads answer, as the fake's
// comment above says (M237).
function graphReply(word: { exitCode: number; stdout: string }, part: GhAnswer): { exitCode: number; stdout: string } {
  if (word.exitCode !== 0) return word
  let view: unknown
  try {
    view = JSON.parse(word.stdout)
  } catch {
    return word
  }
  if (view === null || typeof view !== 'object' || Array.isArray(view)) return word
  let threads: unknown
  if (part !== 'reject' && part.exitCode === 0) {
    try {
      threads = (JSON.parse(part.stdout) as { data?: { repository?: { pullRequest?: { reviewThreads?: unknown } } } })?.data?.repository
        ?.pullRequest?.reviewThreads
    } catch {
      threads = undefined
    }
  }
  const pr = threads === undefined ? { ...view } : { ...view, reviewThreads: threads }
  return { exitCode: 0, stdout: `${JSON.stringify({ data: { repository: { pullRequest: pr } } })}\n` }
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
      // One graphql call reads the github.com URL, and no `gh pr view` runs
      // (M237 AC4).
      expect(calls.reads).toEqual([URL_1250])
      expect(calls.graphql.length).toBe(1)
      expect(calls.calls).toEqual([])
      expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  ${shape.word}`)
    })
  }

  test('a line not yet read shows no state word and no Button', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.reads).toEqual([])
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

  // M246 AC3: a blocked row whose milestone file was archived reads its PR
  // from the archive file. Its line carries `archived` after the number and
  // before the state word, or `archived` alone with no number. A merged one
  // carries the Finish Button for its id. A live row carries no `archived`.
  // The lines are written out by hand from the blocked-archived fixture.
  test('an archived row shows `archived`, its state word, and Finish', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-archived')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const archived = await blockedView($, 'blocked-M202')
    expect(archived.text).toBe('M202  The URL on the Status line  #21  archived  merged')
    expect(archived.buttons).toEqual(['cairn-pane-finish-M202'])
    const bare = await blockedView($, 'blocked-M204')
    expect(bare.text).toBe('M204  A URL only in a later paragraph  archived')
    expect(bare.buttons).toEqual([])
    const live = await blockedView($, 'blocked-M201')
    expect(live.text).toBe('M201  A live file  #11  merged')
    expect((await blockedView($, 'blocked-M206')).text).toBe('M206  A dropped archive')
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await ui.press({ key: 'cairn-pane-finish-M202' })
    await ui.unmount()
    expect(copy.commands).toEqual([{ command: 'cairn:milestone-review', args: 'M202' }])
  })

  // M246 review: an archived row carries no Revise or Check, since its
  // milestone file is gone. A live row keeps its Button.
  for (const each of [
    { answer: prView('OPEN', 'CHANGES_REQUESTED'), word: 'changes requested', live: 'cairn-pane-revise-M201' },
    { answer: prView('CLOSED', ''), word: 'closed', live: 'cairn-pane-check-M201' },
  ]) {
    test(`an archived row whose PR reads \`${each.word}\` carries no Button`, async ($, on) => {
      gh(on, () => each.answer)
      seat(on, copyOf('blocked-archived'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      const archived = await blockedView($, 'blocked-M202')
      expect(archived.text).toBe(`M202  The URL on the Status line  #21  archived  ${each.word}`)
      expect(archived.buttons).toEqual([])
      expect((await blockedView($, 'blocked-M201')).buttons).toEqual([each.live])
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
    calls.reads.length = 0
    calls.graphql.length = 0
    const closed = await $.command.run({ command: COMMAND })
    expect(closed.text).toBe('cairn pane closed')
    await calls.settled()
    expect(calls.reads).toEqual([])
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
    expect(calls.reads).toEqual([])
    expect(calls.graphql).toEqual([])
  })
})

// Each trigger reads the pull request with one `gh api graphql` call (M237),
// and a turn end runs none (M224 AC3, M225 AC1).
describe('the states are read at each pane open and at a Refresh press, and never on a timer (M224 AC3)', () => {
  const ONE_READ = [URL_1250]
  const graphOf = (calls: Gh) => calls.graphql.map(argv => [argOf(argv, 'owner'), argOf(argv, 'repo'), argOf(argv, 'number')])
  const ONE_QUERY = [['upstream', 'repo', '1250']]

  test('the /cairn-pane command reads once', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.reads).toEqual(ONE_READ)
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
    expect(calls.reads).toEqual(ONE_READ)
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
    calls.reads.length = 0
    calls.graphql.length = 0
    await $.session.start(NEW_START)
    await calls.settled()
    expect(listed(copy)).toBe(true)
    expect(calls.reads).toEqual(ONE_READ)
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
    expect((await blockedView($, 'M110-head')).buttons).toEqual(['cairn-pane-home', 'cairn-pane-refresh'])
    const press = async () => {
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      await ui.press({ key: 'cairn-pane-refresh' })
      await ui.unmount()
    }
    await press()
    expect(calls.reads).toEqual([...ONE_READ, ...ONE_READ])
    expect(graphOf(calls)).toEqual([...ONE_QUERY, ...ONE_QUERY])
    // A merged pull request takes the same one call, and no other (M237).
    state = 'MERGED'
    await press()
    expect(calls.reads).toEqual([...ONE_READ, ...ONE_READ, ...ONE_READ])
    expect(graphOf(calls)).toEqual([...ONE_QUERY, ...ONE_QUERY, ...ONE_QUERY])
    expect(calls.calls).toEqual([])
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
    calls.reads.length = 0
    calls.graphql.length = 0
    await $.turn.complete(turn())
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.reads).toEqual([])
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
  // OPEN, and M102 reads MERGED. Each github.com URL takes one query (M237),
  // and the two open ones each draw their own count.
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
    expect(asked.filter(each => each[1] !== 'upstream').sort()).toEqual([
      ['gh api graphql', 'alpha', 'one', '12'],
      ['gh api graphql', 'beta', 'two', '90'],
    ])
    expect(calls.calls).toEqual([])
    // Each query names the state, the decision, and the threads (M237).
    for (const argv of calls.graphql) {
      const query = argOf(argv, 'query') ?? ''
      expect(query.includes('{ state reviewDecision reviewThreads(last: 100) { nodes { isResolved } } }')).toBe(true)
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
  // Since M237 the one query also gives the word, so a line that is not
  // open still takes it, and draws no count.
  for (const each of NOT_OPEN) {
    test(`a ${each.name} line takes one query and draws no count`, async ($, on) => {
      const calls = gh(on, () => each.answer, () => countsReply(3))
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.reads.length).toBe(1)
      expect(calls.graphql.length).toBe(1)
      expect(calls.calls).toEqual([])
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

// Since M237 the word and the threads come in one reply, so a failed call
// reads `unknown` (M224 AC4 above), and only threads that fail the shape
// check leave the word with no count (M237 AC4).
describe('threads that fail the shape check draw no count line and leave the state word (M225 AC4, M237 AC4)', () => {
  const reply = (pr: unknown): GhAnswer => ({ exitCode: 0, stdout: `${JSON.stringify({ data: { repository: { pullRequest: pr } } })}\n` })
  const good = JSON.parse((countsReply(2) as { stdout: string }).stdout).data.repository.pullRequest
  const FAILS: { name: string; answer: GhAnswer }[] = [
    { name: 'no reviewThreads', answer: reply({}) },
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
  'gh', 'pr', 'list', '--repo', url, '--state', 'open', '--author', '@me', '--limit', '100', '--json', 'number,title,url,headRefName,body',
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
  // M237 AC4: a hotfix URL on a host other than github.com takes one
  // `gh pr view` call for its word and gets no count, while the github.com
  // blocked URL beside it takes one graphql call and draws its count.
  test('a hotfix on another host takes one gh pr view call and draws no count', async ($, on) => {
    const OTHER = 'https://ghe.example.com/upstream/repo/pull/7'
    const calls = gh(on, () => prView('OPEN', 'REVIEW_REQUIRED'), () => countsReply(2), {
      remotes: { origin: ORIGIN },
      list: () => listReply([{ number: 7, title: 'Fix 7', url: OTHER, headRefName: 'hotfix-other' }]),
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.calls).toEqual([['gh', 'pr', 'view', OTHER, '--json', 'state,reviewDecision']])
    expect(calls.graphql.map(argv => [argOf(argv, 'owner'), argOf(argv, 'repo'), argOf(argv, 'number')])).toEqual([
      ['upstream', 'repo', '1250'],
    ])
    expect(calls.reads.sort()).toEqual([OTHER, URL_1250].sort())
    const lines = await linesAt($)
    const textOf_ = (key: string) => lines.find(line => line.key === key)?.text
    expect(textOf_('hotfix-7')).toBe('#7  Fix 7  in review')
    expect(textOf_('hotfix-7-counts')).toBe(undefined)
    expect(textOf_('blocked-M111-counts')).toBe('2 unresolved threads')
  })

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
    // Each hotfix takes the one query (M237), and the merged one draws no
    // count, as a merged blocked line draws none.
    expect(calls.graphql.map(argv => argOf(argv, 'number')).sort()).toEqual(['1250', '1263', '1264', '1265'])
    expect(calls.calls).toEqual([])
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
    const viewsOf1265 = () => calls.reads.filter(url => url ===prUrl(1265)).length
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
    // Besides the first line, each candidate line's text grows, so ✎ sits at
    // its right end, and no other line does (M242, M242 review).
    const candidates = got.lines.map(keyOf).filter(key => /^candidate-\d+$/.test(key ?? ''))
    expect(grows(got.lines)).toEqual([[`${firstKey}-text`, 1], ...candidates.map(key => [`${key}-text`, 1])])
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

  test('the Next line with Status after a skill ends, and one active milestone', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await endSkill($)
    const got = await one($, `${FIXTURES['single-in-progress'].pane[0].id}-head`)
    expect(got.keys).toEqual([PANE_HOME, PANE_REFRESH, PANE_NEXT, PANE_STATUS])
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
    expect(calls.reads.filter(url => url ===prUrl(1265)).length).toBe(2)
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
      await until(() => calls.reads.length === 1)
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
    await until(() => calls.reads.length === 1)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.reads.length === 2)
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
    await until(() => calls.reads.length === 1)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.reads.length === 2)
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
      await until(() => calls.reads.length === 2)
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
    expect(calls.reads.length).toBe(3)
  })

  // The first assertion is M237 AC3's: a stored true with no read in flight
  // in this module draws ↻, not ⋯.
  test('a stored reading state with no read in this module draws ↻ and lets a press read', async ($, on) => {
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
    expect(await labelOf($)).toBe('↻')
    await pressKey($, PANE_REFRESH)
    await calls.settled()
    expect(calls.reads.length).toBe(1)
    expect(await labelOf($)).toBe('↻')
  })

  // M237 AC3: a read whose write of `reading` false fails leaves the stored
  // value true, and the next drawing after it settles still shows ↻. The
  // hook answers `{ deny }`, which rejects the mod's write, so the stored
  // value stays true. The redraw the mod asks for after that failure is not
  // tested here: with it removed, a pane mounted through the read still
  // read ↻ in this harness (M237 review).
  test('a failed write of the reading state false still draws ↻ once the read settles', async ($, on) => {
    const held_ = gate()
    const calls = gh(on, async () => {
      await held_.wait
      return prView('OPEN', '')
    })
    seat(on, copyOf('blocked-active'))
    const refused: unknown[] = []
    on('state.set', async ($, e, next) => {
      const value = (e as { value?: { value?: unknown } }).value?.value
      if (e.plugin === 'cairn' && e.key === 'reading' && value === false) {
        refused.push(value)
        return { deny: 'the store refused the write' }
      }
      return next(e)
    })
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await until(() => calls.reads.length === 1)
    expect(await labelOf($)).toBe('⋯')
    held_.release()
    await calls.settled()
    await until(() => refused.length > 0)
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
      await until(() => calls.reads.length > 0)
      expect(calls.reads).toEqual([URL_1250])
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
      await until(() => calls.reads.length > 0)
      expect(calls.reads).toEqual([URL_1250])
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
      await until(() => calls.reads.length > 0)
      await $.session.end({ reason: 'other', sessionId: 's1' })
      newProcess(copy)
      calls.reads.length = 0
      expect(await finishes($.session.start(NEW_START))).toBe('finished')
      expect(listed(copy)).toBe(true)
      await until(() => calls.reads.length > 0)
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      release()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
  })
})

describe('the blocked reads start before the hotfix list settles (M230 AC2)', () => {
  test("the blocked URL's read runs while gh pr list is held", async ($, on) => {
    const { calls, release, listSettled } = held(on)
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    try {
      await $.command.run({ command: COMMAND })
      await until(() => calls.reads.length > 0 && calls.lists.length > 0)
      expect(calls.lists).toEqual([listCall(ORIGIN)])
      expect(listSettled()).toBe(false)
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      release()
    }
    await calls.settled()
    // Once the list settles, its hotfix URL is read too.
    expect(calls.reads).toEqual([URL_1250, prUrl(1265)])
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
      await until(() => calls.reads.length > 0 && calls.lists.length > 0)
      expect(calls.lists).toEqual([listCall(ORIGIN)])
      expect(calls.reads).toEqual([URL_1250])
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
      expect(calls.reads).toEqual([])
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

  // A resumed process raises `session.start` first and then the resume
  // hook, which reads the files again (M237 review).
  test('a resumed process start draws the rows once both hooks have run', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    tick(copy)
    await $.classic.SessionStart({ source: 'resume' })
    const band = await bandText($)
    expect(band).toContain('M002')
    expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBe(T2_DONE)
    await $.turn.complete(turn())
    expect(await bandText($)).toBe(band)
  })

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
          expect(calls.reads.sort()).toEqual([URL_1250, prUrl(1265)].sort())
          expect((await blockedView($, 'blocked-M111')).text).toBe(`${LINE_1250}  in review`)
        } else {
          expect(all).toEqual([])
        }
      })
    }
  }
})

// One draw of the pane, as a surface that places it makes (M238).
async function draw($) {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
  await ui.unmount()
}
const sorted = (list: string[]) => [...list].sort()

// A clear or resume start that finds the pane listed but not placed owes a
// read, and the pane's first draw starts it (M238 AC1). The repo has no
// remote, so no hotfix list runs and `reads` holds the blocked URLs alone.
describe('a pane placed after a clear or resume start reads at its first draw (M238 AC1)', () => {
  const CASES = [
    { source: 'clear', fixture: 'blocked-active', urls: [URL_1250] },
    { source: 'resume', fixture: 'blocked-prs', urls: [prUrl(12), prUrl(34), prUrl(90)] },
  ] as const
  for (const { source, fixture, urls } of CASES) {
    test(`a ${source} start reads nothing, and the first draw reads each URL once (${fixture})`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf(fixture)
      seat(on, copy)
      copy.open = [PANE]
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source })
      await calls.settled()
      expect(calls.reads).toEqual([])
      copy.unplaced = []
      await draw($)
      await calls.settled()
      expect(sorted(calls.reads)).toEqual(sorted([...urls]))
      await draw($)
      await calls.settled()
      expect(sorted(calls.reads)).toEqual(sorted([...urls]))
      // The read's words reach the pane (M238 review).
      const key = fixture === 'blocked-active' ? 'blocked-M111' : 'blocked-M101'
      expect((await blockedView($, key)).text).toMatch(/  in review$/)
    })
  }

  const OPENS: { name: string; open: ($, copy: Copy) => Promise<void> }[] = [
    { name: 'a /cairn-pane open', open: async $ => void (await $.command.run({ command: COMMAND })) },
    {
      name: "a press of the band's open button",
      open: async $ => {
        const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
        await ui.press({ key: 'cairn-open' })
        await ui.unmount()
      },
    },
  ]
  for (const { name, open } of OPENS) {
    test(`${name} between the start and the first draw leaves that draw reading nothing`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf('blocked-active')
      seat(on, copy)
      copy.open = [PANE]
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source: 'clear' })
      await open($, copy)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    })
  }

  const NONE: { name: string; before: ($, copy: Copy) => Promise<void> }[] = [
    { name: 'with no clear or resume start before it', before: async $ => void (await $.turn.complete(turn())) },
    {
      name: 'after a start that found no pane listed',
      before: async ($, copy) => {
        copy.open = []
        await $.classic.SessionStart({ source: 'clear' })
        copy.open = [PANE]
      },
    },
    {
      name: 'after a start whose pane list threw',
      before: async ($, copy) => {
        copy.open = [PANE]
        copy.unplaced = [PANE]
        copy.panesThrow = true
        await $.classic.SessionStart({ source: 'resume' })
        copy.panesThrow = false
        copy.unplaced = []
      },
    },
  ]
  for (const { name, before } of NONE) {
    test(`a first draw ${name} reads nothing`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf('blocked-active')
      seat(on, copy)
      await before($, copy)
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([])
    })
  }
})

// A clear start's pane list answers not placed, and the pane is placed and
// drawn before that answer reaches the hook. The draw comes before the hook
// owes a read, so it reads nothing, and the hook's second list reads (M256
// AC1).
describe('a pane placed while a clear start lists the panes reads with no further draw (M256 AC1)', () => {
  const CASES = [
    { fixture: 'blocked-active', urls: [URL_1250] },
    { fixture: 'blocked-prs', urls: [prUrl(12), prUrl(34), prUrl(90)] },
  ] as const
  for (const { fixture, urls } of CASES) {
    test(`the hook reads each URL once after its held list (${fixture})`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf(fixture)
      seat(on, copy)
      copy.open = [PANE]
      copy.unplaced = [PANE]
      let release = () => {}
      copy.panesHold = new Promise<void>(resolve => {
        release = resolve
      })
      const start = $.classic.SessionStart({ source: 'clear' })
      try {
        await until(() => copy.panesHold === undefined)
        // The hook's list is held, its answer computed as not placed.
        expect(copy.panesHold).toBeUndefined()
        expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(false)
        copy.unplaced = []
        await draw($)
        await calls.settled()
        expect(calls.reads).toEqual([])
      } finally {
        release()
      }
      await start
      await calls.settled()
      expect(sorted(calls.reads)).toEqual(sorted([...urls]))
    })
  }

  // The second list is held too, its answer computed as placed. A draw
  // while it waits takes the owed read, so the list reads nothing more.
  test('a draw while the second list waits takes the read, and the list reads nothing more', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    let releaseFirst = () => {}
    let releaseSecond = () => {}
    copy.panesHold = new Promise<void>(resolve => {
      releaseFirst = resolve
    })
    const second = new Promise<void>(resolve => {
      releaseSecond = resolve
    })
    const start = $.classic.SessionStart({ source: 'clear' })
    try {
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(false)
      copy.unplaced = []
      copy.panesHold = second
      releaseFirst()
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHold).toBeUndefined()
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(true)
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      releaseFirst()
      releaseSecond()
    }
    await start
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })
})

// A session end clears the read a clear start owed, so the pane's first
// draw after the end reads nothing (M256 AC2).
describe('a session end clears an owed read (M256 AC2)', () => {
  test('a pane owed a read at a session end reads nothing at its first draw after it', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    await $.classic.SessionStart({ source: 'clear' })
    await calls.settled()
    expect(calls.reads).toEqual([])
    await $.session.end(CLEAR_END)
    copy.unplaced = []
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([])
  })
})

// A process start can raise both the reopen's `session.start` and a resume
// or clear `classic.SessionStart`. Between them they read each URL once
// (M238 AC2). Source `clear` is a guard, since no record shows a reopened
// start raising it.
describe('one process start reads each URL once (M238 AC2)', () => {
  const OTHER_END = { reason: 'other', sessionId: 's1' } as const
  // An open pane at an `other` end, so the next start in the folder reopens
  // it, with the open's own read settled and cleared from `reads`.
  async function marked($, on): Promise<{ calls: Gh; copy: Copy }> {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    await openPane($, on, copy)
    await calls.settled()
    await $.session.end(OTHER_END)
    newProcess(copy)
    calls.reads.length = 0
    return { calls, copy }
  }
  for (const source of ['resume', 'clear'] as const) {
    test(`the reopen, then a ${source} start, read each URL once`, async ($, on) => {
      const { calls } = await marked($, on)
      await $.session.start(NEW_START)
      await $.classic.SessionStart({ source })
      await calls.settled()
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    })

    test(`a ${source} start, then the reopen, read each URL once`, async ($, on) => {
      const { calls } = await marked($, on)
      await $.classic.SessionStart({ source })
      await $.session.start(NEW_START)
      await calls.settled()
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    })
  }

  test('an unplaced reopen, a resume start, and the first draw read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.notPlaced = 'the terminal is too narrow'
    await $.session.start(NEW_START)
    await $.classic.SessionStart({ source: 'resume' })
    await calls.settled()
    copy.notPlaced = undefined
    copy.unplaced = []
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // The read at the first draw is the start's read, so a reopen after it
  // reads nothing (M238 review). In a new process the pane is not listed
  // before the reopen, so this order is a guard, not one seen on a host.
  test('a resume start that owes, the first draw, then the reopen read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    await $.classic.SessionStart({ source: 'resume' })
    await calls.settled()
    expect(calls.reads).toEqual([])
    copy.unplaced = []
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
    await $.session.start(NEW_START)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // A pane placed before both hooks: the resume hook reads, and the reopen
  // after it reads nothing (M238 review).
  test('a resume start that reads, then the reopen, read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.open = [PANE]
    await $.classic.SessionStart({ source: 'resume' })
    await $.session.start(NEW_START)
    await calls.settled()
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // Both hooks of one start begun together, for a placed pane (M238
  // review). The harness runs the two in turn, so this test passed before
  // the classic hook's second `startRead` check, and it does not test that
  // check.
  test('the reopen and a resume start begun together read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.open = [PANE]
    await Promise.all([$.session.start(NEW_START), $.classic.SessionStart({ source: 'resume' })])
    await calls.settled()
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // A clear start reads again after a session end, also while an open's
  // read is still in flight.
  test('a clear start reads again while an open read is held', async ($, on) => {
    const { calls, release } = held(on)
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start(NEW_START)
    try {
      await $.command.run({ command: COMMAND })
      await until(() => calls.reads.length > 0)
      await $.session.end(CLEAR_END)
      await $.classic.SessionStart({ source: 'clear' })
      await until(() => calls.reads.filter(url => url === URL_1250).length > 1)
      expect(calls.reads.filter(url => url === URL_1250)).toEqual([URL_1250, URL_1250])
    } finally {
      release()
    }
  })

  // A session end ends the start, so after a reopen's read, a clear start in
  // the same process reads again.
  test("a clear start after a session end reads again after the reopen's read", async ($, on) => {
    const { calls } = await marked($, on)
    await $.session.start(NEW_START)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
    await $.session.end(CLEAR_END)
    await $.classic.SessionStart({ source: 'clear' })
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250, URL_1250])
  })
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
    expect(calls.reads.filter(url => url ===URL_1250).length).toBe(1)
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

// Two presses in the same tick of a blocked line's `Finish`: the press marks
// itself busy before its first await, so the second runs nothing (M243 AC1).
describe('two presses at once of a blocked line Button run its command once (M243 AC1)', () => {
  test('cairn-pane-finish-M111', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await Promise.all([ui.press({ key: 'cairn-pane-finish-M111' }), ui.press({ key: 'cairn-pane-finish-M111' })])
    await ui.unmount()
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([{ command: 'cairn:milestone-review', args: 'M111' }])
  })
})

// A Status press and a ⌂ press in the same tick each mark `busy` before
// their first await, so only the press listed first runs (M243 AC2). ⌂
// marks itself since M241, so the ⌂-first order held before M243 too.
describe('a Status press and a ⌂ press at once run only the first one (M243 AC2)', () => {
  const ORDERS = [
    { keys: [PANE_STATUS, PANE_HOME], run: STATUS_RUN },
    { keys: [PANE_HOME, PANE_STATUS], run: CLEAR_RUN },
  ]
  for (const { keys, run } of ORDERS) {
    test(keys.join(' then '), async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      // Both Buttons are drawn, so each press reaches its handler.
      for (const key of keys) expect((await ui.findAll({ key })).length).toBe(1)
      await Promise.all(keys.map(key => ui.press({ key })))
      await ui.unmount()
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([run])
    })
  }
})

// A press whose checks fail takes its mark back, so the next free press
// runs (M243 AC4).
describe('a press whose checks fail leaves the next press free (M243 AC4)', () => {
  test('a Finish press during a step, then a Status press after the step ends', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
    // Finish stays drawn while the step runs (M224 review).
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    await pressKey($, 'cairn-pane-finish-M111')
    expect(copy.commands ?? []).toEqual([])
    await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
    await pressKey($, PANE_STATUS)
    expect(copy.commands).toEqual([STATUS_RUN])
  })

  test('a Finish press that reads a changed PR word, then a Status press', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    // Once `changed` is set, every stored PR reads `closed`, which carries
    // the Check Button, not Finish, so the Finish press's check fails.
    let changed = false
    on('state.get', async ($, e, next) => {
      const got = await next(e)
      if (!changed || e.plugin !== 'cairn' || e.key !== 'prs') return got
      const read_ = (got as { value?: { version?: number; value?: { shape?: string; value?: Record<string, object> } } } | undefined)?.value
      const words = read_?.value?.value ?? {}
      const closed = Object.fromEntries(Object.entries(words).map(([url, each]) => [url, { ...each, word: 'closed' }]))
      return { value: { version: read_?.version ?? 0, value: { shape: read_?.value?.shape ?? 'prs-3', value: closed } } }
    })
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    changed = true
    await ui.press({ key: 'cairn-pane-finish-M111' })
    await ui.unmount()
    expect(copy.commands ?? []).toEqual([])
    // The press read `closed`, not an empty store: a drawing now carries
    // the Check Button.
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-check-M111'])
    await pressKey($, PANE_STATUS)
    expect(copy.commands).toEqual([STATUS_RUN])
  })
})

// M252: a candidate row that an open pull request's body names in a
// `Candidate row: <short title>` line draws as started. The items each case
// expects are written out by hand.
const bodied = (n: number, branch: string, body: unknown) => ({ ...pr(n, branch), body })

describe('startedRows reads the Candidate row lines of each listed body (M252 AC1)', () => {
  const read = (entries: unknown[]) => startedRows(listReply(entries) as { exitCode: number; stdout: string })

  test('every head branch counts, and each line gives one item', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', 'Fixes the parse.\n\nCandidate row: Pane edges (M238 review)\n'),
        bodied(2, 'm252-pane', 'Candidate row: Retitle edges\nCandidate row: Band in the app\'s code font'),
        bodied(3, 'feature-x', 'Candidate row: An idea for later'),
      ]),
    ).toEqual([
      { title: 'Pane edges (M238 review)', number: 1 },
      { title: 'Retitle edges', number: 2 },
      { title: "Band in the app's code font", number: 2 },
      { title: 'An idea for later', number: 3 },
    ])
  })

  test('the prefix must open the line, exactly', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', 'See Candidate row: Not this one\n  Candidate row: Nor this one\ncandidate row: Nor lower case\nCandidate row:No space'),
      ]),
    ).toEqual([])
  })

  test('the rest is trimmed, and an empty or blank rest gives no item', () => {
    expect(read([bodied(1, 'hotfix-a', 'Candidate row: \nCandidate row:    \nCandidate row:  Spaced title \t')])).toEqual([
      { title: 'Spaced title', number: 1 },
    ])
  })

  test('a CRLF body loses each line end', () => {
    expect(read([bodied(1, 'hotfix-a', 'Intro\r\nCandidate row: One\r\nCandidate row: Two\r\n')])).toEqual([
      { title: 'One', number: 1 },
      { title: 'Two', number: 1 },
    ])
  })

  test('an entry with a non-string body or a non-integer number gives none', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', null),
        pr(2, 'hotfix-b'),
        { ...bodied(3, 'hotfix-c', 'Candidate row: Three'), number: '3' },
        { ...bodied(4, 'hotfix-d', 'Candidate row: Four'), number: 4.5 },
        null,
        'Candidate row: Five',
        bodied(6, 'hotfix-f', 'Candidate row: Six'),
      ]),
    ).toEqual([{ title: 'Six', number: 6 }])
  })

  // M257: a line between a fence line and the next fence line names no row.
  test('a line inside a backtick, tilde, or indented fence gives no item', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', '```\nCandidate row: Inside backticks\n```\nCandidate row: After backticks'),
        bodied(2, 'hotfix-b', '~~~markdown\nCandidate row: Inside tildes\n~~~\nCandidate row: After tildes'),
        bodied(3, 'hotfix-c', 'Intro\n   ```\nCandidate row: Inside spaced\n  ```\nCandidate row: After spaced'),
      ]),
    ).toEqual([
      { title: 'After backticks', number: 1 },
      { title: 'After tildes', number: 2 },
      { title: 'After spaced', number: 3 },
    ])
  })

  test('any fence line closes an open fence, whatever its character', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', '```\nCandidate row: Inside mixed\n~~~\nCandidate row: After mixed'),
        bodied(2, 'hotfix-b', '~~~\nCandidate row: Inside mixed\n```\nCandidate row: After mixed'),
      ]),
    ).toEqual([
      { title: 'After mixed', number: 1 },
      { title: 'After mixed', number: 2 },
    ])
  })

  test('a fence that never closes hides the rest of its body only', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', 'Candidate row: Before\n```\nCandidate row: Unclosed one\nCandidate row: Unclosed two'),
        bodied(2, 'hotfix-b', 'Candidate row: Next body'),
      ]),
    ).toEqual([
      { title: 'Before', number: 1 },
      { title: 'Next body', number: 2 },
    ])
  })

  test('a call that rejected, failed, or printed no JSON array gives null', () => {
    expect(startedRows(null)).toBe(null)
    expect(startedRows({ exitCode: 1, stdout: '[]\n' })).toBe(null)
    expect(startedRows({ exitCode: 0, stdout: 'HTTP 502\n' })).toBe(null)
    expect(startedRows({ exitCode: 0, stdout: '{"number":1}\n' })).toBe(null)
  })
})

describe('a candidate row that an item names is not drawn (M261 AC1, AC2)', () => {
  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: [
      { priority: 'high', title: 'High row' },
      { priority: 'normal', title: 'Normal row' },
      { priority: 'low', title: 'Low row' },
      { priority: 'normal', title: 'Unmatched row' },
      { priority: 'normal', title: 'Shared title' },
      { priority: 'low', title: 'Shared title' },
      { priority: 'normal', title: 'case row' },
      { priority: 'normal', title: '' },
    ],
    blocked: [],
    taken: [],
  }
  const items = [
    { title: 'High row', number: 11 },
    { title: 'Normal row', number: 14 },
    { title: 'Normal row', number: 12 },
    { title: 'Low row', number: 13 },
    { title: 'Shared title', number: 15 },
    { title: 'Case row', number: 16 },
    { title: '', number: 17 },
  ]
  const rows = (acts: boolean, started = items) => layout(state, [], acts, {}, [], started).filter(line => /^candidate-\d+$/.test(line.key))
  const heads = (started = items) => layout(state, [], true, {}, [], started).filter(line => line.key.startsWith('candidates-head'))

  for (const acts of [true, false]) {
    test(`matched rows draw no line, and the others draw as before under their own keys (acts ${acts})`, () => {
      const got = rows(acts)
      const before = rows(acts, [])
      // Unmatched, a title that differs only by case, and an empty title.
      const kept = [3, 6, 7]
      expect(got.map(line => line.key)).toEqual(kept.map(i => `candidate-${i}`))
      got.forEach((line, n) => expect([line.key, line]).toEqual([line.key, before[kept[n]]]))
    })

    // A hidden row between a high and a low row, the low one with an empty
    // short title, so neither a priority mark nor the ✎ rule shifts.
    test(`a hidden row between a high and an untitled low row leaves both as before (acts ${acts})`, () => {
      const three: PaneState = {
        ...state,
        candidates: [
          { priority: 'high', title: 'Up' },
          { priority: 'normal', title: 'Taken' },
          { priority: 'low', title: '' },
        ],
      }
      const draw = (started: { title: string; number: number }[]) =>
        layout(three, [], acts, {}, [], started).filter(line => /^candidate-\d+$/.test(line.key))
      const before = draw([])
      const got = draw([{ title: 'Taken', number: 5 }])
      expect(got.map(line => line.key)).toEqual(['candidate-0', 'candidate-2'])
      expect(got).toEqual([before[0], before[2]])
      expect([got[0].lead[0], got[1].lead[0]]).toEqual([MARKS.high, MARKS.low])
      expect([got[0].buttons, got[1].buttons]).toEqual(acts ? [['plan'], undefined] : [undefined, undefined])
    })
  }

  test('the heading counts the drawn rows only (AC2)', () => {
    const [gap, head] = heads()
    expect([gap.key, head.key]).toEqual(['candidates-head-gap', 'candidates-head'])
    expect(head.lead.slice(-1)).toEqual([{ text: '3', color: GRAY }])
    // The control: with no items every row draws and counts.
    expect(heads([])[1].lead.slice(-1)).toEqual([{ text: `${state.candidates.length}`, color: GRAY }])
  })

  test('with every row hidden there is no heading and no gap (AC2)', () => {
    const all = state.candidates.map((row, i) => ({ title: row.title === '' ? 'never' : row.title, number: 100 + i }))
    const one: PaneState = { ...state, candidates: state.candidates.filter(row => row.title !== '' && row.title !== 'case row') }
    const lines = layout(one, [], true, {}, [], all)
    expect(lines.filter(line => line.key.startsWith('candidate'))).toEqual([])
    // The control: one row left draws the heading and its gap.
    const left = layout(one, [], true, {}, [], all.slice(1))
    expect(left.filter(line => line.key.startsWith('candidates-head')).map(line => line.key)).toEqual([
      'candidates-head-gap',
      'candidates-head',
    ])
  })

  // The lines the pre-M252 code drew, written out by hand: the priority
  // mark, no tail, and ✎ on each titled row while `acts` is true.
  test('with no items every candidate line draws as before', () => {
    const lines = rows(true, [])
    expect(lines.length).toBe(state.candidates.length)
    lines.forEach((line, i) => {
      const row = state.candidates[i]
      expect([i, line.lead, line.tail]).toEqual([i, [MARKS[row.priority], { text: ' ' }], undefined])
      expect([i, line.text]).toEqual([i, row.priority === 'low' ? { text: row.title, color: GRAY } : { text: row.title }])
      expect([i, line.buttons, line.target]).toEqual(row.title === '' ? [i, undefined, undefined] : [i, ['plan'], `${i}`])
    })
  })
})

// M258: a counted ` — started <ref>` token on the row marks it too. The
// reader keeps an `M<NNN>` token only while its milestone is `planned` or
// `blocked` (reader.test.ts), so `taken` here holds counted M tokens.
describe('a candidate row that a started token marks is not drawn (M258 AC1-AC3, M261 AC1)', () => {
  const titles = ['Planned', 'Blocked', 'Two ids', 'Listed', 'Unlisted', 'Two numbers', 'Body and id', 'Number and id', 'Body and number', 'Plain']
  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: titles.map(title => ({ priority: 'normal', title })),
    blocked: [],
    taken: [],
  }
  const hotfix = (number: number) => ({ number, title: `Fix ${number}`, url: `https://github.com/o/r/pull/${number}` })
  const draw = (taken: PaneState['taken'], hotfixes = [hotfix(301), hotfix(302), hotfix(305)], started: { title: string; number: number }[] = []) =>
    layout({ ...state, taken }, [], true, {}, hotfixes, started).filter(line => /^candidate-\d+$/.test(line.key))
  // A hidden row draws no line under its key. A drawn row keeps its index
  // in `state.candidates` as its key and its ✎ target (M261).
  const hidden = (lines, i: number) => expect([i, lines.find(line => line.key === `candidate-${i}`)]).toEqual([i, undefined])
  const plain = (lines, i: number) => {
    const line = lines.find(each => each.key === `candidate-${i}`)
    expect([i, line?.lead[0], line?.tail, line?.text]).toEqual([i, MARKS.normal, undefined, { text: titles[i] }])
    expect([i, line?.buttons, line?.target]).toEqual([i, ['plan'], `${i}`])
  }

  test('a counted milestone id hides its row (AC1)', () => {
    const lines = draw([
      { title: 'Planned', ref: 'M258' },
      { title: 'Blocked', ref: 'M240' },
      { title: 'Two ids', ref: 'M300' },
      { title: 'Two ids', ref: 'M259' },
    ])
    hidden(lines, 0)
    hidden(lines, 1)
    hidden(lines, 2)
    for (let i = 3; i < titles.length; i++) plain(lines, i)
  })

  // The milestone row and its neighbours in table order, as M261 AC1 asks.
  test('a hidden row between two plain rows leaves them drawn in order', () => {
    const lines = draw([{ title: 'Unlisted', ref: 'M258' }])
    expect(lines.map(line => line.key)).toEqual(titles.map((_, i) => `candidate-${i}`).filter(key => key !== 'candidate-4'))
    plain(lines, 3)
    plain(lines, 5)
  })

  test('a #n token hides its row only while the open hotfix list holds n (AC2)', () => {
    const taken = [
      { title: 'Listed', ref: '#301' },
      { title: 'Unlisted', ref: '#999' },
      { title: 'Two numbers', ref: '#998' },
      { title: 'Two numbers', ref: '#305' },
    ]
    const lines = draw(taken)
    plain(lines, 2)
    hidden(lines, 3)
    plain(lines, 4)
    hidden(lines, 5)
    plain(lines, 6)
    // With no hotfix list, as before any read or for another root, no #n
    // token counts.
    const none = draw(taken, [])
    titles.forEach((_, i) => plain(none, i))
  })

  test('a body line, a #n token, and a milestone id in any mix hide the row (AC3)', () => {
    const lines = draw(
      [
        { title: 'Body and id', ref: 'M258' },
        { title: 'Number and id', ref: 'M258' },
        { title: 'Number and id', ref: '#302' },
        { title: 'Body and number', ref: '#301' },
      ],
      undefined,
      [
        { title: 'Body and id', number: 400 },
        { title: 'Body and number', number: 350 },
      ],
    )
    hidden(lines, 6)
    hidden(lines, 7)
    hidden(lines, 8)
    plain(lines, 9)
  })

  // The reader's filter and the drawing together (M258 review return 1):
  // an id counts only while its table row is `planned` or `blocked`.
  test('a done, dropped, or absent id leaves the row drawn, planned and blocked hide it (AC1)', () => {
    const roadmap = [
      '| ID | Title | Status | Depends on | Priority | File/Archive |',
      '|---|---|---|---|---|---|',
      '| M258 | P | planned | — | normal | m |',
      '| M240 | B | blocked | — | normal | m |',
      '| M230 | D | done | — | normal | m |',
      '| M231 | X | dropped | — | normal | m |',
      '',
      '## Candidates',
      '',
      '- Planned: x — started M258',
      '- Blocked: x — started M240',
      '- Done: x — started M230',
      '- Dropped: x — started M231',
      '- Absent: x — started M999',
      '- Two ids: x — started M230 — started M240',
    ].join('\n')
    const candidates = candidateRows(roadmap)
    const lines = layout(
      { ...state, candidates, taken: takenRows(roadmap, parseRoadmapRows(roadmap)) },
      [],
      true,
      {},
      [],
      [],
    ).filter(line => /^candidate-\d+$/.test(line.key))
    expect(candidates.map(row => row.title)).toEqual(['Planned', 'Blocked', 'Done', 'Dropped', 'Absent', 'Two ids'])
    expect(lines.map(line => [line.key, line.text?.text, line.target])).toEqual([
      ['candidate-2', 'Done', '2'],
      ['candidate-3', 'Dropped', '3'],
      ['candidate-4', 'Absent', '4'],
    ])
  })

  test('a token on a row with an empty short title hides nothing', () => {
    const lines = layout(
      { ...state, candidates: [{ priority: 'normal', title: '' }], taken: [{ title: '', ref: 'M258' }] },
      [],
      true,
      {},
      [],
      [],
    ).filter(line => /^candidate-\d+$/.test(line.key))
    expect([lines[0].lead[0], lines[0].tail, lines[0].buttons]).toEqual([MARKS.normal, undefined, undefined])
  })
})

// The copy's one candidate row: a read whose items name it hides the row,
// and with it the Candidates heading (M261 AC1, AC2).
describe('the pane read stores the items with the hotfix list and hides the rows they name (M252 AC3, M261)', () => {
  const STARTED_BODY = 'Fixes it.\nCandidate row: An idea for later\n'
  const MARKED = undefined
  const PLAIN = '○ An idea for later'
  const GOOD = () => listReply([bodied(1265, 'm252-pane', STARTED_BODY)])
  const candidateLine = async $ => (await linesAt($)).find(line => line.key === 'candidate-0')?.text

  test('the call asks for body, a read hides the line, and the Hotfixes section skips an m-branch', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: GOOD })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.lists).toEqual([listCall(ORIGIN)])
    expect(await candidateLine($)).toBe(MARKED)
    expect((await keysOf($)).filter(key => key.startsWith('candidate'))).toEqual([])
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
  })

  test('a failed call in the same root keeps the row hidden', async ($, on) => {
    let answer: () => GhAnswer = GOOD
    gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: () => answer() })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect(await candidateLine($)).toBe(MARKED)
    answer = () => 'reject'
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(MARKED)
    answer = () => listReply([])
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
    // The drawn line carries ✎ again (M252 review).
    expect((await blockedView($, 'candidate-0')).buttons).toEqual([`${PANE_PLAN}-0`])
  })

  test('a root with no base-remote URL draws the row again', async ($, on) => {
    const remotes: Record<string, string> = { origin: ORIGIN }
    gh(on, () => prView('MERGED'), undefined, { remotes, list: GOOD })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect(await candidateLine($)).toBe(MARKED)
    delete remotes.origin
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
  })

  test('a failed call in another root draws the row the first root hid', async ($, on) => {
    let answer: () => GhAnswer = GOOD
    gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: () => answer() })
    const copy = copyOf('blocked-prs')
    for (const path of Object.keys(copy.files)) copy.files[`/other${path}`] = copy.files[path]
    copy.unreadable.push(...copy.unreadable.map(path => `/other${path}`))
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect(await candidateLine($)).toBe(MARKED)
    answer = () => 'reject'
    copy.cwd = '/other'
    await $.turn.complete(turn())
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
    // Back in the first root, a failed call finds the other root's empty
    // value, not the first root's items.
    copy.cwd = '/'
    await $.turn.complete(turn())
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
  })
})

// A one-shot hold on the mod's `step` read. It is armed after mount, since
// the draw reads the key too, and it fires once, so the session end's
// update of the key passes (M255).
function holdStep(on: On) {
  let open = () => {}
  const gate = new Promise<void>(resolve => (open = resolve))
  const hold = { armed: false, held: false, release: () => open() }
  on('state.get', async ($, e, next) => {
    if (hold.armed && e.plugin === 'cairn' && e.key === 'step') {
      hold.armed = false
      hold.held = true
      await gate
    }
    return next(e)
  })
  return hold
}

describe('a press check cut off by a session end frees the Buttons and runs nothing late (M255 AC1, AC2)', () => {
  test('a Status press after the end runs once, and the cut-off press runs nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_STATUS })
    await until(() => hold.held)
    expect(hold.held).toBe(true)
    expect(copy.commands ?? []).toEqual([])
    await $.session.end(CLEAR_END)
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands).toEqual([STATUS_RUN])
    hold.release()
    await first
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([STATUS_RUN])
    await ui.unmount()
  })

  // While the end beneath is still running, the cut-off press's mark keeps
  // a new press from reading the state of the session that is ending.
  test('a press during the end, while a cut-off press reads, runs nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_STATUS })
    await until(() => hold.held)
    let finish = () => {}
    copy.endHold = new Promise<void>(resolve => (finish = resolve))
    const end = $.session.end(CLEAR_END)
    await sleep(20)
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands ?? []).toEqual([])
    copy.endHold = undefined
    finish()
    await end
    hold.release()
    await first
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands).toEqual([STATUS_RUN])
    await ui.unmount()
  })

  // A next-step press whose checks would hold its command for a `/clear`.
  const name = PANE_CLEAR_FIRST[0]
  test(`${name}: a cut-off next-step press holds nothing for a later clear end`, async ($, on) => {
    const copy = copyOf(name)
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_NEXT })
    await until(() => hold.held)
    expect(hold.held).toBe(true)
    expect(copy.commands ?? []).toEqual([])
    await $.session.end(CLEAR_END)
    hold.release()
    await first
    await untilRuns(copy, 1, 10)
    expect(copy.commands ?? []).toEqual([])
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 1, 10)
    expect(copy.commands ?? []).toEqual([])
    await ui.unmount()
  })
})

describe("a ⌂ press's open still runs when the session end beneath rejects (M255 AC3)", () => {
  test('a clear end whose next(e) rejects opens the pane once', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const before = copy.opens.length
    await pressKey($, PANE_HOME)
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    await untilOpens(copy, before + 1)
    await untilOpens(copy, before + 2, 10)
    expect(copy.opens.slice(before)).toEqual([{ id: PANE, title: 'cairn' }])
  })

  test('a clear end whose next(e) rejects, with no press, opens nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const before = copy.opens.length
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    await untilOpens(copy, before + 1, 10)
    expect(copy.opens.length).toBe(before)
  })
})

// A session end that rejects frees the action Buttons, so a press whose
// `/clear` run never settles leaves none dead (M260 AC1).
describe('a rejected session end frees the action Buttons (M260 AC1)', () => {
  test("a Status press after a rejected end runs, while the ⌂ press's /clear never settles", async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    let settle = () => {}
    copy.runHold = new Promise<void>(resolve => (settle = resolve))
    void ui.press({ key: PANE_HOME })
    await untilRuns(copy, 1)
    expect(copy.commands).toEqual([CLEAR_RUN])
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    copy.endThrows = undefined
    void ui.press({ key: PANE_STATUS })
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, STATUS_RUN])
    copy.runHold = undefined
    settle()
    await ui.unmount()
  })

  // A press made while the end beneath is pending keeps its run when the
  // end settles, resolved or rejected, so a second press does not run
  // beside it (M260 review, PR #271).
  for (const rejects of [false, true]) {
    test(`a press made during a ${rejects ? 'rejecting' : 'resolving'} end keeps its run past the end`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      let finish = () => {}
      copy.endHold = new Promise<void>(resolve => (finish = resolve))
      copy.endThrows = rejects ? true : undefined
      const end = $.session.end(CLEAR_END).then(
        () => false,
        () => true,
      )
      await sleep(20)
      let settle = () => {}
      copy.runHold = new Promise<void>(resolve => (settle = resolve))
      void ui.press({ key: PANE_STATUS })
      await untilRuns(copy, 1)
      expect(copy.commands).toEqual([STATUS_RUN])
      copy.endHold = undefined
      finish()
      expect(await end).toBe(rejects)
      copy.endThrows = undefined
      void ui.press({ key: PANE_STATUS })
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([STATUS_RUN])
      copy.runHold = undefined
      settle()
      await ui.unmount()
    })
  }

  // A press whose checks are still reading at the rejected end leaves the
  // shared press mark free too, so a later press runs (M260 review).
  test('a Status press after a rejected end that cut off a press still reading runs once', async ($, on) => {
    const copy = copyOf('single-in-progress')
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_STATUS })
    await until(() => hold.held)
    expect(hold.held).toBe(true)
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    copy.endThrows = undefined
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands).toEqual([STATUS_RUN])
    hold.release()
    await first
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([STATUS_RUN])
    await ui.unmount()
  })
})

// A held command that a rejected session end drops goes to the prompt box,
// and a toast says why, for an end of either reason (M260 AC2).
describe('a rejected session end hands its held command to the prompt box (M260 AC2)', () => {
  const name = PANE_CLEAR_FIRST[0]
  for (const reason of ['clear', 'other'] as const) {
    test(`${name}: a rejected ${reason} end fills the held command and toasts`, async ($, on) => {
      const copy = copyOf(name)
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      await ui.press({ key: PANE_NEXT })
      expect(copy.commands).toEqual([CLEAR_RUN])
      copy.endThrows = true
      let rejected = false
      try {
        await $.session.end({ reason, sessionId: 's1' })
      } catch {
        rejected = true
      }
      expect(rejected).toBe(true)
      const run = runOf(name)
      const line = run.args === '' ? `/${run.command}` : `/${run.command} ${run.args}`
      for (let i = 0; i < 200 && ((copy.toasts ?? []).length < 1 || (copy.fills ?? []).length < 1); i++) await sleep(5)
      expect(copy.fills).toEqual([{ text: line, mode: 'append' }])
      expect(copy.toasts).toEqual([`cairn: the session end failed (${line})`])
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([CLEAR_RUN])
      await ui.unmount()
    })
  }
})

// A session end that lands while a ⌂ press reads its step cancels the
// press, so its `/clear` never reaches the conversation that follows. A
// `clear` end still gives the pane the open it gives any ⌂ mark, and an
// `other` end none (M260 AC3).
describe("a session end during a ⌂ press's step read cancels its /clear (M260 AC3)", () => {
  const ENDS = [
    { name: 'a resolving clear end', reason: 'clear', rejects: false, opens: 1 },
    { name: 'a rejecting clear end', reason: 'clear', rejects: true, opens: 1 },
    { name: 'a resolving other end', reason: 'other', rejects: false, opens: 0 },
    { name: 'a rejecting other end', reason: 'other', rejects: true, opens: 0 },
  ] as const
  for (const { name, reason, rejects, opens } of ENDS) {
    test(`${name} runs no /clear and opens the pane ${opens} time(s)`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      const hold = holdStep(on)
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      hold.armed = true
      const first = ui.press({ key: PANE_HOME })
      await until(() => hold.held)
      expect(hold.held).toBe(true)
      expect(copy.commands ?? []).toEqual([])
      const before = copy.opens.length
      copy.endThrows = rejects ? true : undefined
      let rejected = false
      try {
        await $.session.end({ reason, sessionId: 's1' })
      } catch {
        rejected = true
      }
      expect(rejected).toBe(rejects)
      copy.endThrows = undefined
      hold.release()
      await first
      await untilRuns(copy, 1, 10)
      expect(copy.commands ?? []).toEqual([])
      await untilOpens(copy, before + opens)
      await untilOpens(copy, before + opens + 1, 10)
      expect(copy.opens.slice(before)).toEqual(opens === 1 ? [{ id: PANE, title: 'cairn' }] : [])
      await ui.unmount()
    })
  }
})

// A start's second pane listing that is still pending at a session end
// reads nothing when it answers, even placed and with a later start's read
// owed, so the read a later start owes is that start's; here the pane's next
// draw makes it (M260 AC4).
describe('a second listing pending at a session end reads nothing (M260 AC4)', () => {
  test("the old start's placed second listing adds no read, and the next draw reads once", async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    let releaseFirst = () => {}
    let releaseSecond = () => {}
    copy.panesHold = new Promise<void>(resolve => {
      releaseFirst = resolve
    })
    const second = new Promise<void>(resolve => {
      releaseSecond = resolve
    })
    const old = $.classic.SessionStart({ source: 'clear' })
    try {
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(false)
      // The second listing's answer is computed placed when it is held.
      copy.unplaced = []
      copy.panesHold = second
      releaseFirst()
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHold).toBeUndefined()
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(true)
      await $.session.end(CLEAR_END)
      // The new start lists the pane unplaced twice, so it owes a read and
      // makes none.
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source: 'clear' })
      await calls.settled()
      expect(calls.reads).toEqual([])
    } finally {
      releaseFirst()
      releaseSecond()
    }
    await old
    await calls.settled()
    expect(calls.reads).toEqual([])
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // The same holds one list earlier: a first listing pending at a session
  // end reads nothing when it answers placed, and leaves the later start's
  // owed read in place (M260 review).
  test("the old start's placed first listing adds no read, and the next draw reads once", async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = []
    let release = () => {}
    copy.panesHold = new Promise<void>(resolve => {
      release = resolve
    })
    const old = $.classic.SessionStart({ source: 'clear' })
    try {
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(true)
      await $.session.end(CLEAR_END)
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source: 'clear' })
      await calls.settled()
      expect(calls.reads).toEqual([])
    } finally {
      release()
    }
    await old
    await calls.settled()
    expect(calls.reads).toEqual([])
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })
})
