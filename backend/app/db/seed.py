from sqlmodel import Session
from app.db.models import Report, Alert
from app.db.session import engine
import logging

logger = logging.getLogger(__name__)


def seed_database():
    """Seed the database with sample data"""
    with Session(engine) as session:
        # Check if we already have data
        existing_reports = session.query(Report).count()
        if existing_reports > 0:
            logger.info("Database already seeded, skipping...")
            return

        # Sample reports
        sample_reports = [
            Report(
                text="Heavy rainfall causing flooding in downtown area. Multiple roads blocked.",
                lat=40.7128,
                lon=-74.0060,
                source="mobile_app",
                is_analyzed=True
            ),
            Report(
                text="Earthquake felt in mountain region. Buildings shaking for 30 seconds.",
                lat=34.0522,
                lon=-118.2437,
                source="web_portal",
                is_analyzed=True
            ),
            Report(
                text="Forest fire spreading rapidly in national park area.",
                lat=37.7749,
                lon=-122.4194,
                source="sms",
                is_analyzed=True
            ),
            Report(
                text="Severe storm with high winds damaging infrastructure.",
                lat=51.5074,
                lon=-0.1278,
                source="twitter",
                is_analyzed=True
            )
        ]

        for report in sample_reports:
            session.add(report)

        session.commit()

        # Refresh to get IDs
        for report in sample_reports:
            session.refresh(report)

        # Sample alerts
        sample_alerts = [
            Alert(
                report_id=sample_reports[0].id,
                disaster_type="flood",
                severity_score=75,
                summary="Urban flooding due to heavy rainfall",
                location_name="New York, NY, USA"
            ),
            Alert(
                report_id=sample_reports[1].id,
                disaster_type="earthquake",
                severity_score=90,
                summary="Moderate earthquake with potential aftershocks",
                location_name="Los Angeles, CA, USA"
            ),
            Alert(
                report_id=sample_reports[2].id,
                disaster_type="fire",
                severity_score=85,
                summary="Wildfire spreading in forest area",
                location_name="San Francisco, CA, USA"
            ),
            Alert(
                report_id=sample_reports[3].id,
                disaster_type="storm",
                severity_score=65,
                summary="Severe storm causing infrastructure damage",
                location_name="London, UK"
            )
        ]

        for alert in sample_alerts:
            session.add(alert)

        session.commit()
        logger.info(f"Seeded database with {len(sample_reports)} reports and {len(sample_alerts)} alerts")


if __name__ == "__main__":
    seed_database()