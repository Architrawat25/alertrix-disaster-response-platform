import logging
import random
from typing import Dict, Any
from app.integrations import SummarizerAdapter, ClassifierAdapter, WeatherAdapter, GeoAdapter
from app.core.config import settings

logger = logging.getLogger(__name__)


class ReportAnalyzer:
    """Orchestrates AI adapters to analyze disaster reports"""

    def __init__(self):
        self.summarizer = SummarizerAdapter()
        self.classifier = ClassifierAdapter()
        self.weather = WeatherAdapter()
        self.geo = GeoAdapter()

    async def analyze_report(self, text: str, lat: float, lon: float) -> Dict[str, Any]:
        """
        Analyze a disaster report using all AI adapters

        Returns:
            Dict with analysis results including:
            - summary: str
            - disaster_type: str
            - severity_score: int (0-100)
            - location_name: str
            - evidence: Dict with raw adapter results
        """
        logger.info(f"Starting analysis for report at ({lat}, {lon})")

        try:
            # Run all adapters concurrently
            summary_result = await self.summarizer.analyze(text)
            classification_result = await self.classifier.analyze(text)
            weather_result = await self.weather.analyze(lat, lon)
            geo_result = await self.geo.analyze(lat, lon)

            # Calculate severity score based on classification confidence and disaster type
            base_severity = self._calculate_severity(
                classification_result["disaster_type"],
                classification_result["confidence"]
            )

            # Adjust severity based on weather conditions if relevant
            adjusted_severity = self._adjust_severity_by_weather(
                base_severity,
                classification_result["disaster_type"],
                weather_result
            )

            result = {
                "summary": summary_result["summary"],
                "disaster_type": classification_result["disaster_type"],
                "severity_score": adjusted_severity,
                "location_name": geo_result["location_name"],
                "evidence": {
                    "summarizer": summary_result,
                    "classifier": classification_result,
                    "weather": weather_result,
                    "geo": geo_result
                }
            }

            logger.info(f"Analysis completed: {classification_result['disaster_type']} "
                        f"with severity {adjusted_severity}")

            return result

        except Exception as e:
            logger.error(f"Report analysis failed: {str(e)}")
            # Return fallback result
            return self._get_fallback_result(text, lat, lon)

    def _calculate_severity(self, disaster_type: str, confidence: float) -> int:
        """Calculate base severity score"""
        # Base severity by disaster type
        type_base_scores = {
            "earthquake": 70,
            "fire": 65,
            "flood": 60,
            "storm": 55,
            "other": 40
        }

        base_score = type_base_scores.get(disaster_type, 40)

        # Adjust by confidence
        confidence_adjustment = int((confidence - 0.5) * 40)  # -20 to +20

        severity = base_score + confidence_adjustment

        # Ensure within bounds
        return max(0, min(100, severity))

    def _adjust_severity_by_weather(self, base_severity: int, disaster_type: str,
                                    weather_data: Dict[str, Any]) -> int:
        """Adjust severity based on weather conditions"""
        adjustment = 0
        conditions = weather_data.get("conditions", "").lower()
        wind_speed = weather_data.get("wind_speed", 0)

        if disaster_type == "flood" and any(cond in conditions for cond in ["rain", "storm"]):
            adjustment += 15
        elif disaster_type == "storm" and wind_speed > 15:
            adjustment += 10
        elif disaster_type == "fire" and "rain" in conditions:
            adjustment -= 10

        # Add some random variation (±5) to make mock results more realistic
        random_variation = random.randint(-5, 5)

        final_severity = base_severity + adjustment + random_variation
        return max(0, min(100, final_severity))

    def _get_fallback_result(self, text: str, lat: float, lon: float) -> Dict[str, Any]:
        """Generate fallback result when analysis fails"""
        return {
            "summary": f"Emergency report: {text[:50]}... [analysis failed]",
            "disaster_type": "other",
            "severity_score": 50,
            "location_name": "Unknown Location",
            "evidence": {
                "summarizer": {"error": "Analysis failed"},
                "classifier": {"error": "Analysis failed"},
                "weather": {"error": "Analysis failed"},
                "geo": {"error": "Analysis failed"}
            }
        }


# Global analyzer instance
analyzer = ReportAnalyzer()


async def analyze_report(text: str, lat: float, lon: float) -> Dict[str, Any]:
    """Convenience function to analyze a report"""
    return await analyzer.analyze_report(text, lat, lon)