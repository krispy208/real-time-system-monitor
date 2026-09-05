from app.api.schemas.responses import AlertResponse, SystemDetail, SystemSummary
from app.models.alert import Alert
from app.monitoring.evaluator import MonitoringEvaluation


def to_system_summary(evaluation: MonitoringEvaluation) -> SystemSummary:
    reading = evaluation.reading
    return SystemSummary(
        system_id=reading.system_id,
        status=evaluation.overall_status.value,
        cpu_usage=reading.cpu_usage,
        memory_usage=reading.memory_usage,
        temperature=reading.temperature,
        latency=reading.latency,
        timestamp=reading.timestamp,
    )


def to_system_detail(evaluation: MonitoringEvaluation) -> SystemDetail:
    reading = evaluation.reading
    return SystemDetail(
        system_id=reading.system_id,
        status=evaluation.overall_status.value,
        cpu_usage=reading.cpu_usage,
        memory_usage=reading.memory_usage,
        temperature=reading.temperature,
        latency=reading.latency,
        timestamp=reading.timestamp,
        metric_statuses={
            metric: status.value for metric, status in evaluation.metric_statuses.items()
        },
    )
def to_alert_response(alert: Alert) -> AlertResponse:
    return AlertResponse(
        system_id=alert.system_id,
        timestamp=alert.timestamp,
        metric=alert.metric,
        severity=alert.severity,
        current_value=alert.current_value,
        message=alert.message,
    )
