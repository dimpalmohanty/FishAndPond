"""
main.py
-------
FastAPI backend for the Fish Pond AI Chatbot.

Endpoints:
    POST /chat          — Main chat endpoint
    GET  /ponds         — List all ponds with live sensor data
    GET  /ponds/{id}    — Single pond sensor data
    DELETE /session/{id}— Clear conversation history
    GET  /health        — Health check

Run:
    uvicorn main:app --reload --port 8000
"""

import uuid
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from mock_sensors import get_pond_data, get_all_ponds_summary
from ai_engine import chat, clear_history

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ── App Setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Fish Pond AI Chatbot API",
    description="IoT-integrated AI chatbot for fish pond management",
    version="1.0.0"
)

# CORS — allow React frontend on localhost:3000 and localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message:    str            = Field(..., min_length=1, max_length=500,
                                       description="User's question")
    pond_id:    str            = Field(default="pond_1",
                                       description="Which pond to query sensors for")
    session_id: Optional[str]  = Field(default=None,
                                       description="Session ID for conversation history. "
                                                   "Leave empty on first message — one will be generated.")

    class Config:
        json_schema_extra = {
            "example": {
                "message":    "Is the pH level safe for my fish right now?",
                "pond_id":    "pond_1",
                "session_id": None
            }
        }


class ChatResponse(BaseModel):
    reply:           str
    session_id:      str
    pond_id:         str
    latency_ms:      int
    token_usage:     dict
    sensor_snapshot: dict


class SensorResponse(BaseModel):
    pond_id:          str
    pond_name:        str
    fish_type:        str
    fish_count:       int
    ph:               float
    temperature_c:    float
    dissolved_oxygen: float
    ammonia_ppm:      float
    turbidity_ntu:    float
    algae_index:      float
    nitrite_ppm:      float
    water_depth_m:    float
    last_updated:     str
    status:           str


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Simple health check — useful for deployment monitoring."""
    return {"status": "ok", "service": "fishpond-chatbot-api"}


@app.get("/ponds", response_model=list[SensorResponse])
def list_ponds():
    """
    Returns live sensor data for all ponds.
    Frontend uses this to populate the pond selector + status bar.
    """
    return get_all_ponds_summary()


@app.get("/ponds/{pond_id}", response_model=SensorResponse)
def get_pond(pond_id: str):
    """Returns live sensor data for a single pond."""
    valid_ponds = ["pond_1", "pond_2", "pond_3"]
    if pond_id not in valid_ponds:
        raise HTTPException(
            status_code=404,
            detail=f"Pond '{pond_id}' not found. Valid options: {valid_ponds}"
        )
    return get_pond_data(pond_id)


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """
    Main chat endpoint.

    - Generates a session_id if not provided (first message)
    - Fetches fresh sensor data for the selected pond
    - Sends to AI with full conversation history
    - Returns AI reply + metadata (latency, tokens, sensor snapshot)
    """
    # Auto-generate session ID for new conversations
    session_id = req.session_id or str(uuid.uuid4())

    logger.info(f"Chat request | session={session_id} | pond={req.pond_id} | msg='{req.message[:60]}'")

    # Fetch fresh sensor data
    sensor_data = get_pond_data(req.pond_id)

    # Call AI
    try:
        result = chat(
            session_id=session_id,
            user_message=req.message,
            sensor_data=sensor_data
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return ChatResponse(**result)


@app.delete("/session/{session_id}")
def clear_session(session_id: str):
    """
    Clears conversation history for a session.
    Call this when the user clicks 'New Chat'.
    """
    clear_history(session_id)
    return {"message": f"Session '{session_id}' cleared successfully."}
