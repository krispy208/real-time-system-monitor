import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import {
  CHART_THRESHOLDS,
  THRESHOLD_LINE_STYLES,
  type ChartMetricKey,
} from '../config/thresholds'
import type { ChartPoint } from '../types'

interface MetricChartProps {
  title: string
  data: ChartPoint[]
  dataKey: ChartMetricKey
  color: string
}

export function MetricChart({ title, data, dataKey, color }: MetricChartProps) {
  const thresholds = CHART_THRESHOLDS[dataKey]
  const unit = thresholds.unit === '°C' ? '°C' : ' ms'
  const hasData = data.length > 0

  return (
    <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
      <h3 className="mb-3 text-sm font-medium text-slate-200">{title}</h3>
      <div className="h-56">
        {!hasData ? (
          <div className="relative h-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={[]}>
                <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                <XAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <YAxis
                  domain={thresholds.yDomain}
                  tick={{ fill: '#94a3b8', fontSize: 12 }}
                  unit={thresholds.unit === '°C' ? '°C' : undefined}
                />
                {renderThresholdLines(thresholds, dataKey)}
              </LineChart>
            </ResponsiveContainer>
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center text-sm text-slate-500">
              Waiting for live telemetry...
            </div>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
              <XAxis
                dataKey="label"
                tick={{ fill: '#94a3b8', fontSize: 12 }}
                minTickGap={24}
              />
              <YAxis
                domain={thresholds.yDomain}
                tick={{ fill: '#94a3b8', fontSize: 12 }}
                unit={thresholds.unit === '°C' ? '°C' : undefined}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  borderRadius: '0.5rem',
                }}
                labelStyle={{ color: '#cbd5e1' }}
                formatter={(value) => [
                  `${Number(value).toFixed(1)}${unit}`,
                  title,
                ]}
              />
              {renderThresholdLines(thresholds, dataKey)}
              <Line
                type="monotone"
                dataKey={dataKey}
                stroke={color}
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </section>
  )
}

function renderThresholdLines(
  thresholds: (typeof CHART_THRESHOLDS)[ChartMetricKey],
  dataKey: ChartMetricKey,
) {
  const unit = CHART_THRESHOLDS[dataKey].unit

  return (
    <>
      <ReferenceLine
        y={thresholds.warning}
        stroke={THRESHOLD_LINE_STYLES.warning.stroke}
        strokeDasharray="4 4"
        strokeWidth={1.5}
        label={{
          value: `Warning ${thresholds.warning}${unit}`,
          fill: THRESHOLD_LINE_STYLES.warning.labelFill,
          fontSize: 11,
          position: 'insideTopRight',
        }}
      />
      <ReferenceLine
        y={thresholds.critical}
        stroke={THRESHOLD_LINE_STYLES.critical.stroke}
        strokeDasharray="4 4"
        strokeWidth={1.5}
        label={{
          value: `Critical ${thresholds.critical}${unit}`,
          fill: THRESHOLD_LINE_STYLES.critical.labelFill,
          fontSize: 11,
          position: 'insideBottomRight',
        }}
      />
    </>
  )
}
