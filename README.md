# MindGuard MVP

🧠 **Mental Health Monitoring System** - AI-assisted behavioral monitoring and crisis prediction.

## Overview

MindGuard is an MVP prototype that:
- **Monitors behavioral signals** (sleep, mood, social activity, movement, screen time)
- **Predicts mental health crisis risk** using rule-based analysis
- **Displays insights in a dashboard** with trend charts
- **Suggests interventions** based on risk level

## Architecture

```
┌─────────────────┐     HTTP     ┌─────────────────┐
│   Streamlit     │ ──────────►  │    FastAPI      │
│   Frontend      │ ◄──────────  │    Backend      │
│                 │              │                 │
│  • Input Form   │              │  • POST /data   │
│  • Dashboard    │              │  • GET /data    │
│  • Charts       │              │  • POST /predict│
│                 │              │  • GET /health  │
└─────────────────┘              └─────────────────┘
```

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

### 3. Run Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
pytest -v
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/data` | POST | Submit behavioral data |
| `/data` | GET | Get all stored data |
| `/data/latest` | GET | Get latest n entries |
| `/predict` | POST | Get risk prediction |

## Risk Scoring

The risk score (0-1) is calculated based on:

| Factor | Condition | Risk Impact |
|--------|-----------|-------------|
| Sleep | < 4 hours | +0.30 |
| Sleep | < 6 hours | +0.15 |
| Mood | ≤ 3 | +0.40 |
| Mood | ≤ 5 | +0.20 |
| Social | < 5 messages | +0.20 |
| Social | < 10 messages | +0.10 |
| Screen | > 8 hours | +0.10 |
| Movement | < 1000 steps | +0.10 |

### Risk Levels

- 🟢 **Low** (< 0.3): Healthy patterns
- 🟡 **Medium** (0.3-0.6): Some concerns
- 🔴 **High** (≥ 0.6): Intervention recommended

## Project Structure

```
mindguard/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Pydantic models
│   │   ├── repository.py     # In-memory data store
│   │   └── risk_calculator.py # Risk scoring logic
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_repository.py
│   │   └── test_risk_calculator.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api_client.py     # Backend API client
│   │   └── streamlit_app.py  # Streamlit dashboard
│   ├── tests/
│   │   └── test_api_client.py
│   └── requirements.txt
└── README.md
```

## Features

### Input Form
- Sleep hours (0-24)
- Mood score (1-10)
- Messages sent
- Steps walked
- Screen time (hours)

### Dashboard
- Current risk score gauge
- Risk level indicator
- Intervention suggestions
- 7-day trend charts:
  - Mood trend
  - Sleep pattern
  - Activity level
  - Social activity

## Disclaimer

⚠️ **This is a prototype for demonstration purposes only.** 

If you're experiencing mental health challenges, please reach out to a qualified healthcare professional or contact a mental health helpline in your area.

## License

MIT License
