"""API client for communicating with MindGuard backend."""

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class BehavioralData:
    """Data class for behavioral data."""
    sleep_hours: float
    mood_score: int
    messages_sent: int
    steps: int
    app_usage_hours: float


@dataclass
class RiskPrediction:
    """Data class for risk prediction."""
    risk_score: float
    risk_level: str
    intervention_suggestion: str


class APIClient:
    """Client for MindGuard API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
    
    def health_check(self) -> bool:
        """Check if the API is healthy."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200 and response.json().get("status") == "ok"
        except requests.RequestException:
            return False
    
    def submit_data(self, data: BehavioralData) -> Optional[Dict]:
        """Submit behavioral data to the API."""
        try:
            payload = {
                "sleep_hours": data.sleep_hours,
                "mood_score": data.mood_score,
                "messages_sent": data.messages_sent,
                "steps": data.steps,
                "app_usage_hours": data.app_usage_hours
            }
            response = requests.post(
                f"{self.base_url}/data",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error submitting data: {e}")
            return None
    
    def get_all_data(self) -> List[Dict]:
        """Get all behavioral data from the API."""
        try:
            response = requests.get(f"{self.base_url}/data", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting data: {e}")
            return []
    
    def get_latest_data(self, n: int = 7) -> List[Dict]:
        """Get the latest n data entries from the API."""
        try:
            response = requests.get(
                f"{self.base_url}/data/latest",
                params={"n": n},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting latest data: {e}")
            return []
    
    def predict_risk(self, data: Optional[BehavioralData] = None) -> Optional[RiskPrediction]:
        """Get risk prediction from the API."""
        try:
            if data:
                payload = {
                    "sleep_hours": data.sleep_hours,
                    "mood_score": data.mood_score,
                    "messages_sent": data.messages_sent,
                    "steps": data.steps,
                    "app_usage_hours": data.app_usage_hours
                }
                response = requests.post(
                    f"{self.base_url}/predict",
                    json=payload,
                    timeout=10
                )
            else:
                response = requests.post(
                    f"{self.base_url}/predict",
                    timeout=10
                )
            response.raise_for_status()
            result = response.json()
            return RiskPrediction(
                risk_score=result["risk_score"],
                risk_level=result["risk_level"],
                intervention_suggestion=result["intervention_suggestion"]
            )
        except requests.RequestException as e:
            print(f"Error getting prediction: {e}")
            return None
