import type { Flow } from './band'
import { FLOW_COLORS, FLOW_PHASES } from './band'

// The desktop track (M204): an SVG of one rounded track whose three equal
// segments run plan, implement, and review. register.tsx draws it as the
// desktop's `Svg` element, an image, so it cannot read the theme's keys:
// the ground and the marks take a light and a dark palette by
// `prefers-color-scheme` instead.
//
// Back to front: the ground, the item ticks, each segment's fill in a
// dither of its phase's color, the two phase-edge marks, and the pill on
// the active phase's fill edge. Item ticks are n−1 marks inside a segment
// of n items. A segment whose fill is 0 draws no fill; the running plan
// draws a dashed outline instead.

export const TRACK_PX = 224
export const TRACK_H = 18

const SEGMENT = TRACK_PX / 3
const PILL_H = 14
// The pill's width per character and its side padding, an estimate for the
// system font at the pill's size.
const PILL_CHAR = 6.2
const PILL_PAD = 14
const PILL_TEXT = '#1f1e1c'

const STYLE =
  '.ground{fill:#e6e3dc}.tick{stroke:#000;stroke-opacity:.22}.edge{stroke:#000;stroke-opacity:.45}' +
  '@media (prefers-color-scheme: dark){.ground{fill:#2b2a27}.tick{stroke:#fff;stroke-opacity:.25}.edge{stroke:#fff;stroke-opacity:.5}}' +
  '.pill-text{font:600 10.5px -apple-system,system-ui,sans-serif}'

// Two decimals at most, no trailing zeros.
function n(value: number): string {
  return String(Math.round(value * 100) / 100)
}

function escape(text: string): string {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}

// The dither tile: BLOCKS_X by BLOCKS_Y blocks of BLOCK pixels. Each block
// draws the color at one of LEVELS strengths, or a faint light block, in a
// fixed order from a small seeded generator, so a fill reads as pixel noise
// and every drawing of it is the same.
const BLOCK = 2
const BLOCKS_X = 12
const BLOCKS_Y = 9
const LEVELS = [0.45, 0.65, 0.85, 1]

function noise(): number[] {
  let seed = 204
  const out: number[] = []
  for (let i = 0; i < BLOCKS_X * BLOCKS_Y; i++) {
    seed = (seed * 1103515245 + 12345) % 2147483648
    out.push(Math.floor((seed / 2147483648) * 10))
  }
  return out
}
const NOISE = noise()

function dither(phase: string, color: string): string {
  const width = BLOCKS_X * BLOCK
  const height = BLOCKS_Y * BLOCK
  const blocks = NOISE.map((value, i) => {
    const x = (i % BLOCKS_X) * BLOCK
    const y = Math.floor(i / BLOCKS_X) * BLOCK
    // Values 0 to 7 pick a strength of the color; 8 and 9 a light block.
    const paint = value < 8 ? `fill="${color}" fill-opacity="${LEVELS[value % 4]}"` : 'fill="#fff" fill-opacity="0.2"'
    return `<rect x="${x}" y="${y}" width="${BLOCK}" height="${BLOCK}" ${paint}/>`
  })
  return (
    `<pattern id="dither-${phase}" width="${width}" height="${height}" patternUnits="userSpaceOnUse">` +
    `<rect width="${width}" height="${height}" fill="${color}" fill-opacity="0.5"/>` +
    blocks.join('') +
    `</pattern>`
  )
}

// The pill's left edge and width: centered on the active phase's fill edge,
// kept inside the track.
export function pillBox(flow: Flow): { x: number; width: number } {
  const width = flow.pill.length * PILL_CHAR + PILL_PAD
  const index = FLOW_PHASES.indexOf(flow.phase)
  const fill = flow.fills[index]
  const head = SEGMENT * index + (SEGMENT * fill.num) / fill.den
  const x = Math.min(Math.max(head - width / 2, 1), TRACK_PX - width - 1)
  return { x, width }
}

export function trackSvg(flow: Flow): string {
  const parts: string[] = []
  parts.push(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${TRACK_PX}" height="${TRACK_H}" viewBox="0 0 ${TRACK_PX} ${TRACK_H}">`,
  )
  parts.push(`<style>${STYLE}</style>`)
  parts.push('<defs>')
  for (const phase of FLOW_PHASES) parts.push(dither(phase, FLOW_COLORS[phase]))
  parts.push(
    `<clipPath id="track"><rect width="${TRACK_PX}" height="${TRACK_H}" rx="${TRACK_H / 2}"/></clipPath>`,
  )
  parts.push('</defs>')
  parts.push('<g clip-path="url(#track)">')
  parts.push(`<rect class="ground" width="${TRACK_PX}" height="${TRACK_H}"/>`)

  // Item ticks in the implement and review segments.
  flow.items.forEach((items, i) => {
    const left = SEGMENT * (i + 1)
    for (let k = 1; k < items; k++) {
      const x = n(left + (SEGMENT * k) / items)
      parts.push(`<line class="tick" data-phase="${FLOW_PHASES[i + 1]}" x1="${x}" x2="${x}" y1="5" y2="${TRACK_H - 5}"/>`)
    }
  })

  flow.fills.forEach((fill, i) => {
    if (fill.num === 0) return
    const phase = FLOW_PHASES[i]
    const width = n((SEGMENT * fill.num) / fill.den)
    parts.push(
      `<rect class="fill" data-phase="${phase}" x="${n(SEGMENT * i)}" y="0" width="${width}" height="${TRACK_H}" fill="url(#dither-${phase})"/>`,
    )
  })

  if (flow.running) {
    parts.push(
      `<rect class="running" data-phase="plan" x="1" y="1" width="${n(SEGMENT - 2)}" height="${TRACK_H - 2}" rx="${(TRACK_H - 2) / 2}" fill="none" stroke="${FLOW_COLORS.plan}" stroke-dasharray="3 2"/>`,
    )
  }

  for (const i of [1, 2]) {
    const x = n(SEGMENT * i)
    parts.push(`<line class="edge" x1="${x}" x2="${x}" y1="2" y2="${TRACK_H - 2}"/>`)
  }
  parts.push('</g>')

  const pill = pillBox(flow)
  const top = (TRACK_H - PILL_H) / 2
  parts.push(
    `<rect class="pill" x="${n(pill.x)}" y="${top}" width="${n(pill.width)}" height="${PILL_H}" rx="${PILL_H / 2}" fill="${FLOW_COLORS[flow.phase]}"/>`,
  )
  parts.push(
    `<text class="pill-text" x="${n(pill.x + pill.width / 2)}" y="${TRACK_H / 2}" text-anchor="middle" dominant-baseline="central" fill="${PILL_TEXT}">${escape(flow.pill)}</text>`,
  )
  parts.push('</svg>')
  return parts.join('')
}
