import os
from celery import Celery
from .attendance_scraper import get_attendance_data  # This is the correct function name

# Configure the broker URL (Redis in this case)
CELERY_BROKER = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery
celery = Celery("tasks", broker=CELERY_BROKER)

# Optional: Configure JSON serialization (recommended)
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json'
)

# Define the Celery task
@celery.task(name="check_attendance")
def check_attendance(username, password):
    return get_attendance_data(username, password)
