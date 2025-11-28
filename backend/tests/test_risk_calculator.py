"""Tests for risk calculator module."""

import pytest
from app.models import BehavioralData
from app.risk_calculator import (
    calculate_risk_score,
    get_risk_level,
    get_intervention_suggestion,
    predict_risk
)


class TestCalculateRiskScore:
    """Tests for calculate_risk_score function."""
    
    def test_low_risk_good_data(self):
        """Test that good behavioral data results in low risk."""
        data = BehavioralData(
            sleep_hours=8,
            mood_score=8,
            messages_sent=20,
            steps=8000,
            app_usage_hours=2
        )
        risk = calculate_risk_score(data)
        assert 0 <= risk < 0.3
    
    def test_high_risk_poor_sleep(self):
        """Test that very poor sleep increases risk."""
        data = BehavioralData(
            sleep_hours=2,
            mood_score=7,
            messages_sent=20,
            steps=5000,
            app_usage_hours=2
        )
        risk = calculate_risk_score(data)
        assert risk >= 0.3
    
    def test_high_risk_low_mood(self):
        """Test that low mood significantly increases risk."""
        data = BehavioralData(
            sleep_hours=8,
            mood_score=2,
            messages_sent=20,
            steps=5000,
            app_usage_hours=2
        )
        risk = calculate_risk_score(data)
        assert risk >= 0.4
    
    def test_high_risk_low_social(self):
        """Test that low social activity increases risk."""
        data = BehavioralData(
            sleep_hours=8,
            mood_score=7,
            messages_sent=2,
            steps=5000,
            app_usage_hours=2
        )
        risk = calculate_risk_score(data)
        assert risk >= 0.2
    
    def test_high_risk_combined_factors(self):
        """Test high risk with multiple poor factors."""
        data = BehavioralData(
            sleep_hours=3,
            mood_score=2,
            messages_sent=1,
            steps=300,
            app_usage_hours=10
        )
        risk = calculate_risk_score(data)
        assert risk >= 0.8
    
    def test_risk_clamped_to_one(self):
        """Test that risk score is clamped to maximum of 1."""
        data = BehavioralData(
            sleep_hours=0,
            mood_score=1,
            messages_sent=0,
            steps=0,
            app_usage_hours=24
        )
        risk = calculate_risk_score(data)
        assert risk == 1.0


class TestGetRiskLevel:
    """Tests for get_risk_level function."""
    
    def test_low_risk_level(self):
        assert get_risk_level(0.0) == "low"
        assert get_risk_level(0.1) == "low"
        assert get_risk_level(0.29) == "low"
    
    def test_medium_risk_level(self):
        assert get_risk_level(0.3) == "medium"
        assert get_risk_level(0.45) == "medium"
        assert get_risk_level(0.59) == "medium"
    
    def test_high_risk_level(self):
        assert get_risk_level(0.6) == "high"
        assert get_risk_level(0.8) == "high"
        assert get_risk_level(1.0) == "high"


class TestGetInterventionSuggestion:
    """Tests for get_intervention_suggestion function."""
    
    def test_returns_string(self):
        for level in ["low", "medium", "high"]:
            suggestion = get_intervention_suggestion(level)
            assert isinstance(suggestion, str)
            assert len(suggestion) > 0
    
    def test_unknown_level_returns_medium(self):
        suggestion = get_intervention_suggestion("unknown")
        assert isinstance(suggestion, str)


class TestPredictRisk:
    """Tests for predict_risk function."""
    
    def test_returns_tuple(self):
        data = BehavioralData(
            sleep_hours=7,
            mood_score=6,
            messages_sent=15,
            steps=5000,
            app_usage_hours=4
        )
        result = predict_risk(data)
        assert isinstance(result, tuple)
        assert len(result) == 3
    
    def test_returns_correct_types(self):
        data = BehavioralData(
            sleep_hours=7,
            mood_score=6,
            messages_sent=15,
            steps=5000,
            app_usage_hours=4
        )
        risk_score, risk_level, suggestion = predict_risk(data)
        assert isinstance(risk_score, float)
        assert isinstance(risk_level, str)
        assert isinstance(suggestion, str)
        assert 0 <= risk_score <= 1
        assert risk_level in ["low", "medium", "high"]
