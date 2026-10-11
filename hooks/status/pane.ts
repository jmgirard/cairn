import type { CairnHotfixPr, CairnPrRead, CairnPrWord } from '../../types'
import type { PrCounts } from './counts'
import type { Span } from './band'
import type { FlowPhase } from './band'
import { FLOW_COLORS, flowOf, GRAY } from './band'
import type { BandRow, CandidateRow, PaneItem, PaneMilestone, PaneState } from './reader'
import { PILL_TEXT } from './track'

// The cairn pane's lines (M205), as a plain description that register.tsx
// draws. For each active milestone: its id in its phase's color (no phase
// word since M236), and its title, with the
// band's percent for the row at the end of the line when its file reads
// (M208), its goal, its tasks and criteria with their boxes, and its
// newest work-log lines.
// Below them: the command that scripts/cairn_next.py recommends, the
// workable planned milestones, and the planned ones that wait on
// dependencies. Then the blocked milestones, each with the number of the
// pull request its header names (M223), and after a read, that pull
// request's state word and a Button for three of the words (M224), and for
// an open one with unresolved review threads, a line under it with their
// number (M225, M236). After a read, the
// open pull requests that the operator opened from `hotfix-*` branches,
// each with the same word and counts and no Button (M226). With no
// active milestone, the ROADMAP's candidate rows follow, each a priority
// mark and its short title (M207).
// A line's `lead` and `tail` keep their width. Its `text` is cut to one
// line with an ellipsis, but for the goal's lines, which wrap: the operator
// picked one line per item at the M205 live look, so a long task list fits
// on one screen.
// The operator picked the look at the M208 prototypes: a blank row, a
// `▎`, and a gray uppercase label for each section heading, eight squares
// beside the Tasks and Criteria counts, the Next command in a pill, and the
// percent alone on the head line, with no track. At the live look the
// operator asked for the phase colors: a milestone's marks and meters take
// its phase's color, the queue's take plan's, and the pill takes the color
// of the phase its command runs. The colors are theme keys (M217).
// While no cairn skill runs, the Next line also carries the band's
// next-step label after the pill, which register.tsx draws as a Button
// (M218). After that Button the line carries Status, and Clear before it
// while `ended` is true, which register.tsx draws as Buttons (M219).

// The Next line's `action`, when set, is the label of the next-step Button
// drawn after its tail. No other line carries one: register.tsx draws it
// with the one key `cairn-pane-next` and the next-step press.
// A line's `buttons` name the Buttons that register.tsx draws after its
// tail and any action Button, in order: Clear and Status on the Next line
// (M219), and one of Finish, Revise, or Check on a blocked line (M224). A
// blocked line's `target` is its milestone id, which its Button's key and
// press carry. Since M236 the pane's first line carries the one Refresh
// Button, labeled ↻, which reads everything again. Its `grow` makes its
// text take the free room, so its tail and the Button sit at the right end
// of the row. Until M236 the Blocked and Hotfixes headings each carried a
// Refresh.
export type PaneButton = 'clear' | 'status' | 'refresh' | 'finish' | 'revise' | 'check'
export type PaneLine = {
  key: string
  indent: number
  lead: Span[]
  text: Span | null
  tail?: Span[]
  wraps?: true
  action?: string
  buttons?: PaneButton[]
  target?: string
  grow?: true
}

// A blocked milestone's pull request state, as `wordOf` maps it from a
// `gh api graphql` reply (counts.ts `prRead`, M237) or, for a URL on
// another host, from a `gh pr view <url> --json state,reviewDecision` call
// (`prWord`, M224). The state contract holds the one list of words.
export type PrWord = CairnPrWord

// One read of a pull request: its word, and its counts while it is open
// and its threads passed the shape check (M225, M237).
export type PrRead = CairnPrRead

// The words `wordOf` gives an OPEN pull request, the ones that carry
// counts (M225, M237).
export const OPEN_WORDS: readonly PrWord[] = ['changes requested', 'approved', 'in review']

// The count line's text, or null when the count is zero. One thread reads
// in the singular (M225, M236).
export function countsText(counts: PrCounts): string | null {
  if (counts.unresolved === 0) return null
  return `${counts.unresolved} unresolved ${counts.unresolved === 1 ? 'thread' : 'threads'}`
}

