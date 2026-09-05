from pydantic import BaseModel


class SystemSummary(BaseModel):
    system_id: str
    status: str
    cpu_usage: float
    memory_usage: float
    temperature: float
    latency: float
    timestamp: str


class SystemDetail(BaseModel):
    system_id: str
    status: str
    cpu_usage: float
    memory_usage: float
    temperature: float
    latency: float
    timestamp: str
    metric_statuses: dict[str, str]


class TelemetryReadingResponse(BaseModel):
    system_id: str
    timestamp: str
    cpu_usage: float
    memory_usage: float
    temperature: float
    latency: float
    status: str


class AlertResponse(BaseModel):
    system_id: str
    timestamp: str
    metric: str
    severity: str
    current_value: float
    message: str
