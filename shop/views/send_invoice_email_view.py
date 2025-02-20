from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# def send_invoice_email(order):
#     subject = f"Votre facture pour la commande {order.id}"
#     message = "Voici votre facture en pièce jointe."
#
#     # Création de l'email
#     email = EmailMessage(
#         subject,
#         message,
#         'sweetyworld1180@gmail.com',  # Email de l'expéditeur
#         [order.user.email]  # Destinataire (email du client)
#     )
#
#     # Créer une réponse HTTP pour le PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
#     p = canvas.Canvas(response, pagesize=letter)
#     width, height = letter  # Taille de la page (Lettre)
#
#     # Ajouter des informations détaillées sur la facture
#     p.setFont("Helvetica", 12)
#     p.drawString(100, height - 100, f"Facture #{order.id}")
#     p.drawString(100, height - 120, f"Client: {order.user.email}")
#     p.drawString(100, height - 140, f"Date de la commande: {order.order_date}")
#
#     # Formater la date de retrait pour ne pas afficher l'heure
#     pick_up_date_str = order.pick_up_date.strftime('%d/%m/%Y')  # Format: jour/mois/année
#     p.drawString(100, height - 160, f"Date de retrait: {pick_up_date_str}")
#     p.drawString(100, height - 180, f"Montant total: {order.total_price}€")
#
#     # Détails des articles de la commande
#     y_position = height - 200
#     for item in order.order_items.all():
#         p.drawString(100, y_position, f"{item.product.name} x {item.quantity} : {item.total_price_item}€")
#         y_position -= 20
#
#     # Sauvegarder le PDF
#     p.showPage()
#     p.save()
#
#     # Attacher le PDF à l'email
#     email.attach(f"facture_{order.id}.pdf", response.getvalue(), 'application/pdf')
#
#     # Envoyer l'email
#     email.send()


def send_invoice_email(order):
    subject = f"Votre facture pour la commande {order.id}"
    message = "Voici votre facture en pièce jointe."

    # Création de l'email
    email = EmailMessage(
        subject,
        message,
        'noreply@sweetyworld.com',  # Email de l'expéditeur
        [order.user.email]  # Destinataire (email du client)
    )

    # Créer une réponse HTTP pour le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Taille de la page (Lettre)

    # Titre et en-tête de la facture
    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, height - 40, "SWEETYWORLD")

    p.setFont("Helvetica", 12)
    p.drawString(200, height - 60, "Adresse: 123 Rue des Gâteaux, Bruxelles")
    p.drawString(200, height - 80, "Téléphone: +32 485 56 87 56")
    p.drawString(200, height - 100, "Email: sweetyworld1180@gmail.com")

    # Ligne de séparation
    p.setLineWidth(0.5)
    p.line(50, height - 120, width - 50, height - 120)

    # Informations sur la facture
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 140, f"Facture #{order.id}")
    p.drawString(100, height - 160, f"Date de la commande: {order.order_date.strftime('%d/%m/%Y')}")

    # Formater la date de retrait pour ne pas afficher l'heure
    pick_up_date_str = order.pick_up_date.strftime('%d/%m/%Y')  # Format: jour/mois/année
    p.drawString(100, height - 180, f"Date de retrait: {pick_up_date_str}")

    p.drawString(100, height - 200, f"Client: {order.user.email}")
    p.drawString(100, height - 220, f"Montant total: {order.total_price}€")

    # Détails des articles de la commande
    y_position = height - 240
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, "Description des produits :")
    y_position -= 20
    p.setFont("Helvetica", 10)

    for item in order.order_items.all():
        p.drawString(100, y_position, f"{item.product.name} x {item.quantity} : {item.total_price_item}€")
        y_position -= 20

    # Ligne de séparation avant le total
    p.setLineWidth(0.5)
    p.line(50, y_position, width - 50, y_position)
    y_position -= 10

    # Total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, f"Total : {order.total_price}€")

    # Sauvegarder le PDF
    p.showPage()
    p.save()

    # Attacher le PDF à l'email
    email.attach(f"facture_{order.id}.pdf", response.getvalue(), 'application/pdf')

    # Envoyer l'email
    email.send()