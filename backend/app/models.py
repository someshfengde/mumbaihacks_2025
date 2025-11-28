"""Pydantic models for MindGuard MVP."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BehavioralData(BaseModel):
    """Input model for behavioral data entry."""
    
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours of sleep (0-24)")
    mood_score: int = Field(..., ge=1, le=10, description="Mood score (1-10)")
    messages_sent: int = Field(..., ge=0, description="Number of messages sent")
    steps: int = Field(..., ge=0, description="Number of steps walked")
    app_usage_hours: float = Field(..., ge=0, le=24, description="App usage time in hours")
    timestamp: Optional[datetime] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "sleep_hours": 6.5,
                "mood_score": 7,
                "messages_sent": 25,
                "steps": 5000,
                "app_usage_hours": 3.0
            }
        }
    }


class BehavioralDataResponse(BehavioralData):
    """Response model for behavioral data with ID and timestamp."""
    
    id: int
    timestamp: datetime


class RiskPrediction(BaseModel):
    """Response model for risk prediction."""
    
    risk_score: float = Field(..., ge=0, le=1, description="Risk score (0-1)")
    risk_level: str = Field(..., description="Risk level (low, medium, high)")
    intervention_suggestion: str = Field(..., description="Suggested intervention")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "risk_score": 0.3,
                "risk_level": "low",
                "intervention_suggestion": "Keep up the good work! Stay connected with friends."
            }
        }
    }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = "ok"
