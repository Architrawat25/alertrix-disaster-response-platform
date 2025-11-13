import httpx
import random
import logging
from app.integrations.base import AIAdapter
from app.core.config import settings

from typing import Dict, Any # for Dict and Any


logger = logging.getLogger(__name__)


class GeoAdapter(AIAdapter):
    """Reverse geocoding adapter"""

    def __init__(self, use_mock: bool = None):
        super().__init__(use_mock or settings.USE_MOCK_AI)

    async def analyze(self, lat: float, lon: float) -> Dict[str, Any]:
        """Reverse geocode coordinates to location name"""
        return await self._call_api(lat, lon)

    async def _real_analyze(self, lat: float, lon: float) -> Dict[str, Any]:
        """Real reverse geocoding using Nominatim"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "format": "json",
                        "addressdetails": 1
                    },
                    headers={"User-Agent": "Alertrix/1.0"},
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    address = data.get("address", {})

                    # Build location name from available address components
                    location_parts = []
                    if address.get("city"):
                        location_parts.append(address["city"])
                    elif address.get("town"):
                        location_parts.append(address["town"])
                    elif address.get("village"):
                        location_parts.append(address["village"])

                    if address.get("state"):
                        location_parts.append(address["state"])

                    if address.get("country"):
                        location_parts.append(address["country"])

                    location_name = ", ".join(location_parts) if location_parts else "Unknown Location"

                    return {
                        "location_name": location_name,
                        "full_address": address,
                        "source": "nominatim"
                    }
                else:
                    raise Exception(f"Geocoding API error: {response.status_code}")

        except Exception as e:
            logger.error(f"Geocoding failed: {str(e)}")
            raise

    async def _mock_analyze(self, lat: float, lon: float) -> Dict[str, Any]:
        """Mock reverse geocoding"""
        cities = [
            "Mumbai, Maharashtra, India",
            "Delhi, NCT, India",
            "Bengaluru, Karnataka, India",
            "Chennai, Tamil Nadu, India",
            "Kolkata, West Bengal, India"
        ]
        return {
            "location_name": random.choice(cities),
            "full_address": {"mock": True},
            "source": "mock"
        }