# from django.core.mail import EmailMessage
# from django.http import HttpResponse
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from decimal import Decimal
#
#
# def send_invoice_email(order):
#     # Calcul du prix HT (Hors Taxes) en retirant la TVA de 21%
#     tva_rate = Decimal('0.21')  # TVA à 21%
#     price_without_vat = order.total_price / (1 + tva_rate)  # Prix sans TVA
#     price_with_vat = order.total_price  # Prix avec TVA
#
#     subject = f"Votre facture pour la commande {order.id}"
#     message = "Voici votre facture en pièce jointe."
#
#     # Création de l'email
#     email = EmailMessage(
#         subject,
#         message,
#         'noreply@sweetyworld.com',  # Email de l'expéditeur
#         [order.user.email]  # Destinataire (email du client)
#     )
#
#     # Créer une réponse HTTP pour le PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
#     p = canvas.Canvas(response, pagesize=letter)
#     width, height = letter  # Taille de la page (Lettre)
#
#     # Titre et en-tête de la facture
#     p.setFont("Helvetica-Bold", 18)
#     p.drawString(200, height - 40, "SWEETYWORLD")
#
#     p.setFont("Helvetica", 12)
#     p.drawString(200, height - 60, "Adresse: 123 Rue des Gâteaux, Bruxelles")
#     p.drawString(200, height - 80, "Téléphone: +32 485 56 87 56")
#     p.drawString(200, height - 100, "Email: sweetyworld1180@gmail.com")
#
#     # Ligne de séparation
#     p.setLineWidth(0.5)
#     p.line(50, height - 120, width - 50, height - 120)
#
#     # Informations sur la facture
#     p.setFont("Helvetica", 12)
#     p.drawString(100, height - 140, f"Facture #{order.id}")
#     p.drawString(100, height - 160, f"Date de la commande: {order.order_date.strftime('%d/%m/%Y')}")
#
#     # Formater la date de retrait pour ne pas afficher l'heure
#     pick_up_date_str = order.pick_up_date.strftime('%d/%m/%Y')  # Format: jour/mois/année
#     p.drawString(100, height - 180, f"Date de retrait: {pick_up_date_str}")
#
#     p.drawString(100, height - 200, f"Client: {order.user.email}")
#     p.drawString(100, height - 220, f"Montant total (TTC): {price_with_vat}€")
#
#     # Ajouter le montant sans TVA
#     p.drawString(100, height - 240, f"Montant sans TVA (HT): {price_without_vat:.2f}€")
#
#     # Détails des articles de la commande
#     y_position = height - 260
#     p.setFont("Helvetica-Bold", 12)
#     p.drawString(100, y_position, "Description des produits :")
#     y_position -= 20
#     p.setFont("Helvetica", 10)
#
#     for item in order.order_items.all():
#         p.drawString(100, y_position, f"{item.product.name} x {item.quantity} : {item.total_price_item}€")
#         y_position -= 20
#
#     # Ligne de séparation avant le total
#     p.setLineWidth(0.5)
#     p.line(50, y_position, width - 50, y_position)
#     y_position -= 10
#
#     # Total
#     p.setFont("Helvetica-Bold", 12)
#     p.drawString(100, y_position, f"Total (TTC): {price_with_vat:.2f}€")
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
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from decimal import Decimal


def send_invoice_email(order):
    # Calcul du prix HT (Hors Taxes) en retirant la TVA de 21%
    tva_rate = Decimal('0.21')  # TVA à 21%
    price_without_vat = order.total_price / (1 + tva_rate)  # Prix sans TVA
    price_with_vat = order.total_price  # Prix avec TVA
    vat_amount = price_with_vat - price_without_vat  # Montant de la TVA

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

    # Afficher prix HT, TVA et prix TTC
    p.drawString(100, height - 220, f"Montant sans TVA (HT): {price_without_vat:.2f}€")
    p.drawString(100, height - 240, f"Montant TVA (21%): {vat_amount:.2f}€")
    p.drawString(100, height - 260, f"Montant total (TTC): {price_with_vat:.2f}€")

    # Détails des articles de la commande
    y_position = height - 280
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

    # Sauvegarder le PDF
    p.showPage()
    p.save()

    # Attacher le PDF à l'email
    email.attach(f"facture_{order.id}.pdf", response.getvalue(), 'application/pdf')

    # Envoyer l'email
    email.send()
