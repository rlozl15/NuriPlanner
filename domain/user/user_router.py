from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt  # pip install "python-jose[cryptography]"
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_schema, user_crud
from domain.user.user_crud import pwd_context

from datetime import timedelta, datetime, timezone
from config import AccessTokenConfig as config

ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    name = user_crud.get_user(db, user_name = _user_create.username)
    if name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="username : 이미 존재하는 사용자입니다.")
    
    nickname = user_crud.get_user(db, nickname = _user_create.nickname)
    if nickname:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="nickname : 이미 존재하는 닉네임입니다.")

    user_crud.create_user(db, _user_create)


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    # 아이디 비번 확인
    user = user_crud.get_user(db, user_name=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 비밀번호가 틀렸습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # access token 생성
    data = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "nickname": user.nickname,
    }