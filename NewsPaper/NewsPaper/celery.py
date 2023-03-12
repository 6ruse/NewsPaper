import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'weekly_posts': {
        'task': 'news.tasks.weekly_posts',
        'schedule': 20,
    },
}

app.autodiscover_tasks()