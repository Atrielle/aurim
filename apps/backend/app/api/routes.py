from datetime import datetime, timezone

from fastapi import APIRouter

from app.models.schemas import HealthResponse, PlatformContractResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="aurim-backend",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/platform-contract", response_model=PlatformContractResponse)
def platform_contract() -> PlatformContractResponse:
    return PlatformContractResponse(
        system_of_record="PostgreSQL",
        workspace_boundary="Every domain resource is scoped by workspace_id.",
        work_item_model="Calendar, kanban, WBS, and gantt project from one Work Item model.",
        storage_policy="File metadata is platform-owned; file body storage is provider-driven.",
    )

