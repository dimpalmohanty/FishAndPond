## Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/ponds` | Get all pond telemetry |
| GET | `/ponds/{pond_id}` | Get single pond data |
| POST | `/chat` | Main AI chat endpoint |
| DELETE | `/session/{session_id}` | Clear conversation memory |

---

# Example Chat Request

```json
{
  "message": "Is this pond safe for feeding?",
  "pond_id": "pond_2",
  "session_id": null
}
```

---

# Example Chat Response

```json
{
  "reply": "⚠️ CAUTION — Oxygen levels are slightly low and ammonia is elevated. Increase aeration and reduce feeding temporarily to avoid fish stress.",
  "session_id": "abc123",
  "pond_id": "pond_2",
  "latency_ms": 642,
  "token_usage": {
    "prompt_tokens": 168,
    "completion_tokens": 58,
    "total_tokens": 226
  },
  "sensor_snapshot": {
    "ph": 6.8,
    "dissolved_oxygen": 4.7,
    "ammonia_ppm": 0.72
  }
}
```

---

# Example Questions Users Can Ask

## Pond Health
- Is this pond healthy?
- Which pond needs attention?
- Is water quality safe?

## Oxygen
- Is oxygen dangerously low?
- Should aerators be turned on?

## Ammonia
- Is ammonia harmful right now?
- Should feeding be reduced?

## Algae
- Is algae bloom forming?
- Why is the water turning green?

## Operations
- What preventive actions do you recommend?
- Which parameter is most dangerous?

---

# Production Integration

The current system uses simulated telemetry.

To integrate with real IoT devices:

Replace:

```python
mock_sensors.py
```

with:
- MQTT consumers
- .NET APIs
- IoT gateways
- sensor databases

without changing AI architecture.

---

# Design Philosophy

This project intentionally separates:

## Deterministic Analysis
Handled by Python rule engine.

## Conversational Explanation
Handled by the LLM.

This improves:
- reliability
- consistency
- interpretability
- production readiness

---

# Future Improvements

- Historical trend graphs
- Real-time alerts
- Predictive analytics
- Fish disease prediction
- Multi-language farmer support
- MQTT integration
- Redis-backed session storage
- Database persistence
- Real IoT device integration

---

# Deployment

| Service | Platform |
|---|---|
| Frontend | Netlify |
| Backend | Render |
| AI Provider | Groq |

---

# Author

Built as an AI-assisted IoT aquaculture monitoring prototype using FastAPI, React, and LLM integration.