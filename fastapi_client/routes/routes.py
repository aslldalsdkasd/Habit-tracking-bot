from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_client import APIRouter, Depends
from fastapi_client.database.conection import get_session, init_db
from fastapi_client.database.model import Habit, UserHabit
from fastapi_client.schema.habit import HabitCreate, HabitDelete, HabitUpdate

app = APIRouter()










