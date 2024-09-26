from pydantic import BaseModel

class RecPlan(BaseModel):
    id : int
    title : str
    content : str
    activity : str

class RecPlanList(BaseModel):
    rec_plan_list: list[RecPlan] = []