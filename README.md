# Real-Time System Monitor

A full-stack dashboard that monitors simulated system telemetry in real time. I built this project to learn more about WebSockets, FastAPI, and real-time communication between a backend and frontend.

## Features

- Simulates CPU, memory, temperature, and latency for three systems
- Streams live telemetry to the dashboard using WebSockets
- Classifies systems as Healthy, Warning, or Critical
- Generates alerts when a metric changes health status
- Stores telemetry and alerts in SQLite
- Displays live temperature and latency charts

## Tech Stack

**Frontend:** React, TypeScript, Tailwind CSS, Recharts  
**Backend:** Python, FastAPI, WebSockets  
**Database:** SQLite

## How It Works

The backend generates telemetry for three simulated systems about once per second. Each reading is checked against warning and critical thresholds.

REST endpoints provide the initial system state and historical data. A WebSocket connection handles live updates so the dashboard does not need to continuously poll the backend.

Telemetry and alerts are also saved to SQLite so historical data remains available after restarting the server.

## Screenshots

### Dashboard

![Dashboard](docs/images/dashboard2.png)

### Live Telemetry

![Telemetry Charts](docs/images/charts.png)

### Alerts

![Alerts](docs/images/alerts.png)

## Running Locally

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend runs at `http://localhost:8000`.

FastAPI's API documentation is available at `http://localhost:8000/docs`.

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` to view the dashboard.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/systems` | Get the current state of all systems |
| GET | `/api/systems/{system_id}` | Get the current state of one system |
| GET | `/api/telemetry/{system_id}` | Get historical telemetry |
| GET | `/api/alerts` | Get alert history |
| WebSocket | `/ws/telemetry` | Receive live telemetry updates |

## Project Structure

```text
real-time-system-monitor/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── db/
│   │   ├── monitoring/
│   │   ├── services/
│   │   ├── state/
│   │   └── simulator.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── hooks/
│       └── types/
│
└── docs/
    └── images/
```