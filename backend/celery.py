from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PocketDoc.settings')

app = Celery('PocketDoc')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch_and_index_papers_daily': {
        'task': 'website.tasks.fetch_and_index_papers',
        'schedule': crontab(hour=0, minute=0) 
    },
}

