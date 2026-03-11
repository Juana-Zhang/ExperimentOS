from pydantic import BaseModel
from typing import Optional

class ExperimentBase(BaseModel):
    name: str
    hypothesis: str
    owner: str
    status: str = "Draft"
    sample_size: Optional[int] = 0
    conversion_rate: Optional[float] = 0.0
    p_value: Optional[float] = None
    is_significant: Optional[bool] = False

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int

    class Config:
        from_attributes = True