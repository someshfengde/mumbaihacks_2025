"""Tests for the API client module."""

import pytest
import requests
from unittest.mock import Mock, patch
from app.api_client import APIClient, BehavioralData, RiskPrediction


@pytest.fixture
def client():
    """Create an API client for testing."""
    return APIClient("http://localhost:8000")


@pytest.fixture
def sample_data():
    """Create sample behavioral data for testing."""
    return BehavioralData(
        sleep_hours=7.5,
        mood_score=7,
        messages_sent=20,
        steps=6000,
        app_usage_hours=3.5
    )


class TestAPIClient:
    """Tests for APIClient class."""
    
    def test_init_default_url(self):
        """Test default URL is set correctly."""
        client = APIClient()
        assert client.base_url == "http://localhost:8000"
    
    def test_init_custom_url(self):
        """Test custom URL is set correctly."""
        client = APIClient("http://custom:3000/")
        assert client.base_url == "http://custom:3000"
    
    @patch('app.api_client.requests.get')
    def test_health_check_success(self, mock_get, client):
        """Test health check returns True when API is healthy."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_get.return_value = mock_response
        
        assert client.health_check() is True
        mock_get.assert_called_once_with(
            "http://localhost:8000/health",
            timeout=5
        )
    
    @patch('app.api_client.requests.get')
    def test_health_check_failure(self, mock_get, client):
        """Test health check returns False when API is down."""
        mock_get.side_effect = requests.RequestException("Connection error")
        
        assert client.health_check() is False
    
    @patch('app.api_client.requests.post')
    def test_submit_data_success(self, mock_post, client, sample_data):
        """Test successful data submission."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "sleep_hours": 7.5,
            "mood_score": 7,
            "messages_sent": 20,
            "steps": 6000,
            "app_usage_hours": 3.5,
            "timestamp": "2024-01-01T12:00:00"
        }
        mock_post.return_value = mock_response
        
        result = client.submit_data(sample_data)
        
        assert result is not None
        assert result["id"] == 1
        mock_post.assert_called_once()
    
    @patch('app.api_client.requests.post')
    def test_submit_data_failure(self, mock_post, client, sample_data):
        """Test data submission failure returns None."""
        mock_post.side_effect = requests.RequestException("Connection error")
        
        result = client.submit_data(sample_data)
        assert result is None
    
    @patch('app.api_client.requests.get')
    def test_get_all_data_success(self, mock_get, client):
        """Test getting all data successfully."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "sleep_hours": 7},
            {"id": 2, "sleep_hours": 8}
        ]
        mock_get.return_value = mock_response
        
        result = client.get_all_data()
        
        assert len(result) == 2
        assert result[0]["id"] == 1
    
    @patch('app.api_client.requests.get')
    def test_get_all_data_failure(self, mock_get, client):
        """Test get all data returns empty list on failure."""
        mock_get.side_effect = requests.RequestException("Connection error")
        
        result = client.get_all_data()
        assert result == []
    
    @patch('app.api_client.requests.get')
    def test_get_latest_data_success(self, mock_get, client):
        """Test getting latest data successfully."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 5, "sleep_hours": 7},
            {"id": 6, "sleep_hours": 8}
        ]
        mock_get.return_value = mock_response
        
        result = client.get_latest_data(2)
        
        assert len(result) == 2
        mock_get.assert_called_once_with(
            "http://localhost:8000/data/latest",
            params={"n": 2},
            timeout=10
        )
    
    @patch('app.api_client.requests.post')
    def test_predict_risk_with_data(self, mock_post, client, sample_data):
        """Test risk prediction with provided data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "risk_score": 0.25,
            "risk_level": "low",
            "intervention_suggestion": "Keep up the good work!"
        }
        mock_post.return_value = mock_response
        
        result = client.predict_risk(sample_data)
        
        assert result is not None
        assert isinstance(result, RiskPrediction)
        assert result.risk_score == 0.25
        assert result.risk_level == "low"
    
    @patch('app.api_client.requests.post')
    def test_predict_risk_without_data(self, mock_post, client):
        """Test risk prediction without provided data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "risk_score": 0.5,
            "risk_level": "medium",
            "intervention_suggestion": "Take a break."
        }
        mock_post.return_value = mock_response
        
        result = client.predict_risk()
        
        assert result is not None
        assert result.risk_level == "medium"
    
    @patch('app.api_client.requests.post')
    def test_predict_risk_failure(self, mock_post, client, sample_data):
        """Test risk prediction returns None on failure."""
        mock_post.side_effect = requests.RequestException("Connection error")
        
        result = client.predict_risk(sample_data)
        assert result is None


class TestBehavioralData:
    """Tests for BehavioralData dataclass."""
    
    def test_create_behavioral_data(self):
        """Test creating behavioral data."""
        data = BehavioralData(
            sleep_hours=8.0,
            mood_score=8,
            messages_sent=25,
            steps=7000,
            app_usage_hours=2.0
        )
        assert data.sleep_hours == 8.0
        assert data.mood_score == 8
        assert data.messages_sent == 25
        assert data.steps == 7000
        assert data.app_usage_hours == 2.0


class TestRiskPrediction:
    """Tests for RiskPrediction dataclass."""
    
    def test_create_risk_prediction(self):
        """Test creating risk prediction."""
        pred = RiskPrediction(
            risk_score=0.5,
            risk_level="medium",
            intervention_suggestion="Take a walk"
        )
        assert pred.risk_score == 0.5
        assert pred.risk_level == "medium"
        assert pred.intervention_suggestion == "Take a walk"
