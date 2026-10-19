import type { CairnHotfixPr, CairnPrRead, CairnPrWord, CairnRepoRead, CairnStartedRow } from '../../types'
import type { PrCounts } from './counts'
import type { Span } from './band'
import type { FlowPhase } from './band'
import type { BadgeName } from './badge'
import { badgeSpan } from './badge'
import type { IconName } from './icons'
import { FLOW_COLORS, flowOf, GRAY } from './band'
import type { BandRow, CandidateRow, NextStep, PaneItem, PaneMilestone, PaneState, TakenRow } from './reader'

// The cairn pane's lines (M205), as a plain description that register.tsx
// draws. First, the summary card (M286): the base remote repo's open pull
// requests and issues, the drawn candidate rows at each level, and the
// planned, blocked, and done milestones. For each active milestone: its id
// in its phase's color (no phase word since M236), and its title, with the
// band's percent for the row at the end of the line when its file reads
// (M208), its goal, and its tasks and criteria with their boxes. Its
// newest work-log lines drew too until the M286 live look.
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
// The operator picked the look at the M286 prototypes (look B), in place
// of the M208 look: the card in a round border, each section heading a bold
// label, with any count at the right end, a six-cell meter beside the Tasks
// and Criteria counts, the head line's title bold, the Next command after
// an arrow with no pill, and one layout for blocked and hotfix lines. At the
// live look the operator asked for the app's task-list marks, which the
// desktop draws as icons of one size (icons.ts), and dropped look B's rule
// after each heading. A milestone's meters take its phase's color, and the
// Next line takes the color of the phase its command runs. The colors are
// theme keys (M217). The `card` lines draw in the card's Box. Since M289
// the Blocked, Hotfixes, and Candidates headings draw their count as a
// badge in the heading's color (badge.ts).
// While no cairn skill runs, the Next line also carries the band's
// next-step label after the command, which register.tsx draws as a Button
// (M218). After that Button the line carries Status, which register.tsx
// draws as a Button (M219). Until M241 it also carried Clear after a cairn
// skill's end, and the first line's ⌂ took its place.

