"""FastAPI application for MindGuard MVP."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .models import (
    BehavioralData,
    BehavioralDataResponse,
    RiskPrediction,
    HealthResponse
)
from .repository import repository
from .risk_calculator import predict_risk

app = FastAPI(
    title="MindGuard API",
    description="Mental health crisis prediction and monitoring API",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/data", response_model=BehavioralDataResponse, tags=["Data"])
def add_behavioral_data(data: BehavioralData):
    """
    Add a new behavioral data entry.
    
    Accepts daily behavioral inputs and stores them in memory.
    """
    return repository.add(data)


@app.get("/data", response_model=List[BehavioralDataResponse], tags=["Data"])
def get_behavioral_data():
    """
    Get all stored behavioral data entries.
    
    Returns list of all entries with their IDs and timestamps.
    """
    return repository.get_all()


@app.get("/data/latest", response_model=List[BehavioralDataResponse], tags=["Data"])
def get_latest_data(n: int = 7):
    """
    Get the latest n behavioral data entries.
    
    Useful for dashboard trend display.
    """
    return repository.get_latest(n)


@app.post("/predict", response_model=RiskPrediction, tags=["Prediction"])
def predict_mental_health_risk(data: BehavioralData = None):
    """
    Predict mental health risk based on behavioral data.
    
    If no data is provided, uses the latest stored entry.
    Returns risk score (0-1), risk level, and intervention suggestion.
    """
    if data is None:
        # Use latest stored entry
        latest = repository.get_latest(1)
        if not latest:
            raise HTTPException(
                status_code=400,
                detail="No data available. Please submit behavioral data first."
            )
        data = latest[0]
    
    risk_score, risk_level, suggestion = predict_risk(data)
    
    return RiskPrediction(
        risk_score=round(risk_score, 2),
        risk_level=risk_level,
        intervention_suggestion=suggestion
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
