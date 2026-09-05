import {
  CHART_THRESHOLDS,
  type ChartMetricKey,
} from '../config/thresholds'
import type { ChartPoint } from '../types'

/**
 * Build a Y-axis domain that keeps live telemetry readable while still showing
 * warning and critical reference lines.
 */
export function calculateYDomain(
  dataKey: ChartMetricKey,
  data: ChartPoint[],
): [number, number] {
  const config = CHART_THRESHOLDS[dataKey]
  const values = data.map((point) => point[dataKey])

  const dataMin = values.length > 0 ? Math.min(...values) : config.floor
  const dataMax = values.length > 0 ? Math.max(...values) : config.warning

  const minY = Math.min(
    dataMin - config.paddingBelow,
    config.floor,
  )

  const maxY = Math.max(
    dataMax + config.paddingAbove,
    config.warning + config.paddingAbove,
    config.critical + config.paddingAboveCritical,
  )

  if (dataKey === 'temperature') {
    return [Math.floor(minY), Math.ceil(maxY)]
  }

  return [Math.max(config.floor, Math.floor(minY)), Math.ceil(maxY)]
}

/** Domain used before any telemetry arrives — spans thresholds without excess range. */
export function defaultYDomain(dataKey: ChartMetricKey): [number, number] {
  return calculateYDomain(dataKey, [])
}
