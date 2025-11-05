import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./alertrix.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()