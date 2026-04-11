from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    timestamp: datetime


class PlatformContractResponse(BaseModel):
    system_of_record: str
    workspace_boundary: str
    work_item_model: str
    storage_policy: str
