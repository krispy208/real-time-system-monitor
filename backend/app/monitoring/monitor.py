from app.models.alert import Alert
from app.models.telemetry import TelemetryReading
from app.monitoring.alert_detector import AlertDetector
from app.monitoring.evaluator import MonitoringEvaluation, evaluate_reading
from app.monitoring.thresholds import get_thresholds, validate_thresholds


class Monitor:
    """Evaluates telemetry readings and emits alerts on metric status changes."""

    def __init__(self) -> None:
        thresholds = get_thresholds()
        validate_thresholds(thresholds)
        self._thresholds = thresholds
        self._alert_detector = AlertDetector()
        self._latest_alerts: list[Alert] = []

    def evaluate(self, reading: TelemetryReading) -> MonitoringEvaluation:
        overall, metric_statuses = evaluate_reading(reading, self._thresholds)
        evaluation = MonitoringEvaluation(
            reading=reading,
            overall_status=overall,
            metric_statuses=metric_statuses,
        )
        self._latest_alerts = self._alert_detector.process(reading, metric_statuses)
        return evaluation

    @property
    def latest_alerts(self) -> list[Alert]:
        return self._latest_alerts

    def reset(self) -> None:
        self._alert_detector.reset()
        self._latest_alerts = []
