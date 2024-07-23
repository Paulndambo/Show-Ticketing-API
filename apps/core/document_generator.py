import weasyprint
from django.template.loader import render_to_string

class DocumentGenerator:
    def __init__(self):
        pass

    # Render the HTML template
    def generate_pdf_ticket(self, ticket, template):
        html_string = render_to_string(template, {
            'show_title': ticket.show.title,
            "show_date": str(ticket.show.show_date),
            "show_time": str(ticket.show.show_time),
            'name': f"{ticket.user.first_name} {ticket.user.last_name}",
            'email': ticket.user.email,
            'ticket_id': ticket.id,
            'reservations': ticket.ticketreservations.all() 
        })
        
        # Generate PDF
        pdf = weasyprint.HTML(string=html_string).write_pdf()

        return pdf