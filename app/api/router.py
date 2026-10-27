from fastapi import APIRouter

from app.modules.health.router import router as health_router
from app.modules.naukri.router import router as naukri_router
from app.modules.profile.router import router as profile_router
from app.modules.resume.router import router as resume_router
from app.modules.jobs.router import router as jobs_router


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(naukri_router)
api_router.include_router(profile_router)
api_router.include_router(resume_router)
api_router.include_router(jobs_router)