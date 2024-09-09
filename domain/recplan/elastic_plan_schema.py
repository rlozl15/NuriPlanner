from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

class RecPlan(BaseModel):
    id : int
    title : str
    content : str
    activity : str

class RecPlanList(BaseModel):
    rec_plan_list: list[RecPlan] = []