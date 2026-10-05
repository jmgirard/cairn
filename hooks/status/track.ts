import type { Flow, Span } from './band'
import type { FlowPhase } from './band'
import { FLOW_COLORS, FLOW_PHASES } from './band'

// The flow track (M204, M206), the band's one progress form. On the
// desktop it is an SVG of one rounded track whose three equal segments run
// plan, implement, and review. register.tsx draws it as the desktop's `Svg`
// element, an image, so it cannot read the app's theme keys. In a
// browser-pane preview, a `prefers-color-scheme` rule inside such an image
// followed the browser's setting, not the page's (M204). The track draws
// from one palette meant for a light and a dark ground instead (M217).
//
// Back to front: the ground; a field of 2-pixel specks from the left edge
// to the head (the active phase's fill edge), sparse at the left and dense
// near the head, each gray or the active phase's color, the colored share
// growing toward the head; the item ticks; the two phase-edge marks; and
// the pill on the head, in the active phase's color, its label bold and its
// count dimmer. Item ticks fall in the active phase's segment, past the
// head, and only when the items are SPACING pixels apart or more.
// The operator picked this look at a live look over a solid dither per
// segment and two other speck designs (M204).
//
// The track is TRACK_PX wide where the row has room, and shorter where it
// does not. A track too short for the whole pill shows the pill's short
// text: its count alone, `none` for a section with no boxes, or `Planned`
// on the idle row (M206, the operator's pick from three narrow looks).
//
// In the terminal the track is a run of braille cells on the theme's
// `userMessageBackground` ground, with the same specks as dots and the pill
// as `inverseText` text on the phase's theme key (`brailleSpans`, M206, the
// operator's pick from five terminal looks, in theme keys since M217).

export const TRACK_PX = 360
export const TRACK_H = 18

const CELL = 2
const ROWS = TRACK_H / CELL
// The least spacing of item ticks, in pixels.
export const SPACING = 6
// palette
// The desktop track's colors, the only raw colors the mod draws (M217). The
// image cannot read theme keys, so the ground, the gray specks, and the
// marks are translucent grays for a light or a dark ground. The phase fills
// keep the M204 hues, darker, so the pill's white label and its count at
// COUNT_OPACITY reach the WCAG 2.2 text contrast of 4.5:1 on the fill
// whatever the app's ground (the band tests compute it).
const GROUND = 'rgba(128,128,128,0.16)'
const GRAY = 'rgb(160,160,160)'
const MARK = 'rgb(200,200,200)'
export const PHASE_FILLS: Record<FlowPhase, string> = {
  plan: 'rgb(71,103,158)',
  implement: 'rgb(152,85,57)',
  review: 'rgb(68,113,81)',
}
const PILL_LABEL = 'rgb(255,255,255)'
// palette end
const COUNT_OPACITY = 0.85
// A speck's strength, by one of three levels.
const LEVELS = [0.4, 0.65, 0.95]
const PILL_H = TRACK_H - 2
// The pill's width per character of its label and its count, and its side
// padding, an estimate for the system font at the pill's size.
const LABEL_CHAR = 6.3
const COUNT_CHAR = 5.6
const COUNT_GAP = 5
const PILL_PAD = 16

// A fixed hash of a cell, in [0, 1), so every drawing of a state is the
// same.
function hash(x: number, y: number, salt: number): number {
  let h = (x * 374761393 + y * 668265263 + salt * 2147483647) | 0
  h = Math.imul(h ^ (h >>> 13), 1274126177)
  h ^= h >>> 16
  return ((h >>> 0) % 100000) / 100000
}

// A speck's chance at a share `t` of the way from the left edge to the
// head, and its chance of the phase's color rather than gray.
const density = (t: number) => 0.22 + 0.7 * Math.pow(t, 1.4)
const colored = (t: number) => 0.95 * Math.pow(t, 2.2)

// Two decimals at most, no trailing zeros.
function n(value: number): string {
  return String(Math.round(value * 100) / 100)
}

function escape(text: string): string {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}

// The active phase's fill edge, as a share of the track from the left.
function headShare(flow: Flow): number {
  const index = FLOW_PHASES.indexOf(flow.phase)
  const fill = flow.fills[index]
  return (index + fill.num / fill.den) / 3
}

// The active phase's fill edge, in pixels from the left of a track `width`
// pixels wide.
export function headOf(flow: Flow, width = TRACK_PX): number {
  return width * headShare(flow)
}

// The x of each item tick: the active segment's inner item edges k with
// checked < k < n, none when the items are closer than SPACING. The test
// compares whole numbers, k × den > num × n, so an edge at the head never
// draws through rounding.
export function ticksOf(flow: Flow, width = TRACK_PX): number[] {
  const segment = width / 3
  const index = FLOW_PHASES.indexOf(flow.phase)
  const items = index === 0 ? 0 : flow.items[index - 1]
  const step = segment / Math.max(items, 1)
  if (items < 2 || step < SPACING) return []
  const fill = flow.fills[index]
  const out: number[] = []
  for (let k = 1; k < items; k++) {
    if (k * fill.den > fill.num * items) out.push(segment * index + step * k)
  }
  return out
}

// A pill text splits into a bold label and a dimmer count: `Implement 3/7`.
function pillParts(pill: string): [string, string] {
  const match = /^(.*) (\d+\/\d+)$/.exec(pill)
  return match === null ? [pill, ''] : [match[1], match[2]]
}

function pillWidth(pill: string): number {
  const [label, count] = pillParts(pill)
  return label.length * LABEL_CHAR + (count === '' ? 0 : count.length * COUNT_CHAR + COUNT_GAP) + PILL_PAD
}

// The pill's text on a track `width` pixels wide: the whole pill when it
// takes a third of the track or less, else its short text.
export function pillText(flow: Flow, width = TRACK_PX): string {
  return pillWidth(flow.pill) * 3 <= width ? flow.pill : flow.short
}

// The pill's left edge and width: its right edge just past the head, kept
// inside the track.
export function pillBox(flow: Flow, width = TRACK_PX): { x: number; width: number } {
  const w = pillWidth(pillText(flow, width))
  const x = Math.min(Math.max(headOf(flow, width) - w + 6, 1), width - w - 1)
  return { x, width: w }
}

// The specks, one path per color and level, in the desktop palette.
function specks(flow: Flow, width: number): string {
  const head = headOf(flow, width)
  const paths = new Map<string, string[]>()
  for (let cx = 0; cx * CELL < head; cx++) {
    const x = cx * CELL
    // The last column is cut at the head, so no speck runs past it.
    const w = n(Math.min(CELL, head - x))
    const t = x / head
    for (let cy = 0; cy < ROWS; cy++) {
      if (hash(cx, cy, 1) > density(t)) continue
      const level = Math.floor(hash(cx, cy, 2) * LEVELS.length)
      const color = hash(cx, cy, 3) < colored(t) ? flow.phase : 'gray'
      const key = `${color}:${level}`
      const cells = paths.get(key) ?? []
      cells.push(`M${x} ${cy * CELL}h${w}v${CELL}h-${w}z`)
      paths.set(key, cells)
    }
  }
  return [...paths.entries()]
    .map(([key, cells]) => {
      const [color, level] = key.split(':')
      const fill = color === 'gray' ? GRAY : PHASE_FILLS[flow.phase]
      return `<path class="specks" data-color="${color}" d="${cells.join('')}" fill="${fill}" fill-opacity="${LEVELS[Number(level)]}"/>`
    })
    .join('')
}

