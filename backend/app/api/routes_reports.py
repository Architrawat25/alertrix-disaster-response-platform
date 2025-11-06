from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from app.db.session import get_session
from app.db.models import Report
from app.schemas.report import ReportCreate, ReportResponse, AnalyzeRequest
from app.services.analyzer import analyze_report
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
async def analyze_report_endpoint(analyze_request: AnalyzeRequest, session: Session = Depends(get_session)):
    """Analyze a report using AI integration layer"""
    try:
        # Get the report from database
        report = session.get(Report, analyze_request.report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        # Call the AI analyzer
        analysis_result = await analyze_report(report.text, report.lat, report.lon)

        logger.info(f"Analysis completed for report {analyze_request.report_id}: "
                    f"{analysis_result['disaster_type']} (severity: {analysis_result['severity_score']})")

        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed for report {analyze_request.report_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed")