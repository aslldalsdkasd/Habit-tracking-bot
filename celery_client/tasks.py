from .init_celery import celery_app
from vk.init_bot import vk
from fastapi_client.database.model import UserHabit
from celery_client.connect_db import SessionLocal
from sqlalchemy import select
import logging
from logging.config import dictConfig
from logger_conf import LOGGER
dictConfig(LOGGER)
logger = logging.getLogger(__name__)

def get_all_users():
    db = SessionLocal()
    try:
        stmt = select(UserHabit.user_id).distinct()
        users = db.execute(stmt).scalars().all()
        print(users)
        return users
    finally:
        db.close()


@celery_app.task
def check_habits():
    db = SessionLocal()

    try:
        all_users = get_all_users()
        if not all_users:

            logger.info('Нет пользователей')
            return 'Нет пользователей'

        for user in all_users:
            try:
                if not user:
                    continue

                vk.messages.send(
                    user_id=user,
                    message="Не забудьте указать результаты сегодняшнего дня",
                    random_id=0,
                )

            except Exception as e:
                logger.error(f"Ошибка отправки {user}: {e}")
                continue

    except Exception as e:
        return f"Ошибка: {e}"

    finally:
        db.close()