// The Next line's `action`, when set, is the label of the next-step Button
// drawn after its tail. No other line carries one: register.tsx draws it
// with the one key `cairn-pane-next` and the next-step press.
// A line's `buttons` name the Buttons that register.tsx draws after its
// tail and any action Button, in order: Status on the Next line (M219),
// and one of Finish, Revise, or Check on a blocked line (M224). A
// blocked line's `target` is its milestone id, which its Button's key and
// press carry. Since M236 the pane's first line, the card's first since
// M286, carries the one Refresh
// Button, labeled ↻, which reads everything again. Its `grow` makes its
// text take the free room, so its tail and the Button sit at the right end
// of the row. Until M236 the Blocked and Hotfixes headings each carried a
// Refresh. While no cairn skill runs, the Home Button, labeled ⌂, comes
// before ↻: it clears the conversation and opens the pane again (M241).
// While no cairn skill runs, each candidate line whose short title is not
// empty carries the Plan Button, labeled ✎, which plans that row (M242).
// Its `target` is the line's index among the candidate rows, which the
// Button's key carries, so two rows with one title draw two keys, and its
// `title` is the row's short title, which the press carries. A candidate
// line's `grow` puts ✎ at the right end of the row, and a blocked or
// hotfix line with a tail grows so its tail sits there too.
// A line's `full`, set on each head, task, criterion, workable, waiting,
// blocked, hotfix, and candidate line, is its whole text, which the desktop
// shows in a card while the pointer is over the line (M286).
export type PaneButton = 'home' | 'status' | 'refresh' | 'finish' | 'revise' | 'check' | 'plan'
export type PaneLine = {
  key: string
  indent: number
  lead: Span[]
  text: Span | null
  tail?: Span[]
  wraps?: true
  card?: true
  full?: string
  action?: string
  buttons?: PaneButton[]
  target?: string
  title?: string
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

// One `Candidate row: <short title>` line of an open pull request's body,
// with that pull request's number (M252). `/hotfix` and `/milestone-review`
// write one such line per candidate row their merge removes or narrows.
export type StartedRow = CairnStartedRow

// The prefix a body line opens with to name a candidate row (M252).
export const STARTED_PREFIX = 'Candidate row: '

// A body line that opens or closes a fenced code block: three backticks
// or three tildes after optional spaces (M257).
const FENCE_LINE = /^ *(```|~~~)/

// The started items of one `gh pr list --json
// number,title,url,headRefName,body` result, in the order it lists them,
// or null for a call that rejected, exited non-zero, or printed something
// other than a JSON array, as `hotfixPrs` reads it (M252). Every entry with
// an integer `number` and a string `body` counts, whatever its head
// branch. Each body line, split on `\n` with a trailing `\r` removed, that
// opens with exactly `Candidate row: ` gives one item, its title the rest
// trimmed as `candidateRows` trims a title. A blank rest gives none. A
// line between a fence line and the next fence line gives none (M257):
// any fence line closes an open fence, and each body starts with no fence
// open.
export function startedRows(result: { exitCode: number; stdout: string } | null): StartedRow[] | null {
  if (result === null || result.exitCode !== 0) return null
  let list: unknown
  try {
    list = JSON.parse(result.stdout)
  } catch {
    return null
  }
  if (!Array.isArray(list)) return null
  const out: StartedRow[] = []
  for (const entry of list) {
    if (entry === null || typeof entry !== 'object') continue
    const { number, body } = entry as Record<string, unknown>
    if (typeof body !== 'string' || typeof number !== 'number' || !Number.isInteger(number)) continue
    let fenced = false
    for (const raw of body.split('\n')) {
      const line = raw.endsWith('\r') ? raw.slice(0, -1) : raw
      if (FENCE_LINE.test(line)) {
        fenced = !fenced
        continue
      }
      if (fenced || !line.startsWith(STARTED_PREFIX)) continue
      const title = line.slice(STARTED_PREFIX.length).trim()
      if (title !== '') out.push({ title, number })
    }
  }
  return out
}

// What marks the candidate row with this short title as started (M258):
// `numbers` the pull requests whose bodies name it and the `#<n>` tokens
// whose n the open hotfix list holds, in no order, and `ids` its
// `M<NNN>` tokens (the reader keeps only those whose milestone is
// `planned` or `blocked`), lowest first. A row with an empty short title
// has none.
export function startedRefs(
  title: string,
  taken: TakenRow[],
  hotfixes: HotfixPr[],
  started: StartedRow[],
): { numbers: number[]; ids: string[] } {
  if (title === '') return { numbers: [], ids: [] }
  const mine = taken.filter(item => item.title === title)
  const numbers = [
    ...started.filter(item => item.title === title).map(item => item.number),
    ...mine
      .filter(item => item.ref.startsWith('#'))
      .map(item => Number(item.ref.slice(1)))
      .filter(number => hotfixes.some(pr => pr.number === number)),
  ]
  const ids = mine
    .filter(item => item.ref.startsWith('M'))
    .map(item => item.ref)
    .sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)))
  return { numbers, ids }
}

// The candidate row's short title that the next step names while planning
// (M272, M273): the first `[high]` row with a short title that the
// Candidates list draws, under the list's own test (`startedRefs` over the
// counted tokens, the open hotfix list, and the PR bodies that name a row),
// so the Next line, the pane's Plan press, and the band's Plan press never
// name a hidden row or pass over a drawn one. Null outside planning, or
// when the list draws no such row. The reader's `next.title` counts every
// `#` token and reads no PR body, as scripts/cairn_next.py does.
export function nextTitle(
  next: NextStep,
  candidates: CandidateRow[],
  taken: TakenRow[],
  hotfixes: HotfixPr[],
  started: StartedRow[],
): string | null {
  if (next.id !== null || next.command !== '/milestone-plan') return null
  const row = candidates.find(row => {
    if (row.priority !== 'high' || row.title === '') return false
    const { numbers, ids } = startedRefs(row.title, taken, hotfixes, started)
    return numbers.length === 0 && ids.length === 0
  })
  return row?.title ?? null
}

// The Button a blocked line carries for its state word (M224), from the
// routes that /milestone gives a handed-off PR: a merged one goes to
// review's hygiene, one with changes requested back to implement, and a
// closed one to /milestone. The other words carry none. An archived row
// keeps only Finish (M246), since its milestone file is gone.
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

