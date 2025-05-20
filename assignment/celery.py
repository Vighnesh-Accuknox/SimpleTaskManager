from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment.settings')

app = Celery('assignment')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-db-every-minute': {
        'task': 'project.tasks.send_upcoming_deadline_reminders', 
        'schedule': crontab(minute='*/1'),  #for 
    },
}