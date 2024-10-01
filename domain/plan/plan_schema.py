from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

class PlanBase(BaseModel):
    title : str
    content : str
    goal : str
    nuri : str
    topic : str
    activity : str


class PlanCreate(PlanBase):
    
    @field_validator('title')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Plan(PlanBase):
    id : int
    owner_id  : int
    create_date : datetime

    model_config = ConfigDict(from_attributes=True)


class PlanList(BaseModel):
    total: int = 0
    plan_list: list[Plan] = []
