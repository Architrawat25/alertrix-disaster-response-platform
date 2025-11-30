from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api import routes_reports, routes_alerts, routes_health
from app.db.session import create_db_and_tables
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Alertrix API",
    description="AI-Driven Disaster Response & Coordination Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://alertrix-disaster-response-platform.vercel.app/",  #Actual frontend URL
        "http://localhost:3000"  #Local development
    ],
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
    logger.info("Alertrix API started successfully")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Alertrix Disaster Response API",
        "version": "1.0.0",
        "docs": "/docs"
    }
