from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from app.db.session import get_session
from app.db.models import Report
from app.schemas.report import ReportCreate, ReportResponse, AnalyzeRequest, ReportStatusResponse
from app.services.analyzer import analyze_report
from app.services.alerts import run_analysis_and_create_alert
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/report", response_model=ReportStatusResponse)
async def create_report(
        report_data: ReportCreate,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
):
    """Create a new disaster report and trigger background analysis"""
    try:
        db_report = Report(**report_data.dict())
        session.add(db_report)
        session.commit()
        session.refresh(db_report)

        # Trigger background analysis
        background_tasks.add_task(run_analysis_and_create_alert, db_report.id)

        logger.info(f"Created report ID: {db_report.id}, analysis queued")

        return ReportStatusResponse(
            status="received",
            report=db_report,
            message="Report received, analysis in progress"
        )

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