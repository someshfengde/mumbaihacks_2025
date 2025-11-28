"""OpenAI-powered emotion analysis utilities."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

try:  # Optional dependency so the backend can fall back gracefully.
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover - handled at runtime when package is absent
    OpenAI = None  # type: ignore


@dataclass
class EmotionResult:
    """Structured emotion analysis result."""

    primary_emotion: str
    confidence: float
    supporting_emotions: List[str]
    stress_level: str
    summary: str
    recommendation: str

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-serializable dict."""
        return {
            "primary_emotion": self.primary_emotion,
            "confidence": round(self.confidence, 2),
            "supporting_emotions": self.supporting_emotions,
            "stress_level": self.stress_level,
            "summary": self.summary,
            "recommendation": self.recommendation,
        }


def _build_client() -> Optional["OpenAI"]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    return OpenAI(api_key=api_key)


def analyze_emotions(text: str) -> EmotionResult:
    """Analyze emotions using OpenAI when available, else fall back to heuristics."""
    client = _build_client()
    if client:
        try:
            prompt = _build_prompt(text)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                input=prompt,
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            content = response.output[0].content[0].text  # type: ignore[index]
            payload = json.loads(content)
            return EmotionResult(
                primary_emotion=payload.get("primary_emotion", "calm"),
                confidence=float(payload.get("confidence", 0.65)),
                supporting_emotions=payload.get("supporting_emotions", []),
                stress_level=payload.get("stress_level", "low"),
                summary=payload.get(
                    "summary",
                    "You appear balanced with no alarming emotional spikes.",
                ),
                recommendation=payload.get(
                    "recommendation",
                    "Keep reflecting on your feelings and share them with a friend.",
                ),
            )
        except Exception:
            # Fall back silently if API errors out; heuristics will still provide value.
            pass

    return _fallback_emotion_analysis(text)


def _build_prompt(text: str) -> str:
    return (
        "You are an empathetic mental health co-pilot. "
        "Given the reflection below, classify the dominant and secondary emotions, estimate stress level (low, medium, high), "
        "and propose one human-first coping recommendation. Respond strictly as JSON with keys: "
        "primary_emotion (string), confidence (0-1 float), supporting_emotions (array of strings), stress_level (string), "
        "summary (string), recommendation (string). Reflection:\n\n" + text.strip()
    )


_NEGATIVE_WORDS = {
    "anxious": "anxiety",
    "scared": "fear",
    "afraid": "fear",
    "tired": "fatigue",
    "exhausted": "fatigue",
    "sad": "sadness",
    "depressed": "sadness",
    "lonely": "loneliness",
    "stress": "stress",
    "angry": "anger",
}
_POSITIVE_WORDS = {
    "grateful": "gratitude",
    "happy": "joy",
    "excited": "excitement",
    "calm": "calm",
    "peaceful": "calm",
}
_STRESS_SIGNALS = ["deadline", "pressure", "overwhelmed", "panic", "worry", "urgent"]


def _fallback_emotion_analysis(text: str) -> EmotionResult:
    """Lightweight deterministic sentiment/emotion heuristic."""
    lowered = text.lower()
    counts: Dict[str, int] = {}

    for token, label in _NEGATIVE_WORDS.items():
        if token in lowered:
            counts[label] = counts.get(label, 0) + 1

    for token, label in _POSITIVE_WORDS.items():
        if token in lowered:
            counts[label] = counts.get(label, 0) + 1

    if not counts:
        primary = "calm"
        supporting: List[str] = []
        confidence = 0.55
    else:
        primary = max(counts, key=counts.get)
        supporting = [k for k in counts if k != primary]
        total = sum(counts.values())
        confidence = min(0.9, counts[primary] / total)

    stress_hits = sum(1 for signal in _STRESS_SIGNALS if signal in lowered)
    stress_level = "high" if stress_hits >= 2 else ("medium" if stress_hits == 1 else "low")

    summary = _build_summary(primary, stress_level)
    recommendation = _build_recommendation(primary, stress_level)

    return EmotionResult(
        primary_emotion=primary,
        confidence=confidence,
        supporting_emotions=supporting,
        stress_level=stress_level,
        summary=summary,
        recommendation=recommendation,
    )


def _build_summary(primary: str, stress_level: str) -> str:
    return (
        f"Your journal shows dominant {primary} tones with {stress_level} stress."
    )


def _build_recommendation(primary: str, stress_level: str) -> str:
    if stress_level == "high":
        return "Pause for deep breathing and reach out to a trusted person today."
    if stress_level == "medium":
        return "Schedule a short restorative activity and share your feelings with someone you trust."
    if primary in {"gratitude", "joy", "calm"}:
        return "Keep reinforcing these positive habits and note what sparked them."
    return "Take a mindful break and practice gentle movement or journaling."
