from pydantic import BaseModel, field_validator

class RecPlanBase(BaseModel):
    id : int
    title : str
    content : str
    activity : str

class RecPlanCreate(RecPlanBase):
    goal : str
    
    @field_validator('title')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class RecPlanList(BaseModel):
    rec_plan_list: list[RecPlanBase] = []

class RecPlanUpdate(RecPlanBase):
    goal : str

class RecPlanDelete(BaseModel):
    plan_id : int