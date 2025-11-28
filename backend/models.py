"""Pydantic models for MindGuard API."""
from pydantic import BaseModel, Field
from typing import Optional, List
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
    drivers: List[str] = Field(default_factory=list, description="Factors contributing to the risk")
    recommended_actions: List[str] = Field(default_factory=list, description="Actionable next steps")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"


class JournalEntry(BaseModel):
    """Free-form journal text submitted by the user."""
    text: str = Field(..., min_length=10, max_length=2000, description="Reflection or journal text")


class EmotionAnalysis(BaseModel):
    """Emotion analysis output."""
    primary_emotion: str = Field(..., description="Dominant emotion label")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score for the primary emotion")
    supporting_emotions: List[str] = Field(default_factory=list, description="Secondary emotions detected")
    stress_level: str = Field(..., description="Low/medium/high stress classification")
    summary: str = Field(..., description="Short natural language summary")
    recommendation: str = Field(..., description="Actionable coaching advice")
