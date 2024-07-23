# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from apps.notifications.mixins import SendMessage
from apps.reservations.models import Reservation, MovieTicket
from apps.ticketing.models import Show
from apps.users.models import User
from datetime import datetime

date_today = datetime.now().date()


@shared_task
def add(x, y):
    return x + y


@shared_task
def print_hello_world():
    print("Hello World, am running using celery")


