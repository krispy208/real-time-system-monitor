import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import type { ChartPoint } from '../types'

interface MetricChartProps {
  title: string
  data: ChartPoint[]
  dataKey: 'temperature' | 'latency'
  unit: string
  color: string
}

export function MetricChart({
  title,
  data,
  dataKey,
  unit,
  color,
}: MetricChartProps) {
  return (
    <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
      <h3 className="mb-4 text-sm font-medium text-slate-200">{title}</h3>
      <div className="h-64">
        {data.length === 0 ? (
          <div className="flex h-full items-center justify-center text-sm text-slate-500">
            Waiting for live telemetry...
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
                tick={{ fill: '#94a3b8', fontSize: 12 }}
                unit={unit === '°C' ? '°C' : undefined}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  borderRadius: '0.5rem',
                }}
                labelStyle={{ color: '#cbd5e1' }}
                formatter={(value) => [`${Number(value).toFixed(1)}${unit}`, title]}
              />
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