// The state word of one `gh pr view` result, null for a call that
// rejected. A non-zero exit, text that is not a JSON object, or a `state`
// other than MERGED, CLOSED, or OPEN reads as `unknown`. An OPEN pull
// request reads by its `reviewDecision`, and any decision but
// CHANGES_REQUESTED or APPROVED, an empty or absent one included, reads as
// `in review`.
export function prWord(result: { exitCode: number; stdout: string } | null): PrWord {
  if (result === null || result.exitCode !== 0) return 'unknown'
  let view: unknown
  try {
    view = JSON.parse(result.stdout)
  } catch {
    return 'unknown'
  }
  if (view === null || typeof view !== 'object') return 'unknown'
  const { state, reviewDecision } = view as { state?: unknown; reviewDecision?: unknown }
  return wordOf(state, reviewDecision)
}

// The state word of a pull request's `state` and `reviewDecision`, as
// `prWord` reads them from `gh pr view` and `prRead` in counts.ts from
// `gh api graphql` (M237), which give the same values.
export function wordOf(state: unknown, reviewDecision: unknown): PrWord {
  if (state === 'MERGED') return 'merged'
  if (state === 'CLOSED') return 'closed'
  if (state !== 'OPEN') return 'unknown'
  if (reviewDecision === 'CHANGES_REQUESTED') return 'changes requested'
  if (reviewDecision === 'APPROVED') return 'approved'
  return 'in review'
}

// An open pull request from a `hotfix-*` branch (M226).
export type HotfixPr = CairnHotfixPr

// The head branch prefix of a hotfix (tracking-rules git model).
export const HOTFIX_PREFIX = 'hotfix-'

// The hotfix pull requests of one `gh pr list --json
// number,title,url,headRefName` result, in the order it lists them, or
// null for a call that rejected, exited non-zero, or printed something
// other than a JSON array (M226). An entry that is not an object, or has no
// string `headRefName`, no string `url`, or no integer `number`, is
// skipped, and so is one whose branch does not start with `hotfix-`, and a
// second entry with a URL or number already kept, so no two lines share a
// key (M226 review). A title that is not a string reads as empty.
export function hotfixPrs(result: { exitCode: number; stdout: string } | null): HotfixPr[] | null {
  if (result === null || result.exitCode !== 0) return null
  let list: unknown
  try {
    list = JSON.parse(result.stdout)
  } catch {
    return null
  }
  if (!Array.isArray(list)) return null
  const out: HotfixPr[] = []
  for (const entry of list) {
    if (entry === null || typeof entry !== 'object') continue
    const { number, title, url, headRefName } = entry as Record<string, unknown>
    if (typeof headRefName !== 'string' || !headRefName.startsWith(HOTFIX_PREFIX)) continue
    if (typeof url !== 'string' || typeof number !== 'number' || !Number.isInteger(number)) continue
    if (out.some(pr => pr.url === url || pr.number === number)) continue
    out.push({ number, title: typeof title === 'string' ? title : '', url })
  }
  return out
}

// The Button a blocked line carries for its state word (M224), from the
// routes that /milestone gives a handed-off PR: a merged one goes to
// review's hygiene, one with changes requested back to implement, and a
// closed one to /milestone. The other words carry none.
export const PR_BUTTON: Partial<Record<PrWord, PaneButton>> = {
  merged: 'finish',
  'changes requested': 'revise',
  closed: 'check',
}

// A state word's color: the review phase's for a merged or approved pull
// request, the warning key for one with changes requested, gray otherwise.
function prColor(word: PrWord): string {
  if (word === 'merged' || word === 'approved') return FLOW_COLORS.review
  if (word === 'changes requested') return WARNING
  return GRAY
}

// The next-step Button's label by the action that scripts/cairn_next.py
// names (M212), planning among them (M213). The band and the pane read
// this one map (M218).
export const PLAN_LABEL = 'Plan'
export const NEXT_LABELS: Record<string, string> = {
  review: 'Review',
  resume: 'Resume',
  implement: 'Implement',
  'plan the next milestone': PLAN_LABEL,
}

// The actions whose next-step Button runs `/clear` first and its command in
// the cleared conversation (M221): `Implement` and `Plan`. A resumed run
// and a review keep their conversation. Each is a key of `NEXT_LABELS`.
export const CLEARS_FIRST: readonly string[] = ['implement', 'plan the next milestone']

