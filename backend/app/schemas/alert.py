from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AlertResponse(BaseModel):
    """Schema for alert response"""
    id: int
    report_id: int
    disaster_type: str
    severity_score: int
    summary: str
    location_name: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class AlertFilter(BaseModel):
    """Schema for alert filtering"""
    type: Optional[str] = None
    min_severity: Optional[int] = None
    limit: Optional[int] = None
    active_only: Optional[bool] = True