// The Status and Clear Buttons' labels (M212, M216). The band reads both,
// and the pane's Next line reads Status (M219, M241).
export const STATUS_LABEL = 'Status'
export const CLEAR_LABEL = 'Clear'
// The pane's Refresh Button (M224, one ↻ on the first line since M236),
// its label while a read of the pull request states runs (M236), and a
// blocked line's Buttons (M224).
export const REFRESH_LABEL = '↻'
// The pane's Home Button, before ↻ on the first line (M241).
export const HOME_LABEL = '⌂'
// A candidate line's Plan Button (M242).
export const PLAN_CANDIDATE_LABEL = '✎'
export const READING_LABEL = '⋯'
export const FINISH_LABEL = 'Finish'
export const REVISE_LABEL = 'Revise'
export const CHECK_LABEL = 'Check'

export const NO_ROADMAP = 'no cairn ROADMAP found'
export const NO_FILE = 'no milestone file'
export const NO_ACTIVE = 'no active milestone'
// A task or criterion's marks (M286), as the desktop app's own task list
// draws them, at the operator's direction after the pick: a checked box is
// a filled circle with a check, an open one a dashed circle, and the first
// open task of an `in-progress` milestone, the one being worked, a circle
// with three dots. Each names its icon (icons.ts), which the desktop draws
// in place of the glyph, so every mark is one size there; the terminal
// draws the glyph.
export const CHECKED_MARK = '●'
export const ITEM_OPEN_MARK = '◌'
export const CURRENT_MARK = '⊙'
// The empty circle a normal candidate row draws (M253), which a blocked or
// hotfix line also draws before a read (M286).
export const OPEN_MARK = '○'
// A candidate row's mark for each priority (M207). A normal row's mark is
// the empty circle `OPEN_MARK` (M253). Each names its icon (M286).
export const PRIORITY_MARK: Record<CandidateRow['priority'], Span> = {
  high: { text: '↑', color: FLOW_COLORS.implement, bold: true, icon: 'high' },
  normal: { text: OPEN_MARK, icon: 'ring' },
  low: { text: '↓', color: GRAY, icon: 'low' },
  // A parked row waits on a promotion condition that has not held (M284).
  parked: { text: '⧗', color: GRAY, icon: 'parked' },
}
// The order the Candidates list draws each priority in (M280), the parked
// rows last (M284).
const LEVEL_RANK: Record<CandidateRow['priority'], number> = { high: 0, normal: 1, low: 2, parked: 3 }
// The meter's cells, filled and empty, and how many it draws (M208, look B
// in M286).
export const METER_FULL = '━'
export const METER_EMPTY = '─'
export const METER_CELLS = 6
// The empty cells' theme key, as the band's terminal track marks use (M208 review).
export const METER_EMPTY_KEY = 'subtle'
// The room after an item's mark: two spaces, for the operator's ask for
// more space after the pick (M286).
export const ITEM_GAP = '  '
// The warning text's theme key, as the band's warning labels use.
const WARNING = 'warning'
// The Next line's mark before its command (M286).
export const NEXT_MARK = '→ '
// The identifier a hotfix line draws where a blocked line draws its
// milestone id (M286).
export const HOTFIX_ID = 'fix'
// A pull request line's state mark for each word, in the word's color, and
// for a line with no read yet, each with its icon (M286).
export const PR_MARK: Record<PrWord, { text: string; icon: IconName }> = {
  merged: { text: '●', icon: 'merged' },
  approved: { text: '●', icon: 'merged' },
  'changes requested': { text: '▲', icon: 'attention' },
  'in review': { text: '◐', icon: 'review' },
  closed: { text: '✕', icon: 'closed' },
  unknown: { text: '◌', icon: 'open' },
}
export const UNREAD_MARK = { text: OPEN_MARK, icon: 'ring' as IconName }
// The card's line keys (M286), and the text a number draws as before a read
// gives it.
export const CARD_KEYS = {
  repo: 'card-repo',
  candidates: 'card-candidates',
  milestones: 'card-milestones',
  release: 'card-release',
} as const
export const UNKNOWN_NUMBER = '?'

