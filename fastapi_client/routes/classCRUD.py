from typing import List

from fastapi import HTTPException, Depends, APIRouter
from requests import Response

from fastapi_client.database.conection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_client.database.model import Habit, UserHabit
from fastapi_client.schema.habit import HabitGet, HabitPost
from fastapi import Request

router = APIRouter()


@router.get('/get_habits/<user_id:int>', response_model=List[HabitGet])
async def get(self,
              user_id: int,) -> List[HabitGet]:
    habits = UserHabit.objects.filter(user_id=user_id).select_related('habit')
    if habits:
        res = []
        for user_habit in habits:
            habit_obj = user_habit.habit
            res.append(HabitGet(
                created_at=habit_obj.created_at,
                habit_name=habit_obj.habit_name,
                habit_id=habit_obj.habit_id,
                days=habit_obj.days,
                ))
        return res


    else:
       raise HTTPException(status_code=404, detail='not_found')

@router.post('/create_habit/<user_id:int>/<habit_name:str>')
async def post(self,
               request: Request,
               user_id:int,
               habit_name:str,
               db: AsyncSession = Depends(get_session)) -> HabitPost:
    habit_odj = Habit.objects.create(
        habit_name=habit_name
    )
    db.add(habit_odj)
    create_user_habit = UserHabit.objects.create(
        user=user_id,
        habit_id=habit_odj.id,
    )
    db.add(create_user_habit)
    await db.commit()
    return HabitPost(
        habit_id=habit_odj.id,
        created_at=habit_odj.created_at,
        habit_name=habit_odj.habit_name,
    )

@router.put('/update_habit/<user_id:int>/<habit_id:int>/<habit_name:str>',)
async def update(self,
                request: Request,
                user_id:int,
                habit_id: int,
                 habit_name:str,
                db: AsyncSession = Depends(get_session)
                ) -> str:
    data = await request.json()
    exist = Habit.objects.filter(UserHabit.user_id == user_id, Habit.id == habit_id).exists()
    if exist:
        put = Habit.objects.update(
            'habit_name',
        ).where(Habit.id == habit_id).values(habit_name)
        db.add(put)
        await db.commit()
        return 'ok'
    else:
        raise HTTPException(status_code=404, detail='not_found')

@router.delete('/delete_habit/<habit_id:int>/<user_id:int>')
async def delete(self,
                 user_id:int,
                 habit_id:int,
                 db: AsyncSession = Depends(get_session)):
    habit = UserHabit.objects.filter(user_id=user_id).select_related('habit')
    if habit:
        habit.filter(habit.habit_id == habit_id).delete()
        db.add(habit)
        await db.commit()
        return 204
    else:
        raise HTTPException(status_code=404, detail='not_found')

