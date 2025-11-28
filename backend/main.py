"""FastAPI backend for MindGuard."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List

from .models import (
    BehavioralData,
    EmotionAnalysis,
    HealthResponse,
    JournalEntry,
    RiskPrediction,
)
from .risk_calculator import calculate_risk_score
from .ai_insights import analyze_emotions

app = FastAPI(
    title="MindGuard API",
    description="Mental health monitoring and risk prediction API",
    version="1.0.0"
)

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# In-memory data store
data_store: List[dict] = []


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/data")
async def submit_data(data: BehavioralData):
    """Submit behavioral data."""
    entry = data.model_dump()
    entry["timestamp"] = datetime.now().isoformat()
    data_store.append(entry)
    return {"message": "Data submitted successfully", "entry": entry}


@app.get("/data")
async def get_data():
    """Get all stored behavioral data."""
    return {"data": data_store}


@app.post("/predict", response_model=RiskPrediction)
async def predict_risk(data: BehavioralData):
    """Predict risk based on behavioral data."""
    risk_score, risk_level, suggestion, color, drivers, actions = calculate_risk_score(
        sleep_hours=data.sleep_hours,
        mood_score=data.mood_score,
        messages_sent=data.messages_sent,
        steps=data.steps,
        app_usage_hours=data.app_usage_hours
    )
    
    return RiskPrediction(
        risk_score=risk_score,
        risk_level=risk_level,
        suggestion=suggestion,
        color=color,
        drivers=drivers,
        recommended_actions=actions
    )


@app.get("/latest")
async def get_latest():
    """Get the latest 7 entries for trend analysis."""
    return {"data": data_store[-7:] if data_store else []}


@app.post("/analyze-text", response_model=EmotionAnalysis)
async def analyze_text(entry: JournalEntry):
    """Analyze a free-form journal entry for emotional context."""
    result = analyze_emotions(entry.text)
    return EmotionAnalysis(**result.to_dict())
