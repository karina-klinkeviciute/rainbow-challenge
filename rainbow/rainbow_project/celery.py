import os
from datetime import timedelta

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rainbow_project.settings')

app = Celery('rainbow_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print("something")


app.conf.beat_schedule = {
    'streaks-and-medals-calculation': {
        'task': 'calculate_streaks',
        'schedule': crontab(hour=5, minute=0, day_of_week=1),
    },
    'test-task': {
        'task': 'test_task',
        'schedule': timedelta(minutes=10),
    }
}


# running celery:
# celery -A project worker -B --detach -f celery.log --loglevel=DEBUG
