# Fish Pond AI Chatbot — Backend

FastAPI + Gemini 1.5 Flash (free tier) backend for the fish pond management chatbot.

## Folder Structure

```
backend/
├── main.py            # FastAPI app + all routes
├── ai_engine.py       # Gemini API integration + session memory
├── mock_sensors.py    # Simulated IoT sensor data (swap for real API in prod)
├── requirements.txt
├── .env.example       # Copy to .env and add your key
└── README.md
```

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Set up your API key**
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
# Get free key from: https://aistudio.google.com/app/apikey
```

**3. Run the server**
```bash
uvicorn main:app --reload --port 8000
```

**4. Test it**
```bash
# Health check
curl http://localhost:8000/health

# Get pond sensor data
curl http://localhost:8000/ponds/pond_1

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Is the pH safe for my fish?", "pond_id": "pond_1"}'
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/ponds` | All ponds with live sensor data |
| GET | `/ponds/{pond_id}` | Single pond sensor data |
| POST | `/chat` | Main chat endpoint |
| DELETE | `/session/{session_id}` | Clear chat history |

## Chat Request Example

```json
{
  "message": "Can I add 500 new fish to this pond today?",
  "pond_id": "pond_1",
  "session_id": null
}
```

## Chat Response Example

```json
{
  "reply": "⚠️ CAUTION — Not ideal today. Ammonia is at 0.6 ppm (above safe 0.5 ppm limit), which can stress new fish. Temperature at 31°C is also slightly high. Wait 1–2 days, increase aeration, and recheck ammonia before stocking.",
  "session_id": "abc123",
  "pond_id": "pond_1",
  "latency_ms": 980,
  "token_usage": { "prompt_tokens": 210, "completion_tokens": 68, "total_tokens": 278 },
  "sensor_snapshot": { ... }
}
```

## Switching AI Provider (Production)

In `ai_engine.py`, only replace `call_gemini()`:

```python
# Swap to Claude
import anthropic
def call_gemini(system_prompt, history, user_message):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # ... Claude API call here
    return { "reply": ..., "latency_ms": ..., "token_usage": ... }
```

## Connecting Real IoT Data (Production)

In `mock_sensors.py`, replace `get_pond_data()`:

```python
def get_pond_data(pond_id: str):
    response = requests.get(f"https://your-dotnet-api.com/ponds/{pond_id}/sensors")
    return response.json()  # Must return same keys
```

**Nothing else changes.**
