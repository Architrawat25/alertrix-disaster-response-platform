from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.db.models import Report
from app.schemas.report import ReportCreate, ReportResponse, AnalyzeRequest
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/report", response_model=ReportResponse)
async def create_report(
        report_data: ReportCreate,
        session: Session = Depends(get_session)
):
    """Create a new disaster report"""
    try:
        db_report = Report(**report_data.dict())
        session.add(db_report)
        session.commit()
        session.refresh(db_report)

        logger.info(f"Created report ID: {db_report.id}")
        return db_report

    except Exception as e:
        logger.error(f"Error creating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create report")


@router.post("/analyze")
async def analyze_report(analyze_request: AnalyzeRequest):
    """Mock analyze endpoint - will integrate AI in Phase 2"""
    return {
        "message": "analysis pending",
        "report_id": analyze_request.report_id,
        "status": "queued"
    }