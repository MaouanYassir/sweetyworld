from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from shop.models import Order


def generate_invoice(request, order_id):
    # Récupérer l'objet commande par son ID
    order = get_object_or_404(Order, id=order_id)

    # Créer une réponse HTTP de type PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'

    # Créer le PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Dimensions de la page PDF (lettre est une taille standard)

    # Ajouter des informations à la facture
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 100, f"Facture #{order.id}")
    p.drawString(100, height - 120, f"Client: {order.user.email}")
    p.drawString(100, height - 140, f"Date de la commande: {order.order_date}")
    p.drawString(100, height - 160, f"Date de retrait: {order.pick_up_date}")
    p.drawString(100, height - 180, f"Montant total: {order.total_price}€")

    # Détails des produits dans la commande
    y_position = height - 200
    for item in order.order_items.all():
        p.drawString(100, y_position, f"{item.product.name} x {item.quantity} : {item.total_price_item}€")
        y_position -= 20

    # Sauvegarder le PDF et renvoyer la réponse
    p.showPage()
    p.save()

    return response
