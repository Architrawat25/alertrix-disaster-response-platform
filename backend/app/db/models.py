from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class DisasterType(str, Enum):
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"
    FIRE = "fire"
    STORM = "storm"
    OTHER = "other"

class Report(SQLModel, table=True):
    """Report model for disaster reports"""
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    lat: float
    lon: float
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Alert(SQLModel, table=True):
    """Alert model for disaster alerts"""
    id: Optional[int] = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    disaster_type: DisasterType = Field(default=DisasterType.OTHER)
    severity_score: int = Field(default=0, ge=0, le=100)
    summary: str
    location_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)