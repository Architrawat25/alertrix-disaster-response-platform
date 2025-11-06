import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./alertrix.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # AI Integration Settings
    USE_MOCK_AI: bool = os.getenv("USE_MOCK_AI", "true").lower() == "true"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    OPENWEATHER_KEY: str = os.getenv("OPENWEATHER_KEY", "")

settings = Settings()