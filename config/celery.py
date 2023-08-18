import os

from django.conf import settings

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker=settings.CELERY_BROKER_URL)

app.autodiscover_tasks()

# celery -config config worker -l info --pool=solo
