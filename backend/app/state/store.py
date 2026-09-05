from collections import deque
from dataclasses import dataclass, field
from threading import Lock

from app.models.alert import Alert
from app.models.telemetry import TelemetryReading
from app.monitoring.evaluator import MonitoringEvaluation
from app.simulator import SYSTEM_IDS

MAX_TELEMETRY_HISTORY = 100
MAX_ALERTS = 100


@dataclass
class SystemState:
    latest_reading: TelemetryReading | None = None
    latest_evaluation: MonitoringEvaluation | None = None
    telemetry_history: deque[TelemetryReading] = field(
        default_factory=lambda: deque(maxlen=MAX_TELEMETRY_HISTORY)
    )


class StateStore:
    """Thread-safe in-memory store for latest telemetry, evaluations, and alerts."""

    def __init__(self, system_ids: tuple[str, ...] = SYSTEM_IDS) -> None:
        self._system_ids = system_ids
        self._systems: dict[str, SystemState] = {
            system_id: SystemState() for system_id in system_ids
        }
        self._alerts: deque[Alert] = deque(maxlen=MAX_ALERTS)
        self._lock = Lock()

    @property
    def system_ids(self) -> tuple[str, ...]:
        return self._system_ids

    def is_known_system(self, system_id: str) -> bool:
        return system_id in self._systems

    def record(self, evaluation: MonitoringEvaluation, alerts: list[Alert]) -> None:
        with self._lock:
            state = self._systems[evaluation.reading.system_id]
            state.latest_reading = evaluation.reading
            state.latest_evaluation = evaluation
            state.telemetry_history.append(evaluation.reading)
            for alert in alerts:
                self._alerts.append(alert)

    def get_system_state(self, system_id: str) -> SystemState | None:
        if not self.is_known_system(system_id):
            return None
        with self._lock:
            return self._systems[system_id]

    def get_all_system_states(self) -> list[tuple[str, SystemState]]:
        with self._lock:
            return [(system_id, self._systems[system_id]) for system_id in self._system_ids]

    def get_telemetry_history(self, system_id: str) -> list[TelemetryReading] | None:
        if not self.is_known_system(system_id):
            return None
        with self._lock:
            return list(self._systems[system_id].telemetry_history)

    def get_alerts(self) -> list[Alert]:
        with self._lock:
            return list(self._alerts)
