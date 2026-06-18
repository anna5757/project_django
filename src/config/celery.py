import os

from celery import Celery
from celery.schedules import crontab
from celery.schedules import solar

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings',
                       namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-220-seconds': {
        'task': 'task_manager.tasks.add',
        'schedule': 220,
        'args': (16, 16)
    },
    'add-only-3-times': {
        'task': 'task_manager.tasks.mul',
        'schedule': crontab(minute=0, hour=19-21),
        'args': (5, 3)
    },
    'morning-sunrise-notification': {
        'task': 'task_manager.morning_notification',
        'schedule': solar(
            'sunrise',
            53.9006,
            27.5590
        ),
    },

}
# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')