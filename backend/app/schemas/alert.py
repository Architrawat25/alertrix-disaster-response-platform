from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.db.models import DisasterType

class AlertResponse(BaseModel):
    """Schema for alert response - original backend format"""
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

class FrontendAlertResponse(BaseModel):
    """Schema that matches frontend Alert interface"""
    id: int
    alert_type: str  # Map from disaster_type
    summary: str
    location: str    # Map from location_name
    lat: float       # Need to get from associated report
    lon: float       # Need to get from associated report
    severity: int    # Map from severity_score
    timestamp: str   # Map from created_at
    source: str      # Need to get from associated report

    class Config:
        from_attributes = True

class AlertFilter(BaseModel):
    """Schema for alert filtering"""
    type: Optional[str] = None
    min_severity: Optional[int] = None
    limit: Optional[int] = None
    active_only: Optional[bool] = True