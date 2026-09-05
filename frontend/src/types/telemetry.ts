export type SystemStatus = 'healthy' | 'warning' | 'critical'

export interface TelemetryReading {
  system_id: string
  timestamp: string
  cpu_usage: number
  memory_usage: number
  temperature: number
  latency: number
  status: SystemStatus
}
