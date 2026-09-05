import { useCallback, useEffect, useMemo, useState } from 'react'

import { fetchAlerts, fetchSystems } from '../api/client'
import {
  MAX_CHART_POINTS,
  SYSTEM_IDS,
  type SystemId,
} from '../config'
import { useTelemetryWebSocket } from '../hooks/useTelemetryWebSocket'
import type {
  AlertRecord,
  ChartPoint,
  SystemSummary,
  TelemetryUpdate,
} from '../types'
import { AlertPanel } from './AlertPanel'
import { ConnectionStatus } from './ConnectionStatus'
import { MetricChart } from './MetricChart'
import { SummaryBar } from './SummaryBar'
import { SystemCard } from './SystemCard'

const MAX_ALERTS = 100

// Chart history is keyed by system so switching the selector shows accumulated
// data immediately instead of waiting for new WebSocket messages.
function createEmptyChartHistory(): Record<SystemId, ChartPoint[]> {
  return {
    'SYSTEM-01': [],
    'SYSTEM-02': [],
    'SYSTEM-03': [],
  }
}

function toChartPoint(message: TelemetryUpdate): ChartPoint {
  return {
    timestamp: message.timestamp,
    temperature: message.temperature,
    latency: message.latency,
    label: new Date(message.timestamp).toLocaleTimeString(),
  }
}

function toSystemSummary(message: TelemetryUpdate): SystemSummary {
  return {
    system_id: message.system_id,
    status: message.status,
    cpu_usage: message.cpu_usage,
    memory_usage: message.memory_usage,
    temperature: message.temperature,
    latency: message.latency,
    timestamp: message.timestamp,
  }
}

function sortAlertsNewestFirst(alerts: AlertRecord[]): AlertRecord[] {
  return [...alerts].sort(
    (left, right) =>
      new Date(right.timestamp).getTime() - new Date(left.timestamp).getTime(),
  )
}

export function Dashboard() {
  const [systems, setSystems] = useState<Record<string, SystemSummary>>({})
  const [alerts, setAlerts] = useState<AlertRecord[]>([])
  const [chartHistory, setChartHistory] = useState(createEmptyChartHistory)
  const [selectedSystemId, setSelectedSystemId] = useState<SystemId>('SYSTEM-01')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    // REST bootstrap: populate cards, summary, and alert history before live stream.
    async function loadInitialData() {
      try {
        const [systemsResponse, alertsResponse] = await Promise.all([
          fetchSystems(),
          fetchAlerts(),
        ])

        if (cancelled) {
          return
        }

        const systemsById = Object.fromEntries(
          systemsResponse.map((system) => [system.system_id, system]),
        )
        setSystems(systemsById)
        setAlerts(sortAlertsNewestFirst(alertsResponse))
        setError(null)
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : 'Failed to load dashboard data',
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadInitialData()

    return () => {
      cancelled = true
    }
  }, [])

  const handleTelemetryMessage = useCallback((message: TelemetryUpdate) => {
    setSystems((previous) => ({
      ...previous,
      [message.system_id]: toSystemSummary(message),
    }))

    setChartHistory((previous) => {
      const nextPoint = toChartPoint(message)
      const systemId = message.system_id as SystemId
      // Immutable append + slice keeps React state predictable and caps chart points.
      const updatedHistory = [...(previous[systemId] ?? []), nextPoint].slice(
        -MAX_CHART_POINTS,
      )

      return {
        ...previous,
        [systemId]: updatedHistory,
      }
    })

    if (message.alerts.length > 0) {
      setAlerts((previous) =>
        sortAlertsNewestFirst([...message.alerts, ...previous]).slice(
          0,
          MAX_ALERTS,
        ),
      )
    }
  }, [])

  // Open WebSocket only after REST bootstrap succeeds.
  const { connectionState } = useTelemetryWebSocket({
    onMessage: handleTelemetryMessage,
    enabled: !loading && error === null,
  })

  const selectedChartData = useMemo(
    () => chartHistory[selectedSystemId] ?? [],
    [chartHistory, selectedSystemId],
  )

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-300">
        Loading dashboard...
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 px-4 text-center text-red-300">
        {error}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/80">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-5 sm:px-6">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">
              Real-Time System Monitor
            </h1>
            <p className="mt-1 text-sm text-slate-400">
              Live telemetry dashboard
            </p>
          </div>
          <ConnectionStatus state={connectionState} />
        </div>
      </header>

      <main className="mx-auto max-w-7xl space-y-6 px-4 py-6 sm:px-6">
        <SummaryBar systems={systems} />

        <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {SYSTEM_IDS.map((systemId) => {
            const system = systems[systemId]
            if (!system) {
              return null
            }
            return <SystemCard key={systemId} system={system} />
          })}
        </section>

        <section className="flex flex-wrap items-center gap-3">
          <label
            htmlFor="chart-system"
            className="text-sm font-medium text-slate-300"
          >
            Chart system
          </label>
          <select
            id="chart-system"
            value={selectedSystemId}
            onChange={(event) =>
              setSelectedSystemId(event.target.value as SystemId)
            }
            className="rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100"
          >
            {SYSTEM_IDS.map((systemId) => (
              <option key={systemId} value={systemId}>
                {systemId}
              </option>
            ))}
          </select>
        </section>

        <section className="grid gap-4 xl:grid-cols-2">
          <MetricChart
            title={`${selectedSystemId} temperature`}
            data={selectedChartData}
            dataKey="temperature"
            color="#38bdf8"
          />
          <MetricChart
            title={`${selectedSystemId} latency`}
            data={selectedChartData}
            dataKey="latency"
            color="#a78bfa"
          />
        </section>

        <AlertPanel alerts={alerts} />
      </main>
    </div>
  )
}
