# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
from ShowTicketing.celery import app

from apps.notifications.mixins import SendMessage
from apps.core.publisher import BasePublisher
from apps.reservations.models import MovieTicket

date_today = datetime.now().date()


@app.task(name="check_celery_task")
def check_celery_task():
    print("************************Show Ticketing*********************")
    print("It looks like celery is working fine")
    print("************************Show Ticketing*********************")


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

@app.task(name="ticket_cancellation_task")
def ticket_cancellation_task(ticket_id):
    try:
        ticket = MovieTicket.objects.get(id=ticket_id)
        reservations = ticket.ticketreservations.all()
        context_data = {
            "name": f"{ticket.user.first_name} {ticket.user.last_name}",
            "show_title": ticket.show.title,
            "show_date": str(ticket.show.show_date),
            "show_time": str(ticket.show.show_time),
            "subject": "Reservations Cancelled",
            "action_type": "Ticket Cancelled",
            "reservations": reservations,
        }
        send_message = SendMessage()
        send_message.send_mail(
            context_data,
            [
                ticket.user.email,
            ],
            template="reservation_cancelled",
        )
    except Exception as e:
        raise e