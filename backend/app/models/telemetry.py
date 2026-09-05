from dataclasses import asdict, dataclass


@dataclass
class TelemetryReading:
    system_id: str
    timestamp: str
    cpu_usage: float
    memory_usage: float
    temperature: float
    latency: float

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)

    def format_line(self) -> str:
        return (
            f"{self.system_id} | {self.timestamp} | "
            f"CPU: {self.cpu_usage:.1f}% | MEM: {self.memory_usage:.1f}% | "
            f"TEMP: {self.temperature:.1f}°C | LAT: {self.latency:.1f}ms"
        )
