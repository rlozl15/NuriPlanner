from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from domain.recplan import elastic_plan_crud, elastic_plan_schema

router = APIRouter(
    prefix="/api/recplan",
)

@router.get("/{plan_id}/list", response_model=elastic_plan_schema.RecPlanList)
def recplan_list(plan_id: int):
    recplan_list = elastic_plan_crud.get_recplan_list(plan_id)
    return {"rec_plan_list":recplan_list}
