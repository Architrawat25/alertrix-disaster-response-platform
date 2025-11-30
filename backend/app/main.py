from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api import routes_reports, routes_alerts, routes_health
from app.db.session import create_db_and_tables
import logging
import sys
import os

# Add the backend directory to Python path so scripts can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Alertrix API",
    description="AI-Driven Disaster Response & Coordination Platform",
    version="1.0.0"
)

# CORS middleware - SIMPLIFIED TO GET IT WORKING
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes_health.router, tags=["health"])
app.include_router(routes_reports.router, prefix="/api/v1", tags=["reports"])
app.include_router(routes_alerts.router, prefix="/api/v1", tags=["alerts"])


@app.on_event("startup")
def on_startup():
    """Initialize database and seed data on startup"""
    create_db_and_tables()

    # Seed database on startup for deployment
    try:
        from app.db.seed import seed_database
        seed_database()
        logger.info("Basic seeding completed")
    except Exception as e:
        logger.warning(f"Basic seeding failed: {e}")

    # Try to seed realistic data if available
    try:
        from scripts.seed_realistic import seed_realistic_data
        seed_realistic_data()
        logger.info("Realistic data seeding completed")
    except ImportError as e:
        logger.warning(f"Realistic data seeding not available: {e}")
    except Exception as e:
        logger.error(f"Realistic data seeding failed: {e}")

    logger.info("Alertrix API started successfully")


@app.get("/")
async def root():
    return {
        "message": "Welcome to Alertrix Disaster Response API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "deployed"
    }