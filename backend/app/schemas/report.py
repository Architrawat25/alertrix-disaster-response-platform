from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportCreate(BaseModel):
    """Schema for creating a report"""
    text: str
    lat: float
    lon: float
    source: str

class ReportResponse(BaseModel):
    """Schema for report response"""
    id: int
    text: str
    lat: float
    lon: float
    source: str
    created_at: datetime
    is_analyzed: bool

    class Config:
        from_attributes = True

class AnalyzeRequest(BaseModel):
    """Schema for analyze request"""
    report_id: int

class ReportStatusResponse(BaseModel):
    """Schema for report status response"""
    status: str
    report: ReportResponse
    message: str