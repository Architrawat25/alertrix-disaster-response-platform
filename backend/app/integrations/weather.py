import httpx
import random
import logging
from app.integrations.base import AIAdapter
from app.core.config import settings

from typing import Dict, Any # for Dict and Any


logger = logging.getLogger(__name__)


class WeatherAdapter(AIAdapter):
    """Weather information adapter"""

    def __init__(self, use_mock: bool = None):
        super().__init__(use_mock or settings.USE_MOCK_AI)
        self.api_key = settings.OPENWEATHER_KEY

    async def analyze(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get weather information for coordinates"""
        return await self._call_api(lat, lon)

    async def _real_analyze(self, lat: float, lon: float) -> Dict[str, Any]:
        """Real weather data from OpenWeather"""
        if not self.api_key:
            logger.warning("No OpenWeather key, falling back to mock weather")
            return await self._mock_analyze(lat, lon)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric"
                    },
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temperature": data["main"]["temp"],
                        "conditions": data["weather"][0]["description"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                        "source": "openweather"
                    }
                else:
                    raise Exception(f"Weather API error: {response.status_code}")

        except Exception as e:
            logger.error(f"Weather API failed: {str(e)}")
            raise

    async def _mock_analyze(self, lat: float, lon: float) -> Dict[str, Any]:
        """Mock weather data"""
        conditions = ["clear", "cloudy", "rainy", "stormy", "foggy"]
        return {
            "temperature": round(random.uniform(-10, 35), 1),
            "conditions": random.choice(conditions),
            "humidity": random.randint(30, 95),
            "wind_speed": round(random.uniform(0, 25), 1),
            "source": "mock"
        }