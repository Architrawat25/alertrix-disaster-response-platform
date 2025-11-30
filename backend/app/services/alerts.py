import logging
from sqlmodel import Session, select
from app.db.models import Alert, Report
from app.schemas.alert import AlertFilter, FrontendAlertResponse

logger = logging.getLogger(__name__)


async def run_analysis_and_create_alert(report_id: int):
    """
    Background task to analyze report and create alert
    """
    from app.db.session import engine
    from app.services.analyzer import analyze_report

    logger.info(f"Starting background analysis for report {report_id}")

    try:
        with Session(engine) as session:
            # Get the report
            report = session.get(Report, report_id)
            if not report:
                logger.error(f"Report {report_id} not found for analysis")
                return

            # Analyze the report using AI
            analysis_result = await analyze_report(report.text, report.lat, report.lon)

            # Create alert from analysis results
            alert = Alert(
                report_id=report_id,
                disaster_type=analysis_result["disaster_type"],
                severity_score=analysis_result["severity_score"],
                summary=analysis_result["summary"],
                location_name=analysis_result["location_name"]
            )

            # Update report as analyzed
            report.is_analyzed = True

            # Save to database
            session.add(alert)
            session.add(report)
            session.commit()
            session.refresh(alert)

            # Log high severity alerts
            if alert.severity_score > 80:
                logger.warning(f"⚠️ HIGH-SEVERITY ALERT! ID: {alert.id}, "
                               f"Type: {alert.disaster_type}, "
                               f"Severity: {alert.severity_score}")
            else:
                logger.info(f"Alert created: ID {alert.id}, "
                            f"Type: {alert.disaster_type}, "
                            f"Severity: {alert.severity_score}")

            return alert

    except Exception as e:
        logger.error(f"Failed to analyze report {report_id}: {str(e)}")
        # Mark report as analyzed even if failed to prevent infinite retries
        try:
            with Session(engine) as session:
                report = session.get(Report, report_id)
                if report:
                    report.is_analyzed = True
                    session.add(report)
                    session.commit()
        except Exception as inner_e:
            logger.error(f"Failed to mark report {report_id} as analyzed: {str(inner_e)}")


def get_filtered_alerts(session: Session, alert_filter: AlertFilter):
    """
    Get alerts with optional filtering - ORIGINAL VERSION (keep for compatibility)
    """
    from app.db.models import Alert
    query = select(Alert)

    # Apply filters
    if alert_filter.active_only:
        query = query.where(Alert.is_active == True)

    if alert_filter.type:
        query = query.where(Alert.disaster_type == alert_filter.type)

    if alert_filter.min_severity is not None:
        query = query.where(Alert.severity_score >= alert_filter.min_severity)

    # Order by creation date (newest first)
    query = query.order_by(Alert.created_at.desc())

    # Apply limit
    if alert_filter.limit:
        query = query.limit(alert_filter.limit)

    alerts = session.exec(query).all()
    return alerts


def get_filtered_alerts_with_reports(session: Session, alert_filter: AlertFilter):
    """
    Get alerts joined with report data for frontend compatibility
    """
    query = select(Alert, Report).join(Report, Alert.report_id == Report.id)

    # Apply filters
    if alert_filter.active_only:
        query = query.where(Alert.is_active == True)

    if alert_filter.type:
        query = query.where(Alert.disaster_type == alert_filter.type)

    if alert_filter.min_severity is not None:
        query = query.where(Alert.severity_score >= alert_filter.min_severity)

    query = query.order_by(Alert.created_at.desc())

    if alert_filter.limit:
        query = query.limit(alert_filter.limit)

    results = session.exec(query).all()

    # Transform to frontend format
    frontend_alerts = []
    for alert, report in results:
        frontend_alert = FrontendAlertResponse(
            id=alert.id,
            alert_type=alert.disaster_type,
            summary=alert.summary,
            location=alert.location_name,
            lat=report.lat,
            lon=report.lon,
            severity=alert.severity_score,
            timestamp=alert.created_at.isoformat(),
            source=report.source
        )
        frontend_alerts.append(frontend_alert)

    return frontend_alerts