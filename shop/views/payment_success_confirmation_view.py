from django.shortcuts import render, get_object_or_404

from shop.models import Order


def payment_success_confirmation(request, order_id):
    # Récupérer l'objet Order basé sur l'ID
    order = get_object_or_404(Order, id=order_id)

    # Rendre le template avec l'objet order
    return render(request, 'shop/payment_success_confirmation.html', {'order': order})
