import os
from celery import Celery
from grok.attendance_scraper import check_attendance_logic

CELERY_BROKER = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("tasks", broker=CELERY_BROKER)

@celery.task
def check_attendance(user_data):
    return check_attendance_logic(user_data)
