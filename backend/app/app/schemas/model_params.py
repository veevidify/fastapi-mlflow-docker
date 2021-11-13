from typing import Optional
from pydantic import BaseModel


class EnetParam(BaseModel):
    alpha: float
    l1_ratio: float
