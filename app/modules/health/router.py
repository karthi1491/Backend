from fastapi import APIRouter, HTTPException

from app.core.database import db


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "message": "Naukri AI Agent is running",
    }


@router.get("/database")
async def database_health():
    try:
        await db.command("ping")

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )