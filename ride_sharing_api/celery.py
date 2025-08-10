# ride_sharing_api/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ride_sharing_api.settings")

app = Celery("ride_sharing_api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "simulate-ride-movement-every-10-seconds": {
        "task": "ride_app.tasks.simulate_ride_movement",
        "schedule": 10.0,
    },
}
