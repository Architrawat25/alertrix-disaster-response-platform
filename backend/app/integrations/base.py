from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class AIAdapter(ABC):
    """Base class for all AI adapters"""

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """Main analysis method to be implemented by each adapter"""
        pass

    async def _call_api(self, *args, **kwargs) -> Dict[str, Any]:
        """Helper method for API calls with error handling"""
        try:
            if self.use_mock:
                return await self._mock_analyze(*args, **kwargs)
            else:
                return await self._real_analyze(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error in {self.__class__.__name__}: {str(e)}")
            # Fallback to mock mode on error
            return await self._mock_analyze(*args, **kwargs)

    @abstractmethod
    async def _real_analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """Real API implementation"""
        pass

    @abstractmethod
    async def _mock_analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """Mock implementation"""
        pass