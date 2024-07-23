# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from ShowTicketing.celery import app

from apps.core.publisher import BasePublisher
from apps.reservations.models import Reservation, MovieTicket

date_today = datetime.now().date()



@app.task(name="hello_world")
def hello_world():
    publisher = BasePublisher(
        routing_key="hello_world",
        body={
            "message": "Hello World!!"
        }
    )
    publisher.run()
    print("Hello World, am running using celery")


@app.task(name="check_celery_task")
def check_celery_task():
    print("************************Metropolitan*********************")
    print("It looks like celery is working fine")
    print("************************Metropolitan*********************")

@app.task(name="ticket_purchased_notification")
def ticket_purchased_notification():
    tickets = MovieTicket.objects.filter(notification_send=False)
    for ticket in tickets:
        publisher = BasePublisher(
            routing_key="ticket_purchased",
            body={
                "ticket_id": ticket.id
            }
        )
        publisher.run()
        ticket.notification_send = True
        ticket.save()