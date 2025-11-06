import pytest
import asyncio
from app.services.analyzer import analyze_report
from app.core.config import settings


@pytest.mark.asyncio
async def test_analyze_report_mock_mode():
    """Test analyze_report function in mock mode"""
    # Ensure we're in mock mode
    assert settings.USE_MOCK_AI == True

    test_text = "Heavy flooding in downtown area. Multiple roads blocked and vehicles submerged."
    test_lat = 40.7128
    test_lon = -74.0060

    result = await analyze_report(test_text, test_lat, test_lon)

    # Check required keys are present
    assert "summary" in result
    assert "disaster_type" in result
    assert "severity_score" in result
    assert "location_name" in result
    assert "evidence" in result

    # Check evidence contains all adapters
    evidence = result["evidence"]
    assert "summarizer" in evidence
    assert "classifier" in evidence
    assert "weather" in evidence
    assert "geo" in evidence

    # Check data types and ranges
    assert isinstance(result["summary"], str)
    assert result["disaster_type"] in ["flood", "fire", "earthquake", "storm", "other"]
    assert 0 <= result["severity_score"] <= 100
    assert isinstance(result["location_name"], str)

    # Check mock indicators
    assert evidence["summarizer"]["source"] == "mock"
    assert evidence["classifier"]["source"] == "mock"
    assert evidence["weather"]["source"] == "mock"
    assert evidence["geo"]["source"] == "mock"


@pytest.mark.asyncio
async def test_analyze_report_consistency():
    """Test that analyze_report returns consistent structure"""
    test_cases = [
        ("Flooding in city center", 40.7128, -74.0060),
        ("Forest fire spreading rapidly", 34.0522, -118.2437),
        ("Earthquake felt in residential area", 37.7749, -122.4194),
    ]

    for text, lat, lon in test_cases:
        result = await analyze_report(text, lat, lon)

        # Required keys check
        required_keys = ["summary", "disaster_type", "severity_score", "location_name", "evidence"]
        for key in required_keys:
            assert key in result, f"Missing key {key} in result"

        # Evidence structure check
        evidence_keys = ["summarizer", "classifier", "weather", "geo"]
        for key in evidence_keys:
            assert key in result["evidence"], f"Missing evidence key {key}"