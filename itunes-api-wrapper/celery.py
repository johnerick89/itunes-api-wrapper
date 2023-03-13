import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itunes-api-wrapper.settings")
app = Celery("itunes-api-wrapper")
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from music.tasks import seed_music_data_task
app.task(seed_music_data_task)