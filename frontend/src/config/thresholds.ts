/**
 * Frontend chart threshold configuration.
 *
 * These values mirror the backend monitoring thresholds used for alert detection.
 * In a larger production system, threshold configuration should ideally be served
 * by the backend/API so clients do not duplicate threshold logic.
 */
export interface MetricThresholds {
  warning: number
  critical: number
  yDomain: [number, number]
  unit: string
}

export const CHART_THRESHOLDS = {
  temperature: {
    warning: 75,
    critical: 90,
    yDomain: [40, 100],
    unit: '°C',
  },
  latency: {
    warning: 100,
    critical: 200,
    yDomain: [0, 240],
    unit: 'ms',
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
