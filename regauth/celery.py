import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'startappmania.settings')

app = Celery('startappmania')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()