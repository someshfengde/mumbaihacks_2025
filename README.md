# 🧠 MindGuard - Mental Health Monitoring Dashboard

An aesthetically minimal mental health monitoring application built with Streamlit and FastAPI.

## ✨ Features

- **Beautiful Dark Theme**: Modern, glassmorphism-inspired design
- **Daily Check-ins**: Track sleep, mood, social activity, steps, and screen time
- **AI Risk Assessment**: Rule-based risk scoring with personalized suggestions
- **Trend Visualization**: Track your wellness journey over time
- **Responsive Design**: Works seamlessly on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
chmod +x run.sh
./run.sh
```

Or run separately:

```bash
# Terminal 1 - Start the backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Start the frontend
streamlit run frontend/app.py
```

### Access the Application

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
mumbaihacks_2025/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── models.py         # Pydantic models
│   └── risk_calculator.py # Risk scoring logic
├── frontend/
│   ├── __init__.py
│   └── app.py            # Streamlit application
├── requirements.txt
├── run.sh
└── README.md
```

## 🎨 Design Philosophy

MindGuard follows a **minimal aesthetic design** approach:

- **Color Palette**: Dark gradient backgrounds with teal (#4ECDC4) accents
- **Typography**: Inter font family for clean, modern readability
- **Components**: Glassmorphism cards with subtle borders and shadows
- **Animations**: Smooth transitions and hover effects
- **Icons**: Emoji-based for universal accessibility

## 🔮 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/data` | POST | Submit behavioral data |
| `/data` | GET | Retrieve all stored data |
| `/predict` | POST | Get risk prediction |
| `/latest` | GET | Get last 7 entries |

## 📊 Risk Scoring

The risk score (0-1) is calculated based on:

- **Sleep**: < 4 hours adds +0.3, < 6 hours adds +0.15
- **Mood**: Score ≤ 3 adds +0.4, ≤ 5 adds +0.2
- **Social Activity**: < 3 messages adds +0.15
- **Physical Activity**: < 1000 steps adds +0.1
- **Screen Time**: > 6 hours adds +0.1

## 💙 Built For

MumbaiHacks 2025 - Mental Health Innovation Track

---

*Your wellbeing matters. Take care of yourself.* 🌱
