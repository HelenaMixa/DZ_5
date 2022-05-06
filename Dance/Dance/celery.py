import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dance.settings')

app = Celery('Dance')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-spam-every-60-minute': {
        'task': 'main.tasks.send_beat_email',
        'schedule': crontab(minute='*/60'),
    },
}
