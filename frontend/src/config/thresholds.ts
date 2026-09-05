/**
 * Frontend chart threshold configuration.
 *
 * These values mirror backend monitoring thresholds (see app/monitoring/thresholds.py)
 * and are used only for chart reference lines and Y-axis scaling — not alert logic.
 * In production, threshold configuration should ideally be served by the backend/API
 * so clients do not duplicate threshold values.
 */
export interface MetricThresholds {
  warning: number
  critical: number
  unit: string
  /** Lowest sensible Y value when telemetry is healthy. */
  floor: number
  paddingBelow: number
  paddingAbove: number
  /** Extra headroom above the critical line so its label is not clipped. */
  paddingAboveCritical: number
}

export const CHART_THRESHOLDS = {
  temperature: {
    warning: 75,
    critical: 90,
    unit: '°C',
    floor: 45,
    paddingBelow: 6,
    paddingAbove: 6,
    paddingAboveCritical: 5,
  },
  latency: {
    warning: 100,
    critical: 200,
    unit: 'ms',
    floor: 0,
    paddingBelow: 8,
    paddingAbove: 10,
    paddingAboveCritical: 15,
  },
} as const satisfies Record<string, MetricThresholds>

export type ChartMetricKey = keyof typeof CHART_THRESHOLDS

export const THRESHOLD_LINE_STYLES = {
  warning: {
    stroke: '#fbbf24',
    labelFill: '#fbbf24',
  },
  critical: {
    stroke: '#f87171',
    labelFill: '#f87171',
  },
} as const
