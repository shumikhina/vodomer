from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ascuv_emulator.settings')

app = Celery('ascuv_emulator', broker='redis://redis_host:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'provider_creation_task': {
        'task': 'providers.tasks.provider_creation_task',
        'schedule': crontab(minute='*/10'),
    },
    'provider_values_creation_task': {
        'task': 'providers.tasks.provider_values_creation_task',
        'schedule': crontab(minute='*/1'),
    },
    'process_values_sending': {
        'task': 'providers.tasks.process_values_sending',
        'schedule': crontab(minute='*/1'),
    },
}

app.autodiscover_tasks()
