from dataclasses import dataclass

from app.models.telemetry import TelemetryReading
from app.monitoring.status import (
    METRIC_UNITS,
    HealthStatus,
    MONITORED_METRICS,
    SEVERITY_RANK,
)
from app.monitoring.thresholds import MetricThresholds, get_thresholds


def evaluate_metric(
    metric: str,
    value: float,
    thresholds: dict[str, MetricThresholds] | None = None,
) -> HealthStatus:
    """Assign a health status to a single metric value."""
    config = (thresholds or get_thresholds())[metric]

    if value >= config.critical:
        return HealthStatus.CRITICAL
    if value >= config.warning:
        return HealthStatus.WARNING
    return HealthStatus.HEALTHY


def evaluate_reading(
    reading: TelemetryReading,
    thresholds: dict[str, MetricThresholds] | None = None,
) -> tuple[HealthStatus, dict[str, HealthStatus]]:
    """Evaluate all metrics and derive overall status from the worst metric.

    One critical metric (for example temperature) means the whole system is
    treated as critical even if other metrics are healthy.
    """
    metric_statuses = {
        metric: evaluate_metric(metric, getattr(reading, metric), thresholds)
        for metric in MONITORED_METRICS
    }
    overall = max(metric_statuses.values(), key=lambda status: SEVERITY_RANK[status])
    return overall, metric_statuses


@dataclass
class MonitoringEvaluation:
    """Result of evaluating one telemetry reading."""

    reading: TelemetryReading
    overall_status: HealthStatus
    metric_statuses: dict[str, HealthStatus]

    def format_line(self) -> str:
        reading = self.reading
        return (
            f"{reading.system_id} | {reading.timestamp} | "
            f"STATUS: {self.overall_status.value} | "
            f"CPU: {reading.cpu_usage:.1f}% | MEM: {reading.memory_usage:.1f}% | "
            f"TEMP: {reading.temperature:.1f}°C | LAT: {reading.latency:.1f}ms"
        )

    def format_metric_summary(self) -> str:
        parts = []
        for metric in MONITORED_METRICS:
            value = getattr(self.reading, metric)
            status = self.metric_statuses[metric]
            unit = METRIC_UNITS[metric]
            parts.append(f"{metric}={value:.1f}{unit} ({status.value})")
        return "  metrics: " + ", ".join(parts)
