"""Centralized monitoring threshold configuration.

All alert evaluation reads from here so threshold values are not scattered
across the codebase.
"""

from dataclasses import dataclass

from app.monitoring.status import MONITORED_METRICS


@dataclass(frozen=True)
class MetricThresholds:
    """Upper bounds for a metric where higher values are worse."""

    warning: float
    critical: float


DEFAULT_THRESHOLDS: dict[str, MetricThresholds] = {
    "temperature": MetricThresholds(warning=75.0, critical=90.0),
    "cpu_usage": MetricThresholds(warning=75.0, critical=90.0),
    "memory_usage": MetricThresholds(warning=80.0, critical=92.0),
    "latency": MetricThresholds(warning=100.0, critical=200.0),
}


def get_thresholds() -> dict[str, MetricThresholds]:
    """Return the active threshold configuration."""
    return DEFAULT_THRESHOLDS


def validate_thresholds(thresholds: dict[str, MetricThresholds]) -> None:
    """Ensure every monitored metric has thresholds and warning < critical."""
    for metric in MONITORED_METRICS:
        if metric not in thresholds:
            raise ValueError(f"Missing thresholds for metric: {metric}")
        t = thresholds[metric]
        if t.warning >= t.critical:
            raise ValueError(
                f"Thresholds for {metric}: warning ({t.warning}) must be below critical ({t.critical})"
            )
