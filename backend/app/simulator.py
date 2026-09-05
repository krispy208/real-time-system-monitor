"""Telemetry simulator for three monitored systems.

Values drift toward targets rather than being re-randomized each tick so the
time series resembles real infrastructure metrics, which change gradually.

Each system follows an internal simulation state machine:
HEALTHY -> DEGRADING -> RECOVERING -> HEALTHY. That controls how synthetic
data is generated. It is separate from the monitoring layer's HEALTHY /
WARNING / CRITICAL evaluation, which judges the resulting metric values.

Run from the backend directory:

    python -m app.simulator
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from app.models.telemetry import TelemetryReading
from app.monitoring import Monitor

SYSTEM_IDS = ("SYSTEM-01", "SYSTEM-02", "SYSTEM-03")

# Healthy operating ranges (typical steady-state values).
HEALTHY_RANGES: dict[str, tuple[float, float]] = {
    "cpu_usage": (20.0, 65.0),
    "memory_usage": (30.0, 70.0),
    "temperature": (50.0, 70.0),
    "latency": (15.0, 60.0),
}

# Upper bounds when a system is under stress.
STRESS_RANGES: dict[str, tuple[float, float]] = {
    "cpu_usage": (75.0, 95.0),
    "memory_usage": (75.0, 92.0),
    "temperature": (78.0, 92.0),
    "latency": (90.0, 220.0),
}

METRIC_NAMES = ("cpu_usage", "memory_usage", "temperature", "latency")


class Phase(str, Enum):
    """Internal simulation phases — not the same as monitoring health status."""

    HEALTHY = "healthy"
    DEGRADING = "degrading"
    RECOVERING = "recovering"


@dataclass
class MetricTracker:
    """Tracks one metric's current value and the healthy target it drifts toward.

    Separating *value* from *healthy_target* lets the simulator recover to a
    sensible baseline after stress without losing its long-term drift center.
    """

    value: float
    healthy_target: float

    def step_toward(self, target: float, max_delta: float) -> None:
        """Move toward *target* in bounded steps instead of jumping randomly."""
        delta = target - self.value
        if abs(delta) <= max_delta:
            self.value = target
        else:
            self.value += max_delta if delta > 0 else -max_delta

    def nudge_healthy_target(self, low: float, high: float) -> None:
        """Slowly shift the healthy target so readings do not repeat forever."""
        shift = random.uniform(-1.5, 1.5)
        self.healthy_target = max(low, min(high, self.healthy_target + shift))


@dataclass
class SystemSimulator:
    """Simulates one system with gradual drift and temporary stress events."""

    system_id: str
    phase: Phase = Phase.HEALTHY
    phase_tick: int = 0
    phase_duration: int = 0
    intensity: float = 0.0
    stressed_metrics: set[str] = field(default_factory=set)
    stress_targets: dict[str, float] = field(default_factory=dict)
    metrics: dict[str, MetricTracker] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.metrics:
            self.metrics = {
                name: MetricTracker(
                    value=random.uniform(*HEALTHY_RANGES[name]),
                    healthy_target=random.uniform(*HEALTHY_RANGES[name]),
                )
                for name in METRIC_NAMES
            }

    def generate_reading(self) -> TelemetryReading:
        self._advance_phase()
        self._update_intensity()
        self._update_metrics()

        return TelemetryReading(
            system_id=self.system_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            cpu_usage=round(self.metrics["cpu_usage"].value, 1),
            memory_usage=round(self.metrics["memory_usage"].value, 1),
            temperature=round(self.metrics["temperature"].value, 1),
            latency=round(self.metrics["latency"].value, 1),
        )

    def _advance_phase(self) -> None:
        if self.phase == Phase.HEALTHY:
            # Roughly one degradation event every 45–90 seconds per system.
            if random.random() < 0.02:
                self._begin_degradation()
            return

        self.phase_tick += 1
        if self.phase_tick >= self.phase_duration:
            if self.phase == Phase.DEGRADING:
                self._begin_recovery()
            else:
                self._return_to_healthy()

    def _begin_degradation(self) -> None:
        self.phase = Phase.DEGRADING
        self.phase_tick = 0
        self.phase_duration = random.randint(7, 12)
        self.stressed_metrics = self._pick_stressed_metrics()
        self.stress_targets = {
            name: random.uniform(*STRESS_RANGES[name]) for name in self.stressed_metrics
        }

    def _begin_recovery(self) -> None:
        self.phase = Phase.RECOVERING
        self.phase_tick = 0
        self.phase_duration = random.randint(7, 12)

    def _return_to_healthy(self) -> None:
        self.phase = Phase.HEALTHY
        self.phase_tick = 0
        self.phase_duration = 0
        self.intensity = 0.0
        self.stressed_metrics.clear()
        self.stress_targets.clear()

    def _pick_stressed_metrics(self) -> set[str]:
        """Choose one or two metrics to degrade (CPU, temperature, and latency are common)."""
        primary = random.choice(["cpu_usage", "temperature", "latency"])
        candidates = [name for name in METRIC_NAMES if name != primary]
        if random.random() < 0.35:
            return {primary}
        secondary = random.choice(candidates)
        return {primary, secondary}

    def _update_intensity(self) -> None:
        """Ramp stress from 0.0 to 1.0 while degrading, then back to 0.0 while recovering."""
        if self.phase == Phase.HEALTHY:
            self.intensity = 0.0
            return

        progress = self.phase_tick / max(self.phase_duration, 1)
        if self.phase == Phase.DEGRADING:
            self.intensity = min(1.0, progress)
        else:
            self.intensity = max(0.0, 1.0 - progress)

    def _update_metrics(self) -> None:
        for name, tracker in self.metrics.items():
            low, high = HEALTHY_RANGES[name]

            if self.phase == Phase.HEALTHY and random.random() < 0.4:
                tracker.nudge_healthy_target(low, high)

            if name in self.stressed_metrics:
                stress_target = self.stress_targets[name]
                # Interpolate between healthy and stress targets using intensity.
                target = tracker.healthy_target + (stress_target - tracker.healthy_target) * self.intensity
            else:
                target = tracker.healthy_target

            # Small per-step cap keeps changes gradual (roughly 1–4 units per second).
            max_delta = random.uniform(1.0, 4.0)
            tracker.step_toward(target, max_delta)

            # Keep values within plausible physical bounds.
            tracker.value = max(low - 5, min(tracker.value, STRESS_RANGES[name][1]))


class TelemetrySimulator:
    """Coordinates all three system simulators and emits one reading per system per cycle."""

    def __init__(self, system_ids: tuple[str, ...] = SYSTEM_IDS) -> None:
        self.systems = [SystemSimulator(system_id=sid) for sid in system_ids]

    def next_readings(self) -> list[TelemetryReading]:
        return [system.generate_reading() for system in self.systems]


def run(interval_seconds: float = 1.0) -> None:
    """Print telemetry readings and monitoring status to stdout until interrupted."""
    simulator = TelemetrySimulator()
    monitor = Monitor()
    print("Starting telemetry simulator with monitoring (Ctrl+C to stop)\n")

    try:
        while True:
            for reading in simulator.next_readings():
                evaluation = monitor.evaluate(reading)
                print(evaluation.format_line())
                for alert in monitor.latest_alerts:
                    print(alert.format_line())
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    run()
