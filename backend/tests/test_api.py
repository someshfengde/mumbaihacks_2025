"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repository import repository


@pytest.fixture
def client():
    """Create a test client and clear repository before each test."""
    repository.clear()
    with TestClient(app) as client:
        yield client
    repository.clear()


@pytest.fixture
def sample_data():
    """Sample behavioral data for testing."""
    return {
        "sleep_hours": 7.5,
        "mood_score": 7,
        "messages_sent": 20,
        "steps": 6000,
        "app_usage_hours": 3.5
    }


class TestHealthEndpoint:
    """Tests for /health endpoint."""
    
    def test_health_returns_ok(self, client):
        """Test that health endpoint returns ok status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestDataEndpoints:
    """Tests for /data endpoints."""
    
    def test_post_data_success(self, client, sample_data):
        """Test successful data submission."""
        response = client.post("/data", json=sample_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["sleep_hours"] == sample_data["sleep_hours"]
        assert data["mood_score"] == sample_data["mood_score"]
        assert "timestamp" in data
    
    def test_post_data_validation_error(self, client):
        """Test data validation errors."""
        invalid_data = {
            "sleep_hours": 30,  # Invalid: > 24
            "mood_score": 7,
            "messages_sent": 20,
            "steps": 6000,
            "app_usage_hours": 3.5
        }
        response = client.post("/data", json=invalid_data)
        assert response.status_code == 422
    
    def test_get_data_empty(self, client):
        """Test getting data when empty."""
        response = client.get("/data")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_data_returns_all(self, client, sample_data):
        """Test that get returns all submitted data."""
        client.post("/data", json=sample_data)
        client.post("/data", json=sample_data)
        
        response = client.get("/data")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_latest_data(self, client, sample_data):
        """Test getting latest n entries."""
        for _ in range(10):
            client.post("/data", json=sample_data)
        
        response = client.get("/data/latest?n=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3


class TestPredictEndpoint:
    """Tests for /predict endpoint."""
    
    def test_predict_with_provided_data(self, client, sample_data):
        """Test prediction with provided data."""
        response = client.post("/predict", json=sample_data)
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert "risk_level" in data
        assert "intervention_suggestion" in data
        assert 0 <= data["risk_score"] <= 1
        assert data["risk_level"] in ["low", "medium", "high"]
    
    def test_predict_high_risk(self, client):
        """Test prediction with high risk data."""
        high_risk_data = {
            "sleep_hours": 2,
            "mood_score": 2,
            "messages_sent": 1,
            "steps": 200,
            "app_usage_hours": 12
        }
        response = client.post("/predict", json=high_risk_data)
        assert response.status_code == 200
        data = response.json()
        assert data["risk_level"] == "high"
        assert data["risk_score"] >= 0.6
    
    def test_predict_low_risk(self, client):
        """Test prediction with low risk data."""
        low_risk_data = {
            "sleep_hours": 8,
            "mood_score": 9,
            "messages_sent": 30,
            "steps": 10000,
            "app_usage_hours": 1
        }
        response = client.post("/predict", json=low_risk_data)
        assert response.status_code == 200
        data = response.json()
        assert data["risk_level"] == "low"
        assert data["risk_score"] < 0.3
