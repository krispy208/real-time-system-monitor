"""SQLite DDL for telemetry and alert persistence."""

CREATE_TELEMETRY_TABLE = """
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    cpu_usage REAL NOT NULL,
    memory_usage REAL NOT NULL,
    temperature REAL NOT NULL,
    latency REAL NOT NULL,
    status TEXT NOT NULL
);
"""

CREATE_ALERTS_TABLE = """
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    metric TEXT NOT NULL,
    severity TEXT NOT NULL,
    current_value REAL NOT NULL,
    message TEXT NOT NULL
);
"""

CREATE_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_telemetry_system_timestamp ON telemetry (system_id, timestamp);",
    "CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts (timestamp DESC);",
    "CREATE INDEX IF NOT EXISTS idx_alerts_system_id ON alerts (system_id);",
    "CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts (severity);",
)