// A milestone's id draws in its phase's color, with no phase word, which
// the operator dropped at the M236 live look.
const PHASE_COLOR: Record<string, string> = {
  'in-progress': FLOW_COLORS.implement,
  review: FLOW_COLORS.review,
}
// The phase each recommended command runs, for the Next line's color.
export const COMMAND_PHASE: Record<string, FlowPhase> = {
  '/milestone-plan': 'plan',
  '/milestone-implement': 'implement',
  '/milestone-review': 'review',
}

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

// A section heading and the blank row before it (M286): the label in bold,
// and an empty text that grows, so the heading's tail, where it has one,
// sits at the right end after a space. Look B's rule after the label was
// dropped at the live look, where the desktop drew it as two lines.
function heading(key: string, label: string, tail: Span[] = []): PaneLine[] {
  const head: PaneLine = { ...line(key, 0, [{ text: label, bold: true }], { text: '' }), grow: true }
  if (tail.length > 0) head.tail = [{ text: ' ' }, ...tail]
  return [gap(`${key}-gap`), head]
}

// A heading whose tail is its count as a badge in the heading's color
// (M289, badge.ts), where M286 drew a gray number.
function countHeading(key: string, label: string, count: number, name: BadgeName): PaneLine[] {
  return heading(key, label, [badgeSpan(count, name)])
}

// A heading whose tail is the checked and total counts and the meter in
// the phase's color.
function counted(key: string, label: string, list: PaneItem[], color: string): PaneLine[] {
  const checked = list.filter(item => item.checked).length
  return heading(key, label, [{ text: `${checked}/${list.length} `, color: GRAY }, ...meter(checked, list.length, color)])
}

// The item lines. `current` is the index of the item that draws
// `CURRENT_MARK`, or -1 for none.
function items(prefix: string, list: PaneItem[], current = -1): PaneLine[] {
  return list.map((item, i) => {
    const mark: Span = item.checked
      ? { text: CHECKED_MARK, color: GRAY, icon: 'done' }
      : i === current
        ? { text: CURRENT_MARK, icon: 'current' }
        : { text: ITEM_OPEN_MARK, color: GRAY, icon: 'open' }
    return {
      ...line(`${prefix}-${i}`, 2, [mark, { text: ITEM_GAP }], item.checked ? { text: item.text, color: GRAY } : { text: item.text }),
      full: item.text,
    }
  })
}

// A list item's opening marker: `- `, `* `, or digits and `. ` (M286).
const LIST_MARK = /^([-*] |\d+\. )/

// The goal's paragraphs and list items, each one string, so the pane wraps
// them at its own width and not at the file's line breaks (M286). Each line
// is trimmed. A line joins the one above it with one space, unless a blank
// line comes between them or its trimmed text opens with a list marker. One
// or more blank lines give one empty string between blocks.
export function goalBlocks(goal: string): string[] {
  const out: string[] = []
  let open = false
  let blank = false
  for (const raw of goal.split('\n')) {
    const text = raw.trim()
    if (text === '') {
      if (out.length > 0) blank = true
      open = false
      continue
    }
    if (blank) {
      out.push('')
      blank = false
    }
    if (open && !LIST_MARK.test(text)) {
      out[out.length - 1] = `${out[out.length - 1]} ${text}`
    } else {
      out.push(text)
      open = true
    }
  }
  return out
}

function milestoneLines(row: PaneMilestone, band: BandRow | undefined): PaneLine[] {
  const phase = { color: PHASE_COLOR[row.status] ?? GRAY }
  // The id bold in the phase's color and the title bold (M286, look B).
  const head = line(`${row.id}-head`, 0, [{ text: row.id, color: phase.color, bold: true }, { text: '  ' }], {
    text: row.title,
    bold: true,
  })
  head.full = row.title
  const file = row.file
  // The band's percent for the row, from its own counts, which count a box
  // inside an HTML comment where the pane's items do not.
  const flow = file === null || band === undefined ? null : flowOf(band)
  if (flow !== null && flow.percent !== null) head.tail = [{ text: '  ' }, { text: `${flow.percent}%`, color: GRAY }]
  const out: PaneLine[] = [head]
  if (file === null) return [...out, line(`${row.id}-nofile`, 2, [], { text: NO_FILE, color: WARNING })]
  if (file.goal !== '') {
    out.push(...heading(`${row.id}-goal-head`, 'Goal'))
    // One wrapping line per paragraph or list item (M286). The blank row
    // between paragraphs draws as one space, so it keeps its row.
    goalBlocks(file.goal).forEach((text, i) =>
      out.push({ ...line(`${row.id}-goal-${i}`, 2, [], { text: text === '' ? ' ' : text }), wraps: true }),
    )
  }
  if (file.tasks.length > 0) {
    out.push(...counted(`${row.id}-tasks-head`, 'Tasks', file.tasks, phase.color))
    // While the milestone is `in-progress`, its first open task is the one
    // being worked (M286).
    const current = row.status === 'in-progress' ? file.tasks.findIndex(item => !item.checked) : -1
    out.push(...items(`${row.id}-task`, file.tasks, current))
  }
  if (file.criteria.length > 0) {
    out.push(...counted(`${row.id}-criteria-head`, 'Criteria', file.criteria, phase.color))
    out.push(...items(`${row.id}-criterion`, file.criteria))
  }
  // The work log draws no section since the M286 live look, where the
  // operator found its one-row lines added little; the file holds it.
  return out
}

