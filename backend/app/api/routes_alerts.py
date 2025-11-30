from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional
from app.db.session import get_session
from app.schemas.alert import FrontendAlertResponse, AlertFilter
from app.services.alerts import get_filtered_alerts_with_reports

router = APIRouter()


@router.get("/alerts", response_model=List[FrontendAlertResponse])
async def get_alerts(
        type: Optional[str] = Query(None, description="Filter by disaster type"),
        min_severity: Optional[int] = Query(None, ge=0, le=100, description="Minimum severity score"),
        limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of results"),
        active_only: bool = Query(True, description="Show only active alerts"),
        session: Session = Depends(get_session)
):
    """Get alerts with proper frontend-compatible format"""
    alert_filter = AlertFilter(
        type=type,
        min_severity=min_severity,
        limit=limit,
        active_only=active_only
    )

    alerts = get_filtered_alerts_with_reports(session, alert_filter)
    return alerts