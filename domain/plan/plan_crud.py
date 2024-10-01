from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models import Plan, User
from domain.plan.plan_schema import PlanCreate

from datetime import datetime


def get_plan_list(db: Session, skip: int = 0, limit: int = 10):
    _plan_list = db.query(Plan)\
        .order_by(Plan.create_date.desc())
    total = _plan_list.count()
    plan_list = _plan_list.offset(skip).limit(limit).all()
    return total, plan_list

def get_plan(db: Session, plan_id: int):
    plan = db.query(Plan).get(plan_id)
    return plan

def get_plan_id(db: Session):
    id = db.execute(
        select(func.max(Plan.id)).select_from(Plan).limit(1)
        ).scalars().first()
    return id

def create_plan(db: Session, plan_create: PlanCreate, user: User):
    db_plan = Plan(title = plan_create.title,
                   content = plan_create.content,
                   goal = plan_create.goal,
                   nuri = plan_create.nuri,
                   topic = plan_create.topic,
                   activity = plan_create.activity,
                   create_date = datetime.now(),
                   owner = user)
    db.add(db_plan)
    db.commit()
