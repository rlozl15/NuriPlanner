from sqlalchemy.orm import Session
from sqlalchemy import select
from domain.user.user_schema import UserCreate
from models import User
from passlib.context import CryptContext

# 비밀번호 암호화
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username = user_create.username,
                   password = pwd_context.hash(user_create.password),
                   nickname = user_create.nickname)
    db.add(db_user)
    db.commit()

def get_user(db: Session, user_name: str = None, nickname: str = None):
    if user_name:
        user = db.execute(select(User).where(
            User.username == user_name
        ).limit(1)).scalars().first()
    elif nickname:
        user = db.execute(select(User).where(
            User.nickname == nickname
        ).limit(1)).scalars().first()
    else:
        return None
    return user