export type HealthStatus = 'HEALTHY' | 'WARNING' | 'CRITICAL'

export interface SystemSummary {
  system_id: string
  status: HealthStatus
  cpu_usage: number
  memory_usage: number
  temperature: number
  latency: number
  timestamp: string
}

export interface AlertRecord {
  system_id: string
  timestamp: string
  metric: string
  severity: string
  current_value: number
  message: string
}

export interface TelemetryHistoryPoint {
  system_id: string
  timestamp: string
  cpu_usage: number
  memory_usage: number
  temperature: number
  latency: number
}
