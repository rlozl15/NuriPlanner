from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.plan import plan_schema, plan_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/plan",
)


@router.get("/list", response_model=plan_schema.PlanList)
def plan_list(db: Session = Depends(get_db),
              page: int = 0, size: int = 10,
              keyword: str = None):
    total, _plan_list = plan_crud.get_plan_list(
        db, page*size, size, keyword=keyword)
    return {'total': total,
            'plan_list': _plan_list}

@router.get("/detail/{plan_id}", response_model=plan_schema.Plan)
def plan_detail(plan_id: int, db: Session = Depends(get_db)):
    plan = plan_crud.get_plan(db, plan_id)
    return plan

@router.get("/max-id", response_model=int)
def plan_max_id(db: Session = Depends(get_db)):
    max_id = plan_crud.get_max_plan_id(db)
    return max_id

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def plan_create(_plan_create: plan_schema.PlanCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    plan_crud.create_plan(db, 
                          plan_create=_plan_create, 
                          user=current_user)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def plan_update(_plan_update: plan_schema.PlanUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_plan = plan_crud.get_plan(db, plan_id=_plan_update.plan_id)
    if db_plan is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_plan.owner.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    plan_crud.update_plan(db, db_plan, _plan_update)
    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def plan_delete(_plan_delete: plan_schema.PlanDelete, 
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_plan = plan_crud.get_plan(db, plan_id=_plan_delete.plan_id)
    if not db_plan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_plan.owner.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    plan_crud.delete_plan(db, db_plan)