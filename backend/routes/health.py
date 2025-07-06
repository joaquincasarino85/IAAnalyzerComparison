from fastapi import APIRouter
from typing import Dict
import os

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check() -> Dict[str, str]:
    """Simple health check endpoint for Railway"""
    return {
        "status": "healthy",
        "message": "IAAnalyzerComparator is running",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@router.get("/ping")
async def ping() -> Dict[str, str]:
    """Simple ping endpoint"""
    return {"message": "pong"} 