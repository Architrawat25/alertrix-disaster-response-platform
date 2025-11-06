import httpx
import logging
from app.integrations.base import AIAdapter
from app.core.config import settings

from typing import Dict, Any # for Dict and Any


logger = logging.getLogger(__name__)


class SummarizerAdapter(AIAdapter):
    """Text summarization adapter using OpenAI or Hugging Face"""

    def __init__(self, use_mock: bool = None):
        super().__init__(use_mock or settings.USE_MOCK_AI)
        self.openai_key = settings.OPENAI_API_KEY
        self.hf_key = settings.HF_API_KEY

    async def analyze(self, text: str) -> Dict[str, Any]:
        """Summarize the input text"""
        return await self._call_api(text)

    async def _real_analyze(self, text: str) -> Dict[str, Any]:
        """Real summarization using available APIs"""
        # Try OpenAI first if key is available
        if self.openai_key:
            return await self._openai_summarize(text)
        # Fallback to Hugging Face if key is available
        elif self.hf_key:
            return await self._hf_summarize(text)
        else:
            # No API keys available, fallback to mock
            logger.warning("No API keys available, falling back to mock summarizer")
            return await self._mock_analyze(text)

    async def _openai_summarize(self, text: str) -> Dict[str, Any]:
        """Summarize using OpenAI API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a disaster response assistant. Summarize the disaster report concisely, focusing on key facts and urgency."
                            },
                            {
                                "role": "user",
                                "content": f"Summarize this disaster report: {text}"
                            }
                        ],
                        "max_tokens": 150
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    result = response.json()
                    summary = result["choices"][0]["message"]["content"].strip()
                    return {
                        "summary": summary,
                        "source": "openai",
                        "confidence": 0.9
                    }
                else:
                    raise Exception(f"OpenAI API error: {response.status_code}")

        except Exception as e:
            logger.error(f"OpenAI summarization failed: {str(e)}")
            raise

    async def _hf_summarize(self, text: str) -> Dict[str, Any]:
        """Summarize using Hugging Face API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
                    headers={"Authorization": f"Bearer {self.hf_key}"},
                    json={"inputs": text},
                    timeout=30.0
                )

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        summary = result[0].get("summary_text", "").strip()
                        return {
                            "summary": summary,
                            "source": "huggingface",
                            "confidence": 0.8
                        }
                raise Exception(f"HF API error: {response.status_code}")

        except Exception as e:
            logger.error(f"Hugging Face summarization failed: {str(e)}")
            raise

    async def _mock_analyze(self, text: str) -> Dict[str, Any]:
        """Mock summarization - returns first 100 chars"""
        summary = text[:100] + "..." if len(text) > 100 else text
        return {
            "summary": f"{summary} [summary generated]",
            "source": "mock",
            "confidence": 0.7
        }