# Fish Pond AI Chatbot — AI-Assisted Aquaculture Monitoring System

An AI-powered fish pond monitoring and decision-support system built using FastAPI, React, and Groq LLM integration.

This project simulates real-time IoT pond telemetry and converts raw sensor data into conversational, farmer-friendly insights using an AI assistant.

---

# Features

- AI-assisted pond health monitoring
- Real-time simulated IoT sensor telemetry
- Conversational fish farming assistant
- Deterministic pond risk analysis engine
- Low-latency Groq LLM integration
- Session-based conversation memory
- Modern React monitoring dashboard
- Multi-pond support
- Token-efficient AI prompting
- Backend-agnostic architecture

---

# System Architecture

```text
React Frontend
       ↓
FastAPI Backend
       ↓
Risk Analysis Engine (Python)
       ↓
Groq LLM (Llama 3.1)
```

The system separates:
- deterministic pond analysis (Python)
- conversational explanation (LLM)

This reduces hallucinations and improves reliability.

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + CSS |
| Backend | FastAPI |
| AI Provider | Groq |
| AI Model | llama-3.1-8b-instant |
| Language | Python |
| Communication | REST API |
| Sensor Layer | Simulated IoT Telemetry |

---

# Folder Structure

```text
Fish_Pond_AI_Chatbot/
│
├── backend/
│   ├── main.py
│   ├── ai_engine.py
│   ├── mock_sensors.py
│   ├── risk_engine.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Backend Features

## AI Engine
- Groq API integration
- Session-aware chat memory
- Token-efficient prompting
- Structured AI responses

## Risk Engine
Deterministic pond analysis for:
- oxygen risk
- ammonia toxicity
- unsafe pH
- overall pond health

## Mock Sensor Layer
Simulates:
- pH
- dissolved oxygen
- ammonia
- algae
- nitrite
- turbidity
- temperature

Can be replaced directly with real IoT APIs.

---

# Frontend Features

- Real-time pond dashboard
- AI chatbot interface
- Pond selector
- Live sensor cards
- SAFE / RISK indicators
- Token + latency metrics
- Suggested quick prompts
- Independent dashboard scrolling

---

# Setup Instructions

# 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/FishAndPond.git
cd FishAndPond
```

---

# 2. Backend Setup

```bash
cd backend
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 3. Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get Groq API key from:

https://console.groq.com/

---

# 4. Run Backend

```bash
uvicorn main:app --reload --port 8000
```

Backend runs on:

```text
http://localhost:8000
```

---

