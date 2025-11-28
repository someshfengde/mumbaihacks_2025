"""Risk scoring logic for MindGuard."""
from typing import Tuple


def calculate_risk_score(
    sleep_hours: float,
    mood_score: int,
    messages_sent: int,
    steps: int,
    app_usage_hours: float
) -> Tuple[float, str, str, str]:
    """
    Calculate risk score based on behavioral data.
    
    Returns:
        Tuple of (risk_score, risk_level, suggestion, color)
    """
    risk = 0.0
    
    # Sleep factor
    if sleep_hours < 4:
        risk += 0.3
    elif sleep_hours < 6:
        risk += 0.15
    
    # Mood factor (most important)
    if mood_score <= 3:
        risk += 0.4
    elif mood_score <= 5:
        risk += 0.2
    
    # Social activity factor
    if messages_sent < 3:
        risk += 0.15
    
    # Physical activity factor
    if steps < 1000:
        risk += 0.1
    
    # Late-night usage factor
    if app_usage_hours > 6:
        risk += 0.1
    
    # Cap risk at 1.0
    risk = min(risk, 1.0)
    
    # Determine risk level and suggestion
    if risk >= 0.7:
        return (
            round(risk, 2),
            "high",
            "Please consider reaching out to a trusted friend or counselor today. Your wellbeing matters. 💙",
            "#FF6B6B"
        )
    elif risk >= 0.4:
        return (
            round(risk, 2),
            "medium",
            "Try a short walk or a quick breathing exercise. Small steps make a difference. 🌿",
            "#FFE66D"
        )
    else:
        return (
            round(risk, 2),
            "low",
            "You're doing great! Keep up the healthy habits. ✨",
            "#4ECDC4"
        )