// The candidate rows that the Candidates list draws, each with its index in
// `state.candidates`, high rows first, then normal, low, and parked (M280,
// M284), each level in ROADMAP order. A row that `startedRefs` marks is left
// out (M261). The card counts the same rows, so the list and the card share
// this one filter (M286).
export function drawnCandidates(
  state: PaneState,
  hotfixes: HotfixPr[],
  started: StartedRow[],
): { row: CandidateRow; i: number }[] {
  return state.candidates
    .map((row, i) => ({ row, i }))
    .filter(({ row }) => {
      const { numbers, ids } = startedRefs(row.title, state.taken, hotfixes, started)
      return numbers.length === 0 && ids.length === 0
    })
    .sort((a, b) => LEVEL_RANK[a.row.priority] - LEVEL_RANK[b.row.priority] || a.i - b.i)
}

// The summary card's lines (M286, look B), which register.tsx draws in one
// Box with a round border. The first holds the base remote repo's open pull
// requests and open issues, each `?` while the store holds no numbers for
// this root. The second holds the drawn candidate rows at each level, each
// after its level's mark. The third holds the planned and blocked
// milestones. A fourth, the release line, holds the latest release tag, the
// days since its commit, and the milestones done since it, when the last
// read could read them.
export function cardLines(
  state: PaneState,
  drawn: { row: CandidateRow }[],
  repo: CairnRepoRead | null,
): PaneLine[] {
  const counts = repo?.counts ?? null
  const number = (n: number | undefined) => ({ text: n === undefined ? UNKNOWN_NUMBER : `${n}`, bold: true })
  const first: PaneLine = {
    ...line(CARD_KEYS.repo, 0, [
      number(counts?.prs),
      { text: ' PRs', color: GRAY },
      { text: '   ' },
      number(counts?.issues),
      { text: ' issues', color: GRAY },
    ]),
    // An empty text takes the free room, so the Buttons sit at the right end.
    text: { text: '' },
  }
  const levels: CandidateRow['priority'][] = ['high', 'normal', 'low', 'parked']
  const second = line(CARD_KEYS.candidates, 0, [
    { text: 'candidates', color: GRAY },
    ...levels.flatMap((level, i) => [
      { text: i === 0 ? ' ' : '   ' },
      PRIORITY_MARK[level],
      { text: ` ${drawn.filter(({ row }) => row.priority === level).length}` },
    ]),
  ])
  const planned = state.workable.length + state.waiting.length
  const third = line(CARD_KEYS.milestones, 0, [], { text: `${planned} planned · ${state.blocked.length} blocked`, color: GRAY })
  // The release line, while the last read written for this root could read
  // the latest release tag, the days since its commit, and the milestones
  // archived since it (M286).
  const done = repo?.done ?? null
  const release =
    done === null
      ? []
      : [
          line(CARD_KEYS.release, 0, [], {
            text: `${done.tag} · ${done.days === 1 ? '1 day' : `${done.days} days`} ago · ${done.count} done since`,
            color: GRAY,
          }),
        ]
  return [first, second, third, ...release].map(card => ({ ...card, card: true }))
}

