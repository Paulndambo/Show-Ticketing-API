# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowTicketing.settings")

app = Celery("ShowTicketing", broker=settings.BROKER_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "run-every-5-seconds": {"task": "hello_world", "schedule": 5},
    "run-every-7-seconds": {"task": "check_celery_task", "schedule": 7},
    # "run-every-60-seconds": {"task": "check_if_celery_works", "schedule": 60},
    # "run-every-2-minutes": {"task": "event_space_booked_task", "schedule": 120},
    # "run-every-1-minute": {"task": "account_activation_task", "schedule": 60},
    # "run-every-3-minutes": {"task": "hotel_room_booked_task", "schedule": 150},
    # "run-every-45-seconds": {"task": "ticket_purchased_task", "schedule": 45},
    # "run-every-20-seconds": {"task": "payment_received_task", "schedule": 20},
}