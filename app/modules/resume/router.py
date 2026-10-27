from fastapi import APIRouter, File, UploadFile

from app.modules.resume import service
from app.modules.resume.schemas import (
    ResumeOptimizationResult,
    ResumeOptimizeRequest,
    ResumeResponse,
    ResumeReviewRequest,
)

from app.modules.resume.schemas import ResumeVersionResponse

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


@router.post(
    "/optimize",
    response_model=ResumeOptimizationResult,
)
async def optimize_resume_endpoint(
    request: ResumeOptimizeRequest,
):
    return await service.generate_optimization(
        request.job_description
    )





@router.post(
    "/optimizations/{optimization_id}/review",
    response_model=ResumeOptimizationResult,
)
async def review_optimization_endpoint(
    optimization_id: str,
    request: ResumeReviewRequest,
):
    return await service.review_resume_optimization(
        optimization_id,
        request,
    )






@router.post(
    "/optimizations/{optimization_id}/review",
    response_model=ResumeOptimizationResult,
)
async def review_optimization_endpoint(
    optimization_id: str,
    request: ResumeReviewRequest,
):
    return await service.review_resume_optimization(
        optimization_id,
        request,
    )






@router.post(
    "/optimizations/{optimization_id}/create-version",
    response_model=ResumeVersionResponse,
)
async def create_version_endpoint(optimization_id: str):
    return await service.create_approved_resume_version(
        optimization_id
    )


@router.get(
    "/versions/{version_id}",
    response_model=ResumeVersionResponse,
)
async def get_version_endpoint(version_id: str):
    return await service.fetch_resume_version(version_id)