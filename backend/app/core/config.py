from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    app_name: str = "Real-Time System Monitor"
    api_prefix: str = "/api"
    # Local SQLite file for historical telemetry and alerts.
    database_path: Path = BASE_DIR / "data" / "telemetry.db"


settings = Settings()
