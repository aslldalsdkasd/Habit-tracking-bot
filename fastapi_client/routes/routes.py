from sqlalchemy import select, and_
from fastapi import HTTPException, Depends, APIRouter
from requests import Response
from fastapi import status
from sqlalchemy.orm import selectinload

from fastapi_client.database.conection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_client.database.model import Habit, UserHabit
from fastapi_client.schema.habit import HabitGet, HabitPost
from fastapi import Request

router = APIRouter()


@router.get("/get_habits/{user_id}")
async def get(user_id: int, db: AsyncSession = Depends(get_session)) -> dict:
    stmt = (
        select(UserHabit)
        .where(UserHabit.user_id == user_id)
        .options(selectinload(UserHabit.habits.and_(Habit.days < 21)))
    )
    res = await db.execute(stmt)
    habits = res.scalars().all()
    if habits:
        habit_data = []
        for user_habit in habits:
            habit_obj = user_habit.habits
            habit_data.append(
                {  # Добавляем в список
                    "habit_id": habit_obj.id,
                    "habit_name": habit_obj.habit_name,
                    "days": habit_obj.days,
                    "created_at": (
                        habit_obj.created_at.isoformat()
                        if habit_obj.created_at
                        else None
                    ),
                }
            )
        return {"habit_data": habit_data}

    else:
        raise HTTPException(status_code=404, detail="not_found")


@router.post("/create_habit/{user_id:int}/{habit_name:str}")
async def post(
    request: Request,
    user_id: int,
    habit_name: str,
    db: AsyncSession = Depends(get_session),
) -> HabitPost:
    habit_odj = Habit(habit_name=habit_name)
    db.add(habit_odj)
    await db.flush()
    create_user_habit = UserHabit(
        user_id=user_id,
        habit_id=habit_odj.id,
    )
    db.add(create_user_habit)
    await db.commit()
    return HabitPost(
        habit_id=habit_odj.id,
        created_at=habit_odj.created_at,
        habit_name=habit_odj.habit_name,
    )


@router.put(
    "/update_habit/{user_id}/{habit_id}/{habit_name}",
)
async def update(
    request: Request,
    user_id: int,
    habit_id: int,
    habit_name: str,
    db: AsyncSession = Depends(get_session),
) -> dict:

    stmt = select(UserHabit).where(
        and_(UserHabit.user_id == user_id, UserHabit.habit_id == habit_id)
    )
    exists_result = await db.execute(stmt)
    habit_exists = exists_result.scalar_one_or_none()

    if not habit_exists:
        raise HTTPException(status_code=404, detail="Habit not found for this user")

    stmt = select(Habit).where(Habit.id == habit_id)
    result = await db.execute(stmt)
    habit = result.scalar_one_or_none()
    if habit:
        habit.habit_name = habit_name
        await db.commit()
        await db.refresh(habit)

        return {"status": "ok", "message": "habit updated"}

    else:
        raise HTTPException(status_code=404, detail="not_found")


@router.delete("/delete_habit/{habit_id:int}/{user_id:int}")
async def delete(user_id: int, habit_id: int, db: AsyncSession = Depends(get_session)):
    stmt = select(UserHabit).where(
        and_(UserHabit.user_id == user_id, UserHabit.habit_id == habit_id)
    )
    result = await db.execute(stmt)
    user_habit = result.scalar_one_or_none()
    if user_habit:
        await db.delete(user_habit)
        await db.commit()
        return 204
    else:
        raise HTTPException(status_code=404, detail="not_found")

@router.post("/done_habit/{user_id}/{habit_id}")
async def done_habit(
        user_id: int,
        habit_id:int,
        db: AsyncSession = Depends(get_session),
):
    stmt = select(Habit).join(UserHabit).where(
        Habit.id == habit_id,
        UserHabit.user_id == user_id
    )
    result = await db.execute(stmt)
    habit = result.scalar_one_or_none()

    if not habit:
        raise HTTPException(status_code=404, detail="not_found")
    else:
        if habit.days < 21:
            habit.days += 1
            await db.commit()
            await db.refresh(habit)
            return {"status": 'ok',
                    "message": f'{habit.habit_name} \n days = {habit.days}'}
        else:
            return {
                "status": "completed",
                "message": " Привычка уже выполнена 21 день!",
            }

@router.get('/not_done/{user_id}/{habit_id}')
async def not_done(
        user_id:int,
        habit_id:int,
        db: AsyncSession = Depends(get_session),
):
    stmt = select(Habit).join(UserHabit).where(Habit.id == habit_id, UserHabit.user_id == user_id)
    result = await db.execute(stmt)
    habit = result.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="not_found")
    else:
        habit.days = 0
        await db.commit()
        await db.refresh(habit)
        return {
            'status':'ok',
            'user_id': user_id,
            'message':f'ID - {habit_id}\n Прогресс будет обнулен'
        }

