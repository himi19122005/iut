# Office Energy Monitor

A real-time system for monitoring simulated lights and fans across the office — accessible through a live web dashboard and a Discord bot — built to solve one recurring problem: people leaving devices on after hours and driving up the electricity bill.

## Overview

The office has 3 rooms — **Drawing Room**, **Work Room 1**, and **Work Room 2** — each with 2 fans and 3 lights (18 devices total). Since there's no real hardware, a background simulator mimics realistic office behavior by randomly toggling devices on and off over time. A Flask backend holds the live state of every device and streams updates in real time to a web dashboard over WebSockets, while a Discord bot queries the same backend on demand — so both interfaces always reflect the same reality.

## Architecture

```
Simulator (background thread in Flask)
     → mutates in-memory device state
     → emits live updates over WebSocket (device_update, usage_update)
            ↓
Flask backend (single source of truth)
     → REST API: /api/devices, /api/usage
     → WebSocket: real-time push to connected dashboards
            ↓                              ↓
Web Dashboard                    Discord Bot
(Socket.IO client, live UI)      (polls REST endpoints on command)
```

One Flask process owns all device state. The dashboard and the Discord bot are both just clients reading from it — the dashboard via WebSocket + REST, the bot via REST only.

## Features Implemented

### Backend (Flask + Flask-SocketIO)
- In-memory data model for all 18 devices, each tracking: `status` (on/off), `type` (fan/light), `room`, `last_changed` (timestamp), and `total_on_seconds` (cumulative on-time, banked every time a device turns off)
- Background simulator loop giving each device an independent random chance to flip state on every tick — avoids all devices changing in lockstep, producing more realistic, staggered behavior
- Real-time push via WebSocket:
  - `device_update` — broadcast whenever device states change
  - `usage_update` — broadcast every tick with current power/energy figures
- REST API (shared by both the dashboard's initial load and the Discord bot):
  - `GET /api/devices` — full current state of every device
  - `GET /api/usage` — current power draw (W), total accumulated energy (kWh), and estimated cost
- Centralized `calculate_usage()` function — single source of truth for all power/energy math, used by both the REST endpoint and the live WebSocket broadcast, avoiding duplicated/drifting logic

### Web Dashboard
- Live-updating device cards grouped by room, reflecting real-time on/off status with zero page refreshes
- KPI panel showing current power draw (W), total energy used (kWh), and estimated cost
- Initial state fetched via REST on page load, then kept live via WebSocket — dashboard is always correct, even before the first simulator tick
- Dark, control-room-style visual design: devices glow (color-coded by type — amber for lights, teal for fans) with a pulsing animation when on, and recede into the background when off, making wasted energy visually obvious at a glance

### Discord Bot
- `!status` — summarizes how many devices are on/off per room, office-wide
- `!room <name>` — status of a specific room (supports friendly aliases, e.g. `work1` → Work Room 1)
- `!usage` — current power draw, accumulated energy, and estimated cost, pulled live from the same backend as the dashboard
- `!checkafterhours` — checks whether any device is still on and reports which ones (manual trigger for demo purposes)
- Scheduled after-hours check — automatically runs once daily at 9:30 PM and posts an alert to a designated Discord channel if any device is still on, directly addressing the original problem of lights/fans being left running
- Optional natural-language response formatting via LLM (Groq), with automatic fallback to plain formatted text if the LLM call fails or is unavailable — ensures the bot never goes silent
- Error handling around all backend calls (timeouts, connection failures) so the bot degrades gracefully instead of crashing if Flask is unreachable

## Tech Stack
- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML, CSS, vanilla JavaScript, Socket.IO client
- **Bot**: Python, discord.py, requests
- **Optional AI layer**: Groq API (LLM-based response phrasing)

## Why This Design
- **Single source of truth**: All device state and power calculations live in one place (the Flask process). The dashboard and Discord bot are both simply clients of that one backend, guaranteeing they can never show conflicting information.
- **True real-time, not polling**: The dashboard uses WebSocket server-push, so updates appear instantly as they happen rather than on a delay from periodic refreshing.
- **Resilience**: Both the bot and dashboard handle backend downtime gracefully rather than crashing or hanging.
