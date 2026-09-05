# Real-Time System Monitor

A portfolio project for learning and demonstrating real-time system monitoring with a Python/FastAPI backend and a React/TypeScript frontend.

## Architecture (planned)

```
Telemetry simulator → FastAPI backend → threshold evaluation + SQLite storage → WebSocket → React dashboard
```

## Tech stack

**Backend:** Python, FastAPI, WebSockets, SQLite  
**Frontend:** React, Vite, TypeScript, Tailwind CSS, Recharts

## Project structure

```
real-time-system-monitor/
├── backend/          # FastAPI application
└── frontend/         # React dashboard
```

## Getting started

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## Status

Initial project structure only. Telemetry simulation, WebSockets, SQLite persistence, alert logic, and dashboard features are not yet implemented.
