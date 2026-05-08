from celery import Celery
from celery.schedules import crontab

celery_app = Celery("tasks", broker="redis://redis:6379/0")

celery_app.conf.update(
    worker_pool='solo',
    imports=['celery_client.tasks'],
    loglevel='info'
)

celery_app.conf.beat_schedule = {
    "send-habit-reminder": {
        "task": "celery_client.tasks.check_habits",
        'schedule': crontab(hour=20, minute=0),
    }
}

if __name__ == '__main__':
    celery_app.start()
