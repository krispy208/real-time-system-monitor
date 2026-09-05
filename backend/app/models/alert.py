from dataclasses import asdict, dataclass


@dataclass
class Alert:
    system_id: str
    timestamp: str
    metric: str
    severity: str
    current_value: float
    message: str

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)

    def format_line(self) -> str:
        return f"  >> ALERT [{self.severity}] {self.system_id} | {self.message}"
