import httpx
import random
import logging
from typing import List, Dict, Any
from app.integrations.base import AIAdapter
from app.core.config import settings

logger = logging.getLogger(__name__)


class ClassifierAdapter(AIAdapter):
    """Disaster type classification adapter"""

    def __init__(self, use_mock: bool = None):
        super().__init__(use_mock or settings.USE_MOCK_AI)
        self.hf_key = settings.HF_API_KEY
        self.disaster_types = ["flood", "fire", "earthquake", "storm", "other"]

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Classify disaster type from text"""
        return await self._call_api(text)

    async def _real_analyze(self, text: str) -> Dict[str, Any]:
        """Real classification using Hugging Face"""
        if not self.hf_key:
            logger.warning("No HF API key, falling back to mock classifier")
            return await self._mock_analyze(text)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
                    headers={"Authorization": f"Bearer {self.hf_key}"},
                    json={
                        "inputs": text,
                        "parameters": {
                            "candidate_labels": self.disaster_types
                        }
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    result = response.json()
                    labels = result.get("labels", [])
                    scores = result.get("scores", [])

                    if labels and scores:
                        # Get the highest scoring label
                        max_score = max(scores)
                        max_index = scores.index(max_score)
                        disaster_type = labels[max_index]

                        return {
                            "disaster_type": disaster_type,
                            "confidence": max_score,
                            "all_scores": dict(zip(labels, scores)),
                            "source": "huggingface"
                        }

                raise Exception(f"Classification API error: {response.status_code}")

        except Exception as e:
            logger.error(f"Classification failed: {str(e)}")
            raise

    async def _mock_analyze(self, text: str) -> Dict[str, Any]:
        """Mock classification - random choice with weighted probabilities"""
        # Simple keyword-based mock classification
        text_lower = text.lower()

        if any(word in text_lower for word in ["flood", "rain", "water", "inundat"]):
            disaster_type = "flood"
            confidence = random.uniform(0.7, 0.95)
        elif any(word in text_lower for word in ["fire", "burn", "blaze", "smoke"]):
            disaster_type = "fire"
            confidence = random.uniform(0.7, 0.95)
        elif any(word in text_lower for word in ["earthquake", "quake", "tremor", "seismic"]):
            disaster_type = "earthquake"
            confidence = random.uniform(0.7, 0.95)
        elif any(word in text_lower for word in ["storm", "hurricane", "cyclone", "wind"]):
            disaster_type = "storm"
            confidence = random.uniform(0.7, 0.95)
        else:
            disaster_type = "other"
            confidence = random.uniform(0.3, 0.6)

        return {
            "disaster_type": disaster_type,
            "confidence": confidence,
            "all_scores": {disaster_type: confidence},
            "source": "mock"
        }