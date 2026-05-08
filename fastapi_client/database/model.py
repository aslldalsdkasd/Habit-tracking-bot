import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, func, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    habit_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now)
    days = Column(Integer, default=0)
    habit = relationship('UserHabit', back_populates="habits")


class UserHabit(Base):
    __tablename__ = "user_habits"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    habit = relationship("Habit", back_populates="user_habits")