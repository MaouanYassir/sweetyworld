from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def send_invoice_email(order):
    subject = f"Votre facture pour la commande {order.id}"
    message = "Voici votre facture en pièce jointe."

    email = EmailMessage(subject, message, 'noreply@sweetyworld.com', [order.user.email])

    # Générer le PDF de la facture
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Facture #{order.id}")
    # Ajoute plus de contenu ici, comme montré précédemment...
    p.showPage()
    p.save()

    # Ajouter le PDF en pièce jointe
    email.attach(f"facture_{order.id}.pdf", response.getvalue(), 'application/pdf')

    # Envoyer l'email
    email.send()
