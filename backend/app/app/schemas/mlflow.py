from typing import Optional
from pydantic import BaseModel


class EnetParam(BaseModel):
    alpha: float
    l1_ratio: float

class RunInfo(BaseModel):
    artifact_uri: str
    start_time: int
    end_time: Optional[int] = None
    run_id: str
    status: str
    user_id: str

class RunData(BaseModel):
    metrics: dict
    params: dict
    tags: dict

class Run(BaseModel):
    data: RunData
    info: RunInfo

class ModelCreateMeta(BaseModel):
    name: str

class ModelVersion(BaseModel):
    creation_timestamp: int
    last_updated_timestamp: int
    name: str
    current_stage: str
    description: str
    run_id: str
    run_link: str
    source: str
    status: str
    status_message: str
    tags: dict
    user_id: str
    version: str