export function trackSvg(flow: Flow, width = TRACK_PX): string {
  const segment = width / 3
  const head = headOf(flow, width)
  const marks = [1, 2]
    .map(i => {
      const x = segment * i
      return `<rect class="edge" x="${n(x - 0.5)}" y="2" width="1" height="${TRACK_H - 4}" fill="${MARK}" fill-opacity="${x < head ? 0.7 : 0.25}"/>`
    })
    .join('')
  const ticks = ticksOf(flow, width)
    .map(x => `<rect class="tick" x="${n(x - 0.5)}" y="${TRACK_H / 2 - 3}" width="1" height="6" fill="${GRAY}" fill-opacity="0.4"/>`)
    .join('')
  const [label, count] = pillParts(pillText(flow, width))
  const pill = pillBox(flow, width)
  const countSpan = count === '' ? '' : `<tspan dx="${COUNT_GAP}" fill-opacity="${COUNT_OPACITY}" font-weight="500">${escape(count)}</tspan>`
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${n(width)}" height="${TRACK_H}" viewBox="0 0 ${n(width)} ${TRACK_H}">` +
    `<defs><clipPath id="track"><rect width="${n(width)}" height="${TRACK_H}" rx="${TRACK_H / 2}"/></clipPath></defs>` +
    `<g clip-path="url(#track)"><rect class="ground" width="${n(width)}" height="${TRACK_H}" fill="${GROUND}"/>` +
    `${specks(flow, width)}${ticks}${marks}</g>` +
    `<rect class="pill" x="${n(pill.x)}" y="1" width="${n(pill.width)}" height="${PILL_H}" rx="${PILL_H / 2}" fill="${PHASE_FILLS[flow.phase]}"/>` +
    // `textLength` holds the text to the estimated width, so a wider
    // fallback font squeezes the text rather than running past the pill.
    `<text class="pill-text" x="${n(pill.x + PILL_PAD / 2)}" y="${TRACK_H / 2}" textLength="${n(pill.width - PILL_PAD)}" lengthAdjust="spacingAndGlyphs" dominant-baseline="central" font-family="-apple-system,system-ui,sans-serif" font-size="10.5" fill="${PILL_LABEL}">` +
    `<tspan font-weight="650">${escape(label)}</tspan>${countSpan}</text>` +
    `</svg>`
  )
}

// The terminal track's ground, its blank cell, its mark at each third, and
// the pill's text color, all theme keys. The pill's text is `inverseText`
// on the phase's key (M217): white in the light themes, black in the dark.
export const BRAILLE_GROUND = 'userMessageBackground'
export const BRAILLE_BLANK = '⠀'
export const BRAILLE_MARK = '⡇'
const MARK_KEY = 'subtle'
const SPECK_KEY = 'inactive'
export const PILL_TEXT = 'inverseText'
// The eight dots of a braille cell, as bits of its code point.
const DOTS = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]

// The terminal track `cells` columns wide: the specks as braille dots, the
// pill (one space each side of its text), and a mark at each third past the
// head. The pill ends at the head's cell, or starts there when that would
// leave no speck before it. Either way it is then kept inside the track, so
// on a short track the head can fall inside the pill. The last speck
// before the pill or the head always draws in the phase's color, so a short
// track still shows its fill. A track too short for the whole pill in a
// third of it shows the short text. Runs of one style merge into one span.
export function brailleSpans(flow: Flow, cells: number): Span[] {
  const color = FLOW_COLORS[flow.phase]
  const head = Math.round(cells * headShare(flow))
  const full = ` ${flow.pill} `
  const pill = full.length * 3 <= cells ? full : ` ${flow.short} `
  const before = head - pill.length
  const start = Math.max(0, Math.min(before >= 1 ? before : head, cells - pill.length))
  const lastSpeck = Math.min(start, head) - 1
  const thirds = [Math.round(cells / 3), Math.round((2 * cells) / 3)]
  const out: Span[] = []
  const push = (text: string, style: Omit<Span, 'text'>) => {
    const last = out[out.length - 1]
    if (last !== undefined && last.color === style.color && last.backgroundColor === style.backgroundColor && last.bold === style.bold) {
      last.text += text
    } else {
      out.push({ text, ...style })
    }
  }
  for (let i = 0; i < cells; i++) {
    if (i >= start && i < start + pill.length) {
      push(pill[i - start], { color: PILL_TEXT, backgroundColor: color, bold: true })
      continue
    }
    if (i >= head) {
      const mark = thirds.includes(i)
      push(mark ? BRAILLE_MARK : BRAILLE_BLANK, { color: MARK_KEY, backgroundColor: BRAILLE_GROUND })
      continue
    }
    const t = i / head
    let bits = 0
    DOTS.forEach((bit, k) => {
      if (hash(i, k, 1) < density(t)) bits |= bit
    })
    const last = i === lastSpeck
    const hue = last || hash(i, 0, 3) < colored(t) ? color : SPECK_KEY
    if (last && bits === 0) bits = 0xff
    push(String.fromCharCode(0x2800 + bits), { color: hue, backgroundColor: BRAILLE_GROUND })
  }
  return out
}