// A blocked milestone's line or a hotfix pull request's line, in one layout
// (M286): the state mark in its word's color, the identifier bold, the
// title, and a tail that holds the pull request's number in gray, the
// archived mark for a blocked row whose file was archived (M246), and the
// state word in its color. Before a read the mark is `○` in gray and the
// tail holds no word. A blocked row with no pull request has no number. A
// line with a tail grows, so the tail sits at the right end whether or not
// the title is cut.
function prLine(key: string, id: string, title: string, number: number | null, archived: boolean, got: PrRead | undefined): PaneLine {
  const word = got?.word
  const mark: Span = word === undefined ? { ...UNREAD_MARK, color: GRAY } : { ...PR_MARK[word], color: prColor(word) }
  const held: PaneLine = { ...line(key, 2, [mark, { text: ' ' }, { text: id, bold: true }, { text: '  ' }], { text: title }), full: title }
  const tail: Span[] = []
  if (number !== null) tail.push({ text: ' ' }, { text: `#${number}`, color: GRAY })
  if (archived) tail.push({ text: ' ' }, { text: 'archived', color: GRAY })
  if (word !== undefined) tail.push({ text: ' ' }, { text: word, color: prColor(word) })
  if (tail.length > 0) {
    held.tail = [{ text: ' ' }, ...tail]
    held.grow = true
  }
  return held
}

// The line under a pull request's line with its unresolved threads, or null
// when it has no count. The counts sit in the line's text, which is cut at
// the pane's edge, since a 44-column dock leaves no room for them in the
// tail (M225).
function countsLine(key: string, got: PrRead | undefined): PaneLine | null {
  const counts = got?.counts == null ? null : countsText(got.counts)
  return counts === null ? null : line(key, 4, [], { text: counts, color: GRAY })
}

