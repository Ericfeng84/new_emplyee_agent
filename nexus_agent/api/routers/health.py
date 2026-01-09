from fastapi import APIRouter
from nexus_agent.api.schemas.common import HealthCheckResponse

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return {"status": "ok", "version": "0.5.0"}
