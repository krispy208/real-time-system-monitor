from app.models.alert import Alert
from app.monitoring.evaluator import MonitoringEvaluation


def build_telemetry_message(
    evaluation: MonitoringEvaluation,
    alerts: list[Alert],
) -> dict:
    """Build the JSON payload pushed to WebSocket clients for one telemetry update."""
    reading = evaluation.reading
    return {
        "system_id": reading.system_id,
        "timestamp": reading.timestamp,
        "cpu_usage": reading.cpu_usage,
        "memory_usage": reading.memory_usage,
        "temperature": reading.temperature,
        "latency": reading.latency,
        "status": evaluation.overall_status.value,
        "metric_statuses": {
            metric: status.value for metric, status in evaluation.metric_statuses.items()
        },
        "alerts": [alert.to_dict() for alert in alerts],
    }
