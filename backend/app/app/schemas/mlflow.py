from typing import Optional, List
from pydantic import BaseModel

# Note: not to confuse this module's Model with pydantic's Model naming

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

class RegisteredModel(BaseModel):
    latest_versions: List[ModelVersion]
    name: str
    tags: dict
    creation_timestamp: int
    last_updated_timestamp: int
    description: str

class DatapointToPredict(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float
