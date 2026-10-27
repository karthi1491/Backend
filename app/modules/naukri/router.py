from fastapi import APIRouter

from app.modules.naukri.service import naukri_service


router = APIRouter(
    prefix="/naukri",
    tags=["Naukri"],
)


@router.post("/connect")
async def connect_naukri():
    return await naukri_service.connect()


@router.get("/status")
async def connection_status():
    return await naukri_service.get_status()


@router.post("/disconnect")
async def disconnect_naukri():
    return await naukri_service.disconnect()