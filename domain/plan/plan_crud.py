from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update, func, and_
from models import Plan, User
from domain.plan.plan_schema import PlanCreate, PlanUpdate

from datetime import datetime


def get_plan_list(db: Session, skip: int = 0, limit: int = 10,
                  keyword: str = None):
    stmt = select(Plan)

    if keyword:
        keyword = f"%{keyword}%"
        stmt = (stmt
                .filter(
                    Plan.title.ilike(keyword) |
                    Plan.content.ilike(keyword) |
                    Plan.topic.ilike(keyword)
                ))
    
    total_stmt = select(func.count()).select_from(stmt.distinct())
    total = db.execute(total_stmt).scalar()

    plan_stmt = (stmt.order_by(Plan.create_date.desc())
                 .offset(skip).limit(limit))
    plan_list = db.execute(plan_stmt).scalars().all()
    
    return total, plan_list

def get_plan(db: Session, plan_id: int):
    stmt = select(Plan).where(Plan.id == plan_id)
    plan = db.execute(stmt).scalars().first()
    return plan

def get_max_plan_id(db: Session):
    stmt = select(func.max(Plan.id)).select_from(Plan).limit(1)
    id = db.execute(stmt).scalars().first()
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

def update_plan(db: Session, db_plan: Plan,
                plan_update: PlanUpdate):
    stmt = (
            update(Plan)
            .where(Plan.id == db_plan.id)
            .values(
                title = plan_update.title,
                content = plan_update.content,
                goal = plan_update.goal,
                nuri = plan_update.nuri,
                topic = plan_update.topic,
                activity = plan_update.activity,
                modify_date = datetime.now(),
            )
        )
    db.execute(stmt)
    db.commit()

def delete_plan(db: Session, db_plan: Plan):
    stmt = delete(Plan).where(Plan.id == db_plan.id)
    db.execute(stmt)
    db.commit()