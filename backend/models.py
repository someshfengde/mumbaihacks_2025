"""Pydantic models for MindGuard API."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BehavioralData(BaseModel):
    """Input model for behavioral data."""
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours of sleep")
    mood_score: int = Field(..., ge=1, le=10, description="Mood score from 1-10")
    messages_sent: int = Field(..., ge=0, description="Number of messages sent")
    steps: int = Field(..., ge=0, description="Number of steps taken")
    app_usage_hours: float = Field(..., ge=0, le=24, description="Hours of app usage")
    timestamp: Optional[datetime] = None


class RiskPrediction(BaseModel):
    """Output model for risk prediction."""
    risk_score: float = Field(..., ge=0, le=1, description="Risk score from 0 to 1")
    risk_level: str = Field(..., description="Risk level: low, medium, or high")
    suggestion: str = Field(..., description="Intervention suggestion")
    color: str = Field(..., description="Color code for the risk level")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
