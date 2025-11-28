"""In-memory repository for behavioral data."""

from datetime import datetime, timezone
from typing import List, Optional
from .models import BehavioralData, BehavioralDataResponse


class BehavioralDataRepository:
    """In-memory storage for behavioral data entries."""
    
    def __init__(self):
        self._data: List[BehavioralDataResponse] = []
        self._next_id: int = 1
    
    def add(self, data: BehavioralData) -> BehavioralDataResponse:
        """Add a new behavioral data entry."""
        entry = BehavioralDataResponse(
            id=self._next_id,
            sleep_hours=data.sleep_hours,
            mood_score=data.mood_score,
            messages_sent=data.messages_sent,
            steps=data.steps,
            app_usage_hours=data.app_usage_hours,
            timestamp=data.timestamp or datetime.now(timezone.utc)
        )
        self._data.append(entry)
        self._next_id += 1
        return entry
    
    def get_all(self) -> List[BehavioralDataResponse]:
        """Get all behavioral data entries."""
        return self._data.copy()
    
    def get_latest(self, n: int = 7) -> List[BehavioralDataResponse]:
        """Get the latest n entries."""
        return self._data[-n:] if self._data else []
    
    def get_by_id(self, entry_id: int) -> Optional[BehavioralDataResponse]:
        """Get entry by ID."""
        for entry in self._data:
            if entry.id == entry_id:
                return entry
        return None
    
    def clear(self):
        """Clear all data (useful for testing)."""
        self._data.clear()
        self._next_id = 1


# Global repository instance
repository = BehavioralDataRepository()
