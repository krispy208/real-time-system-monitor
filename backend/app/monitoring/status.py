"""Monitoring health status types and severity ordering.

HealthStatus here describes externally evaluated metric/system health based on
thresholds. It must not be confused with the simulator's internal Phase enum
(healthy/degrading/recovering), which only controls synthetic data generation.
"""

from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


SEVERITY_RANK: dict[HealthStatus, int] = {
    HealthStatus.HEALTHY: 0,
    HealthStatus.WARNING: 1,
    HealthStatus.CRITICAL: 2,
}

METRIC_LABELS: dict[str, str] = {
    "cpu_usage": "CPU usage",
    "memory_usage": "Memory usage",
    "temperature": "Temperature",
    "latency": "Latency",
}

METRIC_UNITS: dict[str, str] = {
    "cpu_usage": "%",
    "memory_usage": "%",
    "temperature": "°C",
    "latency": "ms",
}

MONITORED_METRICS = ("cpu_usage", "memory_usage", "temperature", "latency")
