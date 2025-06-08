#
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
#     vat_amount = price_with_vat - price_without_vat  # Montant de la TVA
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
#
#     # Afficher prix HT, TVA et prix TTC
#     p.drawString(100, height - 220, f"Montant sans TVA (HT): {price_without_vat:.2f}€")
#     p.drawString(100, height - 240, f"Montant TVA (21%): {vat_amount:.2f}€")
#     p.drawString(100, height - 260, f"Montant total (TTC): {price_with_vat:.2f}€")
#
#     # Détails des articles de la commande
#     y_position = height - 280
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
    # Calcul du prix HT et TVA
    tva_rate = Decimal('0.21')
    price_without_vat = order.total_price / (1 + tva_rate)
    price_with_vat = order.total_price
    vat_amount = price_with_vat - price_without_vat

    subject = f"Votre facture pour la commande n°{order.id}"

    # 💡 Logo hébergé sur ton site ou sur une URL externe
    logo_url = "https://sweetyworld.com/static/images/logoSweetyworld.png"  # remplace par ton vrai lien

    # Corps HTML de l'e-mail avec le logo
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ font-size: 18px; font-weight: bold; color: #D6336C; }}
        .details {{ margin-top: 10px; }}
        .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
      </style>
    </head>
    <body>
      <img src="{logo_url}" alt="SweetyWorld" width="150">

      <p class="header">Bonjour {order.user.email},</p>

      <p>Merci pour votre commande sur <strong>SweetyWorld</strong> !</p>
      <p>Vous trouverez ci-joint la facture pour votre commande n°{order.id}.</p>

      <div class="details">
        <p><strong>Date de commande :</strong> {order.order_date.strftime('%d/%m/%Y')}</p>
        <p><strong>Date de retrait prévue :</strong> {order.pick_up_date.strftime('%d/%m/%Y')}</p>
        <p><strong>Montant HT :</strong> {price_without_vat:.2f} €</p>
        <p><strong>TVA (21%) :</strong> {vat_amount:.2f} €</p>
        <p><strong>Total TTC :</strong> {price_with_vat:.2f} €</p>
      </div>

      <p class="footer">
        Cet email vous est envoyé automatiquement depuis l’adresse : sweetyworld1180@gmail.com.<br>
        Merci de votre confiance et à très bientôt !
      </p>
    </body>
    </html>
    """

    # Création de l'e-mail
    email = EmailMessage(
        subject,
        body=html_message,
        from_email='noreply@sweetyworld.com',
        to=[order.user.email]
    )
    email.content_subtype = 'html'  # Pour envoyer du HTML

    # Génération du PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, height - 40, "SWEETYWORLD")

    p.setFont("Helvetica", 12)
    p.drawString(200, height - 60, "Adresse: 123 Rue des Gâteaux, Bruxelles")
    p.drawString(200, height - 80, "Téléphone: +32 485 56 87 56")
    p.drawString(200, height - 100, "Email: sweetyworld1180@gmail.com")

    p.setLineWidth(0.5)
    p.line(50, height - 120, width - 50, height - 120)

    p.setFont("Helvetica", 12)
    p.drawString(100, height - 140, f"Facture #{order.id}")
    p.drawString(100, height - 160, f"Date de la commande: {order.order_date.strftime('%d/%m/%Y')}")
    p.drawString(100, height - 180, f"Date de retrait: {order.pick_up_date.strftime('%d/%m/%Y')}")
    p.drawString(100, height - 200, f"Client: {order.user.email}")
    p.drawString(100, height - 220, f"Montant sans TVA (HT): {price_without_vat:.2f}€")
    p.drawString(100, height - 240, f"Montant TVA (21%): {vat_amount:.2f}€")
    p.drawString(100, height - 260, f"Montant total (TTC): {price_with_vat:.2f}€")

    y_position = height - 280
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, "Description des produits :")
    y_position -= 20
    p.setFont("Helvetica", 10)

    for item in order.order_items.all():
        p.drawString(100, y_position, f"{item.product.name} x {item.quantity} : {item.total_price_item:.2f}€")
        y_position -= 20

    p.setLineWidth(0.5)
    p.line(50, y_position, width - 50, y_position)
    y_position -= 10

    p.showPage()
    p.save()

    # Attacher le PDF
    email.attach(f"facture_{order.id}.pdf", response.getvalue(), 'application/pdf')

    # Envoyer
    email.send()
