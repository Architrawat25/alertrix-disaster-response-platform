from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.db.models import DisasterType

class AlertResponse(BaseModel):
    """Schema for alert response"""
    id: int
    report_id: int
    disaster_type: DisasterType
    severity_score: int
    summary: str
    location_name: str
    created_at: datetime

    class Config:
        from_attributes = True