"""Simple WebSocket test client for live telemetry streaming.

Run from the backend directory while the FastAPI server is running:

    python scripts/ws_test_client.py

Optional arguments:
    --url ws://127.0.0.1:8000/ws/telemetry
    --count 10
"""

from __future__ import annotations

import argparse
import asyncio
import json

import websockets


async def run_client(url: str, count: int) -> None:
    print(f"Connecting to {url} ...")
    async with websockets.connect(url) as websocket:
        print(f"Connected. Waiting for {count} message(s):\n")
        for index in range(1, count + 1):
            raw = await websocket.recv()
            message = json.loads(raw)
            print(f"--- message {index} ---")
            print(json.dumps(message, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Test the /ws/telemetry WebSocket")
    parser.add_argument(
        "--url",
        default="ws://127.0.0.1:8000/ws/telemetry",
        help="WebSocket URL",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of messages to receive before exiting",
    )
    args = parser.parse_args()
    asyncio.run(run_client(args.url, args.count))


if __name__ == "__main__":
    main()
