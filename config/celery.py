import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.conf.beat_schedule = {
    'check-overdue-every-day': {
        'task': 'apps.notifications.tasks.check_overdue_borrowings',
        'schedule': crontab(hour=0, minute=0),  # каждый день в полночь
    },
}
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()