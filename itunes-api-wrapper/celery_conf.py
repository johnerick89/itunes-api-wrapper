import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itunes-api-wrapper.settings")
app = Celery("itunes-api-wrapper")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

