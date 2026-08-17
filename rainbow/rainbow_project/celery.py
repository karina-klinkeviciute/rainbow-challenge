import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rainbow_project.settings')

app = Celery('rainbow_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace="CELERY")
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
# Keep retrying the broker connection when the worker starts. This was the
# behaviour before Celery 6 and it is what we want on the server, where the
# worker may come up before redis does; Celery 5.3+ warns on every start unless
# the choice is stated explicitly.
app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django apps.
app.autodiscover_tasks()



# @app.task(bind=True)
# def debug_task(self):
#     print("something")


app.conf.beat_schedule = {
    'streaks-and-medals-calculation': {
        'task': 'results.tasks.calculate_streaks',
        'schedule': crontab(hour=5, minute=0, day_of_week=1),
    },
    'test-task': {
        'task': 'results.tasks.test_task',
        'schedule': crontab(minute=0, hour='12'),
    },
}


# running celery:
# celery -A rainbow_project worker -B --detach -f celery.log --loglevel=DEBUG
