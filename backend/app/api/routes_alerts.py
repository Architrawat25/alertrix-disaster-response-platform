from fastapi import APIRouter
from app.schemas.alert import AlertResponse
from typing import List

router = APIRouter()

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts():
    """Get mock alerts - will be connected to DB in Phase 3"""
    return [
        {
            "id": 1,
            "report_id": 1,
            "disaster_type": "flood",
            "severity_score": 75,
            "summary": "Heavy flooding in downtown area",
            "location_name": "Downtown City",
            "created_at": "2024-01-15T10:30:00"
        },
        {
            "id": 2,
            "report_id": 2,
            "disaster_type": "earthquake",
            "severity_score": 90,
            "summary": "Magnitude 6.5 earthquake reported",
            "location_name": "Mountain Region",
            "created_at": "2024-01-15T11:00:00"
        }
    ]