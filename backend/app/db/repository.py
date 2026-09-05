import sqlite3
import threading
from pathlib import Path

from app.db.schema import CREATE_ALERTS_TABLE, CREATE_INDEXES, CREATE_TELEMETRY_TABLE
from app.models.alert import Alert
from app.monitoring.evaluator import MonitoringEvaluation


class TelemetryRepository:
    """SQLite persistence for telemetry readings and alerts."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._lock = threading.Lock()

    def initialize(self) -> None:
        """Create the database directory and tables if they do not exist."""
        self._database_path.parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as connection:
            connection.execute(CREATE_TELEMETRY_TABLE)
            connection.execute(CREATE_ALERTS_TABLE)
            for statement in CREATE_INDEXES:
                connection.execute(statement)
            connection.commit()

    def insert_telemetry(self, evaluation: MonitoringEvaluation) -> None:
        reading = evaluation.reading
        with self._lock:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO telemetry (
                        system_id,
                        timestamp,
                        cpu_usage,
                        memory_usage,
                        temperature,
                        latency,
                        status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        reading.system_id,
                        reading.timestamp,
                        reading.cpu_usage,
                        reading.memory_usage,
                        reading.temperature,
                        reading.latency,
                        evaluation.overall_status.value,
                    ),
                )
                connection.commit()

    def insert_alerts(self, alerts: list[Alert]) -> None:
        if not alerts:
            return

        with self._lock:
            with self._connect() as connection:
                connection.executemany(
                    """
                    INSERT INTO alerts (
                        system_id,
                        timestamp,
                        metric,
                        severity,
                        current_value,
                        message
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            alert.system_id,
                            alert.timestamp,
                            alert.metric,
                            alert.severity,
                            alert.current_value,
                            alert.message,
                        )
                        for alert in alerts
                    ],
                )
                connection.commit()

    def get_telemetry_history(self, system_id: str, limit: int) -> list[dict]:
        with self._lock:
            with self._connect() as connection:
                rows = connection.execute(
                    """
                    SELECT system_id, timestamp, cpu_usage, memory_usage, temperature, latency, status
                    FROM telemetry
                    WHERE system_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (system_id, limit),
                ).fetchall()

        rows.reverse()
        return [dict(row) for row in rows]

    def get_alerts(
        self,
        limit: int,
        system_id: str | None = None,
        severity: str | None = None,
    ) -> list[Alert]:
        query = """
            SELECT system_id, timestamp, metric, severity, current_value, message
            FROM alerts
            WHERE 1 = 1
        """
        params: list[str | int] = []

        if system_id is not None:
            query += " AND system_id = ?"
            params.append(system_id)

        if severity is not None:
            query += " AND severity = ?"
            params.append(severity)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with self._lock:
            with self._connect() as connection:
                rows = connection.execute(query, params).fetchall()

        return [
            Alert(
                system_id=row["system_id"],
                timestamp=row["timestamp"],
                metric=row["metric"],
                severity=row["severity"],
                current_value=row["current_value"],
                message=row["message"],
            )
            for row in rows
        ]

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        return connection
