from app.models.alert import Alert
from app.models.telemetry import TelemetryReading
from app.monitoring.status import (
    METRIC_LABELS,
    METRIC_UNITS,
    HealthStatus,
    MONITORED_METRICS,
    SEVERITY_RANK,
)


def _is_escalation(previous: HealthStatus, current: HealthStatus) -> bool:
    return SEVERITY_RANK[current] > SEVERITY_RANK[previous]


def build_alert_message(
    metric: str,
    previous: HealthStatus,
    current: HealthStatus,
    value: float,
) -> str:
    label = METRIC_LABELS[metric]
    unit = METRIC_UNITS[metric]
    value_text = f"{value:.1f}{unit}"

    if _is_escalation(previous, current):
        direction = "increased" if current != HealthStatus.HEALTHY else "changed"
        return f"{label} {direction} from {previous.value} to {current.value} ({value_text})"

    return f"{label} decreased from {previous.value} to {current.value} ({value_text})"


class AlertDetector:
    """Emits alerts only when a metric's health status changes."""

    def __init__(self) -> None:
        # system_id -> metric -> last known HealthStatus
        self._previous_statuses: dict[str, dict[str, HealthStatus]] = {}

    def process(
        self,
        reading: TelemetryReading,
        metric_statuses: dict[str, HealthStatus],
    ) -> list[Alert]:
        alerts: list[Alert] = []
        previous = self._previous_statuses.setdefault(reading.system_id, {})

        for metric in MONITORED_METRICS:
            current = metric_statuses[metric]
            prior = previous.get(metric, HealthStatus.HEALTHY)

            if current != prior:
                value = getattr(reading, metric)
                alerts.append(
                    Alert(
                        system_id=reading.system_id,
                        timestamp=reading.timestamp,
                        metric=metric,
                        severity=current.value,
                        current_value=value,
                        message=build_alert_message(metric, prior, current, value),
                    )
                )

            previous[metric] = current

        return alerts

    def reset(self) -> None:
        self._previous_statuses.clear()
