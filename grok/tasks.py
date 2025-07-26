# grok/tasks.py

import os
from celery import Celery
from .attendance_scraper import check_attendance_logic  # You must have this function inside your scraper file

CELERY_BROKER = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("tasks", broker=CELERY_BROKER)

@celery.task
def check_attendance(roll_number):
    return check_attendance_logic(roll_number)