// An action's label, read from the map's own keys only, so an action named
// like an object property, such as `toString`, has none (M218 review).
export function nextLabel(action: string): string | undefined {
  return Object.prototype.hasOwnProperty.call(NEXT_LABELS, action) ? NEXT_LABELS[action] : undefined
}

// The Status and Clear Buttons' labels (M212, M216). The band and the
// pane's Next line read these (M219).
export const STATUS_LABEL = 'Status'
export const CLEAR_LABEL = 'Clear'
// The pane's Refresh Button (M224, one ↻ on the first line since M236),
// its label while a read of the pull request states runs (M236), and a
// blocked line's Buttons (M224).
export const REFRESH_LABEL = '↻'
export const READING_LABEL = '⋯'
export const FINISH_LABEL = 'Finish'
export const REVISE_LABEL = 'Revise'
export const CHECK_LABEL = 'Check'

export const NO_ROADMAP = 'no cairn ROADMAP found'
export const NO_FILE = 'no milestone file'
export const NO_ACTIVE = 'no active milestone'
export const CHECKED_MARK = '✓'
export const OPEN_MARK = '○'
// A candidate row's mark for each priority (M207).
export const PRIORITY_MARK: Record<CandidateRow['priority'], Span> = {
  high: { text: '↑', color: FLOW_COLORS.implement, bold: true },
  normal: { text: '·' },
  low: { text: '↓', color: GRAY },
}
// A section heading's accent mark, in the phase's color (M208).
export const ACCENT_MARK = '▎'
// The meter's squares, filled and empty, and how many it draws (M208).
export const METER_FULL = '■'
export const METER_EMPTY = '□'
export const METER_CELLS = 8
// The empty squares' theme key, as the band's terminal track marks use (M208 review).
export const METER_EMPTY_KEY = 'subtle'
// The warning text's theme key, as the band's warning labels use.
const WARNING = 'warning'

// A milestone's id draws in its phase's color, with no phase word, which
// the operator dropped at the M236 live look.
const PHASE_COLOR: Record<string, string> = {
  'in-progress': FLOW_COLORS.implement,
  review: FLOW_COLORS.review,
}
// The phase each recommended command runs, for the Next pill's color.
export const COMMAND_PHASE: Record<string, FlowPhase> = {
  '/milestone-plan': 'plan',
  '/milestone-implement': 'implement',
  '/milestone-review': 'review',
}
// The queue's headings are about planned, blocked, and candidate work.
const QUEUE_COLOR = FLOW_COLORS.plan

const line = (key: string, indent: number, lead: Span[], text: Span | null = null): PaneLine => ({
  key,
  indent,
  lead,
  text,
})

// One blank row, before each section heading, each milestone after the
// first, and Next.
const gap = (key: string) => line(key, 0, [], { text: ' ' })

// The filled share of the meter: none only with no box checked, and all
// only with every box checked.
export function meterFill(checked: number, total: number): number {
  if (total === 0 || checked === 0) return 0
  if (checked >= total) return METER_CELLS
  return Math.min(METER_CELLS - 1, Math.max(1, Math.round((METER_CELLS * checked) / total)))
}

export function meter(checked: number, total: number, color: string): Span[] {
  const fill = meterFill(checked, total)
  return [
    { text: METER_FULL.repeat(fill), color },
    { text: METER_EMPTY.repeat(METER_CELLS - fill), color: METER_EMPTY_KEY },
  ].filter(span => span.text !== '')
}

// A section heading and the blank row before it: the accent in `color`,
// the label in gray uppercase, and its count and meter where it has them.
function heading(key: string, label: string, color: string, after: Span[] = []): PaneLine[] {
  return [
    gap(`${key}-gap`),
    line(key, 0, [
      { text: ACCENT_MARK, color },
      { text: ' ' },
      { text: label.toUpperCase(), color: GRAY, bold: true },
      ...after,
    ]),
  ]
}

function counted(key: string, label: string, list: PaneItem[], color: string): PaneLine[] {
  const checked = list.filter(item => item.checked).length
  return heading(key, label, color, [
    { text: ' ' },
    { text: `${checked}/${list.length}`, color: GRAY },
    { text: ' ' },
    ...meter(checked, list.length, color),
  ])
}

