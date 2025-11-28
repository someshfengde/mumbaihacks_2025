"""Tests for the repository module."""

import pytest
from datetime import datetime
from app.models import BehavioralData
from app.repository import BehavioralDataRepository


@pytest.fixture
def repository():
    """Create a fresh repository for each test."""
    repo = BehavioralDataRepository()
    yield repo
    repo.clear()


@pytest.fixture
def sample_data():
    """Sample behavioral data for testing."""
    return BehavioralData(
        sleep_hours=7.5,
        mood_score=7,
        messages_sent=20,
        steps=6000,
        app_usage_hours=3.5
    )


class TestBehavioralDataRepository:
    """Tests for BehavioralDataRepository class."""
    
    def test_add_returns_response_with_id(self, repository, sample_data):
        """Test that adding data returns response with ID."""
        result = repository.add(sample_data)
        assert result.id == 1
        assert result.sleep_hours == sample_data.sleep_hours
        assert result.mood_score == sample_data.mood_score
    
    def test_add_increments_id(self, repository, sample_data):
        """Test that IDs increment correctly."""
        result1 = repository.add(sample_data)
        result2 = repository.add(sample_data)
        assert result1.id == 1
        assert result2.id == 2
    
    def test_add_sets_timestamp(self, repository, sample_data):
        """Test that timestamp is set when adding data."""
        result = repository.add(sample_data)
        assert result.timestamp is not None
        assert isinstance(result.timestamp, datetime)
    
    def test_get_all_returns_empty_initially(self, repository):
        """Test that get_all returns empty list initially."""
        result = repository.get_all()
        assert result == []
    
    def test_get_all_returns_all_entries(self, repository, sample_data):
        """Test that get_all returns all added entries."""
        repository.add(sample_data)
        repository.add(sample_data)
        repository.add(sample_data)
        result = repository.get_all()
        assert len(result) == 3
    
    def test_get_latest_returns_n_entries(self, repository, sample_data):
        """Test that get_latest returns correct number of entries."""
        for _ in range(10):
            repository.add(sample_data)
        result = repository.get_latest(5)
        assert len(result) == 5
    
    def test_get_latest_returns_most_recent(self, repository):
        """Test that get_latest returns most recent entries."""
        for i in range(10):
            data = BehavioralData(
                sleep_hours=i,
                mood_score=5,
                messages_sent=10,
                steps=5000,
                app_usage_hours=2
            )
            repository.add(data)
        
        result = repository.get_latest(3)
        assert result[0].sleep_hours == 7
        assert result[1].sleep_hours == 8
        assert result[2].sleep_hours == 9
    
    def test_get_by_id_returns_correct_entry(self, repository, sample_data):
        """Test that get_by_id returns the correct entry."""
        entry = repository.add(sample_data)
        result = repository.get_by_id(entry.id)
        assert result is not None
        assert result.id == entry.id
    
    def test_get_by_id_returns_none_for_missing(self, repository):
        """Test that get_by_id returns None for non-existent ID."""
        result = repository.get_by_id(999)
        assert result is None
    
    def test_clear_removes_all_data(self, repository, sample_data):
        """Test that clear removes all data."""
        repository.add(sample_data)
        repository.add(sample_data)
        repository.clear()
        assert repository.get_all() == []
    
    def test_clear_resets_id_counter(self, repository, sample_data):
        """Test that clear resets the ID counter."""
        repository.add(sample_data)
        repository.add(sample_data)
        repository.clear()
        new_entry = repository.add(sample_data)
        assert new_entry.id == 1
