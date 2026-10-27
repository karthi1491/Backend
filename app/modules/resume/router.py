from fastapi import APIRouter, UploadFile, File

from app.modules.resume import service
from app.modules.resume.schemas import ResumeResponse


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post(
    "/upload",
    response_model=ResumeResponse,
)
async def upload_resume(file: UploadFile = File(...)):
    return await service.upload_resume(file)


@router.get(
    "",
    response_model=ResumeResponse,
)
async def get_resume():
    return await service.get_resume()