function items(prefix: string, list: PaneItem[]): PaneLine[] {
  return list.map((item, i) =>
    line(
      `${prefix}-${i}`,
      2,
      [item.checked ? { text: CHECKED_MARK, color: GRAY } : { text: OPEN_MARK }, { text: ' ' }],
      item.checked ? { text: item.text, color: GRAY } : { text: item.text },
    ),
  )
}

function milestoneLines(row: PaneMilestone, band: BandRow | undefined): PaneLine[] {
  const phase = { color: PHASE_COLOR[row.status] ?? GRAY }
  const head = line(`${row.id}-head`, 0, [{ text: row.id, color: phase.color, bold: true }, { text: '  ' }], { text: row.title })
  const file = row.file
  // The band's percent for the row, from its own counts, which count a box
  // inside an HTML comment where the pane's items do not.
  const flow = file === null || band === undefined ? null : flowOf(band)
  if (flow !== null && flow.percent !== null) head.tail = [{ text: '  ' }, { text: `${flow.percent}%`, color: GRAY }]
  const out: PaneLine[] = [head]
  if (file === null) return [...out, line(`${row.id}-nofile`, 2, [], { text: NO_FILE, color: WARNING })]
  if (file.goal !== '') {
    out.push(...heading(`${row.id}-goal-head`, 'Goal', phase.color))
    // A blank line between paragraphs draws as one space, so it keeps its row.
    file.goal.split('\n').forEach((text, i) =>
      out.push({ ...line(`${row.id}-goal-${i}`, 2, [], { text: text === '' ? ' ' : text }), wraps: true }),
    )
  }
  if (file.tasks.length > 0) {
    out.push(...counted(`${row.id}-tasks-head`, 'Tasks', file.tasks, phase.color))
    out.push(...items(`${row.id}-task`, file.tasks))
  }
  if (file.criteria.length > 0) {
    out.push(...counted(`${row.id}-criteria-head`, 'Criteria', file.criteria, phase.color))
    out.push(...items(`${row.id}-criterion`, file.criteria))
  }
  if (file.log.length > 0) {
    out.push(...heading(`${row.id}-log-head`, 'Work log', phase.color))
    file.log.forEach((text, i) => out.push(line(`${row.id}-log-${i}`, 2, [], { text, color: GRAY })))
  }
  return out
}

// The pane's lines from its state and the band's rows, whose counts give
// each head line its percent. `acts` is true while no cairn skill's step is
// set, and then the Next line carries its action label (M218) and the
// Status Button after it (M219). `ended` is true from a
// Stop that ends a cairn skill's step until the next idle typed prompt,
// cairn skill prompt, or session end, and then the Clear Button comes
// before Status (M219). `prs` holds each pull request's state word by its
// URL, from the last read (M224), with its counts (M225). `hotfixes` holds
// the open hotfix pull requests of the last read for this root (M226).
export function paneLines(
  state: PaneState,
  band: BandRow[] = [],
  acts = false,
  ended = false,
  prs: Record<string, PrRead> = {},
  hotfixes: HotfixPr[] = [],
): PaneLine[] {
  if (!state.found) return [line('no-roadmap', 0, [], { text: NO_ROADMAP, color: GRAY })]
  const out: PaneLine[] = []
  if (state.milestones.length === 0) out.push(line('no-active', 0, [], { text: NO_ACTIVE, color: GRAY }))
  state.milestones.forEach((row, i) => {
    if (i > 0) out.push(gap(`${row.id}-gap`))
    out.push(...milestoneLines(row, band.find(b => b.id === row.id && b.status === row.status)))
  })
  // The first line, the first milestone's head line or the no-active line,
  // carries the ↻ Button at its right end (M236).
  out[0].buttons = ['refresh']
  out[0].grow = true
  if (state.next !== null) {
    const target = state.next.id === null ? state.next.command : `${state.next.command} ${state.next.id}`
    out.push(gap('next-gap'))
    const next = line('next', 0, [{ text: 'Next', bold: true }, { text: '  ' }], {
      text: ` ${target} `,
      color: PILL_TEXT,
      backgroundColor: FLOW_COLORS[COMMAND_PHASE[state.next.command] ?? 'implement'],
      // Bold, as the band's pill is. The text and fill are the theme's own
      // keys (M217), so their contrast is the theme's.
      bold: true,
    })
    const label = nextLabel(state.next.action)
    // Status and Clear follow the next-step Button and show only with it, as
    // the band's show only with a next-step label (M219 review).
    if (acts && label !== undefined) {
      next.action = label
      next.buttons = ended ? ['clear', 'status'] : ['status']
    }
    out.push(next)
  }
  if (state.workable.length > 0) {
    out.push(...heading('workable-head', 'Workable', QUEUE_COLOR))
    for (const row of state.workable) {
      out.push(line(`workable-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], { text: row.title }))
    }
  }
  if (state.waiting.length > 0) {
    out.push(...heading('waiting-head', 'Waiting', QUEUE_COLOR))
    for (const row of state.waiting) {
      out.push(
        line(`waiting-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], {
          text: `${row.title} · on ${row.unmet.join(', ')}`,
        }),
      )
    }
  }
  // The blocked rows, each with its pull request's number when its
  // milestone file's header names one, whether or not a milestone is
  // active (M223). After the number, the state word that the last read
  // found, and the Button that word carries (M224).
  if (state.blocked.length > 0) {
    const head = heading('blocked-head', 'Blocked', QUEUE_COLOR, [
      { text: ' ' },
      { text: `${state.blocked.length}`, color: GRAY },
    ])
    out.push(...head)
    for (const row of state.blocked) {
      const held = line(`blocked-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], { text: row.title })
      if (row.pr !== null) held.tail = [{ text: '  ' }, { text: `#${row.pr}`, color: GRAY }]
      const got = row.url !== null && Object.prototype.hasOwnProperty.call(prs, row.url) ? prs[row.url] : undefined
      const word = got?.word
      if (word !== undefined) {
        held.tail = [...(held.tail ?? []), { text: '  ' }, { text: word, color: prColor(word) }]
        const button = PR_BUTTON[word]
        if (button !== undefined) {
          held.buttons = [button]
          held.target = row.id
        }
      }
      out.push(held)
      // The counts sit in the line's text, which is cut at the pane's edge,
      // since a 44-column dock leaves no room for them in the tail (M225).
      const counts = got?.counts == null ? null : countsText(got.counts)
      if (counts !== null) out.push(line(`blocked-${row.id}-counts`, 4, [], { text: counts, color: GRAY }))
    }
  }
  // The open hotfix pull requests, after the Blocked rows and before the
  // candidates, each its number and title, and after a read its state word
  // and counts as a blocked line shows them, with no Button (M226). No
  // command resumes an open hotfix pull request, so no word routes one.
  // A hotfix pull request whose URL is a blocked row's draws on that blocked
  // line only, which carries any Button its word calls for, and the count
  // leaves it out (M230).
  const shown = hotfixes.filter(pr => !state.blocked.some(row => row.url === pr.url))
  if (shown.length > 0) {
    const head = heading('hotfixes-head', 'Hotfixes', QUEUE_COLOR, [{ text: ' ' }, { text: `${shown.length}`, color: GRAY }])
    out.push(...head)
    for (const pr of shown) {
      const held = line(`hotfix-${pr.number}`, 2, [{ text: `#${pr.number}`, bold: true }, { text: '  ' }], { text: pr.title })
      const got = Object.prototype.hasOwnProperty.call(prs, pr.url) ? prs[pr.url] : undefined
      if (got !== undefined) held.tail = [{ text: '  ' }, { text: got.word, color: prColor(got.word) }]
      out.push(held)
      const counts = got?.counts == null ? null : countsText(got.counts)
      if (counts !== null) out.push(line(`hotfix-${pr.number}-counts`, 4, [], { text: counts, color: GRAY }))
    }
  }
  // With no active milestone, the ROADMAP's candidate rows (M207).
  if (state.milestones.length === 0 && state.candidates.length > 0) {
    out.push(
      ...heading('candidates-head', 'Candidates', QUEUE_COLOR, [{ text: ' ' }, { text: `${state.candidates.length}`, color: GRAY }]),
    )
    state.candidates.forEach((row, i) =>
      out.push(
        line(
          `candidate-${i}`,
          2,
          [PRIORITY_MARK[row.priority], { text: ' ' }],
          row.priority === 'low' ? { text: row.title, color: GRAY } : { text: row.title },
        ),
      ),
    )
  }
  return out
}
