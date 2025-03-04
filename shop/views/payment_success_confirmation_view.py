# from django.shortcuts import render, get_object_or_404
#
# from shop.models import Order
# from shop.views.send_invoice_email_view import send_invoice_email
#
#
# def payment_success_confirmation(request, order_id):
#     # Récupérer l'objet Order basé sur l'ID
#     order = get_object_or_404(Order, id=order_id)
#
#     if order.is_paid:
#         # Envoie la facture par email
#         send_invoice_email(order)
#
#     # Rendre le template avec l'objet order
#     return render(request, 'shop/payment_success_confirmation.html', {'order': order})


from django.shortcuts import render, get_object_or_404, redirect
from django.utils import translation  # Importer translation
from shop.models import Order
from shop.views.send_invoice_email_view import send_invoice_email

def payment_success_confirmation(request, order_id):
    # Récupérer l'objet Order basé sur l'ID
    order = get_object_or_404(Order, id=order_id)

    # Activer la langue de l'utilisateur
    user_language = request.LANGUAGE_CODE  # Récupère la langue actuelle de l'utilisateur
    translation.activate(user_language)  # Active la langue dans la session

    if order.is_paid:
        # Envoie la facture par email
        send_invoice_email(order)

    # Rendre le template avec l'objet order
    return render(request, 'shop/payment_success_confirmation.html', {'order': order})

