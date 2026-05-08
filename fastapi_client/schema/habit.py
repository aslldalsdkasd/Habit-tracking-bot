from datetime import datetime

from pydantic import BaseModel

class HabitGet(BaseModel):
    habit_id: int
    created_at: datetime
    habit_name: str
    days: int

class HabitPost(BaseModel):
    habit_id: int
    created_at: datetime
    habit_name: str