from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.db.models import Report, Alert
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check(session: Session = Depends(get_session)):
    """Enhanced health check with service status"""
    try:
        # Test database connection
        report_count = session.query(Report).count()
        alert_count = session.query(Alert).count()

        return {
            "status": "ok",
            "service": "Alertrix API",
            "database": "connected",
            "ai_service": "mock" if settings.USE_MOCK_AI else "real",
            "report_count": report_count,
            "alert_count": alert_count,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Alertrix API",
            "database": "disconnected",
            "ai_service": "unknown",
            "error": str(e)
        }