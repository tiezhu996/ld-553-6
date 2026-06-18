import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.config.settings")
app = Celery("transithub")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
