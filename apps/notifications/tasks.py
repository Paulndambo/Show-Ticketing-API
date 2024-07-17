# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from apps.notifications.mixins import SendMessage
from apps.reservations.models import Reservation
from apps.ticketing.models import Show
from apps.users.models import User

@shared_task
def add(x, y):
    return x + y

@shared_task
def print_hello_world():
    print("Hello World, am running using celery")

@shared_task
def seat_reservation_task(user_id, show_id, tickets: list):
    user = User.objects.get(id=user_id)
    show = Show.objects.get(id=show_id)
    print(user.email, f"{user.first_name} {user.last_name}", show.title, tickets)
    try:
        reservations = Reservation.objects.filter(id__in=tickets)
        context_data = {
            "name": f"{user.first_name} {user.last_name}",
            "show_title": show.title,
            "show_date": str(show.show_date),
            "show_time": str(show.show_time),
            "subject": "Seat Reserved",
            "action_type": "Ticket Purchased!",
            "reservations": reservations
        }
        send_message = SendMessage()
        send_message.send_mail(
            context_data,
            [
                user.email,
            ],
            template="seat_reserved",
        )
    except Exception as e:
        raise e
    print("Task was reached!!!")