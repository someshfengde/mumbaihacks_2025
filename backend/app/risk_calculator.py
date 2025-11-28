"""Risk score calculation logic for MindGuard MVP."""

from typing import Tuple
from .models import BehavioralData


# Intervention suggestions based on risk level
INTERVENTIONS = {
    "low": [
        "Keep up the good work! Stay connected with friends.",
        "Great job maintaining your routine!",
        "Continue your healthy habits."
    ],
    "medium": [
        "Consider taking a short walk today.",
        "Try a 5-minute breathing exercise.",
        "Reach out to a friend or family member.",
        "Take a break from screens for 30 minutes."
    ],
    "high": [
        "Please talk to a trusted friend or family member today.",
        "Consider contacting a counselor or mental health professional.",
        "Call a mental health helpline if you're feeling overwhelmed.",
        "Reach out to someone you trust - you don't have to face this alone."
    ]
}


def calculate_risk_score(data: BehavioralData) -> float:
    """
    Calculate risk score based on behavioral data.
    
    Risk factors:
    - Less than 4 hours sleep → +0.3 risk
    - Mood ≤ 3 → +0.4 risk
    - Social activity (messages) extremely low (<5) → +0.2
    - High app usage (>8 hours) → +0.1
    - Low movement (<1000 steps) → +0.1
    
    Returns:
        Risk score between 0 and 1
    """
    risk = 0.0
    
    # Sleep factor
    if data.sleep_hours < 4:
        risk += 0.3
    elif data.sleep_hours < 6:
        risk += 0.15
    
    # Mood factor (most important)
    if data.mood_score <= 3:
        risk += 0.4
    elif data.mood_score <= 5:
        risk += 0.2
    
    # Social activity factor
    if data.messages_sent < 5:
        risk += 0.2
    elif data.messages_sent < 10:
        risk += 0.1
    
    # Screen time factor
    if data.app_usage_hours > 8:
        risk += 0.1
    elif data.app_usage_hours > 6:
        risk += 0.05
    
    # Movement factor
    if data.steps < 1000:
        risk += 0.1
    elif data.steps < 3000:
        risk += 0.05
    
    # Clamp to [0, 1]
    return min(max(risk, 0.0), 1.0)


def get_risk_level(risk_score: float) -> str:
    """
    Determine risk level from risk score.
    
    Returns:
        'low', 'medium', or 'high'
    """
    if risk_score < 0.3:
        return "low"
    elif risk_score < 0.6:
        return "medium"
    else:
        return "high"


def get_intervention_suggestion(risk_level: str) -> str:
    """
    Get an intervention suggestion based on risk level.
    
    Returns:
        A suggestion string appropriate for the risk level.
    """
    import random
    suggestions = INTERVENTIONS.get(risk_level, INTERVENTIONS["medium"])
    return random.choice(suggestions)


def predict_risk(data: BehavioralData) -> Tuple[float, str, str]:
    """
    Main prediction function that combines all risk assessment.
    
    Returns:
        Tuple of (risk_score, risk_level, intervention_suggestion)
    """
    risk_score = calculate_risk_score(data)
    risk_level = get_risk_level(risk_score)
    suggestion = get_intervention_suggestion(risk_level)
    return risk_score, risk_level, suggestion
