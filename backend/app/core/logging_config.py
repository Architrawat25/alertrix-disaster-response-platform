import logging
import sys
from app.core.config import settings

def setup_logging():
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("alertrix.log")
        ]
    )