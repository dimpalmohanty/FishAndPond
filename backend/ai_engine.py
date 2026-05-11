"""
ai_engine.py
------------
Handles all AI logic:
  - System prompt construction with injected sensor data
  - Groq API call (using Llama 3 model)
  - Conversation history management (max 6 turns)
  - Token-efficient prompt design

PRODUCTION SWAP NOTE:
    To switch to Claude or OpenAI, only replace `call_groq()`.
    `build_system_prompt()` and session logic stay identical.
"""

import os
import json
import time
import logging
import requests
from typing import Optional
from mock_sensors import get_safe_ranges
from risk_engine import analyze_pond
logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_HISTORY_TURNS = 6     # Keep last 6 exchanges to save tokens
MAX_OUTPUT_TOKENS = 350   # Concise answers, low cost
TEMPERATURE       = 0.3   # Factual domain — low creativity



# ── Session Memory ─────────────────────────────────────────────────────────────
# In-memory session store: { session_id: [ {role, content}, ... ] }
# For production: replace with Redis or a DB-backed store
_sessions: dict[str, list] = {}


def get_history(session_id: str) -> list:
    return _sessions.get(session_id, [])


def update_history(session_id: str, role: str, content: str):
    if session_id not in _sessions:
        _sessions[session_id] = []

    _sessions[session_id].append({"role": role, "content": content})

    # Keep only last MAX_HISTORY_TURNS exchanges (each turn = user + assistant)
    max_messages = MAX_HISTORY_TURNS * 2
    if len(_sessions[session_id]) > max_messages:
        _sessions[session_id] = _sessions[session_id][-max_messages:]


def clear_history(session_id: str):
    _sessions.pop(session_id, None)


# ── Gemini API Call ────────────────────────────────────────────────────────────
def call_groq(system_prompt: str, history: list, user_message: str) -> dict:
    """
    Calls Groq API using Llama 3 model.
    Returns { reply, latency_ms, token_usage }

    PRODUCTION SWAP:
        Replace this function body with Claude or OpenAI SDK call.
        Keep the return shape: { reply, latency_ms, token_usage }
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set in environment")

    # Build messages array: system + history + new user message
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "temperature": TEMPERATURE,
    }

    start = time.time()
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=15
    )
    latency_ms = round((time.time() - start) * 1000)

    if response.status_code != 200:
        logger.error(f"Groq API error {response.status_code}: {response.text}")
        raise RuntimeError(f"Groq API error: {response.status_code} — {response.text}")

    data = response.json()

    # Extract reply text
    try:
        reply = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected Groq response shape: {data}")
        raise RuntimeError("Failed to parse Groq response") from e

    # Token usage
    usage = data.get("usage", {})
    token_usage = {
        "prompt_tokens":     usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens":      usage.get("total_tokens", 0),
    }

    return {
        "reply":       reply,
        "latency_ms":  latency_ms,
        "token_usage": token_usage,
    }

def chat(session_id: str, user_message: str, sensor_data: dict):

    history = get_history(session_id)

    analysis = analyze_pond(sensor_data)

    risk = analysis["risk_level"]
    issues = analysis["issues"]
    recommendations = analysis["recommendations"]

    prompt = f"""
Pond Risk Level: {risk}

Detected Issues:
{issues}

Recommendations:
{recommendations}

Live Sensor Data:
- pH: {sensor_data['ph']}
- Temperature: {sensor_data['temperature_c']}°C
- Oxygen: {sensor_data['dissolved_oxygen']} mg/L
- Ammonia: {sensor_data['ammonia_ppm']} ppm

User Question:
{user_message}

Explain clearly in under 80 words.
"""

    result = call_groq(
        system_prompt="""
You are AquaBot, an expert fish pond management assistant.

Give concise, practical, farmer-friendly advice.
Never invent sensor values.
""",
        history=history,
        user_message=prompt
    )

    update_history(session_id, "user", user_message)
    update_history(session_id, "assistant", result["reply"])

    return {
        "reply": result["reply"],
        "session_id": session_id,
        "pond_id": sensor_data["pond_id"],
        "latency_ms": result["latency_ms"],
        "token_usage": result["token_usage"],
        "sensor_snapshot": sensor_data,
    }