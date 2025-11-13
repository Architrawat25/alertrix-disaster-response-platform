import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from app.main import app
from app.db.session import get_session, create_db_and_tables
from app.db.models import Report, Alert
import time

# Test database
TEST_DATABASE_URL = "sqlite:///./test_alertrix.db"
engine = create_engine(TEST_DATABASE_URL)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    """Setup test database before tests and tear down after"""
    create_db_and_tables()
    yield
    # Clean up (optional: delete test database file)


@pytest.fixture
def client():
    """Test client"""
    return TestClient(app)


def test_end_to_end_report_to_alert_flow(client):
    """Test complete flow: create report -> background analysis -> alert creation"""

    # Step 1: Create a report
    report_data = {
        "text": "Heavy flooding in downtown area. Multiple roads blocked and vehicles submerged.",
        "lat": 40.7128,
        "lon": -74.0060,
        "source": "test_app"
    }

    response = client.post("/api/v1/report", json=report_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
    assert data["message"] == "Report received, analysis in progress"

    report_id = data["report"]["id"]
    assert report_id is not None

    # Step 2: Wait a bit for background task to complete
    time.sleep(2)

    # Step 3: Check that alerts now include the new alert
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    alerts = response.json()

    # Should have at least one alert (our new one + seeded ones)
    assert len(alerts) >= 1

    # Find our alert (most recent one)
    new_alert = alerts[0]  # Most recent first
    assert new_alert["report_id"] == report_id
    assert new_alert["disaster_type"] in ["flood", "fire", "earthquake", "storm", "other"]
    assert 0 <= new_alert["severity_score"] <= 100
    assert new_alert["summary"] is not None
    assert new_alert["location_name"] is not None


def test_alert_filtering(client):
    """Test alert filtering functionality"""

    # Test type filter
    response = client.get("/api/v1/alerts?type=flood")
    assert response.status_code == 200
    flood_alerts = response.json()
    if flood_alerts:  # If there are flood alerts
        for alert in flood_alerts:
            assert alert["disaster_type"] == "flood"

    # Test min_severity filter
    response = client.get("/api/v1/alerts?min_severity=80")
    assert response.status_code == 200
    high_severity_alerts = response.json()
    if high_severity_alerts:
        for alert in high_severity_alerts:
            assert alert["severity_score"] >= 80

    # Test limit filter
    response = client.get("/api/v1/alerts?limit=2")
    assert response.status_code == 200
    limited_alerts = response.json()
    assert len(limited_alerts) <= 2

    # Test combined filters
    response = client.get("/api/v1/alerts?type=earthquake&min_severity=50&limit=1")
    assert response.status_code == 200
    combined_alerts = response.json()
    if combined_alerts:
        alert = combined_alerts[0]
        assert alert["disaster_type"] == "earthquake"
        assert alert["severity_score"] >= 50


def test_direct_analyze_endpoint(client):
    """Test direct analyze endpoint"""
    # First create a report
    report_data = {
        "text": "Forest fire spreading near residential area.",
        "lat": 34.0522,
        "lon": -118.2437,
        "source": "test"
    }

    report_response = client.post("/api/v1/report", json=report_data)
    report_id = report_response.json()["report"]["id"]

    # Test direct analysis
    analyze_response = client.post("/api/v1/analyze", json={"report_id": report_id})
    assert analyze_response.status_code == 200
    analysis_data = analyze_response.json()

    assert "summary" in analysis_data
    assert "disaster_type" in analysis_data
    assert "severity_score" in analysis_data
    assert "location_name" in analysis_data
    assert "evidence" in analysis_data


def test_report_creation_persistence(client):
    """Test that reports are properly persisted"""
    report_data = {
        "text": "Test report for persistence check",
        "lat": 51.5074,
        "lon": -0.1278,
        "source": "persistence_test"
    }

    response = client.post("/api/v1/report", json=report_data)
    assert response.status_code == 200

    # Verify the report was saved by checking database directly
    with Session(engine) as session:
        reports = session.exec(Report.select()).all()
        assert any(r.text == "Test report for persistence check" for r in reports)