// The pane's lines from its state and the band's rows, whose counts give
// each head line its percent. `acts` is true while no cairn skill's step is
// set, and then the Next line carries its action label (M218) and the
// Status Button after it (M219), the first line carries ⌂ (M241), and each
// candidate line with a short title carries ✎ (M242).
// `prs` holds each pull request's state word by its
// URL, from the last read (M224), with its counts (M225). `hotfixes` holds
// the open hotfix pull requests of the last read for this root (M226), and
// `started` the candidate rows that open pull requests' bodies name (M252).
export function paneLines(
  state: PaneState,
  band: BandRow[] = [],
  acts = false,
  prs: Record<string, PrRead> = {},
  hotfixes: HotfixPr[] = [],
  started: StartedRow[] = [],
  repo: CairnRepoRead | null = null,
): PaneLine[] {
  if (!state.found) return [line('no-roadmap', 0, [], { text: NO_ROADMAP, color: GRAY })]
  // The candidate rows the Candidates list draws, whether or not a
  // milestone is active, which the card counts too (M286).
  const drawable = drawnCandidates(state, hotfixes, started)
  const out: PaneLine[] = cardLines(state, drawable, repo)
  // The card's first line carries the ↻ Button at its right end (M236, on
  // the card since M286), and ⌂ before it while no cairn skill's step is
  // set (M241).
  out[0].buttons = acts ? ['home', 'refresh'] : ['refresh']
  out[0].grow = true
  // A blank row under the card, for the operator's ask for more space.
  out.push(gap('card-gap'))
  if (state.milestones.length === 0) out.push(line('no-active', 0, [], { text: NO_ACTIVE, color: GRAY }))
  state.milestones.forEach((row, i) => {
    if (i > 0) out.push(gap(`${row.id}-gap`))
    out.push(...milestoneLines(row, band.find(b => b.id === row.id && b.status === row.status)))
  })
  if (state.next !== null) {
    // Planning names its `[high]` row's short title after the command (M272).
    const named = state.next.id ?? nextTitle(state.next, state.candidates, state.taken, hotfixes, started)
    const target = named === null ? state.next.command : `${state.next.command} ${named}`
    out.push(gap('next-gap'))
    // The arrow and the command, bold in the color of the phase the command
    // runs, with no pill (M286, look B).
    const color = FLOW_COLORS[COMMAND_PHASE[state.next.command] ?? 'implement']
    const next = line('next', 0, [{ text: NEXT_MARK, color, bold: true }], { text: target, color, bold: true })
    const label = nextLabel(state.next.action)
    // Status follows the next-step Button and shows only with it, as the
    // band's shows only with a next-step label (M219 review).
    if (acts && label !== undefined) {
      next.action = label
      next.buttons = ['status']
    }
    out.push(next)
  }
  if (state.workable.length > 0) {
    out.push(...heading('workable-head', 'Workable'))
    for (const row of state.workable) {
      out.push({ ...line(`workable-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], { text: row.title }), full: row.title })
    }
  }
  if (state.waiting.length > 0) {
    out.push(...heading('waiting-head', 'Waiting'))
    for (const row of state.waiting) {
      const text = `${row.title} · on ${row.unmet.join(', ')}`
      out.push({ ...line(`waiting-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], { text }), full: text })
    }
  }
  // The blocked rows, each with its pull request's number when its
  // milestone file's header names one, whether or not a milestone is
  // active (M223). After the number, the state word that the last read
  // found, and the Button that word carries (M224).
  if (state.blocked.length > 0) {
    out.push(...countHeading('blocked-head', 'Blocked', state.blocked.length, 'blocked'))
    for (const row of state.blocked) {
      const got = row.url !== null && Object.prototype.hasOwnProperty.call(prs, row.url) ? prs[row.url] : undefined
      const held = prLine(`blocked-${row.id}`, row.id, row.title, row.pr, row.archived, got)
      const word = got?.word
      if (word !== undefined) {
        // An archived row carries only Finish (M246 review): its milestone
        // file is gone, so Revise and Check have nothing to work on.
        const mapped = PR_BUTTON[word]
        const button = row.archived && mapped !== 'finish' ? undefined : mapped
        if (button !== undefined) {
          held.buttons = [button]
          held.target = row.id
        }
      }
      out.push(held)
      const counts = countsLine(`blocked-${row.id}-counts`, got)
      if (counts !== null) out.push(counts)
    }
  }
  // The open hotfix pull requests, after the Blocked rows and before the
  // candidates, each its number and title, and after a read its state word
  // and counts as a blocked line shows them, with no Button (M226).
  // A hotfix pull request whose URL is a blocked row's draws on that blocked
  // line only, which carries any Button its word calls for, and the count
  // leaves it out (M230).
  const shown = hotfixes.filter(pr => !state.blocked.some(row => row.url === pr.url))
  if (shown.length > 0) {
    out.push(...countHeading('hotfixes-head', 'Hotfixes', shown.length, 'hotfixes'))
    for (const pr of shown) {
      const got = Object.prototype.hasOwnProperty.call(prs, pr.url) ? prs[pr.url] : undefined
      out.push(prLine(`hotfix-${pr.number}`, HOTFIX_ID, pr.title, pr.number, false, got))
      const counts = countsLine(`hotfix-${pr.number}-counts`, got)
      if (counts !== null) out.push(counts)
    }
  }
  // With no active milestone, the ROADMAP's candidate rows (M207), each
  // with ✎ while no cairn skill runs, but for a row with an empty short
  // title, whose press would plan with no args (M242). A row that work has
  // started draws no line (M261): one whose short title an open pull
  // request's body names exactly (M252), or that a counted started token
  // marks (M258). The heading counts the drawn rows, and with none it is
  // not drawn. The lines draw high rows first, then normal, then low, then
  // parked (M284), each level in ROADMAP order, whatever order the file
  // holds them in (M280).
  // `state.candidates` stays in ROADMAP order. A drawn line keeps its row's
  // index there as its key and its ✎ target, and `pressCandidate` looks the
  // row up by that index.
  const drawn = state.milestones.length === 0 ? drawable : []
  if (drawn.length > 0) {
    out.push(...countHeading('candidates-head', 'Candidates', drawn.length, 'candidates'))
    for (const { row, i } of drawn) {
      const candidate = line(
        `candidate-${i}`,
        2,
        [PRIORITY_MARK[row.priority], { text: ' ' }],
        row.priority === 'low' || row.priority === 'parked' ? { text: row.title, color: GRAY } : { text: row.title },
      )
      candidate.grow = true
      candidate.full = row.title
      if (acts && row.title !== '') {
        candidate.buttons = ['plan']
        candidate.target = `${i}`
        candidate.title = row.title
      }
      out.push(candidate)
    }
  }
  // A line whose text is empty has no hover card (M286).
  for (const each of out) if (each.full === '') delete each.full
  return out
}
