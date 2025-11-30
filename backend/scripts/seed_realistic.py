import random
from datetime import datetime, timedelta
from sqlmodel import Session
from app.db.models import Report, Alert
from app.db.session import engine
import logging

logger = logging.getLogger(__name__)

# Realistic disaster scenarios
DISASTER_SCENARIOS = [
    {
        "type": "flood",
        "templates": [
            "Heavy rainfall causing flooding in {area}. Water levels rising rapidly.",
            "Flash floods reported in {area}. Multiple roads submerged.",
            "River overflowing in {area}. Evacuations underway.",
            "Urban flooding in {area}. Drainage systems overwhelmed."
        ],
        "severity_range": (60, 95),
        "areas": ["downtown", "residential areas", "commercial district", "suburbs"]
    },
    {
        "type": "earthquake",
        "templates": [
            "Earthquake magnitude {magnitude} felt in {area}. Buildings shaking.",
            "Seismic activity reported in {area}. Aftershocks expected.",
            "Tremor felt across {area}. Structural damage reported.",
            "Earthquake alert for {area}. Emergency services mobilized."
        ],
        "severity_range": (70, 98),
        "magnitudes": ["4.5", "5.2", "6.1", "5.8", "4.9"]
    },
    {
        "type": "fire",
        "templates": [
            "Wildfire spreading in {area}. Fire department responding.",
            "Forest fire reported in {area}. Evacuations ordered.",
            "Industrial fire in {area}. Smoke visible for miles.",
            "Residential fire outbreak in {area}. Multiple units responding."
        ],
        "severity_range": (65, 90),
        "areas": ["forest area", "industrial zone", "residential district", "national park"]
    },
    {
        "type": "storm",
        "templates": [
            "Severe storm hitting {area}. High winds and heavy rain.",
            "Cyclone approaching {area}. Emergency alerts issued.",
            "Thunderstorm with lightning in {area}. Power outages reported.",
            "Hurricane conditions in {area}. Coastal areas evacuated."
        ],
        "severity_range": (55, 85),
        "areas": ["coastal region", "metropolitan area", "mountain region", "valley area"]
    }
]

# Indian cities with coordinates
INDIAN_CITIES = [
    {"name": "Mumbai, Maharashtra", "lat": 19.0760, "lon": 72.8777},
    {"name": "Delhi, NCT", "lat": 28.6139, "lon": 77.2090},
    {"name": "Bengaluru, Karnataka", "lat": 12.9716, "lon": 77.5946},
    {"name": "Chennai, Tamil Nadu", "lat": 13.0827, "lon": 80.2707},
    {"name": "Kolkata, West Bengal", "lat": 22.5726, "lon": 88.3639},
    {"name": "Hyderabad, Telangana", "lat": 17.3850, "lon": 78.4867},
    {"name": "Pune, Maharashtra", "lat": 18.5204, "lon": 73.8567},
    {"name": "Ahmedabad, Gujarat", "lat": 23.0225, "lon": 72.5714},
    {"name": "Jaipur, Rajasthan", "lat": 26.9124, "lon": 75.7873},
    {"name": "Lucknow, Uttar Pradesh", "lat": 26.8467, "lon": 80.9462}
]

SOURCES = ["mobile_app", "web_portal", "twitter", "sms", "emergency_services"]


def generate_realistic_reports(count=40):
    """Generate realistic disaster reports"""
    reports = []

    for i in range(count):
        disaster_type = random.choice(DISASTER_SCENARIOS)
        city = random.choice(INDIAN_CITIES)

        # Generate report text
        if disaster_type["type"] == "earthquake":
            magnitude = random.choice(disaster_type["magnitudes"])
            area = random.choice(disaster_type["areas"])
            template = random.choice(disaster_type["templates"])
            text = template.format(magnitude=magnitude, area=area)
        else:
            area = random.choice(disaster_type["areas"])
            template = random.choice(disaster_type["templates"])
            text = template.format(area=area)

        # Random time within last 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        created_at = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

        report = Report(
            text=text,
            lat=city["lat"] + random.uniform(-0.5, 0.5),  # Add some variation
            lon=city["lon"] + random.uniform(-0.5, 0.5),
            source=random.choice(SOURCES),
            created_at=created_at,
            updated_at=created_at,
            is_analyzed=True
        )
        reports.append(report)

    return reports


def generate_alerts_from_reports(reports):
    """Generate alerts from reports"""
    alerts = []

    for report in reports:
        # Determine disaster type from report text
        disaster_type = "other"
        severity_range = (40, 70)

        for scenario in DISASTER_SCENARIOS:
            if scenario["type"] in report.text.lower():
                disaster_type = scenario["type"]
                severity_range = scenario["severity_range"]
                break

        severity_score = random.randint(severity_range[0], severity_range[1])

        # Create summary based on disaster type
        summaries = {
            "flood": [
                "Urban flooding due to heavy rainfall",
                "Flash floods causing road closures",
                "River overflow affecting residential areas",
                "Waterlogging in low-lying regions"
            ],
            "earthquake": [
                "Seismic activity with potential aftershocks",
                "Earthquake causing structural assessments",
                "Tremor felt across the region",
                "Building safety inspections underway"
            ],
            "fire": [
                "Wildfire containment operations active",
                "Fire department battling blaze",
                "Emergency evacuation in progress",
                "Smoke affecting air quality"
            ],
            "storm": [
                "Severe weather conditions ongoing",
                "Cyclone preparedness measures active",
                "Storm damage assessment in progress",
                "Emergency shelters opened"
            ],
            "other": [
                "Emergency situation reported",
                "Incident response activated",
                "Local authorities responding",
                "Situation being monitored"
            ]
        }

        summary = random.choice(summaries[disaster_type])

        # Find city name for location
        location_name = "Unknown Location"
        for city in INDIAN_CITIES:
            if abs(city["lat"] - report.lat) < 1.0 and abs(city["lon"] - report.lon) < 1.0:
                location_name = city["name"]
                break

        alert = Alert(
            report_id=report.id,
            disaster_type=disaster_type,
            severity_score=severity_score,
            summary=summary,
            location_name=location_name,
            created_at=report.created_at,
            is_active=random.choice([True, True, True, False])  # 75% active
        )
        alerts.append(alert)

    return alerts


def seed_realistic_data():
    """Seed database with realistic mock data"""
    try:
        with Session(engine) as session:
            # Check if we already have realistic data
            existing_reports = session.query(Report).count()
            if existing_reports > 50:  # Already seeded
                logger.info("Realistic data already seeded, skipping...")
                return

            logger.info("Seeding realistic disaster data...")

            # Generate and add reports
            reports = generate_realistic_reports(40)
            for report in reports:
                session.add(report)

            session.commit()

            # Refresh to get IDs
            for report in reports:
                session.refresh(report)

            # Generate and add alerts
            alerts = generate_alerts_from_reports(reports)
            for alert in alerts:
                session.add(alert)

            session.commit()

            logger.info(f"Seeded {len(reports)} realistic reports and {len(alerts)} alerts")

    except Exception as e:
        logger.error(f"Failed to seed realistic data: {str(e)}")


if __name__ == "__main__":
    seed_realistic_data()