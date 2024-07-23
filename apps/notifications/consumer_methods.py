import json
from datetime import timedelta

from apps.notifications.mixins import SendMessage
from apps.reservations.models import MovieTicket
from apps.core.document_generator import DocumentGenerator

document_generator = DocumentGenerator()

class NotificationConsumer:
    body = None

    @classmethod
    def ticket_purchased(cls):
        """
        When a customer reserves a seat, they should receive an email notification
        """
        try:
            data = json.loads(cls.body)
            ticket = MovieTicket.objects.get(id=data["ticket_id"])
            reservations = ticket.ticketreservations.all()
            context_data = {
                "name": f"{ticket.user.first_name} {ticket.user.last_name}",
                "show_title": ticket.show.title,
                "show_date": str(ticket.show.show_date),
                "show_time": str(ticket.show.show_time),
                "subject": "Seat Reserved",
                "action_type": "Ticket Purchased!",
                "reservations": reservations,
            }
            send_message = SendMessage()
            ticket_pdf = document_generator.generate_pdf_ticket(ticket, "documents/ticket.html")
            attachments = [
                {
                    'name': 'Movie Ticket.pdf',
                    'main_file': ticket_pdf,
                    'media_type': 'application/pdf'
                },
            ]
            context_data["attached_files"] = attachments
            send_message.send_mail(
                context_data,
                [
                    ticket.user.email,
                ],
                template="seat_reserved",
            )
        except Exception as e:
            raise e
        print("Task was reached!!!")


    @classmethod
    def ticket_cancelled(cls):
        try:
            data = json.loads(cls.body)
            ticket = MovieTicket.objects.get(id=data["ticket_id"])
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

   