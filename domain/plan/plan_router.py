from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.plan import plan_schema, plan_crud

router = APIRouter(
    prefix="/api/plan",
)


@router.get("/list", response_model=plan_schema.PlanList)
def plan_list(db: Session = Depends(get_db),
              page: int = 0, size: int = 10):
    total, _plan_list = plan_crud.get_plan_list(db, page*size, size)
    return {'total': total,
            'plan_list': _plan_list}

@router.get("/detail/{plan_id}", response_model=plan_schema.Plan)
def plan_detail(plan_id: int, db: Session = Depends(get_db)):
    plan = plan_crud.get_plan(db, plan_id)
    return plan

@router.get("/max-id", response_model=int)
def plan_max_id(db: Session = Depends(get_db)):
    max_id = plan_crud.get_plan_id(db)
    return max_id

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def plan_create(_plan_create: plan_schema.PlanCreate,
                  db: Session = Depends(get_db)):
    plan_crud.create_plan(db, plan_create=_plan_create)



# def plan_delete(plan_id: int, db: Session = Depends(get_db)):
#     plan = plan_crud.get_plan(db, plan_id)
#     if not plan:
#         raise HTTPException(status_code=404, detail="Plan not found")
    