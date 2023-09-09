from os import environ

from celery.schedules import crontab

CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = environ.get('CELERY_RESULT_BACKEND')

CELERY_BEAT_SCHEDULE = {
    "populate_todays_rates_task": {
        "task": "main.tasks.populate_todays_rates_task",
        "schedule": crontab(hour="12", minute="0"),
        # "schedule": crontab(minute="*/1"),
    },
}
