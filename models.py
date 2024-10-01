from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255), unique=True, nullable=False)
    password = mapped_column(String(255), nullable=False)    
    nickname = mapped_column(String(255), unique=True, nullable=False)
    plans = relationship("Plan", back_populates="owner", cascade='delete')
    is_active = mapped_column(Boolean,default=True)


class Plan(Base):
    __tablename__ = "plans"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(255), nullable=False)
    content = mapped_column(Text)
    goal = mapped_column(Text)
    nuri = mapped_column(Text)
    topic = mapped_column(String(100))
    activity = mapped_column(String(100))
    create_date = mapped_column(DateTime, nullable=False)
    modify_date = mapped_column(DateTime, nullable=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="plans")