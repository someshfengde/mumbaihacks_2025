"""Risk scoring logic for MindGuard."""
from typing import List, Optional, Tuple


def calculate_risk_score(
    sleep_hours: float,
    mood_score: int,
    messages_sent: int,
    steps: int,
    app_usage_hours: float
) -> Tuple[float, str, str, str, List[str], List[str]]:
    """Calculate risk score and provide insight drivers and remedies."""
    risk = 0.0
    drivers: List[str] = []
    actions: List[str] = []

    def flag(condition: bool, delta: float, driver: str, action: Optional[str] = None):
        nonlocal risk
        if condition:
            risk += delta
            drivers.append(f"{driver} (+{delta:.2f})")
            if action:
                actions.append(action)

    # Sleep factor
    flag(
        sleep_hours < 4,
        0.3,
        "Severely low sleep",
        "Block 30 minutes for deep rest tonight",
    )
    flag(
        4 <= sleep_hours < 6,
        0.15,
        "Not enough restorative sleep",
        "Wind down 30 minutes earlier to aim for 6+ hours",
    )

    # Mood factor (most important)
    flag(
        mood_score <= 3,
        0.4,
        "Mood is critically low",
        "Reach out to someone you trust and share how you feel",
    )
    flag(
        3 < mood_score <= 5,
        0.2,
        "Mood trending downward",
        "Do a short grounding exercise or journaling session",
    )

    # Social activity factor
    flag(
        messages_sent < 3,
        0.15,
        "Limited social touchpoints",
        "Send a quick check-in message to a friend",
    )

    # Physical activity factor
    flag(
        steps < 1000,
        0.1,
        "Low movement",
        "Take a 5-minute walk or stretch break",
    )

    # Late-night usage factor
    flag(
        app_usage_hours > 6,
        0.1,
        "Heavy screen time",
        "Try a mini digital detox for one hour",
    )

    # Cap risk at 1.0
    risk = min(risk, 1.0)

    if not drivers:
        drivers.append("Balanced day – no major red flags detected.")
    if not actions:
        actions.append("Keep reinforcing the routines that made today feel balanced.")

    # Determine risk level and suggestion
    if risk >= 0.7:
        return (
            round(risk, 2),
            "high",
            "Please consider reaching out to a trusted friend or counselor today. Your wellbeing matters. 💙",
            "#FF6B6B",
            drivers,
            actions,
        )
    if risk >= 0.4:
        return (
            round(risk, 2),
            "medium",
            "Try a short walk or a quick breathing exercise. Small steps make a difference. 🌿",
            "#FFE66D",
            drivers,
            actions,
        )
    return (
        round(risk, 2),
        "low",
        "You're doing great! Keep up the healthy habits. ✨",
        "#4ECDC4",
        drivers,
        actions,
    )
